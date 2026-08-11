---
id: authored-system-admin-ops
title: System Administration And Operations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# System Administration And Operations

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [System Administration And Operations index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

System administration and operations in Rock RMS is the discipline of keeping the instance trustworthy, observable, performant, and recoverable. It spans scheduled jobs, job history, exception logs, cache behavior, search indexing, persisted Data Views, cleanup routines, security review, configuration hygiene, and release-readiness checks. In practice, an agent working in this area should treat Rock as a living operational system: inspect the live instance first, use official UI paths and model relationships to explain what is happening, and only then recommend changes.

The most important operating principle is that Rock administration is not one screen or one feature. It is a set of feedback loops:

- Jobs run in the background and leave history.
- History, exceptions, and status messages explain what jobs and user-facing requests did.
- Cache and indexes accelerate reads but can make stale state look current.
- Cleanup tasks reduce old data, but can also expose configuration assumptions.
- Data Views, reports, workflows, and security settings rely on the same entity and attribute model.
- Release notes and source code explain version-specific behavior when the UI does not.

RockU frames the foundation as entities, properties, attributes, defined types, campuses, note types, jobs, and automations in its [Core Concepts](https://community.rockrms.com/rocku/core-concepts) track. For operations, those are not abstract ideas. They are the objects an agent will inspect when answering questions like “Why did this automation fail?”, “Why is search stale?”, “Why is this cleanup job warning?”, or “Why can this person see this page?”

The agent-first approach is:

1. Identify the operational surface: service job, exception, cache key, search provider, persisted Data View, workflow, security rule, report, or release note.
2. Identify the authoritative record: Rock UI page, entity row, job history, exception log, configuration table, Model Map entry, official docs, release note, or source code.
3. Verify current state in the live instance before concluding.
4. Distinguish configuration state from runtime state.
5. Preserve evidence: exact job name, job ID, start/stop time, status, status message, exception type, affected entity, schedule, cache/index path, version, and source link.
6. Make the smallest safe change that directly addresses the verified problem.

The provided source pack is strongest for service job history, persisted Data View refresh behavior, Universal Search indexing, Lava cache usage, Data View APIs, Rock’s developer architecture, and release caveats. It is thinner for exception log internals and Rock Cleanup internals, so this guide names the live objects to inspect rather than inventing undocumented behavior.

## 2. Scope And Terminology

This guide covers Rock RMS operational administration. It is focused on:

- Service jobs and scheduling.
- Service job history.
- Diagnostics and exception investigation.
- Cache behavior, especially Lava cache and cache tags.
- Universal Search indexing.
- Persisted Data View refresh behavior.
- Cleanup and data integrity.
- Administrative configuration surfaces.
- Operational guardrails for agents.
- Developer and API landmarks that help explain runtime behavior.
- Release and version caveats that affect operations.

This guide does not replace the official Rock documentation, RockU, release notes, or source code. It is a synthesis intended for agents who need to work operationally inside a real Rock instance.

Key terms:

**Entity**  
A Rock data object. RockU presents “What is an Entity” as a core concept in the [Core Concepts](https://community.rockrms.com/rocku/core-concepts/what-is-an-entity) track. In operations, entities are the records agents inspect: `ServiceJob`, `ServiceJobHistory`, `DataView`, `Attribute`, `AttributeValue`, `Page`, `Block`, `Workflow`, `ExceptionLog`, and similar rows.

**Property**  
A database-backed field on an entity. The RockU [Properties and Attributes](https://community.rockrms.com/rocku/core-concepts/properties-and-attributes) topic distinguishes built-in properties from extensible attributes. For operations, properties are usually the safest basis for precise queries because they are part of the model.

**Attribute**  
A configurable extension point attached to an entity or other Rock object. RockU includes [Custom Attributes](https://community.rockrms.com/rocku/core-concepts/custom-attributes), and the Developer Codex lists attributes and service-layer patterns under [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards). Operationally, attributes can affect jobs, workflows, reports, Lava, blocks, Data Views, and global settings.

**Defined Type and Defined Value**  
A configurable list structure used throughout Rock. RockU includes [Defined Types](https://community.rockrms.com/rocku/core-concepts/defined-types), and the Developer Codex notes that core features using new defined types or values should have well-known GUID constants while still handling missing values defensively in [Defined Types & Defined Values](https://community.rockrms.com/developer/developer-codex/coding-standards/defined-types-defined-values).

**Service Job**  
A scheduled background routine. RockU includes a short [Jobs](https://community.rockrms.com/rocku/core-concepts/jobs) topic. In the source code, service job history is modeled as a scheduled job or routine history record in `ServiceJobHistory` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)).

**Service Job History**  
The execution log for service jobs. The Model Map identifies “Service Job History” as a Core model ([Model Map](https://community.rockrms.com/ModelMap)). The source shows that each history record belongs to a `ServiceJob` and stores job execution data such as job ID, worker, start/stop time, status, and status message ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)).

**Exception Log**  
The runtime error record surface. The source pack does not include a hydrated ExceptionLog model record, so agents should verify the live table/model fields in the target Rock instance before writing exact SQL or drawing conclusions from assumed columns.

**Cache**  
A memory-backed acceleration layer. The Lava cache command documentation describes wrapping Lava output in a cache block with a key and duration so later runs can reuse cached output ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)). RockU also has a [Cache Tags](https://community.rockrms.com/rocku/cms/cache-tags) CMS topic.

**Indexing**  
The process of sending entities or site content into a search provider. The official [Universal Search](https://community.rockrms.com/documentation/bookcontent/32) documentation covers provider configuration, entity enablement, scheduled re-indexing, site crawling, and security caveats.

**Persisted Data View**  
A Data View whose results are refreshed and stored for performance or schedule-based reuse. Source code for `UpdatePersistedDataviews` shows that Rock has a job that refreshes persisted Data Views based on interval or schedule settings ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)).

**Cleanup**  
Routine removal or correction of stale, orphaned, or excessive data. The source pack includes a release note about the Rock Cleanup job deleting `App_Data/Cache` in a scenario that affected Clear Cache behavior ([release notes](https://www.rockrms.com/releasenotes)). It does not include full Rock Cleanup internals, so live verification is required for specific cleanup actions.

## 3. System Administration And Operations Mental Model

Rock operations can be understood as five connected layers.

### Layer 1: Configuration

Use [System Configuration](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/other-essentials/system-configuration), [Jobs](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/jobs), and [Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search) to identify the owning configuration surface before diagnosing runtime or derived-state symptoms.

Configuration is what Rock has been told to do. This includes service job definitions, schedules, job attributes, Data View persisted settings, Universal Search provider settings, site indexing settings, block settings, workflow configuration, security rules, defined values, global attributes, and plugin settings.

Agents should inspect configuration before interpreting symptoms. A failed job may be configured with an impossible schedule, a too-short timeout, a missing attribute, an inactive provider, or a stale defined value. A search problem may be an indexing configuration problem rather than a search engine problem. A workflow issue may be a category permission problem, a block setting problem, or a security issue.

### Layer 2: Runtime Execution

Runtime execution is what actually happened. For jobs, this means job history records. For web requests, this means exception logs, server logs, request logs if available, and user-visible behavior. For Data Views, this means persisted refresh timestamps and whether the underlying query still produces expected rows. For cache and search, this means whether the returned data is current relative to the source of truth.

The `ServiceJobHistory` entity is the clearest source-packed example of this layer. Its model represents scheduled job history, has a required `ServiceJobId`, and belongs to a `ServiceJob` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)). Its service exposes query patterns by job ID and date range ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)).

### Layer 3: Derived State

Derived state is data produced from other data. Indexes, persisted Data Views, caches, reports, analytics tables, and workflow-generated values are derived state. Derived state can be correct, stale, incomplete, or over-broad.

The Universal Search documentation states that Rock uses configured search providers and has a scheduled re-index job for keeping entities in sync, with special handling for the Site entity and site crawling ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). The `UpdatePersistedDataviews` job source shows another derived-state pattern: refresh persisted Data Views when interval or schedule conditions say they are due ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)).

### Layer 4: Security And Authorization

Operational facts are not complete unless authorization is understood. Rock objects can be visible or executable to some users and not others. The Data Views v2 action controller checks authentication and authorization before reporting whether a Data View contains an entity ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)). The AI agent lookup-tools documentation demonstrates the pattern of loading cache-backed objects and then filtering by active state and authorization ([Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)).

An agent must avoid assuming that “the data exists” means “the current user can use it.” Verify both.

### Layer 5: Version Behavior

Rock behavior changes by version. The official release notes are a required source for operational conclusions. For example, Rock v19.1 includes a Core fix for Clear Cache when `App_Data/Cache` does not exist after the Rock Cleanup job has deleted it ([release notes](https://www.rockrms.com/releasenotes)). The same release notes include workflow fixes, including timeout behavior in the Obsidian Workflow List block when loading workflows assigned to groups with many members ([release notes](https://www.rockrms.com/releasenotes)). Agents should always identify the installed Rock version before applying a version-specific explanation.

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. Live Rock instance evidence.
2. Official Rock documentation and release notes.
3. Rock source code and generated model/API code.
4. Rock Model Map.
5. RockU training.
6. Developer Codex and developer documentation.
7. Community recipes and Q&A.
8. Third-party summaries.

Official documentation and source code should outweigh community recipes. Community recipes can suggest inspection patterns, but Rock’s recipe pages warn that contributed recipes are not reviewed or endorsed by the Rock core team and may have performance or security implications ([recipe disclaimer example](https://community.rockrms.com/recipes/522)). Treat recipes as examples, not authority.

Use the [Rock Core Release Notes](https://www.rockrms.com/releasenotes) when symptoms could be version-specific. Release notes are especially important for bugs involving cache, workflows, search, Obsidian blocks, and cleanup.

Use GitHub source snippets when the UI or docs are not specific enough. For example:

- `ServiceJobHistory` model shape: [ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)
- Service job history query and retention behavior: [ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)
- Scheduled Job History block behavior: [ScheduledJobHistoryList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs)
- Persisted Data View refresh job: [UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)
- Data View v2 action API security: [DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)

Use RockU for conceptual grounding, especially when explaining the entity/attribute/defined-type model to a non-developer operator ([Core Concepts](https://community.rockrms.com/rocku/core-concepts)).

When this guide says “inspect in the live instance,” it means the source pack does not provide enough authoritative detail to assert exact behavior. Inspect the actual Rock version, table schema, job attributes, block settings, or source code for that deployment.

## 5. Core Configuration And Data Model

Rock administration depends on a small set of recurring model patterns.

### Entities, Properties, And Attributes

RockU’s Core Concepts sequence establishes that Rock organizes data around entities, their properties, and configurable attributes ([Core Concepts](https://community.rockrms.com/rocku/core-concepts), [Properties and Attributes](https://community.rockrms.com/rocku/core-concepts/properties-and-attributes), [Custom Attributes](https://community.rockrms.com/rocku/core-concepts/custom-attributes)). Operationally:

- Properties are usually stable columns or model fields.
- Attributes are configurable values stored through Rock’s attribute system.
- Many operational features combine both.

Examples:

- `ServiceJobHistory.ServiceJobId` is a property.
- A service job’s configurable timeout or custom setting may be represented as an attribute.
- A Data View’s persistence interval is a property or configured field on the Data View model; verify exact column names in the live version.
- A block setting may be implemented as an attribute on a block type.

Agents should not assume an operational setting is a database column. First identify whether it is a property, attribute, defined value, block setting, global attribute, or plugin configuration.

### Defined Types And Defined Values

Defined Types are configurable lists. RockU covers [Defined Types](https://community.rockrms.com/rocku/core-concepts/defined-types), and the Developer Codex gives a developer-side warning: even when core features define well-known GUIDs for new defined types and values, consuming code should still handle missing values ([Defined Types & Defined Values](https://community.rockrms.com/developer/developer-codex/coding-standards/defined-types-defined-values)).

Operational implications:

- Do not assume a defined value exists just because documentation names it.
- Do not assume a value’s name is stable across customized instances.
- Prefer GUID or IdKey when a source or live system provides it.
- Verify active/inactive state.
- Verify category and order when values are used in UI selection.
- Verify attributes attached to defined values, because integrations and Lava often store operational details there.

The Lava API documentation shows a concrete use of Defined Types: Rock’s Lava webhook matching is configured through the “Lava Webhook” Defined Type, where request URL and HTTP verb determine the template selection ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). That is an operationally sensitive pattern because it can expose data if configured carelessly.

### Service Jobs

A service job is a scheduled routine. RockU includes [Jobs](https://community.rockrms.com/rocku/core-concepts/jobs), and the Universal Search documentation references Jobs Administration as the place to manage jobs such as the Universal Search Re-Index job ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

Common job configuration to inspect:

- Job name.
- Job type/class.
- Active/enabled state.
- Cron or schedule expression.
- Last run.
- Next run.
- Notification settings if configured.
- History count.
- Timeout-related attributes.
- Job-specific attributes.
- Worker/server context in multi-server environments.
- Current status and last status message.

The source pack confirms that job history records are tied to service jobs and that the Scheduled Job History block expects a `ScheduledJobId` page parameter ([ScheduledJobHistoryList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs)).

### Job History

`ServiceJobHistory` is the operational record of job execution. The source model describes it as a scheduled job/routine history record and maps it to the `ServiceJobHistory` table ([ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)). The generated client model shows fields exposed to clients such as `ServiceJobId`, `ServiceWorker`, `StartDateTime`, `Status`, `StatusMessage`, and `StopDateTime` ([client model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Client/CodeGenerated/ServiceJobHistory.cs)).

Operationally, history answers:

- Did the job run?
- Which service worker ran it?
- When did it start?
- Did it stop?
- What status did it report?
- What status message did it write?
- Did the same failure repeat?
- Did the failure begin after a release, configuration change, data import, or plugin install?
- Is the history truncated because of the job’s history count?

The service code includes `GetServiceJobHistory(serviceJobId, startDateTime, stopDateTime)`, which filters by job, start time, and stop time and orders by job and descending start time ([ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)). It also includes retention logic that deletes history beyond a configured maximum, defaulting to 500 when the job’s history count is not positive ([ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)).

### Data Views

Data Views are reporting and segmentation definitions. Source records show operational use in reporting search, communication conversion goals, persisted refresh jobs, and v2 APIs.

The Data View Search block searches Data Views by name and links to the reporting Data View page using a configurable URL format ([DataViewSearch.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs)). Communication flow view models show that “Entered Data View” can be a conversion goal setting ([CommunicationFlowDetailEnteredDataViewSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowDetail/CommunicationFlowDetailEnteredDataViewSettingsBag.cs)).

The Data Views v2 API includes secured endpoints for reading Data Views and action endpoints for checking contents ([DataViewsController](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DataViewsController.CodeGenerated.cs), [DataViewsActionsController](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)). Operations agents should treat Data Views as both report definitions and operational dependencies.

### Universal Search Components

Universal Search has provider configuration, entity enablement, re-index jobs, and site crawling. The official documentation says provider settings live under `Admin Tools > System Settings > Universal Search Index Components`, and the Universal Search Re-Index job can be adjusted under `Admin Tools > System Settings > Jobs Administration > Universal Search Re-Index` ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

Operationally, Universal Search depends on:

- Provider enabled and configured.
- Entity enabled for indexing.
- Entity-specific settings.
- Bulk load or scheduled re-index.
- Site indexing settings for site content.
- Site crawl job for site entity content.
- Search security limitations.

The documentation includes a specific warning for Person attributes: be careful indexing person attributes because attribute security is not available in Universal Search ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). This is a major operational guardrail.

### Cache

Rock exposes cache at multiple levels. The source pack provides two clear surfaces:

- Lava cache command: cache a block of Lava output by key and duration ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)).
- CMS cache tags: RockU topic for CMS cache tags ([Cache Tags](https://community.rockrms.com/rocku/cms/cache-tags)).

The Lava cache command supports parameters named in the docs headings: key, duration, twopass, tags, and maxcachesize ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)). Agents should verify exact syntax and behavior against the installed Rock version and the official doc before modifying production Lava.

### Security Rules

Security is both an operational object and a cross-cutting constraint. The source pack includes a community recipe that builds a page/block security dashboard and highlights useful categories such as role-based permissions, user-specific rules, orphaned rules, and duplicate rules ([Security Management recipe](https://community.rockrms.com/recipes/522)). Because recipes are not core-reviewed, use this as inspiration, not proof.

For authoritative behavior, use Rock UI security dialogs, the live database, the relevant model/service code, and official security documentation for the installed version.

## 6. Primary Entities And Relationships

### ServiceJob And ServiceJobHistory

The source pack provides the strongest data model evidence for job history.

`ServiceJobHistory`:

- Is a Core domain model.
- Maps to table `ServiceJobHistory`.
- Represents scheduled job/routine history.
- Has a required `ServiceJobId`.
- Has a navigation property back to `ServiceJob`.
- Uses a required relationship where a service job has many history records.
- Has generated REST read-only behavior in the model annotation.
- Has security parent authority delegated to the parent `ServiceJob` in logic code.

Sources: [ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs), [ServiceJobHistory.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.Logic.cs), [ServiceJobHistoryService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/ServiceJobHistoryService.CodeGenerated.cs).

The practical relationship is:

```text
ServiceJob 1 -> many ServiceJobHistory
ServiceJobHistory.ServiceJobId -> ServiceJob.Id
ServiceJobHistory.ParentAuthority -> ServiceJob
```

For agents, this means job history should be interpreted through the job definition. If a history record is inaccessible, missing, or filtered, inspect the service job’s security and history retention.

### ServiceJobHistory Fields To Inspect

From the source snippets and generated client model, inspect:

- `Id`
- `ServiceJobId`
- `ServiceWorker`
- `StartDateTime`
- `StopDateTime`
- `Status`
- `StatusMessage`
- Audit fields such as modified values if relevant
- `ForeignId`, `ForeignGuid`, `ForeignKey` only when integration mapping is suspected

Source: [client model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Client/CodeGenerated/ServiceJobHistory.cs).

When troubleshooting, also inspect the parent `ServiceJob` fields in the live instance:

- `Name`
- `Class`
- `CronExpression` or schedule field, depending on version
- Active state
- Last run / next run
- History count
- Job-specific attributes
- Notification settings
- Any command timeout attribute

The source pack does not include the `ServiceJob` model, so verify exact column names in the live schema or source for the installed version.

### DataView And Persisted Data View State

The `UpdatePersistedDataviews` job source shows that persisted Data Views can be refreshed based on either interval minutes or a persisted schedule. The job queries Data Views with `PersistedScheduleIntervalMinutes`, checks `PersistedLastRefreshDateTime`, and also considers `PersistedScheduleId` with the related schedule ([UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)).

Inspect these live fields or equivalent version-specific fields:

- Data View ID, name, category.
- Entity type.
- Persisted enabled state.
- Persisted refresh interval.
- Persisted schedule.
- Last refresh date/time.
- Last refresh duration or status if present.
- Filter tree.
- Transform or security-related settings.
- Dependent reports, workflows, communication flows, blocks, and jobs.

The source pack confirms Data Views are also used in APIs and communication flow conversion goals ([DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs), [CommunicationFlowDetailEnteredDataViewSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowDetail/CommunicationFlowDetailEnteredDataViewSettingsBag.cs)).

### ExceptionLog

Rock's official [View the Exception List](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list) guidance defines the administrator surface. Public source defines `ExceptionLog` as a read-only REST entity with hierarchical parent/inner-exception records and fields for status, type, description, source, stack trace, page URL, request context, site, and page ([ExceptionLog.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ExceptionLog/ExceptionLog.cs)).

In a live Rock instance, inspect:

- `ExceptionLog` table schema.
- Exception detail page.
- Exception date/time.
- Exception type.
- Message.
- Stack trace.
- Page, site, route, or URL context if present.
- Person alias/user context if present.
- Has inner exception / parent exception fields if present.
- Related entity references if present.
- Server or application context if present.
- Count and recurrence pattern.

The service supports outermost/innermost and description-prefix filtering, and falls back to `App_Data/Logs/RockExceptions.csv` if database logging fails ([ExceptionLogService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ExceptionLog/ExceptionLogService.cs)). Use the exact live schema and retention state before writing queries or concluding that a missing database row means no exception occurred.

### Attribute And AttributeValue

Attributes are operationally important because jobs, blocks, workflows, defined values, people, groups, campuses, and other entities may carry custom settings. RockU covers attributes conceptually ([Custom Attributes](https://community.rockrms.com/rocku/core-concepts/custom-attributes)). The Developer Codex source list includes service-layer and data architecture topics under [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards).

Operational checks:

- Is the attribute attached to the expected entity type?
- Is the attribute active?
- Is it required?
- Does it have a default value?
- Does the value exist for the specific entity?
- Is the value malformed for the configured field type?
- Is the attribute category correct?
- Is the attribute secured?
- Is a stale AttributeValue referencing a missing entity?

A Rock v19.1 release note fixed an issue where multiple attribute editing blocks showed Global Attribute categories instead of categories for the actual entity type ([release notes](https://www.rockrms.com/releasenotes)). That is a reminder that attribute UI behavior can be version-specific.

### Page, Block, And Security Relationships

The source pack’s security recipe is community-provided, but it correctly points agents toward page and block security rules as operational objects worth auditing ([Security Management recipe](https://community.rockrms.com/recipes/522)). In live work, inspect:

- Page security.
- Block security.
- Inherited security.
- Explicit allow/deny rules.
- Role/group-based permissions.
- User-specific permissions.
- Orphaned references to deleted pages, blocks, groups, or people.
- Duplicate or conflicting rules.
- Whether the current person is affected by authorization caching.

Community examples should not be copied directly into production without review because Rock recipe pages explicitly warn that recipes may affect performance or security ([recipe disclaimer](https://community.rockrms.com/recipes/522)).

## 7. Common System Administration And Operations Workflows

### Workflow: Investigate A Failed Service Job

1. Identify the exact job.
2. Open Jobs Administration in the live Rock instance.
3. Record job name, ID, active state, schedule, last run, next run, job type, and attributes.
4. Open Scheduled Job History for that job.
5. Review recent history records.
6. Compare failing and successful runs.
7. Capture `StartDateTime`, `StopDateTime`, `Status`, `StatusMessage`, and `ServiceWorker`.
8. Check Exception Log around the same time window.
9. Inspect downstream objects referenced in the message.
10. Check release notes for known bugs in the installed version.
11. If the job uses Data Views, workflows, communications, finance, search, or cleanup, inspect those dependent entities.
12. Make one change at a time and rerun only if safe.

The source confirms that the Scheduled Job History block uses `ScheduledJobId` to load history for a service job and does not expose add/delete operations in the list block ([ScheduledJobHistoryList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs)).

### Workflow: Confirm Whether A Job Actually Ran

Use job history, not only the job list. The job list can show configuration and summary state; history shows execution records. The service layer supports filtering history by job ID and date range ([ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)).

Inspect:

- Any history record in the expected window.
- Whether `StartDateTime` exists without `StopDateTime`.
- Whether `Status` indicates success, warning, failure, or another state in the installed version.
- Whether the `StatusMessage` reports a partial success.
- Whether the same worker handled prior successful runs.
- Whether history retention might have deleted older evidence.

If no history exists, verify:

- Job active state.
- Schedule.
- Rock job runner/service state.
- Server time zone and current time.
- Whether another app server owns job execution.
- Whether the job is disabled by configuration.
- Whether the job definition/class is missing after a plugin or deployment change.

### Workflow: Investigate A Warning Job

A warning status is not always a failure. Treat it as “completed with something to inspect.”

Steps:

1. Read the exact status message.
2. Check whether the warning count is stable, increasing, or decreasing.
3. Look for matching exceptions in the same time window.
4. Identify whether the warning is about skipped records, stale data, configuration gaps, timeouts, or cleanup thresholds.
5. Inspect the affected records directly.
6. Check whether the job has a threshold setting or timeout attribute.
7. Check release notes for known warning behavior.

For cleanup jobs specifically, do not assume the warning means only “too much old data.” It may indicate a missing folder, stale configuration, orphaned records, or a permission/path issue. The v19.1 release note about Clear Cache and `App_Data/Cache` shows that cleanup can remove expected file-system state, and later operations need to handle that absence ([release notes](https://www.rockrms.com/releasenotes)).

### Workflow: Investigate Stale Search Results

1. Identify the search provider and entity.
2. Open `Admin Tools > System Settings > Universal Search Index Components`.
3. Confirm the provider is enabled and configured.
4. Confirm the entity is enabled for Universal Search.
5. Check whether the entity supports indexing in the installed version.
6. Check Universal Search Control Panel for bulk load or status.
7. Check the Universal Search Re-Index job history.
8. If the Site entity is involved, verify site indexing settings, crawling starting location, and the site crawl job.
9. If person attributes are indexed, review privacy/security implications.
10. Run a targeted re-index only if the operational impact is acceptable.

The official docs state that a nightly re-index job keeps most entities in sync and that Site indexing is different and requires site-level setup plus an `Index Rock Site` job ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

### Workflow: Investigate Stale Persisted Data View Results

1. Identify the Data View by ID and name.
2. Open the Data View and inspect persistence settings.
3. Record entity type, filter tree, category, and schedule/interval.
4. Check `PersistedLastRefreshDateTime` or equivalent live field.
5. Check the `Update Persisted DataViews` job history.
6. Review job status messages for failures or skipped views.
7. Evaluate whether the Data View query itself still runs.
8. Compare live query results to persisted results.
9. Check timeout settings, especially SQL command timeout on the job.
10. If a dependent report or workflow is wrong, verify whether it uses persisted results.

The source shows `UpdatePersistedDataviews` has a `SQL Command Timeout` job attribute defaulting to 300 seconds if not configured, and it gathers expired persisted Data Views based on interval or schedule logic ([UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)).

### Workflow: Investigate A Cache Suspect

1. Identify the cache surface: Lava cache, CMS cache tag, object cache, file cache, browser cache, CDN, or search index.
2. Determine the source of truth.
3. Compare source data to rendered output.
4. Inspect cache key, duration, tags, and max cache size if Lava cache is used.
5. Check whether the output varies by current person, campus, security role, query string, or route.
6. If the output varies by user or request, ensure the cache key includes those dimensions.
7. Clear the narrowest relevant cache.
8. Verify the issue recurs or resolves.
9. Record what changed.

The Lava cache documentation explains that cached Lava output is stored in server memory and should not be used carelessly for numerous large results ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)). That matters operationally because over-broad caching can produce stale or cross-context output.

### Workflow: Investigate An Exception Spike

Start with [View the Exception List](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list) and [Exception Handling](https://community.rockrms.com/developer/303---blast-off/exception-handling). Group outermost records separately from inner exceptions and treat request fields, form values, query strings, cookies, and server variables as sensitive operational data.

1. Identify the spike window.
2. Group exceptions by type, message, page/route, and stack trace.
3. Compare first occurrence to deployments, plugin installs, content edits, job runs, imports, or Rock updates.
4. Separate job exceptions from request exceptions.
5. For request exceptions, identify page, block, route, Lava, workflow, or API endpoint.
6. For job exceptions, correlate with `ServiceJobHistory`.
7. For workflow exceptions, inspect the workflow type, activity/action, and entity references.
8. For database exceptions, inspect schema assumptions and recent migrations.
9. For authorization exceptions, inspect current person, role, page/block security, and API permissions.
10. Check release notes for known bugs.

Avoid deleting exception logs before extracting recurrence evidence.

### Workflow: Review Operational Health After Upgrade

1. Confirm installed Rock version and target release notes.
2. Review heads-up notes, Core, Workflow, Reporting, CMS, Security, and Lava sections.
3. Run or inspect job history for critical jobs.
4. Check exception counts before and after upgrade.
5. Verify search provider and re-index jobs.
6. Verify persisted Data Views.
7. Verify cache clear behavior.
8. Verify workflow entry/list behavior if workflows are used heavily.
9. Verify attribute editing screens if admins manage attributes.
10. Review plugin compatibility.

For example, v19.1 includes fixes for cache clearing when `App_Data/Cache` is missing, attribute category dropdown behavior, and workflow-related issues ([release notes](https://www.rockrms.com/releasenotes)). Those are operationally relevant checks after upgrading into or beyond that version.

## 8. Jobs And Scheduling Deep Dive

### What Jobs Are For

Jobs are Rock’s background execution mechanism. They handle recurring work that should not depend on a person opening a page: cleanup, indexing, persisted Data View refresh, workflow launching, communication preparation, integrations, and other scheduled maintenance.

RockU includes Jobs as a Core Concepts topic ([Jobs](https://community.rockrms.com/rocku/core-concepts/jobs)). Official Universal Search documentation also treats jobs as operational infrastructure by directing administrators to Jobs Administration for the Universal Search Re-Index job ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

### Job Configuration Fields To Inspect

The exact field names vary by version, but operational inspection should capture:

- Service job ID.
- Name.
- Description.
- Job type/class.
- Active/enabled flag.
- Schedule or cron expression.
- Last successful run.
- Last run status.
- Next run.
- History count.
- Notification emails or alert settings.
- Job-specific attributes.
- SQL command timeout, API key, endpoint URL, batch size, retention days, or similar settings when present.
- Server/worker assignment if applicable.

The source pack confirms that `ServiceJobHistoryService.DeleteMoreThanMax` reads `HistoryCount` from `ServiceJob` and defaults to 500 when the value is not positive ([ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)). That means history retention is operationally significant: old evidence may be gone even when the job has been running for years.

### Job History Interpretation

Each history record should be read as a single execution attempt. Inspect:

- Did it start?
- Did it stop?
- Did duration change from normal?
- Did status change from success to warning or failure?
- Did the message include counts?
- Did the message include entity IDs, Data View IDs, file paths, URLs, or exception text?
- Did the service worker change?
- Was there a deployment, recycle, or server restart during execution?

`ServiceJobHistoryService.GetServiceJobHistory` returns history filtered by `ServiceJobId`, `StartDateTime`, and `StopDateTime`, ordered by service job and descending start time ([ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)). That ordering supports the normal UI pattern of reviewing most recent runs first.

### Job History UI Behavior

The Obsidian Scheduled Job History block:

- Displays service job histories.
- Uses `ScheduledJobId` as the page parameter.
- Accepts either a hashed ID or integer ID.
- Does not enable add/delete in the list initialization.
- Returns an empty queryable list when no valid job ID is present.

Source: [ScheduledJobHistoryList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs), [ScheduledJobHistoryListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs).

Agent implication: if the history page is empty, first verify the route/page parameter. An empty page may mean the job ID is missing or invalid, not that the job has no history.

### Job History Security

`ServiceJobHistory.ParentAuthority` resolves to the parent `ServiceJob` when available ([ServiceJobHistory.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.Logic.cs)). This matters because access to history can inherit from job security.

Agent implication: when a user cannot view job history, inspect the parent service job’s security rather than only the history row.

### Job Retention

The source shows `DeleteMoreThanMax` behavior:

- It loops service jobs.
- It reads each service job’s `HistoryCount`.
- If history count is not positive, it uses 500.
- It deletes history beyond that count ordered by descending start time.

Source: [ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs).

Agent implication: do not promise that historical evidence exists beyond configured retention. If a question depends on old job history, inspect current retention and backup/log availability.

### Update Persisted DataViews Job

The `UpdatePersistedDataviews` job is a core operational job. Its source states that it ensures persisted Data Views are updated based on their schedule interval ([UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)).

Known source-backed behavior:

- Display name: `Update Persisted DataViews`.
- It has a `SQL Command Timeout` integer field.
- It defaults command timeout to 300 seconds when the attribute is not set.
- It finds Data Views with `PersistedScheduleIntervalMinutes` due for refresh.
- It also handles Data Views with `PersistedScheduleId`.
- It tracks updated count, failed Data Views, and exceptions.

Operational checks:

- Confirm the job is active.
- Confirm it runs frequently enough for the shortest persisted interval.
- Confirm the SQL timeout is appropriate for the largest persisted views.
- Identify failed Data Views by name or ID from the status message.
- Inspect whether Data Views are due but not refreshing.
- Inspect whether heavy Data Views should be optimized rather than simply increasing timeout.

### Universal Search Re-Index Job

The Universal Search docs state that a system job re-indexes every night and can be adjusted under `Admin Tools > System Settings > Jobs Administration > Universal Search Re-Index` ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

Operational checks:

- Job active.
- Last run success.
- Duration trend.
- Provider connectivity.
- Entity enablement.
- Index size and growth.
- Bulk load status.
- Exceptions near run time.

### Index Rock Site Job

The Universal Search docs state that Site indexing requires setting up a new Rock job of type `Index Rock Site`, with site Advanced Settings configured to allow indexing and a crawling starting location set ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

Operational checks:

- Site indexing enabled.
- Starting URL reachable internally.
- Crawl does not require an unauthenticated-inaccessible page unless intended.
- Crawl schedule appropriate.
- Job history clean.
- Site content exclusions understood.
- Search result exposure reviewed.

### Launch Workflow Job

The community podcast import recipe suggests using a `Launch Workflow` system job to run a workflow weekly after a podcast is uploaded ([recipe](https://community.rockrms.com/recipes/503)). Because this is a community recipe, treat it as an example pattern, not an official recommendation.

Operationally, Launch Workflow jobs should be inspected for:

- Workflow type.
- Entity or attribute inputs.
- Schedule.
- Idempotency.
- Failure behavior.
- Duplicate run prevention.
- Security context.
- External API credentials.
- Logging and notification.

## 9. Diagnostics And Exceptions Deep Dive

### Diagnostic Mindset

Diagnostics should begin with evidence, not guesses. The minimum evidence set is:

- Time window.
- User or system actor.
- URL/page/job/API endpoint.
- Exception type/message.
- Stack trace if available.
- Related job history.
- Related release or deployment.
- Reproduction path.
- Scope: one user, one campus, one page, all users, background-only, or external-only.

The source pack does not provide a hydrated ExceptionLog model. Therefore, agents must verify exact fields in the live instance before writing SQL or claiming field semantics.

### Exception Investigation Branches

#### Request-Time Exception

Inspect:

- Page.
- Route.
- Block.
- Lava template or shortcode.
- Current person.
- Security.
- Query string.
- Post body if safe and available.
- Recent content edits.
- Recent theme/plugin changes.

If Lava is involved, check whether Lava commands are enabled, whether a cache block is returning stale content, and whether the template exposes sensitive data. The Lava API docs warn that Lava webhooks do not provide security by themselves and that exposed data must be handled carefully ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).

#### Job-Time Exception

Inspect:

- Service job history for same timestamp.
- Job status message.
- Job attributes.
- Related records.
- Job schedule.
- Last successful run.
- ExceptionLog rows in the same time window.
- Whether retention has deleted earlier history.

Use `ServiceJobHistory` fields as the job execution source of truth ([ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)).

#### DataView Exception

Inspect:

- Data View entity type.
- Filter tree.
- Any nested Data Views.
- Persisted settings.
- Last refresh.
- Timeout.
- SQL generated or SQL-backed filter if available.
- Security and authorization if accessed through API.

The Data Views API action controller checks whether the current person can view a Data View unless the request has unrestricted read authorization ([DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)).

#### Search Exception

Inspect:

- Provider component.
- Provider settings.
- Universal Search Re-Index job.
- Entity settings.
- Site indexing settings.
- Search service availability.
- Version-specific search release notes.
- Person attribute indexing security risk.

Official source: [Universal Search](https://community.rockrms.com/documentation/bookcontent/32).

#### Cache Exception

Inspect:

- Cache clear action.
- `App_Data/Cache` directory existence if file cache is involved.
- File type cache settings.
- Rock version.
- Recent cleanup run.
- Exception message.

Rock v19.1 fixed a Clear Cache error when the Rock Cleanup job had deleted `App_Data/Cache` and no file types recreated it ([release notes](https://www.rockrms.com/releasenotes)). If the instance is below that fix, verify whether the symptom matches before recommending upgrade or workaround.

### Diagnostic Evidence To Capture

For every diagnostic task, preserve:

- Rock version.
- Environment.
- Exact page URL or route.
- Entity IDs and GUIDs.
- Job ID and name.
- History record ID.
- ExceptionLog ID.
- Timestamp with time zone.
- Current person or service account.
- Before/after state.
- Relevant source link.
- Whether live verification was read-only or involved a change.

## 10. Cache And Indexing Deep Dive

### Lava Cache Command

The Lava cache command stores rendered Lava output in Rock memory cache for a configured duration. The docs describe a pattern where a cache block uses a key and duration so later runs avoid repeating the underlying query ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)).

Operationally important parameters listed in the docs include:

- `key`
- `duration`
- `twopass`
- `tags`
- `maxcachesize`

Source: [Cache command docs](https://community.rockrms.com/lava/commands/cache-commands).

Use Lava cache when:

- Output is expensive to compute.
- Output is safe to share across all requests represented by the cache key.
- Staleness for the duration is acceptable.
- Memory impact is bounded.
- Invalidation is understood.

Avoid or redesign Lava cache when:

- Output includes current-person-sensitive data.
- Output depends on authorization.
- Output depends on campus, query string, date, segment, role, or request context not represented in the key.
- Output is very large.
- Output is updated frequently.
- Operators cannot safely invalidate it.

### Cache Keys

The [Lava Cache command](https://community.rockrms.com/lava/commands/cache-commands) defines fragment caching, while [Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags) defines grouped invalidation; neither source can prove that a proposed key contains every live request dimension.

A cache key must uniquely represent every dimension that changes the rendered output. If output differs by campus, include campus. If output differs by person, include person or do not cache. If output differs by route, include route. If output differs by query string, include the relevant query value.

Bad operational cache key:

```liquid
{% cache key:'group-list' duration:'3600' %}
```

Better pattern when campus matters:

```liquid
{% cache key:'group-list-campus-{{ Campus.Id }}' duration:'3600' %}
```

Verify exact Lava syntax and variable names in the live template before changing production code.

### Cache Tags

RockU includes [Cache Tags](https://community.rockrms.com/rocku/cms/cache-tags) as a CMS topic. In an operational guide, treat cache tags as a grouping/invalidation aid. Use them when several cached fragments should be cleared together. Before relying on tag invalidation, verify behavior in the installed version and inspect where the tag is assigned.

### Cache Clearing

Cache clearing can fix stale derived state, but it can also mask root cause. Before clearing:

- Identify the affected cache.
- Capture current wrong output.
- Capture source-of-truth data.
- Identify cache key/tag if possible.
- Clear the narrowest scope.
- Verify output.
- Watch exceptions.

The v19.1 release note about Clear Cache handling a missing `App_Data/Cache` folder is a specific caveat: cleanup and cache operations can interact through the file system ([release notes](https://www.rockrms.com/releasenotes)).

### Universal Search Provider Setup

The official Universal Search docs say provider components are configured under `Admin Tools > System Settings > Universal Search Index Components` ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). The docs discuss Lucene and Elasticsearch provider configuration and version history, including updates for Elasticsearch 8 in Rock 14 documentation notes.

Operational checks:

- Which provider is enabled?
- Are connection settings valid?
- Is the provider reachable from the Rock server?
- Is the index path or endpoint correct?
- Does the provider version match Rock’s supported configuration?
- Are credentials/secrets valid?
- Has a bulk load been run after initial enablement?

### Entity Indexing

The Universal Search docs describe enabling entities for indexing and keeping them in sync ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). For each entity:

- Verify indexing is enabled.
- Verify attributes selected for indexing.
- Verify security exposure.
- Run bulk load when immediate availability is required.
- Confirm scheduled re-index job health.

Person attribute indexing is sensitive because the docs warn that attribute security is not available in Universal Search ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). Do not index sensitive person attributes without explicit review.

### Site Indexing

The Site entity is special. The docs state that the Universal Search Re-Index job keeps all entities except Site indexed, and that Site requires enabling each site, adding a crawling starting location, and setting up an `Index Rock Site` job ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

Operational checks:

- Site advanced setting allows indexing.
- Crawling starting location is correct.
- Crawl job exists.
- Crawl job history is successful.
- Public/private content boundaries are understood.
- Canonical URLs and redirects do not trap the crawler.
- The crawl schedule matches content update frequency.

## 11. Cleanup And Data Integrity Deep Dive

### Cleanup As Operational Risk Management

Cleanup is not just deletion. It is risk management for old records, excessive history, orphaned values, stale derived state, and configuration drift. Agents should treat cleanup work as potentially destructive and evidence-driven.

RockU's Data Integrity lessons are useful training context for this operational posture: they frame data integrity as ongoing review of record correctness, duplicates, stale values, and cleanup targets before reports, workflows, and people operations can be trusted ([Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity), [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1)).

Before cleanup:

- Identify the exact cleanup target.
- Count affected records.
- Identify references and dependencies.
- Confirm retention policy.
- Confirm backups.
- Prefer read-only simulation.
- Run a small batch first when live writes are authorized.
- Verify after state.

### Service Job History Cleanup

The source-backed cleanup behavior in this pack is job history retention. `ServiceJobHistoryService.DeleteMoreThanMax` deletes history beyond each job’s configured history count, defaulting to 500 if the value is not positive ([ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)).

Operational implications:

- If you need longer job audit history, inspect and adjust history count before evidence is lost.
- If the database is bloated by job history, quantify by job before deleting.
- Preserve recent failure windows before reducing retention.
- Do not delete history during an active incident.

### Rock Cleanup And Cache Folder Caveat

The v19.1 release note says the Rock Cleanup job can delete `App_Data/Cache`; previously, Clear Cache could throw `DirectoryNotFoundException` if that folder did not exist and no file types recreated it. The fix checks for directory existence before enumerating/deleting contents ([release notes](https://www.rockrms.com/releasenotes)).

Operational interpretation:

- Cleanup can remove file-system folders used by later operations.
- Cache clear failures may be version bugs rather than permission issues.
- If the instance is older than the fix, inspect whether `App_Data/Cache` exists.
- If no file types are configured to cache to server, folder recreation may not happen automatically.
- Do not create broad cleanup conclusions from this one release note; verify the live Rock Cleanup job configuration and source for the installed version.

### Attribute Data Integrity

Attributes are high-risk for cleanup because they can be attached broadly and referenced by Lava, reports, workflows, integrations, and blocks.

Inspect:

- Attribute entity type.
- Attribute key and GUID.
- Category.
- Field type.
- Required/default behavior.
- Attribute values with missing entity references.
- Attribute values for inactive/deleted entities.
- Values incompatible with field type.
- Values containing old IDs or external references.
- Security settings.

Rock v19.1 included a fix for multiple attribute editing blocks showing incorrect categories ([release notes](https://www.rockrms.com/releasenotes)). When diagnosing attribute category anomalies, check version first.

### Security Data Integrity

The community security recipe highlights useful audit categories: page/block security, user-specific versus role-based rules, orphaned rules, duplicate rules, and rules for people who have left ([Security Management recipe](https://community.rockrms.com/recipes/522)). Because it is community content, use it as a checklist, not an implementation authority.

Live checks:

- Orphaned auth rules.
- Duplicate auth rules.
- Explicit user grants.
- Explicit user denies.
- Role/group grants to inactive groups.
- Security on high-risk pages.
- Security on workflow forms.
- Security on finance, person data, API, and reporting surfaces.

### Data View Integrity

A Data View can become operationally dangerous when it is stale, slow, over-broad, incorrectly secured, or used as a dependency without documentation.

Inspect:

- Category ownership.
- Entity type.
- Filter logic.
- Nested Data Views.
- Persistence settings.
- Dependent reports.
- Dependent communication flows.
- Workflow usage.
- API usage.
- Security rules.
- Last refresh.

The Data View API source shows that Data View contents can be exposed through secured action endpoints if authorized ([DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)). That makes Data View security and content scope operational concerns.

### Integration And Recipe Integrity

The podcast recipe demonstrates a common integration pattern: external API data imported into Defined Values, launched by a workflow/job, then used by content channel attributes ([recipe](https://community.rockrms.com/recipes/503)). This is useful as a pattern but requires review.

Operational checks for similar integrations:

- External endpoint and credentials.
- Workflow idempotency.
- Defined Type and Defined Value structure.
- Content channel attribute mapping.
- Error handling.
- Job schedule.
- Rate limits.
- Secret storage.
- Stale values.
- Manual override path.

## 12. Related Rock Areas: Security, Workflows, Data Views, Reports, Cache, Jobs, Release Notes

### Security

Security affects every operations task. For agents:

- Verify current person permissions.
- Verify page/block security.
- Verify entity security.
- Verify API endpoint security.
- Verify Data View authorization.
- Verify indexed attribute exposure.
- Verify Lava/API exposure.

The Data View action controller explicitly checks authentication and authorization for contains/content-style operations ([DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)). The Universal Search docs warn that Person attribute security is not available in Universal Search ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)).

### Workflows

Workflows interact with operations through jobs, forms, Lava, Data Views, categories, and security. Release notes can be especially important. Rock v19.1 includes workflow fixes, including a timeout issue in the Obsidian Workflow List block for workflows assigned to groups with many members and a Campus selection requirement fix in a Person Entry form scenario ([release notes](https://www.rockrms.com/releasenotes)).

Operational checks:

- Workflow type active state.
- Category permissions.
- Form Builder permissions.
- Activity/action failure.
- Entity context.
- Assigned person/group.
- Trigger.
- Launch job.
- Lava commands.
- Exception log correlation.

### Data Views

Data Views power reports, communication goals, APIs, and persisted datasets. Source records show Data View search, v2 API endpoints, communication conversion settings, and persisted refresh jobs ([DataViewSearch.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs), [DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs), [UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)).

### Reports

Reports are downstream consumers. When a report is wrong:

- Inspect the Data View.
- Inspect report fields.
- Inspect security.
- Inspect persisted state.
- Inspect cache.
- Inspect version-specific reporting release notes.

The source pack does not provide report model details, so verify live schema and configuration.

### Cache

Cache affects CMS, Lava, object lookups, and file-based behavior. Use the Lava cache docs for template-level caching ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)) and RockU cache tags for CMS cache tagging concepts ([Cache Tags](https://community.rockrms.com/rocku/cms/cache-tags)).

### Jobs

Jobs are the operational backbone. Use job history as runtime evidence and source code when behavior is unclear; `ServiceJobHistory` stores execution evidence such as service job, worker, start/stop time, status, and status message ([ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)).

### Release Notes

Release notes are required for version-specific operations. The source pack’s hydrated release note record includes v19.1 and v18.3 headings and examples of Core and Workflow fixes ([release notes](https://www.rockrms.com/releasenotes)). Always verify the installed version.

## 13. Administration And Operational Guardrails

### Read Before Write

Before changing anything:

- Read live configuration.
- Read recent history.
- Read exceptions.
- Read source/release notes if behavior is unclear.
- Count affected records.
- Identify rollback path.

### Do Not Treat Derived State As Source Of Truth

Caches, indexes, persisted Data Views, reports, and dashboards are derived. If derived state disagrees with source state:

- Confirm source state.
- Confirm refresh mechanism.
- Confirm schedule.
- Confirm security.
- Confirm cache/index invalidation.

### Avoid Broad Cache Clears During Incidents

A broad cache clear may cause load spikes or hide evidence. Prefer targeted invalidation when possible, and use cache keys, duration, and cache tags intentionally when the issue is Lava or CMS output rather than global state ([Cache command docs](https://community.rockrms.com/lava/commands/cache-commands), [Cache Tags](https://community.rockrms.com/rocku/cms/cache-tags)).

### Do Not Index Sensitive Attributes Casually

Universal Search’s Person attribute warning is explicit: attribute security is not available in Universal Search ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). Review privacy impact before indexing person attributes.

### Treat Lava APIs As High Risk

The Lava API documentation warns that Lava webhooks do not provide security by themselves ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). Agents should inspect exposed templates, enabled commands, route matching, and returned data before approving a Lava API.

### Validate Community Recipes

Rock recipe pages warn that contributed recipes are not core-reviewed and may affect performance or security ([recipe disclaimer](https://community.rockrms.com/recipes/522)). Before using a recipe:

- Read every SQL/Lava/workflow step.
- Test in non-production.
- Review security.
- Review performance.
- Review rollback.
- Verify version compatibility.

### Keep Version Context Visible

Every operational note should include Rock version when behavior may depend on release. Release notes should be linked inline, especially for Core, Workflow, cache, cleanup, and indexing behavior that may change between releases ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Prefer Entity IDs And GUIDs Over Names

Names can change. IDs can differ across environments. GUIDs are often best for source-controlled references, but live operations often need both.

Record:

- Name for humans.
- ID for live instance.
- GUID for portability when available.
- URL for navigation.
- Source link for authority.

## 14. Developer, API, Lava, And Source-Code Landmarks

### Developer Codex

The [Developer Codex](https://community.rockrms.com/developer/developer-codex) and [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards) are useful when operational behavior depends on Rock architecture. The source pack headings include service layers, data service layer, security patterns, Rock architecture, migrations, logging, API patterns, and performance.

Use it when:

- A behavior is caused by service-layer rules.
- A plugin bypasses expected patterns.
- A migration changed schema.
- A code path needs a source-backed explanation.
- Security behavior depends on Rock architecture.

### ServiceJobHistory Source

Use these landmarks for jobs:

- Model: [ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)
- Logic/security parent: [ServiceJobHistory.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.Logic.cs)
- Service query/retention: [ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)
- Obsidian history block: [ScheduledJobHistoryList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs)
- View model options: [ScheduledJobHistoryListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs)

### Data View Source

Use these landmarks for Data Views:

- Search block: [DataViewSearch.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs)
- Persisted refresh job: [UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs)
- v2 CRUD API: [DataViewsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DataViewsController.CodeGenerated.cs)
- v2 action API: [DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs)
- Communication flow entered Data View setting: [CommunicationFlowDetailEnteredDataViewSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowDetail/CommunicationFlowDetailEnteredDataViewSettingsBag.cs)

### Lava Cache And Lava APIs

Use these docs:

- [Cache command docs](https://community.rockrms.com/lava/commands/cache-commands)
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

Operationally, inspect:

- Enabled Lava commands.
- Cache keys.
- Cache duration.
- Tags.
- Request variables.
- URL matching.
- HTTP verb matching.
- Security exposure.

### Helix

The Helix overview describes HTMX, Lava Applications, Lava Commands, and Control Shortcodes, while warning that application development carries extra responsibility for security and data integrity ([Helix overview](https://community.rockrms.com/developer/helix/overview)). For operations, that means Helix endpoints and Lava applications should be reviewed like application code, not like static content.

Inspect:

- Application endpoints.
- HTTP methods.
- Security.
- Data writes.
- Lava command access.
- Observability.
- Error behavior.

### Agent Lookup Tools

The AI agent lookup tools documentation recommends loading data, formatting it, and returning it, and its sample uses cache objects with authorization filtering ([Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools)). For agent-built tools, the operational pattern should be:

- Use cache objects when appropriate.
- Filter active records.
- Check authorization.
- Return minimal structured data.
- Avoid leaking restricted records.

## 15. Reporting, Analytics, And Model Map

### Model Map

The Model Map identifies “Service Job History” as a Core model ([Model Map](https://community.rockrms.com/ModelMap)). Use Model Map as a navigation aid, then verify details in source or live schema.

### Reports And Operational Dashboards

Operational dashboards should show:

- Failed jobs in last 24 hours.
- Warning jobs in last 24 hours.
- Long-running jobs.
- Jobs with no recent history.
- Exception counts by type/message/page.
- Search re-index status.
- Persisted Data View refresh failures.
- Stale persisted Data Views.
- Cache-related exceptions.
- Security anomalies.
- Version/release note watch items.

When building reports, avoid using stale persisted Data Views unless that is intentional. Document whether a report is live or persisted.

### Analytics Boundaries

Analytics can identify trends, but operations needs exact records. If a dashboard says “job failures increased,” the next step is to open job history and exception logs. If a chart says “exceptions spiked,” group by stack trace and first occurrence.

## 16. Version And Release Caveats

### Rock v19.1 Cache/Cleanup Caveat

Rock v19.1 fixed a Clear Cache error that occurred when `App_Data/Cache` did not exist after Rock Cleanup deleted it and no configured file types recreated it ([release notes](https://www.rockrms.com/releasenotes)). If diagnosing Clear Cache errors:

- Check installed Rock version.
- Check whether `App_Data/Cache` exists.
- Check Rock Cleanup history.
- Check file type cache settings.
- Check exception message.
- Consider upgrade/fix status before recommending manual folder creation.

### Rock v19.1 Attribute Category Caveat

Rock v19.1 fixed category dropdown behavior in multiple attribute editing blocks where Global Attribute categories appeared instead of categories for the actual entity type ([release notes](https://www.rockrms.com/releasenotes)). If admins report wrong categories:

- Check version.
- Identify the block.
- Identify entity type.
- Inspect categories.
- Check whether the fix applies.

### Rock v19.1 Workflow Caveats

Hydrated release notes include v19.1 workflow fixes, including a timeout issue in the Obsidian Workflow List block with workflows assigned to groups with many members and a Person Entry form Campus selection requirement issue ([release notes](https://www.rockrms.com/releasenotes)). If workflow screens time out or forms behave unexpectedly:

- Check installed version.
- Check workflow assignment size.
- Check group membership size.
- Check block type.
- Check release notes.

### Universal Search Version Notes

The Universal Search documentation includes version update notes from Rock 7 through Rock 18.1 and mentions provider-related changes such as Lucene documentation and Elasticsearch 8 instructions in prior versions ([Universal Search](https://community.rockrms.com/documentation/bookcontent/32)). Always match search provider guidance to installed Rock version.

### Third-Party GitHub Spotlight Records

Triumph Tech GitHub Spotlight posts summarize pre-alpha and release highlights, such as v16.7/v17 and v16.10/v17.0 items ([9/20/2024](https://www.triumph.tech/resources/github-spotlight-9202024-2), [12/20/2024](https://www.triumph.tech/resources/github-spotlight-12202024)). Use these as secondary awareness sources, not as final authority. Confirm with official release notes or source code.

## 17. Implementation Playbooks

### Playbook: Build A Job Health Review

Goal: produce a reliable operational snapshot of job health.

Steps:

1. List active service jobs.
2. For each job, capture last history record.
3. Flag jobs with failure or warning status.
4. Flag jobs with no history inside expected schedule window.
5. Flag jobs whose duration is much longer than baseline.
6. Flag jobs with repeated identical status messages.
7. Flag jobs with history count too low for audit needs.
8. Correlate failures with exceptions.
9. Check release notes for known version issues.
10. Produce a table: job ID, name, active, schedule, last start, last stop, status, message summary, worker, action.

Use `ServiceJobHistory` source fields as the evidence model ([ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)).

### Playbook: Validate Universal Search

Goal: confirm search is configured and fresh.

Steps:

1. Open Universal Search Index Components.
2. Record provider.
3. Validate provider settings.
4. Confirm entities enabled.
5. Review Universal Search Re-Index job history.
6. For Person, review indexed attributes and privacy risk.
7. For Site, verify site advanced indexing setting and crawling starting location.
8. Verify `Index Rock Site` job if site indexing is expected.
9. Run bulk load only when approved.
10. Test expected search results.

Source: [Universal Search](https://community.rockrms.com/documentation/bookcontent/32).

### Playbook: Validate Persisted Data Views

Goal: ensure persisted Data Views are current and not hiding stale report results.

Steps:

1. List persisted Data Views.
2. Capture ID, name, category, entity type.
3. Capture interval/schedule.
4. Capture last refresh.
5. Identify overdue views.
6. Review `Update Persisted DataViews` job history.
7. Test failed or overdue Data Views manually.
8. Inspect SQL timeout.
9. Identify dependent reports/workflows/communications.
10. Recommend optimization or schedule changes.

Source: [UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs).

### Playbook: Review Lava Cache Safety

Goal: find over-broad or risky cache usage.

Steps:

1. Search Lava templates for cache blocks.
2. For each cache block, record key, duration, tags, and content.
3. Identify whether output includes person-specific, role-specific, campus-specific, or date-specific data.
4. Verify key includes all relevant dimensions.
5. Check max size for large outputs.
6. Check invalidation path.
7. Test with multiple users/campuses if security-sensitive.
8. Reduce duration or remove caching where unsafe.

Source: [Cache command docs](https://community.rockrms.com/lava/commands/cache-commands).

### Playbook: Review Lava Webhooks

Goal: prevent accidental data exposure.

Steps:

1. Open Defined Types and locate Lava Webhook configuration.
2. List defined values/routes.
3. Record HTTP verb matching.
4. Record URL/regex matching.
5. Inspect templates.
6. Inspect enabled Lava commands.
7. Verify no sensitive data is exposed without authorization.
8. Confirm external consumers.
9. Add logging/monitoring if appropriate.
10. Document ownership and rollback.

Source: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).

### Playbook: Review Security Integrity

Goal: identify risky or stale security rules.

Steps:

1. Inventory high-risk pages and blocks.
2. Export or inspect auth rules.
3. Group by entity type and action.
4. Identify explicit user rules.
5. Identify inactive/departed person references.
6. Identify missing groups.
7. Identify duplicate rules.
8. Identify broad edit/admin grants.
9. Test as affected roles.
10. Remediate one category at a time.

Use the community security recipe only as a checklist seed, not authority ([Security Management recipe](https://community.rockrms.com/recipes/522)).

## 18. Troubleshooting Decision Tree

### A Job Did Not Run

Check:

1. Is the job active?
2. Is the schedule valid?
3. Is next run in the future?
4. Is server time correct?
5. Is the Rock job runner running?
6. Is another server responsible?
7. Is there any history record?
8. Is history retention hiding old records?
9. Is the job class missing?
10. Did a recent upgrade/plugin change affect it?

Evidence source: job configuration plus `ServiceJobHistory`.

### A Job Failed

Check:

1. What is the exact status message?
2. Is there a matching ExceptionLog row?
3. Did it fail once or repeatedly?
4. Did duration change?
5. Did input data change?
6. Did credentials expire?
7. Did a Data View/report/workflow dependency fail?
8. Did a release note mention this behavior?
9. Can it be rerun safely?
10. What is the smallest corrective change?

### Search Is Missing Results

Check:

1. Provider enabled?
2. Entity enabled?
3. Attribute selected?
4. Bulk load run?
5. Re-index job successful?
6. Site entity special setup needed?
7. Site crawl job exists?
8. Security/filtering expected?
9. Stale index?
10. Version-specific provider issue?

Source: [Universal Search](https://community.rockrms.com/documentation/bookcontent/32).

### Search Shows Sensitive Results

Check:

1. Is the result from Person attributes?
2. Was a sensitive attribute indexed?
3. Is the content from site crawling?
4. Is the page public?
5. Is attribute security expected but unavailable in search?
6. Should the entity/attribute be removed from index?
7. Should index be rebuilt after removal?

Source warning: [Universal Search](https://community.rockrms.com/documentation/bookcontent/32).

### Report Results Are Stale

Check:

1. Does the report use a Data View?
2. Is the Data View persisted?
3. When did it last refresh?
4. Did `Update Persisted DataViews` run?
5. Did the Data View fail?
6. Is cache involved?
7. Is the report itself cached?
8. Are permissions filtering rows?
9. Does live query differ from persisted state?
10. Is the dependent block using old settings?

### Clear Cache Throws An Error

Check:

1. Rock version.
2. Exact exception.
3. Does `App_Data/Cache` exist?
4. Did Rock Cleanup delete it?
5. Are file types configured to cache to server?
6. Is the v19.1 fix present?
7. Is there a file permission issue?

Source: [release notes](https://www.rockrms.com/releasenotes).

### A Data View API Call Fails

Check:

1. Is the caller authenticated?
2. Does the Data View exist?
3. Is ID/GUID/IdKey correct?
4. Does current person have View authorization?
5. Does caller have unrestricted read authorization?
6. Is entity ID valid?
7. Does the Data View execute?
8. Is a persisted stale result involved?

Source: [DataViewsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs).

### A Lava Endpoint Exposes Too Much

Check:

1. Is it a Lava webhook?
2. Which Defined Value route matches?
3. Which HTTP verbs match?
4. Which Lava commands are enabled?
5. Does the template check authorization?
6. Does it expose person, finance, workflow, or security data?
7. Is it cached?
8. Can route be disabled or restricted?

Source: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).

## 19. Agent Task Recipes

### Recipe: Answer “Is The System Healthy?”

Return:

- Rock version.
- Job failures/warnings in the last 24 hours.
- Exception spike summary.
- Universal Search Re-Index last status.
- Update Persisted DataViews last status.
- Cleanup job last status.
- Cache-related exceptions.
- Any release-note caveats for installed version.
- Items needing live review.

Do not say “healthy” unless job history, exceptions, and key derived-state jobs have been checked.

### Recipe: Answer “Why Is This Data Wrong?”

1. Identify displayed value.
2. Identify source entity.
3. Identify whether display uses Data View, report, Lava, cache, or search.
4. Compare source-of-truth row to displayed row.
5. Check cache/index/persistence.
6. Check security filtering.
7. Check recent job history.
8. Report exact mismatch and refresh path.

### Recipe: Answer “Can I Clear Cache?”

Return:

- What cache is suspected.
- Whether source data is correct.
- Whether broad clear is necessary.
- Impact risk.
- Version caveat if `App_Data/Cache` issue may apply.
- Preferred narrow action.

### Recipe: Answer “Why Did This Workflow Not Start?”

1. Identify workflow type.
2. Identify trigger or launch job.
3. Check job history if scheduled.
4. Check workflow security/category permissions.
5. Check exception logs.
6. Check required form fields and entity context.
7. Check release notes for workflow fixes.
8. Verify whether it never started or started and failed.

### Recipe: Answer “Why Is This Data View Slow?”

1. Identify Data View ID/name/entity.
2. Inspect filter tree and nested Data Views.
3. Check persistence settings.
4. Check last refresh duration if available.
5. Check `Update Persisted DataViews` timeout.
6. Test live result count.
7. Identify expensive filters.
8. Recommend filter/index/report changes only after evidence.

### Recipe: Answer “What Changed In This Version That Matters Operationally?”

1. Identify current version and target version.
2. Read official release notes.
3. Extract Core, Workflow, Reporting, CMS, Security, Lava, API, and Mobile items if relevant.
4. Map each change to local features in use.
5. Produce test checklist.
6. Include source links.

Use [release notes](https://www.rockrms.com/releasenotes) as primary authority.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `1`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | release_caveat | The v19 Page Load Time diagnostic can expose page-debug timing traces without separate observability setup, helping administrators identify slow page components. Use it for diagnosis and confirm findings with broader telemetry when the issue is intermittent or infrastructure-wide. | [source](https://www.youtube.com/watch?v=c-wycR9HEuQ) |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `1`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/bKmX5yalo7) | approved_for_public_distillation | 5 | media-insight:574371376cd3e666 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

Primary source dependencies:

- RockU Core Concepts establishes entity, property, attribute, defined type, campus, note type, job, and automation vocabulary: [Core Concepts](https://community.rockrms.com/rocku/core-concepts).
- RockU Jobs provides conceptual training coverage for jobs: [Jobs](https://community.rockrms.com/rocku/core-concepts/jobs).
- Model Map identifies Service Job History as a Core model: [Model Map](https://community.rockrms.com/ModelMap).
- `ServiceJobHistory` source defines the job history model and its relationship to `ServiceJob`: [ServiceJobHistory.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs).
- `ServiceJobHistoryService` source defines history filtering and retention behavior: [ServiceJobHistoryService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs).
- Scheduled Job History block source explains the `ScheduledJobId` parameter and UI behavior: [ScheduledJobHistoryList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs).
- `UpdatePersistedDataviews` source explains persisted Data View refresh scheduling and timeout behavior: [UpdatePersistedDataviews.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs).
- Universal Search official docs explain provider configuration, entity indexing, re-index jobs, site indexing, and Person attribute security caveats: [Universal Search](https://community.rockrms.com/documentation/bookcontent/32).
- Lava cache docs explain cache keys, duration, tags, and memory-backed Lava output caching: [Cache command docs](https://community.rockrms.com/lava/commands/cache-commands).
- Lava API docs explain webhook routing through Defined Types and warn about security exposure: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).
- Developer Codex provides architecture, service-layer, security-pattern, migration, logging, API, and performance context: [Developer Codex](https://community.rockrms.com/developer/developer-codex), [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards).
- Defined Types & Defined Values developer note provides the null/missing-value guardrail: [Defined Types & Defined Values](https://community.rockrms.com/developer/developer-codex/coding-standards/defined-types-defined-values).
- AI agent lookup tools documentation demonstrates cache-backed lookup plus authorization filtering: [Lookup Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools).
- Helix overview warns that Lava application development carries security and data integrity responsibility: [Helix overview](https://community.rockrms.com/developer/helix/overview).
- Rock release notes provide version-specific operational caveats, including v19.1 cache, attribute, and workflow fixes: [Release Notes](https://www.rockrms.com/releasenotes).
- Community recipes provide examples only and must be reviewed before use: [Security Management recipe](https://community.rockrms.com/recipes/522), [Podcast import recipe](https://community.rockrms.com/recipes/503).

Dependency notes:

- Security, workflows, Data Views, reports, cache, jobs, and release notes are not separate silos. Most real incidents cross at least two of them.
- Service job history is the primary source for background execution evidence.
- Exception logs are required for diagnostics, but the provided pack does not include enough ExceptionLog source detail to assert exact fields.
- Cleanup internals are under-sourced in this pack except for job history retention and the v19.1 cache-folder caveat. Inspect live configuration/source before making cleanup claims.
- Universal Search has strong official documentation in the pack; use it before community guidance.
- Lava webhooks and Helix-style Lava applications should be treated as application surfaces with explicit security and data integrity review.
