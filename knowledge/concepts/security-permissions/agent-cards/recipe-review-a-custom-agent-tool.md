---
concept_id: security-permissions
task_id: recipe-review-a-custom-agent-tool
title: Recipe: Review A Custom Agent Tool
generated: true
---

# Recipe: Review A Custom Agent Tool

Source: Writing Custom Tools.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Confirm who can run the tool.
2. Confirm tool security before attaching to an agent.
3. For public agents, include only stranger-safe tools.
4. Do not return raw integer IDs to the model; use IdKey and convert internally.
5. Validate input.
6. Avoid exposing sensitive fields.
7. Re-check permissions server-side before mutation.

## Do Not Assume

- Do not return raw integer IDs to the model; use IdKey and convert internally.
- Avoid exposing sensitive fields.

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools
