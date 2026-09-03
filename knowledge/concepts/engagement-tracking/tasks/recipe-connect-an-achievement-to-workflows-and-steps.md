---
concept_id: engagement-tracking
task_id: recipe-connect-an-achievement-to-workflows-and-steps
title: Recipe: Connect an Achievement to workflows and Steps
generated: true
---

# Recipe: Connect an Achievement to workflows and Steps

A successful Achievement produces the intended follow-up and journey record.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `StepProgram`
- `StepType`
- `Step`
- `Workflow`

## Entities And Tables

- `StepProgram`
- `StepType`
- `Step`
- `Workflow`

## Steps

1. Define the Achievement source, target and success conditions.
2. Choose either overachievement or capped accomplishments.
3. Configure start, success and failure workflows as needed.
4. Enable Add Step on Success.
5. Select the Step Program, Step Type and status.
6. Confirm that the target Step’s prerequisites and Allow Multiple behavior match recurring Achievement behavior.
7. Test start, success and failure paths with bounded records.
8. Verify the attempt, workflow result and generated Step independently.

## Do Not Assume

- Achievement success overrides Step prerequisites or repeat limits. (Add Achievement Types, Achievement Type Advanced Settings, Configure Steps in Achievement Types)

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/steps-charts
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings
