from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path
from typing import Any

import pytest
from tools.cleanai_core import cli
from tools.cleanai_core.model import ConfigurationError


@pytest.mark.parametrize(
    ("argv", "target"),
    [
        (["architecture", "--strict"], "command_architecture"),
        (["context-audit", "--strict"], "command_context"),
        (["docs-audit", "--strict"], "command_docs"),
        (["science-audit", "--strict"], "command_science"),
        (["crap", "--coverage", "coverage.json", "--strict"], "command_crap"),
        (
            ["coverage-policy", "--coverage", "coverage.json", "--strict"],
            "command_coverage_policy",
        ),
        (["mutate", "--config", "mutations.toml", "--strict"], "command_mutate"),
        (["gauntlet", "full"], "command_gauntlet"),
        (["prune-plan", "--output", "plan.md"], "command_prune"),
        (["package-smoke", "--dist-dir", "dist"], "command_package_smoke"),
        (
            ["friction", "start", "--task", "task", "--agent", "agent", "--cohort", "root"],
            "friction_start",
        ),
        (
            ["friction", "finish", ".cleanai/runs/one", "--accepted", "yes"],
            "friction_finish",
        ),
        (
            ["friction", "compare", "--runs-root", ".cleanai/runs", "--cohort", "root"],
            "friction_compare",
        ),
    ],
)
def test_cli_routes_each_public_command(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    target: str,
) -> None:
    calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def fake(*args: Any, **kwargs: Any) -> int:
        calls.append((args, kwargs))
        return 37

    monkeypatch.setattr(cli, "repository_root", lambda: tmp_path)
    monkeypatch.setattr(cli, target, fake)
    assert cli.main(argv) == 37
    assert calls
    assert calls[0][0][0] == tmp_path


def test_task_packet_is_bounded_and_refuses_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "repository_root", lambda: tmp_path)
    assert cli.main(["task-packet", "One Safe Change", "--owner", "maintainers"]) == 0
    packet = tmp_path / "docs/tasks/active/one-safe-change.md"
    text = packet.read_text(encoding="utf-8")
    assert "status: draft" in text
    assert "## Verification" in text
    assert cli.main(["task-packet", "One Safe Change"]) == 2
    assert "already exists" in capsys.readouterr().err
    assert cli.main(["task-packet", "bad\nname"]) == 2


def test_main_converts_controlled_error_and_interrupt_to_stable_exits(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cli,
        "repository_root",
        lambda: (_ for _ in ()).throw(ConfigurationError("no policy")),
    )
    assert cli.main(["architecture"]) == 2
    assert "no policy" in capsys.readouterr().err

    class InterruptingParser:
        def parse_args(self, _argv: object) -> argparse.Namespace:
            raise KeyboardInterrupt

    monkeypatch.setattr(cli, "parser", InterruptingParser)
    assert cli.main([]) == 130
    assert "interrupted" in capsys.readouterr().err


def test_thin_executable_delegates_to_core(monkeypatch: pytest.MonkeyPatch) -> None:
    tool = Path(__file__).parents[2] / "tools/cleanai.py"
    monkeypatch.setattr(sys, "argv", [str(tool), "--help"])
    with pytest.raises(SystemExit) as stopped:
        runpy.run_path(str(tool), run_name="__main__")
    assert stopped.value.code == 0
