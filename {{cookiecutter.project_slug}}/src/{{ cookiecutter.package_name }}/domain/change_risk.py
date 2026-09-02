"""Pure release-decision policy used by the quality-harness example."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite

PERCENTAGE_MAX = 100.0


class DecisionStatus(StrEnum):
    """Possible release decisions."""

    APPROVED = "approved"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class QualityPolicy:
    """Human-owned thresholds."""

    max_crap_score: float = {{ cookiecutter.max_crap_score }}.0
    minimum_mutation_score: float = {{ cookiecutter.minimum_mutation_score }}.0


@dataclass(frozen=True, slots=True)
class ReleaseEvidence:
    """Machine-produced evidence presented to the policy."""

    failed_tests: int
    static_analysis_findings: int
    architecture_violations: int
    security_findings: int
    max_crap_score: float
    mutation_score: float
    touches_trust_boundary: bool = False
    trust_boundary_review_complete: bool = False


@dataclass(frozen=True, slots=True)
class ReleaseDecision:
    """Decision plus all deterministic blocking reasons."""

    status: DecisionStatus
    reasons: tuple[str, ...]

    @property
    def approved(self) -> bool:
        """Return whether the policy approved the evidence."""
        return self.status is DecisionStatus.APPROVED


def evaluate_release(
    evidence: ReleaseEvidence,
    policy: QualityPolicy | None = None,
) -> ReleaseDecision:
    """Evaluate raw evidence without side effects or hidden sanitization."""
    effective_policy = policy or QualityPolicy()
    _validate(evidence, effective_policy)
    reasons = _blocking_reasons(evidence, effective_policy)
    status = DecisionStatus.BLOCKED if reasons else DecisionStatus.APPROVED
    return ReleaseDecision(status=status, reasons=tuple(reasons))


def _blocking_reasons(
    evidence: ReleaseEvidence,
    policy: QualityPolicy,
) -> list[str]:
    reasons: list[str] = []
    if evidence.failed_tests > 0:
        reasons.append("tests failed")
    if evidence.static_analysis_findings > 0:
        reasons.append("static-analysis findings remain")
    if evidence.architecture_violations > 0:
        reasons.append("architecture violations remain")
    if evidence.security_findings > 0:
        reasons.append("security findings remain")
    if evidence.max_crap_score > policy.max_crap_score:
        reasons.append("CRAP budget exceeded")
    if evidence.mutation_score < policy.minimum_mutation_score:
        reasons.append("mutation score below floor")
    if evidence.touches_trust_boundary and not evidence.trust_boundary_review_complete:
        reasons.append("trust-boundary review incomplete")
    return reasons


def _validate(evidence: ReleaseEvidence, policy: QualityPolicy) -> None:
    counts = (
        evidence.failed_tests,
        evidence.static_analysis_findings,
        evidence.architecture_violations,
        evidence.security_findings,
    )
    if any(value < 0 for value in counts):
        raise ValueError("finding counts must be non-negative")
    if not isfinite(evidence.max_crap_score) or evidence.max_crap_score < 0:
        raise ValueError("max_crap_score must be finite and non-negative")
    percentages = (evidence.mutation_score, policy.minimum_mutation_score)
    if any(not isfinite(value) or not 0 <= value <= PERCENTAGE_MAX for value in percentages):
        raise ValueError("mutation scores must be finite percentages in [0, 100]")
    if not isfinite(policy.max_crap_score) or policy.max_crap_score < 0:
        raise ValueError("policy.max_crap_score must be finite and non-negative")
