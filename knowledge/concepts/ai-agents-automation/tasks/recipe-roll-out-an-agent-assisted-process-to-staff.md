---
concept_id: ai-agents-automation
task_id: recipe-roll-out-an-agent-assisted-process-to-staff
title: Recipe: Roll out an agent-assisted process to staff
generated: true
---

# Recipe: Roll out an agent-assisted process to staff

Staff understand the approved use case, review boundary and authoritative Rock workflow before volunteer rollout.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Workflow`

## Entities And Tables

- `Group`
- `Workflow`

## Steps

1. Document the approved tasks and prohibited actions.
2. Assign role-specific training through the configured LMS where available.
3. Demonstrate how to verify generated output against Rock records.
4. Provide a short video before any interface change.
5. Require staff completion before expanding access.
6. Pilot with a small staff group and review tool logs and data quality.
7. Correct the process and training.
8. Train volunteers only after staff can support the workflow consistently.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.youtube.com/watch?v=bu5nPeAVCAo
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.LaunchWorkflow.cs
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflow.cs
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools
- https://www.youtube.com/watch?v=dpYJiOAiJYM
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflowAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowBuilderSkill.GetWorkflowActionTypeAvailableAttributes.cs
- https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s
