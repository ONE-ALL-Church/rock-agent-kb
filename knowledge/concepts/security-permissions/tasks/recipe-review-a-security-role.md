---
concept_id: security-permissions
task_id: recipe-review-a-security-role
title: Recipe: Review A Security Role
generated: true
---

# Recipe: Review A Security Role

Complete Review A Security Role with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`

## Entities And Tables

- `Person`
- `Workflow`

## Steps

1. Role name.
2. Purpose/description.
3. Active members.
4. Former/inactive members.
5. Direct auth entries.
6. Sensitive domains granted.
7. Deny rules.
8. Person-specific overlaps.
9. API keys or workflows depending on the role.
10. Recommended cleanup.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools
- https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns
