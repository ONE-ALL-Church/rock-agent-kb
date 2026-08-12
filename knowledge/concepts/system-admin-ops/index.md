---
id: concept-system-admin-ops
title: System Administration And Operations
generated: true
last_built: 2026-08-12T12:45:00+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
source_freshness_status: complete
source_last_checked_at: 2026-08-12T06:18:53+00:00
source_native_migration_status: partial
source_native_article_coverage: 6/70
legacy_summary_retirement_coverage: 6/70
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
- The strongest source families in this build are: rock_documentation, rock_community_hubs, rock_community_blog, rock_core_release_notes, rock_model_map, rock_recipes.
- Related tags found in source records: operations, usage, admin, sql, api, security, lava, finance.
- Source detail types include: community_blog_article, documentation_article, question, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | data quality scope | 11:37 | Rock data quality work should be prioritized because dirty people, family, address, and duplicate data affects check-in, communication, reporting credibility, and leadership decisions. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | cleanup prioritization | 20:00 | A practical cleanup program should separate low-effort automations from medium-effort reports and high-effort duplicate decisions, so staff and volunteers spend human review time on records that require judgment. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | built-in automation | 25:51 | Before building custom cleanup processes, review Rock's built-in data automation options such as profile activation/inactivation rules, adult-child family movement, and gender classification thresholds. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | volunteer governance | 28:48 | Data volunteers can help with duplicate and cleanup queues, but they need training, review time, and bounded scope; adding more volunteers does not scale if every merge decision still requires staff judgment. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |
| Media Watch Transcript Insight | continuous improvement | 30:53 | Track recurring data defects in a shared backlog, choose a small set of fields or defect types to address first, set measurable cleanup goals, and share wins so ministry teams understand the operational value of clean Rock data. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | release_caveat | The v19 Page Load Time diagnostic can expose page-debug timing traces without separate observability setup, helping administrators identify slow page components. Use it for diagnosis and confirm findings with broader telemetry when the issue is intermittent or infrastructure-wide. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |

## Source Coverage

- `rock_community_blog`: 1
- `rock_community_hubs`: 1
- `rock_core_release_notes`: 2
- `rock_documentation`: 70
- `rock_model_map`: 12
- `rock_qa`: 1
- `rock_recipes`: 1
- `rock_rocku`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Add Cache Tags | rock_documentation | When updating content, you’ll sometimes want your Rock site to instantly reflect the changes you’ve made. To meet this need, Rock provides multiple ways to clear a cache. You can clear the cache of all objects using the global “Clear Cache” button, or you can clear a group of cached objects using cache tags. By using cache tags, you can precisely control what objects are removed from cache; without the performance... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) |
| Use Cache Tags | rock_documentation | After adding cache tags, blocks with caching enabled will have an additional attribute of “Cache Tags” populated with the tags you've added. Open the block settings of a page in your external Rock site and click the button. The cache tags created in the *Cache Manager* are displayed. Select the tag(s) you want to assign and click the Save button. 1. **Cache Tags** - In the Content Channel example pictured above, the... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags) |
| Cache Manager | rock_documentation | The Cache Manager lets you manage the information cached on your Rock server(s) through the use of cache tags. Cache tags work a bit like personal and organizational tags, except in this case you're tagging types of information. Using the Cache Manager, you can tell Rock to clear the cache of information based on those tags. There are two sides when it comes to configuring and using the Cache Manager: the more... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Cache Tags | rock_documentation | [Add Cache Tags](/documentation/supporting-rock/caching/cache-tags/add-cache-tags?Version=v19.0) [Use Cache Tags](/documentation/supporting-rock/caching/cache-tags/use-cache-tags?Version=v19.0) [Clear Cache Tags](/documentation/supporting-rock/caching/cache-tags/clear-cache-tags?Version=v19.0) | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) |
| Caching | rock_documentation | SECTIONS [Caching Fundamentals](?Version=v19.0#caching-fundamentals) [Cache Tags](?Version=v19.0#cache-tags) ### Caching Fundamentals Articles [Intro to Caching](/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching?Version=v19.0) [Caching & Rock Performance](/documentation/supporting-rock/caching/caching-fundamentals/caching-rock-performance?Version=v19.0) [Cache... | [source](https://community.rockrms.com/documentation/supporting-rock/caching) |
| Clear Cache Tags | rock_documentation | To clear all items that are tied to a specific tag, go to `Admin Tools > CMS Configuration > Cache Manager`. Click the button to the right of the tag's row. This will empty the cache of all linked keys. | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags) |
| Specifics for Entities | rock_documentation | How does search differ for each entity? Read on for details. # Person The person entity is pretty basic. Once enabled, all individuals in the database will be sent to the index. You can add specific person attributes to be indexed as well (`Admin Tools > General Settings > Person Attributes`). When you add/delete attributes to the index, you'll want to run a bulk load on the Person index to ensure they are available... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Cache Persisted Datasets | rock_documentation | Traditional caching in Rock is limited to specific blocks, or to a particular format when using the Lava cache tag. Persisted Datasets are an always-ready cache that allow you to shape data for speed and use across many different blocks, and with different types of markup. Persisted Datasets are cached on the database or in memory using a job, so they’re quick every time. Persisted Datasets should be used when a... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets) |
| Enable Entities for Universal Search | rock_documentation | Once you have a provider configured, we're ready to enable entities to be indexed. To do this, navigate to `Admin Tools > General Settings > Universal Search Control Panel`. At the top of this page, you'll see a few details about the provider you selected. Below you'll find a list of the entities that are able to be indexed. To enable a new entity type, click the row of the entity and select Enable Indexing on the... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) |
| Enable a Search Provider | rock_documentation | Ready… set… let's get started! (Note: if you choose to use Elasticsearch, it will need to be [installed](/documentation/core-concepts/search/universal-search/installing-elasticsearch) before continuing.) First, we'll need to tell Rock which search provider we'd like to use and provide the configuration details needed to connect. We do this under `Admin Tools > System Settings > Universal Search Index Components`.... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-a-search-provider) |
| Integrating Smart Search | rock_documentation | If you've been using Rock for more than a day, you've used the Smart Search block at the top of the page. Universal Search can be configured to participate in Smart Search, and once it is, you'll find that it's your go-to search type. Once you have Universal Search up and indexing, you'll need to enable the Smart Search integration. You'll do this under `Admin Tools > System Settings > Search Services`. If it isn't... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/integrating-smart-search) |
| Intro to Caching | rock_documentation | Caching in Rock operates on the principle that once a piece of content has been created it doesn’t need to be created again. So, a copy can be kept around in a cache. Keeping content in a cache means it can be served very quickly, without triggering slow database queries or web requests. With caching you can provide individuals with faster page loads and a better experience when your server is under heavy load.... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching) |

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

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Jobs And Scheduling

Keywords: `service job, job history, scheduled job, jobs`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Use Audit Information | rock_documentation | Most changes to the Rock database are tracked in a special audit table. The information in these tables is presented in the screens of this section. This is a helpful tool for you to see what changes are being made and by whom. You can also use these logs to write custom SQL reports or create custom jobs that take action after certain changes. Auditing can be enabled under `Admin Tools > Settings > Global Attributes... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-audit-information) |
| Intro to Observability | rock_documentation | Rock's Observability feature unveils system performance insights. It tackles the challenge of spotting and resolving performance hiccups in Rock. With Observability you can track page loading speed, individual block load times, database transaction duration, and job efficiency. What's unique about Observability is that it's in tune with Rock's architecture—pages, blocks, and jobs—offering precise, relevant,... | [source](https://community.rockrms.com/documentation/supporting-rock/data/observability/intro-to-observability) |
| Service Job History | rock_model_map | Service Job History is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |
| Campuses Training | rock_rocku | Campuses Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/campuses) |
| Categorize Defined Values Training | rock_rocku | Categorize Defined Values Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/categorize-defined-values) |
| Custom Attributes Training | rock_rocku | Custom Attributes Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/custom-attributes) |
| Defined Types Training | rock_rocku | Defined Types Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/defined-types) |
| Jobs Training | rock_rocku | Jobs Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/jobs) |
| Note Types Training | rock_rocku | Note Types Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/note-types) |
| Properties and Attributes Training | rock_rocku | Properties and Attributes Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer What is an Entity 1:05 Properties and Attributes 3:08 Custom Attributes 4:56 Defined Types 4:18 Campuses 5:33 Jobs 2:31 Categorize Defined Values 6:22 IP Address Geocoding 5:03 Note Types 9:28 Experience Mode 3:05 | [source](https://community.rockrms.com/rocku/core-concepts/properties-and-attributes) |

### Diagnostics And Exceptions

Keywords: `exception log, exceptionlog, diagnostics, error, health`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| View the Exception List | rock_documentation | Despite all of our work to eliminate bugs, some will sneak by us. Exceptions, also known as errors, can occur as a result of software bugs or when blocks and pages are misconfigured. While you can set these errors to be emailed to you (see `Admin Tools > Settings > Global Attributes > Email Exceptions List`), you can also view the history of these errors here. Exceptions are sorted chronologically. Instead of... | [source](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list) |
| Use Rock Logs | rock_documentation | Rock provides a simple, easy to use logging tool. Most of the time you won't need this but having logs can be helpful when troubleshooting or researching. The Rock Log is similar to the [Exception List](/documentation/supporting-rock/data/advanced-data/view-the-exception-list), except you can track more than just errors. Logs are turned off by default, and typically should only be turned on if there is a specific... | [source](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/use-rock-logs) |
| Rock Core Release Notes | rock_core_release_notes | Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the folder may not get recreated. Previously, the Clear Cache button would throw a DirectoryNotFoundException in this case. Now it checks for... | [source](https://www.rockrms.com/releasenotes) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yeşu Chum , Houston's First Baptist Church 6 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522) |
| Security Management - Data Integrity and QoL | rock_recipes | 4 Security Management - Data Integrity and QoL Shared by Yeşu Chum , Houston's First Baptist Church 6 months ago Administration / Finance, Security Beginner Finally, Security That Doesn't Make You Want to Cry Ever tried to figure out who has access to what in Rock? It's like playing detective with a blindfold on. This dashboard hopefully saves you a few headaches. What Does This Thing Do? This dashboard gives you a... | [source](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol) |
| Exception Log | rock_model_map | Exception Log is a Rock model in the Core category. | [source](https://community.rockrms.com/ModelMap) |
| Track Workflow Statistics and Health | rock_recipes | 6 Track Workflow Statistics and Health Shared by Matthew Ewing , Lakepointe Church 4 years ago 12.0 General Intermediate Have you wanted to see at a glance how many times a workflow has run? Do you ever wonder how many people using workflows you’ve created are experiencing errors? Do you ever think about all the workflows that are never completed and remain alive in the system and reprocess every few hours? If... | [source](https://community.rockrms.com/recipes/257) |

### Cache And Indexing

Keywords: `cache, indexing, index, search`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Add Cache Tags | rock_documentation | When updating content, you’ll sometimes want your Rock site to instantly reflect the changes you’ve made. To meet this need, Rock provides multiple ways to clear a cache. You can clear the cache of all objects using the global “Clear Cache” button, or you can clear a group of cached objects using cache tags. By using cache tags, you can precisely control what objects are removed from cache; without the performance... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) |
| Use Cache Tags | rock_documentation | After adding cache tags, blocks with caching enabled will have an additional attribute of “Cache Tags” populated with the tags you've added. Open the block settings of a page in your external Rock site and click the button. The cache tags created in the *Cache Manager* are displayed. Select the tag(s) you want to assign and click the Save button. 1. **Cache Tags** - In the Content Channel example pictured above, the... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags) |
| Cache Manager | rock_documentation | The Cache Manager lets you manage the information cached on your Rock server(s) through the use of cache tags. Cache tags work a bit like personal and organizational tags, except in this case you're tagging types of information. Using the Cache Manager, you can tell Rock to clear the cache of information based on those tags. There are two sides when it comes to configuring and using the Cache Manager: the more... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Cache Tags | rock_documentation | [Add Cache Tags](/documentation/supporting-rock/caching/cache-tags/add-cache-tags?Version=v19.0) [Use Cache Tags](/documentation/supporting-rock/caching/cache-tags/use-cache-tags?Version=v19.0) [Clear Cache Tags](/documentation/supporting-rock/caching/cache-tags/clear-cache-tags?Version=v19.0) | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) |
| Caching | rock_documentation | SECTIONS [Caching Fundamentals](?Version=v19.0#caching-fundamentals) [Cache Tags](?Version=v19.0#cache-tags) ### Caching Fundamentals Articles [Intro to Caching](/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching?Version=v19.0) [Caching & Rock Performance](/documentation/supporting-rock/caching/caching-fundamentals/caching-rock-performance?Version=v19.0) [Cache... | [source](https://community.rockrms.com/documentation/supporting-rock/caching) |
| Clear Cache Tags | rock_documentation | To clear all items that are tied to a specific tag, go to `Admin Tools > CMS Configuration > Cache Manager`. Click the button to the right of the tag's row. This will empty the cache of all linked keys. | [source](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags) |
| Specifics for Entities | rock_documentation | How does search differ for each entity? Read on for details. # Person The person entity is pretty basic. Once enabled, all individuals in the database will be sent to the index. You can add specific person attributes to be indexed as well (`Admin Tools > General Settings > Person Attributes`). When you add/delete attributes to the index, you'll want to run a bulk load on the Person index to ensure they are available... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Cache Persisted Datasets | rock_documentation | Traditional caching in Rock is limited to specific blocks, or to a particular format when using the Lava cache tag. Persisted Datasets are an always-ready cache that allow you to shape data for speed and use across many different blocks, and with different types of markup. Persisted Datasets are cached on the database or in memory using a job, so they’re quick every time. Persisted Datasets should be used when a... | [source](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets) |
| Enable Entities for Universal Search | rock_documentation | Once you have a provider configured, we're ready to enable entities to be indexed. To do this, navigate to `Admin Tools > General Settings > Universal Search Control Panel`. At the top of this page, you'll see a few details about the provider you selected. Below you'll find a list of the entities that are able to be indexed. To enable a new entity type, click the row of the entity and select Enable Indexing on the... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) |
| Enable a Search Provider | rock_documentation | Ready… set… let's get started! (Note: if you choose to use Elasticsearch, it will need to be [installed](/documentation/core-concepts/search/universal-search/installing-elasticsearch) before continuing.) First, we'll need to tell Rock which search provider we'd like to use and provide the configuration details needed to connect. We do this under `Admin Tools > System Settings > Universal Search Index Components`.... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-a-search-provider) |

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

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Intro to Data Integrity | rock_documentation | With data coming into Rock from all directions, it can be a real challenge to keep it all clean, consistent and accurate. To help you out with that, we've built tools that find and fix issues as they arise. You'll find these tools under: `Tools > Data Integrity.` Only individuals in the *Data Integrity Worker* security role will have access to these tools. We will look at each part in detail in the following... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/intro-to-data-integrity) |
| Use Duplicate Finder | rock_documentation | The duplicate finder routinely goes through your database looking for records that could be duplicates. When it finds possible matches, it scores them and lists them for you under: `Tools > Data Integrity > Duplicate Finder`. 1. **Confidence** - Indicates the likelihood that this is a duplicate record. 2. **Account Protection Profile** - The [Account Protection... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder) |
| Data | rock_documentation | SECTIONS [Data Integrity](?Version=v19.0#data-integrity) [Interactions](?Version=v19.0#interactions) [Automations](?Version=v19.0#automations) ### Data Integrity Articles [Intro to Data Integrity](/documentation/supporting-rock/data/data-integrity/intro-to-data-integrity?Version=v19.0) [Use Duplicate Finder](/documentation/supporting-rock/data/data-integrity/use-duplicate-finder?Version=v19.0) [Process National... | [source](https://community.rockrms.com/documentation/supporting-rock/data) |
| Data Integrity | rock_documentation | [Intro to Data Integrity](/documentation/supporting-rock/data/data-integrity/intro-to-data-integrity?Version=v19.0) [Use Duplicate Finder](/documentation/supporting-rock/data/data-integrity/use-duplicate-finder?Version=v19.0) [Process National Change of Address](/documentation/supporting-rock/data/data-integrity/process-national-change-of-address?Version=v19.0) [Connection Status... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity) |
| Location Editor | rock_documentation | Clean address data keeps maps, check-in and mailings accurate. The Location Editor is where an administrator finds and fixes location records, most often addresses Rock could not geocode. **Open it**: Go to `Tools > Data Integrity > Location Editor`. **Find ungeocoded addresses**: The list holds every location in your database, so filter it down. Set the Not Geocoded filter to show only addresses missing... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor) |
| Use Audit Information | rock_documentation | Most changes to the Rock database are tracked in a special audit table. The information in these tables is presented in the screens of this section. This is a helpful tool for you to see what changes are being made and by whom. You can also use these logs to write custom SQL reports or create custom jobs that take action after certain changes. Auditing can be enabled under `Admin Tools > Settings > Global Attributes... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-audit-information) |
| Use Data Automation | rock_documentation | Rock ships with a powerful Data Automation job that automatically updates person and family records. This makes things a lot easier for you. The job settings are configured here on the Data Automation page, located at: `Tools > Data Integrity > Data Automation.` The Data Automation job uses these settings to update person and family records in the following ways: * Reactivating individuals who are currently inactive... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation) |
| Administer Photo Requests | rock_documentation | Rock is about fostering relationships. Nothing helps this more than having photos in the system. In the past, keeping up with photos was a complex and time draining task. No longer! Rock makes it easy to populate photos into the database by asking individuals to upload a photo from an emailed request. Let's take a look at how it works. 1. **Request** - Staff sends out a photo request. This request, as we'll learn... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/administer-photo-requests) |
| Merge Duplicate Records | rock_documentation | # Where Duplicates Come From Duplicate records happen - period. It’s important that your organization understands why they occur and has a process to eliminate them by merging duplicate records. There are two main ways duplicate records are added to the system. The first is by a staff person or volunteer using the internal site. Before you add someone to the database, it’s important that you make sure they haven’t... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records) |
| Configure Phone Number Lookup | rock_documentation | The *Phone Number Lookup* feature is a great alternative to traditional methods of identifying a person. Instead of logging in or providing personal information, all the person needs to do is enter their mobile phone number and confirm they’re in possession of the device with that number. # Overview To start, the person enters their mobile phone number in the screen pictured below. After clicking `Lookup`, the... | [source](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/configure-phone-number-lookup) |

### Search

Keywords: `search, universal search, indexing, index, search components`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Specifics for Entities | rock_documentation | How does search differ for each entity? Read on for details. # Person The person entity is pretty basic. Once enabled, all individuals in the database will be sent to the index. You can add specific person attributes to be indexed as well (`Admin Tools > General Settings > Person Attributes`). When you add/delete attributes to the index, you'll want to run a bulk load on the Person index to ensure they are available... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Enable Entities for Universal Search | rock_documentation | Once you have a provider configured, we're ready to enable entities to be indexed. To do this, navigate to `Admin Tools > General Settings > Universal Search Control Panel`. At the top of this page, you'll see a few details about the provider you selected. Below you'll find a list of the entities that are able to be indexed. To enable a new entity type, click the row of the entity and select Enable Indexing on the... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) |
| Enable a Search Provider | rock_documentation | Ready… set… let's get started! (Note: if you choose to use Elasticsearch, it will need to be [installed](/documentation/core-concepts/search/universal-search/installing-elasticsearch) before continuing.) First, we'll need to tell Rock which search provider we'd like to use and provide the configuration details needed to connect. We do this under `Admin Tools > System Settings > Universal Search Index Components`.... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-a-search-provider) |
| Integrating Smart Search | rock_documentation | If you've been using Rock for more than a day, you've used the Smart Search block at the top of the page. Universal Search can be configured to participate in Smart Search, and once it is, you'll find that it's your go-to search type. Once you have Universal Search up and indexing, you'll need to enable the Smart Search integration. You'll do this under `Admin Tools > System Settings > Search Services`. If it isn't... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/integrating-smart-search) |
| Customizing Results for Entities | rock_documentation | How results are returned from the search is important. Luckily, there are numerous ways to customize the results from the search. We cover all the options below. # Default Entity Results Each entity has a default result template that you can change. This is a great place to modify what you'd like to be returned across multiple search interfaces. You can edit these templates on a per-entity basis under Admin Tools >... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/customizing-results-for-entities) |
| Search | rock_documentation | SECTIONS [Searching for People](?Version=v19.0#searching-for-people) ### Searching for People Articles [Search by Name](/documentation/core-concepts/search/searching-for-people/search-by-name?Version=v19.0) [Search by Phone](/documentation/core-concepts/search/searching-for-people/search-by-phone?Version=v19.0) [Search by Other... | [source](https://community.rockrms.com/documentation/core-concepts/search) |
| Search by Name | rock_documentation | To find someone in the database, start by using the *Smart Search*tool found at the top of every page. This tool can be used to search several different types of data, but it defaults to searching for individuals by name. When searching by name, it's important to know some tricks to improve the quality of your search and to save time. Keep in mind that you don't need to type a person's full name to search. You can... | [source](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-name) |
| Search by Other Means | rock_documentation | Searching by *[People](/documentation/core-concepts/search/searching-for-people)* and by *[Name](/documentation/core-concepts/search/searching-for-people/search-by-name)* aren't the only ways to find people in Rock, below are some other ways to search. # Searching by Email Yep, you guessed it: Rock can search by email using the Smart Search tool, too. Partial searches are supported. We're sure you've got it by now,... | [source](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-other-means) |
| Searching for People | rock_documentation | [Search by Name](/documentation/core-concepts/search/searching-for-people/search-by-name?Version=v19.0) [Search by Phone](/documentation/core-concepts/search/searching-for-people/search-by-phone?Version=v19.0) [Search by Other Means](/documentation/core-concepts/search/searching-for-people/search-by-other-means?Version=v19.0) | [source](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people) |
| Installing Elasticsearch | rock_documentation | To install Elasticsearch you will need to follow the steps below. Detailed instructions for installing and running ElasticSearch can also be found on the [elastic.co](https://www.elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html) website. Note **Windows Service**If you want to install and run Elasticsearch as a service on Windows, follow the instructions found... | [source](https://community.rockrms.com/documentation/core-concepts/search/universal-search/installing-elasticsearch) |


## Source Lifecycle

- Official article records routed here: `70`
- Upstream check range: `2026-08-12T06:18:20+00:00` through `2026-08-12T06:18:53+00:00`
- Source-native typed articles: `6` of `70`
- Legacy source summaries retired: `6`; still active: `64`
- Migration status: `partial`

A recent source check or concept rebuild does not imply that every legacy summary has been replaced by reviewed source-native artifacts.

## Rebuild Dependencies

- Source records: `91`
- Approved claims: `1`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
