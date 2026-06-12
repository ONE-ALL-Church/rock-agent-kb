---
concept_id: workflows
title: Workflows Open Questions
generated: true
---

# Workflows Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `5-core-configuration-and-data-model-workflow-attributes`: Workflow Attributes
- `7-common-workflows-workflows-request-intake-workflow`: Request Intake Workflow
- `7-common-workflows-workflows-event-call-to-action-workflow`: Event Call-To-Action Workflow
- `7-common-workflows-workflows-staff-approval-workflow`: Staff Approval Workflow
- `7-common-workflows-workflows-helper-workflow`: Helper Workflow
- `7-common-workflows-workflows-grid-launched-workflow`: Grid-Launched Workflow
- `7-common-workflows-workflows-webhook-to-workflow-integration`: Webhook-To-Workflow Integration
- `7-common-workflows-workflows-electronic-signature-workflow`: Electronic Signature Workflow
- `7-common-workflows-workflows-bulk-creation-workflow`: Bulk Creation Workflow
- `7-common-workflows-workflows-finance-or-contribution-workflow`: Finance Or Contribution Workflow
- `8-triggers-and-activation-deep-dive-webhook-activation`: Webhook Activation
- `8-triggers-and-activation-deep-dive-grid-activation`: Grid Activation
- `8-triggers-and-activation-deep-dive-connection-step-group-and-requirement-activation`: Connection, Step, Group, And Requirement Activation
- `9-workflow-forms-deep-dive-modal-workflow-entry`: Modal Workflow Entry
- `10-workflow-integrations-deep-dive-outbound-webhooks-and-zapier`: Outbound Webhooks And Zapier
- `10-workflow-integrations-deep-dive-inbound-webhooks`: Inbound Webhooks
- `10-workflow-integrations-deep-dive-communications`: Communications
- `10-workflow-integrations-deep-dive-connections`: Connections
- `10-workflow-integrations-deep-dive-groups-and-group-member-attributes`: Groups And Group Member Attributes
- `11-related-rock-areas-lava-jobs-communications-security-attributes-jobs`: Jobs
- `11-related-rock-areas-lava-jobs-communications-security-attributes-attributes`: Attributes
- `12-administration-and-operational-guardrails-where-used-audits`: Where-Used Audits
- `12-administration-and-operational-guardrails-active-workflow-hygiene`: Active Workflow Hygiene
- `14-reporting-analytics-and-model-map-what-to-report`: What To Report
- `14-reporting-analytics-and-model-map-reporting-caveats`: Reporting Caveats
- `14-reporting-analytics-and-model-map-health-metrics`: Health Metrics
- `16-implementation-playbooks-playbook-add-a-workflow-to-a-grid`: Playbook: Add A Workflow To A Grid
- `16-implementation-playbooks-playbook-create-a-helper-workflow`: Playbook: Create A Helper Workflow
- `16-implementation-playbooks-playbook-build-webhook-to-workflow`: Playbook: Build Webhook-To-Workflow
- `16-implementation-playbooks-playbook-audit-a-workflow-before-editing`: Playbook: Audit A Workflow Before Editing

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-workflows-mental-model`: 3. Workflows Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-workflow-type-configuration`: Workflow Type Configuration
- `5-core-configuration-and-data-model-workflow-forms`: Workflow Forms
- `5-core-configuration-and-data-model-persistence-and-processing`: Persistence And Processing
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `7-common-workflows-workflows-event-call-to-action-workflow`: Event Call-To-Action Workflow
- `7-common-workflows-workflows-helper-workflow`: Helper Workflow
- `7-common-workflows-workflows-finance-or-contribution-workflow`: Finance Or Contribution Workflow
- `8-triggers-and-activation-deep-dive-workflow-entry-activation`: Workflow Entry Activation
- `8-triggers-and-activation-deep-dive-entity-triggers`: Entity Triggers
- `8-triggers-and-activation-deep-dive-lava-workflowactivate`: Lava `workflowactivate`
- `8-triggers-and-activation-deep-dive-connection-step-group-and-requirement-activation`: Connection, Step, Group, And Requirement Activation
- `9-workflow-forms-deep-dive-form-design-principles`: Form Design Principles
- `9-workflow-forms-deep-dive-conditional-logic`: Conditional Logic
- `9-workflow-forms-deep-dive-person-entry`: Person Entry
- `9-workflow-forms-deep-dive-campus-selection-and-inactive-campuses`: Campus Selection And Inactive Campuses
- `9-workflow-forms-deep-dive-modal-workflow-entry`: Modal Workflow Entry
- `10-workflow-integrations-deep-dive-outbound-webhooks-and-zapier`: Outbound Webhooks And Zapier
- `10-workflow-integrations-deep-dive-inbound-webhooks`: Inbound Webhooks
- `11-related-rock-areas-lava-jobs-communications-security-attributes-lava`: Lava
- `11-related-rock-areas-lava-jobs-communications-security-attributes-communications`: Communications
- `11-related-rock-areas-lava-jobs-communications-security-attributes-security`: Security
- `12-administration-and-operational-guardrails-naming-standards`: Naming Standards
- `12-administration-and-operational-guardrails-change-management`: Change Management
- `12-administration-and-operational-guardrails-maximum-age-and-auto-completion`: Maximum Age And Auto-Completion
- `12-administration-and-operational-guardrails-public-form-guardrails`: Public Form Guardrails
- `13-developer-api-lava-and-source-code-landmarks-lava-command-source`: Lava Command Source
- `13-developer-api-lava-and-source-code-landmarks-deprecated-activate-workflow-block`: Deprecated Activate Workflow Block
- `13-developer-api-lava-and-source-code-landmarks-person-entry-source`: Person Entry Source
- `13-developer-api-lava-and-source-code-landmarks-api-and-data-access`: API And Data Access
- `14-reporting-analytics-and-model-map-model-map-use`: Model Map Use
- `14-reporting-analytics-and-model-map-reporting-caveats`: Reporting Caveats
- `14-reporting-analytics-and-model-map-health-metrics`: Health Metrics
- `15-version-and-release-caveats`: 15. Version And Release Caveats
- `16-implementation-playbooks-playbook-build-a-public-intake-workflow`: Playbook: Build A Public Intake Workflow
- `16-implementation-playbooks-playbook-add-a-workflow-to-a-grid`: Playbook: Add A Workflow To A Grid

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
