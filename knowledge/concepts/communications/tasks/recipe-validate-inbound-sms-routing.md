---
concept_id: communications
task_id: recipe-validate-inbound-sms-routing
title: Recipe: Validate inbound SMS routing
generated: true
---

# Recipe: Validate inbound SMS routing

One controlled inbound message reaches exactly the intended conversation, reply or workflow path.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Confirm the provider number and Rock System Phone Number.
2. Confirm the SMS transport and medium.
3. Confirm the webhook targets the intended endpoint or pipeline.
4. Review pipeline actions and filters in execution order.
5. Review workflow inputs and security for any workflow-launch action.
6. Decide whether automated replies must be saved to history.
7. Send one controlled inbound message.
8. Verify the expected conversation, reply, workflow and retained history.
9. Confirm no unrelated action executed.
10. Repeat with one negative-filter case when routing depends on keywords.

## Do Not Assume

- An unfiltered action is harmless; it applies to every message reaching it.

## Source Links

- https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline
- https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms
- https://github.com/SparkDevNetwork/Rock/blob/7d31f3f144c14b8a7d86bf7a41760d9d0a49fe07/Rock/Model/Workflow/Workflow/Workflow.Logic.cs
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification
