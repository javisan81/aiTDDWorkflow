---
name: anemic-usecase
description: >
  Run in the REFACTOR phase on any use case just written or touched. Detects use cases
  that are pure proxies to a repository or another service and eliminates them by moving
  the call to the controller or the appropriate adapter.
---

See the full guide at `docs/tdd/anemic-usecase.md`.

Key rules:
- A use case that only calls `repository.find()` and returns the result is anemic — delete it.
- A use case that only calls `repository.save(x)` and returns `x` is anemic — delete it.
- When a use case is deleted, the controller calls the output port (repository) directly.
- A use case is NOT anemic if it: enforces a domain rule, maps between types, coordinates multiple ports, or throws a domain exception based on business logic.
