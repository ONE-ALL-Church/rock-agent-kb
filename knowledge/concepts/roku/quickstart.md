---
concept_id: roku
title: Roku Apps Quickstart
generated: true
---

# Roku Apps Quickstart

Roku developer documentation for Rock-powered SceneGraph applications, pages, commands, controls, focus handling, media playback, layout nodes, resources, and operational guardrails.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inventory Existing Roku App](tasks/recipe-inventory-existing-roku-app.md): Complete Inventory Existing Roku App with evidence-backed checks and a verifiable outcome.
- [Recipe: Review A Roku Page For Safety](tasks/recipe-review-a-roku-page-for-safety.md): Report findings by severity: security/cache leaks first, broken rendering second, analytics inaccuracies third, maintainability last.
- [Recipe: Convert A Static Media List To Dynamic RowList](tasks/recipe-convert-a-static-media-list-to-dynamic-rowlist.md): Complete Convert A Static Media List To Dynamic RowList with evidence-backed checks and a verifiable outcome.
- [Recipe: Diagnose A Cache Leak](tasks/recipe-diagnose-a-cache-leak.md): Complete Diagnose A Cache Leak with evidence-backed checks and a verifiable outcome.
- [Recipe: Add A Safe Diagnostic Page](tasks/recipe-add-a-safe-diagnostic-page.md): Do not show API keys, tokens, person IDs, email addresses, or sensitive attributes. Remove or lock down the page before production launch.
- [Recipe: Validate Post-Upgrade Roku Behavior](tasks/recipe-validate-post-upgrade-roku-behavior.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-50: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 51-74: 2. Scope And Terminology (normal)
- `3-roku-apps-mental-model` lines 75-92: 3. Roku Apps Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 93-118: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model-application-configuration` lines 123-136: Application Configuration (normal)
- `5-core-configuration-and-data-model-page-configuration` lines 137-148: Page Configuration (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the roku guide.
- `Block`: Rock concept/entity referenced by the roku guide.
- `Campus`: Rock concept/entity referenced by the roku guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the roku guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the roku guide.
- `Person`: Rock concept/entity referenced by the roku guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the roku guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
