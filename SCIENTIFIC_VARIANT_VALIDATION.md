# Scientific variant validation

Validation date: 2026-09-02. This is bounded evidence for the branch contents,
not a timeless guarantee or a claim of scientific validity.

## Environment

| Property | Observed value |
|---|---|
| Operating system | Linux 6.18.35, x86_64 |
| CPython | 3.12.13 and 3.13.14 |
| uv | 0.11.33, retained because this is the version independently used to regenerate and check both locks |
| Git | 2.51.1 |
| Cookiecutter | 2.7.1 from the reviewed template environment |
| direnv | unavailable; `.envrc` received Bash syntax and side-effect review only |
| Network | available for dependency resolution; deterministic profiles ran from the installed lock |

## Reproduced paths

| Path | Exact command or probe | Exit | Observed result |
|---|---|---:|---|
| Template | `uv lock --check` | 0 | Root declarations matched the reviewed lock. |
| Template | `uv run --locked --group test python -m pytest -q` | 0 | Generator, validation, hook-safety, license, and replay tests passed. |
| Template | `python -m build --no-isolation` plus `twine check` | 0 | Wheel and sdist built; both metadata checks passed. |
| Default render, Python 3.12 | `uv lock --check`; `uv sync --locked --group dev --python 3.12`; release gauntlet | 0 | Fast/full/hardening/release steps passed, including external-wheel installation. |
| Python 3.13, Apache-2.0, Actions disabled | generation plus locked sync and release gauntlet | 0 | Workflow was absent, Apache license/NOTICE rendered, and release passed. |
| Default render, Python 3.13 | locked sync and release gauntlet | 0 | Product branch coverage 96.75%; harness branch coverage 81.61%; worst local CRAP approximation 10.10; all three code and three specification mutants killed. |
| Hooks | `prek install`; `prek run --all-files` | 0 | Both `pre-commit` and `pre-push` shims existed; the non-mutating fast hook passed. |
| Experimental typing | sync `typing-experimental`; run its gauntlet | 0 | Pinned beta `ty` passed the healthy render. |
| Workflow structure | parse rendered `quality.yml` as YAML | 0 | Four jobs present, including separately named connected Codecov publication. |
| Package contents | inspect wheel and sdist; rebuild with harmless `.env` fixture | 0 | Scientific workspace absent from the wheel; `.env` absent from both archives. |

## Seeded sensitivity

| Intended failure | Seed | Oracle | Exit | Detected |
|---|---|---|---:|---|
| Required type mismatch | A function declared `-> int` returned a string | Pyrefly required check | 1 | yes, `bad-return` |
| Experimental type mismatch | Same controlled file | beta `ty` profile | 1 | yes, `invalid-return-type` |
| Unregistered scientific input | Added `static/unregistered.csv` without a manifest entry | `science-audit --strict` | 1 | yes, `science.static-unregistered` |
| Manifest/path/hash/secret/result-ignore defects | Dedicated tooling fixtures | focused pytest file | 0 | yes; fixtures assert each nonzero finding class |

Every live seeded file was removed after its probe, and the healthy release
gauntlet was rerun. The machine-readable companion records the command list and
exit codes.

## Unverified and bounded claims

- Native macOS and Windows remain **Unverified**. The generated project claims Linux x86_64 only.
- Actual `direnv allow`/deny behavior is **Unverified** here because direnv was unavailable. It is optional and absent from CI.
- Codecov upload is **Unverified** until a generated public repository pushes to `main` with GitHub OIDC and Codecov available. The workflow syntax, condition, least-privilege job permission, action SHA, CLI version, and explicit XML path were inspected.
- Jupyter/marimo execution is **Unverified** and intentionally not installed. Notebooks are a directory contract, not a passing execution claim.
- `science-audit` checks internal paths, explicit imports, metadata, and hashes. It cannot establish dataset truth, license ownership, command execution, statistical validity, privacy, or scientific correctness.
- uv covers the PyPI-resolvable profile only. MPI, CUDA, native solvers, and other system environments require a separately tested decision.
- Pyrefly and beta `ty` can change diagnostics across upgrades; both versions are locked and upgrades require repeated sensitivity trials.

## Release recommendation

**Observed:** no unresolved release-blocking failure remains in the tested Linux
3.12/3.13 matrix. Recommend the branch as a review candidate for small,
PyPI-resolvable open-source scientific Python projects, subject to successful
GitHub branch CI. Do not generalize that recommendation to scientific validity,
secret isolation, notebook reproducibility, native cross-platform support, or
non-PyPI/HPC environments.
