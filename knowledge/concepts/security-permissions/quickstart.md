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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Answer “Who Has Access To This?”](tasks/recipe-answer-who-has-access-to-this.md): Follow the guide section for Recipe: Answer “Who Has Access To This?”.
- [Recipe: Answer “Why Was I Denied?”](tasks/recipe-answer-why-was-i-denied.md): Follow the guide section for Recipe: Answer “Why Was I Denied?”.
- [Recipe: Review A Permission Change Request](tasks/recipe-review-a-permission-change-request.md): Follow the guide section for Recipe: Review A Permission Change Request.
- [Recipe: Review A Custom Agent Tool](tasks/recipe-review-a-custom-agent-tool.md): Follow the guide section for Recipe: Review A Custom Agent Tool.
- [Recipe: Review A Public Route](tasks/recipe-review-a-public-route.md): Follow the guide section for Recipe: Review A Public Route.
- [Recipe: Review A Security Role](tasks/recipe-review-a-security-role.md): Follow the guide section for Recipe: Review A Security Role.
- [Recipe: Review After Upgrade](tasks/recipe-review-after-upgrade.md): Follow the guide section for Recipe: Review After Upgrade.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-55: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology-key-terms` lines 88-119: Key Terms (normal)
- `3-security-and-permissions-mental-model-the-actor-layer` lines 126-143: The Actor Layer (normal)
- `3-security-and-permissions-mental-model-the-object-layer` lines 144-159: The Object Layer (normal)
- `3-security-and-permissions-mental-model-the-action-layer` lines 160-165: The Action Layer (normal)
- `3-security-and-permissions-mental-model-the-code-layer` lines 198-212: The Code Layer (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the security-permissions guide.
- `Block`: Rock concept/entity referenced by the security-permissions guide.
- `Check-in Configuration`: Rock concept/entity referenced by the security-permissions guide.
- `DataView`: Rock concept/entity referenced by the security-permissions guide.
- `Family`: Rock concept/entity referenced by the security-permissions guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the security-permissions guide.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the security-permissions guide.
- `Page`: Rock concept/entity referenced by the security-permissions guide.
- `Person`: Rock concept/entity referenced by the security-permissions guide.

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
