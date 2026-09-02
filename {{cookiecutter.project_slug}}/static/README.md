# Static inputs

Store only small, stable, redistributable input data or fixtures here. Production
or test code must not silently depend on a developer's untracked local data.

Register every additional committed file in `manifest.toml` with its repository-
relative path, SHA-256, source or generation method, license identifier or terms,
and a short description. `science-audit` checks containment, uniqueness,
existence, and hashes. It does not verify that a declared source or license is
truthful or that the data is scientifically suitable.

Keep large, private, regulated, or redistribution-restricted inputs outside Git.
Document an authorized retrieval procedure and stable identifier instead.
