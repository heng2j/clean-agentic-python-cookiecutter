"""JSON command-line adapter."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from math import isfinite
from pathlib import Path
from typing import Any

from {{ cookiecutter.package_name }}.application.assess_release import assess_release
from {{ cookiecutter.package_name }}.domain.change_risk import ReleaseEvidence

REQUIRED_FIELDS = frozenset(
    {
        "architecture_violations",
        "failed_tests",
        "max_crap_score",
        "mutation_score",
        "security_findings",
        "static_analysis_findings",
    }
)
OPTIONAL_FIELDS = frozenset({"touches_trust_boundary", "trust_boundary_review_complete"})


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    return parser


def _from_mapping(data: Mapping[str, Any]) -> ReleaseEvidence:
    if not data.keys() >= REQUIRED_FIELDS or not data.keys() <= REQUIRED_FIELDS | OPTIONAL_FIELDS:
        raise TypeError("evidence fields do not match the documented schema")

    def count(name: str) -> int:
        value = data[name]
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{name} must be an integer")
        return value

    def number(name: str) -> float:
        value = data[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"{name} must be a number")
        try:
            converted = float(value)
        except OverflowError as error:
            raise ValueError(f"{name} is outside the supported numeric range") from error
        if not isfinite(converted):
            raise ValueError(f"{name} must be finite")
        return converted

    def flag(name: str) -> bool:
        value = data.get(name, False)
        if not isinstance(value, bool):
            raise TypeError(f"{name} must be a boolean")
        return value

    return ReleaseEvidence(
        failed_tests=count("failed_tests"),
        static_analysis_findings=count("static_analysis_findings"),
        architecture_violations=count("architecture_violations"),
        security_findings=count("security_findings"),
        max_crap_score=number("max_crap_score"),
        mutation_score=number("mutation_score"),
        touches_trust_boundary=flag("touches_trust_boundary"),
        trust_boundary_review_complete=flag("trust_boundary_review_complete"),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Parse release-evidence input and return a stable policy exit code."""
    args = _parser().parse_args(argv)
    try:
        raw = json.loads(args.evidence.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise TypeError("evidence JSON must be an object")
        decision = assess_release(_from_mapping(raw))
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"invalid evidence: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"status": decision.status, "reasons": decision.reasons}, indent=2))
    return 0 if decision.approved else 1


if __name__ == "__main__":
    raise SystemExit(main())
