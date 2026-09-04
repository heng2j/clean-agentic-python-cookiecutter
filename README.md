# Clean Agentic Scientific Python Cookiecutter

> **Move scientific ideas into tested Python—without losing context, provenance, control, or the joy of discovery.**

This branch is a lightweight, open-source scientific profile of Clean Agentic
Python Cookiecutter. It helps people and coding agents turn a research question
into bounded work and produce installable, reviewable software and traceable
artifacts backed by evidence.

> **Experimental Graft variant.** This branch adds an optional, project-local
> structural-navigation experiment; it does not make Graft a Python dependency
> or a quality gate. No correctness, token, cost, or productivity improvement
> has yet been established. Start with the bounded
> [variant decision record](GRAFT_VARIANT.md).

## Why this exists

Coding agents can turn a promising idea into working code at remarkable speed.
They can also multiply ambiguity: unclear requirements, stale context, broad
changes, weak tests, and confident summaries that are difficult to verify.

I built this project to give myself—and other research engineers—clearer
headspace while harnessing that speed. The codebase, the agents, and the people
guiding them should share enough context to keep innovating on new ideas and
features without constantly wondering what changed, why it changed, or whether
the result is trustworthy.

The aspiration is worry-free momentum, not blind trust. No template can remove
software risk. This one aims to reduce avoidable uncertainty by making intent,
authority, boundaries, checks, evidence, and remaining risk visible—so people
and agents can move quickly while keeping code quality and project clarity in
view.

## What you get

- **Context clarity:** concise `AGENTS.md`, delegated `CLAUDE.md`, and scoped
  rules help agents find current authority without reading the entire repository.
- **Disciplined workflow:** choose the relevant roles from a Specifier → Coder
  → Cleaner → Architect → Hardener → QA workflow; each pass has an explicit
  purpose and finish line.
- **Evidence, not vibes:** after the locked environment is installed, fast,
  full, hardening, and release profiles run offline, fail closed, and write
  inspectable ledgers; the network-connected audit remains separate.
- **Change-risk sensors:** branch-aware coverage, a documented local CRAP
  approximation, curated implementation and executable-specification mutants,
  and architecture fitness checks expose different kinds of weakness.
- **Safer adaptation:** validated preset generation, disposable mutation copies,
  write-path checks, and explicit stop conditions are designed to limit
  unintended changes.
- **A learning path:** the generated project includes a glossary, quickstart,
  hands-on tutorials, how-to guides, reference material, and troubleshooting.
- **A scientific workspace:** scoped `notebooks/`, `static/`, `results/`, and
  `scripts/` directories separate exploration, registered inputs, generated
  outputs, and thin operational entry points from the installed package.
- **Modern contributor tools:** uv, Ruff, rumdl, Pyrefly, pytest, `prek`, GitHub
  Actions, and connected Codecov reporting use one reviewable command surface.
  Optional `direnv` loads the generated project's reviewed shell settings on
  entry and unloads them on exit, reducing manual environment activation and
  accidental cross-project configuration.
- **Portable prompts:** reusable role, audit, cleanup, hardening, release-QA,
  context-hygiene, and agent-friction prompts share one concise contract.
- **Optional structural navigation:** a reviewed, project-local Graft experiment
  can rank likely places to inspect while keeping its derived output separate
  from project authority. It is pinned, bounded, removable, and absent from
  every Python quality gate; the ordinary source-search workflow remains the
  default.

You do not need prior experience with CRAP scores, mutation testing,
architecture fitness functions, or agent context files. The generated project
introduces them progressively and explains what each check can—and cannot—show.

## Optional Graft: deliberate opt-in

Generated projects work fully without Graft. The default path remains current
source, `rg`/`git grep`, human-owned contracts and decisions, tests, and the
deterministic CleanAI gates. The optional experiment pins published
[`@nanonets/graft` 0.16.0](https://github.com/trailhq/Graft) behind a
project-owned adapter. It can provide a structural lead for location and
relationship questions; ranked retrieval is not exhaustive search, observed
behavior, design rationale, or authority.

After generating a project and completing the normal setup, review
`GRAFT_EXPERIMENT.md`. In a reviewed, connected environment, the shortest
opt-in path is:

```bash
# Read-only prerequisite and status check; missing Graft is UNVERIFIED.
uv run --locked --group dev python tools/graft_adapter.py doctor

# Explicitly authorize the pinned, project-local npm installation.
uv run --locked --group dev python tools/graft_adapter.py install --apply
uv run --locked --group dev python tools/graft_adapter.py build
uv run --locked --group dev python tools/graft_adapter.py ask \
  "Where is release blocking decided?" --limit 5 --source
```

The adapter disables deep/model-backed work, MCP, LSP, hooks, prompt injection,
global configuration, and committed graph output. Public results omit or hash
unneeded upstream metadata, label retained text as untrusted, and use
project-relative paths. Before cleanup, stop direct Graft or other writers and
inspect `remove --check`; removal refuses tracked files, unknown descendants,
or altered ownership receipts.

Published Graft 0.16.0 was observed to omit a tracked Python file beneath a
hidden directory. The adapter fails closed in that case: keep using the default
workflow rather than moving, untracking, or ignoring legitimate source. No
accepted-task correctness, token, cost, or productivity improvement has yet
been established, so the integration remains experimental and optional. See
[the variant decision record](GRAFT_VARIANT.md) for the evaluated capability
boundary.

## Scientific variant inspiration

Jonathon Vandezande's ideas directly inspired this variation. In particular:

- [*Setting Up Python Packages*](https://jevandezande.github.io/blog/setting-up-python-packages/)
  proposed the scientific project directories and several of the tool candidates;
- [*How to Make a Great Open Source Scientific Project*](https://www.rowansci.com/blog/how-to-make-a-great-open-source-scientific-project)
  frames focused, packaged, tested, documented, maintained, genuinely open-source
  scientific software; and
- Jonathon's [`uv-cookiecutter`](https://github.com/jevandezande/uv-cookiecutter)
  provides a concrete implementation to inspect and learn from.

Thank you to Jonathon for publishing the ideas, examples, and tradeoffs in the
open. This project independently evaluated and adapted them; it is not a fork,
certification, or endorsement. For example, this profile retains `src/`
isolation, does not auto-install dependencies or create GitHub remotes during
generation, keeps secrets out of deterministic agent runs by default, and does
not treat Codecov or two overlapping type checkers as proof. See the concise
[adopt/adapt/reject decision record](SCIENTIFIC_VARIANT.md).
For branch review, see the [bounded validation record](SCIENTIFIC_VARIANT_VALIDATION.md)
and [migration guide](MIGRATION_SCIENTIFIC_VARIANT.md).

## Quick start

Prerequisites: Linux, CPython 3.12 or 3.13, and
[`uv` 0.11.33](https://docs.astral.sh/uv/getting-started/installation/), which
this release pins for reproducibility.

```bash
uvx --from 'cookiecutter==2.7.1' cookiecutter /path/to/clean-agentic-python-cookiecutter
cd clean-agentic-scientific-python-project
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Expected result: the fast gate exits `0`, every required step runs, and the
harness prints the path to its evidence. Then open
`docs/getting-started/first-run.md` for a guided break → failure → fix → success
exercise.

## Optional project environment with `direnv`

[`direnv`](https://direnv.net/) automatically loads and unloads
directory-specific environment variables as you enter and leave a project. In
each generated project, the reviewed `.envrc` detects the uv-created `.venv`
and puts its executables on `PATH`, so ordinary shell commands use the project
environment without a manual activation step. The required `direnv allow`
step makes authorizing that executable configuration an explicit decision.

First [install `direnv`](https://direnv.net/docs/installation.html),
[hook it into your shell](https://direnv.net/docs/hook.html), and restart the
shell. Then, from the generated project:

```bash
# Review .envrc before authorizing it.
direnv allow

# Optional: create a private, project-local environment file.
cp .env.example .env
# Edit .env, then uncomment this line in .envrc: dotenv_if_exists .env
direnv allow
```

Loading `.env` remains deliberately disabled until that one line is
uncommented. Although `.env` is ignored by Git, `direnv` is not a secret
manager: exported values are inherited by every child process, including
tests and coding agents. Use least-privilege project credentials and run
secret-free deterministic gates whenever credentials are unnecessary.

## Choose the right generation path

Cookiecutter templates, hooks, replay files, and direct `--no-input` context
must be treated as **trusted, code-equivalent input**. Use the direct command
above only with a template and context you trust.

For a JSON preset supplied by a form, an agent, a download, or another
less-trusted source, validate it before Cookiecutter evaluates Jinja. From the
template repository root, run:

```bash
uv run --locked python scripts/generate_safe.py \
  --preset /path/to/project-preset.json \
  --output-dir /path/to/projects
```

See [Safe Generation and Replay](SAFE_GENERATION.md) for the preset schema,
trust boundary, copyright-year replay, and failure behavior.

The defaults avoid publishing a fictional person or email address: the author
is the generated project's contributor group, `not-provided` omits email from
package metadata, and `current` resolves to a concrete generation year. Replace
these defaults with the real project identity whenever one exists.

## Inspiration and credit

This project was inspired by Matt Pocock's livestream conversation with Robert
C. Martin, [*LIVE: Uncle Bob on Software Fundamentals in the Age of
AI*](https://www.youtube.com/watch?v=zcLPGC-tvgk), and by Martin's book
[*Clean Code: A Handbook of Agile Software
Craftsmanship*](https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship/P200000009044).

It also draws on Clean Coders'
[*Clean AI: Agentic Discipline*](https://cleancoders.com/series/clean-ai)
series—especially the numbered specialized-agent workflow on
[Episode 6's public page](https://cleancoders.com/episode/agentic-discipline-6),
which credits Justin Martin and Robert “Uncle Bob” Martin.

Those sources inspired the direction; they do not define every choice here.
These links document inspiration; they do not imply authorship, certification,
approval, or endorsement. The Python implementation, quality harness,
thresholds, prompt contract, documentation model, and evidence schemas are
this project's independent synthesis.

## Trust and support boundary

The documented generation and validation paths have been verified on **Linux
x86_64 with CPython 3.12 and 3.13**. Native macOS and Windows remain
**Unverified**.

A green gate establishes only its named checks. Low CRAP, high coverage, killed
mutants, or a clean architecture report do not by themselves prove correctness,
security, good domain decisions, or meaningful tests.

This is an **independent, unofficial** project. It is not authored, sponsored,
approved, or endorsed by Justin Martin, Robert C. Martin, Clean Coders, Matt
Pocock, OpenAI, Anthropic, or the cited researchers.
