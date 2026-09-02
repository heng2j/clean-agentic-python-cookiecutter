---
status: reference
authority: scientific-source-traceability
owner: maintainers
last_verified: 2026-09-02
retrieved: 2026-09-02
applies_to:
  - "docs/adr/0004-scientific-open-source-profile.md"
  - "notebooks/**"
  - "results/**"
  - "scripts/**"
  - "static/**"
---
# Scientific source traceability

These sources informed candidates for this profile. They do not endorse this
project and do not become repository authority merely because they are cited.

| ID | Source | Bounded support | Limitation or local delta |
|---|---|---|---|
| JV-GUIDE | Jonathon Vandezande, [Setting Up Python Packages](https://jevandezande.github.io/blog/setting-up-python-packages/), published 2026-03-03 | Practitioner rationale for uv, direnv, Ruff, typing, pytest, `prek`, coverage, and the proposed science-oriented directory list. | The author labels layout choices as preference. This profile does not copy automatic environment, Git, hook, or remote side effects. |
| JV-TEMPLATE | Jonathon Vandezande, [`uv-cookiecutter`](https://github.com/jevandezande/uv-cookiecutter), commit `3446ae618cd4e226bee102e30bcf0368fe5d628f` inspected 2026-09-02 | Concrete implementation of the guide. | Local reproduction found a coverage command without a fail-under floor, incomplete claimed hook installation, cross-version CI drift, an invalid `APL-2.0` metadata value, and a wheel smoke command able to import the live flat source. None of those mechanics are inherited. |
| ROWAN-GUIDE | Rowan Scientific, [How to Make a Great Open Source Scientific Project](https://www.rowansci.com/blog/how-to-make-a-great-open-source-scientific-project), published 2025-09-09 | Opinionated practitioner guidance on focused scope, packaging, cleanliness, tests, API design, documentation, maintenance, and open-source licensing. | It is not an empirical standard. Coverage, latest-version, environment-manager, commenting, and licensing preferences are not universalized here. |
| PYPA-SRC | Python Packaging User Guide, [`src` layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) | Explains how `src` layout helps prevent accidental imports from the working tree and keeps non-package files off the import path. | It does not prove a wheel is correct; the external-install smoke test remains required. |
| SPEC-0 | Scientific Python, [SPEC 0: Minimum Supported Dependencies](https://scientific-python.org/specs/spec-0000/) | A time-window policy that projects can use for support decisions. | This starter keeps its narrower tested support claim; adopters decide whether SPEC 0 fits their users. |
| FAIR4RS | Chue Hong et al., [FAIR Principles for Research Software](https://doi.org/10.15497/RDA00068) | Community principles for making research software findable, accessible, interoperable, and reusable. | FAIR principles do not establish scientific correctness or make all artifacts redistributable. |
| FORCE11 | FORCE11, [Software Citation Principles](https://force11.org/info/software-citation-principles-published-2016/) | Treats software as a citable research product. | Structured citation metadata needs real authors and identifiers, so this template does not fabricate a `CITATION.cff`. |
| DIRENV | direnv, [official documentation](https://direnv.net/) | `.envrc` is shell code loaded after explicit authorization and can use the standard library to load dotenv values and adjust paths. | direnv is convenience, not secret storage; inherited variables remain readable by child tools and agents. |
| UV | Astral, [uv documentation](https://docs.astral.sh/uv/) | Locking, syncing, running, and building Python projects. | uv does not manage every system/HPC dependency and a lock does not prove scientific reproducibility. |
| RUFF | Astral, [Ruff documentation](https://docs.astral.sh/ruff/) | Formatter, linter, and pydocstyle convention configuration. | Google convention selection does not prove documentation quality or scientific clarity. |
| TY | Astral, [ty documentation](https://docs.astral.sh/ty/) | Current `ty check` usage and configuration. | `ty` remains beta and is a pinned experimental profile here, not a release gate. |
| PYREFLY | Meta, [Pyrefly documentation](https://pyrefly.org/) | Stable static Python type checker with public scientific-ecosystem work. | It is the local canonical checker, but static analysis remains bounded evidence and Pyrefly does not promise strict semantic-version compatibility. |
| PREK | `prek`, [official documentation](https://prek.j178.dev/) | Fast hook runner with pre-commit-compatible concepts and TOML configuration. | Local hooks are bypassable and do not replace CI. |
| RUMDL | `rumdl`, [official documentation](https://rumdl.readthedocs.io/) | Markdown linting and formatting. | The project gates on `rumdl check`; formatting alone may not expose every remaining violation. |
| CODECOV | Codecov, [GitHub Action documentation](https://github.com/codecov/codecov-action) | Connected publication of a coverage report. | The upload does not prove adequate tests and cannot replace the local coverage threshold. |

## Contradictions preserved

The inspiration sources and their repositories do not demonstrate one universal
scientific layout or tool policy. Rowan projects use different layouts,
docstring conventions, typing configurations, and environment managers. Some
public examples use Conda despite the blog's blanket discouragement. That
variation is evidence to choose per project—not a contradiction to reconcile
silently.
