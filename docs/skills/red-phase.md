---
name: red-phase
description: Execute one TDD RED cycle as a delegated subagent.
recommended_model: gpt-5.3-codex
---

# RED Phase

Run as a dedicated subagent. This skill performs only the RED action selected
by `AGENTS.md`:

1. Write exactly one failing test for the current behavior.
2. Run the smallest relevant existing test command.
3. Confirm the test fails for the intended reason.

## Core mocking rule

> **Only mock interfaces you own and control.** If you cannot change the source code, do not mock it.

Use the `/test-doubles` skill for the full boundary reference, the 5 double types,
and guidance on when to use fakes vs mocks.

---

Do not write production code, additional tests, or refactors. Return only the
test file, concise failure evidence, and any blocker.
