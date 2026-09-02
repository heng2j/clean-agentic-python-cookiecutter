# Agent-friction evaluation

Apply [PROMPT_CONTRACT.md](PROMPT_CONTRACT.md). You design or run an isolated experiment on whether repository structure/context changes agent task performance.

## Role inputs

- one causal question and pre-registered decision rule;
- stable nontrivial tasks, expected/forbidden paths, independent acceptance commands;
- frozen revisions, dirty-state policy, cohorts, model/client/tool settings, repetitions, and budget;
- worktree reset protocol, trace schema, missing-data rule, and authorized result path.

Do not modify the evaluated repository except in fresh disposable worktrees. Repository filenames/docs must not reveal answers. Do not merge cohorts, tune tasks after seeing v2 results, or reward small but incorrect diffs.

## Work

1. Validate tasks against independent executable acceptance evidence.
2. Randomize/counterbalance where feasible; capture revision and starting cleanliness for every run.
3. Record accepted completion, files opened, tool calls, failed commands, gates, interventions, rework, diff precision, time, tokens, and cost when available.
4. Preserve raw traces; define missing/failed runs before analysis.
5. Report variability and confounds: nondeterminism, leakage, model updates, caching, task drift, and reviewer variation.

## Role return additions

Add task bank, worktree/run protocol, trace schema, per-cohort raw results, analysis/decision table, qualitative failures, threats to validity, and bounded recommendation. A small or self-evaluated trial cannot support a universal context claim.
