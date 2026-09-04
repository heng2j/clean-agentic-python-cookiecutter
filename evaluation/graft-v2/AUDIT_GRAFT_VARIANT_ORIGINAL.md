# Audit of the original experimental Graft variant

## Executive verdict

**Observed:** the frozen branch at
`ab3e06f6a402a22f51d8447101f245eab258b8e6` is **not credible for use**, even
as a newcomer-facing experiment. It has two P0 findings, thirteen P1 findings,
and three P2 findings. The adapter can overwrite files outside its intended
state directory through symlinks and exposes arbitrary ambient credentials to
the external npm program. Its required package version is unavailable, most
advertised commands are miswired, and all canonical generated-project gates
are red.

There are useful positive controls: no automatic Cookiecutter-time install,
Graft is absent from the Python dependency/gate boundary, upstream `init`, deep
mode, hooks, and prompt mutation are not enabled, graphs are ignored, persistent
agent files remain concise, and the documentation repeatedly calls Graft
derived navigation evidence rather than authority. Those controls do not
offset the P0/P1 failures.

## Frozen identity

| Item | Observed identity |
|---|---|
| Experimental head | `ab3e06f6a402a22f51d8447101f245eab258b8e6` |
| Intended parent / merge base | `72a7e52eb0e2ac35ef4ca36f716dc2e183afc6c4` |
| Main | `f0d505f9304c0ff42f3cb79deac461b42b7ac3e9` |
| Declared Graft | npm `@nanonets/graft@0.17.0`, upstream `05760b07...` |
| Published Graft at audit | npm/tag `0.16.0`, upstream `aa1e2bb0...` |
| Governing charter SHA-256 | `8dd3e4c95d72ec3675a7b0c8ebebc12ba4e287f8eb1037c5787b1a294ab537a4` |

The detached audit worktree stayed clean and read-only. The manifest contains
SHA-256 values for all 160 tracked files. Commands ran only in isolated copies,
renders, fixtures, or package quarantine directories.

## Environment and evidence boundary

**Observed:** Linux 6.18.35 x86_64; CPython 3.12.13; uv 0.11.33; Git
2.51.1; Node 24.19.0 and independently provisioned Node 22.12.0; npm 11.9.0;
Bash 5.2.21. Graft was absent from the baseline PATH. Credential-like names,
never values, were inventoried; adversarial tests used synthetic values only.

Network syscalls were not packet-captured or blocked for every command.
Consequently, “no observed request” is not a network-silence claim. Native
macOS, Windows, ARM64, and original Python 3.13 execution are **Unverified**.

## Exact baseline reproduction

| Workflow | Exit / result | Classification |
|---|---|---|
| Template `uv lock --check` | 0 | **Observed** |
| Template locked sync/test | 0; 97 tests | **Observed** with task-local cached artifacts after a recorded cold DNS failure |
| Template build/Twine | 0 / 0 | **Observed** |
| Official default render | 0 | **Observed** |
| Non-default render | 0 after an intentionally invalid reserved email was rejected | **Observed** |
| Generated lock/sync | 0 / 0 | **Observed** |
| Healthy/blocked CLI | expected 0 / 1 | **Observed** |
| Generated direct pytest, no Graft | 125 passed | **Observed** |
| Generated build/Twine, no Graft | 0 / 0 | **Observed** |
| `gauntlet fast/full/hardening/release` | all exit 1 at the same Graft-test Ruff format defect | **Observed failure** |
| Missing-Graft doctor | exit 2 | **Observed controlled failure**, but not JSON |
| Original first-run semantic mutant | before/mutated/restored 0/1/0 | **Observed** |
| Final first-run fast | 1 due independent formatter defect | **Observed failure** |
| Python 3.13 original gates | not run | **Unverified** |

## Trust-model verdicts

| Principle | Repository evidence | Executable enforcement | Original behavior | Verdict | Required fix |
|---|---|---|---|---|---|
| Optional/removable | No Python dependency; ignored graph | Direct pytest/build pass without Graft | Global npm install/removal and unignored MCP config | Partial | Project-local lock, local cleanup, ignore/disable activation |
| No automatic init/hooks/deep | Written guide and denylist | No generated invocation | Positive control held | Pass within reviewed version | Preserve with closed schemas |
| Project-scoped writes | Artifact paths | None against symlinks | Outside overwrite reproduced | Fail P0 | Canonical/lstat confinement and atomic writes |
| Private environment | Eight-key denylist | Synthetic env probe | Arbitrary secrets inherited | Fail P0 | Minimal allowlist |
| Reproducible tool | Version/commit prose | PATH semver probe | npm pin E404; fake accepted | Fail P1 | Local exact lock and fixed module path |
| Fail-closed commands | Denylist | Broad `REMAINDER` | Help/version false zero and bound bypass | Fail P1 | Typed schemas and postconditions |
| Fresh derived evidence | Hash refresh setting | Upstream behavior | Ordinary edits detected, but refresh/read failure may still return zero | Partial | Independent freshness/status evidence |
| Graft is not authority | Repeated guide/prompt language | No generated graph in docs | Strong prose boundary | Pass | Preserve and require source/test fallback |
| Concise context | Persistent files unchanged | Context audit | Low delta but feature orphaned; MCP excluded | Partial | One short route, honest runtime inventory |
| Comparable experiment | Tutorial declares controls | Friction ledger | Oracle leak and missing controls | Fail P1 | External held-out oracle and preregistration |

## Most consequential findings

- `GRAFT-O-001` P0 — symlink-following outside overwrite, including from
  `doctor`.
- `GRAFT-O-002` P0 — arbitrary `direnv`/shell secrets inherited by CLI/MCP.
- `GRAFT-O-003` P1 — documented 0.17.0 npm artifact does not exist.
- `GRAFT-O-004`/`005`/`006` P1 — open argument surface, spoofable executable,
  and source-scope escape.
- `GRAFT-O-007` P1 — six of nine advertised operations do not reliably address
  the built graph.
- `GRAFT-O-008` P1 — every canonical generated gate is red while 97 template
  tests pass.
- `GRAFT-O-009` P1 — evaluation leaks its oracle and does not enforce declared
  controls.
- `GRAFT-O-010`/`011` P1 — MCP has an unbounded competing context/write surface
  and commit-prone activation.
- `GRAFT-O-013`/`014` P1 — install-time telemetry order and large scripted/native
  dependency surface are not safely represented.
- `GRAFT-O-015` P1 — structural false negatives materially limit blast-radius
  and exhaustive-change use.

All 18 structured findings, reproductions, impact, root causes, fixes, tests,
and tradeoffs are in `FINDINGS_GRAFT_VARIANT_ORIGINAL.json`.

## Explainability checkpoint

**Observed:** on the preregistered adversarial Python fixture, `ask --source`
had file-level micro precision 12/40 (0.30) and recall 12/15 (0.80). A
duplicate-name callers query had precision and recall 0, returning one legacy
false edge while missing two real callers. Duplicate-symbol blast found 0/4
known downstream nodes; a unique static control found 3/3. Decorator/registry,
computed-import, TOML CLI entry-point, wheel resource, and hidden-file behavior
were absent. Cycles and unique direct static calls were represented correctly.

Freshness correctly detected and refreshed an unstaged edit, staged move,
deletion, and untracked addition in the fixture. A no-server LSP run exited 0
with no additional edges and only `lsp:none`, so LSP value is **Unverified**.
Static exports were generated but inherit the same omissions.

## Source and package checkpoint

**Source-supported:** published Graft imports dotenv configuration, performs
update upkeep for ordinary CLI commands, has opt-out telemetry, and its npm
postinstall can queue an install event and launch a detached flush unless a
gate such as CI or `DO_NOT_TRACK` is present before installation. Upstream MCP
adds instructions, exposes independent schemas, and performs upkeep at boot.

**Observed:** a reviewed 0.16.0 lock resolves 45 transitive packages beyond the
root package and marks 12 packages with install scripts. Node 22.12.0 was needed
for the functional Linux fixture; the declared root Node `>=20` floor conflicts
with Commander's `>=22.12` floor. The original global install approach is
therefore rejected. A project-local exact lock is the only proportionate option
worth testing, and remains experimental.

## Original recommendation

Keep F0 (no Graft). Replace the F1 wrapper and dependency path before any more
productivity evaluation. Disable F2 MCP. Keep F3 export isolated and advisory.
Leave F4 LSP unverified and disabled. Reject F5 deep/model summaries and F6
hooks/prompt injection by default. Do not claim context or token savings until
the same held-out task is independently correct, accepted, reviewable, and
measured end-to-end.
