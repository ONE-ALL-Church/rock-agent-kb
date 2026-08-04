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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inspect An Existing Apple TV App](tasks/recipe-inspect-an-existing-apple-tv-app.md): Complete Inspect An Existing Apple TV App with evidence-backed checks and a verifiable outcome.
- [Recipe: Diagnose A Broken Button](tasks/recipe-diagnose-a-broken-button.md): Complete Diagnose A Broken Button with evidence-backed checks and a verifiable outcome.
- [Recipe: Add A New Page Safely](tasks/recipe-add-a-new-page-safely.md): Complete Add A New Page Safely with evidence-backed checks and a verifiable outcome.
- [Recipe: Review For Security](tasks/recipe-review-for-security.md): Complete Review For Security with evidence-backed checks and a verifiable outcome.
- [Recipe: Review For Performance](tasks/recipe-review-for-performance.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-50: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 51-88: 2. Scope And Terminology (normal)
- `3-apple-tv-apps-mental-model` lines 89-130: 3. Apple TV Apps Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 131-154: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model-apple-tv-app-record` lines 157-186: Apple TV App Record (normal)
- `5-core-configuration-and-data-model-tv-page-record` lines 187-195: TV Page Record (normal)

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
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
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
