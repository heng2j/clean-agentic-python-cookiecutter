# Original claim–evidence matrix

| Claim | Classification | Evidence | Verdict / correction |
|---|---|---|---|
| The experimental branch descends from the scientific variant | **Observed** | Experimental/scientific merge base is `72a7e52e`; experimental head is `ab3e06f` | Supported |
| Graft is optional and not a Python dependency | **Observed** | Render lock, pytest, build, and Twine succeed with no `graft` executable | Supported, but canonical gates are independently broken |
| Required Graft 0.17.0 can be installed as documented | **Observed** | `npm view @nanonets/graft@0.17.0` returns E404; latest published is 0.16.0 | False |
| The pin corresponds to reviewed upstream source | **Source-supported** | Upstream commit `05760b07` declares 0.17.0 but has no matching published npm release/tag | Source exists; distributable identity does not |
| The adapter is project-scoped | **Observed** | State paths are lexical project paths | False under symlinks and positional source symlinks |
| The adapter strips credentials | **Observed** | It removes eight names from a copied environment; arbitrary/cloud/npm/Git credentials remain | Materially incomplete; privacy claim must say minimal allowlist or fail |
| Structural mode is telemetry-off | **Source-supported** | Graft telemetry gate checks `DO_NOT_TRACK`; adapter sets it | Supported for reviewed source path; not a network sandbox, and install/update behavior is separate |
| The adapter suppresses update checks | **Source-supported** | It writes a fresh project-home update cache; upstream consults 24-hour cache | Version-specific and mutating; symlink overwrite reproduced |
| Deep/model access is blocked | **Observed** | Known deep/provider flags are denylisted | Partial: broad pass-through is not a future-proof capability boundary |
| `init`, hooks, and global agent changes are absent by default | **Observed** | No init invocation or committed upstream host files | Supported positive control |
| All nine advertised CLI operations use the project graph | **Observed** | Real 0.16 and source-built 0.17 adapter-semantics trials | False: six operations failed or returned empty due graph-root handoff |
| Ranked retrieval reduces context | **Unverified** | No controlled accepted-task model/client trial; upstream self-estimates exclude fixed/fallback/review cost | Do not claim |
| Ranked retrieval is exhaustive | **Observed** | Fixture misses dynamic/config/wheel/duplicate-symbol edges; docs disclaim exhaustiveness | False, correctly disclaimed in prose |
| `ask --source` is precise on the held-out fixture | **Observed** | File-level micro precision 12/40 = 0.30; recall 12/15 = 0.80 | Mixed; useful lead generator, noisy evidence |
| Blast radius is complete | **Observed** | Duplicate-name case found 0/4 known downstream; unique static control found 3/3 | False; symbol ambiguity is material |
| Freshness detects ordinary edits | **Observed** | Unstaged edit, staged move, deletion, and untracked addition were detected/refreshed | Supported for tested fixture |
| A no-server LSP run is clearly unverified | **Observed** | Exit 0, zero added LSP edges, terse `lsp:none` | False-success risk; cohort remains unverified |
| MCP is merely another bounded adapter surface | **Source-supported** | Upstream server supplies its own instructions/schema and boot upkeep | False; distinct higher-risk capability |
| The MCP opt-in stays local/uncommitted | **Observed** | `.mcp.json` is not ignored and `git add --dry-run` stages it | False operational control |
| Persistent agent context remains concise | **Observed** | Six baseline context files are byte-identical to parent; root route proxy 973 tokens | Supported, but Graft is undiscoverable and MCP runtime schema cost is unmeasured |
| The documented comparison is controlled and blinded | **Observed** | `run.json` exposes expected/forbidden globs and verification; major controls absent | False |
| Graft output is derived navigation evidence | **Observed** | Repeated explicit language in guide/prompt | Supported and must remain |
