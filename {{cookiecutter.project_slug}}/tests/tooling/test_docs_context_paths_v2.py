from __future__ import annotations

from pathlib import Path

import pytest
from tools.cleanai_core.docs import (
    command_context,
    command_docs,
    command_prune,
    context_findings,
    docs_findings,
    parse_frontmatter,
    prune_plan,
)
from tools.cleanai_core.model import ConfigurationError


def _policy(root: Path) -> None:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        """[project]
docs_root = "docs"
[context]
root_agents_max_lines = 8
root_agents_max_words = 35
root_claude_max_lines = 4
scoped_max_lines = 3
warn_doc_age_days = 180
required_sections = ["Repository map", "Canonical commands"]
""",
        encoding="utf-8",
    )


def _document(body: str, *, status: str = "normative", authority: str = "fixture") -> str:
    return (
        "---\n"
        f"status: {status}\nowner: maintainers\nauthority: {authority}\n"
        'last_verified: 2026-09-01\napplies_to: ["src/**"]\n---\n' + body
    )


def test_docs_audit_covers_lifecycle_links_anchors_archive_and_symlinks(tmp_path: Path) -> None:
    _policy(tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    assert {finding.code for finding in docs_findings(tmp_path)} == {"docs.empty"}
    (docs / "target.md").write_text(
        _document("# Section\n\n## Repeated\n\n## Repeated\n", authority="target"),
        encoding="utf-8",
    )
    (docs / "broken.md").write_text(
        _document(
            "# Broken\n\n[missing](absent.md) [anchor](target.md#not-there)\n"
            "42 passing tests. TODO decide.\n",
            authority="broken",
        ),
        encoding="utf-8",
    )
    (docs / "future.md").write_text(
        _document("# Future\n", authority="future").replace(
            "last_verified: 2026-09-01", "last_verified: 2099-01-01"
        ),
        encoding="utf-8",
    )
    (docs / "stale.md").write_text(
        _document("# Stale\n", authority="stale").replace(
            "last_verified: 2026-09-01", "last_verified: 2020-01-01"
        ),
        encoding="utf-8",
    )
    (docs / "old.md").write_text(
        _document("# Old\n", status="historical", authority="old"), encoding="utf-8"
    )
    (docs / "missing-frontmatter.md").write_text("# No metadata\n", encoding="utf-8")
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    (docs / "linked.md").symlink_to(outside)
    codes = {finding.code for finding in docs_findings(tmp_path)}
    assert {
        "docs.dead-or-unsafe-link",
        "docs.dead-anchor",
        "docs.dynamic-test-count",
        "docs.unresolved-marker",
        "docs.future-verification",
        "docs.verification-age",
        "docs.archive-location",
        "docs.frontmatter",
        "docs.symlink",
    } <= codes
    assert command_docs(tmp_path, strict=False) == 0
    assert command_docs(tmp_path, strict=True) == 1


def test_frontmatter_accepts_yaml_indentation_and_rejects_invalid_documents() -> None:
    with pytest.raises(ConfigurationError, match="no closing"):
        parse_frontmatter("---\nstatus: draft\n")
    metadata, _body = parse_frontmatter("---\n status: draft\n---\n")
    assert metadata == {"status": "draft"}
    with pytest.raises(ConfigurationError, match="must be a YAML mapping"):
        parse_frontmatter("---\n  - orphan\n---\n")
    with pytest.raises(ConfigurationError, match="invalid YAML"):
        parse_frontmatter("---\napplies_to: [not valid\n---\n")


def test_context_audit_reports_budgets_loading_conflicts_and_dead_references(
    tmp_path: Path,
) -> None:
    _policy(tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text(
        _document("# Context index\n", authority="context-index"), encoding="utf-8"
    )
    (tmp_path / "AGENTS.md").write_text(
        """# Agent rules
## Repository map
Always preserve exact release evidence for every bounded task.
Always deploy.
Read every file in the entire repository before any task.
There are 58 tests.
See https://example.invalid/issues/12.
Read `missing.md`.
extra words make this context deliberately exceed its configured word budget now
""",
        encoding="utf-8",
    )
    (tmp_path / "CLAUDE.md").write_text(
        """# Claude
Always preserve exact release evidence for every bounded task.
Never deploy.
extra line
extra line
""",
        encoding="utf-8",
    )
    scoped = tmp_path / ".claude/rules/python.md"
    scoped.parent.mkdir(parents=True)
    scoped.write_text("one\ntwo\nthree\nfour\n", encoding="utf-8")
    findings, metrics = context_findings(tmp_path)
    codes = {finding.code for finding in findings}
    assert {
        "context.word-budget",
        "context.missing-section",
        "context.line-budget",
        "context.low-precision",
        "context.dynamic-fact",
        "context.issue-history",
        "context.dead-or-unsafe-reference",
        "context.claude-import",
        "context.duplicate-authority",
        "context.contradiction",
    } <= codes
    assert metrics["context_files"] == 3
    assert len(metrics["loading_source_inventory"]) == 3
    assert command_context(tmp_path, strict=False) == 0
    assert command_context(tmp_path, strict=True) == 1
    plan = prune_plan(tmp_path)
    assert "context.low-precision" in plan
    output = tmp_path / "artifacts/prune.md"
    assert command_prune(tmp_path, output.relative_to(tmp_path)) == 0
    assert output.read_text(encoding="utf-8") == plan
    with pytest.raises(ConfigurationError, match="inside repository"):
        command_prune(tmp_path, tmp_path.parent / "outside-plan.md")
