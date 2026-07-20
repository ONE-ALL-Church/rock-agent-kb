---
id: concept-system-admin-ops
title: System Administration And Operations
generated: true
last_built: 2026-07-20T05:21:43+00:00
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
- The strongest source families in this build are: rock_community_hubs, rock_documentation, rock_community_site, rock_core_release_notes, rock_developer, rock_model_map.
- Related tags found in source records: usage, operations, workflow, development, training, admin, releases, security.
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
| official | release_caveat | The v19 Page Load Time diagnostic can expose page-debug timing traces without separate observability setup, helping administrators identify slow page components. Use it for diagnosis and confirm findings with broader telemetry when the issue is intermittent or infrastructure-wide. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |
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
- `rock_core_release_notes`: 20
- `rock_developer`: 3
- `rock_documentation`: 22
- `rock_lava_docs`: 1
- `rock_model_map`: 12
- `rock_qa`: 1
- `rock_recipes`: 3
- `rock_rocku`: 24
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Skills Rubric | triumph_resources | Level 1: Foundational Awareness Basic understanding and vocabulary; competently follows guidance of experienced team members. Understands the core components of Azure (VMs, SQL, Resource Groups, Networking). Can follow step-by-step documentation to create or configure basic Azure resources (e.g., create VM, attach disk). Follows all Triumph’s Azure naming conventions and resource group structure. Can navigate the... | [source](https://www.triumph.tech/resources/skills-rubric) |
| Add Cache Tags | rock_documentation | When updating content, you’ll sometimes want your Rock site to instantly reflect the changes you’ve made. To meet this need, Rock provides multiple ways to clear a cache. You can clear the cache of all objects using the global “Clear Cache” button, or you can clear a group of cached objects using cache tags. By using cache tags, you can precisely control what objects are removed from cache; without the performance... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) |
| Advanced Finance | rock_documentation | [Finance Common Defined Types](/documentation/church-management/finance/advanced-finance/finance-common-defined-types?Version=v19.0) [Security for Finance](/documentation/church-management/finance/advanced-finance/security-for-finance?Version=v19.0) [Advanced Utility Payment Entry Block Settings](/documentation/church-management/finance/advanced-finance/advanced-utility-payment-entry-block-settings?Version=v19.0) | [source](https://community.rockrms.com/documentation/church-management/finance/advanced-finance) |
| Cache | rock_lava_docs | Cache Command Basics Want your Lava to run like lightning? Enable caching! Wrapping your Lava in a cache command will take the results and store it in Rock's memory cache. Subsequent runs will load faster than a New York minute. Let's take a look at a simple example: {% cache key:'decker-page-list' duration:'3600' %} {% person where:'LastName == "Decker"' %} {% for person in personItems %} {{ person.FullName }} <br... | [source](https://community.rockrms.com/lava/commands/cache-commands) |
| Cache Manager | rock_documentation | The Cache Manager lets you manage the information cached on your Rock server(s) through the use of cache tags. Cache tags work a bit like personal and organizational tags, except in this case you're tagging types of information. Using the Cache Manager, you can tell Rock to clear the cache of information based on those tags. There are two sides when it comes to configuring and using the Cache Manager: the more... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Cache Persisted Datasets | rock_documentation | Traditional caching in Rock is limited to specific blocks, or to a particular format when using the Lava cache tag. Persisted Datasets are an always-ready cache that allow you to shape data for speed and use across many different blocks, and with different types of markup. Persisted Datasets are cached on the database or in memory using a job, so they’re quick every time. Persisted Datasets should be used when a... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets) |
| Cache Tags | rock_documentation | [Add Cache Tags](/documentation/supporting-rock/caching/cache-tags/add-cache-tags?Version=v19.0) [Use Cache Tags](/documentation/supporting-rock/caching/cache-tags/use-cache-tags?Version=v19.0) [Clear Cache Tags](/documentation/supporting-rock/caching/cache-tags/clear-cache-tags?Version=v19.0) | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) |
| Caching | rock_documentation | SECTIONS [Caching Fundamentals](?Version=v19.0#caching-fundamentals) [Cache Tags](?Version=v19.0#cache-tags) ### Caching Fundamentals Articles [Intro to Caching](/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching?Version=v19.0) [Caching & Rock Performance](/documentation/supporting-rock/caching/caching-fundamentals/caching-rock-performance?Version=v19.0) [Cache... | [source](https://community.rockrms.com/documentation/supporting-rock/caching) |
| Clear Cache Tags | rock_documentation | To clear all items that are tied to a specific tag, go to `Admin Tools > CMS Configuration > Cache Manager`. Click the button to the right of the tag's row. This will empty the cache of all linked keys. | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags) |
| Configure Person Tokens | rock_documentation | Person tokens come preconfigured in Rock and can be found in the Global Attributes screen (`Admin Tools > Settings > Global Attributes`).There are three Person Token attributes: Person Token Expire Minutes, Person Token Usage Limit, and Person Token Use Legacy Fallback. Click on an attribute to open its configuration settings. The Person Token Expire Minutes attribute is the length of time the person token is valid,... | [source](https://community.rockrms.com/documentation/core-concepts/security/person-tokens/configure-person-tokens) |
| Core Concepts | rock_documentation | ### Rock Fundamentals Articles [Entities](/documentation/core-concepts/rock-fundamentals/entities?Version=v19.0) [Attributes](/documentation/core-concepts/rock-fundamentals/attributes?Version=v19.0) [Defined Types](/documentation/core-concepts/rock-fundamentals/defined-types?Version=v19.0) [Blocks](/documentation/core-concepts/rock-fundamentals/blocks?Version=v19.0)... | [source](https://community.rockrms.com/documentation/core-concepts) |
| Defined Types | rock_documentation | [Intro to Defined Types](/documentation/core-concepts/rock-fundamentals/defined-types/intro-to-defined-types?Version=v19.0) [Defined Values](/documentation/core-concepts/rock-fundamentals/defined-types/defined-values?Version=v19.0) | [source](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/defined-types) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Service Job History](../../model-map/models/service-job-history.md) | Core | 19.2.0 | 45 | 15 | 30 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Defined Type](../../model-map/models/defined-type.md) | Core | 19.2.0 | 49 | 19 | 34 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Defined Value](../../model-map/models/defined-value.md) | Core | 19.2.0 | 46 | 17 | 31 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Exception Log](../../model-map/models/exception-log.md) | Core | 19.2.0 | 52 | 23 | 37 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Service Job](../../model-map/models/service-job.md) | Core | 19.2.0 | 56 | 26 | 41 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [History Login](../../model-map/models/history-login.md) | Security | 19.2.0 | 52 | 22 | 34 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent](../../model-map/models/ai-agent.md) | AI | 19.2.0 | 45 | 16 | 30 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session](../../model-map/models/ai-agent-session.md) | AI | 19.2.0 | 28 | 12 | 19 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session Anchor](../../model-map/models/ai-agent-session-anchor.md) | AI | 19.2.0 | 29 | 15 | 20 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Session History](../../model-map/models/ai-agent-session-history.md) | AI | 19.2.0 | 27 | 14 | 19 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Agent Skill](../../model-map/models/ai-agent-skill.md) | AI | 19.2.0 | 22 | 8 | 13 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [AI Provider](../../model-map/models/ai-provider.md) | AI | 19.2.0 | 43 | 15 | 28 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `AI Agent.AIAgentSkills` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.AvatarBinaryFile` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `AI Agent.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 19.1 | Core | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| 19.3 | CMS | Fixed Person Attribute Values configured for indexing not being included in Universal Search results after a bulk re-index, and restored the missing "Indexing Enabled" option in the Attributes block so Attributes can be flagged for indexing. Fixes: #6857 | [source](https://www.rockrms.com/releasenotes) |
| 19.3 | Event | Fixed Defined Value attributes not loading their options when editing an Event Item. Fixes: #6878 | [source](https://www.rockrms.com/releasenotes) |
| 19.3 | Event | Fixed inline attribute editors (such as adding a new Defined Value) on the Event Detail block returning an HTTP 401 by adding the Event Calendar Item attribute field type rules to the security grant. Fixes: #6881 | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Core | Fixed issue that prevented anonymous individuals from adding defined files on a workflow entry form configured with a defined value field type even though 'Allow Add' was enabled. Fixes: #6807 | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Core | Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Core | Fixed an issue in the Defined Value picker component where Single-Select Defined Value attributes configured with "Enhanced for Long Lists" did not display the searchable enhanced experience in Obsidian blocks (e.g., Workflow Entry and Event Registration), requiring manual scrolling through values. Fixes: #6658 #6705 | [source](https://www.rockrms.com/releasenotes) |
| 18.2 | Security | Improved security by adding HMAC authentication to encrypted string values to ensure data integrity. | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | Core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | CRM | Added a new Defined Type called "Record Source" to help track where individuals are first introduced into Rock, such as through event registration, Check-in or Workflow entry forms. | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | Event | Fixed an issue in the Registrant Detail block where Categorized Defined Value fields with visibility filters would disappear during editing, preventing required values from being saved. This happened when the category or value was changed, even if visibility conditions were still met. Fixes: #6452 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | CMS | Fixed an issue where indexing a Content Collection threw an exception if a Content Channel Item contained an attribute value larger than Lucene's maximum field size, even when that attribute wasn’t selected for indexing. Fixes: #6385 | [source](https://www.rockrms.com/releasenotes) |

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
| Campuses Training | rock_rocku | Campuses Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/campuses) |
| Categorize Defined Values Training | rock_rocku | Categorize Defined Values Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/categorize-defined-values) |
| Custom Attributes Training | rock_rocku | Custom Attributes Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/custom-attributes) |
| Defined Types Training | rock_rocku | Defined Types Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/defined-types) |
| Jobs Training | rock_rocku | Jobs Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/jobs) |
| Note Types Training | rock_rocku | Note Types Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/note-types) |
| Properties and Attributes Training | rock_rocku | Properties and Attributes Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/properties-and-attributes) |
| What is an Entity Training | rock_rocku | What is an Entity Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/what-is-an-entity) |
| IP Address Geocoding Training | rock_rocku | IP Address Geocoding Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/individuals-in-rock/ip-address-geocoding) |

### Diagnostics And Exceptions

Keywords: `exception log, exceptionlog, diagnostics, error, health`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Rock Core Release Notes | rock_core_release_notes | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yeşu Chum , Houston's First Baptist Church 6 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yeşu Chum , Houston's First Baptist Church 6 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol) |
| View the Exception List | rock_documentation | Despite all of our work to eliminate bugs, some will sneak by us. Exceptions, also known as errors, can occur as a result of software bugs or when blocks and pages are misconfigured. While you can set these errors to be emailed to you (see `Admin Tools > Settings > Global Attributes > Email Exceptions List`), you can also view the history of these errors here. Exceptions are sorted chronologically. Instead of... | [source](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list) |
| Exception Log | rock_model_map | Exception Log is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |
| Intro to Group History | rock_documentation | As you work with groups—adding and removing members, adjusting schedules and member roles, etc.—there may be times when you want to get a 40,000ft view to see how they're doing. Rock's Group History feature allows you to do just that. Group History takes all of the configurations and changes made to a group and compiles them into timeline and table views that let you easily view the life and health of that group.... | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history) |
| Intro to Finance Reports | rock_documentation | Financial reporting is crucial not only for tracking finances but also for understanding significant changes within your organization. Tithing is an important indicator of your organization's health. By analyzing giving patterns, you can identify direct correlations between people and their contributions. For example, you can reach out to individuals who have recently stopped giving to see if they need support or... | [source](https://community.rockrms.com/documentation/church-management/finance/finance-reports/intro-to-finance-reports) |

### Cache And Indexing

Keywords: `cache, indexing, index, search`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Add Cache Tags | rock_documentation | When updating content, you’ll sometimes want your Rock site to instantly reflect the changes you’ve made. To meet this need, Rock provides multiple ways to clear a cache. You can clear the cache of all objects using the global “Clear Cache” button, or you can clear a group of cached objects using cache tags. By using cache tags, you can precisely control what objects are removed from cache; without the performance... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) |
| Use Cache Tags | rock_documentation | After adding cache tags, blocks with caching enabled will have an additional attribute of “Cache Tags” populated with the tags you've added. Open the block settings of a page in your external Rock site and click the button. The cache tags created in the *Cache Manager* are displayed. Select the tag(s) you want to assign and click the Save button. 1. **Cache Tags** - In the Content Channel example pictured above, the... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags) |
| Cache Manager | rock_documentation | The Cache Manager lets you manage the information cached on your Rock server(s) through the use of cache tags. Cache tags work a bit like personal and organizational tags, except in this case you're tagging types of information. Using the Cache Manager, you can tell Rock to clear the cache of information based on those tags. There are two sides when it comes to configuring and using the Cache Manager: the more... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Cache Tags | rock_documentation | [Add Cache Tags](/documentation/supporting-rock/caching/cache-tags/add-cache-tags?Version=v19.0) [Use Cache Tags](/documentation/supporting-rock/caching/cache-tags/use-cache-tags?Version=v19.0) [Clear Cache Tags](/documentation/supporting-rock/caching/cache-tags/clear-cache-tags?Version=v19.0) | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) |
| Z-index | rock_community_site | Z-index Utilities Use our low-level z-index utilities to quickly change the stack level of an element or component. z-40 z-30 z-20 z-10 z-0 Class Properties -z-10 z-index: -10; z-0 z-index: 0; z-10 z-index: 10; z-20 z-index: 20; z-30 z-index: 30; z-40 z-index: 40; z-50 z-index: 50; z-auto z-index: auto; | [source](https://community.rockrms.com/styling/utilities/z-index) |
| Caching | rock_documentation | SECTIONS [Caching Fundamentals](?Version=v19.0#caching-fundamentals) [Cache Tags](?Version=v19.0#cache-tags) ### Caching Fundamentals Articles [Intro to Caching](/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching?Version=v19.0) [Caching & Rock Performance](/documentation/supporting-rock/caching/caching-fundamentals/caching-rock-performance?Version=v19.0) [Cache... | [source](https://community.rockrms.com/documentation/supporting-rock/caching) |
| Clear Cache Tags | rock_documentation | To clear all items that are tied to a specific tag, go to `Admin Tools > CMS Configuration > Cache Manager`. Click the button to the right of the tag's row. This will empty the cache of all linked keys. | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags) |
| Rock Core Release Notes | rock_core_release_notes | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| Specifics for Entities | rock_documentation | How does search differ for each entity? Read on for details. # Person The person entity is pretty basic. Once enabled, all individuals in the database will be sent to the index. You can add specific person attributes to be indexed as well (`Admin Tools > General Settings > Person Attributes`). When you add/delete attributes to the index, you'll want to run a bulk load on the Person index to ensure they are available... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Cache Persisted Datasets | rock_documentation | Traditional caching in Rock is limited to specific blocks, or to a particular format when using the Lava cache tag. Persisted Datasets are an always-ready cache that allow you to shape data for speed and use across many different blocks, and with different types of markup. Persisted Datasets are cached on the database or in memory using a job, so they’re quick every time. Persisted Datasets should be used when a... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets) |

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
| Supporting Rock | rock_documentation | ### Data Articles [Data Integrity](/documentation/supporting-rock/data/data-integrity?Version=v19.0) [Interactions](/documentation/supporting-rock/data/interactions?Version=v19.0) [Automations](/documentation/supporting-rock/data/automations?Version=v19.0) ### Hosting Articles [SaaS Hosting](/documentation/supporting-rock/hosting/saas-hosting?Version=v19.0) ### Caching Articles [Caching... | [source](https://community.rockrms.com/documentation/supporting-rock) |
| Data Integrity Transcript Insight | rock_rocku | Data Integrity adds guidance for people and reporting work: prove the source of truth, understand cleanup ownership, and verify downstream reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| Data Integrity Transcript Insight | rock_rocku | Data Integrity adds operational guidance for cleanup and reporting quality: define correction rules, test known examples, and document ownership before data changes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| Intro to Data Integrity | rock_documentation | With data coming into Rock from all directions, it can be a real challenge to keep it all clean, consistent and accurate. To help you out with that, we've built tools that find and fix issues as they arise. You'll find these tools under: `Tools > Data Integrity.` Only individuals in the *Data Integrity Worker* security role will have access to these tools. We will look at each part in detail in the following... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/intro-to-data-integrity) |
| Use Duplicate Finder | rock_documentation | The duplicate finder routinely goes through your database looking for records that could be duplicates. When it finds possible matches, it scores them and lists them for you under: `Tools > Data Integrity > Duplicate Finder`. 1. **Confidence** - Indicates the likelihood that this is a duplicate record. 2. **Account Protection Profile** - The [Account Protection... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yeşu Chum , Houston's First Baptist Church 6 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yeşu Chum , Houston's First Baptist Church 6 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol) |
| Overview | rock_developer | Helix is the codename for an upcoming project that represents the next evolution of Lava for web development, integrating four distinct technologies. * [HTMX](/documentation/helix/overview#htmx) * [Lava Applications](/documentation/helix/overview#lava-applications) * [Lava Commands](/documentation/helix/overview#lava-commands) * [Control Shortcodes](/documentation/helix/overview#control-shortcodes) Important Before... | [source](https://community.rockrms.com/developer/helix/overview) |

### Search

Keywords: `search, universal search, indexing, index, search components`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Specifics for Entities | rock_documentation | How does search differ for each entity? Read on for details. # Person The person entity is pretty basic. Once enabled, all individuals in the database will be sent to the index. You can add specific person attributes to be indexed as well (`Admin Tools > General Settings > Person Attributes`). When you add/delete attributes to the index, you'll want to run a bulk load on the Person index to ensure they are available... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Enable Entities for Universal Search | rock_documentation | Once you have a provider configured, we're ready to enable entities to be indexed. To do this, navigate to `Admin Tools > General Settings > Universal Search Control Panel`. At the top of this page, you'll see a few details about the provider you selected. Below you'll find a list of the entities that are able to be indexed. To enable a new entity type, click the row of the entity and select Enable Indexing on the... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) |
| Enable a Search Provider | rock_documentation | Ready… set… let's get started! (Note: if you choose to use Elasticsearch, it will need to be [installed](/documentation/core-concepts/search/universal-search/installing-elasticsearch) before continuing.) First, we'll need to tell Rock which search provider we'd like to use and provide the configuration details needed to connect. We do this under `Admin Tools > System Settings > Universal Search Index Components`.... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-a-search-provider) |
| Integrating Smart Search | rock_documentation | If you've been using Rock for more than a day, you've used the Smart Search block at the top of the page. Universal Search can be configured to participate in Smart Search, and once it is, you'll find that it's your go-to search type. Once you have Universal Search up and indexing, you'll need to enable the Smart Search integration. You'll do this under `Admin Tools > System Settings > Search Services`. If it isn't... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/integrating-smart-search) |
| Customizing Results for Entities | rock_documentation | How results are returned from the search is important. Luckily, there are numerous ways to customize the results from the search. We cover all the options below. # Default Entity Results Each entity has a default result template that you can change. This is a great place to modify what you'd like to be returned across multiple search interfaces. You can edit these templates on a per-entity basis under Admin Tools >... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/customizing-results-for-entities) |
| Installing Elasticsearch | rock_documentation | To install Elasticsearch you will need to follow the steps below. Detailed instructions for installing and running ElasticSearch can also be found on the [elastic.co](https://www.elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html) website. Note **Windows Service**If you want to install and run Elasticsearch as a service on Windows, follow the instructions found... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/installing-elasticsearch) |
| Intro to Universal Search | rock_documentation | The basic search capability in Rock is quite powerful, but sometimes you may need more. That's where Universal Search comes in. Universal Search allows you to search multiple types of data at once in a full-text manner. In a sense, it's like Google for Rock. With this great power comes some additional technical knowledge, but don't worry we'll unpack it all here in this guide. # Overview The first thing that you'll... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/intro-to-universal-search) |
| Search | rock_documentation | SECTIONS [Searching for People](?Version=v19.0#searching-for-people) ### Searching for People Articles [Search by Name](/documentation/core-concepts/search/searching-for-people/search-by-name?Version=v19.0) [Search by Phone](/documentation/core-concepts/search/searching-for-people/search-by-phone?Version=v19.0) [Search by Other... | [source](https://community.rockrms.com/documentation/core-concepts/search) |
| Search by Name | rock_documentation | To find someone in the database, start by using the *Smart Search*tool found at the top of every page. This tool can be used to search several different types of data, but it defaults to searching for individuals by name. When searching by name, it's important to know some tricks to improve the quality of your search and to save time. Keep in mind that you don't need to type a person's full name to search. You can... | [source](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-name) |
| Search by Other Means | rock_documentation | Searching by *[People](/documentation/core-concepts/search/searching-for-people)* and by *[Name](/documentation/core-concepts/search/searching-for-people/search-by-name)* aren't the only ways to find people in Rock, below are some other ways to search. # Searching by Email Yep, you guessed it: Rock can search by email using the Smart Search tool, too. Partial searches are supported. We're sure you've got it by now,... | [source](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-other-means) |


## Rebuild Dependencies

- Source records: `91`
- Approved claims: `12`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
