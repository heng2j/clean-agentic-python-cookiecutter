#!/usr/bin/env python3
"""Generate from a validated JSON preset before Cookiecutter evaluates Jinja.

This wrapper treats the bundled template source as trusted executable code. It
protects only the preset-data boundary: unknown fields, Jinja delimiters,
malformed values, unsafe identifiers, and existing/symlink targets are rejected
before Cookiecutter receives the context.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import keyword
import re
import sys
import unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from cookiecutter.main import cookiecutter


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FIELDS = frozenset(
    {
        "author_email",
        "author_name",
        "copyright_holder",
        "copyright_year",
        "include_github_actions",
        "license",
        "max_crap_score",
        "minimum_coverage",
        "minimum_mutation_score",
        "package_name",
        "project_description",
        "project_name",
        "project_slug",
        "python_version",
    }
)
JINJA_DELIMITERS = ("{{", "}}", "{%", "%}", "{#", "#}")
MAX_PRESET_BYTES = 64 * 1024
_SLUG = re.compile(r"[a-z](?:[a-z0-9-]*[a-z0-9])?")
_PACKAGE = re.compile(r"[a-z][a-z0-9_]*")
_EMAIL = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"
)
_INTEGER = re.compile(r"(?:0|[1-9][0-9]*)")
_PYTHON_VERSIONS = frozenset({"3.12", "3.13"})
_LICENSES = frozenset({"MIT", "Apache-2.0"})
_GITHUB_ACTIONS = frozenset({"yes", "no"})
_EMAIL_NOT_PROVIDED = "not-provided"
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
_PLACEHOLDER_HOLDERS = frozenset(
    {
        "copyright holder",
        "name of copyright owner",
        "project copyright holder",
        "tbd",
        "todo",
        "your name",
    }
)


class PresetError(ValueError):
    """An untrusted preset failed validation before Cookiecutter execution."""


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PresetError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_jinja(value: Any, path: str = "preset") -> None:
    if isinstance(value, str):
        found = next((token for token in JINJA_DELIMITERS if token in value), None)
        if found is not None:
            raise PresetError(f"{path} contains forbidden Jinja delimiter {found!r}")
        return
    if isinstance(value, dict):
        for key, child in value.items():
            _reject_jinja(key, f"{path}.<key>")
            _reject_jinja(child, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_jinja(child, f"{path}[{index}]")


def load_preset(path: Path) -> dict[str, str]:
    if not path.exists() or not path.is_file():
        raise PresetError(f"preset is not a regular file: {path}")
    if path.stat().st_size > MAX_PRESET_BYTES:
        raise PresetError(f"preset exceeds {MAX_PRESET_BYTES} bytes")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_object_without_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PresetError(f"preset is not valid UTF-8 JSON: {error}") from error
    _reject_jinja(raw)
    if not isinstance(raw, dict):
        raise PresetError("preset root must be a JSON object")

    if "context" in raw:
        unknown_envelope = set(raw) - {"context", "schema_version", "template"}
        if unknown_envelope:
            raise PresetError(f"unknown replay-envelope fields: {sorted(unknown_envelope)}")
        if raw.get("schema_version") != 1 or isinstance(raw.get("schema_version"), bool):
            raise PresetError("replay envelope schema_version must be integer 1")
        if raw.get("template") != "clean-agentic-scientific-python-cookiecutter-v1":
            raise PresetError("replay envelope template id is missing or unsupported")
        candidate = raw["context"]
    else:
        candidate = raw

    if not isinstance(candidate, dict):
        raise PresetError("preset context must be a JSON object")
    unknown = set(candidate) - PUBLIC_FIELDS
    if unknown:
        raise PresetError(f"unknown context fields: {sorted(unknown)}")
    non_strings = sorted(key for key, value in candidate.items() if not isinstance(value, str))
    if non_strings:
        raise PresetError(f"context values must be strings: {non_strings}")
    return dict(candidate)


def _template_defaults() -> dict[str, str]:
    raw = json.loads((ROOT / "cookiecutter.json").read_text(encoding="utf-8"))
    defaults: dict[str, str] = {}
    for key in PUBLIC_FIELDS - {
        "author_name",
        "copyright_holder",
        "package_name",
        "project_slug",
    }:
        value = raw[key]
        defaults[key] = value[0] if isinstance(value, list) else value
    return defaults


def _derive_context(preset: dict[str, str]) -> dict[str, str]:
    context = {**_template_defaults(), **preset}
    if "project_slug" not in preset:
        context["project_slug"] = (
            context["project_name"].lower().replace(" ", "-").replace("_", "-").replace(".", "")
        )
    if "package_name" not in preset:
        context["package_name"] = context["project_slug"].replace("-", "_")
    if "author_name" not in preset:
        context["author_name"] = f"{context['project_name']} contributors"
    if "copyright_holder" not in preset:
        context["copyright_holder"] = f"{context['project_name']} contributors"
    if context["copyright_year"] == "current":
        context["copyright_year"] = str(dt.date.today().year)
    return context


def _validate_text(
    field: str,
    value: str,
    *,
    maximum: int,
    toml_basic_string: bool = False,
) -> None:
    if not value or not value.strip():
        raise PresetError(f"{field} must not be empty")
    if value != value.strip():
        raise PresetError(f"{field} must not have leading or trailing whitespace")
    if len(value) > maximum:
        raise PresetError(f"{field} must contain at most {maximum} characters")
    for character in value:
        if unicodedata.category(character).startswith("C"):
            raise PresetError(
                f"{field} contains a control or format character U+{ord(character):04X}"
            )
    if toml_basic_string and ('"' in value or "\\" in value):
        raise PresetError(
            f"{field} contains a double quote or backslash unsupported by the generated TOML"
        )


def _validate_integer(field: str, value: str, *, minimum: int, maximum: int) -> None:
    if _INTEGER.fullmatch(value) is None:
        raise PresetError(f"{field} must be a canonical base-10 integer")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise PresetError(f"{field} must be a finite base-10 integer") from error
    if not number.is_finite() or number != number.to_integral_value():
        raise PresetError(f"{field} must be a finite base-10 integer")
    if not minimum <= int(number) <= maximum:
        raise PresetError(f"{field} must be in [{minimum}, {maximum}]")


def _normalized_identity(value: str) -> str:
    return " ".join(value.casefold().split())


def _reserved_email_domain(domain: str) -> bool:
    normalized = domain.casefold().rstrip(".")
    return (
        normalized == "localhost"
        or normalized in _RESERVED_EMAIL_DOMAINS
        or any(normalized.endswith(f".{item}") for item in _RESERVED_EMAIL_DOMAINS)
        or normalized in {suffix[1:] for suffix in _RESERVED_EMAIL_SUFFIXES}
        or normalized.endswith(_RESERVED_EMAIL_SUFFIXES)
    )


def _validate_author_identity(name: str, email: str) -> None:
    normalized_name = _normalized_identity(name)
    if normalized_name in _PLACEHOLDER_AUTHORS or re.search(
        r"[<\[].*(?:author|maintainer|name).*[>\]]", normalized_name
    ):
        raise PresetError("author_name must identify the actual author or contributor group")

    if email == _EMAIL_NOT_PROVIDED:
        return
    if _EMAIL.fullmatch(email) is None:
        raise PresetError("author_email must be 'not-provided' or an ASCII addr-spec")
    local_part, domain = email.rsplit("@", maxsplit=1)
    if local_part.casefold() in _PLACEHOLDER_EMAIL_LOCAL_PARTS:
        raise PresetError("author_email local part is a placeholder")
    if _reserved_email_domain(domain):
        raise PresetError("author_email must not use a reserved example/test domain")


def validate_context(context: dict[str, str]) -> None:
    if set(context) != PUBLIC_FIELDS:
        raise PresetError("normalized context does not contain the exact public field set")
    _validate_text("project_name", context["project_name"], maximum=120)
    _validate_text(
        "project_description",
        context["project_description"],
        maximum=500,
        toml_basic_string=True,
    )
    _validate_text("author_name", context["author_name"], maximum=120, toml_basic_string=True)
    _validate_text("author_email", context["author_email"], maximum=254, toml_basic_string=True)
    _validate_text("copyright_holder", context["copyright_holder"], maximum=200)

    if _SLUG.fullmatch(context["project_slug"]) is None:
        raise PresetError("project_slug is not a safe lowercase ASCII distribution/directory name")
    package = context["package_name"]
    if _PACKAGE.fullmatch(package) is None or keyword.iskeyword(package):
        raise PresetError("package_name is not a lowercase, non-keyword ASCII Python identifier")
    if package in sys.stdlib_module_names:
        raise PresetError(f"package_name collides with standard-library module {package!r}")
    _validate_author_identity(context["author_name"], context["author_email"])

    holder = " ".join(context["copyright_holder"].casefold().split())
    if holder in _PLACEHOLDER_HOLDERS or re.search(r"[<\[].*(?:name|holder).*[>\]]", holder):
        raise PresetError("copyright_holder must name the actual holder, not a placeholder")

    year_text = context["copyright_year"]
    if _INTEGER.fullmatch(year_text) is None or len(year_text) != 4:
        raise PresetError("copyright_year must be a four-digit year")
    if not 1900 <= int(year_text) <= dt.date.today().year + 1:
        raise PresetError(f"copyright_year must be in [1900, {dt.date.today().year + 1}]")

    if context["python_version"] not in _PYTHON_VERSIONS:
        raise PresetError(f"python_version must be one of {sorted(_PYTHON_VERSIONS)}")
    if context["license"] not in _LICENSES:
        raise PresetError(f"license must be one of {sorted(_LICENSES)}")
    if context["include_github_actions"] not in _GITHUB_ACTIONS:
        raise PresetError(f"include_github_actions must be one of {sorted(_GITHUB_ACTIONS)}")
    _validate_integer("minimum_coverage", context["minimum_coverage"], minimum=0, maximum=100)
    _validate_integer("max_crap_score", context["max_crap_score"], minimum=0, maximum=1_000_000)
    _validate_integer(
        "minimum_mutation_score",
        context["minimum_mutation_score"],
        minimum=0,
        maximum=100,
    )


def generate(preset_path: Path, output_dir: Path) -> Path:
    preset = load_preset(preset_path)
    context = _derive_context(preset)
    validate_context(context)

    if output_dir.is_symlink():
        raise PresetError(f"output directory must not be a symlink: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        raise PresetError(f"output path is not a directory: {output_dir}")
    resolved_output = output_dir.resolve(strict=True)
    target = resolved_output / context["project_slug"]
    if target.exists() or target.is_symlink():
        raise PresetError(f"refusing to overwrite existing target: {target}")

    generated = Path(
        cookiecutter(
            str(ROOT),
            no_input=True,
            output_dir=str(resolved_output),
            extra_context=context,
        )
    ).resolve(strict=True)
    if generated.parent != resolved_output or generated.name != context["project_slug"]:
        raise PresetError(f"Cookiecutter returned an unexpected output path: {generated}")
    if generated.is_symlink():
        raise PresetError(f"generated project must not be a symlink: {generated}")
    return generated


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description="Generate this trusted Cookiecutter from a validated untrusted JSON preset."
    )
    command.add_argument("--preset", type=Path, required=True, help="JSON preset or v2 replay context")
    command.add_argument("--output-dir", type=Path, default=Path.cwd(), help="parent output directory")
    return command


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        generated = generate(arguments.preset, arguments.output_dir)
    except (PresetError, OSError, ValueError) as error:
        print(f"safe generation refused: {error}", file=sys.stderr)
        return 2
    print(generated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
