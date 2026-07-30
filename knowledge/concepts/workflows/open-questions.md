---
concept_id: workflows
title: Workflows Open Questions
generated: true
---

# Workflows Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (162 words)
- `known-gaps-and-live-verification`: Known Gaps And Live Verification (252 words)

## Community-Supported Only

- `workflow-integrations-lava-entity-operations`: Lava entity operations
- `adjacent-operational-patterns`: Adjacent Operational Patterns
- `troubleshooting-decision-tree-workflowactivate-starts-a-workflow-but-values-are-blank`: `workflowactivate` starts a workflow but values are blank
- `source-map-community-examples-and-reviewed-patterns`: Community examples and reviewed patterns
- `approved-media-coverage`: Approved Media Coverage

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `agent-summary`: Agent Summary
- `mental-model`: Mental Model
- `triggers-and-activation-entry-pages-and-direct-links`: Entry pages and direct links
- `triggers-and-activation-lava-workflowactivate`: Lava `workflowactivate`
- `workflow-forms-chained-forms-and-branching`: Chained forms and branching
- `workflow-forms-form-builder`: Form Builder
- `workflow-forms-person-and-family-entry-patterns`: Person and family entry patterns
- `workflow-integrations-lava-entity-operations`: Lava entity operations
- `managing-workflow-instances-and-staff-work`: Managing Workflow Instances And Staff Work
- `connections-as-operational-workflows`: Connections As Operational Workflows
- `security-and-governance`: Security And Governance
- `troubleshooting-decision-tree-a-workflow-or-form-is-not-visible`: A workflow or form is not visible
- `troubleshooting-decision-tree-a-form-field-is-missing-unexpectedly-required-or-exposing-data`: A form field is missing, unexpectedly required, or exposing data
- `troubleshooting-decision-tree-a-workflow-action-was-skipped`: A workflow action was skipped
- `troubleshooting-decision-tree-a-workflow-is-stuck-or-repeatedly-processing`: A workflow is stuck or repeatedly processing
- `troubleshooting-decision-tree-a-webhook-returns-404-or-launches-the-wrong-number-of-workflows`: A webhook returns 404 or launches the wrong number of workflows
- `troubleshooting-decision-tree-workflowactivate-starts-a-workflow-but-values-are-blank`: `workflowactivate` starts a workflow but values are blank
- `troubleshooting-decision-tree-a-connection-request-is-missing-from-a-board-or-list`: A connection request is missing from a board or list
- `troubleshooting-decision-tree-sql-or-reporting-cannot-see-a-value-just-submitted-by-a-form`: SQL or reporting cannot see a value just submitted by a form
- `troubleshooting-decision-tree-lava-output-is-blank-or-a-parser-error-points-at-the-wrong-line`: Lava output is blank or a parser error points at the wrong line
- `agent-task-recipes-recipe-design-a-bounded-workflow-type`: Recipe: Design a bounded workflow type
- `agent-task-recipes-recipe-review-a-workflow-form-change`: Recipe: Review a workflow form change
- `agent-task-recipes-recipe-configure-a-selective-workflow-webhook`: Recipe: Configure a selective workflow webhook
- `agent-task-recipes-recipe-diagnose-an-active-workflow-instance`: Recipe: Diagnose an active workflow instance
- `agent-task-recipes-recipe-audit-a-connection-follow-up-process`: Recipe: Audit a connection follow-up process
- `agent-task-recipes-recipe-import-or-adapt-a-workflow-safely`: Recipe: Import or adapt a workflow safely
- `agent-task-recipes-recipe-design-background-orchestration`: Recipe: Design background orchestration
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `approved-claim-coverage`: Approved Claim Coverage

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
