---
concept_id: engagement-tracking
task_id: recipe-configure-a-step-journey-with-reliable-completion-signals
title: Recipe: Configure a Step journey with reliable completion signals
generated: true
---

# Recipe: Configure a Step journey with reliable completion signals

A Step Program whose order, prerequisites and completion semantics match the intended journey.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `Block`
- `Attribute`
- `Workflow`

## Entities And Tables

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `Block`
- `Attribute`
- `Workflow`

## Steps

1. Define the journey’s Step Types and decide whether sequence is required, preferred or display-only.
2. Select the corresponding Completion Flow.
3. Configure statuses and identify which statuses are complete.
4. Configure each type’s prerequisites, repeatability and spans-time behavior.
5. Add only the Step Attributes needed for the operational record; enable Show in Grid or Show on Bulk where appropriate.
6. Test one participant record with the intended date and status combination.
7. Verify the change in Person History.
8. Inspect the Step’s current status.
9. Confirm that the status is configured as an **Is Complete** status in the Step Program.
10. Confirm that both the completion date and completion status are present.
11. If a workflow should have launched, inspect the program- or type-level trigger and installed Rock version.
12. Stop when both completion signals are correct and the expected downstream behavior has been rechecked. (Edit Step Programs)

## Do Not Assume

- A completion date alone means complete.
- A prerequisite survives moving the Step Type to another program.

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/steps-charts
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
