"""Filesystem, command, evidence, and repository trust-boundary primitives."""

from __future__ import annotations

import datetime as dt
import glob
import json
import math
import os
import platform
import secrets
import shlex
import shutil
import subprocess  # nosec B404
import sys
import tempfile
import time
import tomllib
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path, PurePath
from typing import Any

from .model import CommandResult, ConfigurationError, Finding

IGNORED_PARTS = frozenset({".git", ".venv", "artifacts", "build", "dist", "__pycache__"})
PYTHON_MODULE_INVOCATION_PARTS = 3


def repository_root(start: Path | None = None) -> Path:
    """Return the nearest real ancestor containing the Clean AI policy."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".cleanai" / "policy.toml").is_file():
            return candidate
    raise ConfigurationError("could not find .cleanai/policy.toml in this directory or its parents")


def safe_path(
    root: Path,
    raw: str | Path,
    *,
    must_exist: bool = False,
    reject_symlinks: bool = True,
) -> Path:
    """Resolve a lexical relative path and prove it remains inside ``root``."""
    candidate_raw = Path(raw)
    if candidate_raw.is_absolute() or ".." in PurePath(candidate_raw).parts:
        raise ConfigurationError(f"path must be repository-relative without '..': {raw}")
    root_real = root.resolve(strict=True)
    candidate = root / candidate_raw
    if reject_symlinks:
        current = root
        for part in candidate_raw.parts:
            current /= part
            if current.is_symlink():
                raise ConfigurationError(f"symlink paths are not allowed: {raw}")
    try:
        resolved = candidate.resolve(strict=must_exist)
        resolved.relative_to(root_real)
    except (FileNotFoundError, ValueError) as error:
        qualifier = "existing " if must_exist else ""
        raise ConfigurationError(f"{qualifier}path escapes or is absent: {raw}") from error
    return resolved


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML object and convert parser errors to controlled failures."""
    try:
        with path.open("rb") as stream:
            value = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigurationError(f"cannot load TOML {path}: {error}") from error
    if not isinstance(value, dict):
        raise ConfigurationError(f"TOML root must be a table: {path}")
    return value


def load_policy(root: Path) -> dict[str, Any]:
    """Load the repository policy from a contained regular file."""
    path = safe_path(root, ".cleanai/policy.toml", must_exist=True)
    return load_toml(path)


def finite_number(
    value: object, name: str, *, minimum: float, maximum: float | None = None
) -> float:
    """Return a finite bounded numeric configuration value."""
    if isinstance(value, bool):
        raise ConfigurationError(f"{name} must be numeric, not boolean")
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as error:
        raise ConfigurationError(f"{name} must be numeric") from error
    if not math.isfinite(number) or number < minimum or (maximum is not None and number > maximum):
        bound = f"[{minimum}, {maximum}]" if maximum is not None else f">= {minimum}"
        raise ConfigurationError(f"{name} must be finite and in {bound}")
    return number


def atomic_write_text(path: Path, text: str) -> None:
    """Atomically replace a UTF-8 text artifact in its existing directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(raw_temp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def write_json(path: Path, payload: Any) -> None:
    """Write strict, stable, human-readable JSON atomically."""
    atomic_write_text(
        path,
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
    )


def evidence_run_dir(root: Path, family: str) -> Path:
    """Create a concurrency-safe immutable evidence run directory."""
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    run_id = f"{stamp}-{os.getpid()}-{secrets.token_hex(4)}"
    target = safe_path(root, Path("artifacts") / family / "runs" / run_id)
    target.mkdir(parents=True, exist_ok=False)
    return target


def write_findings(
    root: Path,
    name: str,
    findings: list[Finding],
    *,
    metadata: dict[str, Any] | None = None,
) -> Path:
    """Write a unique JSON/Markdown finding bundle and return its directory."""
    output = evidence_run_dir(root, "quality")
    counts = {
        severity: sum(item.severity == severity for item in findings)
        for severity in ("error", "warning", "info")
    }
    write_json(
        output / f"{name}.json",
        {
            "schema_version": 2,
            "name": name,
            "counts": counts,
            "metadata": metadata or {},
            "findings": [asdict(item) for item in findings],
        },
    )
    lines = [
        f"# {name.replace('-', ' ').title()}",
        "",
        f"Errors: **{counts['error']}**; warnings: **{counts['warning']}**; "
        f"info: **{counts['info']}**",
        "",
    ]
    if findings:
        lines.extend(("| Severity | Code | Path | Finding |", "|---|---|---|---|"))
        for item in findings:
            message = item.message.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {item.severity} | `{item.code}` | `{item.path}` | {message} |")
    else:
        lines.append("No findings.")
    atomic_write_text(output / f"{name}.md", "\n".join(lines) + "\n")
    return output


def classify_command(argv: Iterable[str]) -> str:
    """Classify mutable-intelligence commands separately from local controls."""
    parts = tuple(argv)
    if not parts:
        return "deterministic-local"
    executable = Path(parts[0]).name.lower()
    direct_audit = executable.replace("-", "_") == "pip_audit"
    module_audit = (
        len(parts) >= PYTHON_MODULE_INVOCATION_PARTS
        and executable.startswith("python")
        and parts[1] == "-m"
        and parts[2].replace("-", "_") == "pip_audit"
    )
    return "connected" if direct_audit or module_audit else "deterministic-local"


def expand_command(command: str, root: Path) -> tuple[str, ...]:
    """Split trusted command configuration and safely expand contained globs."""
    try:
        parts = shlex.split(command)
    except ValueError as error:
        raise ConfigurationError(f"invalid command quoting: {command!r}: {error}") from error
    if not parts:
        raise ConfigurationError("configured command cannot be empty")
    expanded: list[str] = []
    for part in parts:
        if not any(character in part for character in "*?["):
            expanded.append(part)
            continue
        if Path(part).is_absolute() or ".." in PurePath(part).parts:
            raise ConfigurationError(f"command glob escapes repository: {part}")
        pattern = root / part
        matches = sorted(glob.glob(str(pattern)))  # noqa: PTH207
        if not matches:
            raise ConfigurationError(f"command glob matched no files: {part}")
        for match in matches:
            resolved = Path(match).resolve(strict=True)
            try:
                resolved.relative_to(root.resolve(strict=True))
            except ValueError as error:
                raise ConfigurationError(f"command glob escapes repository: {part}") from error
            expanded.append(str(resolved))
    return tuple(expanded)


def run_command(
    command: str,
    root: Path,
    *,
    timeout_seconds: float,
    environment: dict[str, str] | None = None,
) -> CommandResult:
    """Run one configured command without a shell and classify all failures."""
    started = time.monotonic()
    try:
        argv = expand_command(command, root)
        completed = subprocess.run(  # noqa: S603  # nosec B603
            argv,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            stdin=subprocess.DEVNULL,
            env=environment,
        )
    except ConfigurationError as error:
        return CommandResult(
            command, (), "error", 2, time.monotonic() - started, "", "", "configuration", str(error)
        )
    except FileNotFoundError as error:
        return CommandResult(
            command, (), "error", 127, time.monotonic() - started, "", "", "environment", str(error)
        )
    except PermissionError as error:
        return CommandResult(
            command, (), "error", 126, time.monotonic() - started, "", "", "environment", str(error)
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout if isinstance(error.stdout, str) else ""
        stderr = error.stderr if isinstance(error.stderr, str) else ""
        return CommandResult(
            command,
            tuple(error.cmd) if isinstance(error.cmd, list) else (),
            "timeout",
            124,
            time.monotonic() - started,
            stdout,
            stderr,
            "environment",
            f"timed out after {timeout_seconds:g} seconds",
        )
    status = "passed" if completed.returncode == 0 else "failed"
    return CommandResult(
        command,
        argv,
        status,
        completed.returncode,
        time.monotonic() - started,
        completed.stdout,
        completed.stderr,
        classify_command(argv),
    )


def repository_metadata(root: Path) -> dict[str, Any]:
    """Return reproducibility metadata without failing outside Git."""
    git_commit: str | None = None
    git_status: list[str] | None = None
    executable = shutil.which("git")
    if executable is None:
        return {
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "git_commit": None,
            "git_status": None,
        }
    try:
        revision = subprocess.run(  # noqa: S603  # nosec B603
            [executable, "rev-parse", "HEAD"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        status = subprocess.run(  # noqa: S603  # nosec B603
            [executable, "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if revision.returncode == 0 and status.returncode == 0:
            git_commit = revision.stdout.strip()
            git_status = status.stdout.splitlines()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "git_commit": git_commit,
        "git_status": git_status,
    }


def print_line(value: object = "", *, error: bool = False) -> None:
    """Write one line without relying on the built-in print side effect."""
    stream = sys.stderr if error else sys.stdout
    stream.write(f"{value}\n")
    stream.flush()
