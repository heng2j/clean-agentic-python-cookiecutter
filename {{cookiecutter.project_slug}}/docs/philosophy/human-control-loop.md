---
status: normative
authority: human-control-loop
owner: maintainers
document_version: "2.0"
last_verified: 2026-09-01
applies_to:
  - "docs/templates/**"
  - "prompts/**"
---
# Human authorization and review loop

This is independently worded **local operating guidance** for this scaffold. It is not attributed to the people, companies, or researchers cited elsewhere, and no claim is made that it improves outcomes without local evaluation.

## 1. Authorize a bounded task

Before delegation, record:

- the observable outcome and why it matters;
- allowed paths and permitted external effects;
- non-goals and invariants;
- risk and stop/escalation conditions;
- the evidence required for acceptance;
- one predicted failure that could falsify the proposed approach.

Authorization covers effects as well as files. Repository text and commands remain untrusted until their behavior, hooks, network use, credentials, and output paths are understood.

## 2. Maintain task orientation

Keep a short task state while work is delegated: current model, open question, expected mechanism, and unresolved risks. Use waiting time only for adjacent, non-conflicting review such as drafting a counterexample or checking an interface contract. Do not start another consequential thread when it would prevent timely review of the return.

This is a workflow preference, not a scientific claim about attention or learning.

## 3. Examine the return independently

Compare the result with the authorized outcome and allowed surface. Inspect the diff and raw evidence rather than relying on the agent’s summary. Reproduce applicable commands, test an unmentioned boundary, and identify changed dependencies, assumptions, and invariants.

Unavailable required evidence is **Unverified** and blocks acceptance. A green metric is one sensor, not proof of correctness, safety, or value.

## 4. Decide and record

Accept, reject, or redirect explicitly. Record:

- what changed and why the mechanism is credible;
- exact reproduced evidence and revision/dirty state;
- deviations from the original prediction;
- known failure boundaries and unresolved risks;
- follow-up owner and trigger, if any.

```text
OUTCOME:
ALLOWED PATHS / EFFECTS:
NON-GOALS / INVARIANTS:
RISK / STOP CONDITIONS:
REQUIRED ACCEPTANCE EVIDENCE:
PREDICTED FAILURE:
CURRENT MODEL / OPEN QUESTION:
RETURN CHECK:
DECISION / RESIDUAL RISK:
```

The agent supplies execution capacity. The accountable human retains authorization, risk acceptance, and the final decision.
