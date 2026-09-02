# Copilot Instructions

## Instruction hierarchy

- Read the repository-root `AGENTS.md` first. It is the source of truth for repository-wide workflows, TDD, and skills.
- Before changing files, read the deepest applicable `AGENTS.md` and any project-local instruction files. They contain the authoritative architecture, commands, conventions, and validation rules for that project.
- More-specific instructions may add detail, but must not contradict the repository root or direct user instructions.
- Work from the relevant sub-project directory and use its documented commands.

## Project-specific guidance

- Identify the project containing the files you will change.
- Read the nearest `AGENTS.md`, followed by any project-local instruction files.
- Use `docs/project-map.md` as a human-maintained inventory only; it is not a substitute for project instructions.

## Cross-repository guardrails

- Preserve existing behavior and integration contracts, especially REST/OpenAPI contracts and Module Federation exposed or consumed modules.
- Never commit secrets, credentials, tokens, cookies, payment data, or PII. Do not add debugging logs containing sensitive data.
- Do not hand-edit generated output. Change its source specification or generator configuration and use the project's generation task.
- Prefer the smallest safe change. Keep domain boundaries and dependency direction intact.
- Add or update tests when behavior changes, using the project's prescribed test style.
- Run the narrowest relevant validation first and broaden it as required by the applicable project instructions.
- Do not use `data-testid` or alter existing selectors as a blanket rule: follow the applicable project's testing guidance and preserve production selectors unless explicitly asked otherwise.
- Use ALTO for new React-rendered UI where the project supports it; preserve legacy BAgel usage only where required for compatibility.
- Keep responses in English and concise.

## Conflicts and uncertainty

When instructions conflict, follow this order:

1. System or direct user instruction
2. Repository-root `AGENTS.md`
3. The deepest applicable project `AGENTS.md`
4. Project-local `.github` instructions and skills

If a conflict affects the implementation rather than wording or workflow, stop and ask for clarification instead of guessing.
