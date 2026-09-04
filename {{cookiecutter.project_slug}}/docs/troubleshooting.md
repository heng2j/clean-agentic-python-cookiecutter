---
status: normative
authority: troubleshooting
owner: maintainers
last_verified: 2026-09-03
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

## direnv does not load `.env`

That is the safe default. Review `.envrc` and [the data/secret boundary](science/data-and-secrets.md), then deliberately uncomment `dotenv_if_exists .env` only for tasks that need it. All child processes and coding agents inherit exported values. Run deterministic gates from a secret-free shell.

## `science-audit` rejects a static file

Add a complete entry to `static/manifest.toml` with the repository-relative
path, SHA-256, source or generation method, license, and description. A matching
hash proves file identity only; it does not validate the source, license, or
scientific meaning.

## Graft `doctor` reports that the local runtime is absent

That is the normal no-Graft state, not a Python-project failure. Continue with
F0, or review the npm lock and native install-script boundary in the
[Graft guide](integrations/graft.md) before explicitly running:

```bash
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py doctor
```

Do not replace the local lock with a global install or unpinned `npx` command.

## The Graft adapter reports no Git repository or untracked files

This is a scope guard, not a request to stage everything. From the project root,
inspect the repository and untracked set without changing either:

```bash
git rev-parse --show-toplevel
git status --short
git ls-files --others --exclude-standard
```

For a brand-new render, follow the
[explicit init and first-commit tutorial](tutorials/evaluate-graft.md#1-create-the-required-git-baseline).
For existing work, review each listed file—source, documentation, data, or
otherwise—and either add it through the normal project workflow, ignore it for
a justified project reason, or keep using F0 until its ownership is resolved.
Do not make an invented commit, delete a file, or broaden the graph just to
clear the error.

## Graft installation fails around a native parser

Preserve the JSON failure. Published Graft `0.16.0` requires npm lifecycle
scripts to create a `tree-sitter-kotlin` native binding; `--ignore-scripts` does
not produce a usable runtime. Do not work around the failure by executing a
different unreviewed installer. Mark F1 **Unverified** and continue with F0, or
review the platform/dependency failure before authorizing another attempt.

If the failure reports a stale `.node_modules.previous`, a validated new
runtime may already be active while cleanup of the prior runtime was
interrupted. Do not delete or restore either tree blindly. Preserve the JSON
failure, run `doctor`, inventory with `remove --check`, and compare both trees
before a maintainer chooses removal or recovery.

## The Graft graph is missing, stale, corrupt, or interrupted

Run `uv run --locked --group dev python tools/graft_adapter.py doctor`, then
rebuild. `doctor` validates the
local runtime, not graph freshness, so it can pass while a graph transaction's
`previous-graph` or receipt backup still needs recovery. A successful rebuild
does not prove static-analysis completeness.

An absent or stale graph that prevents the requested operation is
`UNVERIFIED`; malformed, corrupt, tampered, or unsafe state is `FAIL`. Neither
status permits using the graph as evidence.

If an error names stale graph or receipt backup state, do not rename, merge, or
delete either tree by hand. Preserve the JSON failure and copy any evidence you
need outside `artifacts/graft/`. Then inventory the entire contained experiment
before removal:

```bash
uv run --locked --group dev python tools/graft_adapter.py remove --check
uv run --locked --group dev python tools/graft_adapter.py remove --apply
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

`remove --apply` deletes the local runtime, graph, receipts, and experiment
evidence together only after its tracked-file and ownership/receipt preflights
pass. A tracked or unknown descendant returns `FAIL` before any deletion; move
that material through a normal reviewed source change. Reinstall and rebuild
only if the experiment still justifies that cost. Never repair ignored graph
files by hand or treat a directory's existence as freshness.

## Graft `build` fails on a tracked source under a hidden directory

Published Graft `0.16.0` was observed to omit a tracked Python file such as
`.hidden/visible.py`. The adapter compares graph file nodes with the complete
Git-tracked source set, returns `FAIL`, removes the staged graph, and publishes
nothing when the sets differ. This is a known F1 applicability limit, not a
project-source defect.

Keep the legitimate source and continue with F0. Use `git ls-files`,
`rg --hidden`, exact source reads, and executable tests for navigation and
verification. Do not untrack, rename, move, or ignore a file merely to make
Graft pass, and do not weaken the adapter's graph-coverage check. A later,
explicitly reviewed Graft version may be reevaluated against the same fixture.

## I expected a Graft map, caller graph, indexed grep, or blast command

Those upstream surfaces are intentionally not exposed by the bounded adapter.
Controlled evaluation did not establish enough completeness or benefit to earn
their attack surface and maintenance cost. Use current source, `rg`/`git grep`,
the exact Git diff, and executable tests. Testing a broader upstream capability
requires a disposable research fixture outside the F1 workflow.

## My client does not expose Graft through MCP

That is intentional. MCP is not included in this profile because its fixed
schema/instruction context, repository-root assumptions, and server lifecycle
did not earn promotion. Use the bounded CLI adapter or the no-Graft workflow;
do not add an upstream MCP configuration as a troubleshooting shortcut.

## A connected dependency audit is unavailable

Mark the result **Unverified**, record the network/database error and timestamp, and rerun `uv run --locked --group dev python tools/cleanai.py gauntlet connected-audit` when the required service is reachable. Deterministic local release evidence remains separate.
