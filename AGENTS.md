# TDD Guidelines (all projects)

> **Always respond in English, even if the user writes in Spanish.**

---

## AGENTS.md Hierarchy

This is the **root AGENTS.md** — the single source of truth for all projects in this monorepo.
Each sub-project may have its own `AGENTS.md` with project-specific guidance (tech stack, commands, conventions).

**Rules:**
- Always read the sub-project `AGENTS.md` alongside this one when working in a sub-directory.
- The sub-project `AGENTS.md` extends this one — it adds context, it does not replace it.
- If there is any conflict between a sub-project `AGENTS.md` and this file, **this file prevails**.

---

## TDD Protocol — Follow this mechanically, no exceptions

Each step below ends your response. Do not combine steps. Do not anticipate the next step.
Write **just one test** — never more.

Use the `/tdd-outside-in` skill for layer progression, TPP, and test explosion detection.

### Step 0 — PLAN (Once per task, and updated each cycle)
1. Run `/behavior-planning` skill to create the initial Test List.
2. **STOP. Ask for approval on the list before starting RED.**
3. Re-run `/behavior-planning` at the start of each RED phase to adapt the list.

### Step 1 — RED
1. Run `/behavior-planning` to pick the next target behavior from the Test List.
2. Ask the user about expected test quality (if not already established for this session)
3. Write **one** failing test. Run it. Confirm it fails.
4. Run `/yagni` checklist on the test before showing it to the user.
5. **STOP. Show the failing output. Ask: "Feedback before writing code?"**
6. Do not write any production code until the user explicitly approves.

### Step 2 — GREEN
1. Write the **minimum** code to make the test pass. Run all tests. Confirm green.
2. Run `/yagni` checklist on the production code just written before showing it to the user.
3. **STOP. Show the green output. Ask: "Feedback before refactoring?"**
4. Do not refactor until the user explicitly approves.
5. Mock if required using the /test-doubles skill

### Step 3 — REFACTOR
1. Look for code smells. Apply one refactor. Run all tests. Confirm still green.
   - Use comments to guide renaming, extraction, deduplication — then remove the comments.
   - If there is duplicated code, extract to a method with a parameter. Remove the comments.
2. Run `/hexagonal-arch` checklist: verify folder structure, no framework imports in domain, port naming.
3. run /anemic-usecase skill to check if we have anemic usecase and then remove the usecase
4. **STOP. Ask: "Feedback? Shall we commit?"**
5. Do not commit until the user explicitly approves.

### Step 4 — COMMIT
1. Run `/commit` skill — follow every step in the pre-commit checklist.
2. Commit with a message that explains the **intention**, not the changes.
3. **STOP. Ask: "Shall we move to the next test?"**
4. Do not write the next test until the user explicitly approves.

### Violations — stop and flag immediately
- Writing production code without a failing test → YAGNI violation
- Writing test N+1 before the user approved moving on → skipped feedback
- Committing multiple GREENs together → broken narrative
- Combining RED+GREEN in one response → forbidden
- Combining GREEN+REFACTOR in one response → forbidden
- Writing more than one test → forbidden

---

## Core mocking rule

> **Only mock interfaces you own and control.** If you cannot change the source code, do not mock it.

Use the `/test-doubles` skill for the full boundary reference, the 5 double types,
and guidance on when to use fakes vs mocks.

---

## Commits

See `/commit` skill (`docs/tdd/commit.md`) for the full rules.
The short version: one commit per GREEN, ticket number mandatory, intention-based message.

---

## Sub-agents / background tasks

Do the work yourself in the main agent, in the foreground, by default.

Only delegate to a sub-agent (background or otherwise) when there is genuine
parallel work: the main agent keeps doing something else itself while the
sub-agent runs. If the main agent has nothing else to do in the meantime,
do not delegate — just do the task directly and show the work as you go.

---

## Skills reference

| When you need… | Use skill |
|---|---|
| Layer progression, TPP, test explosion warning | `/tdd-outside-in` |
| Fake vs mock, unit vs integration, double types | `/test-doubles` |
| ANY_ prefix, fixtures, full JSON contract | `/test-quality` |
| Hexagonal design, ports, folder structure | `/hexagonal-arch` |
| Kotlin/Spring: controller, use-case, adapter tests | `/backend-tests` |
| React/Next.js: page, component, hook tests | `/frontend-tests` |
| YAGNI check on test (RED) or production code (GREEN) | `/yagni` |
| Detect and remove proxy use cases in REFACTOR | `/anemic-usecase` |
| Committing (format, ticket, boot check, trailer) | `/commit` |
| Plan next tests to implement | `/behavior-plannings` |


Full content lives in `docs/tdd/`.
