# Graft source index

This index records the primary upstream and registry sources used by the audit.
Links to source code are pinned to the reviewed `v0.16.0` commit wherever
possible. An issue is evidence that a limitation was reported, not independent
proof that it affects every environment or remains unresolved.

## Identity, publication, and license

| Subject | Primary source | Audit use |
|---|---|---|
| Reviewed source tree | [`v0.16.0` commit `aa1e2bb0f6326068ac64886da1e67fa25a7804de`](https://github.com/trailhq/Graft/tree/aa1e2bb0f6326068ac64886da1e67fa25a7804de) | **Observed:** npm `gitHead` and tag commit match |
| Published package | [`@nanonets/graft@0.16.0`](https://www.npmjs.com/package/@nanonets/graft/v/0.16.0) | **Observed:** selected published artifact |
| Version metadata | [Registry version record](https://registry.npmjs.org/@nanonets/graft/0.16.0) | **Observed:** name, version, integrity, `gitHead`, engines, scripts, license |
| Publication history | [Full registry record](https://registry.npmjs.org/@nanonets/graft) | **Observed:** `0.16.0` published `2026-08-31T14:35:52.197Z`; versions end at 0.16.0 at audit time |
| License | [Pinned MIT license](https://github.com/trailhq/Graft/blob/aa1e2bb0f6326068ac64886da1e67fa25a7804de/LICENSE) | **Observed:** MIT, copyright 2026 Context Graph Engine contributors |
| Unpublished source comparison | [`main` snapshot `05760b07abc0e427f5af8ad378889ee402c5afc6`](https://github.com/trailhq/Graft/tree/05760b07abc0e427f5af8ad378889ee402c5afc6) | **Observed at freeze:** source declares 0.17.0; it is not the selected distributable |

**Unverified:** the published `dist/` tree has no audit-verified reproducible-build
attestation tying every byte back to the tag source. Registry integrity identifies
the downloaded bytes; it is not source-to-package provenance.

## Runtime and integration boundaries

| Boundary | Pinned source | Audit use |
|---|---|---|
| Installation | [`scripts/postinstall.mjs`](https://github.com/trailhq/Graft/blob/aa1e2bb0f6326068ac64886da1e67fa25a7804de/scripts/postinstall.mjs) | **Source-supported:** install telemetry/flush behavior and pre-install opt-out requirement |
| CLI startup | [`src/cli.ts`](https://github.com/trailhq/Graft/blob/aa1e2bb0f6326068ac64886da1e67fa25a7804de/src/cli.ts) | **Source-supported:** dotenv load, pre-action upkeep, command surface |
| Telemetry | [`TELEMETRY.md`](https://github.com/trailhq/Graft/blob/aa1e2bb0f6326068ac64886da1e67fa25a7804de/TELEMETRY.md) | **Source-supported:** declared events, properties, and opt-out contract |
| Upkeep/background work | [`src/upkeep.ts`](https://github.com/trailhq/Graft/blob/aa1e2bb0f6326068ac64886da1e67fa25a7804de/src/upkeep.ts) | **Source-supported:** update check and detached-process boundary |
| MCP server | [`src/mcp/server.ts`](https://github.com/trailhq/Graft/blob/aa1e2bb0f6326068ac64886da1e67fa25a7804de/src/mcp/server.ts) | **Source-supported:** server-owned instructions, tools, startup, and upkeep boundary |
| Init/global writes | [`2f69b3f60ad86afc23ea8d5b1859725b72b5bf5f`](https://github.com/trailhq/Graft/commit/2f69b3f60ad86afc23ea8d5b1859725b72b5bf5f) | **Source-supported:** host integration and user-level write behavior examined as rejected F6 |

### Transitive install boundary

| Subject | Pinned source | Audit use |
|---|---|---|
| `tree-sitter-cli@0.23.2` registry metadata | [Exact registry version record](https://registry.npmjs.org/tree-sitter-cli/0.23.2) | **Observed:** the reviewed consumer lock resolves this exact install-script package |
| `tree-sitter-cli@0.23.2` install script | [`install.js` at tag commit `d97db6d63507eb62c536bcb2c4ac7d70c8ec665e`](https://github.com/tree-sitter/tree-sitter/blob/d97db6d63507eb62c536bcb2c4ac7d70c8ec665e/cli/npm/install.js) | **Source-supported:** the script constructs a GitHub-release asset URL from platform/architecture and downloads/decompresses that binary during npm install |

**Observed:** the installed `tree-sitter-cli@0.23.2` `install.js` used in the
isolated supply-chain inspection had SHA-256
`e55e399145a389df20c59d042122a8cd746adc87e02851f6f1200962a0fb7ddf`,
identical to the pinned tag source above. The consumer lock authenticates the
npm tarball, not the separately downloaded GitHub-release executable. This
establishes a possible network/integrity boundary; it does not establish that a
new download occurred in every successful install.

## Upstream issue evidence

| Issue | Reported constraint | Audit treatment |
|---|---|---|
| [#234](https://github.com/trailhq/Graft/issues/234) | Graft/Commander Node-engine mismatch | Supports the narrowed Node floor; not a substitute for executed compatibility tests |
| [#117](https://github.com/trailhq/Graft/issues/117) | Retrieval benchmark underperformance versus a lexical baseline | Motivated independent retrieval trials; audit conclusions use its own observed results |
| [#260](https://github.com/trailhq/Graft/issues/260) | Deep-result truncation | One reason F5 remains rejected; F5 was not executed |
| [#211](https://github.com/trailhq/Graft/issues/211) and [#212](https://github.com/trailhq/Graft/issues/212) | MCP interoperability failures | Supports treating F2 as a separate capability; audit also measured fixed MCP context |
| [#119](https://github.com/trailhq/Graft/issues/119) | ARM64 incompatibility | ARM64 remains **Unverified** rather than declared unsupported everywhere |
| [#221](https://github.com/trailhq/Graft/issues/221) | Hidden-directory exclusion | Consistent with observed/source-reviewed scope limits; hidden paths are not treated as indexed |

## Interpretation boundary

**Source-supported** claims describe what the reviewed sources or issue reports
say. **Observed** claims require the audit's own command, filesystem, package, or
benchmark evidence. Current source, tests, contracts, ADRs, and explicit human
decisions remain authoritative within their scope; Graft output is derived
navigation evidence only.
