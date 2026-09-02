# Contributing

Thank you for improving {{ cookiecutter.project_name }}. Start with an issue or a
small task packet when the scientific intent, compatibility impact, or allowed
change surface is unclear.

## Development path

```bash
uv lock --check
uv sync --locked --group dev
uv run --locked --group dev python tools/cleanai.py gauntlet fast
```

Before review, run the smallest relevant focused tests and then the full gate.
Release candidates must pass the release gate from a clean, immutable checkout.
Hooks are optional convenience; install them with
`uv run --locked --group dev prek install` and remember that CI remains the
authority.

## Pull requests

Describe the observable outcome, scientific assumptions, scope and non-goals,
tests and exact commands, data/result provenance, compatibility impact, and
remaining risk. Do not include credentials, private data, or generated result
payloads without explicit maintainer approval. New dependencies need a concrete
need, maintenance/license review, and a reviewed lock diff.

Follow the project license for code. Confirm separate permission for data,
documentation, figures, model weights, or other third-party artifacts.
