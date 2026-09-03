---
concept_id: people-families
title: People And Families Open Questions
generated: true
---

# People And Families Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `known-gaps-and-live-verification`: Known Gaps And Live Verification (196 words)

## Community-Supported Only


## Needs Live Verification

- `agent-summary`: Agent Summary
- `person-model-and-record-lifecycle-editing-inactivating-and-preserving-history`: Editing, inactivating, and preserving history
- `person-profile-and-access-boundaries-tags-signals-and-badges`: Tags, signals, and badges
- `families-membership-and-relationships-known-relationships`: Known relationships
- `person-and-family-attributes-public-self-service-attributes`: Public self-service attributes
- `person-notes-and-note-type-governance`: Person Notes And Note-Type Governance
- `data-integrity-duplicates-and-merge-preparation`: Data Integrity, Duplicates, And Merge Preparation
- `data-integrity-duplicates-and-merge-preparation-rock-v19-merge-evidence`: Rock v19 merge evidence
- `family-preregistration-and-follow-up`: Family Preregistration And Follow-Up
- `connections-as-person-centered-process-state`: Connections As Person-Centered Process State
- `personalization-and-person-data`: Personalization And Person Data
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-person-cannot-be-found-or-a-new-record-may-be-a-duplicate`: A person cannot be found, or a new record may be a duplicate
- `troubleshooting-decision-tree-a-person-is-in-the-wrong-family-campus-or-household-report`: A person is in the wrong family, campus, or household report
- `troubleshooting-decision-tree-a-user-can-see-a-profile-but-cannot-view-or-edit-one-part-of-it`: A user can see a profile but cannot view or edit one part of it
- `troubleshooting-decision-tree-a-note-is-missing-appears-in-the-wrong-place-or-is-visible-too-broadly`: A note is missing, appears in the wrong place, or is visible too broadly
- `troubleshooting-decision-tree-an-attribute-is-absent-blank-stale-or-unexpectedly-overwritten`: An attribute is absent, blank, stale, or unexpectedly overwritten
- `troubleshooting-decision-tree-family-preregistration-creates-partial-or-duplicate-records`: Family preregistration creates partial or duplicate records
- `troubleshooting-decision-tree-a-connection-request-is-missing-or-stuck`: A connection request is missing or stuck
- `troubleshooting-decision-tree-personalized-content-appears-for-the-wrong-person-or-not-at-all`: Personalized content appears for the wrong person or not at all
- `troubleshooting-decision-tree-family-analytics-or-era-values-appear-stale-or-wrong`: Family analytics or eRA values appear stale or wrong
- `agent-task-recipes-recipe-add-a-person-or-family-without-creating-a-duplicate`: Recipe: Add a person or family without creating a duplicate
- `agent-task-recipes-recipe-correct-a-family-structure-or-household-move`: Recipe: Correct a family structure or household move
- `agent-task-recipes-recipe-design-or-review-a-person-or-family-attribute`: Recipe: Design or review a person or family attribute
- `agent-task-recipes-recipe-audit-person-note-governance`: Recipe: Audit Person Note governance
- `agent-task-recipes-recipe-prepare-a-duplicate-person-merge-for-authorized-review`: Recipe: Prepare a duplicate-person merge for authorized review
- `agent-task-recipes-recipe-validate-family-preregistration-end-to-end`: Recipe: Validate family preregistration end to end
- `agent-task-recipes-recipe-diagnose-a-connection-request-from-the-person-record`: Recipe: Diagnose a connection request from the person record
- `agent-task-recipes-recipe-run-a-bounded-people-data-cleanup`: Recipe: Run a bounded people-data cleanup

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
