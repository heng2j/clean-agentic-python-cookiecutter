---
status: normative
authority: troubleshooting
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "README.md"
  - "tools/**"
---
# Troubleshooting

## `uv sync --locked` says the lock is stale or missing

Run `uv lock` in a connected, reviewed environment, inspect the diff, then rerun `uv sync --locked --group dev`. Commit the lock. Do not remove `--locked` in CI.

## A required tool is missing

Rerun the documented development sync. The gate should exit `2` and identify the missing executable plus the exact rerun. A traceback or skipped check is a harness defect.

## Mutation reports invalid or infrastructure error

Check exact target match count, target path/symlink status, baseline command, timeout, and oracle. Invalid cases never improve the mutation score. Confirm `git diff` shows no harness-created source change.

## CRAP rejects coverage

Regenerate branch-aware coverage from this checkout with the command in the tutorial. Empty, partial, malformed, or foreign reports are intentionally rejected. Do not synthesize 100% for absent lines.

## Worktree script says Git is not ready

Initialize Git, create an initial commit, and make the tree clean. The script will not do those ownership decisions for you.

## A connected dependency audit is unavailable

Mark the result **Unverified**, record the network/database error and timestamp, and rerun `uv run --locked --group dev python tools/cleanai.py gauntlet connected-audit` when the required service is reachable. Deterministic local release evidence remains separate.
