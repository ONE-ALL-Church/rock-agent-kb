---
id: concept-ai-agents-automation
title: AI Agents And Automation
generated: true
last_built: 2026-06-18T19:34:55+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - security
  - api-integrations
  - workflows
  - platform-configuration
  - data-views
  - reports
  - operations
  - lava
---

# AI Agents And Automation

Rock AI agents, custom tools, automation patterns, tool security, least privilege, prompt/tool boundaries, review gates, and live verification.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `AI Agents And Automation` spans security, api-integrations, workflows, platform-configuration, data-views, reports. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_podcast_rss, rock_community_hubs, rock_developer, rock_community_site, rock_model_map, rock_core_release_notes.
- Related tags found in source records: lava, development, api, obsidian, security, finance, check-in, mobile.
- Source detail types include: developer_doc, documentation_bookcontent, question, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | release governance | 00:48 | Use the episode as release-awareness context: podcast release discussion can flag security updates, alpha/beta status, and future model-changing work, but upgrade guidance must still be verified against official release notes and the local Rock version. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | community-prioritized roadmap | 01:54 | Community feedback channels such as Rocket Chat, calls, church visits, and conferences can explain why areas like Connections rise in priority, but agents should treat that as roadmap context rather than proof that a feature is present in a given instance. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | AI group matching | 13:31 | For AI-assisted group finding, implementation work needs church-specific matching rules: which group types are findable, which attributes describe affinity, and what boundaries keep the assistant away from inappropriate targets such as security roles. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | documentation currency | 15:00 | Documentation changes should be planned as part of UI and release work; major UI changes can create downstream screenshot and article-refresh work that must be tracked before public guidance is treated as current. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Media Watch Transcript Insight | community analytics | 00:30 | Data analytics meetups can help churches compare dashboards, process designs, and BI-tool choices against real ministry use cases instead of treating reporting as an isolated technical task. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | attendance flow | 36:49 | Attendance-flow analysis can move beyond aggregate weekend counts by classifying engagement patterns, prioritizing follow-up lists, and creating Rock connection requests for campus teams. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | AI governance | 52:13 | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | content selection | 03:12 | Manual curation still matters for sermon and video libraries because view counts alone do not capture pastoral impact, ministry priority, or whether a message should be highlighted again. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) |
| Media Watch Transcript Insight | analytics limits | 04:39 | Video analytics are useful for prioritization, but teams should compare them with qualitative feedback and ministry goals before changing content strategy. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) |
| Media Watch Transcript Insight | AI planning | 08:07 | AI can help draft sermon titles, category ideas, and reuse plans, but churches should keep human review over doctrinal wording, audience fit, and final publication. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) |
| Media Watch Transcript Insight | community review | 02:56 | Peer learning works best when Rock teams bring action-oriented examples, not only abstract tool discussions. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| Media Watch Transcript Insight | AI experimentation | 04:26 | Emerging technology and AI experiments should be bounded, documented, and reviewed before they affect Rock data or public ministry workflows. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| Media Watch Transcript Insight | mobile and finance requests | 06:10 | Mobile launch and finance work should be tracked as real operational projects with explicit owners, requirements, and verification steps. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| Media Watch Transcript Insight | online learning | 02:17 | Online next-step pathways can combine dashboards, content, and LMS when the church defines the discipleship path being supported. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| Media Watch Transcript Insight | AI guardrails | 07:13 | AI coaching should be framed as an assisted resource-routing layer with reviewable prompts, ministry-approved categories, and clear human oversight. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| Media Watch Transcript Insight | engagement measurement | 03:39 | Engagement goals should be tied to the path the church wants people to take, not simply to whether a digital tool was launched. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| Media Watch Transcript Insight | AI framing | 01:30 | AI should be introduced around concrete ministry workflows and reviewable outputs, not as a broad replacement for staff judgment. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/XaBRra9Brd) |
| Media Watch Transcript Insight | model landscape | 02:43 | Because AI model capabilities and vendor terms change quickly, churches should document which tools are approved and what data classes may be used with each one. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/XaBRra9Brd) |
| Media Watch Transcript Insight | policy and training | 02:13 | AI governance should include staff training, data-minimization rules, and a review path before AI-generated content or data summaries influence public communication or pastoral action. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/XaBRra9Brd) |
| Media Watch Transcript Insight | AI search | 02:47 | Intent-based AI search can improve discovery when it is grounded in approved church content and clearly tested against real user questions. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/a0BJvYDBpz) |
| Media Watch Transcript Insight | mobile and website integration | 01:01 | New website and app experiences should be evaluated together because users may move between public pages, logged-in mobile surfaces, search, profile, and next-step actions. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/a0BJvYDBpz) |
| Media Watch Transcript Insight | plugin governance | 02:35 | Before adopting AI or search plugins, teams should verify data sources, answer boundaries, security behavior, and whether generated results can be reviewed or tuned. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/a0BJvYDBpz) |
| Media Watch Transcript Insight | short-form content | 04:46 | Short-form video should be treated as ministry content with a clear next step, not only as entertainment or social promotion. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| Media Watch Transcript Insight | topic routing | 08:07 | Urgent or culturally timely topics can become good candidates for curated content paths when they are connected to trusted ministry resources and follow-up actions. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| Media Watch Transcript Insight | digital engagement | 09:27 | Digital content libraries work best when they connect messages, topics, and practical next steps instead of leaving users to browse isolated videos. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| Media Watch Transcript Insight | AI plugin evaluation | 02:30 | AI plugin ideas should be evaluated against real church tasks, content sources, and security expectations rather than adopted because the model capability is new. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| Media Watch Transcript Insight | workflow backlog | 00:42 | Community-hub follow-up emails and discussion prompts can serve as a backlog for future Rock workflows, content experiments, and review priorities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| Media Watch Transcript Insight | experimentation boundary | 02:27 | Emerging technology pilots should stay clearly labeled as experiments until output quality, data boundaries, and ministry usefulness are verified. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | implementation_pattern | Community-hub follow-up emails and discussion prompts can serve as a backlog for future Rock workflows, content experiments, and review priorities. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| community-reviewed | operational_guidance | Short-form video should be treated as ministry content with a clear next step, not only as entertainment or social promotion. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| community-reviewed | operational_guidance | Emerging technology pilots should stay clearly labeled as experiments until output quality, data boundaries, and ministry usefulness are verified. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| community-reviewed | operational_guidance | Manual curation still matters for sermon and video libraries because view counts alone do not capture pastoral impact, ministry priority, or whether a message should be highlighted again. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) |
| community-reviewed | operational_guidance | Mobile launch and finance work should be tracked as real operational projects with explicit owners, requirements, and verification steps. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| community-reviewed | operational_guidance | AI coaching should be framed as an assisted resource-routing layer with reviewable prompts, ministry-approved categories, and clear human oversight. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | Digital content libraries work best when they connect messages, topics, and practical next steps instead of leaving users to browse isolated videos. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| community-reviewed | operational_guidance | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| community-reviewed | operational_guidance | Online next-step pathways can combine dashboards, content, and LMS when the church defines the discipleship path being supported. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | Peer learning works best when Rock teams bring action-oriented examples, not only abstract tool discussions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdxwPqz) |
| community-reviewed | operational_guidance | Before adopting AI or search plugins, teams should verify data sources, answer boundaries, security behavior, and whether generated results can be reviewed or tuned. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/a0BJvYDBpz) |
| community-reviewed | operational_guidance | AI should be introduced around concrete ministry workflows and reviewable outputs, not as a broad replacement for staff judgment. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/XaBRra9Brd) |
| community-reviewed | operational_guidance | Urgent or culturally timely topics can become good candidates for curated content paths when they are connected to trusted ministry resources and follow-up actions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3GWBEN) |
| community-reviewed | operational_guidance | AI plugin ideas should be evaluated against real church tasks, content sources, and security expectations rather than adopted because the model capability is new. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/vzm1D4MBX6) |
| community-reviewed | operational_guidance | Engagement goals should be tied to the path the church wants people to take, not simply to whether a digital tool was launched. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | Data analytics meetups can help churches compare dashboards, process designs, and BI-tool choices against real ministry use cases instead of treating reporting as an isolated technical task. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| community-reviewed | operational_guidance | Video analytics are useful for prioritization, but teams should compare them with qualitative feedback and ministry goals before changing content strategy. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB98xJP8W) |
| community-reviewed | operational_guidance | For AI-assisted group finding, implementation work needs church-specific matching rules: which group types are findable, which attributes describe affinity, and what boundaries keep the assistant away from inappropriate targets such as security roles. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| More |  | 19 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_community_hubs`: 8
- `rock_community_site`: 11
- `rock_core_release_notes`: 2
- `rock_developer`: 40
- `rock_documentation`: 1
- `rock_model_map`: 12
- `rock_podcast_rss`: 3
- `rock_qa`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 3

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Resources | triumph_resources | All Best Practice (19) Triumph News (10) Leadership (7) Github Spotlight (35) Special Projects (3) June 1, 2026 Skip the Trial and Error: Borrow Our AI Playbook Introducing the AI Agentic Cohort with Claude. The AI skills, tools, and strategy our team uses every day are now available for your church staff. More Details May 21, 2026 GitHub Spotlight: 5/21/2026 Here’s what’s new in Rock’s GitHub for Pre-Alpha Release... | [source](https://www.triumph.tech/resources) |
| Resources | triumph_resources | All Best Practice (19) Triumph News (10) Leadership (7) Github Spotlight (35) Special Projects (3) June 1, 2026 Skip the Trial and Error: Borrow Our AI Playbook Introducing the AI Agentic Cohort with Claude. The AI skills, tools, and strategy our team uses every day are now available for your church staff. More Details May 21, 2026 GitHub Spotlight: 5/21/2026 Here’s what’s new in Rock’s GitHub for Pre-Alpha Release... | [source](https://www.triumph.tech/resources/page/1) |
| Skip the Trial and Error: Borrow Our AI Playbook | triumph_resources | The world is moving fast. Agentic AI is changing everything. And most church staff are still using AI the way they used it a year ago, if they're using it at all. At Triumph Tech, we couldn't keep working that way. So we didn't. This year, we rebuilt how our team uses AI. We moved past basic chat tools and into agentic AI, where Claude doesn't just answer questions, it takes action on our behalf. It runs reports.... | [source](https://www.triumph.tech/resources/ai-agentic-cohort-with-claude) |
| Rock Admin Hero Guide | rock_documentation | Updates for Rock 18.1 Below is a summary of the updates for this version. Automations trigger activities when an event occurs, making some common actions autonomous. You can now Track Entity Interactions by enabling the setting on an Entity Type to link new records to the page interaction that created them, writing a record to the InteractionEntity table for reporting purposes. Track Average Attendance for a campus.... | [source](https://community.rockrms.com/documentation/BookContent/9) |
| AI Agents | rock_developer | Rock has a heavy load, holding all the data that your organization runs on, and we know that you have a heavy load too. Rock has always been about empowering staff and simplifying processes so people can focus on ministry. Agents are the next step. Think of them as digital helpers that free you up for ministry or for that task you've been putting off for months. As a developer building agents and the tools that... | [source](https://community.rockrms.com/developer/ai-agents) |
| Agent Instructions | rock_developer | Overview Each request your agent makes is supported by information provided by the system to help guide and instruct it. This information comes from several sources. Below, we’ll break down these sources and offer guidance to help your agent perform at its best. Note When writing instructions in your prompt, be mindful of the amount of text you add. These instructions are included with every request, so lengthy... | [source](https://community.rockrms.com/developer/ai-agents/agents/agent-instructions) |
| Agents | rock_developer | Overview Agents are the central point of how AI works in Rock. An agent defines the skills and tools that are available for use. It also provides instructions to the language model about how the agent should behave. This means you might have multiple agents configured in Rock. One might be for general staff to use and includes the majority of tools. This would probably be the primary agent used in Rock. When you are... | [source](https://community.rockrms.com/developer/ai-agents/agents) |
| Behaviors | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/controls/behaviors) |
| Borders | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/styling/legacy/borders) |
| CMS | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms) |
| CRM | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm) |
| Check-in | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [AI Agent](../../model-map/models/ai-agent.md) | AI | 19.1.8 | 45 | 16 | 30 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session](../../model-map/models/ai-agent-session.md) | AI | 19.1.8 | 28 | 12 | 19 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session Anchor](../../model-map/models/ai-agent-session-anchor.md) | AI | 19.1.8 | 29 | 15 | 20 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session History](../../model-map/models/ai-agent-session-history.md) | AI | 19.1.8 | 27 | 14 | 19 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Skill](../../model-map/models/ai-agent-skill.md) | AI | 19.1.8 | 22 | 8 | 13 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Automation Event](../../model-map/models/automation-event.md) | Core | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Automation Trigger](../../model-map/models/automation-trigger.md) | Core | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Status Automation](../../model-map/models/connection-status-automation.md) | Engagement | 19.1.8 | 45 | 15 | 30 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Identity Verification](../../model-map/models/identity-verification.md) | CRM | 19.1.8 | 42 | 14 | 26 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Identity Verification Code](../../model-map/models/identity-verification-code.md) | CRM | 19.1.8 | 38 | 11 | 23 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [History Login](../../model-map/models/history-login.md) | Security | 19.1.8 | 52 | 22 | 34 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Provider](../../model-map/models/ai-provider.md) | AI | 19.1.8 | 43 | 15 | 28 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

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
| 18.1 | Communication | Added a new "Chat Message" Automation Trigger that can launch Automation Events when a Chat message is sent. Also added a "Send Fallback Chat Notification" Automation Event that alerts individuals via alternate methods (such as email or SMS) if they don’t have an active personal device or have notifications turned off. | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | API | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to the DataView. Fixes: #6348 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Agent Tools And Lookup Surfaces

Keywords: `custom tool, lookup tool, native tool, available attributes, agent tool`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Lookup Tools | rock_developer | Overview Lookup Tools help Rock AI agents find the exact information they need and return it in a format the agent can use. There are basically three steps to a Lookup . Load data Format data Return data Load Data {% sql return:'results' %} SELECT DISTINCT [Id], [Name] FROM [GroupType] {% endsql %} As you can see, this is quite simple. We just run a simple select statement to retrieve the data we want. In this case,... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools/lookup-tools) |
| Writing Custom Tools | rock_developer | Overview Tools are the actual actions your agents take. Rock comes with many tools out of the box that have been tested and refined, ready to use in Rock, but you're not limited to the skills and tools that come out of the box. You can write your own using native code (C#) or Lava. We provide information on each below. Tool Security Every tool you build inherits Rock's security. A person can only run a tool if they... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools) |
| Native Tools | rock_developer | Lava Tools are great for fast, low-code development inside Rock. Native Tools go further by using compiled C# and the full Rock infrastructure. By creating custom classes that inherit from AgentSkillComponent , you can build more advanced tools for complex logic, external API integrations and heavier database work, while still giving the AI agent clear instructions and strong guardrails. Method Definition... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools) |
| Rock Tool Helper | rock_developer | Overview There is a lot of logic and error checking involved when writing Native Tools , and much of it is repetitive. To reduce that overhead, Rock provides the Rock Tool Helper , a centralized class that standardizes common patterns like validation, error collection, pagination and safe entity access so your tools stay more consistent and the AI agent receives clearer, more actionable feedback. For example,... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper) |
| Gotchas | rock_developer | Overview Things to look out for when writing native tools. Queryable object creation must be identical When using a queryable to get the data directly from the database, as opposed to materializing full entity objects and then pulling out the specific properties you want, you may run into the following error: The type 'Rock.AI.Agent.Classes.Entity.PersonResult' appears in two structurally incompatible... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/gotchas) |
| Lookup Tools | rock_developer | Overview Lookup tools usually take no parameters and are straightforward to implement. There are basically three steps. Load data Format data Return data Typically, steps one and two will be the same since you can often do both in a single query or cache request. For clarity, we will list them separately. Load Data Whenever possible, use cache objects if they are available. Let's take a look at a lookup for... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools) |

### Permissions And Data Boundaries

Keywords: `tool security, least privilege, permission, authorization, data boundary, sensitive data`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Writing Custom Tools | rock_developer | Overview Tools are the actual actions your agents take. Rock comes with many tools out of the box that have been tested and refined, ready to use in Rock, but you're not limited to the skills and tools that come out of the box. You can write your own using native code (C#) or Lava. We provide information on each below. Tool Security Every tool you build inherits Rock's security. A person can only run a tool if they... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools) |
| Lookup Tools | rock_developer | Overview Lookup tools usually take no parameters and are straightforward to implement. There are basically three steps. Load data Format data Return data Typically, steps one and two will be the same since you can often do both in a single query or cache request. For clarity, we will list them separately. Load Data Whenever possible, use cache objects if they are available. Let's take a look at a lookup for... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools) |
| Rock Core Release Notes | rock_core_release_notes | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to the DataView. Fixes: #6348 | [source](https://www.rockrms.com/releasenotes) |
| API Patterns | rock_developer | Starting in Rock v17 a new "v2" API pattern has been introduced. The information on this page only applies to these v2 API endpoints. The new API endpoints are designed to be secure by default. This means that default security is to not allow anyone access to execute the APIs until they have been granted explicit authorization. This means if you add a new endpoint that is [Secured] so that only certain people can... | [source](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns) |
| Security Role Permissions Inspector | rock_recipes | 6 Security Role Permissions Inspector Shared by Jeff Richmond , The Well Community Church 4 years ago 11.0 Security Advanced Description This recipe creates a new page where you can see all of the entity permissions assigned to any given security role. The list of permissions can also be filtered by entity type, name, or status, as well as the permission action and status. NOTE: This is simply a list of the Auth... | [source](https://community.rockrms.com/recipes/243) |
| Securing Access to Your Blocks | rock_developer | A block need not worry about hiding itself if a user shouldn't be allowed to view it. The page framework handles that. However, it does have to check security for other situations. Thankfully securing functionality access within your block is easy to do. To test whether the current user is allowed to perform a certain action, use the IsUserAuthorized (string action) method where action is one of "View", "Edit", or... | [source](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks) |
| Attributes | rock_developer | Attributes are one of the secrets to Rock's amazing capability. Pretty much anything in Rock can have an attribute -- and you can add them at runtime or bake them into your code. Adding Attribute Viewing/Editing Capabilities (the Attribute Value Container) If you have a block that handles a particular entity which may have attributes, you can use the AttributeValuesContainer to quickly add view and edit capability... | [source](https://community.rockrms.com/developer/303---blast-off/attributes) |
| The Rock Rest API | rock_developer | Rock features a REST-based web service that supports integration with third-party websites and applications. The REST API is also utilized by various internal Rock components to retrieve and modify data such as populating item pickers, displaying person badges, and showing charts for metrics. The API is also used for external applications that access Rock data, such as the check-scanner and the financial statement... | [source](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) |
| Using Auth0 | rock_developer | Using Auth0 for your Rock mobile application login. M v5.0 C v15.1 What is Auth0? Auth0 is a cloud-based identity and access management (IAM) platform that provides developers and organizations with secure and easy-to-use solutions for authenticating and authorizing user access to applications. Auth0 offers a range of authentication methods such as username and password, social identity providers, multi-factor... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-auth0) |

### Automation Design And Workflows

Keywords: `automation, automations, workflow automation, scheduled job, trigger, action`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Rock Tool Helper | rock_developer | Overview There is a lot of logic and error checking involved when writing Native Tools , and much of it is repetitive. To reduce that overhead, Rock provides the Rock Tool Helper , a centralized class that standardizes common patterns like validation, error collection, pagination and safe entity access so your tools stay more consistent and the AI agent receives clearer, more actionable feedback. For example,... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/rock-tool-helper) |
| Rock Core Release Notes | rock_core_release_notes | Added a new "Chat Message" Automation Trigger that can launch Automation Events when a Chat message is sent. Also added a "Send Fallback Chat Notification" Automation Event that alerts individuals via alternate methods (such as email or SMS) if they don’t have an active personal device or have notifications turned off. | [source](https://www.rockrms.com/releasenotes) |
| Skip the Trial and Error: Borrow Our AI Playbook | triumph_resources | The world is moving fast. Agentic AI is changing everything. And most church staff are still using AI the way they used it a year ago, if they're using it at all. At Triumph Tech, we couldn't keep working that way. So we didn't. This year, we rebuilt how our team uses AI. We moved past basic chat tools and into agentic AI, where Claude doesn't just answer questions, it takes action on our behalf. It runs reports.... | [source](https://www.triumph.tech/resources/ai-agentic-cohort-with-claude) |
| Automation Event | rock_model_map | Automation Event is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |
| Automation Trigger | rock_model_map | Automation Trigger is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |
| Connection Status Automation | rock_model_map | Connection Status Automation is a Rock model in the Engagement category. | [source](https://community.rockrms.com/ModelMap) |
| Automations | rock_rocku | Automations Presenter: Blake Byers Length: 4:58 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/automations) |
| Connection Request Status Automation | rock_rocku | Connection Request Status Automation Presenter: Cullen McCoy Length: 5:23 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-request-status-automation) |
| Data Automation | rock_rocku | Data Automation Presenter: Cullen McCoy Length: 4:48 " Searching for a Person 3m 19s Person Profile 14m 31s Adding and Editing Individuals and Families 7m 16s Following 6m 14s Tags 3m 30s Person Note 5m 01s Person Attributes 8m 16s Bookmarked Attributes 2m 27s Blended Families 1m 52s Family Attributes 2m 34s Known Relationships 5m 30s Merging Duplicate Records 3m 48s How to Delete a Person 1m 59s Impersonation 3m... | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-automation) |

### Verification And Review Gates

Keywords: `verification, review gate, approval, evidence, hallucination, live verification`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | rock_podcast_rss | Episode 202 adds public-safe operational context for Rock release awareness, community-shaped priorities, AI-assisted group matching, and documentation currency; concrete implementation guidance remains tied to official docs, release notes, source code, or live-instance verification. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Native Tools | rock_developer | Lava Tools are great for fast, low-code development inside Rock. Native Tools go further by using compiled C# and the full Rock infrastructure. By creating custom classes that inherit from AgentSkillComponent , you can build more advanced tools for complex logic, external API integrations and heavier database work, while still giving the AI agent clear instructions and strong guardrails. Method Definition... | [source](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools) |
| Identity Verification | rock_model_map | Identity Verification is a Rock model in the CRM category. | [source](https://community.rockrms.com/ModelMap) |
| Identity Verification Code | rock_model_map | Identity Verification Code is a Rock model in the CRM category. | [source](https://community.rockrms.com/ModelMap) |
| Testing | rock_developer | As a team, we have agreed to the principles and processes below when it comes to testing: The developer is always the primary owner of the quality of their code. Testing should be done as a stand-alone task after the development is complete. Work done during the development stage is ‘verification’ not ‘testing’. Time will be budgeted for the testing phase. Depending on the size and complexity of the task a Peer... | [source](https://community.rockrms.com/developer/developer-codex/coding-standards/testing) |
| Onboard Person | rock_developer | M v2.0 Integrated Scroll This is a powerful block (commonly referred to as "account onboarding") with many configuration options, so we'll explain all of the screens below and the settings available for each. The purpose of this block is to walk users through a step-by-step process of creating an account (or signing in) and confirming demographic information, campus, and notification preferences. Hello Screen This... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security/onboard-person) |
| Rock Core Release Notes | rock_core_release_notes | Added CAPTCHA support to the Group Registration, Prayer Request Entry, Group Simple Register, Email Form, and Sign-Up Register blocks. This setting helps prevent automated bots by requiring individuals to complete a verification step before submitting these forms. Administrators can enable or disable CAPTCHA within each block’s settings. | [source](https://www.rockrms.com/releasenotes) |


## Rebuild Dependencies

- Source records: `82`
- Approved claims: `37`
- Community-reviewed contributions: `0`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
