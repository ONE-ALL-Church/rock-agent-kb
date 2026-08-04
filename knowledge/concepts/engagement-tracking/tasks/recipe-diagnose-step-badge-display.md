---
concept_id: engagement-tracking
task_id: recipe-diagnose-step-badge-display
title: Recipe: Diagnose Step Badge Display
generated: true
---

# Recipe: Diagnose Step Badge Display

Source: Steps Badges.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `Block`

## Entities And Tables

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `Block`

## Steps

1. Badge list under `Admin Tools > Settings > General > Badges`.
2. Entity Type is Person.
3. Badge Type is Steps.
4. Step Program selected.
5. Step Type Show Count on Badge settings.
6. Person has expected Step records.
7. Security.
8. Person Profile block/zone where badges render.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps
- https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/StepProgramStepTypePicker.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
