#!/usr/bin/env python3
"""Thin executable adapter for the tested :mod:`cleanai_core` package."""

from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = str(Path(__file__).resolve().parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

from cleanai_core import callable_blocks, crap_score, parse_frontmatter  # noqa: E402
from cleanai_core.cli import main  # noqa: E402

__all__ = ["callable_blocks", "crap_score", "main", "parse_frontmatter"]


if __name__ == "__main__":
    raise SystemExit(main())
