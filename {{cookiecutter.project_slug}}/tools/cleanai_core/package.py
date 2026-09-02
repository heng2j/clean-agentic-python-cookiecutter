"""Offline wheel/sdist inspection and external-install smoke verification."""

from __future__ import annotations

import email.policy
import os
import re
import subprocess  # nosec B404
import sys
import tarfile
import tempfile
import tomllib
import zipfile
from email.parser import BytesParser
from email.utils import getaddresses
from pathlib import Path, PurePosixPath
from typing import Any

from .io import atomic_write_text, evidence_run_dir, print_line, safe_path, write_json
from .model import ConfigurationError, EvidenceError

SYMLINK_FILE_TYPE = 0o120000
_EMAIL = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"
)
_PLACEHOLDER_AUTHORS = frozenset(
    {
        "author",
        "author name",
        "example author",
        "example maintainer",
        "maintainer",
        "name",
        "not provided",
        "not-provided",
        "tbd",
        "todo",
        "your name",
    }
)
_PLACEHOLDER_EMAIL_LOCAL_PARTS = frozenset(
    {"email", "example", "name", "test", "user", "you", "your-email", "your.name"}
)
_RESERVED_EMAIL_DOMAINS = frozenset({"example.com", "example.net", "example.org"})
_RESERVED_EMAIL_SUFFIXES = (".example", ".invalid", ".localhost", ".test")


def _contained_dist(root: Path, raw: Path) -> Path:
    if raw.is_absolute():
        try:
            relative = raw.resolve(strict=True).relative_to(root.resolve(strict=True))
        except (FileNotFoundError, ValueError) as error:
            raise ConfigurationError(
                "distribution directory must be inside the repository"
            ) from error
    else:
        relative = raw
    return safe_path(root, relative, must_exist=True)


def _safe_member(name: str, archive: Path) -> PurePosixPath:
    member = PurePosixPath(name)
    if member.is_absolute() or ".." in member.parts or not member.parts:
        raise EvidenceError(f"unsafe archive member in {archive.name}: {name!r}")
    return member


def _author_name_problem(value: str) -> str | None:
    normalized = " ".join(value.casefold().split())
    if not normalized:
        return "must not be empty"
    if normalized in _PLACEHOLDER_AUTHORS or re.search(
        r"[<\[].*(?:author|maintainer|name).*[>\]]", normalized
    ):
        return "is a placeholder"
    return None


def _reserved_email_domain(domain: str) -> bool:
    normalized = domain.casefold().rstrip(".")
    return (
        normalized == "localhost"
        or normalized in _RESERVED_EMAIL_DOMAINS
        or any(normalized.endswith(f".{item}") for item in _RESERVED_EMAIL_DOMAINS)
        or normalized in {suffix[1:] for suffix in _RESERVED_EMAIL_SUFFIXES}
        or normalized.endswith(_RESERVED_EMAIL_SUFFIXES)
    )


def _author_email_problem(value: str) -> str | None:
    if _EMAIL.fullmatch(value) is None:
        return "must be an ASCII addr-spec"
    local_part, domain = value.rsplit("@", maxsplit=1)
    if local_part.casefold() in _PLACEHOLDER_EMAIL_LOCAL_PARTS:
        return "local part is a placeholder"
    if _reserved_email_domain(domain):
        return "uses a reserved example/test domain"
    return None


def _validate_project_authors(project: dict[str, Any]) -> None:
    authors = project.get("authors")
    if not isinstance(authors, list) or not authors:
        raise ConfigurationError("project authors must be a nonempty list")
    for index, author in enumerate(authors):
        if not isinstance(author, dict):
            raise ConfigurationError(f"project author {index} must be a table")
        name = author.get("name")
        if not isinstance(name, str):
            raise ConfigurationError(f"project author {index} name must be a string")
        if problem := _author_name_problem(name):
            raise ConfigurationError(f"project author {index} name {problem}")
        email = author.get("email")
        if email is None:
            continue
        if not isinstance(email, str):
            raise ConfigurationError(f"project author {index} email must be a string")
        if problem := _author_email_problem(email):
            raise ConfigurationError(f"project author {index} email {problem}")


def _validate_wheel_authors(message: Any, path: Path) -> None:
    author = str(message.get("Author", "")).strip()
    author_email = str(message.get("Author-email", "")).strip()
    if not author and not author_email:
        raise EvidenceError(f"wheel metadata lacks author identity: {path.name}")
    if author and (problem := _author_name_problem(author)):
        raise EvidenceError(f"wheel author {problem}: {path.name}")
    if author_email:
        addresses = getaddresses([author_email])
        if not addresses:
            raise EvidenceError(f"wheel Author-email is malformed: {path.name}")
        for display_name, address in addresses:
            if problem := _author_name_problem(display_name):
                raise EvidenceError(f"wheel author name {problem}: {path.name}")
            if problem := _author_email_problem(address):
                raise EvidenceError(f"wheel author email {problem}: {path.name}")


def _project_metadata(root: Path) -> tuple[str, str, str, str]:
    path = safe_path(root, "pyproject.toml", must_exist=True)
    try:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigurationError(f"cannot load project metadata: {error}") from error
    project = data.get("project")
    if not isinstance(project, dict):
        raise ConfigurationError("pyproject.toml requires [project]")
    name = project.get("name")
    version = project.get("version")
    scripts = project.get("scripts")
    policy_path = safe_path(root, ".cleanai/policy.toml", must_exist=True)
    try:
        with policy_path.open("rb") as stream:
            policy_data = tomllib.load(stream)
        package = policy_data.get("project", {}).get("package")
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigurationError(f"cannot load package policy: {error}") from error
    if not isinstance(name, str) or not name:
        raise ConfigurationError("project name must be a nonempty string")
    if not isinstance(version, str) or not version:
        raise ConfigurationError("project version must be a nonempty string")
    _validate_project_authors(project)
    if not isinstance(package, str) or not package:
        raise ConfigurationError("import package must be a nonempty string")
    if not isinstance(scripts, dict) or not scripts:
        raise ConfigurationError("package smoke requires at least one [project.scripts] entry")
    script = next(iter(scripts))
    if not isinstance(script, str) or not script:
        raise ConfigurationError("console-script name must be a nonempty string")
    return name, version, package, script


def _wheel_metadata(path: Path) -> tuple[str, str, set[str]]:
    members: set[str] = set()
    metadata_names: list[str] = []
    try:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                member = _safe_member(info.filename, path)
                members.add(member.as_posix())
                if info.filename.endswith(".dist-info/METADATA"):
                    metadata_names.append(info.filename)
                file_type = (info.external_attr >> 16) & 0o170000
                if file_type == SYMLINK_FILE_TYPE:
                    raise EvidenceError(f"wheel contains a symlink: {info.filename}")
            if len(metadata_names) != 1:
                raise EvidenceError(f"wheel must contain exactly one METADATA file: {path.name}")
            message = BytesParser(policy=email.policy.default).parsebytes(
                archive.read(metadata_names[0])
            )
    except (OSError, zipfile.BadZipFile, KeyError) as error:
        raise EvidenceError(f"cannot inspect wheel {path}: {error}") from error
    _validate_wheel_authors(message, path)
    return str(message.get("Name", "")), str(message.get("Version", "")), members


def _sdist_members(path: Path) -> set[str]:
    members: set[str] = set()
    try:
        with tarfile.open(path, mode="r:gz") as archive:  # inspection only
            for info in archive.getmembers():
                member = _safe_member(info.name, path)
                members.add(member.as_posix())
                if info.issym() or info.islnk():
                    raise EvidenceError(f"sdist contains a link: {info.name}")
    except (OSError, tarfile.TarError) as error:
        raise EvidenceError(f"cannot inspect sdist {path}: {error}") from error
    return members


def _run(argv: list[str], cwd: Path, environment: dict[str, str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(  # noqa: S603  # nosec B603
            argv,
            cwd=cwd,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout if isinstance(error.stdout, str) else ""
        stderr = error.stderr if isinstance(error.stderr, str) else ""
        return {
            "argv": argv,
            "status": "timeout",
            "returncode": 124,
            "stdout": stdout,
            "stderr": stderr,
            "error": f"timed out after {error.timeout} seconds",
        }
    except PermissionError as error:
        return {
            "argv": argv,
            "status": "error",
            "returncode": 126,
            "stdout": "",
            "stderr": "",
            "error": str(error),
        }
    except OSError as error:
        return {
            "argv": argv,
            "status": "error",
            "returncode": 127,
            "stdout": "",
            "stderr": "",
            "error": str(error),
        }
    return {
        "argv": argv,
        "status": "passed" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "error": None,
    }


def command_package_smoke(root: Path, dist_dir: Path) -> int:
    """Inspect artifacts and prove wheel install/import/CLI/uninstall outside source."""
    absolute = _contained_dist(root, dist_dir)
    wheels = sorted(absolute.glob("*.whl"))
    sdists = sorted(absolute.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise EvidenceError(
            f"expected exactly one wheel and one sdist; found "
            f"{len(wheels)} wheel(s), {len(sdists)} sdist(s)"
        )
    project_name, version, package, script = _project_metadata(root)
    wheel_name, wheel_version, wheel_members = _wheel_metadata(wheels[0])
    if (wheel_name, wheel_version) != (project_name, version):
        raise EvidenceError(
            f"wheel metadata {wheel_name!r} {wheel_version!r} differs from "
            f"pyproject {project_name!r} {version!r}"
        )
    module_path = package.replace(".", "/")
    suffix = f"/{module_path}/__init__.py"
    if not any(
        name == f"{module_path}/__init__.py" or name.endswith(suffix) for name in wheel_members
    ):
        raise EvidenceError(f"wheel does not contain import package {package!r}")
    sdist_members = _sdist_members(sdists[0])
    if not any(name.endswith("/pyproject.toml") for name in sdist_members):
        raise EvidenceError("sdist does not contain pyproject.toml")

    output = evidence_run_dir(root, "package-smoke")
    commands: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="cleanai-wheel-") as raw_temp:
        temporary = Path(raw_temp).resolve()
        venv = temporary / "venv"
        outside = temporary / "outside-source"
        outside.mkdir()
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        commands.append(_run([sys.executable, "-m", "venv", str(venv)], outside, environment))
        python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        executable = venv / (
            f"Scripts/{script}.exe" if sys.platform == "win32" else f"bin/{script}"
        )
        commands.extend(
            [
                _run(
                    [
                        str(python),
                        "-m",
                        "pip",
                        "--isolated",
                        "--disable-pip-version-check",
                        "install",
                        "--no-index",
                        "--no-deps",
                        str(wheels[0]),
                    ],
                    outside,
                    environment,
                ),
                _run(
                    [str(python), "-c", f"import {package}; print({package}.__file__)"],
                    outside,
                    environment,
                ),
                _run([str(executable), "--help"], outside, environment),
                _run(
                    [
                        str(python),
                        "-m",
                        "pip",
                        "--isolated",
                        "--disable-pip-version-check",
                        "check",
                    ],
                    outside,
                    environment,
                ),
                _run(
                    [
                        str(python),
                        "-m",
                        "pip",
                        "--isolated",
                        "--disable-pip-version-check",
                        "uninstall",
                        "-y",
                        project_name,
                    ],
                    outside,
                    environment,
                ),
                _run([str(python), "-c", f"import {package}"], outside, environment),
            ]
        )
    expected = [0, 0, 0, 0, 0, 0, 1]
    infrastructure_error = any(row["status"] in {"error", "timeout"} for row in commands)
    passed = not infrastructure_error and all(
        row["returncode"] == code for row, code in zip(commands, expected, strict=True)
    )
    payload = {
        "schema_version": 2,
        "project": project_name,
        "version": version,
        "package": package,
        "wheel": wheels[0].name,
        "sdist": sdists[0].name,
        "commands": commands,
        "expected_returncodes": expected,
        "passed": passed,
        "infrastructure_error": infrastructure_error,
    }
    write_json(output / "package-smoke.json", payload)
    atomic_write_text(output / "package-smoke.md", f"# Package smoke\n\nPassed: **{passed}**\n")
    print_line(output / "package-smoke.md")
    if infrastructure_error:
        return 2
    return int(not passed)
