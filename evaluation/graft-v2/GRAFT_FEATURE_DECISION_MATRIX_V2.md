# Graft feature decision matrix — enhanced variant

Each capability is an independent trust decision. F1 does not authorize F2–F6.
Final local validation is **Observed** at `b719459`: exact Python 3.12/3.13
no-Graft release, final late-red-team, README/docs, seeded real lifecycle,
public-output, packaging, and held-out applicability boundaries are recorded.
Two fresh connected installs failed within npm without promoting a runtime;
connected installation/provenance remains **Unverified**; hosted run
`33873556873` passed both supported Python jobs on the identical source tree.

## Decision summary

| Level | Capability | Decision |
|---|---|---|
| F0 | No Graft | **Keep as default and control** |
| F1 | Project-adapted structural CLI | **Keep experimental**, narrowed to `build`, `check`, and `ask` |
| F2 | Structural MCP | **Reject and disable** |
| F3 | Deterministic explainability export | **Reject in this profile** |
| F4 | LSP enrichment | **Reject/disable; capability Unverified** |
| F5 | Deep/model-backed summaries | **Reject by default** |
| F6 | Hooks, status line, prompt injection | **Reject** |

## Capability evidence

The following is the charter-required full decision schema. Costs are reported
as observed proxies, not model-token or billing claims.

| Feature | Intended value | Observed value | Fixed cost | Per-use cost | Accuracy / freshness limits | Privacy / supply-chain impact | Human usability | Agent usability | Failure modes | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| **F0 — no Graft** | Concise context plus source search, contracts, tests, and CleanAI gates | Original no-Graft pytest (125), build, and Twine passed; 3/3 held-out F0 trials were accepted | Existing project context and Python toolchain; no Node/Graft boundary | Median benchmark proxy 960 B; ordinary source reads and executable checks | Lexical queries can be noisy and tests incomplete; scope is explicit; observed mean precision/recall 0.728/0.969 | No added Graft dependency, lifecycle scripts, telemetry, graph, or credentials | Familiar commands; direct evidence remains reviewable | Canonical default and required fallback | Missed synonyms or untested behavior; never a proof of completeness | **Keep/default.** Control and acceptance route |
| **F1 — narrow structural CLI** | First pointers to likely code and source-linked static structure | Research probes: signatures 31/31, literals 10/10, unique blast 3/3; final held-out build failed closed because real Graft omitted tracked `.hidden/visible.py`, before any task agent ran | Exact local npm lock; npm 10.9.0; native scripts; ~375 MiB runtime; final adapter 3,564 lines/131,756 B plus 2,066-line/76,169 B focused test | Benchmark graphs 46,255–1,412,371 B; final seeded graph 2,595,814 B; median benchmark proxy 3,363 B; benchmark cold builds 0.279–0.713 s and warm builds 0.251–0.304 s | Mean precision/recall 0.479/0.748; duplicate, dynamic, config, package, hidden-path misses; stale/incomplete graph fails closed; adapter CRAP **Unverified** | 45 packages beyond root and 12 transitive lifecycle-script packages; minimized environment and isolated state are cooperative controls, not a sandbox | Explicit install/removal and bounded JSON improve reviewability; longer setup and recovery path | May orient when build succeeds, but source/search/tests remain mandatory; accepted-task outcome for final surface **Unverified** | npm/native failure, hidden-source applicability failure, stale/corrupt graph, cleanup races outside portable confinement, detached child, false results | **Keep experimental only.** Public surface is `build`, `check`, bounded `ask` |
| **F2 — structural MCP** | In-client structural retrieval | 48 calls returned the same file sets and accuracy as F1 | Fresh initialize/tool-list payload 4,557 B plus server/tool schemas and upkeep boundary | Median benchmark proxy 6,762 B; server startup/teardown per fresh query | Same observed 0.479/0.748 precision/recall as F1; client amortization behavior **Unverified** | Long-lived process, upstream instructions, lifecycle, root, and tool-schema boundary | More hidden lifecycle and harder teardown than CLI | Convenient transport, but no measured retrieval advantage | Root mismatch, schema drift, lingering process, competing instructions, global/client writes if upstream setup is used | **Reject/disable.** No project MCP command or active example |
| **F3 — deterministic explainability export** | Human-readable static map or impact artifact | Research probes produced 49,342 B blast and 84,532 B map HTML | Export code/path, storage, review and cleanup lifecycle | Regeneration and freshness review per artifact | Inherits static false negatives and symbol ambiguity; can become stale | Creates shareable source-derived artifacts that may expose structure | Visually persuasive but easy to over-trust; newcomer comprehension **Unverified** | Could aid navigation, but no accepted-task benefit was established | Stale artifact, scope ambiguity, disclosure, persuasive false completeness | **Reject in this profile.** Research feasibility only |
| **F4 — optional LSP enrichment** | Improve language-aware relationships | A no-server request exited 0 with no added edges | Additional pinned language server, executable discovery, process and support matrix | Server startup, indexing, memory, refresh and teardown | Real Python LSP precision/recall and failure signaling **Unverified** | Adds executable and dependency supply chain plus a background-process boundary | Silent no-enrichment success is confusing | Potentially richer edges, but no verified cohort | Missing/wrong server, silent fallback, version drift, lingering process | **Reject/disable from profile; capability Unverified** |
| **F5 — authorized deep summaries** | Semantic explanations beyond structural edges | Not run; not authorized | Provider account, model/version policy, credential and cache controls | Source transmission, model tokens/cost, latency and review | Hallucination, truncation and model drift; correctness/recall **Unverified** | Potential source disclosure and provider credential/network boundary | Consent, cost and data policy burden | Could summarize, but cannot become authority | Missing key can silently fall back upstream; leakage, cost, stale cache | **Reject by default** |
| **F6 — hooks, status line, prompt injection** | Automatic freshness and discovery | Source review found `init`, hooks, status, host instructions, global writes, and upkeep mechanisms | Persistent context/config, hook maintenance, host-specific cleanup | Hidden work on commits/shell/client events | Automation can be stale or incomplete while appearing authoritative | Repository and user-home writes; prompt/tool authority and background activity | Low visibility and difficult recovery/removal | Competes with concise project authority and may steer agents implicitly | Prompt injection, unexpected execution, global residue, duplicate/stale authority | **Reject.** No automatic setup or project command |

The upstream `map`, `skeleton`, `callers`, indexed `grep`, and `blast` probes are
retained as evaluation evidence, not v2 commands. Their removal is deliberate:
the adapter should not normalize an unproven broad product surface merely
because the external package implements it.

The same rule applies within a retained command. Real `check` exposed 517
internal pending identifiers (34,206 bytes / 539 lines); v2 keeps the compact
status and records only omission count/hash plus raw-output identity. A byte cap
alone is not a context-precision control.

## Installation strategy

| Strategy | Decision | Evidence and tradeoff |
|---|---|---|
| A. Global exact CLI | **Reject** | Shared mutable state, PATH ambiguity, difficult removal, install telemetry/background behavior |
| B. Project-local exact dependency and reviewed lock | **Use only for F1** | Requires reviewed npm 10.9.0 exactly; most inspectable/removable option, but still executes native scripts and lacks verified build provenance |
| C. Exact npm exec/npx | **Reject** | Cache/network behavior and ordinary use are not bound to a committed consumer lock |
| D. Container/strong OS isolation | **Defer** | Better containment, but disproportionate setup and platform maintenance for this optional experiment |

## Promotion rule and result

The preregistered rule required no correctness, acceptance, review, privacy, or
scope regression before considering at least 15% lower median end-to-end
context, or clearly better recall/precision at equivalent cost.

**Observed:** the broader research C1 did not meet either measured direction.
Mean recall fell from 0.969 to 0.748 and the median net byte proxy grew from 960
to 3,363. C2 retained C1 accuracy and grew to 6,762 B. Six held-out trials were
correct in both cohorts (3/3 each), and every C1 agent used source/search
fallback. Those C1 trials used `grep` and `callers`, which final F1 deliberately
does not expose.

**Observed:** the frozen final-F1 rerun reached current `build`, which returned
exit 2/FAIL because real Graft omitted tracked `.hidden/visible.py`. No graph,
query, agent, or task change followed under the preregistered stop rule.

**Unverified:** accepted-task correctness and scope for the final narrowed F1
surface. The completed applicability probe is not a parity or task result.

**Unverified:** exact model tokens, billed cost, complete review corrections,
human interventions, rework, and file-open counts. Therefore no token,
correctness, or productivity-improvement claim is supported.

**Recommended:** keep F0 default; keep only narrow F1 experimental; reject F2–F6.
