---
concept_id: ai-agents-automation
task_id: recipe-diagnose-incorrect-tool-selection
title: Recipe: Diagnose incorrect tool selection
generated: true
---

# Recipe: Diagnose incorrect tool selection

The model consistently chooses the intended tool for representative requests.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Capture a minimal failing prompt.
2. Inspect the agent’s available skills and tools.
3. Compare names, purposes, prerequisites, parameter descriptions and return descriptions.
4. Remove overlapping or unused tools from the test agent.
5. Add temporary debugging instructions asking which tools were considered.
6. Adjust the narrowest responsible instruction or schema description.
7. Retest the failing prompt, close variations and an intentionally ambiguous request.
8. Remove temporary debugging instructions before production use.
9. Review tool logs to confirm actual calls.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/debugging-tools
