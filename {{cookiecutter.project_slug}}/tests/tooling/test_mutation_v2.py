from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from tools.cleanai_core.model import ConfigurationError
from tools.cleanai_core.mutation import command_mutate


def _write_config(root: Path, body: str, *, minimum: str = "100") -> Path:
    cleanai = root / ".cleanai"
    cleanai.mkdir(exist_ok=True)
    config = cleanai / "mutations.toml"
    config.write_text(
        f'name = "fixture"\nbaseline_command = "python -c \'pass\'"\n'
        f"minimum_score = {minimum}\ntimeout_seconds = 2\n{body}",
        encoding="utf-8",
    )
    return config


def _source(root: Path) -> Path:
    source = root / "sample.py"
    source.write_text("FLAG = True\n", encoding="utf-8")
    return source


def test_mutation_isolated_and_killed_only_by_explicit_oracle(tmp_path: Path) -> None:
    source = _source(tmp_path)
    original = hashlib.sha256(source.read_bytes()).hexdigest()
    config = _write_config(
        tmp_path,
        """[[mutation]]
id = "flip"
path = "sample.py"
find = "FLAG = True"
replace = "FLAG = False"
test_command = '''python -c "assert 'True' in open('sample.py').read(), 'semantic failure'"'''
expected_exit = 1
expected_output_regex = "semantic failure"
""",
    )
    assert command_mutate(tmp_path, config, strict=True) == 0
    assert hashlib.sha256(source.read_bytes()).hexdigest() == original
    evidence = max((tmp_path / "artifacts/mutation/runs").iterdir())
    result = json.loads((evidence / "mutations.json").read_text(encoding="utf-8"))
    assert result["results"][0]["status"] == "killed"
    assert result["isolation"].startswith("per-mutant temporary")


def test_missing_tool_is_infrastructure_error_not_kill(tmp_path: Path) -> None:
    source = _source(tmp_path)
    original = source.read_text(encoding="utf-8")
    config = _write_config(
        tmp_path,
        """[[mutation]]
id = "missing-tool"
path = "sample.py"
find = "FLAG = True"
replace = "FLAG = False"
test_command = "definitely-not-a-real-cleanai-command"
expected_exit = 127
expected_output_regex = ".+"
""",
    )
    assert command_mutate(tmp_path, config, strict=True) == 2
    assert source.read_text(encoding="utf-8") == original
    evidence = max((tmp_path / "artifacts/mutation/runs").iterdir())
    result = json.loads((evidence / "mutations.json").read_text(encoding="utf-8"))
    assert result["results"][0]["status"] == "error"
    assert result["score"] == 0.0


def test_zero_mutants_and_nonfinite_floor_fail_closed(tmp_path: Path) -> None:
    _source(tmp_path)
    empty = _write_config(tmp_path, "")
    with pytest.raises(ConfigurationError, match="at least one"):
        command_mutate(tmp_path, empty, strict=True)
    config = _write_config(
        tmp_path,
        """[[mutation]]
id = "flip"
path = "sample.py"
find = "FLAG = True"
replace = "FLAG = False"
test_command = "python -c 'pass'"
expected_exit = 1
expected_output_regex = "failed"
""",
        minimum="nan",
    )
    with pytest.raises(ConfigurationError, match="finite"):
        command_mutate(tmp_path, config, strict=True)
