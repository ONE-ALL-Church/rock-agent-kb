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

- [Recipe: Audit a content channel before editing](tasks/recipe-audit-a-content-channel-before-editing.md): Follow the guide section for Recipe: Audit a content channel before editing.
- [Recipe: Diagnose “editor cannot see channel in Tools > Content”](tasks/recipe-diagnose-editor-cannot-see-channel-in-tools-content.md): Follow the guide section for Recipe: Diagnose “editor cannot see channel in Tools > Content”.
- [Recipe: Diagnose “segment should include this person”](tasks/recipe-diagnose-segment-should-include-this-person.md): Follow the guide section for Recipe: Diagnose “segment should include this person”.
- [Recipe: Create safe Lava for channel display](tasks/recipe-create-safe-lava-for-channel-display.md): Follow the guide section for Recipe: Create safe Lava for channel display.
- [Recipe: Verify content interactions](tasks/recipe-verify-content-interactions.md): Follow the guide section for Recipe: Verify content interactions.
- [Recipe: Public launch review for content personalization](tasks/recipe-public-launch-review-for-content-personalization.md): Follow the guide section for Recipe: Public launch review for content personalization.

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
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the content-personalization guide.
- `Person`: Rock concept/entity referenced by the content-personalization guide.
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
