---
concept_id: mobile
title: Rock Mobile Quickstart
generated: true
---

# Rock Mobile Quickstart

Mobile shell, XAML, commands, blocks, controls, app configuration, and mobile release caveats.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Create and test a minimal mobile application](tasks/recipe-create-and-test-a-minimal-mobile-application.md): A deployed application opens in the Rock Mobile Core test shell.
- [Recipe: Build personalized Content block output safely](tasks/recipe-build-personalized-content-block-output-safely.md): A mobile page displays current, identity-aware or entity-aware content without malformed XAML.
- [Recipe: Add a command-driven interaction](tasks/recipe-add-a-command-driven-interaction.md): A control executes a supported command with a validated parameter.
- [Recipe: Migrate a page from Shell v5 to v6+](tasks/recipe-migrate-a-page-from-shell-v5-to-v6.md): The page renders correctly on .NET MAUI without silently breaking retained older clients.
- [Recipe: Prepare mobile check-in](tasks/recipe-prepare-mobile-check-in.md): A participant can identify, select, complete check-in and hand labels to a kiosk.
- [Recipe: Prepare an App Factory publication](tasks/recipe-prepare-an-app-factory-publication.md): The publishing provider has a reviewable, secure and complete submission package.
- [Recipe: Validate push notifications](tasks/recipe-validate-push-notifications.md): A real target device receives and opens a notification through the intended route.
- [Recipe: Orchestrate slow media or content work](tasks/recipe-orchestrate-slow-media-or-content-work.md): Slow processing completes asynchronously and only verified output reaches public mobile content.
- [Recipe: Validate Outreach Toolbox for ministry use](tasks/recipe-validate-outreach-toolbox-for-ministry-use.md): Authorized signed-in users can see and complete intended outreach actions, and reminders arrive.

## High-Signal Sections

- `agent-summary` lines 18-32: Agent Summary (normal)
- `mental-model-shell-application-and-core-are-separate-compatibility-surfaces` lines 54-68: Shell, application and core are separate compatibility surfaces (normal)
- `mental-model-deploying-is-not-publishing` lines 69-74: Deploying is not publishing (normal)
- `mental-model-dynamic-content-crosses-a-trust-and-context-boundary` lines 79-89: Dynamic content crosses a trust and context boundary (normal)
- `application-configuration-and-deployment` lines 90-113: Application Configuration And Deployment (normal)
- `content-xaml-and-lava` lines 114-117: Content, XAML And Lava (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the mobile guide.
- `Block`: Rock concept/entity referenced by the mobile guide.
- `Campus`: Rock concept/entity referenced by the mobile guide.
- `Check-in Configuration`: Rock concept/entity referenced by the mobile guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the mobile guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the mobile guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the mobile guide.
- `Person`: Rock concept/entity referenced by the mobile guide.

## Version Caveats

- `19.1`: Fixed external links silently failing on Android when the address belonged to a site that also has an installed app handler (for example, opening a YouTube link on a device with the YouTube app installed). The link now f
- `19.1`: Fixed Android media playback so audio from other apps now lowers in volume when Rock Mobile starts playing audio.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
