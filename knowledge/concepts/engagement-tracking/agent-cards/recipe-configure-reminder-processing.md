---
concept_id: engagement-tracking
task_id: recipe-configure-reminder-processing
title: Recipe: Configure Reminder processing
generated: true
---

# Recipe: Configure Reminder processing

A context-valid reminder produces the intended communication or workflow at its reminder date.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Attribute`

## Steps

1. Define the Reminder Type’s entity and security.
2. Choose Communication or Workflow notification.
3. Configure note inclusion and automatic completion deliberately.
4. For Communication, select the system communication in the Process Reminders job.
5. For Workflow, configure the workflow to receive the supplied reminder-related attributes.
6. Include the type in job processing and set any per-entity limit.
7. Test a bounded reminder and verify delivery or workflow launch, completion behavior and header count.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/additional-engagement-tools
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types
- https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs
- https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types
- https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Attribute/StepProgramStepTypeFieldAttribute.cs
- https://community.rockrms.com/ask/using/2824
