---
name: hexagonal-arch
description: >
  Use when designing folder structure, deciding whether to extract a port or domain service,
  discussing hexagonal or onion architecture, or reviewing whether domain classes have
  framework imports. Covers evolutionary design, port naming, and ArchUnit rules.
---

See the full guide at `docs/tdd/hexagonal-arch.md`.

Key rules:
- Do not design the full architecture before the first test — let it emerge.
- Extract a port only when a second adapter appears or a test demands the boundary.
- Domain must have zero Spring/JPA imports. ArchUnit enforces this.
- Do not create a domain service that is a pure proxy — wait until tests demand logic there.
- Port names are implementation-agnostic; adapter names reveal the implementation.
