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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Configure moderated public prayer intake](tasks/recipe-configure-moderated-public-prayer-intake.md): Public submissions enter the intended category and do not reach the prayer team without the chosen approval gate.
- [Recipe: Operate the administrator moderation queue](tasks/recipe-operate-the-administrator-moderation-queue.md): Flagged and unapproved requests receive documented human disposition.
- [Recipe: Build a secured ministry-specific prayer queue](tasks/recipe-build-a-secured-ministry-specific-prayer-queue.md): A ministry team sees only the intended category scope through a secured page.
- [Recipe: Create and verify a group prayer route](tasks/recipe-create-and-verify-a-group-prayer-route.md): New requests are permanently associated with the correct group and appear only through that group’s prayer route.
- [Recipe: Enable prayer-comment digests](tasks/recipe-enable-prayer-comment-digests.md): Allowed comments are delivered to request-specific email addresses within the intended category scope.
- [Recipe: Add workflow-based care follow-up](tasks/recipe-add-workflow-based-care-follow-up.md): A qualifying prayer event creates a bounded care action without exposing the request broadly.
- [Recipe: Introduce AI assistance with human review](tasks/recipe-introduce-ai-assistance-with-human-review.md): AI processing is limited to known categories and produces reviewable results.
- [Recipe: Validate Outreach Toolbox for prayer touchpoints](tasks/recipe-validate-outreach-toolbox-for-prayer-touchpoints.md): A signed-in mobile user can see, complete, and receive reminders for an assigned prayer touchpoint.

## High-Signal Sections

- `agent-summary` lines 18-33: Agent Summary (normal)
- `scope-and-boundaries` lines 34-51: Scope And Boundaries (high)
- `mental-model` lines 52-67: Mental Model (high)
- `prayer-request-intake-and-lifecycle` lines 68-94: Prayer Request Intake And Lifecycle (high)
- `categories-visibility-and-page-security` lines 95-110: Categories, Visibility, And Page Security (high)
- `teams-approval-and-human-moderation` lines 111-127: Teams, Approval, And Human Moderation (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the prayer-care guide.
- `Block`: Rock concept/entity referenced by the prayer-care guide.
- `Campus`: Rock concept/entity referenced by the prayer-care guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the prayer-care guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Page`: Rock concept/entity referenced by the prayer-care guide.
- `Person`: Rock concept/entity referenced by the prayer-care guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the prayer-care guide.

## Version Caveats

- `17.0`: Fixed an issue where Prayer Request Attributes not marked as "Public" were incorrectly displaying in the Obsidian version of the Prayer Request Entry block. These Attributes are now properly hidden on the Prayer Request
- `19.3`: Fixed the Prayer Comment List block: custom grid columns can now access the prayer request and requester via the Row Lava merge field, the From-column and date-range filters work, and several performance and dead-code is
- `19.1`: Improved the Prayer Request List block to display prayer request text at a wider width for better readability. Fixes: #6824
- `17.5`: Fixed an issue where approving a Prayer Request in the Obsidian Prayer Request Detail block did not update the ApprovedOnDateTime and ApprovedByPersonAliasId fields. Fixes: #6403
- `17.2`: Fixed an issue where the Prayer Request Detail block in Obsidian did not recognize the PersonId URL parameter, which prevented person data from being pre-filled when creating a new prayer request. Fixes: #6357

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
