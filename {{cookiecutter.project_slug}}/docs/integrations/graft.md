---
status: reference
authority: integration-graft
owner: maintainers
last_verified: 2026-09-03
applies_to:
  - "tools/graft_adapter.py"
  - ".cleanai/graft-experiment.toml"
  - ".mcp.json.example"
  - "artifacts/graft/**"
---
# Experimental Graft integration

## What this adds

Graft builds a local structural index of source files, symbols, imports, calls,
and source spans. Its CLI can orient a coding agent, retrieve likely relevant
source, show a file's symbol skeleton, trace callers, search indexed files, and
estimate the structural blast radius of a diff.

This project integrates it as an **optional structural-pull experiment**. Graft
is external to the Python environment and is not required by any ordinary gate.
Its generated state lives under ignored `artifacts/graft/`.

## Authority boundary

Treat every Graft map, ranking, graph edge, summary, and blast report as derived
advisory evidence. Verify consequential conclusions against:

1. current source and observed behavior;
2. normative contracts and ADRs;
3. executable tests and deterministic gates; and
4. task-specific human acceptance.

`graft ask` is ranked retrieval. It can omit relevant files. Use indexed
`graft grep`, ordinary `rg`, tests, runtime evidence, and independent inspection
when a task requires **all**, **every**, **none**, or a complete blast radius.
Static analysis may miss decorators, dynamic imports, plugins, reflection,
configuration-mediated behavior, generated code, and runtime registration.

## Deliberate restrictions

The project-owned adapter:

- requires Graft `0.17.0` and Node `22.12.0` or newer;
- invokes subprocesses without a shell;
- forces `DO_NOT_TRACK=1`;
- removes common model-provider credentials;
- redirects dotenv loading away from the project `.env`;
- stores the graph and runtime home under ignored `artifacts/`;
- seeds the inspected release's update cache to suppress its detached npm check;
- uses content-hash freshness;
- blocks upstream ignore-file edits; and
- rejects `graft init`, hooks/global setup, `--deep`, provider/model/key options,
  LSP enrichment, visualization, and LLM-backed blast naming.

These controls reduce accidental scope; they are not a security sandbox. Direct
`graft` commands bypass them.

## Explicit installation

Review the current upstream repository, MIT license, package metadata, telemetry
contract, security policy, and release notes before installing. The pinned
experiment targets upstream commit
`05760b07abc0e427f5af8ad378889ee402c5afc6`.

```bash
npm install --global @nanonets/graft@0.17.0
graft telemetry disable
uv run --locked --group dev python tools/graft_adapter.py doctor
```

The first command is a connected machine-level side effect and is intentionally
not automated by this template.

## Structural CLI workflow

```bash
uv run --locked --group dev python tools/graft_adapter.py run build
uv run --locked --group dev python tools/graft_adapter.py run check --json
uv run --locked --group dev python tools/graft_adapter.py run map

uv run --locked --group dev python tools/graft_adapter.py run \
  ask "Where is release blocking decided?" --source

uv run --locked --group dev python tools/graft_adapter.py run \
  skeleton src/{{ cookiecutter.package_name }}/domain/change_risk.py

uv run --locked --group dev python tools/graft_adapter.py run \
  callers evaluate_release --depth 2

uv run --locked --group dev python tools/graft_adapter.py run \
  grep "release_blocked" --fixed

uv run --locked --group dev python tools/graft_adapter.py run \
  blast --base origin/main --format markdown
```

## Optional MCP pull mode

`.mcp.json.example` is intentionally inactive. After checking the current client
configuration format, copy it locally:

```bash
cp .mcp.json.example .mcp.json
```

Keep `.mcp.json` uncommitted. Restart the client. Measure MCP as a separate
cohort because tool schemas and always-available tools consume fixed context
before any useful retrieval occurs.

## Privacy and network boundary

According to Graft's repository telemetry contract, official npm builds collect
opt-out anonymous events, while source builds are described as telemetry inert.
The adapter forces telemetry off for children. Its structural profile requires
no LLM, and model-backed options are blocked. The adapter also suppresses the
inspected release's npm update check with a project-local cache record.

This is version-specific behavior, not a network sandbox or promise about future
releases. Graft remains outside the project's offline quality and release trust
boundary. Never put secrets into queries or shared evidence.

## Removal and upgrades

Remove local state and optional MCP configuration with:

```bash
rm -rf artifacts/graft .mcp.json
npm uninstall --global @nanonets/graft
```

For an upgrade, review upstream changes, update every version/commit reference
in one patch, rerun adapter and template tests, and repeat the same registered
task bank. Do not change the benchmark to favor the new release.
