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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Answer "Where is this configured?"](tasks/recipe-answer-where-is-this-configured.md): Follow the guide section for Recipe: Answer "Where is this configured?".
- [Recipe: Review a Rock PR](tasks/recipe-review-a-rock-pr.md): Follow the guide section for Recipe: Review a Rock PR.
- [Recipe: Diagnose "Works for admin but not staff"](tasks/recipe-diagnose-works-for-admin-but-not-staff.md): Follow the guide section for Recipe: Diagnose "Works for admin but not staff".
- [Recipe: Build a source-backed answer](tasks/recipe-build-a-source-backed-answer.md): Follow the guide section for Recipe: Build a source-backed answer.
- [Recipe: Build a Rock agent tool](tasks/recipe-build-a-rock-agent-tool.md): Follow the guide section for Recipe: Build a Rock agent tool.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-47: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 48-71: 2. Scope And Terminology (normal)
- `3-rock-developer-resources-mental-model-layer-1-platform-and-runtime` lines 76-88: Layer 1: Platform and runtime (normal)
- `3-rock-developer-resources-mental-model-layer-2-ui-technology-choice` lines 89-102: Layer 2: UI technology choice (normal)
- `3-rock-developer-resources-mental-model-layer-3-data-model-and-persistence` lines 103-115: Layer 3: Data model and persistence (normal)
- `3-rock-developer-resources-mental-model-layer-4-security-and-operational-guardrails` lines 116-129: Layer 4: Security and operational guardrails (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the developer-resources guide.
- `Block`: Rock concept/entity referenced by the developer-resources guide.
- `DefinedType`: Rock concept/entity referenced by the developer-resources guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the developer-resources guide.
- `Page`: Rock concept/entity referenced by the developer-resources guide.
- `Person`: Rock concept/entity referenced by the developer-resources guide.
- `PersonAlias`: Rock concept/entity referenced by the developer-resources guide.
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
