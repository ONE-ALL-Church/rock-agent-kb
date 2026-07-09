---
concept_id: security-permissions
title: Security And Permissions Agent Cheatsheet
generated: true
---

# Security And Permissions Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Answer “Who Has Access To This?”](tasks/recipe-answer-who-has-access-to-this.md) |  |  |
| [Recipe: Answer “Why Was I Denied?”](tasks/recipe-answer-why-was-i-denied.md) |  |  |
| [Recipe: Review A Permission Change Request](tasks/recipe-review-a-permission-change-request.md) |  |  |
| [Recipe: Review A Custom Agent Tool](tasks/recipe-review-a-custom-agent-tool.md) |  |  |
| [Recipe: Review A Public Route](tasks/recipe-review-a-public-route.md) |  |  |
| [Recipe: Review A Security Role](tasks/recipe-review-a-security-role.md) |  |  |
| [Recipe: Review After Upgrade](tasks/recipe-review-after-upgrade.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.5` | core | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to t |
| `17.8` | core | Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules when someone tried to |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | structural | live verification |
| `2-scope-and-terminology-out-of-scope` | structural | live verification |
| `3-security-and-permissions-mental-model-the-actor-layer` | normal | live verification |
| `3-security-and-permissions-mental-model-the-action-layer` | normal | live verification |
| `3-security-and-permissions-mental-model-the-direct-rule-layer` | community-supported | live verification |
| `3-security-and-permissions-mental-model-the-inheritance-layer` | community-supported | live verification |
| `3-security-and-permissions-mental-model-the-cache-layer` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide-medium-authority-sources` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide-lower-authority-but-useful-sources` | community-supported | live verification |
| `4-source-authority-and-how-to-use-this-guide-how-agents-should-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model` | structural | live verification |
| `5-core-configuration-and-data-model-core-configuration-areas` | normal | live verification |
| `5-core-configuration-and-data-model-auth-records` | community-supported | live verification |
| `5-core-configuration-and-data-model-authorization-constants` | normal | live verification |
| `5-core-configuration-and-data-model-security-roles-as-groups` | community-supported | live verification |
| `5-core-configuration-and-data-model-person-user-login-and-account-security` | normal | live verification |
| `5-core-configuration-and-data-model-api-keys-and-purpose` | normal | live verification |
| `5-core-configuration-and-data-model-document-type-and-file-type-security` | normal | live verification |
| `5-core-configuration-and-data-model-workflow-type-security` | normal | live verification |
| `6-primary-entities-and-relationships` | structural | live verification |
| `6-primary-entities-and-relationships-person-userlogin-group-and-security-role` | normal | live verification |
| `6-primary-entities-and-relationships-entitytype-and-securable-entities` | normal | live verification |
| `6-primary-entities-and-relationships-page-site-and-block` | normal | live verification |
| `6-primary-entities-and-relationships-api-endpoints-auth-clients-claims-and-scopes` | normal | live verification |
| `7-common-security-and-permissions-workflows-grant-a-staff-user-access-to-a-page` | normal | live verification |
| `7-common-security-and-permissions-workflows-explain-why-a-user-can-see-a-page` | community-supported | live verification |
| `7-common-security-and-permissions-workflows-create-a-new-security-role` | community-supported | live verification |
| `7-common-security-and-permissions-workflows-remove-access-for-departed-staff` | community-supported | community-supported |
| `7-common-security-and-permissions-workflows-secure-a-custom-block` | normal | live verification |
| `7-common-security-and-permissions-workflows-secure-a-custom-lava-page` | normal | live verification |
| `7-common-security-and-permissions-workflows-secure-a-rest-integration` | normal | live verification |
| `8-authorization-deep-dive-standard-actions` | normal | live verification |
| `8-authorization-deep-dive-allow-and-deny-strategy` | community-supported | live verification |
| `8-authorization-deep-dive-person-specific-permissions` | community-supported | community-supported |
| `8-authorization-deep-dive-page-and-block-security-order` | normal | live verification |
| `8-authorization-deep-dive-entity-parent-authority` | normal | live verification |
| `8-authorization-deep-dive-authorization-cache` | normal | live verification |
| `9-api-auth-deep-dive-legacy-rest-api-authorization` | normal | live verification |
| `9-api-auth-deep-dive-v2-api-pattern` | normal | live verification |
| `9-api-auth-deep-dive-api-keys` | normal | live verification |
| `9-api-auth-deep-dive-mobile-and-tv-app-api-keys` | normal | live verification |
| `9-api-auth-deep-dive-api-auth-troubleshooting` | normal | live verification |
| `10-related-rock-areas-people-groups-api-cms-workflows-people` | community-supported | live verification |
| `10-related-rock-areas-people-groups-api-cms-workflows-api` | normal | live verification |
| `11-administration-and-operational-guardrails-least-privilege` | community-supported | community-supported |
| `11-administration-and-operational-guardrails-sensitive-domain-guardrails` | community-supported | community-supported |
| `11-administration-and-operational-guardrails-temporary-access-and-impersonation` | community-supported | live verification |
| `11-administration-and-operational-guardrails-public-and-anonymous-access` | normal | live verification |
| `11-administration-and-operational-guardrails-security-audits` | community-supported | live verification |
| `12-developer-api-lava-and-source-code-landmarks-rock-security-authorization` | normal | live verification |
| `13-reporting-analytics-and-model-map-reporting-security` | citation-only | live verification |
| `13-reporting-analytics-and-model-map-dynamic-data-and-sql-reports` | community-supported | community-supported |
| `13-reporting-analytics-and-model-map-dataview-api-caveat` | normal | live verification |
| `13-reporting-analytics-and-model-map-model-map-use` | structural | live verification |
| `14-version-and-release-caveats-v14-check-in-manager-delete-attendance-verb` | normal | live verification |
| `14-version-and-release-caveats-v15-fluid-lava-requirement-for-some-community-security-tools` | community-supported | live verification |
| `14-version-and-release-caveats-v16-7-security-cookie-rejection-setting` | citation-only | live verification |
| `14-version-and-release-caveats-v17-5-dataview-endpoint-permission-fix` | normal | live verification |
| `14-version-and-release-caveats-v18-3-and-v19-1-workflow-type-view-hardening-and-document-type-visibility` | normal | live verification |
| `15-implementation-playbooks-playbook-audit-who-can-administrate-a-page` | community-supported | live verification |
| `15-implementation-playbooks-playbook-build-a-staff-only-report-page` | community-supported | live verification |
| `15-implementation-playbooks-playbook-create-a-public-group-finder-safely` | normal | live verification |
| `15-implementation-playbooks-playbook-harden-a-workflow-type` | normal | live verification |
| `15-implementation-playbooks-playbook-review-a-custom-lava-sql-block` | normal | live verification |
| `15-implementation-playbooks-playbook-add-a-v2-api-endpoint` | normal | live verification |
| `15-implementation-playbooks-playbook-review-document-security-after-upgrade` | normal | live verification |
| `16-troubleshooting-decision-tree-user-cannot-see-a-page` | normal | live verification |
| `16-troubleshooting-decision-tree-user-can-see-page-but-not-button` | normal | live verification |
| `16-troubleshooting-decision-tree-user-can-see-too-much-data` | community-supported | community-supported |
| `16-troubleshooting-decision-tree-api-key-gets-permission-denied` | normal | live verification |
| `16-troubleshooting-decision-tree-api-key-works-but-should-not` | normal | live verification |
| `16-troubleshooting-decision-tree-workflow-visible-to-wrong-users` | normal | live verification |
| `16-troubleshooting-decision-tree-document-or-file-visible-to-wrong-users` | normal | live verification |
| `16-troubleshooting-decision-tree-group-finder-shows-private-groups` | normal | live verification |
| `16-troubleshooting-decision-tree-permission-change-did-not-apply` | normal | live verification |
| `17-agent-task-recipes-recipe-answer-who-has-access-to-this` | community-supported | live verification |
| `17-agent-task-recipes-recipe-answer-why-was-i-denied` | normal | live verification |
| `17-agent-task-recipes-recipe-review-a-permission-change-request` | structural | live verification |
| `17-agent-task-recipes-recipe-review-a-public-route` | normal | live verification |
| `17-agent-task-recipes-recipe-review-a-security-role` | community-supported | live verification |
| `approved-claim-coverage` | normal | live verification |
| `18-source-map-and-dependency-notes-primary-source-map` | normal | live verification |
| `18-source-map-and-dependency-notes-dependency-notes-people` | structural | live verification |
| `18-source-map-and-dependency-notes-dependency-notes-groups` | structural | live verification |
| `18-source-map-and-dependency-notes-dependency-notes-api` | structural | live verification |
| `18-source-map-and-dependency-notes-live-verification-requirements` | normal | live verification |
