# Evaluate Graft on an existing repository

Use this role delta with [`PROMPT_CONTRACT.md`](PROMPT_CONTRACT.md); do not use
it as a standalone authorization to install software, expose source, or edit a
repository.

Act as an independent agent-workflow evaluator, not an advocate for Graft.
Determine whether project-scoped structural Graft access improves
**accepted-change efficiency** without reducing correctness, increasing review
and rework, crowding persistent context, or weakening human understanding.

## Required controls

Freeze the repository commit, clean-worktree protocol, task text, independent
acceptance commands, agent, model, client, permissions, time/token budget,
cache state, reviewer, and network policy. Compare only:

1. `baseline-no-graft`;
2. `graft-structural-cli` through the project adapter.

Use fresh worktrees and at least three repetitions per task/cohort. Counterbalance
order. Keep acceptance oracles and expected paths outside the agent-readable
worktree. Do not enable MCP, `graft init`, upstream hooks, global configuration,
prompt injection, visualization/export, LSP, `--deep`, or model-backed
enrichment. Preserve failed, missing, and rejected runs rather than silently
excluding them.

Treat Graft maps, rankings, summaries, edges, and blast reports as derived
advisory evidence. Ranked retrieval is not exhaustive. Verify consequential
claims against source, contracts, ADRs, tests, runtime evidence, and human
acceptance.

Use Graft to choose where to inspect, then cite the exact current source ranges
you read. For any `all`, `every`, `none`, or completeness claim, use exhaustive
`rg` or `git grep` plus applicable executable verification; do not substitute a
ranked result or blast graph.

## Measurements

Record per trial:

- independently verified task success and human acceptance;
- human interventions, reviewer corrections, and later rework;
- files opened before the first correct edit;
- relevant/irrelevant files opened and changed-file precision;
- Graft calls, ordinary searches, and fallback reads;
- graph build and refresh cost;
- tool calls, tokens, latency, compute, and monetary cost when available;
- exact gates, exit codes, and skipped or unavailable evidence; and
- whether the human can explain what changed, why it works, and where it fails.

Do not invent unavailable measurements. Mark them **Unverified**.

## Adversarial tasks

Include cross-module sibling implementations, decorator/configuration-mediated
behavior, a dynamic import or plugin boundary, an exhaustive "every occurrence"
task where fixed tool overhead can dominate, and a packaging or
release failure not obvious from a static graph.

## Return

Provide the frozen protocol and deviations, raw evidence locations, per-trial
results and cohort distributions, correctness/acceptance analysis before
efficiency analysis, total context and compute accounting, qualitative failure
taxonomy, threats to validity, human-learning observations, and a decision:
adopt, keep experimental, narrow, replace, or remove.

Label material claims **Observed**, **Source-supported**, **Inferred**,
**Recommended**, or **Unverified**. A small self-evaluation cannot establish a
universal token- or cost-saving claim. Do not claim even a local gain until the
same held-out acceptance evidence shows no correctness, scope, review, or rework
regression and total context includes installation, graph work, queries, Graft
output, fallback reads, corrections, and review.
