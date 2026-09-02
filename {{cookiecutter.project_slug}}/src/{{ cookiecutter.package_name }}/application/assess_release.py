"""Application use case."""

from {{ cookiecutter.package_name }}.domain.change_risk import (
    QualityPolicy,
    ReleaseDecision,
    ReleaseEvidence,
    evaluate_release,
)


def assess_release(
    evidence: ReleaseEvidence,
    policy: QualityPolicy | None = None,
) -> ReleaseDecision:
    """Apply explicit policy to already-collected evidence."""
    return evaluate_release(evidence, policy)
