# AI Workflow

An opinionated, repository-aware workflow for using GitHub Copilot with
outside-in Test-Driven Development (TDD), evolutionary hexagonal architecture,
and project-specific agent guidance.

The repository is a workspace containing multiple application projects,
supporting tools, architecture documentation, and reusable Copilot skills.

## What this workflow provides

- **Outside-in TDD:** drive behavior from the entry point toward use cases and
  infrastructure.
- **Strict RED/GREEN/REFACTOR discipline:** write one test at a time, keep
  production code demanded by a failing test, and review refactors separately.
- **Architecture guidance:** evolve ports and domain services only when tests
  or adapters require them.
- **Test-quality rules:** use strict output-contract assertions, meaningful
  fixtures, and appropriate test doubles.
- **Project-aware assistance:** select the nearest `AGENTS.md` and local
  instructions before working in a project.
- **Optional semantic code search:** use Qdrant to navigate large codebases
  conceptually instead of relying only on literal search.

## Getting started

### Clone the workspace

```bash
git clone https://github.com/javier-lopez-fernandez_iagl/aiWorkflow.git
cd aiWorkflow
```

### Read the agent guidance

Start with the repository-root [`AGENTS.md`](AGENTS.md). It is the source of
truth for the workflow, TDD state, architecture rules, and available skills.

Before changing a project:

1. Identify the project directory.
2. Read its nearest `AGENTS.md`, if it has one.
3. Read any project-local Copilot instructions.
4. Run the commands documented by that project.

The root [`docs/project-map.md`](docs/project-map.md) is an inventory of
projects; project-local instructions remain authoritative.

## TDD workflow

The workflow is organized into explicit phases:

1. **PLAN:** define and order the behavior list.
2. **RED:** write exactly one failing test and show the failure.
3. **GREEN:** implement the minimum code needed to pass and run the affected
   tests.
4. **REFACTOR:** make one focused structural improvement without changing
   behavior.
5. **COMMIT:** commit the approved behavior using the repository commit rules.
6. **FINISHED:** run incremental mutation testing when all planned behaviors
   are complete.

The shared [`.tdd-state.json`](.tdd-state.json) file records the active phase,
behavior, approvals, validation, and commit state. Use the `tdd-state` skill
instead of inferring state from conversation history.

### Layer progression

```text
Entry point (HTTP / CLI / queue handler)
  -> Use case (application service)
  -> Persistence or external-service adapter
```

For frontend work, begin with the page or feature integration test, then move
to component and API-hook tests only when the outer test demands it.

## Skills catalog

Skills are available as project documentation in [`docs/skills/`](docs/skills/)
and as Copilot skill entries in [`.github/skills/`](.github/skills/). Invoke a
skill by its name, for example `/behavior-planning`.

| Skill | Purpose |
|---|---|
| [`behavior-planning`](docs/skills/behavior-planning.md) | Create and maintain the ordered behavior/test list. |
| [`tdd-outside-in`](docs/skills/tdd-outside-in.md) | Choose the outermost suitable test layer and avoid test explosion. |
| [`tdd-state`](docs/skills/tdd-state.md) | Maintain and validate `.tdd-state.json` across phase transitions. |
| [`red-phase`](docs/skills/red-phase.md) | Execute one RED cycle with exactly one failing test. |
| [`green-phase`](docs/skills/green-phase.md) | Implement the minimum production code for the current failing test. |
| [`yagni`](docs/skills/yagni.md) | Remove speculative code during RED and GREEN. |
| [`refactor`](docs/skills/refactor.md) | Apply one focused behavior-preserving refactor. |
| [`test-quality`](docs/skills/test-quality.md) | Improve fixtures, naming, signal/noise, and strict serialized assertions. |
| [`test-doubles`](docs/skills/test-doubles.md) | Choose between dummies, stubs, fakes, spies, and mocks. |
| [`backend-tests`](docs/skills/backend-tests.md) | Kotlin/Spring test patterns for controllers, use cases, JPA, and HTTP adapters. |
| [`frontend-tests`](docs/skills/frontend-tests.md) | React/Next.js testing with RTL, child mocks, and MSW. |
| [`hexagonal-arch`](docs/skills/hexagonal-arch.md) | Evolve ports, domain services, and dependency direction safely. |
| [`anemic-use-case-check`](docs/skills/anemic-use-case-check.md) | Detect use cases that only proxy calls without business behavior. |
| [`semantic-search`](docs/skills/semantic-search.md) | Index and search code with Qdrant for conceptual queries. |
| [`mutation-testing`](docs/skills/mutation-testing.md) | Run incremental mutation testing after the behavior list is complete. |
| [`notes`](docs/skills/notes.md) | Capture follow-up ideas and review items without interrupting the main flow. |
| [`commit`](docs/skills/commit.md) | Apply commit format, ticket scope, validation, and commit separation rules. |
| [`migrate-controller-stack`](docs/skills/migrate-controller-stack.md) | Migrate a controller, its lower layers, and full-stack tests between services. |

## Optional semantic code search

Semantic search is optional and is useful for conceptual navigation in large
projects.

### Start Qdrant

```bash
docker run -d --name qdrant \
  -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant
```

### Install and configure the MCP server

```bash
npm install -g qdrant-rag-mcp
```

Add the server to `~/.copilot/mcp.json`:

```json
{
  "mcpServers": {
    "qdrant-rag": {
      "command": "npx",
      "args": ["qdrant-rag-mcp"],
      "env": {
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

Index a specific sub-project with the `index_codebase` tool, following the
collection map and exclusions described by the `semantic-search` skill. Do not
index the workspace root.

## Repository layout

| Path | Contents |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Repository-wide agent, TDD, architecture, and skill rules. |
| [`AGENTS-public.md`](AGENTS-public.md) | Public TDD guidance and testing principles. |
| [`docs/skills/`](docs/skills/) | Full reference documentation for reusable skills. |
| [`.github/skills/`](.github/skills/) | Copilot-discoverable skill definitions. |
| [`docs/project-map.md`](docs/project-map.md) | Inventory of application projects. |
| [`.tdd-state.json`](.tdd-state.json) | Shared state contract for active TDD work. |

## Existing project directories

The workspace includes services, BFFs, frontends, infrastructure repositories,
experiments, and architecture documentation. Some projects have their own
`AGENTS.md` and local skills. Always follow the deepest applicable guidance
when working inside one of them.

## Maintainer

Developed and maintained by
[javierlopezfernandez](https://github.com/javier-lopez-fernandez).
