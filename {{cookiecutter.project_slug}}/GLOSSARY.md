# Plain-language glossary

- **Acceptance evidence:** something observable that shows a requested behavior worked, such as an exit code plus output from an installed wheel.
- **Agent context file:** persistent instructions such as `AGENTS.md` or `CLAUDE.md` that a tool may load automatically. It is configuration, not a project diary.
- **Architecture fitness function:** a repeatable check for one declared structural rule, such as “domain code must not import adapters.” It cannot prove the whole architecture is good.
- **Artifact:** generated output such as coverage JSON, a wheel, or a command ledger. Artifacts are evidence, not authority.
- **CRAP:** an experimental change-risk equation combining complexity and coverage. This project uses a documented local approximation.
- **Gate:** a command that exits nonzero when required evidence fails or is unavailable.
- **Invariant:** a property that must remain true over many inputs, not only a single example.
- **Mutation test:** a deliberate small defect used to see whether a test or specification detects it. A survivor may expose weak evidence, an equivalent mutant, or a bad oracle.
- **Normative document:** a current source of project rules. Research, archives, and generated reports are not normative.
- **Oracle:** the independent condition used to decide success, such as expected CLI output or a package installed outside the checkout.
- **Residual risk:** what the completed checks still cannot establish.
- **Source-supported:** a statement bounded by a cited primary source. It is different from a local design choice.
- **Task packet:** a small change contract containing outcome, allowed paths, non-goals, risks, acceptance evidence, and stop conditions.
- **Worktree:** a second working directory for one Git repository. It is useful for isolation only when the base revision and write ownership are clear.

If a report uses a term not explained here or in its command reference, treat that as a documentation defect.
