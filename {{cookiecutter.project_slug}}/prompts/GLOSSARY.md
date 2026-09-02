# Prompt-pack glossary

- **Acceptance criterion:** an observable condition that decides whether the requested outcome is met.
- **Authority:** the current source allowed to decide behavior or policy, such as an accepted contract—not merely the newest or longest document.
- **Baseline:** the preserved state and result before a change.
- **Command-effect preflight:** checking a command's target, writes, deletion, network, credentials, and isolation before execution.
- **Evidence:** reproducible observations such as exit codes, test output, diffs, hashes, or source citations.
- **Fail closed:** reject or block when required evidence is invalid or missing instead of treating it as healthy.
- **Gate:** a command whose result blocks or permits a workflow stage.
- **Invariant:** a condition that must remain true across allowed cases.
- **Mutation test:** a controlled semantic defect used to check whether evidence detects the wrong behavior. It must run in isolation and be restored.
- **Non-goal:** work explicitly outside the task boundary.
- **Residual risk:** uncertainty or possible harm that remains after verification.
- **Rollback:** a tested way to reverse the authorized change without discarding unrelated user work.
- **Scoped instruction:** guidance that applies only to a directory or path set.
- **Trust boundary:** where data or control crosses between parties/components with different trust.
- **Unverified:** not established because required evidence was unavailable or not executed; it does not mean pass.
- **Worktree:** a separate Git working directory tied to the same repository, useful for isolating writers and destructive probes.
