---
concept_id: engagement-tracking
task_id: recipe-build-an-assessment-result-segment
title: Recipe: Build an assessment-result segment
generated: true
---

# Recipe: Build an assessment-result segment

A person Data View identifies people with a specified supported assessment result.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`
- `Group`
- `Attribute`

## Entities And Tables

- `Person`
- `DataView`
- `Group`
- `Attribute`

## Steps

1. Select the assessment and exact result measurement or attribute.
2. Choose the documented rating or result condition.
3. Build the person Data View filter.
4. Validate sample included and excluded records.
5. Use the resulting population for the separately governed grouping or reporting task.

## Do Not Assume

- Similar-looking measurements across different assessments have the same meaning. (Intro to Assessments, Emotional Intelligence, Conflict Profile)

## Source Links

- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
- https://community.rockrms.com/documentation/engagement/assessments/available-assessments
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types
- https://community.rockrms.com/documentation/engagement/assessments
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Attribute/StepProgramStepTypeFieldAttribute.cs
