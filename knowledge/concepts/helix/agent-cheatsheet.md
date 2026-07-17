---
concept_id: helix
title: Helix Agent Cheatsheet
generated: true
---

# Helix Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Find The Endpoint Behind A Button](tasks/recipe-find-the-endpoint-behind-a-button.md) |  |  |
| [Recipe: Determine Whether A Helix App Is Public-Safe](tasks/recipe-determine-whether-a-helix-app-is-public-safe.md) |  |  |
| [Recipe: Upgrade A Plugin-Era Helix App](tasks/recipe-upgrade-a-plugin-era-helix-app.md) |  |  |
| [Recipe: Review A Community Recipe Before Use](tasks/recipe-review-a-community-recipe-before-use.md) |  |  |
| [Recipe: Add Observability To A Complex Endpoint](tasks/recipe-add-observability-to-a-complex-endpoint.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added Helix support for Lava Applications to core. This provides a great new way to build interactive pages in Rock powered by Lava for more advanced administrators. |
| `19.1` | core | Added Body and RawBody merge fields to Lava Applications. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `3-helix-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-lava-application-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-lava-endpoint-configuration` | normal | live verification |
| `6-primary-entities-and-relationships` | normal | live verification |
| `7-common-helix-workflows-read-only-partial-refresh` | normal | live verification |
| `7-common-helix-workflows-admin-utility` | community-supported | live verification |
| `7-common-helix-workflows-guided-search-or-finder` | citation-only | live verification |
| `8-overview-and-roadmap-deep-dive` | normal | live verification |
| `9-htmx-deep-dive` | normal | live verification |
| `10-lava-applications-deep-dive` | normal | live verification |
| `10-lava-applications-deep-dive-configuration-rigging-strategy` | normal | live verification |
| `11-lava-endpoints-deep-dive-routing` | normal | live verification |
| `11-lava-endpoints-deep-dive-merge-fields-and-request-body` | normal | live verification |
| `12-forms-and-controls-deep-dive-lava-form-pattern` | normal | live verification |
| `12-forms-and-controls-deep-dive-loading-indicators` | normal | live verification |
| `13-security-and-observability-deep-dive-security-principles` | normal | live verification |
| `13-security-and-observability-deep-dive-observability` | normal | live verification |
| `14-strategies-and-limitations-deep-dive` | normal | live verification |
| `15-related-rock-areas-lava-api-integrations-security-cms-workflows-forms-htmx-observability-lava` | normal | live verification |
| `15-related-rock-areas-lava-api-integrations-security-cms-workflows-forms-htmx-observability-workflows` | structural | live verification |
| `15-related-rock-areas-lava-api-integrations-security-cms-workflows-forms-htmx-observability-htmx` | normal | live verification |
| `16-administration-and-operational-guardrails` | normal | live verification |
| `17-developer-api-lava-and-source-code-landmarks` | normal | live verification |
| `18-reporting-analytics-and-model-map` | normal | live verification |
| `19-version-and-release-caveats` | normal | live verification |
| `20-implementation-playbooks-playbook-a-build-a-read-only-results-panel` | normal | live verification |
| `20-implementation-playbooks-playbook-b-build-a-safe-update-form` | normal | live verification |
| `20-implementation-playbooks-playbook-c-convert-a-static-lava-page-to-helix` | structural | live verification |
| `20-implementation-playbooks-playbook-d-audit-an-existing-helix-app` | structural | live verification |
| `21-troubleshooting-decision-tree-the-button-does-nothing` | normal | live verification |
| `21-troubleshooting-decision-tree-endpoint-is-slow` | normal | live verification |
| `21-troubleshooting-decision-tree-endpoint-modifies-wrong-data` | structural | live verification |
| `22-agent-task-recipes-recipe-find-the-endpoint-behind-a-button` | structural | live verification |
| `22-agent-task-recipes-recipe-upgrade-a-plugin-era-helix-app` | structural | live verification |
| `22-agent-task-recipes-recipe-review-a-community-recipe-before-use` | structural | live verification |
| `approved-claim-coverage` | normal | live verification |
| `23-source-map-and-dependency-notes` | normal | live verification |
