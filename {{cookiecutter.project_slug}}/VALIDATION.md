# Validation evidence, not authority

This generated source tree makes no timeless pass claim. Test counts, tool versions,
coverage, mutation results, timestamps, and platform observations belong in the
release evidence for the exact source hash—not in persistent project instructions.

Start with `uv lock --check`, then run
`uv run --locked --group dev python tools/cleanai.py gauntlet release`. Preserve the resulting raw logs,
exit codes, ledger, source revision, dirty state, and environment. A green result
establishes only that the named checks met their bounded oracles; it does not prove
correctness, security, fitness for use, or support on an untested platform.
