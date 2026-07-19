---
name: backend-tests
description: >
  Use when writing Kotlin/Spring Boot tests: controller tests with @WebMvcTest,
  use-case unit tests with InMemory fakes, or JPA/HTTP adapter integration tests.
  Covers MockMvc Kotlin DSL, MockK, Kotest assertions, and test naming conventions.
---

See the full guide at `docs/tdd/backend-tests.md`.

Key rules:
- Controller tests: @WebMvcTest + @MockBean for the input port + full strict JSON contract.
- Use-case tests: entry point is the interface, not the class; InMemory* preferred over mockk.
- Domain collaborators inside use-case tests: real objects (sociable, no mocking).
- Integration adapter tests: @MockBean the use-case interface; test only the adapter wiring.
- Test names are backtick sentences describing observable behaviour.
