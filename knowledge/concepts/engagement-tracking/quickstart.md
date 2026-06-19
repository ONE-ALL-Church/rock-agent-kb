---
concept_id: engagement-tracking
title: Engagement Tracking Quickstart
generated: true
---

# Engagement Tracking Quickstart

Steps, step programs, streaks, assessments, achievements, engagement tools, journey-style tracking, completion signals, and related reporting.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Audit A Step Program](tasks/recipe-audit-a-step-program.md): Follow the guide section for Recipe: Audit A Step Program.
- [Recipe: Diagnose Step Badge Display](tasks/recipe-diagnose-step-badge-display.md): Follow the guide section for Recipe: Diagnose Step Badge Display.
- [Recipe: Review A Streak Type Before Rebuild](tasks/recipe-review-a-streak-type-before-rebuild.md): Follow the guide section for Recipe: Review A Streak Type Before Rebuild.
- [Recipe: Verify Assessment Request Flow](tasks/recipe-verify-assessment-request-flow.md): Follow the guide section for Recipe: Verify Assessment Request Flow.
- [Recipe: Audit Achievement Type](tasks/recipe-audit-achievement-type.md): Follow the guide section for Recipe: Audit Achievement Type.
- [Recipe: Explain Engagement Data To A Ministry User](tasks/recipe-explain-engagement-data-to-a-ministry-user.md): Follow the guide section for Recipe: Explain Engagement Data To A Ministry User.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-42: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 43-92: 2. Scope And Terminology (high)
- `3-engagement-tracking-mental-model` lines 93-114: 3. Engagement Tracking Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 115-133: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-steps-configuration` lines 136-181: Steps Configuration (high)
- `5-core-configuration-and-data-model-step-status-and-completion` lines 182-187: Step Status And Completion (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the engagement-tracking guide.
- `Block`: Rock concept/entity referenced by the engagement-tracking guide.
- `Campus`: Rock concept/entity referenced by the engagement-tracking guide.
- `Family`: Rock concept/entity referenced by the engagement-tracking guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the engagement-tracking guide.
- `LearningClassActivityCompletion`: Person-specific activity completion signal used by LMS reporting, workflow triggers, and downstream engagement steps.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the engagement-tracking guide.
- `Person`: Rock concept/entity referenced by the engagement-tracking guide.
- `PersonAlias`: Rock concept/entity referenced by the engagement-tracking guide.

## Version Caveats

- `18.1`: Added new "Core Steps" Step Program with system-protected Step Types, including initial "eRA" type. Added the ability to transfer Step Types from one Step Program to another.
- `18.3`: Fixed an issue where editing a Step Program removed the Step Type association from its workflow triggers, and also addressed Step Type-level triggers being incorrectly displayed on the Step Program Detail. Fixes: #6753

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
