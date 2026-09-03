---
concept_id: check-in
title: Check-In Agent Cheatsheet
generated: true
---

# Check-In Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Diagnose Labels Not Printing](tasks/diagnose-labels-not-printing.md) | `Device`, `Location`, `Check-in Configuration`, `Label`, `Attendance` | `Device`, `Location`, `Attendance`, `AttendanceOccurrence` |
| [Diagnose Person Found But No Eligible Rooms](tasks/diagnose-person-not-eligible.md) | `Person`, `Family Group`, `GroupType`, `Group`, `Location`, `Schedule`, `Campus` | `Person`, `Group`, `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` |
| [Add A New Check-In Room](tasks/add-new-room.md) | `Group`, `Location`, `Schedule`, `Device`, `Label` | `Group`, `Location`, `Schedule`, `AttendanceOccurrence` |
| [Audit Mobile Check-In](tasks/audit-mobile-check-in.md) | `Mobile Page`, `Mobile Block`, `Check-in Configuration`, `Device/Kiosk`, `Printer` | `Attendance`, `AttendanceOccurrence`, `Device` |
| [Build Or Debug Attendance Reporting](tasks/build-attendance-report.md) | `Attendance`, `AttendanceOccurrence`, `Group`, `Schedule`, `Location`, `Campus` | `Attendance`, `AttendanceOccurrence`, `PersonAlias`, `Group`, `Schedule`, `Location`, `Campus` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `AttendanceOccurrence` | `Attendance`, `Group`, `Schedule`, `Location`, `Campus` | Use this for reporting context. Check group, location, schedule, and SundayDate before blaming the UI. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Device/Kiosk` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family Group` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Mobile Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Mobile Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Printer` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `SecurityCode` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | normal | live verification |
| `mental-model-labels-depend-on-context` | citation-only | live verification |
| `core-configuration-kiosks-locations-and-schedules-locations-schedules-and-room-state` | normal | live verification |
| `core-configuration-kiosks-locations-and-schedules-eligibility-by-age-grade-and-birthdate` | normal | live verification |
| `core-configuration-kiosks-locations-and-schedules-check-in-relationships` | normal | live verification |
| `mobile-check-in-preconditions` | citation-only | live verification |
| `mobile-check-in-participant-flow` | normal | live verification |
| `labels-and-printing-design-link-preview-and-print` | normal | live verification |
| `labels-and-printing-merge-data-and-dynamic-text` | normal | live verification |
| `check-in-manager-and-device-manager` | normal | live verification |
| `attendance-entry-and-analysis-attendance-analytics` | normal | live verification |
| `registration-and-new-families` | normal | live verification |
| `additional-check-in-options-nfc-check-in` | normal | live verification |
| `version-and-authority-caveats` | high | live verification |
| `troubleshooting-decision-tree-a-person-or-family-cannot-be-found` | normal | live verification |
| `troubleshooting-decision-tree-a-person-is-found-but-has-no-check-in-options` | normal | live verification |
| `troubleshooting-decision-tree-a-room-is-unavailable-only-during-one-service` | normal | live verification |
| `troubleshooting-decision-tree-mobile-check-in-reports-no-campus-no-service-or-location-failure` | normal | live verification |
| `troubleshooting-decision-tree-a-mobile-qr-code-does-not-print-labels` | normal | live verification |
| `troubleshooting-decision-tree-symptom-attendance-saved-but-label-did-not-print` | normal | live verification |
| `troubleshooting-decision-tree-a-label-prints-with-wrong-or-duplicated-data` | normal | live verification |
| `troubleshooting-decision-tree-a-label-cannot-be-reprinted` | normal | live verification |
| `troubleshooting-decision-tree-check-in-manager-attendance-updates-lag` | normal | live verification |
| `troubleshooting-decision-tree-rapid-attendance-entry-is-missing-expected-actions` | normal | live verification |
| `troubleshooting-decision-tree-attendance-self-entry-does-not-record-attendance` | normal | live verification |
| `troubleshooting-decision-tree-proximity-attendance-records-the-wrong-service-or-area` | normal | live verification |
| `troubleshooting-decision-tree-a-rest-integration-creates-unexpected-schedules-or-links` | community-supported | live verification |
| `troubleshooting-decision-tree-attendance-appears-to-save-but-the-page-gives-no-confirmation` | community-supported | live verification |
| `agent-task-recipes-recipe-preflight-a-standard-kiosk-session` | normal | live verification |
| `agent-task-recipes-recipe-preflight-mobile-check-in` | citation-only | live verification |
| `agent-task-recipes-recipe-validate-a-next-gen-label-end-to-end` | normal | live verification |
| `agent-task-recipes-recipe-triage-a-live-service-incident` | normal | live verification |
| `agent-task-recipes-recipe-create-a-focused-rapid-attendance-entry-page` | normal | live verification |
| `agent-task-recipes-recipe-prepare-a-new-family-arrival-path` | normal | live verification |
| `agent-task-recipes-recipe-reprint-a-damaged-label` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-community-patterns` | community-supported | live verification |
