---
concept_id: developer-resources
title: Rock Developer Resources Agent Cheatsheet
generated: true
---

# Rock Developer Resources Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Answer "Where is this configured?"](tasks/recipe-answer-where-is-this-configured.md) |  |  |
| [Recipe: Review a Rock PR](tasks/recipe-review-a-rock-pr.md) |  |  |
| [Recipe: Diagnose "Works for admin but not staff"](tasks/recipe-diagnose-works-for-admin-but-not-staff.md) |  |  |
| [Recipe: Build a source-backed answer](tasks/recipe-build-a-source-backed-answer.md) |  |  |
| [Recipe: Build a Rock agent tool](tasks/recipe-build-a-rock-agent-tool.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DefinedType` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.2` | core | Fixed an issue that caused the wrong theme type to be displayed after cloning a theme until the Rock server rebooted. Fixes: #6603 |
| `17.1` | core | Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-rock-developer-resources-mental-model-layer-1-platform-and-runtime` | normal | live verification |
| `3-rock-developer-resources-mental-model-layer-3-data-model-and-persistence` | normal | live verification |
| `3-rock-developer-resources-mental-model-layer-5-release-and-branch-reality` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-pages-layouts-sites-and-blocks` | normal | live verification |
| `5-core-configuration-and-data-model-attributes-and-defined-values` | normal | live verification |
| `5-core-configuration-and-data-model-custom-entities-and-services` | normal | live verification |
| `5-core-configuration-and-data-model-lava-applications-and-lava-endpoints` | normal | live verification |
| `6-primary-entities-and-relationships` | structural | live verification |
| `6-primary-entities-and-relationships-page-block-and-block-type` | normal | live verification |
| `6-primary-entities-and-relationships-person-and-personalias` | normal | live verification |
| `6-primary-entities-and-relationships-attribute-attributevalue-definedtype-definedvalue` | normal | live verification |
| `6-primary-entities-and-relationships-workflow-and-workflow-actions` | normal | live verification |
| `6-primary-entities-and-relationships-lavaapplication-and-lavaendpoint` | normal | live verification |
| `6-primary-entities-and-relationships-interaction-and-analytics` | normal | live verification |
| `6-primary-entities-and-relationships-theme` | normal | live verification |
| `7-common-rock-developer-resources-workflows-choose-the-correct-developer-path` | needs-citation | needs-citation |
| `7-common-rock-developer-resources-workflows-package-and-deploy-a-plugin-or-theme` | normal | live verification |
| `7-common-rock-developer-resources-workflows-diagnose-a-broken-developer-feature` | needs-citation | live verification |
| `8-developer-codex-deep-dive` | normal | live verification |
| `8-developer-codex-deep-dive-code-generator-and-model-changes` | normal | live verification |
| `8-developer-codex-deep-dive-obsidian-chop-swap-sneak` | normal | live verification |
| `8-developer-codex-deep-dive-testing-and-peer-review` | normal | live verification |
| `9-developer-101-launchpad-deep-dive-operational-pattern` | needs-citation | live verification |
| `9-developer-101-launchpad-deep-dive-personalias-vs-person` | structural | live verification |
| `9-developer-101-launchpad-deep-dive-security` | normal | live verification |
| `10-developer-202-ignition-deep-dive-migrations-in-202` | normal | live verification |
| `10-developer-202-ignition-deep-dive-data-migration-helper-methods` | normal | live verification |
| `10-developer-202-ignition-deep-dive-agent-cautions` | structural | live verification |
| `11-developer-303-blast-off-deep-dive-data-view-filters-and-dynamic-linq` | normal | live verification |
| `11-developer-303-blast-off-deep-dive-rest-api` | citation-only | live verification |
| `12-obsidian-deep-dive-detail-blocks` | normal | live verification |
| `12-obsidian-deep-dive-grids` | normal | live verification |
| `12-obsidian-deep-dive-field-types-and-ui-controls` | normal | live verification |
| `13-helix-deep-dive-plugin-vs-core-status` | normal | live verification |
| `13-helix-deep-dive-lava-applications` | normal | live verification |
| `13-helix-deep-dive-lava-endpoints` | normal | live verification |
| `14-ai-agents-deep-dive-lava-tools-vs-native-tools` | needs-citation | needs-citation |
| `14-ai-agents-deep-dive-live-verification` | structural | live verification |
| `15-mobile-docs-deep-dive-mobile-block-categories` | normal | live verification |
| `15-mobile-docs-deep-dive-controls-and-styling` | normal | live verification |
| `16-tv-app-docs-deep-dive-apple-tv` | normal | live verification |
| `17-packaging-plugins-and-themes-deep-dive` | normal | live verification |
| `18-quickstart-tutorials-deep-dive-environment-setup` | normal | live verification |
| `19-slingshot-migration-deep-dive-source-system-specifics` | normal | live verification |
| `20-utility-and-reference-pages-deep-dive-dynamic-linq-syntax` | normal | live verification |
| `20-utility-and-reference-pages-deep-dive-sql-style-guide` | normal | live verification |
| `20-utility-and-reference-pages-deep-dive-design-system` | normal | live verification |
| `21-related-rock-areas-api-integrations-lava-helix-obsidian-mobile-plugins-themes-migration-security-cms-tv-apps-api-integrations` | citation-only | live verification |
| `21-related-rock-areas-api-integrations-lava-helix-obsidian-mobile-plugins-themes-migration-security-cms-tv-apps-mobile` | normal | live verification |
| `21-related-rock-areas-api-integrations-lava-helix-obsidian-mobile-plugins-themes-migration-security-cms-tv-apps-plugins-and-themes` | normal | live verification |
| `22-administration-and-operational-guardrails-version-guardrails` | normal | live verification |
| `22-administration-and-operational-guardrails-data-guardrails` | structural | live verification |
| `22-administration-and-operational-guardrails-migration-guardrails` | structural | live verification |
| `22-administration-and-operational-guardrails-ui-guardrails` | structural | live verification |
| `24-reporting-analytics-and-model-map-model-map` | normal | live verification |
| `24-reporting-analytics-and-model-map-realtime-visualization` | normal | live verification |
| `25-version-and-release-caveats-draft-and-work-in-progress-docs` | normal | live verification |
| `25-version-and-release-caveats-rock-v16` | normal | live verification |
| `25-version-and-release-caveats-branch-caveat` | normal | live verification |
| `26-implementation-playbooks-playbook-add-a-new-configurable-block-setting` | normal | live verification |
| `26-implementation-playbooks-playbook-build-a-safe-lava-endpoint` | normal | live verification |
| `26-implementation-playbooks-playbook-replace-a-webforms-block-with-obsidian` | normal | live verification |
| `26-implementation-playbooks-playbook-create-a-custom-entity-plugin-data-model` | normal | live verification |
| `26-implementation-playbooks-playbook-build-a-roku-page` | normal | live verification |
| `26-implementation-playbooks-playbook-build-an-apple-tv-app-page` | normal | live verification |
| `27-troubleshooting-decision-tree-the-block-does-not-render` | needs-citation | needs-citation |
| `27-troubleshooting-decision-tree-the-obsidian-block-renders-but-actions-fail` | normal | live verification |
| `27-troubleshooting-decision-tree-the-migration-failed` | normal | live verification |
| `27-troubleshooting-decision-tree-the-tv-app-page-is-blank` | normal | live verification |
| `28-agent-task-recipes-recipe-answer-where-is-this-configured` | structural | live verification |
| `28-agent-task-recipes-recipe-review-a-rock-pr` | normal | live verification |
| `28-agent-task-recipes-recipe-diagnose-works-for-admin-but-not-staff` | normal | live verification |
| `28-agent-task-recipes-recipe-build-a-rock-agent-tool` | normal | live verification |
| `approved-claim-coverage` | normal | live verification |
| `29-source-map-and-dependency-notes-community-examples-and-q-a` | community-supported | live verification |
| `29-source-map-and-dependency-notes-official-developer-docs` | normal | live verification |
| `29-source-map-and-dependency-notes-dependency-notes` | needs-citation | live verification |
