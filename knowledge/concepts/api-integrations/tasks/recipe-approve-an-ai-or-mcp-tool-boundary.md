---
concept_id: api-integrations
task_id: recipe-approve-an-ai-or-mcp-tool-boundary
title: Recipe: Approve An AI Or MCP Tool Boundary
generated: true
---

# Recipe: Approve An AI Or MCP Tool Boundary

A tool exposes one managed Rock capability with bounded inputs, results, and authorization.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Record the shipped Rock version and feature status.
2. Identify whether the integration is Chat or MCP and Internal or Public.
3. Identify the current-person, agent, skill, and tool authorization layers.
4. Give the tool a clear verb-and-entity name.
5. Define explicit sanitized parameters and use IdKeys where supported.
6. Route data operations through managed Rock code.
7. Remove arbitrary SQL, unrestricted database access, and unused Lava commands.
8. Shape the smallest structured result needed by the model.
9. Verify OAuth client, token scope, renewal, and revocation behavior if using MCP.
10. Exercise allowed, denied, malformed, and excessive-result cases.
11. Inspect built-in tool logs for calls, inputs, and results.
12. Confirm that organization policy is versioned in the appropriate Rock or external-harness layer.
13. Stop if security depends on the prompt telling the model not to misuse an available capability.
14. Disable or withhold the tool from the agent until its boundary is understood.
15. Identify the current person, agent, skill, tool, and channel: Chat or MCP, Internal or Public.
16. Confirm that authorization is enforced by managed Rock code.
17. Check whether the tool contains open-ended SQL or unrestricted data access.
18. Inspect tool parameters, enabled commands, result shape, and logs.
19. Replace raw integer identifiers with IdKeys where supported.
20. Verify the released version’s OAuth, scope, permission, and revocation behavior.
21. Stop if safe operation depends on trusting model instructions instead of enforced authorization. (AI Summit; RockIQ Q&A)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/security/person-tokens/configure-person-tokens
- https://www.youtube.com/watch?v=UvW68dZBcJ8
- https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s
