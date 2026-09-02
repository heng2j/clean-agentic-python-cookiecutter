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

Every command ledger records a schema version, command argv as a list, working root, base revision/dirty state when Git exists, start/end UTC timestamps, exit code, status, deterministic/connected classification, tool versions, raw-output paths, and limitations.

Allowed result states are `passed`, `failed`, `invalid`, `infrastructure_error`, `blocked`, and `unverified`. Only `passed` can satisfy a required gate. Missing or skipped required records are errors.

Mutation adds target hash, isolated-copy path identity, baseline result, mutant result, declared kill oracle, classification, score numerator/denominator, and live-source after-hash. CRAP adds coverage.py version/schema, exact source file identities, callable spans/complexity/covered and measurable lines, equation label, sort rule, and threshold.

The science audit records findings for required workspace paths, dotenv/result
ignore rules, tracked dotenv filenames, and static-input manifest containment,
metadata, content hashes, and explicit package imports of workspace modules. It
does not detect every dynamic import or filesystem lookup. A passing manifest establishes internal identity
and schema consistency only. It does not prove origin, license, execution,
scientific validity, privacy, or fitness for use.

Generated evidence is never normative authority. Keep it out of default agent context and expire or archive it deliberately.
