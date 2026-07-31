---
name: behavior-planning
description: Plan behaviors and manage the test list at the start of tasks and RED phases.
---

# /behavior-planning Skill

Use this skill at the start of a new feature or task, and at the beginning of each RED phase to manage the Test List.

---

## Core Rule
> **Plan behaviors, not test implementations.** Never write test code, assertions, or production code during planning.

---

## 1. Initial Plan (Task Start)

When starting a task:
1. **Analyze Requirements:** Identify the boundaries, happy path, edge cases, and error conditions.
2. **Draft Test List:** Write a bulleted list of high-level behaviors ordered by complexity (simplest first).
3. **Format:** Use descriptive, domain-focused titles (e.g., `* Should reject order when inventory is zero`).
4. **Validation:** Present the list to the user and wait for explicit approval before moving to Step 1 (RED).

---

## 2. Dynamic Update (Start of each RED phase)

Before starting the next test cycle:
1. **Review:** Check the current Test List against what was learned in the previous GREEN/REFACTOR cycle and our current implementation and list of tests.
2. **Adapt:** 
   - Mark completed behaviors as done (`[x]`).
   - Add newly discovered scenarios or edge cases.
   - Strike through or remove obsolete scenarios (YAGNI).
3. **Select:** Explicitly state which behavior is being tested next.

---

## Output Template

Always output the plan in this format:

### 📋 Behavior Test List
- [ ] Simple happy path scenario
- [ ] Boundary / Edge case scenario
- [ ] Error handling scenario

**Next behavior to test:** `[Insert selected scenario]`
**Ask:** "Does this list and the next target look good, or should we adjust?"