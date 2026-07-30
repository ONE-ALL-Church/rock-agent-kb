---
concept_id: security-permissions
task_id: recipe-answer-why-was-i-denied
title: Recipe: Answer “Why Was I Denied?”
generated: true
---

# Recipe: Answer “Why Was I Denied?”

Do not stop at direct `Auth` rows: Rock security includes inherited authority and code-level action checks, and the role inspector recipe explicitly warns that direct row listings do not account for inheritance (Rock Security, Security Role Permissions Inspector).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `GroupType`
- `Page`
- `Block`

## Entities And Tables

- `Group`
- `GroupType`
- `Page`
- `Block`

## Steps

1. Actor identified.
2. Requested action.
3. Object identified.
4. Direct rule result.
5. Inherited rule result.
6. Role membership state.
7. Version caveat checked.
8. Next remediation.

## Do Not Assume

- Do not stop at direct `Auth` rows: Rock security includes inherited authority and code-level action checks, and the role inspector recipe explicitly warns that direct row listings do not account for inheritance (Rock Security, Security Role Permissions Inspector).

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/developer/303---blast-off/rock-security
- https://community.rockrms.com/recipes/441
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools
- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
- https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns
