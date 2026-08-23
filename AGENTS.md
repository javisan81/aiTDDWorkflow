# TDD Guidelines (all projects)

> **Always respond in English, even if the user writes in Spanish.**

---

## Instruction Authority

This repository-root `AGENTS.md` is the **sole source of truth** for all work in
this monorepo.

Other `AGENTS.md` files, `.github/copilot-instructions.md` files, and custom
agent definitions may extend this guidance with project-specific details, but
must not override or replace it. If they conflict with this file, follow this
file.

If you need to work in a project/subproject change dir to that project and run all commands under that folder.
---

## TDD Protocol — Follow this mechanically, no exceptions for new features

Do not combine steps. Do not anticipate the next step.
Write **just one test** — never more.

If the user talks about doing a refactor and we are green (all tests passes) we can go to refactor stage directly and continue the cycle in that step.
If the user explicitely says not using TDD then you can skip these steps, and follow their approach.

Use the `/behavior-planning` skill to maintain the Test List, and `/tdd-outside-in` for layer progression, TPP, and test explosion detection.

### Step 0 — PLAN (Once per task, and updated each cycle)
1. Check for an existing `.tdd-state.json` at the root/sub-project. If present, read it to restore current session state.
2. Run `/behavior-planning` skill to create or update the Test List.
3. Paint the list of tests planned by the previous step.
4. **STOP. Ask for approval on the list before starting RED.**

### Step 1 — RED
1. Pick the next target behavior from the Test List.
2. Ask the user about expected test quality (if not already established for this session)
3. Run `/red-phase` to write **one** failing test, run it, and confirm it fails. 
4. **STOP. Show the failing output. Ask: "Feedback before writing code?"**
5. Do not write any production code until the user explicitly approves.

### Step 2 — GREEN
1. Run `/green-phase` to write the **minimum** code to make the test pass, run all tests, and confirm green.
2. Save in the context that we are green and all tests passes, go to refactor phase.

### Step 3 — REFACTOR
1. Look for code smells. Apply one refactor. Run all tests to confirm we are green, but skip this run if we come from green-phase and all tests passes (check the .tdd-state.json file).
   - Use comments to guide renaming, extraction, deduplication — then remove the comments.
   - If there is duplicated code, extract to a method with a parameter. Remove the comments.
   - If all tests passes mark the time when they passes in the .tdd-state.json file to make the commit step to skip the execution of all tests.
3. Run `/hexagonal-arch` checklist: verify folder structure, no framework imports in domain, port naming. Just for backend projects.
4. **STOP. Ask: "Feedback? Shall we commit?"**
5. Do not commit until the user explicitly approves.
6. Save in the context that we are green and all tests passes and the time they passes.


### Step 4 — COMMIT
1. Run `/commit` skill — follow every step in the pre-commit checklist, you can skip tests if the context says we are green.
2. Commit with a message that explains the **intention**, not the changes.
3. Update `.tdd-state.json` with the current behavior marked as `DONE`.
4. Go to step PLAN again to follow the next test to implement. Because this is not the end of the ticket, it is the end when there are no more behaviours to add.

### Step 5 — mutation testing (end of the feature)
1. This step only happens when the list of behaviors is completed.
2. Execute mutation testing only when the project provides a reliable incremental changed-code
   mechanism. For PIT projects, first verify that the Git changes plugin is configured and that
   the `git-changes` feature is available, then run for example:
   `./gradlew pitest -Dfeatures="+git-changes(target[origin/main])"`.
3. If incremental mutation testing is unavailable or unreliable, skip Step 5 and record the
   reason in `.tdd-state.json`. Do not fall back to the full mutation-testing suite.
4. Give a list of mutants and the tests that could kill the mutants.
5. **STOP. Ask: "Which mutants should we kill and how?"**
6. Create the tests to kill the mutants.
7. **STOP. Ask: "Feedback? Shall we commit?"**
8. Do not commit until the user explicitly approves.
9. The ticket finishes, we can remove `.tdd-state.json`.


### Violations — stop and flag immediately
- Writing production code without a failing test → YAGNI violation
- Writing test N+1 before the user approved moving on → skipped feedback
- Committing multiple GREENs together → broken narrative
- Combining RED+GREEN in one response → forbidden
- Combining GREEN+REFACTOR in one response → forbidden
- Writing more than one test → forbidden


### Mandatory TDD Phase State

At all times, maintain and state these values internally, and mirror them in `.tdd-state.json` at the root:

- `PHASE`: PLAN | RED | GREEN | REFACTOR | COMMIT | FINISHED (mutation testing)
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
GREEN -> REFACTOR: **do it automatically, dont ask the user**.
REFACTOR -> COMMIT: user approves the refactor
COMMIT -> PLAN: **do it automatically, dont ask the use**

Never skip a transition, combine phases, or start another test before COMMIT.

Before every response, update both internal state and `.tdd-state.json`:
- Phase
- Current behavior
- Test List status
- User approval status
- Commit compaction status (`pending`, `completed`, or `user_action_required`)

### Required `.tdd-state.json` contract

The root `.tdd-state.json` is the shared state contract between the main agent,
TDD skills, and delegated agents. It must be updated before and after every
phase transition. Use this structure:

```json
{
  "task": {
    "ticket": "DWNINVS-304",
    "project": "project-directory",
    "started_at": "2026-01-01T00:00:00Z"
  },
  "phase": "PLAN",
  "previous_phase": null,
  "previous_behavior": null,
  "last_transition_reason": "Task started",
  "cycle": 1,
  "current_behavior": "One behavior from the test list",
  "next_allowed_action": "Await user approval of the behavior list",
  "test_list": [
    {
      "behavior": "A domain-level behavior",
      "status": "pending",
      "commit": null
    }
  ],
  "approvals": {
    "plan": "pending",
    "red_test": "pending",
    "refactor": "pending",
    "commit": "pending"
  },
  "validation": {
    "tests_status": "not_run",
    "tests_command": null,
    "tests_completed_at": null,
    "type_check_status": "not_run",
    "format_status": "not_run"
  },
  "changes": {
    "files": [],
    "production_files": [],
    "test_files": []
  },
  "commit": {
    "status": "pending",
    "hash": null,
    "message": null
  },
  "blockers": [],
  "last_updated_at": "2026-01-01T00:00:00Z"
}
```

Field values must follow these rules:
- `phase` is uppercase: `PLAN`, `RED`, `GREEN`, `REFACTOR`, `COMMIT`, or `FINISHED`.
- `previous_phase` records the phase immediately before `phase`; it is `null`
  only when the task starts.
- `previous_behavior` records the behavior active in `previous_phase`, or
  `null` when there is no previous phase.
- `last_transition_reason` briefly records why the phase changed, such as
  `Plan approved`, `Failing test approved`, or `Commit completed`.
- `current_behavior` contains exactly one behavior from `test_list`.
- `next_allowed_action` describes the only permitted next action.
- `approvals` records the user decision for each transition; never infer approval
  from a general message when the phase requires explicit approval.
- `validation.tests_status` is `not_run`, `running`, `green`, or `red`.
- `validation.type_check_status` and `validation.format_status` are
  `not_run`, `green`, or `red`.
- A behavior is marked `done` only after its GREEN and REFACTOR validation
  succeeds. Its commit hash is recorded after COMMIT.
- `commit_compaction_status` is `pending`, `completed`, or
  `user_action_required`.

### Validation reuse gate

Before running commit validation, read `.tdd-state.json`:
- If `phase` is `COMMIT`, `previous_phase` is `REFACTOR`, and
  `validation.tests_status` is `green` with a non-null
  `validation.tests_completed_at`, do **not** run the test suite again.
- In that case, run only the required formatting and type-check commands, unless
  code changed after the recorded validation or the user explicitly requests a
  fresh test run.
- Delegated commit-checklist agents must receive and obey this same gate. The
  main agent must state whether tests are `SKIP` or `RUN` before delegating.

Every phase transition must update `previous_phase`, `previous_behavior`, and
`last_transition_reason` atomically with `phase`, `current_behavior`, and
`next_allowed_action`. Skills must use these fields instead of inferring the
origin phase from chat history.

## Sub-agents & Phase Isolation

By default, execute single-step reasoning in the main agent context.

However, **you MUST delegate to a dedicated subagent** if you use a skill that says to be executed in a subagent or if there is an explicit rule to do it in the main AGENTS.md.
Subagents must operate with clean, minimal context and return only the required output or failure diagnostics to the main agent (no stopping step). Main agent can continue with the flow.

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
| Execute one RED cycle always in the main agent, no subagents | `/red-phase` |
| Execute one GREEN cycle always in the main agent, no subagents | `/green-phase` |
| Detect and remove proxy use cases in REFACTOR | `/anemic-usecase-check` |
| Committing (format, ticket, boot check, trailer) | `/commit` |
| Plan next tests to implement | `/behavior-planning` |
| Migrage controllers from one bff to another, this is allowed to not do tdd | `/migrate-controller-stack ` |


Full content lives in `docs/skills/`.     


## Semantic Code Search (qdrant-rag), just in case qdrant-rag is configured as a mcp

The workspace is indexed in Qdrant for semantic search, directories under bah, not bah base folder. Target the active sub-project collection automatically based on the working directory path hash.

**Rules:**
- Always use the `qdrant-rag` MCP tool for code search when available — prefer it over `grep` for conceptual/semantic queries.
- **At the start of every working session**, run `reindex_changes` on the collection for the sub-project you are about to work on, indentify first the subfolder to upgrade, not the base one. This is fast and ensures the index reflects the latest code.
- **Never** index from the repo root — the root `.gitignore` uses `*` and blocks everything. Always index sub-projects individually.
- Only run a full `index_codebase` (with `forceReindex: true`) when a sub-project has never been indexed or its collection has been deleted. For all other cases, use `reindex_changes`.
- Ignore patterns must match `.ragignore` (see root `.ragignore`). Pass them via `ignorePatterns` on every `index_codebase` call.