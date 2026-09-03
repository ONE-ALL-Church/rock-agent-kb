---
concept_id: serving-volunteer-ops
title: Serving And Volunteer Operations Open Questions
generated: true
---

# Serving And Volunteer Operations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (161 words)
- `attendance-and-follow-up-build-follow-up-from-verified-states`: Build follow-up from verified states (89 words)

## Community-Supported Only

- `mental-model-serving-status-is-not-volunteer-eligibility`: Serving status is not volunteer eligibility
- `volunteer-requirements-and-training-use-the-evidence-supported-lms-model`: Use the evidence-supported LMS model
- `volunteer-requirements-and-training-connect-completion-to-operations-intentionally`: Connect completion to operations intentionally
- `community-implementation-patterns`: Community Implementation Patterns
- `troubleshooting-decision-tree-training-completion-did-not-change-serving-eligibility`: Training completion did not change serving eligibility
- `agent-task-recipes-recipe-build-an-lms-based-volunteer-training-path`: Recipe: Build an LMS-based volunteer training path
- `agent-task-recipes-recipe-secure-an-embedded-volunteer-dashboard`: Recipe: Secure an embedded volunteer dashboard
- `source-map-approved-answer-bearing-claims`: Approved answer-bearing claims
- `source-map-community-examples`: Community examples

## Needs Live Verification

- `agent-summary`: Agent Summary
- `mental-model-group-scheduling-and-group-rsvp-are-related-but-different`: Group Scheduling and Group RSVP are related but different
- `mental-model-serving-status-is-not-volunteer-eligibility`: Serving status is not volunteer eligibility
- `serving-teams-and-roles-establish-the-operating-group-structure`: Establish the operating group structure
- `serving-teams-and-roles-distinguish-operational-roles`: Distinguish operational roles
- `schedules-and-confirmations-configure-the-scheduling-foundation`: Configure the scheduling foundation
- `schedules-and-confirmations-choose-confirmation-logic-deliberately`: Choose confirmation logic deliberately
- `volunteer-requirements-and-training-connect-completion-to-operations-intentionally`: Connect completion to operations intentionally
- `volunteer-requirements-and-training-train-staff-before-volunteer-rollout`: Train staff before volunteer rollout
- `volunteer-requirements-and-training-treat-background-check-providers-as-versioned-dependencies`: Treat background-check providers as versioned dependencies
- `attendance-and-follow-up-use-rapid-attendance-entry-for-high-volume-entry`: Use Rapid Attendance Entry for high-volume entry
- `attendance-and-follow-up-build-follow-up-from-verified-states`: Build follow-up from verified states
- `reporting-and-operational-visibility`: Reporting And Operational Visibility
- `relationship-care-follow-up-with-outreach-toolbox`: Relationship-Care Follow-Up With Outreach Toolbox
- `community-implementation-patterns`: Community Implementation Patterns
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-the-team-does-not-appear-in-group-scheduling`: The team does not appear in Group Scheduling
- `troubleshooting-decision-tree-a-volunteer-received-no-confirmation-or-reminder`: A volunteer received no confirmation or reminder
- `troubleshooting-decision-tree-a-volunteer-cannot-accept-an-assignment`: A volunteer cannot accept an assignment
- `troubleshooting-decision-tree-the-schedule-coordinator-was-not-alerted`: The Schedule Coordinator was not alerted
- `troubleshooting-decision-tree-rsvp-features-are-missing`: RSVP features are missing
- `troubleshooting-decision-tree-an-rsvp-invitee-is-missing-from-the-response-list`: An RSVP invitee is missing from the response list
- `troubleshooting-decision-tree-the-attendance-button-is-missing`: The attendance button is missing
- `troubleshooting-decision-tree-an-attendance-reminder-was-not-sent`: An attendance reminder was not sent
- `troubleshooting-decision-tree-a-confirmed-volunteer-appears-absent`: A confirmed volunteer appears absent
- `troubleshooting-decision-tree-rapid-attendance-entry-lacks-an-expected-location-schedule-or-action`: Rapid Attendance Entry lacks an expected location, schedule, or action
- `troubleshooting-decision-tree-training-completion-did-not-change-serving-eligibility`: Training completion did not change serving eligibility
- `troubleshooting-decision-tree-outreach-toolbox-reminders-are-not-arriving`: Outreach Toolbox reminders are not arriving
- `agent-task-recipes-recipe-configure-a-serving-team-for-scheduling`: Recipe: Configure a serving team for scheduling
- `agent-task-recipes-recipe-send-and-triage-volunteer-confirmations`: Recipe: Send and triage volunteer confirmations
- `agent-task-recipes-recipe-configure-an-rsvp-based-serving-invitation`: Recipe: Configure an RSVP-based serving invitation
- `agent-task-recipes-recipe-close-out-serving-attendance`: Recipe: Close out serving attendance
- `agent-task-recipes-recipe-build-an-lms-based-volunteer-training-path`: Recipe: Build an LMS-based volunteer training path
- `agent-task-recipes-recipe-configure-an-attendance-digest`: Recipe: Configure an attendance digest
- `agent-task-recipes-recipe-secure-an-embedded-volunteer-dashboard`: Recipe: Secure an embedded volunteer dashboard
- `agent-task-recipes-recipe-pilot-outreach-toolbox-for-relationship-care-follow-up`: Recipe: Pilot Outreach Toolbox for relationship-care follow-up
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
