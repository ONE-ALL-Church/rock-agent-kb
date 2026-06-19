---
id: authored-prayer-care
title: Prayer And Care
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Prayer And Care

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Prayer And Care index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Prayer and care work in Rock RMS sits at the intersection of sensitive personal data, public-facing ministry intake, volunteer participation, moderation, communications, reporting, and sometimes pastoral follow-up workflows. The core Rock feature is the Prayer Request model and its related blocks, pages, categories, comments, approval flags, privacy controls, and prayer-team experiences. The surrounding care system is broader: churches often connect prayer requests to people records, groups, communications, workflows, notes, connection follow-up, mobile surfaces, and external pastoral-care processes.

Agents working on prayer and care should treat every request as potentially sensitive. A prayer request may contain medical details, family conflict, abuse disclosures, crisis language, missionary names, children’s names, addresses, immigration details, or other details that should not be broadly exposed. Rock’s prayer tools support public and private request handling, approval, comments, flagging, categories, group-scoped prayer, prayer counts, request expiration, urgent requests, and prayer-team interfaces. However, local configuration determines the actual behavior in any instance. Always inspect the live block settings, security actions, categories, system jobs, system communications, and workflow configuration before making operational claims.

The main operational flow is:

1. A person submits a prayer request through a Prayer Request Entry surface, commonly on the external site under `Connect > Prayer`, or an administrator enters one internally under `People > Prayer > Add Prayer Request` as described in the official [Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0) documentation.
2. The request is stored as a Prayer Request, associated with submitter information when available, optionally tied to a campus, category, group, custom attributes, approval status, public visibility, comments, urgency, expiration, and prayer count. The model is identified in the [Model Map](https://community.rockrms.com/ModelMap) as a Prayer-category model.
3. A prayer administrator reviews unapproved, flagged, urgent, or otherwise sensitive requests under `People > Prayer`, using list filters and detail views. The official [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0) documentation frames this as the main administrative workspace.
4. Prayer team members pray through a Prayer Session or Prayer Card View experience. Rock’s [Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0) documentation describes category selection, active-request queues, urgent ordering, and least-prayed-first ordering. The [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0) provides a card-based alternative that ships with Rock but is not placed on a page out of the box.
5. Prayer comments can be sent back to the requestor through the Send Prayer Comments job and the Prayer Request Comments Digest system communication, described in [Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0) and [Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication?Version=v19.0).
6. For group-scoped prayer, a request can be attached to a group. The official group-prayer articles explain that group prayer depends on a `GroupGuid` URL parameter and that, when the parameter is present, prayer blocks show only requests associated with that group; without the parameter, group-associated requests are excluded from normal prayer sessions ([Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0), [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests?Version=v19.0)).
7. Newer Rock versions add Obsidian, mobile, and AI-related capabilities. Release notes identify Prayer Automations in v17.0, mobile custom attribute editing for prayer requests in v17.0, a v17.0 public-attribute visibility fix in the Obsidian Prayer Request Entry block, v17.2 PersonId URL prefill support, v17.5 approval-field fixes, v18.3 campus type filtering for the campus picker, and v19.1 Prayer Request List readability improvements ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

For agents, the highest-risk areas are public visibility, auto-approval, prayer team access, comment digest email content, group-scoped leakage, custom attribute exposure, AI formatting of sensitive details, and workflows that send urgent or pastoral-care communications. When uncertain, inspect rather than infer.

## 2. Scope And Terminology

This guide covers prayer and care concepts in Rock RMS. It focuses on:

- Prayer request intake, review, approval, expiration, and visibility.
- Prayer categories and group-scoped prayer.
- Prayer administrators and prayer team roles.
- Prayer sessions, card-based prayer, prayer counts, comments, and answers.
- Comment digest communication back to requestors.
- Care-adjacent workflows, including urgent prayer email, SMS intake, prayer walls, live prayer chat, and pastoral-care summary patterns from community examples.
- Related areas: people, groups, communications, workflows, security, CMS, mobile, reporting, Lava, REST, source-code landmarks, and release caveats.

The main Rock terms are:

- **Prayer Request**: The core entity representing a submitted prayer need. Source-code view models expose fields such as `Text`, `FirstName`, `LastName`, `Email`, `Campus`, `Category`, `Group`, `IsPublic`, `IsApproved`, `IsUrgent`, `IsActive`, `ExpirationDate`, `AllowComments`, `PrayerCount`, `FlagCount`, `Answer`, `RequestedByPersonAlias`, `ModerationFlags`, `OriginalRequest`, and `Sentiment` in the Obsidian detail surface ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs), [prayerRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts)).
- **Requester / Requestor**: The person submitting the prayer request or the person for whom the request is being made. Rock’s workflow action uses a `Requestor` setting and separate first-name, last-name, and email inputs for cases where the person is not resolved to a Rock person record ([PrayerRequestAdd.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs)).
- **RequestedByPersonAlias**: The person-alias link back to the person who submitted or is associated with the request. Reporting filters use `RequestedByPersonAlias.PersonId` to find requests involving selected people ([ContainsPeopleFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs)).
- **Prayer Administrator**: A staff or volunteer role responsible for entering offline requests, reviewing unapproved or flagged requests, and maintaining the prayer-request queue. The official role article names entering card-submitted requests and reviewing flagged or unapproved requests as core responsibilities ([Prayer Team Roles](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)).
- **Prayer Team**: People who pray for requests and flag requests that need administrative review. Rock’s official role article separates this from the administrator role ([Prayer Team Roles](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)).
- **Category**: A Rock category used to organize prayer requests. Official docs say web-submitted requests default to General unless another category is selected, and administrators can assign categories during review ([Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0)).
- **Approval**: A request may need approval before it appears to the prayer team, unless the intake surface is configured to auto-approve. Verify the current block settings and approval-security actions in the live instance.
- **Public**: A visibility flag that controls whether a request is suitable for public display in relevant list or wall experiences. Public does not mean safe by itself; it means a configured surface may include it. Inspect every output block and Lava template before assuming what public means locally.
- **Flagged Request**: A request that a prayer team member has flagged for administrator review. Official docs present flagging as a way to handle inappropriate wording, sensitive details, crisis disclosures, or other content that should be reviewed ([Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests?Version=v19.0)).
- **Prayer Count**: The count of times a request has been prayed for. Prayer Session and Prayer Card View workflows increment prayer activity through the block experience; community prayer-wall recipes may also update this count, but direct SQL or custom webhooks require careful review ([Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0), [Create a Prayer Wall](https://community.rockrms.com/recipes/149)).
- **Comments**: Notes or comments attached to a prayer request. Some surfaces allow prayer team members to add comments; comment-digest jobs can email those comments back to the requestor ([Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0)).
- **Answer**: A single answer field on a Prayer Request. A community recipe notes that Prayer Request has one answer field rather than many answers, which can matter when building external answer-entry surfaces ([Prayer Card View - Add Answered Prayer](https://community.rockrms.com/recipes/389)).
- **Group Prayer Request**: A prayer request associated with a group. Official docs say group-scoped prayer is controlled by the group GUID in the URL and that standard prayer sessions exclude group-associated requests unless the `GroupGuid` parameter is present ([Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests?Version=v19.0)).
- **Care Follow-Up**: Not a single core Prayer feature. It usually means local workflows, person notes, group tasks, connection requests, communications, pastoral-care plugin records, staff follow-up, or care-team processes connected to prayer intake. Community recipes illustrate patterns, but each should be verified and adapted.

## 3. Prayer And Care Mental Model

Think of prayer and care as four connected layers.

The first layer is **intake**. A request enters Rock from an external website block, internal staff entry, mobile block, workflow action, SMS pipeline, imported workflow, or custom integration. The default public site path in official docs is `Connect > Prayer`, and internal administrators can use `People > Prayer > Add Prayer Request` ([Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0)). Intake captures the request text and optionally the requestor’s name, email, phone, campus, category, urgency, public visibility, comments preference, custom attributes, and related person or group.

The second layer is **triage**. This is where privacy and care quality are won or lost. A request may be auto-approved or held for approval. It may be public or private. It may contain details that need editing, redaction, escalation, pastoral contact, or removal from public prayer surfaces. Official docs call out the reason for flagging: public submissions can include dangerous, inappropriate, or crisis-related details, and prayer team members need a way to alert administrators ([Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests?Version=v19.0)). In live operations, triage should also check for duplicate submissions, requests that belong to a group or care team, requests from minors, requests involving abuse or self-harm, and requests that should be handled by pastoral staff rather than general prayer volunteers.

The third layer is **prayer-team execution**. Prayer team members need a low-friction way to pray through current requests. The Prayer Session block uses categories and request ordering; official docs say urgent requests are presented first, followed by remaining requests from least-prayed-for to most-prayed-for ([Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0)). The Prayer Card View block shows requests as cards and counts prayer when a person clicks Pray; it ships with Rock but is not added to an external page by default ([Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0)). Some churches extend card view with modals, comment pages, answer-entry pages, or public prayer walls, but those are local customizations and should be reviewed for security and privacy.

The fourth layer is **care closure**. Some requests end when they expire; some end when they receive enough prayer coverage; some require a pastor, staff member, group leader, or care team to follow up. Rock’s Prayer feature supports comments and comment digests, and community patterns show workflows that email urgent requests, receive SMS prayer requests, and send pastoral-care summaries. However, Rock’s core Prayer entity is not a full pastoral-care case-management system. For care closure, verify whether the instance uses workflows, connection requests, person notes, group member attributes, staff assignments, pastoral-care plugins, or external systems.

Agents should always ask: Where did this request come from? Who can see it? Has it been approved? Is it public? Is it attached to a group? Is there a requestor person record? Are comments enabled? Is there an email or phone number that will be used for follow-up? Has anything been sent externally? Is the request expired, active, answered, flagged, or urgent? Are local AI automations enabled?

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. **Live Rock instance configuration and current data** for local behavior. Block settings, security roles, category trees, workflows, jobs, system communications, and custom Lava decide how a real instance behaves.
2. **Official Rock documentation** for supported concepts and admin behavior. The primary official documentation entry is [Prayer](https://community.rockrms.com/documentation/engagement/prayer?Version=v19.0), with subpages for [Prayer Overview](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview?Version=v19.0), [Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests?Version=v19.0), and [Prayer Team Power Tools](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools?Version=v19.0).
3. **RockU training** for staff training and operational orientation. The [Prayer Requests RockU training](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) is useful for staff readiness, but verify implementation details against current documentation and local configuration.
4. **Release notes** for version-specific caveats. The [Rock Core Release Notes](https://www.rockrms.com/releasenotes) are especially important for v17-v19 prayer changes.
5. **Model Map and source-code landmarks** for entity shape, block view models, API surfaces, reporting selectors, workflow action settings, and mobile block options. Use the [Model Map](https://community.rockrms.com/ModelMap) and SparkDevNetwork/Rock source-code files as implementation references.
6. **Community recipes and Q&A** as examples, not authority. Recipes may include direct SQL, custom workflows, external services, old-version assumptions, or local IDs. Community recipe pages explicitly warn that recipes are contributed and may not follow best practices. Use them for design patterns, then re-implement safely in the target instance.

This guide cites source URLs inline. It does not replace reviewing live configuration. When a field or behavior is source-code-derived, treat it as a landmark for investigation, not proof that the specific block in a given Rock instance is configured to expose that field.

## 5. Core Configuration And Data Model

### Prayer Request Entry Configuration

The Prayer Request Entry block is the common public intake surface. Official docs say many users enter requests online through the external site under `Connect > Prayer`, while administrators can add requests internally under `People > Prayer > Add Prayer Request` ([Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0)).

Source-code view models show that the Obsidian Prayer Request Entry block initializes with configuration and default values including:

- `allowCommentsDefaultValue`
- editable public prayer-request attributes
- campus status and campus type filters
- selectable categories
- character limit
- default campus
- default category GUID
- default email
- default first name
- default last name
- default request text from the `Request` page parameter
- CAPTCHA support control
- whether Allow Comments is shown
- whether the page redirects to parent on save
- whether the page refreshes on save
- public default value
- whether requester info is shown
- whether the urgent field is shown
- navigation URLs
- parent page URL
- security grant token

These appear in the TypeScript and C# initialization models for the Prayer Request Entry block ([prayerRequestEntryInitializationBox.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntryInitializationBox.d.ts), [PrayerRequestEntryInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntryInitializationBox.cs)).

When auditing a live Prayer Request Entry page, inspect:

- The page route and block type.
- Whether requester info is shown or hidden.
- Whether first name, last name, email, mobile phone, and campus are required, optional, defaulted, or hidden.
- Whether category selection is shown.
- The default category.
- Whether `Is Public` is shown and its default value.
- Whether `Is Urgent` is shown.
- Whether `Allow Comments` is shown and its default.
- The character limit.
- CAPTCHA settings.
- Custom Prayer Request attributes and whether they are public.
- Save behavior: stay on page, refresh, redirect to parent, or custom success message.
- Whether a page parameter pre-fills the request text.
- Whether PersonId URL prefill is expected, especially on versions affected by the v17.2 release-note fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

The save request model confirms that saved public-entry data can include category GUID, first name, last name, email, mobile phone, mobile phone country code, campus GUID, request text, urgent flag, allow-comments flag, public flag, and custom attribute values ([PrayerRequestEntrySaveRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntrySaveRequestBag.cs), [prayerRequestEntrySaveRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveRequestBag.d.ts)).

### Prayer Request Detail Configuration

The Prayer Request Detail surface is the administrative detail view. Source-code landmarks show it exposes or handles:

- `AllowComments`
- `Answer`
- custom attribute values
- `Campus`
- `Category`
- `Email`
- `ExpirationDate`
- `FirstName`
- `FlagCount`
- `FullName`
- `Group`
- `IsActive`
- `IsApproved`
- `IsPublic`
- `IsUrgent`
- `LastName`
- `ModerationFlags`
- `OriginalRequest`
- `PrayerCount`
- `RequestedByPersonAlias`
- `Sentiment`
- `Text`

See [PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs) and [prayerRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts).

Detail options include settings such as whether last name is required and AI-disclaimer options in the Obsidian detail block view models ([PrayerRequestDetailOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestDetailOptionsBag.cs), [prayerRequestDetailOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestDetailOptionsBag.d.ts)).

When auditing detail behavior, verify:

- Who can view the detail page.
- Who can approve requests.
- Who can edit request text and visibility.
- Who can see private custom attributes.
- Whether approval updates `ApprovedOnDateTime` and `ApprovedByPersonAliasId`; this was fixed for the Obsidian Prayer Request Detail block in v17.5 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Whether the urgent flag defaults correctly; release notes mention a v17.5 fix to default `IsUrgent` to false when not selected ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Whether PersonId URL prefill works; release notes mention a v17.2 fix for PersonId URL parameter handling in the Obsidian Prayer Request Detail block ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Whether AI automation fields such as original request and sentiment are present and enabled locally.

### Prayer Request List Configuration

Official docs describe `People > Prayer` as the administrative area for current requests, all comments, and add-new behavior. The Prayer Requests list can be filtered to focus on flagged or unapproved requests ([Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0)).

The Obsidian list options model exposes:

- Whether the campus column should be visible, typically when more than one active campus exists.
- Whether the current person can approve prayer requests through the block’s `Approve` security action.

See [PrayerRequestListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs) and [prayerRequestListOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts). Release notes also mention a v19.1 improvement to widen displayed prayer request text for readability in the Prayer Request List block ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Inspect list filters and columns in the live instance. Important filters usually include approval status, active status, public/private, flagged count, category, campus, urgency, date entered, expiration, and group association. Exact filters depend on block version and local customization.

### Categories

Prayer categories organize the queue for administrators and prayer teams. Official docs say requests entered on the website default to General unless the requester selects another category, and selecting a top category enables subcategories as options. Administrators can assign or change categories during review. Predefined examples include categories such as health, grief, family, and similar ministry topics ([Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0)).

Source code includes a reporting data select that returns `PrayerRequest.Category.Name`, confirming category is a first-class reporting field for prayer requests ([CategorySelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/PrayerRequest/CategorySelect.cs)).

For implementation, inspect:

- Category tree under the relevant Prayer Request category root.
- Default category configured on entry blocks.
- Which categories are shown externally.
- Which categories appear to the prayer team.
- Whether subcategories are shown.
- Whether categories imply different approval, escalation, or privacy handling.
- Whether urgent categories exist separately from `IsUrgent`; do not confuse category labels with the urgent flag.
- Whether old categories are inactive, renamed, duplicated, or still referenced by reports and blocks.

### Approval, Visibility, Expiration, And Activity

The Prayer Request model and view models include `IsApproved`, `IsPublic`, `IsActive`, `ExpirationDate`, and `IsUrgent` fields. Source-code view models show these as separate concepts ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)).

Interpretation for agents:

- `IsApproved` controls administrative readiness for prayer-team exposure where approval is enforced.
- `IsPublic` controls whether request content may be used on public-facing or broadly visible surfaces, depending on the block or Lava template.
- `IsActive` indicates whether the request is active in the prayer queue.
- `ExpirationDate` is the date after which the request should no longer be active or listed, depending on block filters and jobs.
- `IsUrgent` influences sorting and attention. Official Prayer Session docs say urgent requests appear at the top of the session queue ([Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0)).

Do not assume any one flag implies another. A request can be public but unapproved, approved but private, active but expired due to configuration drift, urgent but not escalated, or group-scoped and invisible in normal prayer sessions. Inspect the live record and block behavior.

## 6. Primary Entities And Relationships

### Prayer Request To Person

Prayer requests can be associated with a person through a requested-by person alias. The reporting filter `Contains People` matches prayer requests where the selected person IDs include `RequestedByPersonAlias.PersonId` ([ContainsPeopleFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs)). The workflow action can also match the requestor from provided inputs, depending on configuration ([PrayerRequestAdd.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs)).

Operational implications:

- A request may have a known Rock person, manually entered name/email, or anonymous/public name only.
- The email address on the prayer request may not match the person profile email. Official comment communication docs note that the email included with the request is used by the job and may differ from the person record’s profile email ([Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication?Version=v19.0)).
- Duplicate person records can fragment prayer history and reporting. When person matching matters, verify aliases and duplicates before concluding a person has no requests.
- For requestors who are not in Rock, workflow or block configuration may create only a name/email on the prayer request and not a person record.

### Prayer Request To Category

A prayer request can have a category. Categories support user selection, administrator triage, prayer-team filtering, and reporting. The Category data select confirms category is reportable ([CategorySelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/PrayerRequest/CategorySelect.cs)). Official docs describe default and nested category selection behavior ([Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0)).

Operationally, categories should be designed for routing and prayer coverage, not merely for taxonomy. Avoid categories so granular that volunteers avoid them or so broad that staff cannot triage. For sensitive categories, pair category design with approval and security controls.

### Prayer Request To Campus

Prayer entry and detail view models include campus fields. The entry initialization model includes default campus, campus status filters, and campus type filters ([prayerRequestEntryInitializationBox.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntryInitializationBox.d.ts)). Release notes mention a campus type filter added to the campus picker on Prayer Request Detail, allowing administrators or submitters to narrow selectable campuses ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Inspect:

- Whether campus is shown externally.
- Whether default campus comes from the authenticated person.
- Whether campus filters exclude inactive, online-only, or non-ministry campuses.
- Whether reports use campus for staff assignments or prayer-team routing.
- Whether multi-campus teams see all requests or only campus-specific queues.

### Prayer Request To Group

Group prayer requests allow a request to be limited to group members. Official docs describe the group GUID pattern and state that the GroupGuid parameter changes both entry and prayer-team behavior ([Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0), [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests?Version=v19.0)). Source-code view models include a `Group` field on Prayer Request detail ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)). The mobile My Prayer Requests block has an `Include Group Requests` setting that defaults false in the source-code attributes ([MyPrayerRequests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/MyPrayerRequests.cs)).

Operational implications:

- Group-scoped requests may not appear in normal prayer-team sessions.
- The URL parameter is a GUID, not a simple ID.
- A group GUID is hard to guess but not a substitute for page security.
- Group request pages must be protected so only appropriate members or leaders can access them.
- Custom pages that ignore group filtering can accidentally expose group-scoped requests.

### Prayer Request To Comments And Notes

Prayer comments are managed under `People > Prayer`, and official docs mention a comments list and AI approval flow in the administration area ([Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0)). The Prayer Request Comments Digest job sends comments to the requestor using a system communication ([Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0)).

A source-code migration shows the Prayer Request Comments Digest system email template uses variables such as the prayer request, entered date, request text, comments, and global email header/footer ([095_PrayerRequestCommentsNotificationEmailTemplate.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/095_PrayerRequestCommentsNotificationEmailTemplate.cs)). Treat the migration as a historical/source landmark; inspect the actual system communication in the live instance because churches commonly customize templates.

Community recipes show that some churches add comment modals to Prayer Card View by creating a page with a `prayerRequestId` context parameter and a Notes Entry block set to Prayer Request as the context entity ([Prayer Card View - Add Prayer Comment Modal](https://community.rockrms.com/recipes/350)). That is a community pattern, not core authority.

### Prayer Request To Answer

The Prayer Request detail model includes an `Answer` field ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)). A community recipe emphasizes that the answer is a single field and proposes a workflow-entry page for prayer team members to record an answer from Prayer Card View ([Prayer Card View - Add Answered Prayer](https://community.rockrms.com/recipes/389)).

Use answer differently from comments:

- Comments are multiple, often prayer-team encouragement or updates.
- Answer is a singular resolution or answered-prayer description.
- If multiple team members can submit answers, define ownership and edit rules.
- If the answer will be public or emailed, moderate it like request text.

### Prayer Request To Workflow

Rock includes a `Prayer Request Add` workflow action in the People category. The source code describes it as creating a prayer request and optionally updating a workflow attribute with the created request. It can accept requestor input, first name, last name, email, person matching, campus, request text, and category ([PrayerRequestAdd.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs)). A community SMS recipe notes that as of Rock v11 this workflow action exists and is preferable to direct SQL for new implementations ([SMS Prayer Request Capture](https://community.rockrms.com/recipes/135)).

Agents should strongly prefer the workflow action, entity commands, APIs, or supported services over raw SQL inserts. If a recipe uses direct SQL, treat it as historical or advanced and review schema, required fields, security, validation, and side effects in the target Rock version.

## 7. Common Prayer And Care Workflows

### Public Website Prayer Intake

The baseline public workflow is:

1. Visitor opens `Connect > Prayer` or a locally configured prayer page.
2. Prayer Request Entry block displays request fields based on block settings.
3. Visitor submits the request.
4. Rock saves the request with configured defaults for public visibility, comments, approval, category, campus, and urgency.
5. If auto-approval is disabled, an administrator reviews the request under `People > Prayer`.
6. If approved and active, the request becomes available to prayer-team surfaces according to category, group, and visibility filters.

Agents should inspect the live page and block settings before documenting the workflow. The official docs call out that default configurations work for many churches but are customizable ([Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0)).

### Internal Staff Entry

Staff or prayer administrators can add prayer requests internally from `People > Prayer > Add Prayer Request` ([Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0)). This is commonly used for:

- Weekend connection-card prayer requests.
- Phone-call prayer requests.
- Staff-entered requests after a pastoral conversation.
- Requests imported from other ministry systems.
- Requests that should be private and never exposed externally.

For staff entry, verify whether the internal detail block requires last name, auto-populates requester data, exposes custom attributes, or applies approval automatically.

### Administrative Review

Official docs place administration under `People > Prayer`, where administrators can add requests, view current requests, and view comments. The list can be filtered to focus on flagged or unapproved requests ([Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0)).

A strong daily review queue should include:

- New unapproved requests.
- Flagged requests.
- Urgent requests.
- Requests with crisis language.
- Public requests containing full names, phone numbers, addresses, minors, medical details, or unsafe third-party details.
- Requests with comments awaiting approval, if comment approval is enabled.
- Expired-but-active requests.
- Requests with missing categories, campuses, or requestor information.
- Duplicate submissions.

### Prayer Session

Prayer Session is the traditional guided prayer-team experience. Official docs say prayer team members access it on the website under `Connect > Prayer > Prayer Team`, select categories with active prayers, and start a session. Category choices can be remembered for the next session. Urgent requests appear first, and then remaining requests are ordered from least-prayed-for to most-prayed-for ([Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0)).

Operational considerations:

- Small teams may need broad category selection to ensure coverage.
- If many categories exist, requests may be neglected in low-selected categories.
- Least-prayed-first ordering helps distribute coverage but does not replace triage.
- Urgent ordering should be paired with staff escalation policy.
- The prayer team page should require authentication and appropriate security.

### Prayer Card View

Prayer Card View is a card-based prayer-team surface. Official docs describe it as similar to Prayer Session, but with requests displayed as cards and a Pray button that counts the prayer. It ships with Rock but is not added to pages out of the box, so administrators must add it to an external website page or replace the Prayer Session block if desired ([Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0)).

Operational considerations:

- Card view may be easier on mobile and lets team members scan multiple requests.
- Card view templates can expose more data than intended if customized carelessly.
- Community recipes show card customizations for comments, answers, prayer count, date entered, and custom attributes ([Prayer Card View - Add Prayer Comment Modal](https://community.rockrms.com/recipes/350), [Prayer Card View - Add Answered Prayer](https://community.rockrms.com/recipes/389)).
- Review every Lava template for public-safe output.
- Verify that group-scoped requests are filtered correctly.

### Group Prayer Requests

Official docs say group-specific prayer requests are associated with a group, limiting prayer to group members. The only difference in the entry and prayer experience is the presence of the group GUID parameter in the URL. If a prayer block sees `GroupGuid`, it scopes the prayer session to that group. If no `GroupGuid` is present, group-associated requests are not listed for normal prayer ([Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0), [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests?Version=v19.0)).

Use group prayer for:

- Small groups.
- Serving teams.
- Staff teams.
- Recovery or care groups where visibility must remain limited.
- Leader-only prayer boards.

Do not rely only on GUID obscurity. Secure the page, verify group membership checks, and test logged-out, non-member, member, leader, and admin scenarios.

### Prayer Comments Digest

The Send Prayer Comments job can send prayer-team comments back to the requestor. Official docs say the job is included but must be configured, and it uses a system communication such as Prayer Request Comments Digest ([Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0)). The communication article explains that the email includes a greeting, original request, and comments added since the last job run; if the job has never run, all comments may appear ([Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication?Version=v19.0)).

Operational checks:

- Is the job enabled?
- What schedule does it run?
- Which system communication does it use?
- Does the template include private data?
- Does it include all comments on first run?
- Does it respect comment approval?
- Which email address is used?
- Are bounced or invalid emails monitored?
- Are staff or prayer team members warned that comments may be sent to the requestor?

### Urgent Prayer Email

A community recipe shows a workflow and button pattern that lets Prayer Admins email an urgent prayer request to a prayer team from the Prayer Request Detail page ([Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)). This can be useful when a prayer team does not log in daily.

Because it is community-contributed, verify:

- Recipient group or security role.
- Who can invoke the workflow.
- Whether the email includes request text, link only, or both.
- Whether the request is approved and public before sending.
- Whether private or crisis details should be routed to staff instead.
- Whether the workflow logs communications on the person record.
- Whether the link requires authentication.

### SMS Prayer Request Capture

A community recipe shows SMS prayer intake using SMS Pipeline or legacy Text-to-Workflow. It matches messages with a regular expression, attempts to match a phone number to a person, creates a named or anonymous request, and returns a confirmation. The recipe notes that Rock v11 introduced a Prayer Request Add workflow action and recommends using it where possible instead of direct SQL ([SMS Prayer Request Capture](https://community.rockrms.com/recipes/135)).

For modern implementations, prefer:

- SMS Pipeline to workflow.
- `Prayer Request Add` workflow action.
- Clear confirmation response.
- Spam and abuse controls.
- Staff moderation before public or prayer-team exposure.
- Person matching that handles shared phones, minors, and duplicates carefully.
- A fallback anonymous path that still records phone metadata only where policy allows.

### Prayer Wall

A community recipe demonstrates a public prayer wall using HTML Content, Prayer Request Entry, Prayer Request List Lava, and a Lava webhook that increments prayer count ([Create a Prayer Wall](https://community.rockrms.com/recipes/149)). This pattern is high-risk because it makes prayer content public and may use direct SQL updates.

If implementing a prayer wall:

- Require moderation before display.
- Only show `IsPublic` and approved requests.
- Redact names and sensitive details.
- Avoid exposing last names, contact info, children, locations, or medical specifics.
- Avoid direct SQL where supported APIs or block behavior can be used.
- Rate-limit prayer-count actions.
- Prevent repeated anonymous count inflation if the count has ministry significance.
- Verify template output for HTML encoding and Lava safety.
- Test logged-out behavior.

### Live Prayer Chat

A community recipe describes adding an external live chat widget to connect website visitors with prayer team members ([Agent-Style Live Chat Interface On Public Website](https://community.rockrms.com/recipes/157)). This is not a core Rock prayer feature, but it is care-adjacent.

Before using external chat:

- Review data processing agreements and privacy policy.
- Decide whether chat transcripts enter Rock.
- Train prayer volunteers on crisis escalation.
- Avoid collecting confidential details in a third-party widget without consent.
- Define operating hours and offline behavior.
- Decide whether the chat team is the same as the Prayer Team or a more restricted care team.

### Pastoral Care Summary

A community recipe describes an automatic pastoral care summary email using a pastoral-care plugin, workflows, scheduled jobs, and email links for visitation notes ([Automatic Pastoral Care Summary Email](https://community.rockrms.com/recipes/121)). This is care-adjacent, not core Prayer. It illustrates an important pattern: care operations often need scheduled summary communications, secure links, volunteer access, note updates, and lifecycle dates such as discharge or end dates.

If using this pattern, verify plugin installation, workflow IDs, activity IDs, recipient groups, login/security model, auto-login behavior, note permissions, and whether the summary includes protected health or private pastoral data.

## 8. Prayer Requests Deep Dive

### Intake Fields

Based on official docs and source-code models, a prayer request can include:

- Request text.
- First name and last name.
- Email.
- Mobile phone and country code on entry save.
- Campus.
- Category.
- Public/private flag.
- Urgent flag.
- Allow-comments flag.
- Custom attribute values.
- Person alias association.
- Group association.
- Expiration date.
- Approval fields.
- Prayer count.
- Flag count.
- Answer.
- AI-related fields such as original request and sentiment when enabled.

The public entry save model confirms the submitted payload shape for key entry fields ([PrayerRequestEntrySaveRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntrySaveRequestBag.cs)). The detail bag confirms the broader administrative field set ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)).

### Text Handling

Prayer request text is often user-generated and emotionally raw. Agents should not assume text is safe for public display just because it was submitted on a public form. Review for:

- Full names of third parties.
- Minors.
- Addresses, phone numbers, emails, workplaces, schools, hospitals, or travel locations.
- Self-harm, abuse, violence, or mandatory-reporting concerns.
- Details about missionaries, persecuted people, immigration status, addiction, mental health, legal matters, or medical diagnoses.
- Accusations or gossip.
- HTML, script tags, malformed markup, and unsafe embedded content if templates render without encoding.
- Confidential ministry or staff-only information.

If AI automation is enabled, inspect the original request and formatted request. Official docs describe Prayer AI Automations as a way to clean up wording, remove names, and format requests using an AI provider, with disclaimers covered on the AI automations page ([Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations?Version=v19.0)). Release notes identify Prayer Automations as a v17.0 feature and direct administrators to the Tech Bulletin ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Do not assume AI output is safe. Review local prompts, provider settings, disclaimers, logging, and approval workflow.

### Approval

Official docs say administrators review requests before the prayer team sees them, except when requests are configured to auto-approve ([Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0)). In source-code list options, approval visibility depends on the block’s `Approve` security action ([PrayerRequestListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs)).

Agent checks:

- Is auto-approval enabled on the entry block?
- Does the list block show approval status to this user?
- Which security role has `Approve`?
- Does approving set approval timestamp and approver alias? Be especially careful on v17.5 and earlier because release notes mention a fix for Obsidian approval fields ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Are flagged requests automatically hidden after being flagged, or simply marked for review? Verify live behavior.
- Are approval status and public status both required for external display?

### Public And Private Requests

The `IsPublic` field is separate from `IsApproved` and must be handled independently. Entry models include an `isPublicDefaultValue` and save payload includes `isPublic` ([prayerRequestEntryInitializationBox.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntryInitializationBox.d.ts), [PrayerRequestEntrySaveRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntrySaveRequestBag.cs)).

A privacy-safe public workflow should require:

- Explicit requester awareness of public/private choice.
- Default private when the church’s policy is conservative.
- Staff review before public display.
- Redaction of last names and identifying details.
- Public list templates that display only approved public active non-expired requests.
- Separate visibility for prayer team, group members, public website visitors, and administrators.

### Urgent Requests

Urgency is stored as `IsUrgent` and may influence session ordering. Official Prayer Session docs say urgent requests are shown first ([Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0)). Release notes mention a v17.5 fix to default unchecked urgent flags to false rather than null ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Urgent does not automatically mean emergency response. Define:

- What qualifies as urgent.
- Who receives urgent notifications.
- Whether urgent requests require pastoral staff review before prayer-team distribution.
- Whether crisis language bypasses normal prayer workflows and follows safety protocols.
- Whether urgent requests expire sooner or remain pinned until staff resolves them.

### Expiration

The detail view model includes `ExpirationDate` ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)). Entry block documentation references configurable defaults, but exact expiration behavior must be verified in the live instance.

Inspect:

- Default expiration configured on entry and detail blocks.
- Whether expiration is set on save.
- Whether expired requests are hidden from session/card/list blocks.
- Whether expired requests are still visible in My Prayer Requests mobile block when `Show Expired` is enabled ([MyPrayerRequests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/MyPrayerRequests.cs)).
- Whether reports count expired requests.
- Whether cleanup jobs or manual processes deactivate old requests.

### Custom Attributes

Prayer Request attributes can extend intake and reporting. Entry initialization models include editable public attributes ([PrayerRequestEntryInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntryInitializationBox.cs)). Release notes mention a v17.0 bug fix where Prayer Request Attributes not marked Public were incorrectly displayed in the Obsidian Prayer Request Entry block; they are now hidden ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Release notes also mention v17.0 mobile support for editing custom attributes in the Mobile Prayer Request block, with the caveat that Rock Mobile supports common but not all attribute types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agents should audit:

- Which Prayer Request attributes exist.
- Which are marked public.
- Which are shown on external entry.
- Which appear in card/list Lava.
- Which are editable on mobile.
- Whether any attribute stores confidential care triage data.
- Whether attribute values appear in exports, reports, or communications.

## 9. Teams And Moderation Deep Dive

### Role Design

Official docs reduce prayer ministry staffing to two basic roles: Prayer Administrator and Prayer Team. The administrator enters card-submitted requests and reviews flagged or unapproved requests; the team prays and flags requests that may be inappropriate for public viewing ([Prayer Team Roles](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)).

In a real implementation, most churches should refine this into more precise permissions:

- Prayer Administrator: full prayer request review, edit, approve, category assignment, visibility, comments, expiration, and reporting.
- Prayer Team Member: read approved prayer-team-visible requests, pray, optionally comment, optionally flag.
- Care Team Member: access sensitive follow-up queues or assigned care workflows.
- Group Leader: access only group-scoped prayer requests for their group.
- Communications Admin: configure comment digest, urgent email, and prayer notifications.
- Rock Administrator: configure blocks, security, system jobs, and workflows.
- Safety/Pastoral Escalation Team: receive requests involving abuse, self-harm, threats, or high-risk pastoral care.

Do not grant prayer team members broad access to all person records unless the ministry policy requires it. A person can pray faithfully without seeing full CRM history.

### Moderation Flagging

The official flagged-request article explains why flagging exists: public submissions can contain inappropriate wording, dangerous details, or situations needing authority or staff notification, and prayer team members need a way to alert administrators ([Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests?Version=v19.0)). Source-code detail bags include `FlagCount` and `ModerationFlags` ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)).

Moderation process:

1. Prayer team member flags a request.
2. Administrator reviews the request text, requester info, category, public flag, and comments.
3. Administrator decides whether to edit/redact, make private, remove from active queue, escalate, contact the requestor, or approve unchanged.
4. Administrator clears or resolves the flagged state according to local block behavior.
5. If the request contains crisis content, administrator follows the church’s safety process rather than treating it as a normal prayer moderation item.

Live verification needed:

- Which block allows flagging?
- Does a single flag hide the request from all prayer team members?
- Are flag reasons stored as moderation flags, notes, or counts?
- Can prayer team members see existing flags?
- Who can clear flags?
- Are flagged comments separate from flagged requests?
- Are AI comment approvals enabled?

### Comments Moderation

Official administration docs include a Prayer Comments List and Prayer Comments AI Approvals headings ([Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0)). The exact comment approval workflow depends on local version and configuration.

If comments are enabled:

- Train prayer team members that comments may be emailed to requestors.
- Avoid theological correction, advice, medical guidance, counseling diagnoses, or promises.
- Review whether comments require approval before digest.
- Keep comments brief, compassionate, and privacy-safe.
- Define whether comments are visible internally, externally, or only in digest.
- Audit the Send Prayer Comments job before enabling.

### AI Moderation And Formatting

Prayer AI Automations can format incoming requests, remove names, and prepare text for ministry review when an AI Provider is configured ([Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations?Version=v19.0)). Release notes describe this as a v17.0 Prayer feature and advise reading the related Tech Bulletin ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Before enabling AI:

- Verify the AI provider configuration.
- Review prompts and data sent to the provider.
- Understand retention and logging.
- Enable disclaimers where appropriate.
- Decide whether AI output auto-replaces request text or requires approval.
- Inspect `OriginalRequest`, `Sentiment`, and moderation-related fields.
- Test with last names, minors, medical details, abuse disclosures, and missionary-location scenarios.
- Confirm that AI does not mark unsafe text public without human review.

## 10. Follow-Up And Communications Deep Dive

### Comment Digest Email

The comment digest system is the core built-in follow-up communication path. Official docs say Send Prayer Comments can send comments to the originator and uses the Prayer Request Comments Digest system communication ([Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0)). The communication article explains that the message includes the requestor’s name, submitted date, original request, and comments since the job last ran; if it has never run, all comments may be included ([Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication?Version=v19.0)).

Agent checklist:

- Find the Send Prayer Comments job.
- Verify enabled/disabled status.
- Verify schedule.
- Inspect selected system communication.
- Preview with real-looking test data.
- Confirm recipient email source.
- Confirm whether comments are filtered by approval.
- Confirm whether old comments will send on first run.
- Confirm unsubscribe, communication preference, and bounce behavior as applicable.
- Confirm staff approval of wording.

### Communications Security

Prayer communications can expose private ministry content. The v19.1 release notes mention new Communication Detail access controls and a `View All` security action for communication detail visibility ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). While this release note is for communications broadly, it matters for prayer-care emails because staff may assume sent prayer communications are visible to all admins. Verify communication security in the live instance.

For every prayer-related communication:

- Use minimal necessary detail.
- Prefer secure links over full sensitive text when appropriate.
- Require authentication for sensitive linked pages.
- Avoid auto-login links unless security policy permits them.
- Log communications where ministry policy requires.
- Do not send crisis details to large volunteer groups.
- Use separate templates for public encouragement, prayer team alerts, and pastoral-care escalation.

### Urgent Notifications

Urgent prayer emails are often implemented through custom workflow, as in the community recipe for emailing urgent prayer requests from a detail-page button ([Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)). A more mature urgent path may include:

- Field-level urgent flag.
- Administrator review.
- Workflow action to notify a limited group.
- Communication template with link and summary.
- Assignment to a staff care owner.
- Follow-up due date.
- Audit note on the prayer request or person record.

Live verification: check whether urgent currently means a flag only, an email, a workflow launch, a report filter, or a staff escalation process.

### Care Follow-Up Beyond Prayer

Rock prayer comments are not the same as care follow-up. Care follow-up may require:

- Person notes.
- Connection requests.
- Group leader tasks.
- Workflow activities.
- Staff assignment.
- Hospital visitation records.
- Pastoral-care plugin records.
- Background-checked volunteer access.
- Secure communications.
- Reporting dashboards.

Community examples show patterns but not core guarantees. The pastoral-care summary recipe uses a plugin, workflows, scheduled email, and update links for visitation notes ([Automatic Pastoral Care Summary Email](https://community.rockrms.com/recipes/121)). Treat that as an example of how churches connect prayer/care operations, not a built-in Prayer feature.

## 11. Related Rock Areas: People, Groups, Communications, Workflows, Security, Cms

### People

Prayer requests often connect to people records through requested-by person alias, person matching, email, phone, or workflow attributes. RockU’s Individuals in Rock training collection includes person profile, attributes, data integrity, impersonation, and prayer requests as related staff-training topics ([Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock), [Prayer Requests](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests)).

Agent checks:

- Does the request link to the correct person alias?
- Is the person duplicated?
- Does the request contain a manually entered email that differs from the profile?
- Should staff add a person note or connection request?
- Are minors involved?
- Are person attributes or account protection profiles relevant to visibility?
- Does the requester need follow-up from their campus or group leader?

### Groups

Groups matter in two ways: prayer team membership and group-scoped prayer requests. The official group-prayer docs depend on group GUIDs in URLs ([Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0)). Prayer-team access may be implemented as a security role, serving team, group, or other access pattern. The urgent email recipe shows a community implementation using either a security role or group as recipients ([Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)).

Inspect:

- Prayer Team group or role.
- Prayer Administrator group or role.
- Group leader access to group-scoped prayer.
- Whether inactive group members still have access.
- Whether group GUID links are exposed in email or CMS content.

### Communications

Communications support comment digests, urgent emails, SMS confirmations, live prayer chat follow-up, and pastoral-care summaries. Official prayer-comment docs point back to the broader Communications area for email behavior ([Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication?Version=v19.0)).

Inspect:

- System Communication: Prayer Request Comments Digest.
- Communication job scheduling.
- SMS pipeline setup for prayer intake if used.
- Communication recipient groups.
- Sender addresses.
- Communication security.
- Templates for privacy and clarity.

### Workflows

Workflows are the safest extension point for prayer intake and routing. The core `Prayer Request Add` action can create prayer requests from workflow context ([PrayerRequestAdd.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs)). Community recipes use workflows for SMS intake, urgent emails, answer entry, and pastoral-care summaries ([SMS Prayer Request Capture](https://community.rockrms.com/recipes/135), [Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338), [Prayer Card View - Add Answered Prayer](https://community.rockrms.com/recipes/389), [Automatic Pastoral Care Summary Email](https://community.rockrms.com/recipes/121)).

Prefer workflows over direct SQL for:

- Creating prayer requests.
- Sending urgent prayer emails.
- Routing to care teams.
- Sending SMS confirmations.
- Adding follow-up tasks.
- Escalating flagged or crisis requests.

### Security

Prayer security has multiple layers:

- Page view rights.
- Block security actions such as `Approve`.
- REST endpoint permissions.
- Group membership.
- Security roles.
- Person record access.
- Communication detail access.
- Attribute public/private visibility.
- Workflow entry permissions.
- Lava command security.
- External service access.

REST v2 generated endpoints for Prayer Requests require authentication and unrestricted read/write security actions for CRUD operations; the generated controller route is `api/v2/models/prayerrequests` ([PrayerRequestsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs)). This is a developer landmark, not a recommendation to expose unrestricted API access. Use least privilege.

### CMS

Most prayer experiences are CMS pages and blocks:

- External `Connect > Prayer` page.
- Prayer Team page.
- Group-specific prayer pages.
- Prayer Card View page.
- Prayer wall.
- Workflow entry modals.
- Prayer comments or answer-entry pages.
- Mobile pages and blocks.

CMS checks:

- Page routes.
- Page security.
- Block settings.
- Lava templates.
- Pre/Post HTML.
- Querystring parameters.
- Context parameter names.
- Linked pages.
- Template includes.
- Public-site caching behavior.

## 12. Administration And Operational Guardrails

### Daily Operations

A daily prayer-admin routine should include:

1. Review unapproved requests.
2. Review flagged requests.
3. Review urgent requests.
4. Review comments awaiting approval.
5. Review public requests for identifying details.
6. Assign categories and campuses.
7. Escalate crisis or pastoral-care items.
8. Check Send Prayer Comments job status if enabled.
9. Check prayer-team queue health by category.
10. Spot-check public prayer pages and group prayer pages.

### Weekly Operations

Weekly checks:

- Category coverage: categories with active requests but low prayer counts.
- Expired requests still active.
- Requests with no category or campus.
- Old urgent requests still unresolved.
- Requests with comments but no digest sent.
- Prayer team activity and access roster.
- Any direct SQL or custom Lava prayer integrations.
- Prayer wall or card template output.
- Mobile prayer request behavior.
- AI automation exceptions or approvals.

### Privacy Guardrails

Use conservative defaults:

- Do not default public unless ministry policy intentionally supports a public prayer wall.
- Require approval before public display.
- Hide last names publicly.
- Hide contact details.
- Avoid medical and crisis details in public.
- Treat group requests as private to the group.
- Treat comments as potentially sendable.
- Keep care follow-up notes out of public prayer fields.
- Never put staff-only safety assessment in request text.

### Change Management

Before changing prayer configuration:

- Export or document current block settings.
- Screenshot key pages for review.
- Record current category tree.
- Identify dependent reports and workflows.
- Test with logged-out, prayer team, administrator, group member, and non-member users.
- Test mobile if mobile prayer blocks are used.
- Test comment digest in a non-production or test-recipient path.
- Review release notes for the target version.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Model And View Models

Key model landmarks:

- Model Map identifies Prayer Request as a Prayer model ([Model Map](https://community.rockrms.com/ModelMap)).
- Obsidian Prayer Request Detail bags expose the administrative field set ([PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)).
- Prayer Request Entry bags expose public-entry initialization and save payloads ([PrayerRequestEntryInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntryInitializationBox.cs), [PrayerRequestEntrySaveRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntrySaveRequestBag.cs)).
- List options expose approval-column and campus-column behavior ([PrayerRequestListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs)).
- Mobile My Prayer Requests block exposes edit page, answer page, template, show-expired, days-back, max-results, and include-group-requests settings ([MyPrayerRequests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/MyPrayerRequests.cs)).

### REST API

The generated REST v2 Prayer Requests controller provides model CRUD endpoints under `api/v2/models/prayerrequests` and requires authentication and unrestricted read/write security actions ([PrayerRequestsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs)).

For integrations:

- Use official APIs or workflow actions where possible.
- Do not use public unauthenticated endpoints for prayer creation unless specifically designed and secured.
- Avoid unrestricted tokens.
- Use service accounts with minimal permissions.
- Log integration writes.
- Validate request text and visibility fields.
- Avoid writing approval/public flags automatically unless the moderation policy allows it.

### Workflow Action

The `Prayer Request Add` workflow action is a first-class extension point. It can create a prayer request and optionally store the created request in a workflow attribute. Settings include requestor input, first name, last name, email, person matching, campus, request text, and category ([PrayerRequestAdd.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs)). Community SMS guidance specifically points to this action as preferable to direct SQL on newer Rock versions ([SMS Prayer Request Capture](https://community.rockrms.com/recipes/135)).

### Lava

Lava appears in group GUID retrieval, Prayer Card View templates, prayer wall templates, workflow-entry page templates, and community recipes. Official group-prayer docs mention using Lava to retrieve a group GUID when building group-specific prayer URLs ([Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0)). Community recipes use Lava to display prayer counts, dates, attributes, and modal launch links ([Prayer Card View - Add Prayer Comment Modal](https://community.rockrms.com/recipes/350)).

Lava guardrails:

- Encode output unless intentionally rendering trusted HTML.
- Avoid direct SQL in Lava for public pages when supported alternatives exist.
- If SQL is used, parameterize and sanitize carefully.
- Do not expose private attributes.
- Do not render full names on public prayer walls unless policy allows.
- Check whether the Lava command is allowed in the block context.
- Verify group filters before rendering prayer request loops.

## 14. Reporting, Analytics, And Model Map

### Built-In Reporting Landmarks

Prayer Request is a reportable model in the Prayer category ([Model Map](https://community.rockrms.com/ModelMap)). Source-code reporting components include:

- Category select: returns category name for prayer requests ([CategorySelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/PrayerRequest/CategorySelect.cs)).
- Contains People filter: returns prayer requests involving selected people through `RequestedByPersonAlias.PersonId` ([ContainsPeopleFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs)).

Useful reports:

- Active approved requests by category.
- Unapproved requests by age.
- Flagged requests by age and category.
- Urgent requests not reviewed.
- Public requests by category and campus.
- Expired but active requests.
- Prayer count distribution.
- Requests by requested-by person or family.
- Requests with comments in the last week.
- Requests with no category.
- Requests created by intake source, if a custom attribute stores source.

### Metrics To Avoid Misreading

Prayer count is not the same as pastoral care completed. It measures interactions with prayer surfaces. It may be affected by card view, session behavior, prayer wall buttons, custom webhooks, or manual changes. If a community prayer wall increments count anonymously, prayer count can be inflated ([Create a Prayer Wall](https://community.rockrms.com/recipes/149)).

Approval count is not the same as safety. A request can be approved but still contain sensitive details. Public count is not the same as public display; display depends on templates and filters. Category count is not the same as workload; some categories require more care follow-up than others.

### Operational Dashboard Ideas

A useful prayer-care dashboard should include:

- New unapproved requests.
- Flagged requests.
- Urgent requests.
- Old active requests past expiration.
- Requests by category and campus.
- Requests with zero prayer count after a defined number of days.
- Comments pending approval.
- Comment digest last-run status.
- AI automation exceptions or approvals if enabled.
- Group-scoped request counts.
- Public prayer-wall count and oldest public request.
- Care escalation queue, if implemented through workflows or connection requests.

## 15. Version And Release Caveats

Use the [Rock Core Release Notes](https://www.rockrms.com/releasenotes) to verify version-specific behavior. Notable prayer-related caveats in the provided records include:

- **v17.0**: Prayer Automations were added, with release notes advising administrators to read the Tech Bulletin before using them.
- **v17.0**: Mobile Prayer Request block gained support for editing custom attributes, with the caveat that Rock Mobile supports common but not all attribute types.
- **v17.0**: A bug was fixed where Prayer Request Attributes not marked Public were incorrectly displayed in the Obsidian Prayer Request Entry block.
- **v17.2**: Obsidian Prayer Request Detail gained/fixed support for the `PersonId` URL parameter so person data can be prefilled when creating a request.
- **v17.5**: Approving a Prayer Request in the Obsidian Prayer Request Detail block was fixed to update `ApprovedOnDateTime` and `ApprovedByPersonAliasId`.
- **v17.5**: Prayer Request Detail was fixed to default unchecked `IsUrgent` to false to avoid null-related sorting issues.
- **v18.3**: Campus Type filter was added to the campus picker on Prayer Request Detail.
- **v19.1**: Prayer Request List was improved to display request text at a wider width for readability.

Agent version workflow:

1. Identify the Rock version.
2. Identify whether blocks are WebForms, Obsidian, mobile, or custom.
3. Read release notes between the installed version and the target behavior.
4. Inspect the live block settings and source if available.
5. Test the exact flow.

## 16. Implementation Playbooks

### Playbook: Launch Basic Prayer Intake

1. Create or verify the external `Connect > Prayer` page.
2. Add or inspect Prayer Request Entry block.
3. Configure requester fields.
4. Configure categories and default category.
5. Configure campus defaults and filters.
6. Set public default conservatively.
7. Decide whether comments are allowed.
8. Decide whether urgent is shown.
9. Set character limit.
10. Enable CAPTCHA if public spam is a concern.
11. Disable auto-approval until moderation process is proven.
12. Submit test requests as logged-out and logged-in users.
13. Review requests under `People > Prayer`.
14. Verify approval, category, public/private, and expiration behavior.
15. Train prayer administrators.

### Playbook: Launch Prayer Team Page

1. Define Prayer Team role or group.
2. Secure the Prayer Team page.
3. Choose Prayer Session or Prayer Card View.
4. Add block to external authenticated page.
5. Configure categories.
6. Test category selection and active request counts.
7. Verify urgent requests appear first in Prayer Session.
8. Verify prayer count increments.
9. Verify team members can flag requests.
10. Verify team members cannot edit fields they should not edit.
11. Train team members on flagging, comments, privacy, and crisis escalation.

### Playbook: Add Group Prayer

1. Identify group and group leadership.
2. Retrieve group GUID through a safe admin method.
3. Add `GroupGuid` parameter to the entry and prayer page URLs.
4. Secure pages to group members or leaders.
5. Submit a group-scoped test request.
6. Verify it appears only in group-scoped prayer pages.
7. Verify it does not appear in normal prayer sessions without `GroupGuid`.
8. Test non-member access.
9. Document group leader responsibilities.

### Playbook: Enable Comment Digest

1. Review comment policy.
2. Train prayer team members.
3. Inspect Prayer Request Comments Digest system communication.
4. Edit template for privacy-safe language.
5. Configure Send Prayer Comments job.
6. Test with one request and one approved comment.
7. Confirm first-run behavior for old comments.
8. Confirm email recipient source.
9. Enable schedule.
10. Monitor first production run.

### Playbook: Add SMS Prayer Intake

1. Confirm SMS Pipeline availability and phone number routing.
2. Create workflow with `Prayer Request Add` action.
3. Parse incoming message and from-person/from-phone.
4. Match person conservatively.
5. Set approval false by default.
6. Set public false by default unless policy says otherwise.
7. Send brief confirmation.
8. Test matched and unmatched phone numbers.
9. Test spam and malformed messages.
10. Monitor newly created requests.

### Playbook: Add Public Prayer Wall

1. Confirm ministry policy supports public prayer display.
2. Require approval and public flag.
3. Use only approved, active, non-expired, public requests.
4. Hide last names and contact details.
5. Redact sensitive text.
6. Avoid direct SQL where possible.
7. Rate-limit prayer count if public users can increment it.
8. Test logged-out behavior.
9. Review mobile layout.
10. Monitor public content daily.

## 17. Troubleshooting Decision Tree

### Request Was Submitted But Prayer Team Cannot See It

Check:

1. Is the request active?
2. Is it expired?
3. Is it approved?
4. Is it public/private, and does the prayer-team block filter by public?
5. Is it assigned to a category selected by the prayer team?
6. Is it urgent but hidden by a custom filter?
7. Is it group-associated? If yes, is `GroupGuid` present in the prayer-team URL?
8. Is the prayer-team user authenticated and in the right role?
9. Is the block configured to show the relevant categories?
10. Is the request on a campus filtered out by the block?

### Request Appears Publicly When It Should Not

Check:

1. Is `IsPublic` true?
2. Is the public page filtering by `IsPublic`, approval, active, and expiration?
3. Does the Lava template ignore flags?
4. Are custom attributes marked Public incorrectly?
5. Is the instance on a version before the v17.0 public-attribute visibility fix?
6. Is the request group-scoped but displayed by a custom query?
7. Is a cached page showing old content?
8. Did AI formatting remove or preserve sensitive details?

### Approval Does Not Record Approver Or Date

Check:

1. Rock version.
2. Whether the block is Obsidian Prayer Request Detail.
3. Whether the instance includes the v17.5 fix for `ApprovedOnDateTime` and `ApprovedByPersonAliasId`.
4. Whether custom workflow or SQL is bypassing normal approval behavior.
5. Whether the user has the block’s Approve security action.

### Urgent Sorting Looks Wrong

Check:

1. Is `IsUrgent` true, false, or null?
2. Is the instance on a version with the v17.5 null urgent fix?
3. Is the Prayer Session block or Prayer Card View using custom sort?
4. Is category selection excluding urgent requests?
5. Are group-scoped urgent requests being excluded from normal sessions?

### Comment Digest Sends Too Much

Check:

1. Was this the first job run?
2. Are all historical comments included?
3. Are comments filtered by last-run timestamp?
4. Are unapproved comments included?
5. Did the template include original request text and all comments?
6. Which email address was used?
7. Was the job duplicated or run manually?

### SMS Intake Creates Anonymous Requests

Check:

1. Does the inbound phone match a person phone number?
2. Is the phone normalized consistently?
3. Is the from-person workflow attribute populated?
4. Are there duplicate people with the same phone?
5. Is the workflow using direct SQL instead of `Prayer Request Add`?
6. Is person matching enabled in the workflow action?

### Group Prayer Request Appears In General Queue

Check:

1. Is the request actually associated with the group?
2. Did a custom query ignore group filtering?
3. Is the normal prayer block configured differently than official group behavior?
4. Is the `GroupGuid` parameter present accidentally on a general page?
5. Is the mobile block configured to include group requests?

## 18. Agent Task Recipes

### Audit Prayer Configuration

- Identify Rock version.
- List prayer pages and block types.
- Inspect Prayer Request Entry settings.
- Inspect Prayer Request List and Detail settings.
- Inspect Prayer Session/Card View pages.
- Review categories.
- Review Prayer Team and Prayer Administrator security.
- Check Send Prayer Comments job and system communication.
- Check custom prayer workflows.
- Check prayer wall, SMS, urgent email, and group prayer pages.
- Check release-note caveats for installed version.

### Review A Sensitive Request

- Open the request detail.
- Check text, original request, AI-formatted text, and comments.
- Check requester identity and email.
- Check public, approved, active, urgent, category, campus, expiration, group.
- Look for identifying or crisis details.
- If unsafe, make private or unapproved according to policy.
- Escalate to staff if needed.
- Add only appropriate internal notes or workflow actions.

### Build A Prayer-Team Coverage Report

- Use Prayer Request as the model.
- Filter active approved non-expired requests.
- Group by category and campus.
- Include prayer count and entered date.
- Highlight zero-prayer requests older than a threshold.
- Separate group-scoped requests.
- Add flagged and urgent counts.
- Use the Category data select where available ([CategorySelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/PrayerRequest/CategorySelect.cs)).

### Investigate Person Prayer History

- Use person profile and aliases.
- Use reporting filter for Prayer Requests containing selected people where available ([ContainsPeopleFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs)).
- Check manually entered name/email requests that may not link to the person.
- Check duplicate person records.
- Check group-scoped requests if relevant.
- Respect privacy and security policy before exposing history.

### Safely Extend Prayer Intake

- Prefer workflow action `Prayer Request Add`.
- Avoid direct SQL unless there is no supported alternative.
- Set approval false by default.
- Set public false by default.
- Assign category deliberately.
- Attach campus if known.
- Attach person alias only after confident matching.
- Log source through a custom public-safe attribute if useful.
- Test public, private, urgent, and group cases.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `2`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Prayer Requests Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) | approved_for_public_distillation | 2 | media-insight:762111bd5a9d1218 |
| [Rapid Attendance Entry Transcript Insight](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) | approved_for_public_distillation | 3 | media-insight:f131f156d62b7d38 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

Primary official prayer documentation:

- [Prayer](https://community.rockrms.com/documentation/engagement/prayer?Version=v19.0)
- [Prayer Overview](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview?Version=v19.0)
- [About Prayer in Rock](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0)
- [Prayer Team Roles](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)
- [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0)
- [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests?Version=v19.0)
- [Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests?Version=v19.0)
- [Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0)
- [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0)
- [Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0)
- [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests?Version=v19.0)
- [Prayer Team Power Tools](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools?Version=v19.0)
- [Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0)
- [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0)
- [Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0)
- [Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication?Version=v19.0)
- [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations?Version=v19.0)

Training and release references:

- [Prayer Requests RockU](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests)
- [Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock)
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

Model, source-code, and developer landmarks:

- [Model Map](https://community.rockrms.com/ModelMap)
- [PrayerRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs)
- [PrayerRequestEntryInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntryInitializationBox.cs)
- [PrayerRequestEntrySaveRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestEntry/PrayerRequestEntrySaveRequestBag.cs)
- [PrayerRequestListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs)
- [PrayerRequestAdd.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs)
- [PrayerRequestsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs)
- [CategorySelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/PrayerRequest/CategorySelect.cs)
- [ContainsPeopleFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs)
- [MyPrayerRequests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/MyPrayerRequests.cs)
- [Prayer Request Comments Digest migration landmark](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/095_PrayerRequestCommentsNotificationEmailTemplate.cs)

Community examples to treat as implementation patterns, not authoritative core behavior:

- [SMS Prayer Request Capture](https://community.rockrms.com/recipes/135)
- [Create a Prayer Wall](https://community.rockrms.com/recipes/149)
- [Agent-Style Live Chat Interface](https://community.rockrms.com/recipes/157)
- [Automatic Pastoral Care Summary Email](https://community.rockrms.com/recipes/121)
- [Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)
- [Prayer Card View - Add Prayer Comment Modal](https://community.rockrms.com/recipes/350)
- [Prayer Card View - Add Answered Prayer](https://community.rockrms.com/recipes/389)

Dependency notes:

- Prayer depends operationally on People for person identity, aliases, profile email, phone matching, person notes, and data integrity.
- Prayer depends on Groups for prayer team membership and group-scoped prayer requests.
- Prayer depends on Communications for comment digests, urgent notifications, SMS intake confirmations, and pastoral-care summaries.
- Prayer depends on Workflows for safe extension, routing, SMS intake, urgent email, and care follow-up.
- Prayer depends on Security for page access, block actions, REST permissions, group visibility, communication detail access, attribute visibility, and Lava/SQL safety.
- Prayer depends on CMS for external intake pages, prayer team pages, card view, public prayer walls, group prayer pages, and custom workflow-entry pages.
- Prayer depends on live-instance verification because block settings, categories, workflows, jobs, templates, and security roles are commonly customized.
