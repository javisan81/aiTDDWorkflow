---
name: green-phase
description: Execute one TDD GREEN cycle as a delegated subagent.
---

# GREEN Phase

Run as a dedicated subagent. This skill performs only the GREEN action selected
by `AGENTS.md`:

1. Write the minimum production code needed to pass the current failing test.
2. Run all existing tests for the affected project.
3. Confirm the suite is green.

Do not add tests, refactor, or implement unrequested behavior. Return only the
production files changed, concise test evidence, and any blocker.
