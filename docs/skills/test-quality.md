---
name: test-quality
description: >
  Use when writing test fixtures, naming test data, asserting on serialised output (JSON),
  or reviewing whether a test body contains signal or noise. Covers ANY_ prefix,
  scalar vs instance fixtures, copy-based variants, .example.ts fixture files, and full
  JSON contract assertions.
---

# Test Quality Rules

Consider the next sections as steps to pass, to validate the current quality of the test in place, if any of this step does not pass then try to refactor the code to make it pass:

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

### Kotlin example files

Check the current examples in the project you are working on to understand where to put new values or update them.

Reusable Kotlin fixtures belong in a dedicated `*Example.kt` file under
`src/test`, mirroring the production package of the type they describe. Tests
should import examples instead of constructing full domain objects or payloads
inline.

Use companion-object extensions for domain instances, following the project
convention:

```kotlin
// src/test/kotlin/com/bah/flights/domain/model/FlightOfferExample.kt
val FlightOffer.Companion.example: FlightOffer
    get() = realFlightOffer(
        availabilityId = ANY_AVAILABILITY_ID,
        offerId = ANY_OFFER_ID,
        payload = ANY_VALID_FLIGHT_OFFER_PAYLOAD,
    )
```

The example must be a real domain object or real adapter-backed domain
implementation, never a mock. Put incidental identifiers, keys, payload
fragments, and other reusable values in the example file as `ANY_` constants.
Keep only behavior-defining relationships visible in the test, such as using
`FIRST_ORIGINAL_CART_ID` as the first element of `originalCartIds`.

For variants, prefer deriving from a base example with `copy` when the type
supports it. For interfaces or parsed objects that cannot be copied, expose
named companion examples such as `exampleWithoutOfferIdentifier` and build
them through a shared factory in the same example file. Do not duplicate large
JSON payloads or repeated flight keys in individual tests.

If a type has no companion, do not add production-only structure merely to
support a fixture. Use the nearest existing project example convention or a
dedicated fixture factory, and keep that fixture in test sources.

If in the test file you have constants and objects created once and again try to move them to an example.

### Kotlin example files

Reusable Kotlin fixtures belong in a dedicated `*Example.kt` file under
`src/test`, mirroring the production package of the type they describe. Tests
should import examples instead of constructing full domain objects or payloads
inline.

Use companion-object extensions for domain instances, following the project
convention:

```kotlin
// src/test/kotlin/com/bah/flights/domain/model/FlightOfferExample.kt
val FlightOffer.Companion.example: FlightOffer
    get() = realFlightOffer(
        availabilityId = ANY_AVAILABILITY_ID,
        offerId = ANY_OFFER_ID,
        payload = ANY_VALID_FLIGHT_OFFER_PAYLOAD,
    )
```

The example must be a real domain object or real adapter-backed domain
implementation, never a mock. Put incidental identifiers, keys, payload
fragments, and other reusable values in the example file as `ANY_` constants.
Keep only behavior-defining relationships visible in the test, such as using
`FIRST_ORIGINAL_CART_ID` as the first element of `originalCartIds`.

For variants, prefer deriving from a base example with `copy` when the type
supports it. For interfaces or parsed objects that cannot be copied, expose
named companion examples such as `exampleWithoutOfferIdentifier` and build
them through a shared factory in the same example file. Do not duplicate large
JSON payloads or repeated flight keys in individual tests.

If a type has no companion, do not add production-only structure merely to
support a fixture. Use the nearest existing project example convention or a
dedicated fixture factory, and keep that fixture in test sources.

### Domain instances must be real

Never use `mockk<DomainType>()` for domain objects returned by a mocked port or passed to the
system under test. Use an existing example, fake, or real domain instance instead. Mock only the
port boundary and configure the real domain object through its constructor or fixture parameters.
This keeps the test focused on behavior and prevents domain methods such as `cabinClass()` from
being hidden behind mock setup.

Before approving a test, inspect every value repeated across setup, mock expectations, method calls,
and assertions. Reuse existing `ANY_` fixtures from the relevant example file when available.
Otherwise extract repeated identifiers and other incidental scalars into clearly named constants.
In particular, do not repeat cart IDs, availability IDs, offer IDs, or other domain identifiers as
magic strings in `every { ... }` blocks or production calls. Keep the behavior-defining relationship
visible in the test, for example `FIRST_ORIGINAL_CART_ID` as the first item in
`originalCartIds`, while hiding only the literal value behind the fixture.

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
---

## Compare full objects
We prefer comparing, the expected result vs the current executed result, full objects when possible, not the individual attributes of the class we are interested to check the results.
If you decide not comparing full objects explain your decision to the customer.

## If you have comments in your tests
Use comments in your tests to improve names or extract methods and when the comments are irrelevant remove them.

## YAGNI
Run `/yagni` checklist on the test before showing it to the user. If yagni is not passing explains it to the customer.

## Refactor
Run `/refactor` checklist on the test before showing it to the user. Try to fix smells found in the file where your test lives.

