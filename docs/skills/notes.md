---
name: notes
description: >
  You can use this skill to add notes to the current project in a notes file about the tests or things you want to review later.
  Or to read those notes to include something 
recommended_model: gpt-5-mini
---

## Append
Use this skill to append in a notes.md in the base folder, ideas or things that we need to check later.
This append can be executed at any time by the customer without interferring the main agent, so this needs to be done in a subagent.

## Review
Review that notes.md and take them into account for the project, for examle to affect the behaviour test list.
Once one element is checked by the customer and approved or discarded the element is removed from the notes.
There is a third option to defer the note to the future.

## Remove or update
The client can update or remove one note, identifying the note by the order or the text.