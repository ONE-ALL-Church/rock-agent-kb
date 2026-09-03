---
concept_id: engagement-tracking
task_id: recipe-automate-step-completion-from-a-data-view
title: Recipe: Automate Step completion from a Data View
generated: true
---

# Recipe: Automate Step completion from a Data View

The Steps Automation job creates or completes qualifying records while preserving journey rules.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `StepType`
- `Step`
- `DataView`
- `Block`
- `StepProgram`
- `Workflow`

## Entities And Tables

- `Person`
- `StepType`
- `Step`
- `DataView`
- `Block`
- `StepProgram`
- `Workflow`

## Steps

1. Build and validate the person Data View.
2. Assign it as the Step Type’s Auto-Complete Data View.
3. Inspect prerequisites and Allow Multiple.
4. Run or wait for the configured Steps Automation job according to the installation’s operating procedure.
5. Verify qualifying, prerequisite-blocked and already-completed examples.
6. Inspect the Step’s current status.
7. Confirm that the status is configured as an **Is Complete** status in the Step Program.
8. Confirm that both the completion date and completion status are present.
9. If a workflow should have launched, inspect the program- or type-level trigger and installed Rock version.
10. Stop when both completion signals are correct and the expected downstream behavior has been rechecked. (Edit Step Programs)

## Do Not Assume

- Every person in the Data View receives a new record; prerequisites and repeat limits remain active. (Edit Step Types)

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals
- https://community.rockrms.com/documentation/engagement/steps/steps-charts
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
