# Darwin BA Holidays Platform — Copilot Instructions

This is a monorepo for the **Darwin** platform at British Airways Holidays. It contains backend services (Kotlin/Spring Boot), frontend micro-frontends (Next.js 15 + Module Federation), infrastructure (Terraform), and more.

**Mandatory Rule:** The repository-root `AGENTS.md` is the sole source of truth
for all workflows, TDD cycles, and skill references in this repository. Other
`AGENTS.md` files, `.github/copilot-instructions.md` files, and custom agent
definitions may extend it with project-specific details, but must not override
or replace it.

---
# Token Optimization Rules
- Mode: ultra-dense output.
- Do not include greetings, sign-offs, or conversational filler.
- Provide raw code or shell commands directly without unnecessary explanations.


## Platform Map

### AWS Accounts & Services

| AWS Account | Sub-project | Role | Local port |
|---|---|---|---|
| Search & Browse | `searchBrowseBff/` | Kotlin/Spring Boot BFF — hotel & bundle search | — |
| Search & Browse | `holidays-searchBrowse-presentation/` | Next.js shell (MF host) — S&B booking journey | 8090 |
| Search & Browse | `holidays-searchBrowse-presentationprovider/` | Next.js MFE remote (`search-select-provider`) | 8091 |
| Manage Trip | `holidays-manageTrip-service/` | Kotlin/Spring Boot — manage booking BFF | — |
| Manage Trip | `holidays-manageTrip-presentation/` | Next.js MFE remote (`manage-trip-provider`) | — |
| Platform | `holidays-platform-infra/` | Terraform — shared AWS infrastructure | — |
| flight-bff | `holidays-searchBrowse-flight-bff/` | bff (backend for frontend) of flights sos team | — |


Architecture diagrams (Mermaid C4): `darwinC4Diagrams/`  
BFF API docs: `searchBrowseBff/doc/search/`, `holidays-checkoutPay-service/doc/`

The shell (`holidays-searchBrowse-presentation`) both **consumes** remotes and **exposes** its own components (`FlightDetails`, `AccommodationDetailsCardContainer`, `AmendmentCancellationAccordion`). The S&S provider must be running alongside the shell for the full booking flow.


## Backend Services (Kotlin / Spring Boot)
**Common commands** (run from each sub-project root):
```bash
./gradlew check          # lint + tests + coverage
./gradlew test           # unit tests only
./gradlew test --tests "com.bah.MyTest"  # single test class
./gradlew ktlintFormat   # format
./gradlew generateOpenApiDocs  # regenerate doc/openapi.yaml (on API changes only)
```

**Generated OpenAPI clients** live in `build/generate-src/` — never hand-edit them. Change specs, then run the relevant Gradle task.

**Formatting**: ktlint. No wildcard imports. Trailing commas in multiline lists.

**Kotlin conventions** (all services):
- Prefer `val` over `var`. Use `data class` for structured data.
- Never use `!!`; prefer safe calls (`?.`) and Elvis (`?:`).
- Use expression bodies for single-line functions when readable.
- Keep classes/functions `internal` unless they are part of a public API. Specify explicit return types for public functions.

**Testing stack**: JUnit 5 (or Kotest `DescribeSpec`), MockK, Kotest assertions.
- Mock only interfaces, never concrete classes.
- Prefer fakes (`InMemory*`) over mocks for persistence.
- `*Test` = unit, `*IntegrationTest` = Spring/Testcontainers.
- Avoid broad `any()` matchers in MockK — prefer `eq(...)`, `match { ... }`, or `capture(...)`.

**MDC / coroutines**: Trace and session IDs are MDC-based. Kotlin coroutines do not inherit MDC — manually re-apply MDC values inside `runBlocking` / coroutine scopes.

**`holidays-checkoutPay-service` specifics**:
- Load `DOMAIN.md` before working on business logic, pricing, traveller rules, or payment flows. It contains the domain glossary and key business rules.
- `bundle.checkout` (`/v2/checkout/*`) must remain isolated from `checkout` (`/v1/checkout/*`) — enforced by ArchUnit.
- TravelBox generated clients in this service live in `checkout.adapter.generated` and have **no Gradle regen task** — ask a developer to use external tooling if regeneration is needed.
- Test fixtures live in companion objects inside dedicated `*Example.kt` files, mirroring the production source tree under `src/test`.
- Error handling: use `createCustomProblemDetail(HttpStatus, title, detail)` — do not construct `ProblemDetail` directly. Prefer scoped `@ControllerAdvice` over routing through `ExceptionHandlerAdvice`.

**`searchBrowseBff` specifics**:
- Cache names are versioned and must be updated in **two places**: `CacheConfig.kt` and `application.yaml`.
- Two search flows exist: hotel-only and bundles — keep them separate.
- Unsupported search criteria intentionally route to OpenJaw redirect flows (`SearchCriteriaNotSupportedException`).

---

## Frontend MFEs (Next.js 15 + Module Federation)

All frontend repos share these patterns:

**Runtime**: Node 22 required (`nvm install 22`).

**Architecture** — Module Federation:
- `holidays-searchBrowse-presentation/` is the **shell host** (`presentation-shell`).
- `holidays-searchBrowse-presentationprovider/` is the **search-select-provider** remote (port 8091).
- `holidays-manageTrip-presentation/` is the **manage-trip-provider** remote.
- Remote imports in the shell must use `withClientImport()` from `src/shared/federation/withClientImport.tsx` — never `import()` directly. It skips SSR and wraps in `<Suspense>`.

```tsx
const SearchArea = withClientImport(
  () => import("search-select-provider/MainSearchArea"),
);
```

- A `fallbackRemotePlugin` at `module-federation/utils/fallbackRemotePlugin.js` handles unavailable remotes gracefully.

**Design system**:
- `holidays-searchBrowse-presentationprovider/` uses **BAgel** (`ba-*` web elements via Shadow DOM). Self-hosted static files — cannot be updated. BAgel is being deprecated.
- `holidays-manageTrip-presentation/` uses **Bagel** (npm, version 3.72.3).
- New code in other repos should use **ALTO** (`@holidays/designsystems-componentlibrary`). Never use BAgel in new code elsewhere.

**Install** (`@holidays` scoped packages require JFrog auth):
```bash
npm login --registry=https://iagl.jfrog.io/artifactory/api/npm/holidays-design-systems-npm/ --auth-type=web --scope=@holidays
npm install
```

**Common commands**:
```bash
TZ=UTC npm test          # always set TZ=UTC — tests depend on it
npm test                 # silent, with coverage (CI-like)
npm run test:debug       # verbose, thresholds off
npm run test:watch       # watch mode
npm run lint             # ESLint
npm run type-check       # TypeScript
```

**Auth**: `@auth0/nextjs-auth0` v4 in the presentation shell — configured in `src/lib/`, handled by `src/middleware.ts`.

**Contract testing** (presentation shell): lives in `/contract-testing-library/` with its own `package.json`, pre-built during `npm install`. If contract tests fail after dependency updates, sync `react`/`react-dom` versions between root and `contract-testing-library/package.json`.

---

## Infrastructure (Terraform)

Sub-project: `holidays-platform-infra/`

Always use `make`, never `terraform` directly. `ENV` variable is mandatory:

```bash
make ENV=dev init
make ENV=dev plan
make ENV=dev apply
make lint && make format && make validate
make ENV=dev test-unit   # LocalStack (requires Docker)
```

- Environments: `dev`, `tst`, `stg`, `prd`, `dr`
- All resource names: `${var.avios_product}-{resource-name}`
- ECS services communicate via Service Connect, not direct ALB-to-ALB.

---

## Cross-Cutting Rules
- **No `data-testid`** in frontend tests.
- **No hardcoded secrets** anywhere — `.env.example` only, never `.env`.
- **Gitleaks** runs on pre-commit in all projects.
- **Accommodation and flights are separate domains** — do not share test fixtures or utilities between them.
- **Respond in English** regardless of the language the user writes in.
