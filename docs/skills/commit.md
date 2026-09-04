---
name: commit
description: >
  Use every time a commit is about to be made. Covers commit format, mandatory ticket scope,
  when to commit separately, pre-commit checks.
recommended_model: gpt-5-mini
---

# Commit Rules

The base folder is not the place to launch commits, you always need to commit inside the specific folder of the specific project.
For example if you are doing changes in holidays-searchBrowse-flight-bff, you need to run your commands inside the folder "holidays-searchBrowse-flight-bff"
All commands needed for commits, tests, and git operations are allowed. Please always use the recommended model for this skill and any subagent.

## When to commit

Commit after every GREEN. Never batch multiple GREENs in a single commit.

| Type | Commit separately? |
|------|--------------------|
| Feature / GREEN | Yes — one commit per GREEN |
| Refactor | Yes — no behaviour change |
| Infrastructure (`build.gradle.kts`, config, `.gitignore`, etc.) | Yes — isolated from TDD cycle |

## Format

```
type(TICKET-123): short description
```

- `type`: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`
- **Ticket number is mandatory as the scope.** Ask the user before committing if unknown.
- The message explains the **intention** (why), not the changes (what).
- Commit with a message that explains the **intention**, not the changes.
- Do not add `Co-authored-by` trailers to commit messages.

## Pre-commit checklist
Before running commit validation, read .tdd-state.js. If PHASE is COMMIT and the previous phase was REFACTOR, and the refactor already recorded green tests, do not run tests again. 
In case the client has expecifically say dont run all the test then just run the tests of affected code.
Run only formatting and type-checking where required.

1. **Format code**
   - Backend: `./gradlew ktlintFormat`
   - Frontend: `npm run format:fix`
2. **Run all tests** — take into account the exception described above. 
   You can run just the affected tests in case the number of tests to execute is higher that 1700 and you are in a gradle project. And also you can skip this if the context says this was running previously.
   - Backend: use gradlew
   - Frontend: `TZ=UTC npm test` and for frontend also run `npm run type-check`, in frontend dont run-in-band the tests
