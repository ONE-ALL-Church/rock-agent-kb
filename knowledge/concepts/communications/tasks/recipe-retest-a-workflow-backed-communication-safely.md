---
concept_id: communications
task_id: recipe-retest-a-workflow-backed-communication-safely
title: Recipe: Retest a workflow-backed communication safely
generated: true
---

# Recipe: Retest a workflow-backed communication safely

One intended communication action is exercised without broadly reopening unrelated workflow work.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Label`
- `Workflow`

## Entities And Tables

- `Label`
- `Workflow`

## Steps

1. Prefer a new test workflow instance.
2. If an existing marked test instance must be reused, preflight the exact recipient, action criteria, current template, action order and baseline side-effect counts.
3. Leave earlier setters, record-creation actions and unrelated communication actions complete.
4. Reopen only the target action and the minimum containing workflow state required by the reviewed procedure.
5. Save once through the supported Workflow Detail surface.
6. Inspect workflow logs and Communication History before considering any retry.
7. Verify exactly one intended communication, its recipient, rendered content and final workflow state.
8. Confirm no unrelated timestamps or records changed.

## Do Not Assume

- A workflow Status label alone determines activation.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/7d31f3f144c14b8a7d86bf7a41760d9d0a49fe07/Rock/Model/Workflow/Workflow/Workflow.Logic.cs
- https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline
- https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms
- https://community.rockrms.com/documentation/engagement/communications/email/email-integrations
- https://community.rockrms.com/documentation/engagement/communications/email/configure-email
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification
