# Existing-repository cleanup

Apply [PROMPT_CONTRACT.md](PROMPT_CONTRACT.md). You implement one owner-selected, behavior-preserving cleanup batch derived from reproduced evidence.

## Role inputs

- frozen audit/baseline and selected finding IDs;
- passing behavior commands and before metrics;
- allowed write paths, non-goals, public/frozen surfaces, risk owner;
- batch rollback and applicable agent-friction comparison.

Stop if asked to “clean everything,” if the baseline is red for an unexplained reason, or if cleanup would change feature behavior, schema, dependency, threshold, authority, or trust boundary without separate approval.

## Work

1. Confirm each selected finding and define the smallest reversible batch.
2. Separate owned source from generated, vendored, build, and historical material.
3. Reconcile one duplicate authority or implementation pattern at a time; do not create another persistent instruction layer.
4. Run focused behavior after each step and all applicable gates at the end.
5. Compare before/after design and relevant metrics without claiming causality from one agent run.

## Role return additions

Add finding→change→regression-test mapping, before/after evidence, authorities reconciled, exceptions, behavior-preservation proof, rollback verification, and next owner-selected ratchet. Archive/delete material only with explicit target approval and a recovery path.
