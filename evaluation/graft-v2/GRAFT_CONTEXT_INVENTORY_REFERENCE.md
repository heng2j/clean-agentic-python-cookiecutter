# Graft context inventory reference

The machine-readable inventories are:

- `GRAFT_CONTEXT_INVENTORY_ORIGINAL.json` — frozen pre-fix inventory.
- `GRAFT_CONTEXT_INVENTORY_V2.json` — current enhanced-template snapshot.

## Material change

**Observed:** the original feature added zero bytes to routinely loaded context
because it was orphaned from canonical agent routes. V2 adds one concise
on-demand route to `AGENTS.md`: +2 lines, +21 words, +132 characters, or +33
`ceil(characters/4)` proxy tokens. `CLAUDE.md` remains unchanged and delegates
to `AGENTS.md`.

| Effective root route | Original proxy | V2 proxy | Delta |
|---|---:|---:|---:|
| Codex-compatible root `AGENTS.md` | 973 | 1,006 | +33 |
| Claude-compatible `AGENTS.md` + `CLAUDE.md` | 1,134 | 1,167 | +33 |

**Observed:** v2 removes the MCP example and does not configure upstream MCP
instructions, tool schemas, hooks, status lines, prompt injection, or generated
memory. Detailed Graft material is pulled from the entry guide, integration
reference, troubleshooting guide, tutorial, or evaluator prompt only when
needed. Implementation commit `6966b55` adds the observed hidden-directory and
public-versus-durable path boundaries; final implementation source `b719459`
narrows that evidence wording. Neither changes routinely loaded context.

**Observed:** the formal evaluator role requires both
`prompts/evaluate-graft.md` and `prompts/PROMPT_CONTRACT.md`. Their combined
on-demand context is 147 lines, 1,339 words, 9,995 characters, or 2,499
character/4 proxy tokens. The required-before-install runtime-lock README adds
21 lines, 128 words, 1,049 characters, or 263 proxy tokens. The inventory now
records these direct prerequisites; general project README/docs indexes that
merely route to them are ordinary navigation, not Graft-only context.

The complete Graft-specific on-demand inventory sums to 881 lines, 6,111 words,
44,930 characters, or 11,235 proxy tokens. That is an inventory total, not a
routine or recommended single-session load; progressive disclosure requires the
smallest task-relevant subset.

**Unverified:** character/4 values are not client tokenizer or billing truth.
Actual client discovery, managed/user instruction precedence, caching, and
runtime schema injection were not observed. No claim about exact model context
is made.

**Recommended:** retain the single router line while F1 remains experimental.
Do not copy upstream Graft instructions into `AGENTS.md` or `CLAUDE.md`; remove
the route if F1 is removed.
