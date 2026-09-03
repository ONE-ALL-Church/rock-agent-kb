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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Preflight a broad email communication](tasks/recipe-preflight-a-broad-email-communication.md): A reviewed draft whose audience, sender, classification, content, consent and delivery path are ready for the organization’s approval process.
- [Recipe: Diagnose one missing recipient](tasks/recipe-diagnose-one-missing-recipient.md): A specific, evidence-backed reason the person was included, excluded or routed to a different medium.
- [Recipe: Validate an email transport and its event loop](tasks/recipe-validate-an-email-transport-and-its-event-loop.md): A bounded test proves Rock-to-provider handoff, inbox delivery and expected event return.
- [Recipe: Validate inbound SMS routing](tasks/recipe-validate-inbound-sms-routing.md): One controlled inbound message reaches exactly the intended conversation, reply or workflow path.
- [Recipe: Create a communication flow without over-messaging](tasks/recipe-create-a-communication-flow-without-over-messaging.md): A version-appropriate flow with a current audience, measurable goal and explicit exit behavior.
- [Recipe: Investigate rising unsubscribes or saturation](tasks/recipe-investigate-rising-unsubscribes-or-saturation.md): A bounded operational finding identifies affected audiences, senders or message patterns without over-attributing individual motives.
- [Recipe: Retest a workflow-backed communication safely](tasks/recipe-retest-a-workflow-backed-communication-safely.md): One intended communication action is exercised without broadly reopening unrelated workflow work.
- [Recipe: Bound an agent that can draft communications](tasks/recipe-bound-an-agent-that-can-draft-communications.md): An agent can assist with preparation without gaining unintended send or destructive authority.

## High-Signal Sections

- `agent-summary` lines 18-34: Agent Summary (normal)
- `scope-and-boundaries` lines 35-54: Scope And Boundaries (normal)
- `mental-model` lines 55-66: Mental Model (high)
- `communication-foundations` lines 67-83: Communication Foundations (normal)
- `audiences-communication-lists-and-segments` lines 84-93: Audiences, Communication Lists And Segments (normal)
- `templates-and-system-communications` lines 94-103: Templates And System Communications (normal)

## Core Entities

- `Block`: Rock concept/entity referenced by the communications guide.
- `Campus`: Rock concept/entity referenced by the communications guide.
- `DataView`: Rock concept/entity referenced by the communications guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the communications guide.
- `Page`: Rock concept/entity referenced by the communications guide.
- `Person`: Rock concept/entity referenced by the communications guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the communications guide.

## Version Caveats

- `18.3`: Fixed an issue where saving a Communication Template from the Communication Wizard failed if the template name included special characters. The preview image generation used the template name for the file, which caused a
- `18.2`: Fixed an issue where communication approvers were always redirected to the Communication Wizard page, even when the communication was originally created using the Simple Communication page. Approvers are now redirected t

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
