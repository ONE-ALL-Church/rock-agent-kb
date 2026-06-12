---
concept_id: helix
title: Helix Open Questions
generated: true
---

# Helix Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `7-common-helix-workflows-read-only-partial-refresh`: Read-Only Partial Refresh (106 words)
- `20-implementation-playbooks-playbook-a-build-a-read-only-results-panel`: Playbook A: Build A Read-Only Results Panel (103 words)
- `20-implementation-playbooks-playbook-b-build-a-safe-update-form`: Playbook B: Build A Safe Update Form (86 words)

## Community-Supported Only

- `7-common-helix-workflows-admin-utility`: Admin Utility

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `3-helix-mental-model`: 3. Helix Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-lava-application-configuration`: Lava Application Configuration
- `5-core-configuration-and-data-model-lava-endpoint-configuration`: Lava Endpoint Configuration
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `7-common-helix-workflows-read-only-partial-refresh`: Read-Only Partial Refresh
- `7-common-helix-workflows-admin-utility`: Admin Utility
- `7-common-helix-workflows-guided-search-or-finder`: Guided Search Or Finder
- `8-overview-and-roadmap-deep-dive`: 8. Overview And Roadmap Deep Dive
- `9-htmx-deep-dive`: 9. HTMX Deep Dive
- `10-lava-applications-deep-dive`: 10. Lava Applications Deep Dive
- `10-lava-applications-deep-dive-configuration-rigging-strategy`: Configuration Rigging Strategy
- `11-lava-endpoints-deep-dive-routing`: Routing
- `11-lava-endpoints-deep-dive-merge-fields-and-request-body`: Merge Fields And Request Body
- `12-forms-and-controls-deep-dive-lava-form-pattern`: Lava Form Pattern
- `12-forms-and-controls-deep-dive-loading-indicators`: Loading Indicators
- `13-security-and-observability-deep-dive-security-principles`: Security Principles
- `13-security-and-observability-deep-dive-observability`: Observability
- `14-strategies-and-limitations-deep-dive`: 14. Strategies And Limitations Deep Dive
- `15-related-rock-areas-lava-api-integrations-security-cms-workflows-forms-htmx-observability-lava`: Lava
- `15-related-rock-areas-lava-api-integrations-security-cms-workflows-forms-htmx-observability-workflows`: Workflows
- `15-related-rock-areas-lava-api-integrations-security-cms-workflows-forms-htmx-observability-htmx`: HTMX
- `16-administration-and-operational-guardrails`: 16. Administration And Operational Guardrails
- `17-developer-api-lava-and-source-code-landmarks`: 17. Developer, API, Lava, And Source-Code Landmarks
- `18-reporting-analytics-and-model-map`: 18. Reporting, Analytics, And Model Map
- `19-version-and-release-caveats`: 19. Version And Release Caveats
- `20-implementation-playbooks-playbook-a-build-a-read-only-results-panel`: Playbook A: Build A Read-Only Results Panel
- `20-implementation-playbooks-playbook-b-build-a-safe-update-form`: Playbook B: Build A Safe Update Form
- `20-implementation-playbooks-playbook-c-convert-a-static-lava-page-to-helix`: Playbook C: Convert A Static Lava Page To Helix
- `20-implementation-playbooks-playbook-d-audit-an-existing-helix-app`: Playbook D: Audit An Existing Helix App
- `21-troubleshooting-decision-tree-the-button-does-nothing`: The button does nothing
- `21-troubleshooting-decision-tree-endpoint-is-slow`: Endpoint is slow
- `21-troubleshooting-decision-tree-endpoint-modifies-wrong-data`: Endpoint modifies wrong data
- `22-agent-task-recipes-recipe-find-the-endpoint-behind-a-button`: Recipe: Find The Endpoint Behind A Button
- `22-agent-task-recipes-recipe-upgrade-a-plugin-era-helix-app`: Recipe: Upgrade A Plugin-Era Helix App
- `22-agent-task-recipes-recipe-review-a-community-recipe-before-use`: Recipe: Review A Community Recipe Before Use
- `approved-claim-coverage`: Approved Claim Coverage
- `23-source-map-and-dependency-notes`: 23. Source Map And Dependency Notes

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
