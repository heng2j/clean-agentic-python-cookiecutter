"""Fail-fast quality profiles with complete per-command evidence."""

from __future__ import annotations

import hashlib
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .io import (
    atomic_write_text,
    evidence_run_dir,
    finite_number,
    load_policy,
    print_line,
    repository_metadata,
    run_command,
    write_json,
)
from .model import CommandResult, ConfigurationError


def _profile_commands(
    name: str, profiles: dict[str, Any], chain: tuple[str, ...] = ()
) -> list[str]:
    if name not in profiles or not isinstance(profiles[name], dict):
        raise ConfigurationError(f"unknown or invalid gauntlet profile: {name}")
    if name in chain:
        cycle = " -> ".join((*chain, name))
        raise ConfigurationError(f"cyclic gauntlet inheritance: {cycle}")
    profile = profiles[name]
    commands: list[str] = []
    parent = profile.get("extends")
    if parent is not None:
        if not isinstance(parent, str):
            raise ConfigurationError(f"gauntlet.{name}.extends must be a string")
        commands.extend(_profile_commands(parent, profiles, (*chain, name)))
    raw_commands = profile.get("commands", [])
    if not isinstance(raw_commands, list) or any(
        not isinstance(item, str) or not item for item in raw_commands
    ):
        raise ConfigurationError(f"gauntlet.{name}.commands must be a list of nonempty strings")
    commands.extend(raw_commands)
    if not commands:
        raise ConfigurationError(f"gauntlet profile has no commands: {name}")
    return commands


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _result_record(result: CommandResult, stdout_name: str, stderr_name: str) -> dict[str, Any]:
    record = asdict(result)
    record.pop("stdout")
    record.pop("stderr")
    record.update(
        {
            "stdout_file": stdout_name,
            "stderr_file": stderr_name,
            "stdout_sha256": _digest(result.stdout),
            "stderr_sha256": _digest(result.stderr),
        }
    )
    return record


def _skipped(command: str) -> dict[str, Any]:
    return {
        "configured_command": command,
        "argv": [],
        "status": "skipped",
        "returncode": None,
        "duration_seconds": 0.0,
        "classification": "not-executed",
        "error": "skipped because an earlier command did not pass",
        "stdout_file": None,
        "stderr_file": None,
        "stdout_sha256": None,
        "stderr_sha256": None,
    }


def _markdown(profile: str, records: list[dict[str, Any]], passed: bool) -> str:
    lines = [
        f"# Gauntlet: {profile}",
        "",
        f"Overall: **{'PASS' if passed else 'FAIL'}**",
        "",
        "| Command | Status | Exit | Class | Seconds |",
        "|---|---|---:|---|---:|",
    ]
    for record in records:
        exit_value = "—" if record["returncode"] is None else str(record["returncode"])
        lines.append(
            f"| `{record['configured_command']}` | {record['status']} | {exit_value} | "
            f"{record['classification']} | {record['duration_seconds']:.2f} |"
        )
    return "\n".join(lines) + "\n"


def command_gauntlet(root: Path, profile: str) -> int:
    """Run a policy profile and always finalize a complete unique ledger."""
    policy = load_policy(root)
    profiles = policy.get("gauntlet")
    execution = policy.get("execution", {})
    if not isinstance(profiles, dict):
        raise ConfigurationError("policy gauntlet table is required")
    if not isinstance(execution, dict):
        raise ConfigurationError("policy execution table must be a table")
    timeout = finite_number(
        execution.get("command_timeout_seconds", 300),
        "execution.command_timeout_seconds",
        minimum=0.1,
    )
    commands = _profile_commands(profile, profiles)
    output = evidence_run_dir(root, "gauntlet")
    records: list[dict[str, Any]] = []
    failure_kind: str | None = None
    for index, command in enumerate(commands, start=1):
        if failure_kind is not None:
            records.append(_skipped(command))
            continue
        result = run_command(command, root, timeout_seconds=timeout)
        stdout_name = f"command-{index:02d}.stdout.txt"
        stderr_name = f"command-{index:02d}.stderr.txt"
        atomic_write_text(output / stdout_name, result.stdout)
        atomic_write_text(output / stderr_name, result.stderr)
        records.append(_result_record(result, stdout_name, stderr_name))
        print_line(f"$ {' '.join(result.argv) if result.argv else command}")
        if result.stdout:
            print_line(result.stdout.rstrip())
        if result.stderr:
            print_line(result.stderr.rstrip(), error=True)
        if result.status != "passed":
            failure_kind = result.status
    passed = failure_kind is None
    payload = {
        "schema_version": 2,
        "profile": profile,
        "passed": passed,
        "commands_planned": commands,
        "results": records,
        "repository": repository_metadata(root),
    }
    write_json(output / f"gauntlet-{profile}.json", payload)
    atomic_write_text(output / f"gauntlet-{profile}.md", _markdown(profile, records, passed))
    print_line(f"Evidence: {output.relative_to(root)}")
    if passed:
        return 0
    return 2 if failure_kind in {"error", "timeout"} else 1
