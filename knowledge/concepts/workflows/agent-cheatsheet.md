---
concept_id: workflows
title: Workflows Agent Cheatsheet
generated: true
---

# Workflows Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Find Every Launch Path For A Workflow Type](tasks/recipe-find-every-launch-path-for-a-workflow-type.md) |  |  |
| [Recipe: Explain A Workflow To A Staff Owner](tasks/recipe-explain-a-workflow-to-a-staff-owner.md) |  |  |
| [Recipe: Diagnose A Missing Submission](tasks/recipe-diagnose-a-missing-submission.md) |  |  |
| [Recipe: Safely Retire A Workflow](tasks/recipe-safely-retire-a-workflow.md) |  |  |
| [Recipe: Build A Workflow Health Dashboard](tasks/recipe-build-a-workflow-health-dashboard.md) |  |  |
| [Recipe: Validate Person Entry Configuration](tasks/recipe-validate-person-entry-configuration.md) |  |  |
| [Recipe: Audit `workflowactivate` Lava](tasks/recipe-audit-workflowactivate-lava.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-workflows-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-workflow-type-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-workflow-attributes` | community-supported | community-supported |
| `5-core-configuration-and-data-model-workflow-forms` | normal | live verification |
| `5-core-configuration-and-data-model-persistence-and-processing` | normal | live verification |
| `6-primary-entities-and-relationships` | high | live verification |
| `7-common-workflows-workflows-request-intake-workflow` | community-supported | community-supported |
| `7-common-workflows-workflows-event-call-to-action-workflow` | community-supported | live verification |
| `7-common-workflows-workflows-staff-approval-workflow` | community-supported | community-supported |
| `7-common-workflows-workflows-helper-workflow` | community-supported | live verification |
| `7-common-workflows-workflows-grid-launched-workflow` | community-supported | community-supported |
| `7-common-workflows-workflows-webhook-to-workflow-integration` | community-supported | community-supported |
| `7-common-workflows-workflows-electronic-signature-workflow` | community-supported | community-supported |
| `7-common-workflows-workflows-bulk-creation-workflow` | community-supported | community-supported |
| `7-common-workflows-workflows-finance-or-contribution-workflow` | community-supported | live verification |
| `8-triggers-and-activation-deep-dive-workflow-entry-activation` | normal | live verification |
| `8-triggers-and-activation-deep-dive-entity-triggers` | normal | live verification |
| `8-triggers-and-activation-deep-dive-lava-workflowactivate` | normal | live verification |
| `8-triggers-and-activation-deep-dive-webhook-activation` | community-supported | community-supported |
| `8-triggers-and-activation-deep-dive-grid-activation` | community-supported | community-supported |
| `8-triggers-and-activation-deep-dive-connection-step-group-and-requirement-activation` | community-supported | live verification |
| `9-workflow-forms-deep-dive-form-design-principles` | normal | live verification |
| `9-workflow-forms-deep-dive-conditional-logic` | normal | live verification |
| `9-workflow-forms-deep-dive-person-entry` | high | live verification |
| `9-workflow-forms-deep-dive-campus-selection-and-inactive-campuses` | normal | live verification |
| `9-workflow-forms-deep-dive-modal-workflow-entry` | community-supported | live verification |
| `10-workflow-integrations-deep-dive-outbound-webhooks-and-zapier` | community-supported | live verification |
| `10-workflow-integrations-deep-dive-inbound-webhooks` | community-supported | live verification |
| `10-workflow-integrations-deep-dive-communications` | community-supported | community-supported |
| `10-workflow-integrations-deep-dive-connections` | community-supported | community-supported |
| `10-workflow-integrations-deep-dive-groups-and-group-member-attributes` | community-supported | community-supported |
| `11-related-rock-areas-lava-jobs-communications-security-attributes-lava` | normal | live verification |
| `11-related-rock-areas-lava-jobs-communications-security-attributes-jobs` | community-supported | community-supported |
| `11-related-rock-areas-lava-jobs-communications-security-attributes-communications` | structural | live verification |
| `11-related-rock-areas-lava-jobs-communications-security-attributes-security` | normal | live verification |
| `11-related-rock-areas-lava-jobs-communications-security-attributes-attributes` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-naming-standards` | structural | live verification |
| `12-administration-and-operational-guardrails-change-management` | normal | live verification |
| `12-administration-and-operational-guardrails-where-used-audits` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-active-workflow-hygiene` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-maximum-age-and-auto-completion` | normal | live verification |
| `12-administration-and-operational-guardrails-public-form-guardrails` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-lava-command-source` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-deprecated-activate-workflow-block` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-person-entry-source` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-api-and-data-access` | normal | live verification |
| `14-reporting-analytics-and-model-map-what-to-report` | community-supported | community-supported |
| `14-reporting-analytics-and-model-map-model-map-use` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-reporting-caveats` | community-supported | live verification |
| `14-reporting-analytics-and-model-map-health-metrics` | community-supported | live verification |
| `15-version-and-release-caveats` | high | live verification |
| `16-implementation-playbooks-playbook-build-a-public-intake-workflow` | citation-only | live verification |
| `16-implementation-playbooks-playbook-add-a-workflow-to-a-grid` | community-supported | live verification |
| `16-implementation-playbooks-playbook-create-a-helper-workflow` | community-supported | live verification |
| `16-implementation-playbooks-playbook-replace-deprecated-activate-workflow-block` | normal | live verification |
| `16-implementation-playbooks-playbook-build-webhook-to-workflow` | community-supported | live verification |
| `16-implementation-playbooks-playbook-audit-a-workflow-before-editing` | community-supported | live verification |
| `17-troubleshooting-decision-tree-workflow-did-not-start` | normal | live verification |
| `17-troubleshooting-decision-tree-person-entry-creates-duplicates` | normal | live verification |
| `17-troubleshooting-decision-tree-workflow-is-stuck-active` | community-supported | community-supported |
| `17-troubleshooting-decision-tree-webhook-workflow-is-slow` | community-supported | community-supported |
| `18-agent-task-recipes-recipe-find-every-launch-path-for-a-workflow-type` | community-supported | live verification |
| `18-agent-task-recipes-recipe-diagnose-a-missing-submission` | structural | live verification |
| `18-agent-task-recipes-recipe-build-a-workflow-health-dashboard` | community-supported | community-supported |
| `18-agent-task-recipes-recipe-validate-person-entry-configuration` | normal | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `19-source-map-and-dependency-notes` | high | live verification |
