---
status: normative
authority: scientific-data-and-secrets
owner: maintainers
last_verified: 2026-09-02
applies_to:
  - ".env*"
  - ".envrc"
  - "static/**"
  - "notebooks/**"
  - "results/**"
---
# Data and secret handling

`direnv` is optional convenience, not a secret vault. Review `.envrc` before
running `direnv allow`. The shipped file exposes an existing virtual environment
but leaves `dotenv_if_exists .env` commented out. Enable that line only after an
explicit task-level decision. Values exported from `.env` can be read by every child
process—including coding agents and test tools—started in that directory.

Use least-privilege, project-specific credentials; keep `.env` ignored; provide
only empty names or harmless placeholders in `.env.example`; avoid printing the
environment; and rotate a key if it may have entered Git, logs, notebooks, shell
history, artifacts, or agent traces. Use `direnv deny` before running untrusted
repository code that does not need those variables.

Only small, redistributable inputs belong in `static/`. Register each committed
asset in `static/manifest.toml` with origin or generation method, license, and
SHA-256. Large, private, regulated, licensed-with-restrictions, or frequently
changing inputs stay in an appropriate external system; commit metadata and a
retrieval procedure only when redistribution permits it.
