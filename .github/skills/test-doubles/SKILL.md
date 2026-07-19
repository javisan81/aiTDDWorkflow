---
name: test-doubles
description: >
  Use when choosing between fake, mock, stub, spy, or dummy. Use when deciding whether
  to use InMemory* vs mockk, MSW vs axios-mock-adapter, or when a test explosion
  warning is needed. Covers unit vs integration test distinction.
---

See the full guide at `docs/tdd/test-doubles.md`.

Key rules:
- Only mock interfaces you own and control — never third-party libraries.
- Prefer InMemory* fakes for persistence; ask the developer before using mocks.
- Prefer MSW / Wiremock for HTTP; ask the developer before using HTTP-client mocks.
- Doubles belong only at layer boundaries.
- Too many integration tests = anemic domain — stop and flag.
