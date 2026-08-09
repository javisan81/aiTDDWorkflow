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

## TDD Protocol — Follow this mechanically, no exceptions for new features

Each step below ends your response. Do not combine steps. Do not anticipate the next step.
Write **just one test** — never more.

If the user talks about doing a refactor and we are green (all tests passes) we can go to refactor stage directly and continue the cycle in that step.

Use the `/behavior-planning` skill to maintain the Test List, and `/tdd-outside-in` for layer progression, TPP, and test explosion detection.

### Step 0 — PLAN (Once per task, and updated each cycle)
1. Check for an existing `.tdd-state.json` at the root/sub-project. If present, read it to restore current session state.
2. Run `/behavior-planning` skill to create or update the Test List.
3. **STOP. Ask for approval on the list before starting RED.**
4. Re-run `/behavior-planning` at the start of each RED phase to adapt the list.

### Step 1 — RED
1. Run `/behavior-planning` to pick the next target behavior from the Test List.
2. Ask the user about expected test quality (if not already established for this session)
3. Run `/red-phase` in a dedicated subagent to write **one** failing test, run it, and confirm it fails.
4. Run `/yagni` checklist on the test before showing it to the user.
5. run `/test-quality` to understand if the test is good enough.
6. **STOP. Show the failing output. Ask: "Feedback before writing code?"**
7. Do not write any production code until the user explicitly approves.

### Step 2 — GREEN
1. Run `/green-phase` in a dedicated subagent to write the **minimum** code to make the test pass, run all tests, and confirm green.
2. Run `/yagni` checklist on the production code just written before showing it to the user, to be sure your code is the minimum one to make the test to pass.
3. **STOP. Show the green output. Ask: "Feedback before refactoring?"**
4. Do not refactor until the user explicitly approves.
5. Mock if required using the /test-doubles skill

### Step 3 — REFACTOR
1. Look for code smells. Apply one refactor. Run all tests. Confirm still green.
   - Use comments to guide renaming, extraction, deduplication — then remove the comments.
   - If there is duplicated code, extract to a method with a parameter. Remove the comments.
2. Run `/hexagonal-arch` checklist: verify folder structure, no framework imports in domain, port naming.
3. run `/anemic-usecase` skill to check if we have anemic usecase and then remove the usecase
4. **STOP. Ask: "Feedback? Shall we commit?"**
5. Do not commit until the user explicitly approves.

### Step 4 — COMMIT
1. Run `/commit` skill — follow every step in the pre-commit checklist.
2. Commit with a message that explains the **intention**, not the changes.
3. Update `.tdd-state.json` with the current behavior marked as `DONE` and set `commit_compaction_status` to `pending`.
4. **Hard gate: compact the context** using `/compact` in GitHub Copilot or the equivalent available capability.
   - If compaction is available, execute it before continuing.
   - If compaction is unavailable, explicitly ask the user to compact the context and stop. The COMMIT phase is not complete until this happens.
   - Do not ask to move to the next test, write more code, or present the task as complete before this gate is satisfied.
5. **STOP. Ask: "Shall we move to the next test?"**
6. Do not write the next test until the user explicitly approves.



### Violations — stop and flag immediately
- Writing production code without a failing test → YAGNI violation
- Writing test N+1 before the user approved moving on → skipped feedback
- Committing multiple GREENs together → broken narrative
- Combining RED+GREEN in one response → forbidden
- Combining GREEN+REFACTOR in one response → forbidden
- Writing more than one test → forbidden


### Mandatory TDD Phase State

At all times, maintain and state these values internally, and mirror them in `.tdd-state.json` at the root:

- `PHASE`: PLAN | RED | GREEN | REFACTOR | COMMIT
- `CURRENT_BEHAVIOR`: exactly one behavior from the Test List
- `NEXT_ALLOWED_ACTION`: the only action permitted by the current phase

Every response involving code work must begin its tool-use reasoning by checking:
0. **Reading `.tdd-state.json`** (if starting a session or after context compaction)
1. Current phase
2. Current behavior
3. Required approval or transition

Allowed transitions:

PLAN -> RED: user approves the Test List
RED -> GREEN: user approves the failing test
GREEN -> REFACTOR: user approves the passing implementation
REFACTOR -> COMMIT: user approves the refactor
COMMIT -> RED: user approves moving to the next behavior

Never skip a transition, combine phases, or start another test before COMMIT.
After each phase, stop and request the required approval.

Before every response, update both internal state and `.tdd-state.json`:
- Phase
- Current behavior
- Test List status
- User approval status
- Commit compaction status (`pending`, `completed`, or `user_action_required`)

## Sub-agents & Phase Isolation

By default, execute single-step reasoning in the main agent context.

However, **you MUST delegate to a dedicated subagent** if you use a skill that says to be executed in a subagent or if there is an explicit rule to do it.
Subagents must operate with clean, minimal context and return only the required output or failure diagnostics to the main agent.

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
| Execute one RED cycle in a subagent | `/red-phase` |
| Execute one GREEN cycle in a subagent | `/green-phase` |
| Detect and remove proxy use cases in REFACTOR | `/anemic-usecase` |
| Running Gradle tests with compact agent-oriented diagnostics | `/gradle-tests` |
| Committing (format, ticket, boot check, trailer) | `/commit` |
| Plan next tests to implement | `/behavior-plannings` |
| Migrage controllers from one bff to another, this is allowed to not do tdd | `/migrate-controller-stack ` |


Full content lives in `docs/skills/`.

## Agent test execution

When an agent needs to run tests in any Gradle project, it must use the
`/gradle-tests` skill instead of invoking `./gradlew` directly. From the
repository root, run:

```bash
.github/tools/gradle/run-tests.sh <project-directory>
```

Use the `check` task when the project instructions define it as the complete
verification task:

```bash
.github/tools/gradle/run-tests.sh <project-directory> check
```

The command is optimized for agent token usage: stdout contains only a compact
summary and actionable failure lines. Full Gradle output is saved to
`<project-directory>/build/gradle-test-report/gradle.log`, and structured
test diagnostics are saved to
`<project-directory>/build/gradle-test-report/test-results.json`.

Only use `--verbose` when detailed Gradle output is specifically required.

---

## Semantic Code Search (qdrant-rag), just in case qdrant-rag is configured as a mcp

The workspace is indexed in Qdrant for semantic search. Target the active sub-project collection automatically based on the working directory path hash.

**Rules:**
- Always use the `qdrant-rag` MCP tool for code search when available — prefer it over `grep` for conceptual/semantic queries.
- **At the start of every working session**, run `reindex_changes` on the collection for the sub-project you are about to work on. This is fast and ensures the index reflects the latest code.
- **Never** index from the repo root — the root `.gitignore` uses `*` and blocks everything. Always index sub-projects individually.
- Only run a full `index_codebase` (with `forceReindex: true`) when a sub-project has never been indexed or its collection has been deleted. For all other cases, use `reindex_changes`.
- Ignore patterns must match `.ragignore` (see root `.ragignore`). Pass them via `ignorePatterns` on every `index_codebase` call.