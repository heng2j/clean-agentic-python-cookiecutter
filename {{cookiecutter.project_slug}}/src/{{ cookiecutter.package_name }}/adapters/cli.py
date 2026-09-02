"""JSON command-line adapter."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from {{ cookiecutter.package_name }}.application.assess_release import assess_release
from {{ cookiecutter.package_name }}.domain.change_risk import ReleaseEvidence


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    return parser


def _from_mapping(data: Mapping[str, Any]) -> ReleaseEvidence:
    return ReleaseEvidence(
        failed_tests=int(data["failed_tests"]),
        static_analysis_findings=int(data["static_analysis_findings"]),
        architecture_violations=int(data["architecture_violations"]),
        security_findings=int(data["security_findings"]),
        max_crap_score=float(data["max_crap_score"]),
        mutation_score=float(data["mutation_score"]),
        touches_trust_boundary=bool(data.get("touches_trust_boundary", False)),
        trust_boundary_review_complete=bool(data.get("trust_boundary_review_complete", False)),
    )


def main(argv: Sequence[str] | None = None) -> int:
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
