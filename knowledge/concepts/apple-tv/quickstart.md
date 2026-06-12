---
concept_id: apple-tv
title: Apple TV Apps Quickstart
generated: true
---

# Apple TV Apps Quickstart

Apple TV developer documentation for Rock-powered TVML applications, pages, content, sign-in, media commands, styling, themes, images, templates, testing, and operational guardrails.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inspect An Existing Apple TV App](tasks/recipe-inspect-an-existing-apple-tv-app.md): Follow the guide section for Recipe: Inspect An Existing Apple TV App.
- [Recipe: Diagnose A Broken Button](tasks/recipe-diagnose-a-broken-button.md): Follow the guide section for Recipe: Diagnose A Broken Button.
- [Recipe: Add A New Page Safely](tasks/recipe-add-a-new-page-safely.md): Follow the guide section for Recipe: Add A New Page Safely.
- [Recipe: Review For Security](tasks/recipe-review-for-security.md): Follow the guide section for Recipe: Review For Security.
- [Recipe: Review For Performance](tasks/recipe-review-for-performance.md): Follow the guide section for Recipe: Review For Performance.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-48: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 49-86: 2. Scope And Terminology (normal)
- `3-apple-tv-apps-mental-model` lines 87-128: 3. Apple TV Apps Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 129-152: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model-apple-tv-app-record` lines 155-184: Apple TV App Record (normal)
- `5-core-configuration-and-data-model-tv-page-record` lines 185-193: TV Page Record (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the apple-tv guide.
- `Block`: Rock concept/entity referenced by the apple-tv guide.
- `Campus`: Rock concept/entity referenced by the apple-tv guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the apple-tv guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the apple-tv guide.
- `Person`: Rock concept/entity referenced by the apple-tv guide.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the apple-tv guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
