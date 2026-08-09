---
name: red-phase
description: Execute one TDD RED cycle as a delegated subagent.
---

# RED Phase

Run as a dedicated subagent. This skill performs only the RED action selected
by `AGENTS.md`:

1. Write exactly one failing test for the current behavior.
2. Run the smallest relevant existing test command.
3. Confirm the test fails for the intended reason.

Do not write production code, additional tests, or refactors. Return only the
test file, concise failure evidence, and any blocker.
