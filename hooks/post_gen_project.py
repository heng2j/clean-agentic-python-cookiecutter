"""Create license/replay artifacts without following paths outside the project."""

from __future__ import annotations

import datetime as dt
import json
import os
import tempfile
from pathlib import Path


PROJECT_NAME = {{ cookiecutter.project_name | tojson }}
PROJECT_SLUG = {{ cookiecutter.project_slug | tojson }}
PACKAGE_NAME = {{ cookiecutter.package_name | tojson }}
PROJECT_DESCRIPTION = {{ cookiecutter.project_description | tojson }}
AUTHOR_NAME = {{ cookiecutter.author_name | tojson }}
AUTHOR_EMAIL = {{ cookiecutter.author_email | tojson }}
COPYRIGHT_HOLDER = {{ cookiecutter.copyright_holder | tojson }}
RAW_COPYRIGHT_YEAR = {{ cookiecutter.copyright_year | tojson }}
COPYRIGHT_YEAR = (
    str(dt.date.today().year) if RAW_COPYRIGHT_YEAR == "current" else RAW_COPYRIGHT_YEAR
)
PYTHON_VERSION = {{ cookiecutter.python_version | tojson }}
LICENSE_ID = {{ cookiecutter.license | tojson }}
INCLUDE_GITHUB_ACTIONS = {{ cookiecutter.include_github_actions | tojson }}
MINIMUM_COVERAGE = {{ cookiecutter.minimum_coverage | tojson }}
MAX_CRAP_SCORE = {{ cookiecutter.max_crap_score | tojson }}
MINIMUM_MUTATION_SCORE = {{ cookiecutter.minimum_mutation_score | tojson }}

ROOT = Path.cwd().resolve(strict=True)
ASSET_NAMES = {
    "MIT": "MIT.txt",
    "Apache-2.0": "Apache-2.0.txt",
}


def _fail(message: str) -> None:
    raise SystemExit(f"post-generation safety check failed: {message}")


def _safe_path(*parts: str, must_be_file: bool = False) -> Path:
    candidate = ROOT.joinpath(*parts)
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        _fail(f"path escapes generated project: {candidate}")

    probe = candidate
    while probe != ROOT:
        if probe.is_symlink():
            _fail(f"refusing symlink path: {probe.relative_to(ROOT)}")
        probe = probe.parent

    try:
        resolved_parent = candidate.parent.resolve(strict=True)
        resolved_parent.relative_to(ROOT)
    except (FileNotFoundError, ValueError):
        _fail(f"path parent is missing or outside generated project: {candidate}")

    if must_be_file and (not candidate.exists() or not candidate.is_file()):
        _fail(f"expected regular file: {candidate.relative_to(ROOT)}")
    if candidate.exists() and not candidate.is_file():
        _fail(f"expected file path, found another file type: {candidate.relative_to(ROOT)}")
    return candidate


def _atomic_write(target: Path, text: str, *, replace_existing: bool) -> None:
    if target.is_symlink():
        _fail(f"refusing to replace symlink: {target.relative_to(ROOT)}")
    if target.exists() and not replace_existing:
        _fail(f"refusing to overwrite existing file: {target.relative_to(ROOT)}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        temporary.chmod(0o644)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


def _render_license(asset: Path) -> str:
    text = asset.read_text(encoding="utf-8")
    if LICENSE_ID == "Apache-2.0":
        return text if text.endswith("\n") else f"{text}\n"
    tokens = {
        "@@COPYRIGHT_YEAR@@": COPYRIGHT_YEAR,
        "@@COPYRIGHT_HOLDER@@": COPYRIGHT_HOLDER,
    }
    for token, value in tokens.items():
        if text.count(token) != 1:
            _fail(f"license asset {asset.name} must contain {token} exactly once")
        text = text.replace(token, value)
    if "@@" in text:
        _fail(f"license asset {asset.name} contains an unresolved token")
    return text if text.endswith("\n") else f"{text}\n"


def _write_replay_context() -> None:
    context = {
        "author_email": AUTHOR_EMAIL,
        "author_name": AUTHOR_NAME,
        "copyright_holder": COPYRIGHT_HOLDER,
        "copyright_year": COPYRIGHT_YEAR,
        "include_github_actions": INCLUDE_GITHUB_ACTIONS,
        "license": LICENSE_ID,
        "max_crap_score": MAX_CRAP_SCORE,
        "minimum_coverage": MINIMUM_COVERAGE,
        "minimum_mutation_score": MINIMUM_MUTATION_SCORE,
        "package_name": PACKAGE_NAME,
        "project_description": PROJECT_DESCRIPTION,
        "project_name": PROJECT_NAME,
        "project_slug": PROJECT_SLUG,
        "python_version": PYTHON_VERSION,
    }
    envelope = {
        "context": context,
        "schema_version": 1,
        "template": "clean-agentic-scientific-python-cookiecutter-v1",
    }
    target = _safe_path(".cleanai", "template-context.json")
    _atomic_write(
        target,
        json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        replace_existing=False,
    )


def _write_apache_notice() -> None:
    notice = (
        f"{PROJECT_NAME}\n"
        f"Copyright {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}\n\n"
        "This product is licensed under the Apache License, Version 2.0.\n"
    )
    _atomic_write(_safe_path("NOTICE"), notice, replace_existing=False)


def _remove_assets() -> None:
    for name in ASSET_NAMES.values():
        asset = _safe_path(".cleanai", "_license_assets", name, must_be_file=True)
        asset.unlink()
    directory = ROOT / ".cleanai" / "_license_assets"
    if directory.is_symlink():
        _fail("refusing symlink asset directory")
    directory.rmdir()


def main() -> None:
    if LICENSE_ID not in ASSET_NAMES:
        _fail(f"unsupported license id: {LICENSE_ID!r}")
    if not COPYRIGHT_HOLDER.strip():
        _fail("copyright holder is empty")

    asset = _safe_path(
        ".cleanai",
        "_license_assets",
        ASSET_NAMES[LICENSE_ID],
        must_be_file=True,
    )
    license_text = _render_license(asset)
    _atomic_write(_safe_path("LICENSE", must_be_file=True), license_text, replace_existing=True)
    if LICENSE_ID == "Apache-2.0":
        _write_apache_notice()
    _write_replay_context()

    if INCLUDE_GITHUB_ACTIONS == "no":
        workflow = _safe_path(".github", "workflows", "quality.yml")
        if workflow.exists() or workflow.is_symlink():
            if workflow.is_symlink() or not workflow.is_file():
                _fail("refusing non-regular GitHub Actions workflow path")
            workflow.unlink()
    elif INCLUDE_GITHUB_ACTIONS != "yes":
        _fail(f"unsupported include_github_actions value: {INCLUDE_GITHUB_ACTIONS!r}")

    _remove_assets()


main()
