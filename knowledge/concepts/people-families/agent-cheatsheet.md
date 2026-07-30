---
concept_id: people-families
title: People And Families Agent Cheatsheet
generated: true
---

# People And Families Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Identify A Person Safely](tasks/recipe-identify-a-person-safely.md) | `Attendance`, `Person`, `PersonAlias`, `Group`, `Family`, `Workflow` | `Attendance`, `Person`, `PersonAlias`, `Group`, `Family`, `Workflow` |
| [Recipe: Inspect A Person Attribute](tasks/recipe-inspect-a-person-attribute.md) | `Attribute` | `Attribute` |
| [Recipe: Determine If A Value Is Person Id Or Alias Guid](tasks/recipe-determine-if-a-value-is-person-id-or-alias-guid.md) | `Person`, `PersonAlias`, `Workflow`, `Attribute` | `Person`, `PersonAlias`, `Workflow`, `Attribute` |
| [Recipe: Audit A Family For Check-In](tasks/recipe-audit-a-family-for-check-in.md) | `Group`, `GroupType`, `Location`, `Schedule`, `Check-in Configuration`, `Family`, `Workflow`, `Attribute` | `Group`, `GroupType`, `Location`, `Schedule`, `Check-in Configuration`, `Family`, `Workflow`, `Attribute` |
| [Recipe: Review A Person Profile Customization](tasks/recipe-review-a-person-profile-customization.md) | `Person`, `Workflow`, `Page`, `Block`, `Attribute` | `Person`, `Workflow`, `Page`, `Block`, `Attribute` |
| [Recipe: Triage An Accidental Merge](tasks/recipe-triage-an-accidental-merge.md) | `Attendance`, `Person`, `Group`, `Workflow`, `Attribute` | `Attendance`, `Person`, `Group`, `Workflow`, `Attribute` |
| [Recipe: Track New Record Source](tasks/recipe-track-new-record-source.md) | `Person`, `Family`, `Workflow`, `Attribute` | `Person`, `Family`, `Workflow`, `Attribute` |
| [Recipe: Build A Staff Directory From Person Attributes](tasks/recipe-build-a-staff-directory-from-person-attributes.md) | `Person`, `Page`, `Attribute` | `Person`, `Page`, `Attribute` |
| [Recipe: Add A Bookmarked Groups-Like Profile Panel](tasks/recipe-add-a-bookmarked-groups-like-profile-panel.md) | `Person`, `Group` | `Person`, `Group` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup parameter) was excl |
| `18.2` | core | Fixed an issue where the Attribute Editor did not correctly save configuration changes when creating an Attribute designed to store other Attributes (e.g., an Attribute of type Attribute). This affected scenarios such as defining filters in |
| `18.1` | core | Improved the Person Record Source feature by adding support for setting a Record Source within the Get Person From Fields Workflow Action and the internal Add Family page. Also added a configuration option to define a default Record Source  |
| `19.1` | core | Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729 |
| `19.1` | core | Added Registrant eligibility rules to the Registration Template Detail Block and updated the Registration Entry Block to prevent incorrect family member registrations. Added new "Registrant Eligibility" settings to the Registration Template |
| `19.1` | core | Fixed an issue where editing an Event Occurrence Attribute on the Event Item Detail block would incorrectly reject the attribute key value with a validation error, preventing the attribute from being saved. |
| `18.2` | core | Fixed an issue where submitting a registration would disable an individual's SMS setting when the "Show SMS Opt-In" option on the Registration Template was set to False. The registration process will now preserve the individual's existing S |
| `18.2` | core | Fixed an issue where creating a Benevolence Request from a Person Profile did not automatically associate the current person, requiring the individual to be manually selected after the request was created. Fixes: #6631 |
| `18.1` | core | Fixed an issue where the Statement Generator failed to create statements for a Single Individual if a Data View had been used previously and the person wasn’t part of that view. Statements now generate correctly for any selected individual. |
| `18.1` | core | Fixed an issue in the Obsidian Workflow Entry block related to Person Entry. It will now correctly set the Person and Spouse attributes if 'Hide if Current Person Known' is enabled. Fixes: #6568 |
| `18.1` | core | Fixed an issue in the Obsidian Workflow Entry block so it no longer creates a blank Person record for spouse in some situations. This could happen if a non-logged in person filled out a Person Entry form and left Spouse blank. Fixes: #6420 |
| `17.5` | core | Fixed error that prevented removing an individual with a 'Can Check-In' known relationship when using specific configuration options. If a single relationship type was configured for 'can check-in' then trying to remove somebody at a kiosk  |
| `17.2` | core | Fixed an issue where new adults added to an existing family through the Family Registration block were incorrectly set to Individual Giving instead of Combined Giving. Fixes: #6358 |
| `17.1` | core | Fixed an issue that prevented Next-Gen Check-In from sorting families alphabetically by name like the legacy Check-In system did. This now makes it easier to find the family you are looking for when multiple families match the search. Fixes |
| `16.5` | core | Fixed a bug that would show an incorrect alert message when editing a family's Record Status even though there are no deceased people in the family. Fixes: #5802 |
| `16.3` | core | Updated Get Avatar handler to set person photo of any binary file type. Previously, when using a workflow to update a person's profile photo with a different file type, the default avatar continued to be displayed. Rock now correctly sets t |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-people-and-families-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-person` | normal | live verification |
| `5-core-configuration-and-data-model-personalias` | normal | live verification |
| `5-core-configuration-and-data-model-family-group` | normal | live verification |
| `5-core-configuration-and-data-model-groupmember-and-grouptyperole` | normal | live verification |
| `5-core-configuration-and-data-model-known-relationships` | normal | live verification |
| `5-core-configuration-and-data-model-notes-tags-following-badges-assessments-background-checks` | normal | live verification |
| `6-primary-entities-and-relationships-person-to-personalias` | normal | live verification |
| `6-primary-entities-and-relationships-person-to-family-group` | normal | live verification |
| `6-primary-entities-and-relationships-family-group-to-grouplocation-and-location` | normal | live verification |
| `6-primary-entities-and-relationships-group-or-family-to-attributes` | normal | live verification |
| `6-primary-entities-and-relationships-person-to-communications` | normal | live verification |
| `7-common-people-and-families-workflows-search-for-a-person` | normal | live verification |
| `7-common-people-and-families-workflows-add-or-edit-an-individual` | normal | live verification |
| `7-common-people-and-families-workflows-add-or-edit-a-family` | normal | live verification |
| `7-common-people-and-families-workflows-merge-duplicate-records` | normal | live verification |
| `7-common-people-and-families-workflows-delete-or-deactivate-a-person` | community-supported | live verification |
| `7-common-people-and-families-workflows-add-person-or-family-attributes` | normal | live verification |
| `7-common-people-and-families-workflows-track-how-a-person-record-was-created` | community-supported | live verification |
| `7-common-people-and-families-workflows-run-person-based-automation` | normal | live verification |
| `8-person-model-deep-dive-identity-fields` | normal | live verification |
| `8-person-model-deep-dive-names` | normal | live verification |
| `8-person-model-deep-dive-demographics` | normal | live verification |
| `8-person-model-deep-dive-contact-fields` | normal | live verification |
| `8-person-model-deep-dive-logins-account-protection-impersonation-and-passwordless-login` | normal | live verification |
| `9-families-deep-dive-family-as-group` | normal | live verification |
| `9-families-deep-dive-family-giving` | normal | live verification |
| `10-attributes-deep-dive-attribute-lava-filters` | normal | live verification |
| `10-attributes-deep-dive-entity-commands-and-attribute-prefetch` | normal | live verification |
| `10-attributes-deep-dive-attribute-migration-and-source-control` | normal | live verification |
| `11-related-rock-areas-groups-security-communications-check-in-communications` | normal | live verification |
| `12-administration-and-operational-guardrails-before-merging` | structural | live verification |
| `13-developer-api-lava-and-source-code-landmarks-person-lava-filters` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-setpersonattribute-workflow-action` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-personattributeforms-block` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-mobile-person-profile-block` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-mobile-group-members-block` | normal | live verification |
| `14-reporting-analytics-and-model-map-person-reports` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-attribute-reporting` | normal | live verification |
| `14-reporting-analytics-and-model-map-family-reporting` | community-supported | community-supported |
| `14-reporting-analytics-and-model-map-bi-family-report` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-data-views-and-automation` | community-supported | live verification |
| `14-reporting-analytics-and-model-map-profile-custom-reports` | community-supported | community-supported |
| `15-version-and-release-caveats-v16-3` | normal | live verification |
| `15-version-and-release-caveats-v17-2` | normal | live verification |
| `15-version-and-release-caveats-v18-3` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-person-attribute` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-family-attribute` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-new-person-entry-workflow` | normal | live verification |
| `16-implementation-playbooks-playbook-add-a-person-profile-panel` | normal | live verification |
| `16-implementation-playbooks-playbook-safely-merge-duplicate-people` | normal | live verification |
| `16-implementation-playbooks-playbook-recover-from-wrong-merge` | community-supported | live verification |
| `16-implementation-playbooks-playbook-build-a-family-registration-or-pre-registration-flow` | normal | live verification |
| `17-troubleshooting-decision-tree-workflow-person-attribute-resolves-wrong-person` | normal | live verification |
| `17-troubleshooting-decision-tree-profile-custom-tab-exposes-too-much` | normal | live verification |
| `18-agent-task-recipes-recipe-identify-a-person-safely` | structural | live verification |
| `18-agent-task-recipes-recipe-inspect-a-person-attribute` | normal | live verification |
| `18-agent-task-recipes-recipe-determine-if-a-value-is-person-id-or-alias-guid` | normal | live verification |
| `18-agent-task-recipes-recipe-audit-a-family-for-check-in` | normal | live verification |
| `18-agent-task-recipes-recipe-review-a-person-profile-customization` | structural | live verification |
| `18-agent-task-recipes-recipe-triage-an-accidental-merge` | community-supported | live verification |
| `18-agent-task-recipes-recipe-track-new-record-source` | normal | live verification |
| `18-agent-task-recipes-recipe-build-a-staff-directory-from-person-attributes` | community-supported | community-supported |
| `18-agent-task-recipes-recipe-add-a-bookmarked-groups-like-profile-panel` | community-supported | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `19-source-map-and-dependency-notes-community-recipes-used-as-examples-only` | community-supported | community-supported |
| `19-source-map-and-dependency-notes-records-requiring-live-verification` | normal | live verification |
