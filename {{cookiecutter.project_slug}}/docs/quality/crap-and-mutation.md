---
status: normative
authority: crap-mutation-policy
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - ".cleanai/*mutations.toml"
  - "tools/cleanai.py"
---
# CRAP and mutation policy

## CRAP

The original CRAP relationship combines cyclomatic complexity and coverage:

```text
CRAP = complexity² × (1 − coverage/100)³ + complexity
```

The local implementation uses a documented AST complexity approximation and coverage.py line evidence per callable. It does **not** claim exact basis-path coverage or exact equivalence with another complexity tool.

Use CRAP to prioritize risky combinations of branching and weak evidence. A low value does not prove correctness or cohesion; an inherently complex parser may require an explicit exception.

## Curated implementation mutants

Select semantic decisions whose alteration should be caught: invert a threshold, remove fail-closed validation, shift chronology, reuse identity, bypass authorization, or change a boundary.

## Executable-specification mutants

Change a Gherkin input or expected outcome. A killed spec mutant shows that the executable specification plus system distinguishes the altered expectation. A survivor may indicate a permissive harness, unused scenario, or equivalent behavior.

## Broad mutation tools

Use tools such as `mutmut` after curated cases. Pin versions, inspect survivors and equivalents, and avoid score theater. Acceptance requires a passing baseline, one exact target per curated mutant, restoration after failure, preserved output evidence, and explicit disposition of consequential survivors.
