---
id: concept-prayer-care
title: Prayer And Care
generated: true
last_built: 2026-06-18T23:01:18+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 50
depends_on_topics:
  - people
  - groups
  - communications
  - workflows
  - security
  - cms
---

# Prayer And Care

Prayer requests, prayer teams, moderation, categories, care follow-up, visibility, communication, and privacy-sensitive ministry workflows.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Prayer And Care` spans people, groups, communications, workflows, security, cms. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_recipes, rock_rocku, rock_core_release_notes, rock_model_map, triumph_resources.
- Related tags found in source records: usage, operations, workflow, security, admin, training, lava, development.
- Source detail types include: documentation_article, question, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Rapid Attendance Entry Transcript Insight | rapid attendance setup | 00:32 | Rapid Attendance Entry starts from a selected group and attendance date, with location and schedule values available when the group and attendance context support them. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| Rapid Attendance Entry Transcript Insight | attendance and care capture | 02:17 | The block can combine attendance marking with family editing, adding family members, person notes, prayer requests, and workflow launch actions from the same operational screen. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| Rapid Attendance Entry Transcript Insight | block configuration | 03:14 | Rapid Attendance Entry is configurable enough to support multiple page variants, so teams can create focused versions for different ministry workflows instead of using one catch-all setup everywhere. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| Prayer Requests Transcript Insight | staff training | 00:11 | The Prayer Requests RockU lesson provides training context for staff training and operational readiness; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) |
| Prayer Requests Transcript Insight | Rock operations | 02:07 | For Rock operations and administration, Prayer Requests should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) |


## Source Coverage

- `rock_core_release_notes`: 7
- `rock_documentation`: 17
- `rock_model_map`: 12
- `rock_qa`: 1
- `rock_recipes`: 7
- `rock_rocku`: 16
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Prayer | rock_documentation | SECTIONS [Prayer Overview](?Version=v19.0#prayer-overview) [Prayer Requests](?Version=v19.0#prayer-requests) [Prayer Team Power Tools](?Version=v19.0#prayer-team-power-tools) ### Prayer Overview Articles [About Prayer in Rock](/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0) [Prayer Team Roles](/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)... | [source](https://community.rockrms.com/documentation/engagement/prayer) |
| Prayer Team Power Tools | rock_documentation | [Start a Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0) [Prayer Card View Block](/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0) [Prayer Request Comment Digest](/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0) [Prayer Request Comments... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools) |
| Prayer Card View Block | rock_documentation | An alternate way for your prayer team to pray is to use the *Prayer Card View* block. This block is similar to the [Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) block described in the prior article, except prayer requests are viewed as cards on the page. All the person needs to do is click the Pray button to have the prayer counted. The Prayer Card View block ships... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block) |
| Prayer Requests | rock_documentation | [Enter Prayer Requests](/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0) [Administer Prayer Requests](/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0) [Create Group Prayer Requests](/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0) [Pray for Group Prayer... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests) |
| Prayer Overview | rock_documentation | [About Prayer in Rock](/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0) [Prayer Team Roles](/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0) [Prayer Categories](/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0) [Work With Flagged... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview) |
| Enter Prayer Requests | rock_documentation | So now that you understand how prayer functions in Rock, let's look at the details of entering and managing requests. # Adding a Request Most people will enter prayer requests online through the *Prayer Request Entry* block on your website under `Connect > Prayer`. Prayer administrators can also add prayer requests internally from `People > Prayer > Add Prayer Request`. # About Default Configurations Don't forget to... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests) |
| Administer Prayer Requests | rock_documentation | After requests have been entered, and before the Prayer Team can pray for them, the Prayer Administrator needs to take a look at them. One exception to this process is if the requests are set to auto-approve when they are entered. In that case, the Prayer Team has immediate access to new requests. All administration work is done under `People > Prayer`. Here, you can select to add a new prayer request, view current... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests) |
| Prayer Request Comment Digest | rock_documentation | The importance of prayer and the impact it has can’t be overstated. In times of trouble, it helps just simply knowing that people are out there praying for you. Using the *Send Prayer Comments* job, you can ensure that those who submit prayer requests will know that they have the power of prayer behind them. # Setting up the Job As the prayer team comments on requests, you can enable a job to send those comments to... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) |
| Prayer Categories | rock_documentation | Once you have a large number of prayer requests in Rock, it could be difficult to view all of them or to find the one(s) you are looking for. Prayer Categories were created to help you find exactly what you are looking for as an Administrator and to help prayer teams as they work through requests. When a prayer request is entered on the website by a requester, it is automatically given the default category *General*... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) |
| Prayer Team Roles | rock_documentation | You'll basically need two serving roles for prayer requests: Prayer Administrator and Prayer Team. Here’s what each role should be responsible for. ## Prayer Administrator * Enter requests submitted on cards during your weekend services * Review requests that are flagged or unapproved ## Prayer Team * Pray for the requests * Flag any requests that seem inappropriate for public viewing | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles) |
| About Prayer in Rock | rock_documentation | Prayer support is vital to churches of all sizes and the people who support them. After all, what can be more important to your church than building connections through prayer? We’ve joined the natural power of prayer with the built-in power and simplicity of Rock’s relationship management features in a dynamic way. Whether sharing requests or accessing them, Rock will take care of the details so you can focus on... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock) |
| Start a Prayer Session | rock_documentation | Once it's time for the prayer team to begin working through the requests, they will find them on the website under `Connect > Prayer > Prayer Team`. When a member of the prayer team starts a prayer session, all categories with active prayers will show on the webpage, along with a number of active prayers in each. Once one or more categories are selected, they will be auto-filled for the next session. Note... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Prayer Request](../../model-map/models/prayer-request.md) | Prayer | 19.1.8 | 69 | 33 | 51 | 18 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.1.8 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.1.8 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.1.8 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.1.8 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.1.8 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.1.8 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.1.8 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.1.8 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.1.8 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection](../../model-map/models/content-collection.md) | CMS | 19.1.8 | 49 | 21 | 34 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable scraped Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 17.0 | Prayer | Fixed an issue where Prayer Request Attributes not marked as "Public" were incorrectly displaying in the Obsidian version of the Prayer Request Entry block. These Attributes are now properly hidden on the Prayer Request Entry block. Fixes: #6253 | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Prayer | Improved the Prayer Request List block to display prayer request text at a wider width for better readability. Fixes: #6824 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | Prayer | Fixed an issue where approving a Prayer Request in the Obsidian Prayer Request Detail block did not update the ApprovedOnDateTime and ApprovedByPersonAliasId fields. Fixes: #6403 | [source](https://www.rockrms.com/releasenotes) |
| 17.2 | Prayer | Fixed an issue where the Prayer Request Detail block in Obsidian did not recognize the PersonId URL parameter, which prevented person data from being pre-filled when creating a new prayer request. Fixes: #6357 | [source](https://www.rockrms.com/releasenotes) |
| 17.0 | Prayer | Added support for editing custom attributes within the Mobile Prayer Request block. This enhancement allows individuals to update custom attributes when submitting or managing prayer requests from a mobile device. Be aware that Rock Mobile doesn't support all Attribute Types but it does support the most common ones. | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Mobile | Added a Campus Type filter to the campus picker on the Prayer Request Detail block. This allows individuals to narrow the list of selectable campuses when adding a new prayer request. | [source](https://www.rockrms.com/releasenotes) |
| 17.0 | CRM | Added a new feature to Prayer which will optionally run several pre-configured AI completions on saved prayer requests. If you plan on using this feature, read the Tech Bulletin item on this topic. | [source](https://www.rockrms.com/releasenotes) |

## Subguides

### Prayer Requests

Keywords: `prayer request, request, category, expiration, approval`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Prayer Requests Transcript Insight | staff training | 00:11 | The Prayer Requests RockU lesson provides training context for staff training and operational readiness; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) |
| Prayer Requests Transcript Insight | Rock operations | 02:07 | For Rock operations and administration, Prayer Requests should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Prayer | rock_documentation | SECTIONS [Prayer Overview](?Version=v19.0#prayer-overview) [Prayer Requests](?Version=v19.0#prayer-requests) [Prayer Team Power Tools](?Version=v19.0#prayer-team-power-tools) ### Prayer Overview Articles [About Prayer in Rock](/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0) [Prayer Team Roles](/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)... | [source](https://community.rockrms.com/documentation/engagement/prayer) |
| Prayer Team Power Tools | rock_documentation | [Start a Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0) [Prayer Card View Block](/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0) [Prayer Request Comment Digest](/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0) [Prayer Request Comments... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools) |
| Prayer Card View Block | rock_documentation | An alternate way for your prayer team to pray is to use the *Prayer Card View* block. This block is similar to the [Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) block described in the prior article, except prayer requests are viewed as cards on the page. All the person needs to do is click the Pray button to have the prayer counted. The Prayer Card View block ships... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block) |
| Prayer Requests | rock_documentation | [Enter Prayer Requests](/documentation/engagement/prayer/prayer-requests/enter-prayer-requests?Version=v19.0) [Administer Prayer Requests](/documentation/engagement/prayer/prayer-requests/administer-prayer-requests?Version=v19.0) [Create Group Prayer Requests](/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests?Version=v19.0) [Pray for Group Prayer... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests) |
| Prayer Overview | rock_documentation | [About Prayer in Rock](/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0) [Prayer Team Roles](/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0) [Prayer Categories](/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0) [Work With Flagged... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview) |
| Enter Prayer Requests | rock_documentation | So now that you understand how prayer functions in Rock, let's look at the details of entering and managing requests. # Adding a Request Most people will enter prayer requests online through the *Prayer Request Entry* block on your website under `Connect > Prayer`. Prayer administrators can also add prayer requests internally from `People > Prayer > Add Prayer Request`. # About Default Configurations Don't forget to... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests) |
| Administer Prayer Requests | rock_documentation | After requests have been entered, and before the Prayer Team can pray for them, the Prayer Administrator needs to take a look at them. One exception to this process is if the requests are set to auto-approve when they are entered. In that case, the Prayer Team has immediate access to new requests. All administration work is done under `People > Prayer`. Here, you can select to add a new prayer request, view current... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests) |
| Prayer Request Comment Digest | rock_documentation | The importance of prayer and the impact it has can’t be overstated. In times of trouble, it helps just simply knowing that people are out there praying for you. Using the *Send Prayer Comments* job, you can ensure that those who submit prayer requests will know that they have the power of prayer behind them. # Setting up the Job As the prayer team comments on requests, you can enable a job to send those comments to... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) |
| Prayer Categories | rock_documentation | Once you have a large number of prayer requests in Rock, it could be difficult to view all of them or to find the one(s) you are looking for. Prayer Categories were created to help you find exactly what you are looking for as an Administrator and to help prayer teams as they work through requests. When a prayer request is entered on the website by a requester, it is automatically given the default category *General*... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) |
| Prayer Team Roles | rock_documentation | You'll basically need two serving roles for prayer requests: Prayer Administrator and Prayer Team. Here’s what each role should be responsible for. ## Prayer Administrator * Enter requests submitted on cards during your weekend services * Review requests that are flagged or unapproved ## Prayer Team * Pray for the requests * Flag any requests that seem inappropriate for public viewing | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles) |

### Teams And Moderation

Keywords: `prayer team, moderation, approval, confidential, visibility`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Prayer | rock_documentation | SECTIONS [Prayer Overview](?Version=v19.0#prayer-overview) [Prayer Requests](?Version=v19.0#prayer-requests) [Prayer Team Power Tools](?Version=v19.0#prayer-team-power-tools) ### Prayer Overview Articles [About Prayer in Rock](/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0) [Prayer Team Roles](/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0)... | [source](https://community.rockrms.com/documentation/engagement/prayer) |
| Prayer Team Power Tools | rock_documentation | [Start a Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0) [Prayer Card View Block](/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0) [Prayer Request Comment Digest](/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0) [Prayer Request Comments... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools) |
| Prayer Card View Block | rock_documentation | An alternate way for your prayer team to pray is to use the *Prayer Card View* block. This block is similar to the [Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) block described in the prior article, except prayer requests are viewed as cards on the page. All the person needs to do is click the Pray button to have the prayer counted. The Prayer Card View block ships... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block) |
| Prayer Overview | rock_documentation | [About Prayer in Rock](/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock?Version=v19.0) [Prayer Team Roles](/documentation/engagement/prayer/prayer-overview/prayer-team-roles?Version=v19.0) [Prayer Categories](/documentation/engagement/prayer/prayer-overview/prayer-categories?Version=v19.0) [Work With Flagged... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview) |
| Administer Prayer Requests | rock_documentation | After requests have been entered, and before the Prayer Team can pray for them, the Prayer Administrator needs to take a look at them. One exception to this process is if the requests are set to auto-approve when they are entered. In that case, the Prayer Team has immediate access to new requests. All administration work is done under `People > Prayer`. Here, you can select to add a new prayer request, view current... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/administer-prayer-requests) |
| Prayer Request Comment Digest | rock_documentation | The importance of prayer and the impact it has can’t be overstated. In times of trouble, it helps just simply knowing that people are out there praying for you. Using the *Send Prayer Comments* job, you can ensure that those who submit prayer requests will know that they have the power of prayer behind them. # Setting up the Job As the prayer team comments on requests, you can enable a job to send those comments to... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) |
| Prayer Categories | rock_documentation | Once you have a large number of prayer requests in Rock, it could be difficult to view all of them or to find the one(s) you are looking for. Prayer Categories were created to help you find exactly what you are looking for as an Administrator and to help prayer teams as they work through requests. When a prayer request is entered on the website by a requester, it is automatically given the default category *General*... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories) |
| Prayer Team Roles | rock_documentation | You'll basically need two serving roles for prayer requests: Prayer Administrator and Prayer Team. Here’s what each role should be responsible for. ## Prayer Administrator * Enter requests submitted on cards during your weekend services * Review requests that are flagged or unapproved ## Prayer Team * Pray for the requests * Flag any requests that seem inappropriate for public viewing | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-team-roles) |
| About Prayer in Rock | rock_documentation | Prayer support is vital to churches of all sizes and the people who support them. After all, what can be more important to your church than building connections through prayer? We’ve joined the natural power of prayer with the built-in power and simplicity of Rock’s relationship management features in a dynamic way. Whether sharing requests or accessing them, Rock will take care of the details so you can focus on... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/about-prayer-in-rock) |
| Start a Prayer Session | rock_documentation | Once it's time for the prayer team to begin working through the requests, they will find them on the website under `Connect > Prayer > Prayer Team`. When a member of the prayer team starts a prayer session, all categories with active prayers will show on the webpage, along with a number of active prayers in each. Once one or more categories are selected, they will be auto-filled for the next session. Note... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session) |

### Follow-Up And Communications

Keywords: `follow-up, communication, notification, pastoral care`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Prayer Team Power Tools | rock_documentation | [Start a Prayer Session](/documentation/engagement/prayer/prayer-team-power-tools/start-a-prayer-session?Version=v19.0) [Prayer Card View Block](/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block?Version=v19.0) [Prayer Request Comment Digest](/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest?Version=v19.0) [Prayer Request Comments... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools) |
| Prayer Request Comment Digest | rock_documentation | The importance of prayer and the impact it has can’t be overstated. In times of trouble, it helps just simply knowing that people are out there praying for you. Using the *Send Prayer Comments* job, you can ensure that those who submit prayer requests will know that they have the power of prayer behind them. # Setting up the Job As the prayer team comments on requests, you can enable a job to send those comments to... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comment-digest) |
| Prayer Request Comments Communication | rock_documentation | The example email pictured below is generated from the “Prayer Request Comments Digest” system communications template. 1. **Greeting**- The greeting at the top of the email includes the person’s name and references the date on which the person submitted the prayer request. 2. **Request** - The original prayer request that was submitted is copied here for reference. 3. **Comments** - Any comments that have been... | [source](https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication) |
| Automatic Pastoral Care Summary Email | rock_recipes | 5 Automatic Pastoral Care Summary Email Shared by Leah Jennings , Northside Christian Church 6 years ago 8.10 Communications, Serving Intermediate PURPOSE We use Southeast's Pastoral Care plugin to manage our hospitalizations, nursing home residents, and homebound attendees. We have a hospital team that volunteers on rotation to visit those people, and our staff also need the list to be praying over them and... | [source](https://community.rockrms.com/recipes/121) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session gives public-safe guidance for online groups and digital community workflows. It emphasizes that Rock-backed digital ministry can connect group participation, communication, data, and follow-up when teams intentionally design the path from online engagement to pastoral care or in-person connection. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| All This to Increase a Metric? | rock_recipes | 5 Using Workflows, Data Views, and Group Sync to Engage Church Online Shared by Sonja Waltman , LCBC Church 6 years ago 9.0 Operations, Communications Beginner Have you ever attended a church and received a card in the mail that week from the pastor thanking you for joining the church that weekend? Have you ever received a call from the worship leader inviting you back for the following weekend? What about a warm... | [source](https://community.rockrms.com/recipes/158) |
| Connections Notification - Future Follow-Up | rock_recipes | 6 Connections Notification - Future Follow-Up Shared by Tiffany Bunney , Fellowship Greenville 6 years ago General Intermediate The RockRMS Connection Request system includes a powerful feature which allows the Connector to set the state of a request to Future Follow Up. This removes the request from the listing of requests until the Follow-up Date. The only negative of this system is that the Connector would need... | [source](https://community.rockrms.com/recipes/166) |
| Rock Shop Preview | rock_shop_plugins | This plugin is only available on the Rock Shop. To install this plugin, select Admin Tools > Rock Shop from your own instance of Rock. Pastoral Care by Southeast Christian Church Free Note: plugin details are provided here only as a reference for what is available in the Rock Shop. To install this plugin, select Admin Tools > Rock Shop from your own instance of Rock. Required Rock Version 14.0 Documentation... | [source](https://www.rockrms.com/rockshop/plugin/84) |
| The Problem | rock_recipes | 6 Automated Follow Up Shared by Randy Aufrecht , ONE&ALL Church 4 years ago 11.0 Communications Advanced MOVE FROM PAPERWORK TO RELATIONSHIPS Stop clicking your screen and start clicking with people by creating a custom automated system in Rock. All of the details from the RX2021 presentation are located at https://oneandall.church/rx2021takeaway The Problem How do we connect new guests effectively? Lost physical... | [source](https://community.rockrms.com/recipes/244) |
| Rock Core Release Notes | rock_core_release_notes | Fixed an issue where Connection Request workflows using a "Future Follow-up Date Reached" trigger would throw exceptions and fail to add the "Follow-Up Date Reached" activity. Fixes: #6310 | [source](https://www.rockrms.com/releasenotes) |


## Rebuild Dependencies

- Source records: `61`
- Approved claims: `0`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
