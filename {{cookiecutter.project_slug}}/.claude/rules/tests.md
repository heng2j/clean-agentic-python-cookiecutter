---
paths:
  - "tests/**/*.py"
---
# Test scope

- Test observable behavior, invariants, and failure boundaries rather than private structure.
- Reproduce a defect before repair; distinguish expected red from infrastructure failure.
- Never weaken/delete an assertion or exclude a path merely to pass.
- Keep acceptance language understandable without Python knowledge.
