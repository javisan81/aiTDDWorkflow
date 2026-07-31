---
name: backend-tests
description: >
  Use when writing Kotlin/Spring Boot tests: controller tests with @WebMvcTest,
  use-case unit tests with InMemory fakes, or JPA/HTTP adapter integration tests.
  Covers MockMvc Kotlin DSL, MockK, Kotest assertions, and test naming conventions.
---

# Backend Test Patterns (Kotlin / Spring Boot)

## Layer progression

```
HTTP controller  (@WebMvcTest)
  ↓ when controller tests pass and logic is complex enough
Use case         (plain unit test, InMemory* fakes)
  ↓ when use-case tests pass and real persistence is needed
JPA / HTTP adapter  (@SpringBootTest / Testcontainers)
```

---

## Controller tests (`@WebMvcTest`)

- One test class per controller
- `@MockBean` for the **single** input port interface the controller depends on
- Use the Kotlin DSL: `mockMvc.post { }`, `mockMvc.get { }`
- Assert the **full JSON response** in strict mode:

```kotlin
mockMvc.get("/hotels/$ANY_HOTEL_ID") {
    accept = MediaType.APPLICATION_JSON
}.andExpect {
    status { isOk() }
    content { json("""
        {
            "id":    "$ANY_HOTEL_ID",
            "name":  "$ANY_HOTEL_NAME",
            "price": $ANY_PRICE
        }
    """.trimIndent(), true) }
}
```

- One test = one observable API behaviour
- Test error responses with the same full-contract approach

---

## Use case tests

- Entry point: **the use-case interface** (input port), not the concrete service class
- Persistence: `InMemory*` fake is preferred over `mockk<Repository>()` — ask the developer
  which approach they want before proceeding
- Domain collaborators: **real objects** (sociable — no mocking inside the domain)
- The unit is a **behaviour**, not a class

```kotlin
class AddToCartTest {
    private val cart = InMemoryCartRepository()
    private val useCase: AddToCart = AddToCartService(cart)

    @Test
    fun `adds item to an empty cart`() {
        useCase.execute(AddToCartCommand(ANY_CART_ID, ANY_PRODUCT_ID, ANY_QUANTITY))

        assertThat(cart.find(ANY_CART_ID)?.items).containsExactly(
            CartItem(ANY_PRODUCT_ID, ANY_QUANTITY)
        )
    }
}
```

---

## Infrastructure adapter tests (`@DataJpaTest` / `@SpringBootTest` / Testcontainers)

- Code tied to infrastructure is tested with **integration tests** — never with plain MockK unit tests.
- For JPA adapters use `@DataJpaTest` with a real H2 or Testcontainers DB.
- **All tests for one adapter — happy path and every error path — belong in the same integration test class.** Do not create a separate unit test class for the error cases.
- Test the adapter through the **output port interface** (`RoverRepository`), not through the concrete class.
- Force flushing where needed (use `saveAndFlush()` or `TestEntityManager.flush()`) so that constraint violations are surfaced inside the adapter's own boundary.
- One domain exception per domain concern. Adapters **translate** infrastructure exceptions (`DataAccessException`) into the existing domain exception. They do not introduce new exception types.

```kotlin
@DataJpaTest
class JpaRoverRepositoryAdapterIntegrationTest {
    @Autowired private lateinit var jpaRepository: RoverPositionJpaRepository
    private lateinit var adapter: RoverRepository

    @BeforeEach fun setUp() { adapter = JpaRoverRepositoryAdapter(jpaRepository) }

    @Test fun `saves position and finds it back`() { ... }

    @Test fun `throws RoverDeploymentException when JPA fails to save`() {
        // trigger a real DB constraint violation — no mocks
        shouldThrow<RoverDeploymentException> { adapter.save(...) }
    }
}
```

---

## Testing stack

| Purpose | Library |
|---|---|
| Test runner | JUnit 5 or Kotest `DescribeSpec` |
| Mocking | MockK |
| Assertions | Kotest assertions (`shouldBe`, `shouldContain`, etc.) |
| HTTP contract | Spring MockMvc (Kotlin DSL) |
| Fake servers | WireMock |
| DB | Testcontainers (PostgreSQL) or H2 |

- Mock only interfaces, never concrete classes
- Prefer `InMemory*` fakes over `mockk<Repository>()` for persistence

---

## Test naming

Use backtick names that read as a sentence describing the behaviour:

```kotlin
@Test
fun `returns 404 when hotel is not found`() { ... }

@Test
fun `adds item to cart and returns updated total`() { ... }
```
