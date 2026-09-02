from __future__ import annotations

import io
import json
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Any

import pytest
from tools.cleanai_core import package as package_tool
from tools.cleanai_core.model import ConfigurationError, EvidenceError


def _repository(root: Path) -> Path:
    cleanai = root / ".cleanai"
    cleanai.mkdir()
    (cleanai / "policy.toml").write_text('[project]\npackage = "sample_pkg"\n', encoding="utf-8")
    (root / "pyproject.toml").write_text(
        """[project]
name = "sample-project"
version = "1.2.3"
authors = [{ name = "Sample Project Maintainers" }]
[project.scripts]
sample-cli = "sample_pkg:main"
""",
        encoding="utf-8",
    )
    dist = root / "dist"
    dist.mkdir()
    return dist


def _archives(dist: Path, *, name: str = "sample-project", include_module: bool = True) -> None:
    wheel = dist / "sample_project-1.2.3-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(
            "sample_project-1.2.3.dist-info/METADATA",
            (
                f"Metadata-Version: 2.4\nName: {name}\nVersion: 1.2.3\n"
                "Author: Sample Project Maintainers\n"
            ),
        )
        if include_module:
            archive.writestr("sample_pkg/__init__.py", "def main(): pass\n")
    sdist = dist / "sample_project-1.2.3.tar.gz"
    with tarfile.open(sdist, "w:gz") as archive:
        content = b"[project]\nname='sample-project'\n"
        info = tarfile.TarInfo("sample_project-1.2.3/pyproject.toml")
        info.size = len(content)
        archive.addfile(info, io.BytesIO(content))


def test_package_smoke_validates_archives_and_external_command_sequence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _repository(tmp_path)
    _archives(dist)
    returncodes = iter([0, 0, 0, 0, 0, 0, 1])
    calls: list[tuple[list[str], dict[str, str]]] = []

    def fake_run(argv: list[str], _cwd: Path, environment: dict[str, str]) -> dict[str, Any]:
        calls.append((argv, environment))
        returncode = next(returncodes)
        return {
            "argv": argv,
            "status": "passed" if returncode == 0 else "failed",
            "returncode": returncode,
            "stdout": "",
            "stderr": "",
            "error": None,
        }

    monkeypatch.setenv("PYTHONPATH", "must-not-leak")
    monkeypatch.setattr(package_tool, "_run", fake_run)
    assert package_tool.command_package_smoke(tmp_path, Path("dist")) == 0
    assert len(calls) == 7
    assert all("PYTHONPATH" not in environment for _argv, environment in calls)
    install = calls[1][0]
    assert "--isolated" in install
    assert "--disable-pip-version-check" in install
    assert "--no-index" in install
    assert "--no-deps" in install
    evidence = max((tmp_path / "artifacts/package-smoke/runs").iterdir())
    result = json.loads((evidence / "package-smoke.json").read_text(encoding="utf-8"))
    assert result["passed"] is True
    assert result["expected_returncodes"][-1] == 1


def test_package_smoke_rejects_stale_ambiguous_and_mismatched_artifacts(tmp_path: Path) -> None:
    dist = _repository(tmp_path)
    with pytest.raises(EvidenceError, match="exactly one wheel and one sdist"):
        package_tool.command_package_smoke(tmp_path, dist)
    _archives(dist, name="wrong-name")
    with pytest.raises(EvidenceError, match="differs from pyproject"):
        package_tool.command_package_smoke(tmp_path, dist)
    (dist / "stale.whl").write_bytes(b"not a wheel")
    with pytest.raises(EvidenceError, match="exactly one wheel"):
        package_tool.command_package_smoke(tmp_path, dist)


def test_package_smoke_records_behavior_failure_as_exit_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _repository(tmp_path)
    _archives(dist)
    returncodes = iter([0, 0, 0, 9, 0, 0, 1])

    def fake_run(argv: list[str], _cwd: Path, _environment: dict[str, str]) -> dict[str, Any]:
        returncode = next(returncodes)
        return {
            "argv": argv,
            "status": "passed" if returncode == 0 else "failed",
            "returncode": returncode,
            "stdout": "",
            "stderr": "",
            "error": None,
        }

    monkeypatch.setattr(package_tool, "_run", fake_run)
    assert package_tool.command_package_smoke(tmp_path, dist) == 1
    evidence = max((tmp_path / "artifacts/package-smoke/runs").iterdir())
    result = json.loads((evidence / "package-smoke.json").read_text(encoding="utf-8"))
    assert result["passed"] is False
    assert result["infrastructure_error"] is False


def test_archive_validation_rejects_traversal_links_and_missing_package(tmp_path: Path) -> None:
    with pytest.raises(EvidenceError, match="unsafe archive member"):
        package_tool._safe_member("../escape", tmp_path / "bad.whl")
    dist = _repository(tmp_path)
    _archives(dist, include_module=False)
    with pytest.raises(EvidenceError, match="does not contain import package"):
        package_tool.command_package_smoke(tmp_path, dist)
    link_sdist = tmp_path / "link.tar.gz"
    with tarfile.open(link_sdist, "w:gz") as archive:
        link = tarfile.TarInfo("project/link")
        link.type = tarfile.SYMTYPE
        link.linkname = "../../escape"
        archive.addfile(link)
    with pytest.raises(EvidenceError, match="contains a link"):
        package_tool._sdist_members(link_sdist)


def test_project_metadata_and_runner_fail_with_controlled_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _repository(tmp_path)
    (tmp_path / "pyproject.toml").write_text("[project]\nname='only-name'\n", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="version"):
        package_tool._project_metadata(tmp_path)
    result = package_tool._run(
        [sys.executable, "-c", "print('ok')"],
        tmp_path,
        {},
    )
    assert result["returncode"] == 0
    assert result["stdout"].strip() == "ok"

    def timeout(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(["fixture"], 1)

    monkeypatch.setattr(package_tool.subprocess, "run", timeout)
    timed_out = package_tool._run(["fixture"], tmp_path, {})
    assert timed_out["status"] == "timeout"
    assert timed_out["returncode"] == 124


@pytest.mark.parametrize(
    ("authors", "message"),
    [
        ('[{ name = "Your Name" }]', "name is a placeholder"),
        ('[{ name = "[author name]" }]', "name is a placeholder"),
        ('[{ name = "Sample Maintainers", email = "you@acme.dev" }]', "placeholder"),
        (
            '[{ name = "Sample Maintainers", email = "release@example.com" }]',
            "reserved example/test domain",
        ),
        (
            '[{ name = "Sample Maintainers", email = "release@project.invalid" }]',
            "reserved example/test domain",
        ),
        ('[{ name = "Sample Maintainers", email = "" }]', "ASCII addr-spec"),
    ],
)
def test_project_metadata_rejects_placeholder_author_identity(
    tmp_path: Path, authors: str, message: str
) -> None:
    _repository(tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        f"""[project]
name = "sample-project"
version = "1.2.3"
authors = {authors}
[project.scripts]
sample-cli = "sample_pkg:main"
""",
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError, match=message):
        package_tool._project_metadata(tmp_path)


def test_project_metadata_accepts_real_email_and_omitted_email(tmp_path: Path) -> None:
    _repository(tmp_path)
    assert package_tool._project_metadata(tmp_path)[0] == "sample-project"
    path = tmp_path / "pyproject.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            'authors = [{ name = "Sample Project Maintainers" }]',
            'authors = [{ name = "Sample Project Maintainers", email = "release@acme.dev" }]',
        ),
        encoding="utf-8",
    )
    assert package_tool._project_metadata(tmp_path)[0] == "sample-project"


def test_wheel_metadata_rejects_placeholder_author_identity(tmp_path: Path) -> None:
    wheel = tmp_path / "sample.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(
            "sample-1.0.dist-info/METADATA",
            "Metadata-Version: 2.4\nName: sample\nVersion: 1.0\n"
            "Author-email: Your Name <you@example.com>\n",
        )
    with pytest.raises(EvidenceError, match="wheel author name is a placeholder"):
        package_tool._wheel_metadata(wheel)


def test_subprocess_failure_writes_evidence_and_returns_two(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _repository(tmp_path)
    _archives(dist)

    def timeout(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(["fixture"], 1)

    monkeypatch.setattr(package_tool.subprocess, "run", timeout)
    assert package_tool.command_package_smoke(tmp_path, dist) == 2
    evidence = max((tmp_path / "artifacts/package-smoke/runs").iterdir())
    result = json.loads((evidence / "package-smoke.json").read_text(encoding="utf-8"))
    assert result["infrastructure_error"] is True
    assert result["commands"][0]["status"] == "timeout"
