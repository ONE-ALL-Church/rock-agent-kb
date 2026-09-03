---
id: authored-prayer-care
title: Prayer And Care
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "54d943471d6df6598880b2ed865dc703bd672aed17596907a1c995e878685c59"
---

# Prayer And Care

## Agent Summary

Rock’s prayer system supports a bounded ministry lifecycle:

1. A person or administrator enters a prayer request.
2. Rock either approves it automatically or holds it for administrator review.
3. Approved requests become available to an appropriately secured prayer team.
4. Team members pray, optionally comment, and flag requests requiring review.
5. Jobs, workflows, or mobile tools can support communication and follow-up.

Automatic approval makes a request immediately available to the prayer team. Without automatic approval, an administrator must approve the request first. Within a prayer session, urgent requests are prioritized, followed by other requests from least prayed-for to most prayed-for. [Intro to Prayer](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/intro-to-prayer) [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests)

Treat approval, public visibility, category organization, page security, comments, and group association as separate controls. A request can be approved for a prayer-team experience without being appropriate for public display. Category security does not flow down to prayer requests, so sensitive ministry queues should use secured pages with category-scoped blocks. [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories)

Prayer requests may contain sensitive health, safety, family, or pastoral information. Flagging and AI moderation can assist review, but neither replaces an organization’s human escalation procedures. Rock’s documentation specifically warns that AI results require monitoring and human oversight. [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests) [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

## Scope And Boundaries

This guide covers:

- Prayer-request entry, approval, expiration, categories, urgency, public visibility, comments, and custom attributes.
- Prayer administrator and prayer-team responsibilities.
- Prayer Session and Prayer Card View experiences.
- Team flagging, administrative moderation, and supported AI assistance.
- Group-associated prayer requests.
- Prayer-comment communications.
- Workflows that begin at submission, prayer, or flagging.
- Mobile Outreach Toolbox capabilities related to scheduled prayer and relationship-care touchpoints.
- Clearly labeled community patterns for alternate intake, notification, prayer-wall, and pastoral-care scenarios.

This guide does not define a universal pastoral-care policy, crisis-response protocol, mandatory-reporting procedure, data-retention standard, or permission model. The evidence pack does not establish those organizational decisions. It also does not prove that any particular Rock instance has the documented blocks, jobs, AI provider, mobile shell, workflows, or permissions configured.

The primary official documentation set is the Rock v19 prayer documentation. Version-specific release notes and a Rock Mobile v19 preview add narrower caveats. Community recipes are implementation examples only and are not reviewed or endorsed by the Rock core team. [Prayer documentation](https://community.rockrms.com/documentation/engagement/prayer) [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

## Mental Model

A useful agent model is to treat a prayer request as one record moving through several independent gates:

- **Intake:** Who or what created the request, and through which block or workflow?
- **Classification:** Which category, campus, group, urgency state, and custom attributes apply?
- **Approval:** Is the request allowed into prayer-team sessions?
- **Visibility:** Is it marked public, and what secured page or block can display it?
- **Participation:** May the prayer team pray, comment, or flag?
- **Follow-up:** Should comments, workflows, or scheduled touchpoints produce a ministry action?
- **Lifecycle:** Is the request active, expired, answered, deleted, or awaiting review?

Rock’s request-detail data surface includes distinct values for approval, public visibility, urgency, activity, expiration, group, category, comments, flag count, prayer count, moderation flags, sentiment, answer, and the original request before AI formatting. That source-code observation describes the implementation at immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`; it does not establish how a particular installation is configured. [Prayer Request detail view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts)

The most important boundary is that classification is not authorization. Categories organize requests, while secured pages control which teams can reach category-scoped experiences. Group association adds a separate group-specific scope but should not be treated as a substitute for reviewing page and block security. [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests)

## Prayer Request Intake And Lifecycle

Most public requests are entered through the Prayer Request Entry block. Administrators can also enter requests internally from `People > Prayer > Add Prayer Request`. The external block is customizable, so an agent should inspect the actual block rather than assuming the default Rock configuration remains in place. [Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests)

Evidence-supported Prayer Request Entry settings include:

- **Category Selection:** A configured parent exposes its child categories as choices.
- **Default Category:** When category selection is hidden, Rock assigns the configured default category.
- **Enable Auto-Approve:** Makes submitted requests immediately available to the prayer team.
- **Expires After (Days):** Determines how long an approved request remains active, but this entry-block setting applies only when automatic approval is enabled.
- **Enable Urgent Flag:** Lets the requester mark a request urgent.
- **Enable Comments Flag:** Lets the requester choose whether comments are allowed.
- **Default Allow Comments Setting:** Controls the initial state of that comments choice.
- **Enable Public Display Flag:** Lets the requester indicate whether the request may be displayed publicly.
- **Character Limit:** Limits the entered request length.
- **Save Success Text and navigation settings:** Control the post-submission experience.
- **Workflow:** Launches a configured workflow after submission and makes the submitted request available to it.
- **Prayer Request Attributes:** Add organization-defined fields to the request-entry process.

These settings are documented for the v19 Prayer Request Entry experience. [Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests)

Do not describe the expiration-period setting as a general retention policy. The approved claim is narrower: the Prayer Request Entry block’s expiration period controls the active period for an approved request when automatic approval is enabled. The supplied evidence does not define deletion, archival, legal retention, or the behavior of every other request-creation surface.

A workflow-based intake is also supported at the implementation level. At the supplied immutable commit, Rock’s `Prayer Request Add` workflow action creates a prayer request and can optionally place the resulting request into a workflow attribute. Its inputs include requester or name/email values and other request properties exposed by the action. This is source-code evidence, not confirmation that a workflow has been configured or secured in an installation. [Prayer Request Add source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Workflow/Action/People/PrayerRequestAdd.cs)

Rapid Attendance Entry is another possible intake surface. The approved RockU distillation says it can collect prayer requests when its block settings enable that action, and the supplied source model includes request text, category, urgency, and public-display values. Confirm the installed version and block configuration before treating it as an active ministry intake route. [Rapid Attendance Entry training](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) [Rapid Attendance Entry request model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryPrayerRequestBag.cs)

## Categories, Visibility, And Page Security

Prayer categories help administrators find requests and help prayer teams select a workable subset. Administrators can maintain categories under `Administration > Settings > Prayer Categories`. When requesters are allowed to select a category, the children of the Prayer Request Entry block’s configured parent are presented as options. When that selection is hidden, the block’s default category is assigned instead. [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories)

Categories can also scope prayer-team blocks. For example, a team-specific page can contain a Prayer Session or Prayer Card View block configured for that ministry’s category. This should be paired with page security limiting the page to the intended team. Official documentation states that security applied to a prayer category controls access to the category itself in administrative settings and pickers but does not flow down to the category’s prayer requests. [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories)

Accordingly:

- Do not assume category security protects request content.
- Do not expose an unrestricted Prayer Request List to a ministry team merely because categories are secured.
- Do use page security and a category-scoped team block for ministry-specific queues.
- Do review the block’s public-only setting independently of approval and page access.
- Do test with an account that has exactly the intended team role.

The Prayer Card View block can be configured to display only public requests or all requests available to its query. The Prayer Request List implementation also has a “Show Public Only” mode, while visibility of its approval column depends on both a block setting and the current person’s approval authorization. These are implementation observations from the supplied official documentation and immutable source excerpt, not proof of current local settings. [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block) [Prayer Request List options](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts)

## Teams, Approval, And Human Moderation

Official guidance divides the normal operating model into two roles:

- **Prayer Administrator:** Enters card-submitted requests and reviews flagged or unapproved requests.
- **Prayer Team:** Prays for requests and flags content that should not remain visible in the prayer-team experience.

[Prayer Team Roles](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles)

If automatic approval is disabled, new requests remain unavailable to prayer sessions until an administrator approves them. If it is enabled, new requests are immediately available, making responsive flag review especially important. [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests)

Administrators work from `People > Prayer`. The request list can be filtered for flagged or unapproved items. From there, an authorized administrator can inspect details, change approval or urgency, edit the request and expiration date, record an answer, delete the request, or re-approve it. Re-approving a previously flagged request clears its flags and allows the approved request to return to prayer sessions. [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests)

Prayer-team flagging is controlled by block settings. Once the configured flag threshold is reached, Rock unapproves the request, removing it from an approved-only prayer-team experience until administrative review. The documented default example uses a one-person threshold, but the threshold is configurable. [Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests)

A flag is a review signal, not a complete care response. Official examples include requests exposing a worker’s identity or describing possible abuse or self-harm. The evidence does not define who must be contacted, what reporting law applies, or what response time is required. Those decisions belong to the organization’s reviewed care and safeguarding policy. [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests)

## AI-Assisted Processing And Moderation

Rock v19 documentation describes category-level AI automation for submitted prayer requests. An active AI provider is required. A category can select a provider or, when none is selected, use Rock’s first active provider. Documented capabilities include text cleanup, name removal, sentiment classification, automatic categorization among child categories, moderation flags, a moderation-alert workflow, and a public-appropriateness check. [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

When public-appropriateness checking is enabled for a category using an active AI provider, a request judged unsuitable for public display has its public flag set to false and its flag count increased by one. This does not establish that the request is unapproved, that staff have reviewed it, or that an escalation workflow ran. [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

AI category settings can pass from a parent to its direct children. They do not cascade through an inheriting child to grandchildren. Keep that one-level boundary in mind when designing category trees or audit each deeper category explicitly. [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

Automatic categorization also depends on the entry block’s default category. Rock categorizes among the available children of that category, so an unexpected default parent can produce an unexpected classification scope. [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

The Prayer Session and Prayer Request Detail blocks can display a disclaimer when AI has modified a request. The original request remains available to authorized administrators in the internal detail experience while editing. Treat access to that original text as sensitive because it may contain information removed from the displayed version. [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

Prayer comments have a separate AI approval path. The v19 administration documentation describes enabling approvals and AI approvals on the Prayer Comment note type under `Administration > Settings > Note Types`, then supplying approval guidelines. Comments rejected by that configured review are removed. This is separate from request-level category AI settings and should be tested independently. [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests)

## Prayer Sessions And Prayer Card View

The Prayer Session block presents active categories, lets the team choose categories, and then works through individual requests. Urgent requests appear first; remaining requests are ordered from least prayed-for to most prayed-for. Viewing a request records another prayer count. If enabled, team members can add comments or flag the request before moving on. [Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session)

Comment entry has its own permission boundary. Official documentation states that the `RSR - Prayer Access` role alone does not grant permission to add prayer comments out of the box. If that role should be allowed to comment, it must be granted Edit rights on the Prayer Comment note type. An agent should inspect the note-type permissions instead of inferring comment access from page access. [Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session)

Prayer Card View is an alternate card-based experience. It ships with Rock but is not placed on a page by default, so it must be added manually to an external-site page. Selecting its prayer action records the prayer. Supported settings include category scope, public-only filtering, team flagging and threshold, ordering, campus filtering, maximum results, and workflows launched after prayer or flag actions. [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block)

When Prayer Card View launches a workflow:

- A prayed workflow receives the prayer request as its entity and identifies the actor through the `PrayerOfferedByPersonId` workflow attribute.
- A flagged workflow receives the prayer request as its entity and identifies the actor through the `FlaggedByPersonId` workflow attribute.

The receiving workflow must define and handle those attributes correctly. [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block)

A maximum-result limit can make a large card page manageable, but requests beyond the cutoff are unavailable through that block result. Confirm that ordering and maximum-results settings do not systematically hide requests from the team. [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block)

## Group-Specific Prayer Requests

Supplying a group’s GUID through the `GroupGuid` URL parameter to Prayer Request Entry associates the new request with that group and limits it to the group’s members. The entry page does not visibly change merely because the parameter is present, so the association must be confirmed from the administrative prayer-request details. [Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests)

The association is immutable through the documented behavior: once a prayer request is associated with a group, that group cannot be changed or removed. Validate the target group before distributing or using an entry URL. [Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests)

Prayer Session and Prayer Card View use the same parameter for retrieval:

- With `GroupGuid`, they return requests associated with the identified group.
- Without `GroupGuid`, they exclude group-associated requests.

Therefore, a normal prayer-team page will not automatically include group-associated requests, and a group prayer route should not be tested without its parameter. [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests)

Do not treat a GUID as the only privacy control. Confirm that the page requires the intended authentication and authorization and test with a member, a signed-in nonmember, and an anonymous visitor. The supplied evidence establishes group scoping behavior but does not provide a live permission test for any installation.

## Comments, Communications, And Follow-Up

The `Send Prayer Comments` job sends prayer-team comments to the person who submitted the request. It ignores requests where Allow Comments is disabled. The job is included with Rock but must be configured, and Rock provides a Prayer Request Comments Digest system communication for this purpose. [Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest)

The digest includes the original request and comments added since the previous job run. On the first run, it includes all existing comments. It sends to the email address recorded on the prayer request, which may differ from the requester’s current profile email. [Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication)

Category settings on the job control scope:

- To cover requests regardless of category, leave Prayer Categories blank and enable Include Child Categories.
- To restrict delivery, select categories and deliberately choose whether their children are included.
- The Save Communications setting controls whether sent messages are retained as Rock communication records; choosing not to save does not prevent sending.

[Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest)

Because the destination comes from the request rather than necessarily from the current person profile, an address correction on a person record does not prove that an existing request’s digest destination changed. Inspect the request-specific email when diagnosing delivery or privacy concerns.

A submission workflow can turn selected prayer requests into care actions. Official documentation gives the example of recognizing a hospitalization request and notifying the person responsible for hospital visits. This is an example of a configured workflow, not built-in universal pastoral-care routing. [Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests) [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests)

## Outreach Toolbox And Scheduled Care Touchpoints

The official Rock Mobile v19 preview presents Outreach Toolbox as a signed-in mobile experience for maintaining personal outreach contacts and scheduled prayer or connection touchpoints. Its dashboard can surface people due for today’s actions. [Outreach Toolbox v19 preview](https://www.youtube.com/watch?v=LNcx8t0mlQ4) [Outreach Toolbox dashboard short](https://www.youtube.com/shorts/c6T9Ha13jKE)

The preview also shows:

- Onboarding choices for assignment days and reminder preferences.
- Jobs that define reminder time-of-day values.
- Contact-specific prayer and connection cadences.
- Completed touchpoint history.
- Periodic pulse updates.
- Configurable milestone prompts.

[Outreach Toolbox v19 preview](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s) [Outreach Toolbox contact tracking](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s)

This evidence is a release-oriented demonstration, not a verified deployment contract. Before ministry use, confirm the current Rock server version, mobile shell support, page placement, authentication, block settings, permissions, jobs, reminder schedules, push-notification delivery, and who can view contact history.

## Community Implementation Patterns

The following are community-contributed examples, not official Rock behavior or reviewed core implementations:

- **Urgent-request email:** A Rock v10 community recipe uses a workflow, a confirmation page, and a button on Prayer Request Detail to email a prayer team about an urgent request. Treat recipient selection, message content, and page security as local design decisions. [Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)
- **Prayer Card comments:** A Rock v13 community recipe adds a comment modal to Prayer Card View using a separate page, Notes Entry block, context routing, Lava, and an iframe. Current core capabilities and security should be evaluated before reproducing it. [Prayer Card View comment modal](https://community.rockrms.com/recipes/350)
- **Prayer Card answers:** Another Rock v13 recipe adds a workflow entry route and card action for recording an answer. It describes a first-answer-wins customization rather than a core Card View guarantee. [Prayer Card View answered prayer](https://community.rockrms.com/recipes/389)
- **SMS capture:** A community recipe routes matching inbound SMS messages into a workflow and notes that Rock v11 introduced a Prayer Request Add workflow action. Prefer the supported workflow action over the recipe’s legacy direct-SQL examples, subject to current-version verification. [SMS Prayer Request Capture](https://community.rockrms.com/recipes/135)
- **Public prayer wall:** A community recipe displays public requests and uses a Lava webhook with write SQL to increment prayer counts. The recipe itself warns about the SQL. Do not copy that mutation pattern into production without an independent security, concurrency, authorization, and current-API review. [Create a Prayer Wall](https://community.rockrms.com/recipes/149)
- **Live prayer chat:** A community recipe embeds a third-party chat widget into a Rock page header. This creates an external-service privacy and data-governance boundary that the core prayer system does not manage. [Prayer live-chat example](https://community.rockrms.com/recipes/157)
- **Pastoral-care summary:** A community recipe depends on a third-party Pastoral Care plugin, local workflows, scheduled jobs, recipient groups, and optionally login-bearing links. It is an example of plugin-dependent care coordination, not a core prayer workflow. [Automatic Pastoral Care Summary Email](https://community.rockrms.com/recipes/121)
- **Personalized prayer message:** An unpublished community draft proposes a custom prayer attribute and workflows to create more specific weekly messages. Because the source is marked Draft and Not Published, it should not be used as an implementation specification. [Personalized Prayer Requests draft](https://community.rockrms.com/recipes/72)

## Version And Authority Caveats

The principal documentation excerpts identify themselves as current for Rock v19.0. Local behavior may differ because of block generation, installed Rock version, retained legacy pages, plugins, custom Lava, workflows, or permissions. [Prayer documentation](https://community.rockrms.com/documentation/engagement/prayer)

Relevant release history includes:

- Rock v17.0 fixed the Obsidian Prayer Request Entry block so request attributes not marked Public remain hidden.
- Rock v17.2 fixed `PersonId` handling in the Obsidian Prayer Request Detail block when creating a request.
- Rock v17.5 fixed approval audit fields not updating when approval occurred in the Obsidian detail block.
- Rock v19.1 widened prayer-request text in the Prayer Request List.
- Rock v19.3 fixed Prayer Comment List filtering, Row Lava access, and related performance issues.
- Rock v19.5 restored Prayer Request List settings and behavior missed during its Obsidian conversion.
- Rock v20.0 release notes were supplied from an alpha release surface and mention a comments-count column on Prayer Request List; do not treat alpha behavior as production-stable without current verification.

[Rock Core Release Notes](https://www.rockrms.com/releasenotes)

The supplied GitHub excerpts use immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They clarify implementation surfaces but do not prove the installed code, local configuration, permissions, or database state.

## Troubleshooting Decision Tree

### A submitted request does not appear for the prayer team

1. Confirm the request saved successfully.
2. Inspect whether it is approved. If automatic approval is disabled, approve it through the administrative request list.
3. Confirm it is active and inspect its expiration date.
4. Check whether the team block is scoped to a different category.
5. Check whether Public Only is enabled while the request is non-public.
6. Inspect its flag count and whether the configured threshold unapproved it.
7. Determine whether it is group-associated. A normal session without `GroupGuid` excludes group requests.
8. Inspect the block’s maximum-results and ordering settings.
9. Test the page using the affected team member’s exact permissions.

[Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests) [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block) [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests)

### A sensitive request is still visible

1. Identify where it is visible: administrative list, secured team page, public page, group page, or communication.
2. Inspect approval and public visibility separately.
3. Check whether the page or block is restricted to public requests.
4. Review page security; do not rely on category security to protect request content.
5. If flagging is expected to remove it, inspect the enabled flagging setting, threshold, and current count.
6. If AI public-appropriateness checking is expected, inspect the category’s active provider and inherited settings.
7. Check whether the category is a grandchild that did not receive inherited AI settings.
8. Have an authorized administrator edit, unapprove, or delete the request as the situation requires.

[Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations) [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests)

### Prayer-team members cannot add comments

1. Confirm the request allows comments.
2. Confirm the team page actually uses an experience that exposes comment entry.
3. Inspect Edit security on the Prayer Comment note type.
4. Do not assume `RSR - Prayer Access` grants comment-entry rights by itself.
5. If comment AI approvals are enabled, determine whether the comment was saved and then rejected.
6. Retest with the exact prayer-team account.

[Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests)

### Prayer-comment digests are not being delivered

1. Confirm the Send Prayer Comments job exists, is configured, and has run successfully.
2. Confirm the request has Allow Comments enabled.
3. Inspect the job’s category selection and Include Child Categories setting.
4. Inspect the email stored on the prayer request rather than relying on the person’s current profile email.
5. Confirm that a new comment exists within the job’s unsent window.
6. Inspect the configured system communication and outbound communication provider.
7. Determine whether Save Communications is enabled before expecting a saved communication record.
8. Perform a bounded test with non-sensitive content and verify receipt.

[Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) [Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication)

### A group prayer page is empty or shows the wrong scope

1. Confirm the request was created with the intended `GroupGuid`.
2. Inspect the request’s group from its administrative details.
3. Remember that the association cannot be changed or removed after creation.
4. Confirm the prayer page URL carries the same `GroupGuid`.
5. Confirm the page uses Prayer Session or Prayer Card View.
6. Test as an intended group member.
7. Test as a signed-in nonmember and anonymous visitor to validate the surrounding access controls.

[Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests) [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests)

### AI processing is inconsistent across categories

1. Confirm an active AI provider exists.
2. Inspect the provider selected on each relevant category.
3. Identify whether settings are local or inherited.
4. Check category depth; inheritance reaches direct children but not grandchildren.
5. Confirm the Prayer Request Entry block’s default category is the intended parent for automatic categorization.
6. Compare the displayed request with the original available to authorized administrators.
7. Review moderation flags, public status, and flag count independently.
8. Stop automated reliance if results are unsafe or materially inconsistent; retain human review.

[Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

### Outreach reminders do not arrive

1. Confirm Rock Mobile and the server are on a supported version for the intended Outreach Toolbox experience.
2. Confirm the person is signed in and can reach the configured page.
3. Inspect onboarding choices for assignment days and reminders.
4. Inspect the relevant job configuration and time-of-day values.
5. Verify push-notification permissions and delivery in the target mobile environment.
6. Confirm the contact has a due prayer or connection cadence.
7. Compare the dashboard, touchpoint history, and expected next date.
8. Stop calling the rollout complete until an intended user receives and acts on a real test reminder.

[Outreach Toolbox v19 preview](https://www.youtube.com/watch?v=LNcx8t0mlQ4)

## Agent Task Recipes

### Recipe: Configure moderated public prayer intake

**Outcome:** Public submissions enter the intended category and do not reach the prayer team without the chosen approval gate.

1. Open the external Prayer Request Entry block.
2. Set the category parent and default category deliberately.
3. Choose whether category selection is visible.
4. Decide whether automatic approval is appropriate.
5. If automatic approval is enabled, set the supported expiration period and establish a flagged-request review cadence.
6. Configure urgent, comments, and public-display choices.
7. Review which prayer attributes are public.
8. Submit test requests covering ordinary, urgent, private, comment-disabled, and sensitive cases.
9. Verify administrative state and prayer-team visibility for each test.

**Inspect:**

- Category and default-category assignment.
- Approval, public, urgent, active, expiration, and Allow Comments values.
- Page security and block scope.
- Flag threshold.

**Do not assume:**

- Category security protects the request.
- Expiration is a deletion policy.
- Automatic approval is safe merely because flagging is enabled.

**Stop when:**

- A sensitive test reaches an unintended audience.
- A required approval or visibility control cannot be explained from the observed configuration.

[Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests) [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories)

### Recipe: Operate the administrator moderation queue

**Outcome:** Flagged and unapproved requests receive documented human disposition.

1. Filter the prayer-request list for unapproved requests.
2. Filter or sort for flagged requests.
3. Open each request and review its text, public status, urgency, category, expiration, and flags.
4. Edit sensitive or inaccurate text only under the organization’s ministry policy.
5. Choose a disposition: remain unapproved, re-approve, or delete.
6. If re-approving, confirm that flags clear and the request re-enters the intended team scope.
7. Review the Prayer Comments list separately for comment moderation.

**Inspect:**

- Whether AI modified the request.
- The original request when authorized and necessary.
- Any safety concern requiring action outside Rock’s prayer queue.

**Stop when:**

- The request triggers an organizational safeguarding or crisis-response procedure.
- The administrator lacks authority to decide the disposition.

[Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests) [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests)

### Recipe: Build a secured ministry-specific prayer queue

**Outcome:** A ministry team sees only the intended category scope through a secured page.

1. Create or select a page for the ministry prayer team.
2. Restrict page access to the intended security role.
3. Add Prayer Session or Prayer Card View.
4. Configure the block for the ministry’s category.
5. Decide whether the block should show public requests only.
6. Configure flagging, threshold, ordering, and maximum results.
7. Test with an administrator, intended team member, unrelated signed-in person, and anonymous visitor.
8. Confirm that the administrative Prayer Request List remains restricted to administrators.

**Do not assume:**

- Category security flows to request records.
- Page access automatically grants comment-entry rights.
- A small maximum-results value still gives the team complete coverage.

[Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block)

### Recipe: Create and verify a group prayer route

**Outcome:** New requests are permanently associated with the correct group and appear only through that group’s prayer route.

1. Resolve the intended group’s GUID through an authorized administrative method.
2. Construct the Prayer Request Entry URL with `GroupGuid`.
3. Verify the target group before distributing the URL.
4. Submit a non-sensitive test request.
5. Confirm the group association in administrative request details.
6. Open the Prayer Session or Prayer Card View route with the same parameter.
7. Confirm the test request appears.
8. Remove the parameter and confirm the group request is excluded.
9. Test surrounding page security with member, nonmember, and anonymous accounts.

**Do not assume:**

- The entry page will visibly identify the group.
- An incorrect group association can be edited later.
- Possession of the GUID alone is an adequate authorization design.

**Stop when:**

- The request is associated with the wrong group; do not continue creating production requests through that URL.

[Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests) [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests)

### Recipe: Enable prayer-comment digests

**Outcome:** Allowed comments are delivered to request-specific email addresses within the intended category scope.

1. Configure a scheduled job using the Send Prayer Comments job type.
2. Select the Prayer Request Comments Digest system communication.
3. For all categories, leave Prayer Categories blank and enable Include Child Categories.
4. For a narrower scope, select categories and explicitly choose child inclusion.
5. Decide whether sent communications should be saved.
6. Confirm test requests have Allow Comments enabled.
7. Add a non-sensitive test comment.
8. Run the job in a controlled test.
9. Verify the digest includes the original request and expected comments.
10. Verify delivery to the email stored on the request.
11. Run the job again after adding another comment and confirm it sends only comments added since the prior run.

**Do not assume:**

- The person profile’s current email is the destination.
- Comment permission and digest eligibility are the same control.
- An unsaved communication was not sent.

[Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) [Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication)

### Recipe: Add workflow-based care follow-up

**Outcome:** A qualifying prayer event creates a bounded care action without exposing the request broadly.

1. Choose the supported trigger: request submission, Prayer Card prayed action, or Prayer Card flagged action.
2. Define the workflow’s entity and required attributes.
3. For Prayer Card actions, define the appropriate actor attribute: `PrayerOfferedByPersonId` or `FlaggedByPersonId`.
4. Add explicit criteria for the ministry condition being handled.
5. Assign the resulting activity only to authorized care workers.
6. Limit communication content to the minimum necessary.
7. Add an auditable completion or disposition state.
8. Test with synthetic requests that should and should not trigger.
9. Verify that unauthorized users cannot open the workflow or linked request.

**Inspect:**

- Workflow security and assignments.
- Entity and actor values.
- Links embedded in notifications.
- Whether the condition requires immediate action outside the workflow.

**Stop when:**

- The workflow would send sensitive content to an unverified recipient.
- The organization has not defined the human owner or escalation policy.

[Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests) [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block)

### Recipe: Introduce AI assistance with human review

**Outcome:** AI processing is limited to known categories and produces reviewable results.

1. Confirm an active AI provider.
2. Select a small pilot category.
3. Configure only the required capabilities.
4. If using inheritance, keep the pilot to direct child categories or configure deeper categories individually.
5. Confirm the entry block’s default category supports the intended automatic-categorization scope.
6. Enable an AI disclaimer where appropriate.
7. Submit synthetic examples covering names, formatting, private content, public appropriateness, and moderation concerns.
8. Compare processed text with the original.
9. Inspect public status, flag count, category, sentiment, and moderation results.
10. Establish a human review owner before broadening the scope.

**Do not assume:**

- AI inheritance reaches grandchildren.
- A non-public result is also unapproved.
- AI moderation satisfies crisis or safeguarding procedures.

**Stop when:**

- AI changes meaning, exposes sensitive content, or produces an unsafe moderation result.

[Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations)

### Recipe: Validate Outreach Toolbox for prayer touchpoints

**Outcome:** A signed-in mobile user can see, complete, and receive reminders for an assigned prayer touchpoint.

1. Confirm the target server and mobile versions.
2. Confirm the Outreach Toolbox page is placed in the mobile shell.
3. Verify authentication and permissions for a pilot user.
4. Complete onboarding with known assignment days and reminder preferences.
5. Configure a test contact and prayer cadence.
6. Verify the dashboard shows the due action.
7. Complete the touchpoint and inspect its history.
8. Configure and run the applicable reminder job.
9. Verify the push notification on the target device.
10. Review who can see contact details, history, and pulse updates.

**Stop when:**

- Authentication, permissions, job execution, or real-device notification delivery remains unverified.

[Outreach Toolbox v19 preview](https://www.youtube.com/watch?v=LNcx8t0mlQ4) [Outreach Toolbox dashboard short](https://www.youtube.com/shorts/c6T9Ha13jKE)

## Known Gaps And Live Verification

No live Rock instance was reviewed for this guide. Before relying on it operationally, perform a bounded, read-only verification of:

- Installed Rock version and whether each relevant page uses legacy or Obsidian blocks.
- Prayer Request Entry settings on every intake page.
- Approval, expiration, category, public-display, comments, and workflow settings.
- Prayer Session and Prayer Card View placement, scope, ordering, limits, and security.
- Prayer Comment note-type permissions and AI approval settings.
- Prayer-category structure, security, and AI inheritance.
- Active AI provider and actual processing results.
- Group prayer routes and member/nonmember authorization behavior.
- Send Prayer Comments job configuration, run history, category scope, and request-specific destinations.
- Outbound email delivery and whether communications are saved.
- Workflow entity mappings, actor attributes, recipients, and page security.
- Rock Mobile shell compatibility, authentication, Outreach Toolbox placement, jobs, and push delivery.
- Impact of version-specific fixes, especially on installations earlier than v17.5 or v19.5.

The evidence does not establish:

- A universal definition of confidential, pastoral, or public prayer content.
- A crisis, self-harm, abuse, or mandatory-reporting procedure.
- Required response times or escalation owners.
- A retention or deletion policy for expired requests and comments.
- Whether group GUID scoping alone prevents unauthorized access.
- Whether community recipes remain compatible or secure on current Rock releases.
- Whether any third-party pastoral-care or chat plugin is installed, supported, or approved.
- Whether the v20 alpha Prayer Request List behavior will remain unchanged in a stable release.

These are genuine gaps, not details to infer from model names, block titles, source properties, or nearby documentation.

## Source Map

### Approved official prayer documentation

- [Prayer overview](https://community.rockrms.com/documentation/engagement/prayer) — Documentation structure and v19 context.
- [Intro to Prayer](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/intro-to-prayer) — Intake, approval, session ordering, and lifecycle overview.
- [Prayer Team Roles](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles) — Administrator and team responsibilities.
- [Prayer Categories](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) — Category selection, defaults, category scoping, and page-security boundary.
- [Work With Flagged Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/work-with-flagged-requests) — Flagging, thresholds, and administrative disposition.
- [Enter Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests) — Entry settings, expiration condition, attributes, and submission workflows.
- [Administer Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests) — Approval, filtering, editing, answers, deletion, and comment moderation.
- [Create Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests) — `GroupGuid` creation behavior and immutable association.
- [Pray for Group Prayer Requests](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests) — Group-specific retrieval behavior.
- [Start a Prayer Session](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) — Session ordering, prayer counts, flagging, comments, and comment security.
- [Prayer Card View Block](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block) — Card experience, placement, filtering, limits, and action workflows.
- [Prayer Request Comment Digest](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) — Job configuration and request eligibility.
- [Prayer Request Comments Communication](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication) — Digest contents, incremental behavior, and destination address.
- [Prayer AI Automations](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations) — Request AI features, inheritance, public checks, and human-review caveats.

### Release and implementation evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — Version-specific prayer fixes and alpha caveats.
- [Prayer Request Add source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Workflow/Action/People/PrayerRequestAdd.cs) — Immutable implementation evidence for workflow-created requests.
- [Prayer Request detail view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts) — Immutable implementation evidence for request fields.
- [Prayer Request List options](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts) — Immutable implementation evidence for public-only and approval-column behavior.
- [Rapid Attendance Entry request model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryPrayerRequestBag.cs) — Immutable implementation evidence for adjunct prayer intake fields.

### Official training and release demonstrations

- [Prayer Requests training](https://community.rockrms.com/rocku/prayer/prayer-requests) — Staff training context.
- [Rapid Attendance Entry training](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) — Adjunct intake context.
- [Outreach Toolbox v19 preview](https://www.youtube.com/watch?v=LNcx8t0mlQ4) — Signed-in mobile outreach and prayer-touchpoint demonstration.
- [Outreach Toolbox dashboard short](https://www.youtube.com/shorts/c6T9Ha13jKE) — Due-action dashboard demonstration.

### Community examples

- [Email Urgent Prayer Requests](https://community.rockrms.com/recipes/338)
- [Prayer Card View comment modal](https://community.rockrms.com/recipes/350)
- [Prayer Card View answered prayer](https://community.rockrms.com/recipes/389)
- [SMS Prayer Request Capture](https://community.rockrms.com/recipes/135)
- [Create a Prayer Wall](https://community.rockrms.com/recipes/149)
- [Prayer live-chat example](https://community.rockrms.com/recipes/157)
- [Automatic Pastoral Care Summary Email](https://community.rockrms.com/recipes/121)
- [Personalized Prayer Requests draft](https://community.rockrms.com/recipes/72)