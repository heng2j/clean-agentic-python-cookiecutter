"""Small command-line adapter for the repository-local quality harness."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from .architecture import command_architecture
from .coverage_policy import command_coverage_policy
from .crap import command_crap
from .docs import command_context, command_docs, command_prune
from .friction import friction_compare, friction_finish, friction_start
from .gauntlet import command_gauntlet
from .io import atomic_write_text, print_line, repository_root, safe_path
from .model import CleanAIError, ConfigurationError
from .mutation import command_mutate
from .package import command_package_smoke
from .science import command_science

Handler = Callable[[Path, argparse.Namespace], int]
MAX_TASK_TITLE = 160
MAX_TASK_OWNER = 80


def _architecture(root: Path, args: argparse.Namespace) -> int:
    return command_architecture(root, strict=bool(args.strict))


def _context(root: Path, args: argparse.Namespace) -> int:
    return command_context(root, strict=bool(args.strict))


def _docs(root: Path, args: argparse.Namespace) -> int:
    return command_docs(root, strict=bool(args.strict))


def _science(root: Path, args: argparse.Namespace) -> int:
    return command_science(root, strict=bool(args.strict))


def _crap(root: Path, args: argparse.Namespace) -> int:
    return command_crap(root, args.coverage, strict=bool(args.strict))


def _coverage_policy(root: Path, args: argparse.Namespace) -> int:
    return command_coverage_policy(root, args.coverage, strict=bool(args.strict))


def _mutate(root: Path, args: argparse.Namespace) -> int:
    return command_mutate(root, args.config, strict=bool(args.strict))


def _gauntlet(root: Path, args: argparse.Namespace) -> int:
    return command_gauntlet(root, str(args.profile))


def _prune(root: Path, args: argparse.Namespace) -> int:
    return command_prune(root, args.output)


def _package(root: Path, args: argparse.Namespace) -> int:
    return command_package_smoke(root, args.dist_dir)


def _task_packet(root: Path, args: argparse.Namespace) -> int:
    title = str(args.title).strip()
    owner = str(args.owner).strip()
    if not title or len(title) > MAX_TASK_TITLE or any(character in title for character in "\r\n"):
        raise ConfigurationError("task title must be one line containing 1-160 characters")
    if not owner or len(owner) > MAX_TASK_OWNER or any(character in owner for character in "\r\n"):
        raise ConfigurationError("task owner must be one line containing 1-80 characters")
    slug = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-")[:60]
    if not slug:
        raise ConfigurationError("task title must contain at least one letter or number")
    relative = Path("docs/tasks/active") / f"{slug}.md"
    path = safe_path(root, relative)
    if path.exists():
        raise ConfigurationError(f"task packet already exists: {relative.as_posix()}")
    today = dt.date.today().isoformat()
    content = (
        "---\n"
        "status: draft\n"
        f"owner: {owner}\n"
        f"authority: task.{slug}\n"
        f"last_verified: {today}\n"
        "applies_to:\n"
        "  - src/**\n"
        "  - tests/**\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Outcome\n\nDefine one observable outcome.\n\n"
        "## Allowed change surface\n\nList the files or globs that may change.\n\n"
        "## Invariants\n\nList behavior that must remain true.\n\n"
        "## Verification\n\nList exact commands and expected exit codes.\n\n"
        "## Stop and escalate\n\nList conditions that require a maintainer decision.\n"
    )
    atomic_write_text(path, content)
    print_line(relative)
    return 0


def _friction_start(root: Path, args: argparse.Namespace) -> int:
    return friction_start(root, str(args.task), str(args.agent), str(args.cohort))


def _friction_finish(root: Path, args: argparse.Namespace) -> int:
    return friction_finish(
        root,
        args.run_dir,
        accepted=args.accepted == "yes",
        human_interventions=int(args.human_interventions),
        trace=args.trace,
    )


def _friction_compare(root: Path, args: argparse.Namespace) -> int:
    return friction_compare(root, args.runs_root, list(args.cohort))


def _command(
    subparsers: Any,
    name: str,
    handler: Handler,
    *,
    help_text: str,
) -> argparse.ArgumentParser:
    command: argparse.ArgumentParser = subparsers.add_parser(name, help=help_text)
    command.set_defaults(handler=handler)
    return command


def parser() -> argparse.ArgumentParser:
    """Build the public CLI parser."""
    root = argparse.ArgumentParser(prog="cleanai", description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    gauntlet = _command(commands, "gauntlet", _gauntlet, help_text="run a named quality profile")
    gauntlet.add_argument("profile")
    for name, handler in (
        ("architecture", _architecture),
        ("context-audit", _context),
        ("docs-audit", _docs),
        ("science-audit", _science),
    ):
        audit = _command(commands, name, handler, help_text=f"run the {name} control")
        audit.add_argument("--strict", action="store_true")
    crap = _command(commands, "crap", _crap, help_text="calculate callable CRAP estimates")
    crap.add_argument("--coverage", type=Path, required=True)
    crap.add_argument("--strict", action="store_true")
    coverage_policy = _command(
        commands,
        "coverage-policy",
        _coverage_policy,
        help_text="enforce separate product and harness coverage floors",
    )
    coverage_policy.add_argument("--coverage", type=Path, required=True)
    coverage_policy.add_argument("--strict", action="store_true")
    mutation = _command(commands, "mutate", _mutate, help_text="run isolated curated mutants")
    mutation.add_argument("--config", type=Path, required=True)
    mutation.add_argument("--strict", action="store_true")
    prune = _command(
        commands, "prune-plan", _prune, help_text="write a non-destructive cleanup plan"
    )
    prune.add_argument("--output", type=Path, required=True)
    task = _command(commands, "task-packet", _task_packet, help_text="create a bounded task packet")
    task.add_argument("title")
    task.add_argument("--owner", default="maintainers")
    package = _command(
        commands, "package-smoke", _package, help_text="verify built artifacts offline"
    )
    package.add_argument("--dist-dir", type=Path, default=Path("dist"))
    friction = commands.add_parser("friction", help="record and compare agent-friction runs")
    friction_commands = friction.add_subparsers(dest="friction_command", required=True)
    start = _command(friction_commands, "start", _friction_start, help_text="start a clean run")
    start.add_argument("--task", required=True)
    start.add_argument("--agent", required=True)
    start.add_argument("--cohort", required=True)
    finish = _command(
        friction_commands, "finish", _friction_finish, help_text="finish and verify a run"
    )
    finish.add_argument("run_dir", type=Path)
    finish.add_argument("--accepted", choices=("yes", "no"), required=True)
    finish.add_argument("--human-interventions", type=int, default=0)
    finish.add_argument("--trace", type=Path)
    compare = _command(
        friction_commands, "compare", _friction_compare, help_text="compare like runs"
    )
    compare.add_argument("--runs-root", type=Path, default=Path(".cleanai/runs"))
    compare.add_argument("--cohort", action="append", required=True)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Parse and run one command with controlled exit semantics."""
    try:
        args = parser().parse_args(argv)
        handler: Handler = args.handler
        return handler(repository_root(), args)
    except CleanAIError as error:
        print_line(f"cleanai: {error}", error=True)
        return 2
    except KeyboardInterrupt:
        print_line("cleanai: interrupted", error=True)
        return 130
