# Evaluate Graft on an existing repository

Act as an independent agent-workflow evaluator, not an advocate for Graft.
Determine whether project-scoped structural Graft access improves
**accepted-change efficiency** without reducing correctness, increasing review
and rework, crowding persistent context, or weakening human understanding.

## Required controls

Freeze the repository commit, clean-worktree protocol, task text, independent
acceptance commands, agent, model, client, permissions, time/token budget,
cache state, reviewer, and network policy. Compare:

1. `baseline-no-graft`;
2. `graft-structural-cli`; and
3. optional `graft-mcp-pull`.

Use fresh worktrees and at least three repetitions per task/cohort. Counterbalance
order. Do not enable `graft init`, upstream hooks, global configuration, prompt
injection, `--deep`, or model-backed enrichment. Preserve failed, missing, and
rejected runs rather than silently excluding them.

Treat Graft maps, rankings, summaries, edges, and blast reports as derived
advisory evidence. Ranked retrieval is not exhaustive. Verify consequential
claims against source, contracts, ADRs, tests, runtime evidence, and human
acceptance.

## Measurements

Record per trial:

- independently verified task success and human acceptance;
- human interventions, reviewer corrections, and later rework;
- files opened before the first correct edit;
- relevant/irrelevant files opened and changed-file precision;
- Graft calls, ordinary searches, and fallback reads;
- graph build and refresh cost;
- fixed MCP schema/context cost;
- tool calls, tokens, latency, compute, and monetary cost when available;
- exact gates, exit codes, and skipped or unavailable evidence; and
- whether the human can explain what changed, why it works, and where it fails.

Do not invent unavailable measurements. Mark them **Unverified**.

## Adversarial tasks

Include cross-module sibling implementations, decorator/configuration-mediated
behavior, a dynamic import or plugin boundary, an exhaustive "every occurrence"
task, a small local task where MCP overhead can dominate, and a packaging or
release failure not obvious from a static graph.

## Return

Provide the frozen protocol and deviations, raw evidence locations, per-trial
results and cohort distributions, correctness/acceptance analysis before
efficiency analysis, total context and compute accounting, qualitative failure
taxonomy, threats to validity, human-learning observations, and a decision:
adopt, keep experimental, narrow, replace, or remove.

Label material claims **Observed**, **Source-supported**, **Inferred**,
**Recommended**, or **Unverified**. A small self-evaluation cannot establish a
universal token- or cost-saving claim.
