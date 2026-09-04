# Audit of the enhanced experimental Graft variant

> Status: final local source `b719459` is validated and remote review commit
> `4dc3603` has the identical tree. First hosted GitHub Actions run `33873556873`
> passed Python 3.12 and 3.13. The final report-only publication run remains
> pending. This report does not supersede the immutable original checkpoint.

## Superseding final local checkpoint

This section supersedes earlier uses of “final” below, which are retained as an
audit chronology. Four findings were discovered after `4bba7c0` and three more
after `8ae0eb5`; therefore the earlier predecessor statement that no P0/P1
remained was premature.

**Observed:** final source commit
`b719459a051a60d4af1e4fa30b3c32277fa97b8c` (tree
`35819081108685c24f47ba5251ec7e18004b0016`) passed 99 template tests and an
official Cookiecutter render. That render passed the complete release profile
on CPython 3.12.13 and 3.13.14: 243 tests, 94.97% product branch coverage,
83.25% harness branch coverage, worst local CRAP 10.10, six killed curated
mutants, build/Twine, and external-wheel smoke. The canonical Markdown gate
validated the expanded template and generated-project Graft README sections.

**Observed:** GitHub review commit
`4dc3603a6360111a1f9619c3e409d67755cff710` points to that exact tree.
[Hosted run 33873556873](https://github.com/heng2j/clean-agentic-python-cookiecutter/actions/runs/33873556873)
completed successfully for both `render (3.12)` and `render (3.13)`, including
template tests, official generation, generated fast gate, build, and Twine.

**Observed:** the final focused adapter suite passed 122 tests. Seven late
findings—two P0 and five P1—now have regressions for public metadata/path
minimization, bounded hostile diagnostics, tracked-file protection, a
cross-target cleanup race, exact receipt authority, and pre-publication Unicode
validation. Across the whole candidate chronology, 23 falsification findings
were recorded: two P0, twenty P1, and one P2. No P0 or P1 remains unresolved at
the final local test boundary.

**Observed:** a real, byte-identical Graft 0.16 runtime preserved from the prior
successful package fetch was seeded with a new local tamper-detection receipt.
It passed `doctor`, `build`, `check`, and the documented bounded `ask`; the graph
contained 569 nodes, 1,783 edges, and 43 files. Cleanup classified 7,522 paths
as receipt-bound, zero as unknown, removed the runtime and derived state, and a
second check reported `complete: true` with a clean Git worktree. This is a
real-package compatibility/removal control, not an installation or provenance
pass.

**Observed:** two fresh connected installs at the final source boundary ran
the pinned Node 22.12.0/npm 10.9.0 path, ended after about 70.5 seconds with
npm's internal “Exit handler never called” error, returned adapter `FAIL`, and
did not promote a runtime. Their partial staging trees were detected as unknown
and refused by cleanup. **Unverified:** connected installation success and
source-to-package build provenance.

**Recommended:** keep F0 as the default and F1 as a narrow optional experiment.
The controlled benchmark still favored `rg`/source over broader Graft retrieval,
and the frozen final-F1 task trial still cannot run because Graft 0.16 omits a
tracked hidden-directory Python file. No accepted-task correctness, token,
cost, blast-radius, or productivity benefit is established.

## Executive verdict

**Observed:** the original branch at
`ab3e06f6a402a22f51d8447101f245eab258b8e6` was not credible. It had two P0,
thirteen P1, and three P2 findings. The original adapter could overwrite an
outside file through a symlink, exposed arbitrary ambient credentials to an
external npm program, pinned an unpublished package, miswired most advertised
operations, and made every generated-project gauntlet red.

**Observed:** the v2 candidate materially replaces that boundary. It uses the
published `@nanonets/graft@0.16.0` through a reviewed project-local lock, a
fixed CLI module, a minimal child environment, symlink and ownership checks,
transactional install/build publication, typed and bounded JSON fields, output
and time bounds, source/revision receipts, graph-tree hashes, and explicit local
removal. Bounded upstream strings remain untrusted third-party text.
The only public structural operations are `build`, `check`, and bounded `ask`.

**Observed:** F2 MCP, F3 export, F4 LSP, F5 deep/model summaries, and F6 hooks,
status line, or prompt injection are absent from the project-owned surface.
Upstream `map`, `skeleton`, `callers`, indexed `grep`, and `blast` were tested as
research capabilities but were removed from the adapter because their measured
benefit and completeness did not justify an exposed maintenance surface.

**Recommended:** keep F0—current source, `rg`/`git grep`, contracts, tests, and
the ordinary Python gates—as the default. Retain only the narrowed F1 adapter as
an optional experiment. Do not promote it as a correctness, context, token,
blast-radius, or productivity improvement.

**Observed:** an exact `git archive` of implementation commit `6966b55` passed
the Python 3.12 no-Graft template, generation, all four profiles, packaging,
external-wheel, and non-default-render boundaries. It ran 99 template and 230
generated tests, measured 94.97% product and 82.78% harness branch coverage,
reported CRAP 10.10, and killed all three code plus all three specification
mutants. Graft was absent; `doctor` correctly returned `UNVERIFIED` while the
ordinary Python release remained green. The exact same implementation commit
passed the corresponding Python 3.13 all-profile boundary.

**Observed:** exact implementation commit `6966b55` passed seeded real-0.16
doctor/build/check, six ask modes, freshness/tamper rejection, removal, public-
path assertions, and a 230-test post-removal F0 gate. The real check envelope
was 3,644 bytes under the 4,096-byte ceiling; durable build/check evidence kept
full local identity. A prior public install attempt exited 2 after 70.588
seconds with npm's generic
"Exit handler never called" diagnostic. A separate prior direct diagnostic
under the same tool/configuration recorded registry `EAI_AGAIN`; DNS is a
plausible contributor, not a proven cause of the exact adapter failure. The
seeded tree is explicitly not an install or provenance pass.

**Observed:** after `b9ee429c`, a long-parent test found public `check` output at
4,243 bytes because it contained absolute host paths. Implementation commit
`6966b55` separates project-relative successful public output from full durable
local evidence. Its Python 3.12 matrix and exact held-out applicability replay
passed their stated expectations. Historical child `4bba7c0` narrowed the
durable-evidence wording to `install` and structural commands; its 99 root tests,
official render, offline generated sync, strict docs/context audits, and
canonical 76-file Markdown check passed.

**Observed:** exact `6966b55` Python 3.13 also passed 99 template tests, every
230-test generated profile, 94.97% product and 82.78% harness branch coverage,
six curated mutants, packaging, external-wheel lifecycle, no-Graft behavior,
and bounded path-minimized public JSON.

**Unverified:** public connected install, hosted Actions, and report-bearing
commit checksums must be filled by the final validator. Native macOS, Windows,
ARM64, exact model
tokens/cost, independent newcomer comprehension, package build provenance, and
packet-level network silence also remain unverified.

## Frozen identities

| Subject | Identity | Evidence status |
|---|---|---|
| Experimental branch audited | `ab3e06f6a402a22f51d8447101f245eab258b8e6` | **Observed** |
| Scientific parent / merge base | `72a7e52eb0e2ac35ef4ca36f716dc2e183afc6c4` | **Observed** |
| Main at freeze | `f0d505f9304c0ff42f3cb79deac461b42b7ac3e9` | **Observed** |
| V2 branch | `audit/experimental-graft-variant-v2` | **Observed locally**; remote publication pending |
| Final source candidate | `b719459a051a60d4af1e4fa30b3c32277fa97b8c` (tree `35819081108685c24f47ba5251ec7e18004b0016`) | **Observed:** exact local template, Python 3.12/3.13 release, late-red-team, README/docs, and seeded real-package boundaries passed |
| Predecessor implementation checkpoint | `6966b5500eaa22d17f0526dbd051437aadb43255` (tree `1203a71bd165251b2618fc669c4f027bd86e0cf1`) | **Historical observed checkpoint; superseded after late red-team findings** |
| Original declared package | `@nanonets/graft@0.17.0` | **Observed unavailable**: npm E404; no release tag |
| V2 package | `@nanonets/graft@0.16.0` | **Observed published** |
| npm publication | `2026-08-31T14:35:52.197Z` | **Observed** in registry history |
| Upstream mapping | tag `v0.16.0`, commit `aa1e2bb0f6326068ac64886da1e67fa25a7804de` | **Observed** npm `gitHead` match; unsigned |
| Graft license | MIT; 2026 Context Graph Engine contributors | **Observed** in package manifest/tarball and pinned upstream license |
| Registry integrity | `sha512-L3E5F1aDYJDCARgfR7O2VaMt8xwO1XNYyHiW2n1WhKnj87gPqoxoZJGNbGXfw6XeA9JSJX3naA36RZ+jDf4AcQ==` | **Observed** against downloaded tarball |
| Reviewed F1 Node range | `>=22.12.0,<23` | **Recommended** narrow profile; real Linux probes used 22.12.0 |
| Reviewed install npm | `10.9.0` exactly | **Observed selected**; exact adapter attempt failed generically, while a separate diagnostic observed registry `EAI_AGAIN`; connected install **Unverified** |
| Source-to-package provenance | No verified reproducible-build attestation | **Unverified** |

The original 160-file manifest and checkpoint hashes are preserved in this
directory. Baseline and adversarial commands ran in isolated worktrees, renders,
fixtures, or package quarantine directories. Credential values are not recorded;
privacy tests used synthetic values.

## Trust-model matrix

The frozen original audit used a compact six-column table and omitted the
charter's dedicated failure-mode field. That checkpoint remains unchanged; this
v2 matrix supplies the complete schema without retroactively rewriting it.

| Principle | Repository evidence | Executable enforcement | Current Graft integration behavior | Failure mode | Verdict | Required fix |
|---|---|---|---|---|---|---|
| Humans own intent, judgment, integration, and acceptance | Task packets, scoped context, tests, gates, and explicit acceptance remain canonical | Adapter labels graph results as derived; acceptance still requires source/search/tests and human review | F1 ranks or traverses derived structural evidence only | Agent treats a result or edge as the decision or complete scope | **Partially aligned; semantic completeness Unverified** | Keep F0 default and require independent executable acceptance |
| Agents own bounded execution and exploration bandwidth | Repository exposes narrow task commands and evidence schemas | Closed parser, byte/time/result bounds, and typed-field validation; returned upstream strings stay untrusted | Public surface is only `build`, `check`, bounded `ask`; broad upstream probes are research-only | Generic forwarding activates unreviewed behavior or emits unbounded context | **Observed aligned at cross-version and seeded-real boundary** | Retain narrow F1; reject F2–F6 |
| Current source and declared authority outrank derived navigation | `AGENTS.md` routes to source, contracts, tests, ADRs, and explicit decisions | Source/revision receipts, stale-state rejection, source-slice binding, and required fallback | Graphs remain incomplete for dynamic/config/package/hidden relationships | A query misses a runtime path or resolves an ambiguous symbol incorrectly | **Mitigated, not resolved** | Fail closed on detectable staleness and never claim exhaustive retrieval |
| Missing or unrun checks are `UNVERIFIED`, never `PASS` | Evidence contract distinguishes PASS, FAIL, and UNVERIFIED | Command-specific exception/status taxonomy | Candidate first conflated broad states, then `doctor` still mapped unsafe/tampered state to UNVERIFIED | Missing prerequisite becomes a false failure, or unsafe state becomes merely unverified | **Observed corrected in cross-version and seeded-real matrices** | Preserve missing-runtime/graph, stale, unsafe/tamper, and child-failure regressions |
| Graft is optional and removable; absence cannot fail Python gates | No Graft dependency in Python lock/gates/package; explicit removal inventory | Explicit `install --apply`; no generation/gate hook; project-local five-root removal postcondition | npm/native runtime exists only after opt-in; upstream direct setup remains outside controls | Failed install leaves code outside inventory, or no-Graft release becomes red | **Observed aligned:** current implementation passed Python 3.12/3.13 and seeded-runtime removal reached complete | Preserve connected-install limitation and complete final docs/report checks |
| Privacy and network activity require explicit consent | Minimal child environment, isolated state, no provider command | Empty dotenv, allowlist, `CI=1`, `DO_NOT_TRACK=1`, project-local cache/home | Published install/CLI source includes telemetry/upkeep paths; controls are cooperative | Ambient key reaches child, unexpected request occurs, or direct Graft bypasses adapter | **Partially mitigated; network silence Unverified** | Keep install explicit; reject deep/MCP; never claim sandboxing or packet silence |
| Reproducibility binds executable behavior, not just semver | Exact package/lock/hash/tool receipts and fixed local CLI | Node range, npm 10.9.0, manifest/CLI/lock/tree pre/post checks | Published 0.16.0 has native scripts; 0.17.0 was unavailable; source-to-dist attestation absent | Unreviewed npm interprets lock differently or tampered binary reports expected version | **Materially improved; provenance and final install Unverified** | Re-run exact toolchain when registry resolves; re-review every upgrade |
| Persistent context stays concise and product detail is on demand | One short root route; no MCP config, hooks, or injected instructions | Context audit and generated-doc route checks | F1 detail is pull-only; MCP/init could add schemas, hooks, status, and host writes but are absent | Sessions load stale tool guidance or competing authority | **Aligned for F0/F1; client token behavior Unverified** | Retain one route; keep F2/F6 disabled |

## Original reproduction

| Workflow | Result | Status |
|---|---|---|
| Template lock, tests, build, Twine | lock/build/Twine exit 0; 97 tests | **Observed** |
| Official default and non-default renders | exit 0 after the reserved-email negative test | **Observed** |
| Generated direct pytest/build/Twine without Graft | 125 tests; build/Twine exit 0 | **Observed** |
| Generated `fast`, `full`, `hardening`, `release` | each exit 1 at the same Ruff defect | **Observed failure** |
| Documented Graft 0.17 install | npm E404 | **Observed failure** |
| Original Python 3.13 | not executed | **Unverified** |

## V2 boundary and current evidence

| Boundary | V2 design | Evidence state |
|---|---|---|
| Optionality | No Node/Graft install during generation, `uv sync`, hooks, packaging, or gates | **Observed in source and component tests** |
| Installation | Explicit `install --apply`; private exact lock; no global/npx fallback | **Observed attempt:** exact npm ran and returned a generic internal error; separate same-config diagnostic saw `EAI_AGAIN`; causal link **Inferred**, capability **Unverified** |
| Identity | Exact Node/npm/Git identities plus manifest, CLI, lock, package integrity, and installed-tree hashes | **Observed component tests**; hashes are local tamper detection, not provenance |
| Secrets | Allowlisted child environment, `CI=1`, `DO_NOT_TRACK=1`, isolated home/cache/temp | **Observed:** synthetic tests plus 42 sampled Node records without sentinel/proxy keys; not exhaustive isolation |
| Filesystem | Path-chain, owner/mode/type, symlink/hardlink checks; fixed runtime-sibling staging; five-root removal inventory | **Observed:** focused tests plus seeded removal; host OS authority and connected-install residue remain **Unverified** |
| Process | Hard deadline, output cap, signal forwarding, and same-process-group cleanup | **Observed component tests and process sampling**; detached new-session containment is **Unverified** |
| Commands | `doctor`, `install --apply`, `remove --check/--apply`, `build`, `check`, `ask` | **Observed:** real missing doctor, generic npm install failure, seeded lifecycle, and six ask modes; separate diagnostic saw `EAI_AGAIN`; install **Unverified** |
| Source/graph/output | Git-bound tracked snapshot, rejected scope markers, strict graph and typed ask fields, source-span/code binding, and path-minimized successful public output; bounded upstream strings remain untrusted | **Observed:** exact `6966b55` real output/freshness/tamper probes, both Python versions, and held-out replay passed their path assertions; static omissions remain |
| Publication | Pre-commit failures preserve prior complete graph/runtime; after runtime commit, partial old-backup cleanup retains the validated new runtime and exposes remaining stale backup | **Observed fault injection and seeded removal**; public connected-install transaction remains **Unverified** |
| MCP/deep/hooks | No project command or active example | **Observed** |
| Persistent context | One concise `AGENTS.md` route; detail is on demand | **Observed:** current template router is 58 lines, 535 words, 4,022 bytes |

Component and predecessor-source checkpoints are preserved as evidence, but
they do not silently validate the later report-bearing commit. Every count and
source boundary is separated in `VALIDATION_GRAFT_VARIANT_V2.md`.

**Observed maintenance surface:** the final template adapter is 3,564 lines,
131,756 bytes, and 157 top-level classes/functions; its focused test file is
2,066 lines and 76,169 bytes. Ruff C901 is configured, but the project's CRAP
sensor scans product source rather than this adapter. Adapter-specific CRAP is
therefore **Unverified**. This code/maintenance cost weighs against promotion
even if final behavioral validation passes.

### Candidate defects found during falsification

**Observed:** repeated candidate runs found fifteen additional P1 defects and
one P2 rather than merely confirming the implementation.

| ID | Severity | Observed defect | Implemented correction; final status |
|---|---|---|---|
| `GRAFT-V2-001` | P1 | Generated Ruff I001 and format mismatch | Import/format corrected; exact 3.12/3.13 rendered matrices passed |
| `GRAFT-V2-002` | P1 | Eight Pyrefly adapter diagnostics | Explicit handler/stream/path/list types; exact 3.12/3.13 release matrices passed |
| `GRAFT-V2-003` | P1 | npm 10.9 rejected identical user/global `/dev/null` config | Distinct adapter-owned global config passed the real probe; connected install remained **Unverified** |
| `GRAFT-V2-004` | P1 | Real Graft wrote root `.ignore` | With `GRAFT_NO_IGNORE` plus `--no-ignore`, seeded real lifecycle created no root `.ignore` |
| `GRAFT-V2-005` | P1 | `check` emitted 34,206 B / 539 lines including 517 `pendingIds` | Compact projection with count/hash/raw identity passed seeded real check; semantic completeness not implied |
| `GRAFT-V2-006` | P1 | Failed installs left three out-of-project sibling staging directories | Fixed in-project staging and five-root inventory; seeded removal complete, abrupt connected-install residue **Unverified** |
| `GRAFT-V2-007` | P1 | Bare Python selected host 3.11 and failed before JSON | Locked uv command route passed executable rendered regression on both versions; independent newcomer comprehension **Unverified** |
| `GRAFT-V2-008` | P1 | Fake npm 99.0.0 produced a plausible tree and PASS | Require npm 10.9.0 before replacement; exact adapter install failed generically, separate diagnostic saw `EAI_AGAIN`, and capability remains **Unverified** |
| `GRAFT-V2-009` | P1 | Real 0.16 file-span convention caused all 38 file nodes/build to be rejected | Exact file-kind convention with strict symbol bounds passed exact seeded real 540-node build |
| `GRAFT-V2-010` | P1 | Blanket exceptions mislabeled FAIL versus UNVERIFIED states | Real missing doctor and stale/tamper cases behaved correctly; remaining adversarial matrix uses focused tests |
| `GRAFT-V2-011` | P1 | Failed npm evidence claimed install scripts executed without observation | Record authorization and attempt only; cross-version failing-install regression passed |
| `GRAFT-V2-012` | P2 | Workflow omitted the durable experimental branch | Include durable and review branches; review-branch hosted run `33873556873` passed both jobs |
| `GRAFT-V2-013` | P1 | `check` accepted and echoed unknown fields, including imperative text | Exact reviewed schema and project-owned projection passed cross-version and exact-real regressions |
| `GRAFT-V2-014` | P1 | `doctor` labeled unsafe/tampered state UNVERIFIED | Separate prerequisite versus rejection catches passed cross-version and exact-real status matrices |
| `GRAFT-V2-015` | P1 | Public docs omitted the observed hidden-directory F1 availability boundary and safe F0 recovery | Exact rendered regression passed; final `b719459` README/docs gates passed |
| `GRAFT-V2-016` | P1 | Absolute host paths made public `check` output 4,243 B and checkout-location-dependent | `6966b55` path-minimizes successful public envelopes; 3.12, 3.13, exact-real, and held-out path checks passed |
| `GRAFT-V2-017` | P1 | Public PASS graph metadata reflected arbitrary upstream language text | Count/hash-only public projection; exact untrusted metadata remains only in ignored evidence |
| `GRAFT-V2-018` | P1 | Successful install output leaked absolute Node/npm paths | Public tool identities omit paths; local durable evidence retains exact identities |
| `GRAFT-V2-019` | P1 | Huge identifiers and escaped diagnostics exceeded the error context budget | Generic invalid-value errors, hashes, ASCII-safe serialization, and a 128-character cap |
| `GRAFT-V2-020` | P0 | Cleanup deleted a force-tracked scientific result and reported PASS | Git preflight blocks all deletion and preserves tracked bytes/runtime/status |
| `GRAFT-V2-021` | P0 | A later-target writer could race the one-time cleanup inventory and lose work | Full tracked/ownership preflight repeats before each target; unrelated writers must still stop |
| `GRAFT-V2-022` | P1 | Cleanup ignored altered receipt authority, extra keys, and missing tool identity | One exact receipt schema is required for runtime use and deletion authority |
| `GRAFT-V2-023` | P1 | A lone surrogate failed after graph promotion, replacing good state | UTF-8 validation fails before publication and preserves prior graph/receipt bytes |

The structured report contains full reproductions, impacts, root causes,
regression tests, tradeoffs, and mappings to the original finding set. No row is
resolved merely because the correction exists in source.

**Observed:** after the seven late regressions and exact `b719459` local
validation, no P0 or P1 remains unresolved at the tested boundary. This does
not convert connected install, hosted, platform, human-study, packet-level, or
same-user OS-race boundaries from **Unverified** to pass, and it does not justify
promoting F1 beyond an experiment.

## Finding disposition

All 18 original IDs remain traceable in the structured v2 findings.

- `GRAFT-O-001`–`007`: the adapter boundary was replaced and narrowed. Exact
  cross-version tests, seeded real lifecycle, and final-F1 fail-closed behavior
  are observed; connected install remains unverified.
- `GRAFT-O-008`: the generated formatter regression was repaired and the CI
  workflow now exercises a rendered project; Python 3.12 and 3.13
  production-source validation and review-branch hosted execution passed.
- `GRAFT-O-009`: the in-repository friction ledger is labeled visible smoke
  instrumentation; causal claims require an external held-out oracle.
- `GRAFT-O-010`–`011`: MCP is removed and disabled rather than normalized into
  F1.
- `GRAFT-O-012`: canonical routes, Git prerequisites, expected results,
  source/search/test fallback, and recovery/removal are documented; the hidden-
  directory recovery passed exact `6966b55` rendered checks. The wording-only
  `4bba7c0` child passed its root/docs checks, and final `b719459` retained the
  boundary through its cross-version release validation.
- `GRAFT-O-013`–`014`: telemetry controls precede the explicit local install,
  but the native scripted supply chain remains a material residual risk.
- `GRAFT-O-015`: upstream structural false negatives are not fixed. V2 narrows
  retrieval to advisory `ask` and requires source, exhaustive search, tests,
  and package/runtime evidence for consequential conclusions.
- `GRAFT-O-016`–`018`: evidence, context, and support claims are narrowed;
  non-Linux native portability remains unverified.

No P0/P1 is marked resolved merely because code exists. The resolution labels
are bound to the exact observed tests in the structured finding and validation
report; connected, hosted, cohort, and platform residuals remain separately
**Unverified**.

## Retrieval and accepted-task result

The preregistered deterministic benchmark used 16 queries across four frozen
repositories, three repeats per cohort, and external file-level oracles.

| Cohort | Mean precision | Mean recall | Median net byte proxy |
|---|---:|---:|---:|
| C0 / F0: `rg` or `git grep` | 0.728 | 0.969 | 960 B |
| C1 / F1: structural CLI | 0.479 | 0.748 | 3,363 B |
| C2 / F2: structural MCP | 0.479 | 0.748 | 6,762 B |

**Observed:** C1 was 250% larger and C2 605% larger than C0 on the primary
median proxy, while recall was lower. A sensitivity calculation that added
equivalent source-verification reads still made C1 61% and C2 188% larger.

**Observed:** six fresh-clone agent trials on one bounded Unicode-whitespace
change all passed the external oracle and repository tests: 3/3 C0 and 3/3
research C1. Every C1 agent also used `rg` and/or direct source inspection. That
C1 wrapper exposed upstream `grep` and `callers`; final F1 deliberately exposes
neither. The trials therefore show no advantage for the broader upstream
condition and do not validate accepted-task correctness for the narrowed v2
adapter.

**Unverified:** accepted-task outcome for final F1, exact model tokens, cost,
time, file-open counts, complete human intervention, review correction, and
rework. Byte counts are not tokenizer or billing truth. Agent self-reported
“tokens saved” is not accepted as independent evidence.

**Observed:** a preregistered final-adapter rerun could not advance to a task
agent. Real Graft 0.16 omitted tracked `.hidden/visible.py`; the adapter's first
`build` returned exit 2/FAIL after 2.672028 seconds, removed the staged graph,
and published nothing. `check`, `ask`, and the task change did not run;
repetitions 2–3 stopped under the frozen rule. This shows both a real F1
applicability gap and the intended fail-closed behavior. It is not an agent-
correctness regression or a parity result.

## Explainability result

**Observed:** upstream Graft provided useful evidence for some uniquely named,
statically resolvable relationships: 31/31 fixture signatures, 10/10 indexed
Python literal hits, a 3/3 unique blast control, and four freshness mutations.

**Observed limits:** `ask --source` file-level micro precision/recall was
0.30/0.80. Duplicate-name callers were 0/0 with one false edge and two missed
callers. Duplicate-symbol blast missed 4/4 known downstream files. Decorator
registration, dictionary dispatch, computed imports, TOML entry points,
source-versus-wheel resources, and tracked hidden files were absent or flattened.

**Inferred:** the narrowed F1 `ask` may supply a first pointer. It cannot be an
exhaustive search, blast-radius oracle, runtime/packaging proof, or explanation
of why a design was chosen.

## Privacy, telemetry, supply chain, and portability

**Source-supported:** published Graft 0.16.0 loads cwd dotenv configuration,
performs update upkeep for ordinary direct commands, and has install telemetry
that can launch a detached flush unless an opt-out condition exists before
installation. The reviewed dependency tree has 45 packages beyond the root and
12 lifecycle-script packages; a tree-sitter installer can fetch an external
binary outside npm lock integrity. `GRAFT_SOURCE_INDEX.md` links the pinned
source, registry, license, runtime-boundary code, and issue evidence used for
these claims.

**Observed control:** v2 supplies an empty dotenv route, minimizes the child
environment, sets `CI`/`DO_NOT_TRACK` before install and runtime, isolates state,
and exposes no provider/deep operation. In the exact seeded real lifecycle, 42
visible Node records across 867 samples contained neither the synthetic secret
sentinel nor proxy keys; no selected-process socket row was sampled. Sampling
does not establish exhaustive non-access or network silence.

**Inferred residual:** these are cooperative controls, not a filesystem,
network, or process sandbox. A dependency can read process-readable project
files, and a deliberately detached child can escape portable process-group
cleanup. Direct Graft/npm use bypasses all project controls.

Linux x86_64 with Node 22.12.0 is the only executed Graft profile at this
checkpoint. macOS, Windows, ARM64, alternate Node versions, hosted-client MCP,
real LSP, and deep/model cohorts remain **Unverified**.

## Residual engineering boundaries

- **Observed:** public examples use `uv run --locked --group dev python` so the
  selected Python comes from the locked project. The adapter's diagnostic path
  may be read-only after it starts, but uv can reconcile its managed environment
  first; the entire launcher command is not claimed filesystem-pure.
- **Observed:** derived receipts can contain absolute project, executable,
  cache, or temporary paths. They stay ignored/local by default and require
  scrubbing before evidence is shared.
- **Inferred:** path allowlists and post-state checks do not stop a malicious
  dependency from writing another ignored or out-of-scope path with host
  authority. Strong prevention needs OS filesystem/network/process containment,
  which F1 does not provide.
- **Recommended:** removal of derived runtime/graph/evidence uses the reviewed
  adapter inventory. Full retirement of tracked Graft scaffolding remains a
  normal reviewed code change followed by `git grep -n -i graft` and ordinary
  no-Graft gates; it is not automatic deletion.
- **Unverified:** exact Node/npm onboarding beyond the narrowed version
  contract, final connected install after the generic npm failure and separate
  `EAI_AGAIN` diagnostic, source-to-package
  provenance, hostile detached-process containment, and adapter-specific CRAP.

## Capability decision

| Capability | Decision | Basis |
|---|---|---|
| F0 no Graft | **Keep/default** | Ordinary, inspectable source/search/test workflow and control cohort |
| F1 narrow structural CLI | **Keep experimental** | Safer boundary, but no measured retrieval/context/correctness advantage |
| F2 structural MCP | **Reject/disable** | Same retrieval accuracy, larger fixed context, broader lifecycle/instruction boundary |
| F3 deterministic export | **Reject in profile** | Persuasive artifacts inherit omissions and did not earn maintenance/privacy cost |
| F4 LSP | **Reject/disable; capability Unverified** | No real pinned language-server cohort |
| F5 deep summaries | **Reject by default** | Not authorized; disclosure, credential, cost, cache, and hallucination risks |
| F6 hooks/prompt injection | **Reject** | Competing context, global/client writes, and hidden activity violate pull-only use |

## Release decision

**Recommended:** remain experimental and narrow. The exact local green matrices
show that the bounded adapter behaves as specified at the tested boundaries;
they do not prove that Graft improves accepted-task efficiency. Do not promote
F1 based on this audit alone.

See `VALIDATION_GRAFT_VARIANT_V2.md` for exact results and remaining unverified
boundaries, and
`EVIDENCE_REFERENCE.md` for raw-evidence boundaries. See
`GRAFT_SOURCE_INDEX.md` for stable primary-source links and their interpretation
limits.
