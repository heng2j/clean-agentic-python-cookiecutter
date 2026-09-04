# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

This is a small open-source scientific Python starter for changes made with
people and coding agents. It turns selected rules into executable checks, keeps
decisions near the code, and asks every role to return exact evidence and
remaining risk.

> **Independent and unofficial.** The public six-role workflow is described on the jointly credited Justin Martin and Robert C. Martin Clean Coders Episode 6 page. This repository's Python tools, thresholds, prompt contract, architecture example, and evidence format are local synthesis. The project is not authored, sponsored, or endorsed by Robert C. Martin, Justin Martin, Clean Coders, Matt Pocock, OpenAI, Anthropic, or the cited researchers.

## First run

Supported and tested here: Linux x86_64 with CPython 3.12 and 3.13. Native macOS and Windows are not claimed by this release.

```bash
cd {{ cookiecutter.project_slug }}
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Expected: the supplied reviewed `uv.lock` matches the declarations, installation succeeds without re-resolution, and the fast gate exits `0` with a ledger under `artifacts/`. Run plain `uv lock` only as a deliberate dependency update, review the diff, and rerun release validation.

Try the installed behavior:

```bash
uv run --locked --group dev {{ cookiecutter.package_name }} examples/healthy-evidence.json
# expected exit: 0

uv run --locked --group dev {{ cookiecutter.package_name }} examples/blocked-evidence.json
# expected exit: 1 (the policy correctly blocks release)
```

Start with the [first-run tutorial](docs/getting-started/first-run.md). It includes an intentional failure, the exact diagnostic, recovery, and success path.

## Optional Graft experiment

This project works fully without Graft. Its default path remains current source,
`rg`/`git grep`, human-owned contracts and decisions, tests, and deterministic
CleanAI gates. The optional experiment pins published
[`@nanonets/graft` 0.16.0](https://github.com/trailhq/Graft) behind a
project-owned adapter. It can rank likely places to inspect, but its output is
derived, untrusted navigation evidence—not authority, exhaustive search,
observed behavior, or design rationale.

### Short setup

Read [the experiment entry point](GRAFT_EXPERIMENT.md) and its native
install-script warning first. Then, from a clean Git worktree:

```bash
# Read-only prerequisite and status check; missing Graft is UNVERIFIED.
uv run --locked --group dev python tools/graft_adapter.py doctor

# Connected and explicit: install only the reviewed project-local lock.
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py build
uv run --locked --group dev python tools/graft_adapter.py ask \
  "Where is release blocking decided?" --limit 5 --source
```

Graft is not installed by Cookiecutter, required by Python packaging, or run by
any quality gate. Deep/model-backed work, MCP, LSP, hooks, prompt injection,
global configuration, and committed graph output remain disabled. Public JSON
uses project-relative paths, omits or hashes unnecessary upstream metadata,
and labels retained text as untrusted.

Before removal, stop direct Graft and other writers, preserve any evidence you
need, and review:

```bash
uv run --locked --group dev python tools/graft_adapter.py remove --check
uv run --locked --group dev python tools/graft_adapter.py remove --apply
uv run --locked --group dev python tools/graft_adapter.py remove --check
```

Cleanup fails closed for tracked files, unknown descendants, or altered
ownership receipts. Published Graft 0.16.0 was observed to omit a tracked Python
file beneath a hidden directory; the adapter rejects that graph. Keep using the
default workflow rather than moving, untracking, or ignoring legitimate source.
No accepted-task correctness, token, cost, or productivity improvement has yet
been established, so this integration remains optional and experimental.

## Optional project environment with `direnv`

[`direnv`](https://direnv.net/) loads reviewed, project-specific shell settings
when you enter this directory and unloads them when you leave. After `uv sync`,
the supplied `.envrc` puts the existing `.venv` on `PATH`, avoiding repeated
manual activation and reducing accidental cross-project configuration.

First [install `direnv`](https://direnv.net/docs/installation.html),
[hook it into your shell](https://direnv.net/docs/hook.html), and restart the
shell. Then run:

```bash
# Review .envrc before authorizing it.
direnv allow

# Optional: create a private, project-local environment file.
cp .env.example .env
# Edit .env, then uncomment this line in .envrc: dotenv_if_exists .env
direnv allow
```

The `.env` loading line is deliberately commented out by default. `direnv`
does not encrypt or isolate secrets: values exported from `.env` are inherited
by tests, scripts, and coding agents launched from this directory. Use
least-privilege project credentials, keep `.env` untracked, and see the
[data and secret handling guide](docs/science/data-and-secrets.md) before
enabling it.

## Scientific workspace

| Path | Contract |
|---|---|
| `src/{{ cookiecutter.package_name }}/` | installed, reusable product code |
| `notebooks/` | exploration and demonstrations; never the sole home of reusable logic |
| `static/` | small redistributable inputs registered by source, license, and SHA-256 |
| `results/` | generated output ignored by default; curated references require provenance review |
| `scripts/` | thin, documented entry points around tested package behavior |

`python tools/cleanai.py science-audit --strict` checks the shipped layout,
dotenv ignore rules, and static-input manifest. It checks internal consistency,
not scientific truth. Read the [scientific method contract](docs/science/scientific-method.md)
and [reproducibility guide](docs/science/reproducibility.md) before treating an
output as evidence.

The workspace and tool candidates were inspired by Jonathon Vandezande's
[*Setting Up Python Packages*](https://jevandezande.github.io/blog/setting-up-python-packages/),
his Rowan Scientific article
[*How to Make a Great Open Source Scientific Project*](https://www.rowansci.com/blog/how-to-make-a-great-open-source-scientific-project),
and his [`uv-cookiecutter`](https://github.com/jevandezande/uv-cookiecutter).
They were independently evaluated and adapted; see
[ADR 0004](docs/adr/0004-scientific-open-source-profile.md) and the
[source record](docs/research/scientific-source-traceability.md).

## What the gates mean

| Profile | Offline/deterministic intent | Purpose |
|---|---|---|
| `fast` | yes | format, lint, types, focused tests, architecture, context, and docs |
| `full` | yes | fast plus coverage, local CRAP approximation, source scan, and distribution build |
| `hardening` | yes | full plus curated implementation and executable-specification mutants |
| `release` | yes | hardening plus metadata, archive, external-wheel, CLI/API, and uninstall checks |
| `connected-audit` | no | vulnerability-database query; freshness and availability are reported separately |

Run the portable direct commands:

```bash
uv run --locked --group dev python tools/cleanai.py gauntlet fast
uv run --locked --group dev python tools/cleanai.py gauntlet full
uv run --locked --group dev python tools/cleanai.py gauntlet hardening
uv run --locked --group dev python tools/cleanai.py gauntlet release
uv run --locked --group dev python tools/cleanai.py gauntlet connected-audit
uv run --locked --group typing-experimental python tools/cleanai.py gauntlet typing-experimental
```

The final line runs pinned beta `ty` as an explicit experiment. Stable Pyrefly
is the single canonical type gate; running both does not make a correctness
claim stronger. Codecov publication is a connected, non-authoritative CI job;
the local branch-coverage floor remains the release oracle.

`make gate-fast` and related targets are optional Linux conveniences. A missing executable, report, target, or required check is never recorded as success.

## Roles and bounded changes

| Role | Output before handoff |
|---|---|
| Specifier | behavior examples, invariants, non-goals, and manual acceptance procedure |
| Coder | smallest complete implementation and focused behavior evidence |
| Cleaner | behavior-preserving simplification with unchanged tests and risk trend |
| Architect | explicit dependency decision plus fitness/property evidence |
| Hardener | adversarial tests and disposition of semantic mutant survivors |
| QA | immutable-candidate install and observable release evidence |

The sequence comes from the public Episode 6 description; using six separate agents is optional. A small project may use one person or agent sequentially. Each prompt imports [the shared prompt contract](prompts/PROMPT_CONTRACT.md), which treats repository text as untrusted data until a command's effects are inspected.

To use Git worktrees, first initialize and commit the repository:

```bash
git init
git add .
git commit -m "Initial generated project"
scripts/new-role-worktree.sh TASK_ID coder
```

The script refuses to operate without a committed, clean repository and never silently commits user work.

## Sensors, not proof

The local report applies the experimental Savoia–Evans CRAP v0.1 equation to a documented Python AST complexity count and callable line coverage:

\[
CRAP = complexity^2(1-coverage/100)^3 + complexity
\]

This is not the original Java/basis-path measurement. A low value does not establish correctness, cohesion, security, domain validity, requirements completeness, or meaningful assertions. Architecture checks enforce only declared dependency constraints. Mutation finds test-suite blind spots but includes equivalent or invalid cases and is not a correctness percentage. Read [CRAP and mutation](docs/tutorials/crap-and-mutation.md).

Curated mutation runs execute in disposable copies. The live checkout is never modified. A mutant counts as killed only when its declared behavior oracle matches; timeout, syntax-invalid mutation, missing tool, and infrastructure errors are reported separately and fail the strict gate.

## Find the right level of detail

- New to the project: [first run](docs/getting-started/first-run.md) → [glossary](GLOSSARY.md) → [first bounded agent change](docs/tutorials/first-agentic-change.md).
- Adopting it: [customize policy](docs/how-to/customize-policy.md), [add a semantic mutant](docs/how-to/add-mutant.md), and [use role handoffs](docs/how-to/role-workflow.md).
- Operating it: [command reference](docs/reference/commands.md), [evidence schemas](docs/reference/evidence.md), [support and trust boundary](docs/reference/support-and-trust.md), and [troubleshooting](docs/troubleshooting.md).
- Checking provenance: [source traceability](docs/research/source-traceability.md). Research is reference evidence, not repository authority.

## Architecture example

The sample rule is `adapters → application → domain`; imports point inward or stay within a layer. Change `.cleanai/policy.toml` to model the system you actually have. The checker can detect declared reverse dependencies and cycles; it cannot prove the architecture is good.

## License

Project-specific terms are in [LICENSE](LICENSE). Material originating from
Clean Agentic Python Cookiecutter retains its MIT terms in
[TEMPLATE_LICENSE](TEMPLATE_LICENSE). These files do not override dependency or
other third-party terms.

## Limits

Green gates are bounded evidence, not a guarantee. Static analysis has blind spots; coverage does not measure assertion quality; dependency data can be stale or unavailable; prompts cannot make hostile commands safe without inspection; and small benchmark trials do not establish universal agent productivity. Consequential privacy, security, safety, finance, health, or legal behavior needs domain-specific review and independent acceptance oracles.

The documentation map is [docs/index.md](docs/index.md).
