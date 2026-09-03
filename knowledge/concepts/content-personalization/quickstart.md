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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Publish a governed Content Channel Item](tasks/recipe-publish-a-governed-content-channel-item.md): An item is structurally complete, correctly scheduled, reviewable, and eligible for display.
- [Recipe: Add personalization to Content Channel Items](tasks/recipe-add-personalization-to-content-channel-items.md): Matching visitors receive the intended filtered or prioritized content without cross-visitor cache leakage.
- [Recipe: Refresh personalization membership](tasks/recipe-refresh-personalization-membership.md): A persisted segment and its browser-facing membership state reflect current person data.
- [Recipe: Build and refresh a Content Collection](tasks/recipe-build-and-refresh-a-content-collection.md): Multiple channels or calendars are searchable together with deliberate filtering, ranking, and security boundaries.
- [Recipe: Configure a Content Component template](tasks/recipe-configure-a-content-component-template.md): Editors can change structured content without editing presentation markup.
- [Recipe: Automate a channel item attribute with Lava](tasks/recipe-automate-a-channel-item-attribute-with-lava.md): A scheduled job safely writes evaluated Lava output into a compatible target attribute.
- [Recipe: Publish a Media Element through a channel](tasks/recipe-publish-a-media-element-through-a-channel.md): A media item appears through normal content tools with the intended player behavior and analytics.
- [Recipe: Share or refresh Content Library material](tasks/recipe-share-or-refresh-content-library-material.md): An item is uploaded or downloaded with its license and overwrite behavior understood.
- [Recipe: Configure localized currency display safely](tasks/recipe-configure-localized-currency-display-safely.md): Numeric values display the intended currency symbol without implying conversion or silently changing gateway behavior.

## High-Signal Sections

- `agent-summary` lines 18-40: Agent Summary (normal)
- `scope-and-boundaries` lines 41-56: Scope And Boundaries (normal)
- `mental-model` lines 57-82: Mental Model (normal)
- `content-channels-choose-the-structure` lines 85-92: Choose the structure (normal)
- `content-channels-configure-publication-behavior` lines 93-100: Configure publication behavior (normal)
- `content-channels-manage-editorial-work` lines 101-108: Manage editorial work (high)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the content-personalization guide.
- `Block`: Rock concept/entity referenced by the content-personalization guide.
- `DataView`: Rock concept/entity referenced by the content-personalization guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the content-personalization guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the content-personalization guide.
- `Person`: Rock concept/entity referenced by the content-personalization guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the content-personalization guide.

## Version Caveats

- `19.3`: Fixed the Content Channel Item List block to show the add and delete options for individuals with Edit access to the content channel, rather than requiring Edit access on the Content Channel Item entity itself. Fixes: #6
- `17.5`: Fixed an issue where the Content Channel Item View block and the InteractionContentChannelItemWrite Lava command logged interactions using the Content Channel entity type instead of the Content Channel Item entity type.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
