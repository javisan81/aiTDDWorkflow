---
name: yagni
description: >
  Run in the RED phase (on the test just written) and in the GREEN phase (on the production
  code just written). Prevents speculative code, over-engineering, and YAGNI violations
  before they are committed.
---

# YAGNI Check

Run this checklist **twice** in every TDD cycle.

---

## RED phase — on the test you just wrote

Ask these questions before showing the failing test to the user:

- Does the test assert **exactly one** observable behaviour? If it asserts more, split it.
- Are you using `any()` matchers in mocks? → Replace with the exact value the production code will pass.
- Does the test access **fake internals** (e.g. `repository.savedValue`)? → Use the port interface method instead (e.g. `repository.find()`).
- Does the test set up data that **no assertion checks**? → Remove it.
- Does the test import or reference a class that **does not exist yet AND is not the one under test**? → You may be testing too many things at once.
- If a test passes but we are in red phase there was a previous production code doing too much, that previous thing was a yagni. Learn from that case.

---

## GREEN phase — on the production code you just wrote

For **every line** of production code, ask: *"Which currently-failing test demanded this exact line?"*

If you cannot point to the test → **delete the line.**



Common violations to check:

| Violation | Example | Fix |
|-----------|---------|-----|
| Exception handling without a test | `try/catch(DataAccessException)` before a test proves it | Delete; add the test first |
| Response body / field not asserted | `mapOf("status" to "ok")` with no test checking "status" | Delete the field |
| Conditional with only one branch tested | `if (x) { ... } else { ... }` but only one path has a test | Write a constant first |
| Abstraction extracted before duplication | extracting a shared method when only one caller exists | Inline it |
| Method not called by any test or production code | helper added "for future use" | Delete |
| Constructor parameter not required by any test | extra field added speculatively | Remove |

---

## REFACTOR phase — dead props/params must be removed end-to-end

When a behaviour change makes a prop/param unnecessary (e.g. a component now iterates real
segments and no longer needs an aggregate count prop), removing it is not optional cleanup —
it is a YAGNI violation to leave it in "just in case". Trace the **whole call chain** and
remove it everywhere: the prop's own type, every parent component that passes it down, and
any now-unused helper that only existed to compute it. A prop removal is incomplete if any
call site still passes the old value or any helper is now unreferenced.
## Subagent execution

Run this checklist in a dedicated subagent. This is mandatory, including when
the checklist appears small or straightforward. Return only the YAGNI decision
and concise evidence. If validation requires Gradle tests, use `/gradle-tests`
and avoid returning raw command output.
