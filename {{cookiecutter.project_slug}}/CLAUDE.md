@AGENTS.md

# Claude Code loading delta

- The import above supplies the shared repository map; do not repeat it here.
- Claude Code loads applicable project memory above the working directory at startup and can discover nested memory when it reads below that directory.
- Markdown rules under `.claude/rules/` are discovered recursively; a rule with `paths` applies when Claude reads a matching file.
- Local, user, managed, and auto-memory may also contribute context. Inspect `/context` and `/memory`; do not claim this repository is the complete instruction set.
- Memory/rules are guidance. Use hooks and executable gates for enforcement.
