---
name: commit
description: >
  Use every time a commit is about to be made. Covers commit format, mandatory ticket scope,
  when to commit separately, pre-commit checks, and the co-author trailer.
---

See the full guide at `docs/tdd/commit.md`.

Key rules:
- Ticket number is mandatory as the scope — ask before committing if unknown.
- Format code before committing (ktlintFormat / npm run lint).
- Run all tests and verify the application boots before committing.
- One commit per GREEN. Infrastructure commits are separate from feature commits.
- Always append the Co-authored-by trailer.
