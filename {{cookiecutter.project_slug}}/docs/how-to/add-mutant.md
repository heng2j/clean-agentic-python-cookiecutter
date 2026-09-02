---
status: normative
authority: howto-add-mutant
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - ".cleanai/*mutations.toml"
  - "tests/**"
---
# Add a curated semantic mutant

Choose a realistic defect: reversed threshold, wrong branch, missing validation, fail-open decision, stale chronology, or package/runtime mismatch. In the appropriate TOML file record a unique ID, in-repository non-symlink target, exact one-occurrence original/replacement, focused verification command, timeout, and expected exit/output oracle.

Run the configuration once with a deliberately strong test and once with a controlled weak-test fixture. Confirm the first is `KILLED`, the second is `SURVIVED`, both return the documented strict exit, and `git diff` plus a source hash prove the live checkout never changed. Treat invalid or equivalent cases separately from the valid score denominator.
