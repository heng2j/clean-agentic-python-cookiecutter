.DEFAULT_GOAL := help

.PHONY: help bootstrap lock-check test pre-commit gate-fast gate-full gate-hardening gate-release connected-audit context-audit docs-audit prune-plan crap mutate clean

help: ## Show targets.
	@awk 'BEGIN {FS = ":.*## "; printf "Targets:\n"} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

bootstrap: ## Install development dependencies with uv.
	uv sync --locked --group dev

lock-check: ## Verify pyproject.toml agrees with the reviewed lock.
	uv lock --check

test: ## Run all core tests.
	uv run --locked --group dev python -m pytest -q

pre-commit: ## Run non-mutating repository checks.
	uv run --locked --group dev pre-commit run --all-files

gate-fast: ## High-frequency local gate.
	uv run --locked --group dev python tools/cleanai.py gauntlet fast

gate-full: ## Merge-quality gate.
	uv run --locked --group dev python tools/cleanai.py gauntlet full

gate-hardening: ## Full gate plus curated mutations.
	uv run --locked --group dev python tools/cleanai.py gauntlet hardening

gate-release: ## Hardening plus packaging smoke.
	uv run --locked --group dev python tools/cleanai.py gauntlet release

connected-audit: ## Query the live vulnerability database; not an offline gate.
	uv run --locked --group dev python tools/cleanai.py gauntlet connected-audit

context-audit: ## Audit AGENTS/CLAUDE precision.
	uv run --locked --group dev python tools/cleanai.py context-audit --strict

docs-audit: ## Audit Markdown lifecycle and links.
	uv run --locked --group dev python tools/cleanai.py docs-audit --strict

prune-plan: ## Produce a non-destructive cleanup proposal.
	uv run --locked --group dev python tools/cleanai.py prune-plan --output artifacts/context/prune-plan.md

crap: ## Generate coverage and CRAP evidence.
	uv run --locked --group dev python -c "from pathlib import Path; Path('artifacts').mkdir(exist_ok=True)"
	uv run --locked --group dev python -m coverage run -m pytest -q
	uv run --locked --group dev python -m coverage json -o artifacts/coverage.json
	uv run --locked --group dev python tools/cleanai.py crap --coverage artifacts/coverage.json --strict

mutate: ## Run curated code and specification mutants.
	uv run --locked --group dev python tools/cleanai.py mutate --config .cleanai/code-mutations.toml --strict
	uv run --locked --group dev python tools/cleanai.py mutate --config .cleanai/spec-mutations.toml --strict

clean: ## Remove generated evidence/build output.
	python -c "from pathlib import Path; import shutil; [shutil.rmtree(path, ignore_errors=True) for path in map(Path, ('artifacts', 'dist', 'build', 'htmlcov'))]; Path('.coverage').unlink(missing_ok=True)"
