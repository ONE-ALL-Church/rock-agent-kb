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

- [Recipe: Find The Right API Route](tasks/recipe-find-the-right-api-route.md): Complete Find The Right API Route with evidence-backed checks and a verifiable outcome.
- [Recipe: Audit A REST Key](tasks/recipe-audit-a-rest-key.md): Complete Audit A REST Key with evidence-backed checks and a verifiable outcome.
- [Recipe: Diagnose External Website API Failure](tasks/recipe-diagnose-external-website-api-failure.md): Complete Diagnose External Website API Failure with evidence-backed checks and a verifiable outcome.
- [Recipe: Review A Lava Webhook Before Launch](tasks/recipe-review-a-lava-webhook-before-launch.md): Complete Review A Lava Webhook Before Launch with evidence-backed checks and a verifiable outcome.
- [Recipe: Build A Safe Agent Tool](tasks/recipe-build-a-safe-agent-tool.md): See Writing Custom Tools, Get Tools, and List Tools.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-63: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 64-71: 2. Scope And Terminology (normal)
- `2-scope-and-terminology-api` lines 72-85: API (normal)
- `2-scope-and-terminology-rest-api-v1` lines 86-91: REST API v1 (normal)
- `2-scope-and-terminology-rest-api-v2` lines 92-97: REST API v2 (normal)
- `2-scope-and-terminology-odata` lines 98-101: OData (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the api-integrations guide.
- `Block`: Rock concept/entity referenced by the api-integrations guide.
- `DataView`: Rock concept/entity referenced by the api-integrations guide.
- `Family`: Rock concept/entity referenced by the api-integrations guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the api-integrations guide.
- `Person`: Rock concept/entity referenced by the api-integrations guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the api-integrations guide.

## Version Caveats

- `18.1`: Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #
- `16.1`: Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694
- `15.5`: Improved the Mailgun integration to use the API Key for tracking opens, etc. if the HTTP Webhook Signing Key is not defined, as well as logging a single exception to alert Rock admins of this missing key value. Fixes: #5
- `15.4`: Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694
- `18.2`: Fixed an error that prevented the Workflows Action Launch API endpoint from functioning. Fixes: #6604
- `17.5`: Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted expl

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
