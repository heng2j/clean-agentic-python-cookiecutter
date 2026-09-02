---
status: normative
authority: adr-isolated-mutation-evidence
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "tools/**"
  - ".cleanai/*mutations.toml"
---
# ADR 0002: isolate mutation and fail closed on missing evidence

## Decision

Curated mutants run only in disposable repository copies. Targets must be ordinary, non-symlink files whose lexical and resolved paths remain inside the repository. A mutant is killed only when an explicit behavior oracle matches. Zero valid mutants, invalid replacement syntax, baseline failure, timeout, missing tools, malformed coverage, incomplete callable coverage, or foreign coverage are errors and cannot improve a score.

## Consequence and risk

This protects live and concurrent user edits and keeps infrastructure failures out of confidence metrics. It costs temporary disk and makes mutation slower. An isolated copy still does not make an unsafe verification command safe; commands remain maintained configuration and need review.

## Alternatives rejected

- Edit/restore the live checkout: faster, but termination and concurrent edits can corrupt or erase work.
- Count every nonzero mutant command as killed: simpler, but syntax and infrastructure failures create false confidence.
- Treat empty denominators as 100%: mathematically convenient, operationally misleading.

## Verification

Regression fixtures cover termination, timeout, concurrent runs, dirty edits, symlink/path escape, zero/invalid mutants, explicit kill oracles, and live-source hashes.
