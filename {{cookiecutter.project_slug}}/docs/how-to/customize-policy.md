---
status: normative
authority: howto-customize-policy
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - ".cleanai/policy.toml"
  - "docs/architecture/layers.md"
---
# Customize layers and thresholds

1. Describe actual dependency direction in `docs/architecture/layers.md`; do not force the sample three layers onto a different design.
2. Edit `.cleanai/policy.toml` layer names, package root, allowed edges, and finite budgets.
3. Add architecture fixtures for an allowed import, reverse import, relative import, cycle, type-only import, conditional import, dynamic literal import, and similarly named external package.
4. Seed one violation and prove strict mode exits nonzero before accepting the policy.
5. Calibrate numeric budgets from your own stable baseline and risk tolerance. A threshold is a local ratchet, not a scientific boundary.

Record the decision and rejected alternatives in an ADR when changing dependency direction or a release gate. Never raise a budget merely to turn CI green without explaining the changed risk.
