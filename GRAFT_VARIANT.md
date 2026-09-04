# Experimental Graft variant

## Purpose

This branch layers a bounded Graft experiment on
`scientific-open-source-variant` commit
`72a7e52eb0e2ac35ef4ca36f716dc2e183afc6c4`. It asks:

> Can structural navigation reduce total accepted-change cost without reducing
> correctness, scope discipline, reviewability, privacy, or human understanding?

The answer is **not established**. A useful graph or smaller response is not a
successful task. Correctness and human acceptance come first; total context must
include setup, tool schemas, queries, output, fallback source reads, corrections,
and review.

## Existing projects: adopt, do not overwrite

Do not render this Cookiecutter into a living repository or replace its package,
lock, CI, context, license, release, or architecture files wholesale. Generate a
separate sibling reference project, freeze and audit the existing repository,
then adapt one verified capability at a time.

Use the step-by-step [existing-project adoption tutorial](ADOPT_EXISTING_PROJECT.md)
for the recommended audit → context → truthful gates → bounded cleanup → optional
Graft sequence.

## Generate this branch

```bash
uvx --from 'cookiecutter==2.7.1' cookiecutter \
  https://github.com/heng2j/clean-agentic-python-cookiecutter \
  --checkout experimental-graft-variant

cd clean-agentic-scientific-python-project
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

The ordinary Python path above does not install, start, or require Graft. Open
the generated [`GRAFT_EXPERIMENT.md`](%7B%7Bcookiecutter.project_slug%7D%7D/GRAFT_EXPERIMENT.md)
only if you deliberately choose the experiment.

## Capability decisions

| Level | Capability | Decision |
|---|---|---|
| F0 | No Graft: source, `rg`, contracts, tests, and CleanAI gates | **Keep as the default and control** |
| F1 | Bounded structural CLI through the project adapter | **Keep experimental**; verify every consequential result |
| F2 | MCP tools | **Remove/disable**; fixed schemas, upstream instructions, root assumptions, and process lifecycle are not justified |
| F3 | Deterministic visualization/export | **Do not promote**; no safe, useful export earned its maintenance cost |
| F4 | LSP enrichment | **Disable**; extra dependencies and accuracy/cost remain unevaluated |
| F5 | Deep/model-backed summaries | **Disable**; source-disclosure, credential, cost, and hallucination risks are outside this profile |
| F6 | Hooks, status lines, or prompt injection | **Disable**; persistent context and global side effects conflict with the experiment's trust model |

## What the generated project includes

- a concise human entry point and on-demand integration guide;
- a project-owned, command-specific adapter;
- a reviewed project-local npm lock for published `@nanonets/graft` `0.16.0`;
- an ignored project-local runtime under `tools/graft-runtime/node_modules/`
  and regenerable graph/evidence state under `artifacts/graft/`;
- no-Graft and structural-CLI comparison cohorts;
- an evaluation tutorial and portable evaluator prompt; and
- focused adapter, removal, and template tests, plus a separately recorded
  real-package validation journey.

It does not install during generation, alter user-home configuration, call
`graft init`, enable MCP/hooks/status lines/prompt injection, invoke LSP/deep or
model-backed operations, commit graph output, or add Graft to a Python gate.

## Authority and routing

Humans own intent, architecture, epistemic standards, integration, and
acceptance. Use this order:

1. human-owned contracts, ADRs, invariants, and explicit decisions;
2. executable contracts and deterministic gates;
3. current source and observed behavior;
4. derived Graft navigation evidence; and
5. historical or generated reference material.

Graft can suggest **where to inspect**; it cannot decide **what to believe**.
Ranked retrieval and static relationship analysis are not exhaustive. Use `rg` or
`git grep`, exact source reads, runtime evidence, and tests for completeness or
behavior claims.

## Promotion boundary

F1 remains experimental until repeated, fresh-worktree comparisons show no
correctness, human-acceptance, reviewer-correction, rework, privacy, or scope
regression and demonstrate a worthwhile total-cost improvement on more than the
tiny generated example. Missing measurements are `UNVERIFIED`, never zero.

Do not promote this branch to `main` from a visually persuasive graph, a single
agent run, or output-token reduction alone.
