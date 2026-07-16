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
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-check-in-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-check-in-systems` | normal | live verification |
| `5-core-configuration-and-data-model-check-in-type-individual-vs-family` | normal | live verification |
| `5-core-configuration-and-data-model-search` | normal | live verification |
| `5-core-configuration-and-data-model-group-membership-behavior` | normal | live verification |
| `5-core-configuration-and-data-model-locations` | normal | live verification |
| `5-core-configuration-and-data-model-schedules` | normal | live verification |
| `5-core-configuration-and-data-model-location-selection-strategy` | normal | live verification |
| `6-primary-entities-and-relationships-person-personalias-and-family` | normal | live verification |
| `6-primary-entities-and-relationships-grouptype-group-groupmember` | community-supported | live verification |
| `6-primary-entities-and-relationships-grouplocation-location-schedule` | community-supported | live verification |
| `6-primary-entities-and-relationships-device-and-kiosk` | citation-only | live verification |
| `6-primary-entities-and-relationships-attendance-and-attendanceoccurrence` | normal | live verification |
| `7-common-check-in-workflows-attended-check-in` | citation-only | live verification |
| `7-common-check-in-workflows-check-in-manager` | normal | live verification |
| `7-common-check-in-workflows-rapid-attendance-entry` | normal | live verification |
| `7-common-check-in-workflows-group-attendance` | normal | live verification |
| `7-common-check-in-workflows-attendance-self-entry` | citation-only | live verification |
| `7-common-check-in-workflows-proximity-attendance` | normal | live verification |
| `8-labels-deep-dive-legacy-labels-and-next-gen-labels` | community-supported | live verification |
| `8-labels-deep-dive-label-data-model` | normal | live verification |
| `8-labels-deep-dive-security-code-formatting` | normal | live verification |
| `8-labels-deep-dive-merge-fields-and-lava` | normal | live verification |
| `8-labels-deep-dive-fonts-and-icons` | community-supported | live verification |
| `8-labels-deep-dive-label-troubleshooting-branches` | normal | live verification |
| `9-mobile-check-in-deep-dive-configuration-checklist` | citation-only | live verification |
| `9-mobile-check-in-deep-dive-mobile-and-eligibility` | structural | live verification |
| `9-mobile-check-in-deep-dive-mobile-group-attendance-entry` | normal | live verification |
| `9-mobile-check-in-deep-dive-proximity-attendance` | normal | live verification |
| `10-attendance-deep-dive-attendance-rows` | normal | live verification |
| `10-attendance-deep-dive-attendanceoccurrence-sundaydate` | normal | live verification |
| `10-attendance-deep-dive-attendance-analytics-block` | normal | live verification |
| `10-attendance-deep-dive-count-only-attendance` | community-supported | live verification |
| `11-troubleshooting-deep-dive-symptom-no-check-in-locations-are-active` | normal | live verification |
| `11-troubleshooting-deep-dive-symptom-family-search-finds-nothing` | structural | live verification |
| `11-troubleshooting-deep-dive-symptom-rapid-attendance-entry-too-slow-or-wrong-shape` | normal | live verification |
| `12-related-rock-areas-attendance-groups-locations-schedules-labels-mobile-security-groups` | structural | live verification |
| `13-administration-and-operational-guardrails-pre-service-checklist` | citation-only | live verification |
| `13-administration-and-operational-guardrails-configuration-change-control` | structural | live verification |
| `13-administration-and-operational-guardrails-label-safety` | structural | live verification |
| `14-developer-api-lava-and-source-code-landmarks-mobile-check-in-docs` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-and-community-patterns` | community-supported | community-supported |
| `15-reporting-analytics-and-model-map-analytics-caveats` | normal | live verification |
| `15-reporting-analytics-and-model-map-model-map-use` | structural | live verification |
| `16-version-and-release-caveats` | normal | live verification |
| `17-implementation-playbooks-playbook-build-a-basic-family-check-in-area` | citation-only | live verification |
| `17-implementation-playbooks-playbook-add-a-new-room` | citation-only | live verification |
| `17-implementation-playbooks-playbook-configure-mobile-check-in` | citation-only | live verification |
| `17-implementation-playbooks-playbook-configure-rapid-attendance-entry` | normal | live verification |
| `17-implementation-playbooks-playbook-implement-a-qr-code-attendance-pattern` | community-supported | live verification |
| `17-implementation-playbooks-playbook-implement-sms-text-attendance` | community-supported | live verification |
| `18-troubleshooting-decision-tree-b-was-attendance-saved` | structural | live verification |
| `18-troubleshooting-decision-tree-c-is-the-problem-labels` | structural | live verification |
| `18-troubleshooting-decision-tree-d-is-the-problem-check-in-manager` | structural | live verification |
| `18-troubleshooting-decision-tree-e-is-the-problem-analytics` | structural | live verification |
| `18-troubleshooting-decision-tree-f-is-the-problem-mobile` | structural | live verification |
| `19-agent-task-recipes-recipe-prove-why-a-child-cannot-check-in` | citation-only | live verification |
| `19-agent-task-recipes-recipe-prove-which-printer-should-print-a-label` | structural | live verification |
| `19-agent-task-recipes-recipe-reconcile-attendance-analytics-to-raw-rows` | structural | live verification |
| `19-agent-task-recipes-recipe-decide-between-check-in-group-attendance-rapid-attendance-qr-and-sms` | community-supported | community-supported |
| `19-agent-task-recipes-recipe-validate-mobile-check-in-readiness` | structural | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `20-source-map-and-dependency-notes` | high | live verification |
