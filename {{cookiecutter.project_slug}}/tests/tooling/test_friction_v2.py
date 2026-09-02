from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
from tools.cleanai_core.friction import (
    _trace_metrics,
    friction_compare,
    friction_finish,
    friction_start,
)
from tools.cleanai_core.model import ConfigurationError, EvidenceError

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="Git is required")


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        [str(shutil.which("git")), *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _repository(root: Path, *, verification: str = "python -c 'pass'") -> None:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        "[execution]\ncommand_timeout_seconds = 5\n", encoding="utf-8"
    )
    (cleanai / "benchmark-tasks.toml").write_text(
        """[[task]]
id = "bounded"
title = "Bounded fixture task"
prompt = "benchmarks/task.md"
expected_globs = ["src/**"]
forbidden_globs = ["forbidden/**"]
"""
        + f"verification = [{json.dumps(verification)}]\n",
        encoding="utf-8",
    )
    prompt = root / "benchmarks/task.md"
    prompt.parent.mkdir()
    prompt.write_text("Change only src.\n", encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "fixture@example.invalid")
    _git(root, "config", "user.name", "Fixture")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "fixture baseline")


def _run_dir(root: Path) -> Path:
    return next((root / ".cleanai/runs").iterdir())


def test_start_requires_git_cleanliness_and_safe_identifiers(tmp_path: Path) -> None:
    _repository(tmp_path)
    dirty = tmp_path / "untracked.txt"
    dirty.write_text("dirty", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="clean worktree"):
        friction_start(tmp_path, "bounded", "agent", "cohort")
    dirty.unlink()
    with pytest.raises(ConfigurationError, match="agent must use only"):
        friction_start(tmp_path, "bounded", "unsafe agent", "cohort")
    with pytest.raises(ConfigurationError, match="unknown task"):
        friction_start(tmp_path, "absent", "agent", "cohort")

    not_git = tmp_path.parent / f"{tmp_path.name}-not-git"
    not_git.mkdir()
    _repository_files_only(not_git)
    with pytest.raises(ConfigurationError, match="git status"):
        friction_start(not_git, "bounded", "agent", "cohort")


def _repository_files_only(root: Path) -> None:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        "[execution]\ncommand_timeout_seconds = 5\n", encoding="utf-8"
    )
    (cleanai / "benchmark-tasks.toml").write_text(
        """[[task]]
id = "bounded"
title = "Bounded fixture task"
prompt = "benchmarks/task.md"
expected_globs = ["src/**"]
forbidden_globs = []
verification = ["python -c 'pass'"]
""",
        encoding="utf-8",
    )
    prompt = root / "benchmarks/task.md"
    prompt.parent.mkdir()
    prompt.write_text("Fixture\n", encoding="utf-8")


def test_finish_captures_untracked_changes_trace_and_verification(tmp_path: Path) -> None:
    _repository(tmp_path)
    assert friction_start(tmp_path, "bounded", "agent", "minimal") == 0
    run_dir = _run_dir(tmp_path)
    source = tmp_path / "src/change.py"
    source.parent.mkdir()
    source.write_text("VALUE = 2\n", encoding="utf-8")
    trace = tmp_path / "trace.jsonl"
    trace.write_text(
        json.dumps({"event": "read", "path": "src/change.py", "tokens": 12}) + "\n",
        encoding="utf-8",
    )
    assert (
        friction_finish(
            tmp_path,
            run_dir.relative_to(tmp_path),
            accepted=True,
            human_interventions=0,
            trace=trace.relative_to(tmp_path),
        )
        == 0
    )
    result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    assert result["success"] is True
    assert "src/change.py" in result["changed_files"]
    assert result["trace"]["expected_file_reads"] == 1
    assert result["verification_success"] is True


def test_finish_fails_on_forbidden_path_or_failed_verification(tmp_path: Path) -> None:
    _repository(tmp_path, verification="python -c 'raise SystemExit(1)'")
    assert friction_start(tmp_path, "bounded", "agent", "minimal") == 0
    run_dir = _run_dir(tmp_path)
    forbidden = tmp_path / "forbidden/secret.txt"
    forbidden.parent.mkdir()
    forbidden.write_text("no", encoding="utf-8")
    assert (
        friction_finish(
            tmp_path,
            run_dir,
            accepted=True,
            human_interventions=1,
            trace=None,
        )
        == 1
    )
    result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    assert result["success"] is False
    assert result["verification_success"] is False
    assert result["forbidden_changed_files"] == ["forbidden/secret.txt"]
    with pytest.raises(ConfigurationError, match="cannot be negative"):
        friction_finish(
            tmp_path,
            run_dir,
            accepted=True,
            human_interventions=-1,
            trace=None,
        )


def test_finish_rejects_forbidden_file_created_by_verification(tmp_path: Path) -> None:
    verification = (
        "python -c \"from pathlib import Path; Path('forbidden').mkdir(exist_ok=True); "
        "Path('forbidden/by-check.txt').write_text('created')\""
    )
    _repository(tmp_path, verification=verification)
    assert friction_start(tmp_path, "bounded", "agent", "minimal") == 0
    run_dir = _run_dir(tmp_path)
    assert (
        friction_finish(
            tmp_path,
            run_dir,
            accepted=True,
            human_interventions=0,
            trace=None,
        )
        == 1
    )
    result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    assert result["verification_success"] is True
    assert result["success"] is False
    assert result["forbidden_changed_files"] == ["forbidden/by-check.txt"]


def test_trace_and_cohort_comparison_fail_closed(tmp_path: Path) -> None:
    malformed = tmp_path / "trace.jsonl"
    malformed.write_text("not json\n", encoding="utf-8")
    with pytest.raises(EvidenceError, match="cannot parse trace"):
        _trace_metrics(tmp_path, malformed, ["src/**"])
    malformed.write_text('{"event":"read","path":"src/a.py","tokens":-1}\n', encoding="utf-8")
    with pytest.raises(EvidenceError, match="nonnegative"):
        _trace_metrics(tmp_path, malformed, ["src/**"])

    runs = tmp_path / ".cleanai/runs"
    for cohort in ("minimal", "none"):
        run = runs / cohort
        run.mkdir(parents=True)
        (run / "result.json").write_text(
            json.dumps(
                {
                    "cohort": cohort,
                    "task": {"task_id": "bounded"},
                    "baseline_commit": "abc",
                    "success": cohort == "minimal",
                    "change_precision": 1.0,
                    "human_interventions": 0,
                    "changed_files": ["src/a.py"],
                }
            ),
            encoding="utf-8",
        )
    assert friction_compare(tmp_path, Path(".cleanai/runs"), ["minimal", "none", "empty"]) == 0
    second = json.loads((runs / "none/result.json").read_text(encoding="utf-8"))
    second["baseline_commit"] = "different"
    (runs / "none/result.json").write_text(json.dumps(second), encoding="utf-8")
    with pytest.raises(EvidenceError, match="mixes task IDs or baseline"):
        friction_compare(tmp_path, Path(".cleanai/runs"), ["minimal", "none"])
