---
name: hexagonal-arch
description: >
  Use when designing folder structure, deciding whether to extract a port or domain service,
  discussing hexagonal or onion architecture, or reviewing whether domain classes have
  framework imports. Covers evolutionary design, port naming, and ArchUnit rules.
recommended_model: gpt-5.6-luna
---

# Architecture: Hexagonal — Evolutionary, Not Upfront

**Do not design the full architecture before the first test.** Let it emerge.

## Rules

- Start with the simplest thing that could work
- Extract a port (interface) only when a second adapter appears or a test makes the boundary explicit
- The domain must have **zero** framework/infrastructure imports (no Spring, no JPA)
- **Do not create a domain layer just to have one.** If the domain service is a pure proxy —
  it receives a call, does nothing, and delegates straight to the next layer — it has no business
  logic and should not exist yet. Wait until the tests demand it.

## Signals that the domain layer is now needed

- Logic starts accumulating in an adapter (controller, repository) that has nothing to do with
  infrastructure → move it to the domain
- Too many integration tests are needed to cover behaviour that should be a simple unit test
  → logic is trapped in infrastructure, the domain is anemic
- A second adapter appears that needs the same logic → extract to a shared domain service

## Target folder structure

```
domain/
  model/      ← pure domain classes, no framework imports
  port/
    input/    ← use-case interfaces (input ports)
    output/   ← infrastructure interfaces (output ports, e.g. repositories)
  service/    ← application services implement input ports

infrastructure/
  rest/        ← Spring MVC adapter (controllers + DTOs)
  persistence/ ← JPA adapter (entities + repos + adapters)
```

## Port naming

- Port names are **implementation-agnostic**: `CartRepository`, `PaymentGateway`
- Adapter names **reveal the implementation**: `TravelBoxCartRepository`, `StripePaymentGateway`
- Request DTOs expose `toDomain()`; response DTOs expose `fromDomain(...)`

## ArchUnit enforcement

Dependency rules are enforced by ArchUnit tests. The allowed directions are:

```
adapter.input.rest   →  usecase  →  domain
adapter.output.*     ←  domain ports
```

Domain classes must never import from `adapter.*`, `org.springframework.*`, or `jakarta.persistence.*`.

## check anemic use cases
Run `/anemic-use-case-check` skill to check if we have an anemic use case and then remove the use case if it is not required.


## Subagent execution

Run this architecture review in a dedicated subagent. This is mandatory,
including when the review appears small or straightforward. Return only
actionable violations and affected locations.
