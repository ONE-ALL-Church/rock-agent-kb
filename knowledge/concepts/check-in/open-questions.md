---
concept_id: check-in
title: Check-In Open Questions
generated: true
---

# Check-In Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `troubleshooting-decision-tree-a-rest-integration-creates-unexpected-schedules-or-links`: A REST integration creates unexpected schedules or links
- `troubleshooting-decision-tree-attendance-appears-to-save-but-the-page-gives-no-confirmation`: Attendance appears to save but the page gives no confirmation
- `source-map-community-patterns`: Community patterns

## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `mental-model-labels-depend-on-context`: Labels depend on context
- `core-configuration-kiosks-locations-and-schedules-locations-schedules-and-room-state`: Locations, schedules, and room state
- `core-configuration-kiosks-locations-and-schedules-eligibility-by-age-grade-and-birthdate`: Eligibility by age, grade, and birthdate
- `core-configuration-kiosks-locations-and-schedules-check-in-relationships`: Check-in relationships
- `mobile-check-in-preconditions`: Preconditions
- `mobile-check-in-participant-flow`: Participant flow
- `labels-and-printing-design-link-preview-and-print`: Design, link, preview, and print
- `labels-and-printing-merge-data-and-dynamic-text`: Merge data and dynamic text
- `check-in-manager-and-device-manager`: Check-In Manager And Device Manager
- `attendance-entry-and-analysis-attendance-analytics`: Attendance Analytics
- `registration-and-new-families`: Registration And New Families
- `additional-check-in-options-nfc-check-in`: NFC check-in
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-person-or-family-cannot-be-found`: A person or family cannot be found
- `troubleshooting-decision-tree-a-person-is-found-but-has-no-check-in-options`: A person is found but has no check-in options
- `troubleshooting-decision-tree-a-room-is-unavailable-only-during-one-service`: A room is unavailable only during one service
- `troubleshooting-decision-tree-mobile-check-in-reports-no-campus-no-service-or-location-failure`: Mobile check-in reports no campus, no service, or location failure
- `troubleshooting-decision-tree-a-mobile-qr-code-does-not-print-labels`: A mobile QR code does not print labels
- `troubleshooting-decision-tree-symptom-attendance-saved-but-label-did-not-print`: Symptom: Attendance Saved But Label Did Not Print
- `troubleshooting-decision-tree-a-label-prints-with-wrong-or-duplicated-data`: A label prints with wrong or duplicated data
- `troubleshooting-decision-tree-a-label-cannot-be-reprinted`: A label cannot be reprinted
- `troubleshooting-decision-tree-check-in-manager-attendance-updates-lag`: Check-In Manager attendance updates lag
- `troubleshooting-decision-tree-rapid-attendance-entry-is-missing-expected-actions`: Rapid Attendance Entry is missing expected actions
- `troubleshooting-decision-tree-attendance-self-entry-does-not-record-attendance`: Attendance Self Entry does not record attendance
- `troubleshooting-decision-tree-proximity-attendance-records-the-wrong-service-or-area`: Proximity attendance records the wrong service or area
- `troubleshooting-decision-tree-a-rest-integration-creates-unexpected-schedules-or-links`: A REST integration creates unexpected schedules or links
- `troubleshooting-decision-tree-attendance-appears-to-save-but-the-page-gives-no-confirmation`: Attendance appears to save but the page gives no confirmation
- `agent-task-recipes-recipe-preflight-a-standard-kiosk-session`: Recipe: Preflight a standard kiosk session
- `agent-task-recipes-recipe-preflight-mobile-check-in`: Recipe: Preflight mobile check-in
- `agent-task-recipes-recipe-validate-a-next-gen-label-end-to-end`: Recipe: Validate a Next-Gen label end to end
- `agent-task-recipes-recipe-triage-a-live-service-incident`: Recipe: Triage a live-service incident
- `agent-task-recipes-recipe-create-a-focused-rapid-attendance-entry-page`: Recipe: Create a focused Rapid Attendance Entry page
- `agent-task-recipes-recipe-prepare-a-new-family-arrival-path`: Recipe: Prepare a new-family arrival path
- `agent-task-recipes-recipe-reprint-a-damaged-label`: Recipe: Reprint a damaged label
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `source-map-community-patterns`: Community patterns

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
