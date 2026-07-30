---
concept_id: engagement-tracking
title: Engagement Tracking Agent Cheatsheet
generated: true
---

# Engagement Tracking Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Audit A Step Program](tasks/recipe-audit-a-step-program.md) | `Person`, `StepProgram`, `StepType`, `Step`, `DataView`, `Workflow`, `Attribute` | `Person`, `StepProgram`, `StepType`, `Step`, `DataView`, `Workflow`, `Attribute` |
| [Recipe: Diagnose Step Badge Display](tasks/recipe-diagnose-step-badge-display.md) | `Person`, `StepProgram`, `StepType`, `Step`, `Block` | `Person`, `StepProgram`, `StepType`, `Step`, `Block` |
| [Recipe: Review A Streak Type Before Rebuild](tasks/recipe-review-a-streak-type-before-rebuild.md) | `Attendance`, `Person`, `Location` | `Attendance`, `Person`, `Location` |
| [Recipe: Verify Assessment Request Flow](tasks/recipe-verify-assessment-request-flow.md) | `Person`, `DataView`, `Attribute` | `Person`, `DataView`, `Attribute` |
| [Recipe: Audit Achievement Type](tasks/recipe-audit-achievement-type.md) | `Step`, `Workflow` | `Step`, `Workflow` |
| [Recipe: Explain Engagement Data To A Ministry User](tasks/recipe-explain-engagement-data-to-a-ministry-user.md) | `Attendance`, `Step` | `Attendance`, `Step` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `LearningClassActivityCompletion` | `LearningClassActivity`, `LearningClass`, `Person` | Use this to diagnose missing activity completion before escalating to program or step logic. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
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
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-engagement-tracking-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-steps-configuration` | high | live verification |
| `5-core-configuration-and-data-model-step-status-and-completion` | normal | live verification |
| `5-core-configuration-and-data-model-step-program-completion-model` | normal | live verification |
| `5-core-configuration-and-data-model-assessments-configuration` | normal | live verification |
| `6-primary-entities-and-relationships-person-personalias-and-engagement-records` | normal | live verification |
| `6-primary-entities-and-relationships-step-program-to-step-type` | normal | live verification |
| `6-primary-entities-and-relationships-assessments-to-person-history-and-attributes` | normal | live verification |
| `7-common-engagement-tracking-workflows-workflow-build-a-discipleship-step-program` | normal | live verification |
| `7-common-engagement-tracking-workflows-workflow-enter-an-individual-step` | normal | live verification |
| `7-common-engagement-tracking-workflows-workflow-bulk-add-or-update-steps` | normal | live verification |
| `7-common-engagement-tracking-workflows-workflow-send-assessment-requests` | normal | live verification |
| `7-common-engagement-tracking-workflows-workflow-configure-an-achievement-that-adds-a-step` | high | live verification |
| `8-steps-deep-dive-what-steps-are-for` | normal | live verification |
| `8-steps-deep-dive-completion-flow-and-prerequisites` | normal | live verification |
| `8-steps-deep-dive-step-type-design` | normal | live verification |
| `8-steps-deep-dive-step-entry` | normal | live verification |
| `8-steps-deep-dive-step-badges` | normal | live verification |
| `8-steps-deep-dive-step-charts` | normal | live verification |
| `8-steps-deep-dive-moving-step-types` | normal | live verification |
| `8-steps-deep-dive-core-steps` | normal | live verification |
| `9-streaks-deep-dive-what-streaks-are-for` | normal | live verification |
| `9-streaks-deep-dive-streak-maps` | normal | live verification |
| `9-streaks-deep-dive-manual-tracking` | normal | live verification |
| `9-streaks-deep-dive-rebuild-behavior` | normal | live verification |
| `9-streaks-deep-dive-excluding-dates` | normal | live verification |
| `10-assessments-deep-dive-taking-assessments` | normal | live verification |
| `10-assessments-deep-dive-sending-requests` | normal | live verification |
| `10-assessments-deep-dive-retakes` | normal | live verification |
| `10-assessments-deep-dive-assessment-history` | normal | live verification |
| `10-assessments-deep-dive-assessment-results-and-data-views` | normal | live verification |
| `11-achievements-deep-dive-attempts` | high | live verification |
| `11-achievements-deep-dive-prerequisites` | high | live verification |
| `11-achievements-deep-dive-workflow-launches` | high | live verification |
| `11-achievements-deep-dive-badges-and-lava` | high | live verification |
| `11-achievements-deep-dive-add-step-on-success` | normal | live verification |
| `11-achievements-deep-dive-processing` | normal | live verification |
| `12-related-rock-areas-people-groups-workflows-communications-data-views-reports-security-learning-lms-engagement-people` | structural | live verification |
| `12-related-rock-areas-people-groups-workflows-communications-data-views-reports-security-learning-lms-engagement-communications` | normal | live verification |
| `12-related-rock-areas-people-groups-workflows-communications-data-views-reports-security-learning-lms-engagement-learning-lms-engagement` | normal | live verification |
| `13-administration-and-operational-guardrails-configuration-guardrails` | structural | live verification |
| `13-administration-and-operational-guardrails-data-change-guardrails` | structural | live verification |
| `13-administration-and-operational-guardrails-rebuild-guardrails` | normal | live verification |
| `13-administration-and-operational-guardrails-version-guardrails` | normal | live verification |
| `13-administration-and-operational-guardrails-public-safe-documentation-guardrails` | structural | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-landmarks` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-api-notes` | normal | live verification |
| `15-reporting-analytics-and-model-map-model-map` | citation-only | live verification |
| `15-reporting-analytics-and-model-map-data-view-reporting` | citation-only | live verification |
| `16-version-and-release-caveats-v18-1-engagement-changes` | normal | live verification |
| `16-version-and-release-caveats-v18-3-engagement-fixes` | normal | live verification |
| `16-version-and-release-caveats-v19-documentation` | structural | live verification |
| `17-implementation-playbooks-playbook-new-step-program-for-volunteer-onboarding` | normal | live verification |
| `17-implementation-playbooks-playbook-historical-baptism-step-import` | community-supported | live verification |
| `17-implementation-playbooks-playbook-weekend-attendance-streak` | normal | live verification |
| `17-implementation-playbooks-playbook-assessment-driven-volunteer-placement` | normal | live verification |
| `17-implementation-playbooks-playbook-achievement-for-consistent-attendance-that-adds-a-step` | high | live verification |
| `18-troubleshooting-decision-tree-a-step-is-missing-from-a-person` | normal | live verification |
| `18-troubleshooting-decision-tree-step-program-completion-looks-wrong` | normal | live verification |
| `18-troubleshooting-decision-tree-assessment-cannot-be-retaken` | normal | live verification |
| `18-troubleshooting-decision-tree-assessment-results-are-not-reportable` | normal | live verification |
| `18-troubleshooting-decision-tree-achievement-does-not-create-attempts` | normal | live verification |
| `18-troubleshooting-decision-tree-achievement-saves-but-behaves-incorrectly` | normal | live verification |
| `18-troubleshooting-decision-tree-achievement-success-workflow-does-not-run` | normal | live verification |
| `19-agent-task-recipes-recipe-diagnose-step-badge-display` | normal | live verification |
| `20-source-map-and-dependency-notes-training-release-model-and-community-sources` | normal | live verification |
| `20-source-map-and-dependency-notes-source-code-sources` | normal | live verification |
| `20-source-map-and-dependency-notes-dependency-notes` | normal | live verification |
