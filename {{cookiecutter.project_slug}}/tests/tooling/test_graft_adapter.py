from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
ADAPTER = ROOT / "tools" / "graft_adapter.py"


def _executable(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)


def _environment(tmp_path: Path) -> tuple[dict[str, str], Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "graft.json"
    _executable(bin_dir / "node", "#!/bin/sh\nprintf 'v22.12.0\\n'\n")
    _executable(
        bin_dir / "graft",
        r'''#!/bin/sh
if [ "$1" = "--version" ]; then
  printf '%s\n' "${FAKE_GRAFT_VERSION:-0.17.0}"
  exit 0
fi
python3 - "$FAKE_GRAFT_LOG" "$@" <<'INNER'
import json, os, sys
json.dump({
  "args": sys.argv[2:],
  "do_not_track": os.environ.get("DO_NOT_TRACK"),
  "graft_key": "GRAFT_API_KEY" in os.environ,
  "openai_key": "OPENAI_API_KEY" in os.environ,
  "dotenv": os.environ.get("DOTENV_CONFIG_PATH"),
  "home": os.environ.get("HOME"),
  "refresh": os.environ.get("GRAFT_REFRESH"),
}, open(sys.argv[1], "w", encoding="utf-8"))
INNER
exit "${FAKE_GRAFT_EXIT:-0}"
''',
    )
    env = dict(os.environ)
    env.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}",
            "FAKE_GRAFT_LOG": str(log),
        }
    )
    return env, log


def _run(env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ADAPTER), *args],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_doctor_accepts_the_pinned_toolchain(tmp_path: Path) -> None:
    env, _ = _environment(tmp_path)
    completed = _run(env, "doctor", "--json")

    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["ready"] is True
    assert report["graft_expected"] == "0.17.0"
    assert report["node_minimum"] == "22.12.0"
    assert report["graph_dir"].endswith("artifacts/graft/context")


def test_run_is_project_scoped_and_strips_provider_keys(tmp_path: Path) -> None:
    env, log = _environment(tmp_path)
    env["GRAFT_API_KEY"] = "secret"
    env["OPENAI_API_KEY"] = "secret"

    completed = _run(env, "run", "build")

    assert completed.returncode == 0, completed.stderr
    record = json.loads(log.read_text(encoding="utf-8"))
    assert record["args"][:3] == [
        "--dir",
        str(ROOT / "artifacts" / "graft" / "context"),
        "build",
    ]
    assert record["do_not_track"] == "1"
    assert record["graft_key"] is False
    assert record["openai_key"] is False
    assert record["refresh"] == "hash"
    assert record["home"].endswith("artifacts/graft/home")
    assert record["dotenv"].endswith("artifacts/graft/home/empty.env")


@pytest.mark.parametrize(
    "args",
    [
        ("run", "init"),
        ("run", "build", "--deep"),
        ("run", "telemetry", "enable"),
        ("run", "blast", "--name"),
        ("run", "mcp", "."),
        ("run", "viz"),
    ],
)
def test_run_rejects_expanding_modes(tmp_path: Path, args: tuple[str, ...]) -> None:
    env, _ = _environment(tmp_path)
    completed = _run(env, *args)

    assert completed.returncode == 2
    assert "graft-adapter" in completed.stderr


def test_version_drift_fails_closed(tmp_path: Path) -> None:
    env, log = _environment(tmp_path)
    env["FAKE_GRAFT_VERSION"] = "0.18.0"

    completed = _run(env, "run", "map")

    assert completed.returncode == 2
    assert "ready" in completed.stderr
    assert not log.exists()
