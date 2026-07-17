---
concept_id: communications
title: Communications Open Questions
generated: true
---

# Communications Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `6-primary-entities-and-relationships-systemcommunication`: SystemCommunication
- `7-common-communications-workflows-sending-sms`: Sending SMS
- `8-email-deep-dive-email-preview-and-preheaders`: Email preview and preheaders
- `8-email-deep-dive-view-email-on-webpage`: View email on webpage
- `8-email-deep-dive-email-template-design-systems`: Email template design systems
- `9-sms-deep-dive-staff-specific-texting-numbers`: Staff-specific texting numbers
- `9-sms-deep-dive-calls-to-sms-numbers`: Calls to SMS numbers
- `9-sms-deep-dive-sms-cost-segments-and-encoding`: SMS cost, segments, and encoding
- `9-sms-deep-dive-disabled-sms-warnings`: Disabled SMS warnings
- `11-administration-and-operational-guardrails-lower-environment-safety`: Lower environment safety
- `15-implementation-playbooks-playbook-configure-a-safe-email-transport-in-development`: Playbook: Configure a safe email transport in development
- `15-implementation-playbooks-playbook-launch-staff-sms-conversations`: Playbook: Launch staff SMS conversations
- `16-troubleshooting-decision-tree-email-delivered-but-analytics-are-missing`: Email delivered but analytics are missing
- `17-agent-task-recipes-recipe-determine-whether-a-workflow-email-supports-analytics`: Recipe: Determine whether a workflow email supports analytics

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-communications-mental-model`: 3. Communications Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-communication-transports`: Communication transports
- `5-core-configuration-and-data-model-communication-templates`: Communication templates
- `5-core-configuration-and-data-model-communication-lists-and-segments`: Communication lists and segments
- `5-core-configuration-and-data-model-system-phone-numbers-and-sms-pipeline`: System phone numbers and SMS pipeline
- `5-core-configuration-and-data-model-communication-jobs`: Communication jobs
- `6-primary-entities-and-relationships-communication`: Communication
- `6-primary-entities-and-relationships-communicationrecipient`: CommunicationRecipient
- `6-primary-entities-and-relationships-communicationattachment-and-communicationtemplateattachment`: CommunicationAttachment and CommunicationTemplateAttachment
- `6-primary-entities-and-relationships-communicationresponse-and-communicationresponseattachment`: CommunicationResponse and CommunicationResponseAttachment
- `6-primary-entities-and-relationships-smspipeline-and-smsaction`: SmsPipeline and SmsAction
- `7-common-communications-workflows-sending-sms`: Sending SMS
- `7-common-communications-workflows-sending-to-a-communication-list`: Sending to a communication list
- `7-common-communications-workflows-managing-communication-preferences`: Managing communication preferences
- `7-common-communications-workflows-using-communication-flows`: Using Communication Flows
- `8-email-deep-dive-email-authoring`: Email authoring
- `8-email-deep-dive-email-transport-and-validation`: Email transport and validation
- `8-email-deep-dive-deliverability-and-provider-setup`: Deliverability and provider setup
- `8-email-deep-dive-email-analytics`: Email analytics
- `8-email-deep-dive-email-preview-and-preheaders`: Email preview and preheaders
- `8-email-deep-dive-view-email-on-webpage`: View email on webpage
- `8-email-deep-dive-email-template-design-systems`: Email template design systems
- `9-sms-deep-dive-sms-recipient-eligibility`: SMS recipient eligibility
- `9-sms-deep-dive-sms-opt-out-and-opt-in`: SMS opt-out and opt-in
- `9-sms-deep-dive-staff-specific-texting-numbers`: Staff-specific texting numbers
- `9-sms-deep-dive-calls-to-sms-numbers`: Calls to SMS numbers
- `9-sms-deep-dive-disabled-sms-warnings`: Disabled SMS warnings
- `10-related-rock-areas-people-workflows-lava-security-lava`: Lava
- `10-related-rock-areas-people-workflows-lava-security-security`: Security
- `11-administration-and-operational-guardrails-approval-policies`: Approval policies
- `11-administration-and-operational-guardrails-template-operations`: Template operations
- `11-administration-and-operational-guardrails-lower-environment-safety`: Lower environment safety
- `12-developer-api-lava-and-source-code-landmarks-transport-components`: Transport components
- `12-developer-api-lava-and-source-code-landmarks-rest-endpoints`: REST endpoints
- `13-reporting-analytics-and-model-map-unsubscribe-reporting`: Unsubscribe reporting
- `13-reporting-analytics-and-model-map-model-map-coverage`: Model Map coverage

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
