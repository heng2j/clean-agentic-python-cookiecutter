"""Fail-closed callable CRAP approximation over validated coverage.py JSON."""

from __future__ import annotations

import ast
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, override

from .io import (
    atomic_write_text,
    evidence_run_dir,
    finite_number,
    load_policy,
    print_line,
    safe_path,
    write_json,
)
from .model import CallableBlock, ConfigurationError, CrapRecord, EvidenceError

COMPLEXITY_ALGORITHM = "cleanai-ast-v2"
COVERAGE_SCHEMA = "coverage.py-json-v2"
MAX_PERCENT = 100.0


def crap_score(complexity: int, coverage_percent: float) -> float:
    """Calculate CRAP after validating its mathematical domain."""
    if isinstance(complexity, bool) or not isinstance(complexity, int) or complexity < 1:
        raise ValueError("complexity must be at least 1")
    if isinstance(coverage_percent, bool) or not 0.0 <= coverage_percent <= MAX_PERCENT:
        raise ValueError("coverage_percent must be in [0, 100]")
    uncovered_fraction = 1.0 - coverage_percent / MAX_PERCENT
    return complexity**2 * uncovered_fraction**3 + complexity


def _wildcard_case(case: ast.match_case) -> bool:
    return (
        isinstance(case.pattern, ast.MatchAs)
        and case.pattern.name is None
        and case.pattern.pattern is None
    )


class _ComplexityVisitor(ast.NodeVisitor):
    """Count decisions while treating nested callables as separate scopes."""

    def __init__(self) -> None:
        self.value = 1

    @override
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    @override
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    @override
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return

    @override
    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(
            node,
            (ast.If, ast.For, ast.AsyncFor, ast.While, ast.IfExp, ast.ExceptHandler, ast.Assert),
        ):
            self.value += 1
        elif isinstance(node, ast.BoolOp):
            self.value += max(len(node.values) - 1, 0)
        elif isinstance(node, ast.comprehension):
            self.value += 1 + len(node.ifs)
        elif isinstance(node, ast.Match):
            self.value += sum(not _wildcard_case(case) for case in node.cases)
            self.value += sum(case.guard is not None for case in node.cases)
        super().generic_visit(node)


def _complexity(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    visitor = _ComplexityVisitor()
    for child in node.body:
        visitor.visit(child)
    return visitor.value


class _StatementVisitor(ast.NodeVisitor):
    """Collect statement owners without entering nested callable bodies."""

    def __init__(self) -> None:
        self.lines: set[int] = set()

    @override
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    @override
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    @override
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return

    @override
    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, ast.stmt):
            self.lines.add(node.lineno)
        super().generic_visit(node)


def _statement_lines(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[int, ...]:
    visitor = _StatementVisitor()
    body = node.body
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        # coverage.py excludes callable docstrings from executable statements.
        body = body[1:]
    for child in body:
        visitor.visit(child)
    return tuple(sorted(visitor.lines))


def callable_blocks(source: str, *, path: str = "<memory>") -> list[CallableBlock]:
    """Return stable callable records for the v2 complexity algorithm."""
    tree = ast.parse(source, filename=path)
    blocks: list[CallableBlock] = []

    class Collector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.scope: list[str] = []

        @override
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.scope.append(node.name)
            for child in node.body:
                self.visit(child)
            self.scope.pop()

        @override
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._add(node)

        @override
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._add(node)

        def _add(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            qualified = ".".join((*self.scope, node.name))
            callable_id = f"{path}::{qualified}@{node.lineno}"
            blocks.append(
                CallableBlock(
                    callable_id=callable_id,
                    qualified_name=qualified,
                    line=node.lineno,
                    endline=node.end_lineno or node.lineno,
                    complexity=_complexity(node),
                    statement_lines=_statement_lines(node),
                )
            )
            self.scope.append(node.name)
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    self.visit(child)
            self.scope.pop()

    Collector().visit(tree)
    return blocks


def _integer_lines(value: object, label: str) -> set[int]:
    if not isinstance(value, list) or any(
        isinstance(item, bool) or not isinstance(item, int) or item < 1 for item in value
    ):
        raise EvidenceError(f"{label} must be a list of positive integer line numbers")
    return set(value)


def _coverage_files(payload: object, root: Path) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        raise EvidenceError("coverage JSON root must be an object")
    meta = payload.get("meta")
    files = payload.get("files")
    if not isinstance(meta, dict) or not isinstance(meta.get("version"), str):
        raise EvidenceError("coverage JSON requires meta.version from coverage.py")
    if not isinstance(files, dict):
        raise EvidenceError("coverage JSON requires a files object")
    normalized: dict[str, dict[str, Any]] = {}
    for raw_key, raw_entry in files.items():
        if not isinstance(raw_key, str) or not isinstance(raw_entry, dict):
            raise EvidenceError("coverage file entries must map string paths to objects")
        try:
            resolved = safe_path(root, raw_key, must_exist=True)
        except ConfigurationError as error:
            raise EvidenceError(f"unsafe coverage path {raw_key!r}: {error}") from error
        key = resolved.relative_to(root.resolve(strict=True)).as_posix()
        if raw_key.replace("\\", "/") != key:
            raise EvidenceError(
                f"coverage path must be exact repository-relative POSIX form: {raw_key!r}"
            )
        if key in normalized:
            raise EvidenceError(f"duplicate normalized coverage path: {key}")
        normalized[key] = raw_entry
    return normalized


def _validated_entry(entry: dict[str, Any], relative: str) -> tuple[set[int], set[int], set[int]]:
    executed = _integer_lines(entry.get("executed_lines"), f"{relative}.executed_lines")
    missing = _integer_lines(entry.get("missing_lines"), f"{relative}.missing_lines")
    excluded = _integer_lines(entry.get("excluded_lines"), f"{relative}.excluded_lines")
    if executed & missing or executed & excluded or missing & excluded:
        raise EvidenceError(f"coverage line sets overlap for {relative}")
    summary = entry.get("summary")
    if not isinstance(summary, dict):
        raise EvidenceError(f"coverage entry lacks summary for {relative}")
    expected = {
        "covered_lines": len(executed),
        "missing_lines": len(missing),
        "excluded_lines": len(excluded),
        "num_statements": len(executed | missing),
    }
    for name, value in expected.items():
        if summary.get(name) != value:
            raise EvidenceError(
                f"coverage summary mismatch for {relative}: "
                f"{name}={summary.get(name)!r}, expected {value}"
            )
    return executed, missing, excluded


def _load_coverage(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise EvidenceError(f"coverage JSON does not exist: {path}") from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"cannot parse coverage JSON {path}: {error}") from error


def build_crap_report(root: Path, coverage_path: Path) -> list[CrapRecord]:
    """Map complete, exact coverage.py evidence to callable records."""
    policy = load_policy(root)
    project = policy.get("project")
    if not isinstance(project, dict) or not isinstance(project.get("source_root"), str):
        raise ConfigurationError("policy project.source_root must be a string")
    source_root = safe_path(root, project["source_root"], must_exist=True)
    files = _coverage_files(_load_coverage(coverage_path), root)
    source_files = sorted(source_root.rglob("*.py"))
    if not source_files:
        raise EvidenceError(f"source root contains no Python files: {source_root}")
    records: list[CrapRecord] = []
    for path in source_files:
        if path.is_symlink():
            raise EvidenceError(f"source file cannot be a symlink: {path}")
        relative = path.relative_to(root).as_posix()
        entry = files.get(relative)
        if entry is None:
            raise EvidenceError(f"coverage JSON lacks governed source file: {relative}")
        executed, missing, excluded = _validated_entry(entry, relative)
        measurable = executed | missing
        try:
            blocks = callable_blocks(path.read_text(encoding="utf-8"), path=relative)
        except (OSError, UnicodeError, SyntaxError) as error:
            raise EvidenceError(f"cannot analyze governed source {relative}: {error}") from error
        for block in blocks:
            statements = set(block.statement_lines)
            unaccounted = statements - measurable - excluded
            if unaccounted:
                lines = ", ".join(str(line) for line in sorted(unaccounted))
                raise EvidenceError(
                    f"coverage evidence omits callable statement lines in "
                    f"{block.callable_id}: {lines}"
                )
            relevant = statements & measurable
            if not relevant:
                raise EvidenceError(
                    f"callable has no measurable coverage evidence: {block.callable_id}"
                )
            percent = 100.0 * len(relevant & executed) / len(relevant)
            records.append(
                CrapRecord(
                    path=relative,
                    callable_id=block.callable_id,
                    qualified_name=block.qualified_name,
                    line=block.line,
                    endline=block.endline,
                    complexity=block.complexity,
                    coverage_percent=round(percent, 2),
                    crap=round(crap_score(block.complexity, percent), 2),
                )
            )
    return sorted(records, key=_crap_sort_key)


def _crap_sort_key(item: CrapRecord) -> tuple[float, str, int, str]:
    return (-item.crap, item.path, item.line, item.callable_id)


def command_crap(root: Path, coverage: Path, *, strict: bool) -> int:
    """Generate CRAP evidence or fail closed on invalid prerequisites."""
    coverage_path = (
        coverage if coverage.is_absolute() else safe_path(root, coverage, must_exist=True)
    )
    records = build_crap_report(root, coverage_path)
    policy = load_policy(root)
    quality = policy.get("quality")
    if not isinstance(quality, dict):
        raise ConfigurationError("policy quality table is required")
    threshold = finite_number(quality.get("max_crap_score"), "quality.max_crap_score", minimum=1.0)
    output = evidence_run_dir(root, "quality")
    payload = {
        "schema_version": 2,
        "formula": "complexity^2 * (1 - line_coverage/100)^3 + complexity",
        "complexity_algorithm": COMPLEXITY_ALGORITHM,
        "coverage_schema": COVERAGE_SCHEMA,
        "coverage_path": coverage_path.relative_to(root).as_posix(),
        "threshold": threshold,
        "threshold_semantics": "strict failure only when worst score is greater than threshold",
        "records": [asdict(item) for item in records],
    }
    write_json(output / "crap-report.json", payload)
    lines = [
        "# CRAP report",
        "",
        "This is a line-coverage/local-AST sensor, not a correctness or basis-path proof.",
        "",
        "| CRAP | Complexity | Coverage | Callable |",
        "|---:|---:|---:|---|",
    ]
    lines.extend(
        f"| {item.crap:.2f} | {item.complexity} | "
        f"{item.coverage_percent:.2f}% | `{item.callable_id}` |"
        for item in records
    )
    atomic_write_text(output / "crap-report.md", "\n".join(lines) + "\n")
    worst = records[0].crap if records else 0.0
    print_line(f"Analyzed {len(records)} callables; worst CRAP={worst:.2f}; budget={threshold:.2f}")
    print_line(f"Evidence: {output.relative_to(root)}")
    return int(strict and worst > threshold)
