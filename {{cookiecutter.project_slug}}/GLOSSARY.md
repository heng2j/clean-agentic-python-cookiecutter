# Plain-language glossary

- **Acceptance evidence:** something observable that shows a requested behavior worked, such as an exit code plus output from an installed wheel.
- **Agent context file:** persistent instructions such as `AGENTS.md` or `CLAUDE.md` that a tool may load automatically. It is configuration, not a project diary.
- **Architecture fitness function:** a repeatable check for one declared structural rule, such as “domain code must not import adapters.” It cannot prove the whole architecture is good.
- **Artifact:** generated output such as coverage JSON, a wheel, or a command ledger. Artifacts are evidence, not authority.
- **Blast radius:** files or symbols a change may affect through known structural relationships. A static blast report is a lead for inspection, not a complete impact proof.
- **CRAP:** an experimental change-risk equation combining complexity and coverage. This project uses a documented local approximation.
- **Data provenance:** evidence linking an input to its origin, license, transformation, and content identity. A recorded hash alone is not provenance.
- **direnv:** an optional tool that loads reviewed directory-specific shell configuration. It does not isolate or securely store secrets.
- **Gate:** a command that exits nonzero when required evidence fails or is unavailable.
- **Graft:** the optional external code-navigation tool evaluated by this branch. Its index and output are derived evidence, not project authority.
- **Graph freshness:** whether an index represents the current files and revision. A graph can be fresh yet incomplete because static analysis cannot see every runtime relationship.
- **Invariant:** a property that must remain true over many inputs, not only a single example.
- **Mutation test:** a deliberate small defect used to see whether a test or specification detects it. A survivor may expose weak evidence, an equivalent mutant, or a bad oracle.
- **MCP:** Model Context Protocol, a way for a client to expose tool schemas and calls to an agent. Available schemas have a fixed context and lifecycle cost even when the agent never calls them.
- **Normative document:** a current source of project rules. Research, archives, and generated reports are not normative.
- **Oracle:** the independent condition used to decide success, such as expected CLI output or a package installed outside the checkout.
- **Residual risk:** what the completed checks still cannot establish.
- **Ranked retrieval:** a relevance-ordered set of likely useful results. It may omit matching or related code and therefore cannot answer “all,” “every,” or “none” by itself.
- **Structural index:** a regenerable map inferred from files, symbols, imports, and calls. It describes relationships a tool detected, not program truth or design rationale.
- **Symbol skeleton:** a compact view of a file's named interfaces and source spans. Read the exact source before relying on behavior omitted from the skeleton.
- **Source-supported:** a statement bounded by a cited primary source. It is different from a local design choice.
- **Static-input manifest:** the `static/manifest.toml` inventory checked for contained paths, required metadata, and matching SHA-256 values.
- **Task packet:** a small change contract containing outcome, allowed paths, non-goals, risks, acceptance evidence, and stop conditions.
- **Worktree:** a second working directory for one Git repository. It is useful for isolation only when the base revision and write ownership are clear.

If a report uses a term not explained here or in its command reference, treat that as a documentation defect.
