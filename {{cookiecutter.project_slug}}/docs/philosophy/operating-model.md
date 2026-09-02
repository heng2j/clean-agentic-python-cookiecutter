---
status: normative
authority: clean-ai-operating-model
owner: maintainers
document_version: "2.0"
last_verified: 2026-09-01
source_retrieved: 2026-09-01
applies_to:
  - "AGENTS.md"
  - "prompts/**"
  - "docs/runbooks/**"
---
# Clean AI operating model

## Source-derived public spine

The public [Agentic Discipline 6 page](https://cleancoders.com/episode/agentic-discipline-6), credited to **Justin Martin and Robert “Uncle Bob” Martin**, describes six roles, each using an isolated Git worktree, in this numbered workflow:

1. **Specifier:** converts a task into Gherkin acceptance tests and a detailed manual UI QA procedure.
2. **Coder:** implements behavior, unit tests, and the acceptance-test harness.
3. **Cleaner:** iterates on code/tests using DRY- and CRAP-oriented gates.
4. **Architect:** reviews/refines modules and dependencies and adds property-based tests.
5. **Hardener:** performs language-level and Gherkin-level mutation testing.
6. **QA:** automates the original UI procedure and checks user-visible behavior.

**Boundary:** those statements summarize the public page, not an inferred transcript. The UI-specific activities describe its demonstrated workflow and may not fit every library or CLI. The page does not establish this scaffold’s prompts, commands, thresholds, evidence schema, risk tiers, one-writer policy, effectiveness, or undisclosed implementation details. See [source traceability](../research/source-traceability.md).

## Local synthesis

This scaffold turns the public role spine into two locally designed loops:

```text
HUMAN: authorize → stay oriented → inspect evidence → accept, reject, or redirect
MACHINE: specify → code → check → clean → review structure → harden → verify
```

The human retains outcome, risk appetite, causal interpretation, and acceptance. The agent receives a bounded deliverable, allowed surface, non-goals, stop conditions, and required evidence. This allocation is a **local operating proposal**, not a recommendation attributed to the cited sources.

Three local boundaries keep responsibility visible:

- **Authorization:** name the outcome, non-goals, permitted paths/effects, risk, and acceptance evidence before work.
- **Escalation:** stop on contradictory authority, unknown dirty state, changed public contracts, trust-boundary expansion, unexplained drift, or material scope growth.
- **Acceptance:** a human evaluates observable behavior and independently reproducible evidence; fluent prose is not proof.

## Topology and state safety

Use separate worktrees only after recording the base revision, branch/destination names, and tracked/untracked/dirty state. A worktree separates directories; it does not by itself prevent branch collision, unsafe commands, mutation of shared external paths, or loss of concurrent edits. Default to one writer per shared boundary, and verify cleanup/state identity at handoff. If those preconditions cannot be established, stop rather than improvise.

The same person or model may execute multiple low-risk roles sequentially, but that is not independent review. Cleaner and Architect must not quietly change requirements; high-risk design or release claims require an independent oracle or reviewer.

## Risk-shaped local review

| Risk | Typical change | Minimum local review |
|---|---|---|
| R0 | formatting, regenerated index | deterministic check or sampled inspection |
| R1 | local pure helper | focused behavioral check |
| R2 | public API, state, or schema | contract, diff, and package-boundary checks |
| R3 | algorithm, security policy, scientific model | independent oracle and design review |
| R4 | authorization, money, provenance, or release trust | independent reviewer and explicit human sign-off |

These tiers are local defaults, not source-derived standards. Adapt them through an explicit decision record and tests.

Metrics are sensors, not verdicts. Contracts and invariants state selected expectations; passing them does not prove completeness. Accountable acceptance closes the loop.
