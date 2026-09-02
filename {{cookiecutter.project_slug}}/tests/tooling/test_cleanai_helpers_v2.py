from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
from tools.cleanai_core.crap import build_crap_report, callable_blocks, crap_score
from tools.cleanai_core.docs import parse_frontmatter
from tools.cleanai_core.io import classify_command, safe_path
from tools.cleanai_core.model import ConfigurationError, EvidenceError


def _policy(root: Path, extra: str = "") -> None:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        """[project]
package = "pkg"
source_root = "src/pkg"
docs_root = "docs"
[quality]
max_crap_score = 30
minimum_coverage = 90
minimum_mutation_score = 80
"""
        + extra,
        encoding="utf-8",
    )


def test_crap_formula_and_domain_boundaries() -> None:
    assert crap_score(5, 0.0) == pytest.approx(30.0)
    assert crap_score(10, 50.0) == pytest.approx(22.5)
    assert crap_score(1, 100.0) == pytest.approx(1.0)
    for value in (-1.0, 101.0, math.nan, math.inf):
        with pytest.raises(ValueError, match="coverage_percent"):
            crap_score(2, value)
    with pytest.raises(ValueError, match="complexity"):
        crap_score(True, 50.0)


def test_callable_complexity_keeps_nested_scopes_separate() -> None:
    source = """async def outer(value):
    if value and value > 1:
        return [item for item in value if item]
    def inner(flag):
        return 1 if flag else 0
    return []
"""
    blocks = callable_blocks(source, path="src/pkg/sample.py")
    assert [block.qualified_name for block in blocks] == ["outer", "outer.inner"]
    assert [block.complexity for block in blocks] == [5, 2]
    assert 4 not in blocks[0].statement_lines


def test_callable_docstring_is_not_required_as_coverage_statement() -> None:
    blocks = callable_blocks(
        'def documented() -> int:\n    """Not executable coverage evidence."""\n    return 1\n'
    )

    assert blocks[0].statement_lines == (3,)


def test_crap_requires_exact_complete_coverage(tmp_path: Path) -> None:
    _policy(tmp_path)
    source = tmp_path / "src/pkg"
    source.mkdir(parents=True)
    (source / "sample.py").write_text(
        "def sample(value):\n    if value:\n        return 1\n    return 0\n",
        encoding="utf-8",
    )
    coverage = tmp_path / "coverage.json"
    payload = {
        "meta": {"version": "7.16.0"},
        "files": {
            "src/pkg/sample.py": {
                "executed_lines": [2, 3, 4],
                "missing_lines": [],
                "excluded_lines": [],
                "summary": {
                    "covered_lines": 3,
                    "missing_lines": 0,
                    "excluded_lines": 0,
                    "num_statements": 3,
                },
            }
        },
    }
    coverage.write_text(json.dumps(payload), encoding="utf-8")
    records = build_crap_report(tmp_path, coverage)
    assert records[0].coverage_percent == 100.0
    del payload["files"]["src/pkg/sample.py"]
    coverage.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(EvidenceError, match="lacks governed source file"):
        build_crap_report(tmp_path, coverage)


def test_crap_rejects_malformed_and_suffix_only_coverage(tmp_path: Path) -> None:
    _policy(tmp_path)
    source = tmp_path / "src/pkg"
    source.mkdir(parents=True)
    (source / "sample.py").write_text("def sample():\n    return 1\n", encoding="utf-8")
    other = tmp_path / "other"
    other.mkdir()
    (other / "sample.py").write_text("def sample():\n    return 1\n", encoding="utf-8")
    coverage = tmp_path / "coverage.json"
    coverage.write_text('{"files": {}}', encoding="utf-8")
    with pytest.raises(EvidenceError, match=r"meta\.version"):
        build_crap_report(tmp_path, coverage)
    payload = {
        "meta": {"version": "7.16"},
        "files": {
            "other/sample.py": {
                "executed_lines": [2],
                "missing_lines": [],
                "excluded_lines": [],
                "summary": {
                    "covered_lines": 1,
                    "missing_lines": 0,
                    "excluded_lines": 0,
                    "num_statements": 1,
                },
            }
        },
    }
    coverage.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(EvidenceError, match="lacks governed source file"):
        build_crap_report(tmp_path, coverage)


def test_safe_path_rejects_lexical_and_symlink_escape(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(ConfigurationError):
        safe_path(root, "../outside")
    (root / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ConfigurationError, match="symlink"):
        safe_path(root, "link/file")


def test_connected_command_classification_covers_module_invocation() -> None:
    assert classify_command(["pip-audit", "--format=json"]) == "connected"
    assert classify_command(["python", "-m", "pip_audit", "--format=json"]) == "connected"
    assert classify_command(["python3.13", "-m", "pip-audit"]) == "connected"
    assert classify_command(["uv", "export", "--locked"]) == "deterministic-local"


def test_frontmatter_safe_subset_and_duplicates() -> None:
    metadata, body = parse_frontmatter(
        '---\nstatus: reference\napplies_to: ["src/**"]\n---\n# Title\n'
    )
    assert metadata["status"] == "reference"
    assert metadata["applies_to"] == ["src/**"]
    assert body.startswith("# Title")
    with pytest.raises(ConfigurationError, match="duplicate"):
        parse_frontmatter("---\nstatus: draft\nstatus: normative\n---\n")


def test_frontmatter_accepts_safe_yaml_variants() -> None:
    metadata, body = parse_frontmatter(
        """---
# YAML comments and quoted globs are legitimate.
status: normative
owner: "maintainers"
authority: yaml-fixture
last_verified: 2026-09-01
applies_to: ["src/**", 'tests/**']
note: >-
  folded reference text
  remains data
---
# Body
"""
    )

    assert metadata["last_verified"] == "2026-09-01"
    assert metadata["applies_to"] == ["src/**", "tests/**"]
    assert metadata["note"] == "folded reference text remains data"
    assert body.startswith("# Body")
