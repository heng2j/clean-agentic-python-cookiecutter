# Graft variant changelog

## Enhanced experimental candidate

Base: `experimental-graft-variant` at
`ab3e06f6a402a22f51d8447101f245eab258b8e6`

Target branch: `audit/experimental-graft-variant-v2`

F0 remains the default. V2 retains only a bounded F1 structural CLI experiment;
F2–F6 are not product features. Exact final local source `b719459` passed the
template, Python 3.12/3.13 generated release, late-red-team, README/docs, and
seeded real-package boundaries. Remote review commit `4dc3603` has the identical
tree, and hosted Actions run `33873556873` passed Python 3.12 and 3.13. Fresh
connected installation success remains **Unverified**.

Stable-report publication commit `f0b13fc` passed the same hosted matrix in run
`33874894406`; it changed no generated-project implementation path.

### Final red-team closure

- Minimized successful public graph language metadata to count/hash evidence;
  exact labels remain explicitly untrusted in ignored durable evidence
  (`GRAFT-V2-017`).
- Removed absolute Node/npm paths from successful public install JSON while
  retaining exact local identities in durable evidence (`GRAFT-V2-018`).
- Replaced reflected graph identifiers with generic errors plus count/hash
  evidence, reduced diagnostic text to 128 characters, and made omitted-value
  hashing ASCII-safe (`GRAFT-V2-019`).
- Added a Git preflight that blocks all cleanup when any removal target contains
  a tracked file, including force-tracked content under ignored paths
  (`GRAFT-V2-020`).
- Repeats full tracked/ownership preflight before each target deletion to catch
  the reproduced cross-target writer race; public docs require stopping direct
  Graft and unrelated writers (`GRAFT-V2-021`).
- Requires exact install-receipt keys, authority, tool keys, and identity field
  shapes for both runtime use and deletion authority (`GRAFT-V2-022`).
- Rejects lone-surrogate graph metadata before graph publication and preserves
  the prior complete graph/receipt on failure (`GRAFT-V2-023`).
- Expanded the generated README and root README with the no-Graft default,
  short deliberate opt-in, authority/trust boundary, safe removal, and observed
  Graft 0.16 hidden-directory limit.
- Final results: 99 template tests; 243 generated tests per supported Python;
  122 focused adapter tests; 94.97% product and 83.25% harness coverage; six
  killed mutants; clean package and external-wheel checks. A seeded real 0.16
  runtime built 569 nodes/1,783 edges and removed 7,522 receipt-bound paths with
  zero unknown descendants.
- Two final connected install attempts returned `FAIL` on npm's internal
  “Exit handler never called” error and promoted no runtime. This remains
  `UNVERIFIED`, not silently converted to a seeded install pass.

### Narrowed capability surface

- Replaced generic upstream argument forwarding with exact project commands:
  `doctor`, `install --apply`, `remove --check/--apply`, `build`, `check`, and
  bounded `ask` (`GRAFT-O-004`, `GRAFT-O-007`).
- Removed project exposure for upstream map, skeleton, callers, indexed grep,
  blast, visualization/export, LSP, deep/model mode, init, hooks, status lines,
  prompt injection, generated instructions, and MCP (`GRAFT-O-010`,
  `GRAFT-O-011`, `GRAFT-O-015`).
- Kept exact source, `rg`/`git grep`, the Git diff, tests, and package/runtime
  checks as the required route for exhaustive or behavioral conclusions.

### Dependency and installation boundary

- Replaced unavailable `@nanonets/graft@0.17.0` with published exact 0.16.0 in
  a private project-local npm lock (`GRAFT-O-003`).
- Bound execution to the fixed local CLI module and verified package name,
  version, entry point, integrity, full lock, CLI bytes, installed-tree digest,
  and Node/npm/Git identities (`GRAFT-O-005`).
- Required explicit `install --apply`; generation, `uv sync`, Python gates,
  hooks, packaging, and release do not install or require Graft.
- Staged installation at the fixed ignored runtime sibling
  `tools/graft-runtime/.node_modules.installing`, atomically swapped validated
  `node_modules`, and retained rollback state through pre-commit validation and
  evidence publication (`GRAFT-O-014`). A failure while discarding an old
  backup after commit leaves the validated new runtime active and the stale
  backup visible for review; it does not pretend to roll back a partially
  removed backup.
- Narrowed the reviewed optional runtime to Node `>=22.12.0,<23`
  (`GRAFT-O-018`).

### Filesystem, environment, and process safety

- Replaced ambient environment inheritance with an allowlist, isolated
  project-owned home/cache/temp, `CI=1`, and `DO_NOT_TRACK=1`
  (`GRAFT-O-002`, `GRAFT-O-013`).
- Added canonical path-chain, owner/mode/type, symlink/hardlink, containment,
  and atomic-write checks (`GRAFT-O-001`, `GRAFT-O-006`).
- Added active output/deadline supervision, unblocked child signals, process-
  group cleanup, selector-failure cleanup, and explicit timeout/output evidence.
  A child that creates a new session can escape portable group cleanup; the
  adapter remains explicitly not an OS sandbox.
- Added read-only adapter removal inventory and explicit project-local apply.
  Global packages and user/client configuration are not modified.

### Source, graph, and output evidence

- Bound graph receipts to Git identity, tracked-source/status/tree snapshots,
  supported-file hashes, runtime identities, configuration, and the entire graph
  tree rather than only selected files.
- Rejected untracked files and ignored/untracked Graft scope-marker files so
  hidden parser-scope changes cannot enter an unbound build.
- Built into a fresh staging graph and preserved the prior graph/receipt until
  the new graph and evidence were fully validated and durable.
- Added exact graph and ask JSON schemas, finite numeric bounds, required node/
  edge fields, supported source coverage, source span checks, body hashes, and
  `--source` code-slice binding (`GRAFT-O-016`).
- Removed upstream self-reported token-savings text from project evidence.

### Context, documentation, and evaluation

- Added one concise `AGENTS.md` discovery route; Graft detail remains on demand.
  The current delta from the original is +132 characters / +33 character-based
  proxy tokens. `CLAUDE.md` remains a delegation (`GRAFT-O-017`).
- Added an explicit install trust decision, direct-bypass warning, privacy and
  no-sandbox boundary, worked `ask` → source → exhaustive search → test sequence,
  freshness/corruption recovery, upgrade review, and removal path
  (`GRAFT-O-012`, `GRAFT-O-015`).
- Distinguished derived-state removal from full retirement of tracked Graft
  scaffolding, which requires a normal reviewed code change and a residual
  search. Qualified the read-only adapter checks from the enclosing uv launcher's
  possible managed-environment reconciliation.
- Removed a prompt/MCP contradiction and documented the intended status contract:
  malformed/unsafe requests and observed child failures are FAIL; genuinely
  absent, stale, or unrun prerequisites are UNVERIFIED.
- Documented that ignored evidence can contain absolute workstation paths and
  must be scrubbed before sharing; project path checks are not OS containment
  against arbitrary dependency writes.
- Labeled the repository friction ledger visible smoke instrumentation, not a
  blinded causal experiment; held-out acceptance stays external (`GRAFT-O-009`).
- Preserved the 144-record deterministic comparison and six held-out agent
  trials. The broader research C1 did not beat F0 on precision, recall, or byte
  proxy; accepted-task correctness was 3/3 in each cohort with source/search
  fallback in every C1 run. That wrapper exposed `grep` and `callers`, which
  final F1 removes, so accepted-task behavior for the final adapter remains
  **Unverified**. No context, token, cost, or correctness-improvement claim is
  made.
- Ran the frozen final-F1 applicability trial. Real Graft 0.16 omitted tracked
  `.hidden/visible.py`; the adapter returned exit 2/FAIL, removed staging, and
  published no graph. The preregistered stop rule prevented `check`, `ask`, or a
  task agent from running. This preserves the fail-closed invariant but leaves
  accepted-task correctness/scope/cost **Unverified** and narrows the promotion
  case further.

### Defects found during v2 falsification

These were found by rerunning tools, not by aesthetic review:

- The first generated candidate had a Ruff import-order finding and formatting
  mismatch. The files were formatted and the import order corrected; exact
  Python 3.12/3.13 rendered release matrices passed.
- Pyrefly reported eight adapter diagnostics. Handler, stream, path, and list
  types were made explicit; exact Python 3.12/3.13 release matrices passed.
- npm 10.9 rejected identical user/global `/dev/null` config paths during the
  version probe. V2 now uses distinct paths—`/dev/null` for user config and an
  adapter-owned empty global config file—and asserts their identities. The real
  version probe passed. The exact install failed with npm's generic internal
  error; a separate same-config diagnostic observed registry `EAI_AGAIN`, so
  causality and connected installation remain **Unverified**.
- Real Graft 0.16 could create a root `.ignore` file. V2 now sets
  `GRAFT_NO_IGNORE` and supplies `--no-ignore`, binds that choice into receipts,
  and adds regression coverage. The seeded real lifecycle created neither root
  `.ignore` nor root `.graft`.
- Real `check --json` returned 34,206 bytes / 539 lines, including 517
  `graph.pendingIds`, while its useful projected result was about 310 bytes. V2
  omits that list from the public result and records its path, count, and hash
  alongside raw-output byte/hash evidence; seeded real check passed the compact
  projection.
- The same check boundary (`GRAFT-V2-013`) accepted and echoed arbitrary unknown
  keys, including imperative text. Exact reviewed 0.16 schemas and a
  projection with fixed project-owned status/reason plus booleans/counts/hashes
  is implemented; validated `ask`
  strings and failure diagnostics remain bounded, explicitly UNTRUSTED data.
- Failed real installs had left three random sibling staging directories outside
  projects, one with a complete `node_modules`. Staging is now a fixed ignored
  runtime sibling; stale transaction state fails closed; staging, backup, and
  quarantine participate in removal inventory and postconditions. Seeded real
  removal reached `complete: true`; abrupt connected-install residue remains
  **Unverified**.
- Bare public `python tools/graft_adapter.py` commands could select unsupported
  host Python 3.11 and fail before emitting JSON. Every public example now uses
  `uv run --locked --group dev python`, with rendered-doc regression coverage.
- A fake npm 99.0.0 could produce a plausible locked tree and receive PASS. The
  installer now requires npm 10.9.0 exactly before replacement; other versions
  remain unverified. The exact connected install failed with a generic npm
  error; a separate same-config diagnostic returned DNS `EAI_AGAIN`, which is
  a plausible contributor rather than a proven cause.
- Published Graft 0.16 represents file nodes (`GRAFT-V2-009`) as line 1 through
  raw-newline-count plus one. The former validator rejected all 38 real file
  nodes. V2 accepts
  exactly that file-kind convention while keeping symbol spans within real
  lines and source-code slices bound; the exact seeded real 540-node build
  passed.
- Blanket precondition handling (`GRAFT-V2-010`) conflated invalid/unsafe FAIL
  states with missing/unrun UNVERIFIED states. A dedicated general taxonomy and
  exact missing/stale/unsafe/child-failure expectations were added. Real missing
  doctor returned UNVERIFIED, while changed-source and tampered-graph operations
  failed closed; remaining adversarial states rely on focused tests.
- A failed npm attempt (`GRAFT-V2-011`) claimed lifecycle scripts executed even
  when execution was not observed. Evidence now records only
  `install_scripts_authorized=true` and `npm_ci_attempted=true`; it makes no
  execution claim without independent evidence.
- The workflow push filter (`GRAFT-V2-012`) omitted the durable experimental
  branch. It now
  includes both `experimental-graft-variant` and the temporary review branch;
  hosted review-branch run `33873556873` passed both supported Python jobs.
- A subsequent command-specific check (`GRAFT-V2-014`) found that `doctor`
  still mapped unsafe managed-state symlinks and runtime receipt/tool/version
  tamper to UNVERIFIED. It now preserves UNVERIFIED only for missing/unsupported
  prerequisites and returns FAIL for rejected/tampered state; exact cross-
  version and seeded-real status matrices passed.
- The frozen final-F1 trial exposed a public-guidance gap (`GRAFT-V2-015`): real
  Graft 0.16 omits tracked Python under hidden directories, making the hardened
  build intentionally unavailable, but generated docs did not state the
  limitation or recovery. The generated guidance now gives concise F0/source-
  authority/do-not-move-or-untrack recovery; exact rendered regressions, the
  historical `4bba7c0` matrix, and final `b719459` README/docs gates passed.
- A long-parent rerun (`GRAFT-V2-016`) produced a 4,243-byte public `check`
  envelope—above the unchanged 4 KiB limit—solely because absolute host paths
  expanded. `6966b55` now uses project-relative managed paths and omits host
  executable paths across every successful public JSON envelope while retaining
  full identity for install and structural commands in durable ignored evidence.
  Long-path, doctor, and removal regressions preserve the original bound and
  privacy boundary; exact Python 3.12/3.13, real-package, and held-out path
  assertions passed.

### Residual and unverified

- The final template adapter is 3,564 lines / 131,756 bytes (157 top-level
  classes/functions), with a 2,066-line / 76,169-byte focused test file. Ruff
  C901 is configured, but adapter-specific CRAP remains **Unverified** because
  the ordinary sensor scans product source.
- The locked runtime retains 45 packages beyond the root, 12 lifecycle-script
  packages, native code, and approximately 375 MiB observed install cost.
- Source-to-package build provenance, current vulnerability intelligence,
  packet-level network silence, and hostile detached-process containment remain
  **Unverified**.
- Native macOS, Windows, ARM64, alternate Node versions, real LSP, deep/model,
  and human-participant cohorts remain **Unverified**.
- Exact `b719459` source passed Python 3.12/3.13 no-Graft release, final focused
  regressions, README/docs, package/external-wheel, and seeded-real
  lifecycle/removal boundaries. Connected install/provenance, accepted-task
  correctness and token/cost benefit for final F1, hosted Actions,
  charter-complete per-command metadata, independent newcomer comprehension,
  and native non-Linux platforms remain **Unverified**.
- The per-target cleanup preflight resolves the reproduced cross-target race,
  but it is not OS confinement. A same-user writer that mutates a target after
  its last preflight remains a documented residual; stop unrelated writers.

The recommendation remains: keep F0 default, retain only narrow F1 as an
optional experiment, and reject F2–F6 from the project profile.
