---
concept_id: platform-configuration
task_id: recipe-design-a-bounded-rock-agent-tool
title: Recipe: Design a bounded Rock agent tool
generated: true
---

# Recipe: Design a bounded Rock agent tool

An authorized tool performs one clear task and returns a controlled result.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Define the underlying task and current-person authorization boundary.
2. Decide whether the capability belongs in a Rock tool, Rock skill, or external organization skill.
3. Name the tool with a clear verb and entity.
4. Define explicit, sanitized parameters.
5. Use IdKeys rather than raw integer identifiers in agent context.
6. Choose a bounded result shape.
7. For Lava, return a structured `AgentToolResult`.
8. Use reviewed static logic where database access is necessary; do not expose arbitrary SQL execution.
9. Enable only the tool required for the agent and audience.
10. Exercise success, empty, invalid, unauthorized, and oversized-result cases.
11. Inspect tool logs for calls, inputs, and outputs.
12. Version the tool and associated business-rule instructions.
13. Check whether the tool name clearly expresses a verb and entity.
14. Check parameter names, descriptions, and sanitization.
15. Replace broad results with a bounded result shape.
16. Review the agent, skill, and tool authorization layers.
17. Inspect built-in tool logs for the actual call, input, and result.
18. Remove open-ended SQL execution capability.
19. Re-test with the current-person security context.

## Do Not Assume

- Use reviewed static logic where database access is necessary; do not expose arbitrary SQL execution.

## Source Links

- https://www.youtube.com/watch?v=c-wycR9HEuQ
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://www.youtube.com/watch?v=UvW68dZBcJ8
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
