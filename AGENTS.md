# Repository Guidelines

> Always respond in English, even if the user writes in another language.

## Instruction authority

This repository-root `AGENTS.md` is the source of truth for work in this
monorepo. More-specific `AGENTS.md` files and project-local instructions may
extend it, but must not contradict it.

Before changing files:

1. Identify the project containing the files.
2. Read the deepest applicable `AGENTS.md` and project-local instructions.
3. Work from that project directory and use its documented commands.

We do TDD as a rule for all the tasks, the only reason to skip the flow is the customer requiring to change it.

## TDD protocol

For new features, follow the TDD cycle mechanically unless the user explicitly
opts out. Do not combine phases or write more than one test at a time.

Use these skills for the detailed checklists and state management:
`/behavior-planning`, `/tdd-outside-in`, `/tdd-state`, `/red-phase`,
`/green-phase`, `/yagni`, `/refactor`, `/hexagonal-arch`, `/commit`, and
`/mutation-testing`.
Update qdrant-rag in the project you are changing files.
Use the semantic-search skill to search for files or info, prefer this approach to anythinge else.

The following are the steps to follow, please pay attention to the Allowed transitions section and TDD violations. 

### PLAN

Use `/behavior-planning` to create or update the Test List, then show the list
and stop for explicit user approval before RED. 
Review the notes and use them in the `/behavior-planning` to create or update the Test List.

### RED

Select the next behavior, use `/red-phase` to write and run exactly one failing
test, show the failure, and **stop for explicit feedback** before production code.

### GREEN

Use `/green-phase` to write the minimum production code and run the applicable
tests. Proceed automatically to REFACTOR when green.

### REFACTOR

Apply one focused refactor using `/refactor`. If the project is backend code,
run `/hexagonal-arch`; if a test was refactored, use `/test-quality`. Preserve
behavior, run the applicable validation, and **stop for feedback** and explicit
approval before committing.

### COMMIT

Use `/commit`, obey its validation-reuse rules, commit the approved behavior,
and then return automatically to PLAN for the next pending behavior. A behavior
is complete only after GREEN, REFACTOR, and COMMIT.

### FINISHED

After all planned behaviors are complete, and all notes are marked as done or are empty, use `/mutation-testing`. Do not run a
full mutation suite when no reliable incremental mechanism exists; record the
reason in `.tdd-state.json` and follow the skill's approval flow.

### TDD violations

Stop and flag immediately if production code is written without a failing test,
phases are combined, a test is added before approval, or multiple GREEN cycles
are committed together.

### Mandatory user-feedback gates

Every instruction in this workflow that says to stop, request feedback, or wait
for explicit approval is an absolute blocking gate. The agent must stop all
further work until the required user response is received. This applies to
plan approval, approval of each concrete RED test before GREEN, refactor
feedback and approval before COMMIT, and any approval required by a skill.

Approvals must never be inferred from earlier approvals, bundled with another
approval, assumed from the user's intent, or bypassed because a change is
small, obvious, or already validated. If the required approval is missing, do
not edit production code, add another test, refactor, commit, or advance the
TDD state.

### Allowed transitions
Use this transtions for each of the previous states. 
Move from one to another once the first has finished or their requirements have been fulfilled, then execute the next one.
*Follow them, they are mandatory*:
- `PLAN -> RED`: user approves the Test List.
- `RED -> GREEN`: user approves the failing test.
- `GREEN -> REFACTOR`: proceed automatically after GREEN.
- `REFACTOR -> COMMIT`: user approves the refactor.
- `COMMIT -> PLAN`: **proceed automatically after the commit, go to plan**.
- `PLAN -> FINISHED`: all planned behaviors are complete and mutation testing
  has finished or has been explicitly skipped according to `/mutation-testing`.

## Shared TDD state

When TDD is active, `.tdd-state.json` is the shared state contract. Always use
`/tdd-state`: read it before TDD actions and update it atomically after phase
transitions. Never infer phase, behavior, approvals, validation, or commit state
from conversation history.

## Sub-agents and phase isolation

Execute single-step reasoning in the main agent context by default. Delegate
only when a skill or an explicit repository rule requires a subagent. Provide
complete context and do not duplicate the delegated investigation.

## Search

Use direct `glob`, `rg`, or file reads for literal lookups. For conceptual or
cross-cutting searches, use `/semantic-search` when Qdrant is available; follow
that skill's sub-project indexing rules.

## Change guardrails

- Preserve REST/OpenAPI contracts and Module Federation boundaries.
- Never commit secrets, credentials, tokens, cookies, payment data, or PII.
- Do not hand-edit generated output.
- Prefer the smallest safe change and preserve dependency direction.
- Add or update tests when behavior changes, using project conventions.
- Do not use `data-testid` for new tests; preserve existing selectors unless the
  task requires otherwise.
- Use ALTO for new React UI where supported; preserve legacy BAgel only when
  compatibility requires it.
- Do not silently swallow errors or add broad catches.
- Do not revert unrelated user changes or use destructive git commands.

## Skills reference

| When you need... | Use skill |
|---|---|
| Plan behaviors and maintain the Test List | `/behavior-planning` |
| Layer progression, TPP, and test explosion detection | `/tdd-outside-in` |
| Maintain and validate `.tdd-state.json` | `/tdd-state` |
| Choose test doubles | `/test-doubles` |
| Kotlin/Spring tests | `/backend-tests` |
| React/Next.js tests | `/frontend-tests` |
| Test fixture and assertion quality | `/test-quality` |
| Execute one RED cycle | `/red-phase` |
| Execute one GREEN cycle | `/green-phase` |
| YAGNI check | `/yagni` |
| Surgical refactoring | `/refactor` |
| Detect anemic use cases | `/anemic-use-case-check` |
| Hexagonal architecture | `/hexagonal-arch` |
| Incremental mutation testing | `/mutation-testing` |
| Conceptual Qdrant search | `/semantic-search` |
| Commit workflow | `/commit` |
| Add project notes | `/notes` |
| Migrate a controller stack | `/migrate-controller-stack` |

Full skill content lives in `docs/skills/` and is exposed through
`.github/skills/`.
