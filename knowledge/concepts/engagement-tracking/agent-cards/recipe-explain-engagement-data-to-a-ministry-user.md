---
concept_id: engagement-tracking
task_id: recipe-explain-engagement-data-to-a-ministry-user
title: Recipe: Explain Engagement Data To A Ministry User
generated: true
---

# Recipe: Explain Engagement Data To A Ministry User

Then ask for the operational decision they need to make. That determines the correct data source.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Step`

## Entities And Tables

- `Attendance`
- `Step`

## Steps

1. Steps show where someone is in a configured ministry path.
2. Streaks show consistency over eligible attendance periods.
3. Assessments show self-assessment results and history.
4. Achievements show whether a configured goal has been attempted or met.
5. Reports depend on which of those definitions the ministry means by “engaged.”

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps
- https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/StepProgramStepTypePicker.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
