---
status: normative
authority: agent-friction-policy
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - ".cleanai/benchmark-tasks.toml"
  - "benchmarks/**"
  - "tools/cleanai.py"
---
# Agent-friction evaluation

Static metrics are proxies. The stronger question is whether agents complete the same bounded task families more correctly, locally, and cheaply after a repository change.

## Stable task bank

Include tasks for locating/explaining behavior, a local change, a cross-module change, an invariant/adversarial test, and a packaging or documentation repair. Keep prompts, starting revisions, environment, agent/model settings, and acceptance evidence comparable.

## Measurements

- accepted completion and post-merge rework;
- human interventions;
- files opened and exploration precision when traceable;
- failed commands and repeated searches;
- changed-file precision, forbidden-surface edits, and diff amplification;
- verification commands actually run and pass rate;
- tokens, tool calls, duration, and cost when available;
- stale or contradictory authority encountered.

## Optional trace format

```json
{"event":"open","path":"src/example/domain/policy.py","tokens":230}
{"event":"tool","tool":"pytest","tokens":0}
```

The bundled ledger reports transparent counts and proportions. It does not establish causal certainty: model nondeterminism, task leakage, prompt drift, caching, model updates, and reviewer differences can dominate small cohorts. Run repeated trials and inspect qualitative failure traces rather than collapsing everything into one vanity score.
