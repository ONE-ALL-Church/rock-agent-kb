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

- [Recipe: Create a minimal Rock Apple TV application](tasks/recipe-create-a-minimal-rock-apple-tv-application.md): A Rock-managed application with a valid Start Screen and documented baseline settings.
- [Recipe: Add a cache-aware TVML page](tasks/recipe-add-a-cache-aware-tvml-page.md): A new page that emits valid TVML and uses an intentional cache policy.
- [Recipe: Implement remote sign-in](tasks/recipe-implement-remote-sign-in.md): A viewer can authenticate from a phone or computer by scanning a QR code or entering a short code.
- [Recipe: Add tracked video or audio playback](tasks/recipe-add-tracked-video-or-audio-playback.md): A supported media file plays with intentional resume and interaction behavior.
- [Recipe: Build a theme-safe styling pass](tasks/recipe-build-a-theme-safe-styling-pass.md): Text, badges, images, and focus states remain legible in both Light and Dark themes.
- [Recipe: Prepare the application image package](tasks/recipe-prepare-the-application-image-package.md): A delivery set contains the documented icon, launch, Top Shelf, and optional parallax assets.
- [Recipe: Test through demo mode](tasks/recipe-test-through-demo-mode.md): The community shell loads the intended Rock application configuration for bounded testing.
- [Recipe: Review a Lava API before connecting it to Apple TV](tasks/recipe-review-a-lava-api-before-connecting-it-to-apple-tv.md): The agent can state what a Lava webhook exposes and whether its protection has been verified.

## High-Signal Sections

- `agent-summary` lines 18-37: Agent Summary (normal)
- `scope-and-boundaries` lines 38-59: Scope And Boundaries (normal)
- `mental-model` lines 60-73: Mental Model (normal)
- `creating-and-configuring-an-application` lines 74-91: Creating And Configuring An Application (normal)
- `pages-lava-and-cache-behavior-page-content-and-merge-fields` lines 94-114: Page content and merge fields (normal)
- `pages-lava-and-cache-behavior-creating-page-content` lines 115-120: Creating page content (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Block`: Rock concept/entity referenced by the apple-tv guide.
- `Campus`: Rock concept/entity referenced by the apple-tv guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the apple-tv guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the apple-tv guide.
- `Page`: Rock concept/entity referenced by the apple-tv guide.
- `Person`: Rock concept/entity referenced by the apple-tv guide.
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
