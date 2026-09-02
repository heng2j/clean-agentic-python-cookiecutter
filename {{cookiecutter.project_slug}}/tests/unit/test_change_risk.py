from __future__ import annotations

import pytest

from {{ cookiecutter.package_name }}.domain.change_risk import (
    DecisionStatus,
    QualityPolicy,
    ReleaseEvidence,
    evaluate_release,
)


def healthy(**overrides: object) -> ReleaseEvidence:
    values: dict[str, object] = {
        "failed_tests": 0,
        "static_analysis_findings": 0,
        "architecture_violations": 0,
        "security_findings": 0,
        "max_crap_score": 11.0,
        "mutation_score": 95.0,
        "touches_trust_boundary": False,
        "trust_boundary_review_complete": False,
    }
    values.update(overrides)
    return ReleaseEvidence(**values)  # type: ignore[arg-type]


def test_healthy_evidence_is_approved() -> None:
    decision = evaluate_release(healthy())

    assert decision.status is DecisionStatus.APPROVED
    assert decision.reasons == ()


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"failed_tests": 1}, "tests failed"),
        ({"static_analysis_findings": 1}, "static-analysis findings remain"),
        ({"architecture_violations": 1}, "architecture violations remain"),
        ({"security_findings": 1}, "security findings remain"),
        ({"max_crap_score": 31.0}, "CRAP budget exceeded"),
        ({"mutation_score": 79.0}, "mutation score below floor"),
        ({"touches_trust_boundary": True}, "trust-boundary review incomplete"),
    ],
)
def test_each_failed_gate_blocks(overrides: dict[str, object], reason: str) -> None:
    decision = evaluate_release(healthy(**overrides))

    assert decision.status is DecisionStatus.BLOCKED
    assert reason in decision.reasons


def test_completed_trust_review_unblocks_that_reason() -> None:
    decision = evaluate_release(
        healthy(
            touches_trust_boundary=True,
            trust_boundary_review_complete=True,
        )
    )

    assert decision.approved


@pytest.mark.parametrize(
    ("bad", "message"),
    [
        (healthy(failed_tests=-1), "finding counts"),
        (healthy(max_crap_score=float("nan")), "max_crap_score"),
        (healthy(mutation_score=101.0), "mutation scores"),
    ],
)
def test_invalid_raw_evidence_fails_closed(bad: ReleaseEvidence, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        evaluate_release(bad)


def test_policy_is_explicit_and_replaceable() -> None:
    policy = QualityPolicy(max_crap_score=10.0, minimum_mutation_score=99.0)

    decision = evaluate_release(healthy(), policy)

    assert set(decision.reasons) == {
        "CRAP budget exceeded",
        "mutation score below floor",
    }
