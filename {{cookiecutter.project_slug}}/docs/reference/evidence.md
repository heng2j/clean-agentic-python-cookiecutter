---
status: normative
authority: reference-evidence-schema
owner: maintainers
last_verified: 2026-09-01
applies_to:
  - "artifacts/**"
  - "tools/**"
---
# Evidence and status schema

Evidence schemas are command-specific. A gauntlet JSON ledger records its
schema version, profile, overall result, planned commands, and repository
metadata (Python, platform, machine, Git revision, and dirty-state entries when
available). Each step records configured text, expanded argv, one of `passed`,
`failed`, `error`, `timeout`, or `skipped`, the child return code, duration,
local/connected classification, error detail when applicable, and separate
stdout/stderr filenames and SHA-256 hashes. A skipped required step cannot make
the gauntlet pass.

The unique run-directory name contains a UTC creation timestamp. The gauntlet
payload does **not** claim per-step wall-clock timestamps, arbitrary tool
versions, or a universal limitations field; preserve those separately when a
review or release needs them. The child return code in a failed step is not the
same thing as the outer gauntlet exit code.

Mutation evidence records the configuration, isolation claim, complete
baseline result, per-mutant status/result, and score/floor. CRAP evidence
records its local equation and algorithm labels, coverage schema/path,
threshold semantics, and each callable's span, complexity, line-coverage
percentage, and estimate. These are distinct schemas, not interchangeable
universal result states.

The science audit records findings for required workspace paths, dotenv/result
ignore rules, tracked dotenv filenames, and static-input manifest containment,
metadata, content hashes, and explicit package imports of workspace modules. It
does not detect every dynamic import or filesystem lookup. A passing manifest establishes internal identity
and schema consistency only. It does not prove origin, license, execution,
scientific validity, privacy, or fitness for use.

Generated evidence is never normative authority. Keep it out of default agent context and expire or archive it deliberately.
