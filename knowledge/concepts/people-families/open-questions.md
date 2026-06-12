---
concept_id: people-families
title: People And Families Open Questions
generated: true
---

# People And Families Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `12-administration-and-operational-guardrails-person-data-is-high-impact`: Person Data Is High Impact (94 words)
- `12-administration-and-operational-guardrails-data-integrity-monitoring`: Data Integrity Monitoring (104 words)
- `19-source-map-and-dependency-notes-records-requiring-live-verification`: Records Requiring Live Verification (106 words)

## Community-Supported Only

- `7-common-people-and-families-workflows-delete-or-deactivate-a-person`: Delete Or Deactivate A Person
- `7-common-people-and-families-workflows-track-how-a-person-record-was-created`: Track How A Person Record Was Created
- `14-reporting-analytics-and-model-map-family-reporting`: Family Reporting
- `14-reporting-analytics-and-model-map-data-views-and-automation`: Data Views And Automation
- `14-reporting-analytics-and-model-map-profile-custom-reports`: Profile Custom Reports
- `16-implementation-playbooks-playbook-recover-from-wrong-merge`: Playbook: Recover From Wrong Merge
- `18-agent-task-recipes-recipe-triage-an-accidental-merge`: Recipe: Triage An Accidental Merge
- `18-agent-task-recipes-recipe-build-a-staff-directory-from-person-attributes`: Recipe: Build A Staff Directory From Person Attributes
- `18-agent-task-recipes-recipe-add-a-bookmarked-groups-like-profile-panel`: Recipe: Add A Bookmarked Groups-Like Profile Panel
- `19-source-map-and-dependency-notes-community-recipes-used-as-examples-only`: Community Recipes Used As Examples Only

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-people-and-families-mental-model`: 3. People And Families Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-person`: Person
- `5-core-configuration-and-data-model-personalias`: PersonAlias
- `5-core-configuration-and-data-model-family-group`: Family Group
- `5-core-configuration-and-data-model-groupmember-and-grouptyperole`: GroupMember And GroupTypeRole
- `5-core-configuration-and-data-model-known-relationships`: Known Relationships
- `5-core-configuration-and-data-model-notes-tags-following-badges-assessments-background-checks`: Notes, Tags, Following, Badges, Assessments, Background Checks
- `6-primary-entities-and-relationships-person-to-personalias`: Person To PersonAlias
- `6-primary-entities-and-relationships-person-to-family-group`: Person To Family Group
- `6-primary-entities-and-relationships-family-group-to-grouplocation-and-location`: Family Group To GroupLocation And Location
- `6-primary-entities-and-relationships-group-or-family-to-attributes`: Group Or Family To Attributes
- `6-primary-entities-and-relationships-person-to-communications`: Person To Communications
- `7-common-people-and-families-workflows-search-for-a-person`: Search For A Person
- `7-common-people-and-families-workflows-add-or-edit-an-individual`: Add Or Edit An Individual
- `7-common-people-and-families-workflows-add-or-edit-a-family`: Add Or Edit A Family
- `7-common-people-and-families-workflows-merge-duplicate-records`: Merge Duplicate Records
- `7-common-people-and-families-workflows-delete-or-deactivate-a-person`: Delete Or Deactivate A Person
- `7-common-people-and-families-workflows-add-person-or-family-attributes`: Add Person Or Family Attributes
- `7-common-people-and-families-workflows-track-how-a-person-record-was-created`: Track How A Person Record Was Created
- `7-common-people-and-families-workflows-run-person-based-automation`: Run Person-Based Automation
- `8-person-model-deep-dive-identity-fields`: Identity Fields
- `8-person-model-deep-dive-names`: Names
- `8-person-model-deep-dive-demographics`: Demographics
- `8-person-model-deep-dive-contact-fields`: Contact Fields
- `8-person-model-deep-dive-logins-account-protection-impersonation-and-passwordless-login`: Logins, Account Protection, Impersonation, And Passwordless Login
- `9-families-deep-dive-family-as-group`: Family As Group
- `9-families-deep-dive-family-giving`: Family Giving
- `10-attributes-deep-dive-attribute-lava-filters`: Attribute Lava Filters
- `10-attributes-deep-dive-entity-commands-and-attribute-prefetch`: Entity Commands And Attribute Prefetch
- `10-attributes-deep-dive-attribute-migration-and-source-control`: Attribute Migration And Source Control
- `11-related-rock-areas-groups-security-communications-check-in-communications`: Communications
- `12-administration-and-operational-guardrails-before-merging`: Before Merging
- `13-developer-api-lava-and-source-code-landmarks-person-lava-filters`: Person Lava Filters
- `13-developer-api-lava-and-source-code-landmarks-setpersonattribute-workflow-action`: SetPersonAttribute Workflow Action
- `13-developer-api-lava-and-source-code-landmarks-personattributeforms-block`: PersonAttributeForms Block
- `13-developer-api-lava-and-source-code-landmarks-mobile-person-profile-block`: Mobile Person Profile Block

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
