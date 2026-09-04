---
name: behavior-planning
description: Plan behaviors and manage the test list at the start of tasks and RED phases.
recommended_model: gpt-5.4-mini
---

# /behavior-planning Skill

Use this skill at the start of a new feature or task, and at the beginning of each RED phase to manage the Test List.

---

## Core Rule
> **Plan behaviors, not test implementations.** Never write test code, assertions, or production code during planning.

---

## 1. Initial Plan (Task Start)

When starting a task:
1. **Analyze Requirements:** Identify the boundaries, happy path, edge cases, and error conditions. If you have a jira ticket access to it.
   Identify the files to minimize the context size using a local rag if configured as mcp or you have access to it. 
2. **Draft Test List:** Write a bulleted list of high-level behaviors ordered and adapted by the skill /tdd-outside-in .
3. **Format:** Use descriptive, domain-focused titles (e.g., `* Should reject order when inventory is zero`).
4. **Check the list of tests:** Check that the list of tests will change something in production, this means reading the tests of the files identified to be changed and compare them with the new tests suggested, if this is not clear enough reduce the list to the steps that will produce a change in production code.
5. **Validation:** Present the list to the user and wait for explicit approval before moving to Step 1 (RED).

---

## 2. Dynamic Update (When coming from a previous TDD cycle)

Before starting the next test cycle:
1. **Review:** Check the current Test List against what was learned in the previous GREEN/REFACTOR cycle and our current implementation and list of tests.
2. **Adapt:** 
   - Mark completed behaviors as done (`[x]`).
   - Add newly discovered scenarios or edge cases.
   - Strike through or remove obsolete scenarios from the test lists planned based on the previous review step done (YAGNI).
   - Read the files changed and the tests created in the code during the session and use that info to understand if it is required more iterations and behavioural tests. Also search for TODOS or other marks in the project of remaining things related to the current changes.
   - Remove notes with /notes skill already covered
   - Review the notes with /notes skill to take them into account to change the list of tests or plan refactors, ask the client which ones to take into account for this new cycle. 
3. **Select:** Explicitly state which behavior is being tested next.
4. **Validation:** Present the list to the user and wait for explicit approval before moving to Step 1 (RED).

---

## 3. Adding new tests to the list.
1. The user can add new tests to the behavioral list at any moment, just update teh tdd-state.json with the new test to do and take it into account for the next exeuction.
2. Dont interrupt the current cycle of TDD in this case, just run this in a subagent.


## Output Template

Always output the plan in this format:

### 📋 Behavior Test List
- [ ] Simple happy path scenario
- [ ] Boundary / Edge case scenario
- [ ] Error handling scenario

**Next behavior to test:** `[Insert selected scenario]`
**Ask:** "Does this list and the next target look good, or should we adjust?"

Pass to the main agent the list of current files that are probably affected by the behaviours planned.

# Subagent execution

Run this planning skill in a dedicated subagent. This is mandatory, including
when the behavior analysis appears small or straightforward. Return only the
concise behavior list, selected target, and decisions needed by the parent
agent.