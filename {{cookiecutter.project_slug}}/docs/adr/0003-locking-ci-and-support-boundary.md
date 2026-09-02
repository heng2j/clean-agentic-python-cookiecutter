---
status: normative
authority: adr-locking-ci-support
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "pyproject.toml"
  - "uv.lock"
  - ".github/workflows/**"
  - "README.md"
---
# ADR 0003: reviewed lock, pinned CI actions, and narrow support

## Decision

The generated project includes a reviewed `uv.lock`; first setup checks it and installs with `--locked`. Plain `uv lock` is a deliberate dependency-update operation whose diff must be reviewed. Builds use the already locked development environment with `python -m build --no-isolation`, so release profiles do not silently resolve a separate backend. CI actions use immutable commit SHAs with minimal permissions. Deterministic release evidence is separate from connected vulnerability queries. The v2 support claim is Linux x86_64 on CPython 3.12 and 3.13 only.

## Consequence and risk

The lock makes tested resolution visible and reproducible, but it does not freeze a vulnerability database. `--no-isolation` is safe here only because Hatchling is an explicit locked development dependency and the release command runs inside that environment. Narrow support is honest but less convenient for untested platforms.

## Alternatives rejected

- Live resolution on every gate: exposes silent tool drift.
- Mutable CI action tags: convenient upgrades but weaker provenance.
- Put network audit inside “deterministic full”: makes offline failure look like code failure and stale green evidence easy to misread.
- Claim cross-platform based on Python syntax alone: ignores shells, permissions, path rules, and runner behavior.

## Verification

CI checks the lock, exercises 3.12/3.13 deterministic release paths, requires evidence artifacts, and runs the connected audit in its own job. macOS and Windows remain explicitly Unverified.
