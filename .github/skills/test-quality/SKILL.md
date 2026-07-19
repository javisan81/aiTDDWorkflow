---
name: test-quality
description: >
  Use when writing test fixtures, naming test data, asserting on serialised output (JSON),
  or reviewing whether a test body contains signal or noise. Covers ANY_ prefix,
  scalar vs instance fixtures, copy-based variants, .example.ts fixture files, and full
  JSON contract assertions.
---

See the full guide at `docs/tdd/test-quality.md`.

Key rules:
- Every irrelevant value in a test must use the ANY_ prefix and live in a fixture.
- Scalar constants are top-level const val; object instances are companion object extensions.
- Use copy() to derive fixture variants — never duplicate constructor calls.
- TS/React: colocate fixtures in `__mocks__/*.example.ts` next to the component; derive
  second instances via `{ ...FIRST, override }`, never a fresh object literal.
- Always assert the full JSON response in strict mode — never assert on a partial fragment.
- Never derive an expected value by calling the production function under test (or its
  formatting helpers) — compose the expected literal from the fixture's raw field values instead.
