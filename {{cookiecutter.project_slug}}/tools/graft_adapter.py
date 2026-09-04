#!/usr/bin/env python3
"""Project-scoped runner for the optional Graft structural experiment.

This wrapper never installs Graft, runs ``graft init``, enables hooks, or invokes
model-backed enrichment. It pins the inspected release, forces telemetry off,
removes common model credentials, and stores Graft state under ignored
``artifacts/``. Its output is advisory navigation evidence, not project
authority.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess  # nosec B404
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
GRAPH_DIR: Final = ROOT / "artifacts" / "graft" / "context"
HOME_DIR: Final = ROOT / "artifacts" / "graft" / "home"
EXPECTED_GRAFT: Final = (0, 17, 0)
MINIMUM_NODE: Final = (22, 12, 0)
VERSION_RE: Final = re.compile(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?!\d)")
ALLOWED: Final = frozenset(
    {"ask", "blast", "build", "callers", "check", "grep", "map", "mcp", "skeleton"}
)
BLOCKED: Final = frozenset(
    {
        "--api-key",
        "--base-url",
        "--concurrency",
        "--deep",
        "--dir",
        "--export-viz",
        "--extensions",
        "--follow-nested-repos",
        "--follow-submodules",
        "--include-dir",
        "--lsp",
        "--model",
        "--name",
        "--no-follow-nested-repos",
        "--no-follow-submodules",
        "--no-refresh",
        "--no-reuse",
        "--only-dir",
        "--provider",
        "-e",
        "-j",
        "init",
        "telemetry",
        "uninstall",
        "upgrade",
        "version",
        "viz",
    }
)
MODEL_KEYS: Final = (
    "ANTHROPIC_API_KEY",
    "GRAFT_API_KEY",
    "GRAFT_BASE_URL",
    "GRAFT_MODEL",
    "GRAFT_PROVIDER",
    "OPENAI_API_KEY",
    "OPENROUTER_API_KEY",
    "ORCAROUTER_API_KEY",
)


class AdapterError(RuntimeError):
    """A safe precondition for the experiment was not satisfied."""


def _version(text: str, label: str) -> tuple[int, int, int]:
    match = VERSION_RE.search(text)
    if match is None:
        raise AdapterError(f"cannot parse {label} version from {text.strip()!r}")
    return tuple(int(value) for value in match.groups())  # type: ignore[return-value]


def _executable(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise AdapterError(f"{name} is not on PATH")
    return path


def _probe(name: str) -> tuple[str, tuple[int, int, int]]:
    executable = _executable(name)
    environment = _environment() if name == "graft" else None
    completed = subprocess.run(  # noqa: S603  # nosec B603
        [executable, "--version"],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if completed.returncode:
        raise AdapterError(f"{name} --version failed: {completed.stderr.strip()}")
    return executable, _version(completed.stdout, name)


def _environment() -> dict[str, str]:
    HOME_DIR.mkdir(parents=True, exist_ok=True)
    empty_env = HOME_DIR / "empty.env"
    empty_env.write_text("", encoding="utf-8")
    update_cache = HOME_DIR / ".graft" / "update-check.json"
    update_cache.parent.mkdir(parents=True, exist_ok=True)
    update_cache.write_text(
        json.dumps(
            {
                "checkedAt": int(time.time() * 1000),
                "latest": ".".join(map(str, EXPECTED_GRAFT)),
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    environment = dict(os.environ)
    environment.update(
        {
            "DO_NOT_TRACK": "1",
            "DOTENV_CONFIG_PATH": str(empty_env),
            "GRAFT_DIR": str(GRAPH_DIR),
            "GRAFT_NO_GITIGNORE": "1",
            "GRAFT_NO_IGNORE": "1",
            "GRAFT_REFRESH": "hash",
            "HOME": str(HOME_DIR),
            "NO_COLOR": "1",
            "USERPROFILE": str(HOME_DIR),
        }
    )
    for key in MODEL_KEYS:
        environment.pop(key, None)
    environment.pop("GRAFT_NO_REFRESH", None)
    return environment


def _doctor() -> dict[str, object]:
    node_path, node_version = _probe("node")
    graft_path, graft_version = _probe("graft")
    ready = node_version >= MINIMUM_NODE and graft_version == EXPECTED_GRAFT
    return {
        "schema_version": 1,
        "ready": ready,
        "node": {"path": node_path, "version": ".".join(map(str, node_version))},
        "node_minimum": ".".join(map(str, MINIMUM_NODE)),
        "graft": {"path": graft_path, "version": ".".join(map(str, graft_version))},
        "graft_expected": ".".join(map(str, EXPECTED_GRAFT)),
        "graph_dir": str(GRAPH_DIR),
        "graph_exists": GRAPH_DIR.is_dir(),
        "telemetry_forced_off": True,
        "deep_mode_blocked": True,
    }


def _arguments(values: Sequence[str]) -> list[str]:
    arguments = list(values)
    if arguments[:1] == ["--"]:
        arguments = arguments[1:]
    if not arguments or arguments[0] not in ALLOWED:
        raise AdapterError(f"allowed commands: {', '.join(sorted(ALLOWED))}")
    if arguments[0] == "mcp" and len(arguments) != 1:
        raise AdapterError("mcp accepts no extra arguments in this profile")
    for value in arguments:
        if value in BLOCKED or any(value.startswith(f"{flag}=") for flag in BLOCKED):
            raise AdapterError(f"blocked in structural-only profile: {value}")
        if "\x00" in value:
            raise AdapterError("arguments must not contain NUL")
        path_value = Path(value)
        if path_value.is_absolute() or ".." in path_value.parts:
            raise AdapterError(f"absolute or parent-traversing argument: {value}")
    return arguments


def _run(values: Sequence[str]) -> int:
    report = _doctor()
    if not report["ready"]:
        raise AdapterError(json.dumps(report, sort_keys=True))
    GRAPH_DIR.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(report["graft"]["path"]),  # type: ignore[index]
        *_arguments(values),
    ]
    completed = subprocess.run(  # noqa: S603  # nosec B603
        command,
        cwd=ROOT,
        env=_environment(),
        check=False,
        timeout=None if values[:1] == ["mcp"] else 300,
    )
    return completed.returncode


def parser() -> argparse.ArgumentParser:
    """Build the project-owned command-line interface."""
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="check pinned prerequisites")
    doctor.add_argument("--json", action="store_true")
    run = commands.add_parser("run", help="run one allowlisted Graft command")
    run.add_argument("graft_arguments", nargs=argparse.REMAINDER)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Run one constrained Graft experiment command."""
    try:
        arguments = parser().parse_args(argv)
        if arguments.command == "doctor":
            report = _doctor()
            print(json.dumps(report, indent=2, sort_keys=True))
            return int(not report["ready"])
        return _run(arguments.graft_arguments)
    except (AdapterError, OSError, subprocess.TimeoutExpired) as error:
        print(f"graft-adapter: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
