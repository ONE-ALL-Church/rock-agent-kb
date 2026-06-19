---
concept_id: cms-websites
title: CMS And Websites Quickstart
generated: true
---

# CMS And Websites Quickstart

Pages, blocks, themes, content channels, personalization, media, and website operations.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: “Find The Block That Controls This Text”](tasks/recipe-find-the-block-that-controls-this-text.md): Follow the guide section for Recipe: “Find The Block That Controls This Text”.
- [Recipe: “Why Is This Content Item Not Public?”](tasks/recipe-why-is-this-content-item-not-public.md): Follow the guide section for Recipe: “Why Is This Content Item Not Public?”.
- [Recipe: “Can I Enable SQL In This HTML Block?”](tasks/recipe-can-i-enable-sql-in-this-html-block.md): Follow the guide section for Recipe: “Can I Enable SQL In This HTML Block?”.
- [Recipe: “Add A Detail Page For Channel Items”](tasks/recipe-add-a-detail-page-for-channel-items.md): Follow the guide section for Recipe: “Add A Detail Page For Channel Items”.
- [Recipe: “Review A Community Recipe Before Installing”](tasks/recipe-review-a-community-recipe-before-installing.md): Follow the guide section for Recipe: “Review A Community Recipe Before Installing”.
- [Recipe: “Build A Page View Report”](tasks/recipe-build-a-page-view-report.md): Follow the guide section for Recipe: “Build A Page View Report”.
- [Recipe: “Troubleshoot Required Watching”](tasks/recipe-troubleshoot-required-watching.md): Follow the guide section for Recipe: “Troubleshoot Required Watching”.

## High-Signal Sections

- `2-scope-and-terminology` lines 60-124: 2. Scope And Terminology (normal)
- `3-cms-and-websites-mental-model` lines 125-144: 3. CMS And Websites Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 145-169: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model-blocks` lines 202-219: Blocks (normal)
- `5-core-configuration-and-data-model-themes` lines 230-245: Themes (normal)
- `5-core-configuration-and-data-model-content-channel-types` lines 246-258: Content Channel Types (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the cms-websites guide.
- `Block`: Rock concept/entity referenced by the cms-websites guide.
- `Campus`: Rock concept/entity referenced by the cms-websites guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the cms-websites guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the cms-websites guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the cms-websites guide.
- `Person`: Rock concept/entity referenced by the cms-websites guide.
- `Workflow`: Rock concept/entity referenced by the cms-websites guide.

## Version Caveats

- `17.1`: Fixed an issue in the Content Channel Item View block where breadcrumbs did not function correctly when accessing the page directly via a link rather than navigating through the site. This caused a 'Page Not Found' error
- `16.1`: Fixed issue where editing the block settings on a Dynamic Data block would update the page name of the internal page editor page. Fixes: #5542

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
