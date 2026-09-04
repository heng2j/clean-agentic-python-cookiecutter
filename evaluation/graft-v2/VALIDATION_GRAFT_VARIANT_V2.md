# Validation of the enhanced Graft variant

> Status: **FINAL LOCAL SOURCE AND FIRST HOSTED CI VALIDATED; REPORT PUBLICATION
> RUN PENDING**. Exact source
> `b719459` passed template and generated-project release validation on Python
> 3.12 and 3.13, focused late-red-team regressions, and a seeded real-Graft
> lifecycle/removal control. Two fresh connected installs failed inside npm and
> promoted no runtime; connected installation and provenance remain
> `UNVERIFIED`. Remote review commit `4dc3603` has the identical source tree and
> its first hosted 3.12/3.13 matrix passed. The final narrowed-F1 task outcome
> also remains `UNVERIFIED`.
> No pending or unverified row is a pass.

## Identity

| Field | Value | Status |
|---|---|---|
| Candidate branch | `audit/experimental-graft-variant-v2` | **Observed locally** |
| Final local candidate | `b719459a051a60d4af1e4fa30b3c32277fa97b8c` (tree `35819081108685c24f47ba5251ec7e18004b0016`) | **Observed:** exact local template/render/release/late-red-team/seeded-real boundary |
| First remote review commit | `4dc3603a6360111a1f9619c3e409d67755cff710` (same tree `35819081108685c24f47ba5251ec7e18004b0016`) | **Observed hosted:** Actions run `33873556873` passed both jobs |
| Predecessor implementation checkpoint | `6966b5500eaa22d17f0526dbd051437aadb43255` (tree `1203a71bd165251b2618fc669c4f027bd86e0cf1`) | **Historical observed checkpoint; superseded by later findings** |
| Audited base | `ab3e06f6a402a22f51d8447101f245eab258b8e6` | **Observed** |
| Graft | `@nanonets/graft@0.16.0` | **Observed selected and seeded-tree exercised**; public connected install/provenance **Unverified** |
| Graft upstream | `aa1e2bb0f6326068ac64886da1e67fa25a7804de` | **Observed mapping** |
| OS / architecture | Python 3.12/3.13 runs: Linux 6.18.35 x86_64 | **Observed** for those runs; other native platforms **Unverified** |
| Shell | Bash 5.2.21 | **Observed** |
| Python 3.12 / 3.13 | CPython 3.12.13 / 3.13.14 | **Observed** |
| Node / npm / uv / Git | No-Graft: uv 0.11.33 and Git 2.51.1; Node absent from 3.13 gate `PATH`. Seeded F1: Node 22.12.0, npm 10.9.0, Git-bound source | **Observed**; public connected npm install **Unverified** |
| Agent/client/model version | Client did not expose a stable version identifier to the evaluator | **Unverified**; original checkpoint omitted this field |

## Final `b719459` local checkpoint

The sections below retain predecessor checkpoints as chronology. This section
is the controlling local result.

| Boundary | Observed result | Status |
|---|---|---|
| Template | `uv lock --check`, official render, 99 tests | **PASS** |
| Generated Python 3.12 | Full release profile; 243 tests; package/external-wheel checks | **PASS** |
| Generated Python 3.13 | Full release profile; 243 tests; package/external-wheel checks | **PASS** |
| Quality | Product 94.97%; harness 83.25%; CRAP 10.10; 3/3 code and 3/3 specification mutants killed | **PASS** at named sensor boundaries |
| Adapter | 122 focused tests, Ruff, formatting, Pyrefly | **PASS** |
| README/docs | Expanded no-Graft default, short opt-in/removal, authority and hidden-path boundaries; canonical Markdown/docs audits | **PASS** |
| Seven late findings | 2 P0 and 5 P1 regressions covering output, deletion, receipt, race, and Unicode publication cases | **PASS** for reproduced cases |
| Fresh connected install | Two npm 10.9.0 attempts returned adapter `FAIL`; no runtime promoted | **UNVERIFIED** capability/provenance |
| Seeded real 0.16 runtime | Doctor/build/check/documented ask; 569 nodes/1,783 edges | **PASS** compatibility control; not install/provenance |
| Real cleanup | 7,522 owned, 0 unknown; apply and second check `complete: true`; Git clean | **PASS** |
| Hosted Actions | Run `33873556873`; `render (3.12)` and `render (3.13)` | **PASS** for the exact implementation tree; report-only follow-up pending |

The generated release ledgers are under the final evidence bundle. The exact
source hashes are recorded in `EVALUATION_RESULTS_SUMMARY.json`. The first
noncanonical direct Markdown invocation omitted the repository's documented
rule exclusions and is not used as release evidence; the canonical release
command passed.

The final seeded real-package control recorded all eight expected exit paths,
returned the worktree to clean with runtime and state absent, and verified its
own file ledger. Its result SHA-256 is
`f9656d29c2fbf3a771d5e772fe4479e7868efd51545499ae76ab525eca0afae6`;
the ledger SHA-256 is
`e27d8a78cf6857fd75a534293e9d958f20f0df205fe99b68d6b00e54b4aa5761`.
This remains a seeded real-package compatibility/removal control, not an
installation or source-to-package provenance pass.

## Required matrix

| Area | Required result | Final evidence | Status |
|---|---|---|---|
| Template | `uv lock --check`; locked sync; full template tests; build; Twine | Exact final source `b719459` passed lock/sync, 99 tests, build, and Twine | **Observed final-source pass** |
| Python 3.12 render | Official default render; locked sync; fast/full/hardening/release | Exact `b719459` render passed release with 243 tests, all subordinate profiles, packaging, and a clean tracked tree | **Observed final-source pass** |
| Python 3.13 render | Official default render; locked sync; fast/full/hardening/release | Exact `b719459` render passed release with 243 tests, all subordinate profiles, packaging, and a clean tracked tree | **Observed final-source pass** |
| Non-default render | Supported license/Actions options and package build | `6966b55` Apache-2.0 / Actions-off / Python-3.13 option render passed option checks, lock, offline sync, build, and Twine | **Observed on Python 3.12 host** |
| No Graft | Generation, sync, tests, packaging, release without Node/Graft | Exact `b719459` 3.12/3.13 release profiles passed; Graft is absent from Python dependencies and mandatory gates | **Observed final-source pass** |
| Adapter unit | Full focused suite, Ruff, Pyrefly, branch coverage | `b719459` release passed the complete 243-test generated suite on both versions; the focused adapter suite passed 122 tests plus Ruff and Pyrefly | **Observed final-source implementation** |
| Adapter complexity / CRAP | Ruff C901 for `tools/graft_adapter.py`; adapter-targeted callable CRAP using its own coverage | No committed adapter-targeting CRAP sensor; ordinary CleanAI CRAP scans product `source_root` only | **Unverified**; do not infer from release/full |
| Real Graft | Pure missing doctor; doctor; build; check; ask with/without source; empty/structural/lexical modes; removal | Exact `6966b55`: missing doctor behaved as designed; seeded doctor/build/check, six ask modes, freshness/tamper rejection, removal, and post-removal F0 passed | **Observed seeded lifecycle; connected install and provenance Unverified** |
| Strict output | Malformed/extra/missing/non-finite fields; source span and code binding | Exact `6966b55` seeded build/check/six asks passed; malformed/injected cases passed in the cross-version 230-test suites | **Observed implementation** |
| Real file spans | Accept exact 0.16 file-node newline convention; reject invalid file/symbol spans; symbols remain within real lines | Exact `6966b55` real build passed with 540 nodes/1,689 edges; invalid-boundary regressions passed in both version suites | **Observed implementation** |
| Check projection | Exact reviewed 0.16 top/context/graph keys; reject injected extras; real and 517-item fake omit upstream prose/identifier strings, preserve count/hash/raw identity, and return fixed project status/reason plus booleans/counts/hashes under 4 KiB | Exact `6966b55` real check returned 3,644 B; focused long-parent/injection regressions passed | **Observed implementation** |
| Public path privacy/stability | Every successful public command uses project-relative managed paths and omits host executable paths; durable install/structural-command evidence retains full identity | `6966b55` doctor/check/remove selection passed 3/3; held-out build stdout/stderr/durable evidence had zero absolute-path markers | **Observed implementation** |
| Evidence status | Missing/unrun prerequisites are UNVERIFIED; invalid/unsafe requests and observed child failures are FAIL | Cross-version focused matrix passed; real missing doctor was UNVERIFIED and freshness/tamper failures were FAIL | **Observed implementation** |
| Doctor status | Missing/unsupported runtime is UNVERIFIED; unsafe state symlink and receipt/tool/version tamper are FAIL | Cross-version focused matrix passed; exact real missing and seeded-ready states behaved as specified | **Observed implementation** |
| Filesystem | Parent/leaf/nested symlink, hardlink, mode, ownership, traversal, ignored marker | Cross-version focused matrix passed | **Observed implementation**; arbitrary dependency writes need OS confinement |
| Identity | PATH conflict, manifest/lock/CLI/tree tamper, pre/post tool substitution | Cross-version focused matrix passed; exact seeded runtime identity was checked | **Observed local tamper controls**; source-to-dist provenance Unverified |
| npm version/config | Exact 10.9.0; reject 99.0.0; `/dev/null` user plus contained empty global config | Focused version-drift/config regressions passed; prior exact npm 10.9 probe passed | **Observed controls**; connected install Unverified |
| Install evidence truth | Failed npm records scripts authorized and npm attempted, never scripts executed without observation | Cross-version failing-install regression passed | **Observed implementation** |
| Environment | Arbitrary/common credentials absent; empty dotenv route; isolated state | 867 exact-`6966b55` samples included 42 visible Node records with neither synthetic sentinel nor proxy keys; sampled socket rows zero | **Observed sampling; exhaustive credential/network isolation Unverified** |
| Pre-commit transactions | Failed install/build, evidence-write/swap/staging failure preserves prior complete state | Cross-version focused fault-injection matrix passed | **Observed implementation**; real interruption Unverified |
| Post-commit cleanup | Partial old-backup cleanup keeps validated new runtime active and stale backup visible | Cross-version focused cleanup-fault regression passed | **Observed implementation** |
| Install residue | Staging/backup/quarantine are in-project, inventoried, removable; second check complete | Focused recovery matrix passed; exact seeded real removal was complete with 101 absence samples | **Observed implementation and seeded lifecycle**; connected-install crash residue Unverified |
| Process | Timeout, early pipe close, inherited signal mask, same-group descendant cleanup, selector failure | Cross-version focused process matrix passed; exact lifecycle sampled 867 observations | **Observed controls**; sampling is not containment proof |
| Detached process | Bounded wrapper return; document inability to contain new-session child | `PENDING` | **Unverified containment** |
| Freshness | Clean, staged, unstaged, rename/move/delete, branch/revision, untracked/source-marker cases | Exact real changed-source check/ask failed closed; cross-version focused matrix passed | **Observed implementation**; semantic completeness not implied |
| Project writes | Real build/check/ask creates no root `.ignore` or other out-of-state file | No `.ignore` or root `.graft`; final tracked tree restored | **Observed** for seeded lifecycle; arbitrary dependency writes remain outside OS confinement |
| Removal | Pure check; apply only validated roots; second check has `complete: true`, every removable target absent, and only declared retained inputs/inventory metadata | Seeded lifecycle: before-check incomplete, apply complete, after-check complete; all 101 post-command samples found managed state absent; empty adapter lock retained as declared | **Observed** for seeded runtime; connected-install cleanup and hostile detached process Unverified |
| Package | Wheel/sdist metadata and external wheel install/CLI/runtime smoke | Exact `b719459` template and 3.12/3.13 generated build, Twine, and external-wheel lifecycle passed | **Observed final-source pass** |
| Context/docs | Context budget, route/link checks, Markdown lint, generated docs audit | Exact `b719459` passed 99 root tests, official render, strict docs/context audits, and the canonical 76-file Markdown check | **Observed final-source pass** |
| Hidden-path recovery docs | Public route states real 0.16 omission, intentional FAIL/no graph, F0 fallback, and no move/untrack/weaken workaround | Exact `b719459` rendered regressions and final root/docs gates passed | **Observed final-source pass** |
| Public commands | No uncovered bare adapter interpreter; locked uv command works without venv/direnv activation | Covered by generated tests and release on both versions; a separate novice comprehension exercise remains `PENDING` | **Observed** for executable regression; independent newcomer comprehension **Unverified** |
| Evaluation | Same explainability fixture/task bank; no changed oracle | Exact `6966b55` replay retained the frozen fixture/task/oracle and hit the same hidden-source stop condition before a task agent | **Observed applicability replay**; accepted-task outcome Unverified |
| Final F1 accepted-task trial | Repeat the frozen Unicode-whitespace task through current `build`/`check`/`ask`; do not use removed `grep`/`callers` adapter commands | Exact `6966b55` prerequisite build exited 2/FAIL after 2.672028 s because real 0.16 omitted tracked `.hidden/visible.py`; no graph, query, agent, or task change; repetitions 2–3 not run under the preregistered stop rule | **Observed applicability failure; accepted-task outcome Unverified** |
| Workflow triggers | Push filter includes durable experimental and review branches | Source inspection and hosted PR run `33873556873` | **Observed execution** |
| Hosted Actions | Review-branch run on 3.12/3.13 | Both jobs in run `33873556873` passed every step | **Observed first publication pass**; report-only follow-up pending |

**Observed:** the canonical Markdown command is
`rumdl check --disable MD013,MD041,MD071 .`; it passed 76 files at `b719459`.
A noncanonical one-file invocation that omitted those policy suppressions
reported MD071. That diagnostic is expected under a different policy and is not
classified as a failure of the documented gate.

## Historical documentation-only checkpoint

**Observed:** predecessor source `4bba7c0` (tree `8aaa45d4`) passed 14/14
recorded expectations: commit/tree/clean preflight, lock, offline 3.12 sync, 99
root tests, official render, generated offline sync, the canonical 76-file
Markdown policy, strict docs/context audits, exact wording assertion, and final
source-diff/clean checks.

Evidence directory:
`evidence/v2/documentation-followup/final-4bba7c0/`. The summary SHA-256 is
`cf7085eaa0451300d07d22626f3d6cd0b4f1915bedea0bebfc10adb37c4daf70`;
the artifact-checksum ledger SHA-256 is
`f5e5d1362d94a5d6af166cfdb144772f22fa6e968589d8b165423392c26413ed`.
This checkpoint validates only the documentation delta from `6966b55`. Raw
records retain absolute local paths; dependency setup used uv offline, but
network access was not observed at the operating-system boundary.

## Observed implementation-commit Python 3.12 checkpoint

**Observed:** a clean `git archive` snapshot of implementation commit
`6966b5500eaa22d17f0526dbd051437aadb43255` ran from
`2026-09-04T05:23:14Z` through `2026-09-04T05:26:58Z` on Linux 6.18.35
x86_64 with CPython 3.12.13, uv 0.11.33, and Git 2.51.1. All 42 recorded
commands returned their expected exit.

| Measure | Observed result |
|---|---:|
| Template tests | 99 passed |
| Generated tests | 230 passed |
| Public profiles | fast, full, hardening, release: all passed |
| Product branch coverage | 94.97% (90% floor) |
| Harness branch coverage | 82.78% (70% floor) |
| Worst local CRAP approximation | 10.10 (30 budget) |
| Curated code mutants | 3/3 killed |
| Curated specification mutants | 3/3 killed |
| Public-envelope focused selection | 3/3 passed |

**Observed:** template lock/sync/build/Twine, official default render, generated
lock/sync, all four gauntlets, generated build/Twine, and isolated external-
wheel install/import/CLI/dependency/uninstall passed. The alternate
Apache-2.0, Actions-off, Python-3.13-option render passed option checks, lock,
offline sync, build, and Twine on the 3.12 host. The generated Git tree remained
`26a0e7cbdb61f61bfd87f17b6f65863f6ffaf519`. With Graft absent, `doctor`
exited 2 with status `UNVERIFIED` and wrote no managed state.

Evidence directory: `evidence/v2/python312/final-6966b55/`. The template-copy
hash-list SHA-256 is
`39bd52c077bab56916ed2d2b658a0ce197d49e4fc81a73f934ec316853f295ee`;
the summary JSON SHA-256 is
`afb6ff8eb969244fdba769c59c52807edfc2ff6cb508dcec97f445262c876107`;
the environment record SHA-256 is
`203f2b77ebda37dd0c01b7f023f8e12c8dd204eb88acfd73992c85a6a0306a80`.

**Observed boundary:** validation used `env -i` with a fixed non-secret
allowlist. uv ran offline from a pre-populated cache; other processes were not
OS-network-blocked or packet-monitored. Per-command records include most of the
charter fields, but do not record per-command start/end timestamps or ignored-
file deltas; aggregate state checks cover the latter. Command-record
completeness is therefore **Unverified**. This checkpoint binds implementation
behavior to `6966b55`, not the
documentation-only child or eventual report-bearing distribution bytes.

## Observed implementation-commit Python 3.13 checkpoint

**Observed:** a clean `git archive` snapshot of implementation commit
`6966b5500eaa22d17f0526dbd051437aadb43255` ran from
`2026-09-04T05:23:46Z` through `2026-09-04T05:27:49Z` on Linux 6.18.35
x86_64 with CPython 3.13.14, uv 0.11.33, Cookiecutter 2.7.1, and Git 2.51.1.
All 30 recorded commands returned their expected exit; there were zero
unexpected exits.

| Measure | Observed result |
|---|---:|
| Template tests | 99 passed |
| Generated fast profile | 230 passed |
| Generated full profile | 230 passed |
| Generated hardening profile | 230 passed |
| Generated release profile | 230 passed |
| Product branch coverage | 94.97% (90% floor) |
| Harness branch coverage | 82.78% (70% floor) |
| Worst local CRAP approximation | 10.10 (30 budget) |
| Curated code mutants | 3/3 killed |
| Curated specification mutants | 3/3 killed |

**Observed:** template and generated wheel/sdist build, Twine checks, official
render, locked sync, all four profiles, and isolated external-wheel
install/import/CLI/uninstall passed. The generated
tracked tree and index were byte-identical before and after validation, with
zero final status lines. With Node deliberately absent from the gate `PATH`,
`doctor` and `check` exited 2 and reported `UNVERIFIED`; `remove --check`
reported `PASS`; all three public documents were below 4,096 bytes with no host
project path. All four ordinary profiles remained green.

Evidence directory: `evidence/v2/python313/final-6966b55/`. The commit tree is
`1203a71bd165251b2618fc669c4f027bd86e0cf1`; the authored-source manifest
SHA-256 is
`3f1eba7c792cfc561ed18538cf199ff7f3bc0c831da86e41775b890682f3c132`;
the command-ledger SHA-256 is
`bbe6052636859edc96fb376bde9a744ee9b427b3fa68308615cae0072e2d9551`;
the runner SHA-256 is
`501d0c24799c9b8f00438c0b2200b9f6ea5a7852b05e810739b9bc63c640b1e2`;
the report and result JSON SHA-256 values are
`e84b2a99a8cdb89d775f830ba7dc4e4709e760dad6b8a27a987a896f01f6b396`
and
`aa4f78055d1c1cad4b050c4013305faa27c3babd2fc9232dece9fab48c0aa0a3`.

**Unverified:** this checkpoint did not exercise installed Graft, npm network
behavior, native macOS/Windows, hosted Actions, or an external provider. Python
3.12 is reported independently above at the same implementation source. This
snapshot excluded the still-changing untracked evaluation reports; it does not
validate the documentation-only child or eventual report-bearing bytes.

## Observed final-adapter applicability trial

**Observed:** the preregistered final-F1 task trial used adapter commit
`6966b55`, real Graft 0.16.0, Node 22.12.0, npm 10.9.0, and the unchanged
Unicode-whitespace fixture. Its first prerequisite `build` returned exit 2 and
`FAIL` in 2.672028 seconds because Graft omitted the tracked Python file
`.hidden/visible.py`. The adapter detected the tracked-source mismatch, removed
the staged graph, and published no graph. `check`, `ask`, the task agent, task
edits, acceptance, and repository tests did not run. Repetitions 2 and 3 were
not run under the preregistered stop rule.

**Observed:** build stdout was 254 bytes, stderr was empty, and build stdout,
stderr, and durable adapter evidence contained zero absolute-path markers. The
only reported source path was project-relative `.hidden/visible.py`.

**Observed:** this is an applicability failure and a successful fail-closed
postcondition, not a task-agent correctness failure. **Unverified:** accepted-
task correctness, scope, fallback reads, interventions, corrections, rework,
files opened, time, model tokens, and cost for final F1.

Evidence directory: `evidence/v2/final-adapter-trials/final-6966b55/`, with the
updated top-level report and result in `evidence/v2/final-adapter-trials/`. The
report SHA-256 is
`015b80b3ed40fe4778b2a477bfd5ec486ca1efacce28f26f6da6407478858d1b`;
the result JSON SHA-256 is
`b77ad0c44b4b162528751154ce30295dd6625a8fc466d7c9b29b00e96d9d6ce6`.
The evidence ledger covers 29 entries; its SHA-256 is
`abf5206a7452b4cb0ac889517d9abceb97cdafea9aa500359ccd8f1bef8d2fb9`.
The exact-candidate submanifest SHA-256 is
`0678c519dba85d7111404b4b991a72bb5e8b0103775c40a59f081ab296ddfe73`.
**Recommended:** preserve exact tracked-
source coverage and keep F1 experimental; do not weaken the fixture or adapter
to manufacture a runnable trial.

## Observed real-Graft lifecycle checkpoint

**Observed:** the real-package track rendered exact implementation commit
`6966b55` with Cookiecutter 2.7.1 into a 305-character project path. Node
22.12.0, npm 10.9.0, and Graft 0.16.0 identities were checked. The adapter
SHA-256 was
`8b8ce3c39a8f6994b20dcf9b9148718f87a261195cb5dce5c46c0e9792eb7b94`.
A runtime seeded from the exact previously fetched package tree was explicitly
labeled `FIXTURE_READY_NOT_INSTALL_PASS`; its package build provenance remains
`UNVERIFIED`.

| Capability | Observed result |
|---|---|
| Missing-runtime doctor | Exit 2 / `UNVERIFIED`; pure tree check passed |
| Connected `install --apply` | Not rerun at `6966b55`; prior exact adapter attempt exited 2/FAIL after 70.588 s with npm's generic "Exit handler never called" error; capability `UNVERIFIED` |
| Supporting direct diagnostic | Prior same Node/npm/minimal configuration separately recorded three registry `EAI_AGAIN` attempts; contribution to the prior exact adapter failure is **Inferred**, not proven |
| Seeded-tree doctor/build/check | PASS |
| Graph | 540 nodes, 1,689 edges, 43 files, 2,443,178 bytes |
| Ask | Lexical, structural, and empty modes; source off/on: 6/6 PASS |
| Freshness/tamper | Changed-source check/ask and graph-tamper check/ask failed closed |
| Public JSON | All successful public path strings project-relative; no host paths; check 3,644 B under 4,096 B |
| Durable evidence | Build/check records retained exact project, Node, and Git paths |
| Removal | Before-check incomplete; apply complete; after-check complete; tracked tree restored |
| F0 after removal | 230-test fast profile passed without Graft |

**Observed:** 867 process samples contained 42 visible Node records; none
contained the synthetic secret sentinel or proxy keys. No selected-process
socket row was sampled. Neither root `.ignore` nor root `.graft` appeared. All
101 post-removal samples found managed runtime/state absent; the declared empty
`artifacts/.graft-adapter.lock` remained. The final source Git status was clean.

**Unverified:** sampling does not prove exhaustive network silence, credential
non-access, or containment of a fully detached/renamed process. The public
install path and npm package build provenance are not passed by substituting the
seeded tree.

Evidence directory: `evidence/v2/real-graft/final-6966b55/`. The summary
SHA-256 is
`f63c0d37ba9778ca03c0fc20db03eefe42766e82e3eae01ad9418359c5b158a3`;
the results JSON SHA-256 is
`95820c841b72589b8e96646e3e60d0c76b8187f06392b3b1d869ee2950572248`;
the evidence-manifest and command-record SHA-256 values are
`5009ea3b91ca61ca8f5bbbeffb59fa965d7b8bcae5896768485d7e5249847fc0`
and
`9f1d89c86ded4c39fd7a3348ee709b0bb1964f615224bb90d8411daad38cf0bc`.

## Canonical command skeleton

Run from clean, isolated copies and record exact paths and environment controls.

```bash
uv lock --check
uv sync --python 3.12 --locked --group dev
uv run --python 3.12 --locked --group dev pytest -q
uv build
uv run --locked --group dev twine check dist/*
```

Ruff's configured C901 check is the current complexity sensor for the adapter.
To produce adapter-specific CRAP evidence, first capture exact adapter coverage:

```bash
uv run --locked --group dev coverage run --branch \
  --include='tools/graft_adapter.py' -m pytest tests/tooling/test_graft_adapter.py
uv run --locked --group dev coverage json \
  -o artifacts/quality/graft-adapter-coverage.json
```

Then map that file's executed/missing statement lines to
`cleanai_core.crap.callable_blocks()` and apply `crap_score()` against the
unchanged configured threshold. The existing `cleanai.py crap` command is not a
valid substitute because its policy intentionally scans only the product source
root. Until this adapter-targeting mapping is committed, tested, and recorded,
adapter CRAP remains **Unverified**.

For each official render, initialize and review Git only when exercising F1;
ordinary Python validation must not need Node or Graft.

```bash
uv run --locked --group dev python tools/cleanai.py gauntlet fast
uv run --locked --group dev python tools/cleanai.py gauntlet full
uv run --locked --group dev python tools/cleanai.py gauntlet hardening
uv run --locked --group dev python tools/cleanai.py gauntlet release
```

The optional connected sequence is:

```bash
uv run --locked --group dev python tools/graft_adapter.py doctor
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py doctor
uv run --locked --group dev python tools/graft_adapter.py build
uv run --locked --group dev python tools/graft_adapter.py check
uv run --locked --group dev python tools/graft_adapter.py ask \
  "Where is release blocking decided?" --limit 5
uv run --locked --group dev python tools/graft_adapter.py ask \
  "Where is release blocking decided?" --limit 5 --source
uv run --locked --group dev python tools/graft_adapter.py remove --check
uv run --locked --group dev python tools/graft_adapter.py remove --apply
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

## Required command record fields

For every command, record working directory, exact command, tool versions,
environment controls, starting revision/dirty policy, start/end time, exit code,
stdout/stderr path, files written/changed/removed, network access, potentially
visible credential names (never values), determinism/model/heuristic class, and
what the result can and cannot establish.

## Release interpretation

The exact adapter install attempt ended with npm's generic internal error. A
separate direct diagnostic under the same Node/npm and minimal configuration
recorded three registry `EAI_AGAIN` attempts. **Inferred:** DNS likely
contributed, but the evidence does not establish that causal link for the exact
adapter attempt. Connected installation remains **Unverified**, not a package
pass or product-capability failure. Rerun the optional connected sequence where
the configured npm registry resolves, preserving npm 10.9.0 and all adapter
environment controls.

Even if every pending row becomes pass, the feature decision does not change:
F0 remains default; narrow F1 remains experimental; F2–F6 remain rejected from
the project profile. Green adapter validation establishes the named controls only. It does
not establish complete static analysis, network/process sandboxing, token
savings, human comprehension, or productivity improvement.
