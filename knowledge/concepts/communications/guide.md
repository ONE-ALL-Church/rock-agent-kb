---
id: authored-communications
title: Communications
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Communications

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Communications index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock Communications is not one feature. It is a coordinated system for authoring messages, selecting recipients, honoring communication preferences, sending through configured transports, recording delivery outcomes, and reporting engagement. Agents working in this area should treat every communication problem as a path through four layers:

1. **Audience selection**: Who is eligible to receive the message?
2. **Medium selection**: Is the message email, SMS, push, or a recipient-preference blend?
3. **Transport execution**: Which configured provider or component actually sends it?
4. **Recipient history and analytics**: What did Rock record about delivery, unsubscribe, engagement, and response?

The official `Communicating With Rock` manual is the primary operational source for the communication engine, mediums, transports, send job, unsubscribes, bounced mail, templates, lists, preferences, analytics, and SMS detail ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). RockU provides feature-level training paths for the modern Communication Wizard, templates, lists, preferences, flows, analytics, saturation reporting, SMS conversations, and SMS pipeline ([RockU Communication](https://community.rockrms.com/rocku/communication)). Release notes are required when working in modern Rock versions because communications changed materially in 17.x, 18.x, and 19.x ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

For practical agent work, start from the record or block actually involved:

- For a sent or pending message, inspect the `Communication` and `CommunicationRecipient` records.
- For a list send, inspect the communication list group, active group members, member communication preferences, segments, and the recipient detail logic.
- For template problems, inspect `CommunicationTemplate`, category, active state, version, wizard support, template security, preview image, Lava fields, and whether the message is a system-wide template or a Communication Flow template.
- For SMS problems, inspect system phone numbers, SMS pipeline, SMS actions, the person's mobile phone record, SMS enabled state, opt-out handling, and the SMS Conversations action.
- For analytics problems, determine whether the communication was sent by a path that supports analytics, whether the transport supplies open/click data, and whether Rock has recipient engagement rows to report.
- For security problems, inspect block security, template security, communication detail access mode, approver permissions, list visibility, and the v19.1 `View All` behavior for Communication Detail ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Do not assume a communication was sent simply because a user saw a blue message bubble, a communication row exists, or a workflow completed. Confirm the recipient status, medium entity type, selected transport, send date, status note, and any exception or job history. For SMS, also confirm that the recipient's mobile phone is SMS enabled and not opted out; community operational examples show staff can believe a reply was sent even when the recipient's phone record prevents SMS delivery ([Disabled SMS Mobile Phone Warning](https://community.rockrms.com/recipes/438)).

The most important version caveats are:

- v17 introduced communication-template versioning and recipient-detail fixes, including corrected SMS eligibility logic and `GroupMember.CommunicationPreference` handling in the recipient detail stored procedure ([migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)).
- v17.4 improved duplicate-recipient removal for large communications ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v18.1 added Communication Flows, improved analytics, saturation reporting, refreshed preferences/list surfaces, and an Obsidian Communication Detail block ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8), [Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v18.2 and v18.3 fixed several Communication Entry Wizard, approval, template, and allowed-type enforcement issues ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v19.1 adds Communication Detail access control changes and a `View All` security action; agents must verify block configuration and permissions after upgrading ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

## 2. Scope And Terminology

This guide covers Rock RMS Communications as an operational and data-model concept: email, SMS, push-related communication fields, communication templates, transports, communication lists and segments, preferences, conversations, system communications, flow communications, analytics, reporting, security, and agent troubleshooting. It depends on People, Workflows, Lava, and Security because communications are usually selected from people records, often triggered by workflows, rendered through Lava, and constrained by security rules.

A **Communication** is a message instance. It represents the authored send: subject, message content, sender metadata, type/medium data, future send time, status, approval state, attachments, and related recipients. The Model Map lists `Communication` as a core model in the Communication category ([Model Map](https://community.rockrms.com/ModelMap)).

A **Communication Recipient** is an individual recipient row tied to a communication. It carries recipient-level send state such as pending/delivered/failure status, medium, person alias, send time, unsubscribe information, and status note. The Model Map lists `Communication Recipient` separately from `Communication`, which is critical: most delivery investigations should happen at recipient level, not only at the parent communication ([Model Map](https://community.rockrms.com/ModelMap)). Rock also exposes a v2 model endpoint for communication recipients, guarded by model read/write security actions ([CommunicationRecipientsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/CommunicationRecipientsController.CodeGenerated.cs)).

A **Medium** is the logical channel, such as email or SMS. The official manual separates mediums from transports: the medium decides the communication channel and the transport is the implementation that sends through a configured provider or component ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).

A **Transport** is the implementation used by a medium. Email might use SMTP, Mailgun, or another configured email transport. SMS might use Twilio, a test transport, or another SMS transport. Community recipes show real installations using SMTP-compatible services like Mailtrap for development testing and AWS SES through Rock's SMTP transport, but those examples should be treated as community guidance and verified against the current transport component and provider configuration ([Mailtrap Email Testing](https://community.rockrms.com/recipes/138), [AWS SES SMTP Transport](https://community.rockrms.com/recipes/171)).

A **Communication Template** is reusable message structure and sender metadata. Modern template records include fields for email, SMS, push-related options, category, active state, starter state, template version, CSS inlining, preview image, logo, Lava fields, and attachments according to Obsidian template detail view models and the official communication manual ([Communication Template Detail source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailCommunicationTemplateBag.d.ts), [Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).

A **System Communication** is a reusable communication definition used by Rock's internal features and system workflows, such as receipts, scheduling responses, and notifications. It is a different concept from user-created communication templates. The Model Map lists `System Communication` in the Communication category ([Model Map](https://community.rockrms.com/ModelMap)), and RockU includes a System Communications module ([System Communications](https://community.rockrms.com/rocku/communication/system-emails)).

A **Communication List** is a group used as a subscribable or sendable audience. RockU notes that shipped lists are not automatically synced; if an organization wants to use them, it should wire them to organizational data views or another membership sync strategy ([Communication Lists & Segments](https://community.rockrms.com/rocku/communication/communication-lists--segments)). Agents must not assume list membership reflects current attendance, membership, giving, serving, or campus state unless a live sync path is verified.

A **Segment** is a personalization or filtering layer used to refine recipients. The recipient detail stored procedure accepts a personalization segment list and a match type for OR or AND behavior, then filters recipient people by `PersonAliasPersonalization` rows ([recipient detail SQL source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql)).

A **Communication Flow** is a v18.1+ automation feature for multi-step communication sequences across email, SMS, and push notifications, with progress and conversion tracking ([Rock Release Notes](https://www.rockrms.com/releasenotes), [Communication Flows](https://community.rockrms.com/rocku/communication/communication-flows)). The Model Map includes `Communication Flow`, `Communication Flow Communication`, `Communication Flow Instance`, `Communication Flow Instance Recipient`, `Communication Flow Instance Communication`, and conversion-related models ([Model Map](https://community.rockrms.com/ModelMap)).

An **SMS Pipeline** is the inbound SMS routing/action system. It determines how inbound texts, keywords, and conversation messages are processed. RockU has SMS Pipeline training ([SMS Pipeline](https://community.rockrms.com/rocku/communication/sms-pipeline)), and the Model Map lists `Sms Pipeline` and `Sms Action` ([Model Map](https://community.rockrms.com/ModelMap)).

**Nameless People** and anonymous recipients are communication edge cases. Source code has explicit anonymous recipient creation for both email and SMS message recipients, meaning not every send target necessarily maps to a full Person record ([RockEmailMessageRecipient source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockEmailMessageRecipient.cs), [RockSMSMessageRecipient source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockSMSMessageRecipient.cs)). RockU also includes a Nameless People module in the communication training path ([Nameless People](https://community.rockrms.com/rocku/communication/nameless-people)).

## 3. Communications Mental Model

A Rock communication moves through a lifecycle:

1. **Create**: A user, block, workflow, system process, mobile block, or flow creates a communication.
2. **Resolve recipients**: Rock loads people, person aliases, list members, entity-set members, connection-request contacts, or explicit anonymous addresses/numbers.
3. **Evaluate eligibility**: Rock considers deceased status, email/SMS availability, active email, bulk email preference, SMS enabled state, medium preference, push eligibility, list subscription, and segment filters.
4. **Author content**: The sender selects a template or writes message content, subject, SMS body, push content, additional details, sender metadata, attachments, and Lava merge fields.
5. **Approve**: If required, the communication waits for an approver or is auto-approved based on block and security settings.
6. **Queue or send**: Immediate sends may be queued directly; scheduled or future sends rely on the communications job path.
7. **Transport**: The medium routes to the configured transport. The transport sends and returns recipient-level results.
8. **Persist results**: Rock updates recipient statuses, send dates, status notes, delivery/engagement data, and history.
9. **Report and respond**: Admins review detail pages, analytics, saturation, unsubscribe reports, recipient grids, SMS conversations, or flow analytics.

This model is more reliable than navigating by page names because the same underlying communication behavior can be reached from different blocks: Simple Communication Entry, Communication Entry Wizard, mobile Communication Entry, list pages, group member lists, workflow actions, system notifications, connections, prayer, finance receipts, and Communication Flows.

The official documentation frames communications around Rock's communication engine, mediums and transports, and the send job ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). Source code shows transport components turning communication/message objects into transport-specific sends. `EmailTransportComponent` validates a From address, builds a template email message with merge fields and global attributes, then sends recipient tasks with a configurable async parallelization path where supported ([EmailTransportComponent source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/EmailTransportComponent.cs)). The SMS test transport re-queries the communication, checks that it is approved and due, counts pending recipients for the SMS medium, requires a From system phone number, gathers attachments, and sends pending recipients in parallel batches ([SmsTest source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/SmsTest.cs)).

For agents, the recipient layer is the decisive layer. Parent communication status can be misleading if only some recipients are eligible, if duplicate removal changed the final list, if the communication is approved but future-dated, or if the parent communication was created by a path that later failed in a transport. Inspect individual `CommunicationRecipient` rows and their status notes before concluding.

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. **Official documentation and release notes** for current configuration, feature behavior, version caveats, and upgrade action. The primary manual is [Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8). Current version changes come from [Rock Release Notes](https://www.rockrms.com/releasenotes).
2. **Source code and generated view models** for implementation landmarks, exact field names, route prefixes, and data shape. Examples include `EmailTransportComponent`, `SmsTest`, `CommunicationTemplateDetail` bags, and REST model controllers.
3. **RockU training** for UI workflow orientation. RockU's communication playlist covers lists, templates, wizard, preferences, analytics, flows, saturation reporting, system communications, SMS pipeline, SMS conversations, and sending email/SMS in simple mode ([RockU Communication](https://community.rockrms.com/rocku/communication)).
4. **Model Map** for entity inventory and category membership. It confirms models but usually does not supply relationship depth in the compact source pack ([Model Map](https://community.rockrms.com/ModelMap)).
5. **Community recipes and Q&A** for operational examples and patterns. Recipes can be useful but are not official; the recipe pages themselves warn that community recipes are not reviewed or endorsed by the core team and may affect performance or security. Treat them as patterns requiring local review, not authoritative configuration instructions.

This guide intentionally avoids reproducing long source passages. It synthesizes the source pack into an operational manual for agents. When a behavior is likely instance-specific or the pack is thin, this guide names the live object to inspect rather than inventing certainty.

## 5. Core Configuration And Data Model

### Communication transports

The transport layer is configured under Rock's communication administration area. The official manual distinguishes mediums and transports, and community configuration examples refer to `Admin Tools > Communications > Communication Transports` for transport selection and provider credentials ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8), [Mailtrap Email Testing](https://community.rockrms.com/recipes/138)).

Operational checks:

- Inspect the active transport component for the medium.
- Confirm provider credentials and endpoint settings.
- Confirm whether the transport supports analytics, open tracking, click tracking, bounces, delivery callbacks, MMS, or opt-out events.
- Confirm whether the transport is disabled in lower environments.
- Confirm whether the communications send job is enabled if the communication is scheduled or queued rather than immediate.

For development instances, use a trap or test transport. A community Mailtrap recipe describes routing all development email to a captured inbox by configuring Mailtrap as an SMTP transport and selecting SMTP as the Email medium transport container ([Mailtrap Email Testing](https://community.rockrms.com/recipes/138)). Treat this as a pattern: in any live instance, verify actual SMTP host, port, SSL, username, password, active state, and selected medium transport.

For SMTP-based providers such as AWS SES, a community recipe notes that standard SMTP send can deliver mail but may not automatically write open/click analytics back into Rock ([AWS SES SMTP Transport](https://community.rockrms.com/recipes/171)). If an analytics investigation involves a non-native provider, verify both provider-side tracking and Rock-side callback/integration support.

### Communication mediums

The medium controls the channel. Common mediums include email, SMS, and push notifications. Recipient-preference sends use recipient-level preference and eligibility to choose a medium where supported by the entry block and configuration.

The v17 recipient detail stored procedure returns the data needed to determine whether a person can receive email, SMS, or push notifications, and it accepts either a communication list ID or communication ID as the input list type ([recipient detail SQL source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql)). Agents should treat this as a key implementation landmark for list and recipient eligibility issues in modern Rock.

### Communication templates

Template configuration is central because templates influence content, sender metadata, available channels, wizard support, preview behavior, and security. The official manual describes template categories, starter templates, preview images, permissions, and where to create templates in `Admin Tools > Settings > Communication Templates` ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). RockU has both modern and legacy template training ([Communication Templates](https://community.rockrms.com/rocku/communication/communication-templates), [Communication Templates Legacy](https://community.rockrms.com/rocku/communication/communication-templates-legacy)).

Modern template detail data includes:

- attachments
- BCC and CC email addresses
- category
- description
- from email
- from name
- preview image file
- active state
- CSS inlining enabled
- starter state
- Lava fields
- logo binary file
- email message content
- template name
- push message and push options
- reply-to email
- SMS From system phone number
- SMS message
- email subject
- template version

These fields are visible in the Obsidian `CommunicationTemplateDetailCommunicationTemplateBag` and initialization box source records ([template detail bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailCommunicationTemplateBag.d.ts), [template initialization box](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailInitializationBox.d.ts)).

Important distinctions:

- A system-wide Communication Template is not the same thing as a Communication Flow template. The official manual notes that email templates inside Communication Flows differ from system-wide communication templates ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).
- Template visibility depends on security. If a user cannot see a template, inspect permissions and whether it is set up for use with the relevant wizard or block ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).
- v17 added a `Version` column to `CommunicationTemplate` ([v17 migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)).
- v18.3 fixed template saving failures when special characters in the template name affected preview image generation ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### Communication lists and segments

Communication lists are group-backed audiences. The key operational warning from RockU is that shipped lists are not automatically synced and may need to be wired to data views if used organizationally ([Communication Lists & Segments](https://community.rockrms.com/rocku/communication/communication-lists--segments)). Agents should inspect the group, group type, group members, sync jobs, data view rules, and member statuses before trusting a list name.

Segment filtering is implemented through the recipient detail path. The source snippet shows inputs for personalization segment IDs and match type: `1 = OR` and `2 = AND`. The procedure loads group members, excludes deceased people, requires active group-member status, then applies personalization segment filtering if provided ([recipient detail SQL source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql)).

Live checks:

- Does the group membership represent the intended audience?
- Are group members active?
- Are deceased people excluded?
- Are segments supplied?
- Is the segment match mode OR or AND?
- Are `PersonAliasPersonalization` rows present for the people expected to match?
- Is the list using a sync job or manual membership?

### System phone numbers and SMS pipeline

For SMS, the From number is not cosmetic. SMS transport code expects a communication's SMS From system phone number to exist, and the SMS test transport throws if it gets to send time without a From number ([SmsTest source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/SmsTest.cs)). Operationally, inspect:

- System phone number record
- assigned person, if any
- security on the number
- provider/Twilio phone number state
- SMS capability
- voice behavior if people call the number
- pipeline actions
- opt-in/opt-out settings
- forwarding behavior, if configured

SMS Pipeline training is part of RockU ([SMS Pipeline](https://community.rockrms.com/rocku/communication/sms-pipeline)). Release notes indicate v18.1 added configuration options to system phone number settings for SMS opt-in and opt-out handling, and fixed missing START/STOP keyword visibility in SMS Conversations when the SMS Pipeline includes the SMS Conversations action ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### Communication jobs

The official manual includes the Communications Send Job as part of the engine ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). The agent pattern is simple:

- Immediate approved sends may queue directly, especially after v18.1 improvements for communications scheduled for "now" after approval ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- Future-dated or scheduled communications depend on job processing.
- If a communication exists but did not send, inspect status, approval, future send time, job state, job history, exceptions, and recipient pending counts.

## 6. Primary Entities And Relationships

### Communication

`Communication` is the parent send record. It connects to recipients, attachments, sender metadata, message content, status, future send time, template usage, and history. The Model Map lists it in the Communication category ([Model Map](https://community.rockrms.com/ModelMap)). Source transports re-query the communication before sending; this matters because stale in-memory objects should not be trusted in operational debugging ([EmailTransportComponent source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/EmailTransportComponent.cs), [SmsTest source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/SmsTest.cs)).

Inspect:

- `Id`, `Guid`
- `Status`
- `CommunicationType`
- `Subject`
- message/SMS/push content fields
- sender fields
- `FutureSendDateTime`
- `CreatedByPersonAlias`
- template references, if present
- `SmsFromSystemPhoneNumber`
- attachments
- approval fields and audit fields

### CommunicationRecipient

`CommunicationRecipient` is the recipient delivery record. It links a person alias to a communication and tracks status, medium, send time, status note, unsubscribe date, and unsubscribe level. The Model Map lists it as its own Communication model ([Model Map](https://community.rockrms.com/ModelMap)). The v2 REST controller exposes model CRUD endpoints with secured read/write actions ([CommunicationRecipientsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/CommunicationRecipientsController.CodeGenerated.cs)).

Inspect:

- `CommunicationId`
- `PersonAliasId`
- `MediumEntityTypeId`
- `Status`
- `StatusNote`
- `SendDateTime`
- `UnsubscribeDateTime`
- `UnsubscribeLevel`
- recipient merge data, if available
- failures or pending rows

### CommunicationAttachment and CommunicationTemplateAttachment

The Model Map lists both `Communication Attachment` and `Communication Template Attachment` ([Model Map](https://community.rockrms.com/ModelMap)). Runtime communications can have attachments, and templates can define default attachments. The SMS test transport also checks communication SMS attachments through `GetAttachmentBinaryFileIds( CommunicationType.SMS )` before sending ([SmsTest source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/SmsTest.cs)).

When attachments are missing or unexpected, inspect:

- template attachments
- communication attachments
- binary file type and file security
- medium-specific attachment support
- provider support for MMS or attachments
- template-to-communication copy behavior

### CommunicationTemplate

`CommunicationTemplate` stores reusable message content and metadata. It has an explicit version in v17+ ([v17 migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)). Obsidian view models show fields such as active state, starter state, CSS inlining, Lava fields, category, preview image, logo, message, SMS message, push message, subject, sender, reply-to, and selected system phone number ([template detail bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailCommunicationTemplateBag.d.ts)).

### SystemCommunication

`System Communication` is listed in the Model Map ([Model Map](https://community.rockrms.com/ModelMap)) and covered by RockU ([System Communications](https://community.rockrms.com/rocku/communication/system-emails)). It is often used by workflows and system features. Recipes show common modifications to system communications, such as giving receipts and scheduling responses, but agents must review Lava commands, security, and finance/privacy impact before implementing community snippets ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510), [Decline Reason in Scheduling Response Email](https://community.rockrms.com/recipes/419)).

### CommunicationResponse and CommunicationResponseAttachment

The Model Map lists response models, implying separate records for responses and response attachments ([Model Map](https://community.rockrms.com/ModelMap)). When troubleshooting inbound replies or conversation-like behavior, do not assume everything is stored only in the original communication row.

### SmsPipeline and SmsAction

The Model Map lists `Sms Pipeline` and `Sms Action` ([Model Map](https://community.rockrms.com/ModelMap)). SMS pipeline configuration determines inbound message handling. Release notes specifically tie START/STOP keyword visibility in SMS Conversations to whether the SMS Pipeline includes the SMS Conversations action ([Rock Release Notes](https://www.rockrms.com/releasenotes)). For inbound SMS issues, the pipeline is the first admin object to inspect after provider webhook delivery.

### CommunicationFlow entities

Communication Flows are modeled separately:

- `Communication Flow`
- `Communication Flow Communication`
- `Communication Flow Instance`
- `Communication Flow Instance Communication`
- `Communication Flow Instance Recipient`
- `Communication Flow Instance Communication Conversion`

The Model Map lists these as Communication category models ([Model Map](https://community.rockrms.com/ModelMap)). Release notes describe Communication Flows as automated multi-step sequences across email, SMS, and push, tracking opens, clicks, forms, registrations, group joins, step progress, and flow analytics ([Rock Release Notes](https://www.rockrms.com/releasenotes)). Flow recipient metrics view models include sent date, opened date, clicked date, conversion date, unsubscribe date, person, and parent flow instance communication identifiers ([recipient metrics source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowInstanceMessageMetrics/recipientMetricsBag.d.ts)).

## 7. Common Communications Workflows

### Sending a standard email

Use the Communication Wizard or Simple Communication Entry depending on the page and block configuration. RockU has separate modern Communication Wizard and legacy/simple mode training ([Communication Wizard](https://community.rockrms.com/rocku/communication/communication-wizard), [Sending Email Simple Mode](https://community.rockrms.com/rocku/communication/sending-email-legacy)). The official manual covers sending communications and template selection ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).

Agent checklist:

1. Identify the entry block used.
2. Identify recipients and source: list, group, grid action, entity set, connection requests, workflow, or manual entry.
3. Confirm allowed communication types in block settings.
4. Confirm selected template supports the medium and wizard path.
5. Confirm from name, from email, reply-to, subject, body, attachments, and Lava fields.
6. Confirm approval requirements.
7. Confirm send time.
8. Confirm recipient statuses after sending.

v18.2 fixed an approval redirect issue where approvers were sent to the wrong editing page when a communication came from Simple Communication rather than the wizard ([Rock Release Notes](https://www.rockrms.com/releasenotes)). If approvers report wrong navigation on an older instance, check version first.

### Sending SMS

SMS sends require a valid From system phone number, recipients with SMS-capable/allowed phone records, a configured SMS medium/transport, and content that fits the provider's cost and encoding expectations. RockU covers Sending SMS in Simple Mode and SMS Conversations ([Sending SMS Simple Mode](https://community.rockrms.com/rocku/communication/sending-sms-legacy), [SMS Conversations](https://community.rockrms.com/rocku/communication/sms-conversations)).

Agent checklist:

1. Confirm SMS medium is enabled for the block.
2. Confirm From system phone number exists and is available to the sender.
3. Confirm recipient phone type is mobile where required.
4. Confirm recipient SMS enabled state.
5. Confirm opt-out state.
6. Confirm message content length, encoding, and MMS/attachment behavior.
7. Confirm pipeline/action for replies.
8. Confirm recipient statuses after send.

A community SMS segment calculator recipe highlights a practical operational issue: Unicode characters can change SMS encoding and segment counts, increasing credits across a recipient list ([SMS Credit/Segment Calculator](https://community.rockrms.com/recipes/542)). Use this as a reminder to inspect content length and encoding before large sends; do not assume one visible message equals one billable segment.

### Sending to a communication list

RockU notes shipped lists are not automatically synced and should be wired to data views if an organization wants them to reflect current criteria ([Communication Lists & Segments](https://community.rockrms.com/rocku/communication/communication-lists--segments)). A list send is only as good as its group membership.

Agent checklist:

1. Inspect the communication list group.
2. Confirm group members and active status.
3. Confirm sync source, if any.
4. Confirm data view criteria, if used.
5. Confirm segments and AND/OR match behavior.
6. Confirm member communication preferences.
7. Confirm unsubscribes and list subscriptions.
8. Preview recipient detail counts before sending.

### Managing communication preferences

Communication Preferences is a first-class user and admin concern. RockU has modern and legacy preference modules ([Communication Preferences](https://community.rockrms.com/rocku/communication/communication-preferences), [Communication Preferences Legacy](https://community.rockrms.com/rocku/communication/communication-preferences-legacy)). The v18.1 documentation update identifies the refreshed Email Preferences block as the go-to place for communication preferences and list subscriptions ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).

Agents should distinguish:

- person-level email preference
- phone-level SMS enabled state
- group/list subscription
- group member communication preference
- unsubscribe from a specific communication
- unsubscribe from a list
- global/all unsubscribe
- provider-level opt-out or suppression
- push notification preference

The v17 stored procedure explicitly added `GroupMember.CommunicationPreference` into recipient details ([v17 migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)). If recipient-preference behavior looks wrong, inspect both the person and group-member preference layers.

### Using Communication Flows

Communication Flows are for strategic multi-step journeys, not one-off sends. They were added in v18.1 under Admin Tools > Communications, with support for automated sequences across email, SMS, and push, plus tracking for opens, clicks, forms, registrations, group joins, step progress, and analytics ([Rock Release Notes](https://www.rockrms.com/releasenotes)). RockU has a Communication Flows module ([Communication Flows](https://community.rockrms.com/rocku/communication/communication-flows)).

Use flows when the objective is a goal over time: onboarding, next steps, event follow-up, serving recruitment, re-engagement, donor journeys, or ministry nurture. Do not use a flow when a one-time communication, system communication, or workflow notification is simpler and more auditable.

Agent checklist:

1. Identify flow goal and conversion event.
2. Inspect flow communications and templates.
3. Confirm entry criteria.
4. Confirm exit criteria.
5. Confirm message timing and delays.
6. Confirm medium configuration.
7. Confirm analytics expectations.
8. Inspect flow instance and recipient records for a specific person.

### Using mobile communication blocks

Rock Mobile includes communication blocks, including Communication Entry, Communication List Subscribe, Communication View, SMS Conversation List, and SMS Conversation in the mobile docs communication section ([Mobile Communication Blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication)).

The mobile Communication Entry block allows email/SMS communications to a group of recipients and requires an `EntitySetGuid` page parameter whose entity set type should be Person. The docs note that Group Member List can generate those parameters. Settings include enabling email, enabling SMS, showing From Name, and showing Reply To, among others ([Mobile Communication Entry](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry)).

Mobile Communication List Subscribe lets users subscribe or unsubscribe from communication lists, can show descriptions, medium preferences, push notifications as a medium preference, filter by campus context, and always include subscribed lists ([Mobile Communication List Subscribe](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe)).

Mobile SMS Conversation List manages SMS conversation inboxes, with settings for allowed SMS numbers, showing only personal SMS numbers, hiding personal SMS numbers, months of conversations, max conversations, database timeout, conversation page, and person search behavior ([Mobile SMS Conversation List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list)).

Mobile Communication View handles push notification "Show Details" behavior and uses additional details entered in the communication authoring path ([Mobile Communication View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-view)).

## 8. Email Deep Dive

### Email authoring

Email authoring combines subject, body, sender metadata, reply-to, CC/BCC, attachments, template choice, Lava merge fields, and previewing. The official manual describes choosing templates, using categories, and preview images ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). Obsidian template view models confirm email-specific fields such as `fromEmail`, `fromName`, `replyToEmail`, `ccEmails`, `bccEmails`, `subject`, `message`, `attachments`, and CSS inlining ([template detail bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailCommunicationTemplateBag.d.ts)).

Agents should verify:

- Sender domain alignment with the transport provider.
- Reply-to behavior.
- Whether CC/BCC are intended and allowed.
- Template category and starter behavior.
- Template permissions.
- Whether CSS inlining is enabled and appropriate.
- Whether images and links are absolute and public.
- Whether Lava fields render for the current recipient and preview person.
- Whether the template supports the wizard being used.

### Email transport and validation

`EmailTransportComponent` is the main code landmark for how Rock prepares email transport sends. It validates that a From address exists, builds a template email message, gets global attributes, and sends to recipients with async parallelization where supported ([EmailTransportComponent source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/EmailTransportComponent.cs)). Email transport tests show that Rock normalizes certain header-style inputs, including subject newline trimming and reply-to composition behavior ([EmailTransportComponentTests source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Communications/EmailTransportComponentTests.cs)).

A transport response carries a recipient status and status note through `EmailSendResponse` ([EmailSendResponse source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/EmailSendResponse.cs)). When investigating delivery, inspect the recipient status note before checking provider dashboards.

### Deliverability and provider setup

Deliverability depends on Rock configuration and external provider configuration. This source pack does not include full deliverability documentation for SPF, DKIM, DMARC, suppression lists, provider webhooks, or bounce processing. Agents should inspect live provider DNS records, domain authentication, webhook endpoints, bounce processing settings, and suppression state rather than infer them.

The official manual includes bounced mail and unsubscribing sections ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). Community recipes show alternate SMTP provider setups, but they should be reviewed for current provider pricing, security, and analytics limitations ([AWS SES SMTP Transport](https://community.rockrms.com/recipes/171), [Mailtrap Email Testing](https://community.rockrms.com/recipes/138)).

### Email analytics

RockU includes Communication Analytics training ([Communication Analytics](https://community.rockrms.com/rocku/communication/communication-analytics)). The v18.1 documentation update says analytics were enhanced with charts and metrics for opens, clicks, and other engagement indicators ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). Communication Flow recipient metrics include opened date, clicked date, sent date, conversion date, and unsubscribe date ([recipient metrics source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowInstanceMessageMetrics/recipientMetricsBag.d.ts)).

Do not assume analytics exist for every email path. A community Q&A reports a scenario where Mailgun tracking worked for Communication Wizard emails but not workflow emails, with no answers in the source pack ([Mailgun Tracking Q&A](https://community.rockrms.com/ask/using/2824)). For such cases, verify:

- whether the workflow action creates a `Communication` record or sends a direct email
- whether communication tracking is enabled for that action
- whether the selected transport injects tracking links/pixels for that path
- whether provider webhooks post back to Rock
- whether Rock has recipient engagement data
- whether the email was sent through the same medium and transport as wizard emails

### Email preview and preheaders

A community recipe documents a Communication Wizard pattern for email preview/preheader content using an element with a `preheader-text` ID in the template ([Control Email Preview Contents](https://community.rockrms.com/recipes/179)). Treat it as a useful but non-official pattern. In a live instance, inspect the actual template HTML and wizard behavior before relying on it.

### View email on webpage

A community recipe describes rendering a communication on a webpage by passing a communication GUID and displaying its message with Lava ([View Email On Webpage](https://community.rockrms.com/recipes/297)). This can be useful for "view in browser" links but has security implications. Before implementing, verify:

- page security
- whether the communication GUID is sufficient access control
- whether message content contains sensitive personalized data
- whether `RunLava` is safe in that context
- whether SQL Lava is enabled only where appropriate
- whether unsubscribe and tracking behavior remains correct

### Email template design systems

A community recipe describes using an external email builder while keeping Rock as the communication and tracking system ([Empower Your Teams to Easily Create Beautiful Emails](https://community.rockrms.com/recipes/305)). The operational lesson is sound: template governance matters. If staff can freely paste inconsistent HTML, sender reputation, accessibility, branding, and mobile rendering suffer.

For production template systems:

- establish approved categories
- mark only high-use templates as starter templates
- restrict template edit rights
- review CSS inlining
- test Outlook, Gmail, mobile, and webmail rendering
- test Lava rendering for multiple recipient types
- preserve unsubscribe and organization footer requirements
- avoid unreviewed external scripts in email content

## 9. SMS Deep Dive

### SMS recipient eligibility

SMS eligibility is not just "person has a number." The recipient detail logic and view models separate `smsNumber` and `isSmsAllowed` ([CommunicationEntryRecipientBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts), [CommunicationEntryWizardRecipientBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardRecipientBag.d.ts)). The v17 migration explicitly fixed SMS eligibility logic in the recipient details stored procedure ([v17 migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)).

Inspect:

- phone number record
- phone type
- cleaned number
- SMS enabled flag
- opt-out state
- country/format provider support
- duplicate people sharing the same phone number
- communication recipient medium and status
- status note

### SMS opt-out and opt-in

Rock includes SMS opt-out processing. Source code shows `IdentifySmsOptOutCommunicationRecipientTransaction` attempts to associate an opt-out event with the most recent delivered SMS communication recipient in the last 60 days for people sharing the originating number. It then stamps unsubscribe date and sets unsubscribe level to all if a matching delivered recipient is found ([IdentifySmsOptOutCommunicationRecipientTransaction source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Transactions/IdentifySmsOptOutCommunicationRecipientTransaction.cs)).

This is explicitly best-effort behavior. If multiple people share a phone number or messages were sent from different contexts, agents must inspect actual person phone rows, person aliases, recipient records, and provider webhook payloads.

Release caveats:

- v18.1 fixed missing START/STOP keyword history in SMS Conversations when the SMS Pipeline includes the SMS Conversations action. If that action is not configured, the keywords remain omitted ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v18.2 fixed a registration issue where submitting a registration could disable SMS when `Show SMS Opt-In` was false. The fix preserves existing SMS values unless opt-in is shown and answered ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v19.1 includes a fix so bad-number errors from Twilio are not incorrectly treated as actual opt-outs ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### SMS conversations

SMS Conversations is the staff-facing conversation surface. RockU has SMS Conversations training ([SMS Conversations](https://community.rockrms.com/rocku/communication/sms-conversations)). Mobile docs provide SMS Conversation List configuration options, including allowed SMS numbers, personal-number filtering, non-personal-number hiding, conversation age, max conversations, database timeout, conversation page, and person search threshold ([Mobile SMS Conversation List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list)).

Operational checks:

- Is the inbound provider webhook reaching Rock?
- Is the SMS Pipeline active?
- Does the pipeline include the SMS Conversations action?
- Does the selected system phone number allow this staff person to view the conversation?
- Is the system phone number assigned to a person?
- Are block filters hiding the conversation?
- Is the conversation older than the configured months threshold?
- Is database timeout too low for the query?
- Are security rules on the block or page limiting access?

### Staff-specific texting numbers

A community recipe describes staff-specific Twilio numbers, separate SMS pipeline setup, system phone number assignment, and block-level security so staff see only their number while admins can see all ([Staff Specific Texting Numbers](https://community.rockrms.com/recipes/357)). This pattern is operationally useful because it combines privacy, accountability, and staff workflow. Before adopting it, verify:

- provider phone number ownership
- SMS capability
- system phone number setup
- assigned person
- page/block security
- pipeline actions
- after-hours expectations
- retention/audit policies
- child/youth safety policies
- whether calls to the texting number should forward, route to voicemail, or play a message

### Calls to SMS numbers

People may call SMS numbers. Community recipes document both voicemail and forwarding patterns for Twilio numbers ([Create a Voicemail Message](https://community.rockrms.com/recipes/224), [Use Your Twilio Texting Number for Incoming Calls](https://community.rockrms.com/recipes/507)). These are not core Rock behavior by default; they require provider voice configuration and often Lava webhook or Twilio configuration. In live work, inspect provider settings directly.

### SMS cost, segments, and encoding

SMS billing is provider-specific, but segment count and encoding are universal operational concerns. A community calculator recipe shows a local widget that estimates GSM-7 vs UCS-2 encoding, character count, credits per recipient, and total credits across recipients ([SMS Credit/Segment Calculator](https://community.rockrms.com/recipes/542)). Agents should check for:

- smart quotes
- emojis
- non-GSM characters
- long URLs
- personalization that changes length per recipient
- MMS attachments
- recipient count
- provider long-code throttling or campaign rules

### Disabled SMS warnings

A community recipe describes staff confusion when replies appear visually sent but are not delivered because the recipient's mobile phone is not SMS enabled ([Disabled SMS Mobile Phone Warning](https://community.rockrms.com/recipes/438)). Agents should always inspect `isSmsAllowed`, phone SMS enabled state, and recipient status rather than relying on UI impression alone.

## 10. Related Rock Areas: People, Workflows, Lava, Security

### People

Communications depend on Person and PersonAlias. Source recipients are built from Person records for known people and can be anonymous for raw email addresses or SMS numbers ([RockEmailMessageRecipient source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockEmailMessageRecipient.cs), [RockSMSMessageRecipient source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockSMSMessageRecipient.cs)). Recipient detail logic excludes deceased people in list and communication recipient paths ([recipient detail SQL source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql)).

Person checks:

- Is the person deceased?
- Is there a primary alias?
- Is email active?
- Is email preference set to allow bulk?
- Does the person have a mobile phone?
- Is SMS enabled?
- Are multiple people sharing one number?
- Are family members receiving through the expected adult/child rules?
- Does campus context filter the list or preference block?

### Workflows

Workflows can send emails, trigger communications, activate utility workflows, and create custom notification paths. Recipes show workflows used for first-gift emails, urgent prayer emails, Teams posts, quick replies, and system communication enhancements ([Automated First Gift Thank You](https://community.rockrms.com/recipes/133), [Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338), [Post to Teams From a Workflow](https://community.rockrms.com/recipes/435), [Quick Email Reply](https://community.rockrms.com/recipes/466)).

Agent workflow checks:

- Does the workflow send through a Rock communication action or a direct email action?
- Does it create `Communication` and `CommunicationRecipient` records?
- Does it support analytics?
- Which Lava commands are enabled?
- Which person alias is the sender/current person?
- Does it run under a system account?
- Does it bypass user approval policies?
- Are workflow type view permissions hardened in the current version? v19.1 release notes include workflow type security hardening in the broader release context ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### Lava

Lava is used in templates, system communications, workflow messages, shortcodes, webhooks, and custom blocks. Communication template detail models include `lavaFields`, and initialization comments note a convention where keys ending in `Color` indicate color picker values ([template initialization box](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailInitializationBox.d.ts)).

Community recipes demonstrate Lava in communication contexts, including giving receipt shortcodes, view-email web pages, external builder shortcodes, scheduling response customization, and Teams workflow activation ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510), [View Email On Webpage](https://community.rockrms.com/recipes/297), [Empower Your Teams](https://community.rockrms.com/recipes/305), [Decline Reason](https://community.rockrms.com/recipes/419), [Post to Teams](https://community.rockrms.com/recipes/435)).

Security warning: enabling SQL, Rock Entity, or `RunLava` in communication-facing blocks can expose data or execute expensive queries. Verify allowed Lava commands and page/block security before implementing recipes.

### Security

Communication security is layered:

- page security
- block security
- template security
- category security
- system phone number security
- communication list/group security
- communication detail access
- REST model security
- workflow type security
- Lava command permissions

The official manual notes template permissions and that users may not see templates without proper permission or wizard support ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). Communication Template List source includes options for whether the security column is visible and whether the current user can edit the block ([CommunicationTemplateListOptions source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateList/communicationTemplateListOptionsBag.d.ts)).

v19.1 adds a `Communication Access Mode` setting to Communication Detail and a `View All` security action. The default mode is `Strict`, limiting detail viewing to the creator/sender unless the viewer has `View All` ([Rock Release Notes](https://www.rockrms.com/releasenotes)). After upgrades, agents must verify communication detail pages for admins, communications staff, ministry staff, and approvers.

## 11. Administration And Operational Guardrails

### Governance

The official [Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8) manual defines the communication, template, transport, approval, preference, and saturation surfaces. Apply those controls to the target instance's actual roles, categories, transports, system phone numbers, and recipient policies before approving broad sends.

Use communication governance to prevent over-sending, inconsistent branding, privacy mistakes, and deliverability problems.

Recommended guardrails:

- Limit who can send to large lists.
- Require approval above recipient thresholds.
- Use starter templates for approved high-use designs.
- Restrict template edit rights.
- Maintain separate categories for ministry, finance, events, care, and general communications.
- Keep system communications under admin ownership.
- Use development transports that cannot reach real recipients.
- Review Lava commands enabled in blocks and templates.
- Audit system phone number access.
- Review saturation reporting before broad campaigns.
- Monitor bounces, unsubscribes, and opt-outs.

### Saturation and over-communication

RockU includes Communication Saturation Report training ([Communication Saturation Report](https://community.rockrms.com/rocku/communication/communication-saturation-report)). The v18.1 documentation update describes the report as a way to monitor recipients who may be overwhelmed by communication volume ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). Agents should use saturation data when asked whether a group is receiving too many emails or texts.

### Approval policies

Approval behavior depends on block configuration, security, maximum recipient settings, and version. Release notes mention improvements and fixes around `Send When Approved`, immediate queuing after approval, appropriate redirect after approval, and maximum-recipient auto-approval bugs ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Inspect:

- block settings for approval
- maximum recipients
- allowed communication types
- approver security
- communication status
- approval fields
- whether send is future-dated
- version-specific known bugs

### Template operations

For template lifecycle management:

1. Create templates in the official template admin surface.
2. Assign categories.
3. Mark only common templates as starter.
4. Add a preview image for recognition.
5. Configure email, SMS, and push fields intentionally.
6. Test CSS inlining.
7. Test Lava fields with multiple preview people.
8. Restrict edit permissions.
9. Verify wizard support.
10. Review after Rock upgrades, especially v17+ template version behavior and v18.3 special-character fixes.

### Lower environment safety

Never let development or staging accidentally email or text real people. Community Mailtrap guidance demonstrates the concept of trapping outbound email in a development inbox ([Mailtrap Email Testing](https://community.rockrms.com/recipes/138)). For SMS, use provider test numbers, inactive transports, or SMS test transport where appropriate. Confirm scheduled jobs are disabled or pointed to test transports.

## 12. Developer, API, Lava, And Source-Code Landmarks

### Transport components

- `Rock/Communication/EmailTransportComponent.cs`: email send preparation, validation, merge fields, async send behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/EmailTransportComponent.cs)).
- `Rock/Communication/Transport/SmsTest.cs`: SMS test transport, approved/due communication checks, pending recipient count, From number requirement, attachment handling ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/SmsTest.cs)).
- `Rock/Communication/Transport/EmailSendResponse.cs`: email transport response status and status note ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/EmailSendResponse.cs)).

### Recipient objects

- `RockEmailMessageRecipient`: wraps a person email or anonymous email address ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockEmailMessageRecipient.cs)).
- `RockSMSMessageRecipient`: wraps a person SMS number or anonymous SMS number ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockSMSMessageRecipient.cs)).

### Recipient detail stored procedure

`spCommunicationRecipientDetails` is a key SQL landmark. The v17 migration source says it fixes SMS eligibility logic and adds `GroupMember.CommunicationPreference` ([migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)). The SQL accepts communication list vs communication input, match type, and personalization segments, then returns data needed for the Communication Wizard ([SQL source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql)).

### Obsidian communication blocks

Relevant generated view models include:

- Communication Entry recipient request/recipient state ([request bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryGetRecipientsRequestBag.d.ts), [recipient bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts)).
- Communication Entry Wizard template and recipient bags ([template detail](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateDetailBag.d.ts), [template list item](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardCommunicationTemplateListItemBag.d.ts), [recipient bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntryWizard/communicationEntryWizardRecipientBag.d.ts)).
- Communication Detail recipient grid settings and personal template request ([recipient grid options](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/communicationRecipientGridOptionsBag.d.ts), [recipient grid settings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/communicationRecipientGridSettingsBag.d.ts), [personal template request](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts)).
- Communication Template Detail and Template List ([template detail](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateDetail/communicationTemplateDetailCommunicationTemplateBag.d.ts), [template list options](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationTemplateList/communicationTemplateListOptionsBag.d.ts)).
- Communication Flow templates and metrics ([flow template bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowDetail/communicationFlowDetailCommunicationTemplateBag.d.ts), [recipient metrics](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowInstanceMessageMetrics/recipientMetricsBag.d.ts)).

The Obsidian component structure documentation explains the general component file shape: template, imports, properties/events, and logic ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)). Use it when tracing or extending Obsidian communication blocks.

### REST endpoints

The v2 generated controller for Communication Recipients uses route prefix `api/v2/models/communicationrecipients` and secured read/write actions ([CommunicationRecipientsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/CommunicationRecipientsController.CodeGenerated.cs)). Flow instance recipients similarly expose `api/v2/models/communicationflowinstancerecipients` ([CommunicationFlowInstanceRecipientsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/CommunicationFlowInstanceRecipientsController.CodeGenerated.cs)).

When using APIs, verify current instance version, API availability, auth method, security actions, and whether model endpoints are appropriate for the task. For operational reads, prefer least-privilege access.

## 13. Reporting, Analytics, And Model Map

### Communication analytics

Modern communication analytics report opens, clicks, and other engagement indicators, with improvements noted in v18.1 documentation ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)). RockU includes a Communication Analytics module ([Communication Analytics](https://community.rockrms.com/rocku/communication/communication-analytics)) and a legacy module ([Communication Analytics Legacy](https://community.rockrms.com/rocku/communication/communication-analytics-legacy)).

Agent interpretation rules:

- Opens can be inflated or blocked by email clients.
- Clicks are stronger engagement signals than opens.
- Delivery does not mean read.
- Provider analytics and Rock analytics may differ.
- Workflow-sent emails may not behave like wizard-created communications.
- Flow analytics are not identical to one-off communication analytics.

### Saturation reporting

The Communication Saturation Report helps identify recipients receiving too much communication ([Communication Saturation Report](https://community.rockrms.com/rocku/communication/communication-saturation-report)). Use it for campaign governance and staff planning.

### Unsubscribe reporting

RockU's current playlist includes an Unsubscribe Report item in the communication section source excerpts ([RockU Communication](https://community.rockrms.com/rocku/communication)). When troubleshooting unsubscribes, inspect recipient unsubscribe fields, list subscription state, SMS opt-out handling, and provider-level suppressions.

### Model Map coverage

The Model Map confirms Communication category models:

- Communication
- Communication Attachment
- Communication Recipient
- Communication Response
- Communication Response Attachment
- Communication Template
- Communication Template Attachment
- Communication Flow
- Communication Flow Communication
- Communication Flow Instance
- Communication Flow Instance Communication
- Communication Flow Instance Communication Conversion
- Communication Flow Instance Recipient
- Email Section
- Notification Recipient
- Sms Action
- Sms Pipeline
- System Communication

Use Model Map for entity discovery, then verify relationships in source code, database schema, or a live Rock instance because the source pack's Model Map records are compact ([Model Map](https://community.rockrms.com/ModelMap)).

### Business Intelligence

RockU's BI Template training points to a Power BI template for Rock v7-era BI work ([BI Template](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template)). This source pack does not establish modern communication-specific BI model details. If asked for communication BI reporting, inspect the current Rock BI job output, available BI models, and whether Communication/CommunicationRecipient are included in the organization's extract.

## 14. Version And Release Caveats

### v17.x

v17 introduced a `Version` column on `CommunicationTemplate` and included recipient-detail stored procedure changes to fix SMS eligibility and include group-member communication preference ([v17 migration source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)).

v17.1 added a `Remove All` button to recipient modals in Simple Communication Entry and Communication Entry Wizard, useful when resetting copied communications ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

v17.4 fixed delays/errors preparing large communications with duplicate recipients by improving duplicate removal ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

v17.5 improved system notifications so certain messages check whether SMS is enabled before choosing SMS vs email ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### v18.1

v18.1 is a major communications release. It added Communication Flows, improved analytics, refreshed communication preferences, added saturation reporting, refreshed the communication list surface, and added an Obsidian Communication Detail block ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8), [Rock Release Notes](https://www.rockrms.com/releasenotes)).

v18.1 also fixed SMS START/STOP keyword history visibility when SMS Conversations action is included in the SMS Pipeline and improved approval/send-now queue behavior ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### v18.2

v18.2 fixed:

- approvers redirected to the correct page depending on whether communication was created in Simple Communication or Wizard
- recipient exclusion after changing communication type mid-wizard
- registration SMS opt-in preservation when `Show SMS Opt-In` is false

These are important when troubleshooting missing recipients, approval navigation, or registration-related SMS preference changes ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### v18.3

v18.3 fixed:

- allowed Communication Types enforcement in Obsidian Communication Entry Wizard when a communication is started externally, such as a grid `Communicate` action
- Communication Template saving failure when special characters in template names affected preview image file generation
- Simple Communication Entry error when sending a template without changes, according to release note excerpts

These caveats affect policy enforcement, template operations, and user-facing send errors ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### v19.1

v19.1 adds Communication Detail access control changes: `Communication Access Mode`, default `Strict` behavior, and a `View All` security action. This is high-impact because users who previously viewed communication details may lose access unless permissions are adjusted ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

v19.1 release notes also include a fix preventing bad-number Twilio errors from being incorrectly marked as opt-outs ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

## 15. Implementation Playbooks

### Playbook: Configure a safe email transport in development

1. Disable real production email transports or ensure they are not selected by the Email medium.
2. Configure a trap/test SMTP transport such as Mailtrap, following current provider documentation and Rock transport fields.
3. Set the Email medium transport container to the test SMTP transport.
4. Disable scheduled communication jobs unless testing scheduled sends.
5. Send a test communication to a real-looking recipient and verify it is captured, not delivered.
6. Inspect `CommunicationRecipient` status and provider inbox.
7. Document the lower-environment transport policy.

Community Mailtrap guidance demonstrates the pattern, but verify current credentials and settings in the live development instance ([Mailtrap Email Testing](https://community.rockrms.com/recipes/138)).

### Playbook: Build a governed template library

1. Inventory existing templates.
2. Create categories matching organizational ownership.
3. Remove or deactivate obsolete templates.
4. Set starter templates for the few most-used approved designs.
5. Add preview images for recognition.
6. Restrict edit/admin rights to communications admins or ministry owners.
7. Verify wizard support and template version.
8. Test email, SMS, and push fields where used.
9. Test Lava merge fields and CSS inlining.
10. Record owner, purpose, and last review date.

Use the official manual for category, starter, preview, and permission behavior ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).

### Playbook: Create or audit a communication list

1. Identify the group behind the list.
2. Confirm group type and security.
3. Confirm active group members.
4. Confirm whether the list is manually managed or synced.
5. If synced, inspect the data view and sync job.
6. Validate campus, age, membership, attendance, or giving criteria.
7. Check list subscriptions and member communication preference.
8. Test recipient preview with and without segments.
9. Compare list count to expected source count.
10. Document the membership source of truth.

Remember that shipped lists are not automatically synced ([Communication Lists & Segments](https://community.rockrms.com/rocku/communication/communication-lists--segments)).

### Playbook: Launch staff SMS conversations

1. Buy or assign provider numbers with SMS capability.
2. Create or verify system phone number records.
3. Assign numbers to staff where appropriate.
4. Configure SMS transport and provider webhooks.
5. Create or verify SMS Pipeline and SMS Conversations action.
6. Configure SMS Conversations page or mobile block.
7. Apply number-specific and block-specific security.
8. Test inbound, outbound, START, STOP, and bad-number behavior.
9. Decide what happens when someone calls the texting number.
10. Train staff to verify SMS enabled state and message status.

Use RockU for SMS pipeline/conversation orientation ([SMS Pipeline](https://community.rockrms.com/rocku/communication/sms-pipeline), [SMS Conversations](https://community.rockrms.com/rocku/communication/sms-conversations)). Staff-specific number and voice-routing recipes are useful patterns but must be security-reviewed ([Staff Specific Texting Numbers](https://community.rockrms.com/recipes/357), [Use Your Twilio Texting Number for Incoming Calls](https://community.rockrms.com/recipes/507)).

### Playbook: Implement a Communication Flow

1. Define the goal and measurable conversion.
2. Identify entry audience and exclusion criteria.
3. Choose channels per step: email, SMS, push.
4. Create flow-specific templates.
5. Define timing and delays.
6. Configure conversion triggers.
7. Test on internal people.
8. Verify analytics and recipient metrics.
9. Monitor saturation and unsubscribes.
10. Review after the first full cycle.

Communication Flows were added in v18.1 and track step progress and conversion signals ([Rock Release Notes](https://www.rockrms.com/releasenotes), [Communication Flows](https://community.rockrms.com/rocku/communication/communication-flows)).

## 16. Troubleshooting Decision Tree

### A communication did not send

1. Find the `Communication` record.
2. Check status: draft, pending approval, approved, sent, failed, or future-dated.
3. Check `FutureSendDateTime`.
4. Check approval state and approver permissions.
5. Check Communications Send Job state and history.
6. Check recipient rows: are there pending recipients?
7. Check medium entity type on recipients.
8. Check transport active/configured state.
9. Check exceptions and status notes.
10. Check version caveats for approval/send-now behavior.

### Some recipients are missing

1. Identify recipient source: list, communication, grid, entity set, workflow, connection requests.
2. If list-based, inspect group membership and active status.
3. Check deceased status.
4. Check segments and AND/OR match behavior.
5. Check duplicate removal.
6. Check email/SMS/push eligibility.
7. Check communication type changes during wizard authoring.
8. Check v18.2 recipient exclusion fix if the user changed communication type mid-wizard ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
9. Check v17 recipient detail behavior if on an older version.
10. Re-run recipient preview if available.

### Email delivered but analytics are missing

1. Confirm the send created `CommunicationRecipient` records.
2. Confirm it used the expected email medium.
3. Confirm transport supports analytics.
4. Confirm tracking is enabled for this send path.
5. Confirm provider webhooks/callbacks.
6. Confirm Rock has opens/clicks in the relevant analytics table or model.
7. Compare with a wizard-sent test email.
8. If workflow-sent, verify whether the workflow action path supports communication analytics. A community Q&A reports this exact difference for Mailgun but does not provide a confirmed fix in the source pack ([Mailgun Tracking Q&A](https://community.rockrms.com/ask/using/2824)).

### SMS reply is not visible

1. Check provider inbound webhook delivery.
2. Check SMS Pipeline.
3. Confirm SMS Conversations action is present.
4. Check system phone number.
5. Check conversation block filters and allowed numbers.
6. Check assigned person and personal-number filters.
7. Check conversation age/month limit.
8. Check page/block security.
9. Check v18.1 START/STOP keyword caveat ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### SMS recipient did not receive message

1. Check recipient `CommunicationRecipient` status and status note.
2. Check person's phone record.
3. Confirm mobile phone type.
4. Confirm SMS enabled state.
5. Confirm opt-out state.
6. Confirm bad-number provider errors.
7. Confirm From number and provider send logs.
8. Check whether the UI only appeared to send. Community experience shows staff can miss pending/failure state without stronger UI warnings ([Disabled SMS Mobile Phone Warning](https://community.rockrms.com/recipes/438)).
9. Check v19.1 bad-number vs opt-out fix if relevant ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### Template is missing from wizard

1. Check template active state.
2. Check category filter.
3. Check template permissions.
4. Check whether template supports the wizard.
5. Check template version.
6. Check block allowed communication types.
7. Check whether it is a Communication Flow template rather than a system-wide Communication Template.
8. Check whether the current user has edit/view rights, as the official manual notes templates may be hidden by permissions or setup ([Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8)).

### User cannot view communication detail

1. Check page and block security.
2. Check whether the user created or sent the communication.
3. Check Communication Detail `Communication Access Mode`.
4. Check `View All` security action in v19.1+.
5. Check whether strict access is expected.
6. Review release notes and tech bulletin for the current version ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

## 17. Agent Task Recipes

### Recipe: Audit a single sent communication

Collect:

- Communication ID/GUID
- created by
- sender fields
- subject/content summary
- communication type
- status
- future send date
- approval state
- template
- recipient count by status
- recipient count by medium
- failures with status notes
- unsubscribe count
- open/click metrics if available
- transport used
- job/exceptions if relevant

Report:

- whether it was sent
- who was eligible
- who failed and why
- whether analytics are available
- what to inspect next

### Recipe: Explain why a person did not get an email

Inspect:

- Person email
- email active
- email preference
- deceased status
- list membership
- subscription state
- recipient row
- medium entity type
- status/status note
- unsubscribe fields
- transport/provider logs
- bounce/suppression state

Answer in evidence form: "Person was in audience but excluded by preference", "Person was not in audience", "Person had pending recipient row but transport failed", or "Rock sent successfully; provider logs must be checked."

### Recipe: Explain why a person did not get SMS

Inspect:

- mobile phone exists
- SMS enabled
- opt-out state
- phone type
- cleaned number
- shared number
- recipient row
- status note
- From system phone number
- provider send log
- pipeline only if inbound/reply issue

Use source-code awareness that Rock models separate `smsNumber` from `isSmsAllowed` ([CommunicationEntryRecipientBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts)).

### Recipe: Audit communication list freshness

Inspect:

- list group ID/name
- group type
- member count
- active/inactive members
- sync job
- data view
- last sync time
- expected source population
- segment usage
- subscription/preference settings
- security

Flag if the list is one of Rock's shipped lists and no sync path exists, because RockU notes shipped lists are not automatically synced ([Communication Lists & Segments](https://community.rockrms.com/rocku/communication/communication-lists--segments)).

### Recipe: Review a communication template

Inspect:

- name
- category
- active
- starter
- version
- wizard support
- template security
- preview image
- from/reply/cc/bcc
- subject
- message
- SMS message
- push message/options
- attachments
- CSS inlining
- Lava fields
- logo/image references

Test:

- preview as multiple people
- send to internal test recipients
- mobile rendering
- unsubscribe link
- link tracking
- spam/deliverability signals if available

### Recipe: Investigate SMS conversation access

Inspect:

- system phone number
- assigned person
- block allowed numbers
- "show only personal" setting
- "hide personal" setting
- page security
- block security
- conversation age setting
- database timeout
- pipeline action
- inbound provider logs

Use mobile docs configuration names as the inspection checklist ([Mobile SMS Conversation List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list)).

### Recipe: Determine whether a workflow email supports analytics

Inspect:

- workflow action type
- whether a `Communication` record is created
- whether recipients are `CommunicationRecipient` rows
- selected medium/transport
- tracking setting
- provider tracking/webhook state
- comparison send through wizard
- recipient engagement rows

Do not promise analytics for workflow emails unless confirmed in the live instance. The source pack includes an unanswered community question showing this can differ by path ([Mailgun Tracking Q&A](https://community.rockrms.com/ask/using/2824)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `152`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | release_caveat | The v19 Unsubscribe Report can show recipient, send and unsubscribe timing, communication type or topic, and sender. Use it to investigate patterns and coach senders rather than assuming every unsubscribe has one cause. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |
| official | release_caveat | Selected v19 connection requests can be reassigned, moved to another status, completed, updated by state, sent to a workflow or activity, and used to initiate SMS or email. Each action remains subject to configured templates, snippets, phone eligibility and user permissions. | [source](https://www.youtube.com/watch?v=7rxTGLLhlrU) |
| official | release_caveat | The v19 Communication Wizard distinguishes personal or need-to-know messages from bulk or marketing messages, and block settings can customize the labels and descriptions. Clear local wording helps senders choose the classification that protects audience trust and sender reputation. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |
| official | release_caveat | Agent capabilities are intended to be controlled at the individual tool level, allowing an organization to enable drafting while disabling sending, or to omit destructive tools such as delete operations. Tool availability and Rock permissions should both be treated as required controls. | [source](https://www.youtube.com/watch?v=dpYJiOAiJYM) |
| official | release_caveat | A v19 SMS Pipeline send action can save its response so the automated message appears in Communication History, the person's history and SMS Conversations. Enable this deliberately when auditability is needed and account for the additional retained communication history. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |
| official | release_caveat | Rock v19 adds workflow actions for sending a Rock Chat channel message or direct message. Verify Rock Chat configuration, recipient resolution, workflow security and delivery behavior before operational use. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |
| rocku-confirmed | operational_guidance | For staff training and operational readiness, Communication Lists & Segments should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-lists--segments) |
| rocku-confirmed | operational_guidance | The Communication Preferences RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-preferences) |
| rocku-confirmed | operational_guidance | For ministry process design, Communication Templates should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-templates) |
| rocku-confirmed | operational_guidance | The Communication Templates [Legacy] RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-templates-legacy) |
| rocku-confirmed | operational_guidance | The SMS Pipeline RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/sms-pipeline) |
| rocku-confirmed | operational_guidance | For reporting, analytics, and measurement, Communication Analytics [Legacy] should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-analytics-legacy) |
| More |  | 140 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `39`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Communication Analytics Transcript Insight](https://community.rockrms.com/rocku/communication/communication-analytics) | approved_for_public_distillation | 3 | media-insight:e08bd9ab6c410d25 |
| [Communication Analytics [Legacy] Transcript Insight](https://community.rockrms.com/rocku/communication/communication-analytics-legacy) | approved_for_public_distillation | 2 | media-insight:d1aacd14e5660e87 |
| [Communication Flows Transcript Insight](https://community.rockrms.com/rocku/communication/communication-flows) | approved_for_public_distillation | 3 | media-insight:349e6f04286e8cab |
| [Communication Lists & Segments Transcript Insight](https://community.rockrms.com/rocku/communication/communication-lists--segments) | approved_for_public_distillation | 3 | media-insight:387bdcba06ac8a09 |
| [Communication Overview Transcript Insight](https://community.rockrms.com/rocku/communication/communication-overview) | approved_for_public_distillation | 3 | media-insight:cb96416a43f75f86 |
| [Communication Preferences Transcript Insight](https://community.rockrms.com/rocku/communication/communication-preferences) | approved_for_public_distillation | 3 | media-insight:d0e322520f4ef2bc |
| [Communication Preferences [Legacy] Transcript Insight](https://community.rockrms.com/rocku/communication/communication-preferences-legacy) | approved_for_public_distillation | 3 | media-insight:424563b14f71f033 |
| [Communication Saturation Report Transcript Insight](https://community.rockrms.com/rocku/communication/communication-saturation-report) | approved_for_public_distillation | 3 | media-insight:5548c23004402975 |
| More |  | 31 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 18. Source Map And Dependency Notes

Primary official sources:

- [Communicating With Rock](https://community.rockrms.com/documentation/bookcontent/8): communication engine, sending, templates, mediums, transports, send job, unsubscribes, bounced mail, version update notes.
- [RockU Communication](https://community.rockrms.com/rocku/communication): training index for lists, templates, wizard, SMS conversations, preferences, analytics, pipeline, system communications, flows, overview, saturation, unsubscribe report.
- [Rock Release Notes](https://www.rockrms.com/releasenotes): v17-v19 communication fixes, features, access control changes, SMS opt-in/opt-out behavior, flows, analytics, detail blocks.

Key RockU modules:

- [Communication Lists & Segments](https://community.rockrms.com/rocku/communication/communication-lists--segments)
- [Communication Templates](https://community.rockrms.com/rocku/communication/communication-templates)
- [Communication Wizard](https://community.rockrms.com/rocku/communication/communication-wizard)
- [Communication Preferences](https://community.rockrms.com/rocku/communication/communication-preferences)
- [Communication Analytics](https://community.rockrms.com/rocku/communication/communication-analytics)
- [Communication Flows](https://community.rockrms.com/rocku/communication/communication-flows)
- [Communication Saturation Report](https://community.rockrms.com/rocku/communication/communication-saturation-report)
- [SMS Pipeline](https://community.rockrms.com/rocku/communication/sms-pipeline)
- [SMS Conversations](https://community.rockrms.com/rocku/communication/sms-conversations)
- [System Communications](https://community.rockrms.com/rocku/communication/system-emails)

Developer and source-code landmarks:

- [EmailTransportComponent](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/EmailTransportComponent.cs)
- [SmsTest Transport](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/SmsTest.cs)
- [EmailSendResponse](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/Transport/EmailSendResponse.cs)
- [RockEmailMessageRecipient](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockEmailMessageRecipient.cs)
- [RockSMSMessageRecipient](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Communication/RockSMSMessageRecipient.cs)
- [Identify SMS Opt-Out Recipient Transaction](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Transactions/IdentifySmsOptOutCommunicationRecipientTransaction.cs)
- [v17 Communication Template Version and Recipient Detail Migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)
- [spCommunicationRecipientDetails SQL](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP_spCommunicationRecipientDetails.sql)
- [Communication Recipient API Controller](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/CommunicationRecipientsController.CodeGenerated.cs)

Mobile and Obsidian docs:

- [Mobile Communication Blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication)
- [Mobile Communication Entry](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry)
- [Mobile Communication List Subscribe](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe)
- [Mobile SMS Conversation List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list)
- [Mobile Communication View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-view)
- [Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)

Community examples requiring review before implementation:

- [Mailtrap Email Testing](https://community.rockrms.com/recipes/138)
- [AWS SES Email SMTP Transport](https://community.rockrms.com/recipes/171)
- [Control Email Preview Contents](https://community.rockrms.com/recipes/179)
- [View Email On Webpage](https://community.rockrms.com/recipes/297)
- [Empower Your Teams to Easily Create Beautiful Emails](https://community.rockrms.com/recipes/305)
- [SMS Credit/Segment Calculator](https://community.rockrms.com/recipes/542)
- [Disabled SMS Mobile Phone Warning](https://community.rockrms.com/recipes/438)
- [Staff Specific Texting Numbers](https://community.rockrms.com/recipes/357)
- [Create a Voicemail Message for Twilio SMS Accounts](https://community.rockrms.com/recipes/224)
- [Use Your Twilio Texting Number for Incoming Calls](https://community.rockrms.com/recipes/507)
- [Unread SMS Badge](https://community.rockrms.com/recipes/520)
- [Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510)
- [Decline Reason in Scheduling Response Email](https://community.rockrms.com/recipes/419)
- [Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)
- [Post to Teams From a Workflow](https://community.rockrms.com/recipes/435)

Dependency notes:

- **People**: recipient identity, aliases, deceased status, email preference, phone/SMS state.
- **Workflows**: automated sends, direct email actions, system communications, utility notifications.
- **Lava**: personalization, templates, shortcodes, webhooks, custom reporting, and significant security risk when SQL/Rock Entity/RunLava are enabled.
- **Security**: template visibility, communication detail access, phone number access, block/page access, model API access, workflow type visibility, and v19.1 `View All` behavior.

Review status: this guide should be validated against a live Rock instance before operational use, especially for version-specific behavior, provider transport settings, analytics support, SMS opt-in/out behavior, and security configuration.
