---
id: concept-system-admin-ops
title: System Administration And Operations
generated: true
last_built: 2026-06-18T21:40:09+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - security
  - workflows
  - data-views
  - reports
  - cache
  - jobs
  - release-notes
---

# System Administration And Operations

Service jobs, exception logs, cache, cleanup, indexing, data integrity, settings, diagnostics, and operational health.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `System Administration And Operations` spans security, workflows, data-views, reports, cache, jobs. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_community_hubs, rock_documentation, rock_community_site, rock_core_release_notes, triumph_resources, rock_developer.
- Related tags found in source records: operations, usage, releases, development, admin, workflow, training, security.
- Source detail types include: developer_doc, documentation_article, question, recipe, rock_community_site, rock_lava_docs, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | data quality scope | 11:37 | Rock data quality work should be prioritized because dirty people, family, address, and duplicate data affects check-in, communication, reporting credibility, and leadership decisions. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | cleanup prioritization | 20:00 | A practical cleanup program should separate low-effort automations from medium-effort reports and high-effort duplicate decisions, so staff and volunteers spend human review time on records that require judgment. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | built-in automation | 25:51 | Before building custom cleanup processes, review Rock's built-in data automation options such as profile activation/inactivation rules, adult-child family movement, and gender classification thresholds. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | volunteer governance | 28:48 | Data volunteers can help with duplicate and cleanup queues, but they need training, review time, and bounded scope; adding more volunteers does not scale if every merge decision still requires staff judgment. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | continuous improvement | 30:53 | Track recurring data defects in a shared backlog, choose a small set of fields or defect types to address first, set measurable cleanup goals, and share wins so ministry teams understand the operational value of clean Rock data. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | sender trust | 01:04 | Email logo branding should be treated as sender-trust work that makes messages easier to recognize, not as a guaranteed fix for spam-folder placement. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| Media Watch Transcript Insight | BIMI prerequisites | 13:18 | Before pursuing BIMI or logo display, teams should verify SPF, DKIM, DMARC, domain alignment, and the logo-hosting requirements for the target mail clients. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| Media Watch Transcript Insight | verification options | 12:07 | Self-asserted, CMC, and VMC-style verification paths differ in cost, trademark requirements, and inbox support, so churches should pick the level that matches their domain risk and communication volume. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| Media Watch Transcript Insight | deliverability boundary | 30:53 | Logo display and domain authentication should be documented separately from Mailgun, IP reputation, list quality, and message-content factors that influence deliverability. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| Data Integrity Transcript Insight | data integrity | 00:00 | Data integrity work should start from the exact entity and field being corrected, then identify the owner, source of truth, duplicate risk, and reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| Data Integrity Transcript Insight | people records | 00:00 | People and reporting guides should distinguish cleanup, merge, verification, and governance tasks because each has different audit and permission requirements. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| Data Integrity Transcript Insight | data integrity | 00:00 | Data Integrity work should be repeatable: identify the record population, define the correction rule, test with known examples, and document the owner before making bulk changes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| Data Integrity Transcript Insight | reporting quality | 00:00 | For reporting agents, data integrity issues should be surfaced as source-data problems, not hidden by report logic that masks duplicates, missing values, or stale attributes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | operational_guidance | Before building custom cleanup processes, review Rock's built-in data automation options such as profile activation/inactivation rules, adult-child family movement, and gender classification thresholds. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| community-reviewed | operational_guidance | Data volunteers can help with duplicate and cleanup queues, but they need training, review time, and bounded scope; adding more volunteers does not scale if every merge decision still requires staff judgment. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| community-reviewed | operational_guidance | Email logo branding should be treated as sender-trust work that makes messages easier to recognize, not as a guaranteed fix for spam-folder placement. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| community-reviewed | operational_guidance | A practical cleanup program should separate low-effort automations from medium-effort reports and high-effort duplicate decisions, so staff and volunteers spend human review time on records that require judgment. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| community-reviewed | operational_guidance | Before pursuing BIMI or logo display, teams should verify SPF, DKIM, DMARC, domain alignment, and the logo-hosting requirements for the target mail clients. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| community-reviewed | operational_guidance | Self-asserted, CMC, and VMC-style verification paths differ in cost, trademark requirements, and inbox support, so churches should pick the level that matches their domain risk and communication volume. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| community-reviewed | operational_guidance | Logo display and domain authentication should be documented separately from Mailgun, IP reputation, list quality, and message-content factors that influence deliverability. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| community-reviewed | operational_guidance | Rock data quality work should be prioritized because dirty people, family, address, and duplicate data affects check-in, communication, reporting credibility, and leadership decisions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| community-reviewed | operational_guidance | Track recurring data defects in a shared backlog, choose a small set of fields or defect types to address first, set measurable cleanup goals, and share wins so ministry teams understand the operational value of clean Rock data. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| community-reviewed | source_summary | This Digital Strategy Hub session gives a practical overview of email logo branding for churches, including BIMI-style logo display, DMARC/SPF/DKIM prerequisites, certificate options, Apple and Gmail behavior, and the distinction between sender trust and actual deliverability. It is useful public guidance for Rock communication administrators evaluating domain authentication and brand-trust work around email sent from Rock or related tools. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X6mkVJ2BJW) |
| community-reviewed | source_summary | This Data Analytics Hub presentation gives public-safe operational guidance for Rock data quality programs: use built-in automation where possible, prioritize a small number of high-value data defects, move actionable cleanup reports into Rock, train a bounded volunteer team, and connect data quality work to ministry outcomes such as check-in, communication, and leadership reporting. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |

## Source Coverage

- `rock_community_hubs`: 2
- `rock_community_site`: 1
- `rock_core_release_notes`: 27
- `rock_developer`: 1
- `rock_documentation`: 22
- `rock_lava_docs`: 1
- `rock_model_map`: 12
- `rock_qa`: 1
- `rock_recipes`: 3
- `rock_rocku`: 14
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 6

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Azure Mobile App | triumph_resources | If you use Azure to host your Rock instance, the Azure Mobile App is a must have companion. The app allows you to quickly view your hosting resources and provides a view of resource graphs. The app also serves as a conduit for receiving alerts about service health. While the app isn’t meant for daily administrative tasks, like adding new services, it is an indispensable tool for keeping tabs on the health of your... | [source](https://www.triumph.tech/resources/azure-mobile-app) |
| GitHub Spotlight: 12/20/2024 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release v17.0.34 released on 12/19/2024. v16.10 Highlights Added a new setting named ‘AutoFocus’ to the Obsidian Content Collection View block which automatically selects the search bar, so individuals can start typing in the search bar immediately after the page loads without needing to select the search bar first. Added a new setting called 'Enable Default Address... | [source](https://www.triumph.tech/resources/github-spotlight-12202024) |
| GitHub Spotlight: 2/6/2025 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release v17.0.37, released on 2/6/2025. v16.9 Highlights v16.9 was released in Alpha on February 5, 2025. See the Release Notes for complete details. Issue 6165 Fixed an issue in v16.7 where the Auto Schedule did not honor the group members’ “Every Other Week” schedule preference and instead selected them every week whenever an available slot was present. 16.10... | [source](https://www.triumph.tech/resources/github-spotlight-262025) |
| GitHub Spotlight: 4/30/2025 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release 18.0.5, released on 4/29/2025. 17.0 Highlights v17.0 was released as the latest secured version for early access on April 21, 2025. See the Release Notes for complete details. 17.1 Highlights Added a new feature to IP Geolocation to allow site visitors from selected countries to be blocked, in order to reduce unwanted traffic from high-risk regions. Added a... | [source](https://www.triumph.tech/resources/github-spotlight-4302025) |
| GitHub Spotlight: 6/25/2025 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release 18.0.8, released on 6/24/2025. 17.1 Highlights v17.1 was released as the latest secured version for Early Access on June 23, 2025. See the Release Notes for complete details. 17.2 Highlights Added the Icon Picker control, allowing individuals to select an icon from the gallery Added a new feature to pin or categorize Short Links. Added a new feature to upload... | [source](https://www.triumph.tech/resources/github-spotlight-6252025) |
| GitHub Spotlight: 9/20/2024 | triumph_resources | Below is what's new in Rock's Github for pre-alpha release v17.0.28 that was released on 9/19/2024. v16.7 New setting in the Family Pre-Registration to move Child Information panel above the Adult panel. The team added buttons to hide the 'Clone Schedules' and 'Auto Schedule' in the Obsidian Group Scheduler block settings. Improved the logic that allows interactive experiences to work with a blank Enable Minutes... | [source](https://www.triumph.tech/resources/github-spotlight-9202024-2) |
| Add Cache Tags | rock_documentation | When updating content, you’ll sometimes want your Rock site to instantly reflect the changes you’ve made. To meet this need, Rock provides multiple ways to clear a cache. You can clear the cache of all objects using the global “Clear Cache” button, or you can clear a group of cached objects using cache tags. By using cache tags, you can precisely control what objects are removed from cache; without the performance... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) |
| Advanced Finance | rock_documentation | [Finance Common Defined Types](/documentation/church-management/finance/advanced-finance/finance-common-defined-types?Version=v19.0) [Security for Finance](/documentation/church-management/finance/advanced-finance/security-for-finance?Version=v19.0) [Advanced Utility Payment Entry Block Settings](/documentation/church-management/finance/advanced-finance/advanced-utility-payment-entry-block-settings?Version=v19.0) | [source](https://community.rockrms.com/documentation/church-management/finance/advanced-finance) |
| Cache | rock_lava_docs | Cache Command Basics Want your Lava to run like lightning? Enable caching! Wrapping your Lava in a cache command will take the results and store it in Rock's memory cache. Subsequent runs will load faster than a New York minute. Let's take a look at a simple example: {% cache key:'decker-page-list' duration:'3600' %} {% person where:'LastName == "Decker"' %} {% for person in personItems %} {{ person.FullName }} <br... | [source](https://community.rockrms.com/lava/commands/cache-commands) |
| Cache Manager | rock_documentation | The Cache Manager lets you manage the information cached on your Rock server(s) through the use of cache tags. Cache tags work a bit like personal and organizational tags, except in this case you're tagging types of information. Using the Cache Manager, you can tell Rock to clear the cache of information based on those tags. There are two sides when it comes to configuring and using the Cache Manager: the more... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Cache Persisted Datasets | rock_documentation | Traditional caching in Rock is limited to specific blocks, or to a particular format when using the Lava cache tag. Persisted Datasets are an always-ready cache that allow you to shape data for speed and use across many different blocks, and with different types of markup. Persisted Datasets are cached on the database or in memory using a job, so they’re quick every time. Persisted Datasets should be used when a... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets) |
| Cache Tags | rock_documentation | [Add Cache Tags](/documentation/supporting-rock/caching/cache-tags/add-cache-tags?Version=v19.0) [Use Cache Tags](/documentation/supporting-rock/caching/cache-tags/use-cache-tags?Version=v19.0) [Clear Cache Tags](/documentation/supporting-rock/caching/cache-tags/clear-cache-tags?Version=v19.0) | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Service Job History](../../model-map/models/service-job-history.md) | Core | 19.1.8 | 45 | 15 | 30 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Defined Type](../../model-map/models/defined-type.md) | Core | 19.1.8 | 49 | 19 | 34 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Defined Value](../../model-map/models/defined-value.md) | Core | 19.1.8 | 46 | 17 | 31 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Exception Log](../../model-map/models/exception-log.md) | Core | 19.1.8 | 52 | 23 | 37 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Service Job](../../model-map/models/service-job.md) | Core | 19.1.8 | 56 | 26 | 41 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [History Login](../../model-map/models/history-login.md) | Security | 19.1.8 | 52 | 22 | 34 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent](../../model-map/models/ai-agent.md) | AI | 19.1.8 | 45 | 16 | 30 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session](../../model-map/models/ai-agent-session.md) | AI | 19.1.8 | 28 | 12 | 19 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session Anchor](../../model-map/models/ai-agent-session-anchor.md) | AI | 19.1.8 | 29 | 15 | 20 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session History](../../model-map/models/ai-agent-session-history.md) | AI | 19.1.8 | 27 | 14 | 19 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Skill](../../model-map/models/ai-agent-skill.md) | AI | 19.1.8 | 22 | 8 | 13 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
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
| 19.1 | Core | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Core | Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729 | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Core | Fixed issue that prevented anonymous individuals from adding defined files on a workflow entry form configured with a defined value field type even though 'Allow Add' was enabled. Fixes: #6807 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Core | Fixed an issue in the Defined Value picker component where Single-Select Defined Value attributes configured with "Enhanced for Long Lists" did not display the searchable enhanced experience in Obsidian blocks (e.g., Workflow Entry and Event Registration), requiring manual scrolling through values. Fixes: #6658 #6705 | [source](https://www.rockrms.com/releasenotes) |
| 18.2 | Security | Improved security by adding HMAC authentication to encrypted string values to ensure data integrity. | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | Core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | CRM | Added a new Defined Type called "Record Source" to help track where individuals are first introduced into Rock, such as through event registration, Check-in or Workflow entry forms. | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | Event | Fixed an issue in the Registrant Detail block where Categorized Defined Value fields with visibility filters would disappear during editing, preventing required values from being saved. This happened when the category or value was changed, even if visibility conditions were still met. Fixes: #6452 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | CMS | Fixed an issue where indexing a Content Collection threw an exception if a Content Channel Item contained an attribute value larger than Lucene's maximum field size, even when that attribute wasn’t selected for indexing. Fixes: #6385 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | Core | Fixed an issue where saving new Workflow Types or Registration Templates could result in duplicate records if an error occurred mid-save. Now, the save operation must complete fully or it will be rolled back entirely to maintain data integrity. Fixes: #6238 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | Core | Removed the v17.2 change to the Database Maintenance job that set the default database index fill factor to 100%. The job now returns to its previous behavior while we take additional time to design a long-term solution that better balances index performance with minimizing unnecessary rebuilds. Fixes: #6414 | [source](https://www.rockrms.com/releasenotes) |
| 17.2 | CMS | Updated ElasticSearch UniversalSearch Index and related components to include support for bulk indexing operations. | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Jobs And Scheduling

Keywords: `service job, job history, scheduled job, jobs`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Service Job History | rock_model_map | Service Job History is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |
| Automations | rock_rocku | Automations Presenter: Blake Byers Length: 4:58 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/automations) |
| CSS Icons | rock_rocku | CSS Icons Presenter: Jon Edmiston Length: 1:05 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/css-icons) |
| Campuses | rock_rocku | Campuses Presenter: Cullen McCoy Length: 5:33 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/campuses) |
| Categorize Defined Values | rock_rocku | Categorize Defined Values Presenter: Cullen McCoy Length: 6:22 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/categorize-defined-values) |
| Core Concepts | rock_rocku | Core Concepts Learn the fundamental ideas behind how Rock RMS works and organizes data. What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts) |
| Custom Attributes | rock_rocku | Custom Attributes Presenter: Cullen McCoy Length: 4:56 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/custom-attributes) |
| Jobs | rock_rocku | Jobs Presenter: Jon Edmiston Length: 2:31 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/jobs) |
| Note Types | rock_rocku | Note Types Presenter: Cullen McCoy Length: 10:10 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/note-types) |
| Properties and Attributes | rock_rocku | Properties and Attributes Presenter: Jon Edmiston Length: 3:08 " What is an Entity 1m 05s Properties and Attributes 3m 08s Custom Attributes 4m 56s Defined Types 4m 18s Campuses 5m 33s Note Types 10m 10s Jobs 2m 31s CSS Icons 1m 05s Categorize Defined Values 6m 22s Automations 4m 58s | [source](https://community.rockrms.com/rocku/core-concepts/properties-and-attributes) |

### Diagnostics And Exceptions

Keywords: `exception log, exceptionlog, diagnostics, error, health`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Rock Core Release Notes | rock_core_release_notes | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yesu Chum , Houston's First Baptist Church 4 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yesu Chum , Houston's First Baptist Church 4 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol) |
| Azure Mobile App | triumph_resources | If you use Azure to host your Rock instance, the Azure Mobile App is a must have companion. The app allows you to quickly view your hosting resources and provides a view of resource graphs. The app also serves as a conduit for receiving alerts about service health. While the app isn’t meant for daily administrative tasks, like adding new services, it is an indispensable tool for keeping tabs on the health of your... | [source](https://www.triumph.tech/resources/azure-mobile-app) |
| View the Exception List | rock_documentation | Despite all of our work to eliminate bugs, some will sneak by us. Exceptions, also known as errors, can occur as a result of software bugs or when blocks and pages are misconfigured. While you can set these errors to be emailed to you (see `Admin Tools > Settings > Global Attributes > Email Exceptions List`), you can also view the history of these errors here. Exceptions are sorted chronologically. Instead of... | [source](https://community.rockrms.com/documentation/supporting-rock/data/advanced/view-the-exception-list) |
| Exception Log | rock_model_map | Exception Log is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |

### Cache And Indexing

Keywords: `cache, indexing, index, search`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Cache Manager | rock_documentation | The Cache Manager lets you manage the information cached on your Rock server(s) through the use of cache tags. Cache tags work a bit like personal and organizational tags, except in this case you're tagging types of information. Using the Cache Manager, you can tell Rock to clear the cache of information based on those tags. There are two sides when it comes to configuring and using the Cache Manager: the more... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Add Cache Tags | rock_documentation | When updating content, you’ll sometimes want your Rock site to instantly reflect the changes you’ve made. To meet this need, Rock provides multiple ways to clear a cache. You can clear the cache of all objects using the global “Clear Cache” button, or you can clear a group of cached objects using cache tags. By using cache tags, you can precisely control what objects are removed from cache; without the performance... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) |
| Cache Tags | rock_documentation | [Add Cache Tags](/documentation/supporting-rock/caching/cache-tags/add-cache-tags?Version=v19.0) [Use Cache Tags](/documentation/supporting-rock/caching/cache-tags/use-cache-tags?Version=v19.0) [Clear Cache Tags](/documentation/supporting-rock/caching/cache-tags/clear-cache-tags?Version=v19.0) | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) |
| Use Cache Tags | rock_documentation | After adding cache tags, blocks with caching enabled will have an additional attribute of “Cache Tags” populated with the tags you've added. Open the block settings of a page in your external Rock site and click the button. The cache tags created in the *Cache Manager* are displayed. Select the tag(s) you want to assign and click the Save button. 1. **Cache Tags** - In the Content Channel example pictured above, the... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags) |
| Z-index | rock_community_site | Z-index Utilities Use our low-level z-index utilities to quickly change the stack level of an element or component. z-40 z-30 z-20 z-10 z-0 Class Properties -z-10 z-index: -10; z-0 z-index: 0; z-10 z-index: 10; z-20 z-index: 20; z-30 z-index: 30; z-40 z-index: 40; z-50 z-index: 50; z-auto z-index: auto; | [source](https://community.rockrms.com/styling/utilities/z-index) |
| Caching | rock_documentation | SECTIONS [Caching Fundamentals](?Version=v19.0#caching-fundamentals) [Cache Tags](?Version=v19.0#cache-tags) ### Caching Fundamentals Articles [Intro to Caching](/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching?Version=v19.0) [Caching & Rock Performance](/documentation/supporting-rock/caching/caching-fundamentals/caching-rock-performance?Version=v19.0) [Cache... | [source](https://community.rockrms.com/documentation/supporting-rock/caching) |
| Rock Core Release Notes | rock_core_release_notes | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| GitHub Spotlight: 12/20/2024 | triumph_resources | Here’s what’s new in Rock’s GitHub for Pre-Alpha Release v17.0.34 released on 12/19/2024. v16.10 Highlights Added a new setting named ‘AutoFocus’ to the Obsidian Content Collection View block which automatically selects the search bar, so individuals can start typing in the search bar immediately after the page loads without needing to select the search bar first. Added a new setting called 'Enable Default Address... | [source](https://www.triumph.tech/resources/github-spotlight-12202024) |
| Specifics for Entities | rock_documentation | How does search differ for each entity? Read on for details. # Person The person entity is pretty basic. Once enabled, all individuals in the database will be sent to the index. You can add specific person attributes to be indexed as well (`Admin Tools > General Settings > Person Attributes`). When you add/delete attributes to the index, you'll want to run a bulk load on the Person index to ensure they are available... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Cache | rock_lava_docs | Cache Command Basics Want your Lava to run like lightning? Enable caching! Wrapping your Lava in a cache command will take the results and store it in Rock's memory cache. Subsequent runs will load faster than a New York minute. Let's take a look at a simple example: {% cache key:'decker-page-list' duration:'3600' %} {% person where:'LastName == "Decker"' %} {% for person in personItems %} {{ person.FullName }} <br... | [source](https://community.rockrms.com/lava/commands/cache-commands) |

### Cleanup And Data Integrity

Keywords: `cleanup, data integrity, integrity, stale, orphaned`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | data quality scope | 11:37 | Rock data quality work should be prioritized because dirty people, family, address, and duplicate data affects check-in, communication, reporting credibility, and leadership decisions. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | cleanup prioritization | 20:00 | A practical cleanup program should separate low-effort automations from medium-effort reports and high-effort duplicate decisions, so staff and volunteers spend human review time on records that require judgment. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | built-in automation | 25:51 | Before building custom cleanup processes, review Rock's built-in data automation options such as profile activation/inactivation rules, adult-child family movement, and gender classification thresholds. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | volunteer governance | 28:48 | Data volunteers can help with duplicate and cleanup queues, but they need training, review time, and bounded scope; adding more volunteers does not scale if every merge decision still requires staff judgment. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | continuous improvement | 30:53 | Track recurring data defects in a shared backlog, choose a small set of fields or defect types to address first, set measurable cleanup goals, and share wins so ministry teams understand the operational value of clean Rock data. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Data Integrity Transcript Insight | data integrity | 00:00 | Data integrity work should start from the exact entity and field being corrected, then identify the owner, source of truth, duplicate risk, and reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| Data Integrity Transcript Insight | people records | 00:00 | People and reporting guides should distinguish cleanup, merge, verification, and governance tasks because each has different audit and permission requirements. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| Data Integrity Transcript Insight | data integrity | 00:00 | Data Integrity work should be repeatable: identify the record population, define the correction rule, test with known examples, and document the owner before making bulk changes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| Data Integrity Transcript Insight | reporting quality | 00:00 | For reporting agents, data integrity issues should be surfaced as source-data problems, not hidden by report logic that masks duplicates, missing values, or stale attributes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Media Watch Transcript Insight | rock_community_hubs | This Data Analytics Hub presentation gives public-safe operational guidance for Rock data quality programs: use built-in automation where possible, prioritize a small number of high-value data defects, move actionable cleanup reports into Rock, train a bounded volunteer team, and connect data quality work to ministry outcomes such as check-in, communication, and leadership reporting. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Rock Core Release Notes | rock_core_release_notes | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| GitHub Spotlight: 9/20/2024 | triumph_resources | Below is what's new in Rock's Github for pre-alpha release v17.0.28 that was released on 9/19/2024. v16.7 New setting in the Family Pre-Registration to move Child Information panel above the Adult panel. The team added buttons to hide the 'Clone Schedules' and 'Auto Schedule' in the Obsidian Group Scheduler block settings. Improved the logic that allows interactive experiences to work with a blank Enable Minutes... | [source](https://www.triumph.tech/resources/github-spotlight-9202024-2) |
| Supporting Rock | rock_documentation | ### Data Articles [Data Integrity](/documentation/supporting-rock/data/data-integrity?Version=v19.0) [Interactions](/documentation/supporting-rock/data/interactions?Version=v19.0) [Automations](/documentation/supporting-rock/data/automations?Version=v19.0) ### Hosting Articles [SaaS Hosting](/documentation/supporting-rock/hosting/saas-hosting?Version=v19.0) ### Caching Articles [Caching... | [source](https://community.rockrms.com/documentation/supporting-rock) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yesu Chum , Houston's First Baptist Church 4 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yesu Chum , Houston's First Baptist Church 4 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol) |
| Data Integrity Transcript Insight | rock_rocku | Data Integrity adds guidance for people and reporting work: prove the source of truth, understand cleanup ownership, and verify downstream reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| Data Integrity Transcript Insight | rock_rocku | Data Integrity adds operational guidance for cleanup and reporting quality: define correction rules, test known examples, and document ownership before data changes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |


## Rebuild Dependencies

- Source records: `91`
- Approved claims: `11`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
