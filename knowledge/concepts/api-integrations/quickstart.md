---
concept_id: api-integrations
title: API And Integrations Quickstart
generated: true
---

# API And Integrations Quickstart

REST APIs, API v1/v2, OData, webhooks, external integrations, and GitHub/source-code landmarks.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Preflight A REST Integration](tasks/recipe-preflight-a-rest-integration.md): A documented, least-privilege integration contract ready for safe testing.
- [Recipe: Configure And Review A REST Key](tasks/recipe-configure-and-review-a-rest-key.md): An active external credential with a named owner, bounded permissions, and a revocation plan.
- [Recipe: Perform A Bounded API v2 Partial Update](tasks/recipe-perform-a-bounded-api-v2-partial-update.md): Only the integration-owned fields are changed and independently verified.
- [Recipe: Review A Lava Webhook Before Production](tasks/recipe-review-a-lava-webhook-before-production.md): A bounded webhook with an explicit security and input contract.
- [Recipe: Review A Helix Application Flow](tasks/recipe-review-a-helix-application-flow.md): The exact endpoint work units, permissions, methods, and performance risks are understood before modification.
- [Recipe: Build A Provider Event Health Report](tasks/recipe-build-a-provider-event-health-report.md): Staff can understand delivery health in Rock context without seeing unnecessary raw provider data.
- [Recipe: Approve An AI Or MCP Tool Boundary](tasks/recipe-approve-an-ai-or-mcp-tool-boundary.md): A tool exposes one managed Rock capability with bounded inputs, results, and authorization.

## High-Signal Sections

- `agent-summary` lines 18-31: Agent Summary (normal)
- `rest-api` lines 67-70: REST API (normal)
- `rest-api-api-v1` lines 71-82: API v1 (normal)
- `rest-api-api-v2` lines 83-104: API v2 (normal)
- `rest-api-odata-and-response-shaping` lines 105-110: OData And Response Shaping (normal)
- `rest-api-partial-and-relationship-writes` lines 111-118: Partial And Relationship Writes (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the api-integrations guide.
- `Block`: Rock concept/entity referenced by the api-integrations guide.
- `DataView`: Rock concept/entity referenced by the api-integrations guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the api-integrations guide.
- `Label`: Rock concept/entity referenced by the api-integrations guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the api-integrations guide.
- `Person`: Rock concept/entity referenced by the api-integrations guide.
- `Workflow`: Rock concept/entity referenced by the api-integrations guide.

## Version Caveats

- `18.1`: Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #
- `16.1`: Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
