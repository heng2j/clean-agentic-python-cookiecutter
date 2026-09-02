"""Curated semantic mutation in isolated disposable repository copies."""

from __future__ import annotations

import ast
import os
import re
import shutil
import tempfile
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .io import (
    IGNORED_PARTS,
    atomic_write_text,
    evidence_run_dir,
    finite_number,
    load_toml,
    print_line,
    run_command,
    safe_path,
    write_json,
)
from .model import ConfigurationError, MutationResult


def _copy_ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORED_PARTS or name.endswith((".pyc", ".pyo"))}


def _isolated_copy(root: Path, destination: Path) -> None:
    shutil.copytree(root, destination, symlinks=True, ignore=_copy_ignore)


def _mutation_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = data.get("mutation")
    if not isinstance(rows, list) or not rows:
        raise ConfigurationError("mutation config must contain at least one [[mutation]]")
    if any(not isinstance(row, dict) for row in rows):
        raise ConfigurationError("every mutation entry must be a table")
    identifiers = [row.get("id") for row in rows]
    if any(not isinstance(identifier, str) or not identifier.strip() for identifier in identifiers):
        raise ConfigurationError("every mutation requires a nonempty string id")
    if len(set(identifiers)) != len(identifiers):
        raise ConfigurationError("mutation ids must be unique")
    return rows


def _required_string(row: dict[str, Any], name: str, mutation_id: str) -> str:
    value = row.get(name)
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"mutation {mutation_id!r} requires nonempty {name}")
    return value


def _validate_row(root: Path, row: dict[str, Any]) -> tuple[Path, re.Pattern[str]]:
    mutation_id = _required_string(row, "id", "<unknown>")
    raw_path = _required_string(row, "path", mutation_id)
    target = safe_path(root, raw_path, must_exist=True, reject_symlinks=True)
    if not target.is_file():
        raise ConfigurationError(f"mutation target must be a regular file: {raw_path}")
    find = _required_string(row, "find", mutation_id)
    replace = _required_string(row, "replace", mutation_id)
    if find == replace:
        raise ConfigurationError(f"mutation {mutation_id!r} replacement is equivalent text")
    _required_string(row, "test_command", mutation_id)
    expected_exit = row.get("expected_exit")
    if isinstance(expected_exit, bool) or not isinstance(expected_exit, int) or expected_exit == 0:
        raise ConfigurationError(
            f"mutation {mutation_id!r} requires explicit nonzero expected_exit"
        )
    raw_regex = _required_string(row, "expected_output_regex", mutation_id)
    try:
        oracle = re.compile(raw_regex)
    except re.error as error:
        raise ConfigurationError(
            f"mutation {mutation_id!r} has invalid output oracle: {error}"
        ) from error
    return target, oracle


def _replace_in_copy(path: Path, find: str, replace: str) -> None:
    original = path.read_text(encoding="utf-8")
    count = original.count(find)
    if count != 1:
        raise ConfigurationError(
            f"target must occur exactly once in {path}; found {count}: {find!r}"
        )
    path.chmod(path.stat().st_mode | 0o200)
    path.write_text(original.replace(find, replace, 1), encoding="utf-8")


def _syntax_valid(path: Path) -> tuple[bool, str]:
    if path.suffix != ".py":
        return True, ""
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as error:
        return False, str(error)
    return True, ""


def _mutation_environment(copy_root: Path) -> dict[str, str]:
    environment = os.environ.copy()
    source = str(copy_root / "src")
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = source if not existing else os.pathsep.join((source, existing))
    environment["CLEANAI_MUTATION_COPY"] = str(copy_root)
    return environment


def _run_one(
    root: Path,
    row: dict[str, Any],
    *,
    timeout_seconds: float,
) -> MutationResult:
    mutation_id = str(row["id"])
    original_target, oracle = _validate_row(root, row)
    relative = original_target.relative_to(root.resolve(strict=True))
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="cleanai-mutant-") as raw_directory:
        copy_root = Path(raw_directory) / "repository"
        _isolated_copy(root, copy_root)
        copy_target = safe_path(copy_root, relative, must_exist=True, reject_symlinks=True)
        _replace_in_copy(copy_target, str(row["find"]), str(row["replace"]))
        syntax_ok, syntax_reason = _syntax_valid(copy_target)
        if not syntax_ok:
            return MutationResult(
                mutation_id,
                relative.as_posix(),
                "invalid",
                2,
                time.monotonic() - started,
                "",
                syntax_reason,
                "mutant is not syntactically valid",
            )
        command = run_command(
            str(row["test_command"]),
            copy_root,
            timeout_seconds=timeout_seconds,
            environment=_mutation_environment(copy_root),
        )
    combined = f"{command.stdout}\n{command.stderr}"
    expected_exit = int(row["expected_exit"])
    if command.status in {"error", "timeout"}:
        status = "error"
        reason = command.error or command.status
    elif command.returncode == 0:
        status = "survived"
        reason = "verification command passed against the mutant"
    elif command.returncode == expected_exit and oracle.search(combined):
        status = "killed"
        reason = "explicit exit and output oracle matched"
    else:
        status = "error"
        reason = (
            f"unexpected verification failure: exit {command.returncode}; "
            "explicit exit/output oracle did not both match"
        )
    return MutationResult(
        mutation_id,
        relative.as_posix(),
        status,
        command.returncode,
        time.monotonic() - started,
        command.stdout,
        command.stderr,
        reason,
    )


def _mutation_markdown(
    name: str, score: float, minimum: float, results: list[MutationResult]
) -> str:
    lines = [
        f"# {name}",
        "",
        f"Mutation score: **{score:.1f}%**; floor: **{minimum:.1f}%**.",
        "",
        "| Mutant | Status | Exit | Seconds | Target | Reason |",
        "|---|---|---:|---:|---|---|",
    ]
    for item in results:
        reason = item.reason.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{item.mutation_id}` | {item.status} | {item.returncode} | "
            f"{item.duration_seconds:.2f} | `{item.path}` | {reason} |"
        )
    return "\n".join(lines) + "\n"


def command_mutate(root: Path, config: Path, *, strict: bool) -> int:
    """Run curated mutants in isolated copies and publish explicit outcomes."""
    config_path = config if config.is_absolute() else safe_path(root, config, must_exist=True)
    try:
        config_path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except ValueError as error:
        raise ConfigurationError("mutation config must be inside the repository") from error
    data = load_toml(config_path)
    rows = _mutation_rows(data)
    minimum = finite_number(data.get("minimum_score"), "minimum_score", minimum=0.0, maximum=100.0)
    timeout = finite_number(data.get("timeout_seconds", 120), "timeout_seconds", minimum=0.1)
    baseline_command = data.get("baseline_command")
    if not isinstance(baseline_command, str) or not baseline_command:
        raise ConfigurationError("mutation config requires baseline_command")
    for row in rows:
        _validate_row(root, row)
    baseline = run_command(baseline_command, root, timeout_seconds=timeout)
    if baseline.status != "passed":
        raise ConfigurationError(
            f"mutation baseline must pass; status={baseline.status}, exit={baseline.returncode}"
        )
    results = [_run_one(root, row, timeout_seconds=timeout) for row in rows]
    scored = [item for item in results if item.status in {"killed", "survived"}]
    killed = sum(item.status == "killed" for item in scored)
    score = 100.0 * killed / len(scored) if scored else 0.0
    output = evidence_run_dir(root, "mutation")
    name = str(data.get("name", config_path.stem))
    payload = {
        "schema_version": 2,
        "name": name,
        "config": config_path.relative_to(root).as_posix(),
        "isolation": "per-mutant temporary repository copy; live source is never modified",
        "baseline": asdict(baseline),
        "killed": killed,
        "scored": len(scored),
        "total": len(results),
        "score": score,
        "minimum_score": minimum,
        "results": [asdict(item) for item in results],
    }
    write_json(output / f"{config_path.stem}.json", payload)
    atomic_write_text(
        output / f"{config_path.stem}.md",
        _mutation_markdown(name, score, minimum, results),
    )
    for item in results:
        print_line(f"{item.status.upper():8} {item.mutation_id} ({item.duration_seconds:.2f}s)")
    print_line(f"Evidence: {output.relative_to(root)}")
    errors = not scored or any(item.status in {"invalid", "error"} for item in results)
    if errors:
        return 2
    return int(strict and score < minimum)
