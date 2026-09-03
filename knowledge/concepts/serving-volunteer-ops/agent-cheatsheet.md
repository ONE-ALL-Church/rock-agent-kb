---
concept_id: serving-volunteer-ops
title: Serving And Volunteer Operations Agent Cheatsheet
generated: true
---

# Serving And Volunteer Operations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Configure a serving team for scheduling](tasks/recipe-configure-a-serving-team-for-scheduling.md) | `Attendance`, `Group`, `GroupType`, `Location`, `Schedule`, `Workflow`, `Block` | `Attendance`, `Group`, `GroupType`, `Location`, `Schedule`, `Workflow`, `Block` |
| [Recipe: Send and triage volunteer confirmations](tasks/recipe-send-and-triage-volunteer-confirmations.md) | `Group`, `Location`, `Schedule`, `Workflow`, `Page` | `Group`, `Location`, `Schedule`, `Workflow`, `Page` |
| [Recipe: Configure an RSVP-based serving invitation](tasks/recipe-configure-an-rsvp-based-serving-invitation.md) | `Attendance`, `Person`, `Group`, `GroupType`, `Location`, `Schedule`, `Workflow` | `Attendance`, `Person`, `Group`, `GroupType`, `Location`, `Schedule`, `Workflow` |
| [Recipe: Close out serving attendance](tasks/recipe-close-out-serving-attendance.md) | `Attendance`, `Group`, `Location`, `Schedule`, `Label` | `Attendance`, `Group`, `Location`, `Schedule`, `Label` |
| [Recipe: Build an LMS-based volunteer training path](tasks/recipe-build-an-lms-based-volunteer-training-path.md) | `Group`, `Workflow` | `Group`, `Workflow` |
| [Recipe: Configure an attendance digest](tasks/recipe-configure-an-attendance-digest.md) | `Attendance`, `Person`, `Group` | `Attendance`, `Person`, `Group` |
| [Recipe: Secure an embedded volunteer dashboard](tasks/recipe-secure-an-embedded-volunteer-dashboard.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Pilot Outreach Toolbox for relationship-care follow-up](tasks/recipe-pilot-outreach-toolbox-for-relationship-care-follow-up.md) | `Group`, `Schedule`, `Page`, `Block`, `Person` | `Group`, `Schedule`, `Page`, `Block`, `Person` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.3` | core | Fixed an issue with the RSVP Response block where the heading would show the generic "RSVP for Event" text instead of the Attendance Occurrence Name when accessed through the Accept or Decline link in an RSVP email. Fixes: #6872 |
| `18.3` | core | Fixed the Send Attendance Reminder job so Group leaders still receive reminders when a Group only has scheduling/RSVP-related Attendance records. The job now treats those tracking records as not being “attendance” and only suppresses remind |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | needs-citation |
| `mental-model-group-scheduling-and-group-rsvp-are-related-but-different` | normal | live verification |
| `mental-model-serving-status-is-not-volunteer-eligibility` | community-supported | live verification |
| `serving-teams-and-roles-establish-the-operating-group-structure` | normal | live verification |
| `serving-teams-and-roles-distinguish-operational-roles` | normal | live verification |
| `schedules-and-confirmations-configure-the-scheduling-foundation` | normal | live verification |
| `schedules-and-confirmations-choose-confirmation-logic-deliberately` | normal | live verification |
| `volunteer-requirements-and-training-use-the-evidence-supported-lms-model` | community-supported | community-supported |
| `volunteer-requirements-and-training-connect-completion-to-operations-intentionally` | community-supported | live verification |
| `volunteer-requirements-and-training-train-staff-before-volunteer-rollout` | citation-only | live verification |
| `volunteer-requirements-and-training-treat-background-check-providers-as-versioned-dependencies` | normal | live verification |
| `attendance-and-follow-up-use-rapid-attendance-entry-for-high-volume-entry` | normal | live verification |
| `attendance-and-follow-up-build-follow-up-from-verified-states` | needs-citation | live verification |
| `reporting-and-operational-visibility` | normal | live verification |
| `relationship-care-follow-up-with-outreach-toolbox` | citation-only | live verification |
| `community-implementation-patterns` | community-supported | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-the-team-does-not-appear-in-group-scheduling` | normal | live verification |
| `troubleshooting-decision-tree-a-volunteer-received-no-confirmation-or-reminder` | high | live verification |
| `troubleshooting-decision-tree-a-volunteer-cannot-accept-an-assignment` | normal | live verification |
| `troubleshooting-decision-tree-the-schedule-coordinator-was-not-alerted` | normal | live verification |
| `troubleshooting-decision-tree-rsvp-features-are-missing` | normal | live verification |
| `troubleshooting-decision-tree-an-rsvp-invitee-is-missing-from-the-response-list` | normal | live verification |
| `troubleshooting-decision-tree-the-attendance-button-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-an-attendance-reminder-was-not-sent` | high | live verification |
| `troubleshooting-decision-tree-a-confirmed-volunteer-appears-absent` | normal | live verification |
| `troubleshooting-decision-tree-rapid-attendance-entry-lacks-an-expected-location-schedule-or-action` | normal | live verification |
| `troubleshooting-decision-tree-training-completion-did-not-change-serving-eligibility` | community-supported | live verification |
| `troubleshooting-decision-tree-outreach-toolbox-reminders-are-not-arriving` | citation-only | live verification |
| `agent-task-recipes-recipe-configure-a-serving-team-for-scheduling` | normal | live verification |
| `agent-task-recipes-recipe-send-and-triage-volunteer-confirmations` | normal | live verification |
| `agent-task-recipes-recipe-configure-an-rsvp-based-serving-invitation` | normal | live verification |
| `agent-task-recipes-recipe-close-out-serving-attendance` | normal | live verification |
| `agent-task-recipes-recipe-build-an-lms-based-volunteer-training-path` | community-supported | live verification |
| `agent-task-recipes-recipe-configure-an-attendance-digest` | normal | live verification |
| `agent-task-recipes-recipe-secure-an-embedded-volunteer-dashboard` | community-supported | live verification |
| `agent-task-recipes-recipe-pilot-outreach-toolbox-for-relationship-care-follow-up` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-approved-answer-bearing-claims` | community-supported | community-supported |
| `source-map-community-examples` | community-supported | community-supported |
