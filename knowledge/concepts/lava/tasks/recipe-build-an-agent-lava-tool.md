---
concept_id: lava
task_id: recipe-build-an-agent-lava-tool
title: Recipe: Build An Agent Lava Tool
generated: true
---

# Recipe: Build An Agent Lava Tool

```json

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Name: specific action, not generic.
2. Description: tells the agent when to call it.
3. Parameters: typed, required only when necessary.
4. Prompt: Lava template with parameterized SQL or entity commands.
5. Output: JSON with stable keys.
6. Commands: minimal.
7. Security: same review as any Lava endpoint.
8. Failure: include status and message fields.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools
