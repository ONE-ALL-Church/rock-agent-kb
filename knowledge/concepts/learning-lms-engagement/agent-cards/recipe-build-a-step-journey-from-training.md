---
concept_id: learning-lms-engagement
task_id: recipe-build-a-step-journey-from-training
title: Recipe: Build A Step Journey From Training
generated: true
---

# Recipe: Build A Step Journey From Training

Connect training completion to an engagement journey only through explicit workflows, data views, or step-writing logic.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Learning Class Activity Completion`
- `Learning Program Completion`
- `Step Program`
- `Step Type`
- `Step`
- `Data View`
- `Workflow`

## Entities And Tables

- `LearningClassActivityCompletion`
- `LearningProgramCompletion`
- `StepProgram`
- `StepType`
- `Step`
- `DataView`
- `Workflow`

## Steps

1. Define which completion event should create or update the engagement step.
2. Inspect the Step Program and Step Type before configuring workflow or data view logic.
3. Verify prerequisites, badge or achievement display behavior, and reporting scope.
4. Test with a known learner and confirm both completion and Step records exist.
5. Document the boundary between training history and engagement journey state.

## Do Not Assume

- Do not assume a completed training automatically creates a Step.
- Do not troubleshoot badge display until the Step row and Step Type are verified.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/39
- https://www.triumph.tech/resources/github-spotlight-11142025
- https://community.rockrms.com/rocku/engagement
- https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms
- https://community.rockrms.com/rocku/engagement/steps-badges
- https://community.rockrms.com/rocku/engagement/adding-steps
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/use-group-requirement-jobs
- https://community.rockrms.com/documentation/bookcontent/43/354
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/view-group-requirements
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/intro-to-group-requirements
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/ModelMap
