---
concept_id: prayer-care
title: Prayer And Care Agent Cheatsheet
generated: true
---

# Prayer And Care Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Audit Prayer Configuration](tasks/audit-prayer-configuration.md) |  |  |
| [Review A Sensitive Request](tasks/review-a-sensitive-request.md) |  |  |
| [Build A Prayer-Team Coverage Report](tasks/build-a-prayer-team-coverage-report.md) |  |  |
| [Investigate Person Prayer History](tasks/investigate-person-prayer-history.md) |  |  |
| [Safely Extend Prayer Intake](tasks/safely-extend-prayer-intake.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.0` | core | Fixed an issue where Prayer Request Attributes not marked as "Public" were incorrectly displaying in the Obsidian version of the Prayer Request Entry block. These Attributes are now properly hidden on the Prayer Request Entry block. Fixes:  |
| `19.1` | core | Improved the Prayer Request List block to display prayer request text at a wider width for better readability. Fixes: #6824 |
| `17.5` | core | Fixed an issue where approving a Prayer Request in the Obsidian Prayer Request Detail block did not update the ApprovedOnDateTime and ApprovedByPersonAliasId fields. Fixes: #6403 |
| `17.2` | core | Fixed an issue where the Prayer Request Detail block in Obsidian did not recognize the PersonId URL parameter, which prevented person data from being pre-filled when creating a new prayer request. Fixes: #6357 |
| `17.0` | core | Added support for editing custom attributes within the Mobile Prayer Request block. This enhancement allows individuals to update custom attributes when submitting or managing prayer requests from a mobile device. Be aware that Rock Mobile  |
| `18.3` | core | Added a Campus Type filter to the campus picker on the Prayer Request Detail block. This allows individuals to narrow the list of selectable campuses when adding a new prayer request. |
| `17.0` | core | Added a new feature to Prayer which will optionally run several pre-configured AI completions on saved prayer requests. If you plan on using this feature, read the Tech Bulletin item on this topic. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-prayer-and-care-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-prayer-request-entry-configuration` | high | live verification |
| `5-core-configuration-and-data-model-prayer-request-detail-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-prayer-request-list-configuration` | high | live verification |
| `5-core-configuration-and-data-model-categories` | high | live verification |
| `5-core-configuration-and-data-model-approval-visibility-expiration-and-activity` | high | live verification |
| `6-primary-entities-and-relationships-prayer-request-to-person` | high | live verification |
| `6-primary-entities-and-relationships-prayer-request-to-campus` | normal | live verification |
| `6-primary-entities-and-relationships-prayer-request-to-comments-and-notes` | high | live verification |
| `7-common-prayer-and-care-workflows-public-website-prayer-intake` | normal | live verification |
| `7-common-prayer-and-care-workflows-internal-staff-entry` | normal | live verification |
| `7-common-prayer-and-care-workflows-prayer-card-view` | normal | live verification |
| `7-common-prayer-and-care-workflows-group-prayer-requests` | normal | live verification |
| `7-common-prayer-and-care-workflows-urgent-prayer-email` | community-supported | live verification |
| `7-common-prayer-and-care-workflows-sms-prayer-request-capture` | community-supported | community-supported |
| `7-common-prayer-and-care-workflows-prayer-wall` | community-supported | live verification |
| `7-common-prayer-and-care-workflows-live-prayer-chat` | community-supported | community-supported |
| `7-common-prayer-and-care-workflows-pastoral-care-summary` | community-supported | live verification |
| `8-prayer-requests-deep-dive-text-handling` | high | live verification |
| `8-prayer-requests-deep-dive-approval` | high | live verification |
| `8-prayer-requests-deep-dive-expiration` | normal | live verification |
| `9-teams-and-moderation-deep-dive-ai-moderation-and-formatting` | high | live verification |
| `10-follow-up-and-communications-deep-dive-comment-digest-email` | normal | live verification |
| `10-follow-up-and-communications-deep-dive-communications-security` | normal | live verification |
| `10-follow-up-and-communications-deep-dive-urgent-notifications` | community-supported | community-supported |
| `10-follow-up-and-communications-deep-dive-care-follow-up-beyond-prayer` | community-supported | community-supported |
| `11-related-rock-areas-people-groups-communications-workflows-security-cms-groups` | normal | live verification |
| `11-related-rock-areas-people-groups-communications-workflows-security-cms-communications` | normal | live verification |
| `12-administration-and-operational-guardrails-change-management` | structural | live verification |
| `13-developer-api-lava-and-source-code-landmarks-lava` | normal | live verification |
| `14-reporting-analytics-and-model-map-metrics-to-avoid-misreading` | community-supported | community-supported |
| `15-version-and-release-caveats` | normal | live verification |
| `16-implementation-playbooks-playbook-launch-basic-prayer-intake` | normal | live verification |
| `16-implementation-playbooks-playbook-launch-prayer-team-page` | normal | live verification |
| `16-implementation-playbooks-playbook-add-group-prayer` | structural | live verification |
| `16-implementation-playbooks-playbook-enable-comment-digest` | structural | live verification |
| `16-implementation-playbooks-playbook-add-sms-prayer-intake` | structural | live verification |
| `16-implementation-playbooks-playbook-add-public-prayer-wall` | structural | live verification |
| `18-agent-task-recipes-audit-prayer-configuration` | structural | live verification |
| `18-agent-task-recipes-safely-extend-prayer-intake` | structural | live verification |
