---
concept_id: security-permissions
title: Security And Permissions Quickstart
generated: true
---

# Security And Permissions Quickstart

Authorization, roles, security inheritance, API auth, block/page security, and operational guardrails.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Explain an effective permission result](tasks/recipe-explain-an-effective-permission-result.md): A sourced explanation of why one person is allowed or denied one action.
- [Recipe: Publish a page or block with bounded access](tasks/recipe-publish-a-page-or-block-with-bounded-access.md): The intended audience can use the surface while unauthorized users cannot.
- [Recipe: Preflight a least-privilege REST integration](tasks/recipe-preflight-a-least-privilege-rest-integration.md): A documented integration identity with only the access required for known routes and methods.
- [Recipe: Secure a Lava API or Helix endpoint](tasks/recipe-secure-a-lava-api-or-helix-endpoint.md): A directly callable endpoint with explicit identity, authorization, validation, and bounded output.
- [Recipe: Audit Person Profile notes](tasks/recipe-audit-person-profile-notes.md): Sensitive notes are categorized, visible, and consumed only as intended.
- [Recipe: Validate an AI agent tool before production](tasks/recipe-validate-an-ai-agent-tool-before-production.md): A bounded tool whose availability, authorization, input handling, and output have been demonstrated.
- [Recipe: Run a security-sensitive upgrade preflight](tasks/recipe-run-a-security-sensitive-upgrade-preflight.md): A version-aware plan that distinguishes security fixes from feature changes.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 18-34: 1. Executive Summary For Agents (normal)
- `scope-and-boundaries` lines 35-58: Scope And Boundaries (normal)
- `3-security-and-permissions-mental-model-the-object-layer` lines 65-68: The Object Layer (normal)
- `3-security-and-permissions-mental-model-the-action-layer` lines 69-84: The Action Layer (high)
- `authorization-and-security-roles` lines 85-92: Authorization And Security Roles (normal)
- `authorization-and-security-roles-permission-evaluation` lines 93-106: Permission evaluation (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the security-permissions guide.
- `Block`: Rock concept/entity referenced by the security-permissions guide.
- `Campus`: Rock concept/entity referenced by the security-permissions guide.
- `Check-in Configuration`: Rock concept/entity referenced by the security-permissions guide.
- `DataView`: Rock concept/entity referenced by the security-permissions guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the security-permissions guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the security-permissions guide.
- `Person`: Rock concept/entity referenced by the security-permissions guide.
- `Step`: Person-specific engagement milestone instance.

## Version Caveats

- `17.5`: Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted expl
- `17.8`: Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules w

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
