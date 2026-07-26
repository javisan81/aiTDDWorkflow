# Darwin BA Holidays Platform — Copilot Instructions

This is a monorepo for the **Darwin** platform at British Airways Holidays. It contains backend services (Kotlin/Spring Boot), frontend micro-frontends (Next.js 15 + Module Federation), infrastructure (Terraform), and more.

**Mandatory Rule:** Read and adhere strictly to `AGENTS.md` for all workflows, TDD cycles, and skill references in this repository.

Each sub-project has its own `AGENTS.md` or `.github/copilot-instructions.md` with detailed, project-specific guidance. **Always read the sub-project instructions before working in a sub-directory, use those instructions in conjuction with the root AGENTS.md, if they are opposite, always the root AGENTS.md wins.**

---

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

---

## TDD Protocol (all projects — non-negotiable)

The full protocol lives in `AGENTS.md` at the repo root. The short version:

1. **RED** — write one failing test, stop, show output, ask for feedback before writing code.
2. **GREEN** — write minimum code to pass, stop, show output, ask for feedback before refactoring.
3. **REFACTOR** — one refactor, confirm green, ask for feedback before committing.
4. **COMMIT** — commit, ask before moving to the next test.

Violations: combining steps, writing production code without a failing test, writing more than one test at a time.

---

## Commits

Conventional commits are mandatory. Ticket number is **required** as the scope:

```
feat(DWNFLB-123): short description
```

- Format code before committing (see per-project instructions for the tool).
- Infrastructure files (`build.gradle.kts`, `next.config.ts`, `.gitignore`, etc.) must be committed separately from feature/refactor commits.
- **Git workflow**: trunk-based. Commit to local `main`, then run `./pr` to create a branch, move commits, push, and open a PR.

---

## Backend Services (Kotlin / Spring Boot)

All Kotlin services (`searchBrowseBff`, `holidays-checkoutPay-service`, `holidays-manageTrip-service`, `flight-bff` ) share these patterns:

**Architecture** — Onion/Hexagonal, enforced by ArchUnit:
```
adapter.input.rest   →  usecase  →  domain
adapter.output.*     ←  domain ports
```
- `domain` has zero Spring/JPA/generated-client imports.
- Port names are implementation-agnostic (`CartRepository`); adapter names reveal the implementation (`TravelBoxCartRepository`).
- Request DTOs have `toDomain()`; response DTOs have `fromDomain(...)`.
- Use cases expose one primary action: `execute`.
- Avoid anemic use cases: if a use case would only proxy a repository call, call the repository directly from the controller instead.

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

**Testing conventions**:
- Never use `data-testid`. Query by role, text, or ARIA label.
- Mock only what crosses the layer boundary (API hooks at page level, child components at component level, HTTP via MSW at hook level — never mock `fetch`/`axios` directly).
- Test fixtures use `A_` prefix for arbitrary/irrelevant values.
- In `presentationprovider`, tests use `jest-fixed-jsdom` with `shadow-dom-testing-library` (BAgel renders in Shadow DOM). Test files mirror `src/` under `__tests__/`.

**Feature flags**: DevCycle.
- In `presentationprovider`: use `useFlagValue` from `src/featureToggles/value.tsx`.
- In `manageTrip-presentation`: use `useDevCycleClient()` wrapped in hooks under `src/flags/`.
- In `presentation-shell`: use `src/shared/toggles/devcycle.ts` via `FeatureToggleProvider`.

**Environment config**: Never use `process.env` inside components in the S&S provider — read from `useEnvironmentContext()`. Register required startup vars in `validate-env.ts`. In the shell, `NEXT_PUBLIC_*` vars must be explicitly forwarded via `next.config.ts` `env:` block.

**`reactStrictMode: false`** in the presentation shell — intentional, do not enable. Some TBX endpoints are non-idempotent.

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
