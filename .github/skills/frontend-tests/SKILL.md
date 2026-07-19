---
name: frontend-tests
description: >
  Use when writing React/Next.js tests: page integration tests with RTL,
  component tests with child component mocks, or API hook tests with MSW.
  Covers query rules (no data-testid), semantic HTML, ALTO design system,
  Module Federation notes, and domain boundary rules.
---

See the full guide at `docs/tdd/frontend-tests.md`.

Key rules:
- Page tests: mock only API hooks and the router; assert on roles, names, visible text.
- Component tests: mock child components with jest.mocked(); assert on rendered output.
- Hook tests: use MSW as the fake server — never mock fetch or axios directly.
- Never use data-testid. Query by role, accessible name, or visible text.
- Use ALTO components; never BAgel in new code.
- Accommodation and flights are separate domains — do not share fixtures between them.
- RTL only normalises rendered DOM text, not your query string — never build a `getByText`
  query from a production helper with its own whitespace/formatting quirks; use a plain
  literal or raw fixture field instead.
