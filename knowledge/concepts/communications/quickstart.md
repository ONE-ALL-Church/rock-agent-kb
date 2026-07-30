---
concept_id: communications
title: Communications Quickstart
generated: true
---

# Communications Quickstart

Email, SMS, communication templates, transports, segments, and deliverability.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Audit a single sent communication](tasks/recipe-audit-a-single-sent-communication.md): Complete Audit a single sent communication with evidence-backed checks and a verifiable outcome.
- [Recipe: Explain why a person did not get an email](tasks/recipe-explain-why-a-person-did-not-get-an-email.md): Answer in evidence form: "Person was in audience but excluded by preference", "Person was not in audience", "Person had pending recipient row but transport failed", or "Rock sent successfully; provider logs must be checked."
- [Recipe: Explain why a person did not get SMS](tasks/recipe-explain-why-a-person-did-not-get-sms.md): Complete Explain why a person did not get SMS with evidence-backed checks and a verifiable outcome.
- [Recipe: Audit communication list freshness](tasks/recipe-audit-communication-list-freshness.md): Flag if the list is one of Rock's shipped lists and no sync path exists, because RockU notes shipped lists are not automatically synced (Communication Lists & Segments).
- [Recipe: Review a communication template](tasks/recipe-review-a-communication-template.md): Complete Review a communication template with evidence-backed checks and a verifiable outcome.
- [Recipe: Investigate SMS conversation access](tasks/recipe-investigate-sms-conversation-access.md): Complete Investigate SMS conversation access with evidence-backed checks and a verifiable outcome.
- [Recipe: Determine whether a workflow email supports analytics](tasks/recipe-determine-whether-a-workflow-email-supports-analytics.md): Do not promise analytics for workflow emails unless confirmed in the live instance. The source pack includes an unanswered community question showing this can differ by path (Mailgun Tracking Q&A).

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-58: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 59-84: 2. Scope And Terminology (high)
- `3-communications-mental-model` lines 85-104: 3. Communications Mental Model (high)
- `4-source-authority-and-how-to-use-this-guide` lines 105-116: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-communication-transports` lines 119-134: Communication transports (normal)
- `5-core-configuration-and-data-model-communication-mediums` lines 135-140: Communication mediums (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Block`: Rock concept/entity referenced by the communications guide.
- `Campus`: Rock concept/entity referenced by the communications guide.
- `DataView`: Rock concept/entity referenced by the communications guide.
- `Family`: Rock concept/entity referenced by the communications guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the communications guide.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Page`: Rock concept/entity referenced by the communications guide.
- `Person`: Rock concept/entity referenced by the communications guide.
- `PersonAlias`: Rock concept/entity referenced by the communications guide.
- `Step`: Person-specific engagement milestone instance.

## Version Caveats

- `18.3`: Fixed an issue where saving a Communication Template from the Communication Wizard failed if the template name included special characters. The preview image generation used the template name for the file, which caused a
- `18.2`: Fixed an issue where communication approvers were always redirected to the Communication Wizard page, even when the communication was originally created using the Simple Communication page. Approvers are now redirected t
- `18.2`: Fixed an issue with the Communication Entry Wizard block where changing the Communication Type (e.g., from Recipient Preference to Email or SMS) while creating a message could result in some recipients being excluded fro
- `18.1`: Added an Obsidian Communication Detail block with improved message visualization and Communication Recipient insights, allowing administrators to review communication content, delivery status, and recipient activity more
- `19.1`: Added a "Communication Access Mode" setting to the Communication Detail Block along with a new "View All" security action. The default mode is "Strict", which limits viewing of Communication details to the individual who
- `18.3`: Fixed an issue where the Obsidian Communication Entry Wizard block did not enforce the allowed Communication Types configured in block settings when a Communication was started from outside the wizard (e.g., when using a
- `18.2`: Fixed an issue where submitting a registration would disable an individual's SMS setting when the "Show SMS Opt-In" option on the Registration Template was set to False. The registration process will now preserve the ind
- `18.1`: Added Communication Flows, a new tool under Admin Tools › Communications that lets administrators create automated, multi-step sequences across email, SMS, and push notifications. The feature tracks email opens, link cli

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
