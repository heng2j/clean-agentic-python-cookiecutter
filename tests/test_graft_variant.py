from __future__ import annotations

import json
from pathlib import Path

from cookiecutter.main import cookiecutter

ROOT = Path(__file__).parents[1]


def test_graft_experiment_renders_as_optional_external_tool(tmp_path: Path) -> None:
    project = Path(cookiecutter(str(ROOT), no_input=True, output_dir=str(tmp_path)))

    expected = (
        ".cleanai/graft-experiment.toml",
        ".mcp.json.example",
        "GRAFT_EXPERIMENT.md",
        "docs/integrations/graft.md",
        "docs/tutorials/evaluate-graft.md",
        "prompts/evaluate-graft.md",
        "tests/tooling/test_graft_adapter.py",
        "tools/graft_adapter.py",
    )
    for relative in expected:
        assert (project / relative).is_file(), relative

    pyproject = (project / "pyproject.toml").read_text(encoding="utf-8")
    assert "@nanonets/graft" not in pyproject
    assert not (project / ".mcp.json").exists()

    mcp = json.loads((project / ".mcp.json.example").read_text(encoding="utf-8"))
    assert mcp["mcpServers"]["graft"]["command"] == "uv"
    assert mcp["mcpServers"]["graft"]["args"][-2:] == ["run", "mcp"]

    adapter = (project / "tools/graft_adapter.py").read_text(encoding="utf-8")
    assert 'EXPECTED_GRAFT: Final = (0, 17, 0)' in adapter
    assert '"--deep"' in adapter
    assert '"init"' in adapter
