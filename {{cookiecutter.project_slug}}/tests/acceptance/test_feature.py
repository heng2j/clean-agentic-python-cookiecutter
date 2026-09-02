from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pytest

from {{ cookiecutter.package_name }}.domain.change_risk import (
    DecisionStatus,
    ReleaseEvidence,
    evaluate_release,
)


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    evidence: ReleaseEvidence
    expected: DecisionStatus
    reason: str | None


def _parse_feature() -> list[Scenario]:
    feature = Path(__file__).parent / "features" / "release_decision.feature"
    text = feature.read_text(encoding="utf-8")
    blocks = re.split(r"^\s*Scenario:\s*", text, flags=re.MULTILINE)[1:]
    return [_parse_block(block) for block in blocks]


def _parse_block(block: str) -> Scenario:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    body = "\n".join(lines[1:])
    crap = re.search(r"maximum CRAP score is (\d+)", body)
    mutation = re.search(r"mutation score is (\d+)", body)
    if crap is None or mutation is None:
        raise ValueError(f"scenario lacks numeric evidence: {lines[0]}")
    status = (
        DecisionStatus.APPROVED
        if "Then the release is approved" in body
        else DecisionStatus.BLOCKED
    )
    reason = re.search(r'And "([^"]+)" is a reason', body)
    evidence = ReleaseEvidence(
        failed_tests=0,
        static_analysis_findings=0,
        architecture_violations=0,
        security_findings=0,
        max_crap_score=float(crap.group(1)),
        mutation_score=float(mutation.group(1)),
    )
    return Scenario(
        name=lines[0],
        evidence=evidence,
        expected=status,
        reason=reason.group(1) if reason else None,
    )


@pytest.mark.parametrize("scenario", _parse_feature(), ids=lambda scenario: scenario.name)
def test_executable_scenario(scenario: Scenario) -> None:
    decision = evaluate_release(scenario.evidence)

    assert decision.status is scenario.expected
    if scenario.reason:
        assert scenario.reason in decision.reasons
