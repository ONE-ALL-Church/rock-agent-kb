---
concept_id: api-integrations
title: API And Integrations Open Questions
generated: true
---

# API And Integrations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (174 words)
- `mental-model`: Mental Model (195 words)
- `source-map-approved-claim-sources`: Approved Claim Sources (126 words)

## Community-Supported Only

- `lava-apis-and-webhooks-community-webhook-example`: Community Webhook Example
- `ai-mcp-and-custom-integration-tools-tool-contracts`: Tool Contracts
- `troubleshooting-decision-tree-a-relationship-write-created-unexpected-related-records`: A relationship write created unexpected related records
- `troubleshooting-decision-tree-a-create-request-succeeds-but-no-new-identifier-is-returned`: A create request succeeds but no new identifier is returned
- `agent-task-recipes-recipe-build-a-provider-event-health-report`: Recipe: Build A Provider Event Health Report
- `source-map-community-patterns-and-examples`: Community Patterns And Examples

## Needs Live Verification

- `scope-and-boundaries`: Scope And Boundaries
- `mental-model`: Mental Model
- `rest-api-api-v1`: API v1
- `rest-api-api-v2`: API v2
- `rest-api-partial-and-relationship-writes`: Partial And Relationship Writes
- `lava-apis-and-webhooks`: Lava APIs And Webhooks
- `helix-lava-endpoints`: Helix Lava Endpoints
- `helix-lava-endpoints-rendering-and-caching`: Rendering And Caching
- `helix-lava-endpoints-public-ui-integration-boundary`: Public UI Integration Boundary
- `provider-webhooks-and-operational-reporting`: Provider Webhooks And Operational Reporting
- `ai-mcp-and-custom-integration-tools`: AI, MCP, And Custom Integration Tools
- `ai-mcp-and-custom-integration-tools-tool-contracts`: Tool Contracts
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-the-api-request-is-rejected-with-an-authorization-error`: The API request is rejected with an authorization error
- `troubleshooting-decision-tree-a-request-works-in-a-server-client-but-fails-in-a-browser`: A request works in a server client but fails in a browser
- `troubleshooting-decision-tree-a-v2-update-cleared-or-changed-fields-the-integration-did-not-own`: A v2 update cleared or changed fields the integration did not own
- `troubleshooting-decision-tree-a-relationship-write-created-unexpected-related-records`: A relationship write created unexpected related records
- `troubleshooting-decision-tree-a-create-request-succeeds-but-no-new-identifier-is-returned`: A create request succeeds but no new identifier is returned
- `troubleshooting-decision-tree-a-lava-webhook-is-reachable-more-broadly-than-expected`: A Lava webhook is reachable more broadly than expected
- `troubleshooting-decision-tree-a-helix-endpoint-behaves-differently-from-its-front-end`: A Helix endpoint behaves differently from its front end
- `troubleshooting-decision-tree-provider-events-arrive-but-staff-cannot-interpret-delivery-health`: Provider events arrive but staff cannot interpret delivery health
- `troubleshooting-decision-tree-an-ai-tool-can-access-more-data-or-actions-than-expected`: An AI tool can access more data or actions than expected
- `agent-task-recipes-recipe-preflight-a-rest-integration`: Recipe: Preflight A REST Integration
- `agent-task-recipes-recipe-configure-and-review-a-rest-key`: Recipe: Configure And Review A REST Key
- `agent-task-recipes-recipe-perform-a-bounded-api-v2-partial-update`: Recipe: Perform A Bounded API v2 Partial Update
- `agent-task-recipes-recipe-review-a-lava-webhook-before-production`: Recipe: Review A Lava Webhook Before Production
- `agent-task-recipes-recipe-review-a-helix-application-flow`: Recipe: Review A Helix Application Flow
- `agent-task-recipes-recipe-build-a-provider-event-health-report`: Recipe: Build A Provider Event Health Report
- `agent-task-recipes-recipe-approve-an-ai-or-mcp-tool-boundary`: Recipe: Approve An AI Or MCP Tool Boundary
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `source-map-official-documentation-and-release-evidence`: Official Documentation And Release Evidence
- `source-map-approved-claim-sources`: Approved Claim Sources

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
