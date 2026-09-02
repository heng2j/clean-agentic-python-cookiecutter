# Scientific open-source variant

This branch adapts Clean Agentic Python Cookiecutter for small open-source
scientific Python projects. It is inspired by Jonathon Vandezande's
[package setup guide](https://jevandezande.github.io/blog/setting-up-python-packages/),
his [`uv-cookiecutter`](https://github.com/jevandezande/uv-cookiecutter), and
Rowan Scientific's
[open-source project guide](https://www.rowansci.com/blog/how-to-make-a-great-open-source-scientific-project).
Those are practitioner sources, not standards, and their inclusion does not
imply sponsorship or endorsement.

## Decision summary

| Candidate practice | Decision | Reason |
|---|---|---|
| Top-level package directory | Reject | The retained `src/` layout helps prevent source-checkout imports from hiding wheel defects. |
| `notebooks/`, `results/`, `scripts/`, `static/` | Adapt | Each directory has a narrow contract; generated results and private or large inputs are not committed by default. |
| `direnv` and `.env` | Adapt | `.envrc` is reviewable and side-effect-light; `.env` is ignored and never treated as a secret vault. |
| Automatic sync, hook installation, Git commit, or remote creation during generation | Reject | Generation must not create hidden network, repository, or account side effects. |
| Ruff and Google-style docstrings | Adopt with limits | Ruff enforces a consistent convention; scientific rationale, units, equations, and numerical caveats still belong in useful prose. |
| `ty` and Pyrefly | Adapt | Stable Pyrefly is the canonical gate. Beta `ty` is a pinned explicit experiment, not a second claim of correctness. |
| `prek` | Adapt | Hooks call locked, non-mutating project commands; hooks remain bypassable, so CI is authoritative. |
| Codecov | Adapt | It publishes the already-generated XML report as a connected CI check; local coverage policy remains authoritative. |
| Separate `.coveragerc` | Reject | Coverage already has one configuration authority in `pyproject.toml`. |
| Universal coverage percentage or latest-Python-only policy | Reject | Thresholds and support windows are local risk decisions, not universal scientific rules. |
| uv-only for every scientific stack | Narrow | uv is the verified default for PyPI-resolvable Python projects; MPI, CUDA, system solvers, or non-Python stacks may need another environment profile. |

## What this branch adds

- scientific directory contracts and a checked static-input manifest;
- safe-by-default local environment loading;
- a concise contributor, security, and pull-request path;
- scientific method, reproducibility, data, and results guidance;
- Ruff, rumdl, Pyrefly, pytest, `prek`, GitHub Actions, and an optional pinned `ty` experiment;
- a connected Codecov upload that cannot replace the local coverage gate; and
- source-to-decision documentation for the adaptations above.

The generated project remains intentionally small. It does not install a
notebook runtime until an adopter deliberately chooses Jupyter, marimo, or
another tool and records that dependency decision.
