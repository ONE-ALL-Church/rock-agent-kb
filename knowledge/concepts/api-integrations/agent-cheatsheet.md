---
concept_id: api-integrations
title: API And Integrations Agent Cheatsheet
generated: true
---

# API And Integrations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Preflight A REST Integration](tasks/recipe-preflight-a-rest-integration.md) |  |  |
| [Recipe: Configure And Review A REST Key](tasks/recipe-configure-and-review-a-rest-key.md) |  |  |
| [Recipe: Perform A Bounded API v2 Partial Update](tasks/recipe-perform-a-bounded-api-v2-partial-update.md) |  |  |
| [Recipe: Review A Lava Webhook Before Production](tasks/recipe-review-a-lava-webhook-before-production.md) | `Workflow` | `Workflow` |
| [Recipe: Review A Helix Application Flow](tasks/recipe-review-a-helix-application-flow.md) |  |  |
| [Recipe: Build A Provider Event Health Report](tasks/recipe-build-a-provider-event-health-report.md) | `Person`, `DataView` | `Person`, `DataView` |
| [Recipe: Approve An AI Or MCP Tool Boundary](tasks/recipe-approve-an-ai-or-mcp-tool-boundary.md) | `Person` | `Person` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 |
| `16.1` | core | Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | needs-citation | live verification |
| `mental-model` | needs-citation | live verification |
| `rest-api-api-v1` | normal | live verification |
| `rest-api-api-v2` | normal | live verification |
| `rest-api-partial-and-relationship-writes` | normal | live verification |
| `lava-apis-and-webhooks` | citation-only | live verification |
| `lava-apis-and-webhooks-community-webhook-example` | community-supported | community-supported |
| `helix-lava-endpoints` | normal | live verification |
| `helix-lava-endpoints-rendering-and-caching` | normal | live verification |
| `helix-lava-endpoints-public-ui-integration-boundary` | normal | live verification |
| `provider-webhooks-and-operational-reporting` | normal | live verification |
| `ai-mcp-and-custom-integration-tools` | citation-only | live verification |
| `ai-mcp-and-custom-integration-tools-tool-contracts` | community-supported | live verification |
| `version-and-authority-caveats` | high | live verification |
| `troubleshooting-decision-tree-the-api-request-is-rejected-with-an-authorization-error` | normal | live verification |
| `troubleshooting-decision-tree-a-request-works-in-a-server-client-but-fails-in-a-browser` | normal | live verification |
| `troubleshooting-decision-tree-a-v2-update-cleared-or-changed-fields-the-integration-did-not-own` | normal | live verification |
| `troubleshooting-decision-tree-a-relationship-write-created-unexpected-related-records` | community-supported | live verification |
| `troubleshooting-decision-tree-a-create-request-succeeds-but-no-new-identifier-is-returned` | community-supported | live verification |
| `troubleshooting-decision-tree-a-lava-webhook-is-reachable-more-broadly-than-expected` | citation-only | live verification |
| `troubleshooting-decision-tree-a-helix-endpoint-behaves-differently-from-its-front-end` | normal | live verification |
| `troubleshooting-decision-tree-provider-events-arrive-but-staff-cannot-interpret-delivery-health` | normal | live verification |
| `troubleshooting-decision-tree-an-ai-tool-can-access-more-data-or-actions-than-expected` | citation-only | live verification |
| `agent-task-recipes-recipe-preflight-a-rest-integration` | normal | live verification |
| `agent-task-recipes-recipe-configure-and-review-a-rest-key` | normal | live verification |
| `agent-task-recipes-recipe-perform-a-bounded-api-v2-partial-update` | normal | live verification |
| `agent-task-recipes-recipe-review-a-lava-webhook-before-production` | normal | live verification |
| `agent-task-recipes-recipe-review-a-helix-application-flow` | normal | live verification |
| `agent-task-recipes-recipe-build-a-provider-event-health-report` | community-supported | live verification |
| `agent-task-recipes-recipe-approve-an-ai-or-mcp-tool-boundary` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-official-documentation-and-release-evidence` | high | live verification |
| `source-map-approved-claim-sources` | needs-citation | live verification |
| `source-map-community-patterns-and-examples` | community-supported | community-supported |
