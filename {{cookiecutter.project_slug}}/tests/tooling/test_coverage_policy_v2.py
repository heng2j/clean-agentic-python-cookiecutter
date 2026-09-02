from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.cleanai_core.coverage_policy import command_coverage_policy, coverage_groups
from tools.cleanai_core.model import ConfigurationError, EvidenceError


def _repository(root: Path) -> tuple[Path, Path]:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        """[project]
source_root = "src/pkg"
[quality]
minimum_coverage = 90
minimum_harness_coverage = 70
""",
        encoding="utf-8",
    )
    product = root / "src/pkg/model.py"
    product.parent.mkdir(parents=True)
    product.write_text("VALUE = 1\n", encoding="utf-8")
    harness = root / "tools/check.py"
    harness.parent.mkdir()
    harness.write_text("VALUE = 1\n", encoding="utf-8")
    return product, harness


def _entry(covered_lines: int, statements: int, covered_branches: int, branches: int) -> dict:
    return {
        "summary": {
            "covered_lines": covered_lines,
            "num_statements": statements,
            "covered_branches": covered_branches,
            "num_branches": branches,
        }
    }


def _coverage(root: Path, product: dict, harness: dict) -> Path:
    path = root / "coverage.json"
    path.write_text(
        json.dumps(
            {
                "meta": {"version": "7.16.0"},
                "files": {"src/pkg/model.py": product, "tools/check.py": harness},
            }
        ),
        encoding="utf-8",
    )
    return path


def test_product_and_harness_floors_are_independent_and_branch_aware(tmp_path: Path) -> None:
    _repository(tmp_path)
    coverage = _coverage(tmp_path, _entry(9, 10, 1, 1), _entry(7, 10, 0, 0))
    product, harness = coverage_groups(tmp_path, coverage)
    assert product.percent == pytest.approx(90.91)
    assert product.minimum_percent == 90.0
    assert harness.percent == 70.0
    assert harness.minimum_percent == 70.0
    assert command_coverage_policy(tmp_path, coverage, strict=True) == 0


def test_below_floor_returns_one_and_absent_file_fails_closed(tmp_path: Path) -> None:
    _repository(tmp_path)
    coverage = _coverage(tmp_path, _entry(10, 10, 0, 0), _entry(6, 10, 0, 0))
    assert command_coverage_policy(tmp_path, coverage, strict=False) == 0
    assert command_coverage_policy(tmp_path, coverage, strict=True) == 1
    payload = json.loads(coverage.read_text(encoding="utf-8"))
    del payload["files"]["tools/check.py"]
    coverage.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(EvidenceError, match="lacks required harness file"):
        coverage_groups(tmp_path, coverage)


def test_coverage_policy_rejects_malformed_counts_and_external_evidence(tmp_path: Path) -> None:
    _repository(tmp_path)
    coverage = _coverage(tmp_path, _entry(11, 10, 0, 0), _entry(10, 10, 0, 0))
    with pytest.raises(EvidenceError, match="exceed measurable"):
        coverage_groups(tmp_path, coverage)
    outside = tmp_path.parent / "outside-coverage.json"
    outside.write_text("{}", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="inside the repository"):
        command_coverage_policy(tmp_path, outside, strict=True)
