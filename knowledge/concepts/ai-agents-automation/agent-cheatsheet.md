---
concept_id: ai-agents-automation
title: AI Agents And Automation Agent Cheatsheet
generated: true
---

# AI Agents And Automation Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Design a safe read-only lookup surface](tasks/recipe-design-a-safe-read-only-lookup-surface.md) |  |  |
| [Recipe: Build a bounded List and Get pair](tasks/recipe-build-a-bounded-list-and-get-pair.md) | `Page` | `Page` |
| [Recipe: Add a controlled AddOrUpdate capability](tasks/recipe-add-a-controlled-addorupdate-capability.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Configure a drafting agent without send authority](tasks/recipe-configure-a-drafting-agent-without-send-authority.md) | `Group` | `Group` |
| [Recipe: Launch a workflow through an agent](tasks/recipe-launch-a-workflow-through-an-agent.md) | `Person`, `Workflow`, `Attribute` | `Person`, `Workflow`, `Attribute` |
| [Recipe: Review a Public agent before launch](tasks/recipe-review-a-public-agent-before-launch.md) |  |  |
| [Recipe: Diagnose incorrect tool selection](tasks/recipe-diagnose-incorrect-tool-selection.md) |  |  |
| [Recipe: Roll out an agent-assisted process to staff](tasks/recipe-roll-out-an-agent-assisted-process-to-staff.md) | `Group`, `Workflow` | `Group`, `Workflow` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added a new "Chat Message" Automation Trigger that can launch Automation Events when a Chat message is sent. Also added a "Send Fallback Chat Notification" Automation Event that alerts individuals via alternate methods (such as email or SMS |
| `17.5` | core | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to t |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `mental-model-control-stack` | citation-only | live verification |
| `permissions-and-data-boundaries-apply-least-privilege-at-every-layer` | normal | live verification |
| `permissions-and-data-boundaries-bound-mcp-authentication` | citation-only | live verification |
| `prompt-and-tool-boundaries` | normal | live verification |
| `automation-design-and-workflows-use-rock-workflows-as-bounded-action-surfaces` | normal | live verification |
| `automation-design-and-workflows-connect-event-driven-automation-carefully` | normal | live verification |
| `automation-design-and-workflows-treat-generated-summaries-as-assistance` | citation-only | live verification |
| `verification-and-review-gates` | normal | live verification |
| `troubleshooting-decision-tree-the-agent-does-not-show-a-tool` | normal | live verification |
| `troubleshooting-decision-tree-the-agent-chooses-the-wrong-tool` | normal | live verification |
| `troubleshooting-decision-tree-the-agent-acts-on-the-wrong-person-or-entity` | normal | live verification |
| `troubleshooting-decision-tree-the-tool-returns-unauthorized-or-sensitive-data` | normal | live verification |
| `troubleshooting-decision-tree-a-list-is-incomplete-repeats-items-or-becomes-slow-on-later-pages` | normal | live verification |
| `troubleshooting-decision-tree-a-lava-tool-errors-or-returns-unexpected-no-data` | normal | live verification |
| `troubleshooting-decision-tree-a-mutation-was-refused-or-changed-the-wrong-state` | normal | live verification |
| `troubleshooting-decision-tree-a-connection-request-ai-summary-is-missing` | citation-only | live verification |
| `troubleshooting-decision-tree-an-mcp-client-cannot-authenticate-or-discovers-unexpected-tools` | citation-only | live verification |
| `troubleshooting-decision-tree-a-workflow-does-not-launch` | normal | live verification |
| `agent-task-recipes-recipe-design-a-safe-read-only-lookup-surface` | normal | live verification |
| `agent-task-recipes-recipe-build-a-bounded-list-and-get-pair` | normal | live verification |
| `agent-task-recipes-recipe-add-a-controlled-addorupdate-capability` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-drafting-agent-without-send-authority` | normal | live verification |
| `agent-task-recipes-recipe-launch-a-workflow-through-an-agent` | normal | live verification |
| `agent-task-recipes-recipe-review-a-public-agent-before-launch` | normal | live verification |
| `agent-task-recipes-recipe-diagnose-incorrect-tool-selection` | normal | live verification |
| `agent-task-recipes-recipe-roll-out-an-agent-assisted-process-to-staff` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
