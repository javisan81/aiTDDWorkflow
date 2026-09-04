---
name: green-phase
description: Execute one TDD GREEN cycle.
---

# GREEN Phase

This skill performs only the GREEN action selected by `AGENTS.md`, run it in the main agent, **all steps are mandatory dont skip any step**:

1. Write the **minimum production code needed to pass the current failing test**. Dont implement methods of a class implementing an interface that is not needed to pass the test. If you need to implement something in prod, because the compiler dont pass, just make the signature to pass and use todos or nulls or whatever you want that is the minimum thing to compile. It is **forbidden** to implement code that is not required by the test we are trying to fix.
2. Run all existing tests for the affected project, we are only interested if tests passes and reasons to fail in case they fail, so adapt the command with this in mind, try to execute the command once. As there are big repos wait for enough time the response at least 5mins and check the errors.
3. Confirm the suite is green, we dont care about coverage right now.
4. In case there are old tests failing and **contradicting** the current behaviour, and the new test passes, try first to adapt their scenarios maintaining the intention of the test. In case is completely against change the name of the test or remove it if it is not needed anymore. In case of doubt ask the client.
5. If we are working on backend and we have clases that require beans to be injected, and if we use interfaces in our test create a bean with a todo implementation. If the class is placed in domain use configuration files to create beans.
6. Run `/yagni` checklist on the production code just written before showing it to the user, to be sure your code is the minimum one to make the test to pass. YAGNI can be run in parallel with previous step.
7. If you are forced to implement a class of a mocked interface in the test create it with todo.

Do not add tests, refactor, or implement unrequested behavior. Return only the
production files changed, concise test evidence, and any blocker.
