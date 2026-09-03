---
concept_id: ai-agents-automation
task_id: recipe-launch-a-workflow-through-an-agent
title: Recipe: Launch a workflow through an agent
generated: true
---

# Recipe: Launch a workflow through an agent

The agent launches one permitted workflow with valid attribute values and verifies the resulting record.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `Workflow`
- `Attribute`

## Steps

1. Lookup the permitted workflow types.
2. Resolve the requested type to an `IdKey`.
3. Retrieve its available attributes and formatting requirements.
4. Gather missing required values from the user.
5. Confirm any consequential side effects.
6. Call the launch action once.
7. Capture the returned workflow reference.
8. Retrieve the workflow and verify activation, status and supplied values.
9. Produce a durable handoff when another person or process must continue the work.
10. Confirm the workflow type exists and is active.
11. Confirm the current person is authorized for it.
12. Confirm the Workflow skill is attached to the agent.
13. Check whether the agent’s configuration limits launchable workflow types.
14. Retrieve AvailableAttributes for the workflow type before supplying values.
15. Inspect the action result and logs for validation errors.
16. Read the workflow back to verify activation and supplied values.
17. Do not infer downstream completion merely because launch succeeded.

## Do Not Assume

- Do not infer downstream completion merely because launch succeeded.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.LaunchWorkflow.cs
- https://www.youtube.com/watch?v=bu5nPeAVCAo
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflow.cs
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools
- https://www.youtube.com/watch?v=dpYJiOAiJYM
- https://community.rockrms.com/developer/ai-agents/agents/context-anchors
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/PersonSkill.GetPersonAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflowAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowBuilderSkill.GetWorkflowActionTypeAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetBlockAvailableAttributes.cs
