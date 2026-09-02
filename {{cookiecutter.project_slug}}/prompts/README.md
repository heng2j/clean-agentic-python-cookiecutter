# Portable Clean AI prompt pack

Use [PROMPT_CONTRACT.md](PROMPT_CONTRACT.md) with one role prompt; role files intentionally contain only their delta. Do not copy a role by itself. Start with the [glossary](GLOSSARY.md) if terms such as authority, invariant, mutation, or trust boundary are unfamiliar.

For an authorized consequential change, use sequentially:

```text
Specifier → Coder → Cleaner → Architect → Hardener → QA
```

Choose only the roles justified by consequence:

| Local risk | Minimum pattern |
|---|---|
| Read-only/explanatory | Relevant audit or Specifier pass; no implementation |
| Small reversible behavior change | Specifier, Coder, QA; record why other roles are not applicable |
| Structural or high-consequence change | Use all relevant roles; require an independent human/domain/security oracle for consequential semantics |

The same human or agent may perform several low-risk passes, but that is self-review, not independent evidence. Each pass must preserve its phase boundary. Audit-only work finishes before implementation, and the final human owner accepts risk and release.

Standalone interventions:

| Need | Prompt | Default mode |
|---|---|---|
| Freeze and assess a repository | [audit-existing-repo.md](audit-existing-repo.md) | Audit-only |
| Apply an owner-selected cleanup batch | [clean-existing-repo.md](clean-existing-repo.md) | Implementation |
| Falsify tests and gates | [harden-existing-repo.md](harden-existing-repo.md) | Implementation in isolation |
| Verify a release artifact | [qa-existing-repo.md](qa-existing-repo.md) | Audit-only |
| Audit persistent agent context | [context-hygiene.md](context-hygiene.md) | Audit-only; optional separately authorized remediation |
| Evaluate agent friction | [agent-friction-evaluation.md](agent-friction-evaluation.md) | Isolated experiment |
| Coordinate role handoffs | [orchestrator.md](orchestrator.md) | Coordination; one writer at a time |

These prompts are an unofficial local synthesis inspired by the public Agentic Discipline 6 role spine. The exact contract, ordering, controls, metrics, and one-writer policy are local design choices—not attributed recommendations or endorsement.
