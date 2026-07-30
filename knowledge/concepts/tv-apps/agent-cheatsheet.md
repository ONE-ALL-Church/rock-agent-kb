---
concept_id: tv-apps
title: TV Apps Agent Cheatsheet
generated: true
---

# TV Apps Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Audit A TV App Configuration](tasks/recipe-audit-a-tv-app-configuration.md) | `Person`, `Page`, `Block`, `Attribute` | `Person`, `Page`, `Block`, `Attribute` |
| [Recipe: Trace A Page GUID](tasks/recipe-trace-a-page-guid.md) | `Device`, `Page` | `Device`, `Page` |
| [Recipe: Validate Remote Auth In Data](tasks/recipe-validate-remote-auth-in-data.md) | `Person`, `PersonAlias`, `Device`, `Page` | `Person`, `PersonAlias`, `Device`, `Page` |
| [Recipe: Review A Roku Page For Focus](tasks/recipe-review-a-roku-page-for-focus.md) | `Group`, `Label`, `Page` | `Group`, `Label`, `Page` |
| [Recipe: Review Apple TV Markup](tasks/recipe-review-apple-tv-markup.md) |  |  |
| [Recipe: Decide Cache Policy](tasks/recipe-decide-cache-policy.md) | `Person`, `Campus`, `Page` | `Person`, `Campus`, `Page` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-tv-apps-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-apple-tv-application-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-roku-application-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-tv-page-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-remote-authentication-data-model` | normal | live verification |
| `6-primary-entities-and-relationships-application-to-page` | normal | live verification |
| `6-primary-entities-and-relationships-application-to-api-key` | normal | live verification |
| `6-primary-entities-and-relationships-remoteauthenticationsession-to-person-and-site` | normal | live verification |
| `6-primary-entities-and-relationships-page-to-interaction` | normal | live verification |
| `7-common-tv-apps-workflows-create-a-new-apple-tv-app` | normal | live verification |
| `7-common-tv-apps-workflows-create-a-new-roku-app` | normal | live verification |
| `7-common-tv-apps-workflows-add-media-playback` | normal | live verification |
| `8-apple-tv-deep-dive-apple-tv-platform-contract` | normal | live verification |
| `8-apple-tv-deep-dive-apple-tv-pages-and-merge-fields` | normal | live verification |
| `8-apple-tv-deep-dive-apple-tv-testing-and-demo-key` | normal | live verification |
| `8-apple-tv-deep-dive-apple-tv-application-images` | normal | live verification |
| `9-roku-deep-dive-roku-pages` | normal | live verification |
| `9-roku-deep-dive-roku-commands` | normal | live verification |
| `10-security-and-authentication-deep-dive-api-key-security` | normal | live verification |
| `10-security-and-authentication-deep-dive-remote-authentication-flow` | normal | live verification |
| `10-security-and-authentication-deep-dive-remote-auth-component-selection` | normal | live verification |
| `11-styling-and-controls-deep-dive-apple-tv-styling` | normal | live verification |
| `11-styling-and-controls-deep-dive-apple-tv-custom-controls` | normal | live verification |
| `11-styling-and-controls-deep-dive-roku-controls` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-mobile-api-integrations` | citation-only | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-mobile-lava` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks` | normal | live verification |
| `15-reporting-analytics-and-model-map` | normal | live verification |
| `16-version-and-release-caveats` | normal | live verification |
| `17-implementation-playbooks-playbook-campus-selection` | normal | live verification |
| `18-troubleshooting-decision-tree-app-does-not-launch-or-shows-wrong-content` | normal | live verification |
| `18-troubleshooting-decision-tree-page-is-blank` | normal | live verification |
| `18-troubleshooting-decision-tree-roku-focus-does-not-move` | normal | live verification |
| `19-agent-task-recipes-recipe-trace-a-page-guid` | structural | live verification |
| `19-agent-task-recipes-recipe-validate-remote-auth-in-data` | normal | live verification |
| `19-agent-task-recipes-recipe-decide-cache-policy` | structural | live verification |
| `approved-claim-coverage` | normal | live verification |
| `20-source-map-and-dependency-notes-release-notes-and-community-examples` | normal | live verification |
