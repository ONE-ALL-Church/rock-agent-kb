---
concept_id: giving-finance
title: Giving And Finance Agent Cheatsheet
generated: true
---

# Giving And Finance Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Read-Only Finance Record Inspection](tasks/recipe-read-only-finance-record-inspection.md) |  |  |
| [Recipe: Statement Eligibility Explanation](tasks/recipe-statement-eligibility-explanation.md) |  |  |
| [Recipe: Safe Account Cleanup Assessment](tasks/recipe-safe-account-cleanup-assessment.md) |  |  |
| [Recipe: Giving Automation Review](tasks/recipe-giving-automation-review.md) |  |  |
| [Recipe: Pledge Progress Analysis](tasks/recipe-pledge-progress-analysis.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added Financial Batch Detail block to support check scanning, creation of batch, batch detail viewing, and batch modifications. Also added Financial Batch List to view available batches. |
| `18.3` | core | Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup parameter) was excl |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-financial-accounts` | normal | live verification |
| `5-core-configuration-and-data-model-financial-gateways` | high | live verification |
| `5-core-configuration-and-data-model-blocks-and-pages` | normal | live verification |
| `6-primary-entities-and-relationships-batches-and-transactions` | high | live verification |
| `6-primary-entities-and-relationships-scheduled-transactions-and-payment-plans` | normal | live verification |
| `6-primary-entities-and-relationships-pledges` | normal | live verification |
| `6-primary-entities-and-relationships-people-personalias-businesses-families-and-giving-units` | normal | live verification |
| `7-common-giving-and-finance-workflows-text-giving` | normal | live verification |
| `7-common-giving-and-finance-workflows-manual-entry-and-check-processing` | high | live verification |
| `7-common-giving-and-finance-workflows-external-giving-imports` | community-supported | live verification |
| `8-transactions-deep-dive-transaction-dates` | normal | live verification |
| `8-transactions-deep-dive-transaction-types` | normal | live verification |
| `8-transactions-deep-dive-transaction-attributes` | community-supported | community-supported |
| `8-transactions-deep-dive-transaction-security` | normal | live verification |
| `9-statements-deep-dive-statement-recipients` | normal | live verification |
| `9-statements-deep-dive-statement-eligibility` | normal | live verification |
| `9-statements-deep-dive-receipts-vs-statements` | community-supported | community-supported |
| `10-batches-deep-dive-batch-fields-to-inspect` | normal | live verification |
| `10-batches-deep-dive-automated-batches` | normal | live verification |
| `10-batches-deep-dive-check-scanning-and-mobile-batch-processing` | normal | live verification |
| `11-related-rock-areas-people-groups-workflows-security-reporting-people` | structural | live verification |
| `11-related-rock-areas-people-groups-workflows-security-reporting-groups` | normal | live verification |
| `11-related-rock-areas-people-groups-workflows-security-reporting-workflows` | community-supported | live verification |
| `11-related-rock-areas-people-groups-workflows-security-reporting-reporting` | citation-only | live verification |
| `12-administration-and-operational-guardrails-change-control` | structural | live verification |
| `12-administration-and-operational-guardrails-account-governance` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-gateway-governance` | normal | live verification |
| `12-administration-and-operational-guardrails-receipt-and-statement-controls` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-api-considerations` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-lava-considerations` | community-supported | live verification |
| `13-developer-api-lava-and-source-code-landmarks-mobile-developer-landmarks` | normal | live verification |
| `14-reporting-analytics-and-model-map-giving-analytics` | normal | live verification |
| `14-reporting-analytics-and-model-map-bi-financial-transaction-reporting` | citation-only | live verification |
| `15-version-and-release-caveats` | high | live verification |
| `16-implementation-playbooks-playbook-add-a-new-giving-account` | normal | live verification |
| `16-implementation-playbooks-playbook-configure-online-giving` | structural | live verification |
| `16-implementation-playbooks-playbook-enable-mobile-batch-check-scanning` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-giving-analytics-report` | citation-only | live verification |
| `16-implementation-playbooks-playbook-import-giving-from-an-external-system` | community-supported | live verification |
| `17-troubleshooting-decision-tree-recurring-gift-did-not-run` | normal | live verification |
| `17-troubleshooting-decision-tree-receipt-language-is-wrong` | normal | live verification |
| `18-agent-task-recipes-recipe-read-only-finance-record-inspection` | structural | live verification |
| `18-agent-task-recipes-recipe-statement-eligibility-explanation` | structural | live verification |
| `18-agent-task-recipes-recipe-safe-account-cleanup-assessment` | structural | live verification |
| `18-agent-task-recipes-recipe-giving-automation-review` | community-supported | live verification |
| `18-agent-task-recipes-recipe-pledge-progress-analysis` | community-supported | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `19-source-map-and-dependency-notes` | high | live verification |
