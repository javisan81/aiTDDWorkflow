---
name: migrate-controller-stack
description: Migrates a controller, its complete lower-layer stack, and all full-stack test suites from one service/BFF to another, purging unused code.
recommended_model: gpt-5.6-luna
---

# Skill: Migrate Controller & Full Stack

## Context & Role
Act as an expert software engineer performing a full-stack code migration across microservices or BFF architectures.

---

## IMPORTANT OVERRIDE: TDD Bypass
Ignore any TDD (Test-Driven Development) rules from `AGENTS.md` or local guidelines. For this task, do NOT follow TDD. You are allowed to write or migrate all production code, refactor dependencies, and migrate/update tests all in a single batch execution ("all in one go"). This override applies strictly to this migration task.

---

## Inputs / Parameters
When invoking this skill, declare these variables:
- **`$SOURCE_SERVICE`**: Source repository/module name (e.g., `searchbrowse-bff`)
- **`$DEST_SERVICE`**: Destination repository/module name (e.g., `flight-bff`)
- **`$CONTROLLER_NAME`**: Name of the controller class (e.g., `CabinUpgradesController`)

---

## Task Overview
Migrate `$CONTROLLER_NAME` and its ENTIRE underlying stack from `$SOURCE_SERVICE` to `$DEST_SERVICE`. 

We will execute this in two distinct phases:
1. **Phase 1 (Current Task):** Make all endpoints function correctly in `$DEST_SERVICE` with full test parity.
2. **Phase 2 (Subsequent Task):** Remove the migrated code from `$SOURCE_SERVICE` once Phase 1 is verified.

---

## Requirements

### 1. PRODUCTION CODE MIGRATION (FULL STACK)
- Identify `$CONTROLLER_NAME` in `$SOURCE_SERVICE` and trace down its full execution tree.
- Copy and adapt ALL associated layers to `$DEST_SERVICE`: Controller, Services, Repositories, API Clients, Mappers, Helpers, and DTOs/Models.
- Ensure `$DEST_SERVICE` exposes and serves all endpoints formerly handled by `$CONTROLLER_NAME`.
- **PURGE UNUSED CODE:** In the migrated classes across all layers, remove any methods, fields, or endpoints that are NOT strictly used by `$CONTROLLER_NAME` in production.

### 2. FULL STACK TEST SUITE MIGRATION (CRITICAL)
- Do NOT migrate only the controller tests. You MUST migrate ALL unit, integration, and target tests for EVERY class in the stack underneath `$CONTROLLER_NAME` (services, mappers, clients, helpers, etc.) from `$SOURCE_SERVICE` to `$DEST_SERVICE`.
- Ensure tests covering lower-level classes are trimmed to ONLY assert functionality relevant to `$CONTROLLER_NAME`.
- Delete test cases for any methods or code paths that were purged during cleanup.

---

## Definition of Done (Phase 1)
- `$DEST_SERVICE` compiles without errors.
- All migrated endpoints function identically in `$DEST_SERVICE`.
- The COMPLETE test suite across the entire migrated stack passes in `$DEST_SERVICE` with equivalent or better coverage compared to `$SOURCE_SERVICE`.

---

## Execution Instructions
- Execute all file creations, refactors, dead code removal, and multi-layer test migrations in a single step—no red-green-refactor cycles required.
- Trace and list all layers, classes, and test files associated with `$CONTROLLER_NAME` across the entire stack, then execute the full migration and cleanup directly into `$DEST_SERVICE`.

### Example of Usage
Apply skill migrate-controller-stack with SOURCE_SERVICE=searchbrowse-bff DEST_SERVICE=flight-bff CONTROLLER_NAME=CabinUpgradesController
## Subagent execution

Run this migration skill in a dedicated subagent. This is mandatory, including
when the migration scope appears small or straightforward. Return only
completed moves, remaining blockers, and concise verification results. If
Gradle tests are required, use `/gradle-tests`.