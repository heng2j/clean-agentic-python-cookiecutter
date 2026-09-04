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

## Included

A generated project receives:

- a pinned, project-owned structural adapter for Graft `0.17.0` that forces
  telemetry off, strips model credentials, blocks project `.env` loading, uses
  hash freshness, suppresses the inspected release's npm update check, and
  prevents upstream ignore-file writes;
- concise `AGENTS.md` guidance that keeps Graft output non-authoritative;
- a gitignored local graph path;
- an inactive project-local MCP example;
- CLI, MCP, and no-Graft cohort definitions;
- source, privacy, upgrade, and removal documentation;
- a hands-on A/B evaluation tutorial and evaluator prompt; and
- focused adapter and template tests.

## Deliberately excluded

The template does not:

- install Node or Graft;
- add Graft to Python dependencies;
- run `graft init`;
- activate hooks, status lines, prompt injection, or global configuration;
- invoke `graft build --deep` or expose model-provider credentials;
- commit the generated `graft/` cache; or
- make Graft part of fast, full, hardening, or release gates.

## Branch workflow

Generate the control project from `scientific-open-source-variant` and the
experimental project from `experimental-graft-variant`. For the strongest
causal comparison, also run no-Graft and Graft cohorts on the same committed
experimental project, changing only tool availability.

See the generated project's:

- `docs/integrations/graft.md`;
- `docs/tutorials/evaluate-graft.md`;
- `docs/research/graft-source-traceability.md`;
- `docs/adr/0005-experimental-graft-context-layer.md`; and
- `prompts/evaluate-graft.md`.

## Promotion boundary

Keep the work on this branch until repeated task-level evidence shows no
correctness or rework regression and the total context, setup, compute, privacy,
portability, and maintenance costs are justified. The first promoted version
may retain only CLI pull mode even if MCP or automatic integration underperforms.
