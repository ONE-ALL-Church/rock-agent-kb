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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inventory A Mobile App](tasks/recipe-inventory-a-mobile-app.md): Follow the guide section for Recipe: Inventory A Mobile App.
- [Recipe: Determine Whether A Feature Can Be Used](tasks/recipe-determine-whether-a-feature-can-be-used.md): Follow the guide section for Recipe: Determine Whether A Feature Can Be Used.
- [Recipe: Add Analytics To A Tap](tasks/recipe-add-analytics-to-a-tap.md): Follow the guide section for Recipe: Add Analytics To A Tap.
- [Recipe: Modernize Legacy Platform XAML](tasks/recipe-modernize-legacy-platform-xaml.md): Follow the guide section for Recipe: Modernize Legacy Platform XAML.
- [Recipe: Review App Store Readiness](tasks/recipe-review-app-store-readiness.md): Follow the guide section for Recipe: Review App Store Readiness.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-54: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 55-95: 2. Scope And Terminology (normal)
- `3-rock-mobile-mental-model-rock-core-configuration` lines 100-122: Rock Core Configuration (normal)
- `3-rock-mobile-mental-model-native-shell-runtime` lines 123-133: Native Shell Runtime (normal)
- `3-rock-mobile-mental-model-device-and-platform-environment` lines 134-139: Device And Platform Environment (normal)
- `3-rock-mobile-mental-model-deployment-flow` lines 140-152: Deployment Flow (normal)

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
