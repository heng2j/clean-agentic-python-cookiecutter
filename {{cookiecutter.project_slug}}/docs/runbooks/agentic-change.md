---
status: normative
authority: agentic-change-runbook
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "docs/plans/active/**"
  - "prompts/**"
  - "scripts/**"
---
# Agentic-change runbook

## Frame and authorize

Create one task packet. State outcome, current reproduction, authority, allowed surface, non-goals, invariants, risk, acceptance commands, adversarial cases, and stop conditions. Write a prediction before launch.

## Specify

Use the Specifier prompt to create implementation-independent examples and a manual QA procedure. Establish a baseline that fails for the missing behavior.

## Isolate

```bash
scripts/new-role-worktree.sh TASK_ID coder
```

Use an independent worktree for a reviewer or risky alternative. Keep one integration branch and one writer per shared boundary.

## Implement and gate

Run the smallest relevant check first, then `make gate-fast`. Return exact commands and results. Do not combine unrelated repository cleanup with a behavior change.

## Clean and architect

Cleaner removes duplication and accidental complexity without changing behavior. Architect evaluates dependencies, state ownership, locality, and property-level invariants. Record a decision when a new boundary or exception appears.

## Harden

Add curated semantic and executable-spec mutants, malformed/boundary cases, and other risk-relevant adversarial evidence. Run `make gate-hardening`; disposition survivors.

## QA and accept

Exercise the user-visible path from a clean environment. Human acceptance requires: what changed, why it works, exact evidence, unverified assumptions, failure boundary, and rollback.

## Store and prune

Update the contract/ADR, write a learning ledger, move the completed plan out of the active path, and run context/docs audits. Do not leave an issue transcript or one-off prompt as accidental permanent authority.
