---
concept_id: apple-tv
title: Apple TV Apps Agent Cheatsheet
generated: true
---

# Apple TV Apps Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Inspect An Existing Apple TV App](tasks/recipe-inspect-an-existing-apple-tv-app.md) |  |  |
| [Recipe: Diagnose A Broken Button](tasks/recipe-diagnose-a-broken-button.md) |  |  |
| [Recipe: Add A New Page Safely](tasks/recipe-add-a-new-page-safely.md) |  |  |
| [Recipe: Review For Security](tasks/recipe-review-for-security.md) |  |  |
| [Recipe: Review For Performance](tasks/recipe-review-for-performance.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-apple-tv-apps-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-apple-tv-app-record` | normal | live verification |
| `5-core-configuration-and-data-model-tv-page-record` | normal | live verification |
| `5-core-configuration-and-data-model-page-list-block-options` | normal | live verification |
| `5-core-configuration-and-data-model-remote-authentication-data-model` | normal | live verification |
| `5-core-configuration-and-data-model-lava-endpoint-and-api-context` | normal | live verification |
| `6-primary-entities-and-relationships-apple-tv-app-to-site` | normal | live verification |
| `6-primary-entities-and-relationships-apple-tv-app-to-tv-pages` | normal | live verification |
| `6-primary-entities-and-relationships-tv-pages-to-lava-merge-fields` | normal | live verification |
| `6-primary-entities-and-relationships-tv-pages-to-commands` | normal | live verification |
| `7-common-apple-tv-apps-workflows-create-a-new-app` | normal | live verification |
| `7-common-apple-tv-apps-workflows-add-a-content-page` | normal | live verification |
| `7-common-apple-tv-apps-workflows-build-a-campus-selector` | normal | live verification |
| `7-common-apple-tv-apps-workflows-add-login` | normal | live verification |
| `7-common-apple-tv-apps-workflows-play-media` | normal | live verification |
| `8-building-your-first-apple-tv-app-deep-dive-step-1-confirm-preconditions` | normal | live verification |
| `8-building-your-first-apple-tv-app-deep-dive-step-2-create-the-app` | normal | live verification |
| `8-building-your-first-apple-tv-app-deep-dive-step-3-create-the-start-screen` | normal | live verification |
| `8-building-your-first-apple-tv-app-deep-dive-step-6-add-images` | normal | live verification |
| `8-building-your-first-apple-tv-app-deep-dive-step-7-test-the-app` | normal | live verification |
| `9-apple-tv-sign-in-and-authentication-deep-dive-server-setup` | normal | live verification |
| `9-apple-tv-sign-in-and-authentication-deep-dive-security-guardrails` | normal | live verification |
| `10-apple-tv-javascript-commands-deep-dive-navigation-commands` | normal | live verification |
| `10-apple-tv-javascript-commands-deep-dive-media-commands` | normal | live verification |
| `10-apple-tv-javascript-commands-deep-dive-personal-commands` | normal | live verification |
| `10-apple-tv-javascript-commands-deep-dive-utility-commands` | normal | live verification |
| `10-apple-tv-javascript-commands-deep-dive-demo-commands` | normal | live verification |
| `11-apple-tv-styling-deep-dive` | normal | live verification |
| `11-apple-tv-styling-deep-dive-style-placement` | structural | live verification |
| `11-apple-tv-styling-deep-dive-global-styles` | normal | live verification |
| `11-apple-tv-styling-deep-dive-themes-and-media-queries` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-lava` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-cms` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-media` | normal | live verification |
| `13-administration-and-operational-guardrails-environment-separation` | structural | live verification |
| `13-administration-and-operational-guardrails-api-key-hygiene` | structural | live verification |
| `13-administration-and-operational-guardrails-release-gate` | structural | live verification |
| `15-reporting-analytics-and-model-map` | normal | live verification |
| `16-version-and-release-caveats` | normal | live verification |
| `17-implementation-playbooks-playbook-weekend-messages-app` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-campus-aware-app` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-remote-login` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-media-resume` | structural | live verification |
| `18-troubleshooting-decision-tree-navigation-does-not-work` | normal | live verification |
| `18-troubleshooting-decision-tree-styles-do-not-apply` | structural | live verification |
| `19-agent-task-recipes-recipe-diagnose-a-broken-button` | structural | live verification |
| `19-agent-task-recipes-recipe-add-a-new-page-safely` | structural | live verification |
| `19-agent-task-recipes-recipe-review-for-security` | structural | live verification |
| `19-agent-task-recipes-recipe-review-for-performance` | structural | live verification |
| `approved-claim-coverage` | normal | live verification |
| `20-source-map-and-dependency-notes-release-notes-and-community-examples` | normal | live verification |
