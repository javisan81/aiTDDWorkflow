---
name: tdd-state
description: Maintain and validate the shared TDD state across every phase.
---

# TDD state management

Read `.tdd-state.json` before every TDD action and update it after every phase
transition. Never infer state from conversation history.

## Required fields

- `task`: ticket, project, and start time
- `phase`: `PLAN`, `RED`, `GREEN`, `REFACTOR`, `COMMIT`, or `FINISHED`
- `previous_phase`, `previous_behavior`, and `last_transition_reason`
- `cycle`, `current_behavior`, and `next_allowed_action`
- `test_list`, with behavior, status, and commit for each entry
- `approvals`: plan, red test, refactor, and commit
- `validation`: tests, type-check, format, command, and completion time
- `changes`: all files, production files, and test files
- `commit`: status, hash, and message
- `blockers`, `last_updated_at`, `projectsModified`, and `decisions`

## Update rules

- `current_behavior` must be exactly one behavior from `test_list`.
- Update `previous_phase`, `previous_behavior`, and
  `last_transition_reason` atomically with every phase transition.
- Record validation as `not_run`, `running`, `green`, or `red`.
- Record approval explicitly; never infer it from a general user message.
- A behavior is `done` only after GREEN and REFACTOR validation succeed.
- Record every changed file and every project modified by the feature.
- Record the commit hash only after the commit completes.

## Phase checklist

Before acting:

1. Read `.tdd-state.json`.
2. Confirm the current phase and behavior.
3. Confirm the required approval and `next_allowed_action`.

After acting:

1. Record the phase result and validation.
2. Record changed files and decisions.
3. Set the next phase, behavior, and allowed action.
4. Update `.tdd-state.json` atomically.
