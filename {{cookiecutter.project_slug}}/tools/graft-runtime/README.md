# Optional Graft runtime lock

This directory pins the optional structural-navigation experiment. It is not a
Python project dependency and is not installed by generation, `uv sync`, tests,
packaging, hooks, or release gates.

The reviewed npm artifact is `@nanonets/graft@0.16.0` with registry integrity
`sha512-L3E5F1aDYJDCARgfR7O2VaMt8xwO1XNYyHiW2n1WhKnj87gPqoxoZJGNbGXfw6XeA9JSJX3naA36RZ+jDf4AcQ==`.
Its unsigned upstream tag resolves to commit
`aa1e2bb0f6326068ac64886da1e67fa25a7804de`; build provenance remains
unverified.

The reviewed installer requires npm `10.9.0` exactly. A different npm version
is a new supply-chain experiment and fails closed until the lock and real-package
journey are revalidated.

Use `uv run --locked --group dev python tools/graft_adapter.py install --apply`
only after reviewing this
lock and the experiment guide. The explicit opt-in runs locked native npm
install scripts. `--ignore-scripts` is not a functional alternative for this
release because a required Tree-sitter native binding is then unavailable.
