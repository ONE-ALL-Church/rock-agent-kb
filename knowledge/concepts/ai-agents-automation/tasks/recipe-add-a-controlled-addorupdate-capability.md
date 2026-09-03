---
concept_id: ai-agents-automation
task_id: recipe-add-a-controlled-addorupdate-capability
title: Recipe: Add a controlled AddOrUpdate capability
generated: true
---

# Recipe: Add a controlled AddOrUpdate capability

An authorized user can create or edit one entity through a validated, auditable tool.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Attribute`

## Steps

1. Decide whether the same tool should support both create and update.
2. Accept an optional entity `IdKey`; treat its presence as update and absence as create.
3. Add explicit qualifier keys required for creation.
4. Retrieve available attributes before accepting attribute values.
5. Load existing entities with security checks or create through Rock’s managed entity infrastructure.
6. Validate required fields and state-dependent rules.
7. Apply attributes through reviewed helper or entity logic.
8. Save only when no validation errors remain.
9. Return a bounded full result with a compact history reference.
10. Read the entity back independently before reporting completion.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.LaunchWorkflow.cs
- https://www.youtube.com/watch?v=bu5nPeAVCAo
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflow.cs
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools
- https://www.youtube.com/watch?v=dpYJiOAiJYM
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/addorupdate-tools
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowSkill.GetWorkflowAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/WorkflowBuilderSkill.GetWorkflowActionTypeAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetBlockAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetSiteAvailableAttributes.cs
