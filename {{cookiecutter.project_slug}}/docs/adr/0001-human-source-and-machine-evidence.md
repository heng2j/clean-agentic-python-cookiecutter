---
status: normative
authority: adr-0001-human-source-machine-evidence
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "docs/contracts/**"
  - "tests/acceptance/**"
  - "src/**"
---
# ADR 0001: Human-readable source and machine evidence

## Status

Accepted.

## Context

When agents produce substantial implementation, code alone is a fragile place to preserve human intent. Natural-language documents can also become stale, contradictory, and too broad to constrain behavior.

## Decision

Use this authority order:

1. human-owned contracts, acceptance examples, invariants, architecture decisions, and risk policy;
2. executable tests and deterministic fitness functions that can falsify violations;
3. generated implementation and evidence artifacts;
4. issue, chat, and audit history as non-normative evidence.

A generated implementation may be rewritten. A public behavior or boundary change requires an explicit update to human-readable authority and executable evidence.

## Consequences

Specifications must remain understandable independently of one implementation; documents need owners and lifecycle; repeated hard constraints move into tools; history is distilled rather than copied into every context; and green metrics cannot substitute for product, domain, security, or scientific judgment.
