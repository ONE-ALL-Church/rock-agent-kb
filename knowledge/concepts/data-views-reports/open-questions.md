---
concept_id: data-views-reports
title: Data Views And Reports Open Questions
generated: true
---

# Data Views And Reports Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `3-data-views-and-reports-mental-model-record-set-vs-presentation`: Record Set vs Presentation
- `3-data-views-and-reports-mental-model-reports-are-not-security-boundaries-by-themselves`: Reports Are Not Security Boundaries By Themselves
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-dynamic-report-block-configuration`: Dynamic Report Block Configuration
- `6-primary-entities-and-relationships-reportfield`: `ReportField`
- `6-primary-entities-and-relationships-block-and-page`: `Block` And `Page`
- `6-primary-entities-and-relationships-finance`: Finance
- `7-common-data-views-and-reports-workflows-workflow-2-build-a-ministry-dashboard`: Workflow 2: Build A Ministry Dashboard
- `7-common-data-views-and-reports-workflows-workflow-3-build-a-data-view-finder`: Workflow 3: Build A Data View Finder
- `7-common-data-views-and-reports-workflows-workflow-4-build-a-report-finder`: Workflow 4: Build A Report Finder
- `7-common-data-views-and-reports-workflows-workflow-5-convert-a-one-off-sql-request-into-a-governed-report`: Workflow 5: Convert A One-Off SQL Request Into A Governed Report
- `9-reports-deep-dive-report-field-design`: Report Field Design
- `9-reports-deep-dive-reports-as-page-contracts`: Reports As Page Contracts
- `9-reports-deep-dive-report-inventory-and-governance`: Report Inventory And Governance
- `10-business-intelligence-deep-dive-bi-model-layer`: BI Model Layer
- `10-business-intelligence-deep-dive-bi-finance-reports`: BI Finance Reports
- `10-business-intelligence-deep-dive-bi-family-reports`: BI Family Reports
- `11-related-rock-areas-sql-model-map-lava-finance-attendance-model-map`: Model Map
- `11-related-rock-areas-sql-model-map-lava-finance-attendance-finance`: Finance
- `12-administration-and-operational-guardrails-reporting-governance`: Reporting Governance
- `12-administration-and-operational-guardrails-database-maintenance`: Database Maintenance
- `14-reporting-analytics-and-model-map-analytics-tables-vs-transactional-tables`: Analytics Tables vs Transactional Tables
- `14-reporting-analytics-and-model-map-model-discovery-process`: Model Discovery Process
- `16-implementation-playbooks-playbook-d-build-a-finance-giving-report`: Playbook D: Build A Finance Giving Report
- `16-implementation-playbooks-playbook-f-build-a-reporting-inventory-dashboard`: Playbook F: Build A Reporting Inventory Dashboard
- `18-agent-task-recipes-recipe-build-lapsed-givers`: Recipe: Build "Lapsed Givers"
- `18-agent-task-recipes-recipe-build-where-are-our-reporting-tools`: Recipe: Build "Where Are Our Reporting Tools?"

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `2-scope-and-terminology-core-terms`: Core Terms
- `3-data-views-and-reports-mental-model-data-view-composition`: Data View Composition
- `3-data-views-and-reports-mental-model-related-data-view-semantics`: Related Data View Semantics
- `3-data-views-and-reports-mental-model-data-view-caching-and-persisted-values`: Data View Caching And Persisted Values
- `3-data-views-and-reports-mental-model-reports-are-not-security-boundaries-by-themselves`: Reports Are Not Security Boundaries By Themselves
- `4-source-authority-and-how-to-use-this-guide-how-agents-should-use-this-guide`: How Agents Should Use This Guide
- `4-source-authority-and-how-to-use-this-guide-citation-policy`: Citation Policy
- `5-core-configuration-and-data-model-data-view-configuration`: Data View Configuration
- `5-core-configuration-and-data-model-data-view-filter-data-model`: Data View Filter Data Model
- `5-core-configuration-and-data-model-dynamic-report-block-configuration`: Dynamic Report Block Configuration
- `5-core-configuration-and-data-model-lava-sql-configuration`: Lava SQL Configuration
- `6-primary-entities-and-relationships-dataview`: `DataView`
- `6-primary-entities-and-relationships-dataviewfilter`: `DataViewFilter`
- `6-primary-entities-and-relationships-report`: `Report`
- `6-primary-entities-and-relationships-reportfield`: `ReportField`
- `6-primary-entities-and-relationships-category`: `Category`
- `6-primary-entities-and-relationships-block-and-page`: `Block` And `Page`
- `6-primary-entities-and-relationships-attribute-and-attributevalue`: `Attribute` And `AttributeValue`
- `6-primary-entities-and-relationships-person-and-alias`: Person And Alias
- `6-primary-entities-and-relationships-attendance`: Attendance
- `6-primary-entities-and-relationships-analytics-models`: Analytics Models
- `7-common-data-views-and-reports-workflows-workflow-1-build-a-staff-list-report`: Workflow 1: Build A Staff List Report
- `7-common-data-views-and-reports-workflows-workflow-2-build-a-ministry-dashboard`: Workflow 2: Build A Ministry Dashboard
- `7-common-data-views-and-reports-workflows-workflow-3-build-a-data-view-finder`: Workflow 3: Build A Data View Finder
- `7-common-data-views-and-reports-workflows-workflow-6-build-a-bi-report`: Workflow 6: Build A BI Report
- `8-data-views-deep-dive-filter-tree-design`: Filter Tree Design
- `8-data-views-deep-dive-security`: Security
- `8-data-views-deep-dive-related-data-views`: Related Data Views
- `8-data-views-deep-dive-post-filter-transformations`: Post-Filter Transformations
- `8-data-views-deep-dive-data-view-usage-before-editing`: Data View Usage Before Editing
- `8-data-views-deep-dive-testing-data-views`: Testing Data Views
- `8-data-views-deep-dive-common-data-view-anti-patterns`: Common Data View Anti-Patterns
- `9-reports-deep-dive-dynamic-report-runtime-filters`: Dynamic Report Runtime Filters
- `9-reports-deep-dive-reports-as-page-contracts`: Reports As Page Contracts
- `9-reports-deep-dive-report-security`: Report Security
- `10-business-intelligence-deep-dive-bi-job`: BI Job
- `10-business-intelligence-deep-dive-power-bi-template`: Power BI Template

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
