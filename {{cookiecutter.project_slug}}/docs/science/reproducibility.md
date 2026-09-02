---
status: normative
authority: scientific-reproducibility
owner: maintainers
last_verified: 2026-09-02
applies_to:
  - "notebooks/**"
  - "results/**"
  - "scripts/**"
  - "static/**"
---
# Reproducibility and artifact provenance

The reviewed `uv.lock` reproduces one Python dependency resolution. It does not
capture external datasets, environment variables, operating-system libraries,
hardware, accelerators, thread settings, clocks, remote services, or scientific
validity.

For a result intended for review or publication, preserve at least:

- repository commit and dirty state;
- exact argv/configuration and working directory;
- Python, platform, dependency-lock, and relevant native-library identity;
- input dataset identifiers, origins, licenses, and content hashes;
- random seeds or generator state when meaningful;
- hardware/backend/thread settings that may affect the result;
- start/end timestamps and output hashes;
- the validation oracle, uncertainty method, and known limitations.

Do not put credentials in manifests, notebooks, logs, or result bundles. Do not
claim exact reproduction where a connected service, unpinned external asset, or
nondeterministic backend prevents it. Label such a path **Unverified** and name
the missing condition.

Generated payloads under `results/` are ignored by default. Curated reference
results require an explicit maintainer decision covering size, license, privacy,
provenance, and a repeatable verification command.
