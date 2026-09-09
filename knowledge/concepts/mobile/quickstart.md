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

- `agent-summary` lines 34-48: Agent Summary (normal)
- `mental-model-shell-application-and-core-are-separate-compatibility-surfaces` lines 70-84: Shell, application and core are separate compatibility surfaces (normal)
- `mental-model-deploying-is-not-publishing` lines 85-90: Deploying is not publishing (normal)
- `mental-model-dynamic-content-crosses-a-trust-and-context-boundary` lines 95-105: Dynamic content crosses a trust and context boundary (normal)
- `application-configuration-and-deployment` lines 106-129: Application Configuration And Deployment (normal)
- `content-xaml-and-lava` lines 130-133: Content, XAML And Lava (normal)

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

- `7.0`: Fixed an issue where the ShowPopUp command displayed the popup on a white screen instead of overlaying the triggering page when running in MAUI. Fixes: #38
- `7.0`: Added the ExecuteCommand control, enabling command execution with configurable timing and repetition.
- `4.0`: Added a custom ScrollView control that allows you to disable the native iOS bounce when scrolling.
- `2.1`: Fixed bug that prevented Flyout Shell from working properly if ListItem was not the root XAML element.
- `2.0`: Fixed bug in iOS that prevented a person from choosing the "Save..." option during a ShareFile command.
- `6.0`: Updated all of the mobile blocks to follow the new design system.
- `7.0`: Added the CopyToClipboard command, allowing text to be copied to the clipboard.
- `7.0`: Fixed an issue that caused the AddEventToCalendar command to not function properly.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
