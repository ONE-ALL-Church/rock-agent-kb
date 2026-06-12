---
concept_id: api-integrations
title: API And Integrations Agent Cheatsheet
generated: true
---

# API And Integrations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Find The Right API Route](tasks/recipe-find-the-right-api-route.md) |  |  |
| [Recipe: Audit A REST Key](tasks/recipe-audit-a-rest-key.md) |  |  |
| [Recipe: Diagnose External Website API Failure](tasks/recipe-diagnose-external-website-api-failure.md) |  |  |
| [Recipe: Review A Lava Webhook Before Launch](tasks/recipe-review-a-lava-webhook-before-launch.md) |  |  |
| [Recipe: Build A Safe Agent Tool](tasks/recipe-build-a-safe-agent-tool.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 |
| `16.1` | core | Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694 |
| `15.5` | core | Improved the Mailgun integration to use the API Key for tracking opens, etc. if the HTTP Webhook Signing Key is not defined, as well as logging a single exception to alert Rock admins of this missing key value. Fixes: #5780 |
| `15.4` | core | Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694 |
| `18.2` | core | Fixed an error that prevented the Workflows Action Launch API endpoint from functioning. Fixes: #6604 |
| `17.5` | core | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to t |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | needs-citation | needs-citation |
| `2-scope-and-terminology-api` | needs-citation | live verification |
| `2-scope-and-terminology-rest-api-v1` | normal | live verification |
| `2-scope-and-terminology-odata` | normal | live verification |
| `2-scope-and-terminology-swagger-api-docs` | community-supported | live verification |
| `2-scope-and-terminology-rest-key-authorization-token` | normal | live verification |
| `2-scope-and-terminology-webhook-to-workflow` | community-supported | live verification |
| `3-api-and-integrations-mental-model-identity-and-permission-chain` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | community-supported | live verification |
| `5-core-configuration-and-data-model-rest-controllers-and-rest-actions` | normal | live verification |
| `5-core-configuration-and-data-model-rest-cors-domains` | normal | live verification |
| `5-core-configuration-and-data-model-lava-webhook-defined-type` | normal | live verification |
| `5-core-configuration-and-data-model-workflow-webhook-defined-type` | community-supported | live verification |
| `6-primary-entities-and-relationships-restcontroller-and-restaction` | citation-only | live verification |
| `6-primary-entities-and-relationships-person-userlogin-rest-key-and-person-token` | normal | live verification |
| `6-primary-entities-and-relationships-binaryfile-document-type-and-file-security` | normal | live verification |
| `7-common-api-and-integrations-workflows-external-site-reads-public-calendar-data` | community-supported | live verification |
| `7-common-api-and-integrations-workflows-external-system-sends-a-webhook-to-rock` | community-supported | community-supported |
| `7-common-api-and-integrations-workflows-rock-calls-an-external-api-from-lava` | normal | live verification |
| `7-common-api-and-integrations-workflows-launch-a-workflow-through-rest-v2` | normal | live verification |
| `8-rest-api-deep-dive-route-discovery` | normal | live verification |
| `8-rest-api-deep-dive-cruds-pattern` | normal | live verification |
| `8-rest-api-deep-dive-identifier-handling` | normal | live verification |
| `8-rest-api-deep-dive-odata-querying` | normal | live verification |
| `9-api-authentication-deep-dive-api-key-purpose` | normal | live verification |
| `9-api-authentication-deep-dive-external-identity-providers` | normal | live verification |
| `10-webhooks-deep-dive-lava-webhook-matching` | normal | live verification |
| `10-webhooks-deep-dive-response-content-types` | community-supported | community-supported |
| `10-webhooks-deep-dive-workflow-webhook-response` | community-supported | live verification |
| `11-related-rock-areas-security-workflows-lava-model-map-model-map` | normal | live verification |
| `12-administration-and-operational-guardrails-rate-limiting-and-load` | normal | live verification |
| `12-administration-and-operational-guardrails-observability` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-security-and-workflow-source` | normal | live verification |
| `14-reporting-analytics-and-model-map-api-usage-reporting` | normal | live verification |
| `15-version-and-release-caveats-api-v2-starts-in-v17-pattern` | normal | live verification |
| `15-version-and-release-caveats-mailgun-api-key-and-webhook-signing-key` | normal | live verification |
| `15-version-and-release-caveats-helix-and-lava-applications` | normal | live verification |
| `15-version-and-release-caveats-mobile-and-shell-caveats` | normal | live verification |
| `16-implementation-playbooks-playbook-a-server-to-server-rest-read-integration` | needs-citation | live verification |
| `16-implementation-playbooks-playbook-b-browser-public-data-feed` | needs-citation | needs-citation |
| `16-implementation-playbooks-playbook-c-webhook-to-workflow-intake` | needs-citation | live verification |
| `16-implementation-playbooks-playbook-e-custom-rest-v2-endpoint` | normal | live verification |
| `16-implementation-playbooks-playbook-f-agent-tool-for-rock-data` | normal | live verification |
| `17-troubleshooting-decision-tree-works-in-postman-but-not-browser` | structural | live verification |
| `18-agent-task-recipes-recipe-find-the-right-api-route` | structural | live verification |
| `18-agent-task-recipes-recipe-diagnose-external-website-api-failure` | structural | live verification |
| `18-agent-task-recipes-recipe-review-a-lava-webhook-before-launch` | structural | live verification |
| `18-agent-task-recipes-recipe-build-a-safe-agent-tool` | normal | live verification |
| `approved-claim-coverage` | normal | live verification |
