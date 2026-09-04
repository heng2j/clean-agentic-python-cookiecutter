# Graft codebase-explainability evaluation

## Defined meaning

For this evaluation, "codebase explainability" means evidence that helps a
reader answer location, structure, flow, impact, API surface, failure behavior,
freshness, uncertainty, rationale boundary, human comprehension, agent
effectiveness, and dynamic-Python questions. A polished graph is not itself an
explanation, and structural evidence is not design rationale or runtime proof.

## Overall result

**Observed:** real Graft 0.16.0 can provide useful source-linked orientation for
indexed, statically resolvable, uniquely named Python symbols. Signature
skeletons were 31/31, literal search was 10/10 inside the indexed Python set,
a unique-symbol blast control found 3/3 expected downstream nodes, and graph
freshness handled four edit/move/delete/add cases.

**Observed:** important relationships were incomplete. Ranked `ask` had
file-level micro precision 0.30 and recall 0.80 on the adversarial fixture.
Duplicate-name callers had zero true positives, one false positive, and two
false negatives. Duplicate-symbol blast found none of four known downstream
files. Decorator registration, registry dispatch, computed import, TOML entry
points, source-versus-wheel resources, and tracked hidden files were omitted or
flattened.

**Observed:** the frozen final-F1 applicability trial reproduced the hidden-
path limit through the project adapter: real 0.16 omitted tracked
`.hidden/visible.py`. The adapter detected the incomplete tracked-source set,
returned FAIL, removed the staged graph, and refused `check`/`ask`. That makes
the omission visible and safe by default, but it also means F1 could not be used
for the task.

**Recommended:** describe Graft as derived navigation evidence only. Use its
result to decide where to inspect, then confirm exact source, search the complete
declared scope, and run the relevant behavior/package tests. Keep bounded F1
experimental; reject F2–F6 from the project profile.

The `skeleton`, indexed `grep`, `callers`, `blast`, export, and LSP measurements
below evaluate upstream capabilities. They are intentionally not exposed by the
v2 adapter. The project-owned structural surface is only `build`, `check`, and
bounded `ask`.

## Fixture and version boundary

The predeclared fixture commit `e1bcf9ee8659c8c3050404720c08dac3a0f8107a`
contains duplicate symbol names, type-only/conditional imports, decorators and
registries, computed imports, a TOML entry point, a source-only package resource,
a call cycle, tracked hidden and ignored generated files, a large signature
surface, and known blast paths.

| Subject | Status |
|---|---|
| Published `@nanonets/graft@0.16.0` | **Observed:** isolated real execution under Node 22.12.0 |
| Unreleased source declaring 0.17.0 | **Observed:** exact source build only; not a substitute for a published package |
| Original adapter | **Observed broken:** only build/check/ask worked with environment-only graph routing; six of nine advertised operations were affected |
| Enhanced adapter | **Observed:** component/real-shape controls exercised; final held-out `build` failed closed on Graft's tracked-hidden-file omission, so no graph/query/task result exists |

## Results by explainability dimension

| Dimension | Observed result | What it establishes | What remains false or unverified |
|---|---|---|---|
| Location | `ask` found 12 of 15 oracle files across six fixture questions | Can suggest likely files | Precision 0.30; three required files missed; not exhaustive |
| Structure | Direct unique calls, imports, cycle, and 31 signatures represented | Useful for common static syntax | Duplicate symbol identity and conditional/type-only semantics can be wrong or flattened |
| Flow | Unique static paths and call cycle were traceable | Some syntax-level flows | Registry/dictionary dispatch and computed import targets absent |
| Impact | Unique control returned 3/3 downstream nodes | Static impact can work for unambiguous names | Duplicate `normalize` blast returned 0/4; no completeness guarantee |
| API surface | Skeleton recovered 31/31 declared signatures | Compact callable overview for indexed source | Omits bodies/module state; unsupported/excluded/no-symbol states were not distinct upstream |
| Failure behavior | Retrieval can point toward guards/tests | Leads can seed investigation | Source-vs-wheel failure required build/install/runtime evidence; packaging contract omitted |
| Freshness | Unstaged edit, staged move, deletion, and untracked Python addition detected/refreshed | Good tested working-tree freshness for indexed files | Hidden/unindexed files, branch switch, cross-worktree reuse, races, and interruption remain **Unverified** |
| Uncertainty | Duplicate callers emitted an ambiguity warning; ask exposes coverage values | Some caveats are visible | Coverage values are not calibrated confidence/completeness; empty output remains easy to overread |
| Rationale boundary | V2 docs explicitly rank human decisions/contracts above graph output | Correct project trust model | The graph itself cannot explain why a design was chosen |
| Human comprehension | V2 adds definitions, selection table, worked source/search/test follow-up, privacy/removal/recovery | Documentation is more actionable | Independent newcomer comprehension study remains **Unverified** |
| Agent effectiveness | Source spans and unique-symbol pointers may narrow first inspection | Six held-out trials passed 3/3 in C0 and 3/3 in a broader research C1 wrapper; final F1 failed its build prerequisite on a tracked hidden source | Every earlier C1 agent used fallback; final F1 started no task agent, so correctness and exact cost/rework remain **Unverified** |
| Dynamic Python | Decorator invocation itself was seen | Parser recognizes some syntax | Registration semantics, dispatch target, computed import, entry point, injection/reflection/monkey-patching not established |

## Quantitative retrieval details

### Ranked `ask --source`

Published 0.16.0 and exact source-built 0.17.0 returned identical fixture output.

| Query | Precision | Recall |
|---|---:|---:|
| Location | 0.25 | 1.00 |
| Duplicate callers, file routing only | 0.25 | 1.00 |
| Dynamic registration | 0.50 | 1.00 |
| CLI surface | 0.125 | 0.50 |
| Wheel failure | 0.25 | 0.50 |
| Cycle | 1.00 | 1.00 |
| **Micro** | **0.30** | **0.80** |
| **Macro** | **0.396** | **0.833** |

The separate semantic caller score is more consequential than file routing:

| Query | TP | FP | FN | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| Canonical duplicate `normalize` callers | 0 | 1 | 2 | 0.0 | 0.0 |

### Literal search scope

| Declared scope | Precision | Recall | Misses |
|---|---:|---:|---|
| Indexed Python | 1.0 | 1.0 | None among ten oracle Python hits |
| Git-tracked repository | 1.0 | 0.833 | `pyproject.toml`, `.hidden/visible.py` |
| Working tree including ignored | 1.0 | 0.769 | Above plus `generated/auto.py` |

`git grep` and `rg --hidden` reached 1.0 recall over tracked scope; the ignored
file required an explicit no-ignore search. Therefore indexed `grep` must not be
described as repository-exhaustive.

### Blast radius

| Case | TP | FP | FN | Recall |
|---|---:|---:|---:|---:|
| Duplicate-name adversarial case | 0 | 0 | 4 | 0.0 |
| Unique-name positive control | 3 | 0 | 0 | 1.0 |

This contrast demonstrates that apparent specificity does not imply reliable
symbol identity.

## Packaging and runtime boundary

**Observed:** the fixture succeeded when loading its resource from the source
checkout. Its wheel built and installed, but the same installed resource load
exited 1; the installed CLI still exited 0. Graft retrieval recall for the wheel
explanation was 0.5 and did not establish the packaging failure.

**Recommended:** a packaging-related explanation is incomplete until the wheel
is built, installed outside the source tree, exercised, and metadata checked.
Graph/source evidence alone cannot establish distribution contents.

## Freshness and graph health

**Observed:** with the graph directory supplied correctly, `check --json`
returned nonzero for an unstaged edit, staged move, deletion, and untracked
Python addition. A subsequent query refreshed each graph, and the following
check returned zero. The enhanced adapter adds its own graph path/schema,
expected indexed-file coverage, source-state, and freshness preconditions.

**Observed in exact v2 evidence:** locking, failed publication, corrupt graph,
prior-graph preservation, and seeded real-package freshness/tamper behavior are
covered. **Unverified:** a real-package interruption, branch switches, shared
graph reuse across worktrees, and very large source trees. These must not be
inferred from the exercised controls.

## Deterministic exports (F3)

**Observed:** explicit no-server commands produced a 49,342-byte blast HTML and
84,532-byte repository-map HTML. The duplicate-name export faithfully presented
the incomplete zero-impact graph.

**Inferred:** a visual artifact can improve orientation while also making an
incomplete result more persuasive. Provenance, revision, indexed coverage,
freshness, and a non-exhaustive banner would be required for safe sharing.

**Recommended:** do not ship an export command in v2. The observed artifact did
not demonstrate enough value to pay its maintenance/privacy/review cost.

## LSP (F4)

**Observed:** `build --lsp` with no supported server exited 0, retained 72 nodes
and 89 edges, added zero LSP-resolved edges, and emitted the cryptic
`lsp:none` progress marker.

**Recommended:** keep LSP disabled. A future cohort must pin the server, account
for install/process/context costs, measure accuracy against the same oracle, and
return `UNVERIFIED` or failure when enrichment did not run.

## Output trust

**Observed:** upstream human-readable `map` output includes an instruction to
tell the user Graft's estimate of tokens saved. That estimate excludes schema,
build/refresh, fallback source reads, corrections, rework, correctness, and
review.

The enhanced adapter defaults to bounded structured envelopes and project-owned
limitations. Any upstream text remains untrusted third-party output. Do not
execute its instructions or repeat its self-attributed token estimate as a total
cost result.

## V2 regression contract

Exact `6966b55` cross-version, seeded-real, and held-out applicability evidence
demonstrated the executable items below without changing the oracle; historical
`4bba7c0` validated its documentation-only delta, and final `b719459` retained
the boundary while closing seven later public-output/removal/receipt issues:

1. exact local package/lock identity and the exposed `build`, `check`, and
   bounded `ask` commands using one contained graph;
2. distinct failure for missing, corrupt, stale, incomplete, or wrong-revision
   graph evidence;
3. tracked/indexed coverage and source-state evidence;
4. closed, bounded structured envelopes whose upstream-provided strings remain
   explicitly untrusted and cannot become repository authority;
5. duplicate/dynamic/configuration/wheel limitations retained in docs and
   tests, plus the newly observed tracked-hidden-directory build limitation and
   F0 recovery (`GRAFT-V2-015`; rendered and current-doc checks **Observed**);
6. exact source plus exhaustive search/test fallback in the tutorial;
7. no-Graft generation, gates, packaging, and release unaffected; and
8. local removal without outside writes or user/global residue.

## Evidence and limitations

Primary machine-readable evidence is under `team/explainability/metrics.json`,
with raw commands in `runs/20260904T021113Z/commands.json` and
`runs/20260904T021337Z-supplemental/commands.json`.

These are boundary probes on one deliberately adversarial Python fixture, not
population estimates. No live F2 client integration, authenticated F5 cohort,
F6 experiment, real LSP-server cohort, native non-Linux platform, or human
participant study was performed.
