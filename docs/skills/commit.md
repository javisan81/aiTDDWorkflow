---
name: commit
description: >
  Use every time a commit is about to be made. Covers commit format, mandatory ticket scope,
  when to commit separately, pre-commit checks, and the co-author trailer.
recommended_model: gpt-5-mini
---

# Commit Rules

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

## Pre-commit checklist

1. **Format code**
   - Backend: `./gradlew ktlintFormat`
   - Frontend: `npm run lint`
2. **Run all tests** — confirm everything is green, in case the whole test suite has been executed before and since that moment no code change happened you can skip this step. 
   You can run the affected tests in case the number of tests to execute is higher that 1500 and you are in a gradle project. 
   - Backend: `.github/tools/gradle/run-tests.sh <project-directory> test`
   - Frontend: `TZ=UTC npm test` and for frontend also run `npm run type-check`
3. **Verify the application boots** — the Spring context must load without errors.
   If context fails to start, fix it before committing. No exceptions.

## Subagent execution

Run the commit checklist in a dedicated subagent. This is mandatory, including
when the checklist appears small or straightforward. Return only the checklist
result and blocking findings.
