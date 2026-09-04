# Experimental Graft variant

## Purpose

This branch layers a bounded Graft experiment on top of
`scientific-open-source-variant` at baseline commit
`72a7e52eb0e2ac35ef4ca36f716dc2e183afc6c4`.

It exists to answer an empirical question before anything is promoted to
`main`:

> Does Graft reduce repeated repository exploration and total accepted-change
> cost for generated Python projects without reducing correctness, increasing
> review/rework, crowding persistent context, or weakening human understanding?

## Generate a project from this branch

```bash
uvx --from 'cookiecutter==2.7.1' cookiecutter \
  https://github.com/heng2j/clean-agentic-python-cookiecutter \
  --checkout experimental-graft-variant

cd clean-agentic-scientific-python-project
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Then open `GRAFT_EXPERIMENT.md` in the generated project. Graft remains absent
until you explicitly review and install the pinned external package.

## Included

A generated project receives:

- `GRAFT_EXPERIMENT.md` as the human entry point;
- a project-owned structural adapter pinned to Graft `0.17.0`;
- a conservative Node floor of `22.12.0`;
- graph and runtime state confined to the already ignored
  `artifacts/graft/` tree;
- an inactive, project-local `.mcp.json.example`;
- a machine-readable experiment policy under `.cleanai/`;
- no-Graft, CLI-pull, and MCP-pull evaluation cohorts;
- an integration/trust-boundary guide;
- a hands-on A/B evaluation tutorial and portable evaluator prompt; and
- focused adapter and template-rendering tests.

The adapter forces telemetry off, removes common model credentials, redirects
dotenv loading away from the project `.env`, uses content-hash freshness,
suppresses the inspected release's npm update check, and prevents upstream
ignore-file writes.

The variant deliberately does **not** append a large Graft block to `AGENTS.md`
or `CLAUDE.md`. Product-specific instructions stay on demand so persistent
context remains small.

## Deliberately excluded

The template does not:

- install Node or Graft;
- add Graft to Python dependencies;
- run `graft init`;
- activate hooks, status lines, automatic prompt injection, or global settings;
- invoke `graft build --deep`, LSP enrichment, visualization, or model-backed
  blast naming;
- commit the generated graph; or
- make Graft part of fast, full, hardening, or release gates.

Graft output is derived navigation evidence. It does not override current
source, executable behavior, contracts, ADRs, tests, or human acceptance.
Ranked retrieval is not exhaustive search.

## Evaluation workflow

For the strongest causal comparison, use the same committed generated project
and change only tool availability:

1. `baseline-no-graft`;
2. `graft-structural-cli`; and
3. optional `graft-mcp-pull`.

Use stable tasks, fresh worktrees, the same model/client/permissions/budget,
independent acceptance commands, repeated runs, and a decision rule written
before results exist. Include graph build and refresh cost, fixed MCP context,
human interventions, reviewer corrections, and rework—not only token savings.

For a secondary template-overhead comparison, generate a control project from
`scientific-open-source-variant` and an experimental project from this branch.
That answers a different question because their tracked files differ.

## Promotion boundary

Keep this work on `experimental-graft-variant` until repeated task-level evidence
shows no correctness or rework regression and the total context, setup, compute,
privacy, portability, and maintenance costs are justified. The first promoted
version may retain only CLI pull mode even if MCP or broader automation
underperforms.
