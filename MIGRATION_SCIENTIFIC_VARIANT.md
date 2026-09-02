# Migrating to the scientific variant

This branch is intended for review and new generation. Do not copy its files
over an active project without reviewing local policy, data, license, and hook
choices.

## Material changes

| Area | Main template | Scientific branch | Migration action |
|---|---|---|---|
| Package layout | `src/` | unchanged | Keep it; do not move the package to repository root. |
| Workspace | product/tests/docs | adds notebooks, results, scripts, and static-input contracts | Classify existing files before moving them; preserve history and references. |
| Licenses | MIT, Apache-2.0, proprietary | MIT or Apache-2.0 | Existing proprietary replay contexts are intentionally rejected; obtain a maintainer/legal decision instead of silently relicensing. |
| Hooks | pre-commit YAML | `prek.toml` | Remove the old shim/config, review `prek.toml`, sync, then run `prek install`. |
| Required typing | mypy | Pyrefly 1.2.0 | Run both against the existing tree during migration, review semantic differences, then remove obsolete ignores/config only after acceptance. |
| Experimental typing | none | pinned beta `ty` profile | Treat results as advisory; do not add suppressions merely to make two tools agree. |
| Markdown | docs audit | docs audit plus rumdl | Review reported issues; do not bulk-reformat scientific prose without inspecting equations, tables, links, and front matter. |
| Local environment | uv | uv plus optional direnv | Review `.envrc`; secret loading is disabled by default. Never copy a populated `.env`. |
| Results | project-defined | ignored by default | Decide which small reference outputs merit provenance review before force-adding them. |
| Coverage hosting | local evidence | local evidence plus connected Codecov publication | Configure repository-side Codecov/OIDC only if wanted; local coverage remains the gate. |

## Suggested migration sequence

1. Freeze the current revision, dirty state, commands, lock, and release evidence.
2. Read `SCIENTIFIC_VARIANT.md` and the generated ADR 0004; record project-specific deviations.
3. Add directory contracts and classify existing data/results without moving private or large artifacts into Git.
4. Replace hook and typing configuration, update the lock deliberately, and compare seeded type defects before retiring the old checker.
5. Run the scientific audit, fast gate, release gate, and external-wheel smoke from a clean copy.
6. Reinstall hooks only after the new configuration has been reviewed.

Branch-protection job names, Codecov repository settings, citation metadata,
support policy, contributor governance, and any non-PyPI environment profile are
repository-owner decisions; this branch does not change them automatically.
