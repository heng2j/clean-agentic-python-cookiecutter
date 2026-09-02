"""Strict document lifecycle, link, anchor, and persistent-context audits."""

from __future__ import annotations

import datetime as dt
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

from .io import atomic_write_text, load_policy, print_line, safe_path, write_findings
from .model import ConfigurationError, Finding

WORD_RE = re.compile(r"\b[\w.-]+\b")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
BACKTICKED_MD_RE = re.compile(r"`([^`\n]+\.md(?:#[^`\n]+)?)`")
DYNAMIC_TEST_COUNT_RE = re.compile(r"\b\d+[,+]?\s+(?:passing\s+)?tests?\b", re.IGNORECASE)
ISSUE_URL_RE = re.compile(r"https?://[^\s)]+/issues?/\d+", re.IGNORECASE)
BROAD_CONTEXT_RE = re.compile(
    r"\b(?:read|review|inspect)\b.{0,45}\b(?:all|every|entire)\b.{0,45}"
    r"\b(?:files?|markdown|documents?|repository|repo)\b",
    re.IGNORECASE,
)
ALLOWED_STATUS = frozenset(
    {"normative", "reference", "draft", "generated", "historical", "superseded"}
)
MIN_DUPLICATE_LINE_LENGTH = 24


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _unique_mapping(loader: _UniqueKeyLoader, node: MappingNode, deep: bool = False) -> object:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise ConstructorError(
                "while constructing front matter",
                node.start_mark,
                "mapping keys must be scalar and hashable",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise ConstructorError(
                "while constructing front matter",
                node.start_mark,
                f"duplicate front-matter key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _unique_mapping,
)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse complete safe YAML front matter or raise a controlled error."""
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        return {}, text
    closing = normalized.find("\n---\n", 4)
    if closing < 0:
        raise ConfigurationError("front matter opens with --- but has no closing --- line")
    metadata_text = normalized[4:closing]
    body = normalized[closing + 5 :]
    try:
        # The loader subclasses SafeLoader and only adds duplicate-key rejection.
        loaded = yaml.load(metadata_text, Loader=_UniqueKeyLoader)  # nosec B506  # noqa: S506
    except yaml.YAMLError as error:
        raise ConfigurationError(f"invalid YAML front matter: {error}") from error
    if loaded is None:
        metadata: dict[str, Any] = {}
    elif not isinstance(loaded, dict):
        raise ConfigurationError("front matter must be a YAML mapping")
    else:
        if any(not isinstance(key, str) for key in loaded):
            raise ConfigurationError("front-matter keys must be strings")
        metadata = dict(loaded)
    verified = metadata.get("last_verified")
    if isinstance(verified, (dt.date, dt.datetime)):
        metadata["last_verified"] = verified.isoformat()
    return metadata, body


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def _slug(value: str) -> str:
    plain = re.sub(r"[`*_~]", "", value).strip().lower()
    plain = re.sub(r"[^\w\- ]", "", plain)
    return re.sub(r"[\s-]+", "-", plain).strip("-")


def _anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    for match in HEADING_RE.finditer(text):
        base = _slug(match.group(2))
        if not base:
            continue
        count = counts[base]
        anchor = base if count == 0 else f"{base}-{count}"
        counts[base] += 1
        anchors.add(anchor)
    return anchors


def _resolve_doc_target(root: Path, source: Path, raw_target: str) -> Path:
    candidate = source.parent / unquote(raw_target)
    root_real = root.resolve(strict=True)
    try:
        # Deliberately normalize lexical ``..`` without resolving symlinks yet.
        lexical = Path(os.path.abspath(candidate))  # noqa: PTH100
        relative = lexical.relative_to(root_real)
    except (FileNotFoundError, ValueError) as error:
        raise ConfigurationError(
            f"link target is absent or escapes repository: {raw_target}"
        ) from error
    current = root_real
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ConfigurationError(f"link target traverses symlink: {raw_target}")
    try:
        resolved = lexical.resolve(strict=True)
        resolved.relative_to(root_real)
    except (FileNotFoundError, ValueError) as error:
        raise ConfigurationError(
            f"link target is absent or escapes repository: {raw_target}"
        ) from error
    return resolved


def _link_findings(root: Path, path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = match.group(1).strip().strip("<>")
        if raw.startswith(("http://", "https://", "mailto:")):
            continue
        target_text, separator, anchor = raw.partition("#")
        target = path
        if target_text:
            try:
                target = _resolve_doc_target(root, path, target_text)
            except ConfigurationError as error:
                findings.append(
                    Finding(
                        "error",
                        "docs.dead-or-unsafe-link",
                        path.relative_to(root).as_posix(),
                        str(error),
                    )
                )
                continue
        if separator and anchor:
            try:
                target_text_content = target.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                findings.append(Finding("error", "docs.link-read", str(target), str(error)))
                continue
            if unquote(anchor).lower() not in _anchors(target_text_content):
                findings.append(
                    Finding(
                        "error",
                        "docs.dead-anchor",
                        path.relative_to(root).as_posix(),
                        f"anchor does not exist in {target.relative_to(root)}: #{anchor}",
                    )
                )
    return findings


def _date_findings(relative: str, raw: object, max_age_days: int) -> list[Finding]:
    if not isinstance(raw, str):
        return [
            Finding(
                "error", "docs.last-verified", relative, "last_verified must be an ISO date string"
            )
        ]
    try:
        verified = dt.date.fromisoformat(raw)
    except ValueError:
        return [Finding("error", "docs.last-verified", relative, f"invalid date: {raw!r}")]
    age = (dt.date.today() - verified).days
    if age < 0:
        return [
            Finding(
                "error",
                "docs.future-verification",
                relative,
                f"last_verified is in the future: {raw}",
            )
        ]
    if age > max_age_days:
        return [
            Finding(
                "error",
                "docs.verification-age",
                relative,
                f"last verified {age} days ago; revalidate or archive",
            )
        ]
    return []


def _metadata_findings(relative: str, metadata: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    status = metadata.get("status")
    if status not in ALLOWED_STATUS:
        findings.append(Finding("error", "docs.status", relative, f"invalid status: {status!r}"))
    findings.extend(
        Finding("error", f"docs.{field}", relative, f"missing or invalid {field}")
        for field in ("owner", "authority")
        if not isinstance(metadata.get(field), str) or not str(metadata[field]).strip()
    )
    applies = metadata.get("applies_to")
    if (
        not isinstance(applies, list)
        or not applies
        or any(not isinstance(item, str) or not item for item in applies)
    ):
        findings.append(
            Finding(
                "error",
                "docs.applies-to",
                relative,
                "applies_to must be a nonempty list of strings",
            )
        )
    return findings


def docs_findings(root: Path) -> list[Finding]:  # noqa: C901, PLR0912
    """Audit lifecycle schema, links, anchors, dates, and authority uniqueness."""
    policy = load_policy(root)
    project = policy.get("project")
    context = policy.get("context")
    if not isinstance(project, dict) or not isinstance(project.get("docs_root"), str):
        raise ConfigurationError("policy project.docs_root must be a string")
    if not isinstance(context, dict) or not isinstance(context.get("warn_doc_age_days"), int):
        raise ConfigurationError("policy context.warn_doc_age_days must be an integer")
    docs_root = safe_path(root, project["docs_root"], must_exist=True)
    paths = sorted(docs_root.rglob("*.md"))
    if not paths:
        return [
            Finding(
                "error", "docs.empty", str(docs_root.relative_to(root)), "docs root has no Markdown"
            )
        ]
    findings: list[Finding] = []
    authorities: defaultdict[str, list[str]] = defaultdict(list)
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            findings.append(
                Finding("error", "docs.symlink", relative, "document cannot be a symlink")
            )
            continue
        try:
            text = path.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(text)
        except (OSError, UnicodeError, ConfigurationError) as error:
            findings.append(Finding("error", "docs.frontmatter", relative, str(error)))
            continue
        if not metadata:
            findings.append(
                Finding("error", "docs.frontmatter", relative, "missing lifecycle front matter")
            )
            continue
        findings.extend(_metadata_findings(relative, metadata))
        findings.extend(
            _date_findings(relative, metadata.get("last_verified"), context["warn_doc_age_days"])
        )
        status = metadata.get("status")
        authority = metadata.get("authority")
        if status == "normative" and isinstance(authority, str):
            authorities[authority].append(relative)
        if status in {"historical", "superseded"} and not relative.startswith("docs/archive/"):
            findings.append(
                Finding(
                    "error",
                    "docs.archive-location",
                    relative,
                    f"{status} document must be under docs/archive/",
                )
            )
        if DYNAMIC_TEST_COUNT_RE.search(body):
            findings.append(
                Finding(
                    "error",
                    "docs.dynamic-test-count",
                    relative,
                    "volatile test count belongs in evidence",
                )
            )
        if status == "normative" and re.search(r"\b(?:TODO|FIXME|TBD)\b", body):
            findings.append(
                Finding(
                    "error",
                    "docs.unresolved-marker",
                    relative,
                    "normative document has unresolved marker",
                )
            )
        findings.extend(_link_findings(root, path, text))
    for authority, owners in sorted(authorities.items()):
        if len(owners) > 1:
            findings.append(
                Finding(
                    "error",
                    "docs.duplicate-authority",
                    ", ".join(owners),
                    f"authority {authority!r} is claimed by multiple documents",
                )
            )
    return findings


def _ignored_context(path: Path, root: Path) -> bool:
    return any(
        part in {".git", ".venv", "artifacts", "build", "dist"}
        for part in path.relative_to(root).parts
    )


def _context_files(root: Path) -> list[Path]:
    candidates = set(root.glob("**/AGENTS.md")) | set(root.glob("**/CLAUDE.md"))
    candidates |= set((root / ".claude" / "rules").glob("**/*.md"))
    return sorted(
        path for path in candidates if path.is_file() and not _ignored_context(path, root)
    )


def _normalized_lines(text: str) -> set[str]:
    values: set[str] = set()
    for line in text.splitlines():
        value = " ".join(line.strip().lower().split())
        if (
            value
            and not value.startswith(("#", "@", "---"))
            and len(value) > MIN_DUPLICATE_LINE_LENGTH
        ):
            values.add(value)
    return values


def _directive(value: str) -> tuple[str, str] | None:
    normalized = " ".join(value.strip().lower().lstrip("-0123456789. ").split()).rstrip(".")
    prefixes = (
        ("never ", "negative"),
        ("do not ", "negative"),
        ("must not ", "negative"),
        ("always ", "positive"),
        ("must ", "positive"),
    )
    for prefix, polarity in prefixes:
        if normalized.startswith(prefix):
            return polarity, normalized.removeprefix(prefix)
    return None


def _context_inventory(path: Path, root: Path, text: str) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    if path.name == "AGENTS.md":
        tool, source = "Codex-compatible agents", "AGENTS.md discovery by directory scope"
    elif path.name == "CLAUDE.md":
        tool, source = "Claude-compatible agents", "CLAUDE.md import and directory scope"
    else:
        tool, source = "Claude-compatible agents", ".claude/rules path-scoped loading"
    return {
        "path": relative,
        "tool": tool,
        "loading_source": source,
        "scope": path.parent.relative_to(root).as_posix() or ".",
        "precedence_depth": len(path.relative_to(root).parts),
        "owner": "repository maintainers",
        "authority": f"persistent-context:{relative}",
        "lines": len(text.splitlines()),
        "words": _word_count(text),
        "approximate_tokens": (len(text) + 3) // 4,
        "verification": "deterministic syntax/budget/reference heuristics only",
    }


def context_findings(  # noqa: C901, PLR0912, PLR0915
    root: Path,
) -> tuple[list[Finding], dict[str, Any]]:
    """Audit persistent context and return a loading-source inventory."""
    policy = load_policy(root).get("context")
    if not isinstance(policy, dict):
        raise ConfigurationError("policy context table is required")
    files = _context_files(root)
    texts: dict[Path, str] = {}
    findings: list[Finding] = []
    inventory: list[dict[str, Any]] = []
    directives: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(Finding("error", "context.read", relative, str(error)))
            continue
        texts[path] = text
        inventory.append(_context_inventory(path, root, text))
        lines = text.splitlines()
        words = _word_count(text)
        if path == root / "AGENTS.md":
            line_limit = int(policy["root_agents_max_lines"])
            if words > int(policy["root_agents_max_words"]):
                findings.append(
                    Finding(
                        "error", "context.word-budget", relative, f"{words} words exceeds budget"
                    )
                )
            required = policy.get("required_sections", [])
            if not isinstance(required, list):
                raise ConfigurationError("context.required_sections must be a list")
            findings.extend(
                Finding("error", "context.missing-section", relative, f"missing: {section}")
                for section in required
                if f"## {section}".lower() not in text.lower()
            )
        elif path == root / "CLAUDE.md":
            line_limit = int(policy["root_claude_max_lines"])
            if not text.lstrip().startswith("@AGENTS.md"):
                findings.append(
                    Finding(
                        "error", "context.claude-import", relative, "must begin with @AGENTS.md"
                    )
                )
        else:
            line_limit = int(policy["scoped_max_lines"])
        if len(lines) > line_limit:
            findings.append(
                Finding(
                    "error",
                    "context.line-budget",
                    relative,
                    f"{len(lines)} lines exceeds {line_limit}",
                )
            )
        if BROAD_CONTEXT_RE.search(text):
            findings.append(
                Finding("error", "context.low-precision", relative, "broad read-all instruction")
            )
        if DYNAMIC_TEST_COUNT_RE.search(text):
            findings.append(
                Finding("error", "context.dynamic-fact", relative, "volatile test count")
            )
        if ISSUE_URL_RE.search(text):
            findings.append(
                Finding("warning", "context.issue-history", relative, "distill issue history first")
            )
        for line in lines:
            directive = _directive(line)
            if directive:
                directives[directive[1]].append((directive[0], relative))
        for reference in BACKTICKED_MD_RE.findall(text):
            target_text = reference.split("#", 1)[0]
            try:
                safe_path(root, target_text, must_exist=True)
            except ConfigurationError as error:
                findings.append(
                    Finding("error", "context.dead-or-unsafe-reference", relative, str(error))
                )
    agents = _normalized_lines(texts.get(root / "AGENTS.md", ""))
    claude = _normalized_lines(texts.get(root / "CLAUDE.md", ""))
    duplicate = agents & claude
    if duplicate:
        findings.append(
            Finding(
                "error",
                "context.duplicate-authority",
                "CLAUDE.md",
                f"duplicates {len(duplicate)} instruction lines",
            )
        )
    for instruction, rows in directives.items():
        if {polarity for polarity, _path in rows} == {"positive", "negative"}:
            locations = ", ".join(sorted({path for _polarity, path in rows}))
            findings.append(
                Finding(
                    "error",
                    "context.contradiction",
                    locations,
                    f"contradictory directive: {instruction}",
                )
            )
    metrics: dict[str, Any] = {
        "context_files": len(inventory),
        "total_words": sum(item["words"] for item in inventory),
        "total_lines": sum(item["lines"] for item in inventory),
        "loading_source_inventory": inventory,
    }
    return findings, metrics


def command_docs(root: Path, *, strict: bool) -> int:
    """Run document lifecycle and link checks and write evidence."""
    findings = docs_findings(root)
    output = write_findings(root, "documentation-audit", findings)
    _show(findings, output, root)
    return int(strict and any(item.severity in {"error", "warning"} for item in findings))


def command_context(root: Path, *, strict: bool) -> int:
    """Run persistent-context checks and write the loading-source inventory."""
    findings, metrics = context_findings(root)
    output = write_findings(root, "context-audit", findings, metadata=metrics)
    _show(findings, output, root)
    return int(strict and any(item.severity in {"error", "warning"} for item in findings))


def _show(findings: list[Finding], output: Path, root: Path) -> None:
    if not findings:
        print_line("No findings.")
    for item in findings:
        print_line(f"{item.severity.upper():7} {item.code:34} {item.path}: {item.message}")
    print_line(f"Evidence: {output.relative_to(root)}")


def prune_plan(root: Path) -> str:
    """Return a non-destructive proposal covering every docs/context finding."""
    docs = docs_findings(root)
    context, _metrics = context_findings(root)
    candidates = [*docs, *context]
    lines = [
        "# Context and documentation pruning plan",
        "",
        "> Proposal only: this command never deletes, moves, or rewrites source files.",
        "",
        "## Candidates",
        "",
    ]
    if candidates:
        lines.extend(f"- **{item.path}** — `{item.code}`: {item.message}" for item in candidates)
    else:
        lines.append("No deterministic pruning candidates were found.")
    return "\n".join(lines) + "\n"


def command_prune(root: Path, output: Path) -> int:
    """Write a contained, non-destructive context pruning proposal."""
    target = output if output.is_absolute() else safe_path(root, output)
    try:
        target.resolve().relative_to(root.resolve(strict=True))
    except ValueError as error:
        raise ConfigurationError("prune-plan output must remain inside repository") from error
    atomic_write_text(target, prune_plan(root))
    print_line(target.relative_to(root))
    return 0
