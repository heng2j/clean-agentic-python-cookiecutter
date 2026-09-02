# Clean Agentic Python Cookiecutter

> **Move faster with coding agents—without losing context, clarity, control, or the joy of building.**

Clean Agentic Python Cookiecutter is a lightweight starter for building Python
software with AI coding agents. It provides a practical blueprint for creating 
a clean agentic coding workspace: combines concise agent instructions, 
bounded task handoffs, deterministic quality gates, architecture checks, 
mutation testing, context-hygiene tools, and traceable evidence so that
AI-generated changes remain understandable, verifiable, and safe to evolve.
It helps humans and coding agents to sustain true productivity 
with high-throughput of code and ideas. 


## Why this exists

Coding agents have changed the bottleneck in software development. Producing code
is becoming remarkably fast; directing, reviewing, integrating, and trusting a
growing volume of changes is now the harder problem. That is not true productivity. 
It is **software entropy produced at higher throughput**.

I built this project for myself and for other engineers, researchers, and
independent builders who want the leverage of AI coding agents without
surrendering the discipline and craftsmanship of software engineering.

The aspiration is **worry-free momentum, not blind trust**. No template can remove
software risk. This one aims to reduce avoidable uncertainty by making intent,
authority, boundaries, checks, evidence, and remaining risk visible—so humans
and agents can move quickly while keeping code quality and project clarity in
view with software engineering best practices.

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
- **Portable prompts:** reusable role, audit, cleanup, hardening, release-QA,
  context-hygiene, and agent-friction prompts share one concise contract.

You do not need prior experience with [CRAP scores](https://testing.googleblog.com/2011/02/this-code-is-crap.html), [mutation testing](https://testing.googleblog.com/2021/04/mutation-testing.html),
architecture fitness functions, or agent context files. The generated project
introduces them progressively and explains what each check can—and cannot—show.

## Quick start

Prerequisites: Linux, CPython 3.12 or 3.13, and
[`uv` 0.11.33](https://docs.astral.sh/uv/getting-started/installation/), which
this release pins for reproducibility.

```bash
uvx --from 'cookiecutter==2.7.1' cookiecutter /path/to/clean-agentic-python-cookiecutter-v2
cd clean-agentic-python-project
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Expected result: the fast gate exits `0`, every required step runs, and the
harness prints the path to its evidence. Then open
`docs/getting-started/first-run.md` for a guided break → failure → fix → success
exercise.

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
