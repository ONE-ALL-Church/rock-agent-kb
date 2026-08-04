---
concept_id: engagement-tracking
task_id: recipe-verify-assessment-request-flow
title: Recipe: Verify Assessment Request Flow
generated: true
---

# Recipe: Verify Assessment Request Flow

Sources: Send Requests, Retake Assessments, View Assessment History.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`
- `Attribute`

## Entities And Tables

- `Person`
- `DataView`
- `Attribute`

## Steps

1. Assessment Type settings.
2. Retake interval.
3. Requires request setting.
4. Person Profile Actions menu.
5. Request message.
6. Person Profile History.
7. Completion status.
8. Result attributes.
9. Data View search.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history
- https://www.triumph.tech/resources/sparks-top-8-personality-assessments
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments/disc-personality-assessment
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Attribute/StepProgramStepTypeFieldAttribute.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs
