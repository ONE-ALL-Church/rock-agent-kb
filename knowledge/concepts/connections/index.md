---
id: concept-connections
title: Connections
generated: true
last_built: 2026-06-12T09:20:13+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - people
  - workflows
  - groups
  - communications
  - security
  - reporting
---

# Connections

Connection types, opportunities, requests, statuses, boards, lists, assignments, follow-up, and pipeline reporting.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Connections` spans people, workflows, groups, communications, security, reporting. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_community_hubs, rock_podcast_rss, rock_developer, rock_community_site, rock_rocku, rock_qa.
- Related tags found in source records: workflow, development, lava, mobile, usage, security, check-in, finance.
- Source detail types include: developer_doc, documentation_bookcontent, question, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | community analytics | 00:30 | Data analytics meetups can help churches compare dashboards, process designs, and BI-tool choices against real ministry use cases instead of treating reporting as an isolated technical task. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | attendance flow | 36:49 | Attendance-flow analysis can move beyond aggregate weekend counts by classifying engagement patterns, prioritizing follow-up lists, and creating Rock connection requests for campus teams. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | AI governance | 52:13 | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | reporting suite design | 06:04 | A mature reporting suite can separate executive dashboards, campus or ministry dashboards, and functional operational dashboards so each audience sees the level of detail needed for its decisions. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | executive dashboards | 12:09 | Executive dashboards work better when they expose a small set of organization-wide goals with clear current values, goal values, and status indicators instead of hiding many rolled-up metrics behind ambiguous scores. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | campus dashboards | 14:24 | Campus dashboards should help leaders compare current year-to-date values against both goals and prior-year context, while leaving deeper campus-specific measures available without crowding the organization-wide dashboard. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | ministry dashboards | 21:16 | Ministry and program dashboards should avoid standalone numbers when possible; compare measures to goals, historical baselines, or funnels so teams can interpret whether a result needs action. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | connection requests | 39:51 | Functional dashboards such as connection-request views may justify live database connections when leaders need up-to-date queues, while slower-changing attendance or giving dashboards can usually use scheduled refreshes. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | report access | 49:32 | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | digital connection goal | 03:24 | Digital strategy should be evaluated by whether it helps people take a real next step, not only whether the church published more content. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/OLmW03olAp) |
| Media Watch Transcript Insight | content role | 04:33 | Content still matters, but Rock-backed web and mobile experiences should connect content to identity, forms, groups, communication, and follow-up when possible. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/OLmW03olAp) |
| Media Watch Transcript Insight | strategy ownership | 02:04 | Digital ministry should be integrated into ministry culture and team workflows instead of living as a separate channel owned only by a few specialists. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/OLmW03olAp) |
| Media Watch Transcript Insight | Rock data | 01:56 | Digital group strategy is stronger when it remains tied to Rock data instead of creating disconnected community records outside the ministry system. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| Media Watch Transcript Insight | online groups | 03:24 | Online groups should be treated as real group ministry with ownership, communication expectations, and connection follow-up, not only as a digital convenience. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| Media Watch Transcript Insight | communication | 02:00 | Communication planning should be part of the digital-group design from the start so members know what action to take next and leaders can follow engagement. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| Media Watch Transcript Insight | guest retention | 02:33 | First-time guest retention is a useful ministry health signal when it is measured consistently and connected to the church's actual follow-up process. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | benchmarking | 02:49 | Retention benchmarks can help leadership interpret results, but local context and data definitions should be documented before comparing one church's numbers to another's. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | connection workflow | 03:00 | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | release governance | 00:48 | Use the episode as release-awareness context: podcast release discussion can flag security updates, alpha/beta status, and future model-changing work, but upgrade guidance must still be verified against official release notes and the local Rock version. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | community-prioritized roadmap | 01:54 | Community feedback channels such as Rocket Chat, calls, church visits, and conferences can explain why areas like Connections rise in priority, but agents should treat that as roadmap context rather than proof that a feature is present in a given instance. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | AI group matching | 13:31 | For AI-assisted group finding, implementation work needs church-specific matching rules: which group types are findable, which attributes describe affinity, and what boundaries keep the assistant away from inappropriate targets such as security roles. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Rock's Future Anchored in Vision \| Ep 202 Transcript Insight | documentation currency | 15:00 | Documentation changes should be planned as part of UI and release work; major UI changes can create downstream screenshot and article-refresh work that must be tracked before public guidance is treated as current. | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| Media Watch Transcript Insight | preregistration use case | 01:16 | Family preregistration is useful when it reduces first-visit friction and improves the quality of people, family, and child data before check-in. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | implementation path | 02:10 | Before launching preregistration broadly, teams should test the full path from public form through family record creation, check-in eligibility, and staff follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | public page design | 03:50 | A public preregistration page should explain the value to families and avoid creating duplicate or partial records that staff later need to clean manually. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | workflow follow-up | 00:37 | New-family preregistration should be connected to a clear follow-up workflow or connection process so the data captured before arrival leads to ministry action. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | communication alignment | 02:24 | Communication teams often feel siloed, so content and campaign strategy should be tied to ministry ownership, shared goals, and a visible next-step path in Rock. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |
| Media Watch Transcript Insight | SEO and content | 00:51 | SEO and content planning can support outreach when they are connected to the church's actual ministry offers and not treated as a separate marketing exercise. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |
| Media Watch Transcript Insight | measurement | 01:01 | Long-form training or strategy material should be broken into actionable sections with a way to measure whether leaders and teams are adopting the recommendations. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | implementation_pattern | Before launching preregistration broadly, teams should test the full path from public form through family record creation, check-in eligibility, and staff follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | implementation_pattern | New-family preregistration should be connected to a clear follow-up workflow or connection process so the data captured before arrival leads to ministry action. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | operational_guidance | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Family preregistration is useful when it reduces first-visit friction and improves the quality of people, family, and child data before check-in. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | operational_guidance | A public preregistration page should explain the value to families and avoid creating duplicate or partial records that staff later need to clean manually. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| community-reviewed | implementation_pattern | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| community-reviewed | operational_guidance | Long-form training or strategy material should be broken into actionable sections with a way to measure whether leaders and teams are adopting the recommendations. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |
| community-reviewed | operational_guidance | Campus dashboards should help leaders compare current year-to-date values against both goals and prior-year context, while leaving deeper campus-specific measures available without crowding the organization-wide dashboard. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Communication teams often feel siloed, so content and campaign strategy should be tied to ministry ownership, shared goals, and a visible next-step path in Rock. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/x9l4WxRmaE) |
| community-reviewed | operational_guidance | A mature reporting suite can separate executive dashboards, campus or ministry dashboards, and functional operational dashboards so each audience sees the level of detail needed for its decisions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Functional dashboards such as connection-request views may justify live database connections when leaders need up-to-date queues, while slower-changing attendance or giving dashboards can usually use scheduled refreshes. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| community-reviewed | operational_guidance | Online groups should be treated as real group ministry with ownership, communication expectations, and connection follow-up, not only as a digital convenience. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| community-reviewed | operational_guidance | Digital group strategy is stronger when it remains tied to Rock data instead of creating disconnected community records outside the ministry system. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| community-reviewed | operational_guidance | Data analytics meetups can help churches compare dashboards, process designs, and BI-tool choices against real ministry use cases instead of treating reporting as an isolated technical task. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| community-reviewed | operational_guidance | For AI-assisted group finding, implementation work needs church-specific matching rules: which group types are findable, which attributes describe affinity, and what boundaries keep the assistant away from inappropriate targets such as security roles. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-202-rocks-future-anchored-in-vision) |
| community-reviewed | operational_guidance | Executive dashboards work better when they expose a small set of organization-wide goals with clear current values, goal values, and status indicators instead of hiding many rolled-up metrics behind ambiguous scores. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Communication planning should be part of the digital-group design from the start so members know what action to take next and leaders can follow engagement. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| More |  | 19 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_community_hubs`: 7
- `rock_community_site`: 23
- `rock_core_release_notes`: 2
- `rock_developer`: 22
- `rock_documentation`: 1
- `rock_model_map`: 12
- `rock_podcast_rss`: 1
- `rock_qa`: 1
- `rock_recipes`: 3
- `rock_rocku`: 17
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| GitHub Spotlight: 4/2/2025 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release v18.0.3, released on 4/1/2025. 17.0 Highlights v17.0 was released in Alpha on March 4, 2025. See the Release Notes for complete details. 17.1 Highlights Added a new feature to the Registration List, Registrant List, Registration Detail, and Group Placement blocks that disables editing of person, registration, and group member attributes based on the... | [source](https://www.triumph.tech/resources/github-spotlight-422025) |
| Engagement | rock_documentation | Updates for Rock 18.1 Below is a summary of the updates for this version. Step Analytics updates introduce powerful charts to track KPIs, Trends, Campuses, Totals and Flow. Core Steps bring a new eRA step type and an easy way to move Step Types between programs. Completion Flow for Steps helps you define the flow of a Step Program. Steps now offer Milestones, Rhythms and Impact Weight as configurable settings, and... | [source](https://community.rockrms.com/documentation/bookcontent/39) |
| Adding Steps | rock_rocku | Adding Steps Presenter: Cullen McCoy Length: 7:56 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/adding-steps) |
| Connection Opportunities | rock_rocku | Connection Opportunities Presenter: Jon Edmiston Length: 8:27 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-opportunities) |
| Connection Request Status Automation | rock_rocku | Connection Request Status Automation Presenter: Cullen McCoy Length: 5:23 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-request-status-automation) |
| Connection Types | rock_rocku | Connection Types Presenter: Jon Edmiston Length: 9:04 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-types) |
| Connections Board | rock_rocku | Coming Soon: Connections Board Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| Connections List | rock_rocku | Coming Soon: Connections List Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-list-1) |
| Connections Opportunities | rock_rocku | Coming Soon: Connections Opportunities Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-opportunities) |
| Connections Overview | rock_rocku | Coming Soon: Connections Overview Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-overview) |
| Connections Overview | rock_rocku | Connections Overview Presenter: Cullen McCoy Length: 13:59 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/overview) |
| Connections Types | rock_rocku | Coming Soon: Connections Types Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-types) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Connection Opportunity](../../model-map/models/connection-opportunity.md) | Engagement | 18.2.4 | 58 | 22 | 38 | 16 | 3 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Opportunity Campus](../../model-map/models/connection-opportunity-campus.md) | Engagement | 18.2.4 | 42 | 12 | 27 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Opportunity Connector Group](../../model-map/models/connection-opportunity-connector-group.md) | Engagement | 18.2.4 | 42 | 12 | 27 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Opportunity Group](../../model-map/models/connection-opportunity-group.md) | Engagement | 18.2.4 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Opportunity Group Config](../../model-map/models/connection-opportunity-group-config.md) | Engagement | 18.2.4 | 44 | 14 | 29 | 15 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Request](../../model-map/models/connection-request.md) | Engagement | 18.2.4 | 60 | 24 | 44 | 20 | 12 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Request Activity](../../model-map/models/connection-request-activity.md) | Engagement | 18.2.4 | 45 | 14 | 30 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| Connection Request Status History | Engagement |  |  |  |  |  | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Request Workflow](../../model-map/models/connection-request-workflow.md) | Engagement | 18.2.4 | 44 | 14 | 29 | 15 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Status](../../model-map/models/connection-status.md) | Engagement | 18.2.4 | 47 | 18 | 32 | 14 | 4 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Status Automation](../../model-map/models/connection-status-automation.md) | Engagement | 18.2.4 | 45 | 15 | 30 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Connection Type](../../model-map/models/connection-type.md) | Engagement | 18.2.4 | 59 | 25 | 43 | 19 | 10 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable scraped Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Connection Opportunity.AttributeValues` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.Attributes` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.ConnectionOpportunityCampuses` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.ConnectionType` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.CreatedByPersonId` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.CreatedByPersonName` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.EntityStringValue` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Connection Opportunity.IdKey` is Lava-marked but not database-marked in the scraped Model Map (Rock 18.2.4; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 18.1 | Connection | Improved the Connection Request Board with updates to campus filtering, connector preferences, and workflow configuration. Added new block settings to define default Connection State and Status filters. Workflows on the Connection Opportunity block can now be reordered using drag-and-drop functionality. Additionally, workflows on this block can be... | [source](https://www.rockrms.com/releasenotes) |
| 17.2 | Connection | Fixed an issue where the Connection Opportunity Signup block only displayed request attributes defined on the opportunity itself, now correctly including attributes inherited from the Connection Type. Fixes: #6356 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Opportunities

Keywords: `connection opportunity, opportunity, opportunities`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Connection Opportunity List | rock_developer | Displays the list of connection opportunities for a single connection type. M v3.0 C v13.3 This block is used to display a list of connection opportunities for a single connection type. If you are unfamiliar with Connections in Rock, please refer to the connections manual . Getting Content Getting the connection types In order for the block to know which 'Connection Type' to display opportunities for, you need to... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list) |
| Add Connection Request | rock_developer | Allows a Person to create a new Connection. M v5.0 C v16.1 Block Configuration If you are unfamiliar with Connections in Rock, please first refer to the connections manual . Connection Types The connection types that will be made available to this block. If none are selected, all available connection types will be shown. Post Save Action The navigation command to execute after a save successfully occurs. Post Cancel... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request) |
| Connections Board | rock_rocku | Coming Soon: Connections Board Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| Connections List | rock_rocku | Coming Soon: Connections List Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-list-1) |
| Connection Type | rock_qa | 0 Connection Type 1 Blake Anglin posted 3 Years Ago If I wanted to create a block on our website that uses lava to pull the connections opportunities from a connection type how would the lava code look. For each opportunity i want it to create a card the displays the title, Details and image that you can add in the connection Opportunity Detail and when you click on it it sends you to the connection form affiliated... | [source](https://community.rockrms.com/ask/developing/2645) |
| Connection Request List | rock_developer | M v3.0 C v13.3 This block is used to display a list of Connection Requests for a single connection opportunity. If you are unfamiliar with Connections in Rock, please refer to the connections manual . Note Requests that are in a "Connected" state are not pulled down by this block. The purpose is to manage requests that have not been completed yet. To summarize, this block looks for the connectionOpportunityGuid as a... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list) |
| Connection Opportunities | rock_rocku | Connection Opportunities Presenter: Jon Edmiston Length: 8:27 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-opportunities) |

### Requests And Statuses

Keywords: `connection request, request, status, state, placement`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | community analytics | 00:30 | Data analytics meetups can help churches compare dashboards, process designs, and BI-tool choices against real ministry use cases instead of treating reporting as an isolated technical task. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | attendance flow | 36:49 | Attendance-flow analysis can move beyond aggregate weekend counts by classifying engagement patterns, prioritizing follow-up lists, and creating Rock connection requests for campus teams. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | AI governance | 52:13 | When AI summaries are generated from person-profile data, the review should include data minimization, avoidance of direct identifiers, privacy-policy alignment, and vendor assurances about model training. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | reporting suite design | 06:04 | A mature reporting suite can separate executive dashboards, campus or ministry dashboards, and functional operational dashboards so each audience sees the level of detail needed for its decisions. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | executive dashboards | 12:09 | Executive dashboards work better when they expose a small set of organization-wide goals with clear current values, goal values, and status indicators instead of hiding many rolled-up metrics behind ambiguous scores. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | campus dashboards | 14:24 | Campus dashboards should help leaders compare current year-to-date values against both goals and prior-year context, while leaving deeper campus-specific measures available without crowding the organization-wide dashboard. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | ministry dashboards | 21:16 | Ministry and program dashboards should avoid standalone numbers when possible; compare measures to goals, historical baselines, or funnels so teams can interpret whether a result needs action. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | connection requests | 39:51 | Functional dashboards such as connection-request views may justify live database connections when leaders need up-to-date queues, while slower-changing attendance or giving dashboards can usually use scheduled refreshes. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | report access | 49:32 | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Media Watch Transcript Insight | rock_community_hubs | The Data Analytics Hub launch frames community analytics as a shared practice space where churches compare dashboards, ministry processes, BI tooling, and Rock-based reporting patterns. The session also includes a Life.Church attendance-flow case study that uses Rock attendance and connection data to prioritize pastoral follow-up while treating AI profile summaries and privacy controls as governance concerns. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | rock_community_hubs | This Data Analytics Hub walkthrough gives public-safe guidance for building a layered Rock reporting suite with Power BI or similar tools. It distinguishes executive, campus/ministry, and functional reporting, emphasizes comparison against goals or history, and shows when scheduled refreshes, live queries, Rock security roles, and embedded report pages each fit. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Add Connection Request | rock_developer | Allows a Person to create a new Connection. M v5.0 C v16.1 Block Configuration If you are unfamiliar with Connections in Rock, please first refer to the connections manual . Connection Types The connection types that will be made available to this block. If none are selected, all available connection types will be shown. Post Save Action The navigation command to execute after a save successfully occurs. Post Cancel... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request) |
| Connections Board | rock_rocku | Coming Soon: Connections Board Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| Connections List | rock_rocku | Coming Soon: Connections List Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-list-1) |
| Connection Request List | rock_developer | M v3.0 C v13.3 This block is used to display a list of Connection Requests for a single connection opportunity. If you are unfamiliar with Connections in Rock, please refer to the connections manual . Note Requests that are in a "Connected" state are not pulled down by this block. The purpose is to manage requests that have not been completed yet. To summarize, this block looks for the connectionOpportunityGuid as a... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list) |
| Connection Opportunities | rock_rocku | Connection Opportunities Presenter: Jon Edmiston Length: 8:27 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-opportunities) |
| Connection Request Status Automation | rock_rocku | Connection Request Status Automation Presenter: Cullen McCoy Length: 5:23 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-request-status-automation) |
| Connection Types | rock_rocku | Connection Types Presenter: Jon Edmiston Length: 9:04 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connection-types) |

### Boards And Lists

Keywords: `connections board, connections list, board, list`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Connection Opportunity List | rock_developer | Displays the list of connection opportunities for a single connection type. M v3.0 C v13.3 This block is used to display a list of connection opportunities for a single connection type. If you are unfamiliar with Connections in Rock, please refer to the connections manual . Getting Content Getting the connection types In order for the block to know which 'Connection Type' to display opportunities for, you need to... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list) |
| Connections Board | rock_rocku | Coming Soon: Connections Board Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| Connections List | rock_rocku | Coming Soon: Connections List Release Date: Monday, June 1, 2026 " Connections Overview 13m 59s Connection Types 9m 04s Connection Opportunities 8m 27s Step Programs [Legacy] 6m 29s Adding Steps 7m 56s Steps Badges 4m 33s Connection Request Status Automation 5m 23s Step Flow [Legacy] 4m 19s Sign-Ups 8m 29s Reminders 5m 29s Step Programs 5m 26s Step Charts 7m 55s Step Types 6m 25s Steps Overview 4m 13s | [source](https://community.rockrms.com/rocku/engagement/connections-list-1) |
| Connection Request List | rock_developer | M v3.0 C v13.3 This block is used to display a list of Connection Requests for a single connection opportunity. If you are unfamiliar with Connections in Rock, please refer to the connections manual . Note Requests that are in a "Connected" state are not pulled down by this block. The purpose is to manage requests that have not been completed yet. To summarize, this block looks for the connectionOpportunityGuid as a... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list) |
| Connection | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection) |
| 👨‍💻 Developers | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/developers) |
| CMS | rock_developer | Mobile Docs 📱 Building Your First App 📱 Building Your First App Creating An App App Configuration Adding Content Deploying Your App 📖 Lexicon 🧱 Essentials 🧱 Essentials Animations Blocks Blocks CMS CMS Content Content Channel Item View Content Collection View Daily Challenge Entry Hero Lava Item List Login Login Using Auth0 Using Entra Profile Details Register Structured Content View Workflow Entry Voice Agent... | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms) |

### Assignment And Follow-Up

Keywords: `assignment, assigned, follow-up, follow up, connector`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | guest retention | 02:33 | First-time guest retention is a useful ministry health signal when it is measured consistently and connected to the church's actual follow-up process. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | benchmarking | 02:49 | Retention benchmarks can help leadership interpret results, but local context and data definitions should be documented before comparing one church's numbers to another's. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | connection workflow | 03:00 | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | preregistration use case | 01:16 | Family preregistration is useful when it reduces first-visit friction and improves the quality of people, family, and child data before check-in. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | implementation path | 02:10 | Before launching preregistration broadly, teams should test the full path from public form through family record creation, check-in eligibility, and staff follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | public page design | 03:50 | A public preregistration page should explain the value to families and avoid creating duplicate or partial records that staff later need to clean manually. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Media Watch Transcript Insight | workflow follow-up | 00:37 | New-family preregistration should be connected to a clear follow-up workflow or connection process so the data captured before arrival leads to ministry action. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Media Watch Transcript Insight | rock_community_hubs | The Data Analytics Hub launch frames community analytics as a shared practice space where churches compare dashboards, ministry processes, BI tooling, and Rock-based reporting patterns. The session also includes a Life.Church attendance-flow case study that uses Rock attendance and connection data to prioritize pastoral follow-up while treating AI profile summaries and privacy controls as governance concerns. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session gives public-safe guidance for online groups and digital community workflows. It emphasizes that Rock-backed digital ministry can connect group participation, communication, data, and follow-up when teams intentionally design the path from online engagement to pastoral care or in-person connection. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/GKBqYVpBW8) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session gives public-safe guidance for using first-time guest and retention measures as a connection strategy input. It emphasizes defining the few metrics that matter, comparing retention patterns over time, and using data to improve follow-up without replacing the relational work of connecting new people to ministry. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session is a strong public-safe source for family preregistration and check-in readiness. It describes using Rock preregistration to capture family information before arrival, prepare for check-in, and design follow-up around new families, while making clear that preregistration should be tested as part of the real family and check-in data flow. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Connection Request Connector Report with Unavailability Workflow | rock_recipes | 0 Connection Request Connector Report with Unavailability Workflow Shared by Christine Ronk , Trinity Fellowship Church one year ago 15.0 Connection, Operations, Reporting Intermediate Description : This short workflow and report help us to better manage assigning Connectors to Connection Requests. For the following process, our primary focus is on our “New Connections” connection type which we catch brand new... | [source](https://community.rockrms.com/recipes/446) |
| Rock Core Release Notes | rock_core_release_notes | Improved the Connection Request Board with updates to campus filtering, connector preferences, and workflow configuration. Added new block settings to define default Connection State and Status filters. Workflows on the Connection Opportunity block can now be reordered using drag-and-drop functionality. Additionally, workflows on this block can be... | [source](https://www.rockrms.com/releasenotes) |
| Change Connector for Multiple Connection Requests | rock_recipes | 1 Change Connector for Multiple Connection Requests Shared by Carrie White , Cornerstone Christian Fellowship 4 years ago 12.0 General Beginner I found myself having to spend too much time changing the connector for active connection requests when a staff member left so I created a simple workflow to do the work for me. Import the workflow, edit it to specify who the new connector is, select the connection requests... | [source](https://community.rockrms.com/recipes/276) |
| Connection Request Workload | rock_recipes | 7 Connection Request Workload Shared by Jeff Richmond , The Well Community Church 2 years ago 15.0 Connection, Operations Beginner Description This recipe provides a way to see your staff's current connection request workload at a glance. All staff members are displayed with counts for each of the various connection request states and statuses. Some adjustment may be needed for how your organization uses connection... | [source](https://community.rockrms.com/recipes/442) |
| Connections Board Transcript Insight | rock_rocku | Connections Board adds workflow guidance for connection-request queues: troubleshoot visible cards through opportunity, status, assignment, filters, and security. | [source](https://community.rockrms.com/rocku/engagement/connections-board) |
| Connections List Transcript Insight | rock_rocku | Connections List adds workflow guidance for filtered connection-request review: compare filters, opportunity, status, assignment, and user security when results differ. | [source](https://community.rockrms.com/rocku/engagement/connections-list-1) |


## Rebuild Dependencies

- Source records: `91`
- Approved claims: `37`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
