---
status: normative
authority: tutorial-crap-mutation
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - ".cleanai/policy.toml"
  - ".cleanai/*mutations.toml"
  - "tools/**"
  - "tests/**"
---
# CRAP and mutation: two fallible sensors

## Read the CRAP report

```bash
mkdir -p artifacts/coverage
uv run --locked --group dev coverage run --branch -m pytest -q
uv run --locked --group dev coverage json -o artifacts/coverage/coverage.json
uv run --locked --group dev python tools/cleanai.py crap --coverage artifacts/coverage/coverage.json --strict
```

The tool requires a valid coverage.py JSON report, exact in-repository file identities, and measurable evidence for every assessed callable. Empty, partial, foreign, missing, and malformed input are errors. The equation is the experimental Savoia–Evans v0.1 equation; complexity and callable line coverage are local Python approximations, not original basis-path measurement.

A low score says only that the chosen complexity/coverage combination is below a local budget. It does not prove correctness, cohesion, coupling quality, security, domain validity, useful assertions, or exercised branches.

## Observe a killed mutant

```bash
uv run --locked --group dev python tools/cleanai.py mutate \
  --config .cleanai/code-mutations.toml --strict
```

Expected: the passing baseline is recorded; each declared semantic change runs in a disposable copy; an explicit expected exit/output oracle kills the bundled mutant; the live checkout hash stays unchanged.

## Create and understand a survivor

Copy one mutant entry, give it a new ID, and choose a one-occurrence replacement that preserves current tested examples but changes an untested boundary. Run the same command. Expected: strict mode exits nonzero and marks `SURVIVED`.

Do not immediately add an assertion that merely mirrors implementation. First decide whether the mutant represents a real requirement. Then either:

- add behavior evidence that fails for the intended reason;
- mark a demonstrably equivalent mutant with a written rationale outside the score; or
- remove an invalid mutant whose replacement cannot execute as meaningful code.

Timeouts, missing tools, syntax-invalid replacements, baseline failures, and unmatched targets are `INVALID` or `INFRASTRUCTURE_ERROR`, never “killed.” Zero valid mutants is not 100%.
