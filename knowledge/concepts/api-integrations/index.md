---
id: concept-api-integrations
title: API And Integrations
generated: true
last_built: 2026-06-18T16:39:00+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - security
  - workflows
  - lava
  - model-map
---

# API And Integrations

REST APIs, API v1/v2, OData, webhooks, external integrations, and GitHub/source-code landmarks.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `API And Integrations` spans security, workflows, lava, model-map. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_community_hubs, triumph_resources, rock_podcast_rss, rock_developer, rock_api_docs, rock_community_site.
- Related tags found in source records: api, development, lava, obsidian, security, operations, releases, sql.
- Source detail types include: developer_doc, question, recipe, rock_community_site, rock_developer, rock_lava_docs, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | Mailgun webhook | 02:49 | Mailgun or similar provider webhooks can update Rock communication status, but the endpoint should be treated as an external integration with authentication and logging requirements. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| Media Watch Transcript Insight | communication status | 02:57 | Email delivery and engagement events are more useful when they are tied back to the Rock communication record or person context that generated the message. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| Media Watch Transcript Insight | reporting value | 01:43 | Provider event data should be summarized into operational reports that help staff understand delivery health without exposing unnecessary raw event detail. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | AI and automation | 00:00 | AI should be treated as an assistive ministry operations layer: useful for drafting, summarizing, classifying, and routing work, but still requiring human judgment and local policy before action. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | staff training | 03:12 | Public guidance should frame AI adoption around responsible enablement, including data boundaries, staff training, review expectations, and clear ownership of final decisions. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | data and reporting | 03:36 | For Rock-adjacent automation, agents should verify source data and system state rather than treating generated AI output as an authoritative record. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Escaping the Complexity Trap \| Ep 209 Transcript Insight | ministry process |  | the Escaping the Complexity Trap episode gives public operational perspective on ministry process design; use it to frame questions for staff process review rather than as authoritative configuration guidance. | [source](https://shows.acast.com/rock-cast/episodes/episode-209-escaping-the-complexity-trap) |
| Escaping the Complexity Trap \| Ep 209 Transcript Insight | Rock operations |  | When applying Rock operations and administration ideas from Escaping the Complexity Trap, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://shows.acast.com/rock-cast/episodes/episode-209-escaping-the-complexity-trap) |
| Escaping the Complexity Trap \| Ep 209 Transcript Insight | risk and governance |  | When applying risk, governance, permissions, and policy review ideas from Escaping the Complexity Trap, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://shows.acast.com/rock-cast/episodes/episode-209-escaping-the-complexity-trap) |
| v19 Updates and Shaping Ministry Culture in 2026 \| Ep 206 Transcript Insight | staff training | 05:51 | the v19 Updates and Shaping Ministry Culture in 2026 episode gives public operational perspective on staff training and operational readiness; use it to frame questions for staff process review rather than as authoritative configuration guidance. | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| v19 Updates and Shaping Ministry Culture in 2026 \| Ep 206 Transcript Insight | Rock operations | 00:05 | When applying Rock operations and administration ideas from v19 Updates and Shaping Ministry Culture in 2026, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| v19 Updates and Shaping Ministry Culture in 2026 \| Ep 206 Transcript Insight | ministry process | 03:33 | When applying ministry process design ideas from v19 Updates and Shaping Ministry Culture in 2026, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| Media Watch Transcript Insight | chat feature scope | 03:04 | A church mobile chat experience should define expected features such as threaded messages, reactions, notifications, moderation, and staff access before implementation. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) |
| Media Watch Transcript Insight | group sync | 03:11 | If chat membership is based on Rock groups or teams, synchronization rules and permission boundaries need to be explicit so conversations match the ministry structure. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) |
| Media Watch Transcript Insight | staff web access | 02:27 | Staff may need a web-facing companion experience even when the primary community surface is mobile, especially for moderation, support, and repeated communication work. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) |
| Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World Transcript Insight | Rock operations | 00:00 | the Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World episode gives public operational perspective on Rock operations and administration; use it to frame questions for staff process review rather than as authoritative configuration guidance. | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World Transcript Insight | AI and automation | 04:24 | When applying AI, automation, and responsible tool use ideas from Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World Transcript Insight | ministry process | 02:25 | When applying ministry process design ideas from Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team Transcript Insight | ministry process | 00:21 | the Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team episode gives public operational perspective on ministry process design; use it to frame questions for staff process review rather than as authoritative configuration guidance. | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team Transcript Insight | staff training | 03:35 | When applying staff training and operational readiness ideas from Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team Transcript Insight | data and reporting | 03:43 | When applying reporting, analytics, and measurement ideas from Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| community-reviewed | operational_guidance | Provider event data should be summarized into operational reports that help staff understand delivery health without exposing unnecessary raw event detail. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| community-reviewed | operational_guidance | Email delivery and engagement events are more useful when they are tied back to the Rock communication record or person context that generated the message. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| community-reviewed | operational_guidance | When applying staff training and operational readiness ideas from Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| community-reviewed | operational_guidance | When applying reporting, analytics, and measurement ideas from Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| community-reviewed | operational_guidance | When applying Rock operations and administration ideas from Escaping the Complexity Trap, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-209-escaping-the-complexity-trap) |
| community-reviewed | operational_guidance | the v19 Updates and Shaping Ministry Culture in 2026 episode gives public operational perspective on staff training and operational readiness; use it to frame questions for staff process review rather than as authoritative configuration guidance. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| community-reviewed | operational_guidance | When applying ministry process design ideas from Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| community-reviewed | operational_guidance | the Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team episode gives public operational perspective on ministry process design; use it to frame questions for staff process review rather than as authoritative configuration guidance. _(live verification recommended)_ | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| community-reviewed | operational_guidance | Staff may need a web-facing companion experience even when the primary community surface is mobile, especially for moderation, support, and repeated communication work. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) |
| community-reviewed | operational_guidance | AI should be treated as an assistive ministry operations layer: useful for drafting, summarizing, classifying, and routing work, but still requiring human judgment and local policy before action. _(live verification recommended)_ | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| community-reviewed | operational_guidance | When applying AI, automation, and responsible tool use ideas from Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| community-reviewed | operational_guidance | the Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World episode gives public operational perspective on Rock operations and administration; use it to frame questions for staff process review rather than as authoritative configuration guidance. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| community-reviewed | operational_guidance | When applying ministry process design ideas from v19 Updates and Shaping Ministry Culture in 2026, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| community-reviewed | operational_guidance | When applying Rock operations and administration ideas from v19 Updates and Shaping Ministry Culture in 2026, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| community-reviewed | operational_guidance | A church mobile chat experience should define expected features such as threaded messages, reactions, notifications, moderation, and staff access before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) |
| community-reviewed | operational_guidance | For Rock-adjacent automation, agents should verify source data and system state rather than treating generated AI output as an authoritative record. _(live verification recommended)_ | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| More |  | 12 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_api_docs`: 1
- `rock_community_hubs`: 2
- `rock_community_site`: 10
- `rock_core_release_notes`: 6
- `rock_demo_api_docs_v1`: 1
- `rock_demo_api_docs_v2`: 1
- `rock_developer`: 35
- `rock_lava_docs`: 2
- `rock_model_map`: 12
- `rock_podcast_rss`: 4
- `rock_qa`: 3
- `rock_recipes`: 5
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 9

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Five Layers of Defense from Bot Attacks | triumph_resources | Bot traffic is frustrating, unpredictable and heavier than most churches realize. If you’re seeing late-night exception alerts, sluggish page loads or a flood of fake form entries, you’re not alone. The good news is that there are practical steps you can take to reduce unwanted bots and protect your Rock site from spam and overload. Here are five actionable ways to harden your site, starting with simple, quick wins... | [source](https://www.triumph.tech/resources/defense-from-bot-attacks) |
| GitHub Spotlight: 1/8/2025 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release v17.0.35, released on 1/8/2025. v16.10 Highlights A new optional Lava merge field, <!--[[ SignatureDetails ]]--> , has been added to the Electronic Signatures templates. This field allows you to insert a signer's final signature directly into the document, enabling the signature to appear throughout the document rather than being limited to the bottom. Issue... | [source](https://www.triumph.tech/resources/github-spotlight-182025) |
| GitHub Spotlight: 2/4/2026 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release 19.0.5, released on February 4, 2025. 18.3 Highlights Added a new Command Timeout setting to the Process Group History job (default 300 seconds) to prevent SQL timeouts when processing large volumes of group history records. Added a Campus Type filter to the campus picker in the Prayer Request Detail block, allowing users to narrow campus selections. Fixed a... | [source](https://www.triumph.tech/resources/github-spotlight-242026) |
| GitHub Spotlight: 8/7/2025 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release 18.0.10, released on 8/5/2025. 17.4 Highlights Added a filter to the Obsidian Device List block to show only Active or Inactive devices. Added a filter to Data Views to include individuals based on their group or sign-up schedules. Improved system communication templates to check the recipients’ preferred communication method before delivery. Issue 6167 Fixed... | [source](https://www.triumph.tech/resources/github-spotlight-872025) |
| GitHub Spotlight: 9/6/2024 | triumph_resources | Below is what's new in Rock's Github for pre-alpha release v17.0.27 that was released on 9/5/2024. v16.7 A new setting was added to allow rejecting security cookies that are older than a date specified. This could be helpful in situations where a login token was inappropriately used or shared. Note that this will require all individuals to re-login if they had logged in before the date provided. Logic has been added... | [source](https://www.triumph.tech/resources/github-spotlight-962024-2) |
| New Resi Media Sync Plugin for Rock | triumph_resources | Seamless Video Integration at Your Fingertips We’re excited to announce the Resi Media Sync plugin for Rock! This integration lets you effortlessly import metadata from videos from your Resi account into Rock media files. Once connected, any new video added in Resi automatically appears in your Rock instance, ready for embedding and detailed tracking. Whether it’s a sermon, event, or announcement, this sync ensures... | [source](https://www.triumph.tech/resources/new-resi-media-sync-plugin-for-rock) |
| One Thing Every Executive Pastor Needs to Know About Rock Integrations | triumph_resources | Let’s start at the beginning - What’s an API? Simply put, an API is a way that two software programs can talk to each other and share data. Just as humans share data through a common language so do computers. In life there’s often a right way and a wrong way to do things. Software development is no different. When done wrong, one common issue we see with Rock integrations is how they use the Rock API (data sharing... | [source](https://www.triumph.tech/resources/one-thing-every-executive-pastor-needs-to-know-about-rock-integrations) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | triumph_resources | AI's Role in Digital Ministry adds public-safe guidance for AI use around Rock: treat AI as assistive, define data and approval boundaries, train staff, and verify outputs against real systems before acting. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| What To Do About the Microsoft Windows PrintNightmare Vulnerability | triumph_resources | You may have recently heard about a windows security vulnerability in the news called PrintNightmare (CVE-2021-1675). Although your firewall should be configured to prevent such an attack, Microsoft recommends the following PowerShell commands be run on your Windows server to disable the print spooler service (you can also disable this service manually in the UI). Stop-Service -Name Spooler -Force Set-Service -Name... | [source](https://www.triumph.tech/resources/microsoft-windows-printnightmare-vulnerability) |
| API Documentation | rock_api_docs | Rock API Resources Build, integrate and create. Discover Rock’s APIs and take advantage of Rock's valuable database. API v1 Classic. Reliable. Now legacy. Try the API v1 Login: admin / admin API v2 Fast. Designed to do more. Try the API v2 Login: admin / admin Shared Resources Guides and walkthroughs that equip you for Rock's API. API Documentation The full reference. All things API. Introduction to Rock API... | [source](https://community.rockrms.com/api-docs) |
| Creating APIs Using Lava | rock_lava_docs | Creating APIs Using Lava Please note that there isn't any security on running Lava through these webhooks. Please be careful what data you expose through them. We've seen how we can add dynamic content using Lava. Now, let's look at how we can use Lava to create new custom APIs. This method of creating APIs is a great way to build things like an XML API for Apple TV or a Roku channel. This is all done through a... | [source](https://community.rockrms.com/lava/lava-api) |
| Using Lava Remotely | rock_lava_docs | Using Lava Remotely Many people assume that Lava is limited to being used inside Rock. For the most part that is true, but we have created some neat tools to help you extend the power of Lava to other websites running alternative technologies. Lava REST Endpoint The Lava REST endpoint is a simple endpoint that takes Lava as input and returns the rendered template as output. This endpoint is easily used by any... | [source](https://community.rockrms.com/lava/remote-lava) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Lava Endpoint](../../model-map/models/lava-endpoint.md) | CMS | 19.1.8 | 52 | 23 | 36 | 13 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Person Token](../../model-map/models/person-token.md) | Core | 19.1.8 | 26 | 12 | 16 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Rest Action](../../model-map/models/rest-action.md) | CMS | 19.1.8 | 44 | 15 | 28 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Rest Controller](../../model-map/models/rest-controller.md) | CMS | 19.1.8 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [History Login](../../model-map/models/history-login.md) | Security | 19.1.8 | 52 | 22 | 34 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent](../../model-map/models/ai-agent.md) | AI | 19.1.8 | 45 | 16 | 30 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session](../../model-map/models/ai-agent-session.md) | AI | 19.1.8 | 28 | 12 | 19 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session Anchor](../../model-map/models/ai-agent-session-anchor.md) | AI | 19.1.8 | 29 | 15 | 20 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session History](../../model-map/models/ai-agent-session-history.md) | AI | 19.1.8 | 27 | 14 | 19 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Skill](../../model-map/models/ai-agent-skill.md) | AI | 19.1.8 | 22 | 8 | 13 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Provider](../../model-map/models/ai-provider.md) | AI | 19.1.8 | 43 | 15 | 28 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Skill](../../model-map/models/ai-skill.md) | AI | 19.1.8 | 43 | 13 | 28 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable scraped Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `AI Agent.AIAgentSkills` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.AttributeValues` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.Attributes` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.AvatarBinaryFile` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.CreatedByPersonId` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.CreatedByPersonName` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.EntityStringValue` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.IdKey` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 18.1 | Core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 | [source](https://www.rockrms.com/releasenotes) |
| 16.1 | Communication | Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694 | [source](https://www.rockrms.com/releasenotes) |
| 15.5 | Communication | Improved the Mailgun integration to use the API Key for tracking opens, etc. if the HTTP Webhook Signing Key is not defined, as well as logging a single exception to alert Rock admins of this missing key value. Fixes: #5780 | [source](https://www.rockrms.com/releasenotes) |
| 15.4 | Communication | Added support for separate "API key" and "HTTP webhook signing key" values within Mailgun integration. Fixes: #5694 | [source](https://www.rockrms.com/releasenotes) |
| 18.2 | API | Fixed an error that prevented the Workflows Action Launch API endpoint from functioning. Fixes: #6604 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | API | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to the DataView. Fixes: #6348 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### REST API

Keywords: `rest, api v1, api v2`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| The Rock Rest API | rock_developer | Rock features a REST-based web service that supports integration with third-party websites and applications. The REST API is also utilized by various internal Rock components to retrieve and modify data such as populating item pickers, displaying person badges, and showing charts for metrics. The API is also used for external applications that access Rock data, such as the check-scanner and the financial statement... | [source](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) |
| API Documentation | rock_api_docs | Rock API Resources Build, integrate and create. Discover Rock’s APIs and take advantage of Rock's valuable database. API v1 Classic. Reliable. Now legacy. Try the API v1 Login: admin / admin API v2 Fast. Designed to do more. Try the API v2 Login: admin / admin Shared Resources Guides and walkthroughs that equip you for Rock's API. API Documentation The full reference. All things API. Introduction to Rock API... | [source](https://community.rockrms.com/api-docs) |
| Using Lava Remotely | rock_developer | Using Lava Remotely Many people assume that Lava is limited to being used inside Rock. For the most part that is true, but we have created some neat tools to help you extend the power of Lava to other websites running alternative technologies. Lava REST Endpoint The Lava REST endpoint is a simple endpoint that takes Lava as input and returns the rendered template as output. This endpoint is easily used by any... | [source](https://community.rockrms.com/lava/remote-lava) |
| RX2018 Watch Video | rock_community_site | Using the Rock REST API Mike Peterson Summary Learn the basics of REST and how to use it in a Rock environment to connect and interact with data. We’ll also cover OData and Swagger, two tools for building and viewing the Rock REST API. Download Presentation Download Video | [source](https://community.rockrms.com/subscriptions/rx2018/using-the-rock-rest-api) |
| Rock Rest API v2 | rock_demo_api_docs_v2 | Rock Rest API v2 | [source](https://rock.rocksolidchurchdemo.com/api/v2/docs/index) |
| REST API for Schedules | rock_community_site | 0 REST API for Schedules 0 Leroy Eldred posted 3 Years Ago I'm trying to access the REST API for Schedules. Works fine under Postman, but throws an exception when run from a browser. No set method for property 'FriendlyScheduleText' in type 'Rock.Model.Schedule'. We're running v 12.8 | [source](https://community.rockrms.com/ask/developing/2710) |

### API Authentication

Keywords: `auth, token, bearer, api key`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Using Lava Remotely | rock_developer | Using Lava Remotely Many people assume that Lava is limited to being used inside Rock. For the most part that is true, but we have created some neat tools to help you extend the power of Lava to other websites running alternative technologies. Lava REST Endpoint The Lava REST endpoint is a simple endpoint that takes Lava as input and returns the rendered template as output. This endpoint is easily used by any... | [source](https://community.rockrms.com/lava/remote-lava) |
| Rock Security | rock_developer | See https://community.rockrms.com/developer/videos/70 (from the beta launch at CITRT 2014) Block Security Order Entity Parent Authority Block Security Actions Entity Type Security (Admin UI) Custom Action Verbs PersonActionIdentifier The RSVP system uses our newer 'non-security' type identification token generator (called PersonActionIdentifier) which identifies a person for only one particular action. In this case,... | [source](https://community.rockrms.com/developer/303---blast-off/rock-security) |
| Check Scanning | rock_developer | Overview Check Scanner use document intelligence prebuilt model specifically for scanning US Check. Below is instruction on how to set up the document intelligence for check scanning. Set up Document Intelligence (AI Foundry) 1. Open Document Intelligence in your AI Foundry. 2. Click "Create". 3. Fill out the project and instance details, then continue. 4. Review the configuration and create the resource. 5. After... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail/check-scanning) |
| Applications | rock_developer | Learn how to create a Roku application in Rock to manage your TV content. Application Settings When creating or editing a Roku application, you have access to the following configuration options. Enable Page Views Whether (or not) page interactions should be written to track the usage of your application. Page View Retention Duration The duration (in days) to retain the page interactions that are written. API Key... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| GitHub Spotlight: 9/6/2024 | triumph_resources | Below is what's new in Rock's Github for pre-alpha release v17.0.27 that was released on 9/5/2024. v16.7 A new setting was added to allow rejecting security cookies that are older than a date specified. This could be helpful in situations where a login token was inappropriately used or shared. Note that this will require all individuals to re-login if they had logged in before the date provided. Logic has been added... | [source](https://www.triumph.tech/resources/github-spotlight-962024-2) |
| webrequest not running?? | rock_community_site | 0 webrequest not running?? 1 Kelvin Liu posted 3 Years Ago Hi I have noticed that since sometime in mid March our lava codes which use webrequest have all been failing silently. No noticeable errors just suddenly not doing what it has been doing for more than a year(s). We were on Rock v9.x ... Just upgraded to 10 (in May) but I know it's not related to the upgrade because the problem has been there since March.... | [source](https://community.rockrms.com/ask/developing/2708) |
| Creating An App | rock_developer | Creating a TV application from scratch. Creating an Application In your Rock instance, go ahead and navigate to Admin Tools > CMS Configuration > Apple TV Apps . Once there, create a new site. Let's break this down. Name - the name of your application. This is private to your Rock Instance, and isn't what it has to be named when published to the App Store. Description - An optional description of the application.... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) |
| Feature Branch Merging Workflow | rock_developer | Before merging your feature branch into develop or a hotfix branch do the following: From your feature branch copy the migration Up\Down code you were testing with to a text editor temporarily. Check out the destination branch (develop, hotfix, etc.) in SmartGit. Obtain the migration token . From PackageManager console run Add-Migration <your migration name> against the destination branch you checked out in... | [source](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/standard-ef-migrations/feature-branch-merging-workflow) |

### Webhooks

Keywords: `webhook, integration`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | Mailgun webhook | 02:49 | Mailgun or similar provider webhooks can update Rock communication status, but the endpoint should be treated as an external integration with authentication and logging requirements. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| Media Watch Transcript Insight | communication status | 02:57 | Email delivery and engagement events are more useful when they are tied back to the Rock communication record or person context that generated the message. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| Media Watch Transcript Insight | reporting value | 01:43 | Provider event data should be summarized into operational reports that help staff understand delivery health without exposing unnecessary raw event detail. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session adds public-safe technical context for email-status and webhook workflows. It discusses Mailgun calling back into Rock through a webhook, using delivery or engagement data to update Rock-side communication context, and treating external provider callbacks as integration points that need authentication, logging, and operational reporting. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| The Rock Rest API | rock_developer | Rock features a REST-based web service that supports integration with third-party websites and applications. The REST API is also utilized by various internal Rock components to retrieve and modify data such as populating item pickers, displaying person badges, and showing charts for metrics. The API is also used for external applications that access Rock data, such as the check-scanner and the financial statement... | [source](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) |
| Lava Webhook to Create an iCal (.ics) File | rock_community_site | 0 Lava Webhook to Create an iCal (.ics) File Shared by Brandon Meeks , The Creek 23 days ago 16.13 Event, General, Web Intermediate What does it do? This webhook creates a file that can be downloaded to add an item to someone's calendar on their device. The contents of the .ics file are written per RFC 5545 specifications. How do I set it up? Navigate to General Settings -> Defined Types -> Lava Webhook Create new... | [source](https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file) |
| Lava Webhook to Create an iCal (.ics) File | rock_recipes | 0 Lava Webhook to Create an iCal (.ics) File Shared by Brandon Meeks , The Creek 23 days ago 16.13 Event, General, Web Intermediate What does it do? This webhook creates a file that can be downloaded to add an item to someone's calendar on their device. The contents of the .ics file are written per RFC 5545 specifications. How do I set it up? Navigate to General Settings -> Defined Types -> Lava Webhook Create new... | [source](https://community.rockrms.com/recipes/540) |
| Creating APIs Using Lava | rock_developer | Creating APIs Using Lava Please note that there isn't any security on running Lava through these webhooks. Please be careful what data you expose through them. We've seen how we can add dynamic content using Lava. Now, let's look at how we can use Lava to create new custom APIs. This method of creating APIs is a great way to build things like an XML API for Apple TV or a Roku channel. This is all done through a... | [source](https://community.rockrms.com/lava/lava-api) |
| Step 1: Create OpenAI Account | rock_recipes | 6 ChatGPT Shortcode Shared by Brian Davis , ONE&ALL Church 3 years ago 10.0 General Intermediate In this recipe we'll walk through the steps to build a basic integration in Rock RMS to communicate with ChatGPT to ask questions via the ChatGPT API. I'll also provide some examples of how this integration might be used. The recipe might look alarmingly long, but I'll have you chatting with an AI in a couple minutes and... | [source](https://community.rockrms.com/recipes/362) |
| Extending Communication Transports | rock_developer | SMS Transports In Rock v12.1, we’ve added the ISmsPipelineWebhook interface that will let you identify the location of any corresponding webhook. The SmsPipelineWebhookPath property will be used by the SMS Pipeline block to display the full URL to the webhook which is useful when administrators are setting up the interface with the remote service. | [source](https://community.rockrms.com/developer/303---blast-off/extending-communication-transports) |
| Docker Desktop | rock_developer | We use Docker Desktop to provide a clean database for each suite of integration tests. This makes sure the database is 1) in a known clean state and 2) does not require any specific steps to prepare the database for tests. To run the integration tests you just need to make sure Docker Desktop is installed and running. Everything else will be automatic. The first time you run the tests for that specific version of... | [source](https://community.rockrms.com/developer/developer-codex/coding-standards/testing/unit-testing/docker-desktop) |


## Lava Capability References

This concept depends on the generated Lava capability layer. Agents should use the stable guidance first, then verify syntax and behavior against the official source and the live Rock instance.

- Reference index: [../lava/lava-reference-index.md](../lava/lava-reference-index.md)
- Safety matrix: [../lava/lava-safety-matrix.md](../lava/lava-safety-matrix.md)
- Agent usage examples: [../lava/lava-agent-usage-examples.md](../lava/lava-agent-usage-examples.md)
- Machine-readable rows: [agent/lava-capabilities.jsonl](../../../agent/lava-capabilities.jsonl)

## Rebuild Dependencies

- Source records: `143`
- Lava capability source records: `53`
- Approved claims: `30`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
