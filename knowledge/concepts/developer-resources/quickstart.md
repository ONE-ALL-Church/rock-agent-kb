---
concept_id: developer-resources
title: Rock Developer Resources Quickstart
generated: true
---

# Rock Developer Resources Quickstart

Rock developer documentation across tutorials, Developer Codex, Obsidian, Helix, mobile and TV shells, packaging, Slingshot migration, design-system, dynamic LINQ, release/changelog notes, and developer utilities.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Select the correct developer resource](tasks/recipe-select-the-correct-developer-resource.md): Route a request to the narrowest applicable Rock development surface.
- [Recipe: Review an Obsidian block change](tasks/recipe-review-an-obsidian-block-change.md): Identify and validate all layers affected by an Obsidian block change.
- [Recipe: Regenerate artifacts after a model change](tasks/recipe-regenerate-artifacts-after-a-model-change.md): Produce synchronized C# and Obsidian view models.
- [Recipe: Review a Helix endpoint before changing it](tasks/recipe-review-a-helix-endpoint-before-changing-it.md): Establish the endpoint’s current contract, security boundary, and runtime dependencies.
- [Recipe: Validate Rock Mobile compatibility](tasks/recipe-validate-rock-mobile-compatibility.md): Determine whether a feature is supported by the exact Core/Shell pair.
- [Recipe: Build or repair a Roku page](tasks/recipe-build-or-repair-a-roku-page.md): Produce a navigable, correctly cached Lava-driven SceneGraph page.
- [Recipe: Prepare a plugin or theme package](tasks/recipe-prepare-a-plugin-or-theme-package.md): Produce a reviewable extension package with understood install and uninstall behavior.
- [Recipe: Validate a Slingshot migration](tasks/recipe-validate-a-slingshot-migration.md): Demonstrate that imported data supports the intended Rock workflows.
- [Recipe: Inspect page content with a Rock AI agent](tasks/recipe-inspect-page-content-with-a-rock-ai-agent.md): Determine what blocks and settings contribute to a page, when the installed agent tools support it.
- [Recipe: Verify a save or Rock-managed file deployment](tasks/recipe-verify-a-save-or-rock-managed-file-deployment.md): Confirm that the intended state persisted at the exact target.

## High-Signal Sections

- `agent-summary` lines 18-30: Agent Summary (normal)
- `mental-model` lines 50-61: Mental Model (normal)
- `learning-path-quickstart-101-202-and-303` lines 62-74: Learning Path: Quickstart, 101, 202, And 303 (normal)
- `learning-path-quickstart-101-202-and-303-rest-authorization-in-303` lines 75-80: REST authorization in 303 (normal)
- `developer-codex-naming-and-compatibility` lines 85-90: Naming and compatibility (normal)
- `developer-codex-model-changes-and-generated-artifacts` lines 91-103: Model changes and generated artifacts (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the developer-resources guide.
- `Block`: Rock concept/entity referenced by the developer-resources guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the developer-resources guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Page`: Rock concept/entity referenced by the developer-resources guide.
- `Person`: Rock concept/entity referenced by the developer-resources guide.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the developer-resources guide.

## Version Caveats

- `18.2`: Fixed an issue that caused the wrong theme type to be displayed after cloning a theme until the Rock server rebooted. Fixes: #6603
- `17.1`: Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
