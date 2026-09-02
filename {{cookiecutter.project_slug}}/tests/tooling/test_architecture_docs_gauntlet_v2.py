from __future__ import annotations

import json
from pathlib import Path

from tools.cleanai_core.architecture import architecture_findings
from tools.cleanai_core.docs import docs_findings
from tools.cleanai_core.gauntlet import command_gauntlet


def _architecture_repo(root: Path) -> Path:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        """[project]
package = "pkg"
source_root = "src/pkg"
docs_root = "docs"
[architecture]
"pkg.domain" = 0
"pkg.application" = 1
"pkg.adapters" = 2
[architecture_options]
detect_cycles = true
""",
        encoding="utf-8",
    )
    source = root / "src/pkg"
    for layer in ("domain", "application", "adapters"):
        directory = source / layer
        directory.mkdir(parents=True)
        (directory / "__init__.py").write_text("", encoding="utf-8")
    return source


def test_architecture_detects_relative_type_dynamic_and_cycles(tmp_path: Path) -> None:
    source = _architecture_repo(tmp_path)
    (source / "domain/a.py").write_text(
        "from typing import TYPE_CHECKING\n"
        "if TYPE_CHECKING:\n    from ..adapters import port\n"
        "import importlib\nimportlib.import_module('pkg.adapters.port')\n",
        encoding="utf-8",
    )
    (source / "adapters/port.py").write_text("VALUE = 1\n", encoding="utf-8")
    (source / "application/a.py").write_text("from . import b\n", encoding="utf-8")
    (source / "application/b.py").write_text("from . import a\n", encoding="utf-8")
    findings = architecture_findings(tmp_path)
    codes = [finding.code for finding in findings]
    assert codes.count("architecture.outward-import") >= 2
    assert "architecture.cycle" in codes


def test_similarly_named_external_package_is_not_internal(tmp_path: Path) -> None:
    source = _architecture_repo(tmp_path)
    (source / "domain/a.py").write_text("import pkg_extra.adapters\n", encoding="utf-8")
    assert architecture_findings(tmp_path) == []


def _document(text: str, authority: str, status: str = "normative") -> str:
    return (
        "---\n"
        f"status: {status}\nowner: maintainers\nauthority: {authority}\n"
        'last_verified: 2026-09-01\napplies_to: ["src/**"]\n---\n'
        f"# {authority}\n\n{text}\n"
    )


def test_reference_authorities_do_not_create_normative_duplicates(tmp_path: Path) -> None:
    cleanai = tmp_path / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        """[project]
docs_root = "docs"
[context]
warn_doc_age_days = 180
""",
        encoding="utf-8",
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text(_document("Evidence", "shared", "reference"), encoding="utf-8")
    (docs / "b.md").write_text(_document("Evidence", "shared", "reference"), encoding="utf-8")
    assert not any(
        finding.code == "docs.duplicate-authority" for finding in docs_findings(tmp_path)
    )
    (docs / "a.md").write_text(_document("Rule", "shared"), encoding="utf-8")
    (docs / "b.md").write_text(_document("Rule", "shared"), encoding="utf-8")
    assert any(finding.code == "docs.duplicate-authority" for finding in docs_findings(tmp_path))


def test_gauntlet_missing_tool_has_ledger_and_skips_following(tmp_path: Path) -> None:
    cleanai = tmp_path / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text(
        """[execution]
command_timeout_seconds = 2
[gauntlet.fast]
commands = ["definitely-not-a-real-cleanai-command", "python -c 'pass'"]
""",
        encoding="utf-8",
    )
    assert command_gauntlet(tmp_path, "fast") == 2
    evidence = max((tmp_path / "artifacts/gauntlet/runs").iterdir())
    report = json.loads((evidence / "gauntlet-fast.json").read_text(encoding="utf-8"))
    assert [row["status"] for row in report["results"]] == ["error", "skipped"]
    assert report["results"][0]["returncode"] == 127
