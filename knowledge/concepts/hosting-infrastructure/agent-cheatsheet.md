---
concept_id: hosting-infrastructure
title: Hosting And Infrastructure Agent Cheatsheet
generated: true
---

# Hosting And Infrastructure Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Inventory Hosting](tasks/recipe-inventory-hosting.md) |  |  |
| [Recipe: Validate Azure Hosting](tasks/recipe-validate-azure-hosting.md) |  |  |
| [Recipe: Review SQL Performance](tasks/recipe-review-sql-performance.md) |  |  |
| [Recipe: Review Backup And Restore](tasks/recipe-review-backup-and-restore.md) |  |  |
| [Recipe: Review Web Farm](tasks/recipe-review-web-farm.md) |  |  |
| [Recipe: Public Launch Hosting Gate](tasks/recipe-public-launch-hosting-gate.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Added an automatic data migration that moves File Storage Provider settings from any existing legacy Azure Blob Storage provider plugin (Pillars) to the core Azure Blob Storage provider. This is required because the legacy provider can no l |
| `17.5` | core | Fixed an error that occurred when editing a Content Channel Type with Attributes of type Image, File, or Binary File. The issue happened if the storage location was set to Azure Blob Storage or File System (or newly created FileType). This  |
| `17.0` | core | Improved database performance with new and revised indexes across multiple tables. These changes improve query efficiency for transactions, person records, group hierarchies, and interactions, based on SQL Server recommendations and other a |
| `18.1` | core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 |
| `17.5` | core | Fixed an issue where loading the Obsidian Attendance History block without person context could cause severe performance issues and possible server crashes by attempting to load all attendance records. The block now prevents loading attenda |
| `17.1` | core | Fixed a performance issue in Next-Gen Check-in that caused delays when printing to Bluetooth printers. The slowdown was due to how label image data was encoded, which has now been optimized. Printing performance should now be smooth and imm |
| `16.3` | core | Fixed issue where Communication Entry Wizard block becomes unusable when an SMS image attachment is auto-resized and uploaded to Azure Blob Storage. Fixes: #5719 |
| `17.2` | core | Improved the database index fill factor from 80% to 100% to reduce table size and improve maintenance performance. In the past, this was changed due to a common practice of reserving space to reduce page splits in the tables but, upon furth |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-hosting-and-infrastructure-mental-model-layer-1-request-entry` | normal | live verification |
| `3-hosting-and-infrastructure-mental-model-layer-2-web-runtime` | normal | live verification |
| `3-hosting-and-infrastructure-mental-model-layer-3-database-and-persistence` | normal | live verification |
| `3-hosting-and-infrastructure-mental-model-layer-4-shared-services` | normal | live verification |
| `3-hosting-and-infrastructure-mental-model-layer-5-operations-and-governance` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-iis-and-windows-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-sql-configuration` | high | live verification |
| `5-core-configuration-and-data-model-rock-database-records-that-affect-hosting` | high | live verification |
| `5-core-configuration-and-data-model-azure-resource-configuration` | normal | live verification |
| `6-primary-entities-and-relationships-site-domain-and-request-handling` | normal | live verification |
| `6-primary-entities-and-relationships-file-type-and-storage-provider` | normal | live verification |
| `6-primary-entities-and-relationships-communication-transport-and-smtp` | community-supported | live verification |
| `6-primary-entities-and-relationships-jobs-and-background-processing` | community-supported | community-supported |
| `6-primary-entities-and-relationships-web-farm-nodes-and-message-bus` | normal | live verification |
| `6-primary-entities-and-relationships-authentication-services` | normal | live verification |
| `7-common-hosting-and-infrastructure-workflows-refresh-development-from-production` | community-supported | live verification |
| `8-sizing-and-service-options-deep-dive-large-pattern` | community-supported | live verification |
| `9-azure-hosting-deep-dive-azure-monitoring` | citation-only | live verification |
| `10-operational-readiness-deep-dive-backup-readiness` | community-supported | community-supported |
| `10-operational-readiness-deep-dive-restore-readiness` | community-supported | live verification |
| `10-operational-readiness-deep-dive-ssl-readiness` | community-supported | live verification |
| `10-operational-readiness-deep-dive-smtp-readiness` | community-supported | live verification |
| `10-operational-readiness-deep-dive-security-readiness` | normal | live verification |
| `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-operations` | citation-only | live verification |
| `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-security` | normal | live verification |
| `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-jobs` | community-supported | live verification |
| `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-search` | normal | live verification |
| `11-related-rock-areas-operations-security-jobs-cache-search-cms-api-integrations-api-integrations` | normal | live verification |
| `12-administration-and-operational-guardrails-production-and-development-separation` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-upgrade-guardrails` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-lava-endpoints` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-source-code-version-caveat` | structural | live verification |
| `14-reporting-analytics-and-model-map-useful-operational-reports` | structural | live verification |
| `14-reporting-analytics-and-model-map-model-map-usage` | normal | live verification |
| `15-version-and-release-caveats-v19-1` | normal | live verification |
| `16-implementation-playbooks-playbook-production-readiness-review` | structural | live verification |
| `16-implementation-playbooks-playbook-azure-cost-and-capacity-review` | normal | live verification |
| `16-implementation-playbooks-playbook-storage-provider-upgrade-review` | normal | live verification |
| `17-troubleshooting-decision-tree-site-is-down` | community-supported | community-supported |
| `17-troubleshooting-decision-tree-check-in-is-slow` | citation-only | live verification |
| `17-troubleshooting-decision-tree-file-uploads-fail` | normal | live verification |
| `17-troubleshooting-decision-tree-development-environment-sends-real-messages` | community-supported | live verification |
| `18-agent-task-recipes-recipe-review-backup-and-restore` | structural | live verification |
| `18-agent-task-recipes-recipe-public-launch-hosting-gate` | structural | live verification |
| `19-source-map-and-dependency-notes` | high | live verification |
