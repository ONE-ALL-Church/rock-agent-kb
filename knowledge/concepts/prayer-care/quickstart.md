---
concept_id: prayer-care
title: Prayer And Care Quickstart
generated: true
---

# Prayer And Care Quickstart

Prayer requests, prayer teams, moderation, categories, care follow-up, visibility, communication, and privacy-sensitive ministry workflows.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Audit Prayer Configuration](tasks/audit-prayer-configuration.md): Follow the guide section for Audit Prayer Configuration.
- [Review A Sensitive Request](tasks/review-a-sensitive-request.md): Follow the guide section for Review A Sensitive Request.
- [Build A Prayer-Team Coverage Report](tasks/build-a-prayer-team-coverage-report.md): Follow the guide section for Build A Prayer-Team Coverage Report.
- [Investigate Person Prayer History](tasks/investigate-person-prayer-history.md): Follow the guide section for Investigate Person Prayer History.
- [Safely Extend Prayer Intake](tasks/safely-extend-prayer-intake.md): Follow the guide section for Safely Extend Prayer Intake.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-46: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 47-75: 2. Scope And Terminology (high)
- `3-prayer-and-care-mental-model` lines 76-89: 3. Prayer And Care Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 90-102: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-prayer-request-entry-configuration` lines 105-153: Prayer Request Entry Configuration (high)
- `5-core-configuration-and-data-model-prayer-request-detail-configuration` lines 154-195: Prayer Request Detail Configuration (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the prayer-care guide.
- `Block`: Rock concept/entity referenced by the prayer-care guide.
- `Campus`: Rock concept/entity referenced by the prayer-care guide.
- `Family`: Rock concept/entity referenced by the prayer-care guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the prayer-care guide.
- `Person`: Rock concept/entity referenced by the prayer-care guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the prayer-care guide.

## Version Caveats

- `17.0`: Fixed an issue where Prayer Request Attributes not marked as "Public" were incorrectly displaying in the Obsidian version of the Prayer Request Entry block. These Attributes are now properly hidden on the Prayer Request
- `19.1`: Improved the Prayer Request List block to display prayer request text at a wider width for better readability. Fixes: #6824
- `17.5`: Fixed an issue where approving a Prayer Request in the Obsidian Prayer Request Detail block did not update the ApprovedOnDateTime and ApprovedByPersonAliasId fields. Fixes: #6403
- `17.2`: Fixed an issue where the Prayer Request Detail block in Obsidian did not recognize the PersonId URL parameter, which prevented person data from being pre-filled when creating a new prayer request. Fixes: #6357
- `17.0`: Added support for editing custom attributes within the Mobile Prayer Request block. This enhancement allows individuals to update custom attributes when submitting or managing prayer requests from a mobile device. Be awa
- `18.3`: Added a Campus Type filter to the campus picker on the Prayer Request Detail block. This allows individuals to narrow the list of selectable campuses when adding a new prayer request.
- `17.0`: Added a new feature to Prayer which will optionally run several pre-configured AI completions on saved prayer requests. If you plan on using this feature, read the Tech Bulletin item on this topic.

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
