# Evidence reference and lifecycle

## Stable committed evidence

This directory contains the frozen original reports, stable cross-run summaries,
feature decisions, threat models, structured findings, and migration guidance.
The original manifest covers 160 tracked files. Its original checksum ledger is
committed here as `ORIGINAL_SHA256SUMS.txt`; raw command-output checksums are
also retained in the external evidence bundle.

## Volatile evidence kept outside Git

Raw stdout/stderr, command JSON records, npm tarballs/caches, installed native
runtime, generated Graft graphs, fresh worktrees, and process/network probes are
machine-specific or source-derived. They must remain under the ignored audit
workspace and be attached to the draft pull request as a checksummed evidence
archive. Committing them would turn transient derived output into stale project
history.

Expected archive groups:

| Group | Content | Stable reference |
|---|---|---|
| `original/` | Baseline commands, manifest, adversarial originals | Original reports and structured findings here |
| `supply-chain/` | Registry/source/tarball/lock inspection | Audit and threat model |
| `adapter/` | Focused seeds, fault injection, real-package runs | V2 structured findings and validation |
| `explainability/` | Gold fixture, raw Graft outputs, metrics | Explainability report |
| `context-benchmark/` | Preregistration, 144 query records, external oracles | Retrieval/context report |
| `actual-agent-trials/` | Preregistration, six diffs, held-out oracle results | Retrieval/context report |
| `final/` | Exact final-source 3.12/3.13 release records, connected-install failures, seeded real-package compatibility/removal control, held-out applicability, and report validation | Validation report |

## Known stable hashes

| Artifact | SHA-256 |
|---|---|
| Governing charter — 813 lines / 29,709 bytes | `8dd3e4c95d72ec3675a7b0c8ebebc12ba4e287f8eb1037c5787b1a294ab537a4` |
| Benchmark preregistration | `83ed278a19f2ad3bf77e56ffcc375831aabd48cd91480f6f86217613fa96840c` |
| Full benchmark result JSON | `f2d0a4a38b6d95a270fcf4c1acc62846d1249ca35c124b09c15f27f4e5a23c62` |
| Benchmark runner | `457ccb2ed0a7265e2458d1bef7403f7a7946ab1fe80fcaa54610c8d8b66ad7b1` |
| Agent trial task | `99771a55c2580ec4a574ab359faa4fc5591c02f3e42ecb06e0a2f709b149256d` |
| Held-out agent acceptance oracle | `8f8eb5a99bea98e5fec961d877df92aa71e18db2dcfd036cddf6cd16eba9c3f9` |
| Agent trial preregistration | `75707330adb0063e14164899bc5d566fa362f1a5d01119c96d965bfe9a2c76c8` |
| Python 3.12 template-copy hash list at `6966b55` | `39bd52c077bab56916ed2d2b658a0ce197d49e4fc81a73f934ec316853f295ee` |
| Python 3.12 command-summary JSON at `6966b55` | `afb6ff8eb969244fdba769c59c52807edfc2ff6cb508dcec97f445262c876107` |
| Python 3.12 environment record at `6966b55` | `203f2b77ebda37dd0c01b7f023f8e12c8dd204eb88acfd73992c85a6a0306a80` |
| Python 3.13 authored-source manifest at `6966b55` | `3f1eba7c792cfc561ed18538cf199ff7f3bc0c831da86e41775b890682f3c132` |
| Python 3.13 command ledger at `6966b55` | `bbe6052636859edc96fb376bde9a744ee9b427b3fa68308615cae0072e2d9551` |
| Python 3.13 runner at `6966b55` | `501d0c24799c9b8f00438c0b2200b9f6ea5a7852b05e810739b9bc63c640b1e2` |
| Python 3.13 public-output verifier at `6966b55` | `2fe596166ff31d289d13cb7b36ffd884d1b38874c6cddc455e8b2605f2dc4f13` |
| Final-F1 applicability-trial report at `6966b55` | `015b80b3ed40fe4778b2a477bfd5ec486ca1efacce28f26f6da6407478858d1b` |
| Final-F1 applicability-trial result JSON at `6966b55` | `b77ad0c44b4b162528751154ce30295dd6625a8fc466d7c9b29b00e96d9d6ce6` |
| Final-F1 applicability-trial top-level ledger at `6966b55` | `abf5206a7452b4cb0ac889517d9abceb97cdafea9aa500359ccd8f1bef8d2fb9` |
| Real-Graft seeded-lifecycle summary at `6966b55` | `f63c0d37ba9778ca03c0fc20db03eefe42766e82e3eae01ad9418359c5b158a3` |
| Real-Graft seeded-lifecycle result JSON at `6966b55` | `95820c841b72589b8e96646e3e60d0c76b8187f06392b3b1d869ee2950572248` |
| Real-Graft evidence manifest at `6966b55` | `5009ea3b91ca61ca8f5bbbeffb59fa965d7b8bcae5896768485d7e5249847fc0` |
| Documentation-follow-up summary at `4bba7c0` | `cf7085eaa0451300d07d22626f3d6cd0b4f1915bedea0bebfc10adb37c4daf70` |
| Documentation-follow-up artifact-checksum ledger at `4bba7c0` | `f5e5d1362d94a5d6af166cfdb144772f22fa6e968589d8b165423392c26413ed` |
| Final source tree at local `b719459` and remote `4dc3603` | `35819081108685c24f47ba5251ec7e18004b0016` |
| Final template README | `6bed52806381a37059149e06c64dc2ecf366ffc91e88587bfe70bf295cfe0039` |
| Final generated-project README template | `16a5973f34c94b25d41bdabfbe36bed0ddbf707d67995eea29dc85684793a529` |
| Final adapter | `bda5c77cdc96523f62d6a645f01b6dacf680a5a5657c3a29dba8358352501b64` |
| Final focused adapter tests | `7f347e2fd21483493536a3bc0919338d165ba452ec42f0c333ce05a3c836702d` |
| Final seeded real-package control result | `f9656d29c2fbf3a771d5e772fe4479e7868efd51545499ae76ab525eca0afae6` |
| Final seeded real-package control ledger | `e27d8a78cf6857fd75a534293e9d958f20f0df205fe99b68d6b00e54b4aa5761` |

The final external evidence archive and its checksum ledger are produced only
after the hosted publication checkpoint. Until then, their final bytes remain
**Unverified**. A hash identifies bytes; it does not establish that a claim
drawn from them is correct.

## Command-record schema limitation

**Observed:** the raw benchmark query records capture arguments, working
directory, exit status, output, and elapsed time, while top-level metadata binds
repository/tool identities and limitations. The exact Python 3.12 records
capture most charter fields, but omit per-command start/end timestamps and
per-command ignored-file deltas; aggregate state checks cover the latter. The
Python 3.13 ledger captures command and expected/actual exit, with separate run-
level environment, source, timing, and integrity records, so more fields are not
repeated per command. Neither set is charter-complete. Baseline records also
generally omit an explicit per-command starting-revision/dirty policy.

The seeded real-Graft lifecycle is richer: each `.meta` file records argv, cwd,
start/end, duration, exit, and stream hashes, and selected operations add
process/environment/socket observations. It still does not provide every field
above for every command, so it does not close the charter-completeness gap.

**Unverified:** the existing raw archive, including the otherwise successful
Python 3.12/3.13 exit records, is not charter-complete command evidence for those
fields. Stable repository-level metadata and clean-tree checks cannot be
silently promoted to missing per-command records. Exit behavior is reported
separately as **Observed**; command-evidence completeness remains
**Unverified**. Any future rerun should emit the full command schema named in
`VALIDATION_GRAFT_VARIANT_V2.md`.
