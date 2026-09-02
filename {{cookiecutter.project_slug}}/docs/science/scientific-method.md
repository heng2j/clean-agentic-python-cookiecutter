---
status: normative
authority: scientific-method-contract
owner: maintainers
last_verified: 2026-09-02
applies_to:
  - "src/**"
  - "tests/**"
  - "notebooks/**"
  - "static/**"
  - "results/**"
---
# Scientific method contract

Before treating an output as evidence, record the question or claim, input
population, assumptions, units and coordinate conventions, algorithm and
scientifically material defaults, validity domain, numerical tolerances,
randomness policy, comparison oracle, and known limitations.

Tests should distinguish software behavior from scientific validation. A unit
test can prove that a formula was implemented as specified; it cannot by itself
prove that the formula or dataset represents the phenomenon of interest.

Comments and docstrings should preserve information the code cannot express
clearly: equation provenance, units, frame conventions, stability choices,
validity ranges, and reasons for non-obvious approximations. Google-style
structure is a local presentation convention, not a substitute for that content.

If randomness matters, use an explicit generator or seed, test statistical
properties where appropriate, and report nondeterministic limits. Never promise
bit-for-bit reproduction across untested hardware, BLAS libraries, accelerators,
thread counts, or dependency versions.
