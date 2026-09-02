---
name: mutation-testing
description: Run incremental mutation testing after all planned behaviors are complete.
---

# Mutation testing

Use this skill only after the behavior list is complete.

1. Read `.tdd-state.json` and identify the projects modified by the feature.
2. Run mutation testing separately for each applicable project.
3. Prefer PIT history-based incremental execution when configured. Use
   `build/reports/pitest-history.txt` for both history input and output, and
   preserve the project's CI cache behavior.
4. Use the `git-changes` feature only when it is explicitly configured.
5. If no reliable incremental mechanism exists, skip the suite and record the
   reason in `.tdd-state.json`. Do not fall back to a full mutation suite.
6. Report surviving mutants and the tests that could kill them.
7. Ask which mutants to address before writing tests.

