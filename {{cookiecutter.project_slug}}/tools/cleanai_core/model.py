"""Shared immutable models and controlled harness errors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class CleanAIError(Exception):
    """Base class for a controlled harness failure."""


class ConfigurationError(CleanAIError):
    """Configuration is absent, malformed, ambiguous, or unsafe."""


class EvidenceError(CleanAIError):
    """Required evidence is absent, malformed, incomplete, or mismatched."""


@dataclass(frozen=True, slots=True)
class Finding:
    """One machine-readable audit finding."""

    severity: str
    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Complete result of one configured command."""

    configured_command: str
    argv: tuple[str, ...]
    status: str
    returncode: int
    duration_seconds: float
    stdout: str
    stderr: str
    classification: str
    error: str | None = None


@dataclass(frozen=True, slots=True)
class CallableBlock:
    """One callable and the local, versioned complexity approximation."""

    callable_id: str
    qualified_name: str
    line: int
    endline: int
    complexity: int
    statement_lines: tuple[int, ...]

    @property
    def name(self) -> str:
        """Compatibility alias retained for template adopters."""
        return self.qualified_name


@dataclass(frozen=True, slots=True)
class CrapRecord:
    """One callable's complexity, coverage, and CRAP estimate."""

    path: str
    callable_id: str
    qualified_name: str
    line: int
    endline: int
    complexity: int
    coverage_percent: float
    crap: float


@dataclass(frozen=True, slots=True)
class MutationResult:
    """One isolated curated mutation result."""

    mutation_id: str
    path: str
    status: str
    returncode: int
    duration_seconds: float
    stdout: str
    stderr: str
    reason: str


@dataclass(frozen=True, slots=True)
class BenchmarkTask:
    """One repeatable agent-friction task."""

    task_id: str
    title: str
    prompt: str
    expected_globs: tuple[str, ...]
    forbidden_globs: tuple[str, ...]
    verification: tuple[str, ...]


JsonObject = dict[str, Any]
