---
status: reference
authority: source-traceability
owner: maintainers
evidence_version: "2.0"
last_verified: 2026-09-01
retrieved: 2026-09-01
applies_to:
  - "README.md"
  - "docs/philosophy/**"
  - "docs/research/**"
  - "prompts/**"
---
# Source traceability

This repository is an independent, unofficial synthesis. It is not authored, sponsored, or endorsed by Justin Martin, Robert C. Martin, Clean Coders, Matt Pocock, Alberto Savoia, Bob Evans, OpenAI, Anthropic, or the cited researchers. A citation supports only the bounded statement recorded below; it does not endorse this scaffold or transfer authority from its authors.

## Public source register

| ID | Source/version | What it supports | What it does not establish |
|---|---|---|---|
| CLEANAI-SERIES | [Clean AI series](https://cleancoders.com/series/clean-ai), live page retrieved 2026-09-01 | The named public series exists. | The correctness or efficacy of this Python scaffold. |
| AD6 | [“Agentic Discipline 6: Swarm Forge Demonstration”](https://cleancoders.com/episode/agentic-discipline-6), public page credited to **Justin Martin and Robert “Uncle Bob” Martin**, retrieved 2026-09-01 | Six named roles, isolated Git worktrees, numbered handoff order, Gherkin/manual UI artifacts, unit/acceptance testing, DRY/CRAP cleaning, modular/dependency review, property tests, language/Gherkin mutation, and automated UI QA. | Universal thresholds, local commands, context lifecycle, risk classes, evidence schemas, one-writer policy, measured efficacy, or nonpublic implementation/license details. |
| INTERVIEW | [“LIVE: Uncle Bob on Software Fundamentals in the Age of AI”](https://www.youtube.com/watch?v=zcLPGC-tvgk), public live video interview hosted by Matt Pocock, retrieved 2026-09-01 | Publicly identifies an interview/conversation with Robert C. Martin. | No substantive workflow claim here relies on an inaccessible transcript, inferred episode detail, or the ambiguous label “podcast.” |
| CRAP-V01 | Alberto Savoia, [“The CRAP Metric Equation” / Part II](https://www.artima.com/weblogs/viewpost.jsp?thread=210575), 2007-07-19 | Experimental CRAP v0.1 equation and change-risk framing; identifies Bob Evans as collaborator; defines Java-method cyclomatic complexity with basis-path coverage. | Peer-reviewed validation, universal predictive accuracy, this Python measurement basis, or a universal gate. |
| CRAP4J | Alberto Savoia, [crap4j article](https://www.artima.com/weblogs/viewpost.jsp?thread=215899), 2007-10-02 | Later prototype discussion and the authors’ **initial experimental** interpretation that scores 30 or higher were CRAP; points back to CRAP-V01 as the original blog. | Calibration of this repository’s local AST/line score or its strict comparator. |
| FOWLER-REFACTOR | Martin Fowler, [Refactoring guide](https://martinfowler.com/tags/refactoring.html), live page retrieved 2026-09-01 | Small internal, behavior-preserving transformations that keep software working. | This prompt’s exact Cleaner contract or proof that a change preserved behavior. |
| NORTH-BDD | Dan North, [Introducing BDD](https://dannorth.net/blog/introducing-bdd/), [BDD by example](https://dannorth.net/blog/bdd-by-example/), and [testing essay](https://dannorth.net/blog/we-need-to-talk-about-testing/), retrieved 2026-09-01 | Examples, scenarios, shared vocabulary, business value, and stakeholder-facing evidence. | That Gherkin syntax alone guarantees shared understanding or adequate testing. |
| CD | Martin Fowler, [Continuous delivery guide](https://martinfowler.com/delivery.html), retrieved 2026-09-01 | Always-releasable software and staged automated feedback with increasing confidence. | That this repository’s profiles are complete, passing, or universally appropriate. |
| EVO-ARCH | Martin Fowler’s foreword to Neal Ford, Rebecca Parsons, and Pat Kua’s [*Building Evolutionary Architectures*](https://martinfowler.com/articles/evo-arch-forward.html), retrieved 2026-09-01 | Fitness functions monitor selected architecture characteristics. | That a Python import parser proves good architecture in general. |

Versioned empirical-paper metadata, samples, methods, findings, contradictions, and limits are in [empirical paper evidence](paper-notes.md).

## Current official product documentation

These are live product documents, not frozen specifications. Recheck them when changing integration behavior.

| ID | Official source | Bounded support |
|---|---|---|
| OAI-AGENTS | OpenAI, [AGENTS.md configuration](https://developers.openai.com/codex/agent-configuration/agents-md), retrieved 2026-09-01 | Codex root-to-working-directory instruction chain, one recognized file per directory, closer-file precedence, and configured size/fallback behavior. |
| OAI-CUSTOM | OpenAI, [Codex customization overview](https://developers.openai.com/codex/customization/overview), retrieved 2026-09-01 | Keep routing guidance small and place specialized instructions near their scope. |
| OAI-LONG | OpenAI, [long-horizon task case report](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/), retrieved 2026-09-01 | One bounded practitioner example using durable prompt/plan/implementation artifacts and milestone validation. |
| OAI-HARNESS | OpenAI, [Harness engineering](https://openai.com/index/harness-engineering/), retrieved 2026-09-01 | One repository-specific case favoring a concise map, repository system of record, legibility, and executable feedback; the article limits generalization. |
| ANTH-MEM | Anthropic, [Claude Code memory](https://code.claude.com/docs/en/memory), retrieved 2026-09-01 | Claude Code reads `CLAUDE.md`, supports `@AGENTS.md` import, recursive rules, and `paths:`-scoped rules. Prose remains context, not guaranteed enforcement. |

## CRAP: original metric versus local approximation

| Property | CRAP-V01 / CRAP4J | This repository |
|---|---|---|
| Unit | Java method | Python callable |
| Complexity | Cyclomatic decisions as defined by the original tool | Documented local Python AST decision count |
| Coverage | Basis-path coverage | coverage.py line evidence mapped to a callable |
| Equation | `complexity² × (1 - coverage/100)³ + complexity` | Same algebra applied to non-equivalent local measurements |
| Threshold | Later article’s initial, explicitly experimental “30 or higher” interpretation | Configurable `max_crap_score`; current strict check fails only when the worst score is **greater than** the configured budget, so exactly 30 passes at the default |

The local value is therefore a **CRAP approximation**, not a result comparable to crap4j. The default 30 and `>` comparator are local design choices, not a Savoia–Evans recommendation. A low score does not prove correctness, assertion quality, cohesion/coupling, security, domain validity, or maintainability.

## Source-to-practice mapping

| Local practice | Source support | Local delta and verification status |
|---|---|---|
| Six role names and public handoff spine | AD6 | Prompt fields, risk shaping, evidence schema, and use outside the demonstrated UI workflow are local synthesis. |
| Cleaner preserves behavior | FOWLER-REFACTOR; AD6 names Cleaner/DRY/CRAP activity | Exact commands, budgets, and behavior oracle are local and require executable evidence. |
| Gherkin/examples for acceptance | AD6; NORTH-BDD | Local parser, task-packet format, and coverage of non-UI projects are local. |
| CRAP report | CRAP-V01 and CRAP4J | AST/line mapping, configurable budget, and `>` boundary are local; predictive value is unverified. |
| Layered feedback profiles | CD | Profile composition, connected checks, and release criteria are local and must be reproduced rather than inferred from tradition. |
| Import-based architecture check | EVO-ARCH | Enforces selected declared constraints only; false negatives/positives and dynamic imports remain tool-specific risks. |
| Concise/scoped agent instructions | OAI-AGENTS, OAI-CUSTOM, ANTH-MEM | Numeric budgets, lifecycle metadata, and effectiveness are local hypotheses. |
| Durable plans and executable repository feedback | OAI-LONG, OAI-HARNESS | First-party case reports are bounded; this scaffold’s causal benefit is unverified. |
| Paper-influenced context/refactoring/debt practices | PAPER-CTX through PAPER-REFACTOR | Research notes are reference evidence. Normative choices require a local decision record and local tests. |
| Human authorization/review loop | [local human-control guidance](../philosophy/human-control-loop.md) | Independently worded local synthesis; no claim of third-party authorship, endorsement, or empirical validation. |

## Release discipline for claims

When a source or product document changes, update the frozen version/retrieval field, describe the actual change, and rerun the affected local check. Do not update `last_verified` merely because a date elapsed. An inaccessible source, missing client, or unresolved contradiction is **Unverified**, not supported.
