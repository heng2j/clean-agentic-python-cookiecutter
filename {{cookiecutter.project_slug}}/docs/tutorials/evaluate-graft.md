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
  - "tools/graft-runtime/**"
---
# Evaluate Graft without grading your own enthusiasm

## Question and current answer

> For one frozen repository, task, agent/model/client, permissions, budget, and
> held-out acceptance oracle, does bounded structural CLI access reduce total
> accepted-change cost without reducing correctness, scope discipline, review,
> privacy, or human understanding?

The current answer is **Unverified**. This tutorial is an experiment protocol,
not evidence that Graft saves tokens or improves work.

Compare only:

| Cohort | Tool access |
|---|---|
| `baseline-no-graft` (F0) | current source, `rg`/`git grep`, contracts, tests, and ordinary gates |
| `graft-structural-cli` (F1) | the same tools plus bounded project-adapter CLI commands |

MCP, exports, LSP, deep/model-backed operations, hooks, status lines, and prompt
injection are not experimental cohorts in this profile.

## 1. Create the required Git baseline

Cookiecutter deliberately does not initialize or commit a repository. From a
freshly generated project, make that human-owned decision before using the
friction ledger or building a structural index:

```bash
git init -b main
git add .
git commit -m "Initial generated project"
git status --short
git rev-parse HEAD
```

Expected: the commit succeeds, status is empty, and the final command prints
the baseline revision. If identity is not configured, Git will stop; configure
the correct project identity deliberately and retry. Do not let a script invent
an identity or commit existing user work.

Record the printed `git rev-parse HEAD` value as the frozen starting revision.
Use a fresh clone or worktree from that exact commit for every repetition.

## 2. Preregister outside the agent's readable task surface

Before any run, the human evaluator records:

- task text and a predicted failure;
- held-out expected paths, acceptance commands, and review rubric;
- commit and clean-state rule;
- OS/architecture, Python, uv, Node, Graft package/integrity, and cache state;
- agent, model, client, settings, permissions, network, time, and token budget;
- available tools and persistent/tool-schema context;
- repetition count, counterbalanced order, exclusions, and stopping rule; and
- the decision rule below.

Keep acceptance oracles and expected paths outside the agent-readable worktree
and permissions. The bundled `.cleanai/benchmark-tasks.toml` and friction ledger
are useful instrumentation examples, not a blinded oracle: their expected globs
and verification commands are repository-readable. If a run can read its answer
key, label it **task-leaked** and exclude it from causal claims without deleting
the raw result.

The bundled three tasks are smoke examples. They are not broad enough to support
a promotion decision. A scored bank also needs cross-module behavior, sibling
implementations, exhaustive contract search, a dynamic-Python edge, a seeded
defect, blast-radius analysis, source-versus-wheel behavior, and stale-context
correction on a medium fixture and a frozen real repository.

## 3. Validate the independent oracle first

Run each acceptance command on a known-good and deliberately failing state before
the agent trial. Record exact commands, cwd, exits, output, writes, network, and
what each command cannot establish. If the oracle cannot distinguish red from
green, stop; efficiency measurements cannot rescue the experiment.

## 4. Run F0 and F1 from fresh states

In a fresh F0 worktree, start a bundled instrumentation smoke run:

```bash
uv run --locked --group dev python tools/cleanai.py friction start \
  --task locate-and-explain --agent codex --cohort baseline-no-graft
```

Record the printed value as `<f0-run-directory>`. For the F0 cohort, the agent
must not call the adapter and no Graft process may be available through its
tools. Run the task, apply the held-out review, and finish that exact record:

```bash
uv run --locked --group dev python tools/cleanai.py friction finish \
  <f0-run-directory> --accepted yes --human-interventions 0
```

Return to a separate fresh worktree at the same frozen revision. Start F1 and
record its distinct `<f1-run-directory>` before setup, so cold installation and
graph-build cost are not silently excluded:

```bash
uv run --locked --group dev python tools/cleanai.py friction start \
  --task locate-and-explain --agent codex --cohort graft-structural-cli
```

For F1, authorize and install the reviewed local runtime once per declared cold
or warm-cache protocol, then verify it:

```bash
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py doctor
uv run --locked --group dev python tools/graft_adapter.py build
```

The agent may use only the command-specific adapter surface documented in the
[integration guide](../integrations/graft.md). Direct `graft`, `npx`, MCP, and
provider-backed calls invalidate the cohort. Preserve adapter JSON and
`artifacts/graft/evidence/last-run.json` with the external trial evidence.

Run the same task and finish only the F1 record after independent review:

```bash
uv run --locked --group dev python tools/cleanai.py friction finish \
  <f1-run-directory> --accepted yes --human-interventions 0
```

Do not set `--accepted yes` from the agent's own summary. The human reviewer
applies the preregistered rubric and held-out oracle.

Compare completed like-task, like-baseline records:

```bash
uv run --locked --group dev python tools/cleanai.py friction compare \
  --cohort baseline-no-graft --cohort graft-structural-cli
```

The bundled comparison is descriptive. Confirm separately that every row used
the same held-out controls; missing metadata is `UNVERIFIED`, not equality.

## 5. Account for the whole task

Record correctness and human acceptance before efficiency:

- acceptance command results and human decision;
- missed sibling implementations, forbidden edits, reviewer corrections, and
  later rework;
- time/tool calls/files opened to first relevant source and first correct edit;
- relevant versus irrelevant reads and changed-file precision;
- cold install/build, warm refresh, CPU, peak memory, and disk;
- persistent instructions and any fixed tool context;
- queries, Graft output, exact follow-up source reads, and `rg`/test fallbacks;
- total input/output tokens and cost when available; and
- whether the reviewer can explain the final change without the agent summary.

Use clearly labelled proxies when exact token or resource traces are unavailable:

```text
context precision = task-relevant retrieved tokens / all retrieved tokens

net context cost = persistent context + tool context + queries + tool output
                 + fallback reads + correction/rework context

net operational cost = install + build/refresh + compute + maintenance
                     + human review
```

Never report missing traces as zero. Never count a smaller Graft response while
omitting the source reads and correction context needed to verify it.

## 6. Exercise known failure modes

The shipped adapter exposes only bounded `ask` retrieval. Evaluate the broader
upstream capabilities below only in disposable, isolated research fixtures;
their appearance in this task bank does not authorize them in F1.

Include runs where:

- ranked retrieval misses a required sibling;
- a decorator, registry, entry point, dynamic import, or configuration creates
  a relationship absent from the graph;
- an exhaustive `rg`/`git grep` baseline finds more than indexed `grep`;
- the graph is stale after staged, unstaged, renamed, moved, or deleted files;
- duplicate symbol names produce an ambiguous caller result;
- a package works from source but fails from its installed wheel;
- a small local task makes tool overhead dominate; and
- persuasive output tempts the agent to skip an exact source read or test.

Preserve failures, timeouts, missing tools, rejected work, and invalid runs with
their disposition. Do not silently remove them from the denominator.

## 7. Apply the decision rule

Reject promotion for any reproducible correctness, human-acceptance, privacy,
scope, reviewer-correction, or rework regression. Only then consider whether
median total context or operational cost improved across representative
multi-file tasks without harming relevant-file recall.

Report distributions and task-level failures, not only a best run or one scalar.
The human owns acceptance, causal interpretation, and promotion. Until those
controlled results exist, keep F0 as default and F1 experimental.
