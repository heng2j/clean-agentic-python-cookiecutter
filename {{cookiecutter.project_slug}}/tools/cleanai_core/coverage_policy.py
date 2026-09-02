"""Separate branch-aware product and quality-harness coverage floors."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .io import (
    atomic_write_text,
    evidence_run_dir,
    finite_number,
    load_policy,
    print_line,
    safe_path,
    write_json,
)
from .model import ConfigurationError, EvidenceError


@dataclass(frozen=True, slots=True)
class CoverageGroup:
    """Aggregate line-plus-branch coverage for one explicit file group."""

    name: str
    files: int
    covered: int
    measurable: int
    percent: float
    minimum_percent: float


def _load(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise EvidenceError(f"coverage JSON does not exist: {path}") from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"cannot parse coverage JSON {path}: {error}") from error
    if not isinstance(payload, dict):
        raise EvidenceError("coverage JSON root must be an object")
    meta = payload.get("meta")
    files = payload.get("files")
    if not isinstance(meta, dict) or not isinstance(meta.get("version"), str):
        raise EvidenceError("coverage JSON requires coverage.py meta.version")
    if not isinstance(files, dict):
        raise EvidenceError("coverage JSON requires a files object")
    return payload


def _count(summary: dict[str, Any], name: str, path: str) -> int:
    value = summary.get(name)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise EvidenceError(f"{path}.summary.{name} must be a nonnegative integer")
    return value


def _group(
    name: str,
    expected: list[str],
    entries: dict[str, Any],
    minimum: float,
) -> CoverageGroup:
    if not expected:
        raise EvidenceError(f"{name} coverage group contains no Python files")
    covered = 0
    measurable = 0
    for path in expected:
        entry = entries.get(path)
        if not isinstance(entry, dict):
            raise EvidenceError(f"coverage JSON lacks required {name} file: {path}")
        summary = entry.get("summary")
        if not isinstance(summary, dict):
            raise EvidenceError(f"coverage JSON lacks summary for {path}")
        covered_lines = _count(summary, "covered_lines", path)
        statements = _count(summary, "num_statements", path)
        covered_branches = _count(summary, "covered_branches", path)
        branches = _count(summary, "num_branches", path)
        if covered_lines > statements or covered_branches > branches:
            raise EvidenceError(f"coverage counts exceed measurable totals for {path}")
        covered += covered_lines + covered_branches
        measurable += statements + branches
    if measurable == 0:
        raise EvidenceError(f"{name} coverage group contains no measurable statements or branches")
    return CoverageGroup(
        name=name,
        files=len(expected),
        covered=covered,
        measurable=measurable,
        percent=round(100.0 * covered / measurable, 2),
        minimum_percent=minimum,
    )


def _python_files(root: Path, directory: Path, name: str) -> list[str]:
    paths = sorted(directory.rglob("*.py"))
    for path in paths:
        if path.is_symlink():
            raise EvidenceError(f"{name} coverage file cannot be a symlink: {path}")
    return [path.relative_to(root).as_posix() for path in paths]


def coverage_groups(root: Path, coverage_path: Path) -> tuple[CoverageGroup, CoverageGroup]:
    """Validate evidence completeness and calculate the two configured floors."""
    policy = load_policy(root)
    project = policy.get("project")
    quality = policy.get("quality")
    if not isinstance(project, dict) or not isinstance(project.get("source_root"), str):
        raise ConfigurationError("policy project.source_root must be a string")
    if not isinstance(quality, dict):
        raise ConfigurationError("policy quality table is required")
    product_minimum = finite_number(
        quality.get("minimum_coverage"),
        "quality.minimum_coverage",
        minimum=0.0,
        maximum=100.0,
    )
    harness_minimum = finite_number(
        quality.get("minimum_harness_coverage"),
        "quality.minimum_harness_coverage",
        minimum=0.0,
        maximum=100.0,
    )
    source_root = safe_path(root, project["source_root"], must_exist=True)
    tools_root = safe_path(root, "tools", must_exist=True)
    payload = _load(coverage_path)
    entries = payload["files"]
    if not isinstance(entries, dict):
        raise EvidenceError("coverage JSON requires a files object")
    product = _group(
        "product",
        _python_files(root, source_root, "product"),
        entries,
        product_minimum,
    )
    harness = _group(
        "harness",
        _python_files(root, tools_root, "harness"),
        entries,
        harness_minimum,
    )
    return product, harness


def command_coverage_policy(root: Path, coverage: Path, *, strict: bool) -> int:
    """Write evidence and enforce product/harness floors independently."""
    coverage_path = (
        coverage if coverage.is_absolute() else safe_path(root, coverage, must_exist=True)
    )
    try:
        coverage_path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (FileNotFoundError, ValueError) as error:
        raise ConfigurationError("coverage JSON must be inside the repository") from error
    groups = coverage_groups(root, coverage_path)
    output = evidence_run_dir(root, "quality")
    passed = all(group.percent >= group.minimum_percent for group in groups)
    write_json(
        output / "coverage-policy.json",
        {
            "schema_version": 1,
            "measurement": "aggregate covered lines plus covered branches",
            "coverage_path": coverage_path.relative_to(root).as_posix(),
            "groups": [asdict(group) for group in groups],
            "passed": passed,
        },
    )
    lines = [
        "# Coverage policy",
        "",
        "| Group | Files | Covered | Measurable | Result | Floor |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    lines.extend(
        f"| {group.name} | {group.files} | {group.covered} | {group.measurable} | "
        f"{group.percent:.2f}% | {group.minimum_percent:.2f}% |"
        for group in groups
    )
    atomic_write_text(output / "coverage-policy.md", "\n".join(lines) + "\n")
    for group in groups:
        print_line(
            f"{group.name}: {group.percent:.2f}% branch-aware coverage; "
            f"floor={group.minimum_percent:.2f}%"
        )
    print_line(f"Evidence: {output.relative_to(root)}")
    return int(strict and not passed)
