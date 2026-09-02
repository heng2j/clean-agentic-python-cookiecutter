"""Git-grounded agent-friction task recording and cohort comparison."""

from __future__ import annotations

import datetime as dt
import fnmatch
import json
import re
import secrets
import shutil
import subprocess  # nosec B404
from dataclasses import asdict
from pathlib import Path
from statistics import median
from typing import Any

from .io import (
    atomic_write_text,
    finite_number,
    load_policy,
    load_toml,
    print_line,
    run_command,
    safe_path,
    write_json,
)
from .model import BenchmarkTask, ConfigurationError, EvidenceError

PORCELAIN_PREFIX = 3
SCHEMA_VERSION = 2


def _git(root: Path, *args: str) -> str:
    executable = shutil.which("git")
    if executable is None:
        raise ConfigurationError("Git is required for comparable friction runs")
    try:
        completed = subprocess.run(  # noqa: S603  # nosec B603
            [executable, *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        raise ConfigurationError(
            f"Git is required for comparable friction runs: {error}"
        ) from error
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ConfigurationError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def _status(root: Path) -> list[str]:
    return _git(root, "status", "--porcelain=v1", "--untracked-files=all").splitlines()


def _revision(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD").strip()


def _slug(value: str, label: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-.")
    if not slug or slug != value:
        raise ConfigurationError(
            f"{label} must use only letters, numbers, dot, underscore, or hyphen"
        )
    return slug


def _string_tuple(raw: dict[str, Any], name: str, task_id: str) -> tuple[str, ...]:
    value = raw.get(name, [])
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ConfigurationError(f"benchmark {task_id}.{name} must be a string list")
    return tuple(value)


def load_benchmark_tasks(root: Path) -> dict[str, BenchmarkTask]:
    path = safe_path(root, ".cleanai/benchmark-tasks.toml", must_exist=True)
    data = load_toml(path)
    rows = data.get("task")
    if not isinstance(rows, list) or not rows:
        raise ConfigurationError("benchmark task bank must contain [[task]] entries")
    tasks: dict[str, BenchmarkTask] = {}
    for raw in rows:
        if not isinstance(raw, dict):
            raise ConfigurationError("benchmark task entry must be a table")
        required = ("id", "title", "prompt")
        if any(not isinstance(raw.get(name), str) or not raw[name] for name in required):
            raise ConfigurationError("benchmark task requires nonempty id/title/prompt")
        task_id = _slug(raw["id"], "task id")
        if task_id in tasks:
            raise ConfigurationError(f"duplicate benchmark task id: {task_id}")
        prompt = safe_path(root, raw["prompt"], must_exist=True).relative_to(root).as_posix()

        verification = _string_tuple(raw, "verification", task_id)
        if not verification:
            raise ConfigurationError(f"benchmark {task_id} requires verification commands")
        tasks[task_id] = BenchmarkTask(
            task_id,
            raw["title"],
            prompt,
            _string_tuple(raw, "expected_globs", task_id),
            _string_tuple(raw, "forbidden_globs", task_id),
            verification,
        )
    return tasks


def friction_start(root: Path, task_id: str, agent: str, cohort: str) -> int:
    """Start a comparable run only from a clean committed Git worktree."""
    tasks = load_benchmark_tasks(root)
    if task_id not in tasks:
        raise ConfigurationError(f"unknown task {task_id!r}; choices: {', '.join(sorted(tasks))}")
    if _status(root):
        raise ConfigurationError(
            "friction runs require a clean worktree; commit or stash all changes first"
        )
    baseline = _revision(root)
    safe_agent = _slug(agent, "agent")
    safe_cohort = _slug(cohort, "cohort")
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    run_name = f"{stamp}-{task_id}-{safe_cohort}-{secrets.token_hex(4)}"
    run_dir = safe_path(root, Path(".cleanai/runs") / run_name)
    run_dir.mkdir(parents=True, exist_ok=False)
    task = tasks[task_id]
    shutil.copy2(safe_path(root, task.prompt, must_exist=True), run_dir / "task.md")
    write_json(
        run_dir / "run.json",
        {
            "schema_version": 2,
            "task": asdict(task),
            "agent": safe_agent,
            "cohort": safe_cohort,
            "started_at": dt.datetime.now(dt.UTC).isoformat(),
            "baseline_commit": baseline,
            "baseline_status": [],
        },
    )
    print_line(run_dir.relative_to(root))
    return 0


def _contained_run(root: Path, run_dir: Path) -> Path:
    if run_dir.is_absolute():
        try:
            relative = run_dir.resolve(strict=True).relative_to(root.resolve(strict=True))
        except (FileNotFoundError, ValueError) as error:
            raise ConfigurationError("friction run directory must be inside repository") from error
    else:
        relative = run_dir
    absolute = safe_path(root, relative, must_exist=True)
    runs_root = safe_path(root, ".cleanai/runs")
    try:
        absolute.relative_to(runs_root)
    except ValueError as error:
        raise ConfigurationError("friction run directory must be under .cleanai/runs") from error
    return absolute


def _status_path(line: str) -> str:
    value = line[PORCELAIN_PREFIX:] if len(line) > PORCELAIN_PREFIX else ""
    return value.rsplit(" -> ", 1)[-1]


def _changed_files(root: Path, baseline: str) -> list[str]:
    tracked = set(_git(root, "diff", "--name-only", baseline, "--").splitlines())
    tracked.update(_status_path(line) for line in _status(root))
    return sorted(path for path in tracked if path)


def _matches(path: str, patterns: list[str] | tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def _trace_metrics(root: Path, trace: Path | None, expected: list[str]) -> dict[str, Any]:
    if trace is None:
        return {"available": False, "reason": "no trace supplied"}
    path = trace if trace.is_absolute() else safe_path(root, trace, must_exist=True)
    if path.is_absolute():
        try:
            path.resolve(strict=True).relative_to(root.resolve(strict=True))
        except ValueError as error:
            raise EvidenceError("trace must remain inside repository") from error
    rows: list[dict[str, Any]] = []
    try:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line:
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise EvidenceError(f"trace row {number} must be an object")
            rows.append(row)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"cannot parse trace {path}: {error}") from error
    opened = [
        str(row["path"])
        for row in rows
        if row.get("event") in {"open", "read", "search-hit"} and isinstance(row.get("path"), str)
    ]
    tokens = 0
    for row in rows:
        value = row.get("tokens", 0)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EvidenceError("trace tokens must be nonnegative integers")
        tokens += value
    relevant = [item for item in opened if _matches(item, expected)]
    return {
        "available": True,
        "files_opened": len(opened),
        "unique_files_opened": len(set(opened)),
        "expected_file_reads": len(relevant),
        "exploration_precision": round(len(relevant) / max(len(opened), 1), 3),
        "tokens": tokens,
        "tool_calls": len(rows),
    }


def friction_finish(
    root: Path,
    run_dir: Path,
    *,
    accepted: bool,
    human_interventions: int,
    trace: Path | None,
) -> int:
    """Finish with Git-complete change capture and verification-derived success."""
    if human_interventions < 0:
        raise ConfigurationError("human interventions cannot be negative")
    absolute = _contained_run(root, run_dir)
    try:
        metadata = json.loads((absolute / "run.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"cannot load friction run metadata: {error}") from error
    if not isinstance(metadata, dict) or metadata.get("schema_version") != SCHEMA_VERSION:
        raise EvidenceError("friction run metadata has unsupported schema")
    task = metadata.get("task")
    baseline = metadata.get("baseline_commit")
    if not isinstance(task, dict) or not isinstance(baseline, str):
        raise EvidenceError("friction run metadata lacks task/baseline")
    _git(root, "cat-file", "-e", baseline + "^" + "{commit}")
    expected_globs = list(task.get("expected_globs", []))
    forbidden_globs = list(task.get("forbidden_globs", []))
    policy = load_policy(root)
    execution = policy.get("execution", {})
    if not isinstance(execution, dict):
        raise ConfigurationError("policy execution table must be a table")
    timeout = finite_number(
        execution.get("command_timeout_seconds", 300), "command timeout", minimum=0.1
    )
    commands = task.get("verification")
    if not isinstance(commands, list) or not commands:
        raise EvidenceError("friction task has no verification commands")
    verification = [run_command(command, root, timeout_seconds=timeout) for command in commands]
    verification_success = all(item.status == "passed" for item in verification)
    # Verification is untrusted repository configuration and may mutate the worktree.
    # Classify the final state so those writes cannot evade expected/forbidden paths.
    changed = _changed_files(root, baseline)
    expected = [path for path in changed if _matches(path, expected_globs)]
    forbidden = [path for path in changed if _matches(path, forbidden_globs)]
    success = verification_success and not forbidden and accepted
    result: dict[str, Any] = {
        **metadata,
        "finished_at": dt.datetime.now(dt.UTC).isoformat(),
        "finish_commit": _revision(root),
        "finish_status": _status(root),
        "human_accepted": accepted,
        "verification_success": verification_success,
        "success": success,
        "human_interventions": human_interventions,
        "changed_files": changed,
        "expected_changed_files": expected,
        "forbidden_changed_files": forbidden,
        "change_precision": round(len(expected) / max(len(changed), 1), 3),
        "verification": [asdict(item) for item in verification],
        "trace": _trace_metrics(root, trace, expected_globs),
    }
    write_json(absolute / "result.json", result)
    atomic_write_text(absolute / "report.md", _report(result))
    print_line(absolute / "report.md")
    return int(not success)


def _report(result: dict[str, Any]) -> str:
    task = result["task"]
    lines = [
        f"# Agent-friction run: {task['title']}",
        "",
        f"- Cohort: `{result['cohort']}`",
        f"- Agent: `{result['agent']}`",
        f"- Verification success: **{result['verification_success']}**",
        f"- Human accepted: **{result['human_accepted']}**",
        f"- Overall success: **{result['success']}**",
        f"- Human interventions: **{result['human_interventions']}**",
        f"- Change precision: **{result['change_precision']:.3f}**",
        "",
        "## Changed files",
        "",
    ]
    lines.extend(f"- `{path}`" for path in result["changed_files"])
    return "\n".join(lines) + "\n"


def friction_compare(root: Path, runs_root: Path, cohorts: list[str]) -> int:
    """Compare only like-task, like-baseline completed runs and state limitations."""
    absolute = _contained_runs_root(root, runs_root)
    groups: dict[str, list[dict[str, Any]]] = {_slug(cohort, "cohort"): [] for cohort in cohorts}
    for path in absolute.glob("*/result.json"):
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise EvidenceError(f"cannot parse friction result {path}: {error}") from error
        cohort = row.get("cohort")
        if cohort in groups:
            groups[cohort].append(row)
    signatures = {
        (row["task"]["task_id"], row["baseline_commit"]) for rows in groups.values() for row in rows
    }
    if len(signatures) > 1:
        raise EvidenceError("cohort comparison mixes task IDs or baseline revisions")
    lines = [
        "# Agent-friction cohort comparison",
        "",
        "Comparability is limited to the recorded task, baseline revision, tools, and traces.",
        "",
        "| Cohort | Runs | Success | Precision | Interventions | Files changed |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for cohort, rows in groups.items():
        if not rows:
            lines.append(f"| {cohort} | 0 | — | — | — | — |")
            continue
        success = sum(bool(row["success"]) for row in rows) / len(rows)
        precision = median(float(row["change_precision"]) for row in rows)
        interventions = median(float(row["human_interventions"]) for row in rows)
        changed = median(float(len(row["changed_files"])) for row in rows)
        lines.append(
            f"| {cohort} | {len(rows)} | {success:.0%} | {precision:.3f} | "
            f"{interventions:.1f} | {changed:.1f} |"
        )
    output = absolute / f"comparison-{secrets.token_hex(4)}.md"
    atomic_write_text(output, "\n".join(lines) + "\n")
    print_line(output)
    return 0


def _contained_runs_root(root: Path, runs_root: Path) -> Path:
    if runs_root.is_absolute():
        try:
            relative = runs_root.resolve(strict=True).relative_to(root.resolve(strict=True))
        except (FileNotFoundError, ValueError) as error:
            raise ConfigurationError("runs root must be inside repository") from error
    else:
        relative = runs_root
    return safe_path(root, relative, must_exist=True)
