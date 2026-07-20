---
concept_id: event-registration
title: Event Registration Agent Cheatsheet
generated: true
---

# Event Registration Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Summarize A Registration Instance](tasks/recipe-summarize-a-registration-instance.md) |  |  |
| [Recipe: Verify A Public Registration URL](tasks/recipe-verify-a-public-registration-url.md) |  |  |
| [Recipe: Audit Payment Risk](tasks/recipe-audit-payment-risk.md) |  |  |
| [Recipe: Audit Discount Codes](tasks/recipe-audit-discount-codes.md) |  |  |
| [Recipe: Audit Wait List](tasks/recipe-audit-wait-list.md) |  |  |
| [Recipe: Build A Registrant Packet Export](tasks/recipe-build-a-registrant-packet-export.md) |  |  |
| [Recipe: Add Staff Notes To Registration Detail](tasks/recipe-add-staff-notes-to-registration-detail.md) |  |  |
| [Recipe: Investigate API Registration URL Issues](tasks/recipe-investigate-api-registration-url-issues.md) |  |  |

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
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant without a valid Signatur |
| `19.1` | core | Added a Prevent Duplicate Registrants setting to the Registration Template that prevents the same person record from registering for the same Registration Instance more than once. When enabled, the Registration Entry Block checks for existi |
| `19.1` | core | Added Registrant eligibility rules to the Registration Template Detail Block and updated the Registration Entry Block to prevent incorrect family member registrations. Added new "Registrant Eligibility" settings to the Registration Template |
| `19.1` | core | Fixed an issue in the Registration Instance Registration List block where the Discount Code column on the Registrations tab was hidden when the registration template had no per-registrant cost, even if a discount code was applied to fees on |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-event-registration-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-configuration-surfaces` | high | live verification |
| `5-core-configuration-and-data-model-data-model-orientation` | community-supported | live verification |
| `6-primary-entities-and-relationships-registration-template` | community-supported | community-supported |
| `6-primary-entities-and-relationships-registration` | normal | live verification |
| `6-primary-entities-and-relationships-registrationregistrant` | normal | live verification |
| `6-primary-entities-and-relationships-event-item-occurrence-and-linkage` | normal | live verification |
| `6-primary-entities-and-relationships-attributes-and-form-fields` | normal | live verification |
| `7-common-event-registration-workflows-paid-registration` | citation-only | live verification |
| `7-common-event-registration-workflows-wait-list-registration` | normal | live verification |
| `7-common-event-registration-workflows-group-placement` | normal | live verification |
| `8-registration-instances-deep-dive-instance-identity` | normal | live verification |
| `8-registration-instances-deep-dive-active-and-date-windows` | structural | live verification |
| `8-registration-instances-deep-dive-capacity-and-spots` | community-supported | community-supported |
| `8-registration-instances-deep-dive-url-slug-and-public-linkage` | normal | live verification |
| `8-registration-instances-deep-dive-attributes` | citation-only | live verification |
| `9-payments-deep-dive-partial-payments` | normal | live verification |
| `9-payments-deep-dive-payment-plans` | normal | live verification |
| `9-payments-deep-dive-payment-gateways-and-saved-accounts` | citation-only | live verification |
| `10-related-rock-areas-events-finance-workflows-communications-groups-finance` | community-supported | community-supported |
| `10-related-rock-areas-events-finance-workflows-communications-groups-workflows` | community-supported | community-supported |
| `11-administration-and-operational-guardrails-naming` | community-supported | live verification |
| `11-administration-and-operational-guardrails-change-management` | structural | live verification |
| `11-administration-and-operational-guardrails-notes-and-auditability` | community-supported | community-supported |
| `11-administration-and-operational-guardrails-operational-health-checks` | normal | live verification |
| `12-developer-api-lava-and-source-code-landmarks-public-mobile-event-occurrence-rendering` | normal | live verification |
| `12-developer-api-lava-and-source-code-landmarks-api-linkage-caveat` | community-supported | live verification |
| `13-reporting-analytics-and-model-map-reporting-entity-choice` | community-supported | community-supported |
| `13-reporting-analytics-and-model-map-model-map-verification` | community-supported | live verification |
| `13-reporting-analytics-and-model-map-analytics-checks` | community-supported | community-supported |
| `14-version-and-release-caveats-rock-18-3` | normal | live verification |
| `14-version-and-release-caveats-v16-10-v17-0-spotlight` | citation-only | live verification |
| `15-implementation-playbooks-playbook-a-create-a-standard-paid-event-registration` | citation-only | live verification |
| `15-implementation-playbooks-playbook-b-add-eligibility-rules-in-v19-1` | normal | live verification |
| `15-implementation-playbooks-playbook-c-prevent-duplicate-registrants-in-v19-1` | structural | live verification |
| `15-implementation-playbooks-playbook-d-configure-payment-reminders` | high | live verification |
| `15-implementation-playbooks-playbook-e-diagnose-a-missing-public-registration-button` | structural | live verification |
| `16-troubleshooting-decision-tree-public-page-says-registration-is-closed` | structural | live verification |
| `17-agent-task-recipes-recipe-verify-a-public-registration-url` | structural | live verification |
| `17-agent-task-recipes-recipe-audit-payment-risk` | structural | live verification |
| `17-agent-task-recipes-recipe-audit-discount-codes` | structural | live verification |
| `17-agent-task-recipes-recipe-audit-wait-list` | structural | live verification |
| `17-agent-task-recipes-recipe-build-a-registrant-packet-export` | community-supported | community-supported |
| `17-agent-task-recipes-recipe-add-staff-notes-to-registration-detail` | community-supported | live verification |
| `17-agent-task-recipes-recipe-investigate-api-registration-url-issues` | community-supported | live verification |
| `approved-claim-coverage` | normal | live verification |
| `18-source-map-and-dependency-notes` | high | live verification |
