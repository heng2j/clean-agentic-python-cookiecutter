---
status: normative
authority: getting-started-first-run
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "README.md"
  - "src/**"
  - "tests/**"
  - "tools/**"
---
# First run, first failure, and recovery

This tutorial assumes Linux, `uv`, and CPython 3.12 or 3.13. Commands run from the generated project root.

## 1. Install the tested dependency set

```bash
uv lock --check
uv sync --locked --group dev
```

Expected: both commands exit `0`. The generated project includes a reviewed `uv.lock`; `--check` verifies that declarations have not drifted, and `--locked` prevents silent re-resolution. Run plain `uv lock` only when intentionally updating dependencies, then review its diff and repeat the release checks.

## 2. Run one behavior and the fast gate

```bash
uv run --locked --group dev {{ cookiecutter.package_name }} examples/healthy-evidence.json
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Expected: both exit `0`. The CLI prints an approved decision. The gate prints each required check and writes a JSON ledger under `artifacts/quality/`.

## 3. Create a controlled failure

Open `src/{{ cookiecutter.package_name }}/domain/change_risk.py`. In `_blocking_reasons`, change this comparison:

```python
if evidence.failed_tests > 0:
```

to the deliberately wrong `< 0`. This makes failed tests pass open while leaving the rest of the policy unchanged.

Run only that file:

```bash
uv run --locked --group dev pytest -q tests/unit/test_change_risk.py
```

Expected: exit `1` with the `failed_tests` case of `test_each_failed_gate_blocks` failing because the decision is approved and the `tests failed` reason is absent. This is evidence that the focused test detects this fail-open behavior; it is not yet evidence that every meaningful behavior is tested.

If the command exits `0`, stop. Confirm you edited the intended file and that the locked command used this project. Do not weaken the assertion or gate.

## 4. Recover and prove success

Restore the original `> 0` comparison, then run:

```bash
uv run --locked --group dev pytest -q tests/unit/test_change_risk.py
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Expected: both exit `0`. Check `git diff --check` and `git status --short` before discarding or committing anything. The tutorial never asks a script to overwrite your edits.

## What you established

**Observed:** one installed behavior works, the focused test detects a controlled contradiction, recovery works, and the fast checks pass. **Not established:** requirements completeness, all security properties, usefulness to users, or release readiness. Continue to the [first bounded agentic change](../tutorials/first-agentic-change.md).
