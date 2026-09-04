# Migration guide: original experimental Graft variant to v2

## Who should migrate

Migrate only if you deliberately want to continue the optional F1 structural
CLI experiment. The recommended ordinary workflow remains F0: current source,
`rg`/`git grep`, contracts, tests, and CleanAI gates without Node or Graft.

The enhanced branch starts from original experimental commit
`ab3e06f6a402a22f51d8447101f245eab258b8e6`. It does not modify the original
branch or `main`.

## Important safety warning

Do not run the original adapter's `doctor` or cleanup commands against
unreviewed existing `artifacts/graft` state. The original adapter follows
symlinks and a nominal diagnostic command can overwrite an outside file.

Before adopting v2:

```bash
git status --short
find artifacts/graft -type l -print 2>/dev/null
```

If any symlink is listed, stop and inspect both the link and target. Do not use
a recursive deletion command on a path whose ownership or real target is not
understood. Preserve or commit ordinary user work before migration, but do not
commit Graft graph/runtime artifacts.

## Breaking changes

| Original behavior | Enhanced behavior | Migration effect |
|---|---|---|
| Documented npm `@nanonets/graft@0.17.0` | Published exact `0.16.0` plus reviewed local lock | 0.17.0 never existed as a public npm artifact; do not substitute source `main` |
| Global npm install / PATH executable | Private `tools/graft-runtime` install and fixed local CLI module | Global installs are ignored by the safe adapter |
| Generic `run` plus arbitrary remainder | Closed lifecycle commands plus only `build`, `check`, and bounded `ask` | Scripts must call the explicit adapter subcommands below; broader upstream operations have no replacement |
| Environment-only graph selection | Adapter-owned explicit graph directory and project root | Old graphs are not treated as trustworthy v2 evidence |
| Human/prose output and mutating doctor | Read-only adapter doctor and bounded JSON evidence envelopes | Consumers must parse status/evidence, not scrape upstream prose; the surrounding uv launcher has a separate environment lifecycle |
| MCP example and adapter mode | MCP removed and `.mcp.json` ignored | Disable/remove any local MCP client registration manually |
| Map/skeleton/callers/indexed grep/blast/LSP/deep/viz/init reachable through broad pass-through | No project adapter surface | These were not justified by the evaluation; use source/search/tests or design a separately reviewed cohort |
| Flexible repository positionals | Fixed Git project root and tracked supported source | Commit/stage intentionally; untracked source is rejected rather than silently omitted |
| Hard-coded `origin/main` blast example | Blast removed from the v2 adapter | Existing scripts must use the exact Git diff, exhaustive search, and applicable tests instead |
| Node floor based on mixed claims | `>=22.12.0,<23` | Other Node versions are outside the reviewed profile |

## Preferred migration: render a fresh project

For a template consumer, the safest path is to render the enhanced branch into
a new directory, validate its no-Graft path, and migrate only the project's
human-owned domain source, tests, data, contracts, and decisions.

After the branch is published:

```bash
uvx --from 'cookiecutter==2.7.1' cookiecutter \
  https://github.com/heng2j/clean-agentic-python-cookiecutter \
  --checkout audit/experimental-graft-variant-v2

cd clean-agentic-scientific-python-project
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Compare the new render with the existing project before copying anything. Do
not copy old `.mcp.json`, `artifacts/graft`, a global npm installation, or an
old graph into the new project.

## In-place adoption checklist

If regeneration is impractical, review and port these files as one bounded
change rather than copying the whole template over user work:

- `.cleanai/graft-experiment.toml`
- `.gitignore`
- `tools/graft_adapter.py`
- `tools/graft-runtime/package.json`
- `tools/graft-runtime/package-lock.json`
- `tools/graft-runtime/README.md`
- `tests/tooling/test_graft_adapter.py`
- the Graft integration/tutorial/troubleshooting/glossary routes
- the focused template/CI render regression where applicable

Remove the obsolete `.mcp.json.example`. Keep `.mcp.json` ignored, but first
disable any corresponding tool registration in the actual client. Client or
user-home configuration is outside Git and cannot be proven absent by this
repository.

Run the ordinary Python checks before installing Graft:

```bash
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

A failure here is a Python/project regression, not a reason to install Graft.

## Retire old local and global state

After the new adapter is present, inspect only. The adapter's `remove --check`
path is read-only; the enclosing `uv run` can still reconcile its managed Python
environment before the adapter starts, so first complete the locked sync and do
not describe the whole launcher command as filesystem-pure:

```bash
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

Review every reported target. If it rejects a symlink or unfamiliar path, stop
and resolve ownership manually. Altered/missing receipt fields, tracked files,
and unknown descendants intentionally block deletion. Stop direct Graft and
other writers before cleanup: the adapter lock coordinates adapter commands,
not unrelated processes. If the inventory is exactly the project-local
runtime/graph/evidence state you intend to discard:

```bash
uv run --locked --group dev python tools/graft_adapter.py remove --apply
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

The second check should report `complete: true` with every removable target
absent; its inventory metadata and retained concurrency lock remain. It does not
make recursive deletion an OS sandbox. The adapter repeats its full preflight
before each target, but same-user mutation after the final preflight remains a
residual. It also does not
touch a global npm package or user configuration. The inventory covers installed
`node_modules`, fixed install staging, prior-runtime backup, failed-runtime
quarantine, and `artifacts/graft/`; the stable lock inode is retained for
concurrency safety. A stale transaction is visible and requires review rather
than being silently discarded.

If the original guide led you to install a global package, inspect shared state
before changing it:

```bash
npm list -g @nanonets/graft --depth=0
```

Only the person who owns that global environment should decide whether to run
`npm uninstall -g @nanonets/graft`; doing so may affect other projects. The v2
adapter neither depends on nor removes it.

## Install the reviewed optional runtime

First verify Node/npm and the adapter's read-only diagnostic report:

```bash
node --version
npm --version
uv run --locked --group dev python tools/graft_adapter.py doctor
```

The reviewed profile requires Node `>=22.12.0,<23`; installation additionally
requires npm `10.9.0` exactly. A not-ready doctor result is
not a Python failure and must be reported as **Unverified** for Graft.
Other npm versions and Node/npm combinations require a new qualification; a
syntactically valid version is not evidence of equivalent lock or lifecycle
behavior.

Provisioning the exact Node/npm pair is intentionally not automated by this
Python template. If npm is not exactly 10.9.0, stop and treat F1 as
**Unverified** until a maintainer selects a project-appropriate, reviewable
toolchain route; do not silently substitute another version or global Graft.

Read `tools/graft-runtime/README.md` and review the lock. Installation is an
explicit connected trust decision because native npm lifecycle scripts execute:

```bash
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py doctor
```

The adapter sets CI/telemetry controls before install and isolates state, but it
is not an OS sandbox. Do not run the install from a sensitive/untrusted source
tree or assume the controls prove network silence.

Successful public JSON now uses project-relative managed paths and omits host
executable paths, so its size/privacy behavior does not depend on checkout
length. Ignored durable evidence for install and structural commands can still
contain absolute project, executable, cache, or temporary paths. Treat it as
local diagnostic evidence and scrub such paths before sharing an archive.
Adapter-owned path checks also cannot prevent a malicious dependency from
writing some other ignored or out-of-scope path with the host process's
authority; that requires OS-level filesystem/network/process containment, which
this profile does not provide.

The adapter uses `/dev/null` for npm user configuration and a distinct empty
adapter-owned global configuration file. Do not collapse both roles back to
`/dev/null`; npm 10.9 rejected that configuration in the real-package probe.

## Create the Git/source baseline

The F1 graph binds to the generated project root and tracked source. For a fresh
render only, after reviewing every file and choosing the correct identity:

```bash
git init -b main
git add .
git commit -m "Initial generated project"
git status --short
```

Do not stage unrelated work merely to satisfy the adapter. In an existing
repository, use its current reviewed commit and preserve its dirty-state policy.

## Command mapping

| Original call | Enhanced call |
|---|---|
| `... doctor --json` | `uv run --locked --group dev python tools/graft_adapter.py doctor` |
| `... run build` | `uv run --locked --group dev python tools/graft_adapter.py build` |
| `... run check --json` | `uv run --locked --group dev python tools/graft_adapter.py check` |
| `... run ask "QUERY" --source` | `uv run --locked --group dev python tools/graft_adapter.py ask "QUERY" --limit 5 --source` |
| `... run map/skeleton/callers/grep/blast ...` | No v2 adapter command; use exact source, `rg`/`git grep`, `git diff`, and tests |
| `... mcp` | No replacement; F2 is disabled |

For regex, hidden paths, unsupported file types, or exhaustive repository
claims, use explicit `rg`/`git grep` instead of bypassing the adapter.

Real Graft 0.16 was observed omitting a tracked Python file beneath a hidden
directory. The hardened adapter treats that as `FAIL` and publishes no graph.
If this occurs, remain on F0, inspect authoritative source with
`rg --hidden`/Git, and report F1 unavailable. Do not move, rename, or untrack
source merely to make the optional integration build.

## Verify one result correctly

```bash
uv run --locked --group dev python tools/graft_adapter.py build
uv run --locked --group dev python tools/graft_adapter.py ask \
  "Where is release blocking decided?" --limit 5 --source
```

V2 sets `GRAFT_NO_IGNORE` and supplies upstream `--no-ignore`. A build must not
create a root `.ignore`; treat such a file or any write outside
`artifacts/graft/` and the private runtime as a failed boundary, not harmless
tool setup.

Use returned paths as leads, then verify:

```bash
rg -n "evaluate_release|release_blocked|blocking_reasons" src tests docs/contracts
uv run --locked --group dev pytest -q tests/unit/test_change_risk.py
```

For an exhaustive or packaging claim, add the relevant complete search and
installed-wheel/runtime evidence. Never infer "none" from an empty graph result.

## Replace old blast automation

The v2 adapter does not expose upstream blast. Replace old automation with an
explicit reviewed base and independently verifiable evidence:

```bash
BASE_REF="$(git rev-parse HEAD)"
git rev-parse --verify "${BASE_REF}^{commit}"
git diff --stat "$BASE_REF" --
git diff "$BASE_REF" -- src tests
rg -n "KNOWN_CONTRACT_OR_SYMBOL" src tests docs/contracts
```

Then run the applicable focused and project gates. A Git diff and lexical
search still require human scope judgment; they are not complete semantic impact
proof.

## Rollback

Rollback means returning to F0, not restoring the unsafe adapter:

1. stop using F1 and preserve any audit record needed for review;
2. run the enhanced `remove --check` and review the exact local targets;
3. run enhanced `remove --apply` only when the inventory is safe;
4. remove the migration commit through the repository's normal reviewed Git
   workflow; and
5. rerun the ordinary locked fast/release path without Node/Graft.

Do not re-enable the original broad adapter, global install, MCP example, deep
mode, or automatic hooks to recover convenience.

## Residual limitations after migration

- Static Graft output remains incomplete for duplicate symbols, dynamic Python,
  configuration, packaging, hidden paths, and generated/ignored material.
- The locked npm runtime remains large and executes native lifecycle scripts.
- Same-process-group descendants are supervised, but a deliberately detached
  new-session process can escape portable cleanup; the adapter is not an OS
  sandbox.
- Published build provenance, live vulnerability status, packet-level network
  silence, macOS/Windows/ARM64, and real LSP remain **Unverified**.
- Deterministic benchmark results did not show a context or retrieval advantage
  over F0.
- Final v2 release validation numbers and their source-versus-report commit
  boundary must be taken from the validation report, not this migration guide.
