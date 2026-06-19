---
concept_id: hosting-infrastructure
title: Hosting And Infrastructure Open Questions
generated: true
---

# Hosting And Infrastructure Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `5-core-configuration-and-data-model-rock-database-records-that-affect-hosting`: Rock Database Records That Affect Hosting (121 words)
- `14-reporting-analytics-and-model-map-model-map-usage`: Model Map Usage (83 words)

## Community-Supported Only

- `6-primary-entities-and-relationships-communication-transport-and-smtp`: Communication Transport And SMTP
- `6-primary-entities-and-relationships-jobs-and-background-processing`: Jobs And Background Processing
- `7-common-hosting-and-infrastructure-workflows-refresh-development-from-production`: Refresh Development From Production
- `8-sizing-and-service-options-deep-dive-large-pattern`: Large Pattern
- `10-operational-readiness-deep-dive-backup-readiness`: Backup Readiness
- `10-operational-readiness-deep-dive-restore-readiness`: Restore Readiness
- `10-operational-readiness-deep-dive-ssl-readiness`: SSL Readiness
- `10-operational-readiness-deep-dive-smtp-readiness`: SMTP Readiness
- `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-jobs`: Jobs
- `12-administration-and-operational-guardrails-production-and-development-separation`: Production And Development Separation
- `17-troubleshooting-decision-tree-site-is-down`: Site Is Down
- `17-troubleshooting-decision-tree-development-environment-sends-real-messages`: Development Environment Sends Real Messages

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-hosting-and-infrastructure-mental-model-layer-1-request-entry`: Layer 1: Request Entry
- `3-hosting-and-infrastructure-mental-model-layer-2-web-runtime`: Layer 2: Web Runtime
- `3-hosting-and-infrastructure-mental-model-layer-3-database-and-persistence`: Layer 3: Database And Persistence
- `3-hosting-and-infrastructure-mental-model-layer-4-shared-services`: Layer 4: Shared Services
- `3-hosting-and-infrastructure-mental-model-layer-5-operations-and-governance`: Layer 5: Operations And Governance
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-iis-and-windows-configuration`: IIS And Windows Configuration
- `5-core-configuration-and-data-model-sql-configuration`: SQL Configuration
- `5-core-configuration-and-data-model-rock-database-records-that-affect-hosting`: Rock Database Records That Affect Hosting
- `5-core-configuration-and-data-model-azure-resource-configuration`: Azure Resource Configuration
- `6-primary-entities-and-relationships-site-domain-and-request-handling`: Site, Domain, And Request Handling
- `6-primary-entities-and-relationships-file-type-and-storage-provider`: File Type And Storage Provider
- `6-primary-entities-and-relationships-communication-transport-and-smtp`: Communication Transport And SMTP
- `6-primary-entities-and-relationships-web-farm-nodes-and-message-bus`: Web Farm Nodes And Message Bus
- `6-primary-entities-and-relationships-authentication-services`: Authentication Services
- `7-common-hosting-and-infrastructure-workflows-refresh-development-from-production`: Refresh Development From Production
- `8-sizing-and-service-options-deep-dive-large-pattern`: Large Pattern
- `9-azure-hosting-deep-dive-azure-monitoring`: Azure Monitoring
- `10-operational-readiness-deep-dive-restore-readiness`: Restore Readiness
- `10-operational-readiness-deep-dive-ssl-readiness`: SSL Readiness
- `10-operational-readiness-deep-dive-smtp-readiness`: SMTP Readiness
- `10-operational-readiness-deep-dive-security-readiness`: Security Readiness
- `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-operations`: Operations
- `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-security`: Security
- `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-jobs`: Jobs
- `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-search`: Search
- `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-api-integrations`: API Integrations
- `12-administration-and-operational-guardrails-upgrade-guardrails`: Upgrade Guardrails
- `13-developer-api-lava-and-source-code-landmarks`: 13. Developer, API, Lava, And Source-Code Landmarks
- `13-developer-api-lava-and-source-code-landmarks-lava-endpoints`: Lava Endpoints
- `13-developer-api-lava-and-source-code-landmarks-source-code-version-caveat`: Source-Code Version Caveat
- `14-reporting-analytics-and-model-map-useful-operational-reports`: Useful Operational Reports
- `14-reporting-analytics-and-model-map-model-map-usage`: Model Map Usage
- `15-version-and-release-caveats-v19-1`: v19.1
- `16-implementation-playbooks-playbook-production-readiness-review`: Playbook: Production Readiness Review
- `16-implementation-playbooks-playbook-azure-cost-and-capacity-review`: Playbook: Azure Cost And Capacity Review
- `16-implementation-playbooks-playbook-storage-provider-upgrade-review`: Playbook: Storage Provider Upgrade Review

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
