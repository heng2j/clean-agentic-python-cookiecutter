---
status: normative
authority: architecture-layer-policy
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "src/**"
  - ".cleanai/policy.toml"
---
# Architecture layers

The starter system declares:

```text
adapters  →  application  →  domain
```

- `domain` contains stable immutable values and deterministic policy.
- `application` coordinates use cases using domain types.
- `adapters` translate CLI, JSON, network, framework, or persistence concerns.

Imports may point inward or remain in a layer. The AST fitness function fails when an inward layer imports an outward layer. Replace the layer names and levels in `.cleanai/policy.toml` to model the actual project. Add explicit exceptions rather than hiding violations.

Architecture is not merely folders or diagrams. Its value is reduced change amplification, explicit state/policy ownership, and replaceable delivery mechanisms.
