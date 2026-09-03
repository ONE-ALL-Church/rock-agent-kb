---
id: authored-communications
title: Communications
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "51f9d38672cb5339f187f347aae78be183e7155702794c00c21315cb7fc6d17f"
---

# Communications

## Agent Summary

Treat every communication as a governed operation with six independently verified parts:

1. **Audience** — the intended people, the source of that audience and each recipient’s eligibility.
2. **Sender** — the visible identity, reply path, authorized operator and applicable sender domain or phone number.
3. **Message** — the approved template or content, rendered personalization, links and attachments.
4. **Channel** — email, SMS or another enabled medium connected to the correct transport.
5. **Consent and classification** — personal versus bulk treatment, list membership, medium preference and opt-out state.
6. **Evidence** — the communication record, recipient outcomes, provider-reported events and any required approval.

Rock’s v19 documentation covers preparation, email, SMS, sending, preferences and reports as connected parts of one communication system. Do not validate only the editor screen and assume the rest is ready. [Communications documentation](https://community.rockrms.com/documentation/engagement/communications)

For operational work, verify the audience, sender, template, channel, consent and reporting behavior in the installed Rock environment before acting on broad training or community advice. Email safeguards also belong to governance and deliverability: review sender policy, access, templates and version-specific behavior together. [Approved claim `claim:33cbfdb2d0556acc66ff` — Rock Communication](https://shows.acast.com/rock-cast/episodes/5ae33294443021c473c0f5fa) [Approved claim `claim:21e74a6bcebdab9c194a` — Email Safeguards](https://shows.acast.com/rock-cast/episodes/episode-168-rocking-security-navigating-new-features-and-ema)

A successful save, preview, approval or provider handoff is not proof that every intended recipient received the message. Completion requires the appropriate readback: communication status, recipient-level results, provider events when available and a representative real inbox or device test.

## Scope And Boundaries

This guide owns the operational path from audience selection through delivery reporting for email and SMS. It includes communication lists, templates, system communications, transports, mediums, the Communication Wizard, the Simple Editor, approval, preferences, flows, SMS Conversations, the SMS Pipeline and communication reports. Those are the major surfaces identified by the v19 communications documentation. [Communications documentation](https://community.rockrms.com/documentation/engagement/communications)

Related concepts remain in their own guides:

- **People** owns person records, aliases, email and phone data quality.
- **Groups** owns group membership and Group Sync mechanics.
- **Data Views and Reports** owns targeting-query design.
- **Workflows** owns workflow lifecycle, actions and processing.
- **Lava** owns merge logic and safe rendering.
- **Security and Permissions** owns authorization design.
- **Learning Management** owns programs, courses, classes and training completion.
- **Connections** owns connection-request state and follow-up.
- **Mobile** owns Rock Mobile and push-notification configuration.

This guide may describe how those concepts affect communications, but it does not reproduce their full configuration.

The evidence pack primarily documents Rock v19. Version-specific statements are labeled. Community recipes are optional patterns requiring local review and testing; they are not core Rock guarantees. Public source-code excerpts describe implementation at an immutable commit and do not establish an installation’s version, configuration or behavior.

## Mental Model

A Rock communication is more than message content. An agent should reason through the following chain:

**Audience source → recipient eligibility → communication classification → medium → transport → provider or carrier → recipient event → Rock history and reporting**

A communication list is a group of a specific type. Its members can be maintained manually or synchronized from a Data View through Group Sync. The sender then chooses recipients, a medium and usually a template. The medium supplies channel-level rules and points to a transport; the transport hands the message to a delivery provider. Rock stores communication and recipient context, while available delivery and engagement evidence depends on what the transport reports back. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) [Communication Mediums](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-mediums) [Communication Transports](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-transports)

Recipient eligibility is channel-specific. A supplied v19 source snapshot shows the communication-entry recipient model carrying separate values for email preference, bulk-email allowance, active email state, email allowance, SMS allowance, push allowance and the selected SMS number. This is implementation evidence that “the person exists in the audience” and “the person is eligible for this channel” are different questions. [Rock source at `471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts)

Reporting is also layered. A communication can have a Rock status and recipient records while open, click, bounce, spam or unsubscribe details remain incomplete because the provider integration or webhook is not reporting them. Link delivery evidence back to the Rock communication and person context when possible, then summarize provider events into staff-facing operational reports without exposing unnecessary raw event data. [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics) [Approved claim `claim:fb85d514f4ed765acad4` — provider events and Rock context](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) [Approved claim `claim:cd52138ec6ca3848cae9` — operational reporting](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5)

## Communication Foundations

Before testing content, establish the installed communication foundation:

1. Confirm the Rock version and whether the page uses the current wizard, Simple Editor or a legacy surface.
2. Confirm the required communication medium is active.
3. Confirm that medium points to the intended active transport.
4. Confirm provider credentials and webhook configuration without exposing credentials.
5. Confirm sender-domain or system-phone-number configuration.
6. Confirm page, block, template, list and approval permissions.
7. Confirm preference, unsubscribe and reporting surfaces.
8. Use a bounded test audience before any broad send.

Rock v19 exposes transports at `Admin Tools > Settings > Communication Transports`. Its documented built-in email transport choices include SMTP, Mailgun HTTP and SendGrid HTTP. SMTP testing also requires the server or service to permit relay from the Rock server. [Communication Transports](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-transports)

Communication Mediums at `Admin Tools > Settings > Communication Mediums` represent available methods and connect a medium to its transport. The v19 Email medium also contains settings for unsubscribe markup, non-HTML content, CSS inlining, the bulk threshold, an unsubscribe-request address, one-click unsubscribe and an alternate unsubscribe URL. Transport capabilities can limit features such as CSS inlining, so the presence of a medium setting does not prove that the selected transport implements it. [Communication Mediums](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-mediums) [Configure Email](https://community.rockrms.com/documentation/engagement/communications/email/configure-email)

## Audiences, Communication Lists And Segments

Rock communication lists are groups of a designated type. Inspect them at `Admin Tools > Settings > Communication Lists`. Because the list is a group, membership may be manual or maintained through Group Sync from a Data View. Recipient troubleshooting should therefore inspect both the group and its synchronization source rather than assuming that the current Data View result automatically equals current list membership. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) [Approved claim `claim:a774892d024b8bbe0560` — Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

Categories organize lists and participate in visibility. The v19 subscribe block can be restricted to selected categories; category security determines whether a person can see associated lists. Campus context can filter displayed lists, while an “always include subscribed lists” setting can preserve already-subscribed lists that campus filtering would otherwise hide. [Configure Communication List Subscriptions](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/configure-communication-list-subscriptions)

The v2 Communication Wizard changes older communication-segment behavior toward Personalization Segments. Existing Data Views may be used in that model, but the segment category must match the Personalization Segment Category selected in the block settings. Treat unexpected segment results as a version-and-block-configuration problem until those conditions have been checked. [Communication Lists — Segments](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

A reviewed community pattern recommends refreshing a Data View-backed list immediately before a send and comparing the resulting group count with the source result. It also recommends testing a personalized call-to-action with a representative valid person or alias. This is a useful preflight pattern, not a core guarantee: the source calculation, refresh mechanism and count comparison require local verification. [Community contribution: refresh and verify source count](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

## Templates And System Communications

Communication Templates provide reusable content for email, SMS and push. In v19 they can be categorized, marked as starter templates, given preview images and individually secured for View, Edit or Administrate access. A template missing from the wizard may be hidden by permissions or may not be configured for that wizard version. [Communication Templates](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-templates) [Communication Wizard](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-wizard)

The v19 template documentation distinguishes Legacy templates from a Beta template version. Legacy templates use HTML for email and have stated SMS/push limitations; the Beta option includes the drag-and-drop builder and additional capabilities. Do not convert, recreate or troubleshoot a template without first identifying its version and the editor that consumes it. [Communication Templates](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-templates)

System Communications are templates used for specific, commonly automated messages such as password-reset communications. They can support email or SMS, are maintained under `Admin Tools > Settings > System Communications`, must have a category and can have per-item security. Their preview can render against a selected person and, when applicable, a selected date; a test can then be sent to a supplied address. [System Communications](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/system-communications)

Do not treat a correct template preview as delivery proof. Preview verifies a chosen render context. Operational verification must separately cover the triggering action, actual recipient resolution, medium, transport and recorded result.

## Email

Rock sends email through a communication transport. The v19 documentation identifies Mailgun and SendGrid as included provider integrations and recommends a delivery service that can return information such as bounces, opens and clicks. Other integrations may be available through the Rock Shop, so installed provider support must be verified locally. [Intro to Email](https://community.rockrms.com/documentation/engagement/communications/email/intro-to-email) [Configure Email](https://community.rockrms.com/documentation/engagement/communications/email/configure-email)

For an email transport review, inspect:

- Whether the transport is active.
- Whether the Email medium points to it.
- Whether its sending domain matches the provider’s configured domain.
- Whether provider credentials and webhook-signing values are present.
- Whether open, click, unsubscribe, bounce and spam reporting are enabled where supported.
- Whether sender addresses comply with the configured safe-sender policy.
- Whether DNS and provider authentication are complete.
- Whether a representative message reaches real inboxes and returns the expected events.

Mailgun documentation notes that differing sender and From domains can produce “on behalf of” presentation and advises aligning the domains. It also documents separate Mailgun API and HTTP webhook-signing key fields for Rock 14.4, 15.4, 16.1 and later. SendGrid setup likewise requires its Rock transport, the Email medium assignment and provider-side event webhook configuration. [Email Integrations](https://community.rockrms.com/documentation/engagement/communications/email/email-integrations)

The Email medium can add unsubscribe behavior and classify messages as bulk based on a configured threshold. When Mailgun is used, Rock’s v19 Mediums documentation advises reviewing provider tracking settings so recipients do not receive duplicate unsubscribe options. [Communication Mediums](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-mediums)

Domain-authentication and inbox-logo work should be kept conceptually separate. A reviewed community distillation discusses SPF, DKIM, DMARC and BIMI-style branding as related sender-trust work, while emphasizing that logo display is not itself proof of deliverability. Provider requirements and mailbox behavior can change, so verify them against current provider documentation before implementation. [Community media insight: email logo branding](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW)

## SMS

Rock v19 SMS setup begins with a provider-backed phone number, an active SMS transport, the SMS medium assigned to that transport and a corresponding System Phone Number. System Phone Numbers are maintained at `Admin Tools > Settings > System Phone Numbers`; the documented settings include active state, SMS enablement, forwarding, an optional received-message workflow, a notification group and per-number security. [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms)

A person must opt in before being texted. Before sending, verify the intended audience’s SMS eligibility and the selected sending number rather than assuming that a populated mobile phone field is sufficient. [Intro to SMS](https://community.rockrms.com/documentation/engagement/communications/sms/intro-to-sms)

Per-number security does not automatically transfer to SMS Conversations, the Communication Wizard or Simple Communication blocks. Review security on those surfaces separately. Communication History also carries a documented warning that the personalized history block does not respect SMS view access configured on the communication. Treat SMS content visibility as a cross-surface security review, not merely a phone-number permission. [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms) [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics)

### SMS Conversations

`People > Communications > SMS Conversations` provides a staff surface for starting and continuing conversations, filtering recipients, switching among active SMS numbers, adding notes or reminders and inserting SMS snippets. Incoming messages may arrive there directly or be routed there from the SMS Pipeline. [SMS Conversations](https://community.rockrms.com/documentation/engagement/communications/sms/sms-conversations)

When response-recipient forwarding is enabled, Rock can relay a response to the assigned person’s mobile number with a response code. A reply containing that code can be matched back to the original conversation. Verify the assigned response recipient, their valid SMS number and the correct handling of response codes before relying on this workflow. [SMS Conversations](https://community.rockrms.com/documentation/engagement/communications/sms/sms-conversations)

### SMS Pipeline

The SMS Pipeline is the entry point for incoming SMS messages. Messages move through ordered actions whose filters determine whether an action runs. An action with no filters applies to every message that reaches it, so unfiltered actions require deliberate review. Supported documented patterns include sending a reply, routing to SMS Conversations and launching a workflow. [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline)

In v19, a pipeline send action can enable **Save Response**. When enabled, Rock retains the automated response as a Communication or Communication Response and exposes it in SMS Conversations, Communication History and the person’s history. Enable this when auditability is required, while accounting for the additional retained history. [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline) [Approved claim `claim:c8435f854b9e7075ab76` — v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=684s)

MMS delivery depends on carrier and device support. The documentation advises representative testing across carriers and phone types; it also documents provider attachment limits and configurable long-code throttling. Treat the configured rate and provider policy as local, time-sensitive conditions. [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms) [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline)

A community recipe for Rock 17.2 adds a browser-side SMS segment and credit estimator to the communication page. It explicitly describes its total as an estimate, not a provider quote, and depends on page DOM selectors and recipient-label wording. Use it only as an optional reviewed customization; validate encoding, segment calculation, current editor compatibility and provider billing independently. [Community recipe: SMS Credit/Segment Calculator](https://community.rockrms.com/recipes/542/sms-creditsegment-calculator-widget-qol)

## Sending, Classification And Approval

The Communication Wizard supports recipient selection, medium selection, templates, sender settings, message construction, scheduling and confirmation. The Simple Editor provides a smaller surface for direct communications and can start from a selected grid, Data View, group or manually entered recipients. [Intro to Sending](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/intro-to-sending) [Communication Wizard](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-wizard) [Simple Editor](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor)

For each send, verify:

1. The internal communication name and topic.
2. The recipient source and final eligible count.
3. The personal or bulk classification.
4. The enabled mediums.
5. The sender, From address or number and reply path.
6. The template and rendered content.
7. Links, images and attachments.
8. Duplicate-prevention behavior where contact details are shared.
9. Scheduled time and time-zone interpretation.
10. Approval status.
11. The test result.
12. The post-send recipient outcomes.

The v19 Communication Wizard distinguishes personal or need-to-know messages from bulk or marketing messages. Block settings can customize those labels and descriptions. Use local wording that helps senders classify messages consistently because the choice affects audience trust and sender reputation. [Approved claim `claim:809519cf51bf3b32119f` — v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=627s)

In the Simple Editor, bulk communications include an unsubscribe link and exclude people who have declined bulk email. If the bulk option is hidden, the documentation says the communication is being treated as bulk. The editor can also expose duplicate prevention so a shared email address or phone number receives one message rather than one per selected person. [Simple Editor](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor)

A test send renders merge fields using the first recipient while sending the result to the logged-in person. Therefore, a successful test proves only that specific render path; test representative recipients for important personalization branches. [Simple Editor](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor)

By default, v19 documentation says email communications to 300 or more recipients require approval, although the threshold is configurable in the applicable communication-entry block. Pending communications notify the `RSR - Communication Approvers` group by email and remain unsent until a person with approval access approves them. Approval access and notification membership are separate controls and should both be inspected. [Advanced Email](https://community.rockrms.com/documentation/engagement/communications/email/advanced-email)

## Preferences, Consent And Sender Reputation

Communication preferences are operational state, not merely a footer link. Rock v19 provides a static Communication Preferences mode and a link-driven Unsubscribe mode. Depending on configuration, a person can update their email address, change global email preference, manage list subscriptions and choose a medium preference for a list. Preference changes are recorded in person history. [Set Subscription Preferences](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/set-subscription-preferences)

The global email choices documented for v19 distinguish receiving all email, personal email without mass email and no email. Unsubscribe behavior can also operate at list, flow, bulk or global scope. Diagnose the exact scope before editing membership or interpreting a missing recipient. [Set Subscription Preferences](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/set-subscription-preferences) [Unsubscribe Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/unsubscribe-report)

The external Communication List Subscribe block is available under `Connect > Subscribe`. Its block settings control list categories, medium-preference display, campus-context filtering and whether already-subscribed lists remain visible despite campus filtering. A list being public is necessary for the documented public-list scenario but does not replace category, page and block authorization checks. [Configure Communication List Subscriptions](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/configure-communication-list-subscriptions)

Rock’s documentation recommends making unsubscribe easy, enabling one-click unsubscribe and processing requests promptly. Because mailbox-provider policies and legal obligations change, an agent should verify the organization’s current obligations with authoritative legal and provider guidance rather than treating an older threshold, deadline or penalty amount as permanently current. [Intro to Communication Preferences](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/intro-to-communication-preferences)

When Mailgun or SendGrid reports a spam complaint through the configured integration, Rock can inactivate the person’s email address and add a note documenting the complaint. This depends on the relevant provider webhook being configured. [Advanced Email](https://community.rockrms.com/documentation/engagement/communications/email/advanced-email)

## Communication Flows And Automation Boundaries

Communication Flows create sequences of email, SMS or push messages around a defined audience and goal. The documented v19 flow types are recurring, on-demand and one-time. Recurring flows rebuild their audience from a Data View for each scheduled instance; on-demand flows add people through events such as a workflow action; one-time flows run on a fixed schedule without recurrence. [Communication Flows](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-flows)

A flow can define conversion goals based on completed forms or workflows, joining a group or group type, completing a Step, completing a registration or entering a Data View. Each message can have its own delay and send time. A recipient can exit after the last message, an email open, an email click or conversion. Use the earliest meaningful exit condition to avoid continuing a sequence after its purpose has been achieved. [Communication Flows](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-flows)

Flow email templates are distinct from system-wide Communication Templates. Saving an email within a flow makes it available for flow use, not necessarily as a general communication template. Pausing a flow by making it inactive stops messages, new instances and conversion tracking until it is reactivated. [Communication Flows](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-flows)

Adjacent automation requires its owning concept’s controls:

- In v19, selected connection requests can initiate SMS or email alongside other bulk actions. The result still depends on templates, snippets, phone eligibility and user permissions. [Approved claim `claim:5eedd5acf0194a87c5ce` — v19 Connections](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=466s)
- Rock v19 adds workflow actions for Rock Chat channel and direct messages. Verify Chat configuration, recipient resolution, workflow security and delivery before operational use. [Approved claim `claim:f8380a3e786ab33df98f` — v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1056s)
- Agent integrations should be controlled at individual-tool level. Drafting can be enabled while sending remains disabled, and destructive tools can be omitted. Tool availability and Rock permissions are both required controls. [Approved claim `claim:903c8ff9b5d2590fd616` — RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)
- LMS completion can participate in group, Group Sync and workflow follow-up patterns. Training may include acknowledgements, required video, quizzes, uploads and facilitator-scored activities, so any resulting communication workflow must distinguish learner actions from staff review responsibilities. This is a community-reviewed integration pattern, not a universal LMS configuration. [Approved claims `claim:4bc0aee305fa6b1bd524` and `claim:882208fdf2bb82703931` — LMS Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

## History, Analytics And Deliverability Reporting

Communication History is available at `People > Communication Reports > Communication History` and can be filtered by medium, status, topic, date and other list settings. A person’s History tab also exposes communications associated with that individual. [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics)

A communication’s detail can show creator, approver, sender details, content, recipient list, channel variants and recipient-level outcomes. Duplicating a communication copies its stored recipient list; it does not rerun a dynamic source such as a Data View. Recalculate the audience when current membership matters. [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics)

Email Analytics summarizes opens, clicks, client usage and top links over selectable time windows. Unique-link counts record one click per recipient. These measures depend on data returned by the configured transport; missing or low analytics may represent missing provider tracking rather than low engagement. [Email Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/email-analytics)

The Communication Saturation Report can be filtered by date, Data View, connection status, medium and bulk status. Its chart, recipient and communication views help identify people receiving many messages and communications with broad reach. Use this as a targeting and cadence diagnostic, not as an automatic rule that a specific count is excessive for every audience. [Communication Saturation Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-saturation-report)

The v19 Unsubscribe Report shows recent opt-outs and their scope, including list, flow, bulk or all-email outcomes. The `All` filter means global unsubscribes, not every report row. Approved v19 evidence also identifies recipient, send and unsubscribe timing, communication type or topic and sender as useful investigative fields. Use patterns to coach senders; do not assign a single cause to every unsubscribe. [Unsubscribe Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/unsubscribe-report) [Approved claim `claim:147ee6dbc7db220dc7ba` — v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=714s)

A reviewed community Helix pattern separates a communication-history filter shell from its results endpoint, allowlists enum values and page sizes, parameterizes text search, pages before calculating recipient aggregates and keeps message bodies and recipient-level details out of the initial staff view. This is an optional community design requiring local security, performance and live-data verification. [Community contribution: Communication History Active Search](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/communication-history-active-search)

## Version And Authority Caveats

Most official documentation in this pack targets Rock v19.0. Verify the installed version, block generation and transport/plugin versions before applying a path or setting exactly as written.

Version-specific evidence includes:

- **v17 implementation:** An immutable migration adds a `Version` column to `CommunicationTemplate` and changes communication-recipient detail logic. This is implementation evidence, not proof that an installation has applied the migration. [Rock source at `471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202504021715459_AddVersionToCommunicationTemplateAndFixRecipientDetailsSP.cs)
- **v18.2:** Release notes say approvers are redirected to the editor appropriate to the communication’s original creation surface. Earlier versions may exhibit the old redirect behavior. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- **v18.3:** Release notes say template names are sanitized when producing preview images, fixing failures caused by unsupported special characters. Confirm patch level when reproducing that symptom. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- **v19:** The pack’s approved release claims cover personal-versus-bulk classification, the Unsubscribe Report, optional SMS Pipeline response retention, connection-request communication actions and Rock Chat workflow actions.
- **v19.5:** The supplied release-note excerpt reports fixes for the wizard medium picker, Mailgun HTTP plain-text bodies, Chat workflow actions without attachments, drafts with no recipients and Internal Communication View paging. These fixes should not be assumed on earlier v19 patch levels. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- **v20.0 alpha:** The supplied release notes identify v20 as alpha and describe improved SMS opt-out association, a Create Connection Request pipeline action and Communication List selection in the Simple Communication Entry block. Do not present these as stable v19 behavior. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

The supplied v20-oriented source snapshot shows an SMS opt-out transaction attempting to associate an opt-out with the most recent delivered SMS recipient record within 60 days for people who may share the originating number. The source comments describe this as best effort and potentially imperfect. This implementation observation must not be generalized to v19 or treated as infallible attribution. [Rock source at `471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Transactions/IdentifySmsOptOutCommunicationRecipientTransaction.cs)

Legacy RockU communication analytics material may still provide training context, but it is explicitly labeled legacy. Confirm the current replacement surface before using its implementation instructions. [Communication Analytics — Legacy](https://community.rockrms.com/rocku/communication/communication-analytics-legacy)

## Troubleshooting Decision Tree

### Intended recipients are missing or shown as ineligible

1. Confirm the original audience source: manual selection, grid, communication list, Data View, group or stored communication.
2. If it is a communication list, inspect the underlying group and its current active membership.
3. If membership is synchronized, confirm the Group Sync source and last successful refresh.
4. Check whether Personalization Segments, category settings or match behavior reduce the audience.
5. Inspect the person’s email or SMS eligibility, bulk preference, list membership and medium preference.
6. Check whether the person is deceased, inactive for the relevant address or otherwise excluded by the current recipient logic.
7. Verify the selected medium and sending number.
8. Compare the final eligible count with the intended source count.
9. Stop before sending if unexplained differences remain. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) [Simple Editor](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor)

### Email appears sent but delivery or analytics are missing

1. Locate the communication in Communication History and inspect recipient statuses.
2. Distinguish pending, failed, delivered and interacted records.
3. Confirm the Email medium points to the intended active transport.
4. Inspect provider-side acceptance and delivery events without exposing credentials or raw recipient data.
5. Verify bounce, open, click, unsubscribe and spam webhooks or tracking options.
6. Check whether the transport supports the expected analytic event.
7. Send a bounded test to representative mailbox providers.
8. Stop when the Rock record, provider event and test inbox establish where the chain breaks. [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics) [Email Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/email-analytics)

### Email shows an unexpected sender or “on behalf of” label

1. Inspect the communication’s From and Reply-To values.
2. Confirm the sender domain permitted by local policy.
3. Compare the visible From domain with the domain configured in the provider and Rock transport.
4. Verify provider-domain authentication and DNS state.
5. Retest with the exact production sender pattern.
6. Do not change DNS or transport credentials without authorized change control. [Email Integrations](https://community.rockrms.com/documentation/engagement/communications/email/email-integrations) [Configure Email](https://community.rockrms.com/documentation/engagement/communications/email/configure-email)

### Two unsubscribe options appear in an email

1. Inspect Rock’s Email medium unsubscribe HTML and one-click setting.
2. Inspect the provider’s tracking or unsubscribe insertion.
3. Determine which layer should own each visible option.
4. For Mailgun, compare the configuration with Rock’s instruction to avoid overlapping tracking behavior.
5. Send a new test and inspect both the header and body.
6. Stop when the unsubscribe path is clear, functional and not duplicated unintentionally. [Communication Mediums](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-mediums)

### A template is missing or cannot be saved

1. Confirm whether the editor expects a Legacy, Beta or flow-specific template.
2. Check template Active state, category and View/Edit permissions.
3. Confirm whether it is enabled for the current wizard or editor.
4. Check the Rock patch level.
5. If saving fails when the name contains special characters, determine whether the installation includes the v18.3 fix before applying a workaround.
6. Retest with a bounded copy; do not overwrite a production template merely to diagnose visibility. [Communication Templates](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-templates) [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### A communication remains pending approval

1. Confirm whether its recipient count triggered the configured approval threshold.
2. Inspect its `Pending Approval` status in Communication History.
3. Confirm the approver has block-level Approve permission.
4. Confirm the approval-notification recipients are members of `RSR - Communication Approvers`.
5. Inspect the configured approval System Communication and email transport.
6. If the approver lands in the wrong editor, check whether the installation predates the v18.2 redirect fix.
7. Do not bypass approval by recreating the communication on another surface. [Advanced Email](https://community.rockrms.com/documentation/engagement/communications/email/advanced-email) [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Incoming SMS does not reach the expected conversation or workflow

1. Confirm the provider number and public webhook URL target the intended Rock endpoint or pipeline.
2. Confirm the transport and System Phone Number are active and SMS-enabled.
3. Inspect the pipeline attached to the number.
4. Walk actions in order and inspect every filter.
5. Pay special attention to unfiltered actions because they execute for every message reaching them.
6. Confirm the workflow type, input mapping and security if an action launches a workflow.
7. Confirm forwarding, assigned recipient and notification settings separately.
8. Test with one controlled inbound message and verify the resulting conversation, workflow or reply. [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms) [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline)

### An automated SMS reply is absent from history

1. Confirm that the expected pipeline action actually executed.
2. Inspect whether **Save Response** is enabled on that action.
3. Check SMS Conversations, Communication History and the person’s History tab.
4. Confirm that the message was associated with the intended person.
5. If auditability is required, enable retention only through an authorized configuration change and account for the additional stored history.
6. Retest with one controlled message. [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline)

### SMS segments, cost or delivery differ from expectations

1. Inspect the final rendered message, not only the template text.
2. Check characters that may change encoding and segment count.
3. Confirm the final eligible recipient count.
4. Compare any local calculator result with the provider’s actual segmentation and billing rules.
5. Inspect provider throttling, attachment limits and delivery events.
6. Test representative carriers and device types for MMS.
7. Treat community calculators as estimates and revalidate them after editor changes. [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms) [Community recipe: SMS Credit/Segment Calculator](https://community.rockrms.com/recipes/542/sms-creditsegment-calculator-widget-qol)

### An unsubscribe appears unexpected

1. Determine whether the scope is list, flow, bulk or all email.
2. Identify the communication, sender, topic and relevant timing where the report provides them.
3. Review the person’s current preference and history.
4. Check recent saturation across channels.
5. Inspect whether the message was correctly classified and targeted.
6. Review provider complaint or unsubscribe events when available.
7. Coach from patterns across multiple records; do not assign motive from one event.
8. For v20 SMS opt-out attribution, account for the documented best-effort association behavior. [Unsubscribe Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/unsubscribe-report) [Communication Saturation Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-saturation-report)

## Agent Task Recipes

### Recipe: Preflight a broad email communication

**Outcome:** A reviewed draft whose audience, sender, classification, content, consent and delivery path are ready for the organization’s approval process.

1. Record the installed Rock version, editor surface and intended send time.
2. Identify the authoritative audience source and calculate its current result.
3. Refresh any synchronized communication-list group through its approved mechanism.
4. Compare source count, group count and final eligible-recipient count.
5. Investigate exclusions rather than adding people manually to force count alignment.
6. Confirm personal-versus-bulk classification.
7. Confirm From, Reply-To, sender domain, topic and template.
8. Preview representative personalization cases and every important call-to-action.
9. Send bounded tests to representative mailbox providers.
10. Confirm the transport, tracking and unsubscribe behavior.
11. Save as draft or submit for approval.
12. After authorization and sending, verify Communication History and recipient outcomes.

**Inspect:**

- List and Group Sync source
- Recipient exclusions
- Template version and permissions
- Medium and transport
- Unsubscribe path
- Approval threshold and status

**Do not assume:**

- A Data View reruns when an old communication is duplicated.
- Every selected person is eligible.
- A preview proves provider delivery.

**Stop when:**

- Counts do not reconcile.
- Sender identity is unclear.
- A required test or approval is missing. [Simple Editor](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor) [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics)

### Recipe: Diagnose one missing recipient

**Outcome:** A specific, evidence-backed reason the person was included, excluded or routed to a different medium.

1. Confirm the person belongs in the authoritative targeting result.
2. Confirm current membership in the communication-list group.
3. Inspect sync state and applicable segment filters.
4. Inspect the person’s email address, SMS number and channel-specific eligibility.
5. Inspect global email preference, list subscription and medium preference.
6. Confirm whether the communication was personal or bulk.
7. Confirm duplicate prevention did not consolidate a shared destination.
8. Inspect the stored recipient result for the communication.
9. Report the exact failing layer without changing consent or contact data.

**Do not assume:**

- Group membership equals email eligibility.
- A mobile number is SMS-eligible.
- Shared contact information should generate duplicate messages.

**Stop when:** The exclusion is explained or a data-owner decision is required. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) [Set Subscription Preferences](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/set-subscription-preferences)

### Recipe: Validate an email transport and its event loop

**Outcome:** A bounded test proves Rock-to-provider handoff, inbox delivery and expected event return.

1. Confirm the active Email medium and assigned transport.
2. Review transport configuration without copying secrets into notes.
3. Confirm the sending domain and safe-sender policy.
4. Confirm provider webhooks and selected tracking events.
5. Send a uniquely named test to a bounded recipient set.
6. Confirm the Rock communication and recipient records.
7. Confirm provider acceptance.
8. Confirm real inbox delivery.
9. Generate only the approved test events, such as an open or link click.
10. Confirm those events return to the corresponding Rock record.
11. Record which events the transport does and does not provide.

**Stop when:** Any layer is unverified; do not interpret missing analytics as recipient disengagement until tracking is proven. [Configure Email](https://community.rockrms.com/documentation/engagement/communications/email/configure-email) [Email Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/email-analytics)

### Recipe: Validate inbound SMS routing

**Outcome:** One controlled inbound message reaches exactly the intended conversation, reply or workflow path.

1. Confirm the provider number and Rock System Phone Number.
2. Confirm the SMS transport and medium.
3. Confirm the webhook targets the intended endpoint or pipeline.
4. Review pipeline actions and filters in execution order.
5. Review workflow inputs and security for any workflow-launch action.
6. Decide whether automated replies must be saved to history.
7. Send one controlled inbound message.
8. Verify the expected conversation, reply, workflow and retained history.
9. Confirm no unrelated action executed.
10. Repeat with one negative-filter case when routing depends on keywords.

**Do not assume:** An unfiltered action is harmless; it applies to every message reaching it.

**Stop when:** More than the intended path executes or the sender cannot be resolved safely. [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline) [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms)

### Recipe: Create a communication flow without over-messaging

**Outcome:** A version-appropriate flow with a current audience, measurable goal and explicit exit behavior.

1. Choose recurring, on-demand or one-time behavior.
2. Define the authoritative audience or activation event.
3. Define a measurable conversion goal supported by Rock.
4. Set the goal window and target.
5. Add only evidence-supported email, SMS or push messages.
6. Define the buffer and send time for each message.
7. Choose when recipients exit.
8. Verify consent and channel eligibility for each medium.
9. Test representative recipients and conversion paths.
10. Activate only after audience, timing and exit behavior are approved.
11. Monitor recipient logs, conversion and unsubscribe results.
12. Pause the flow if targeting or timing is wrong.

**Do not assume:** Flow templates and system-wide Communication Templates are interchangeable.

**Stop when:** A converted person would continue receiving unnecessary messages or the recurring Data View is not trusted. [Communication Flows](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-flows)

### Recipe: Investigate rising unsubscribes or saturation

**Outcome:** A bounded operational finding identifies affected audiences, senders or message patterns without over-attributing individual motives.

1. Select a consistent date window.
2. Review the Unsubscribe Report by scope.
3. Review saturation across the same window and mediums.
4. Identify recurring senders, topics, lists, flows or broad communications.
5. Inspect classification and targeting for representative messages.
6. Compare provider spam complaints where available.
7. Separate isolated events from repeated patterns.
8. Recommend a concrete audience, cadence, template or training adjustment.
9. Measure the same reports after the change.

**Do not assume:** Every unsubscribe has the same cause.

**Stop when:** The report lacks enough context to identify a defensible pattern. [Unsubscribe Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/unsubscribe-report) [Communication Saturation Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-saturation-report)

### Recipe: Retest a workflow-backed communication safely

**Outcome:** One intended communication action is exercised without broadly reopening unrelated workflow work.

1. Prefer a new test workflow instance.
2. If an existing marked test instance must be reused, preflight the exact recipient, action criteria, current template, action order and baseline side-effect counts.
3. Leave earlier setters, record-creation actions and unrelated communication actions complete.
4. Reopen only the target action and the minimum containing workflow state required by the reviewed procedure.
5. Save once through the supported Workflow Detail surface.
6. Inspect workflow logs and Communication History before considering any retry.
7. Verify exactly one intended communication, its recipient, rendered content and final workflow state.
8. Confirm no unrelated timestamps or records changed.

**Do not assume:** A workflow Status label alone determines activation.

**Stop when:**

- The recipient or template is uncertain.
- The instance is not clearly marked for testing.
- The first processing attempt has an unexplained result.
- A retry could duplicate an irreversible send.

This is a reviewed community pattern grounded in an immutable Rock source reference. It requires live verification and does not authorize direct database updates. [Community contribution: controlled workflow-action retest](https://github.com/SparkDevNetwork/Rock/blob/7d31f3f144c14b8a7d86bf7a41760d9d0a49fe07/Rock/Model/Workflow/Workflow/Workflow.Logic.cs)

### Recipe: Bound an agent that can draft communications

**Outcome:** An agent can assist with preparation without gaining unintended send or destructive authority.

1. List the exact communication tasks the agent needs.
2. Enable only the required tools.
3. Separate draft, preview, audience-inspection, approval and send capabilities.
4. Leave send disabled when the task is drafting or analysis.
5. Omit destructive tools unless explicitly required.
6. Verify the Rock identity and permissions used by the integration.
7. Test denied operations as well as allowed ones.
8. Require action-time authorization before any external send.

**Do not assume:** Hiding a user-interface control removes the underlying tool, or enabling a tool bypasses Rock permissions. [Approved claim `claim:903c8ff9b5d2590fd616` — RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)

## Known Gaps And Live Verification

The evidence pack does not establish the configuration of any target Rock installation. Before operational use, verify:

- Installed Rock version and patch level.
- Wizard, Simple Editor and legacy block versions.
- Installed communication plugins and provider packages.
- Active mediums and their assigned transports.
- Provider credentials, DNS authentication, sender domains and webhooks.
- Current mailbox-provider and carrier requirements.
- Current legal requirements for email and SMS consent and opt-out handling.
- System Phone Numbers, routing URLs, forwarding and number-level security.
- Page and block security for SMS Conversations, Communication History, templates and approval.
- Group Sync schedules and current list membership.
- Personalization Segment categories and block settings.
- Local approval thresholds and approver membership.
- Duplicate-prevention configuration.
- Flow schedules, audiences, goals and exit conditions.
- Provider event retention and staff-facing report exposure.
- Real inbox, carrier and device behavior.

Reviewed read-only evidence associated with several approved claims confirmed that relevant communication, recipient, template, person-linkage, report, workflow, group and LMS structural surfaces existed in one examined environment. That supports the feasibility of the described inspections, but it does not prove another installation’s schema version, configuration, permissions, data quality or provider behavior.

No live send, inbox delivery, SMS exchange, workflow execution, provider-event callback or target-instance security review occurred as part of this guide. Those checks remain required wherever the operational conclusion depends on them.

The anonymous SMS verification contribution is also only a community pattern. Its proposed controls—one exact person match, a bounded server-side challenge, no alias exposure to the browser and atomic consumption before the protected action—require application-security review and live verification before adoption. [Community contribution: Workflow-Backed SMS Verification](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)

## Source Map

| Source | Authority and use |
| --- | --- |
| [Rock Communications documentation](https://community.rockrms.com/documentation/engagement/communications) | Official v19 section map for preparation, email, SMS, sending, preferences and reports. |
| [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) | Official v19 evidence for group-backed lists, Group Sync, categories and segments. |
| [Communication Templates](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-templates) | Official v19 evidence for template versions, categories, starter state and security. |
| [System Communications](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/system-communications) | Official v19 evidence for automated templates, categories, preview and security. |
| [Communication Transports](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-transports) | Official v19 evidence for transport purpose, built-in choices and SMTP relay caveat. |
| [Communication Mediums](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-mediums) | Official v19 evidence for medium activation, transport assignment, classification and unsubscribe settings. |
| [Configure Email](https://community.rockrms.com/documentation/engagement/communications/email/configure-email) | Official v19 email transport, tracking and safe-sender configuration context. |
| [Email Integrations](https://community.rockrms.com/documentation/engagement/communications/email/email-integrations) | Official provider-specific Mailgun and SendGrid configuration context. |
| [Advanced Email](https://community.rockrms.com/documentation/engagement/communications/email/advanced-email) | Official v19 approval and spam-reporting behavior. |
| [Configure SMS](https://community.rockrms.com/documentation/engagement/communications/sms/configure-sms) | Official v19 System Phone Number, provider, forwarding, workflow and throttling context. |
| [SMS Conversations](https://community.rockrms.com/documentation/engagement/communications/sms/sms-conversations) | Official v19 two-way conversation and response-forwarding behavior. |
| [SMS Pipeline](https://community.rockrms.com/documentation/engagement/communications/sms/sms-pipeline) | Official v19 inbound-routing, action-filter, workflow and response-retention behavior. |
| [Communication Wizard](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-wizard) | Official v19 wizard, template and message-building behavior. |
| [Simple Editor](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/simple-editor) | Official v19 direct-send, bulk, test, duplicate-prevention and scheduling behavior. |
| [Communication Flows](https://community.rockrms.com/documentation/engagement/communications/send-a-communication/communication-flows) | Official v19 flow types, goals, timing, exit behavior and analytics. |
| [Set Subscription Preferences](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/set-subscription-preferences) | Official v19 preference, subscription and unsubscribe modes. |
| [Configure Communication List Subscriptions](https://community.rockrms.com/documentation/engagement/communications/communication-preferences/configure-communication-list-subscriptions) | Official v19 subscribe-block, category, campus and medium-preference behavior. |
| [Communication History & Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-history-analytics) | Official v19 communication, person-history, recipient and security context. |
| [Email Analytics](https://community.rockrms.com/documentation/engagement/communications/communication-reports/email-analytics) | Official v19 provider-dependent open, click and client reporting. |
| [Communication Saturation Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/communication-saturation-report) | Official v19 cadence and audience-load reporting. |
| [Unsubscribe Report](https://community.rockrms.com/documentation/engagement/communications/communication-reports/unsubscribe-report) | Official v19 unsubscribe scope and investigation context. |
| [Rock Core Release Notes](https://www.rockrms.com/releasenotes) | Official version-specific fixes and alpha release caveats. |
| [v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ) | Approved official release claims for classification, SMS response retention, unsubscribe reporting and Rock Chat actions. |
| [Rock source snapshot](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3) | Immutable implementation evidence; not proof of installed configuration. |
| [Email Safeguards](https://shows.acast.com/rock-cast/episodes/episode-168-rocking-security-navigating-new-features-and-ema) | Community-reviewed governance guidance with a reviewed public-safe structural verification conclusion. |
| [SMS Credit/Segment Calculator](https://community.rockrms.com/recipes/542/sms-creditsegment-calculator-widget-qol) | Community recipe and estimate; not official provider billing behavior. |
| [ONE&ALL public communication recipes](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes) | Reviewed community implementation patterns requiring local security and live verification. |