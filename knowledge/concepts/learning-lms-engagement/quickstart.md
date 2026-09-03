---
concept_id: learning-lms-engagement
title: Learning, LMS, And Engagement Quickstart
generated: true
---

# Learning, LMS, And Engagement Quickstart

Learning programs, LMS courses, lessons, requirements, completion tracking, engagement journeys, and learning-related reporting.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Audit One LMS Program](tasks/recipe-audit-one-lms-program.md): Trace a program from source content through courses, classes, activities, completion, communications, and reporting.
- [Recipe: Find Why A Person Is Not Complete](tasks/recipe-find-why-a-person-is-not-complete.md): Determine whether the missing completion is caused by enrollment, activity completion, program rollup, workflow timing, or reporting filters.
- [Recipe: Prepare A Course For Launch](tasks/recipe-prepare-a-course-for-launch.md): Prepare a course or class for learners by checking structure, activities, schedules, access, communications, and reporting.
- [Recipe: Build A Step Journey From Training](tasks/recipe-build-a-step-journey-from-training.md): Connect training completion to an engagement journey only through explicit workflows, data views, or step-writing logic.
- [Recipe: Review Upgrade Risk](tasks/recipe-review-upgrade-risk.md): Review LMS, engagement, requirement, workflow, and communication behavior against current release notes and source-code caveats.

## High-Signal Sections

- `agent-summary` lines 18-36: Agent Summary (normal)
- `mental-model` lines 54-67: Mental Model (normal)
- `courses-and-lessons-choose-the-program-mode-first` lines 70-77: Choose the program mode first (normal)
- `courses-and-lessons-build-the-hierarchy-in-configuration-order` lines 78-94: Build the hierarchy in configuration order (normal)
- `courses-and-lessons-revise-a-class-without-disrupting-the-current-one` lines 95-100: Revise a class without disrupting the current one (normal)
- `activity-design-and-staff-responsibilities-content-article` lines 111-116: Content article (high)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `Data View`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `DataView`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Group Member Requirement`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `GroupMemberRequirement`: Serving or membership qualification gate that can depend on training, background checks, documents, or manual review.
- `Label`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `Learning Class`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `Learning Class Activity`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `Learning Class Activity Completion`: Rock concept/entity referenced by the learning-lms-engagement guide.
- `Learning Course`: Rock concept/entity referenced by the learning-lms-engagement guide.

## Version Caveats

- `18.1`: Added the new Content Article Learning Activity type, allowing individuals to complete training by reading content articles. Also added support for SMS notifications to alert individuals about new learning activities. Im
- `17.0`: Added the Learning Management System (LMS) that provides tools to create and manage educational content, training programs, and courses within your organization.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
