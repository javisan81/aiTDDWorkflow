---
name: green-phase
description: Execute one TDD GREEN cycle.
---

# GREEN Phase

This skill performs only the GREEN action selected by `AGENTS.md`, run it in the main agent:

1. Write the minimum production code needed to pass the current failing test.
2. Run all existing tests for the affected project.
3. Confirm the suite is green.
4. Run `/yagni` checklist on the production code just written before showing it to the user, to be sure your code is the minimum one to make the test to pass. YAGNI can be run in parallel with previous step.
5. Show the diff of the current production code to the customer

Do not add tests, refactor, or implement unrequested behavior. Return only the
production files changed, concise test evidence, and any blocker.
