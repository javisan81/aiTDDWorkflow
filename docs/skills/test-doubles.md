---
name: test-doubles
description: >
  Use when choosing between fake, mock, stub, spy, or dummy. Use when deciding whether
  to use InMemory* vs mockk, MSW vs axios-mock-adapter, or when a test explosion
  warning is needed. Covers unit vs integration test distinction.
---

# Test Types, Test Doubles and Mocking

## Unit test vs Integration test

**Unit test** — tests **pure logic** (no side effects). Same input always produces same output.
No infrastructure in the setup. The "unit" is a **behaviour**, not a class — it can include
multiple real domain collaborators together (sociable test). This is where **domain classes
and use cases** live: entities, value objects, domain services, application services.
These tests are the majority and drive the design of the domain model.

**Integration test** — tests **side effects**: that your code correctly uses infrastructure
to produce an observable change (write to DB, HTTP call, render to DOM). Requires non-trivial
infrastructure in the setup. This is where **adapters** live: repository adapters (JPA, HTTP
clients) and entry-point adapters (REST controllers). These tests verify that your
infrastructure wiring is correct, not that your business logic is correct.

| Non-trivial setup (→ integration test) | Trivial (→ unit test) |
|----------------------------------------|----------------------|
| H2 / Testcontainers / Docker | `InMemory*` data structure |
| Spring MockMvc / RTL rendering | Plain function/constructor call |
| MSW / Wiremock fake server | — |

In integration tests, **domain input ports (use case interfaces)** are mocked — intentionally.
The goal is to verify the infrastructure layer in isolation. The mock defines
*what the domain can do*, not *how*.

**Design signal**: too many integration tests = anemic domain. Logic is trapped in
infrastructure. Move it to the domain.

---

## The five types of test doubles

All five are valid. Choose the one that fits:

| Type | What it does | When to use |
|------|-------------|-------------|
| **Dummy** | Passed around but never used | Fill required parameters irrelevant to the test |
| **Stub** | Returns canned answers | Provide a fixed response so the SUT can proceed |
| **Fake** | Working implementation, simplified | Replace infrastructure (`InMemory*` repo, fake server) |
| **Spy** | Stub that also records calls | Verify a collaborator was called correctly |
| **Mock** | Pre-programmed with expectations | Verify a specific interaction protocol |

Prefer **fakes** for persistence, **stubs** for responses. Use **mocks** when the interaction
protocol itself is under test. Avoid doubles for input data / output results — if constructing
them is hard, the interface is too large (ISP violation).

---

## The core rule: only mock what you own

> **Only mock interfaces you own and control.** If you cannot change the source code, do not mock it.

Every test double defines an implicit contract. If the production code changes and the double
is not updated, tests stay green and production breaks. This risk is minimised by placing
doubles **only at layer boundaries**.

**Layer boundary reference:**

| Boundary | Double to use | Example |
|----------|--------------|---------|
| Controller → UseCase interface | Mock (library) | `@MockBean UseCase` |
| UseCase → Repository interface | Fake (hand-written) preferred | `InMemory*` — ask if mock is acceptable |
| HTTP adapter → external server | Fake server preferred | MSW / Wiremock — ask if `axios-mock-adapter` is acceptable |
| Component → child component | Mock (library) | `jest.mocked(Child)` |
| Domain collaborator inside domain | **Real object** | sociable unit test |
| Third-party library (axios, fetch) | Prefer fake server | ask before mocking directly |

---

## The trap — mocking a library you'll upgrade

```
mock axios v0.27 → tests pass
upgrade to axios v1.0 (breaking change) → tests still pass
deploy → production broken 💥
```

Use MSW / Wiremock instead: the real client runs, you catch integration bugs early,
and you can write contract tests between your fake server and the real one.

---

## Why mocking libraries are valuable — and how to use them safely

MockK, Mockito, and Jest mocks are **powerful TDD tools** — not something to avoid.
They let you design collaborator APIs on the fly without implementing them,
keeping the RED→GREEN loop short.

Two rules to get the benefits without the risks:
1. **Only use mocking tools for code you can change** — never third-party libraries
2. **Only mock interfaces at layer boundaries**

Discipline: when you change a mock, **immediately update production code to match**.
When you change production code, **find all mocks of that interface and update them**.

Trade-off: fakes are safer (you can write contract tests); mocks are faster (design APIs
without implementing them). Use both consciously.
