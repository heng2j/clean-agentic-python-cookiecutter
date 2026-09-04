# Graft retrieval and context evaluation

## Decision

**Observed:** on the preregistered deterministic benchmark, task-shaped
`rg`/`git grep` (F0/C0) was both more complete and smaller than published Graft
0.16.0 through structural CLI (F1/C1) or MCP (F2/C2). F0 mean precision/recall
was 0.728/0.969. F1 and F2 were 0.479/0.748. Median one-query net context proxies
were 960, 3,363, and 6,762 bytes respectively.

**Recommended:** do not promote Graft as a context-reduction, exhaustive-search,
or blast-radius control. Retain only the bounded F1 CLI as optional navigation
evidence. Keep F2 disabled. For *all*, *every*, *none*, or *complete* claims,
start with exhaustive lexical search and executable verification.

**Observed:** six fresh-clone agent trials on one held-out bounded change passed
the external acceptance oracle and repository tests: 3/3 C0 and 3/3 research
C1. Every C1 agent also used `rg` and/or direct source inspection, so no
correctness advantage from the broader Graft condition was observed. The trial
wrapper exposed upstream `grep` and `callers`; final F1 does not. Accepted-task
behavior for the final narrowed adapter is **Unverified**.

**Observed:** the preregistered final-adapter rerun stopped before any task
agent started. Real Graft 0.16 omitted tracked `.hidden/visible.py`; the exact
`6966b55` adapter returned exit 2/FAIL after 2.672028 seconds, removed the
staged graph, and did
not run `check` or `ask`. Repetitions 2–3 were not run under the frozen stop
rule. This is an F1 applicability failure plus a successful fail-closed control,
not an accepted-task correctness result.

**Unverified:** no model was called in the deterministic benchmark. Byte counts
are not tokenizer or billing traces. Exact trial tokens, billed cost, elapsed
time, file-open counts, complete human intervention, reviewer correction, and
rework were not captured.

## Preregistered design

The decision rule was frozen before comparative outputs were inspected. The
evaluation used 16 file-level queries across four frozen repositories and three
repetitions per cohort, yielding 144 query records. Runs 1 and 3 used C0→C1→C2;
run 2 reversed query and cohort order. Held-out truth sets were outside every
searched/indexed repository.

| Repository | Frozen revision | Tracked files | Purpose |
|---|---|---:|---|
| Generated Clean Agentic project | `eb4804ec4210762d4e86274eaae363136116a313` | 141 | Real generated Python starter |
| Adversarial Python fixture | `cbc0c46993201002082b8ef5496cabbfc7083feb` | 26 | Duplicate names, dynamic import, package/wheel failure |
| Mixed-language fixture | `cee054b3f759e118bdbb98414b464210a25662d5` | 16 | JavaScript → JSON → dynamic Python flow |
| Jonathon Vandezande's `uv-cookiecutter` snapshot | benchmark copy `0a6ea135cadcc227823923eed76a91cc539f484c`; upstream source `3446ae6` | 47 | Frozen modest open-source template |

The cohorts were:

- **C0 / F0:** task-shaped `rg` or `git grep`, followed by source/executable
  verification.
- **C1 / F1:** real `@nanonets/graft` 0.16.0 structural CLI under Node 22.12.0.
- **C2 / F2:** a fresh project-scoped Graft MCP server per query, including
  initialize, tool discovery, one call, and teardown.

Graft ran with isolated home/state, `DO_NOT_TRACK=1`, `CI=1`, an empty dotenv
file, no inherited provider credentials, and graphs outside source worktrees.
All source trees remained clean.

The C1 benchmark exercised upstream structural capabilities to evaluate them
individually. It is not a claim that the final adapter exposes each capability;
v2 intentionally narrows the project-owned surface to `build`, `check`, and
bounded `ask`.

## Coverage against the required task bank

The evidence is narrower than the charter's full representative-task design.
Deterministic retrieval probes and executable fixture checks are useful, but
they are not substitutes for repeated agent changes with independent human
acceptance.

| Required task family | Deterministic / fixture evidence | Repeated fresh-agent evidence | Status |
|---|---|---|---|
| Locate and explain a local behavior | Generated and fixture retrieval queries | None | **Observed at query level; agent outcome Unverified** |
| Trace a cross-module behavior | Mixed-language retrieval queries | None | **Observed at query level; agent outcome Unverified** |
| Make one bounded behavior change | External Unicode-whitespace oracle | 3 C0 + 3 broader research-C1 runs; final F1 prerequisite stopped before agent execution | **Observed for one task only; final F1 applicability failed and task outcome Unverified** |
| Find every implementation of a contract | Duplicate `normalize` oracle; same whitespace task required sibling edits | Same six runs, not an independent task family | **Observed narrowly; broader generalization Unverified** |
| Cross-module interface refactor | No representative change task | None | **Unverified** |
| Diagnose a seeded defect | Failure-path retrieval and executable fixture probes | None | **Observed at probe level; agent diagnosis Unverified** |
| Identify blast radius | Unique and duplicate-symbol static oracles | None | **Observed at tool-output level; agent use Unverified** |
| Handle a dynamic-Python relationship | Dynamic import, decorator, and dispatch fixtures | None | **Observed omissions; agent change Unverified** |
| Repair source-versus-wheel discrepancy | Executable wheel fixture and retrieval query | None | **Observed at fixture level; agent repair Unverified** |
| Correct stale context without treating history as authority | Four graph freshness mutations | None | **Observed at tool level; agent correction Unverified** |

| Required repository scale | Evidence actually used | Coverage status |
|---|---|---|
| Small generated example | 141-file generated starter | **Observed** |
| Medium realistic fixture with dynamic Python | Separate 26-file Python and 16-file mixed-language synthetic fixtures | **Unverified:** neither fixture establishes the required medium realistic cohort |
| Large enough frozen real open-source Python repository | A modest 47-file `uv-cookiecutter` snapshot | **Unverified:** no large real-Python cohort with meaningful exploration cost |

**Recommended:** do not represent the 16-query bank or the one agent-change
family as complete Stage 7 coverage. Before any promotion claim, run all ten
families across a realistic medium fixture and a frozen real repository large
enough to exercise exploration cost, with exact model/client identity, token,
time, file-open, correction, rework, and human-acceptance records.

## Metrics and accounting

The benchmark used:

```text
context precision = task-relevant retrieved bytes / all retrieved bytes

net context proxy = persistent/tool-schema bytes + query/result bytes
                  + required fallback bytes

net operational cost = installation + build/index + refresh
                     + compute + maintenance + human review
```

The exact charter definition additionally requires correction/rework context.
Those model/human quantities were unavailable and are therefore
**Unverified**, not zero.

No single net-operational-cost scalar is reported. **Observed:** F1 adds an
approximately 375 MiB runtime, benchmark cold/warm builds, a 3,217-line adapter,
and a 1,784-line focused test. **Unverified:** connected-install cost, distinct
refresh cost, CPU/peak process-tree memory, ongoing maintenance effort, and
human review time. Those missing terms prevent a total-cost advantage claim.

### Required-measure coverage

| Measure group | Captured evidence | Unverified boundary |
|---|---|---|
| Correctness, acceptance, change scope | External oracle, repository pytest, changed files, sibling implementations for one bounded task | Changed-file precision and missed siblings beyond that task; full applicable gate set per trial |
| Retrieval relevance | File-level precision/recall, false positives/negatives, result/fallback byte proxies | Actual relevant/irrelevant files opened and files before first correct edit |
| Human/review process | Agent-attributable unrelated edits and final oracle disposition | Human interventions; reviewer correction; post-review/merge rework; explanation without agent summary |
| Time and tool activity | Cold/warm graph build time; benchmark command duration | Time/tool calls to first relevant file; total task wall time; distinct refresh time |
| Compute and storage | Approximate installed disk footprint; graph bytes | CPU and reliable peak process-tree memory |
| Context and tokens | Persistent character/4 proxy, MCP fixed bytes, query/result/fallback byte proxies | Query versus response versus Graft-source tokens; tokenizer traces; correction/rework tokens; total tokens/cost |

**Unverified:** missing measures above were not assigned zero and are not
implied by a correct final diff. They must be captured per trial before any
end-to-end efficiency or newcomer-explainability claim.

| Cohort | Mean precision | Mean recall | Median output | Median fallback | Median one-query net proxy | Approx. bytes/4 |
|---|---:|---:|---:|---:|---:|---:|
| C0 — `rg`/`git grep` | 0.728 | 0.969 | 717 B | 0 B | 960 B | 240 |
| C1 — Graft CLI | 0.479 | 0.748 | 3,140 B | 51 B | 3,363 B | 841 |
| C2 — Graft MCP | 0.479 | 0.748 | 2,020 B | 51 B | 6,762 B | 1,691 |

**Observed:** relative to C0, C1's median proxy was 250% larger and C2's 605%
larger, while both had 0.221 lower absolute mean recall. C0 accumulated 21
file-level false positives and one false negative across query medians; C1 and
C2 each accumulated 55 false positives and 14 false negatives.

Adding the same relevant-source verification bytes to all cohorts gives median
proxies of 2,964 B (C0), 4,758 B (C1), and 8,535 B (C2). In that sensitivity
case, C1 is still 61% and C2 188% larger than C0.

## Results by repository

| Repository | Cohort | Mean precision | Mean recall | Median net proxy |
|---|---|---:|---:|---:|
| Generated | C0 | 0.896 | 1.000 | 923 B |
| Generated | C1 | 0.575 | 0.825 | 5,111 B |
| Generated | C2 | 0.575 | 0.825 | 8,274 B |
| Adversarial Python | C0 | 0.600 | 1.000 | 592 B |
| Adversarial Python | C1 | 0.271 | 0.688 | 3,096 B |
| Adversarial Python | C2 | 0.271 | 0.688 | 6,762 B |
| Mixed language | C0 | 0.708 | 1.000 | 819 B |
| Mixed language | C1 | 0.667 | 0.812 | 1,997 B |
| Mixed language | C2 | 0.667 | 0.812 | 5,955 B |
| OSS template | C0 | 0.708 | 0.875 | 1,562 B |
| OSS template | C1 | 0.403 | 0.667 | 8,646 B |
| OSS template | C2 | 0.403 | 0.667 | 12,260 B |

## Task-level interpretation

The `skeleton`, `callers`, indexed `grep`, and `blast` results below are upstream
capability probes. They are not v2 adapter commands. V2 exposes only `build`,
`check`, and bounded `ask` because the broader surface did not earn promotion.

### Where F1 helped

- **Observed:** `skeleton` identified the generated domain API file with
  precision/recall 1.0/1.0.
- **Observed:** one mixed-fixture static caller result matched C0's file score
  at precision 0.667 and recall 1.0.
- **Observed:** returned source spans were useful first-navigation pointers.
- **Observed:** all outputs were byte-stable across the three repetitions.

### Where F1 failed or added noise

- Duplicate `normalize` callers: recall 0.0; both real caller files missed.
- Exhaustive-looking indexed `grep direnv`: one of six OSS oracle files found;
  `git grep` found all six.
- Mixed cross-language flow: `routes.json` absent from all three relevant
  queries, including the query asking for every reference.
- Source-versus-wheel diagnosis: `pyproject.toml` missed; only installed-wheel
  execution established the failure.
- Generated failure path: one of two oracle files found and seven unrelated
  harness files added (precision 0.125, recall 0.5).
- Generated impact: the package re-export in `__init__.py` was missed.

**Inferred:** Graft can be useful when a location is unknown but the relationship
is statically supported and symbol identity is unambiguous. It is not safe as the
sole sensor for dynamic Python, configuration, packaging, duplicate symbols,
documentation, hidden paths, or exhaustive impact.

## MCP fixed context

**Observed:** all 48 MCP calls were operational. Initialize plus `tools/list`
was 4,557 bytes for every fresh server. C2 returned exactly the same file sets
and precision/recall as C1. Its smaller median result body did not offset the
fixed schema/instruction payload.

**Inferred:** a persistent server could amortize discovery bytes, while a model
client could re-inject schemas on many turns. Neither behavior was measured.
MCP demonstrated transport convenience, not better retrieval. The project-owned
v2 profile therefore removes it.

## On-demand evaluation context

**Observed:** the formal Graft evaluator role requires both
`prompts/evaluate-graft.md` and `prompts/PROMPT_CONTRACT.md`. Together they are
9,995 characters, or 2,499 character/4 proxy tokens. That on-demand workflow
context was not added to the deterministic per-query proxy because no model or
repository prompt loader participated in that benchmark; it is nevertheless a
real cost when a human launches the full evaluation protocol. It applies to the
evaluation workflow, not to every ordinary F1 query.

**Unverified:** actual client tokenization, caching, and repeated prompt loading
were not observed. This prompt proxy cannot be added to or subtracted from billed
model tokens.

## Build, refresh, and storage cost

| Repository | Median cold build | Median warm build | Graph files | Graph bytes |
|---|---:|---:|---:|---:|
| Generated | 0.713 s | 0.297 s | 43 | 1,412,371 |
| Adversarial Python | 0.311 s | 0.304 s | 26 | 122,698 |
| Mixed language | 0.279 s | 0.251 s | 17 | 46,255 |
| OSS template | 0.318 s | 0.277 s | 13 | 112,661 |

All 24 cold/warm builds exited zero. Direct-child peak RSS was not captured
reliably before process exit, and descendant/native memory is **Unverified**.
The optional runtime itself was observed at roughly 375 MiB in the isolated
install track.

**Observed freshness controls:** a clean graph passed; an unstaged Python edit,
JavaScript rename, and test deletion were reported stale; subsequent queries
refreshed the graph and reflected each change. The explainability fixture also
covered a staged move and an untracked Python addition.

**Observed in exact v2 matrices:** concurrent-use locking, failed publication,
prior-graph preservation, and seeded real-package lifecycle/freshness behavior
were exercised. **Unverified:** a real-package interruption, branch switches,
very large repositories, parser crashes outside seeded cases, and shared graph
reuse across worktrees.

## Correctness and accepted-change boundary

Executable repository controls passed during benchmark setup:

| Repository | Oracle result |
|---|---|
| Generated project | 125 tests passed |
| Adversarial Python fixture | 3 tests passed |
| Mixed fixture | 2 tests passed |
| OSS template hooks | 7 passed, 1 skipped; Python 3.12 despite declared 3.13, therefore diagnostic only |

The held-out agent task required every `normalize` implementation to collapse
runs of Unicode whitespace while preserving each implementation's case policy.
The oracle stayed outside all six fresh clones.

The C1 task wrapper exposed upstream `grep`, `callers`, and `ask`; current v2 F1
exposes only `build`, `check`, and bounded `ask`. The following C1 row is thus an
upstream-capability trial, not evidence that the final adapter preserves the
same accepted-task result.

| Cohort | Accepted | Repository tests | Agent-attributable unrelated edits | Required source/search fallback |
|---|---:|---:|---:|---:|
| C0 | 3/3 | 3/3 | 0 | ordinary tooling by definition |
| C1 | 3/3 | 3/3 | 0 | 3/3 |

**Observed:** C0 changed eight task files across the three runs (mean 2.67);
research C1 changed nine (mean 3.0). C1 setup had already modified `.gitignore`
before each agent began, so literal final-worktree scope was broader in C1 even
though no task agent caused that mutation. This setup overhead is retained
rather than silently excluded.

**Observed:** the frozen final-adapter condition then failed its first
prerequisite build because real Graft omitted tracked `.hidden/visible.py`.
The adapter rejected the incomplete graph, published nothing, and the task agent
did not start. Two planned repetitions were not run under the preregistered stop
rule.

**Unverified:** accepted-task correctness/scope for current narrowed F1; no
final-F1 task run exists. Three runs per earlier cohort on one small task are not
a population estimate. Exact tokens, file opens, time, complete review/rework,
and causal productivity remain unavailable. Agent self-reported token savings
are rejected as non-independent evidence.

## Routing rule retained in v2

| Task shape | Required route |
|---|---|
| Likely location or orientation | F1 may provide a first pointer; read exact source next |
| Known static symbol/reference | Bounded structural operation may assist; verify ambiguity and scope |
| Every/all/none/complete | Start with `rg`/`git grep` across the declared scope plus executable verification |
| Dynamic/configuration/package behavior | Inspect configuration/source and run runtime/wheel tests |
| Design rationale/authority | Human-owned contracts, ADRs, and decisions; never infer from graph shape alone |

## Promotion result

The suggested promotion target required no correctness/acceptance/review
regression and at least 15% lower median total context for representative
multi-file tasks, or clearly superior recall/precision at equivalent cost.

**Observed:** the broader research C1 did not meet either measured direction.
Final F1 was narrowed further; its frozen trial stopped at the first fail-closed
build because real Graft omitted a tracked hidden source, so it has no accepted-
task result. **Recommended:** keep F0 as default; retain F1 only as a bounded
optional experiment; remove F2 from the project profile. Do not use Graft's own
"tokens saved" estimate as evidence of total task cost.

## Reproducibility

Primary evidence currently exists in the ignored audit workspace and is planned
for the final checksummed raw-evidence archive. Archive creation and its final
checksum ledger remain **Unverified**:

- `team/context_benchmark/PRE_REGISTRATION.md`
- `team/context_benchmark/CONTEXT_BENCHMARK_RESULTS.json`
- `team/context_benchmark/results/raw/`
- `team/context_benchmark/oracles/`
- `team/context_benchmark/run_benchmark.py`
- `team/actual_trials/ACTUAL_AGENT_TRIAL_RESULTS.json`
- `team/actual_trials/ACTUAL_AGENT_TRIAL_REPORT.md`
- `evidence/v2/final-adapter-trials/FINAL_ADAPTER_TRIAL_RESULTS.json`
- `evidence/v2/final-adapter-trials/FINAL_ADAPTER_TRIAL_REPORT.md`

Recorded SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| Preregistration | `83ed278a19f2ad3bf77e56ffcc375831aabd48cd91480f6f86217613fa96840c` |
| Machine-readable results | `f2d0a4a38b6d95a270fcf4c1acc62846d1249ca35c124b09c15f27f4e5a23c62` |
| Benchmark runner | `457ccb2ed0a7265e2458d1bef7403f7a7946ab1fe80fcaa54610c8d8b66ad7b1` |
| Final-adapter trial results | `b77ad0c44b4b162528751154ce30295dd6625a8fc466d7c9b29b00e96d9d6ce6` |
| Final-adapter trial report | `015b80b3ed40fe4778b2a477bfd5ec486ca1efacce28f26f6da6407478858d1b` |
| Final-adapter trial ledger | `abf5206a7452b4cb0ac889517d9abceb97cdafea9aa500359ccd8f1bef8d2fb9` |
