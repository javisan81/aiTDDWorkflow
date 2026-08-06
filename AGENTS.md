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
3. Compact context use /compact in github copilot or the equivalent in the current agentic tool 
5. **STOP. Ask: "Shall we move to the next test?"**
6. Do not write the next test until the user explicitly approves.



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
| Migrage controllers from one bff to another, this is allowed to not do tdd | `/migrate-controller-stack ` |


Full content lives in `docs/skills/`.

---

## Semantic Code Search (qdrant-rag), just in case qdrant-rag is configured as a mcp

The workspace is indexed in Qdrant for semantic search. Each sub-project has its own collection (the tool auto-generates collection names from path hashes).

**Rules:**
- Always use the `qdrant-rag` MCP tool for code search when available — prefer it over `grep` for conceptual/semantic queries.
- **At the start of every working session**, run `reindex_changes` on the collection(s) for the sub-project(s) you are about to work on. This is fast and ensures the index reflects the latest code.
- **Never** index from the repo root (`/Users/javierlopezfernandez/IdeaProjects/bah`) — the root `.gitignore` uses `*` and blocks everything. Always index sub-projects individually.
- Only run a full `index_codebase` (with `forceReindex: true`) when a sub-project has never been indexed or its collection has been deleted. For all other cases, use `reindex_changes`.
- Ignore patterns must match `.ragignore` (see root `.ragignore`). Pass them via `ignorePatterns` on every `index_codebase` call.

**Active collections (as of last reindex):**

| Sub-project | Collection |
|---|---|
| `searchBrowseBff` | `code_2890ade2` |
| `holidays-manageTrip-service` | `code_c1ed0005` |
| `holidays-manageTrip-presentation` | `code_8cf8edf0` |
| `holidays-searchBrowse-presentation` | `code_b7836da0` |
| `holidays-searchBrowse-presentationprovider` | `code_2995f24f` |
| `holidays-searchBrowse-flight-bff` | `code_0564df04` |
| `holidays-platform-infra` | `code_37d18fe6` |
| `flight-orders-adapter-service` | `code_b3164bd8` |
| `payments-payments-orchestrator` | `code_bedc9270` |
| `holidays-designSystems-componentlibrary` | `code_3c091510` |
| `monitoring-datadog-ba-holidays` | `code_cbe3c1ab` |
| `mars-rover` | `code_a8cafd45` |

> **Note:** The `qdrant-rag` tool does not support custom collection names — names are derived from path hashes and cannot be changed. When searching, target the collection for the relevant sub-project. When in doubt, search across all active collections listed above.
