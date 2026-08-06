---
concept_id: security-permissions
task_id: recipe-review-a-permission-change-request
title: Recipe: Review A Permission Change Request
generated: true
---

# Recipe: Review A Permission Change Request

Then implement the smallest change and test.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Is this access temporary or durable?
2. Does an existing role match?
3. Does the requested action require View, Edit, Administrate, Approve, Delete, Refund, or ManageMembers?
4. Is the data sensitive?
5. Is there a lower-scope object?
6. Does this require workflow/report/API changes too?
7. Confirm the rule was saved.
8. Confirm it was saved on the correct entity.
9. Confirm action verb.
10. Confirm role membership.
11. Confirm user logged out/in if membership/session is stale.
12. Check direct deny rules.
13. Check inheritance.
14. Check cache/message-bus state in multi-node environments.
15. Check custom code path.
16. Test with another controlled account.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs
- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools
- https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn
- https://community.rockrms.com/rocku/groups/group-security
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs
