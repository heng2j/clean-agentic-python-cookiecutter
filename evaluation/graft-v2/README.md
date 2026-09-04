# Graft variant evaluation evidence

This directory holds stable review artifacts for the experimental Graft branch.
It intentionally excludes raw command logs, generated graphs, caches, and
machine-specific install state. Those volatile artifacts belong in the ignored
evidence workspace or the draft pull request attachment.

## Read in this order

1. `AUDIT_GRAFT_VARIANT_ORIGINAL.md` — immutable pre-fix verdict.
2. `AUDIT_GRAFT_VARIANT_V2.md` — enhanced candidate and residual risks.
3. `GRAFT_FEATURE_DECISION_MATRIX_V2.md` — F0 default, narrow F1 experimental,
   F2–F6 rejected from the project profile.
4. `VALIDATION_GRAFT_VARIANT_V2.md` — exact final-source checkpoints and
   remaining hosted, connected-install, platform, and cohort boundaries.
   Pending cells are **Unverified**, not passes.
5. `GRAFT_SOURCE_INDEX.md` — pinned primary sources and issue-evidence limits.
6. Retrieval, explainability, UX, threat-model, migration, and structured finding
   reports for the supporting detail.

## Evidence boundary

- The original audit, findings, claim matrix, feature decision, threat model,
  context inventory, manifest, and checksum files are copied byte-for-byte from
  the frozen checkpoint. `GRAFT_CLAIM_EVIDENCE_MATRIX_V2.md` extends the frozen
  claim matrix with a separately labeled v2 section.
- Stable numeric results retain their original evidence classification.
- Exact model tokens, billed cost, independent newcomer comprehension, native
  non-Linux support, packet-level network silence, and source-to-package build
  provenance are not claimed.
- Graft output is derived navigation evidence. Current source, observed
  behavior, contracts, tests, ADRs, and explicit human decisions retain
  authority within their declared scope.

## Decision

**Recommended:** do not promote Graft as a correctness, token-saving,
blast-radius, or productivity control. Keep ordinary no-Graft work as F0 and
retain only the project-owned `build`, `check`, and bounded `ask` surface as an
optional F1 experiment. F2–F6 remain rejected from the project profile.

The final local implementation source is `b719459` (tree `3581908`); GitHub
publishes the identical tree as remote review commit `4dc3603`. Stable reports
are a publication wrapper around that validated implementation tree and are not
part of generated projects.

Hosted runs `33873556873` (implementation) and `33874894406` (stable-report
publication) passed both supported Python jobs.
