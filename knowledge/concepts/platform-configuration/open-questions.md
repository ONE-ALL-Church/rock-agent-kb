---
concept_id: platform-configuration
title: Platform Configuration Open Questions
generated: true
---

# Platform Configuration Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `version-and-authority-caveats`: Version And Authority Caveats (198 words)

## Community-Supported Only

- `analytics-and-reporting-configuration`: Analytics And Reporting Configuration
- `troubleshooting-decision-tree-a-dashboard-is-slow`: A dashboard is slow
- `troubleshooting-decision-tree-an-embedded-bi-report-is-inaccessible-or-overexposed`: An embedded BI report is inaccessible or overexposed
- `agent-task-recipes-recipe-move-an-expensive-dashboard-calculation-to-scheduled-storage`: Recipe: Move an expensive dashboard calculation to scheduled storage
- `agent-task-recipes-recipe-secure-an-embedded-bi-report`: Recipe: Secure an embedded BI report
- `source-map-reviewed-community-evidence`: Reviewed community evidence

## Needs Live Verification

- `agent-summary`: Agent Summary
- `attributes-and-attribute-values-separate-the-definition-from-stored-values`: Separate the definition from stored values
- `attributes-and-attribute-values-present-attributes-intentionally`: Present attributes intentionally
- `attributes-and-attribute-values-account-for-channel-specific-support`: Account for channel-specific support
- `defined-types-and-values-defined-value-attributes`: Defined Value attributes
- `defined-types-and-values-detect-source-mismatches`: Detect source mismatches
- `categories-and-entity-types-categories-are-scoped-configuration`: Categories are scoped configuration
- `campuses-and-global-settings-campus-configuration`: Campus configuration
- `campuses-and-global-settings-campus-attributes`: Campus attributes
- `campuses-and-global-settings-room-capacity-and-schedule-availability`: Room capacity and schedule availability
- `campuses-and-global-settings-global-attributes-and-system-settings`: Global attributes and system settings
- `analytics-and-reporting-configuration`: Analytics And Reporting Configuration
- `ai-agents-lava-tools-and-extensions`: AI Agents, Lava Tools, And Extensions
- `cross-domain-version-19-configuration-captcha`: CAPTCHA
- `cross-domain-version-19-configuration-check-in`: Check-in
- `cross-domain-version-19-configuration-event-registration`: Event registration
- `cross-domain-version-19-configuration-communications-and-workflows`: Communications and workflows
- `cross-domain-version-19-configuration-person-merge-and-record-provenance`: Person merge and record provenance
- `troubleshooting-decision-tree-an-attribute-exists-but-is-not-visible`: An attribute exists but is not visible
- `troubleshooting-decision-tree-a-workflow-stores-a-value-but-the-report-shows-the-wrong-label`: A workflow stores a value but the report shows the wrong label
- `troubleshooting-decision-tree-seasonal-options-are-missing-or-still-selectable`: Seasonal options are missing or still selectable
- `troubleshooting-decision-tree-a-campus-selector-is-absent-or-chooses-a-campus-automatically`: A campus selector is absent or chooses a campus automatically
- `troubleshooting-decision-tree-a-campus-cannot-use-the-intended-location`: A campus cannot use the intended location
- `troubleshooting-decision-tree-check-in-room-capacity-or-availability-is-wrong`: Check-in room capacity or availability is wrong
- `troubleshooting-decision-tree-an-embedded-bi-report-is-inaccessible-or-overexposed`: An embedded BI report is inaccessible or overexposed
- `troubleshooting-decision-tree-the-v19-check-in-manager-roster-does-not-update-live`: The v19 Check-In Manager roster does not update live
- `troubleshooting-decision-tree-a-v19-registration-rejects-an-apparently-eligible-person`: A v19 registration rejects an apparently eligible person
- `troubleshooting-decision-tree-an-agent-chooses-the-wrong-tool-or-returns-too-much-data`: An agent chooses the wrong tool or returns too much data
- `agent-task-recipes-recipe-add-and-verify-a-campus-attribute`: Recipe: Add and verify a campus attribute
- `agent-task-recipes-recipe-place-person-attributes-on-a-profile-tab`: Recipe: Place person attributes on a profile tab
- `agent-task-recipes-recipe-audit-a-defined-value-source-mismatch`: Recipe: Audit a Defined Value source mismatch
- `agent-task-recipes-recipe-operate-seasonal-defined-value-options`: Recipe: Operate seasonal Defined Value options
- `agent-task-recipes-recipe-stage-a-campus`: Recipe: Stage a campus
- `agent-task-recipes-recipe-move-an-expensive-dashboard-calculation-to-scheduled-storage`: Recipe: Move an expensive dashboard calculation to scheduled storage
- `agent-task-recipes-recipe-secure-an-embedded-bi-report`: Recipe: Secure an embedded BI report
- `agent-task-recipes-recipe-preflight-a-v19-configuration-change`: Recipe: Preflight a v19 configuration change
- `agent-task-recipes-recipe-design-a-bounded-rock-agent-tool`: Recipe: Design a bounded Rock agent tool
- `agent-task-recipes-recipe-plan-a-rock-upgrade-as-configuration-change`: Recipe: Plan a Rock upgrade as configuration change
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
