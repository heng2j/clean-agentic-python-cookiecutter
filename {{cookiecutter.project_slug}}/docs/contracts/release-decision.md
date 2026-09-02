---
status: normative
authority: release-decision-contract
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "src/{{ cookiecutter.package_name }}/domain/**"
  - "tests/acceptance/**"
---
# Release-decision contract

The starter domain demonstrates a human-owned policy consuming machine-produced evidence.

A release is blocked when any of these is true:

- one or more tests failed;
- lint/type findings remain;
- architecture violations remain;
- security findings remain;
- the maximum CRAP score exceeds the policy budget;
- mutation score is below the policy floor;
- a trust boundary changed without completed review.

Counts must be non-negative. CRAP and mutation values must be finite. Mutation percentages must be within `[0, 100]`. Invalid raw evidence raises an error rather than being sanitized into a healthy-looking decision.

Executable stakeholder examples live in `tests/acceptance/features/release_decision.feature`. The canonical pure policy lives in `src/{{ cookiecutter.package_name }}/domain/change_risk.py`.
