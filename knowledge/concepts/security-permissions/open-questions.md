---
concept_id: security-permissions
title: Security And Permissions Open Questions
generated: true
---

# Security And Permissions Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `3-security-and-permissions-mental-model-the-direct-rule-layer`: The Direct Rule Layer
- `3-security-and-permissions-mental-model-the-inheritance-layer`: The Inheritance Layer
- `4-source-authority-and-how-to-use-this-guide-lower-authority-but-useful-sources`: Lower Authority But Useful Sources
- `5-core-configuration-and-data-model-auth-records`: `Auth` Records
- `5-core-configuration-and-data-model-security-roles-as-groups`: Security Roles As Groups
- `7-common-security-and-permissions-workflows-explain-why-a-user-can-see-a-page`: Explain Why A User Can See A Page
- `7-common-security-and-permissions-workflows-create-a-new-security-role`: Create A New Security Role
- `7-common-security-and-permissions-workflows-remove-access-for-departed-staff`: Remove Access For Departed Staff
- `8-authorization-deep-dive-allow-and-deny-strategy`: Allow And Deny Strategy
- `8-authorization-deep-dive-person-specific-permissions`: Person-Specific Permissions
- `10-related-rock-areas-people-groups-api-cms-workflows-people`: People
- `11-administration-and-operational-guardrails-least-privilege`: Least Privilege
- `11-administration-and-operational-guardrails-sensitive-domain-guardrails`: Sensitive Domain Guardrails
- `11-administration-and-operational-guardrails-temporary-access-and-impersonation`: Temporary Access And Impersonation
- `11-administration-and-operational-guardrails-security-audits`: Security Audits
- `13-reporting-analytics-and-model-map-dynamic-data-and-sql-reports`: Dynamic Data And SQL Reports
- `14-version-and-release-caveats-v15-fluid-lava-requirement-for-some-community-security-tools`: v15: Fluid Lava Requirement For Some Community Security Tools
- `15-implementation-playbooks-playbook-audit-who-can-administrate-a-page`: Playbook: Audit Who Can Administrate A Page
- `15-implementation-playbooks-playbook-build-a-staff-only-report-page`: Playbook: Build A Staff-Only Report Page
- `16-troubleshooting-decision-tree-user-can-see-too-much-data`: User Can See Too Much Data
- `17-agent-task-recipes-recipe-answer-who-has-access-to-this`: Recipe: Answer “Who Has Access To This?”
- `17-agent-task-recipes-recipe-review-a-security-role`: Recipe: Review A Security Role

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `2-scope-and-terminology-out-of-scope`: Out Of Scope
- `3-security-and-permissions-mental-model-the-actor-layer`: The Actor Layer
- `3-security-and-permissions-mental-model-the-action-layer`: The Action Layer
- `3-security-and-permissions-mental-model-the-direct-rule-layer`: The Direct Rule Layer
- `3-security-and-permissions-mental-model-the-inheritance-layer`: The Inheritance Layer
- `3-security-and-permissions-mental-model-the-cache-layer`: The Cache Layer
- `4-source-authority-and-how-to-use-this-guide-medium-authority-sources`: Medium Authority Sources
- `4-source-authority-and-how-to-use-this-guide-lower-authority-but-useful-sources`: Lower Authority But Useful Sources
- `4-source-authority-and-how-to-use-this-guide-how-agents-should-use-this-guide`: How Agents Should Use This Guide
- `5-core-configuration-and-data-model`: 5. Core Configuration And Data Model
- `5-core-configuration-and-data-model-core-configuration-areas`: Core Configuration Areas
- `5-core-configuration-and-data-model-auth-records`: `Auth` Records
- `5-core-configuration-and-data-model-authorization-constants`: Authorization Constants
- `5-core-configuration-and-data-model-security-roles-as-groups`: Security Roles As Groups
- `5-core-configuration-and-data-model-person-user-login-and-account-security`: Person, User Login, And Account Security
- `5-core-configuration-and-data-model-api-keys-and-purpose`: API Keys And Purpose
- `5-core-configuration-and-data-model-document-type-and-file-type-security`: Document Type And File Type Security
- `5-core-configuration-and-data-model-workflow-type-security`: Workflow Type Security
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `6-primary-entities-and-relationships-person-userlogin-group-and-security-role`: Person, UserLogin, Group, And Security Role
- `6-primary-entities-and-relationships-entitytype-and-securable-entities`: EntityType And Securable Entities
- `6-primary-entities-and-relationships-page-site-and-block`: Page, Site, And Block
- `6-primary-entities-and-relationships-api-endpoints-auth-clients-claims-and-scopes`: API Endpoints, Auth Clients, Claims, And Scopes
- `7-common-security-and-permissions-workflows-grant-a-staff-user-access-to-a-page`: Grant A Staff User Access To A Page
- `7-common-security-and-permissions-workflows-explain-why-a-user-can-see-a-page`: Explain Why A User Can See A Page
- `7-common-security-and-permissions-workflows-create-a-new-security-role`: Create A New Security Role
- `7-common-security-and-permissions-workflows-secure-a-custom-block`: Secure A Custom Block
- `7-common-security-and-permissions-workflows-secure-a-custom-lava-page`: Secure A Custom Lava Page
- `7-common-security-and-permissions-workflows-secure-a-rest-integration`: Secure A REST Integration
- `8-authorization-deep-dive-standard-actions`: Standard Actions
- `8-authorization-deep-dive-allow-and-deny-strategy`: Allow And Deny Strategy
- `8-authorization-deep-dive-page-and-block-security-order`: Page And Block Security Order
- `8-authorization-deep-dive-entity-parent-authority`: Entity Parent Authority
- `8-authorization-deep-dive-authorization-cache`: Authorization Cache
- `9-api-auth-deep-dive-legacy-rest-api-authorization`: Legacy REST API Authorization
- `9-api-auth-deep-dive-v2-api-pattern`: v2 API Pattern
- `9-api-auth-deep-dive-api-keys`: API Keys

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
