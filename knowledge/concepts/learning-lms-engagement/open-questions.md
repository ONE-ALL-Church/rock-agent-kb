---
concept_id: learning-lms-engagement
title: Learning, LMS, And Engagement Open Questions
generated: true
---

# Learning, LMS, And Engagement Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `14-developer-api-lava-and-source-code-landmarks-lava-landmarks`: Lava Landmarks

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model`: 5. Core Configuration And Data Model
- `6-primary-entities-and-relationships-lms-entity-relationships`: LMS Entity Relationships
- `7-common-learning-lms-and-engagement-workflows-create-an-on-demand-training-program`: Create An On-Demand Training Program
- `7-common-learning-lms-and-engagement-workflows-create-an-academic-calendar-program`: Create An Academic Calendar Program
- `7-common-learning-lms-and-engagement-workflows-assign-training-to-volunteers-or-staff`: Assign Training To Volunteers Or Staff
- `7-common-learning-lms-and-engagement-workflows-record-a-ministry-milestone`: Record A Ministry Milestone
- `7-common-learning-lms-and-engagement-workflows-automate-follow-up-from-learning-completion`: Automate Follow-Up From Learning Completion
- `8-courses-and-lessons-deep-dive-course-configuration-checks`: Course Configuration Checks
- `8-courses-and-lessons-deep-dive-class-design`: Class Design
- `8-courses-and-lessons-deep-dive-learning-plan-activity-design`: Learning Plan Activity Design
- `8-courses-and-lessons-deep-dive-lessons-versus-activities`: Lessons Versus Activities
- `9-requirements-and-completion-deep-dive-lms-course-requirements`: LMS Course Requirements
- `9-requirements-and-completion-deep-dive-completion-tracking`: Completion Tracking
- `9-requirements-and-completion-deep-dive-activity-completion-workflows`: Activity Completion Workflows
- `10-engagement-journeys-deep-dive-step-types`: Step Types
- `10-engagement-journeys-deep-dive-adding-steps`: Adding Steps
- `10-engagement-journeys-deep-dive-achievements-and-streaks`: Achievements And Streaks
- `11-reporting-and-administration-deep-dive-lms-reporting`: LMS Reporting
- `11-reporting-and-administration-deep-dive-administration`: Administration
- `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-people`: People
- `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-communications`: Communications
- `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-workflows`: Workflows
- `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-event-registration`: Event Registration
- `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-security`: Security
- `13-administration-and-operational-guardrails-guardrail-3-verify-entity-types-before-automating`: Guardrail 3: Verify Entity Types Before Automating
- `13-administration-and-operational-guardrails-guardrail-4-preserve-customized-system-communications`: Guardrail 4: Preserve Customized System Communications
- `13-administration-and-operational-guardrails-guardrail-7-mark-legacy-training-as-legacy`: Guardrail 7: Mark Legacy Training As Legacy
- `14-developer-api-lava-and-source-code-landmarks-source-repository`: Source Repository
- `14-developer-api-lava-and-source-code-landmarks-lava-landmarks`: Lava Landmarks
- `15-reporting-analytics-and-model-map`: 15. Reporting, Analytics, And Model Map
- `16-version-and-release-caveats-rock-v17-0`: Rock v17.0
- `16-version-and-release-caveats-rock-v18-1`: Rock v18.1
- `16-version-and-release-caveats-rock-v18-3-and-v19-1-release-notes-in-pack`: Rock v18.3 And v19.1 Release Notes In Pack
- `16-version-and-release-caveats-develop-branch-caveat`: Develop Branch Caveat
- `17-implementation-playbooks-playbook-launch-a-volunteer-training-lms-program`: Playbook: Launch A Volunteer Training LMS Program
- `17-implementation-playbooks-playbook-add-a-new-course-requirement`: Playbook: Add A New Course Requirement
- `17-implementation-playbooks-playbook-convert-a-training-completion-into-an-engagement-step`: Playbook: Convert A Training Completion Into An Engagement Step

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
