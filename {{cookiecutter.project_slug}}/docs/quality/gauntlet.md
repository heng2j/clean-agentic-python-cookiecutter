---
status: normative
authority: quality-gauntlet-policy
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - ".cleanai/policy.toml"
  - "tools/cleanai.py"
---
# Deterministic quality gauntlet

The gauntlet delegates exact questions to deterministic tools before asking an agent or human for judgment.

1. parsing/build/format;
2. lint and type analysis;
3. unit and executable acceptance behavior;
4. invariant/property and architecture checks;
5. coverage and CRAP/change-risk analysis;
6. source and dependency security;
7. curated implementation/specification mutation;
8. package/release reproducibility;
9. risk-shaped agent and human review.

Classify each control:

- **Invariant:** zero violations, such as failing tests or reverse dependencies.
- **Ratchet:** no new debt, then lower an explicit baseline.
- **Budget:** a limit requiring a reviewed exception, such as complexity.
- **Diagnostic trend:** inspect movement without optimizing blindly, such as total LOC.

`tools/cleanai.py gauntlet` resolves inherited profiles from `.cleanai/policy.toml`, executes them fail-fast without a shell, and writes a ledger. External security databases can change; preserve the lockfile, timestamp, and tool version with the evidence.
