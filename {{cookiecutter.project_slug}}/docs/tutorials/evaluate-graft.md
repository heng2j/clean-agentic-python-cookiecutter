---
status: reference
authority: tutorial-evaluate-graft
owner: maintainers
last_verified: 2026-09-03
applies_to:
  - ".cleanai/graft-experiment.toml"
  - ".cleanai/benchmark-tasks.toml"
  - ".cleanai/runs/**"
  - "tools/graft_adapter.py"
---
# Evaluate Graft without grading your own enthusiasm

## Research question

> For the same repository revision, task, agent, model, permissions, budget, and
> acceptance oracle, does structural Graft access reduce irrelevant exploration
> and total accepted-change cost without reducing correctness, increasing human
> intervention, or increasing review and rework?

Write the decision rule before the first run. Reject any reproducible correctness
or accepted-rework regression before considering token, latency, or cost gains.

## Cohorts

| Cohort | Graft access |
|---|---|
| `baseline-no-graft` | none; no MCP and no adapter calls |
| `graft-structural-cli` | project adapter CLI only |
| `graft-mcp-pull` | reviewed local MCP example; no hooks or prompt injection |

Use the same committed generated project for the primary comparison. Changing
only tool availability gives a cleaner causal test than comparing two templates
with different tracked files.

## Freeze the trial

Record repository commit/cleanliness, OS and architecture, Python, uv, Node,
Graft, agent, model and client versions, enabled MCP servers, tool permissions,
time/token budget, cache state, network policy, reviewer, and exact acceptance
commands. Use a fresh worktree or clone for every run.

Use stable tasks from `.cleanai/benchmark-tasks.toml`; validate their independent
oracles before testing. Do not reveal expected file paths in the prompt. Run at
least three repetitions per task and cohort, and counterbalance cohort order.

## Run and record

Start the existing agent-friction ledger:

```bash
uv run --locked --group dev python tools/cleanai.py friction start \
  --task locate-and-explain --agent codex --cohort baseline-no-graft
```

Repeat from the same baseline for the CLI cohort. The agent may use only commands
through `tools/graft_adapter.py`. For MCP, copy `.mcp.json.example` locally,
restart the client, and record the fixed tool-schema/context overhead.

Capture, when available:

- independently verified success and human acceptance;
- files opened before the first correct edit;
- relevant and irrelevant files opened;
- Graft calls, normal searches, and fallback reads;
- tool calls, tokens, latency, compute, and monetary cost;
- graph build and refresh cost;
- fixed MCP schema/context cost;
- changed-file precision and forbidden-surface edits;
- exact gates and exit codes;
- human interventions and reviewer corrections; and
- post-review or post-merge rework.

Do not invent unavailable measurements or treat missing traces as zero cost.

Finish using the run directory printed by the start command:

```bash
uv run --locked --group dev python tools/cleanai.py friction finish \
  .cleanai/runs/<run-directory> --accepted yes --human-interventions 0
```

Then compare like cohorts only:

```bash
uv run --locked --group dev python tools/cleanai.py friction compare \
  --cohort baseline-no-graft --cohort graft-structural-cli
```

## Adversarial task selection

Include a cross-module change with sibling implementations, an exhaustive
"every implementation" task, decorator/configuration-mediated behavior, a
dynamic import or plugin boundary, a small local task where MCP overhead may
dominate, and a packaging/release defect that a call graph cannot reveal.

Inspect cases where the graph is fresh but incomplete, ranked retrieval misses a
required sibling, a generated explanation is treated as authority, or context
saved during exploration is repaid through correction and review.

## Decision record

Report distributions, not only a best run. Separate observed measurements from
inference. Record the task bank, exclusions, correctness, acceptance, total
context/compute accounting, qualitative failures, privacy/portability burden,
and the decision: adopt, keep experimental, narrow, replace, or remove.

The agent can collect evidence. The human owns the acceptance rule, causal
interpretation, integration decision, and learning.
