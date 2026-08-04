---
concept_id: tv-apps
title: TV Apps Quickstart
generated: true
---

# TV Apps Quickstart

Apple TV and Roku developer documentation for Rock-powered TV applications, pages, commands, controls, styling, media, authentication, and app operations.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Audit A TV App Configuration](tasks/recipe-audit-a-tv-app-configuration.md): Complete Audit A TV App Configuration with evidence-backed checks and a verifiable outcome.
- [Recipe: Trace A Page GUID](tasks/recipe-trace-a-page-guid.md): Complete Trace A Page GUID with evidence-backed checks and a verifiable outcome.
- [Recipe: Validate Remote Auth In Data](tasks/recipe-validate-remote-auth-in-data.md): Complete Validate Remote Auth In Data with evidence-backed checks and a verifiable outcome.
- [Recipe: Review A Roku Page For Focus](tasks/recipe-review-a-roku-page-for-focus.md): Complete Review A Roku Page For Focus with evidence-backed checks and a verifiable outcome.
- [Recipe: Review Apple TV Markup](tasks/recipe-review-apple-tv-markup.md): Sources: Apple TV Tips, Apple TV Templates.
- [Recipe: Decide Cache Policy](tasks/recipe-decide-cache-policy.md): Verify actual headers and CDN behavior in the live environment.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-51: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 52-66: 2. Scope And Terminology (normal)
- `3-tv-apps-mental-model` lines 67-94: 3. TV Apps Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 95-118: 4. Source Authority And How To Use This Guide (normal)
- `5-core-configuration-and-data-model-apple-tv-application-configuration` lines 121-134: Apple TV Application Configuration (normal)
- `5-core-configuration-and-data-model-roku-application-configuration` lines 135-145: Roku Application Configuration (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the tv-apps guide.
- `Block`: Rock concept/entity referenced by the tv-apps guide.
- `Campus`: Rock concept/entity referenced by the tv-apps guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the tv-apps guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the tv-apps guide.
- `Page`: Rock concept/entity referenced by the tv-apps guide.
- `Person`: Rock concept/entity referenced by the tv-apps guide.
- `PersonAlias`: Rock concept/entity referenced by the tv-apps guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
