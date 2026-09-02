"""Scientific-layout and static-input provenance checks."""

from __future__ import annotations

import ast
import hashlib
import os
import re
import shutil
import subprocess  # nosec B404
from pathlib import Path, PurePosixPath
from typing import Any

from .io import load_policy, load_toml, print_line, safe_path, write_findings
from .model import ConfigurationError, Finding

MANIFEST = "static/manifest.toml"
STATIC_EXEMPT = frozenset({"static/README.md", MANIFEST})
REQUIRED_PATHS = (
    ".gitignore",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/pull_request_template.md",
    ".env.example",
    ".envrc",
    "notebooks/README.md",
    "results/README.md",
    "results/.gitignore",
    "results/reference/README.md",
    "scripts/README.md",
    "static/README.md",
    MANIFEST,
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")
WORKSPACE_MODULES = frozenset({"notebooks", "results", "scripts", "static"})


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _manifest_path(raw: object, index: int) -> str:
    field = f"files[{index}].path"
    if not isinstance(raw, str) or not raw:
        raise ConfigurationError(f"{field} must be a nonempty string")
    if "\\" in raw:
        raise ConfigurationError(f"{field} must use '/' separators")
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or not raw.startswith("static/"):
        raise ConfigurationError(f"{field} must be a contained path below static/")
    normalized = path.as_posix()
    if normalized in STATIC_EXEMPT:
        raise ConfigurationError(f"{field} cannot register a control file")
    return normalized


def _required_text(entry: dict[str, Any], field: str, index: int) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"files[{index}].{field} must be a nonempty string")
    return value.strip()


def _tracked_secret_paths(root: Path) -> list[str]:
    """Return tracked dotenv paths without reading their contents."""
    git = shutil.which("git")
    if git is None:
        return []
    try:
        completed = subprocess.run(  # noqa: S603  # nosec B603
            [git, "ls-files", "-z"],
            cwd=root,
            check=False,
            capture_output=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if completed.returncode != 0:
        return []
    paths = completed.stdout.decode("utf-8", errors="surrogateescape").split("\0")
    return sorted(
        path
        for path in paths
        if path
        and (Path(path).name == ".env" or Path(path).name.startswith(".env."))
        and Path(path).name != ".env.example"
    )


def _static_paths(root: Path) -> tuple[set[str], list[Finding]]:
    static_root = safe_path(root, "static", must_exist=True)
    paths: set[str] = set()
    findings: list[Finding] = []
    for current, directories, filenames in os.walk(static_root, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for name in directories:
            candidate = current_path / name
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink():
                findings.append(
                    Finding("error", "science.static-symlink", relative, "symlinks are not allowed")
                )
            else:
                retained.append(name)
        directories[:] = retained
        for name in filenames:
            candidate = current_path / name
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink():
                findings.append(
                    Finding("error", "science.static-symlink", relative, "symlinks are not allowed")
                )
            elif candidate.is_file() and relative not in STATIC_EXEMPT:
                paths.add(relative)
    return paths, findings


def _ignore_findings(root: Path) -> list[Finding]:
    try:
        root_ignore = (root / ".gitignore").read_text(encoding="utf-8")
        results_ignore = (root / "results/.gitignore").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ConfigurationError(f"cannot read scientific ignore policy: {error}") from error
    ignore_lines = {
        line.strip()
        for line in root_ignore.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    required = (".env", ".env.*", "!.env.example", ".direnv/", ".ipynb_checkpoints/")
    findings = [
        Finding(
            "error",
            "science.secret-ignore",
            ".gitignore",
            f"required pattern is absent: {pattern}",
        )
        for pattern in required
        if pattern not in ignore_lines
    ]
    findings.extend(
        Finding(
            "error",
            "science.tracked-secret",
            path,
            "tracked dotenv file may contain credentials; keep only .env.example",
        )
        for path in _tracked_secret_paths(root)
    )
    results_lines = {
        line.strip()
        for line in results_ignore.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    results_required = ("*", "!.gitignore", "!README.md", "!reference/", "!reference/**")
    findings.extend(
        Finding(
            "error",
            "science.results-ignore",
            "results/.gitignore",
            f"required pattern is absent: {pattern}",
        )
        for pattern in results_required
        if pattern not in results_lines
    )
    return findings


def _manifest_findings(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    payload = load_toml(safe_path(root, MANIFEST, must_exist=True))
    if payload.get("schema_version") != 1:
        raise ConfigurationError("static manifest schema_version must equal 1")
    entries = payload.get("files")
    if not isinstance(entries, list):
        raise ConfigurationError("static manifest files must be an array")

    registered: set[str] = set()
    for index, raw_entry in enumerate(entries):
        if not isinstance(raw_entry, dict):
            raise ConfigurationError(f"files[{index}] must be a table")
        path_text = _manifest_path(raw_entry.get("path"), index)
        if path_text in registered:
            findings.append(
                Finding(
                    "error",
                    "science.static-duplicate",
                    MANIFEST,
                    f"duplicate entry: {path_text}",
                )
            )
            continue
        registered.add(path_text)
        expected_hash = _required_text(raw_entry, "sha256", index).lower()
        _required_text(raw_entry, "source", index)
        _required_text(raw_entry, "license", index)
        _required_text(raw_entry, "description", index)
        if not SHA256_RE.fullmatch(expected_hash):
            raise ConfigurationError(f"files[{index}].sha256 must be 64 lowercase hex characters")
        try:
            path = safe_path(root, path_text, must_exist=True)
        except ConfigurationError as error:
            findings.append(Finding("error", "science.static-path", path_text, str(error)))
            continue
        if not path.is_file():
            findings.append(
                Finding("error", "science.static-path", path_text, "manifest target is not a file")
            )
            continue
        actual_hash = _sha256(path)
        if actual_hash != expected_hash:
            findings.append(
                Finding(
                    "error",
                    "science.static-hash",
                    path_text,
                    f"expected {expected_hash}, observed {actual_hash}",
                )
            )

    actual, path_findings = _static_paths(root)
    findings.extend(path_findings)
    findings.extend(
        Finding(
            "error",
            "science.static-unregistered",
            path,
            f"add a complete entry to {MANIFEST}",
        )
        for path in sorted(actual - registered)
    )
    findings.extend(
        Finding(
            "error",
            "science.static-missing",
            path,
            "manifest entry has no regular file",
        )
        for path in sorted(registered - actual)
        if (root / path).exists()
    )
    return findings


def _workspace_import_findings(root: Path) -> list[Finding]:
    project = load_policy(root).get("project")
    if not isinstance(project, dict) or not isinstance(project.get("source_root"), str):
        raise ConfigurationError("policy project.source_root must be a string")
    source_root = safe_path(root, project["source_root"], must_exist=True)
    findings: list[Finding] = []
    for path in sorted(source_root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            findings.append(
                Finding("error", "science.source-symlink", relative, "source cannot be a symlink")
            )
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except (OSError, UnicodeError, SyntaxError) as error:
            findings.append(Finding("error", "science.source-parse", relative, str(error)))
            continue
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.partition(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imported.add(node.module.partition(".")[0])
        findings.extend(
            Finding(
                "error",
                "science.workspace-import",
                relative,
                f"installed package imports root workspace module {name!r}",
            )
            for name in sorted(imported & WORKSPACE_MODULES)
        )
    return findings


def science_findings(root: Path) -> list[Finding]:
    """Validate scientific layout, secret-ignore, and static manifest contracts."""
    findings = [
        Finding("error", "science.missing-path", relative, "required scientific profile path")
        for relative in REQUIRED_PATHS
        if not (root / relative).is_file()
    ]
    if findings:
        return findings
    return [
        *_ignore_findings(root),
        *_manifest_findings(root),
        *_workspace_import_findings(root),
    ]


def command_science(root: Path, *, strict: bool) -> int:
    """Run the scientific-profile audit and emit stable evidence."""
    findings = science_findings(root)
    output = write_findings(root, "science-audit", findings)
    if not findings:
        print_line("No findings.")
    for item in findings:
        print_line(f"{item.severity.upper():7} {item.code:34} {item.path}: {item.message}")
    print_line(f"Evidence: {output.relative_to(root)}")
    return int(strict and any(item.severity in {"error", "warning"} for item in findings))
