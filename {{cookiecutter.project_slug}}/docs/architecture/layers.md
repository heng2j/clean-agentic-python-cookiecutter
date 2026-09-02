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

The root scientific workspace is not a second runtime layer. Production modules
must not import notebooks, scripts, generated results, or root `static/` files.
Package runtime resources belong below `src/{{ cookiecutter.package_name }}/`
with explicit build configuration and an installed-wheel test. `science-audit`
detects direct absolute imports of those workspace names; dynamic imports and
arbitrary filesystem lookups remain outside that check.

Architecture is not merely folders or diagrams. Its value is reduced change amplification, explicit state/policy ownership, and replaceable delivery mechanisms.
