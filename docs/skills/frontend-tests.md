---
name: frontend-tests
description: >
  Use when writing React/Next.js tests: page integration tests with RTL,
  component tests with child component mocks, or API hook tests with MSW.
  Covers query rules (no data-testid), semantic HTML, ALTO design system,
  Module Federation notes, and domain boundary rules.
recommended_model: gpt-5.6-luna
---

# Frontend Test Patterns (React / Next.js)

## Layer progression

```
Page / Feature integration test  (RTL, full render)
  ↓ when page test passes and component logic is complex enough
Component test                    (RTL, isolated render)
  ↓ when component test passes and external data is needed
Hook / API adapter test           (MSW fake server)
```

---

## Page tests (outer loop)

- Render the full page with React Testing Library
- Mock only **API hooks** and the **Next.js router** — everything else is real
- Assert on what the user sees: roles, accessible names, visible text
- **Never use `data-testid`**

```tsx
jest.mock("../hooks/useHotels");

it("displays the hotel list when data loads", async () => {
    jest.mocked(useHotels).mockReturnValue({ hotels: [ANY_HOTEL], loading: false });

    render(<HotelsPage />);

    expect(await screen.findByRole("listitem", { name: ANY_HOTEL.name })).toBeInTheDocument();
});
```

---

## Component tests (inner loop)

- Render the component in isolation
- Mock child components with `jest.mock` + `jest.mocked` — never render their internals
- Assert on **rendered output**, not on mock call arguments

**Type-safe child component mock pattern:**
```tsx
jest.mock("./FilterBadge");

jest.mocked(FilterBadge).mockImplementation(({ label, onRemove }) => (
    <button onClick={onRemove}>{label}</button>
));

it("renders one badge per active filter", () => {
    render(<FilterBar filters={[ANY_FILTER]} />);

    expect(screen.getByRole("button", { name: ANY_FILTER.label })).toBeInTheDocument();
});
```

---

## Hook / API adapter tests (innermost loop)

- Use **MSW** (Mock Service Worker) as the fake server — the real HTTP client runs
- Never mock `fetch`, `axios`, or any HTTP client directly
- Ask the developer before using `axios-mock-adapter` or similar

```ts
server.use(
    http.get("/api/hotels", () =>
        HttpResponse.json({ hotels: [ANY_HOTEL] })
    )
);

it("returns hotels from the API", async () => {
    const { result } = renderHook(() => useHotels());
    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.hotels).toEqual([ANY_HOTEL]);
});
```

---

## Test query rules — always from the user's perspective

**Never use `data-testid`**. Query by what the user sees or interacts with:

| Prefer | Avoid |
|--------|-------|
| `getByRole("button", { name: "Clear filter" })` | `getByTestId("clear-btn")` |
| `getByRole("region", { name: "Applied filters" })` | `getByTestId("filter-row")` |
| `getByText("Outbound: Morning")` | `getByTestId("outbound-badge")` |

For "is this rendered at all", use a semantic role with `aria-label` — improves accessibility too.

**`getByText`/`getByRole` name matching is not symmetric.** RTL normalises the *rendered DOM
text* (trims/collapses whitespace) before matching, but it does **not** normalise the *query
string* you pass in. If you build the query from a production helper that pads its output
(e.g. `cabinClass(flight)` returning `" " + value`), the query keeps the leading space and the
match silently fails even though the text looks identical on screen. Always query with a plain
literal or a raw fixture field — never with a helper that has its own whitespace/formatting
quirks.

---

## Semantic HTML — buttons vs links

- `<button>` (or ALTO `Button`) for **actions** (clear, submit, toggle)
- `<a>` (or ALTO `Link`) for **navigation**
- Never `<a href="#">` with `preventDefault` — breaks keyboard and screen reader users

---

## Design system

- **ALTO** (`@holidays/designsystems-componentlibrary`) for all new components
- **BAgel** (`ba-*`) is deprecated — do not use in new code
- Components available: `Badge`, `Button`, `Box`, `Heading`, `Paragraph`, `Icon`,
  `Checkbox`, `CheckboxGroup`, `Form`, `FieldsetDropdown`, `VisuallyHidden`, `Link`,
  `ExpandableBlock`, `ExpandableCard`, `FlightLine`, `useBreakpoint`

---

## Domain boundaries

Accommodation and flights are separate domains. Do not import fixtures, utilities,
or constants from one into the other.

---

## Environment and feature flags

- Never use `process.env` inside components in the S&S provider — read from `useEnvironmentContext()`
- Feature flags via DevCycle:
  - `presentationprovider`: `useFlagValue` from `src/featureToggles/value.tsx`
  - `manageTrip-presentation`: `useDevCycleClient()` wrapped in hooks under `src/flags/`

---

## Module Federation notes

- `holidays-searchBrowse-presentation` is the **shell host** (`presentation-shell`)
- Remote imports in the shell must use `withClientImport()` — never `import()` directly
- `reactStrictMode: false` in the presentation shell — intentional, do not enable
  (some TBX endpoints are non-idempotent)
