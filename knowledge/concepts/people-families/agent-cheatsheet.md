---
concept_id: people-families
title: People And Families Agent Cheatsheet
generated: true
---

# People And Families Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Add a person or family without creating a duplicate](tasks/recipe-add-a-person-or-family-without-creating-a-duplicate.md) | `Person`, `Campus`, `Family` | `Person`, `Campus`, `Family` |
| [Recipe: Correct a family structure or household move](tasks/recipe-correct-a-family-structure-or-household-move.md) | `Campus`, `Family`, `Page`, `Person` | `Campus`, `Family`, `Page`, `Person` |
| [Recipe: Design or review a person or family attribute](tasks/recipe-design-or-review-a-person-or-family-attribute.md) | `Person`, `Group`, `Family`, `Workflow`, `Block`, `Attribute`, `Campus` | `Person`, `Group`, `Family`, `Workflow`, `Block`, `Attribute`, `Campus` |
| [Recipe: Audit Person Note governance](tasks/recipe-audit-person-note-governance.md) | `Location`, `Workflow` | `Location`, `Workflow` |
| [Recipe: Prepare a duplicate-person merge for authorized review](tasks/recipe-prepare-a-duplicate-person-merge-for-authorized-review.md) | `Person`, `Family`, `Attribute` | `Person`, `Family`, `Attribute` |
| [Recipe: Validate family preregistration end to end](tasks/recipe-validate-family-preregistration-end-to-end.md) | `Person`, `Campus`, `Family`, `Workflow`, `Attribute` | `Person`, `Campus`, `Family`, `Workflow`, `Attribute` |
| [Recipe: Diagnose a connection request from the person record](tasks/recipe-diagnose-a-connection-request-from-the-person-record.md) | `Person`, `Workflow` | `Person`, `Workflow` |
| [Recipe: Run a bounded people-data cleanup](tasks/recipe-run-a-bounded-people-data-cleanup.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup parameter) was excl |
| `18.2` | core | Fixed an issue where the Attribute Editor did not correctly save configuration changes when creating an Attribute designed to store other Attributes (e.g., an Attribute of type Attribute). This affected scenarios such as defining filters in |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `person-model-and-record-lifecycle-editing-inactivating-and-preserving-history` | normal | live verification |
| `person-profile-and-access-boundaries-tags-signals-and-badges` | normal | live verification |
| `families-membership-and-relationships-known-relationships` | normal | live verification |
| `person-and-family-attributes-public-self-service-attributes` | high | live verification |
| `person-notes-and-note-type-governance` | citation-only | live verification |
| `data-integrity-duplicates-and-merge-preparation` | citation-only | live verification |
| `data-integrity-duplicates-and-merge-preparation-rock-v19-merge-evidence` | citation-only | live verification |
| `family-preregistration-and-follow-up` | normal | live verification |
| `connections-as-person-centered-process-state` | citation-only | live verification |
| `personalization-and-person-data` | citation-only | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-person-cannot-be-found-or-a-new-record-may-be-a-duplicate` | normal | live verification |
| `troubleshooting-decision-tree-a-person-is-in-the-wrong-family-campus-or-household-report` | normal | live verification |
| `troubleshooting-decision-tree-a-user-can-see-a-profile-but-cannot-view-or-edit-one-part-of-it` | normal | live verification |
| `troubleshooting-decision-tree-a-note-is-missing-appears-in-the-wrong-place-or-is-visible-too-broadly` | citation-only | live verification |
| `troubleshooting-decision-tree-an-attribute-is-absent-blank-stale-or-unexpectedly-overwritten` | normal | live verification |
| `troubleshooting-decision-tree-family-preregistration-creates-partial-or-duplicate-records` | normal | live verification |
| `troubleshooting-decision-tree-a-connection-request-is-missing-or-stuck` | citation-only | live verification |
| `troubleshooting-decision-tree-personalized-content-appears-for-the-wrong-person-or-not-at-all` | citation-only | live verification |
| `troubleshooting-decision-tree-family-analytics-or-era-values-appear-stale-or-wrong` | normal | live verification |
| `agent-task-recipes-recipe-add-a-person-or-family-without-creating-a-duplicate` | normal | live verification |
| `agent-task-recipes-recipe-correct-a-family-structure-or-household-move` | normal | live verification |
| `agent-task-recipes-recipe-design-or-review-a-person-or-family-attribute` | normal | live verification |
| `agent-task-recipes-recipe-audit-person-note-governance` | citation-only | live verification |
| `agent-task-recipes-recipe-prepare-a-duplicate-person-merge-for-authorized-review` | citation-only | live verification |
| `agent-task-recipes-recipe-validate-family-preregistration-end-to-end` | normal | live verification |
| `agent-task-recipes-recipe-diagnose-a-connection-request-from-the-person-record` | citation-only | live verification |
| `agent-task-recipes-recipe-run-a-bounded-people-data-cleanup` | citation-only | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
