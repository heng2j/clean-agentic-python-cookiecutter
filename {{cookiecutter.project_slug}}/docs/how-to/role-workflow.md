---
status: normative
authority: howto-role-workflow
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "prompts/**"
  - "scripts/new-role-worktree.sh"
---
# Use role handoffs without ceremony

Use only roles justified by the change risk. The public six-role order is a useful complete example, not a mandate for six simultaneous agents.

For each handoff, provide the immutable base revision, clean/dirty state, task packet, allowed paths, acceptance oracle, prior exact evidence, and unresolved questions. The receiver rechecks authority and does not trust a predecessor's summary as proof.

Worktrees require a committed Git repository. Give each active writer a disjoint surface. If writers need the same boundary, run them sequentially or stop and assign one owner. Read-only reviewers may run in parallel.

QA works from an immutable candidate and installs the wheel outside the source tree. A phase may return `Blocked` or `Unverified`; the orchestrator must not translate those into success.
