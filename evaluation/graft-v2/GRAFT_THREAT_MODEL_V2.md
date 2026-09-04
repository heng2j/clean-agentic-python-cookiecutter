# Enhanced Graft integration threat model

Target: local candidate branch `audit/experimental-graft-variant-v2`, based on
audited commit `ab3e06f6a402a22f51d8447101f245eab258b8e6`.
Final local source is
`b719459a051a60d4af1e4fa30b3c32277fa97b8c` (tree
`35819081108685c24f47ba5251ec7e18004b0016`). Its local cross-version,
late-red-team, README/docs, and seeded real-package boundaries are validated;
remote review commit `4dc3603` has the identical tree and hosted run
`33873556873` passed both supported Python jobs.

## Protected assets and authority

Protected assets are source and Git state; user files outside adapter-owned
state; credentials loaded by the shell or `direnv`; agent context; deterministic
quality evidence; network/privacy choices; dependency identity; and the
human-owned acceptance decision. Graft output is derived navigation evidence,
never project authority.

## Boundaries and disposition

| Boundary | Threat | V2 control | Residual status |
|---|---|---|---|
| Cookiecutter input → generated project | Automatic install, network, or activation | No Graft execution during generation | **Observed:** exact 3.12/3.13 implementation renders and current documentation render passed without Graft execution |
| Parent shell / `.env` → child | Ambient credentials or configuration leak | Minimal allowlist, empty dotenv route, isolated state, no provider surface | **Observed focused tests**; dependency can still read process-readable project files |
| Adapter → Node/npm/Graft | PATH spoof, manifest/lock/CLI tamper, version spoof, unreviewed npm lock interpretation | Exact tool identity, fixed local CLI, npm 10.9.0, exact hashes/integrity, pre/post checks | **Observed focused tests**; exact install failed generically and a separate diagnostic saw `EAI_AGAIN`; causality, connected install, and source-to-dist provenance **Unverified** |
| Project → runtime/graph/evidence | Symlink, hardlink, mode/owner, traversal, out-of-root write | Full path-chain checks, regular-file/type checks, atomic writes, contained owned directories | **Observed focused tests**; external code keeps host filesystem authority |
| Install transaction → existing runtime | Failed install destroys prior runtime or leaves unowned sibling state | Fixed ignored runtime-sibling staging, stale-state rejection, rollback, post-swap validation, durable evidence, five-root removal inventory | **Observed cross-version fault injection and seeded removal**; SIGKILL/connected-install interruption remains **Unverified** |
| Build transaction → existing graph | Partial/stale build replaces prior evidence | Fresh staging graph, strict validation, transaction rollback, graph-tree digest | **Observed cross-version fault injection and held-out fail-closed publication**; real interruption remains **Unverified** |
| User arguments → CLI | Option smuggling, huge/NUL/Unicode/path inputs, no-op success | Parser abbreviation disabled; command-specific bounded schema; no generic remainder | **Observed** in exact cross-version seed matrices |
| Git/source → graph | Untracked or ignored scope marker changes parser behavior; stale branch/worktree reuse; upstream creates root `.ignore` | Git config isolation; tracked-source snapshot; reject untracked files and Graft markers; pass `GRAFT_NO_IGNORE` plus `--no-ignore`; bind controls/commit/status/tree/tool identities | **Observed focused plus real probes:** no root `.ignore`; changed source failed closed; hidden tracked source made F1 unavailable; semantic omissions remain |
| Graft JSON → evidence/context | Malformed, partial, extra, non-finite, unbound, or overbroad output | Strict graph/ask schemas, finite bounds, source span/code binding; `check` projects away 517-item `pendingIds` with count/hash evidence | **Observed focused and seeded-real projection**; semantic completeness is not proven |
| Untrusted metadata/error → public context | Imperative labels, huge identifiers, or escaped malformed Unicode consume/inject context | Count/hash-only public language metadata, generic invalid-value errors, 128-character diagnostic cap, ASCII-safe hashing, explicit untrusted labels | **Observed** in exact late-red-team and final focused tests |
| Local paths → public JSON | Long checkout paths exceed output budget or disclose host layout | `6966b55` uses project-relative managed paths and omits host executable paths in every successful public envelope; durable install/structural-command evidence retains full identity | **Observed:** 4,243 B predecessor failure; exact real check 3,644 B, both-version public probes, and held-out path scan passed |
| Check JSON → agent context | Unknown upstream fields inject imperative prose into a PASS response | Exact reviewed 0.16 key sets; projection excludes upstream prose/identifiers and retains fixed project status/reason plus booleans/counts/hashes | **Observed corrected:** exact cross-version injection and real 3,644-byte projection passed |
| Graft file-node spans → graph validation | Real package convention rejected as invalid, or relaxed bounds admit invalid symbols | Accept exact 0.16 file-kind L1-to-L(raw-newline-count+1); keep symbols within physical source lines and bind returned code | Earlier validator rejected all 38 real file nodes; corrected rule passed the exact seeded real 540-node graph; invalid-symbol matrix passed cross-version |
| Adapter errors/attempts → evidence status | Missing prerequisite, unsafe/tampered state, or failed install is mislabeled or overclaimed | Command-specific FAIL/UNVERIFIED taxonomy, including separate doctor catches; record install authorization/attempt without asserting unobserved execution | **Observed corrected** in exact cross-version and seeded-real status/failing-install matrices |
| Documentation → interpreter | Bare `python` selects unsupported host interpreter and fails before JSON | All public adapter commands use locked `uv run --locked --group dev python`; rendered-doc scan | **Observed fix**; independent newcomer journey **Unverified**; uv remains required |
| uv launcher → adapter | Environment reconciliation occurs before a read-only adapter diagnostic | Locked uv command and prior locked sync; documentation does not call the whole launcher pure | **Qualified boundary:** uv may create/update managed environment state before adapter startup |
| Process → host | Timeout, inherited signal mask, lingering same-group descendants | Active output/deadline supervisor, unblocked child signals, process-group termination | **Observed focused tests and no sampled post-removal residue**; a `setsid` child can escape portable group cleanup: **Unverified containment** |
| npm/Graft → network | Telemetry/update/install requests | `CI=1`, `DO_NOT_TRACK=1`, isolated cache/home, no deep/provider command | Separate same-config diagnostic reached registry and saw `EAI_AGAIN`; exact adapter failure was generic. Seeded lifecycle sampled no socket rows, but controls are not a sandbox and packet silence is **Unverified** |
| MCP/client → agent | Competing instructions, schemas, lifecycle, root mismatch | No MCP command or active example; `.mcp.json` ignored | **Observed design**; direct user configuration is outside repository scope |
| Optional LLM provider → source/credentials/network/cache | Source disclosure, provider-key inheritance, cost, model drift, cached or hallucinated summaries | No F5/deep command, provider credential route, or default model call; minimized child environment | **Rejected/disabled:** F5 was not executed; direct upstream use is outside controls and remains high risk |
| Explainability export → human/shared storage | Stale source-derived artifact, structural disclosure, or persuasive false completeness | No F3 export command or committed graph/map; research outputs stay in ignored evidence | **Rejected in profile:** feasibility probes exist, but human comprehension and safe sharing are **Unverified** |
| Generated graph → human/agent | Incomplete structure treated as exhaustive truth | Only bounded `ask`; advisory labels; exact source/search/test fallback | **Mitigated, not fixed**; dynamic/config/package false negatives persist |
| Removal → user/global state | Recursive cleanup deletes tracked, unrelated, shared, or concurrently created state | Pure inventory, explicit apply, Git tracked-file block, exact receipt authority, unknown-descendant refusal, and repeated full preflight before each target | **Observed:** tracked/race/receipt regressions plus 7,522-path seeded real complete postcondition; same-user post-preflight mutation, connected-install, and hostile detached residue remain **Unverified** |
| Public recovery guidance → source layout | User/agent moves or untracks legitimate hidden source to make F1 build | Version-specific warning, F0 fallback, source-authority and do-not-weaken instructions | **Observed gap in initial held-out trial; exact `6966b55` rendered regression and final `b719459` root/docs gates passed** |
| Local evidence → shared archive | Absolute project/tool/cache/temp paths disclose workstation structure | Public envelopes are path-minimized; durable evidence remains ignored/local and migration requires scrubbing before sharing | **Mitigated operationally**; no automatic archive-redaction proof |
| Third-party child → ignored/out-of-scope filesystem | Dependency writes outside enumerated adapter-owned state | Minimal environment, working directory, receipts, and post-state checks | **Not contained:** prevention requires OS sandboxing; external code retains host authority |

## Process-containment limit

The wrapper is not an operating-system sandbox. Its supervisor can enforce a
deadline and terminate descendants that remain in the reviewed child's process
group. A malicious or compromised child can create a new session or otherwise
escape that group. Portable hard containment was not available in the audit
environment, so termination of such detached processes is **Unverified**.

The exact `6966b55` seeded lifecycle sampled no final visible residue for the
pinned build/check/ask sequence. That observation does not prove containment
against malicious dependency behavior or a process that detached between
samples.

## Supply-chain and privacy residuals

- The exact 0.16.0 npm bytes are identifiable, but tag signature and reproducible
  source-to-dist build provenance are **Unverified**.
- The dependency tree contains 45 packages beyond the root and 12 lifecycle-
  script packages. Installation necessarily executes third-party code.
- The reviewed `tree-sitter-cli@0.23.2` install script can download a
  platform-specific executable from a GitHub release outside npm tarball
  integrity; `GRAFT_SOURCE_INDEX.md` pins the exact script.
- Cooperative telemetry variables do not prove network silence.
- Direct `node`, `npm`, `npx`, or `graft` invocation bypasses the adapter.
- Static analysis does not model every dynamic Python, configuration, packaging,
  generated, ignored, or runtime relationship.
- Native macOS, Windows, ARM64, and alternate Node behavior are **Unverified**.

## Remaining validation boundary

Exact `b719459` local cross-version, late-red-team, seeded-real, README/docs,
and packaging runs exercised the named seed families and integrity checks.
Publication must still bind the source to the hosted branch and Actions run.
Connected installation, native non-Linux platforms, same-user post-preflight
filesystem mutation, packet-level network containment, and missing external
cohorts remain **Unverified**, never pass.
