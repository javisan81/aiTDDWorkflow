---
name: test-quality
description: >
  Use when writing test fixtures, naming test data, asserting on serialised output (JSON),
  or reviewing whether a test body contains signal or noise. Covers ANY_ prefix,
  scalar vs instance fixtures, copy-based variants, .example.ts fixture files, and full
  JSON contract assertions.
---

# Test Quality Rules

## Signal vs noise — the `ANY_` prefix

Every detail in a test is either **relevant** (reader needs it) or **irrelevant** (only needed
to compile). Apply consistently:

- Relevant details → show clearly in the test body
- Irrelevant details → hide in a fixture with `ANY_` prefix

If you can change a value and all tests still pass, it was irrelevant. Move it to a fixture.

---

## Fixtures: scalars vs. instances (Kotlin)

Scalar constants are top-level `const val`:
```kotlin
const val ANY_BOOKING_REF = "BK-001"
const val ANY_HOTEL_ID    = "hotel-42"
const val ANY_PRICE       = 100
const val ANY_NIGHTS      = 3
```

Object instances are companion object extensions. Derived values reference the already-named
constants — never duplicate literals:
```kotlin
val Hotel.Companion.ANY_HOTEL  get() = Hotel(id = ANY_HOTEL_ID, name = "Some Hotel")
val SearchResult.Companion.ANY_RESULT get() =
    SearchResult(hotel = Hotel.ANY_HOTEL, price = ANY_PRICE, nights = ANY_NIGHTS)
```

Use `copy` to derive variants — makes explicit what changed, hides everything else:
```kotlin
// BAD — reader must compare constructors to spot the difference
val SearchResult.Companion.ANY_CHEAPER get() =
    SearchResult(hotel = Hotel.ANY_HOTEL, price = 50, nights = ANY_NIGHTS)
// GOOD — only price changed
val SearchResult.Companion.ANY_CHEAPER get() = ANY_RESULT.copy(price = 50)
```

---

## Fixtures: `.example.ts` files (TypeScript/React)

The same scalar/instance split applies in frontend tests, colocated with the component in a
`__mocks__/*.example.ts` file (e.g. `flight-info/__mocks__/flight-details.example.ts`) rather
than inline in the test — this lets multiple test files for the same component share one
source of truth.

```ts
// __mocks__/flight-details.example.ts
export const ANY_FIRST_CABIN_CLASS = "Economy";
export const ANY_SECOND_CABIN_CLASS = "Business";
export const ANY_FIRST_CHECKED_BAGGAGE = 1;
export const ANY_SECOND_CHECKED_BAGGAGE = 2;

export const FIRST_FLIGHT_DETAILS_EXAMPLE: FlightDetails = {
  cabinClass: ANY_FIRST_CABIN_CLASS,
  checkedBaggage: ANY_FIRST_CHECKED_BAGGAGE,
  // ...
};

// Second instance derived via spread + overrides — never a fresh duplicate
// object literal. Shared boundary values (e.g. arrival of the first segment
// = departure of the second) are wired explicitly to show the relationship.
export const SECOND_FLIGHT_DETAILS_EXAMPLE: FlightDetails = {
  ...FIRST_FLIGHT_DETAILS_EXAMPLE,
  cabinClass: ANY_SECOND_CABIN_CLASS,
  checkedBaggage: ANY_SECOND_CHECKED_BAGGAGE,
  departure: { ...FIRST_FLIGHT_DETAILS_EXAMPLE.arrival },
};
```

Rules:
- One `.example.ts` file per component/domain concept, next to the component under `__mocks__/`.
- Scalars are top-level `ANY_`-prefixed `const`s; instances are `const` objects named
  `..._EXAMPLE` (or `FIRST_/SECOND_..._EXAMPLE` when a test needs two distinguishable variants).
- Derive the second instance from the first with `{ ...FIRST, override }` — never write a second
  full object literal from scratch.
- Do **not** put pre-formatted "expected text" strings in the example file (see next section) —
  only raw field values belong here.

---

## Full JSON contract — always strict

When asserting on serialised output, assert the **full structure** in strict mode.
Never assert on a partial fragment — contracts can drift silently.

```kotlin
// BAD — contract can drift silently
assertThat(response.body).contains("\"status\":\"OK\"")

// GOOD — full contract, strict mode
content { json("""
    {
        "bookingRef": "$ANY_BOOKING_REF",
        "hotelId":    "$ANY_HOTEL_ID",
        "price":      $ANY_PRICE,
        "nights":     $ANY_NIGHTS,
        "status":     "CONFIRMED"
    }
""".trimIndent(), true) }
```

---

## Mock matchers — always use real values

Never use broad matchers (`any()`, `anyString()`, etc.) in mock expectations.
Specify the exact argument the production code will pass:

```kotlin
// BAD — any() hides what the controller actually sends to the use case
every { deployRover.execute(any()) } returns RoverPosition(x = 0, y = 0, direction = "N")

// GOOD — exact value makes the contract explicit and catches mapping bugs
every { deployRover.execute(DeployRoverCommand(x = 0, y = 0, direction = "N")) } returns RoverPosition(x = 0, y = 0, direction = "N")
```

If the argument is truly irrelevant to the behaviour under test, extract the value as an `ANY_` fixture
constant and use it both in the expectation and in the request body — the pairing makes the mapping
visible without repeating a magic literal.

---

## Never build the expected value with the code under test

A test is tautological when it derives its expected value by calling the same production
function (or formatting logic) that the component under test also calls — it can no longer
catch a regression in that logic, because a bug would shift both sides of the assertion
together.

```tsx
// BAD — checkedBaggageText() is the same helper the component renders with;
// a formatting bug in checkedBaggageText() would never be caught here
expect(screen.getByText(checkedBaggageText(SEGMENT))).toBeInTheDocument();

// BAD too — a pre-baked "expected text" constant hides the actual segment data
// used to build it, and still risks drifting out of sync silently
const SEGMENT_CHECKED_BAGGAGE_TEXT_EXAMPLE = "1 checked bag (23kg/50lb)";
expect(screen.getByText(SEGMENT_CHECKED_BAGGAGE_TEXT_EXAMPLE)).toBeInTheDocument();

// GOOD — expected text is composed in the test from the fixture's own field value,
// independent of the production formatting code
expect(
  screen.getByText(`${SEGMENT.checkedBaggage} checked bag (23kg/50lb)`),
).toBeInTheDocument();
```

Prefer composing the expected literal in the test from the fixture's raw field(s) over either
(a) calling the production formatter, or (b) hiding a pre-formatted string behind an opaque
fixture constant — the reader should be able to see which segment value produced which text.

In a test dont create json with mappers, use the string as json string.
So this is an example of something wrong:
```kotlin
  val expected =
            jacksonObjectMapper().writeValueAsString(
                AlternativeFlightsResponse.fromDomain(
                    domain,
                    AlternativeFlightFilters(emptyList(), emptyList(), Stops.ANY_NUMBER_OF_STOPS),
                ),
            )
```
The above example should be the string representing the thing.
## Subagent execution

Run this review in a dedicated subagent. This is mandatory, including when the
review appears small or straightforward. Return only actionable quality
findings and the smallest required correction. If Gradle tests are required,
use `/gradle-tests` and report only compact diagnostics.
