#!/usr/bin/env python3
"""Constrained, project-local adapter for optional Graft structural evidence.

This closed interface never discovers a ``graft`` executable on ``PATH`` and
never exposes init, MCP, LSP, deep/model-backed analysis, hooks, telemetry
controls, visualization, or upgrades. Graft output is derived navigation
evidence, not project authority.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import math
import os
import re
import selectors
import shutil
import signal
import stat
import subprocess  # nosec B404
import tempfile
import threading
import time
from collections.abc import Callable, Generator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import FrameType
from typing import Any, BinaryIO, Final, NoReturn, TypeGuard, cast, override

ROOT: Final = Path(__file__).resolve().parents[1]
RUNTIME_DIR: Final = ROOT / "tools" / "graft-runtime"
PACKAGE_JSON: Final = RUNTIME_DIR / "package.json"
PACKAGE_LOCK: Final = RUNTIME_DIR / "package-lock.json"
GRAFT_PACKAGE: Final = RUNTIME_DIR / "node_modules" / "@nanonets" / "graft"
GRAFT_MANIFEST: Final = GRAFT_PACKAGE / "package.json"
GRAFT_CLI: Final = GRAFT_PACKAGE / "dist" / "cli.js"
INSTALL_RECEIPT: Final = RUNTIME_DIR / "node_modules" / ".clean-agentic-graft-receipt.json"
STATE_DIR: Final = ROOT / "artifacts" / "graft"
GRAPH_DIR: Final = STATE_DIR / "context"
HOME_DIR: Final = STATE_DIR / "home"
CACHE_DIR: Final = STATE_DIR / "cache"
TEMP_DIR: Final = STATE_DIR / "tmp"
NPM_GLOBAL_CONFIG: Final = HOME_DIR / "empty-global-npmrc"
RUNTIME_BACKUP: Final = RUNTIME_DIR / ".node_modules.previous"
RUNTIME_QUARANTINE: Final = RUNTIME_DIR / ".node_modules.failed"
RUNTIME_STAGING: Final = RUNTIME_DIR / ".node_modules.installing"
EVIDENCE_FILE: Final = STATE_DIR / "evidence" / "last-run.json"
GRAPH_RECEIPT: Final = STATE_DIR / "evidence" / "graph-receipt.json"
# The lock lives beside, not inside, removable state. Otherwise removal could
# unlink the held lock and let a second process enter through a new inode.
LOCK_FILE: Final = ROOT / "artifacts" / ".graft-adapter.lock"
REMOVAL_TARGETS: Final = (
    RUNTIME_DIR / "node_modules",
    RUNTIME_BACKUP,
    RUNTIME_QUARANTINE,
    RUNTIME_STAGING,
    STATE_DIR,
)

SignalHandler = int | None | Callable[[int, FrameType | None], object]

EXPECTED_PACKAGE: Final = "@nanonets/graft"
EXPECTED_GRAFT: Final = "0.16.0"
EXPECTED_NPM: Final = "10.9.0"
EXPECTED_COMMIT: Final = "aa1e2bb0f6326068ac64886da1e67fa25a7804de"
EXPECTED_INTEGRITY: Final = (
    "sha512-L3E5F1aDYJDCARgfR7O2VaMt8xwO1XNYyHiW2n1WhKnj87gPqoxoZJGNbGXf"
    "w6XeA9JSJX3naA36RZ+jDf4AcQ=="
)
EXPECTED_LOCK_SHA256: Final = "a8f38c1b33be3a6960ef8abf6e8c8e60ba07c0df9a94dd83e331c4b40136b441"
EXPECTED_PACKAGE_JSON_SHA256: Final = (
    "507febf881dc64c9242d8d7fd019ed3e388f55ac97345919e77888c2c4209101"
)
EXPECTED_CLI_SHA256: Final = "3d73ba67e2f95bcb9d8d511fc061c995b5ddda841eda30be0792ac419a09aaf0"
LOCKFILE_VERSION: Final = 3
ADAPTER_SCHEMA_VERSION: Final = 2
FIRST_CONTROL_CODEPOINT: Final = 32
NODE_VERSION_RE: Final = re.compile(r"^v?(\d{1,3})\.(\d{1,6})\.(\d{1,6})\s*$")
GRAFT_VERSION_RE: Final = re.compile(r"^0\.16\.0\s*$")
NPM_VERSION_RE: Final = re.compile(r"^10\.9\.0\s*$")
SOURCE_SUFFIXES: Final = frozenset(
    {
        ".bb",
        ".c",
        ".cc",
        ".cjs",
        ".clj",
        ".cljc",
        ".cljs",
        ".cpp",
        ".cs",
        ".cts",
        ".cxx",
        ".dart",
        ".ex",
        ".exs",
        ".go",
        ".h",
        ".hh",
        ".hpp",
        ".java",
        ".js",
        ".jsx",
        ".kt",
        ".kts",
        ".lua",
        ".mjs",
        ".ml",
        ".mli",
        ".mts",
        ".nix",
        ".php",
        ".py",
        ".pyi",
        ".r",
        ".rb",
        ".rs",
        ".sc",
        ".scala",
        ".sol",
        ".swift",
        ".ts",
        ".tsx",
        ".vue",
        ".zig",
    }
)
EDGE_RELATIONS: Final = frozenset(
    {"calls", "contains", "extends", "implements", "imports", "references"}
)
JSON_OUTPUT_KEYS: Final = {
    "ask": frozenset({"hits", "mode", "query"}),
    "check": frozenset({"context", "graph"}),
}
ASK_KEYS: Final = frozenset(
    {
        "coverage",
        "coverageStrong",
        "hits",
        "mode",
        "note",
        "query",
        "saved",
        "scopes",
        "subject",
    }
)
ASK_HIT_KEYS: Final = frozenset(
    {
        "code",
        "kind",
        "pointer",
        "related",
        "relation",
        "scope",
        "score",
        "snippet",
        "title",
    }
)
CHECK_KEYS: Final = frozenset({"context", "graph"})
CHECK_CONTEXT_KEYS: Final = frozenset(
    {"contentDrift", "coverage", "indexDrift", "missing", "ok", "removed"}
)
CHECK_GRAPH_KEYS: Final = frozenset(
    {"added", "changed", "missing", "nodes", "ok", "pending", "pendingIds", "removed", "stale"}
)
CHECK_GRAPH_LIST_KEYS: Final = ("added", "changed", "pendingIds", "removed", "stale")
MINIMUM_NODE: Final = (22, 12, 0)
MAXIMUM_NODE: Final = (23, 0, 0)
MAX_OUTPUT_BYTES: Final = 256 * 1024
MAX_JSON_FILE_BYTES: Final = 32 * 1024 * 1024
MAX_JSON_DEPTH: Final = 64
MAX_JSON_ITEMS: Final = 1_000_000
TIMEOUT_SECONDS: Final = 300
LOCK_TIMEOUT_SECONDS: Final = 5.0
MAX_LABEL_CHARS: Final = 500
MAX_POINTER_CHARS: Final = 4_096
MAX_TEXT_FIELD_CHARS: Final = 32_768
MAX_SPAN_CHARS: Final = 32
MAX_INLINE_SOURCE_LINES: Final = 80
MAX_ERROR_MESSAGE_CHARS: Final = 128
ERROR_TRUST: Final = "untrusted-bounded-diagnostic-text"
GRAPH_NODE_KINDS: Final = frozenset(
    {
        "class",
        "constant",
        "enum",
        "file",
        "function",
        "interface",
        "method",
        "module",
        "struct",
        "trait",
        "type",
        "variable",
    }
)
GRAPH_NODE_REQUIRED_KEYS: Final = frozenset(
    {
        "body_hash",
        "crux",
        "exported",
        "id",
        "kind",
        "name",
        "origin",
        "path",
        "signature",
        "span",
        "summary",
        "summary_state",
    }
)
GRAPH_NODE_OPTIONAL_KEYS: Final = frozenset({"arity", "chars", "owner", "variadic"})
GRAPH_SCOPE_MARKERS: Final = frozenset(
    {
        "Cargo.toml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        "go.mod",
        "package.json",
        "pnpm-workspace.yaml",
        "pom.xml",
        "pyproject.toml",
        "setup.py",
    }
)


class AdapterError(RuntimeError):
    """The adapter rejected a request, state, or result."""


class UnverifiedError(AdapterError):
    """The requested operation could not run to an evidence-bearing result."""


class UntrustedValueError(AdapterError):
    """A fixed diagnostic plus an identity for an omitted upstream string."""

    def __init__(self, message: str, value: str) -> None:
        """Attest to an omitted value without retaining it in the public message."""
        self.value_chars = len(value)
        self.value_sha256 = hashlib.sha256(
            value.encode("utf-8", errors="surrogatepass")
        ).hexdigest()
        super().__init__(message)


class AdapterSignalError(AdapterError):
    """The wrapper received a POSIX stop signal while supervising a child."""

    def __init__(self, signal_number: int) -> None:
        """Capture the received signal and produce a bounded public message."""
        self.signal_number = signal_number
        name = signal.Signals(signal_number).name
        super().__init__(f"adapter received {name}; child process group was terminated")


class ExecutedOperationError(AdapterError):
    """A named child ran, but its result could not be accepted or published."""

    def __init__(self, error: BaseException | str) -> None:
        """Preserve the underlying error while marking the operation executed."""
        self.original = AdapterError(error) if isinstance(error, str) else error
        super().__init__(str(self.original))


class InstallCommitError(ExecutedOperationError):
    """A validated new runtime is live but old-backup cleanup did not finish."""


class SafeParser(argparse.ArgumentParser):
    """Raise a structured error instead of printing argparse prose."""

    @override
    def error(self, message: str) -> NoReturn:
        """Reject invalid syntax without probing tools or writing state."""
        raise AdapterError(message)


@dataclass(frozen=True)
class Completed:
    """Bounded result from one supervised child process."""

    returncode: int
    stdout: str
    stderr: str
    stdout_bytes: int
    stderr_bytes: int
    stdout_sha256: str
    stderr_sha256: str
    truncated: bool
    output_limit_exceeded: bool
    background_processes_terminated: bool
    timed_out: bool
    duration_ms: int


@dataclass(frozen=True)
class Captured:
    """Bounded bytes drained from one supervised child."""

    byte_counts: Mapping[str, int]
    prefixes: Mapping[str, bytes]
    digests: Mapping[str, str]
    timed_out: bool
    output_limit_exceeded: bool
    background_processes_terminated: bool


@dataclass(frozen=True)
class EvidenceContext:
    """Optional provenance fields attached to one adapter command."""

    source: Mapping[str, object] | None = None
    source_changed: bool = False
    parameters: Mapping[str, object] | None = None
    runtime: Mapping[str, str] | None = None


@dataclass(frozen=True)
class RunContext:
    """Validated identities and paths held for one locked structural run."""

    tracked: set[str]
    source_before: Mapping[str, object]
    node: Path
    git: Path
    git_identity: Mapping[str, str]
    environment: Mapping[str, str]
    command_arguments: Sequence[str]
    installed: Mapping[str, str]
    run_graph_dir: Path


@dataclass(frozen=True)
class InstallContext:
    """Prerequisites and identities held for one explicit install."""

    tracked: set[str]
    source_before: Mapping[str, object]
    node: Path
    npm: Path
    git: Path
    node_identity: Mapping[str, str]
    npm_identity: Mapping[str, str]
    git_identity: Mapping[str, str]
    node_version: str
    npm_version: str
    provenance: Mapping[str, object]
    environment: Mapping[str, str]


@dataclass(frozen=True)
class InstallResult:
    """npm result plus enough state to commit or restore the runtime swap."""

    completed: Completed
    replaced: bool
    had_previous: bool


@dataclass(frozen=True)
class GraphSwap:
    """Prior derived-state inventory retained until a build is fully evidenced."""

    had_graph: bool
    had_receipt: bool


@dataclass(frozen=True)
class ExecutionPublication:
    """Validated values published together after a structural command."""

    evidence: Mapping[str, object]
    graph: Mapping[str, object] | None
    source: Mapping[str, object]
    runtime: Mapping[str, str]
    status: str


def _json_print(value: Mapping[str, object]) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _error_details(error: BaseException) -> dict[str, object]:
    """Return a bounded diagnostic that callers must continue to treat as untrusted."""
    underlying = error.original if isinstance(error, ExecutedOperationError) else error
    message = str(underlying)
    details: dict[str, object] = {
        "type": type(underlying).__name__,
        "message": message[:MAX_ERROR_MESSAGE_CHARS],
        "message_chars": len(message),
        "message_sha256": hashlib.sha256(
            message.encode("utf-8", errors="surrogatepass")
        ).hexdigest(),
        "message_truncated": len(message) > MAX_ERROR_MESSAGE_CHARS,
        "message_trust": ERROR_TRUST,
    }
    if isinstance(underlying, UntrustedValueError):
        details["omitted_untrusted_value"] = {
            "chars": underlying.value_chars,
            "sha256": underlying.value_sha256,
        }
    return details


def _error_report(
    command: str,
    error: BaseException,
    *,
    status: str,
) -> dict[str, object]:
    return {
        "schema_version": 2,
        "command": command,
        "status": status,
        "error": _error_details(error),
        "error_trust": ERROR_TRUST,
        "authority": "derived-advisory-evidence",
    }


def _executed_error(error: BaseException) -> BaseException:
    if isinstance(error, (AdapterSignalError, ExecutedOperationError)):
        return error
    return ExecutedOperationError(error)


def _validate_json_shape(value: object, label: str) -> object:
    """Bound traversal cost and reject pathological JSON nesting."""
    pending: list[tuple[object, int]] = [(value, 0)]
    visited = 0
    while pending:
        current, depth = pending.pop()
        visited += 1
        if visited > MAX_JSON_ITEMS:
            raise AdapterError(f"{label} contains too many values")
        if depth > MAX_JSON_DEPTH:
            raise AdapterError(f"{label} is nested too deeply")
        if isinstance(current, dict):
            if not all(isinstance(key, str) for key in current):
                raise AdapterError(f"{label} contains a non-string object key")
            pending.extend((item, depth + 1) for item in current.values())
        elif isinstance(current, list):
            pending.extend((item, depth + 1) for item in current)
    return value


def _decode_json(value: str, label: str) -> object:
    def reject_constant(constant: str) -> NoReturn:
        raise ValueError(f"non-finite JSON number {constant!r}")

    try:
        decoded = json.loads(value, parse_constant=reject_constant)
    except (json.JSONDecodeError, RecursionError, ValueError) as error:
        raise AdapterError(f"invalid {label}: {error}") from error
    return _validate_json_shape(decoded, label)


def _read_json(path: Path, label: str) -> object:
    try:
        details = path.lstat()
        if details.st_size > MAX_JSON_FILE_BYTES:
            raise AdapterError(f"{label} exceeds the {MAX_JSON_FILE_BYTES}-byte limit")
        return _decode_json(path.read_text(encoding="utf-8"), label)
    except AdapterError:
        raise
    except (OSError, UnicodeError, RecursionError, ValueError) as error:
        raise AdapterError(f"invalid {label} at {path}: {error}") from error


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise AdapterError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def _path_sort_key(path: Path) -> str:
    return path.as_posix()


def _assert_regular(path: Path, label: str) -> None:
    try:
        details = path.lstat()
    except FileNotFoundError as error:
        raise AdapterError(f"missing {label}: {path}") from error
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
        raise AdapterError(f"{label} must be a regular, non-symlink file: {path}")


def _assert_directory(path: Path, label: str) -> None:
    _assert_path_chain(path, allow_missing=False)
    details = path.lstat()
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISDIR(details.st_mode):
        raise AdapterError(f"{label} must be a real directory: {path}")


def _assert_path_chain(path: Path, *, allow_missing: bool = True) -> None:
    """Reject symlinks or non-directories from ROOT through ``path``."""
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise AdapterError(f"path is outside the project: {path}") from error
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        try:
            details = cursor.lstat()
        except FileNotFoundError:
            if allow_missing:
                continue
            raise AdapterError(f"missing required path: {cursor}") from None
        if stat.S_ISLNK(details.st_mode):
            raise AdapterError(f"symlink is not allowed in managed path: {cursor}")
        if cursor != path and not stat.S_ISDIR(details.st_mode):
            raise AdapterError(f"non-directory in managed path: {cursor}")


def _assert_state_tree() -> None:
    if not STATE_DIR.exists():
        return
    _assert_path_chain(STATE_DIR)
    root_details = STATE_DIR.lstat()
    if not stat.S_ISDIR(root_details.st_mode):
        raise AdapterError(f"managed state root must be a real directory: {STATE_DIR}")
    if root_details.st_mode & 0o077:
        raise AdapterError(f"managed state root must be private to its owner: {STATE_DIR}")
    if hasattr(os, "getuid") and root_details.st_uid != os.getuid():
        raise AdapterError(f"managed state root has a different owner: {STATE_DIR}")
    for current, directories, files in os.walk(STATE_DIR, followlinks=False):
        for name in [*directories, *files]:
            candidate = Path(current) / name
            details = candidate.lstat()
            is_directory = stat.S_ISDIR(details.st_mode)
            is_safe_file = stat.S_ISREG(details.st_mode) and details.st_nlink == 1
            if not is_directory and not is_safe_file:
                raise AdapterError(f"unsafe file type or hardlink in managed state: {candidate}")
            if details.st_mode & 0o077:
                raise AdapterError(f"managed state must be private to its owner: {candidate}")
            if hasattr(os, "getuid") and details.st_uid != os.getuid():
                raise AdapterError(f"managed state has a different owner: {candidate}")


def _make_owned_dir(path: Path) -> None:
    _assert_path_chain(path)
    cursor = ROOT
    for part in path.relative_to(ROOT).parts:
        cursor /= part
        if cursor.exists():
            if cursor.is_symlink() or not cursor.is_dir():
                raise AdapterError(f"unsafe managed directory: {cursor}")
        else:
            cursor.mkdir(mode=0o700)


def _atomic_bytes(path: Path, payload: bytes) -> None:
    """Replace a private managed file and make its bytes durable."""
    _make_owned_dir(path.parent)
    if path.exists() or path.is_symlink():
        _assert_regular(path, "state file")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            temporary.unlink()


def _atomic_json(path: Path, value: Mapping[str, object]) -> None:
    _atomic_bytes(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def _runtime_lock() -> dict[str, object]:
    _assert_directory(RUNTIME_DIR, "runtime directory")
    _assert_regular(PACKAGE_JSON, "runtime package manifest")
    _assert_regular(PACKAGE_LOCK, "runtime package lock")
    package_sha256 = _sha256(PACKAGE_JSON)
    if package_sha256 != EXPECTED_PACKAGE_JSON_SHA256:
        raise AdapterError("runtime package manifest differs from the reviewed manifest")
    package = _read_json(PACKAGE_JSON, "runtime package manifest")
    lock = _read_json(PACKAGE_LOCK, "runtime package lock")
    if not isinstance(package, dict) or not isinstance(lock, dict):
        raise AdapterError("runtime package manifest and lock must be JSON objects")
    dependencies = package.get("dependencies")
    packages = lock.get("packages")
    if not isinstance(dependencies, dict) or not isinstance(packages, dict):
        raise AdapterError("runtime dependency metadata is missing")
    root_lock = packages.get("")
    graft_lock = packages.get(f"node_modules/{EXPECTED_PACKAGE}")
    if not isinstance(root_lock, dict) or not isinstance(graft_lock, dict):
        raise AdapterError("runtime lock does not contain Graft")
    locked_dependencies = root_lock.get("dependencies")
    if not isinstance(locked_dependencies, dict):
        raise AdapterError("runtime lock root dependencies are missing")
    if (
        dependencies.get(EXPECTED_PACKAGE) != EXPECTED_GRAFT
        or locked_dependencies.get(EXPECTED_PACKAGE) != EXPECTED_GRAFT
    ):
        raise AdapterError(f"runtime must pin exact {EXPECTED_PACKAGE} {EXPECTED_GRAFT}")
    if (
        graft_lock.get("version") != EXPECTED_GRAFT
        or graft_lock.get("integrity") != EXPECTED_INTEGRITY
    ):
        raise AdapterError("Graft lock identity does not match the reviewed release")
    lock_sha256 = _sha256(PACKAGE_LOCK)
    if lock.get("lockfileVersion") != LOCKFILE_VERSION:
        raise AdapterError("runtime requires npm lockfileVersion 3")
    if lock_sha256 != EXPECTED_LOCK_SHA256:
        raise AdapterError("runtime package lock differs from the reviewed lock")
    return {
        "package": EXPECTED_PACKAGE,
        "version": EXPECTED_GRAFT,
        "source_tag_commit": EXPECTED_COMMIT,
        "artifact_build_provenance": "UNVERIFIED",
        "integrity": EXPECTED_INTEGRITY,
        "package_json_sha256": package_sha256,
        "lock_sha256": lock_sha256,
    }


def _assert_installed_tree(node_modules: Path) -> None:
    """Reject escapes and special files before moving an npm result into place."""
    details = node_modules.lstat()
    if not stat.S_ISDIR(details.st_mode) or stat.S_ISLNK(details.st_mode):
        raise AdapterError("installed node_modules must be a real directory")
    resolved_root = node_modules.resolve()
    for candidate in node_modules.rglob("*"):
        details = candidate.lstat()
        if stat.S_ISLNK(details.st_mode):
            try:
                resolved = candidate.resolve(strict=True)
            except OSError as error:
                raise AdapterError(
                    f"installed tree contains a broken symlink: {candidate}"
                ) from error
            if not resolved.is_relative_to(resolved_root):
                raise AdapterError(f"installed tree symlink escapes node_modules: {candidate}")
        elif not stat.S_ISDIR(details.st_mode) and not stat.S_ISREG(details.st_mode):
            raise AdapterError(f"installed tree contains an unsafe file type: {candidate}")


def _installed_tree_sha256(node_modules: Path) -> str:
    """Hash names, types, link targets, and file bytes, excluding the receipt itself."""
    digest = hashlib.sha256(b"clean-agentic-graft-installed-tree-v1\0")
    for candidate in sorted(node_modules.rglob("*"), key=_path_sort_key):
        relative = candidate.relative_to(node_modules).as_posix()
        if relative == INSTALL_RECEIPT.name:
            continue
        encoded = relative.encode("utf-8")
        details = candidate.lstat()
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        if stat.S_ISLNK(details.st_mode):
            target = str(candidate.readlink()).encode("utf-8")
            digest.update(b"L")
            digest.update(len(target).to_bytes(8, "big"))
            digest.update(target)
        elif stat.S_ISDIR(details.st_mode):
            digest.update(b"D")
        elif stat.S_ISREG(details.st_mode):
            digest.update(b"F")
            digest.update(bytes.fromhex(_sha256(candidate)))
        else:
            raise AdapterError(f"installed tree contains an unsafe file type: {candidate}")
    return digest.hexdigest()


def _installed_runtime_at(node_modules: Path) -> dict[str, str]:
    package = node_modules / "@nanonets" / "graft"
    manifest_path = package / "package.json"
    cli_path = package / "dist" / "cli.js"
    _assert_installed_tree(node_modules)
    for candidate in (package, manifest_path, cli_path):
        cursor = node_modules
        for part in candidate.relative_to(node_modules).parts:
            cursor /= part
            details = cursor.lstat()
            if stat.S_ISLNK(details.st_mode):
                raise AdapterError(f"symlink is not allowed in the Graft entry path: {cursor}")
    _assert_regular(manifest_path, "installed Graft manifest")
    _assert_regular(cli_path, "installed Graft CLI module")
    manifest = _read_json(manifest_path, "installed Graft manifest")
    if not isinstance(manifest, dict):
        raise AdapterError("installed Graft manifest must be a JSON object")
    binary = manifest.get("bin")
    if (
        manifest.get("name") != EXPECTED_PACKAGE
        or manifest.get("version") != EXPECTED_GRAFT
        or not isinstance(binary, dict)
        or binary.get("graft") != "dist/cli.js"
    ):
        raise AdapterError("installed Graft identity or entry point is unexpected")
    cli_sha256 = _sha256(cli_path)
    if cli_sha256 != EXPECTED_CLI_SHA256:
        raise AdapterError("installed Graft CLI differs from the reviewed npm artifact")
    installed = {
        "cli": str(cli_path),
        "cli_sha256": cli_sha256,
        "manifest_sha256": _sha256(manifest_path),
        "installed_tree_sha256": _installed_tree_sha256(node_modules),
    }
    return installed


def _installed_runtime(
    *,
    require_receipt: bool = True,
    node_identity: Mapping[str, str] | None = None,
) -> dict[str, str]:
    node_modules = RUNTIME_DIR / "node_modules"
    if not node_modules.exists() and not node_modules.is_symlink():
        raise UnverifiedError("local Graft runtime is not installed; run adapter install --apply")
    _assert_path_chain(GRAFT_PACKAGE, allow_missing=False)
    _assert_path_chain(GRAFT_MANIFEST, allow_missing=False)
    _assert_path_chain(GRAFT_CLI, allow_missing=False)
    installed = _installed_runtime_at(RUNTIME_DIR / "node_modules")
    if require_receipt:
        if not INSTALL_RECEIPT.exists() and not INSTALL_RECEIPT.is_symlink():
            raise UnverifiedError("adapter install receipt is absent; run adapter install --apply")
        _assert_regular(INSTALL_RECEIPT, "adapter install receipt")
        receipt = _read_json(INSTALL_RECEIPT, "adapter install receipt")
        core = _install_receipt_core(installed)
        if not _valid_install_receipt(receipt, core):
            raise AdapterError("adapter install receipt does not match installed runtime bytes")
        tools = cast(dict[str, object], receipt["tools"])
        if node_identity is not None and tools["node"] != dict(node_identity):
            raise AdapterError("current Node executable differs from the installed-runtime receipt")
    return installed


def _install_receipt_core(installed: Mapping[str, str]) -> dict[str, object]:
    return {
        "schema_version": 2,
        "package": EXPECTED_PACKAGE,
        "version": EXPECTED_GRAFT,
        "package_json_sha256": EXPECTED_PACKAGE_JSON_SHA256,
        "package_lock_sha256": EXPECTED_LOCK_SHA256,
        "manifest_sha256": installed["manifest_sha256"],
        "cli_sha256": installed["cli_sha256"],
        "installed_tree_sha256": installed["installed_tree_sha256"],
    }


def _install_receipt(
    installed: Mapping[str, str],
    *,
    node_identity: Mapping[str, str],
    npm_identity: Mapping[str, str],
) -> dict[str, object]:
    return {
        **_install_receipt_core(installed),
        "tools": {
            "node": dict(node_identity),
            "npm": dict(npm_identity),
        },
        "authority": "local-tamper-detection-not-build-provenance",
    }


def _valid_tool_receipt(value: object) -> bool:
    """Recognize the exact, locally observed identity recorded for one executable."""
    if not isinstance(value, dict) or value.keys() != {"path", "sha256", "provenance"}:
        return False
    path = value.get("path")
    digest = value.get("sha256")
    return (
        isinstance(path, str)
        and Path(path).is_absolute()
        and isinstance(digest, str)
        and re.fullmatch(r"[0-9a-f]{64}", digest) is not None
        and value.get("provenance") == "UNVERIFIED-system-tool"
    )


def _valid_install_receipt(
    value: object,
    core: Mapping[str, object],
) -> TypeGuard[dict[str, object]]:
    """Require the exact adapter receipt schema; extra or missing claims fail closed."""
    if not isinstance(value, dict) or value.keys() != {*core, "tools", "authority"}:
        return False
    tools = value.get("tools")
    return (
        all(value.get(name) == expected for name, expected in core.items())
        and value.get("authority") == "local-tamper-detection-not-build-provenance"
        and isinstance(tools, dict)
        and tools.keys() == {"node", "npm"}
        and _valid_tool_receipt(tools.get("node"))
        and _valid_tool_receipt(tools.get("npm"))
    )


def _resolve_executable(name: str) -> Path:
    found = shutil.which(name)
    if found is None:
        raise UnverifiedError(f"{name} is not available")
    path = Path(found).resolve()
    _assert_regular(path, name)
    if not os.access(path, os.X_OK):
        raise AdapterError(f"{name} is not executable: {path}")
    if path.is_relative_to(ROOT.resolve()):
        raise AdapterError(f"{name} must not be loaded from the project: {path}")
    for ancestor in (path, *path.parents):
        details = ancestor.lstat()
        writable = details.st_mode & 0o022
        if writable:
            raise AdapterError(f"{name} resolves through a writable path: {ancestor}")
        if ancestor == ancestor.parent:
            break
    return path


def _tool_identity(path: Path) -> dict[str, str]:
    return {
        "path": str(path),
        "sha256": _sha256(path),
        "provenance": "UNVERIFIED-system-tool",
    }


def _require_tool_identity(
    path: Path,
    expected: Mapping[str, str],
    label: str,
) -> None:
    """Fail before executing a tool whose bound bytes or path have changed."""
    if _tool_identity(path) != dict(expected):
        raise AdapterError(f"{label} executable changed during the adapter operation")


def _git_environment() -> dict[str, str]:
    """Disable ambient Git configuration, prompts, hooks, locks, and fsmonitor."""
    return {
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": "core.fsmonitor",
        "GIT_CONFIG_VALUE_0": "false",
        "GIT_CONFIG_KEY_1": "core.hooksPath",
        "GIT_CONFIG_VALUE_1": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    }


def _minimal_environment(
    node: Path,
    *,
    install: bool = False,
    git: Path | None = None,
    npm: Path | None = None,
) -> dict[str, str]:
    paths = [node.parent]
    if npm is not None:
        paths.append(npm.parent)
    if git is not None:
        paths.append(git.parent)
    paths.extend((Path("/usr/local/bin"), Path("/usr/bin"), Path("/bin")))
    unique_paths = list(dict.fromkeys(path for path in paths if path.is_dir()))
    child_path = os.pathsep.join(str(path) for path in unique_paths)
    expected_tools = {
        "node": node,
        **({"npm": npm} if npm is not None else {}),
        **({"git": git} if git is not None else {}),
    }
    for name, expected in expected_tools.items():
        found = shutil.which(name, path=child_path)
        if found is None or Path(found).resolve() != expected.resolve():
            raise AdapterError(f"child PATH cannot preserve the bound {name} executable identity")
    environment = {
        "CI": "1",
        "DO_NOT_TRACK": "1",
        "DOTENV_CONFIG_PATH": os.devnull,
        "GRAFT_DIR": str(GRAPH_DIR),
        "GRAFT_NO_GITIGNORE": "1",
        "GRAFT_NO_IGNORE": "1",
        "GRAFT_NO_REFRESH": "1",
        "HOME": str(HOME_DIR),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
        "PATH": child_path,
        "TEMP": str(TEMP_DIR),
        "TMP": str(TEMP_DIR),
        "TMPDIR": str(TEMP_DIR),
        "USERPROFILE": str(HOME_DIR),
        "XDG_CACHE_HOME": str(CACHE_DIR),
        "XDG_CONFIG_HOME": str(HOME_DIR / "config"),
        "XDG_DATA_HOME": str(HOME_DIR / "data"),
    }
    if install:
        environment.update(
            {
                "npm_config_audit": "false",
                "npm_config_cache": str(CACHE_DIR / "npm"),
                "npm_config_fund": "false",
                "npm_config_globalconfig": str(NPM_GLOBAL_CONFIG),
                "npm_config_userconfig": os.devnull,
                "npm_config_update_notifier": "false",
            }
        )
    if git is not None:
        environment.update(_git_environment())
    for key in ("COMSPEC", "PATHEXT", "SYSTEMROOT", "WINDIR"):
        if key in os.environ:
            environment[key] = os.environ[key]
    return environment


def _prepare_state() -> None:
    _assert_state_tree()
    directories = (
        GRAPH_DIR,
        HOME_DIR,
        CACHE_DIR,
        TEMP_DIR,
        EVIDENCE_FILE.parent,
        HOME_DIR / "config",
        HOME_DIR / "data",
        HOME_DIR / ".graft",
    )
    for directory in directories:
        _make_owned_dir(directory)
    # npm 10 rejects using /dev/null as both user and global configuration.
    # Keep the global source distinct, private, adapter-owned, and empty.
    _atomic_bytes(NPM_GLOBAL_CONFIG, b"")
    _atomic_json(
        HOME_DIR / ".graft" / "update-check.json",
        {"checkedAt": int(time.time() * 1000), "latest": EXPECTED_GRAFT},
    )


def _process_group_exists(identifier: int) -> bool:
    """Return whether a POSIX process group can still receive a signal."""
    try:
        os.killpg(identifier, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _terminate_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate the child's isolated POSIX group, including descendants."""
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)
    deadline = time.monotonic() + 0.25
    while _process_group_exists(process.pid) and time.monotonic() < deadline:
        time.sleep(0.01)
    if _process_group_exists(process.pid):
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
    if process.poll() is None:
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=2)


def _terminate(process: subprocess.Popen[bytes]) -> None:
    """Terminate a supervised child and its isolated group where supported."""
    if os.name == "posix":
        _terminate_group(process)
        return
    if process.poll() is not None:
        return
    try:
        process.terminate()
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        with contextlib.suppress(OSError):
            process.kill()


def _restore_signal_handlers(previous: Mapping[signal.Signals, SignalHandler]) -> None:
    for watched, handler in previous.items():
        signal.signal(watched, handler)


def _install_launch_signal_latch(received: list[int]) -> dict[signal.Signals, SignalHandler]:
    """Latch stop signals across Popen/setup without leaking a blocked child mask."""
    if os.name != "posix" or threading.current_thread() is not threading.main_thread():
        return {}
    previous: dict[signal.Signals, SignalHandler] = {}

    def latch(signal_number: int, _frame: object) -> None:
        received.append(signal_number)

    for watched in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        previous[watched] = signal.getsignal(watched)
        signal.signal(watched, latch)
    return previous


@contextlib.contextmanager
def _defer_stop_signals() -> Generator[None]:
    """Defer POSIX stop signals until an install transaction is recoverable."""
    received: list[int] = []
    previous = _install_launch_signal_latch(received)
    failed = False
    try:
        yield
    except BaseException:
        failed = True
        raise
    finally:
        _restore_signal_handlers(previous)
        if received and not failed:
            raise AdapterSignalError(received[0])


@contextlib.contextmanager
def _forward_termination(
    process: subprocess.Popen[bytes],
    previous: Mapping[signal.Signals, SignalHandler] | None = None,
) -> Generator[None]:
    """Terminate the isolated child group when the wrapper receives a stop signal."""
    if os.name != "posix" or threading.current_thread() is not threading.main_thread():
        yield
        return
    restore = dict(previous or {})

    def terminate_child(received: int, _frame: object) -> NoReturn:
        _terminate(process)
        raise AdapterSignalError(received)

    try:
        for watched in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
            if watched not in restore:
                restore[watched] = signal.getsignal(watched)
            signal.signal(watched, terminate_child)
        yield
    finally:
        _restore_signal_handlers(restore)


def _close_selected_streams(selector: selectors.BaseSelector) -> None:
    """Stop inherited descendant pipe handles from extending the hard deadline."""
    for key in list(selector.get_map().values()):
        stream = cast(BinaryIO, key.fileobj)
        with contextlib.suppress(Exception):
            selector.unregister(stream)
        with contextlib.suppress(OSError):
            stream.close()


def _drain_selected_streams(
    selector: selectors.BaseSelector,
    byte_counts: dict[str, int],
    digests: dict[str, Any],
    prefixes: dict[str, bytearray],
    *,
    wait: float,
) -> bool:
    """Drain ready chunks and report whether either byte ceiling was crossed."""
    exceeded = False
    for key, _mask in selector.select(timeout=wait):
        stream = cast(BinaryIO, key.fileobj)
        chunk = os.read(key.fd, 64 * 1024)
        if not chunk:
            selector.unregister(stream)
            stream.close()
            continue
        label = str(key.data)
        digests[label].update(chunk)
        byte_counts[label] += len(chunk)
        remaining = MAX_OUTPUT_BYTES - len(prefixes[label])
        if remaining > 0:
            prefixes[label].extend(chunk[:remaining])
        exceeded = exceeded or byte_counts[label] > MAX_OUTPUT_BYTES
    return exceeded


def _background_group_exists(process: subprocess.Popen[bytes]) -> bool:
    return process.poll() is not None and os.name == "posix" and _process_group_exists(process.pid)


def _await_leader(process: subprocess.Popen[bytes], deadline: float) -> bool:
    """Wait only within the original deadline; report forced cleanup."""
    if process.poll() is not None:
        return False
    try:
        process.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        _terminate(process)
        return True
    return False


def _capture_child(
    process: subprocess.Popen[bytes],
    selector: selectors.BaseSelector,
    deadline: float,
) -> Captured:
    """Drain both pipes while enforcing active byte and time limits."""
    byte_counts = {"stdout": 0, "stderr": 0}
    digests = {"stdout": hashlib.sha256(), "stderr": hashlib.sha256()}
    prefixes = {"stdout": bytearray(), "stderr": bytearray()}
    timed_out = False
    output_limit_exceeded = False
    background_processes_terminated = False
    stop_capture = False
    while True:
        now = time.monotonic()
        if now >= deadline:
            timed_out = True
            _terminate(process)
            _close_selected_streams(selector)
            break

        if _background_group_exists(process):
            background_processes_terminated = True
            _terminate(process)

        if not selector.get_map():
            if process.poll() is not None:
                break
            time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))
            continue

        wait = min(0.05, max(0.0, deadline - time.monotonic()))
        exceeded = _drain_selected_streams(
            selector,
            byte_counts,
            digests,
            prefixes,
            wait=wait,
        )
        if exceeded and not output_limit_exceeded:
            output_limit_exceeded = True
            _terminate(process)
            _close_selected_streams(selector)
            stop_capture = True
        if stop_capture:
            break

    timed_out = timed_out or _await_leader(process, deadline)
    if _background_group_exists(process):
        background_processes_terminated = True
        _terminate(process)
    _close_selected_streams(selector)
    return Captured(
        byte_counts=byte_counts,
        prefixes={name: bytes(value) for name, value in prefixes.items()},
        digests={name: value.hexdigest() for name, value in digests.items()},
        timed_out=timed_out,
        output_limit_exceeded=output_limit_exceeded,
        background_processes_terminated=background_processes_terminated,
    )


def _completed(process: subprocess.Popen[bytes], capture: Captured, started: float) -> Completed:
    """Convert bounded capture state into the stable adapter result schema."""
    returncode = process.returncode
    if capture.timed_out:
        returncode = 124
    elif capture.output_limit_exceeded:
        returncode = 125
    elif capture.background_processes_terminated:
        returncode = 126
    stdout_bytes = capture.byte_counts["stdout"]
    stderr_bytes = capture.byte_counts["stderr"]
    return Completed(
        returncode=returncode,
        stdout=capture.prefixes["stdout"].decode("utf-8", errors="replace"),
        stderr=capture.prefixes["stderr"].decode("utf-8", errors="replace"),
        stdout_bytes=stdout_bytes,
        stderr_bytes=stderr_bytes,
        stdout_sha256=capture.digests["stdout"],
        stderr_sha256=capture.digests["stderr"],
        truncated=stdout_bytes > MAX_OUTPUT_BYTES or stderr_bytes > MAX_OUTPUT_BYTES,
        output_limit_exceeded=capture.output_limit_exceeded,
        background_processes_terminated=capture.background_processes_terminated,
        timed_out=capture.timed_out,
        duration_ms=round((time.monotonic() - started) * 1000),
    )


def _cleanup_supervision(
    selector: selectors.BaseSelector | None,
    process: subprocess.Popen[bytes] | None,
) -> None:
    if selector is not None:
        selector.close()
    if process is None:
        return
    for stream in (process.stdout, process.stderr):
        if stream is not None:
            with contextlib.suppress(OSError):
                stream.close()


def _supervise(
    command: Sequence[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    timeout: float | None = None,
    temp_root: Path | None = None,
) -> Completed:
    """Run a child with active output, time, process-group, and environment bounds."""
    limit = TIMEOUT_SECONDS if timeout is None else timeout
    started = time.monotonic()
    _ = temp_root  # Kept for a stable call interface; pipes avoid temporary output files.
    received_signals: list[int] = []
    previous_handlers = _install_launch_signal_latch(received_signals)
    process: subprocess.Popen[bytes] | None = None
    selected: selectors.BaseSelector | None = None
    try:
        process = subprocess.Popen(  # noqa: S603  # nosec B603
            list(command),
            cwd=cwd,
            env=dict(environment),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=os.name == "posix",
            umask=0o077 if os.name == "posix" else -1,
        )
        if process.stdout is None or process.stderr is None:
            raise AdapterError("cannot supervise child output pipes")
        selected = selectors.DefaultSelector()
        selected.register(process.stdout, selectors.EVENT_READ, "stdout")
        selected.register(process.stderr, selectors.EVENT_READ, "stderr")
        with _forward_termination(process, previous_handlers):
            if received_signals:
                raise AdapterSignalError(received_signals[0])
            capture = _capture_child(process, selected, time.monotonic() + limit)
    except BaseException:
        if process is not None:
            _terminate(process)
        raise
    finally:
        if previous_handlers:
            _restore_signal_handlers(previous_handlers)
        _cleanup_supervision(selected, process)
    if process is None:
        raise AdapterError("child process did not start")
    return _completed(process, capture, started)


def _probe_node(node: Path) -> str:
    completed = _supervise(
        [str(node), "--version"],
        cwd=ROOT,
        environment=_minimal_environment(node),
        timeout=10,
    )
    match = NODE_VERSION_RE.fullmatch(completed.stdout)
    if completed.returncode or completed.truncated or completed.stderr or match is None:
        raise UnverifiedError("Node version probe failed or returned unexpected output")
    version = tuple(int(value) for value in match.groups())
    if version < MINIMUM_NODE or version >= MAXIMUM_NODE:
        raise UnverifiedError("Node must be >=22.12.0 and <23.0.0")
    return ".".join(str(part) for part in version)


def _probe_graft(node: Path, *, require_receipt: bool = True) -> dict[str, str]:
    node_identity = _tool_identity(node)
    runtime = _installed_runtime(
        require_receipt=require_receipt,
        node_identity=node_identity if require_receipt else None,
    )
    completed = _supervise(
        [str(node), str(GRAFT_CLI), "--version"],
        cwd=ROOT,
        environment=_minimal_environment(node),
        timeout=10,
    )
    if (
        completed.returncode
        or completed.truncated
        or completed.stderr
        or GRAFT_VERSION_RE.fullmatch(completed.stdout) is None
    ):
        raise AdapterError("local Graft version probe failed or returned unexpected output")
    if _tool_identity(node) != node_identity:
        raise AdapterError("Node executable changed during the Graft version probe")
    return {
        **runtime,
        "node_path": node_identity["path"],
        "node_sha256": node_identity["sha256"],
        "node_provenance": node_identity["provenance"],
    }


def _doctor() -> dict[str, object]:
    """Inspect prerequisites without creating, deleting, or replacing files."""
    report: dict[str, object] = {
        "schema_version": 2,
        "command": "doctor",
        "status": "UNVERIFIED",
        "ready": False,
        "authority": "derived-advisory-evidence",
        "capabilities": {
            "structural_cli": True,
            "mcp": False,
            "lsp": False,
            "deep": False,
            "hooks": False,
            "viz": False,
            "init": False,
        },
        "state_dir": STATE_DIR.relative_to(ROOT).as_posix(),
    }
    try:
        _assert_path_chain(STATE_DIR)
        _assert_state_tree()
        provenance = _runtime_lock()
        node = _resolve_executable("node")
        _installed_runtime(node_identity=_tool_identity(node))
        node_version = _probe_node(node)
        installed = _probe_graft(node)
        report.update(
            {
                "status": "PASS",
                "ready": True,
                "node": {
                    "sha256": installed["node_sha256"],
                    "provenance": "UNVERIFIED-system-tool",
                    "version": node_version,
                    "required": ">=22.12.0,<23",
                },
                "graft": {
                    "cli": GRAFT_CLI.relative_to(ROOT).as_posix(),
                    "version": EXPECTED_GRAFT,
                    "cli_sha256": installed["cli_sha256"],
                    "manifest_sha256": installed["manifest_sha256"],
                },
                "provenance": provenance,
            }
        )
    except AdapterSignalError:
        raise
    except UnverifiedError as error:
        report["error"] = _error_details(error)
        report["error_trust"] = ERROR_TRUST
    except (AdapterError, OSError, subprocess.SubprocessError) as error:
        report["status"] = "FAIL"
        report["error"] = _error_details(error)
        report["error_trust"] = ERROR_TRUST
    return report


def _git(*arguments: str, executable: Path | None = None) -> Completed:
    git = _resolve_executable("git") if executable is None else executable
    return _supervise(
        [
            str(git),
            "-c",
            "core.fsmonitor=false",
            "-c",
            "core.hooksPath=/dev/null",
            "-C",
            str(ROOT),
            *arguments,
        ],
        cwd=ROOT,
        environment={
            **_git_environment(),
            "HOME": os.devnull,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": str(git.parent),
        },
        timeout=30,
    )


def _nul_paths(completed: Completed, label: str) -> list[Path]:
    if completed.returncode:
        message = completed.stderr.strip()
        raise AdapterError(f"cannot determine {label}: {message}")
    if "\ufffd" in completed.stdout:
        raise AdapterError(f"{label} contain a non-UTF-8 path")
    return [Path(value) for value in completed.stdout.split("\0") if value]


def _source_scope(git: Path | None = None) -> set[str]:
    top = _git("rev-parse", "--show-toplevel", executable=git)
    if top.returncode:
        raise AdapterError("Graft structural evidence requires a Git worktree")
    if Path(top.stdout.strip()).resolve() != ROOT.resolve():
        raise AdapterError("Git top level does not match the project root")
    tracked = _nul_paths(_git("ls-files", "-z", executable=git), "tracked files")
    untracked = _nul_paths(
        _git(
            "ls-files",
            "-z",
            "--others",
            "--exclude-standard",
            executable=git,
        ),
        "untracked files",
    )
    if untracked:
        raise AdapterError(
            "untracked files are outside the reproducible graph scope: "
            + ", ".join(str(path) for path in sorted(untracked)[:5])
        )
    tracked_strings: set[str] = set()
    for relative in [*tracked, *untracked]:
        if relative.is_absolute() or ".." in relative.parts:
            raise AdapterError(f"Git reported an out-of-scope path: {relative}")
        candidate = ROOT / relative
        if candidate.is_symlink():
            raise AdapterError(f"source symlinks are not allowed: {relative}")
        if candidate.exists() and not candidate.resolve().is_relative_to(ROOT.resolve()):
            raise AdapterError(f"source resolves outside the project: {relative}")
    for relative in tracked:
        tracked_strings.add(PurePosixPath(relative).as_posix())
    _reject_unbound_graph_markers(tracked_strings)
    return tracked_strings


def _reject_unbound_graph_markers(tracked: set[str]) -> None:
    """Reject ignored marker bytes that pinned Graft reads outside Git's file set."""
    directories = {PurePosixPath(".")}
    for relative in tracked:
        parent = PurePosixPath(relative).parent
        directories.update((parent, *parent.parents))
    for directory in directories:
        for marker in GRAPH_SCOPE_MARKERS:
            relative = (directory / marker).as_posix()
            if relative.startswith("./"):
                relative = relative[2:]
            candidate = ROOT / relative
            if (candidate.exists() or candidate.is_symlink()) and relative not in tracked:
                raise AdapterError(
                    "ignored or untracked Graft scope marker is outside the source receipt: "
                    f"{relative}"
                )


def _reject_legacy_root_state() -> None:
    legacy = ROOT / ".graft"
    if legacy.exists() or legacy.is_symlink():
        raise AdapterError(
            "legacy root .graft state could alter upstream traversal; "
            "inspect and remove it manually"
        )


def _source_snapshot(tracked: set[str], git: Path | None = None) -> dict[str, object]:
    selected_git = _resolve_executable("git") if git is None else git
    git_identity = _tool_identity(selected_git)
    head = _git("rev-parse", "HEAD", executable=selected_git)
    status = _git(
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        executable=selected_git,
    )
    if head.returncode or status.returncode:
        raise AdapterError("cannot bind evidence to the current Git worktree")
    digest = hashlib.sha256(b"clean-agentic-graft-source-v1\0")
    tree_digest = hashlib.sha256(b"clean-agentic-graft-tracked-tree-v1\0")
    source_count = 0
    for relative in sorted(tracked):
        path = ROOT / relative
        raw_hash: str | None = None
        encoded = relative.encode("utf-8")
        tree_digest.update(len(encoded).to_bytes(8, "big"))
        tree_digest.update(encoded)
        if not path.exists():
            tree_digest.update(b"\0missing\0")
        else:
            _assert_regular(path, "tracked file")
            raw_hash = _sha256(path)
            tree_digest.update(bytes.fromhex(raw_hash))
        if path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        source_count += 1
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        if not path.exists():
            digest.update(b"\0missing\0")
            continue
        if raw_hash is None:
            raise AdapterError(f"tracked source disappeared during hashing: {path}")
        digest.update(bytes.fromhex(raw_hash))
    return {
        "head_commit": head.stdout.strip(),
        "status_bytes": status.stdout_bytes,
        "status_sha256": status.stdout_sha256,
        "dirty": bool(status.stdout),
        "git": git_identity,
        "tracked_files": len(tracked),
        "tracked_tree_sha256": tree_digest.hexdigest(),
        "tracked_source_files": source_count,
        "tracked_source_sha256": digest.hexdigest(),
    }


def _load_graph(graph_path: Path) -> tuple[dict[str, object], list[object], list[object]]:
    """Load the small set of graph fields the adapter can validate."""
    _assert_regular(graph_path, "Graft graph")
    value = _read_json(graph_path, "Graft graph")
    if (
        not isinstance(value, dict)
        or value.keys() != {"meta", "nodes", "edges"}
        or not isinstance(value.get("meta"), dict)
    ):
        raise AdapterError("Graft graph has no valid meta object")
    meta = value["meta"]
    nodes = value.get("nodes")
    edges = value.get("edges")
    required_meta = {"version", "nodeCount", "edgeCount", "languages"}
    if (
        not required_meta <= meta.keys()
        or not meta.keys() <= required_meta | {"scopes"}
        or not isinstance(nodes, list)
        or not isinstance(edges, list)
        or meta.get("version") != 1
    ):
        raise AdapterError("Graft graph has an unsupported schema")
    if meta.get("nodeCount") != len(nodes) or meta.get("edgeCount") != len(edges):
        raise AdapterError("Graft graph counts do not match its contents")
    languages = meta.get("languages")
    if not _valid_string_list(languages, allow_empty=False) or len(languages) != len(
        set(languages)
    ):
        raise AdapterError("Graft graph has invalid language metadata")
    if "scopes" in meta and not _valid_graph_scopes(meta["scopes"]):
        raise AdapterError("Graft graph has invalid scope metadata")
    return meta, nodes, edges


def _valid_graph_scopes(value: object) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict) or item.keys() != {"prefix", "label", "markers"}:
            return False
        prefix = item["prefix"]
        label = item["label"]
        if not isinstance(prefix, str) or not isinstance(label, str):
            return False
        if prefix.startswith(("/", "\\")) or ".." in PurePosixPath(prefix).parts:
            return False
        if not _valid_string_list(item["markers"], allow_empty=False):
            return False
    return True


def _valid_optional_nonnegative_integer(value: Mapping[str, object], name: str) -> bool:
    item = value.get(name)
    return name not in value or (isinstance(item, int) and not isinstance(item, bool) and item >= 0)


def _span_bounds(value: object) -> tuple[int, int] | None:
    if not isinstance(value, str) or len(value) > MAX_SPAN_CHARS:
        return None
    match = re.fullmatch(r"L([1-9]\d{0,8})-L([1-9]\d{0,8})", value)
    if match is None:
        return None
    first, last = (int(match.group(index)) for index in (1, 2))
    return (first, last) if first <= last else None


def _valid_node_fields(value: Mapping[str, object]) -> bool:
    signature = value.get("signature")
    name = value.get("name")
    return all(
        (
            isinstance(name, str),
            bool(name.strip()) if isinstance(name, str) else False,
            len(name) <= MAX_LABEL_CHARS if isinstance(name, str) else False,
            _span_bounds(value.get("span")) is not None,
            isinstance(value.get("exported"), bool),
            signature is None or isinstance(signature, str),
            re.fullmatch(r"[0-9a-f]{64}", str(value.get("body_hash"))) is not None,
            "owner" not in value or isinstance(value.get("owner"), str),
            _valid_optional_nonnegative_integer(value, "arity"),
            _valid_optional_nonnegative_integer(value, "chars"),
            "variadic" not in value or isinstance(value.get("variadic"), bool),
        )
    )


def _span_within_source(
    value: object,
    path: str,
    node_kind: str,
    line_bounds: dict[str, tuple[int, int]],
) -> bool:
    if path not in line_bounds:
        raw = (ROOT / path).read_bytes()
        source_lines = max(1, raw.count(b"\n") + (not raw.endswith(b"\n")))
        graft_file_end = raw.count(b"\n") + 1
        line_bounds[path] = (source_lines, graft_file_end)
    span = _span_bounds(value)
    if span is None:
        return False
    source_lines, graft_file_end = line_bounds[path]
    if node_kind == "file":
        return span == (1, graft_file_end)
    return span[1] <= source_lines


def _invalid_node_id_error(value: object) -> AdapterError:
    """Create fixed wording plus an identity when an invalid ID is a string."""
    message = "Graft graph contains an invalid or duplicate node id"
    return UntrustedValueError(message, value) if isinstance(value, str) else AdapterError(message)


def _validated_node(
    value: object,
    *,
    expected_sources: set[str],
    node_ids: set[str],
    line_bounds: dict[str, tuple[int, int]],
) -> tuple[str, str, str]:
    """Validate one structural-only node and return its stable fields."""
    if not isinstance(value, dict):
        raise AdapterError("Graft graph contains a non-object node")
    if not value.keys() >= GRAPH_NODE_REQUIRED_KEYS or not value.keys() <= (
        GRAPH_NODE_REQUIRED_KEYS | GRAPH_NODE_OPTIONAL_KEYS
    ):
        raise AdapterError("Graft graph node does not match the reviewed NodeV1 fields")
    node_id = value.get("id")
    node_path = value.get("path")
    node_kind = value.get("kind")
    if (
        not isinstance(node_id, str)
        or not node_id
        or len(node_id) > MAX_POINTER_CHARS
        or any(ord(character) < FIRST_CONTROL_CODEPOINT for character in node_id)
        or node_id in node_ids
    ):
        raise _invalid_node_id_error(node_id)
    if not isinstance(node_path, str) or node_path not in expected_sources:
        raise AdapterError("Graft graph contains an invalid source path")
    if not isinstance(node_kind, str) or node_kind not in GRAPH_NODE_KINDS:
        raise AdapterError("Graft graph node has no valid kind")
    if not _valid_node_fields(value):
        raise AdapterError("Graft graph node has malformed structural fields")
    if not _span_within_source(value.get("span"), node_path, node_kind, line_bounds):
        raise AdapterError("Graft graph node span is outside its source")
    if value.get("origin") != "ast":
        raise AdapterError("Graft graph contains non-structural node provenance")
    if (
        value.get("summary_state") != "pending"
        or value.get("summary") is not None
        or value.get("crux") is not None
    ):
        raise AdapterError("Graft graph contains deep or summary-derived meaning")
    return node_id, node_path, node_kind


def _validate_graph_nodes(nodes: list[object], expected_sources: set[str]) -> set[str]:
    """Require unique AST nodes and exact file coverage of tracked source."""
    node_ids: set[str] = set()
    file_nodes: list[str] = []
    line_bounds: dict[str, tuple[int, int]] = {}
    for value in nodes:
        node_id, node_path, node_kind = _validated_node(
            value,
            expected_sources=expected_sources,
            node_ids=node_ids,
            line_bounds=line_bounds,
        )
        node_ids.add(node_id)
        if node_kind != "file":
            continue
        file_nodes.append(node_path)
        if not isinstance(value, dict) or value.get("body_hash") != _sha256(ROOT / node_path):
            raise AdapterError(f"Graft file node does not match source bytes: {node_path}")
    actual_sources = set(file_nodes)
    if len(file_nodes) != len(actual_sources):
        raise AdapterError("Graft graph contains duplicate file nodes")
    if actual_sources != expected_sources:
        missing = [f"missing {path}" for path in sorted(expected_sources - actual_sources)[:5]]
        extra = [f"extra {path}" for path in sorted(actual_sources - expected_sources)[:5]]
        raise AdapterError(
            "Graft graph file nodes differ from tracked sources: " + ", ".join(missing + extra)
        )
    return node_ids


def _validate_graph_edges(edges: list[object], node_ids: set[str]) -> None:
    """Reject duplicate, non-structural, or invalid graph edges."""
    seen: set[tuple[str, str, str]] = set()
    for value in edges:
        if not isinstance(value, dict) or value.keys() != {
            "source",
            "target",
            "relation",
            "confidence",
        }:
            raise AdapterError("Graft graph contains a non-object edge")
        source = value.get("source")
        target = value.get("target")
        relation = value.get("relation")
        confidence = value.get("confidence")
        if not isinstance(source, str) or not isinstance(target, str):
            raise AdapterError("Graft graph edge has a non-string endpoint")
        if not isinstance(relation, str):
            raise AdapterError("Graft graph edge has a non-string relation")
        if not isinstance(confidence, str):
            raise AdapterError("Graft graph edge has a non-string confidence")
        identity = (source, target, relation)
        valid = (
            source in node_ids
            and bool(target)
            and relation in EDGE_RELATIONS
            and confidence in {"extracted", "inferred"}
            and (relation not in {"calls", "contains"} or target in node_ids)
        )
        if not valid or identity in seen:
            raise AdapterError("Graft graph contains a duplicate or invalid edge")
        seen.add(identity)


def _graph_tree_identity(graph_dir: Path) -> dict[str, object]:
    """Bind every graph/cache artifact that a pinned query could consume."""
    _assert_directory(graph_dir, "Graft graph directory")
    digest = hashlib.sha256(b"clean-agentic-graft-graph-tree-v1\0")
    files = 0
    total_bytes = 0
    for candidate in sorted(graph_dir.rglob("*"), key=_path_sort_key):
        relative = candidate.relative_to(graph_dir).as_posix().encode("utf-8")
        details = candidate.lstat()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        if stat.S_ISDIR(details.st_mode):
            digest.update(b"D")
            continue
        if not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
            raise AdapterError(f"Graft graph contains an unsafe file type: {candidate}")
        digest.update(b"F")
        digest.update(bytes.fromhex(_sha256(candidate)))
        files += 1
        total_bytes += details.st_size
    return {
        "tree_sha256": digest.hexdigest(),
        "files": files,
        "bytes": total_bytes,
    }


def _validate_graph(tracked: set[str], graph_dir: Path | None = None) -> dict[str, object]:
    """Validate exact structural graph coverage and return its content identity."""
    selected = GRAPH_DIR if graph_dir is None else graph_dir
    graph_path = selected / ".graph" / "wiring.json"
    if not graph_path.exists() and not graph_path.is_symlink():
        raise UnverifiedError("Graft graph is absent; run adapter build")
    meta, nodes, edges = _load_graph(graph_path)
    expected_sources = {
        path
        for path in tracked
        if (ROOT / path).is_file() and Path(path).suffix.lower() in SOURCE_SUFFIXES
    }
    node_ids = _validate_graph_nodes(nodes, expected_sources)
    _validate_graph_edges(edges, node_ids)
    tree = _graph_tree_identity(selected)
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "languages": meta.get("languages", []),
        "language_metadata_trust": "untrusted-validated-upstream-metadata",
        "wiring_sha256": _sha256(graph_path),
        "tree_sha256": tree["tree_sha256"],
        "tree_files": tree["files"],
        "tree_bytes": tree["bytes"],
    }


@contextlib.contextmanager
def _exclusive_lock() -> Generator[None]:
    _make_owned_dir(LOCK_FILE.parent)
    if LOCK_FILE.is_symlink():
        raise AdapterError(f"adapter lock must not be a symlink: {LOCK_FILE}")
    descriptor = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        if os.name != "posix":
            raise UnverifiedError("exclusive adapter locking is unverified on this platform")
        deadline = time.monotonic() + LOCK_TIMEOUT_SECONDS
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise UnverifiedError(
                        "another adapter process holds the project lock"
                    ) from None
                time.sleep(0.05)
        yield
    finally:
        os.close(descriptor)


def _replace_graph(staged: Path) -> GraphSwap:
    """Publish a graph while retaining prior graph/receipt rollback state."""
    _assert_directory(staged, "staged graph")
    backup = TEMP_DIR / "previous-graph"
    receipt_backup = TEMP_DIR / "previous-graph-receipt.json"
    for candidate in (backup, receipt_backup):
        if candidate.exists() or candidate.is_symlink():
            raise AdapterError(f"stale graph backup requires manual review: {candidate}")
    had_graph = GRAPH_DIR.exists()
    had_receipt = GRAPH_RECEIPT.exists()
    graph_moved = False
    receipt_moved = False
    graph_promoted = False
    try:
        if had_graph:
            _assert_directory(GRAPH_DIR, "existing graph")
            GRAPH_DIR.rename(backup)
            graph_moved = True
        if had_receipt:
            _assert_regular(GRAPH_RECEIPT, "existing graph receipt")
            GRAPH_RECEIPT.rename(receipt_backup)
            receipt_moved = True
        staged.rename(GRAPH_DIR)
        graph_promoted = True
    except BaseException:
        if graph_promoted and GRAPH_DIR.exists():
            _assert_directory(GRAPH_DIR, "failed replacement graph")
            shutil.rmtree(GRAPH_DIR)
        if graph_moved and backup.exists():
            backup.rename(GRAPH_DIR)
        if receipt_moved and receipt_backup.exists():
            receipt_backup.rename(GRAPH_RECEIPT)
        raise
    return GraphSwap(had_graph=had_graph, had_receipt=had_receipt)


def _restore_graph(swap: GraphSwap) -> None:
    """Restore the pre-build graph and receipt after a publication failure."""
    backup = TEMP_DIR / "previous-graph"
    receipt_backup = TEMP_DIR / "previous-graph-receipt.json"
    if GRAPH_DIR.exists():
        _assert_directory(GRAPH_DIR, "failed replacement graph")
        shutil.rmtree(GRAPH_DIR)
    with contextlib.suppress(FileNotFoundError):
        GRAPH_RECEIPT.unlink()
    if swap.had_graph:
        _assert_directory(backup, "previous graph")
        backup.rename(GRAPH_DIR)
    if swap.had_receipt:
        _assert_regular(receipt_backup, "previous graph receipt")
        receipt_backup.rename(GRAPH_RECEIPT)


def _commit_graph(swap: GraphSwap) -> None:
    """Discard prior derived state only after new evidence is durable."""
    backup = TEMP_DIR / "previous-graph"
    receipt_backup = TEMP_DIR / "previous-graph-receipt.json"
    if swap.had_graph:
        _assert_directory(backup, "previous graph")
        shutil.rmtree(backup)
    if swap.had_receipt:
        _assert_regular(receipt_backup, "previous graph receipt")
        receipt_backup.unlink()


def _evidence(
    command: str,
    completed: Completed,
    status: str,
    context: EvidenceContext,
) -> dict[str, object]:
    evidence: dict[str, object] = {
        "schema_version": 2,
        "command": command,
        "status": status,
        "returncode": completed.returncode,
        "duration_ms": completed.duration_ms,
        "stdout": {
            "bytes": completed.stdout_bytes,
            "sha256": completed.stdout_sha256,
        },
        "stderr": {
            "bytes": completed.stderr_bytes,
            "sha256": completed.stderr_sha256,
        },
        "output_truncated": completed.truncated,
        "output_limit_exceeded": completed.output_limit_exceeded,
        "background_processes_terminated": completed.background_processes_terminated,
        "timed_out": completed.timed_out,
        "graft": {
            "package": EXPECTED_PACKAGE,
            "version": EXPECTED_GRAFT,
            "source_tag_commit": EXPECTED_COMMIT,
            "artifact_build_provenance": "UNVERIFIED",
        },
        "root": str(ROOT),
        "graph_dir": str(GRAPH_DIR),
        "authority": "derived-advisory-evidence",
    }
    if context.source is not None:
        evidence["source"] = dict(context.source)
        evidence["source_changed_during_run"] = context.source_changed
    if context.parameters is not None:
        evidence["parameters"] = dict(context.parameters)
    if context.runtime is not None:
        graft = evidence["graft"]
        if isinstance(graft, dict):
            graft.update(
                {
                    "cli_sha256": context.runtime["cli_sha256"],
                    "manifest_sha256": context.runtime["manifest_sha256"],
                    "installed_tree_sha256": context.runtime["installed_tree_sha256"],
                    "node_path": context.runtime["node_path"],
                    "node_sha256": context.runtime["node_sha256"],
                    "node_provenance": context.runtime["node_provenance"],
                }
            )
    return evidence


def _evidence_parameters(arguments: argparse.Namespace) -> dict[str, object]:
    values: dict[str, object] = {}
    for name in ("limit",):
        value = getattr(arguments, name, None)
        if value is not None:
            values[name] = value
    for name in ("query",):
        value = getattr(arguments, name, None)
        if isinstance(value, str):
            values[f"{name}_chars"] = len(value)
            values[f"{name}_sha256"] = hashlib.sha256(value.encode()).hexdigest()
    if hasattr(arguments, "source"):
        values["source"] = bool(arguments.source)
    return values


def _graph_receipt(
    graph: Mapping[str, object],
    source: Mapping[str, object],
    runtime: Mapping[str, str],
) -> dict[str, object]:
    return {
        "schema_version": 2,
        "mode": "bounded-structural-cli",
        "capabilities": {"deep": False, "lsp": False, "mcp": False},
        "build_arguments": [
            "build",
            str(ROOT),
            "--no-gitignore",
            "--no-ignore",
            "--no-reuse",
        ],
        "graph_wiring_sha256": graph["wiring_sha256"],
        "graph_tree_sha256": graph["tree_sha256"],
        "graph_tree_files": graph["tree_files"],
        "graph_tree_bytes": graph["tree_bytes"],
        "source": dict(source),
        "runtime": {
            "package": EXPECTED_PACKAGE,
            "version": EXPECTED_GRAFT,
            "cli_sha256": runtime["cli_sha256"],
            "manifest_sha256": runtime["manifest_sha256"],
            "installed_tree_sha256": runtime["installed_tree_sha256"],
            "node_path": runtime["node_path"],
            "node_sha256": runtime["node_sha256"],
            "node_provenance": runtime["node_provenance"],
        },
        "authority": "adapter-owned-provenance-receipt",
    }


def _require_graph_receipt(
    graph: Mapping[str, object],
    source: Mapping[str, object],
    runtime: Mapping[str, str],
) -> None:
    if not GRAPH_RECEIPT.exists() and not GRAPH_RECEIPT.is_symlink():
        raise UnverifiedError("adapter graph receipt is absent; run adapter build")
    _assert_regular(GRAPH_RECEIPT, "adapter graph receipt")
    receipt = _read_json(GRAPH_RECEIPT, "adapter graph receipt")
    if receipt != _graph_receipt(graph, source, runtime):
        raise AdapterError("graph receipt does not match current source, graph, and runtime")


def _omitted_value_evidence(value: object) -> dict[str, object]:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return {
        "items": len(value) if isinstance(value, (dict, list)) else None,
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def _project_check_output(
    value: Mapping[str, object],
) -> tuple[dict[str, object], list[str], dict[str, object]]:
    """Return a compact, project-owned projection with no upstream prose."""
    context = cast(dict[str, object], value["context"])
    graph = cast(dict[str, object], value["graph"])
    omitted: list[str] = ["context"]
    omitted_evidence: dict[str, object] = {"context": _omitted_value_evidence(context)}
    drift: dict[str, int] = {}
    for name in CHECK_GRAPH_LIST_KEYS:
        entries = cast(list[object], graph[name])
        omitted.append(f"graph.{name}")
        omitted_evidence[f"graph.{name}"] = _omitted_value_evidence(entries)
        if name != "pendingIds":
            drift[name] = len(entries)
    result: dict[str, object] = {
        "context_status": {
            "status": "NOT_APPLICABLE",
            "reason": "model-backed context is outside structural F1",
        },
        "graph": {
            "ok": graph["ok"],
            "missing": graph["missing"],
            "nodes": graph["nodes"],
            "pending": graph["pending"],
            "drift": drift,
        },
    }
    return result, omitted, omitted_evidence


def _public_result(
    completed: Completed,
    evidence: Mapping[str, object],
) -> tuple[object | None, str | None, list[str], dict[str, object]]:
    """Select only the validated output needed by the public envelope."""
    command = evidence.get("command")
    status = evidence.get("status")
    result: object | None = None
    omitted: list[str] = []
    omitted_evidence: dict[str, object] = {}
    decoded: object | None = None
    with contextlib.suppress(AdapterError):
        decoded = _decode_json(completed.stdout, "Graft output")
    result_trust: str | None = None
    if status == "PASS" and command == "check" and isinstance(decoded, dict):
        result, omitted, omitted_evidence = _project_check_output(decoded)
        result_trust = "project-owned-projection-of-validated-untrusted-output"
    elif status == "PASS" and command == "ask" and isinstance(decoded, dict):
        result = dict(decoded)
        if "saved" in result:
            saved = result.pop("saved")
            omitted.append("saved")
            omitted_evidence["saved"] = _omitted_value_evidence(saved)
        result_trust = "untrusted-derived-navigation-evidence"
    elif completed.stdout:
        omitted.append("stdout")
        omitted_evidence["stdout"] = {
            "bytes": completed.stdout_bytes,
            "sha256": completed.stdout_sha256,
        }
    return result, result_trust, omitted, omitted_evidence


def _public_evidence(evidence: Mapping[str, object]) -> dict[str, object]:
    """Remove host-path length and disclosure from the public JSON envelope."""
    public = dict(evidence)
    public["root"] = "."
    public["graph_dir"] = GRAPH_DIR.relative_to(ROOT).as_posix()

    graft = evidence.get("graft")
    if isinstance(graft, dict):
        public_graft = dict(graft)
        public_graft.pop("node_path", None)
        public["graft"] = public_graft

    graph = evidence.get("graph")
    if isinstance(graph, dict):
        public_graph = dict(graph)
        languages = public_graph.pop("languages", None)
        if languages is not None:
            language_evidence = _omitted_value_evidence(languages)
            public_graph["language_count"] = language_evidence["items"]
            public_graph["languages_sha256"] = language_evidence["sha256"]
        public["graph"] = public_graph

    tools = evidence.get("tools")
    if isinstance(tools, dict):
        public_tools: dict[str, object] = {}
        for name, identity in tools.items():
            if isinstance(identity, dict):
                public_identity = dict(identity)
                public_identity.pop("path", None)
                public_tools[name] = public_identity
            else:
                public_tools[name] = identity
        public["tools"] = public_tools

    for name in ("source", "source_before"):
        source = evidence.get(name)
        if not isinstance(source, dict):
            continue
        public_source = dict(source)
        git = source.get("git")
        if isinstance(git, dict):
            public_git = dict(git)
            public_git.pop("path", None)
            public_source["git"] = public_git
        public[name] = public_source
    return public


def _payload(completed: Completed, evidence: Mapping[str, object]) -> dict[str, object]:
    result, result_trust, omitted, omitted_evidence = _public_result(completed, evidence)
    status = evidence.get("status")
    payload: dict[str, object] = {
        **_public_evidence(evidence),
        "evidence_file": EVIDENCE_FILE.relative_to(ROOT).as_posix(),
    }
    if result is not None:
        payload["result"] = result
    if result_trust is not None:
        payload["result_trust"] = result_trust
    if completed.stderr and status != "PASS":
        payload["diagnostics"] = completed.stderr
        payload["diagnostics_trust"] = "untrusted-upstream-diagnostic-text"
    elif completed.stderr:
        omitted.append("stderr")
        omitted_evidence["stderr"] = {
            "bytes": completed.stderr_bytes,
            "sha256": completed.stderr_sha256,
        }
    if omitted:
        payload["omitted_upstream_fields"] = omitted
    if omitted_evidence:
        payload["omitted_upstream_field_evidence"] = omitted_evidence
    return payload


def _graft_command(
    node: Path, arguments: Sequence[str], graph_dir: Path | None = None
) -> list[str]:
    selected_graph_dir = GRAPH_DIR if graph_dir is None else graph_dir
    return [str(node), str(GRAFT_CLI), "--dir", str(selected_graph_dir), *arguments]


def _check_fresh(node: Path, environment: Mapping[str, str], tracked: set[str]) -> Completed:
    return _check_fresh_at(node, environment, tracked, GRAPH_DIR)


def _check_fresh_at(
    node: Path,
    environment: Mapping[str, str],
    tracked: set[str],
    graph_dir: Path,
) -> Completed:
    completed = _supervise(
        _graft_command(node, ["check", str(ROOT), "--json"], graph_dir),
        cwd=ROOT,
        environment={**environment, "GRAFT_DIR": str(graph_dir)},
        temp_root=TEMP_DIR,
    )
    _assert_state_tree()
    if completed.returncode or completed.truncated:
        raise UnverifiedError("graph freshness check did not pass; run adapter build")
    report = _decode_json(completed.stdout, "graph freshness output")
    graph = report.get("graph") if isinstance(report, dict) else None
    if not isinstance(graph, dict) or graph.get("ok") is not True:
        raise UnverifiedError("graph is absent or stale; run adapter build")
    _validate_graph(tracked, graph_dir)
    return completed


def _command_arguments(arguments: argparse.Namespace) -> list[str]:
    command = arguments.command
    choices = {
        "build": [
            "build",
            str(ROOT),
            "--no-gitignore",
            "--no-ignore",
            "--no-reuse",
        ],
        "check": ["check", str(ROOT), "--json"],
        "ask": [
            "ask",
            str(getattr(arguments, "query", "")),
            str(ROOT),
            "--limit",
            str(getattr(arguments, "limit", 8)),
            "--json",
            "--no-refresh",
        ],
    }
    try:
        values = choices[command]
    except KeyError as error:
        raise AdapterError(f"unsupported command: {command}") from error
    if command == "ask" and arguments.source:
        values.append("--source")
    return values


def _assess_result(
    command: str,
    completed: Completed,
    context: RunContext,
) -> tuple[str, dict[str, object] | None]:
    status = "PASS" if completed.returncode == 0 and not completed.truncated else "FAIL"
    graph_summary: dict[str, object] | None = None
    if command == "build" and status == "PASS":
        if any(line.lstrip().startswith("✗") for line in completed.stderr.splitlines()):
            status = "FAIL"
        else:
            graph_summary = _validate_graph(context.tracked, context.run_graph_dir)
            _check_fresh_at(
                context.node,
                context.environment,
                context.tracked,
                context.run_graph_dir,
            )
    if command == "check" and status == "PASS":
        try:
            checked = _decode_json(completed.stdout, "Graft check output")
        except AdapterError:
            status = "FAIL"
        else:
            graph = checked.get("graph") if isinstance(checked, dict) else None
            if not isinstance(graph, dict) or graph.get("ok") is not True:
                status = "FAIL"
            else:
                graph_summary = _validate_graph(context.tracked, context.run_graph_dir)
    if command not in {"build", "check"} and status == "PASS":
        graph_summary = _validate_graph(context.tracked, context.run_graph_dir)
    return status, graph_summary


def _expects_json(arguments: argparse.Namespace) -> bool:
    return arguments.command != "build"


def _finite_number(value: object, *, minimum: float, maximum: float) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value) and minimum <= value <= maximum
    except (OverflowError, TypeError, ValueError):
        return False


def _pointer_source(pointer: object, tracked: set[str]) -> str | None:
    if not isinstance(pointer, str) or not pointer or len(pointer) > MAX_POINTER_CHARS:
        return None
    path, separator, span = pointer.partition(":L")
    line_range: tuple[int, int] | None = None
    if separator:
        line_range = _span_bounds(f"L{span}")
        if line_range is None:
            return None
    if path not in tracked or Path(path).suffix.lower() not in SOURCE_SUFFIXES:
        return None
    source_path = ROOT / path
    _assert_regular(source_path, "ask pointer source")
    if line_range is not None:
        raw = source_path.read_bytes()
        line_count = max(1, raw.count(b"\n") + (not raw.endswith(b"\n")))
        if line_range[1] > line_count:
            return None
    return path


def _expected_pointer_code(pointer: object, tracked: set[str]) -> str | None:
    if not isinstance(pointer, str) or _pointer_source(pointer, tracked) is None:
        return None
    path, separator, span_text = pointer.partition(":L")
    bounds = _span_bounds(f"L{span_text}") if separator else None
    if bounds is None:
        return None
    raw = (ROOT / path).read_bytes()
    if raw.startswith(b"\xfe\xff"):
        return None
    if raw.startswith(b"\xff\xfe"):
        source = raw[2:].decode("utf-16le", errors="replace")
    else:
        source = raw.decode("utf-8", errors="replace")
    selected = source.split("\n")[bounds[0] - 1 : bounds[1]]
    if len(selected) > MAX_INLINE_SOURCE_LINES:
        omitted = len(selected) - MAX_INLINE_SOURCE_LINES
        selected = [
            *selected[:MAX_INLINE_SOURCE_LINES],
            f"… (+{omitted} more lines; open {path}:L{bounds[0]}-L{bounds[1]})",
        ]
    return "\n".join(selected) or None


def _valid_concept_pointer(pointer: object, tracked: set[str]) -> bool:
    """Accept only concept pointers whose comma-separated sources are tracked."""
    if not isinstance(pointer, str) or not pointer or len(pointer) > MAX_POINTER_CHARS:
        return False
    paths = [path.strip() for path in pointer.split(",")]
    return bool(paths) and all(
        path and path in tracked and Path(path).suffix.lower() in SOURCE_SUFFIXES for path in paths
    )


def _valid_external_pointer(pointer: object) -> bool:
    """Validate an opaque unresolved-module label without treating it as a path."""
    if not isinstance(pointer, str) or not pointer or len(pointer) > MAX_LABEL_CHARS:
        return False
    return not any(ord(character) < FIRST_CONTROL_CODEPOINT for character in pointer)


def _valid_string_list(value: object, *, allow_empty: bool = True) -> TypeGuard[list[str]]:
    return isinstance(value, list) and all(
        isinstance(item, str)
        and (allow_empty or bool(item))
        and len(item) <= MAX_LABEL_CHARS
        and not any(ord(character) < FIRST_CONTROL_CODEPOINT for character in item)
        and _utf8_encodable(item)
        for item in value
    )


def _utf8_encodable(value: str) -> bool:
    """Reject lone surrogates before they can enter promoted graph state."""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _valid_common_ask_hit(value: Mapping[str, object], include_source: bool) -> bool:
    relation = value.get("relation")
    title = value.get("title")
    snippet = value.get("snippet")
    scope = value.get("scope")
    code = value.get("code")
    return all(
        (
            value.keys() <= ASK_HIT_KEYS,
            isinstance(value.get("kind"), str),
            isinstance(title, str),
            len(title) <= MAX_TEXT_FIELD_CHARS if isinstance(title, str) else False,
            isinstance(snippet, str),
            len(snippet) <= MAX_TEXT_FIELD_CHARS if isinstance(snippet, str) else False,
            _finite_number(value.get("score"), minimum=0, maximum=1_000_000),
            relation is None or (isinstance(relation, str) and relation in EDGE_RELATIONS),
            "code" not in value or isinstance(code, str),
            include_source or "code" not in value,
            "scope" not in value or (isinstance(scope, str) and len(scope) <= MAX_LABEL_CHARS),
            "related" not in value or _valid_string_list(value.get("related"), allow_empty=False),
        )
    )


def _valid_structural_hit(value: Mapping[str, object], tracked: set[str]) -> bool:
    kind = value.get("kind")
    relation = value.get("relation")
    pointer = value.get("pointer")
    required_shape = (
        kind in {"caller", "callee"} and isinstance(relation, str) and "related" not in value
    )
    if not required_shape:
        return False
    if _pointer_source(pointer, tracked) is not None:
        return True
    return (
        kind == "callee"
        and relation in {"extends", "implements", "imports", "references"}
        and _valid_external_pointer(pointer)
    )


def _valid_lexical_hit(value: Mapping[str, object], tracked: set[str]) -> bool:
    kind = value.get("kind")
    relation = value.get("relation")
    pointer = value.get("pointer")
    if kind == "concept":
        return (
            relation is None and "scope" not in value and _valid_concept_pointer(pointer, tracked)
        )
    return (
        kind == "symbol"
        and relation is None
        and "related" not in value
        and _pointer_source(pointer, tracked) is not None
    )


def _valid_inline_code(
    value: Mapping[str, object], tracked: set[str], include_source: bool
) -> bool:
    expected = _expected_pointer_code(value.get("pointer"), tracked)
    if expected is None:
        return "code" not in value
    return not include_source or value.get("code") == expected


def _valid_ask_hit(
    value: object,
    tracked: set[str],
    include_source: bool,
    mode: str,
) -> bool:
    if not isinstance(value, dict) or not _valid_common_ask_hit(value, include_source):
        return False
    kind = value.get("kind")
    if not isinstance(kind, str) or kind not in {"concept", "symbol", "caller", "callee"}:
        return False
    if not _valid_inline_code(value, tracked, include_source):
        return False
    if mode == "structural":
        return _valid_structural_hit(value, tracked)
    return _valid_lexical_hit(value, tracked)


def _valid_saved(value: object) -> bool:
    return (
        isinstance(value, dict)
        and value.keys() == {"files", "baselineChars"}
        and all(
            isinstance(item, int) and not isinstance(item, bool) and item >= 0
            for item in value.values()
        )
    )


def _valid_scopes(value: object) -> bool:
    if not isinstance(value, dict) or value.keys() != {"federated", "alsoMatched"}:
        return False
    if not _valid_string_list(value["federated"]):
        return False
    also_matched = value["alsoMatched"]
    return isinstance(also_matched, list) and all(
        isinstance(item, dict)
        and item.keys() == {"scope", "bestId"}
        and isinstance(item["scope"], str)
        and isinstance(item["bestId"], str)
        and bool(item["bestId"])
        and len(item["scope"]) <= MAX_LABEL_CHARS
        and len(item["bestId"]) <= MAX_POINTER_CHARS
        for item in also_matched
    )


def _valid_ask_mode_fields(value: Mapping[str, object], mode: str, hits: list[object]) -> bool:
    if mode == "empty":
        return not hits and not {"coverage", "coverageStrong", "subject"} & value.keys()
    if mode == "structural":
        subject = value.get("subject")
        return (
            bool(hits)
            and isinstance(subject, str)
            and bool(subject)
            and not {"coverage", "coverageStrong", "scopes"} & value.keys()
        )
    return (
        bool(hits)
        and "subject" not in value
        and _finite_number(value.get("coverage"), minimum=0, maximum=1)
        and _finite_number(value.get("coverageStrong"), minimum=0, maximum=1)
    )


def _valid_ask_output(
    value: dict[str, object], arguments: argparse.Namespace, tracked: set[str]
) -> bool:
    if not value.keys() <= ASK_KEYS or value.get("query") != arguments.query:
        return False
    mode = value.get("mode")
    hits = value.get("hits")
    if (
        not isinstance(mode, str)
        or mode not in {"empty", "lexical", "structural"}
        or not isinstance(hits, list)
    ):
        return False
    valid_hits = len(hits) <= arguments.limit and all(
        _valid_ask_hit(hit, tracked, arguments.source, mode) for hit in hits
    )
    valid_note = "note" not in value or isinstance(value.get("note"), str)
    valid_saved = "saved" not in value or (arguments.source and _valid_saved(value.get("saved")))
    valid_scopes = "scopes" not in value or (
        mode in {"empty", "lexical"} and _valid_scopes(value.get("scopes"))
    )
    return (
        valid_hits
        and valid_note
        and valid_saved
        and valid_scopes
        and _valid_ask_mode_fields(value, mode, hits)
    )


def _valid_check_output(value: Mapping[str, object]) -> bool:
    if value.keys() != CHECK_KEYS:
        return False
    context = value.get("context")
    graph = value.get("graph")
    if not isinstance(context, dict) or context.keys() != CHECK_CONTEXT_KEYS:
        return False
    if not isinstance(graph, dict) or graph.keys() != CHECK_GRAPH_KEYS:
        return False
    context_flags = all(isinstance(context.get(name), bool) for name in ("missing", "ok"))
    content_drift = context.get("contentDrift")
    valid_content_drift = isinstance(content_drift, list) and all(
        isinstance(item, dict)
        and item.keys() == {"from", "path", "to"}
        and isinstance(item["path"], str)
        and bool(item["path"])
        and len(item["path"]) <= MAX_POINTER_CHARS
        and not any(ord(character) < FIRST_CONTROL_CODEPOINT for character in item["path"])
        and isinstance(item["from"], str)
        and re.fullmatch(r"[0-9a-f]{8}", item["from"]) is not None
        and isinstance(item["to"], str)
        and re.fullmatch(r"[0-9a-f]{8}", item["to"]) is not None
        for item in content_drift
    )
    context_lists = all(
        _valid_string_list(context.get(name), allow_empty=False)
        for name in ("coverage", "indexDrift", "removed")
    )
    context_ok = (
        not context["missing"]
        and not content_drift
        and not any(context[name] for name in ("coverage", "indexDrift", "removed"))
    )
    if (
        not context_flags
        or not valid_content_drift
        or not context_lists
        or context["ok"] is not context_ok
    ):
        return False
    graph_flags = all(isinstance(graph.get(name), bool) for name in ("missing", "ok"))
    graph_lists = all(
        _valid_string_list(graph.get(name), allow_empty=False) for name in CHECK_GRAPH_LIST_KEYS
    )
    nodes = graph.get("nodes")
    pending = graph.get("pending")
    pending_ids = graph.get("pendingIds")
    graph_ok = not graph["missing"] and not any(
        graph[name] for name in ("added", "changed", "removed", "stale")
    )
    return (
        graph_flags
        and graph_lists
        and graph["ok"] is graph_ok
        and isinstance(nodes, int)
        and not isinstance(nodes, bool)
        and nodes >= 0
        and isinstance(pending, int)
        and not isinstance(pending, bool)
        and 0 <= pending <= nodes
        and isinstance(pending_ids, list)
        and pending == len(pending_ids)
    )


def _valid_json_output(
    arguments: argparse.Namespace,
    completed: Completed,
    tracked: set[str],
) -> bool:
    if completed.truncated:
        return False
    try:
        value = _decode_json(completed.stdout, f"Graft {arguments.command} output")
    except AdapterError:
        return False
    required = JSON_OUTPUT_KEYS.get(arguments.command)
    if not isinstance(value, dict) or required is None or not required <= value.keys():
        return False
    if arguments.command == "ask":
        return _valid_ask_output(value, arguments, tracked)
    return arguments.command != "check" or _valid_check_output(value)


def _mark_attempt(command: str, parameters: Mapping[str, object] | None = None) -> None:
    """Replace any old PASS evidence before a stateful attempt proceeds."""
    value: dict[str, object] = {
        "schema_version": 2,
        "command": command,
        "status": "UNVERIFIED",
        "attempt_started": True,
        "authority": "derived-advisory-evidence",
    }
    if parameters is not None:
        value["parameters"] = dict(parameters)
    _atomic_json(EVIDENCE_FILE, value)


def _prepare_execution(arguments: argparse.Namespace) -> RunContext:
    """Bind source, runtime, tool, graph, and command identities under the lock."""
    _assert_state_tree()
    _prepare_state()
    _mark_attempt(arguments.command, _evidence_parameters(arguments))
    git = _resolve_executable("git")
    git_identity = _tool_identity(git)
    tracked = _source_scope(git)
    source_before = _source_snapshot(tracked, git)
    _require_tool_identity(git, git_identity, "Git")
    _runtime_lock()
    node = _resolve_executable("node")
    environment = _minimal_environment(node, git=git)
    _installed_runtime(node_identity=_tool_identity(node))
    _probe_node(node)
    installed = _probe_graft(node)
    if arguments.command == "build":
        run_graph_dir = Path(tempfile.mkdtemp(prefix="graph-build-", dir=TEMP_DIR))
    else:
        current_graph = _validate_graph(tracked)
        _require_graph_receipt(current_graph, source_before, installed)
        run_graph_dir = GRAPH_DIR
    if arguments.command == "ask":
        _check_fresh(node, environment, tracked)
    return RunContext(
        tracked=tracked,
        source_before=source_before,
        node=node,
        git=git,
        git_identity=git_identity,
        environment=environment,
        command_arguments=_command_arguments(arguments),
        installed=installed,
        run_graph_dir=run_graph_dir,
    )


def _promote_build(context: RunContext) -> GraphSwap:
    """Publish an already validated staged graph while retaining rollback state."""
    _validate_graph(context.tracked, context.run_graph_dir)
    return _replace_graph(context.run_graph_dir)


def _run_structural(context: RunContext) -> Completed:
    """Run only the command constructed by the closed adapter interface."""
    environment = {**context.environment, "GRAFT_DIR": str(context.run_graph_dir)}
    completed = _supervise(
        _graft_command(context.node, context.command_arguments, context.run_graph_dir),
        cwd=ROOT,
        environment=environment,
        temp_root=TEMP_DIR,
    )
    _assert_state_tree()
    return completed


def _remove_staged_graph(context: RunContext) -> None:
    if context.run_graph_dir == GRAPH_DIR or not context.run_graph_dir.exists():
        return
    _assert_directory(context.run_graph_dir, "staged graph")
    shutil.rmtree(context.run_graph_dir)


def _persist_execution(
    command: str,
    context: RunContext,
    publication: ExecutionPublication,
) -> None:
    """Publish a graph/receipt/evidence transaction or preserve its predecessor."""
    swap: GraphSwap | None = None
    try:
        if publication.status == "PASS" and publication.graph is not None:
            receipt = _graph_receipt(
                publication.graph,
                publication.source,
                publication.runtime,
            )
            if command == "build":
                swap = _promote_build(context)
                _atomic_json(GRAPH_RECEIPT, receipt)
            else:
                _require_graph_receipt(
                    publication.graph,
                    publication.source,
                    publication.runtime,
                )
        _atomic_json(EVIDENCE_FILE, publication.evidence)
    except BaseException:
        if swap is not None:
            _restore_graph(swap)
        raise
    if swap is not None:
        _commit_graph(swap)


def _finish_execution(
    arguments: argparse.Namespace,
    context: RunContext,
    completed: Completed,
) -> dict[str, object]:
    """Validate post-state, write current evidence, and return the JSON envelope."""
    status, graph = _assess_result(
        arguments.command,
        completed,
        context,
    )
    if status == "PASS" and _expects_json(arguments):
        valid_output = _valid_json_output(arguments, completed, context.tracked)
        status = "PASS" if valid_output else "FAIL"
    _assert_state_tree()
    installed_after = _probe_graft(context.node)
    if installed_after != context.installed:
        status = "FAIL"
    _require_tool_identity(context.git, context.git_identity, "Git")
    source_after = _source_snapshot(context.tracked, context.git)
    source_changed = context.source_before != source_after
    if source_changed:
        status = "FAIL"
    evidence = _evidence(
        arguments.command,
        completed,
        status,
        EvidenceContext(
            source=source_after,
            source_changed=source_changed,
            parameters=_evidence_parameters(arguments),
            runtime=installed_after,
        ),
    )
    if source_changed:
        evidence["source_before"] = context.source_before
    if graph is not None:
        evidence["graph"] = graph
    _persist_execution(
        arguments.command,
        context,
        ExecutionPublication(
            evidence=evidence,
            graph=graph,
            source=source_after,
            runtime=installed_after,
            status=status,
        ),
    )
    _remove_staged_graph(context)
    return _payload(completed, evidence)


def _execute(arguments: argparse.Namespace) -> dict[str, object]:
    _reject_legacy_root_state()
    _assert_state_tree()
    with _exclusive_lock(), _defer_stop_signals():
        context = _prepare_execution(arguments)
        try:
            completed = _run_structural(context)
            try:
                return _finish_execution(arguments, context, completed)
            except (
                AdapterError,
                OSError,
                RecursionError,
                UnicodeError,
                json.JSONDecodeError,
                subprocess.SubprocessError,
            ) as error:
                raise _executed_error(error) from error
        except BaseException:
            _remove_staged_graph(context)
            raise


def _reject_npm_configuration() -> None:
    """Reject project-controlled npm configuration before lifecycle scripts run."""
    for npmrc in (ROOT / ".npmrc", RUNTIME_DIR / ".npmrc"):
        if npmrc.exists() or npmrc.is_symlink():
            raise AdapterError(
                f"npm configuration is not allowed for the reviewed install: {npmrc}"
            )


def _prepare_install() -> InstallContext:
    """Bind source, manifests, and system tool identities under the project lock."""
    _assert_state_tree()
    _prepare_state()
    _mark_attempt("install")
    _assert_directory(RUNTIME_DIR, "runtime directory")
    provenance = _runtime_lock()
    _assert_path_chain(RUNTIME_DIR / "node_modules")
    _reject_stale_runtime_transactions()
    _reject_npm_configuration()
    node = _resolve_executable("node")
    npm = _resolve_executable("npm")
    git = _resolve_executable("git")
    node_identity = _tool_identity(node)
    npm_identity = _tool_identity(npm)
    git_identity = _tool_identity(git)
    tracked = _source_scope(git)
    environment = _minimal_environment(node, install=True, git=git, npm=npm)
    npm_probe = _supervise(
        [str(node), str(npm), "--version"],
        cwd=RUNTIME_DIR,
        environment=environment,
        timeout=10,
    )
    if (
        npm_probe.returncode
        or npm_probe.truncated
        or npm_probe.stderr
        or NPM_VERSION_RE.fullmatch(npm_probe.stdout) is None
    ):
        raise UnverifiedError(f"npm must be exactly {EXPECTED_NPM} for the reviewed install")
    return InstallContext(
        tracked=tracked,
        source_before=_source_snapshot(tracked, git),
        node=node,
        npm=npm,
        git=git,
        node_identity=node_identity,
        npm_identity=npm_identity,
        git_identity=git_identity,
        node_version=_probe_node(node),
        npm_version=npm_probe.stdout.strip(),
        provenance=provenance,
        environment=environment,
    )


def _reject_stale_runtime_transactions(*, include_staging: bool = True) -> None:
    """Refuse a new swap while prior backup or quarantine state exists."""
    transactions = [
        (RUNTIME_BACKUP, "install backup"),
        (RUNTIME_QUARANTINE, "failed-runtime quarantine"),
    ]
    if include_staging:
        transactions.append((RUNTIME_STAGING, "incomplete install staging"))
    for candidate, label in transactions:
        _assert_path_chain(candidate)
        if candidate.exists() or candidate.is_symlink():
            raise AdapterError(f"stale {label} requires manual review: {candidate}")


def _replace_node_modules(staged: Path) -> bool:
    """Atomically replace only the validated project-local installed tree."""
    destination = RUNTIME_DIR / "node_modules"
    backup = RUNTIME_BACKUP
    _reject_stale_runtime_transactions(include_staging=False)
    had_destination = destination.exists()
    if had_destination:
        _assert_directory(destination, "existing node_modules")
        destination.rename(backup)
    try:
        staged.rename(destination)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
        if had_destination and backup.exists():
            backup.rename(destination)
        raise
    return had_destination


def _restore_node_modules(result: InstallResult) -> None:
    """Restore the exact pre-install runtime after any post-swap failure."""
    if not result.replaced:
        return
    destination = RUNTIME_DIR / "node_modules"
    backup = RUNTIME_BACKUP
    quarantine = RUNTIME_QUARANTINE
    if quarantine.exists() or quarantine.is_symlink():
        raise AdapterError(f"stale failed-runtime quarantine requires manual review: {quarantine}")
    moved_destination = False
    if destination.exists():
        _assert_directory(destination, "failed installed node_modules")
        destination.rename(quarantine)
        moved_destination = True
    try:
        if result.had_previous:
            _assert_directory(backup, "previous node_modules")
            backup.rename(destination)
    except BaseException:
        if moved_destination and quarantine.exists():
            quarantine.rename(destination)
        raise
    if moved_destination:
        try:
            shutil.rmtree(quarantine)
        except OSError as error:
            raise AdapterError(
                "the prior runtime was restored, but cleanup of the failed replacement "
                f"did not finish; review the quarantine: {quarantine}"
            ) from error


def _commit_node_modules(result: InstallResult) -> None:
    """Discard the pre-install backup only after final evidence is durable."""
    if not result.replaced or not result.had_previous:
        return
    backup = RUNTIME_BACKUP
    _assert_directory(backup, "previous node_modules")
    try:
        shutil.rmtree(backup)
    except OSError as error:
        raise InstallCommitError(
            "the validated new runtime is active, but cleanup of the prior runtime "
            f"did not finish; review the stale backup before retrying: {backup}"
        ) from error


def _staging_environment(context: InstallContext, staging: Path) -> dict[str, str]:
    """Return a secret-minimal npm environment rooted in disposable state."""
    return {
        **context.environment,
        "HOME": str(staging / "home"),
        "USERPROFILE": str(staging / "home"),
        "XDG_CACHE_HOME": str(staging / "cache"),
        "XDG_CONFIG_HOME": str(staging / "home" / "config"),
        "XDG_DATA_HOME": str(staging / "home" / "data"),
        "TEMP": str(staging / "tmp"),
        "TMP": str(staging / "tmp"),
        "TMPDIR": str(staging / "tmp"),
        "npm_config_cache": str(staging / "cache" / "npm"),
    }


def _stage_install(context: InstallContext) -> InstallResult:
    """Run npm lifecycle scripts in removable project state and validate the result."""
    staging = RUNTIME_STAGING
    _assert_path_chain(staging)
    staging.mkdir(mode=0o700)
    result: InstallResult | None = None
    completed: Completed | None = None
    swapped = False
    had_previous = False
    try:
        shutil.copy2(PACKAGE_JSON, staging / "package.json")
        shutil.copy2(PACKAGE_LOCK, staging / "package-lock.json")
        for name in ("home", "cache", "tmp"):
            (staging / name).mkdir(mode=0o700)
        completed = _supervise(
            [
                str(context.node),
                str(context.npm),
                "ci",
                "--no-audit",
                "--no-fund",
            ],
            cwd=staging,
            environment=_staging_environment(context, staging),
            temp_root=staging / "tmp",
        )
        replaced = completed.returncode == 0 and not completed.truncated
        if replaced:
            node_modules = staging / "node_modules"
            _installed_runtime_at(node_modules)
            had_previous = _replace_node_modules(node_modules)
            swapped = True
        result = InstallResult(
            completed=completed,
            replaced=replaced,
            had_previous=had_previous,
        )
    except BaseException as error:
        rollback = result
        if rollback is None and swapped and completed is not None:
            rollback = InstallResult(completed, replaced=True, had_previous=had_previous)
        if rollback is not None:
            _restore_node_modules(rollback)
        with contextlib.suppress(OSError):
            shutil.rmtree(staging)
        if completed is not None:
            raise _executed_error(error) from error
        raise
    try:
        shutil.rmtree(staging)
    except BaseException as error:
        if result is not None:
            _restore_node_modules(result)
            raise _executed_error(error) from error
        raise
    if result is None:
        raise AdapterError("install did not produce a supervised result")
    return result


def _finish_install(context: InstallContext, result: InstallResult) -> dict[str, object]:
    """Validate install post-state, persist receipt/evidence, and return JSON."""
    completed = result.completed
    status = "PASS" if result.replaced else "FAIL"
    _require_tool_identity(context.node, context.node_identity, "Node")
    _require_tool_identity(context.npm, context.npm_identity, "npm")
    _require_tool_identity(context.git, context.git_identity, "Git")
    installed: dict[str, str] | None = None
    if status == "PASS":
        _runtime_lock()
        installed = _installed_runtime(require_receipt=False)
        _atomic_json(
            INSTALL_RECEIPT,
            _install_receipt(
                installed,
                node_identity=context.node_identity,
                npm_identity=context.npm_identity,
            ),
        )
        installed = _probe_graft(context.node)
    tracked_after = _source_scope(context.git)
    source_after = _source_snapshot(tracked_after, context.git)
    source_changed = tracked_after != context.tracked or context.source_before != source_after
    if source_changed:
        status = "FAIL"
        with contextlib.suppress(FileNotFoundError):
            INSTALL_RECEIPT.unlink()
    evidence = _evidence(
        "install",
        completed,
        status,
        EvidenceContext(
            source=source_after,
            source_changed=source_changed,
            runtime=installed if status == "PASS" else None,
        ),
    )
    if source_changed:
        evidence["source_before"] = context.source_before
    evidence.update(
        {
            "provenance": context.provenance,
            "node_version": context.node_version,
            "npm_version": context.npm_version,
            "tools": {"node": context.node_identity, "npm": context.npm_identity},
            "install_scripts_authorized": True,
            "npm_ci_attempted": True,
            "isolated_staging": True,
        }
    )
    _atomic_json(EVIDENCE_FILE, evidence)
    return _payload(completed, evidence)


def _install() -> dict[str, object]:
    _assert_state_tree()
    _assert_path_chain(RUNTIME_DIR / "node_modules")
    _reject_npm_configuration()
    with _exclusive_lock():
        context = _prepare_install()
        with _defer_stop_signals():
            result: InstallResult | None = None
            try:
                result = _stage_install(context)
                _assert_state_tree()
                report = _finish_install(context, result)
            except BaseException as error:
                if result is not None:
                    try:
                        _restore_node_modules(result)
                    except BaseException as recovery_error:
                        raise _executed_error(recovery_error) from recovery_error
                    raise _executed_error(error) from error
                raise
            if report["status"] == "PASS":
                _commit_node_modules(result)
            else:
                _restore_node_modules(result)
            return report


def _tracked_removal_evidence() -> dict[str, object]:
    """Attest to tracked files below removal roots without publishing their names."""
    relative_targets = [path.relative_to(ROOT).as_posix() for path in REMOVAL_TARGETS]
    tracked = _nul_paths(
        _git("ls-files", "-z", "--", *relative_targets),
        "tracked files in removal targets",
    )
    names: list[str] = []
    for relative in tracked:
        if relative.is_absolute() or ".." in relative.parts:
            raise AdapterError("Git reported an out-of-scope removal path")
        candidate = ROOT / relative
        if not any(
            candidate == target or candidate.is_relative_to(target) for target in REMOVAL_TARGETS
        ):
            raise AdapterError("Git reported a tracked file outside removal targets")
        names.append(PurePosixPath(relative).as_posix())
    evidence = _omitted_value_evidence(sorted(names))
    return {"count": len(names), "sha256": evidence["sha256"]}


def _tree_inventory(root: Path) -> set[Path]:
    """Inventory one removal root without following any nested symlink."""
    if not root.exists() and not root.is_symlink():
        return set()
    paths = {root}
    if root.is_symlink() or not root.is_dir():
        return paths
    for current, directories, files in os.walk(root, followlinks=False):
        paths.update(Path(current) / name for name in [*directories, *files])
    return paths


def _owned_runtime_tree(root: Path, paths: set[Path]) -> set[Path]:
    """Accept a runtime tree only when its local install receipt binds every byte."""
    try:
        installed = _installed_runtime_at(root)
        receipt_path = root / INSTALL_RECEIPT.name
        _assert_regular(receipt_path, "candidate runtime receipt")
        receipt = _read_json(receipt_path, "candidate runtime receipt")
        core = _install_receipt_core(installed)
        if not _valid_install_receipt(receipt, core):
            return set()
    except (AdapterError, OSError, RecursionError, UnicodeError, json.JSONDecodeError):
        return set()
    return paths


def _owned_staging_tree(paths: set[Path]) -> set[Path]:
    """Recognize only the empty, post-install staging layout created by the adapter."""
    expected = {
        RUNTIME_STAGING,
        RUNTIME_STAGING / "package.json",
        RUNTIME_STAGING / "package-lock.json",
        RUNTIME_STAGING / "home",
        RUNTIME_STAGING / "cache",
        RUNTIME_STAGING / "tmp",
    }
    try:
        _assert_regular(RUNTIME_STAGING / "package.json", "staged package manifest")
        _assert_regular(RUNTIME_STAGING / "package-lock.json", "staged package lock")
        for candidate in (
            RUNTIME_STAGING / "home",
            RUNTIME_STAGING / "cache",
            RUNTIME_STAGING / "tmp",
        ):
            _assert_directory(candidate, "staged private directory")
        valid = (
            paths == expected
            and _sha256(RUNTIME_STAGING / "package.json") == EXPECTED_PACKAGE_JSON_SHA256
            and _sha256(RUNTIME_STAGING / "package-lock.json") == EXPECTED_LOCK_SHA256
        )
    except (AdapterError, OSError):
        return set()
    return paths if valid else set()


def _valid_last_run_file() -> bool:
    try:
        value = _read_json(EVIDENCE_FILE, "adapter last-run evidence")
    except (AdapterError, OSError, RecursionError, UnicodeError, json.JSONDecodeError):
        return False
    return (
        isinstance(value, dict)
        and value.get("schema_version") == ADAPTER_SCHEMA_VERSION
        and value.get("authority") == "derived-advisory-evidence"
        and value.get("command") in {"ask", "build", "check", "install"}
        and value.get("status") in {"FAIL", "PASS", "UNVERIFIED"}
    )


def _valid_update_check_file(path: Path) -> bool:
    try:
        value = _read_json(path, "adapter update-check state")
    except (AdapterError, OSError, RecursionError, UnicodeError, json.JSONDecodeError):
        return False
    return (
        isinstance(value, dict)
        and value.keys() == {"checkedAt", "latest"}
        and isinstance(value.get("checkedAt"), int)
        and not isinstance(value.get("checkedAt"), bool)
        and value.get("latest") == EXPECTED_GRAFT
    )


def _owned_graph_tree(paths: set[Path]) -> set[Path]:
    graph_paths = {path for path in paths if path == GRAPH_DIR or path.is_relative_to(GRAPH_DIR)}
    if graph_paths == {GRAPH_DIR}:
        return graph_paths
    try:
        receipt = _read_json(GRAPH_RECEIPT, "adapter graph receipt")
        tree = _graph_tree_identity(GRAPH_DIR)
    except (AdapterError, OSError, RecursionError, UnicodeError, json.JSONDecodeError):
        return set()
    valid = (
        isinstance(receipt, dict)
        and receipt.get("schema_version") == ADAPTER_SCHEMA_VERSION
        and receipt.get("authority") == "adapter-owned-provenance-receipt"
        and receipt.get("graph_tree_sha256") == tree["tree_sha256"]
        and receipt.get("graph_tree_files") == tree["files"]
        and receipt.get("graph_tree_bytes") == tree["bytes"]
    )
    return graph_paths if valid else set()


def _private_state_path(path: Path) -> bool:
    """Recognize the ownership and permissions required for removable state."""
    try:
        details = path.lstat()
    except OSError:
        return False
    safe_type = stat.S_ISDIR(details.st_mode) or (
        stat.S_ISREG(details.st_mode) and details.st_nlink == 1
    )
    owned = not hasattr(os, "getuid") or details.st_uid == os.getuid()
    return safe_type and not details.st_mode & 0o077 and owned


def _owned_state_tree(paths: set[Path]) -> set[Path]:
    """Recognize exact adapter files plus a graph bound by its durable receipt."""
    known_directories = {
        STATE_DIR,
        GRAPH_DIR,
        HOME_DIR,
        HOME_DIR / "config",
        HOME_DIR / "data",
        HOME_DIR / ".graft",
        CACHE_DIR,
        TEMP_DIR,
        EVIDENCE_FILE.parent,
    }
    owned = {path for path in known_directories & paths if _private_state_path(path)}
    update_check = HOME_DIR / ".graft" / "update-check.json"
    if NPM_GLOBAL_CONFIG in paths and _private_state_path(NPM_GLOBAL_CONFIG):
        with contextlib.suppress(OSError):
            if NPM_GLOBAL_CONFIG.read_bytes() == b"":
                owned.add(NPM_GLOBAL_CONFIG)
    if (
        update_check in paths
        and _private_state_path(update_check)
        and _valid_update_check_file(update_check)
    ):
        owned.add(update_check)
    if EVIDENCE_FILE in paths and _private_state_path(EVIDENCE_FILE) and _valid_last_run_file():
        owned.add(EVIDENCE_FILE)
    owned_graph = _owned_graph_tree(paths)
    graph_has_contents = any(path != GRAPH_DIR for path in owned_graph)
    if owned_graph and all(_private_state_path(path) for path in owned_graph):
        owned.update(owned_graph)
    else:
        owned_graph = set()
    if (
        GRAPH_RECEIPT in paths
        and _private_state_path(GRAPH_RECEIPT)
        and owned_graph
        and graph_has_contents
    ):
        owned.add(GRAPH_RECEIPT)
    return owned


def _removal_ownership_evidence() -> dict[str, dict[str, object]]:
    """Classify every deletion candidate without publishing descendant names."""
    all_paths: set[Path] = set()
    owned: set[Path] = set()
    for target in REMOVAL_TARGETS:
        paths = _tree_inventory(target)
        all_paths.update(paths)
        if not paths:
            continue
        if target in {RUNTIME_DIR / "node_modules", RUNTIME_BACKUP, RUNTIME_QUARANTINE}:
            owned.update(_owned_runtime_tree(target, paths))
        elif target == RUNTIME_STAGING:
            owned.update(_owned_staging_tree(paths))
        elif target == STATE_DIR:
            owned.update(_owned_state_tree(paths))
    unknown = all_paths - owned

    def attest(paths: set[Path]) -> dict[str, object]:
        names = sorted(path.relative_to(ROOT).as_posix() for path in paths)
        evidence = _omitted_value_evidence(names)
        return {"count": len(names), "sha256": evidence["sha256"]}

    return {"owned": attest(owned), "unknown": attest(unknown)}


def _removal_inventory() -> dict[str, object]:
    targets: list[dict[str, object]] = []
    for path in REMOVAL_TARGETS:
        _assert_path_chain(path)
        exists = path.exists() or path.is_symlink()
        safe = not path.is_symlink() and path.resolve(strict=False).is_relative_to(ROOT.resolve())
        targets.append({"path": str(path), "exists": exists, "safe": safe})
    tracked = _tracked_removal_evidence()
    ownership = _removal_ownership_evidence()
    legacy = ROOT / ".graft"
    _assert_path_chain(legacy)
    legacy_exists = legacy.exists() or legacy.is_symlink()
    removable_exists = any(item["exists"] for item in targets)
    tracked_files = tracked["count"]
    if not isinstance(tracked_files, int):
        raise AdapterError("invalid tracked removal evidence")
    unknown_files = ownership["unknown"]["count"]
    if not isinstance(unknown_files, int):
        raise AdapterError("invalid removal ownership evidence")
    return {
        "schema_version": 2,
        "command": "remove",
        "status": (
            "FAIL"
            if tracked_files or unknown_files
            else ("UNVERIFIED" if legacy_exists else "PASS")
        ),
        "complete": (
            not legacy_exists and not removable_exists and tracked_files == 0 and unknown_files == 0
        ),
        "mode": "check",
        "targets": targets,
        "tracked_target_files": tracked,
        "ownership": ownership,
        "legacy_root_state": {
            "path": str(legacy),
            "exists": legacy_exists,
            "action": "manual-review-not-removed",
        },
        "retained_lock_file": {
            "path": str(LOCK_FILE),
            "reason": "stable inode retained to prevent concurrent removal races",
        },
        "authority": "project-local-cleanup-plan",
    }


def _assert_removal_inventory_safe(inventory: Mapping[str, object], *, changed: bool) -> None:
    """Fail closed unless an inventory contains only untracked adapter-owned paths."""
    qualifier = "gained " if changed else "contains "
    tracked = inventory.get("tracked_target_files")
    if not isinstance(tracked, dict) or tracked.get("count") != 0:
        raise AdapterError(f"refusing removal because a managed target {qualifier}tracked files")
    ownership = inventory.get("ownership")
    unknown = ownership.get("unknown") if isinstance(ownership, dict) else None
    if not isinstance(unknown, dict) or unknown.get("count") != 0:
        raise AdapterError(
            f"refusing removal because a managed target {qualifier}unknown descendants"
        )


def _remove(apply: bool) -> dict[str, object]:
    if not apply:
        return _removal_inventory()
    with _exclusive_lock():
        inventory = _removal_inventory()
        removed: list[str] = []
        _assert_removal_inventory_safe(inventory, changed=False)
        targets = inventory["targets"]
        if not isinstance(targets, list):
            raise AdapterError("invalid removal inventory")
        for item in targets:
            # Recheck the complete deletion surface immediately before every
            # target. This catches files created by non-cooperating writers
            # after the initial inventory and before a later target is removed.
            current = _removal_inventory()
            _assert_removal_inventory_safe(current, changed=True)
            if not isinstance(item, dict) or item.get("safe") is not True:
                raise AdapterError("refusing an unsafe removal target")
            path = Path(str(item["path"]))
            if not item["exists"]:
                continue
            if path.is_symlink():
                raise AdapterError(f"refusing to remove symlink target: {path}")
            shutil.rmtree(path)
            removed.append(str(path))
        postcondition = _removal_inventory()
        return {
            **postcondition,
            "mode": "apply",
            "removed": removed,
            "pre_removal_targets": targets,
        }


def _relative_public_path(value: object) -> str:
    """Represent an adapter-owned path without disclosing its host prefix."""
    try:
        return Path(str(value)).relative_to(ROOT).as_posix()
    except ValueError as error:
        raise AdapterError("public removal inventory contains a non-project path") from error


def _public_removal(report: Mapping[str, object]) -> dict[str, object]:
    """Return a project-relative copy of the internal removal inventory."""
    public = dict(report)
    for name in ("targets", "pre_removal_targets"):
        items = report.get(name)
        if items is None:
            continue
        if not isinstance(items, list):
            raise AdapterError("public removal inventory has invalid targets")
        public_items: list[dict[str, object]] = []
        for item in items:
            if not isinstance(item, dict) or "path" not in item:
                raise AdapterError("public removal inventory has an invalid target")
            public_items.append({**item, "path": _relative_public_path(item["path"])})
        public[name] = public_items
    removed = report.get("removed")
    if isinstance(removed, list):
        public["removed"] = [_relative_public_path(path) for path in removed]
    for name in ("legacy_root_state", "retained_lock_file"):
        item = report.get(name)
        if isinstance(item, dict) and "path" in item:
            public[name] = {**item, "path": _relative_public_path(item["path"])}
    return public


def _bounded_text(maximum: int, label: str):
    def validate(value: str) -> str:
        invalid = (
            not value
            or len(value) > maximum
            or value.startswith("-")
            or "\x00" in value
            or any(ord(character) < FIRST_CONTROL_CODEPOINT for character in value)
        )
        if invalid:
            raise argparse.ArgumentTypeError(
                f"{label} must contain 1..{maximum} printable characters"
            )
        return value

    return validate


def _bounded_integer(minimum: int, maximum: int):
    def validate(value: str) -> int:
        try:
            number = int(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError("expected an integer") from error
        if number < minimum or number > maximum:
            raise argparse.ArgumentTypeError(f"expected {minimum}..{maximum}")
        return number

    return validate


def _record_failed_attempt(
    command: str,
    error: BaseException,
    parameters: Mapping[str, object] | None = None,
    *,
    status: str,
) -> None:
    if command not in {"ask", "build", "check", "install"}:
        return
    try:
        _assert_state_tree()
        with _exclusive_lock():
            evidence: dict[str, object] = {
                "schema_version": 2,
                "command": command,
                "status": status,
                "error": _error_details(error),
                "error_trust": ERROR_TRUST,
                "evidence_complete": False,
                "authority": "derived-advisory-evidence",
            }
            if parameters is not None:
                evidence["parameters"] = dict(parameters)
            _atomic_json(EVIDENCE_FILE, evidence)
    except (AdapterError, OSError):
        # Unsafe state or an active writer is precisely when following/replacing
        # a path would be worse than leaving file evidence unavailable.
        return


def parser() -> argparse.ArgumentParser:
    """Build the project-owned, closed command interface."""
    root = SafeParser(description=__doc__, add_help=False, allow_abbrev=False)
    commands = root.add_subparsers(dest="command", required=True, parser_class=SafeParser)
    commands.add_parser(
        "doctor",
        help="pure JSON prerequisite inspection",
        add_help=False,
        allow_abbrev=False,
    )
    install = commands.add_parser(
        "install",
        help="explicitly install the reviewed project-local npm lock",
        add_help=False,
        allow_abbrev=False,
    )
    install.add_argument(
        "--apply",
        action="store_true",
        required=True,
        help="acknowledge network access and native install scripts",
    )
    remove = commands.add_parser(
        "remove",
        help="inspect or remove project-local Graft state",
        add_help=False,
        allow_abbrev=False,
    )
    remove_mode = remove.add_mutually_exclusive_group(required=True)
    remove_mode.add_argument("--check", action="store_true")
    remove_mode.add_argument("--apply", action="store_true")
    commands.add_parser(
        "build",
        help="build the deterministic structural graph",
        add_help=False,
        allow_abbrev=False,
    )
    commands.add_parser(
        "check",
        help="fail if the graph is missing or stale",
        add_help=False,
        allow_abbrev=False,
    )
    ask = commands.add_parser(
        "ask",
        help="bounded ranked structural retrieval",
        add_help=False,
        allow_abbrev=False,
    )
    ask.add_argument("query", type=_bounded_text(500, "query"))
    ask.add_argument("--limit", type=_bounded_integer(1, 12), default=8)
    ask.add_argument("--source", action="store_true")
    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Run one constrained operation and always emit a JSON document."""
    command = "parse"
    arguments: argparse.Namespace | None = None
    try:
        arguments = parser().parse_args(argv)
        command = arguments.command
        if command == "doctor":
            report = _doctor()
            _json_print(report)
            return 0 if report["status"] == "PASS" else 2
        if command == "install":
            report = _install()
        elif command == "remove":
            report = _public_removal(_remove(arguments.apply))
        else:
            report = _execute(arguments)
        _json_print(report)
        return 0 if report["status"] == "PASS" else 2
    except AdapterSignalError as error:
        parameters = _evidence_parameters(arguments) if arguments is not None else None
        _record_failed_attempt(command, error, parameters, status="FAIL")
        _json_print(_error_report(command, error, status="FAIL"))
        return 128 + error.signal_number
    except (
        AdapterError,
        OSError,
        RecursionError,
        UnicodeError,
        json.JSONDecodeError,
        subprocess.SubprocessError,
    ) as error:
        parameters = _evidence_parameters(arguments) if arguments is not None else None
        status = "UNVERIFIED" if isinstance(error, UnverifiedError) else "FAIL"
        _record_failed_attempt(command, error, parameters, status=status)
        _json_print(_error_report(command, error, status=status))
        return 2
    except KeyboardInterrupt:
        error = AdapterError("interrupted; child process was terminated")
        _json_print(_error_report(command, error, status="FAIL"))
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
