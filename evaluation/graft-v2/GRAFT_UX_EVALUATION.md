# Graft human and agent UX evaluation — enhanced variant

## Verdict

**Observed:** the original integration was not newcomer-ready. It was absent
from canonical README/docs/agent/prompt routes; its fast gate was red; its
tutorial assumed Git state and `origin/main` that a fresh render did not have;
its global install was unavailable; and its privacy wording did not match the
adapter's inherited environment.

**Observed:** v2 adds a concise on-demand route, an explicit Git baseline,
project-local exact installation, a read-only adapter doctor, a bounded command
table, a worked Graft → exact source → exhaustive search → focused test
sequence, freshness and failure recovery, privacy limits, and local removal. It
keeps F0 as default and does not add Graft to ordinary generation, Python
dependencies, hooks, or gates.

**Observed:** exact final `b719459` passed 99 template tests, official render,
243-test release profiles on Python 3.12/3.13, docs/context audits, Markdown
lint, package smoke, and the expanded root/generated Graft README routes. The
template `AGENTS.md` is 58 lines, 535 words, and 4,022 bytes; `CLAUDE.md`
remains a 9-line, 98-word delegation.

**Observed:** clean no-Graft generation and release passed on CPython 3.12 and
3.13; exact seeded removal also passed. **Unverified:** no independent human
participant or comprehension study was performed; connected installation and
the first hosted 3.12/3.13 run passed. Documentation inspection and executable link/
gate checks are not a substitute for observed user behavior.

**Observed:** the root and generated README now put the no-Graft default next
to a short opt-in sequence, define Graft output as derived untrusted navigation
evidence, state disabled capabilities, provide the three-step removal flow, and
name the hidden-directory limit. Cleanup guidance requires stopping direct
Graft and unrelated writers and explains its tracked/unknown/receipt refusal.

**Observed gap (`GRAFT-V2-015`):** at the final-F1 trial checkpoint, generated
public guidance lacked the concrete hidden-directory limitation and safe
recovery. Current guidance explains that hardened `build` will FAIL rather than
publish an incomplete graph, that F0/source remain authoritative, and that users
must not move or untrack source merely to make Graft run. Exact `6966b55`
rendered regressions and the final `b719459` root/docs gates validate that
correction.

## Progressive-disclosure route

The intended path is:

```text
branch README
→ generated GRAFT_EXPERIMENT.md
→ first safe integration run
→ bounded-command reference
→ evaluation tutorial
→ troubleshooting/privacy/upgrade/removal
→ source and empirical evidence
```

**Observed:** the root README identifies the branch as an experiment; the
generated README links the optional entry; `AGENTS.md` contains one concise
router bullet; the docs and prompt indexes link the detailed material. Full
upstream instruction blocks, MCP schemas, hooks, and generated prompt context
are not committed.

## Newcomer journey

| Requirement | Original | Enhanced evidence | V2 status |
|---|---|---|---|
| Explain what Graft is and is not | Derived-evidence wording existed but was orphaned | One-minute boundary: structural index, not behavior/rationale/authority | **Observed documented** |
| Generate and use Python project without Graft | Render/install worked; fast gate failed | F0 remains default; exact `b719459` renders passed 243-test release profiles on Python 3.12/3.13 without Graft | **Observed local and hosted implementation**; run `33873556873` passed both jobs |
| Find the optional experiment | No inbound canonical link | README, docs, agent, and prompt routes added | **Observed** |
| Establish Git prerequisite | Tutorial failed from fresh output | Explicit `git init -b main`, review, first commit, clean-status steps | **Observed documented**; clean newcomer execution pending |
| Use the supported interpreter | Bare `python` could select host 3.11 and fail before JSON | Every public adapter command uses `uv run --locked --group dev python` | **Observed corrected**; independent newcomer journey pending |
| Install reviewed version | Global 0.17.0 command was impossible | Explicit `install --apply` against exact local 0.16.0 lock | Exact attempt reached npm and failed with a generic internal error; a separate same-config diagnostic saw `EAI_AGAIN`; causality and connected capability are **Unverified**; seeded tree is not an install pass |
| Understand the trust decision | Install side effects underexplained | Native lifecycle scripts, network, integrity, unsigned tag/build provenance, and no-sandbox limit stated before command | **Observed documented** |
| Run doctor/install/build/check/ask | Doctor prose/mutation and graph miswiring | Read-only adapter doctor, explicit install, and closed `build`/`check`/`ask` surface | Missing doctor and seeded-tree doctor/build/check/six ask modes **Observed**; connected install **Unverified** |
| Recover when hidden tracked source blocks F1 | Not documented | Version-specific warning: keep F0/source authority; do not move or untrack source to appease Graft | **Observed:** exact `6966b55` rendered regression and final `b719459` root/docs gates passed |
| Understand missing map/skeleton/callers/grep/blast | Original advertised them despite broken/incomplete results | Guide explains why the broader upstream surface is evaluation evidence, not a project command | **Observed rejected by decision rule** |
| Interpret bounded ask | Syntax only; no representative interpretation | Explicit bounds, uncertainty, and worked source/search/test sequence | **Observed documented** |
| Recognize ranked vs exhaustive | Present in deep guide | Repeated near the first-use commands and exhaustive-keyword rule | **Observed** |
| Understand data/privacy boundary | Eight-key denylist overstated safety | Minimal environment, project state, no provider mode, direct-bypass and no-OS-sandbox warnings | **Observed documented and focused-tested** |
| Recover from missing/stale/corrupt state | Little guidance | Missing runtime, Git/untracked source, stale/corrupt graph, timeout, failed transaction, and removal recovery added | **Observed documented** |
| Remove the integration | Global npm removal plus local deletion | Read-only adapter `remove --check`, explicit `remove --apply`, exact receipt/tracked/unknown refusal, repeated per-target preflight, then `complete: true` | **Observed** on 7,522-path seeded real runtime and focused faults; connected-install/detached/same-user post-preflight race **Unverified** |
| Explain graph is not proof | Repeated warning | Authority hierarchy plus executable worked example | **Observed** |

## Experienced-engineer journey

| Requirement | V2 answer | Status |
|---|---|---|
| Alter indexed scope safely | V2 fixes scope to tracked supported source instead of reopening generic path flags | **Recommended limitation**, not a flexible cohort |
| Reason about cold/warm cost | Evaluation guide requires install/build/refresh, disk, compute, context, correction, and review accounting | **Observed documented**; peak descendant memory **Unverified** |
| Choose CLI versus MCP | Only bounded CLI is a valid project cohort; MCP is explicitly disabled | **Observed** |
| Create reproducible comparison | External oracle, frozen commit, fixed controls, repetitions, counterbalancing, and decision rule required | **Observed documented and used by deterministic benchmark** |
| Preserve evidence without graph authority | Adapter writes ignored JSON; graph/artifacts remain ignored and regenerable | **Observed implementation** |
| Upgrade deliberately | New tarball/lock/integrity/source review plus unchanged task-bank rerun required | **Observed documented** |
| Interpret false positives/negatives | Quantitative original results and routing limits are explicit | **Observed documented** |
| Decide promotion | Correctness/acceptance/review/privacy/scope gates precede context savings | **Observed documented** |

Fixing scope to the project root is intentional: a flexible `--only-dir` or
extension cohort was not shown to improve total accepted-task cost, and generic
scope flags were a source of boundary bypass. An experienced user who needs a
new scope must make a reviewed adapter change and add tests.

## Fresh coding-agent journey

| Capability | Evidence | Status |
|---|---|---|
| Discover without long persistent block | One `AGENTS.md` bullet routes on demand; no MCP schema/instruction context | **Observed** |
| Select operation by task | Bounded operation table and exhaustive-keyword routing rule | **Observed documented** |
| Cite exact source | Tutorial follows returned paths/spans with a literal source read | **Observed documented** |
| Fall back for completeness | `rg`/`git grep` and test/package verification required | **Observed documented** |
| Keep authority straight | Human intent/contracts → deterministic evidence → source/behavior → Graft → history | **Observed documented** |
| Run applicable gates | Worked example ends in a focused test; ordinary gauntlets remain separate | **Observed documented** |
| Report uncertainty | Guide requires stale/missing/corrupt evidence as UNVERIFIED and lists dynamic-Python limits | **Observed documented** |
| Improve actual agent outcome | Held-out task passed 3/3 in C0 and 3/3 in a broader research C1 wrapper; final F1 then failed its first build because real Graft omitted tracked `.hidden/visible.py`, before any task agent ran | **No observed correctness advantage**; final F1 has an observed applicability gap, while accepted-task outcome and exact cost/rework are **Unverified** |

## Context cost and duplication

The original persistent Graft delta was zero bytes because the feature was
orphaned. The effective original root routes were approximately 973 proxy tokens
for Codex and 1,134 for Claude, using `ceil(characters/4)` rather than a client
tokenizer.

**Observed:** v2 adds only one Graft router bullet to `AGENTS.md`; product detail
stays in on-demand documents. Relative to the original inventory it adds two
lines, 21 words, 132 characters, or 33 `ceil(characters/4)` proxy tokens.
Because actual client loading and tokenization were not observed, that proxy is
not billing truth.

**Observed:** the formal `prompts/evaluate-graft.md` role is not a standalone
873-proxy-token prompt. It requires `prompts/PROMPT_CONTRACT.md`; together they
are 147 lines, 1,339 words, 9,995 characters, and 2,499 character/4 proxy
tokens. Installation also requires review of the 263-proxy-token runtime-lock
README. These remain on demand, but they are part of the real evaluation/install
context cost.

**Observed:** the original MCP config proxy was only 61 estimated tokens, but
that excluded tool schemas and upstream initialize instructions. The measured
fresh MCP fixed response was 4,557 bytes. V2 avoids that routine context by
removing the MCP cohort.

**Observed:** upstream `check` produced 34,206 bytes / 539 lines on the generated
project, mostly 517 internal pending identifiers. V2 projects those identifiers
out of the public response while retaining their count/hash and the raw-output
identity in evidence. This is an output-usability control, not a claim that the
underlying graph is complete.

**Observed:** a later long-checkout run still produced 4,243 bytes because the
public envelope carried absolute host paths. Final `b719459` uses project-
relative managed paths and omits host executable paths across successful public
stdout; it also replaces public language labels with count/hash evidence and
bounds escaped hostile diagnostics. Full identities and exact untrusted labels
remain in local install/structural durable evidence. Stable public output and
shareable durable evidence remain separate concerns.

## Language and comprehension checks

The enhanced material now defines or demonstrates:

- structural index, ranked retrieval, graph freshness, and why the broader
  skeleton/callers/indexed-grep/blast surface was not promoted;
- the difference between a graph lead and source/runtime evidence;
- why project-local installation still executes third-party native scripts;
- why `DO_NOT_TRACK` and a minimal environment reduce risk but are not a
  network sandbox;
- why no output, a fresh graph, or an attractive visualization does not prove
  absence/correctness;
- why held-out acceptance criteria must stay outside an agent-readable worktree.

The final human study should ask unambiguous questions such as:

1. Which evidence outranks Graft output?
2. When must `rg`/`git grep` replace or supplement ranked retrieval?
3. What network/code-execution decision does `install --apply` authorize?
4. Where is Graft state stored, and how is it removed?
5. What does a successful or empty `ask` fail to prove?
6. What should a missing, stale, or corrupt graph be reported as?

**Unverified:** whether independent newcomers answer those correctly and can
complete the journey without assistance.

## Failure and recovery quality

| Failure | Required response |
|---|---|
| No Node/local runtime | Doctor JSON is not ready; inspect/install explicitly; ordinary Python remains usable |
| No Git repository or untracked source | Establish/review the intended Git baseline; do not stage unrelated work merely to appease the adapter |
| Missing or stale graph | Report Graft evidence UNVERIFIED; rebuild after reviewing source state |
| Corrupt/incomplete graph | Remove only validated local state, rebuild, and use source/search/tests meanwhile |
| Adapter timeout/output bound | Preserve structured failure; narrow the question or use direct source/search, not a broad bypass |
| Removal | Run `remove --check`, review targets, `remove --apply`, then check again |
| Direct Graft/npx use | Treat as an unevaluated bypass; project privacy/scope/evidence controls do not apply |

## UX decision

**Recommended:** the v2 documentation is sufficient for a reviewed experimental
branch at the observed local boundary. It is not sufficient evidence to claim
that Graft improves newcomer understanding or agent productivity. Retain the
concise route and worked verification pattern, keep F1 opt-in, and do not restore
MCP, automatic setup, or broad upstream instructions. Hosted PR checks and an
independent newcomer study remain **Unverified**.

## Evidence

- Original audit: `team/context_ux/CONTEXT_UX_AUDIT_ORIGINAL.md`
- Original machine inventory: `team/context_ux/GRAFT_CONTEXT_INVENTORY_ORIGINAL.json`
- Enhanced documentation validation: `team/context_ux/CONTEXT_UX_V2_VALIDATION.md`
- Context benchmark: `team/context_benchmark/CONTEXT_BENCHMARK_REPORT.md`
