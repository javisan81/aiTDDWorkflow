---
name: tdd-outside-in
description: >
  Use when starting a new feature, writing the first test, deciding which layer to test first,
  or doing TDD in a layered architecture. Explains the double loop, layer progression,
  TPP, and test explosion warning.
---

# Outside-In TDD (Double Loop)

Start from the outermost layer and drive inward.
**Only move to the next layer when the current one demands it.**

---

## Vertical slicing and the walking skeleton

Work **one use case at a time**. A use case is a vertical slice: it cuts through every layer
(controller → use case → adapter) and delivers a complete, observable behaviour.

**Walking skeleton**: start with the thinnest possible slice that crosses all layers end-to-end.
It does not need to be correct — it needs to prove that every layer is wired together.
Add behaviour layer by layer, test by test, until the slice is complete.

```
Use case A
  controller test    → GREEN
  use-case test      → GREEN
  adapter test       → GREEN
  ✓ vertical slice complete

Use case B  ← only start here once A is fully done
  ...
```

**Rule**: do not start the next use case until the current vertical slice is fully tested at every layer.

---

## The two loops

```
     Outer loop (acceptance / feature level)
     ┌─────────────────────────────────────┐
     │                                     │
     │   RED (feature test fails)          │
     │     ↓                               │
     │   Inner loop (unit level)           │
     │   ┌──────────────────────────┐      │
     │   │  RED → GREEN → REFACTOR  │      │
     │   └──────────────────────────┘      │
     │     ↓                               │
     │   GREEN (feature test passes)       │
     │                                     │
     └─────────────────────────────────────┘
```

## Layer progression

```
Entry point (outermost — HTTP controller, CLI, queue handler)
  ↓ only when entry-point tests pass AND logic is non-trivial
Use case (application service)
  ↓ only when use-case tests pass AND real infrastructure is needed
Infrastructure adapter (persistence, HTTP client, external service)
```

**The rule**: if you can make the entry-point test green by putting logic directly
in the controller, do it. Extract to a use case only when a test demands it.

## What each layer tests

| Layer | What it tests | What it mocks |
|---|---|---|
| Entry point | Correct wiring: input → output contract | The use-case interface (input port) |
| Use case | Business behaviour | Infrastructure interfaces (output ports) |
| Infrastructure adapter | Correct use of the external system | Nothing (or the external system via fake server) |

## Transformation Priority Premise (TPP)

When writing the minimum GREEN code, apply the **simplest** transformation first:

1. No code → return `null` / constant
2. Constant → scalar variable
3. Unconditional → conditional (`if`)
4. Scalar → collection
5. `if` → loop

**Signal**: if you need a catch-all / default branch without an explicit branch for each
case, a new type is trying to emerge. Stop and model it.

## Test explosion — warning signal

**Test explosion** (J.B. Rainsberger) = combinatorial explosion when a test depends
on the correctness of **more than one piece of non-trivial behaviour**.

> ⚠️ **"Integrated" ≠ "Integration"**
> - **Integration test**: verifies one infrastructure boundary. Healthy in small numbers.
> - **Integrated test**: result depends on multiple non-trivial units, each with their own
>   branching. This causes explosion — regardless of whether it uses a framework or not.

With 4 branch points per layer and 3 layers: `4^3 = 64` tests needed. Add a layer → 256.

> ⚠️ **If many tests are needed to cover combinations of behaviour across layers, stop and warn:**
> *"We may be heading towards a test explosion. Testing each layer in isolation —
> mocking the boundary interface — would cover the same paths with far fewer tests:
> N_client + N_server instead of N_client × N_server."*

## Layer-specific patterns

For the concrete patterns of each layer in this project:

- **Backend** (Kotlin / Spring Boot): use the `/backend-tests` skill
- **Frontend** (React / Next.js): use the `/frontend-tests` skill
