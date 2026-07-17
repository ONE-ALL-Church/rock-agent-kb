---
concept_id: api-integrations
title: API And Integrations Open Questions
generated: true
---

# API And Integrations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `2-scope-and-terminology-swagger-api-docs`: Swagger / API Docs
- `2-scope-and-terminology-webhook-to-workflow`: Webhook To Workflow
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-workflow-webhook-defined-type`: Workflow Webhook Defined Type
- `7-common-api-and-integrations-workflows-external-site-reads-public-calendar-data`: External Site Reads Public Calendar Data
- `7-common-api-and-integrations-workflows-external-system-sends-a-webhook-to-rock`: External System Sends A Webhook To Rock
- `10-webhooks-deep-dive-response-content-types`: Response Content Types
- `10-webhooks-deep-dive-workflow-webhook-response`: Workflow Webhook Response

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology-api`: API
- `2-scope-and-terminology-rest-api-v1`: REST API v1
- `2-scope-and-terminology-odata`: OData
- `2-scope-and-terminology-swagger-api-docs`: Swagger / API Docs
- `2-scope-and-terminology-rest-key-authorization-token`: REST Key / Authorization Token
- `2-scope-and-terminology-webhook-to-workflow`: Webhook To Workflow
- `3-api-and-integrations-mental-model-identity-and-permission-chain`: Identity And Permission Chain
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-rest-controllers-and-rest-actions`: REST Controllers And REST Actions
- `5-core-configuration-and-data-model-rest-cors-domains`: REST CORS Domains
- `5-core-configuration-and-data-model-lava-webhook-defined-type`: Lava Webhook Defined Type
- `5-core-configuration-and-data-model-workflow-webhook-defined-type`: Workflow Webhook Defined Type
- `6-primary-entities-and-relationships-restcontroller-and-restaction`: RestController And RestAction
- `6-primary-entities-and-relationships-person-userlogin-rest-key-and-person-token`: Person, UserLogin, REST Key, And Person Token
- `6-primary-entities-and-relationships-binaryfile-document-type-and-file-security`: BinaryFile, Document Type, And File Security
- `7-common-api-and-integrations-workflows-external-site-reads-public-calendar-data`: External Site Reads Public Calendar Data
- `7-common-api-and-integrations-workflows-rock-calls-an-external-api-from-lava`: Rock Calls An External API From Lava
- `7-common-api-and-integrations-workflows-launch-a-workflow-through-rest-v2`: Launch A Workflow Through REST v2
- `8-rest-api-deep-dive-route-discovery`: Route Discovery
- `8-rest-api-deep-dive-cruds-pattern`: CRUDS Pattern
- `8-rest-api-deep-dive-identifier-handling`: Identifier Handling
- `8-rest-api-deep-dive-odata-querying`: OData Querying
- `9-api-authentication-deep-dive-api-key-purpose`: API Key Purpose
- `9-api-authentication-deep-dive-external-identity-providers`: External Identity Providers
- `10-webhooks-deep-dive-lava-webhook-matching`: Lava Webhook Matching
- `10-webhooks-deep-dive-workflow-webhook-response`: Workflow Webhook Response
- `11-related-rock-areas-security-workflows-lava-model-map-model-map`: Model Map
- `12-administration-and-operational-guardrails-rate-limiting-and-load`: Rate Limiting And Load
- `12-administration-and-operational-guardrails-observability`: Observability
- `13-developer-api-lava-and-source-code-landmarks-security-and-workflow-source`: Security And Workflow Source
- `14-reporting-analytics-and-model-map-api-usage-reporting`: API Usage Reporting
- `15-version-and-release-caveats-api-v2-starts-in-v17-pattern`: API v2 Starts In v17 Pattern
- `15-version-and-release-caveats-mailgun-api-key-and-webhook-signing-key`: Mailgun API Key And Webhook Signing Key
- `15-version-and-release-caveats-helix-and-lava-applications`: Helix And Lava Applications
- `15-version-and-release-caveats-mobile-and-shell-caveats`: Mobile And Shell Caveats
- `16-implementation-playbooks-playbook-a-server-to-server-rest-read-integration`: Playbook A: Server-To-Server REST Read Integration
- `16-implementation-playbooks-playbook-c-webhook-to-workflow-intake`: Playbook C: Webhook To Workflow Intake
- `16-implementation-playbooks-playbook-e-custom-rest-v2-endpoint`: Playbook E: Custom REST v2 Endpoint

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
