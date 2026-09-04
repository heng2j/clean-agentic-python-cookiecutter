# Original Graft integration threat model

Audit target: `experimental-graft-variant` at
`ab3e06f6a402a22f51d8447101f245eab258b8e6`. This checkpoint predates all
remediation.

## Assets and authority

The protected assets are source and Git state, project/user files outside the
ignored Graft state directory, credentials loaded by the shell or `direnv`,
agent context, deterministic quality evidence, network/privacy choices, and the
human-owned acceptance decision. Graft output is derived navigation evidence;
it is not authority.

## Boundaries and adversaries

| Boundary | Adversarial condition | Original control | Observed result |
|---|---|---|---|
| Python wrapper → npm program | A PATH-first executable lies about its version | Search PATH and parse any semver in stdout | **Failed:** arbitrary executable accepted and run |
| Parent shell → Graft child | Ambient project/cloud/repository secrets exist | Copy environment, remove eight provider names | **Failed:** arbitrary synthetic credential names crossed boundary |
| Project → artifact state | `artifacts/`, home, cache, or graph is a symlink | Lexical paths only | **Failed:** `doctor` overwrote outside sentinels and exited 0 |
| User arguments → upstream CLI | Help/version aliases, attached flags, huge limits, source symlinks | Command denylist over `REMAINDER` | **Failed:** no-op success, cost bypass, and outside-source read reproduced |
| Adapter graph → upstream query/MCP | Non-default graph directory | `GRAFT_DIR` environment only | **Failed:** six advertised operations could not consume the built graph correctly |
| Upstream process → network/home | Update and telemetry background behavior | `DO_NOT_TRACK` plus synthetic update cache | **Partial:** telemetry gate is source-supported; cache writes are mutating and symlink-unsafe; no network sandbox exists |
| MCP server → agent context | Upstream instructions and broad schemas | Direct upstream MCP exposure | **Failed by design review:** schemas bypass adapter caps and instructions compete with project authority |
| Structural graph → decisions | Dynamic/config/runtime behavior is absent | Written disclaimer and source fallback guidance | **Partial:** disclaimer is strong; measured false negatives remain material |
| Evaluation harness → agent | Acceptance oracle should be held out | Run metadata stored beside task | **Failed:** paths and verification commands are agent-readable |
| Optional experiment → ordinary project | Graft absent | No Python dependency or gate hook | **Partial:** direct tests/build pass, but all canonical gauntlets are red because an added test is not formatted |

## Abuse cases reproduced

1. Replace `artifacts/graft/home/empty.env` or an ancestor with a symlink to an
   outside sentinel. `doctor` truncates the outside file and reports success.
2. Put a synthetic executable first on PATH, print `0.17.0`, and observe both
   arbitrary inherited secret names and an out-of-root write.
3. Invoke `run build --help`, `run build -v`, `run build -j99`, or unbounded
   retrieval options. The wrapper forwards them; help/version can return zero
   without building anything.
4. Pass a relative symlink as a positional repository argument. Lexical checks
   accept it and the child reads outside the project.
5. Copy the advertised MCP example. Git will stage it because `.mcp.json` is
   not ignored, while the context audit still reports green.

## Residual threats at the checkpoint

The wrapper is not a sandbox. A direct `graft` command bypasses it; an npm
package executes with the user's OS authority; static Python extraction is
necessarily incomplete; Git history may contain personal data; graph artifacts
contain source-derived material; and the package/install path has transitive
native dependencies. Those risks require explicit opt-in, project-local
installation, minimal environment, bounded schemas, containment, and
independent source/tests even after remediation.
