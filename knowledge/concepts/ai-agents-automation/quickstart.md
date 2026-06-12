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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: “Find The Right Person”](tasks/recipe-find-the-right-person.md): Follow the guide section for Recipe: “Find The Right Person”.
- [Recipe: “Summarize This Person”](tasks/recipe-summarize-this-person.md): Follow the guide section for Recipe: “Summarize This Person”.
- [Recipe: “Draft A Communication”](tasks/recipe-draft-a-communication.md): Follow the guide section for Recipe: “Draft A Communication”.
- [Recipe: “Create A Connection Request”](tasks/recipe-create-a-connection-request.md): Follow the guide section for Recipe: “Create A Connection Request”.
- [Recipe: “Explain A Workflow Queue”](tasks/recipe-explain-a-workflow-queue.md): Follow the guide section for Recipe: “Explain A Workflow Queue”.
- [Recipe: “Audit Agent Security”](tasks/recipe-audit-agent-security.md): Follow the guide section for Recipe: “Audit Agent Security”.
- [Recipe: “Build A Safe Public Agent”](tasks/recipe-build-a-safe-public-agent.md): Follow the guide section for Recipe: “Build A Safe Public Agent”.
- [Recipe: “Review An Agent Answer”](tasks/recipe-review-an-agent-answer.md): Follow the guide section for Recipe: “Review An Agent Answer”.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-54: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 55-107: 2. Scope And Terminology (high)
- `3-ai-agents-and-automation-mental-model` lines 108-135: 3. AI Agents And Automation Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 136-163: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model` lines 164-215: 5. Core Configuration And Data Model (normal)
- `6-primary-entities-and-relationships` lines 216-244: 6. Primary Entities And Relationships (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Block`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Campus`: Rock concept/entity referenced by the ai-agents-automation guide.
- `DataView`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Family`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Page`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Person`: Rock concept/entity referenced by the ai-agents-automation guide.
- `PersonAlias`: Rock concept/entity referenced by the ai-agents-automation guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.

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
