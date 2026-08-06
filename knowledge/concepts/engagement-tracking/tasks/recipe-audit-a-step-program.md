---
concept_id: engagement-tracking
task_id: recipe-audit-a-step-program
title: Recipe: Audit A Step Program
generated: true
---

# Recipe: Audit A Step Program

Primary sources: Edit Step Programs, Edit Step Types.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `DataView`
- `Workflow`
- `Attribute`
- `PersonAlias`
- `Campus`

## Entities And Tables

- `Person`
- `StepProgram`
- `StepType`
- `Step`
- `DataView`
- `Workflow`
- `Attribute`
- `PersonAlias`
- `Campus`

## Steps

1. Program name, ID/GUID if available, active state, category.
2. Step Types and active state.
3. Statuses and which count as completion.
4. Completion flow and prerequisites.
5. Attributes.
6. Workflow triggers.
7. Badge configuration.
8. Chart counts.
9. Sample person verification.
10. Reports/Data Views depending on the program.
11. Version caveats.
12. Confirm each required Step Type has a completed Step.
13. Confirm statuses are marked as completion statuses.
14. Confirm inactive Step Types should or should not count.
15. Confirm person alias identity.
16. Confirm campus expectations.
17. Inspect the Step Program Completion model in the live instance.
18. Compare source-code rule in `StepProgramCompletion.cs`.

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
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts
