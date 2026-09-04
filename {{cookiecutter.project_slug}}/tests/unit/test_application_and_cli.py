from __future__ import annotations

import json
from pathlib import Path

import pytest

from {{ cookiecutter.package_name }}.adapters.cli import main
from {{ cookiecutter.package_name }}.application.assess_release import assess_release
from {{ cookiecutter.package_name }}.domain.change_risk import (
    QualityPolicy,
    ReleaseEvidence,
)


def evidence(**overrides: object) -> ReleaseEvidence:
    values: dict[str, object] = {
        "failed_tests": 0,
        "static_analysis_findings": 0,
        "architecture_violations": 0,
        "security_findings": 0,
        "max_crap_score": 11.0,
        "mutation_score": 95.0,
    }
    values.update(overrides)
    return ReleaseEvidence(**values)  # type: ignore[arg-type]


def test_application_accepts_an_explicit_policy() -> None:
    decision = assess_release(evidence(), QualityPolicy(max_crap_score=10.0))

    assert decision.reasons == ("CRAP budget exceeded",)


def test_cli_uses_exit_codes_and_json(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    clean = {
        "failed_tests": 0,
        "static_analysis_findings": 0,
        "architecture_violations": 0,
        "security_findings": 0,
        "max_crap_score": 11,
        "mutation_score": 95,
    }
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(clean), encoding="utf-8")

    assert main([str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "approved"

    clean["failed_tests"] = 1
    path.write_text(json.dumps(clean), encoding="utf-8")
    assert main([str(path)]) == 1
    assert "tests failed" in json.loads(capsys.readouterr().out)["reasons"]


@pytest.mark.parametrize("payload", ["[]", "{not-json", '{"failed_tests": 0}'])
def test_cli_rejects_malformed_or_incomplete_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    payload: str,
) -> None:
    path = tmp_path / "bad.json"
    path.write_text(payload, encoding="utf-8")

    assert main([str(path)]) == 2
    assert "invalid evidence:" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("failed_tests", False),
        ("max_crap_score", "11"),
        ("touches_trust_boundary", "false"),
        ("trust_boundary_review_complete", "false"),
    ],
)
def test_cli_rejects_coerced_evidence_types(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    field: str,
    value: object,
) -> None:
    payload: dict[str, object] = {
        "failed_tests": 0,
        "static_analysis_findings": 0,
        "architecture_violations": 0,
        "security_findings": 0,
        "max_crap_score": 11,
        "mutation_score": 95,
        field: value,
    }
    path = tmp_path / "coerced.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert main([str(path)]) == 2
    assert "invalid evidence:" in capsys.readouterr().err


def test_cli_rejects_unknown_evidence_fields(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    payload = {
        "failed_tests": 0,
        "static_analysis_findings": 0,
        "architecture_violations": 0,
        "security_findings": 0,
        "max_crap_score": 11,
        "mutation_score": 95,
        "approve_anyway": True,
    }
    path = tmp_path / "unknown.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert main([str(path)]) == 2
    assert "documented schema" in capsys.readouterr().err
