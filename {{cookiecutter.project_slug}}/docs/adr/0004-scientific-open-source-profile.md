---
status: normative
authority: adr-scientific-open-source-profile
owner: maintainers
last_verified: 2026-09-02
applies_to:
  - "src/**"
  - "notebooks/**"
  - "results/**"
  - "scripts/**"
  - "static/**"
  - ".envrc"
  - "prek.toml"
  - ".github/**"
---
# ADR 0004: scientific open-source profile

## Decision

Keep the installed package under `src/{{ cookiecutter.package_name }}` and add
narrow contracts for notebooks, results, scripts, and static inputs. Use uv for
the reviewed Python environment, Ruff for formatting and linting, rumdl for
Markdown, Pyrefly as the canonical type check, pytest for behavior, and `prek`
as a convenience runner for the same non-mutating commands. Beta `ty` is
available only as a deliberately invoked experimental profile. Codecov may publish the XML
coverage report in connected CI; the local branch-coverage policy remains the
release oracle.

`.envrc` may load an ignored `.env` and expose an existing `.venv`, but it must
not install dependencies, approve itself, modify Git, create remotes, or contact
external services. The project does not install Jupyter or marimo until notebook
execution becomes a real, tested requirement.

## Scientific artifact policy

- Reusable behavior lives in the installed package, not only in a notebook or script.
- Committed static inputs are small and redistributable, and are registered with origin, license, and SHA-256.
- Generated results are ignored by default. A curated reference result needs an explicit provenance review.
- Scientific claims document assumptions, units, validity limits, tolerances, and known nondeterminism.
- Code, data, documentation, and model artifacts may have different license obligations.

## Source-supported versus local

The directory names and tool candidates were inspired by Jonathon Vandezande's
package guide and repository and Rowan Scientific's opinionated guide. The
source layout, trust boundary, exact commands, thresholds, evidence schemas,
manifest rules, and one-canonical-checker policy are local decisions. See
[scientific source traceability](../research/scientific-source-traceability.md).

## Alternatives rejected

- A flat import package: it can let local imports mask missing wheel contents.
- Running `uv sync`, installing hooks, committing, or creating a GitHub remote during generation: surprising external or repository side effects violate bounded generation.
- Requiring both `ty` and Pyrefly in every fast gate: overlapping analyzers add cost and diagnostic churn without proving correctness.
- A second coverage configuration file: duplicate authority invites drift.
- Committing arbitrary result payloads or private `.env` values: creates size, provenance, privacy, and secret-loss risks.
- A blanket ban on Conda/Pixi/system tooling: some compiled scientific stacks cannot be represented as PyPI-only environments.

## Consequences and verification

The starter has more scientific guardrails but still cannot prove that a model,
dataset, result, or conclusion is scientifically valid. `science-audit` checks
the shipped directory and manifest contracts. The release gate still builds and
installs the wheel outside the checkout. Native macOS/Windows behavior, notebook
execution, non-PyPI stacks, and Codecov availability remain separate claims.
