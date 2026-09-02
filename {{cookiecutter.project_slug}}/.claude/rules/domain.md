---
paths:
  - "src/{{ cookiecutter.package_name }}/domain/**/*.py"
---
# Domain scope

- Keep domain policy deterministic and free of file, network, framework, clock, and environment effects.
- Preserve typed immutable values and inward dependencies.
- Reproduce behavior before policy edits; consequential comparison/threshold changes require focused behavior evidence and an isolated curated mutant.
