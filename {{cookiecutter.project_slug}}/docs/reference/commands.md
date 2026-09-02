---
status: normative
authority: reference-commands
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "tools/**"
  - "Makefile"
  - ".github/workflows/**"
---
# Command reference

| Command | Network | Success contract |
|---|---|---|
| `uv lock --check` | offline | supplied lock matches declarations; exit 0 |
| `uv lock` | connected when updating | deliberately refreshes `uv.lock`; review the diff before acceptance |
| `uv sync --locked --group dev` | may download, no re-resolution | declarations match lock; install exit 0 |
| `uv run --locked --group dev prek run --all-files` | offline after install | reviewed pre-commit stage calls the canonical fast gate |
| `uv run --locked --group dev prek install` | local Git write | installs the declared pre-commit and pre-push shims after review |
| `uv run --locked --group dev python tools/cleanai.py gauntlet fast` | offline after install | every required fast step and ledger complete |
| `… gauntlet full` | offline after install | fast + coverage/CRAP/source/build/wheel smoke complete |
| `… gauntlet hardening` | offline after install | full + valid curated mutants meet local floor |
| `… gauntlet release` | offline after install | hardening + archive/metadata/external install/API/CLI/uninstall complete |
| `… gauntlet connected-audit` | connected | vulnerability query executed; timestamp/source recorded |
| `… context-audit --strict` | offline | all active loading sources pass context rules |
| `… docs-audit --strict` | offline | lifecycle, authority, in-root links/anchors pass |
| `… science-audit --strict` | offline | scientific paths, dotenv ignore rules, and static manifest pass |
| `uv run --locked --group typing-experimental python tools/cleanai.py gauntlet typing-experimental` | offline after optional install | beta `ty` comparison runs; result is advisory and not a release criterion |
| `… prune-plan --output PATH` | offline | proposal written; no deletion |

Exit `0` means the named checks ran and met their declared oracles. Exit `1` means measured evidence failed. Exit `2` means invalid input, missing evidence/tool, infrastructure failure, or an unsafe precondition. The JSON ledger is the stable machine interface; console prose is for people.

Before deterministic or mutation runs, use a secret-free shell. The shipped
`.envrc` does not load `.env` unless a maintainer deliberately enables it.
