# Original capability decision matrix

These decisions use the frozen original implementation and evidence. “Cost”
includes setup, fixed context, fallback inspection, review, and correction—not
only Graft output size.

| Capability | Intended value | Observed value | Material cost / failure | Original decision |
|---|---|---|---|---|
| F0 — no Graft | Ordinary concise context, `rg`, tests | Direct pytest (125), build, and Twine passed without Graft | Canonical gauntlets still stop on a Graft-test format defect | **Keep; repair regression** |
| F1 — structural CLI | Faster location, API, flow, impact navigation | Unique static calls and freshness controls worked; `ask --source` fixture recall 0.80 | Package pin unavailable; six commands miswired; precision 0.30; duplicate/dynamic/config/package misses; unsafe wrapper | **Replace boundary; remain experimental** |
| F2 — structural MCP | On-demand structured retrieval inside clients | Upstream exposes six tools | Fixed schemas/instructions unmeasured in clients; schemas bypass caps; graph root/upkeep/lifecycle hazards; config commit-prone | **Disable** |
| F3 — deterministic export | Reviewable map/blast artifact | Isolated real Graft emitted 49 KB radius and 85 KB map HTML | Inherits false negatives and source/history sensitivity; not an authority artifact | **Experimental only; do not promote** |
| F4 — LSP enrichment | Better compiler-grade call edges | `--lsp` with no server exited 0 and added zero edges | Cryptic `lsp:none`; real Python LSP cohort not executed | **Unverified; disabled** |
| F5 — model-backed deep summaries | Concept explanations | Not run; prohibited by default contract | Source disclosure, credentials, variable cost, hallucination/staleness | **Reject by default** |
| F6 — hooks/prompt injection | Automatic freshness and tool use | Source inspection shows host instructions/hooks/status/upkeep paths | Global/host writes, fixed context, competing authority, hidden activity | **Reject** |

## Promotion rule

No token or orientation gain can promote F1 until the same independently
verified task remains correct and accepted, the adapter has a closed command
surface, the real package is reproducibly installable, and P0/P1 findings are
resolved. F2–F6 are not implied by any F1 result.
