---
concept_id: engagement-tracking
task_id: recipe-bulk-record-a-step
title: Recipe: Bulk-record a Step
generated: true
---

# Recipe: Bulk-record a Step

Multiple selected people receive the intended Step data without silently losing per-person attribute differences.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `Attribute`
- `DataView`

## Entities And Tables

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `Attribute`
- `DataView`

## Steps

1. Choose either selected-person grid update or Step Program/Step Type bulk entry.
2. Confirm the target program, type, status and applicable date fields.
3. Apply shared attributes only when Show on Bulk is enabled and one value is correct for every selected person.
4. Enter differing attribute values separately for each person.
5. Verify sample records and their profile history.
6. Confirm the person currently qualifies for the Auto-Complete Data View.
7. Confirm the Steps Automation job has processed the Step Type.
8. Inspect unmet prerequisite Steps.
9. If a record already exists, inspect **Allow Multiple** before expecting another occurrence.
10. Do not assume Data View membership overrides prerequisites or repeat limits. (Edit Step Types)

## Do Not Assume

- Do not assume Data View membership overrides prerequisites or repeat limits.

## Source Links

- https://community.rockrms.com/documentation/engagement/steps/fundamentals
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/steps-charts
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
