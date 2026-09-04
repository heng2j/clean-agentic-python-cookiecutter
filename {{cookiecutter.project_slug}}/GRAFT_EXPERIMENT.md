# Optional Graft experiment

This generated project includes a bounded experiment with
[Graft](https://github.com/trailhq/Graft), a structural code-context tool for
coding agents.

Graft is **not** installed automatically, is not a Python dependency, and is not
part of the build, test, quality, or release boundary. The project does not run
`graft init`, enable upstream hooks, alter global agent settings, or invoke the
model-backed `--deep` mode.

Start here:

1. Read [`docs/integrations/graft.md`](docs/integrations/graft.md).
2. Review the pinned policy in [`.cleanai/graft-experiment.toml`](.cleanai/graft-experiment.toml).
3. Install the exact external version only after reviewing its current package,
   license, telemetry, and security documentation.
4. Run `uv run --locked --group dev python tools/graft_adapter.py doctor`.
5. Follow [`docs/tutorials/evaluate-graft.md`](docs/tutorials/evaluate-graft.md)
   to compare no-Graft, CLI-pull, and optional MCP-pull cohorts.

Graft maps, rankings, call graphs, and blast-radius reports are **derived
navigation evidence**. They may tell a person or agent where to inspect; they do
not override current source, executable behavior, contracts, ADRs, tests, or
human acceptance. Ranked retrieval is not exhaustive search.
