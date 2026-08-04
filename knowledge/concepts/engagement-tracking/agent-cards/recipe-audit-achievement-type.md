---
concept_id: engagement-tracking
task_id: recipe-audit-achievement-type
title: Recipe: Audit Achievement Type
generated: true
---

# Recipe: Audit Achievement Type

Sources: Add Achievement Types, Achievement Type Advanced Settings, `AchievementType.cs`.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Step`
- `Workflow`

## Entities And Tables

- `Step`
- `Workflow`

## Steps

1. Name, active state, category.
2. Component/entity type.
3. Source entity type.
4. Achiever entity type.
5. Target count.
6. Max accomplishments.
7. Over-achievement setting.
8. Prerequisites.
9. Start/success/failure workflows.
10. Badge/results/custom summary Lava.
11. Add Step on Success fields.
12. Attempt counts and sample attempts.
13. Version caveats.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps
- https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests
