from __future__ import annotations

import json
import tomllib
from pathlib import Path

from cookiecutter.main import cookiecutter

ROOT = Path(__file__).parents[1]


def test_graft_experiment_renders_as_optional_external_tool(tmp_path: Path) -> None:
    project = Path(cookiecutter(str(ROOT), no_input=True, output_dir=str(tmp_path)))

    expected = (
        ".cleanai/graft-experiment.toml",
        "GRAFT_EXPERIMENT.md",
        "docs/integrations/graft.md",
        "docs/tutorials/evaluate-graft.md",
        "prompts/evaluate-graft.md",
        "tests/tooling/test_graft_adapter.py",
        "tools/graft_adapter.py",
        "tools/graft-runtime/README.md",
        "tools/graft-runtime/package-lock.json",
        "tools/graft-runtime/package.json",
    )
    for relative in expected:
        assert (project / relative).is_file(), relative

    pyproject = (project / "pyproject.toml").read_text(encoding="utf-8")
    assert "@nanonets/graft" not in pyproject
    assert not (project / ".mcp.json").exists()
    assert not (project / ".mcp.json.example").exists()

    policy = tomllib.loads(
        (project / ".cleanai/graft-experiment.toml").read_text(encoding="utf-8")
    )
    assert policy["package"] == "@nanonets/graft"
    assert policy["version"] == "0.16.0"
    assert policy["source_tag_commit"] == "aa1e2bb0f6326068ac64886da1e67fa25a7804de"
    assert policy["artifact_build_provenance"] == "UNVERIFIED"
    assert policy["npm_version"] == "10.9.0"
    assert policy["mode"] == "bounded-structural-cli"
    assert policy["mcp"] is False

    runtime = project / "tools/graft-runtime"
    package = json.loads((runtime / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((runtime / "package-lock.json").read_text(encoding="utf-8"))
    assert package["private"] is True
    assert package["dependencies"] == {"@nanonets/graft": "0.16.0"}
    assert lock["packages"]["node_modules/@nanonets/graft"]["version"] == "0.16.0"
    assert lock["packages"]["node_modules/@nanonets/graft"]["integrity"].startswith("sha512-")

    adapter = (project / "tools/graft_adapter.py").read_text(encoding="utf-8")
    assert "argparse.REMAINDER" not in adapter
    assert 'which("graft")' not in adapter
    assert "EXPECTED_GRAFT" in adapter

    ignored = (project / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".mcp.json" in ignored
    assert "artifacts/" in ignored
    assert "tools/graft-runtime/node_modules/" in ignored
    assert "tools/graft-runtime/.node_modules.previous/" in ignored
    assert "tools/graft-runtime/.node_modules.failed/" in ignored
    assert "tools/graft-runtime/.node_modules.installing/" in ignored

    command_prefix = "uv run --locked --group dev python tools/graft_adapter.py"
    for document in project.rglob("*.md"):
        content = document.read_text(encoding="utf-8")
        assert "python tools/graft_adapter.py" not in content.replace(command_prefix, "")


def test_graft_routes_are_discoverable_without_persistent_product_detail(tmp_path: Path) -> None:
    project = Path(cookiecutter(str(ROOT), no_input=True, output_dir=str(tmp_path)))

    assert "GRAFT_EXPERIMENT.md" in (project / "README.md").read_text(encoding="utf-8")
    assert "GRAFT_EXPERIMENT.md" in (project / "AGENTS.md").read_text(encoding="utf-8")
    assert "integrations/graft.md" in (project / "docs/index.md").read_text(encoding="utf-8")
    assert "evaluate-graft.md" in (project / "prompts/README.md").read_text(encoding="utf-8")

    agents = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.count("Graft") <= 2
    assert "Graft output" not in agents


def test_graft_hidden_source_limit_is_disclosed_with_safe_recovery(tmp_path: Path) -> None:
    project = Path(cookiecutter(str(ROOT), no_input=True, output_dir=str(tmp_path)))

    experiment = (project / "GRAFT_EXPERIMENT.md").read_text(encoding="utf-8")
    integration = (project / "docs/integrations/graft.md").read_text(encoding="utf-8")
    troubleshooting = (project / "docs/troubleshooting.md").read_text(encoding="utf-8")

    for document in (experiment, integration, troubleshooting):
        plain = document.replace("**", "").lower()
        assert "hidden director" in plain
        assert "f0" in plain
        assert "do not untrack" in plain

    assert ".hidden/visible.py" in integration
    assert "publishes no graph" in integration
    assert ".hidden/visible.py" in troubleshooting
    assert "removes the staged graph" in troubleshooting


def test_existing_project_adoption_route_is_current_and_safety_first() -> None:
    guide_path = ROOT / "ADOPT_EXISTING_PROJECT.md"
    assert guide_path.is_file()

    guide = guide_path.read_text(encoding="utf-8")
    variant = (ROOT / "GRAFT_VARIANT.md").read_text(encoding="utf-8")

    assert "Never generate this Cookiecutter directly into an existing repository" in guide
    assert "generate the template into a separate sibling directory" in guide
    assert "Audit before implementation" in guide
    assert "Add Graft only after the repository is ready" in guide
    assert "baseline-no-graft" in guide
    assert "graft-structural-cli" in guide
    assert "ADOPT_EXISTING_PROJECT.md" in variant
    assert "--checkout experimental-graft-variant" in variant
    assert "--checkout audit/experimental-graft-variant-v2" not in variant
