---
concept_id: ai-agents-automation
title: AI Agents And Automation Quickstart
generated: true
---

# AI Agents And Automation Quickstart

Rock AI agents, custom tools, automation patterns, tool security, least privilege, prompt/tool boundaries, review gates, and live verification.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Design a safe read-only lookup surface](tasks/recipe-design-a-safe-read-only-lookup-surface.md): The agent can resolve a natural-language reference to an authorized Rock entity without receiving unnecessary data.
- [Recipe: Build a bounded List and Get pair](tasks/recipe-build-a-bounded-list-and-get-pair.md): The agent can search a large entity set and retrieve details only for the selected item.
- [Recipe: Add a controlled AddOrUpdate capability](tasks/recipe-add-a-controlled-addorupdate-capability.md): An authorized user can create or edit one entity through a validated, auditable tool.
- [Recipe: Configure a drafting agent without send authority](tasks/recipe-configure-a-drafting-agent-without-send-authority.md): Staff can research and compose a communication while sending remains a separate approved action.
- [Recipe: Launch a workflow through an agent](tasks/recipe-launch-a-workflow-through-an-agent.md): The agent launches one permitted workflow with valid attribute values and verifies the resulting record.
- [Recipe: Review a Public agent before launch](tasks/recipe-review-a-public-agent-before-launch.md): The public surface exposes only reviewed, non-sensitive and non-destructive capabilities.
- [Recipe: Diagnose incorrect tool selection](tasks/recipe-diagnose-incorrect-tool-selection.md): The model consistently chooses the intended tool for representative requests.
- [Recipe: Roll out an agent-assisted process to staff](tasks/recipe-roll-out-an-agent-assisted-process-to-staff.md): Staff understand the approved use case, review boundary and authoritative Rock workflow before volunteer rollout.

## High-Signal Sections

- `agent-summary` lines 18-40: Agent Summary (normal)
- `scope-and-boundaries` lines 41-60: Scope And Boundaries (normal)
- `mental-model-agent-skill-and-tool` lines 63-70: Agent, skill and tool (normal)
- `mental-model-chat-mcp-internal-and-public-are-separate-choices` lines 86-91: Chat, MCP, Internal and Public are separate choices (normal)
- `agent-tools-and-lookup-surfaces-shape-tools-around-intent` lines 94-110: Shape tools around intent (normal)
- `agent-tools-and-lookup-surfaces-use-lookup-list-and-get-as-a-sequence` lines 111-116: Use lookup, list and get as a sequence (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the ai-agents-automation guide.
- `DataView`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Page`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Person`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Workflow`: Rock concept/entity referenced by the ai-agents-automation guide.

## Version Caveats

- `18.1`: Added a new "Chat Message" Automation Trigger that can launch Automation Events when a Chat message is sent. Also added a "Send Fallback Chat Notification" Automation Event that alerts individuals via alternate methods (
- `17.5`: Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted expl

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
