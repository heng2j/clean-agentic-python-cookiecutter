---
status: normative
authority: context-hygiene-policy
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "AGENTS.md"
  - "CLAUDE.md"
  - ".claude/rules/**"
  - "docs/**"
---
# Context precision and hygiene

## Objective

Optimize relevant context per token rather than total context volume:

```text
context precision = task-relevant context retrieved / all context retrieved
```

Persistent files should route an agent to stable authorities, canonical commands, invariants, definition of done, and stop conditions. Dynamic counts, exhaustive trees, generated output, completed plans, old audits, and style rules already enforced by tools should load only when needed.

## Lifecycle

Every active document declares `status`, `owner`, unique `authority`, `last_verified`, and `applies_to`. A document is stale when behavior contradicts it, commands or paths are dead, another document claims the same authority, superseded material remains on the default route, or volatile evidence is frozen in prose.

## Issue/history distillation

Do not pass an entire thread by default. Distill:

```text
current problem and reproduction
current acceptance criteria
current non-goals
current authoritative decisions
open questions
minimal selected historical evidence
```

## Enforcement

The context audit checks budgets, required sections, broad instructions, duplicate root guidance, dynamic facts, issue links, and stale references. The docs audit checks lifecycle metadata, authority collisions, dead links, unresolved markers, archive location, and verification age. The prune command proposes changes but never deletes.

## Empirical posture

Research findings are mixed and benchmark-bound: additional repository guidance can increase task cost and sometimes reduce success, while concise developer-authored instructions can still improve particular tasks. Treat every persistent instruction as a hypothesis whose cost should be measured on stable representative tasks.
