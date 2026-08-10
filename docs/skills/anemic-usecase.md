---
name: anemic-use-case-check
description: Checklist to identify and refactor anemic use cases in the architecture.
recommended_model: gpt-5.4-mini
---

# Anemic Use Case Check

Run this checklist in the **REFACTOR phase** on every use case you write or touch.

---

## The question

> *"If I delete this use case, does any domain logic disappear?"*

If the answer is **no** → the use case is anemic. Delete it.

---

## Checklist

Ask these questions about the use case under review:

- Does it do nothing but call `repository.find()` and return the result? → **Anemic. Delete.**
- Does it do nothing but call `repository.save(x)` and return `x`? → **Anemic. Delete.**
- Does it delegate entirely to one other service/port with no logic of its own? → **Anemic. Delete.**
- Does it enforce a domain rule (e.g. throw an exception based on state)? → **Not anemic. Keep.**
- Does it coordinate two or more ports? → **Not anemic. Keep.**
- Does it map or transform a domain object? → **Not anemic. Keep.**

---

## What to do when a use case is anemic

Move the call directly to the **controller** (input adapter):

```kotlin
// Instead of:
class GetRoverPositionUseCase(private val repo: RoverRepository) : GetRoverPosition {
    override fun execute() = repo.find() ?: throw RoverNotDeployedException()
}

// Do this in the controller:
@GetMapping
fun get(): RoverPosition = roverRepository.find() ?: throw RoverNotDeployedException()
```

The controller may depend on an **output port** (repository interface) directly — it still depends on an abstraction, not a concrete class.

---

## What stays in a use case

| Has domain logic? | Coordinates ports? | Maps types? | Verdict |
|---|---|---|---|
| ✅ | — | — | Keep |
| — | ✅ | — | Keep |
| — | — | ✅ | Keep |
| ❌ | ❌ | ❌ | **Delete** |

---

## Real example from this project

`GetRoverPositionUseCase` was deleted because it was:
```kotlin
override fun execute() = roverRepository.find() ?: throw RoverNotDeployedException()
```
One line. No domain logic beyond what the controller can express directly.
`GetRoverPositionController` now injects `RoverRepository` and calls `find()` itself.
# Subagent execution

Run this skill in a dedicated subagent. This is mandatory, including when the
review appears small or straightforward. Return only the actionable findings
and completed changes to the parent agent. If test execution is required in a
Gradle project, use `/gradle-tests` and report only its compact result.
