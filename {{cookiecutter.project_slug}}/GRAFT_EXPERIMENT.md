# Optional Graft experiment

This project works fully without Graft. Its default, **F0**, is current source,
`rg`, human-owned contracts and ADRs, tests, and deterministic CleanAI gates.

The optional **F1** experiment uses published `@nanonets/graft` `0.16.0` through
a project-owned structural CLI adapter. Graft may help locate code or suggest
static relationships. Its output is derived navigation evidence—not authority,
an exhaustive search, a correctness result, or design rationale. No token,
cost, correctness, or productivity gain has been established.

## First safe route

1. Read the [integration and privacy guide](docs/integrations/graft.md).
2. Inspect `tools/graft-runtime/package-lock.json` and the native install-script
   warning before authorizing a connected installation.
3. Confirm that the project is a Git repository and its intended source files
   are tracked. A fresh Cookiecutter render is not initialized automatically;
   use the [evaluation tutorial](docs/tutorials/evaluate-graft.md#1-create-the-required-git-baseline)
   for the explicit init/first-commit path. Graft `0.16.0` can omit tracked
   Python files under hidden directories; the adapter then fails closed and
   F1 is unavailable. Keep using F0—do not untrack, move, or ignore legitimate
   source to make the graph pass. See [troubleshooting](docs/troubleshooting.md#graft-build-fails-on-a-tracked-source-under-a-hidden-directory).
4. From the project root, run the read-only adapter check:

   ```bash
   uv run --locked --group dev python tools/graft_adapter.py doctor
   ```

   The adapter subcommand writes no Graft state. The `uv run` wrapper may prepare
   the locked Python environment if it is missing or stale; complete the normal
   `uv sync --locked --group dev` setup first.
5. Only after explicit authorization, install the reviewed local lock:

   ```bash
   uv run --locked --group dev python tools/graft_adapter.py install --apply
   uv run --locked --group dev python tools/graft_adapter.py doctor
   uv run --locked --group dev python tools/graft_adapter.py build
   ```

6. Follow the [worked structural example](docs/integrations/graft.md#worked-source-verification)
   and, for an actual comparison, the
   [evaluation tutorial](docs/tutorials/evaluate-graft.md).

Installation is never a Cookiecutter or Python-gate side effect. MCP,
`graft init`, global installs/configuration, hooks, status lines, prompt injection,
visualization/export, LSP, deep/model-backed operations, and provider
credentials are outside this profile.

Before invoking any external tool, use a secret-free shell. The adapter supplies
an allowlisted child environment, but it is not an operating-system sandbox.
Stop direct Graft processes and other writers before cleanup; the project lock
coordinates adapter commands, not unrelated processes.
Use `uv run --locked --group dev python tools/graft_adapter.py remove --check`
to inventory local state and
`remove --apply` only after reviewing that inventory.
