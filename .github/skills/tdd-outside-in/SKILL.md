---
name: tdd-outside-in
description: >
  Use when starting a new feature, writing the first test, deciding which layer to test first,
  or doing TDD in a layered architecture. Explains the double loop, vertical slicing,
  walking skeleton, layer progression, TPP, and test explosion warning.
---

See the full guide at `docs/tdd/outside-in.md`.

Key rules:
- Work in **vertical slices**: one use case at a time, all layers, fully tested before moving on.
- Build a **walking skeleton** first: the thinnest possible slice that crosses all layers end-to-end.
- Start from the outermost layer (entry point). Only move inward when the current layer demands it.
- Complete the full vertical slice (controller → use case → adapter) before starting the next use case.
- Apply TPP: return a constant before writing a conditional.
- Warn immediately if a test explosion pattern is detected.
- For layer-specific patterns: use `/backend-tests` or `/frontend-tests`.
