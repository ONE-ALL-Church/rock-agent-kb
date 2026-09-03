---
concept_id: communications
task_id: recipe-bound-an-agent-that-can-draft-communications
title: Recipe: Bound an agent that can draft communications
generated: true
---

# Recipe: Bound an agent that can draft communications

An agent can assist with preparation without gaining unintended send or destructive authority.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. List the exact communication tasks the agent needs.
2. Enable only the required tools.
3. Separate draft, preview, audience-inspection, approval and send capabilities.
4. Leave send disabled when the task is drafting or analysis.
5. Omit destructive tools unless explicitly required.
6. Verify the Rock identity and permissions used by the integration.
7. Test denied operations as well as allowed ones.
8. Require action-time authorization before any external send.

## Do Not Assume

- Hiding a user-interface control removes the underlying tool, or enabling a tool bypasses Rock permissions.

## Source Links

- https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s
