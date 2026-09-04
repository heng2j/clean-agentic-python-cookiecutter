# Graft claim–evidence matrix

Primary upstream and registry links are centralized in
`GRAFT_SOURCE_INDEX.md`. Source code links there are pinned to the reviewed
commit; issue reports are treated as reported constraints, not as substitutes
for this audit's observations.

## Original checkpoint

| Claim | Classification | Evidence | Verdict / correction |
|---|---|---|---|
| The experimental branch descends from the scientific variant | **Observed** | Experimental/scientific merge base is `72a7e52e`; experimental head is `ab3e06f` | Supported |
| Graft is optional and not a Python dependency | **Observed** | Render lock, pytest, build, and Twine succeed with no `graft` executable | Supported, but canonical gates are independently broken |
| Required Graft 0.17.0 can be installed as documented | **Observed** | `npm view @nanonets/graft@0.17.0` returns E404; latest published is 0.16.0 | False |
| The pin corresponds to reviewed upstream source | **Source-supported** | Upstream commit `05760b07` declares 0.17.0 but has no matching published npm release/tag | Source exists; distributable identity does not |
| The adapter is project-scoped | **Observed** | State paths are lexical project paths | False under symlinks and positional source symlinks |
| The adapter strips credentials | **Observed** | It removes eight names from a copied environment; arbitrary/cloud/npm/Git credentials remain | Materially incomplete; privacy claim must say minimal allowlist or fail |
| Structural mode is telemetry-off | **Source-supported** | Graft telemetry gate checks `DO_NOT_TRACK`; adapter sets it | Supported for reviewed source path; not a network sandbox, and install/update behavior is separate |
| The adapter suppresses update checks | **Source-supported** | It writes a fresh project-home update cache; upstream consults 24-hour cache | Version-specific and mutating; symlink overwrite reproduced |
| Deep/model access is blocked | **Observed** | Known deep/provider flags are denylisted | Partial: broad pass-through is not a future-proof capability boundary |
| `init`, hooks, and global agent changes are absent by default | **Observed** | No init invocation or committed upstream host files | Supported positive control |
| All nine advertised CLI operations use the project graph | **Observed** | Real 0.16 and source-built 0.17 adapter-semantics trials | False: six operations failed or returned empty due graph-root handoff |
| Ranked retrieval reduces context | **Unverified** | No controlled accepted-task model/client trial; upstream self-estimates exclude fixed/fallback/review cost | Do not claim |
| Ranked retrieval is exhaustive | **Observed** | Fixture misses dynamic/config/wheel/duplicate-symbol edges; docs disclaim exhaustiveness | False, correctly disclaimed in prose |
| `ask --source` is precise on the held-out fixture | **Observed** | File-level micro precision 12/40 = 0.30; recall 12/15 = 0.80 | Mixed; useful lead generator, noisy evidence |
| Blast radius is complete | **Observed** | Duplicate-name case found 0/4 known downstream; unique static control found 3/3 | False; symbol ambiguity is material |
| Freshness detects ordinary edits | **Observed** | Unstaged edit, staged move, deletion, and untracked addition were detected/refreshed | Supported for tested fixture |
| A no-server LSP run is clearly unverified | **Observed** | Exit 0, zero added LSP edges, terse `lsp:none` | False-success risk; cohort remains unverified |
| MCP is merely another bounded adapter surface | **Source-supported** | Upstream server supplies its own instructions/schema and boot upkeep | False; distinct higher-risk capability |
| The MCP opt-in stays local/uncommitted | **Observed** | `.mcp.json` is not ignored and `git add --dry-run` stages it | False operational control |
| Persistent agent context remains concise | **Observed** | Six baseline context files are byte-identical to parent; root route proxy 973 tokens | Supported, but Graft is undiscoverable and MCP runtime schema cost is unmeasured |
| The documented comparison is controlled and blinded | **Observed** | `run.json` exposes expected/forbidden globs and verification; major controls absent | False |
| Graft output is derived navigation evidence | **Observed** | Repeated explicit language in guide/prompt | Supported and must remain |

## Enhanced candidate

| Claim | Classification | Evidence | Verdict / correction |
|---|---|---|---|
| Published identity, date, and license are known | **Observed** | Registry history records 0.16.0 at `2026-08-31T14:35:52.197Z`; manifest, tarball, and pinned source license say MIT | Supported for identity; reproducible source-to-dist build remains **Unverified** |
| V2 uses a published reviewed package | **Observed** | `@nanonets/graft@0.16.0`; registry integrity and npm `gitHead` match tag commit `aa1e2bb0...` | Supported for byte identity; source-to-dist reproducibility remains **Unverified** |
| Graft remains optional | **Observed** | Exact `b719459` no-Graft generation, 243-test release, packaging, and external wheel passed on Python 3.12/3.13; identical remote tree passed hosted run `33873556873`; Graft is absent from Python gates | Connected install remains **Unverified** |
| V2 exposes the whole upstream structural surface | **Observed false** | Public adapter has only `build`, `check`, and bounded `ask` plus lifecycle commands | Narrowing is deliberate; map/skeleton/callers/grep/blast are evaluation evidence only |
| V2 inherits arbitrary shell or direnv secrets | **Observed false in focused tests** | Child environment is constructed from an allowlist with isolated home/cache/temp | Dependency code can still read process-readable project files; no network sandbox |
| V2 is safe against PATH/version spoofing | **Observed in focused tests** | Fixed CLI module plus Node/npm/Git and manifest/CLI/lock/tree identity checks before/after execution | Local tamper detection supported; tool/package provenance remains **Unverified** |
| Pre-commit install/build failure preserves the prior complete state | **Observed in fault-injection tests** | Staging, rollback, post-state validation, and durable-evidence ordering before commit | Final real interruption rerun pending |
| Post-commit install cleanup failure restores the prior runtime | **Observed false by design** | Once the validated replacement is active, partial old-backup cleanup retains that new runtime and exposes remaining stale backup | This is a visible recovery state, not rollback; final real cleanup-fault rerun pending |
| V2 works with npm 10.9 using `/dev/null` for both config roles | **Observed false** | Real version probe rejected identical user/global config paths | Distinct adapter-owned global config passed the exact probe; exact install then failed generically, while a separate diagnostic observed `EAI_AGAIN`; connected install **Unverified** |
| Real Graft never writes a root `.ignore` file | **Observed false before correction** | Real 0.16 probe created `.ignore` without explicit suppression | With `GRAFT_NO_IGNORE` and `--no-ignore`, seeded real build/check/ask created no root `.ignore` |
| `check` output is automatically context-efficient | **Observed false twice** | Raw real output was 34,206 B / 539 lines with 517 `pendingIds`; later absolute paths made the projected output 4,243 B in a long checkout | V2 omits identifiers; exact `6966b55` real check was 3,644 B and path-minimized; no completeness claim |
| Public evidence size/privacy is checkout-path-independent | **Observed false before correction** | Absolute validation/graph/executable/evidence paths caused a 4,243 B response and exposed host structure | Exact `6966b55` real/cross-version/held-out probes found no host paths in public output; full identity stays in install/structural durable evidence |
| Successful public metadata contains no unneeded upstream prose | **Observed false before final correction** | Imperative text in graph `meta.languages` appeared verbatim in PASS output | Final public output uses count/hash/untrusted classification; exact labels stay in ignored evidence |
| Successful public install output omits host tool paths | **Observed false before final correction** | Absolute Node/npm paths appeared in a PASS install envelope | Final public tool projection keeps version/hash/provenance and moves exact paths to durable evidence |
| Every error remains bounded after JSON escaping | **Observed false before final correction** | A 1 MiB identifier and repeated surrogate/control/emoji text exceeded the intended context budget | Final tests require omitted identifier evidence and escaped error JSON below 4 KiB |
| A bounded `check` payload is necessarily safe from injected upstream fields | **Observed false** | Former validator accepted unknown top-level/context/graph keys and the payload echoed an `instruction` field | Exact 0.16 key sets and a projection with no upstream prose/identifiers—only fixed project status/reason plus booleans/counts/hashes—passed exact real and focused reruns |
| Failed install staging is fully project-scoped and removable | **Observed false before correction** | Three random sibling directories remained outside projects; one contained full `node_modules` | Fixed staging inside `tools/graft-runtime` and expanded removal inventory; final crash/residue rerun pending |
| Cleanup cannot delete tracked content under ignored target roots | **Observed false before final correction** | A force-tracked scientific result was deleted and cleanup returned PASS | Git preflight now blocks all deletion; exact late-red-team replay preserves file, runtime, and status |
| Cleanup authorization remains current across all target deletions | **Observed false before final correction** | A writer added a private file to a later target after initial inventory; cleanup deleted it and returned PASS | Final adapter repeats full preflight before each target and preserves the reproduced late file; same-user post-preflight mutation remains a documented OS residual |
| A runtime receipt authorizes deletion if its digest core matches | **Observed false** | Altered authority, extra ownership note, or missing tools still allowed deletion | Runtime use and cleanup now require exact receipt keys, authority, tool keys, and identity shapes |
| Invalid graph Unicode cannot replace known-good state | **Observed false before final correction** | A lone surrogate failed during public hashing after graph/receipt promotion | UTF-8 validation now rejects before publication and exact prior graph/receipt bytes are preserved |
| Bare `python` examples select the supported project interpreter | **Observed false** | Host Python 3.11 failed on `typing.override` before JSON after uv had provisioned supported interpreters | Public examples now use locked `uv run --locked --group dev python`; generated Python 3.12/3.13 gates passed, while independent newcomer use remains Unverified |
| Any npm semver can reproducibly install the reviewed lock | **Observed false** | Fake npm 99.0.0 produced a plausible tree and received PASS | V2 requires npm 10.9.0 exactly; exact install failed generically and separate same-config diagnostic saw `EAI_AGAIN`; causality and connected install **Unverified** |
| All valid real 0.16 graph spans match ordinary symbol bounds | **Observed false** | Real file nodes use L1 through raw-newline-count plus one; the former rule rejected all 38 files | V2's version-specific file convention passed the exact seeded real 540-node build while retaining strict symbol/source binding |
| Every precondition error has the same evidentiary status | **Observed false** | Missing/unrun prerequisites and invalid/unsafe requests require different UNVERIFIED versus FAIL meanings | General taxonomy passed the cross-version focused matrix; real missing-runtime and stale/tamper behavior matched it |
| Unsafe or tampered `doctor` state is merely unavailable | **Observed false** | Managed-state symlink and runtime receipt/tool/version mismatch previously returned UNVERIFIED | Doctor's UNVERIFIED/FAIL split passed the cross-version focused matrix and real missing-runtime probe |
| Authorizing install scripts proves they executed | **Observed false** | Failed npm could stop before script execution was observable | Evidence records authorization and attempt only; no execution claim without independent observation |
| Direct pushes to the durable experimental branch trigger the template workflow | **Observed false before correction** | Push filter named the review branch but omitted `experimental-graft-variant` | Both branch names are now present; review-branch hosted execution passed in run `33873556873`; a direct durable-branch push was not performed |
| V2 is an OS sandbox | **Observed false** | Process-group supervisor and environment/path controls only | Detached new-session process containment and packet-level network silence are **Unverified** |
| A successful v2 ask is structurally well formed and source-bound | **Observed in focused tests** | Exact keys/types/modes, finite numbers, tracked spans, source code slice binding | Schema validity does not establish semantic completeness |
| V2 Graft output is exhaustive | **Observed false** | Ask 0.30/0.80 micro precision/recall; dynamic/config/package/hidden/duplicate misses | Exact source, exhaustive search, and executable verification remain required |
| F1 reduces context | **Observed false on byte proxy** | Median 3,363 B versus F0 960 B; mean recall 0.748 versus 0.969 | No context-saving claim; exact model tokens/cost **Unverified** |
| Final narrow F1 improves accepted-task correctness | **Unverified** | Trials passed 3/3 in C0 and 3/3 in a broader C1 wrapper; final F1 then failed its first prerequisite build because real Graft omitted tracked `.hidden/visible.py`, so no task agent ran | No observed upstream-condition advantage; final F1 has an observed applicability gap and no accepted-task result |
| Final F1 silently accepts an incomplete tracked-source graph | **Observed false** | On the frozen trial it returned exit 2/FAIL, removed staging, and published no graph when `.hidden/visible.py` was absent | Preserve fail-closed coverage; this safety result does not make F1 generally applicable |
| Public guidance explains the tracked-hidden-directory F1 boundary | **Observed false at trial checkpoint; corrected** | Exact `6966b55` rendered regressions and final `b719459` root/docs gates include the real-0.16 omission, intentional FAIL/no-graph behavior, F0 fallback, and do-not-move/untrack warning | **Observed** |
| MCP adds retrieval accuracy | **Observed false in benchmark** | C2 returned the same file sets/accuracy as C1 and added 4,557 B fresh fixed payload | F2 rejected/disabled |
| V2 adds only bounded persistent discovery context | **Observed template snapshot** | `AGENTS.md` delta +132 characters / +33 proxy tokens; `CLAUDE.md` unchanged | Supported as proxy; actual client tokens **Unverified** |
| No telemetry or network request can occur | **Unverified** | CI/DNT and isolated state are cooperative controls; no packet-complete enforcement | Never claim network silence |
| Native platform support is broad | **Unverified** | Real F1 probes used Linux x86_64 and Node 22.12.0 | macOS, Windows, ARM64, and alternate Node versions remain unverified |
| Final v2 local and hosted validation passes | **Observed** | Exact `b719459` passed 99 template tests, official render, 243-test release on Python 3.12/3.13, package/external-wheel checks, 122 focused adapter tests, README/docs gates, and seeded real lifecycle/removal; identical remote tree passed hosted run `33873556873` | Two fresh connected installs failed inside npm without runtime promotion; connected install/provenance and native non-Linux platforms remain **Unverified** |

## Decision

**Recommended:** preserve F0 as default; retain only narrow F1 as an optional
experiment; reject F2–F6 from the project profile. No token, correctness, blast-radius,
newcomer-comprehension, or productivity improvement is supported.
