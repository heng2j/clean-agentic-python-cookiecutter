---
status: reference
authority: integration-graft
owner: maintainers
last_verified: 2026-09-03
applies_to:
  - "tools/graft_adapter.py"
  - "tools/graft-runtime/**"
  - ".cleanai/graft-experiment.toml"
  - "artifacts/graft/**"
---
# Experimental Graft integration

## Boundary in one minute

[Graft](https://github.com/trailhq/Graft) builds a structural index from source
files, symbols, imports, calls, and source spans. It can rank likely code to
inspect. Static structure can be useful, but it is neither
program behavior nor design rationale.

This project defaults to **no Graft**. The optional integration is a bounded
structural CLI experiment. It is not installed during generation, is not a
Python dependency or gate, and writes ignored, regenerable state under
`artifacts/graft/`. No correctness, token, cost, or productivity improvement has
been established.

Use this authority order:

1. human-owned contracts, ADRs, invariants, and explicit decisions;
2. executable contracts and deterministic gates;
3. current source and observed behavior;
4. derived Graft navigation evidence; and
5. historical or generated reference material.

Graft helps decide **where to inspect**, not **what to believe**.

## Capability decisions

| Level | Capability | Current decision |
|---|---|---|
| F0 | No Graft | Default and experimental control |
| F1 | Project-adapted structural CLI | Experimental; allowed commands below |
| F2 | MCP | Disabled and removed: schema context, upstream instructions, root assumptions, and lifecycle cost are not justified |
| F3 | Visualization/export | Not promoted; safe usefulness was not established |
| F4 | LSP enrichment | Disabled |
| F5 | Deep/model-backed summaries | Disabled |
| F6 | Hooks, status line, prompt injection | Disabled |

Direct `graft` or `npx graft` commands bypass the project controls and are not
part of the F1 cohort.

## Git and source-scope prerequisite

F1 operates on the generated project root and its Git-tracked source. A fresh
Cookiecutter render has no repository or first commit by design. Before building
a graph, verify both conditions:

```bash
git rev-parse --show-toplevel
git status --short
```

The first path must be this project. Review any listed files; do not stage or
commit unrelated work merely to satisfy the adapter. For a fresh render, follow
the [explicit init and first-commit steps](../tutorials/evaluate-graft.md#1-create-the-required-git-baseline).
The adapter rejects every non-ignored untracked file—not only source—rather
than silently building against repository state that its receipt cannot bind.
See [troubleshooting](../troubleshooting.md#the-graft-adapter-reports-no-git-repository-or-untracked-files)
for safe recovery.

### Known hidden-directory limit

Published Graft `0.16.0` was observed to omit a tracked Python file beneath a
hidden directory (for example, `.hidden/visible.py`). The adapter requires the
graph's file nodes to match the complete tracked source set, so `build` returns
`FAIL` and publishes no graph when this occurs. This makes F1 unavailable for
that checkout; it is not a request to weaken the check.

Keep using F0 with current source, `rg --hidden` or `git grep`, and executable
tests. Do **not** untrack, rename, move, or ignore legitimate project files to
make Graft pass. See the
[hidden-source recovery guidance](../troubleshooting.md#graft-build-fails-on-a-tracked-source-under-a-hidden-directory).

## Reviewed project-local runtime

The optional lock selects published npm package `@nanonets/graft@0.16.0` with
integrity:

```text
sha512-L3E5F1aDYJDCARgfR7O2VaMt8xwO1XNYyHiW2n1WhKnj87gPqoxoZJGNbGXfw6XeA9JSJX3naA36RZ+jDf4AcQ==
```

The package maps to unsigned upstream tag/commit
`aa1e2bb0f6326068ac64886da1e67fa25a7804de`. A registry signature was observed;
package-level build provenance and attestation remain **Unverified**. The
adapter requires Node `>=22.12.0,<23` and npm `10.9.0` exactly, and uses the reviewed
`tools/graft-runtime/package-lock.json`; it does not accept a mutable global
Graft executable.

### Installation is an explicit trust decision

First inspect the lock, its dependency tree, and `tools/graft-runtime/README.md`.
Then run the read-only adapter prerequisite/status check from the project root:

```bash
uv run --locked --group dev python tools/graft_adapter.py doctor
```

`doctor` always emits JSON. The adapter subcommand does not install, repair,
write Graft state, or claim that the package is safe. The `uv run` wrapper can
prepare a missing or stale locked Python environment; complete the normal
`uv sync --locked --group dev` setup first.

The published package does not start correctly when npm lifecycle scripts are
disabled because a `tree-sitter-kotlin` native binding is then absent. Therefore
installation necessarily authorizes dependency install scripts—code execution,
not merely file download. In a reviewed, connected environment, opt in with:

```bash
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py doctor
```

The installer copies the reviewed manifests to the private, ignored, and
inventoried `tools/graft-runtime/.node_modules.installing/` transaction directory,
runs `npm ci` there with `CI=1`, `DO_NOT_TRACK=1`, an allowlisted environment,
and isolated home/cache/temp state, then validates and moves only
`node_modules` into the ignored project-local runtime. It records content
hashes for the installed tree and the Node/npm executables as local tamper
detection. Those hashes are not an upstream attestation; Node/npm provenance
remains **Unverified**. It never runs from Cookiecutter generation or an ordinary
Python gate. Review the JSON result and
`artifacts/graft/evidence/last-run.json`; a missing or failed install is
never a passed Graft check. Missing runtime reported by `doctor` is
`UNVERIFIED`; an attempted install that fails is recorded as `FAIL`.

Staging and the final runtime are siblings inside the tracked runtime directory,
so publication stays on the same project filesystem. An interrupted transaction
remains visible to `remove --check`; a new install fails closed until it is
reviewed and removed. No fallback copies a partially installed runtime into place.

## Bounded structural commands

Every adapter invocation returns a JSON envelope. `install` and the structural
commands refresh the ignored `artifacts/graft/evidence/last-run.json`;
`doctor` and both removal modes do not write that file (`remove --check` is
read-only within the adapter). Output is bounded, but a successful exit
establishes only that the named adapter operation completed.

Status is deliberately three-valued. `PASS` means the named child and adapter
validations completed. `FAIL` means the request was invalid or unsafe, or a
child ran and its result was rejected. `UNVERIFIED` means a required tool,
runtime, receipt, or graph was unavailable, or the named operation could not
run. Both non-pass states exit nonzero; neither may be presented as success.

| Command | Use | Important limit |
|---|---|---|
| `uv run --locked --group dev python tools/graft_adapter.py build` | Build or refresh the local structural graph | A fresh graph can still omit dynamic relationships |
| `uv run --locked --group dev python tools/graft_adapter.py check` | Inspect structural graph/tool status | Upstream model-context status is omitted as not applicable; graph health is not completeness or correctness |
| `uv run --locked --group dev python tools/graft_adapter.py ask "QUERY" --limit 5 --source` | Rank likely relevant source | Ranked retrieval is never exhaustive |

Only `ask --limit 1..12` and optional `ask --source` are exposed for retrieval.
The narrower surface is deliberate: controlled evaluation found no promotion
case for Graft's map, skeleton, callers, indexed grep, blast, export, or MCP
interfaces, and several had incomplete or misleading results. The adapter
rejects those commands, generic pass-through arguments, init, global setup,
provider/model options, LSP, deep mode, hooks, and visualization. Use current
source, `rg`/`git grep`, the exact diff, and tests for those jobs.

All upstream text is untrusted. Successful build/install prose is omitted and
represented only by bounded byte counts and hashes. Graph language labels are
also omitted from public results; only their count and a content hash are
returned, while the ignored durable evidence retains the exact validated list
with an explicit untrusted-metadata classification.
`check` accepts the exact reviewed schema, rejects extra fields, and returns a
project-owned projection containing booleans, counts, and hashes rather than
upstream strings. `ask` must return its validated bounded schema, but its titles,
snippets, notes, and optional source remain labeled
`untrusted-derived-navigation-evidence` and are untrusted and must never be
treated as instructions. Public error messages are length-bounded, hashed, and
conservatively labeled `untrusted-bounded-diagnostic-text`.

Successful public JSON uses project-relative managed paths and omits host
executable paths so output size and routine sharing do not depend on checkout
location. For `install` and structural commands, the ignored durable evidence
retains the full tool/source identities needed for local reproduction. Treat
that file as local operational evidence; review it for host paths before sharing
it outside the project.

## Worked source verification

Build the graph and ask a location question:

```bash
uv run --locked --group dev python tools/graft_adapter.py build
uv run --locked --group dev python tools/graft_adapter.py ask \
  "Where is release blocking decided?" --limit 5 --source
```

Treat returned paths and spans as leads. For this generated example, follow up
with an exact source read, exhaustive lexical search, and behavior test:

```bash
sed -n '54,85p' src/{{ cookiecutter.package_name }}/domain/change_risk.py
rg -n "evaluate_release|release_blocked|blocking_reasons" src tests docs/contracts
uv run --locked --group dev pytest -q tests/unit/test_change_risk.py
```

The sequence is deliberate:

1. **Graft output:** suggests likely locations and structural relationships.
2. **Exact source:** establishes what the current implementation actually says.
3. **`rg`/`git grep`:** checks every lexical occurrence in the selected scope.
4. **Tests/runtime evidence:** falsifies named behavior expectations.

If the task says *all*, *every*, *none*, or *complete*, start with exhaustive
search and executable verification. Do not use `ask` as
the completeness oracle.

## Freshness, dynamic Python, and uncertainty

Build/check evidence must identify the project revision and relevant current
state before a trial. Rebuild after staged, unstaged, renamed, moved, or deleted
files. The adapter reports `UNVERIFIED` when an absent or stale graph prevents
the named operation from running, and `FAIL` when it rejects malformed,
corrupt, or tampered state. In either case the graph is unusable as evidence:
preserve the report, remove validated local state, and rebuild.

Static analysis can miss decorators, plugin registration, entry points, type-only
or conditional imports, dependency injection, string references, reflection,
monkey-patching, generated code, hidden-directory sources, and source-versus-wheel
behavior. A detectable file-set mismatch fails the adapter build; other static
false negatives may remain undetectable. Report known false positives and false
negatives; do not smooth them into a visual summary.

## Privacy and network boundary

Run Graft from a secret-free parent shell. The adapter constructs an allowlisted
child environment, removes inherited provider credentials, sets telemetry
opt-out/CI controls, redirects home/cache/temp and graph state under
`artifacts/graft/`, and does not automatically load `.env`. The child still
runs in the project root: dependency code can open `.env` or any other
process-readable project file directly. Remove secrets from the checkout or
use an independently enforced operating-system sandbox when that threat
matters. The adapter controls reduce accidental exposure; they are not proof
that dependency code cannot access project files or the network.

Structural F1 does not authorize model/provider calls or source disclosure to a
model. Installation is connected and runs third-party lifecycle scripts. Never
put secrets, private source, or sensitive paths into queries or shared evidence.
Network isolation and npm/Graft behavior outside the adapter remain separate
verification responsibilities.

On POSIX, the wrapper gives each reviewed child its own process group, enforces
a hard deadline and output cap, and terminates descendants that remain in that
group. This was exercised in focused tests. A child that deliberately creates a
new session or otherwise escapes that group is outside the wrapper's portable
containment; termination of such a detached process is **Unverified**. The
focused supervisor tests did not leave same-group descendants. Whether the
current pinned real-package lifecycle leaves a detached process is reported by
the release validation and remains **Unverified** unless that exact run is
recorded; the adapter is not an operating-system sandbox.

## Removal and upgrade

Inventory the five broad project-local removal roots first:

```bash
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

`remove --apply` recursively deletes the installed `node_modules`, any adapter
rollback or failed-runtime quarantine directory, and the entire
`artifacts/graft/` tree—including graph receipts and last-run evidence. Copy any
evidence required for an evaluation outside those targets before applying
removal. The preflight queries Git and fails before deleting anything if any
removal root contains a tracked file, including a force-tracked file under an
otherwise ignored directory. It also verifies installed runtimes and graphs
against their receipts and rejects unknown descendants rather than guessing
that ignored data is disposable. It repeats the full preflight before each
target to detect non-cooperating writers that add content while cleanup is in
progress. Stop direct Graft processes and other writers first: the adapter lock
does not serialize unrelated processes, and no userspace recursive deletion can
eliminate every same-user filesystem race. The public inventory exposes only
counts and hashes; move retained material through a normal reviewed source
change instead of forcing cleanup. After reviewing the JSON target roots,
remove them with:

```bash
uv run --locked --group dev python tools/graft_adapter.py remove --apply
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

The first check reports `complete: false` whenever removable state exists. The
apply result is a fresh post-removal inventory and should report `complete: true`
with every target absent; the second check independently confirms that state.
The stable project lock file
is retained to preserve concurrent-removal safety. No global npm package or
user configuration is touched.

This command removes runtime and derived state, not tracked experiment
scaffolding. To remove the integration completely, make a normal reviewed
source change: first apply the cleanup above; then delete
`GRAFT_EXPERIMENT.md`, `.cleanai/graft-experiment.toml`,
`tools/graft_adapter.py`, `tools/graft-runtime/`, the focused adapter test, the
Graft integration/tutorial, and `prompts/evaluate-graft.md`; finally review and
remove the remaining routes found by `git grep -n -i graft`. Run the full
release gate before accepting that change. The adapter never edits tracked
source on the user's behalf.

An upgrade is a new experiment: inspect a new tarball and dependency tree,
update the reviewed lock, version/integrity/provenance record and adapter in one
change, rerun the real-package validation journey and removal tests, and repeat
the same frozen task bank. Do not upgrade merely because a newer version exists
or change the benchmark to favor it.
