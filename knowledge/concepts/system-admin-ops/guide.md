---
id: authored-system-admin-ops
title: System Administration And Operations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "d3fe999a05020bfd62c171ede1e6ab12704aff9764230be78e038a0285a5c07a"
---

# System Administration And Operations

## Agent Summary

Treat Rock operations as several connected control loops:

1. Scheduled jobs perform recurring work and record execution history.
2. Exception and page-timing diagnostics reveal failures or slow components.
3. Caches and persisted datasets trade freshness for faster delivery.
4. Data-integrity tools surface records that require review or controlled automation.
5. Universal Search depends on a provider, enabled entity types, re-index jobs, and entity-specific settings.

Do not treat a configured schedule as proof that a job ran, an empty exception screen as proof that infrastructure is healthy, a cache clear as a permanent performance fix, or a completed re-index as proof that every intended field was eligible for indexing.

For Rock v19, the Page Load Time diagnostic can expose page-debug timing traces without separate observability setup. Use it to identify slow page components, then corroborate intermittent or infrastructure-wide problems with broader telemetry. This statement is the approved answer-bearing claim `claim:091606bd3b8b0472392a`, sourced to the official [v19 features presentation at 16:43](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s).

## Scope And Boundaries

This guide covers the operational behavior directly supported by the supplied Rock v19 documentation, selected release notes, and immutable source excerpts:

- Scheduled jobs, job history, and job-backed processes.
- Exception history, optional exception email configuration, auditing, and page timing.
- Block/output caching, cache tags, cache statistics, and persisted datasets.
- Duplicate review and merging, location correction, Data Automation, photo verification, and record-source inspection.
- Smart Search and Universal Search provider, entity, indexing, crawling, and result configuration.

This is not a hosting, database-maintenance, backup, security-policy, workflow-design, report-design, or API-administration guide. Those are related concepts and should retain their own implementation details. For example, this guide preserves search and merge security conditions but does not define a complete security model.

The evidence pack does not contain reviewed live-instance findings. Therefore, it cannot establish which jobs, providers, plugins, cache types, data views, indexed attributes, schedules, or security roles are currently configured in any installation.

The pack also does not document a general Rock Cleanup policy, database retention plan, stale-record deletion workflow, or orphan-repair procedure. The only supplied cleanup-specific evidence is a v19.1 cache-folder bug fix, so broader cleanup behavior remains a documented gap rather than an inferred capability.

## Mental Model

An operational symptom can originate in more than one layer:

- **Execution:** A job may be disabled, delayed, failing, or recording misleading history.
- **Application:** A page or block may throw an exception or spend excessive time in one component.
- **Freshness:** A cache, persisted dataset, search index, or crawler may not yet reflect source changes.
- **Eligibility:** A record may exist but not qualify for automation or indexing because an entity, attribute, group type, channel, calendar, site, or data view is not enabled.
- **Security:** An administrator may be able to see a task without having enough access to merge protected records or inspect all surviving values.
- **External dependency:** Elasticsearch or another provider may be installed but unreachable or pointed at the wrong environment.

Keep these mechanisms distinct:

- A **scheduled job** runs work.
- **Service Job History** records a job run.
- An **exception record** records an application error.
- A **cache** reuses previously rendered or retrieved material.
- A **persisted dataset** prepares expensive data through a job for repeated use.
- A **Universal Search index** is a separate searchable representation of selected Rock entities.
- **Smart Search** is a user-facing search entry point that can route to Universal Search after integration is configured.

## Jobs And Scheduling

### Job configuration and history

Rock places job-dependent configuration under `Admin Tools > System Settings > Jobs Administration` in the supplied documentation. Examples include the Universal Search re-index job and the separate `Index Rock Site` job used for site crawling. Data Automation exposes its business rules under `Tools > Data Integrity > Data Automation`, while its updates occur when the associated service job runs. [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation)

At immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, Rock models `ServiceJobHistory` as the history of a scheduled job or routine, associated with a specific service job. The supplied implementation exposes start time, stop time, status, status message, and service-worker information, and the Scheduled Job History block lists history for a supplied job identifier. These are implementation observations from that commit, not proof of what a particular installation retains or displays. [ServiceJobHistory model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs) [Scheduled Job History block](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs)

The same commit’s history service deletes entries beyond each job’s configured history count; its implementation uses 500 when that value is not positive. Treat this as commit-specific retention behavior and verify the installed version and job settings before relying on an old run remaining available. [ServiceJobHistoryService implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs)

### Version-specific job-history failures

Official v19.5 release notes describe two operationally important fixes:

- A scheduled job could silently stop running until Rock restarted if an internal error occurred while Rock recorded run status, wrote job history, or sent the job notification email.
- Jobs completing in under one second could produce duplicate Service Job History rows, a false `Incomplete` status, and exaggerated run times.

The supplied immutable development record explains the second defect as a failure to pair the start and completion callbacks reliably for extremely fast jobs. That source is implementation evidence for the fixed defect, not evidence that every `Incomplete` row on another version has this cause. [Rock release notes](https://www.rockrms.com/releasenotes) [Immutable implementation record](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/specs/completed/core/260731-servicejobhistory-sub-second-orphaned-incomplete-rows.md)

When investigating job health, inspect multiple consecutive runs. Compare expected schedule, start and stop times, status, duration, and status message. A single history row—especially on a version affected by the v19.5 fixes—does not independently prove whether the underlying work succeeded.

### Job-backed operational processes

The evidence identifies several processes whose freshness depends on jobs:

- Universal Search queues a bulk index when an entity is enabled and uses a nightly `Universal Search Re-Index` job to reconcile entities other than Site. [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search)
- Site content requires its own scheduled `Index Rock Site` job. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- Persisted Datasets are prepared in database or memory through a job. [Cache Persisted Datasets](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets)
- Data Automation changes person and family records only when its job runs. The v19 documentation says the default schedule is Tuesday morning, but installations may change it. [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation)
- At the supplied immutable commit, the `Update Persisted DataViews` job locates persisted data views due for refresh based on interval or schedule configuration. This is source-code evidence, not confirmation that the job is installed, active, or scheduled in a specific instance. [UpdatePersistedDataviews implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Jobs/UpdatePersistedDataviews.cs)

For any freshness problem, identify both the producer and its job. Inspecting only the consumer page cannot establish whether the scheduled producer ran.

## Diagnostics And Exceptions

### Exception history

Rock records application exceptions that can result from software defects or misconfigured pages and blocks. Administrators can inspect grouped exception types at `Admin Tools > Settings > Exception List`; the list is chronological, and an exception type can be opened for detail. Rock can also send exception information to recipients configured through `Admin Tools > Settings > Global Attributes > Email Exceptions List`. [View the Exception List](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list)

Use exception grouping to distinguish recurrence from a one-off event:

1. Identify the repeating exception type.
2. Open its details and correlate timestamps with the affected page, job, or user action.
3. Determine whether the same failure appears across different pages or only one configuration.
4. Check the installed Rock version against relevant release notes.
5. Reproduce only in a controlled context; do not infer the cause from the exception title alone.

Email delivery is an alerting path, not the underlying exception store. A lack of email does not prove a lack of exceptions; inspect the Exception List directly.

### Page performance diagnostics

In Rock v19, the Page Load Time diagnostic can expose page-debug timing traces without requiring separate observability setup. Use it to locate a slow page component. If the slowdown is intermittent, affects many pages, or appears infrastructure-wide, confirm the finding with broader telemetry rather than treating one trace as a complete diagnosis. This is approved claim `claim:091606bd3b8b0472392a`, supported by the official [v19 features presentation](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s).

Caching can mask slow first-load behavior. Rock’s caching documentation warns that an inherently slow data operation remains a problem because cached content is not permanent. For large, repeatedly expensive datasets, the documented alternative is a Persisted Dataset rather than relying solely on an output cache. [Intro to Caching](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching) [Cache Persisted Datasets](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets)

### Auditing

Rock’s documentation says most database changes are tracked in audit tables and can be reviewed to determine what changed and who made the change. Auditing is controlled under `Admin Tools > Settings > Global Attributes > Enable Auditing`. Enabling it has a significant performance impact, so the documentation recommends using it only for brief periods when needed. [Use Audit Information](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-audit-information)

Do not enable auditing as an open-ended response to a vague performance problem. First define the change or time window being investigated, then stop the diagnostic period when sufficient evidence has been collected.

## Cache And Persisted Data

### What Rock caches

Rock caching reuses previously prepared content so Rock can avoid repeating database queries or web requests. The v19 documentation describes caching for HTML Content blocks, content-channel blocks, Lava cache commands, and Persisted Datasets. For content-channel blocks, Item Cache retains underlying entity data while Output Cache retains the rendered block output; these two modes are mutually exclusive. Output Cache is appropriate only when the result is not personalized by the current person, page, or another changing merge value. [Intro to Caching](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching)

A Lava cache key determines whether different locations reuse the same cached result. A shared key intentionally reuses content; a unique key isolates it. The `twopass` option can cache the first-pass result and process the cached material through Lava again for supported personalization patterns. Validate the actual merge fields and privacy implications before caching personalized output. [Intro to Caching](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching)

The administrative web-cache toggle temporarily disables caching through a cookie for supported blocks. In the supplied v19 documentation, the supported list is HTML Content, Content Channel View, Content Channel Item View, and Internal Communication View. This is a troubleshooting aid, not a global cache-state change. [Intro to Caching](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching)

### Cache Manager and cache tags

At `Admin Tools > CMS Configuration > Cache Manager`, an administrator can inspect tags and linked keys, clear entries by tag, view cache statistics, and clear selected cache types. Targeted tag clearing avoids the broader impact of clearing every cached object. [Cache Manager](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager)

Cache tags must be lowercase and contain no spaces. The documentation states that created tags cannot be modified or deleted, so use a short stable name and record its purpose in the description. After a tag exists, caching-enabled blocks expose a Cache Tags setting and may be linked to one or multiple tags. Clearing any linked tag refreshes the cache for the associated block. [Add Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) [Use Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags)

Clearing a tag removes cached items tied to its linked keys. The Cache Manager documentation notes that the displayed linked-key count does not change merely because those cached items were cleared, so that count alone is not proof that stale output remains. [Clear Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags) [Cache Manager](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager)

Cache statistics report hits, misses, adds, gets, and clears. They are disabled by default for performance reasons. Enabling them causes Rock to restart, so schedule that action for a low-activity period and obtain the appropriate operational authorization first. [Cache Manager](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager)

### Persisted Datasets

Persisted Datasets provide an always-ready representation of shaped data that can be reused across blocks and markup styles. Rock prepares them in database or memory through a job. The documentation recommends them for large datasets that take seconds or minutes to process, or for queries that do not scale safely when repeated per request. [Cache Persisted Datasets](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets)

A Persisted Dataset introduces two separate checks:

- Did its producing job run successfully?
- Does the consuming Lava or block request the intended dataset?

Clearing an unrelated output cache will not demonstrate that the persisted data itself was regenerated.

### Cleanup-related cache caveat

Rock v19.1 fixed a case in which the Rock Cleanup job deleted the cache directory, no server-cached file types recreated it, and the Clear Cache action then threw `DirectoryNotFoundException`. The fix checks for the directory before enumerating and deleting its contents. On an affected earlier build, this specific error can be version-related rather than evidence of a permissions or disk failure. [Rock release notes](https://www.rockrms.com/releasenotes)

## Cleanup And Data Integrity

### Access and review boundary

Rock’s data-integrity tools are located under `Tools > Data Integrity`. The supplied v19 documentation says access is limited to members of the Data Integrity Worker security role. [Intro to Data Integrity](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/intro-to-data-integrity)

Finding a candidate problem is not authorization to repair it automatically. Duplicate merging, status automation, photo-request sending, and bulk changes can affect identity, security roles, communication, and family structure.

### Duplicate detection and merging

The Duplicate Finder routinely evaluates possible duplicate people, assigns a confidence score, and lists candidates under `Tools > Data Integrity > Duplicate Finder`. The list includes confidence, Account Protection Profile, name, match count, modification time, and creator. The detail view supports marking a pair as not duplicates, deferring the decision, or selecting records for merge. Record Source can help explain where each record originated. [Use Duplicate Finder](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder) [Track Record Sources](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/track-record-sources)

The confidence score is a heuristic based on matching fields such as names, email, phone, address, birthday, gender, campus, marital status, and suffix. It is not proof of identity. If evidence is insufficient, Rock supports leaving the pair unresolved until additional information changes the score. [Use Duplicate Finder](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder)

During a merge, the operator selects the primary record and the values that survive. Address selection remains separate from choosing the primary record. Merging two different people is the central risk, and incomplete attribute visibility can cause Rock to retain values from the chosen primary record without letting the operator compare all alternatives. [Merge Duplicate Records](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records)

Out of the box, Data Integrity Workers complete merges. A person without sufficient edit access can create a Merge Request instead. Account Protection Profiles introduce further restrictions for Medium, High, or Extreme records according to configured Security Settings. Do not bypass or generalize those controls. [Merge Duplicate Records](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records)

### Record Source

Record Source is a Defined Type that identifies the originating channel or process for a person record. Blocks that create people can assign a default source, and a page parameter can override the block setting. Administrators can use this value when analyzing duplicate-entry patterns or comparing data quality across entry points. [Track Record Sources](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/track-record-sources)

Treat Record Source as provenance, not proof that every field on the record came from that source or remains unchanged.

### Location correction

The Location Editor at `Tools > Data Integrity > Location Editor` lists location records and can be filtered to addresses that have not been geocoded. An administrator can open a location, correct its address fields, save it, and have Rock resolve the coordinates again. [Location Editor](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor)

A corrected address should be verified in the consuming feature—such as a map, check-in configuration, or mailing process—because saving the location is not by itself evidence that every downstream use is now correct.

### Data Automation

The Data Automation page controls job-driven rules for:

- Reactivating inactive people.
- Inactivating active people.
- Updating family campus.
- Moving adult children into their own families.
- Updating Connection Status.
- Updating Family Status.
- Optionally filling unknown gender values according to a configured confidence threshold.

Updates occur when the Data Automation job runs. The supplied v19 documentation says its default schedule is Tuesday morning, although the schedule can be changed. [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation)

Data views can include or exclude people from automation. Inactive reasons can also disallow automated reactivation. When inactivation is enabled, affected people may be inactivated in most groups they belong to, including security roles. Processing can launch workflows, and a maximum-record setting limits how many people are processed per run; the documented default is 200. These consequences require review before changing criteria or running the job. [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation)

### Photo verification

Photo requests follow a request, email, upload, and staff-verification workflow. Uploaded photos become visible immediately while also entering a verification list at `Tools > Data Integrity > Photo Requests > Verify Photos`. Bulk requests are initiated elsewhere and may require the same approval process as bulk email when their configured threshold is exceeded. [Administer Photo Requests](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/administer-photo-requests)

Photo verification is an operational review task; sending new requests is a communication action and should be authorized separately. The photo-request opt-out list is represented through the Photo Request application group with inactive membership. [Administer Photo Requests](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/administer-photo-requests)

## Search And Indexing

### Smart Search and person-name behavior

Smart Search appears at the top of Rock pages and defaults to person-name searching. Name fragments are supported. With one search term, Rock treats the term as a last name unless `Allow Search by Only First Name` is enabled for the Person Name search service under `Admin Tools > Settings > System > Search Services > Person Name`. A single match can route directly to the Person Profile; multiple matches produce a selection list. [Search by Name](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-name)

This person-name service should not be conflated with Universal Search. Universal Search participates in Smart Search only after its provider, indexes, search service, and results URL are configured.

### Provider configuration

Universal Search first requires an index provider configured under `Admin Tools > System Settings > Universal Search Index Components`. The supplied documentation describes Lucene and Elasticsearch options and states that Elasticsearch must be installed before it can be selected and configured in Rock. [Enable a Search Provider](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-a-search-provider)

The v19 Elasticsearch article recommends Elasticsearch 8.x and gives Windows-oriented instructions based on 8.1.2. It requires Rock to be configured with the provider’s node URL, username, password, and certificate fingerprint. Do not copy those values into logs or public output. Confirm compatibility, connectivity, certificate details, and service operation in the actual environment before enabling indexing. [Installing Elasticsearch](https://community.rockrms.com/documentation/core-concepts/search/universal-search/installing-elasticsearch)

After an environment refresh, Rock may still reference the source environment’s Elasticsearch settings. The documentation directs administrators to update the node and relevant credentials or fingerprint for the refreshed environment; a failed connection appears in the Universal Search Control Panel. [Installing Elasticsearch](https://community.rockrms.com/documentation/core-concepts/search/universal-search/installing-elasticsearch)

### Enabling entities and keeping them current

Enable indexable entity types at `Admin Tools > General Settings > Universal Search Control Panel`. Enabling an entity queues a bulk index. The panel also supports a bulk re-index and an index delete-and-recreate operation; the latter is useful when old indexed attributes must be purged. [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search)

Entity changes should update the index as they occur. A nightly `Universal Search Re-Index` job also reconciles changes, including items introduced through SQL or other paths, for all supported entities except Site. Site crawling is managed separately. [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search)

### Entity-specific eligibility

Universal Search eligibility varies by entity:

- **Person:** Enabling Person sends individuals to the index. Selected person attributes can also be indexed. Attribute additions or removals require a Person bulk load for immediate availability; otherwise the nightly bulk re-index must run. Attribute security is not enforced in Universal Search, so do not index sensitive person attributes merely because they are secured elsewhere. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- **Business:** Businesses share Person entity configuration even though Universal Search presents them as a separate filtering option. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- **Group:** The entity and the intended Group Types must be enabled. Group-attribute changes require a manual index reload. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- **Content Channel Item:** Intended content channels and attributes must be selected. The Content Channel Item Publishing Point controls how results link to the item; without one, Rock uses the internal item page. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- **Site:** Enable indexing in the site’s advanced settings, supply a Crawling Starting Location, and schedule an `Index Rock Site` job. Crawlers discover pages through hyperlinks, so unlinked pages are not discoverable from the starting path. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- **Event Item:** Indexing is enabled at the calendar level. Indexed terms include the event item’s title, description, and summary. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)
- **Document:** Enable the Document entity in the Universal Search Control Panel. The supplied documentation does not require a separate per-document-type indexing switch and describes search by document name or type. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)

For authenticated site crawling, the documentation describes a dedicated crawler account and a secured starting page containing discoverable links. A logout link can terminate the crawler session before Rock evaluates a no-index response; restricting the crawler’s access to logout is the documented mitigation. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)

### Smart Search integration and result presentation

After Universal Search is operational, configure it under `Admin Tools > System Settings > Search Services`, move it to the desired position in the component list, and provide a results URL pointing to a page containing the Universal Search block. The documented Smart Search integration appends `SmartSearch=true`; `ShowRefineSearch=true` can be added when the results page should retain refinement controls. Entity visibility and additional options are configured in the Universal Search Control Panel. [Integrating Smart Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/integrating-smart-search)

Per-entity result rendering and result URLs can be customized under `Admin Tools > Security > Entity Administration` through the Index Results Template and Index Document URL Pattern. The Universal Search block can also use custom Lava, and the Lava `search` command provides lower-level control. Treat template changes as presentation and routing changes; they do not make absent fields eligible for indexing. [Customizing Results for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/customizing-results-for-entities)

Rock v19.3 fixed Person Attribute Values being omitted from Universal Search after a bulk re-index and restored the Attributes block’s missing `Indexing Enabled` option. On an affected earlier v19 build, a correct-looking attribute configuration and re-index may still exhibit this documented defect. [Rock release notes](https://www.rockrms.com/releasenotes)

## Version And Authority Caveats

Most operational documentation in this evidence pack is scoped to Rock v19.0. Two supplied release-note fixes alter the interpretation of symptoms:

- v19.1 fixed Clear Cache failing when the cleanup process had removed a cache directory that was not recreated.
- v19.3 fixed indexed Person Attribute Values being absent after bulk re-index.
- The hydrated v19.5 release notes describe job stoppage and misleading history fixes affecting status recording, notifications, and sub-second runs.

Check the exact installed Rock version before applying those explanations. [Rock release notes](https://www.rockrms.com/releasenotes)

The Page Load Time statement is an approved, medium-confidence, v19.0-scoped claim. It supports using the diagnostic for component-level page analysis but explicitly requires broader telemetry for intermittent or infrastructure-wide incidents. [Official v19 presentation](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s)

GitHub observations in this guide are pinned to commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They clarify implementation at that revision; they do not prove an installation’s deployed code, database state, configuration, or plugin behavior.

No community recipe in the pack supplies reviewed system-administration behavior for this guide. The supplied podcast-import recipe is a draft, community-authored example and is not used as authority for Rock job behavior.

## Troubleshooting Decision Tree

### A scheduled job stopped producing new history

1. Inspect the job’s expected schedule and its most recent consecutive history rows.
2. Compare start time, stop time, status, status message, and duration rather than relying on the last status label alone.
3. Check whether the installed version predates the v19.5 fix for jobs silently stopping after errors while recording status, writing history, or sending notifications.
4. If rows are duplicated, falsely `Incomplete`, or show implausible durations for extremely fast work, check applicability of the separate v19.5 sub-second-history fix.
5. Verify the downstream result independently; history recording and business work are related but not identical outcomes.
6. Stop when version applicability or the installed job configuration cannot be established without live review. [Rock release notes](https://www.rockrms.com/releasenotes) [Immutable job-history defect record](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/specs/completed/core/260731-servicejobhistory-sub-second-orphaned-incomplete-rows.md)

### A page is slow

1. On v19, capture the Page Load Time diagnostic and identify the slow component.
2. Compare an uncached or first request with a cached request.
3. If the expensive work is a large reusable dataset, inspect whether a Persisted Dataset is appropriate.
4. If the issue is intermittent or spans multiple pages, correlate it with infrastructure telemetry and exception timestamps.
5. Stop before enabling broad auditing or cache statistics unless their restart or performance effects are authorized. [Approved claim source](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s) [Intro to Caching](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching)

### Updated content remains stale

1. Identify whether the block uses Item Cache, Output Cache, Lava caching, or a Persisted Dataset.
2. Inspect the block’s assigned cache tags.
3. Clear only the relevant tag when one exists.
4. Do not interpret an unchanged linked-key count as proof that the clear failed.
5. If a Persisted Dataset supplies the data, inspect its producing job rather than repeatedly clearing output cache.
6. Verify the rendered page after the appropriate refresh path completes. [Cache Manager](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) [Use Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags) [Cache Persisted Datasets](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets)

### Clear Cache throws a missing-directory error

1. Record the exact exception and installed Rock version.
2. Check whether the error is `DirectoryNotFoundException` involving the cache directory.
3. Check applicability of the Rock v19.1 fix for the cache directory being removed by Rock Cleanup and not recreated.
4. Do not infer a filesystem-permission problem from this signature alone.
5. Stop if the signature or version differs; the pack supplies no broader cache-directory repair procedure. [Rock release notes](https://www.rockrms.com/releasenotes)

### Exceptions repeat after a page or block change

1. Open `Admin Tools > Settings > Exception List`.
2. Locate the grouped exception type and correlate its timestamps with the configuration change.
3. Open the exception detail and identify the affected page, block, or code path.
4. Revert or adjust only the configuration demonstrated to be involved.
5. Confirm whether the exception stops recurring.
6. If email alerts were absent, inspect the Exception List directly and separately verify the Email Exceptions List configuration. [View the Exception List](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list)

### Universal Search cannot connect after an environment refresh

1. Open the Universal Search Control Panel and confirm the provider connection error.
2. Inspect the configured provider under `Universal Search Index Components`.
3. Confirm that node URL, environment-specific credentials, and certificate fingerprint refer to the refreshed environment’s Elasticsearch service.
4. Verify the external service independently without exposing credentials.
5. Only after connectivity is restored, inspect entity indexing and re-index status. [Installing Elasticsearch](https://community.rockrms.com/documentation/core-concepts/search/universal-search/installing-elasticsearch)

### A person attribute is missing from Universal Search

1. Confirm that Person indexing is enabled.
2. Confirm that the specific attribute is selected for indexing.
3. Assess whether the attribute is safe to expose, because Universal Search does not enforce person-attribute security.
4. Run the supported Person bulk load or wait for the nightly re-index.
5. If the installed version predates v19.3, check applicability of the documented Person Attribute Values defect.
6. Stop if the desired attribute is sensitive or version applicability is unknown. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) [Rock release notes](https://www.rockrms.com/releasenotes)

### An entity type returns no Universal Search results

1. Confirm the provider is connected.
2. Confirm the entity is enabled in the Universal Search Control Panel.
3. Apply the entity-specific eligibility check: Group Type, Content Channel, site settings and crawl, calendar, or Person attribute.
4. Inspect the relevant re-index or site-crawl job history.
5. For sites, verify that the crawling starting location links to the missing content and that the crawler did not encounter an accessible logout link.
6. Re-index only after correcting eligibility or connectivity.
7. Verify one known eligible result after completion. [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)

### Universal Search works directly but not through Smart Search

1. Confirm Universal Search is enabled in Search Services.
2. Confirm its position in the component list matches the intended default behavior.
3. Inspect the configured results URL and its Smart Search parameter.
4. Confirm the target page contains the Universal Search block.
5. Inspect which entities are allowed to appear through Smart Search.
6. Treat result templates and index contents as separate checks. [Integrating Smart Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/integrating-smart-search)

### Two person records may be duplicates, but identity is uncertain

1. Open the candidate in Duplicate Finder.
2. Compare contact, name, family, birthday, Record Source, creator, modification time, and other available evidence.
3. Treat confidence as a heuristic.
4. If evidence is insufficient, defer the decision so Rock can reassess as records gain information.
5. Merge only when both records are established to represent the same person and the operator can review the values that will survive.
6. Stop when security restrictions or incomplete attribute visibility prevent a safe comparison. [Use Duplicate Finder](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder) [Merge Duplicate Records](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records)

### An address is missing coordinates

1. Open `Tools > Data Integrity > Location Editor`.
2. Filter for locations that are not geocoded.
3. Open the affected location and correct its address fields.
4. Save so Rock can resolve coordinates again.
5. Verify the corrected location in the downstream feature that reported the problem. [Location Editor](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor)

### Data Automation changed more records than expected

1. Identify which automation function changed the records.
2. Inspect its inclusion and exclusion Data Views, inactive-reason settings, and processing limit.
3. Check whether affected people were also changed in groups or security roles.
4. Correlate the changes with the Data Automation job’s execution history and audit information already available.
5. Do not rerun the job until the criteria and downstream effects are understood.
6. If temporary auditing is proposed, account for its significant performance cost. [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation) [Use Audit Information](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-audit-information)

## Agent Task Recipes

### Recipe: Triage a recurring exception

**Outcome:** Identify the narrowest supported failure boundary without claiming an unverified root cause.

1. Open the Exception List and locate the grouped exception type.
2. Record the recurrence count and relevant timestamps.
3. Open a detail record and identify the associated page, block, job, or action.
4. Correlate the first occurrence with recent configuration or version changes.
5. Check official release notes for the installed version.
6. Reproduce only through a bounded, non-destructive path.
7. Verify that the exception stops recurring after the demonstrated cause is corrected.

**Inspect:**

- Exception type and detail.
- First and most recent timestamps.
- Affected component.
- Installed Rock version.
- Related job history, when applicable.

**Do not assume:**

- Missing notification email means no exception occurred.
- Every exception is a software defect; page and block misconfiguration are also documented causes.

**Stop when:**

- Reproduction requires a production write or destructive configuration change.
- The installed version or affected component cannot be established. [View the Exception List](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list)

### Recipe: Refresh stale cached output with minimum scope

**Outcome:** Refresh the affected output without unnecessarily clearing unrelated caches.

1. Identify the stale block and its caching mode.
2. Open its settings and identify assigned cache tags.
3. Open Cache Manager.
4. Clear the most specific applicable tag.
5. Reload the affected page and confirm that the intended content changed.
6. If it remains stale, determine whether the data comes from a Persisted Dataset or another cache layer before taking broader action.

**Inspect:**

- Block cache mode.
- Cache tag assignments.
- Persisted Dataset dependency.
- Result before and after the clear.

**Do not assume:**

- The linked-key count must decrease after a tag clear.
- A global cache clear will regenerate a Persisted Dataset.

**Stop when:**

- The only proposed next step is enabling statistics, because that restarts Rock and requires an operational window. [Cache Manager](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) [Clear Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags)

### Recipe: Create and assign a cache tag

**Outcome:** Establish a durable, targeted invalidation boundary for related cached blocks.

1. Define the content group whose caches should be invalidated together.
2. Choose a short lowercase name without spaces.
3. Write a description that explains the tag’s intended scope.
4. Add the tag in `Admin Tools > CMS Configuration > Cache Manager`.
5. Open each caching-enabled block in scope and assign the tag.
6. Test the relationship by changing non-sensitive content, clearing the tag, and verifying all intended blocks.
7. Record the tag as permanent because the documentation says it cannot be modified or deleted.

**Do not assume:**

- Similar block names imply that blocks share a cache.
- A tag can be renamed later. [Add Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags) [Use Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags)

### Recipe: Audit a scheduled job’s recent health

**Outcome:** Determine whether recorded executions match the expected schedule and whether the downstream result is current.

1. Identify the exact scheduled job.
2. Inspect several consecutive history records.
3. Compare expected schedule with start and stop timestamps.
4. Review status, status message, and duration.
5. Check whether the installed version is affected by the v19.5 job-history defects.
6. Inspect the job’s downstream artifact, such as index freshness, automated record changes, or persisted data.
7. Report history status and downstream verification separately.

**Do not assume:**

- A false `Incomplete` row on an affected version proves the job failed.
- A successful history row proves the intended business records changed.

**Stop when:**

- Verification would require changing the schedule, manually running a mutating job, or querying private data without authorization. [Rock release notes](https://www.rockrms.com/releasenotes) [Service Job History implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs)

### Recipe: Restore a missing Universal Search entity

**Outcome:** Return one known eligible record to search without rebuilding unrelated indexes first.

1. Verify provider connectivity.
2. Confirm the entity is enabled.
3. Confirm the entity-specific eligibility setting.
4. Confirm that intended attributes are permitted and safe to index.
5. Inspect the relevant re-index or site-crawl job.
6. Correct connectivity or eligibility before initiating a bulk operation.
7. Run the supported entity-specific bulk load or allow the scheduled job to complete.
8. Search for one known eligible record and verify its destination URL.

**Inspect:**

- Provider component.
- Entity toggle.
- Group Type, Content Channel, calendar, site, or attribute setting.
- Job history.
- Rock version.

**Do not assume:**

- A record in Rock is automatically eligible for Universal Search.
- Attribute security carries into Universal Search.
- Re-indexing corrects a wrong provider or eligibility setting.

**Stop when:**

- The requested field is sensitive.
- A delete-and-recreate operation is proposed without confirming its scope and operational window. [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search) [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)

### Recipe: Configure a bounded site-index crawl

**Outcome:** Index the intended site pages without unintentionally exposing or omitting secured content.

1. Enable indexing in the site’s advanced settings.
2. Choose a crawling starting location that links to every intended page.
3. If secured content is required, use a dedicated crawler identity and restrict the link page to that identity and administrators.
4. Ensure the crawler cannot access a logout action that would terminate its session.
5. Configure an `Index Rock Site` job with the intended schedule.
6. Inspect job history after execution.
7. Verify representative public and authorized results separately.

**Do not assume:**

- Unlinked pages will be discovered.
- The nightly Universal Search Re-Index job crawls Site entities.
- Hiding a link page from navigation alone provides the documented security boundary.

**Stop when:**

- Credentials would need to be exposed in task output.
- The intended content-access boundary has not been approved. [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities)

### Recipe: Review and resolve a duplicate-person candidate

**Outcome:** Merge only records demonstrated to belong to the same person while preserving the intended values.

1. Open the pair in Duplicate Finder.
2. Compare identity evidence and Record Source.
3. Review Account Protection Profile and operator permissions.
4. If uncertain, defer rather than merge.
5. If confirmed, select the primary record.
6. Review each surviving value, including the address separately.
7. Submit a Merge Request if the operator lacks merge authority.
8. Verify the resulting profile and any expected notification after completion.

**Inspect:**

- Identity evidence.
- Record Source and creator.
- Modification dates.
- Account Protection Profile.
- Attribute visibility.
- Primary record and surviving values.

**Do not assume:**

- A high confidence score proves identity.
- The primary record automatically supplies the correct address.
- Access to start a merge means access to complete it.

**Stop when:**

- Two distinct people cannot be ruled out.
- Security restrictions prevent a complete comparison. [Use Duplicate Finder](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder) [Merge Duplicate Records](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records)

### Recipe: Review a Data Automation change before execution

**Outcome:** Define the expected affected population and side effects before a job mutates records.

1. Identify the exact automation function being changed.
2. Inspect all inclusion and exclusion Data Views.
3. Inspect inactive-reason restrictions when reactivation is involved.
4. Review effects on family structure, campus, connection status, family status, groups, security roles, and launched workflows as applicable.
5. Review the maximum records processed per run.
6. Record the expected population and expected field changes.
7. Obtain authorization before saving material changes or running the job.
8. After execution, compare job history and a bounded sample of resulting records.

**Do not assume:**

- A Data View name proves its current membership logic.
- Person inactivation affects only the person’s Active flag.
- The documented Tuesday schedule is still configured locally.

**Stop when:**

- The affected population has not been evaluated.
- Security-role or workflow side effects are unclear. [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation)

## Known Gaps And Live Verification

No reviewed live-instance evidence was supplied. A bounded, read-only review is required to establish:

- Exact installed Rock version and applicability of the v19.1, v19.3, and v19.5 fixes.
- Enabled, disabled, paused, or missing scheduled jobs.
- Actual schedules, time zones, history counts, notification settings, and recent job outcomes.
- Whether misleading historical rows remain from a pre-fix version.
- Configured cache types, block cache modes, cache tags, and current cache statistics state.
- Whether a stale page uses a Persisted Dataset and which job refreshes it.
- Data Automation criteria, Data Views, inactive reasons, record limits, workflows, and current schedule.
- Data Integrity Worker membership and merge security for protected records.
- Universal Search provider, connection health, credentials scope, certificate configuration, and environment isolation.
- Enabled search entities, indexed attributes, group types, content channels, calendars, sites, crawl starting locations, and Smart Search settings.
- Whether candidate indexed person attributes contain information that should not be exposed through Universal Search.
- Actual exception frequency and whether email alerts are configured and delivering.
- Page Load Time findings correlated with infrastructure or application telemetry.
- Any general Rock Cleanup configuration, retention policy, stale-record cleanup, or orphan-repair mechanism not described in this pack.

The pack does not support claiming that a cleanup, re-index, job execution, cache clear, duplicate merge, location correction, Data Automation run, or search-provider repair has occurred. Completion requires direct readback from the relevant instance and, for user-visible functions, verification of the affected result.

## Source Map

| Guide area | Authority and scope | Sources |
|---|---|---|
| Page Load Time diagnostic | Approved answer-bearing claim; Rock v19.0; medium confidence | `claim:091606bd3b8b0472392a`; [official v19 presentation](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s) |
| Job-history model and retention implementation | Immutable public source observation at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` | [ServiceJobHistory](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs); [history service](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs); [history block](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs) |
| v19.5 scheduled-job defects | Official release notes plus immutable implementation decision record | [Rock release notes](https://www.rockrms.com/releasenotes); [sub-second history record](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/specs/completed/core/260731-servicejobhistory-sub-second-orphaned-incomplete-rows.md) |
| Exceptions and auditing | Official v19.0 documentation | [View the Exception List](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list); [Use Audit Information](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-audit-information) |
| Cache behavior and administration | Official v19.0 documentation | [Intro to Caching](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching); [Cache Manager](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager) |
| Cache tags | Official v19.0 documentation | [Add Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags); [Use Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags); [Clear Cache Tags](https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags) |
| Persisted data | Official v19.0 documentation and immutable implementation observation | [Cache Persisted Datasets](https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets); [Update Persisted DataViews job](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Jobs/UpdatePersistedDataviews.cs) |
| Cache cleanup defect | Official v19.1 release note | [Rock release notes](https://www.rockrms.com/releasenotes) |
| Data-integrity access and tools | Official v19.0 documentation | [Intro to Data Integrity](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/intro-to-data-integrity); [Data Integrity index](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity) |
| Duplicate review and merge | Official v19.0 documentation | [Use Duplicate Finder](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder); [Merge Duplicate Records](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records); [Track Record Sources](https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/track-record-sources) |
| Location correction | Official v19.0 documentation | [Location Editor](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor) |
| Data Automation | Official v19.0 documentation | [Use Data Automation](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation) |
| Photo verification | Official v19.0 documentation | [Administer Photo Requests](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/administer-photo-requests) |
| Smart Search person behavior | Official v19.0 documentation | [Search by Name](https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-name) |
| Universal Search provider and Elasticsearch | Official v19.0 documentation | [Enable a Search Provider](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-a-search-provider); [Installing Elasticsearch](https://community.rockrms.com/documentation/core-concepts/search/universal-search/installing-elasticsearch) |
| Universal Search entities and jobs | Official v19.0 documentation | [Enable Entities for Universal Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search); [Specifics for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities) |
| Search integration and result templates | Official v19.0 documentation | [Integrating Smart Search](https://community.rockrms.com/documentation/core-concepts/search/universal-search/integrating-smart-search); [Customizing Results for Entities](https://community.rockrms.com/documentation/core-concepts/search/universal-search/customizing-results-for-entities) |
| Person attribute indexing defect | Official v19.3 release note | [Rock release notes](https://www.rockrms.com/releasenotes) |