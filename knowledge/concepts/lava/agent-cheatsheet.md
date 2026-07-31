---
concept_id: lava
title: Lava Agent Cheatsheet
generated: true
---

# Lava Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Inventory Lava Risk On A Page](tasks/recipe-inventory-lava-risk-on-a-page.md) | `Workflow`, `Page`, `Block` | `Workflow`, `Page`, `Block` |
| [Recipe: Review A Shortcode For Production](tasks/recipe-review-a-shortcode-for-production.md) | `Block`, `Attribute` | `Block`, `Attribute` |
| [Recipe: Find Legacy Attribute Lava](tasks/recipe-find-legacy-attribute-lava.md) | `Workflow`, `Page`, `Block`, `Attribute` | `Workflow`, `Page`, `Block`, `Attribute` |
| [Recipe: Safely Use `securityenabled:'false'`](tasks/recipe-safely-use-securityenabled-false.md) | `Page`, `Block`, `Attribute` | `Page`, `Block`, `Attribute` |
| [Recipe: Create A Staff-Friendly Link Copy Shortcode](tasks/recipe-create-a-staff-friendly-link-copy-shortcode.md) | `Label`, `Workflow`, `Page`, `Attribute` | `Label`, `Workflow`, `Page`, `Attribute` |
| [Recipe: Add A Translation Shortcode](tasks/recipe-add-a-translation-shortcode.md) |  |  |
| [Recipe: Generate Labels With Lava](tasks/recipe-generate-labels-with-lava.md) | `Group`, `Device`, `Label` | `Group`, `Device`, `Label` |
| [Recipe: Build An Agent Lava Tool](tasks/recipe-build-an-agent-lava-tool.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Added a new Shortcode Scope Behavior property to the Lava Shortcode Entity. This setting allows Rock administrators to choose whether variables defined inside a shortcode should be isolated from or shared with the surrounding Lava. This hel |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | community-supported | live verification |
| `5-core-configuration-and-data-model-lava-engine-liquid-framework` | normal | live verification |
| `5-core-configuration-and-data-model-default-enabled-lava-commands` | normal | live verification |
| `5-core-configuration-and-data-model-html-block-command-enablement` | normal | live verification |
| `5-core-configuration-and-data-model-communication-entry-command-enablement` | normal | live verification |
| `5-core-configuration-and-data-model-lava-shortcode-entity` | normal | live verification |
| `5-core-configuration-and-data-model-lava-shortcode-cache` | normal | live verification |
| `5-core-configuration-and-data-model-lava-webhooks` | normal | live verification |
| `5-core-configuration-and-data-model-remote-lava-rest-endpoint` | normal | live verification |
| `6-primary-entities-and-relationships-block-page-site-theme-and-include-files` | normal | live verification |
| `6-primary-entities-and-relationships-entity-commands-and-rock-models` | normal | live verification |
| `6-primary-entities-and-relationships-attribute-and-attributevalue` | normal | live verification |
| `6-primary-entities-and-relationships-workflow-workflow-type-activity-type-and-attributes` | normal | live verification |
| `6-primary-entities-and-relationships-interaction-records` | normal | live verification |
| `6-primary-entities-and-relationships-devices-and-printers` | normal | live verification |
| `6-primary-entities-and-relationships-search-index-documents` | normal | live verification |
| `7-common-lava-workflows-building-a-dynamic-report-page` | community-supported | live verification |
| `7-common-lava-workflows-formatting-data-with-shortcodes` | community-supported | community-supported |
| `7-common-lava-workflows-calling-external-apis` | normal | live verification |
| `7-common-lava-workflows-adding-page-level-css` | normal | live verification |
| `8-commands-deep-dive-entity-command` | normal | live verification |
| `8-commands-deep-dive-interaction-write-commands` | normal | live verification |
| `8-commands-deep-dive-adaptive-message-command` | normal | live verification |
| `8-commands-deep-dive-helix-commands-and-data-modification` | normal | live verification |
| `9-filters-deep-dive` | structural | live verification |
| `9-filters-deep-dive-attribute-filter` | normal | live verification |
| `9-filters-deep-dive-legacy-attribute-syntax` | community-supported | live verification |
| `9-filters-deep-dive-date-filters` | normal | live verification |
| `9-filters-deep-dive-person-filters` | normal | live verification |
| `9-filters-deep-dive-text-filters` | normal | live verification |
| `9-filters-deep-dive-culture-affected-filters` | normal | live verification |
| `10-shortcodes-deep-dive-shortcode-configuration-fields` | normal | live verification |
| `10-shortcodes-deep-dive-enabled-commands-inside-shortcodes` | normal | live verification |
| `10-shortcodes-deep-dive-scope-behavior` | normal | live verification |
| `11-related-rock-areas-cms-workflows-sql-security-cms` | normal | live verification |
| `11-related-rock-areas-cms-workflows-sql-security-workflows` | normal | live verification |
| `11-related-rock-areas-cms-workflows-sql-security-sql` | normal | live verification |
| `12-administration-and-operational-guardrails-pre-change-checklist` | structural | live verification |
| `12-administration-and-operational-guardrails-exception-list-checklist` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-remote-execution-checklist` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-rocku` | community-supported | community-supported |
| `13-developer-api-lava-and-source-code-landmarks-helix` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-source-files` | normal | live verification |
| `14-reporting-analytics-and-model-map-reporting-with-lava` | community-supported | community-supported |
| `14-reporting-analytics-and-model-map-model-map` | community-supported | live verification |
| `15-version-and-release-caveats-fluid-migration` | normal | live verification |
| `15-version-and-release-caveats-v19` | normal | live verification |
| `16-implementation-playbooks-playbook-add-a-safe-read-only-entity-list` | normal | live verification |
| `16-implementation-playbooks-playbook-replace-unsafe-sql-with-parameterized-sql` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-reusable-shortcode` | normal | live verification |
| `16-implementation-playbooks-playbook-diagnose-a-broken-shortcode` | structural | live verification |
| `16-implementation-playbooks-playbook-migrate-dotliquid-lava-to-fluid` | normal | live verification |
| `16-implementation-playbooks-playbook-create-a-lava-webhook` | normal | live verification |
| `16-implementation-playbooks-playbook-add-remote-lava-preview-tooling` | normal | live verification |
| `16-implementation-playbooks-playbook-add-interaction-analytics` | normal | live verification |
| `17-troubleshooting-decision-tree-page-shows-another-person-s-data` | normal | live verification |
| `18-agent-task-recipes-recipe-review-a-shortcode-for-production` | structural | live verification |
| `18-agent-task-recipes-recipe-find-legacy-attribute-lava` | community-supported | live verification |
| `18-agent-task-recipes-recipe-safely-use-securityenabled-false` | normal | live verification |
| `18-agent-task-recipes-recipe-create-a-staff-friendly-link-copy-shortcode` | community-supported | live verification |
| `18-agent-task-recipes-recipe-add-a-translation-shortcode` | community-supported | live verification |
| `18-agent-task-recipes-recipe-generate-labels-with-lava` | normal | live verification |
| `approved-claim-coverage` | normal | live verification |
| `approved-media-coverage` | community-supported | community-supported |
| `19-source-map-and-dependency-notes-release-notes-and-source-code` | normal | live verification |
| `19-source-map-and-dependency-notes-community-pattern-sources` | community-supported | live verification |
