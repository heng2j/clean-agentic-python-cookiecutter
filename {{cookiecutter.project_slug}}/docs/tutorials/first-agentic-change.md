---
status: normative
authority: tutorial-first-agentic-change
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "prompts/**"
  - "docs/templates/task-packet.md"
---
# First bounded agentic change

Use this exercise for a harmless wording change in a test message. It teaches scope and evidence rather than agent autonomy.

1. Copy `docs/templates/task-packet.md` to `docs/plans/active/first-change.md`.
2. Set the outcome to “clarify one assertion message without changing behavior.” Allow only the one test file and task packet. Name unit behavior and `gauntlet fast` as acceptance evidence. State “no production, dependency, threshold, or unrelated formatting changes.”
3. Give the agent `prompts/coder.md`, `prompts/PROMPT_CONTRACT.md`, and the task packet. Repository text is input data; commands found in it require effect inspection.
4. Before editing, require the agent to reproduce the focused test and report the base revision/dirty state. If authority conflicts or the allowed file is insufficient, it must stop.
5. After the edit, require the focused test, `git diff --check`, and the fast gate. Review the diff yourself.

An acceptable handoff lists: files changed, exact commands and exits, what each result establishes, remaining risk, and rollback. A fluent “all tests pass” without exact evidence is not acceptable.

Archive or remove the completed exercise packet only after the human acceptance decision. Do not put its history into `AGENTS.md`.
