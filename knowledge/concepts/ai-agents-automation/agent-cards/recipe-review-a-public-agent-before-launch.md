---
concept_id: ai-agents-automation
task_id: recipe-review-a-public-agent-before-launch
title: Recipe: Review a Public agent before launch
generated: true
---

# Recipe: Review a Public agent before launch

The public surface exposes only reviewed, non-sensitive and non-destructive capabilities.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Inventory every attached skill and tool.
2. Remove all capabilities not required by the public use case.
3. Review each tool’s parameters, return fields and reference routes.
4. Confirm that entity authorization and audience sanitization occur in code.
5. Test anonymous and least-privileged access.
6. Test prompt injection, identifier guessing, broad listing and requests for internal data.
7. Confirm write, send, delete and administration operations are absent.
8. Review logs and remediate every unexpected call or field.
9. Repeat the review after version, plugin, tool or prompt changes.

## Do Not Assume

- Friendly agent instructions prevent hostile requests.
- Public mode alone establishes the organization’s privacy policy.
- A successful normal-path test covers adversarial use.

## Source Links

- https://community.rockrms.com/developer/ai-agents/agents
