---
concept_id: ai-agents-automation
title: AI Agents And Automation Open Questions
generated: true
---

# AI Agents And Automation Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only


## Needs Live Verification

- `agent-summary`: Agent Summary
- `mental-model-control-stack`: Control stack
- `permissions-and-data-boundaries-apply-least-privilege-at-every-layer`: Apply least privilege at every layer
- `permissions-and-data-boundaries-bound-mcp-authentication`: Bound MCP authentication
- `prompt-and-tool-boundaries`: Prompt And Tool Boundaries
- `automation-design-and-workflows-use-rock-workflows-as-bounded-action-surfaces`: Use Rock workflows as bounded action surfaces
- `automation-design-and-workflows-connect-event-driven-automation-carefully`: Connect event-driven automation carefully
- `automation-design-and-workflows-treat-generated-summaries-as-assistance`: Treat generated summaries as assistance
- `verification-and-review-gates`: Verification And Review Gates
- `troubleshooting-decision-tree-the-agent-does-not-show-a-tool`: The agent does not show a tool
- `troubleshooting-decision-tree-the-agent-chooses-the-wrong-tool`: The agent chooses the wrong tool
- `troubleshooting-decision-tree-the-agent-acts-on-the-wrong-person-or-entity`: The agent acts on the wrong person or entity
- `troubleshooting-decision-tree-the-tool-returns-unauthorized-or-sensitive-data`: The tool returns unauthorized or sensitive data
- `troubleshooting-decision-tree-a-list-is-incomplete-repeats-items-or-becomes-slow-on-later-pages`: A list is incomplete, repeats items or becomes slow on later pages
- `troubleshooting-decision-tree-a-lava-tool-errors-or-returns-unexpected-no-data`: A Lava tool errors or returns unexpected no-data
- `troubleshooting-decision-tree-a-mutation-was-refused-or-changed-the-wrong-state`: A mutation was refused or changed the wrong state
- `troubleshooting-decision-tree-a-connection-request-ai-summary-is-missing`: A connection-request AI summary is missing
- `troubleshooting-decision-tree-an-mcp-client-cannot-authenticate-or-discovers-unexpected-tools`: An MCP client cannot authenticate or discovers unexpected tools
- `troubleshooting-decision-tree-a-workflow-does-not-launch`: A workflow does not launch
- `agent-task-recipes-recipe-design-a-safe-read-only-lookup-surface`: Recipe: Design a safe read-only lookup surface
- `agent-task-recipes-recipe-build-a-bounded-list-and-get-pair`: Recipe: Build a bounded List and Get pair
- `agent-task-recipes-recipe-add-a-controlled-addorupdate-capability`: Recipe: Add a controlled AddOrUpdate capability
- `agent-task-recipes-recipe-configure-a-drafting-agent-without-send-authority`: Recipe: Configure a drafting agent without send authority
- `agent-task-recipes-recipe-launch-a-workflow-through-an-agent`: Recipe: Launch a workflow through an agent
- `agent-task-recipes-recipe-review-a-public-agent-before-launch`: Recipe: Review a Public agent before launch
- `agent-task-recipes-recipe-diagnose-incorrect-tool-selection`: Recipe: Diagnose incorrect tool selection
- `agent-task-recipes-recipe-roll-out-an-agent-assisted-process-to-staff`: Recipe: Roll out an agent-assisted process to staff
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
