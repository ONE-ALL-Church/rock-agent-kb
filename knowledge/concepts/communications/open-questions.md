---
concept_id: communications
title: Communications Open Questions
generated: true
---

# Communications Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `agent-task-recipes-recipe-retest-a-workflow-backed-communication-safely`: Recipe: Retest a workflow-backed communication safely
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

## Needs Live Verification

- `agent-summary`: Agent Summary
- `scope-and-boundaries`: Scope And Boundaries
- `communication-foundations`: Communication Foundations
- `audiences-communication-lists-and-segments`: Audiences, Communication Lists And Segments
- `templates-and-system-communications`: Templates And System Communications
- `email`: Email
- `sms`: SMS
- `sms-sms-conversations`: SMS Conversations
- `sms-sms-pipeline`: SMS Pipeline
- `sending-classification-and-approval`: Sending, Classification And Approval
- `preferences-consent-and-sender-reputation`: Preferences, Consent And Sender Reputation
- `communication-flows-and-automation-boundaries`: Communication Flows And Automation Boundaries
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-intended-recipients-are-missing-or-shown-as-ineligible`: Intended recipients are missing or shown as ineligible
- `troubleshooting-decision-tree-email-appears-sent-but-delivery-or-analytics-are-missing`: Email appears sent but delivery or analytics are missing
- `troubleshooting-decision-tree-email-shows-an-unexpected-sender-or-on-behalf-of-label`: Email shows an unexpected sender or “on behalf of” label
- `troubleshooting-decision-tree-two-unsubscribe-options-appear-in-an-email`: Two unsubscribe options appear in an email
- `troubleshooting-decision-tree-a-template-is-missing-or-cannot-be-saved`: A template is missing or cannot be saved
- `troubleshooting-decision-tree-a-communication-remains-pending-approval`: A communication remains pending approval
- `troubleshooting-decision-tree-incoming-sms-does-not-reach-the-expected-conversation-or-workflow`: Incoming SMS does not reach the expected conversation or workflow
- `troubleshooting-decision-tree-an-automated-sms-reply-is-absent-from-history`: An automated SMS reply is absent from history
- `troubleshooting-decision-tree-sms-segments-cost-or-delivery-differ-from-expectations`: SMS segments, cost or delivery differ from expectations
- `troubleshooting-decision-tree-an-unsubscribe-appears-unexpected`: An unsubscribe appears unexpected
- `agent-task-recipes-recipe-preflight-a-broad-email-communication`: Recipe: Preflight a broad email communication
- `agent-task-recipes-recipe-diagnose-one-missing-recipient`: Recipe: Diagnose one missing recipient
- `agent-task-recipes-recipe-validate-an-email-transport-and-its-event-loop`: Recipe: Validate an email transport and its event loop
- `agent-task-recipes-recipe-validate-inbound-sms-routing`: Recipe: Validate inbound SMS routing
- `agent-task-recipes-recipe-create-a-communication-flow-without-over-messaging`: Recipe: Create a communication flow without over-messaging
- `agent-task-recipes-recipe-investigate-rising-unsubscribes-or-saturation`: Recipe: Investigate rising unsubscribes or saturation
- `agent-task-recipes-recipe-retest-a-workflow-backed-communication-safely`: Recipe: Retest a workflow-backed communication safely
- `agent-task-recipes-recipe-bound-an-agent-that-can-draft-communications`: Recipe: Bound an agent that can draft communications
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `source-map`: Source Map

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
