---
concept_id: communications
title: Communications Agent Cheatsheet
generated: true
---

# Communications Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Audit a single sent communication](tasks/recipe-audit-a-single-sent-communication.md) |  |  |
| [Recipe: Explain why a person did not get an email](tasks/recipe-explain-why-a-person-did-not-get-an-email.md) |  |  |
| [Recipe: Explain why a person did not get SMS](tasks/recipe-explain-why-a-person-did-not-get-sms.md) |  |  |
| [Recipe: Audit communication list freshness](tasks/recipe-audit-communication-list-freshness.md) |  |  |
| [Recipe: Review a communication template](tasks/recipe-review-a-communication-template.md) |  |  |
| [Recipe: Investigate SMS conversation access](tasks/recipe-investigate-sms-conversation-access.md) |  |  |
| [Recipe: Determine whether a workflow email supports analytics](tasks/recipe-determine-whether-a-workflow-email-supports-analytics.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed an issue where saving a Communication Template from the Communication Wizard failed if the template name included special characters. The preview image generation used the template name for the file, which caused an error on systems t |
| `18.2` | core | Fixed an issue where communication approvers were always redirected to the Communication Wizard page, even when the communication was originally created using the Simple Communication page. Approvers are now redirected to the appropriate ed |
| `18.2` | core | Fixed an issue with the Communication Entry Wizard block where changing the Communication Type (e.g., from Recipient Preference to Email or SMS) while creating a message could result in some recipients being excluded from the send list. Thi |
| `18.1` | core | Added an Obsidian Communication Detail block with improved message visualization and Communication Recipient insights, allowing administrators to review communication content, delivery status, and recipient activity more efficiently. |
| `19.1` | core | Added a "Communication Access Mode" setting to the Communication Detail Block along with a new "View All" security action. The default mode is "Strict", which limits viewing of Communication details to the individual who created or sent the |
| `18.3` | core | Fixed an issue where the Obsidian Communication Entry Wizard block did not enforce the allowed Communication Types configured in block settings when a Communication was started from outside the wizard (e.g., when using a grid's "Communicate |
| `18.2` | core | Fixed an issue where submitting a registration would disable an individual's SMS setting when the "Show SMS Opt-In" option on the Registration Template was set to False. The registration process will now preserve the individual's existing S |
| `18.1` | core | Added Communication Flows, a new tool under Admin Tools › Communications that lets administrators create automated, multi-step sequences across email, SMS, and push notifications. The feature tracks email opens, link clicks, form completion |
| `18.1` | core | Fixed an issue that caused opt-in and opt-out SMS keywords (like START and STOP) to be missing from the message history in the SMS Conversations block. These keywords will now appear in the conversation history, as long as the SMS Pipeline  |
| `18.1` | core | Improved the help text for the "Send When Approved" setting in the Communication Entry Wizard block to clarify when a Communication will be sent. Also updated the Communication Detail block to immediately queue Communications scheduled for  |
| `17.5` | core | Improved several system notifications—including Group Attendance Reminders, Sign-Up Registration Confirmations, and Sign-Up Reminders—to check if the recipient has SMS enabled before choosing between SMS or email delivery. |
| `17.1` | core | Added a "Remove All" button to the recipient modal of the Simple Communication Entry and Communication Entry Wizard blocks. This button clears all recipients at once, improving efficiency when resetting recipients in a copied communication. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-communications-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-communication-transports` | normal | live verification |
| `5-core-configuration-and-data-model-communication-templates` | high | live verification |
| `5-core-configuration-and-data-model-communication-lists-and-segments` | normal | live verification |
| `5-core-configuration-and-data-model-system-phone-numbers-and-sms-pipeline` | normal | live verification |
| `5-core-configuration-and-data-model-communication-jobs` | high | live verification |
| `6-primary-entities-and-relationships-communication` | normal | live verification |
| `6-primary-entities-and-relationships-communicationrecipient` | normal | live verification |
| `6-primary-entities-and-relationships-communicationattachment-and-communicationtemplateattachment` | normal | live verification |
| `6-primary-entities-and-relationships-systemcommunication` | community-supported | community-supported |
| `6-primary-entities-and-relationships-communicationresponse-and-communicationresponseattachment` | citation-only | live verification |
| `6-primary-entities-and-relationships-smspipeline-and-smsaction` | normal | live verification |
| `7-common-communications-workflows-sending-sms` | community-supported | live verification |
| `7-common-communications-workflows-sending-to-a-communication-list` | citation-only | live verification |
| `7-common-communications-workflows-managing-communication-preferences` | high | live verification |
| `7-common-communications-workflows-using-communication-flows` | normal | live verification |
| `8-email-deep-dive-email-authoring` | high | live verification |
| `8-email-deep-dive-email-transport-and-validation` | normal | live verification |
| `8-email-deep-dive-deliverability-and-provider-setup` | normal | live verification |
| `8-email-deep-dive-email-analytics` | high | live verification |
| `8-email-deep-dive-email-preview-and-preheaders` | community-supported | live verification |
| `8-email-deep-dive-view-email-on-webpage` | community-supported | live verification |
| `8-email-deep-dive-email-template-design-systems` | community-supported | live verification |
| `9-sms-deep-dive-sms-recipient-eligibility` | normal | live verification |
| `9-sms-deep-dive-sms-opt-out-and-opt-in` | normal | live verification |
| `9-sms-deep-dive-staff-specific-texting-numbers` | community-supported | live verification |
| `9-sms-deep-dive-calls-to-sms-numbers` | community-supported | live verification |
| `9-sms-deep-dive-sms-cost-segments-and-encoding` | community-supported | community-supported |
| `9-sms-deep-dive-disabled-sms-warnings` | community-supported | live verification |
| `10-related-rock-areas-people-workflows-lava-security-lava` | normal | live verification |
| `10-related-rock-areas-people-workflows-lava-security-security` | high | live verification |
| `11-administration-and-operational-guardrails-approval-policies` | normal | live verification |
| `11-administration-and-operational-guardrails-template-operations` | structural | live verification |
| `11-administration-and-operational-guardrails-lower-environment-safety` | community-supported | live verification |
| `12-developer-api-lava-and-source-code-landmarks-transport-components` | normal | live verification |
| `12-developer-api-lava-and-source-code-landmarks-rest-endpoints` | normal | live verification |
| `13-reporting-analytics-and-model-map-unsubscribe-reporting` | citation-only | live verification |
| `13-reporting-analytics-and-model-map-model-map-coverage` | citation-only | live verification |
| `13-reporting-analytics-and-model-map-business-intelligence` | citation-only | live verification |
| `15-implementation-playbooks-playbook-configure-a-safe-email-transport-in-development` | community-supported | live verification |
| `15-implementation-playbooks-playbook-build-a-governed-template-library` | normal | live verification |
| `15-implementation-playbooks-playbook-create-or-audit-a-communication-list` | citation-only | live verification |
| `15-implementation-playbooks-playbook-launch-staff-sms-conversations` | community-supported | live verification |
| `15-implementation-playbooks-playbook-implement-a-communication-flow` | normal | live verification |
| `16-troubleshooting-decision-tree-some-recipients-are-missing` | normal | live verification |
| `16-troubleshooting-decision-tree-email-delivered-but-analytics-are-missing` | community-supported | live verification |
| `17-agent-task-recipes-recipe-audit-a-single-sent-communication` | structural | live verification |
| `17-agent-task-recipes-recipe-explain-why-a-person-did-not-get-an-email` | structural | live verification |
| `17-agent-task-recipes-recipe-explain-why-a-person-did-not-get-sms` | normal | live verification |
| `17-agent-task-recipes-recipe-audit-communication-list-freshness` | citation-only | live verification |
| `17-agent-task-recipes-recipe-review-a-communication-template` | structural | live verification |
| `17-agent-task-recipes-recipe-investigate-sms-conversation-access` | normal | live verification |
| `17-agent-task-recipes-recipe-determine-whether-a-workflow-email-supports-analytics` | community-supported | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `18-source-map-and-dependency-notes` | high | live verification |
