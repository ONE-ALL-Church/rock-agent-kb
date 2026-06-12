---
concept_id: platform-configuration
title: Platform Configuration Open Questions
generated: true
---

# Platform Configuration Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `8-attributes-and-attribute-values-deep-dive-attribute-definition-fields`: Attribute Definition Fields (92 words)
- `15-reporting-analytics-and-model-map-reporting-rules`: Reporting Rules (145 words)
- `18-troubleshooting-decision-tree-attribute-does-not-appear`: Attribute Does Not Appear (96 words)

## Community-Supported Only

- `11-campuses-and-global-settings-deep-dive-campus-filters-in-reports`: Campus Filters In Reports
- `12-related-rock-areas-people-groups-workflows-cms-security-data-views-reports-operations-groups`: Groups

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-platform-configuration-mental-model`: 3. Platform Configuration Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-entity-types`: Entity Types
- `5-core-configuration-and-data-model-attribute-values`: Attribute Values
- `5-core-configuration-and-data-model-field-types`: Field Types
- `5-core-configuration-and-data-model-categories`: Categories
- `5-core-configuration-and-data-model-global-attributes-and-system-settings`: Global Attributes And System Settings
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `6-primary-entities-and-relationships-campus-relationship-map`: Campus Relationship Map
- `7-common-platform-configuration-workflows-add-a-person-attribute`: Add A Person Attribute
- `7-common-platform-configuration-workflows-add-a-connection-request-attribute`: Add A Connection Request Attribute
- `7-common-platform-configuration-workflows-configure-a-campus-aware-report`: Configure A Campus-Aware Report
- `7-common-platform-configuration-workflows-add-mobile-site-attributes`: Add Mobile Site Attributes
- `7-common-platform-configuration-workflows-use-attributes-in-custom-blocks`: Use Attributes In Custom Blocks
- `8-attributes-and-attribute-values-deep-dive-attribute-definition-fields`: Attribute Definition Fields
- `8-attributes-and-attribute-values-deep-dive-qualifiers`: Qualifiers
- `8-attributes-and-attribute-values-deep-dive-raw-values-versus-formatted-values`: Raw Values Versus Formatted Values
- `8-attributes-and-attribute-values-deep-dive-attribute-values-in-lava`: Attribute Values In Lava
- `9-defined-types-and-values-deep-dive-defined-type-fields-to-inspect`: Defined Type Fields To Inspect
- `9-defined-types-and-values-deep-dive-defined-value-fields-to-inspect`: Defined Value Fields To Inspect
- `9-defined-types-and-values-deep-dive-categorizing-defined-values`: Categorizing Defined Values
- `10-categories-and-entity-types-deep-dive-entity-type-security`: Entity Type Security
- `10-categories-and-entity-types-deep-dive-category-version-caveats`: Category Version Caveats
- `11-campuses-and-global-settings-deep-dive-campus-as-context`: Campus As Context
- `11-campuses-and-global-settings-deep-dive-campus-filters-in-reports`: Campus Filters In Reports
- `11-campuses-and-global-settings-deep-dive-global-attributes`: Global Attributes
- `11-campuses-and-global-settings-deep-dive-system-settings`: System Settings
- `12-related-rock-areas-people-groups-workflows-cms-security-data-views-reports-operations-data-views`: Data Views
- `13-administration-and-operational-guardrails-change-management`: Change Management
- `13-administration-and-operational-guardrails-public-exposure`: Public Exposure
- `14-developer-api-lava-and-source-code-landmarks-field-types-and-field-attributes`: Field Types And Field Attributes
- `15-reporting-analytics-and-model-map-reporting-rules`: Reporting Rules
- `16-version-and-release-caveats-rock-v10-3`: Rock v10.3+
- `16-version-and-release-caveats-rock-v15-0`: Rock v15.0+
- `16-version-and-release-caveats-rock-v17-and-v17-5`: Rock v17 And v17.5+
- `16-version-and-release-caveats-rock-v19-1`: Rock v19.1
- `17-implementation-playbooks-playbook-audit-an-attribute-before-editing`: Playbook: Audit An Attribute Before Editing

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
