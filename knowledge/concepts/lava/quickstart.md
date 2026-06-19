---
concept_id: lava
title: Lava Quickstart
generated: true
---

# Lava Quickstart

Lava syntax, filters, commands, shortcodes, remote Lava, and safe operational use.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inventory Lava Risk On A Page](tasks/recipe-inventory-lava-risk-on-a-page.md): Follow the guide section for Recipe: Inventory Lava Risk On A Page.
- [Recipe: Review A Shortcode For Production](tasks/recipe-review-a-shortcode-for-production.md): Follow the guide section for Recipe: Review A Shortcode For Production.
- [Recipe: Find Legacy Attribute Lava](tasks/recipe-find-legacy-attribute-lava.md): Follow the guide section for Recipe: Find Legacy Attribute Lava.
- [Recipe: Safely Use `securityenabled:'false'`](tasks/recipe-safely-use-securityenabled-false.md): Follow the guide section for Recipe: Safely Use `securityenabled:'false'`.
- [Recipe: Create A Staff-Friendly Link Copy Shortcode](tasks/recipe-create-a-staff-friendly-link-copy-shortcode.md): Follow the guide section for Recipe: Create A Staff-Friendly Link Copy Shortcode.
- [Recipe: Add A Translation Shortcode](tasks/recipe-add-a-translation-shortcode.md): Follow the guide section for Recipe: Add A Translation Shortcode.
- [Recipe: Generate Labels With Lava](tasks/recipe-generate-labels-with-lava.md): Follow the guide section for Recipe: Generate Labels With Lava.
- [Recipe: Build An Agent Lava Tool](tasks/recipe-build-an-agent-lava-tool.md): Follow the guide section for Recipe: Build An Agent Lava Tool.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-53: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 54-98: 2. Scope And Terminology (normal)
- `3-lava-mental-model` lines 99-140: 3. Lava Mental Model (normal)
- `5-core-configuration-and-data-model-lava-engine-liquid-framework` lines 170-188: Lava Engine Liquid Framework (normal)
- `5-core-configuration-and-data-model-default-enabled-lava-commands` lines 189-200: Default Enabled Lava Commands (normal)
- `5-core-configuration-and-data-model-html-block-command-enablement` lines 201-211: HTML Block Command Enablement (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the lava guide.
- `Block`: Rock concept/entity referenced by the lava guide.
- `Campus`: Rock concept/entity referenced by the lava guide.
- `DataView`: Rock concept/entity referenced by the lava guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the lava guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the lava guide.
- `Person`: Rock concept/entity referenced by the lava guide.
- `Workflow`: Rock concept/entity referenced by the lava guide.

## Version Caveats

- `19.1`: Added a new Shortcode Scope Behavior property to the Lava Shortcode Entity. This setting allows Rock administrators to choose whether variables defined inside a shortcode should be isolated from or shared with the surrou

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
