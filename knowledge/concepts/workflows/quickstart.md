---
concept_id: workflows
title: Workflows Quickstart
generated: true
---

# Workflows Quickstart

Workflow types, actions, triggers, forms, automation, jobs, and operational process design.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Find Every Launch Path For A Workflow Type](tasks/recipe-find-every-launch-path-for-a-workflow-type.md): Follow the guide section for Recipe: Find Every Launch Path For A Workflow Type.
- [Recipe: Explain A Workflow To A Staff Owner](tasks/recipe-explain-a-workflow-to-a-staff-owner.md): Follow the guide section for Recipe: Explain A Workflow To A Staff Owner.
- [Recipe: Diagnose A Missing Submission](tasks/recipe-diagnose-a-missing-submission.md): Follow the guide section for Recipe: Diagnose A Missing Submission.
- [Recipe: Safely Retire A Workflow](tasks/recipe-safely-retire-a-workflow.md): Follow the guide section for Recipe: Safely Retire A Workflow.
- [Recipe: Build A Workflow Health Dashboard](tasks/recipe-build-a-workflow-health-dashboard.md): Follow the guide section for Recipe: Build A Workflow Health Dashboard.
- [Recipe: Validate Person Entry Configuration](tasks/recipe-validate-person-entry-configuration.md): Follow the guide section for Recipe: Validate Person Entry Configuration.
- [Recipe: Audit `workflowactivate` Lava](tasks/recipe-audit-workflowactivate-lava.md): Follow the guide section for Recipe: Audit `workflowactivate` Lava.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-48: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 49-95: 2. Scope And Terminology (high)
- `3-workflows-mental-model` lines 96-147: 3. Workflows Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 148-173: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-workflow-type-configuration` lines 176-196: Workflow Type Configuration (normal)
- `5-core-configuration-and-data-model-activities-and-actions` lines 225-239: Activities And Actions (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the workflows guide.
- `Block`: Rock concept/entity referenced by the workflows guide.
- `Campus`: Rock concept/entity referenced by the workflows guide.
- `Family`: Rock concept/entity referenced by the workflows guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the workflows guide.
- `Label`: Rock concept/entity referenced by the workflows guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the workflows guide.
- `Person`: Rock concept/entity referenced by the workflows guide.
- `PersonAlias`: Rock concept/entity referenced by the workflows guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
