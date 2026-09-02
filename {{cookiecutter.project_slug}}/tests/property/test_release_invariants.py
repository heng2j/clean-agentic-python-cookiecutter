from __future__ import annotations

import itertools

import pytest

from {{ cookiecutter.package_name }}.domain.change_risk import (
    DecisionStatus,
    ReleaseEvidence,
    evaluate_release,
)


@pytest.mark.parametrize(
    ("failed_tests", "mutation_score", "max_crap_score"),
    list(itertools.product((1, 2, 100), (0.0, 80.0, 100.0), (0.0, 30.0, 1000.0))),
)
def test_failed_tests_always_block(
    failed_tests: int,
    mutation_score: float,
    max_crap_score: float,
) -> None:
    evidence = ReleaseEvidence(
        failed_tests=failed_tests,
        static_analysis_findings=0,
        architecture_violations=0,
        security_findings=0,
        max_crap_score=max_crap_score,
        mutation_score=mutation_score,
    )

    assert evaluate_release(evidence).status is DecisionStatus.BLOCKED
