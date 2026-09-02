---
status: normative
authority: tutorial-context-pruning
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "AGENTS.md"
  - "CLAUDE.md"
  - ".claude/rules/**"
  - "docs/**"
---
# Context-pruning exercise

1. Add a temporary sentence to a disposable copy of `AGENTS.md`: “Read every file and all issue history before any task.”
2. Run `uv run --locked --group dev python tools/cleanai.py context-audit --strict`. Expected: nonzero with a broad-context diagnostic.
3. Replace the sentence with one route to the smallest relevant scoped instruction, or remove it if an executable check already carries the rule.
4. Add a temporary second active document with the same `authority` field. Run `docs-audit --strict`; expect nonzero for duplicate normative authority.
5. Restore/delete the temporary document, rerun both strict audits, and review the non-destructive prune plan:

```bash
uv run --locked --group dev python tools/cleanai.py context-audit --strict
uv run --locked --group dev python tools/cleanai.py docs-audit --strict
uv run --locked --group dev python tools/cleanai.py prune-plan --output artifacts/context/prune-plan.md
```

The planner proposes actions; it never deletes. A human decides whether to reconcile, scope, archive, or remove material. Do not report a smaller word count as universal agent improvement. Compare controlled task runs and state sample/model/tool limitations.
