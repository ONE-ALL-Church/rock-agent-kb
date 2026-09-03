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

- [Recipe: Create an Apple TV application skeleton](tasks/recipe-create-an-apple-tv-application-skeleton.md): A Rock-managed Apple TV application with a valid Start Screen and explicitly reviewed application settings.
- [Recipe: Build a Roku content page](tasks/recipe-build-a-roku-content-page.md): A Roku page whose rendered SceneGraph loads with deterministic initial focus.
- [Recipe: Add Roku navigation with application context](tasks/recipe-add-roku-navigation-with-application-context.md): Selecting one control sets a context value and opens a destination page that reads it.
- [Recipe: Configure remote TV sign-in](tasks/recipe-configure-remote-tv-sign-in.md): A person can authenticate on a website and the TV client transitions to the configured success page.
- [Recipe: Add tracked media playback with resume](tasks/recipe-add-tracked-media-playback-with-resume.md): A supported media resource plays and resumes according to an explicitly selected interaction strategy.
- [Recipe: Make an Apple TV page theme-aware](tasks/recipe-make-an-apple-tv-page-theme-aware.md): One TVML page remains legible in both Light and Dark themes.

## High-Signal Sections

- `agent-summary` lines 18-32: Agent Summary (normal)
- `scope-and-boundaries` lines 33-48: Scope And Boundaries (normal)
- `mental-model` lines 49-61: Mental Model (normal)
- `apple-tv-application-configuration` lines 64-80: Application configuration (normal)
- `apple-tv-pages-and-lava-output` lines 81-103: Pages and Lava output (normal)
- `apple-tv-commands` lines 104-109: Commands (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the tv-apps guide.
- `Block`: Rock concept/entity referenced by the tv-apps guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the tv-apps guide.
- `Page`: Rock concept/entity referenced by the tv-apps guide.
- `Person`: Rock concept/entity referenced by the tv-apps guide.
- `Workflow`: Rock concept/entity referenced by the tv-apps guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
