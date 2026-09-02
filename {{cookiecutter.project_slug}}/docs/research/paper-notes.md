---
status: reference
authority: agentic-coding-paper-evidence
owner: maintainers
evidence_version: "2.0"
last_verified: 2026-09-01
retrieved: 2026-09-01
applies_to:
  - "AGENTS.md"
  - "CLAUDE.md"
  - ".cleanai/**"
  - "tools/cleanai.py"
---
# Empirical paper evidence

This is **reference evidence, not normative repository authority**. Each card distinguishes what a versioned study reports from the local practice it influenced. A reported association or benchmark result is not a universal recommendation, a causal result, or an endorsement of this scaffold.

## Source registry

| ID | Exact work and frozen version | Status at retrieval |
|---|---|---|
| PAPER-CTX | Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, and Martin Vechev, “Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?”, [arXiv:2602.11988v2](https://arxiv.org/html/2602.11988v2), revised 2026-06-23 | arXiv record states no publication venue |
| PAPER-README | Worawalan Chatlatanagulchai et al., “Agent READMEs: An Empirical Study of Context Files for Agentic Coding”, [arXiv:2511.12884v2](https://arxiv.org/html/2511.12884v2), revised 2026-08-09 | arXiv record states no publication venue |
| PAPER-REPO | Yanlin Wang et al., “RepoReasoner: Evaluating Repository-Level Code Reasoning Ability of Long-Context Language Models”, [arXiv:2607.25996v1](https://arxiv.org/html/2607.25996v1), submitted 2026-07-28 | published in FSE 2026; DOI `10.1145/3808131` |
| PAPER-DEBT | Yue Liu, Ratnadira Widyasari, Yanjie Zhao, Ivana Clairine Irsan, Junkai Chen, and David Lo, “Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild”, [arXiv:2603.28592v2](https://arxiv.org/html/2603.28592v2), revised 2026-04-26 | arXiv record states no publication venue |
| PAPER-REFACTOR | Kosei Horikawa, Hao Li, Yutaro Kashiwa, Bram Adams, Hajimu Iida, and Ahmed E. Hassan, “Agentic Refactoring: An Empirical Study of AI Coding Agents”, [arXiv:2511.04824v1](https://arxiv.org/html/2511.04824v1), submitted 2025-11-06 | arXiv record says “submitted to ACM TOSEM”; it does not report acceptance/publication |

“No publication venue stated” describes the cited arXiv record as retrieved; it does not prove that no related publication exists elsewhere.

## PAPER-CTX — repository instruction files

**Sample and method (Source-supported):** Version 2 evaluates 138 Python change tasks from 12 repositories in CTXbench and 300 Python SWE-bench tasks from 11 repositories. It compares no context, agent-generated context, and—on CTXbench—developer-committed context across four agent/model configurations, with one completion per task and condition. Success means the evaluation tests pass; it also measures steps and inference cost.

**Findings (Source-supported):** Developer context changed average success by about +2.4 percentage points (`p=.21`) against no context. Generated context changed it by about -0.5 points on SWE-bench (`p=.87`) and -2 points on CTXbench (`p=.37`). These differences were not statistically significant. Generated files increased mean inference cost by about 20% and 23% in the two benchmarks; developer-file cost rose by at most 19%. Reasoning-token and tool-step effects vary by condition, so “all context costs more than 20%” is not supported.

**Limits:** Python-only selected tasks, repositories, model/client versions, one completion per condition, test-pass success, generated/reviewed task material, and stochastic agents bound the result. It does not show that every concise instruction helps or that every repository should omit persistent context.

**Local practice (Inferred / Recommended):** Treat persistent instructions as hypotheses. Keep them scoped and nonredundant, then compare stable tasks before and after changes. This benchmark design is local synthesis, not a study prescription.

## PAPER-README — context-file contents and evolution

**Sample and method (Source-supported):** Version 2 collects 2,303 conventional root files—922 `CLAUDE.md`, 694 `AGENTS.md`, and 687 Copilot instruction files—from 1,925 open-source repositories selected through the AIDev corpus. Size, structure, and Flesch Reading Ease cover the full corpus. Topic frequencies come from a proportional random subset of 332 files, not all 2,303. Commit-history analyses use separate tool-specific context-file histories.

**Findings (Source-supported):** Files are often long and shallowly structured and tend to grow through small additions. In the 332-file coded subset, testing, implementation, and architecture topics are common, while security and performance appear much less often. “Difficult to read” is based on Flesch Reading Ease, a surface lexical/syntactic proxy; the paper reports only weak agreement with its manual readability check.

**Limits:** Open-source, AIDev, root-file, and three-tool selection limits generalization. Binary topic coding and Flesch scores do not measure whether an agent follows instructions or whether a person understands them. Repository mining is descriptive, not causal.

**Local practice (Inferred / Recommended):** Give persistent context an owner, scope, and review path; keep consequential nonfunctional constraints discoverable. The exact lifecycle schema and deletion policy remain local choices.

## PAPER-REPO — cross-file reasoning

**Sample and method (Source-supported):** RepoReasoner contains 858 Output Prediction and 169 Call Chain Prediction samples from 14 Python repositories and evaluates seven models. It compares traced-file “oracle” context with BM25 retrieval and, for selected conditions, 10k- and 30k-token contexts. Matching is evaluated statically against derived outputs/call chains.

**Findings (Source-supported):** The best reported oracle Output Prediction result is 69.1% Pass@1. Larger evaluated models often exceed 80% call-chain precision while recall remains below 40%; exact-chain match is much lower. More BM25-retrieved context has mixed effects and can reduce results for some models. “Oracle” means selected traced files within the experiment, not complete knowledge of a repository.

**Limits:** Fourteen Python repositories, tracing/AST derivation, BM25-only retrieval, possible task rewriting/leakage, and static matching bound the result. Prediction benchmarks do not measure safe autonomous edits, architecture quality, or this scaffold.

**Local practice (Inferred / Recommended):** Make dependency direction and ownership discoverable and test locate/explain tasks. Do not equate a larger context window with repository understanding.

## PAPER-DEBT — static-analysis findings in AI-attributed commits

**Sample and method (Source-supported):** Version 2 mines 302,579 commits attributed to five AI tools through explicit Git metadata across 6,299 public repositories with at least 100 stars. Analysis covers selected Python, JavaScript, and TypeScript production files and uses static analyzers to match introduced, fixed, and later-present findings. “AI-attributed” is more accurate than “verified AI-authored”: commits can include human changes.

**Findings that can be stated without resolving a contradiction:** The analyzers report 484,366 introduced findings, 89.3% categorized as code smells. At aggregate level, AI-attributed commits fixed more smells than they introduced but introduced more correctness/security findings than they fixed. Separately, 22.7% of all tracked finding types still matched at repository head. That persistence value is not specific to correctness/security findings and need not describe the same commits.

**Unresolved source contradiction (Unverified):** Table II reports 27,677 issue-introducing commits out of 302,579, or about 9.1%. The abstract and Section V-B say more than 15% of commits for every tool introduced an issue, while Table I’s five tool counts sum to the same 302,579 total. The cited version does not expose a denominator change that reconciles these statements. This scaffold therefore makes no single prevalence claim from them.

**Limits:** Static-analysis findings are proxies with false positives/blind spots; explicit metadata does not prove exclusively AI authorship; there is no matched human baseline; deleted/rewritten files affect lifecycle matching; public/language/popularity filters and omitted debt types constrain generalization. The study does not establish that AI caused a particular defect.

**Local practice (Inferred / Recommended):** Use before/after analysis and post-merge monitoring as fallible sensors, alongside behavioral and human review. The Cleaner/Architect/Hardener role split is this scaffold’s design, not a paper result.

## PAPER-REFACTOR — refactoring by coding agents

**Sample and method (Source-supported):** Version 1 studies 14,998 non-merge, Java-changing commits across 12,256 pull requests and 1,613 repositories. RefactoringMiner identifies structural changes. The study calls 3,907 commits (26.1%) “intentional” when a detected refactoring coincides with self-affirming commit-message patterns; that is an operational classifier, not access to an agent’s intent. About 89.3% of sampled commits are attributed to Codex.

**Findings (Source-supported):** Low-level consistency changes are common. Some structural metrics improve slightly in selected groups, while typical smell-count change is zero and reported significant differences have negligible practical effects. The study does not show that behavior was preserved.

**Limits:** Java/open-source sampling, extreme tool imbalance, commit attribution, analyzer/classifier errors, human edits, cross-study comparison, static structural proxies, and no behavioral execution limit generalization. The manuscript was submitted to TOSEM; the cited record does not say it was accepted.

**Local practice (Inferred / Recommended):** A refactoring should name the behavior oracle and targeted system property and avoid change for metric movement alone. Separate Cleaner/Architect roles are a local workflow choice.

## Synthesis boundary

The thresholds, front-matter schema, task bank, friction formulas, exact mutants, role topology, one-writer default, and dependency stack are local hypotheses. A study can motivate an experiment; it does not make these choices normative or validated.
