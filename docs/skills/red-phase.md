---
name: red-phase
description: Execute one TDD RED cycle.
---

# RED Phase

This skill performs only the RED action selected by `AGENTS.md`, **run it in the main agent**, **all steps are mandatory, dont skip any step**:

0. Based on the behavior tests to implement select the layer based on the skill /tdd-outside-in, try to find the closer project to the customer with the higher layout. Perhaps multiple tests need to be done, based on this, update the list of tests with this info.
1. Write exactly one failing test for the current behavior. Use `/backend-tests` or `/frontend-tests` skills to have the guidelines about what tests to write.
2. Mock if required using the `/test-doubles` skill
3. Run the smallest relevant existing test command, this means run the tests in the file you updated the red test.
4. Confirm the test fails for the intended reason, run all tests in that file.
5. run `/test-quality` to understand if the test is good enough. This step and previous one can be executed in parallel. If there are things that does not match, then fix them.
6. show the diff of the current change in tests to the customer, in the cli console with git diff and the files changed

## Core mocking rule

> **Only mock interfaces you own and control.** If you cannot change the source code, do not mock it.

Use the `/test-doubles` skill for the full boundary reference, the 5 double types,
and guidance on when to use fakes vs mocks.

---

Do not write production code, additional tests, or refactors. Return only the
test file, concise failure evidence, any blocker and the diff to be shown.
