---
name: yagni
description: >
  Run in the RED phase (on the test just written) and in the GREEN phase (on the production
  code just written). Prevents speculative code, over-engineering, and YAGNI violations
  before they are committed.
---

See the full guide at `docs/tdd/yagni.md`.

Key rules:
- RED: one behaviour per test; no `any()` matchers; no access to fake internals; no unused setup.
- GREEN: every line of production code must be demanded by a currently-failing test. If you cannot point to the test, delete the line.
- Most common violation: adding exception handling (try/catch) before a test proves the exception is thrown.
- REFACTOR: when a prop/param becomes dead, remove it end-to-end through every call site and delete any helper that only existed to compute it — don't leave it "just in case".
