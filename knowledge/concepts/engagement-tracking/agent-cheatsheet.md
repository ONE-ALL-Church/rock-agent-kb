---
concept_id: engagement-tracking
title: Engagement Tracking Agent Cheatsheet
generated: true
---

# Engagement Tracking Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Configure a Step journey with reliable completion signals](tasks/recipe-configure-a-step-journey-with-reliable-completion-signals.md) | `Person`, `StepProgram`, `StepType`, `Step`, `Block`, `Attribute`, `Workflow` | `Person`, `StepProgram`, `StepType`, `Step`, `Block`, `Attribute`, `Workflow` |
| [Recipe: Bulk-record a Step](tasks/recipe-bulk-record-a-step.md) | `Person`, `StepProgram`, `StepType`, `Step`, `Attribute`, `DataView` | `Person`, `StepProgram`, `StepType`, `Step`, `Attribute`, `DataView` |
| [Recipe: Automate Step completion from a Data View](tasks/recipe-automate-step-completion-from-a-data-view.md) | `Person`, `StepType`, `Step`, `DataView`, `Block`, `StepProgram`, `Workflow` | `Person`, `StepType`, `Step`, `DataView`, `Block`, `StepProgram`, `Workflow` |
| [Recipe: Build a Streak Type safely](tasks/recipe-build-a-streak-type-safely.md) | `Person`, `Page` | `Person`, `Page` |
| [Recipe: Correct one person’s streak](tasks/recipe-correct-one-person-s-streak.md) | `Attendance`, `Person` | `Attendance`, `Person` |
| [Recipe: Rebuild a Streak with a controlled boundary](tasks/recipe-rebuild-a-streak-with-a-controlled-boundary.md) | `Attendance`, `Person` | `Attendance`, `Person` |
| [Recipe: Request and monitor assessments](tasks/recipe-request-and-monitor-assessments.md) | `Person` | `Person` |
| [Recipe: Build an assessment-result segment](tasks/recipe-build-an-assessment-result-segment.md) | `Person`, `DataView`, `Group`, `Attribute` | `Person`, `DataView`, `Group`, `Attribute` |
| [Recipe: Connect an Achievement to workflows and Steps](tasks/recipe-connect-an-achievement-to-workflows-and-steps.md) | `StepProgram`, `StepType`, `Step`, `Workflow` | `StepProgram`, `StepType`, `Step`, `Workflow` |
| [Recipe: Configure Reminder processing](tasks/recipe-configure-reminder-processing.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Configure a secure Following event](tasks/recipe-configure-a-secure-following-event.md) | `Group` | `Group` |
| [Recipe: Operate a moderated Interactive Experience](tasks/recipe-operate-a-moderated-interactive-experience.md) | `DataView`, `Group`, `Schedule`, `Campus` | `DataView`, `Group`, `Schedule`, `Campus` |
| [Recipe: Configure a Sign-Up registration and attendance route](tasks/recipe-configure-a-sign-up-registration-and-attendance-route.md) | `Attendance`, `Group`, `Location`, `Schedule`, `Page` | `Attendance`, `Group`, `Location`, `Schedule`, `Page` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `StepProgram` | `StepType`, `Step`, `Person` | Do not equate a training completion with a Step unless the workflow or data view explicitly writes it. |
| `StepType` | `StepProgram`, `Step` | Check prerequisites, filters, workflows, and achievement behavior when a badge or step is missing. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added new "Core Steps" Step Program with system-protected Step Types, including initial "eRA" type. Added the ability to transfer Step Types from one Step Program to another. |
| `18.3` | core | Fixed an issue where editing a Step Program removed the Step Type association from its workflow triggers, and also addressed Step Type-level triggers being incorrectly displayed on the Step Program Detail. Fixes: #6753 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `steps-workflows-and-permissions` | high | live verification |
| `steps-badges-metrics-and-charts` | normal | live verification |
| `streaks-types-and-maps` | normal | live verification |
| `assessments-retake-controls` | normal | live verification |
| `achievements-overrides-and-rebuilds` | normal | live verification |
| `sign-ups` | normal | live verification |
| `troubleshooting-decision-tree-a-step-has-a-completion-date-but-is-not-counted-as-complete` | normal | live verification |
| `troubleshooting-decision-tree-step-automation-did-not-create-or-complete-a-record` | normal | live verification |
| `troubleshooting-decision-tree-step-metrics-or-charts-appear-inflated-or-use-unexpected-dates` | normal | live verification |
| `troubleshooting-decision-tree-a-manually-enrolled-person-has-a-streak-of-zero` | normal | live verification |
| `troubleshooting-decision-tree-a-streak-type-map-was-changed-but-participant-totals-have-not-updated` | normal | live verification |
| `troubleshooting-decision-tree-a-streak-spans-a-date-that-still-looks-absent` | normal | live verification |
| `troubleshooting-decision-tree-a-person-cannot-retake-an-assessment` | normal | live verification |
| `troubleshooting-decision-tree-an-assessment-request-cannot-be-canceled` | normal | live verification |
| `troubleshooting-decision-tree-achievement-progress-or-attempt-state-looks-wrong` | normal | live verification |
| `troubleshooting-decision-tree-a-reminder-was-created-but-no-notification-occurred` | normal | live verification |
| `troubleshooting-decision-tree-a-following-notification-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-an-interactive-experience-response-is-missing-from-the-visualizer` | normal | live verification |
| `troubleshooting-decision-tree-a-sign-up-communication-or-attendance-link-fails` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-step-journey-with-reliable-completion-signals` | normal | live verification |
| `agent-task-recipes-recipe-bulk-record-a-step` | normal | live verification |
| `agent-task-recipes-recipe-automate-step-completion-from-a-data-view` | normal | live verification |
| `agent-task-recipes-recipe-build-a-streak-type-safely` | normal | live verification |
| `agent-task-recipes-recipe-correct-one-person-s-streak` | normal | live verification |
| `agent-task-recipes-recipe-rebuild-a-streak-with-a-controlled-boundary` | normal | live verification |
| `agent-task-recipes-recipe-request-and-monitor-assessments` | normal | live verification |
| `agent-task-recipes-recipe-build-an-assessment-result-segment` | normal | live verification |
| `agent-task-recipes-recipe-connect-an-achievement-to-workflows-and-steps` | normal | live verification |
| `agent-task-recipes-recipe-configure-reminder-processing` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-secure-following-event` | normal | live verification |
| `agent-task-recipes-recipe-operate-a-moderated-interactive-experience` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-sign-up-registration-and-attendance-route` | normal | live verification |
| `known-gaps-and-live-verification` | normal | live verification |
| `source-map-community-example` | community-supported | community-supported |
