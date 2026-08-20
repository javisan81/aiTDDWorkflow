---
name: red-phase
description: Execute one TDD RED cycle.
---

# RED Phase

This skill performs only the RED action selected by `AGENTS.md`:

1. Write exactly one failing test for the current behavior.
2. Mock if required using the `/test-doubles` skill
3. Run the smallest relevant existing test command, this means run the tests in the file you updated the red test.
4. Confirm the test fails for the intended reason.
5. run `/test-quality` to understand if the test is good enough. This step and previous one can be executed in parallel.
6. show the diff of the current change in tests to the customer with git diff

## Core mocking rule

> **Only mock interfaces you own and control.** If you cannot change the source code, do not mock it.

Use the `/test-doubles` skill for the full boundary reference, the 5 double types,
and guidance on when to use fakes vs mocks.

---

Do not write production code, additional tests, or refactors. Return only the
test file, concise failure evidence, and any blocker.
