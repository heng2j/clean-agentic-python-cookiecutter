---
status: reference
authority: thought-leader-lineage
owner: maintainers
evidence_version: "2.0"
last_verified: 2026-09-01
retrieved: 2026-09-01
applies_to:
  - "docs/philosophy/**"
  - "prompts/**"
---
# Thought-leader lineage and local synthesis

This scaffold combines public ideas without claiming that their authors created, recommend, sponsor, or endorse this implementation. “Influenced” below means a local design connection, not source approval or proof of effectiveness.

## Justin Martin and Robert C. Martin: the public role spine

The public [Agentic Discipline 6 page](https://cleancoders.com/episode/agentic-discipline-6), credited to **Justin Martin and Robert “Uncle Bob” Martin**, describes six roles in isolated Git worktrees and assigns them acceptance specification, implementation/testing, DRY/CRAP cleaning, architecture/property review, two mutation levels, and UI QA.

The deterministic command definitions, context/document lifecycle, risk tiers, evidence schemas, exact thresholds, one-writer rule, and applicability beyond the demonstrated workflow are **local synthesis**. The public page neither validates those choices nor establishes undisclosed implementation or license details.

## Martin Fowler: refactoring preserves behavior

[Fowler’s refactoring guide](https://martinfowler.com/tags/refactoring.html) defines refactoring as small internal transformations that preserve observable behavior and keep the system working. This influenced the local Cleaner constraint. Passing tests are evidence for selected behavior, not proof that every behavior is preserved.

## Dan North: examples as shared behavioral language

North’s [Introducing BDD](https://dannorth.net/blog/introducing-bdd/), [BDD by example](https://dannorth.net/blog/bdd-by-example/), and [testing essay](https://dannorth.net/blog/we-need-to-talk-about-testing/) support examples, scenarios, shared vocabulary, business value, and stakeholder-facing evidence. This influenced the Specifier role. Gherkin syntax alone cannot guarantee shared understanding or meaningful assertions.

## Alberto Savoia and Bob Evans: an experimental change-risk heuristic

Savoia’s [2007 CRAP v0.1 equation article](https://www.artima.com/weblogs/viewpost.jsp?thread=210575) identifies Bob Evans as collaborator and uses Java-method complexity with basis-path coverage. The later [crap4j article](https://www.artima.com/weblogs/viewpost.jsp?thread=215899) discusses a prototype and an initial experimental “30 or higher” interpretation.

This project reuses the algebra with a documented Python AST count and callable line coverage. Its configurable maximum and strict `>` comparator are local choices; at the default, exactly 30 passes. The values are not directly comparable to crap4j, and a threshold is never proof of code quality.

## Continuous delivery: short feedback and releasability

[Fowler’s continuous-delivery guide](https://martinfowler.com/delivery.html) describes always-releasable software and staged automated feedback that trades speed for increasing confidence. It influenced the layered-profile concept. Whether this repository’s exact profiles are sufficient, deterministic, or passing is an operational claim that must be reproduced independently.

## Ford, Parsons, and Kua: architecture fitness functions

Fowler’s [foreword to *Building Evolutionary Architectures*](https://martinfowler.com/articles/evo-arch-forward.html) credits Neal Ford, Rebecca Parsons, and Pat Kua and describes fitness functions monitoring architectural characteristics. The local import check is one modest application: it enforces selected declared dependency constraints. It cannot prove good architecture or eliminate false positives/negatives.

## OpenAI and Anthropic: scoped instructions and repository feedback

Current official [OpenAI AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md), [Codex customization](https://developers.openai.com/codex/customization/overview), and [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory) documentation supports concise/scoped instruction topology and the documented `CLAUDE.md` import/rules patterns. OpenAI’s [long-horizon](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/) and [harness-engineering](https://openai.com/index/harness-engineering/) articles are bounded practitioner case reports about durable artifacts and executable feedback.

The numeric context budgets, lifecycle schema, agent-friction formula, and claimed effects in this scaffold remain **local, unverified hypotheses**. Product semantics are live; sources were retrieved 2026-09-01 and must be rechecked for integration changes.

## Local project choices

The following are not attributed to the cited people or vendors:

- the paired human-authorization and machine-delivery loops;
- authorization, escalation, and acceptance boundaries;
- the one-writer default and risk tiers;
- the exact context/document checks and friction metrics;
- curated exact mutation configuration;
- tool selection and default thresholds.

Treat these as changeable design decisions. Keep them only when local behavior, safety evidence, usability, and maintenance cost justify them.
