"""Python import-graph architecture fitness checks."""

from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .io import load_policy, print_line, safe_path, write_findings
from .model import ConfigurationError, Finding


@dataclass(frozen=True, slots=True)
class ImportEdge:
    """One statically recoverable import edge."""

    target: str
    line: int
    kind: str


def _module_name(source_root: Path, package: str, path: Path) -> str:
    relative = path.relative_to(source_root).with_suffix("")
    parts = [package, *relative.parts]
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _layer_for(module: str, levels: dict[str, int]) -> int | None:
    matches = [prefix for prefix in levels if module == prefix or module.startswith(f"{prefix}.")]
    return levels[max(matches, key=len)] if matches else None


def _module_package(module: str, *, is_init: bool) -> list[str]:
    parts = module.split(".")
    return parts if is_init else parts[:-1]


def _relative_base(module: str, node: ast.ImportFrom, *, is_init: bool) -> str:
    if node.level == 0:
        return node.module or ""
    package_parts = _module_package(module, is_init=is_init)
    remove = node.level - 1
    if remove > len(package_parts):
        return ""
    base = package_parts[: len(package_parts) - remove]
    if node.module:
        base.extend(node.module.split("."))
    return ".".join(base)


def _known_target(candidate: str, known: set[str]) -> bool:
    return candidate in known or any(name.startswith(f"{candidate}.") for name in known)


def _literal_dynamic_import(node: ast.Call) -> str | None:
    if (
        not node.args
        or not isinstance(node.args[0], ast.Constant)
        or not isinstance(node.args[0].value, str)
    ):
        return None
    function = node.func
    if isinstance(function, ast.Name) and function.id in {"__import__", "import_module"}:
        return node.args[0].value
    if isinstance(function, ast.Attribute) and function.attr == "import_module":
        return node.args[0].value
    return None


def _imports(tree: ast.AST, module: str, *, is_init: bool, known: set[str]) -> list[ImportEdge]:
    edges: list[ImportEdge] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            edges.extend(ImportEdge(alias.name, node.lineno, "import") for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _relative_base(module, node, is_init=is_init)
            if base:
                edges.append(ImportEdge(base, node.lineno, "from-base"))
            for alias in node.names:
                if alias.name == "*":
                    continue
                candidate = f"{base}.{alias.name}" if base else alias.name
                if _known_target(candidate, known):
                    edges.append(ImportEdge(candidate, node.lineno, "from-member"))
        elif isinstance(node, ast.Call):
            target = _literal_dynamic_import(node)
            if target:
                edges.append(ImportEdge(target, node.lineno, "dynamic-literal"))
    return edges


def _strong_components(graph: dict[str, set[str]]) -> list[set[str]]:  # noqa: C901
    """Tarjan SCC; its state transitions are kept together for auditability."""
    index = 0
    stack: list[str] = []
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    active: set[str] = set()
    components: list[set[str]] = []

    def connect(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        active.add(node)
        for target in graph.get(node, set()):
            if target not in graph:
                continue
            if target not in indices:
                connect(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in active:
                lowlinks[node] = min(lowlinks[node], indices[target])
        if lowlinks[node] != indices[node]:
            return
        component: set[str] = set()
        while stack:
            member = stack.pop()
            active.remove(member)
            component.add(member)
            if member == node:
                break
        components.append(component)

    for node in sorted(graph):
        if node not in indices:
            connect(node)
    return components


def _policy(root: Path) -> tuple[str, Path, dict[str, int], bool]:
    policy = load_policy(root)
    project = policy.get("project")
    raw_levels = policy.get("architecture")
    options = policy.get("architecture_options", {})
    if not isinstance(project, dict) or not isinstance(project.get("package"), str):
        raise ConfigurationError("policy project.package must be a string")
    if not isinstance(project.get("source_root"), str):
        raise ConfigurationError("policy project.source_root must be a string")
    if not isinstance(raw_levels, dict) or not raw_levels:
        raise ConfigurationError("policy architecture table must be nonempty")
    try:
        levels = {str(name): int(level) for name, level in raw_levels.items()}
    except (TypeError, ValueError) as error:
        raise ConfigurationError("architecture levels must be integers") from error
    if not isinstance(options, dict) or not isinstance(options.get("detect_cycles", True), bool):
        raise ConfigurationError("architecture_options.detect_cycles must be boolean")
    source_root = safe_path(root, project["source_root"], must_exist=True)
    return project["package"], source_root, levels, bool(options.get("detect_cycles", True))


def architecture_findings(root: Path) -> list[Finding]:
    """Return reverse-dependency, syntax, configuration, and cycle findings."""
    package, source_root, levels, detect_cycles = _policy(root)
    paths = sorted(source_root.rglob("*.py"))
    modules = {_module_name(source_root, package, path): path for path in paths}
    governed = {name for name in modules if _layer_for(name, levels) is not None}
    findings: list[Finding] = []
    if not governed:
        return [
            Finding(
                "error",
                "architecture.zero-governed-modules",
                str(source_root.relative_to(root)),
                "architecture policy matches no Python modules; "
                "check package/source_root/layer prefixes",
            )
        ]
    known = set(modules)
    graph: dict[str, set[str]] = defaultdict(set)
    for module, path in sorted(modules.items()):
        relative = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except (OSError, UnicodeError, SyntaxError) as error:
            findings.append(Finding("error", "architecture.syntax", relative, str(error)))
            continue
        source_layer = _layer_for(module, levels)
        for edge in _imports(tree, module, is_init=path.name == "__init__.py", known=known):
            internal_targets = [
                name for name in known if name == edge.target or name.startswith(f"{edge.target}.")
            ]
            target = (
                edge.target
                if edge.target in known
                else (min(internal_targets, key=len) if internal_targets else edge.target)
            )
            if target in known:
                graph[module].add(target)
            target_layer = _layer_for(edge.target, levels)
            if (
                source_layer is not None
                and target_layer is not None
                and target_layer > source_layer
            ):
                findings.append(
                    Finding(
                        "error",
                        "architecture.outward-import",
                        f"{relative}:{edge.line}",
                        f"{module} (layer {source_layer}) imports outward {edge.target} "
                        f"(layer {target_layer}) via {edge.kind}",
                    )
                )
    if detect_cycles:
        for component in _strong_components(graph):
            cyclic = len(component) > 1 or any(node in graph.get(node, set()) for node in component)
            if cyclic:
                cycle = " -> ".join(sorted(component))
                findings.append(
                    Finding("error", "architecture.cycle", cycle, "internal import cycle detected")
                )
    return findings


def command_architecture(root: Path, *, strict: bool) -> int:
    """Run the declared architecture checks and write inspectable evidence."""
    findings = architecture_findings(root)
    output = write_findings(
        root,
        "architecture-audit",
        findings,
        metadata={
            "relative_imports": "resolved using current module and ImportFrom.level",
            "type_and_conditional_imports": "enforced identically to runtime imports",
            "dynamic_imports": (
                "literal importlib.import_module/import_module/__import__ calls enforced"
            ),
        },
    )
    for item in findings:
        print_line(f"{item.severity.upper():7} {item.code:32} {item.path}: {item.message}")
    if not findings:
        print_line("No findings.")
    print_line(f"Evidence: {output.relative_to(root)}")
    return int(strict and any(item.severity == "error" for item in findings))
