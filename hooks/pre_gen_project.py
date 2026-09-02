"""Fail closed before Cookiecutter commits an invalid project.

All Jinja substitutions below use ``tojson`` so context values become Python
string literals, never executable source fragments. Direct Cookiecutter
templates and replay contexts are trusted inputs; the repository's safe
preset wrapper validates untrusted JSON before Cookiecutter evaluates Jinja.
"""

from __future__ import annotations

import datetime as dt
import keyword
import re
import sys
import unicodedata
from decimal import Decimal, InvalidOperation


PROJECT_NAME = {{ cookiecutter.project_name | tojson }}
PROJECT_SLUG = {{ cookiecutter.project_slug | tojson }}
PACKAGE_NAME = {{ cookiecutter.package_name | tojson }}
PROJECT_DESCRIPTION = {{ cookiecutter.project_description | tojson }}
AUTHOR_NAME = {{ cookiecutter.author_name | tojson }}
AUTHOR_EMAIL = {{ cookiecutter.author_email | tojson }}
COPYRIGHT_HOLDER = {{ cookiecutter.copyright_holder | tojson }}
COPYRIGHT_YEAR = {{ cookiecutter.copyright_year | tojson }}
PYTHON_VERSION = {{ cookiecutter.python_version | tojson }}
LICENSE_ID = {{ cookiecutter.license | tojson }}
INCLUDE_GITHUB_ACTIONS = {{ cookiecutter.include_github_actions | tojson }}
MINIMUM_COVERAGE = {{ cookiecutter.minimum_coverage | tojson }}
MAX_CRAP_SCORE = {{ cookiecutter.max_crap_score | tojson }}
MINIMUM_MUTATION_SCORE = {{ cookiecutter.minimum_mutation_score | tojson }}

_SLUG = re.compile(r"[a-z](?:[a-z0-9-]*[a-z0-9])?")
_PACKAGE = re.compile(r"[a-z][a-z0-9_]*")
_EMAIL = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"
)
_INTEGER = re.compile(r"(?:0|[1-9][0-9]*)")
_PYTHON_VERSIONS = frozenset({"3.12", "3.13"})
_LICENSES = frozenset({"MIT", "Apache-2.0", "LicenseRef-Proprietary"})
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


def _fail(field: str, message: str) -> None:
    raise SystemExit(f"invalid {field}: {message}")


def _validate_text(
    field: str,
    value: str,
    *,
    maximum: int,
    toml_basic_string: bool = False,
) -> None:
    if not value or not value.strip():
        _fail(field, "must not be empty")
    if value != value.strip():
        _fail(field, "must not have leading or trailing whitespace")
    if len(value) > maximum:
        _fail(field, f"must contain at most {maximum} characters")
    for character in value:
        if unicodedata.category(character).startswith("C"):
            _fail(field, f"contains a control or format character U+{ord(character):04X}")
    if toml_basic_string and ('"' in value or "\\" in value):
        _fail(field, "double quotes and backslashes are unsupported in this template field")


def _validate_integer(field: str, value: str, *, minimum: int, maximum: int) -> None:
    if _INTEGER.fullmatch(value) is None:
        _fail(field, "must be a canonical base-10 integer")
    try:
        number = Decimal(value)
    except InvalidOperation:
        _fail(field, "must be a finite base-10 integer")
    if not number.is_finite() or number != number.to_integral_value():
        _fail(field, "must be a finite base-10 integer")
    if not minimum <= int(number) <= maximum:
        _fail(field, f"must be in [{minimum}, {maximum}]")


def _validate_enum(field: str, value: str, allowed: frozenset[str]) -> None:
    if value not in allowed:
        _fail(field, f"must be one of {', '.join(sorted(allowed))}")


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


def _validate_author_identity() -> None:
    normalized_name = _normalized_identity(AUTHOR_NAME)
    if normalized_name in _PLACEHOLDER_AUTHORS or re.search(
        r"[<\[].*(?:author|maintainer|name).*[>\]]", normalized_name
    ):
        _fail("author_name", "must identify the actual author or contributor group")

    if AUTHOR_EMAIL == _EMAIL_NOT_PROVIDED:
        return
    if _EMAIL.fullmatch(AUTHOR_EMAIL) is None:
        _fail("author_email", "must be 'not-provided' or an ASCII addr-spec")
    local_part, domain = AUTHOR_EMAIL.rsplit("@", maxsplit=1)
    if local_part.casefold() in _PLACEHOLDER_EMAIL_LOCAL_PARTS:
        _fail("author_email", "local part is a placeholder")
    if _reserved_email_domain(domain):
        _fail("author_email", "must not use a reserved example/test domain")


def validate() -> None:
    _validate_text("project_name", PROJECT_NAME, maximum=120)
    _validate_text(
        "project_description",
        PROJECT_DESCRIPTION,
        maximum=500,
        toml_basic_string=True,
    )
    _validate_text("author_name", AUTHOR_NAME, maximum=120, toml_basic_string=True)
    _validate_text("author_email", AUTHOR_EMAIL, maximum=254, toml_basic_string=True)
    _validate_text("copyright_holder", COPYRIGHT_HOLDER, maximum=200)

    if _SLUG.fullmatch(PROJECT_SLUG) is None:
        _fail(
            "project_slug",
            "must start with a lowercase ASCII letter, end with an ASCII letter or digit, "
            "and contain only lowercase ASCII letters, digits, and internal hyphens",
        )
    if _PACKAGE.fullmatch(PACKAGE_NAME) is None or keyword.iskeyword(PACKAGE_NAME):
        _fail(
            "package_name",
            "must be a lowercase, non-keyword ASCII Python identifier",
        )
    if PACKAGE_NAME in sys.stdlib_module_names:
        _fail("package_name", f"collides with Python standard-library module {PACKAGE_NAME!r}")
    _validate_author_identity()

    normalized_holder = " ".join(COPYRIGHT_HOLDER.casefold().split())
    if normalized_holder in _PLACEHOLDER_HOLDERS:
        _fail("copyright_holder", "must name the actual holder, not a placeholder")
    if re.search(r"[<\[].*(?:name|holder).*[>\]]", normalized_holder):
        _fail("copyright_holder", "must not contain a bracketed placeholder")

    if COPYRIGHT_YEAR == "current":
        year = dt.date.today().year
    elif _INTEGER.fullmatch(COPYRIGHT_YEAR) is None or len(COPYRIGHT_YEAR) != 4:
        _fail("copyright_year", "must be a four-digit year")
    else:
        year = int(COPYRIGHT_YEAR)
    if not 1900 <= year <= dt.date.today().year + 1:
        _fail("copyright_year", f"must be in [1900, {dt.date.today().year + 1}]")

    _validate_enum("python_version", PYTHON_VERSION, _PYTHON_VERSIONS)
    _validate_enum("license", LICENSE_ID, _LICENSES)
    _validate_enum("include_github_actions", INCLUDE_GITHUB_ACTIONS, _GITHUB_ACTIONS)
    _validate_integer("minimum_coverage", MINIMUM_COVERAGE, minimum=0, maximum=100)
    _validate_integer("max_crap_score", MAX_CRAP_SCORE, minimum=0, maximum=1_000_000)
    _validate_integer("minimum_mutation_score", MINIMUM_MUTATION_SCORE, minimum=0, maximum=100)


validate()
