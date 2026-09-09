---
concept_id: communications
title: Communications Agent Cheatsheet
generated: true
---

# Communications Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Preflight a broad email communication](tasks/recipe-preflight-a-broad-email-communication.md) | `Person`, `DataView`, `Group` | `Person`, `DataView`, `Group` |
| [Recipe: Diagnose one missing recipient](tasks/recipe-diagnose-one-missing-recipient.md) | `Person`, `Group` | `Person`, `Group` |
| [Recipe: Validate an email transport and its event loop](tasks/recipe-validate-an-email-transport-and-its-event-loop.md) |  |  |
| [Recipe: Validate inbound SMS routing](tasks/recipe-validate-inbound-sms-routing.md) | `Workflow` | `Workflow` |
| [Recipe: Create a communication flow without over-messaging](tasks/recipe-create-a-communication-flow-without-over-messaging.md) | `Person`, `DataView` | `Person`, `DataView` |
| [Recipe: Investigate rising unsubscribes or saturation](tasks/recipe-investigate-rising-unsubscribes-or-saturation.md) |  |  |
| [Recipe: Retest a workflow-backed communication safely](tasks/recipe-retest-a-workflow-backed-communication-safely.md) | `Label`, `Workflow` | `Label`, `Workflow` |
| [Recipe: Bound an agent that can draft communications](tasks/recipe-bound-an-agent-that-can-draft-communications.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
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
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | normal | live verification |
| `communication-foundations` | normal | live verification |
| `audiences-communication-lists-and-segments` | normal | live verification |
| `templates-and-system-communications` | normal | live verification |
| `email` | normal | live verification |
| `sms` | normal | live verification |
| `sms-sms-conversations` | normal | live verification |
| `sms-sms-pipeline` | normal | live verification |
| `sending-classification-and-approval` | normal | live verification |
| `preferences-consent-and-sender-reputation` | normal | live verification |
| `communication-flows-and-automation-boundaries` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-intended-recipients-are-missing-or-shown-as-ineligible` | normal | live verification |
| `troubleshooting-decision-tree-email-appears-sent-but-delivery-or-analytics-are-missing` | normal | live verification |
| `troubleshooting-decision-tree-email-shows-an-unexpected-sender-or-on-behalf-of-label` | normal | live verification |
| `troubleshooting-decision-tree-two-unsubscribe-options-appear-in-an-email` | normal | live verification |
| `troubleshooting-decision-tree-a-template-is-missing-or-cannot-be-saved` | high | live verification |
| `troubleshooting-decision-tree-a-communication-remains-pending-approval` | high | live verification |
| `troubleshooting-decision-tree-incoming-sms-does-not-reach-the-expected-conversation-or-workflow` | normal | live verification |
| `troubleshooting-decision-tree-an-automated-sms-reply-is-absent-from-history` | normal | live verification |
| `troubleshooting-decision-tree-sms-segments-cost-or-delivery-differ-from-expectations` | normal | live verification |
| `troubleshooting-decision-tree-an-unsubscribe-appears-unexpected` | normal | live verification |
| `agent-task-recipes-recipe-preflight-a-broad-email-communication` | normal | live verification |
| `agent-task-recipes-recipe-diagnose-one-missing-recipient` | normal | live verification |
| `agent-task-recipes-recipe-validate-an-email-transport-and-its-event-loop` | normal | live verification |
| `agent-task-recipes-recipe-validate-inbound-sms-routing` | normal | live verification |
| `agent-task-recipes-recipe-create-a-communication-flow-without-over-messaging` | normal | live verification |
| `agent-task-recipes-recipe-investigate-rising-unsubscribes-or-saturation` | normal | live verification |
| `agent-task-recipes-recipe-retest-a-workflow-backed-communication-safely` | normal | live verification |
| `agent-task-recipes-recipe-bound-an-agent-that-can-draft-communications` | citation-only | live verification |
| `known-gaps-and-live-verification` | citation-only | live verification |
| `source-map` | high | live verification |
| `approved-claim-coverage` | normal | live verification |
