---
concept_id: content-personalization
title: Content And Personalization Agent Cheatsheet
generated: true
---

# Content And Personalization Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Audit a content channel before editing](tasks/recipe-audit-a-content-channel-before-editing.md) |  |  |
| [Recipe: Diagnose “editor cannot see channel in Tools > Content”](tasks/recipe-diagnose-editor-cannot-see-channel-in-tools-content.md) |  |  |
| [Recipe: Diagnose “segment should include this person”](tasks/recipe-diagnose-segment-should-include-this-person.md) |  |  |
| [Recipe: Create safe Lava for channel display](tasks/recipe-create-safe-lava-for-channel-display.md) |  |  |
| [Recipe: Verify content interactions](tasks/recipe-verify-content-interactions.md) |  |  |
| [Recipe: Public launch review for content personalization](tasks/recipe-public-launch-review-for-content-personalization.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.5` | core | Fixed an issue where the Content Channel Item View block and the InteractionContentChannelItemWrite Lava command logged interactions using the Content Channel entity type instead of the Content Channel Item entity type. This caused interact |
| `18.2` | core | Fixed a security issue affecting multiple blocks that interact with Content Channels, where individuals with only View permissions could delete content items. The delete option is now correctly limited to those with Edit access. Fixes: #653 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `3-content-and-personalization-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model` | high | live verification |
| `6-primary-entities-and-relationships` | high | live verification |
| `7-common-content-and-personalization-workflows-create-a-structured-content-channel` | normal | live verification |
| `7-common-content-and-personalization-workflows-publish-a-content-item` | normal | live verification |
| `7-common-content-and-personalization-workflows-display-a-list-of-channel-items` | normal | live verification |
| `7-common-content-and-personalization-workflows-display-a-single-channel-item` | normal | live verification |
| `7-common-content-and-personalization-workflows-aggregate-content-into-a-collection` | normal | live verification |
| `7-common-content-and-personalization-workflows-add-personalization-to-channel-items` | normal | live verification |
| `8-content-channels-deep-dive-channel-configuration` | needs-citation | live verification |
| `8-content-channels-deep-dive-display-and-lava` | normal | live verification |
| `8-content-channels-deep-dive-security` | high | live verification |
| `9-asset-manager-deep-dive-viewing-and-managing-assets` | high | live verification |
| `9-asset-manager-deep-dive-storage-provider-setup` | normal | live verification |
| `9-asset-manager-deep-dive-image-and-file-performance` | normal | live verification |
| `9-asset-manager-deep-dive-structured-content-file-behavior` | normal | live verification |
| `10-adaptive-messages-deep-dive-when-to-use-adaptive-messages` | needs-citation | needs-citation |
| `10-adaptive-messages-deep-dive-setup-model` | normal | live verification |
| `10-adaptive-messages-deep-dive-entity-and-api-landmarks` | normal | live verification |
| `10-adaptive-messages-deep-dive-troubleshooting-adaptive-messages` | needs-citation | live verification |
| `11-personalization-and-segments-deep-dive-site-level-prerequisites` | normal | live verification |
| `11-personalization-and-segments-deep-dive-segment-types` | normal | live verification |
| `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-lava` | normal | live verification |
| `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-security` | high | live verification |
| `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-communications` | normal | live verification |
| `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-media` | high | live verification |
| `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-workflows` | normal | live verification |
| `12-related-rock-areas-cms-lava-security-communications-media-workflows-people-people` | structural | live verification |
| `13-administration-and-operational-guardrails-change-management` | structural | live verification |
| `13-administration-and-operational-guardrails-job-monitoring` | normal | live verification |
| `13-administration-and-operational-guardrails-cache-and-indexing` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-rest-and-model-landmarks` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-content-channel-item-personal-list-lava-block` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-interaction-logging` | normal | live verification |
| `15-reporting-analytics-and-model-map-content-item-reporting` | needs-citation | live verification |
| `15-reporting-analytics-and-model-map-content-collection-analytics` | normal | live verification |
| `15-reporting-analytics-and-model-map-personalization-reporting` | normal | live verification |
| `16-version-and-release-caveats` | normal | live verification |
| `17-implementation-playbooks-playbook-build-a-ministry-resource-library` | normal | live verification |
| `17-implementation-playbooks-playbook-convert-html-heavy-channel-items-to-structured-content` | citation-only | live verification |
| `17-implementation-playbooks-playbook-add-personalized-homepage-promos` | normal | live verification |
| `17-implementation-playbooks-playbook-use-adaptive-messages-for-giving-campaign-variants` | normal | live verification |
| `17-implementation-playbooks-playbook-publish-sermon-media-through-content-channel-items` | high | live verification |
| `17-implementation-playbooks-playbook-configure-rss-feed-for-a-content-channel` | normal | live verification |
| `18-troubleshooting-decision-tree-content-item-is-missing-from-a-page` | needs-citation | needs-citation |
| `18-troubleshooting-decision-tree-asset-image-does-not-display` | needs-citation | needs-citation |
| `19-agent-task-recipes-recipe-diagnose-segment-should-include-this-person` | structural | live verification |
| `19-agent-task-recipes-recipe-create-safe-lava-for-channel-display` | high | live verification |
| `19-agent-task-recipes-recipe-public-launch-review-for-content-personalization` | structural | live verification |
