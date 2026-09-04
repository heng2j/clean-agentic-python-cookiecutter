# Adopt Clean Agentic Python in an existing project

> **Adopt the operating model one verified capability at a time. Do not pour a
> Cookiecutter over a living codebase.**

This tutorial is for maintainers of an existing Python repository—possibly a
large, old, fast-growing, partially documented, or agent-heavy one—who want to
adopt the useful parts of `experimental-graft-variant` without losing current
behavior, history, tooling, or human understanding.

The objective is not to make the repository *look* like the generated example.
The objective is to make it easier for people and coding agents to answer:

- What are we trying to change?
- Which source is current authority?
- What must not change?
- What is the smallest safe change surface?
- Which deterministic evidence decides whether the change works?
- What uncertainty remains?
- Did the new workflow reduce accepted-change cost, or merely produce more code?

The recommended sequence is:

```text
Preserve and measure the existing repository
        ↓
Generate a separate reference project
        ↓
Audit without editing
        ↓
Establish concise authority and context routing
        ↓
Make existing commands deterministic and truthful
        ↓
Adopt quality sensors and ratchets in small batches
        ↓
Clean selected problems with bounded role prompts
        ↓
Evaluate optional Graft retrieval against the no-Graft workflow
        ↓
Keep only capabilities that improve correct, reviewable work
```

## The most important rule

**Never generate this Cookiecutter directly into an existing repository.**

A mature repository already has decisions embedded in its package metadata,
lockfiles, CI, directory layout, release process, test conventions, documentation,
and developer habits. Replacing those files with a template can destroy useful
information while creating a deceptively tidy but incorrect project.

Instead:

1. generate the template into a separate sibling directory;
2. treat that render as a **reference implementation and donor**, not authority;
3. audit the existing project before changing it;
4. select one capability to adopt;
5. adapt it to the repository's real architecture and toolchain;
6. verify behavior and rollback; and
7. stop before beginning the next capability.

The normal no-Graft workflow—current source, exhaustive search, human-owned
contracts and decisions, tests, and deterministic gates—remains the default.
Graft is a later, optional experiment. The current branch exposes only a narrow
project-adapted structural `build`, `check`, and bounded `ask`; it does not
promote MCP, hooks, automatic prompt injection, deep summaries, visualization,
LSP enrichment, or broad upstream commands. See the
[variant decision record](GRAFT_VARIANT.md) and the
[latest Graft audit](evaluation/graft-v2/AUDIT_GRAFT_VARIANT_V2.md).

---

# 1. Choose the right adoption lane

Use the smallest lane that matches the repository.

| Existing repository | Recommended starting lane |
|---|---|
| Healthy Python 3.12/3.13 project already using uv | Adopt the prompt/context layer, then adapt the CleanAI harness and policies in separate changes |
| Python project using Poetry, PDM, Hatch, pip-tools, Conda, Pixi, Bazel, Pants, or another workflow | Keep the existing environment and package authority; adopt prompts and context first, then wrap the existing commands instead of replacing the toolchain |
| Python version older than the template's supported range | Use the generated project as documentation and design reference; do not copy the harness until its runtime compatibility has been tested or isolated |
| Polyglot monorepo | Pilot one Python subsystem with explicit scope; do not claim repository-wide coverage from a Python-only gate or Graft graph |
| Repository with a red, flaky, or unknown baseline | Freeze and audit first; separate pre-existing failures from migration failures before any cleanup |
| Repository containing sensitive source or credentials | Start with no Graft and secret-free local checks; require an explicit supply-chain, process, filesystem, and network isolation decision before third-party indexing tools |
| Repository with many active agents and unreviewed changes | Reduce work in progress first; one writer and one pending review artifact is a safer starting point than more automation |

The template's currently documented support boundary is Linux x86_64 with
CPython 3.12 and 3.13. Treat other platforms and runtimes as **Unverified** until
your own project executes the relevant checks.

---

# 2. Define success before migration

Write a one-page adoption charter outside the agent's default readable context.
Do this before copying files or asking an agent to “clean the repository.”

```text
ADOPTION OUTCOME
What should become easier, safer, or cheaper?

CURRENT PAIN
Which observed failures motivate the change?

NON-GOALS
Which architecture, runtime, behavior, release process, and toolchain will not
change in this adoption pass?

PROTECTED SURFACES
Which public APIs, schemas, fixtures, data, generated assets, and legal files
must remain unchanged?

FIRST CAPABILITY
Which single capability will be adopted first?

ACCEPTANCE EVIDENCE
Which commands, held-out tests, reviews, and measurements decide success?

ROLLBACK
Which commit, branch, worktree, or reverse patch restores the prior state?

HUMAN OWNER
Who decides architecture, risk, exceptions, and acceptance?
```

Good first outcomes are narrow:

- “A fresh agent can find the current build and test commands without reading
  historical documents.”
- “Every pull request runs one truthful fast gate that cannot silently skip a
  required check.”
- “Root agent instructions fit a declared context budget and contain no stale
  test counts or duplicate authority.”
- “One high-risk module has a behavior oracle and curated semantic mutants.”
- “We can compare the same task with and without bounded Graft retrieval.”

Poor first outcomes are unbounded:

- “Clean the whole repository.”
- “Modernize everything.”
- “Make the architecture good.”
- “Let the agent decide what is obsolete.”
- “Install all recommended tools.”
- “Use Graft so the agent understands the codebase.”

---

# 3. Preserve the current repository

## 3.1 Record identity and dirty state

From the existing repository root:

```bash
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
```

Record the outputs. Do not ask an agent or script to reset, stash, commit,
rebase, or discard existing work.

If the worktree is dirty, the human owner should decide whether to:

- complete and commit the current work;
- preserve it on a separate human-named branch;
- export a reviewed patch;
- or create the migration worktree from the last known-good commit while leaving
  the dirty checkout untouched.

## 3.2 Prefer an isolated adoption worktree

From a clean, reviewed commit:

```bash
git worktree add -b chore/clean-agentic-adoption \
  ../my-project-clean-agentic HEAD
cd ../my-project-clean-agentic

git status --short
git rev-parse HEAD
```

Expected result: the new worktree begins at the recorded commit and has no
unexpected changes.

Do not use this command blindly when the branch name or target directory already
exists. Inspect both first.

## 3.3 Capture the real baseline

Run the project's existing documented commands exactly as written before adding
new tools. Record:

- installation or bootstrap command;
- focused test command;
- full test command;
- formatting and lint command;
- type check;
- build/package command;
- release or deployment smoke;
- operating system, architecture, runtime, package-manager, and compiler versions;
- exit codes and skipped checks;
- duration and major resource constraints; and
- known flaky or environment-dependent failures.

A failure is not automatically a migration blocker. It is a blocker when you
cannot distinguish a pre-existing failure from a change introduced by the
migration.

Keep volatile logs outside normal agent context. Until the repository has an
ignored evidence directory, use a sibling directory such as:

```text
../my-project-clean-agentic-evidence/
```

---

# 4. Generate a separate reference project

Generate the experimental variant in a directory that is **not inside the
existing repository**:

```bash
cd /path/to/a/safe-parent-directory

uvx --from 'cookiecutter==2.7.1' cookiecutter \
  https://github.com/heng2j/clean-agentic-python-cookiecutter \
  --checkout experimental-graft-variant
```

Choose a clearly disposable reference name, for example:

```text
my-project-clean-agentic-reference
```

Validate the reference render on its own terms:

```bash
cd my-project-clean-agentic-reference
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

This establishes only that the reference project works in the tested
environment. It does **not** establish compatibility with the existing project.

Keep the following directories conceptually separate:

```text
my-project/                         existing project and authority
my-project-clean-agentic/           isolated migration worktree
my-project-clean-agentic-reference/ generated donor/reference
my-project-clean-agentic-evidence/  volatile audit and comparison evidence
```

## Files that must never be copied wholesale

Do not overwrite these existing-project files from the reference render:

- `pyproject.toml`;
- `uv.lock` or another lockfile;
- `.gitignore`;
- CI workflows;
- release configuration;
- `AGENTS.md`;
- `CLAUDE.md`;
- `.envrc`;
- `Makefile`;
- license, notice, ownership, or security-policy files;
- package source and tests; or
- current architecture and domain documentation.

Diff them to learn from the reference. Merge only owner-approved pieces.

---

# 5. Audit before implementation

Use the portable prompt pack from the reference project. A role prompt is a
small delta and must be paired with the
[shared prompt contract](%7B%7Bcookiecutter.project_slug%7D%7D/prompts/PROMPT_CONTRACT.md).
Start with the
[existing-repository audit](%7B%7Bcookiecutter.project_slug%7D%7D/prompts/audit-existing-repo.md).

Attach or provide those two files to a fresh audit session and use a starter such
as:

```markdown
# Existing repository — Clean Agentic adoption audit

Use the attached `PROMPT_CONTRACT.md` and `audit-existing-repo.md` as the
operating and role contract.

Repository: `<absolute-or-connected-repository>`
Revision: `<commit>`
Dirty-state policy: `<clean worktree / preserved dirty checkout>`
Mode: audit only; do not modify repository files
Evidence output: `<authorized external or ignored path>`

Audit whether this repository supports narrow, correct, reproducible
agent-assisted changes. Concentrate on:

- current authority and contradictions;
- setup, tests, package, and release truthfulness;
- persistent agent context and stale history;
- architecture and change locality;
- deterministic feedback latency and skipped checks;
- generated, vendored, historical, and owned material;
- test sensitivity and high-consequence untested behavior;
- dependencies, secrets, network, and supply-chain boundaries;
- and the smallest safe adoption sequence.

Return an immutable baseline, claim–evidence matrix, P0–P3 findings, gate
sensitivity results from disposable copies only, a do-not-change-yet list, and
phased remediation options. Do not repair anything in this pass.
```

The audit should answer at least:

1. What are the existing canonical commands, and do they work?
2. Which files currently claim authority over the same decision?
3. Which context files are loaded by each agent client?
4. Which documentation is current, generated, historical, or ownerless?
5. Which small changes cause unexpectedly large diffs?
6. Which gates can pass while a seeded defect survives?
7. Which checks are too slow for the inner loop?
8. Which failures are silently skipped or converted into warnings?
9. Which package/install behavior differs from the source checkout?
10. Which cleanup would be dangerous before better behavior evidence exists?

Do not begin remediation until a human owner selects finding IDs and approves a
bounded write surface.

---

# 6. Establish the context control plane first

The highest-leverage first implementation is often not a refactor. It is making
current authority and canonical commands easy to locate.

## 6.1 Create or reconcile one compact root `AGENTS.md`

Use the generated `AGENTS.md` as a structural example, not text to paste blindly.
The existing repository's root file should contain only information needed by
most tasks:

```markdown
# Agent operating map

## Repository map
- Product code: `<paths>`
- Tests and behavior evidence: `<paths>`
- Current contracts and decisions: `<paths>`
- Generated, vendored, archived, and ignored material: `<paths>`

## Canonical commands
- Bootstrap: `<command>`
- Focused test: `<command>`
- Fast gate: `<command>`
- Full or release gate: `<command>`

## Non-negotiable invariants
- `<behavior, trust, data, compatibility, or architecture invariants>`

## Stop and escalate
- `<authority conflict, unsafe command, user-work risk, scope expansion,
  missing oracle, dependency/public-contract change>`

## Definition of done
- `<required evidence, restoration, residual risk, and human acceptance>`
```

Do not put these in the root file:

- a complete directory tree;
- issue or chat history;
- old audit narratives;
- generated API documentation;
- tutorials for one optional tool;
- fixed test counts;
- volatile versions that can be queried;
- duplicated formatter, linter, or type rules already enforced by tools;
- or “read every file/document before working.”

A practical initial budget is the reference policy's 120 lines and 700 words,
but that budget is a local design choice, not a universal law. Measure whether
it improves the actual clients and tasks you use.

## 6.2 Make `CLAUDE.md` a client-specific delta

Where the client supports imports, prefer:

```markdown
@AGENTS.md

# Claude Code loading delta

- `<only Claude-specific loading, tool, or memory differences>`
```

Do not maintain a second copy of repository commands and invariants. Confirm
current client loading and precedence behavior from first-party documentation or
runtime inspection; filenames alone do not prove what a client loads.

## 6.3 Use scoped instructions sparingly

Add nested `AGENTS.md` or path-scoped rules only when a subdirectory has a real,
recurring difference, such as:

- domain-specific invariants;
- generated-code restrictions;
- data/privacy handling;
- expensive scientific verification;
- or a distinct package build command.

Closer context should narrow or specialize the root contract, not contradict it.

## 6.4 Separate current authority from history

A useful initial documentation map is:

```text
docs/
  contracts/       current observable behavior and invariants
  adr/             accepted architectural decisions and alternatives
  runbooks/        current operational procedures
  tasks/active/    one bounded active task packet per authorized change
  plans/completed/ completed implementation plans
  archive/         historical or superseded material
```

Do not reorganize all documentation in the first pull request. Classify and move
only material needed to resolve a current authority conflict, with owner review
and recoverable Git history.

Distill issue or chat history into a current task packet rather than placing the
whole discussion in every agent context. The reference project includes
`docs/templates/task-packet.md` and `docs/templates/issue-distillation.md`.

---

# 7. Make the existing command surface truthful

Before adding new quality tools, define one canonical fast feedback path around
the commands the project already trusts.

## 7.1 Write a command contract

| Purpose | Canonical command | Expected writes | Network/credentials | Success meaning |
|---|---|---|---|---|
| Bootstrap | project-specific | environment/lock/cache | declare explicitly | environment was prepared as documented |
| Focused behavior | project-specific | test cache or temp | normally none | named behavior oracle passed |
| Fast gate | project-specific | bounded evidence/cache | normally none | every listed inner-loop check ran and passed |
| Full gate | project-specific | coverage/build output | normally none after setup | broader repository checks ran and passed |
| Connected audit | project-specific | audit report | yes | named live query ran at recorded time |
| Release | project-specific | immutable candidate | declare explicitly | candidate, not just source checkout, passed named checks |

Keep connected vulnerability, deployment, or provider checks separate from a
claim of deterministic offline quality.

## 7.2 Build the fast gate from the inside out

A useful first fast gate often contains:

```text
format check
lint
canonical type check
focused or appropriately scoped tests
architecture smoke where already defined
context/document checks after those controls are adopted
```

Do not add every template tool at once. A gate that takes too long will be
avoided; a fast gate that silently skips work creates false trust.

For a legacy repository with existing debt, use a visible ratchet:

- preserve a dated, reviewable baseline;
- reject new violations in changed or owned code;
- reduce the baseline package by package;
- keep correctness and security rules active;
- and record every temporary exception with an owner and removal condition.

Do not obtain green output by blanket exclusions, disabling rules, lowering
thresholds, or classifying all legacy files as generated.

## 7.3 Prove that each gate can fail

In a disposable worktree, seed one controlled defect at a time:

- formatting or lint violation;
- type error;
- behavior regression;
- reverse dependency;
- stale or contradictory context;
- broken documentation link;
- reduced coverage;
- surviving semantic mutant;
- missing required tool or report;
- or package content missing from the installed artifact.

For each seed, verify:

1. the intended command returns nonzero;
2. the diagnostic identifies the real failure;
3. the check does not silently skip;
4. the seed is restored; and
5. the original baseline returns.

A green gate on healthy code is weaker evidence than a gate that detects its
intended defect.

---

# 8. Port Clean Agentic features in bounded bundles

Adopt one bundle per reviewed change. Each later bundle depends on the earlier
ones being understood, not merely present.

## Bundle A — Prompt and task discipline

Candidate donor material:

```text
prompts/PROMPT_CONTRACT.md
prompts/GLOSSARY.md
prompts/audit-existing-repo.md
prompts/clean-existing-repo.md
prompts/context-hygiene.md
prompts/harden-existing-repo.md
prompts/qa-existing-repo.md
prompts/specifier.md
prompts/coder.md
prompts/cleaner.md
prompts/architect.md
prompts/hardener.md
prompts/qa.md
prompts/orchestrator.md
docs/templates/task-packet.md
docs/templates/issue-distillation.md
docs/templates/learning-ledger.md
```

Recommended adaptation:

- preserve the shared contract plus one role delta;
- replace reference-project paths with real paths;
- define the repository's risk owner and acceptance commands;
- keep audit and implementation phases separate;
- and use one writing agent at a time.

This bundle can often be adopted without changing the Python runtime.

## Bundle B — Context and documentation hygiene

Candidate donor material:

```text
AGENTS.md                 structure only; manually reconcile
a concise CLAUDE.md       client-specific delta only
.cleanai/policy.toml      context section, adapted
tools/cleanai_core/docs.py
tests for context and documentation checks
docs/quality/context-hygiene.md
```

Recommended adaptation:

- inventory every real loading source first;
- set budgets from observed needs;
- define lifecycle states and owners;
- classify generated and historical material;
- and test the checker on seeded contradictions and stale references.

Do not force lifecycle front matter onto the entire historical archive in one
mechanical change. Start with current normative documents.

## Bundle C — Repository-local quality harness

Candidate donor material:

```text
tools/cleanai.py
tools/cleanai_core/
.cleanai/policy.toml
tests/tooling/
docs/quality/
docs/reference/commands.md
docs/reference/evidence.md
```

Recommended adaptation:

- change `project.package`, `source_root`, and `docs_root`;
- replace every gauntlet command with an existing or deliberately adopted
  command;
- model the actual package layout;
- review every dependency before adding it;
- ensure the harness measures itself;
- preserve JSON evidence schemas and nonzero missing-tool behavior;
- and test package artifacts outside the source checkout.

Do not overwrite the existing `pyproject.toml` or lockfile. Merge selected
configuration and dependencies through the project's normal dependency-review
process.

## Bundle D — Quality sensors

Candidate capabilities:

- branch-aware coverage;
- separate product and harness coverage;
- local CRAP approximation;
- architecture fitness rules;
- curated implementation mutations;
- executable-specification mutations;
- package/wheel smoke;
- security source scan;
- connected dependency audit; and
- release evidence.

Adopt them as sensors, not proof.

The reference architecture `adapters → application → domain` is an example. Do
not impose it on a repository whose real boundaries differ. First document the
existing dependency model, then encode one consequential rule and test a seeded
violation.

Do not interpret low CRAP, high coverage, or a mutation percentage as proof of
correctness, cohesion, security, or good requirements. Start mutation with a few
realistic high-consequence defects and execute them in disposable copies.

## Bundle E — Scientific workspace, only when applicable

The template's `notebooks/`, `static/`, `results/`, and `scripts/` contracts are
useful for scientific projects. They are not mandatory for ordinary services,
libraries, or applications.

Adopt these paths only when they solve an observed provenance or reproducibility
problem. Do not move reusable code merely to match the example layout.

## Bundle F — Optional Graft experiment

Adopt only after Bundles A–C or equivalent controls make authority, source
scope, and verification clear. The Graft section later in this tutorial lists
the exact bounded files and workflow.

---

# 9. Clean persistent context before cleaning code

A messy context layer can cause an agent to reproduce obsolete patterns even
when the implementation itself is serviceable.

Use the shared prompt contract with the
[context-hygiene prompt](%7B%7Bcookiecutter.project_slug%7D%7D/prompts/context-hygiene.md)
in **audit-only mode** first.

Inventory at least:

```text
AGENTS.md and nested AGENTS.md
CLAUDE.md and imported memory
.claude/rules/**
Copilot, Cursor, Gemini, or other repository instructions
MCP tool schemas and descriptions
hooks and status-line output
active plans
generated documentation
issue/chat summaries
historical audits
user- and managed-level context visible to the client
```

Classify each source as:

- **keep persistent** — needed for most tasks;
- **scope** — load only within a package or path;
- **retrieve** — find on demand;
- **generate** — derive from code or tools when needed;
- **reconcile** — conflicts with another authority;
- **archive** — useful history, not current guidance; or
- **delete** — no remaining value and owner-approved recovery exists.

A context cleanup should usually remove duplication before adding new guidance.
Do not create a new “master instructions” file that repeats every existing one.

After the CleanAI document controls are adopted, use the non-destructive prune
planner:

```bash
python tools/cleanai.py prune-plan \
  --output artifacts/context/prune-plan.md
```

Adapt the Python launcher to the repository's environment. Review the proposal;
it is not authorization to delete files.

---

# 10. Turn findings into small cleanup batches

Use the
[existing-repository cleanup prompt](%7B%7Bcookiecutter.project_slug%7D%7D/prompts/clean-existing-repo.md)
only after a human selects finding IDs from the frozen audit.

Prioritize cleanup in this order unless project risk says otherwise:

1. false-green gates, destructive behavior, secrets, and supply-chain hazards;
2. contradictory authority and broken canonical commands;
3. flaky or excessively slow inner-loop feedback;
4. missing behavior contracts around high-consequence code;
5. architectural cycles and large change blast radii;
6. duplicate implementations and competing patterns;
7. local complexity, names, and organization; and
8. cosmetic consistency.

## One cleanup batch should have one sentence of purpose

Example:

```text
Replace the two competing release-policy implementations with one existing
canonical implementation while preserving public behavior and proving both
call paths through the current acceptance tests.
```

A useful task envelope is:

```markdown
# Outcome
One observable result.

# Selected findings
Stable finding IDs from the frozen audit.

# Allowed writes
Exact files or globs.

# Non-goals
Adjacent cleanup and redesign that are not authorized.

# Invariants
Public behavior, schemas, dependencies, performance, data, or scientific
assumptions that must remain true.

# Baseline
Exact reproduction and current passing/failing evidence.

# Acceptance
Focused commands, applicable gates, held-out cases, and human review.

# Stop conditions
Authority conflict, unsafe write, scope expansion, dependency/public-contract
change, missing oracle, or inability to restore a probe.

# Return evidence
Diff, commands/cwd/exits, criterion mapping, rollback, and residual risk.
```

## Select roles by consequence

```text
Read-only uncertainty
    → Audit or Specifier

Small reversible behavior change
    → Specifier → Coder → QA

Structural or high-consequence change
    → Specifier → Coder → Cleaner → Architect → Hardener → QA
```

The same person or agent may perform several low-risk passes, but that is
self-review, not independent evidence. Keep phase boundaries explicit and use
one writing agent per worktree.

## Preserve human learning and epistemic continuity

Before launching an agent, the human owner should write:

```text
ANCHOR QUESTION
CURRENT MODEL
PREDICTED FILES OR MECHANISM
LIKELY FAILURE
ACCEPTANCE EVIDENCE
LEARNING TARGET
```

While the agent works, remain in the same problem neighborhood: write a test,
inspect an adjacent interface, predict the diff, or prepare review criteria.
When it returns, inspect the actual change and evidence, explain the mechanism in
your own words, and store a short learning or decision record.

Do not let high agent throughput create a queue of unreviewed artifacts. Stop
launching substantial tasks when one material result already waits for review.

---

# 11. Add Graft only after the repository is ready

The experimental branch treats Graft as optional derived navigation evidence.
It is not the mechanism that makes a messy repository trustworthy.

## 11.1 Readiness checklist

Do not start the F1 experiment until:

- the repository root and target source scope are unambiguous;
- the intended source files are Git-tracked;
- dirty-state handling is explicit;
- current contracts, tests, and canonical commands are known;
- a no-Graft workflow can complete the selected task;
- persistent context has a clear authority hierarchy;
- project secrets are absent from the child process environment and sensitive
  checkout exposure has been reviewed;
- Graft failure cannot fail ordinary Python gates;
- the project can preserve ignored local evidence safely; and
- a human has defined the comparison task and acceptance oracle.

Published Graft `0.16.0` was observed by the branch audit to omit a tracked
Python source file under a hidden directory. The adapter fails closed when its
tracked-source comparison detects that condition. If the repository has such
source, remain on F0. Do not move, ignore, or untrack legitimate code to make an
optional graph pass.

## 11.2 Port the bounded Graft bundle

Review and adapt these files from the generated reference project as one
separate change:

```text
GRAFT_EXPERIMENT.md
.cleanai/graft-experiment.toml
tools/graft_adapter.py
tools/graft-runtime/package.json
tools/graft-runtime/package-lock.json
tools/graft-runtime/README.md
tests/tooling/test_graft_adapter.py
docs/integrations/graft.md
docs/tutorials/evaluate-graft.md
prompts/evaluate-graft.md
relevant troubleshooting and glossary routes
```

Also merge—not replace—the required ignore entries for the private runtime and
`artifacts/graft/` state.

Do not copy or enable:

- `.mcp.json` or MCP registration;
- `graft init`;
- a global Graft installation;
- upstream-generated `AGENTS.md` instructions;
- Claude hooks or status lines;
- automatic prompt injection;
- `--deep` or provider/model credentials;
- LSP enrichment;
- visualization/export;
- or direct `graft`/`npx graft` commands.

The current project adapter intentionally exposes a smaller capability surface
than upstream Graft.

## 11.3 Adapt before installing

At minimum, inspect and update:

- repository source-scope rules;
- supported file extensions;
- ignored/generated/vendor directories;
- Node and npm qualification;
- package-lock integrity and provenance notes;
- evidence and runtime paths;
- timeout and output budgets;
- adapter tests;
- and removal ownership rules.

The current reviewed profile uses Node `>=22.12.0,<23`, npm `10.9.0` exactly,
and published `@nanonets/graft` `0.16.0`. These are the branch's bounded
qualification—not a claim that every existing repository should adopt those
versions. A changed toolchain requires a new review and tests.

## 11.4 Run the lifecycle through the project adapter

Complete the existing project's ordinary bootstrap first. Then run the
adapted equivalents of:

```bash
python tools/graft_adapter.py doctor
```

A missing runtime should be reported as **Unverified**, not as a failed Python
project.

After reviewing the local npm lock and explicitly authorizing connected native
lifecycle scripts:

```bash
python tools/graft_adapter.py install --apply
python tools/graft_adapter.py doctor
python tools/graft_adapter.py build
python tools/graft_adapter.py check
```

Ask one bounded location question:

```bash
python tools/graft_adapter.py ask \
  "Where is request authorization decided?" \
  --limit 5 --source
```

The exact launcher may need your project environment prefix. Use the generated
reference command only when the project actually uses that uv group.

## 11.5 Verify every Graft lead

Use this sequence:

```text
Graft result
    ↓
Exact current source read
    ↓
Exhaustive search in the declared scope
    ↓
Focused behavior or runtime test
    ↓
Applicable fast/full/release gate
    ↓
Human explanation and acceptance
```

For example:

```bash
python tools/graft_adapter.py ask \
  "Where is request authorization decided?" --limit 5 --source

rg -n --hidden \
  "authorize|authorization|permission|policy|access" \
  src tests config docs/contracts

pytest -q tests/path/to/authorization_test.py
```

Adapt the paths and terms. Do not run a copied placeholder command.

When a task contains *all*, *every*, *none*, *only*, or *complete*, start with
exhaustive search and executable verification. Bounded `ask` is a ranking aid,
not a completeness oracle.

## 11.6 Remove local Graft state safely

Stop direct Graft and other writers. Inspect first:

```bash
python tools/graft_adapter.py remove --check
```

Only after reviewing the inventory:

```bash
python tools/graft_adapter.py remove --apply
python tools/graft_adapter.py remove --check
```

The final check should report complete removal of the adapter-owned runtime and
derived state. It does not delete the tracked integration scaffolding. Remove
tracked files through a normal reviewed source change if the experiment is
retired.

A failed or unavailable Graft installation is not a reason to weaken the
project, alter legitimate source, or bypass the adapter. Return to F0.

---

# 12. Measure Graft against the clean no-Graft workflow

Do not evaluate Graft while simultaneously refactoring the repository,
rewriting `AGENTS.md`, changing the model, and replacing the test toolchain.
That experiment cannot identify what caused the result.

Compare:

| Cohort | Allowed navigation |
|---|---|
| `baseline-no-graft` | current source, `rg`/`git grep`, contracts, tests, and ordinary gates |
| `graft-structural-cli` | the same tools plus the bounded project adapter |

Hold constant:

- repository commit and clean state;
- task wording;
- agent, model, client, and permissions;
- persistent context;
- time and token budget;
- held-out acceptance commands;
- and human review rubric.

Use fresh worktrees and repeated runs. Keep expected paths and acceptance answers
outside agent-readable context when making a causal claim.

If the CleanAI friction ledger has been adapted and validated, the workflow is:

```bash
python tools/cleanai.py friction start \
  --task <task-id> --agent <agent-id> --cohort baseline-no-graft

# Run the task and independent review, then use the returned directory:
python tools/cleanai.py friction finish \
  <f0-run-directory> --accepted yes --human-interventions <count>

python tools/cleanai.py friction start \
  --task <task-id> --agent <agent-id> --cohort graft-structural-cli

# Include authorized install/build time according to the preregistered protocol.
# Run the same task and independent review.
python tools/cleanai.py friction finish \
  <f1-run-directory> --accepted yes --human-interventions <count>

python tools/cleanai.py friction compare \
  --cohort baseline-no-graft --cohort graft-structural-cli
```

Do not set `--accepted yes` from the agent's own summary.

Measure correctness and review before efficiency:

- independent acceptance result;
- human acceptance;
- missed sibling implementations;
- forbidden or unnecessary changes;
- reviewer corrections and later rework;
- relevant and irrelevant files opened;
- changed-file precision;
- time and tool calls to first relevant source and first correct edit;
- cold install/build and warm refresh cost;
- CPU, memory, disk, and process overhead;
- persistent instructions and tool-schema context;
- Graft queries and returned context;
- exact source and exhaustive fallback reads;
- total input/output tokens and monetary cost when available; and
- whether the reviewer can explain the final change without the agent summary.

Use this accounting model:

```text
net context cost
  = persistent context
  + tool schemas
  + retrieval queries
  + returned context
  + fallback source reads
  + correction and rework context

net operational cost
  = setup and installation
  + graph build and refresh
  + compute and storage
  + tool maintenance
  + human review
```

Missing measurements are **Unverified**, not zero.

Reject promotion after any reproducible regression in correctness, human
acceptance, privacy, scope discipline, reviewer correction, or rework. Only then
consider context, time, or monetary savings.

---

# 13. A practical pull-request sequence

A complex repository usually benefits from several small pull requests rather
than one transformation branch.

## PR 1 — Freeze and route

- baseline manifest and known failures;
- compact root context map;
- canonical commands;
- authority hierarchy;
- one active task-packet template;
- no code cleanup;
- no Graft.

## PR 2 — Truthful fast feedback

- one canonical fast gate using existing tools;
- CI invocation of the same command;
- missing-tool and skipped-check failure behavior;
- seeded sensitivity tests;
- no broad new quality stack.

## PR 3 — Context and document hygiene

- inventory and conflict map;
- selected duplicate authority reconciled;
- historical material scoped or archived;
- no mass deletion;
- before/after context measurement.

## PR 4 — One quality ratchet

Choose one:

- architecture fitness rule;
- product/harness coverage boundary;
- package smoke;
- curated semantic mutation;
- or dependency/security boundary.

Test that the control detects its intended seeded defect.

## PR 5 and later — Selected cleanup batches

Use finding IDs, bounded role prompts, one writer, focused behavior evidence,
applicable gates, rollback, and human acceptance.

## Separate experimental PR — Graft F1

Port the bounded Graft bundle only after the no-Graft workflow is useful. Keep
Graft absent from ordinary gates and compare the same tasks before retaining it.

---

# 14. Common migration mistakes

## Mistake: copying the complete generated repository over existing files

**Why it fails:** the template's example architecture and toolchain are not the
existing project's history or authority.

**Better:** generate a sibling donor and migrate one capability per PR.

## Mistake: starting with Graft

**Why it fails:** better retrieval cannot resolve contradictory requirements,
false-green tests, stale authority, or an unsafe release process.

**Better:** establish F0—source, exhaustive search, contracts, tests, and gates—then
evaluate Graft as an optional delta.

## Mistake: asking an agent to clean everything

**Why it fails:** the agent cannot know which apparent duplication encodes
compatibility, migration state, or domain distinction.

**Better:** freeze an audit, select finding IDs, and authorize one reversible
batch.

## Mistake: adding every quality tool immediately

**Why it fails:** setup and diagnostic churn can make feedback slower and less
trusted.

**Better:** begin with existing commands, then add one sensor that catches an
observed risk.

## Mistake: making green output the objective

**Why it fails:** blanket ignores, lower thresholds, skipped checks, and weak
assertions can produce a cleaner dashboard with less trustworthy software.

**Better:** test gate sensitivity and preserve explicit debt or Unverified
status.

## Mistake: treating generated summaries or graphs as documentation authority

**Why it fails:** static and generated representations can omit dynamic Python,
configuration, packaging, hidden paths, and design rationale.

**Better:** use them to route exact inspection and tests.

## Mistake: measuring only output tokens

**Why it fails:** fixed MCP context, setup, fallback reads, reviewer correction,
and rework may cost more than the tool saves.

**Better:** measure accepted-change correctness and total context/operational
cost.

## Mistake: launching more agents than the human can review

**Why it fails:** integration and verification debt becomes the bottleneck.

**Better:** stop launching material work when one result is waiting for review.

---

# 15. Definition of a successful first adoption

The first adoption milestone is complete when:

- the pre-migration revision and baseline are preserved;
- existing behavior has not changed unintentionally;
- one compact root context map identifies current authority and commands;
- `CLAUDE.md` or other client files contain only real client-specific deltas;
- one fast gate runs every named check and can detect seeded failures;
- historical and generated material is not loaded by default;
- one bounded task packet and prompt workflow has been completed end to end;
- the human owner can explain what changed, why it works, how it was verified,
  and where it may fail;
- rollback is tested or mechanically clear;
- remaining debt is explicit rather than hidden behind green output; and
- Graft is either absent or remains an optional experiment whose failure does
  not affect ordinary project quality.

A clean agentic workspace is not one with the most tools, documents, graphs, or
agents. It is one in which the correct path is easy to find, dangerous actions
are difficult or explicit, feedback is fast and truthful, and every accepted
change leaves both the software and the human mental model in a better state.

---

# 16. Where to go next

From the generated reference project, read only the route needed for the next
step:

- Prompt contract and roles:
  `prompts/README.md` and `prompts/PROMPT_CONTRACT.md`
- First bounded change:
  `docs/tutorials/first-agentic-change.md`
- Context hygiene:
  `docs/quality/context-hygiene.md`
- Quality gauntlet:
  `docs/quality/gauntlet.md`
- Architecture:
  `docs/architecture/layers.md`
- CRAP and mutation:
  `docs/tutorials/crap-and-mutation.md`
- Agent-friction evaluation:
  `docs/quality/agent-friction.md`
- Graft trust boundary:
  `docs/integrations/graft.md`
- Controlled Graft experiment:
  `docs/tutorials/evaluate-graft.md`
- Troubleshooting:
  `docs/troubleshooting.md`

Use the smallest route that answers the current task. Do not make reading the
entire template a prerequisite for changing one existing repository.
