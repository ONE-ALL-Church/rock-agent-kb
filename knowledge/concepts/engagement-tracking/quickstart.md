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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Configure a Step journey with reliable completion signals](tasks/recipe-configure-a-step-journey-with-reliable-completion-signals.md): A Step Program whose order, prerequisites and completion semantics match the intended journey.
- [Recipe: Bulk-record a Step](tasks/recipe-bulk-record-a-step.md): Multiple selected people receive the intended Step data without silently losing per-person attribute differences.
- [Recipe: Automate Step completion from a Data View](tasks/recipe-automate-step-completion-from-a-data-view.md): The Steps Automation job creates or completes qualifying records while preserving journey rules.
- [Recipe: Build a Streak Type safely](tasks/recipe-build-a-streak-type-safely.md): A Streak Type calculates the intended cadence from the intended source.
- [Recipe: Correct one person’s streak](tasks/recipe-correct-one-person-s-streak.md): A bounded correction is made without unnecessarily rebuilding the entire Streak Type.
- [Recipe: Rebuild a Streak with a controlled boundary](tasks/recipe-rebuild-a-streak-with-a-controlled-boundary.md): Attendance-derived streak data is regenerated at the smallest necessary scope.
- [Recipe: Request and monitor assessments](tasks/recipe-request-and-monitor-assessments.md): The intended people receive valid assessment requests and their completion state can be reviewed.
- [Recipe: Build an assessment-result segment](tasks/recipe-build-an-assessment-result-segment.md): A person Data View identifies people with a specified supported assessment result.
- [Recipe: Connect an Achievement to workflows and Steps](tasks/recipe-connect-an-achievement-to-workflows-and-steps.md): A successful Achievement produces the intended follow-up and journey record.
- [Recipe: Configure Reminder processing](tasks/recipe-configure-reminder-processing.md): A context-valid reminder produces the intended communication or workflow at its reminder date.
- [Recipe: Configure a secure Following event](tasks/recipe-configure-a-secure-following-event.md): Authorized subscribers receive the intended daily event without exposing related sensitive context.
- [Recipe: Operate a moderated Interactive Experience](tasks/recipe-operate-a-moderated-interactive-experience.md): Participants receive the intended actions while only approved responses appear publicly.
- [Recipe: Configure a Sign-Up registration and attendance route](tasks/recipe-configure-a-sign-up-registration-and-attendance-route.md): Guests or an existing group can register, and authorized operators can record attendance.

## High-Signal Sections

- `agent-summary` lines 18-29: Agent Summary (normal)
- `scope-and-boundaries` lines 30-45: Scope And Boundaries (normal)
- `mental-model` lines 46-57: Mental Model (normal)
- `steps-programs-types-and-completion` lines 60-71: Programs, types and completion (normal)
- `steps-entry-attributes-and-history` lines 72-83: Entry, attributes and history (normal)
- `steps-bulk-entry-and-automation` lines 84-91: Bulk entry and automation (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the engagement-tracking guide.
- `Block`: Rock concept/entity referenced by the engagement-tracking guide.
- `Campus`: Rock concept/entity referenced by the engagement-tracking guide.
- `DataView`: Rock concept/entity referenced by the engagement-tracking guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the engagement-tracking guide.
- `Person`: Rock concept/entity referenced by the engagement-tracking guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `StepProgram`: Engagement journey container that can represent milestones, achievements, or discipleship paths.

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
