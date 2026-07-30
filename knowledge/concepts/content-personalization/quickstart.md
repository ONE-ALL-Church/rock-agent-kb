---
concept_id: content-personalization
title: Content And Personalization Quickstart
generated: true
---

# Content And Personalization Quickstart

Content channels, assets, structured content, adaptive messages, personalization, segments, website content operations, and publishing workflows.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Audit a content channel before editing](tasks/recipe-audit-a-content-channel-before-editing.md): Do not change anything until you know which pages and workflows depend on the channel.
- [Recipe: Diagnose “editor cannot see channel in Tools > Content”](tasks/recipe-diagnose-editor-cannot-see-channel-in-tools-content.md): The `Tools > Content` page lists channels the current user has View access to, according to official docs (Manage Content Items).
- [Recipe: Diagnose “segment should include this person”](tasks/recipe-diagnose-segment-should-include-this-person.md): Complete Diagnose “segment should include this person” with evidence-backed checks and a verifiable outcome.
- [Recipe: Verify content interactions](tasks/recipe-verify-content-interactions.md): Complete Verify content interactions with evidence-backed checks and a verifiable outcome.
- [Recipe: Public launch review for content personalization](tasks/recipe-public-launch-review-for-content-personalization.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-46: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 47-65: 2. Scope And Terminology (normal)
- `3-content-and-personalization-mental-model` lines 66-81: 3. Content And Personalization Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 82-96: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model` lines 97-134: 5. Core Configuration And Data Model (high)
- `6-primary-entities-and-relationships` lines 135-156: 6. Primary Entities And Relationships (high)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the content-personalization guide.
- `Block`: Rock concept/entity referenced by the content-personalization guide.
- `Campus`: Rock concept/entity referenced by the content-personalization guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the content-personalization guide.
- `Person`: Rock concept/entity referenced by the content-personalization guide.
- `PersonAlias`: Rock concept/entity referenced by the content-personalization guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the content-personalization guide.

## Version Caveats

- `17.5`: Fixed an issue where the Content Channel Item View block and the InteractionContentChannelItemWrite Lava command logged interactions using the Content Channel entity type instead of the Content Channel Item entity type.
- `18.2`: Fixed a security issue affecting multiple blocks that interact with Content Channels, where individuals with only View permissions could delete content items. The delete option is now correctly limited to those with Edit

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
