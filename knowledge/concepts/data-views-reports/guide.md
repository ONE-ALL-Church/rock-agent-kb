---
id: authored-data-views-reports
title: Data Views And Reports
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "db220b334e3b41ae0681ce5dda8e6dac3255e59ffb2e96497bdeb87898822d0f"
---

# Data Views And Reports

## Agent Summary

Treat Rock reporting as a layered system:

1. Define the qualifying record set with a Data View.
2. Present or operate on that set with a Report, Dynamic Report block, workflow, group sync, metric, Lava template, or another consumer.
3. Move to SQL or a Dynamic Data block only when the supported reporting tools cannot express the requirement.
4. Use metrics, persisted datasets, or BI analytics tables when repeated historical calculation is too expensive for interactive use.
5. Secure the delivered report surface and verify the actual audience, because access to a report can expose data the viewer could not otherwise access in Rock.
6. Validate the grain, source data, refresh timing, permissions, and downstream consumers before changing reporting logic.

This separation between qualification and presentation is the central Rock reporting model. A Data View answers “which records qualify?” while a Report determines fields, sorting, limits, and available grid actions. Reusing the Data View avoids reproducing the same selection logic in multiple reports or automations. [Data View Overview](https://community.rockrms.com/rocku/reporting/data-view-overview), [Intro to Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/intro-to-reports)

Use Rock-native reporting when staff need operational, person-actionable results inside Rock. External BI is better suited to broader analytical exploration, complex combinations, third-party sources, or leadership dashboards, but it introduces refresh, licensing, and access-control responsibilities. This decision frame is a reviewed community pattern rather than a universal product rule. [Data Analytics Hub panel](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz)

## Scope And Boundaries

This guide covers:

- Data Views as reusable record-set definitions.
- Reports as presentation and action layers.
- Dynamic Report and Dynamic Data blocks.
- persistence, metrics, and scheduled capture.
- BI analytics tables and external BI delivery.
- bounded SQL patterns for reporting.
- reporting-oriented data-integrity checks.
- operational workflows involving communication lists, registrations, provider events, and embedded dashboards.

Related concepts own the detailed mechanics of SQL, Lava, finance, attendance, event registration, communications, connections, and security. This guide addresses those topics only where they affect reporting design or verification.

A source-code excerpt can explain an implementation surface, but it does not prove that a particular installation has the same version, plugins, filters, schedules, or configuration. For example, the supplied Rock source at an immutable commit represents Data View filters as a tree whose nodes can require all child conditions or at least one child condition. Treat that as an implementation observation and verify behavior in the installed version. [DataViewFilter source at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)

Community recipes and organizational contributions are patterns to adapt. They are not official Rock behavior and often require local schema, configuration, security, and rendered-page verification.

## Mental Model

A reporting request should be decomposed into five questions:

1. **Grain:** What does one result row represent—a person, registration, registrant, transaction detail, communication recipient, group, or metric value?
2. **Population:** What exact records qualify, and which Data View or query owns that definition?
3. **Presentation:** Which fields, calculations, sorting, limits, charts, or export-only columns are needed?
4. **Delivery:** Will the result appear as a Report, Dynamic Report, Dynamic Data block, metric chart, embedded BI page, workflow input, group sync, or export?
5. **Freshness and authority:** Is the result live, persisted, scheduled, snapshot-based, or externally refreshed, and who may view or act on it?

The layers can be summarized as:

- **Operational records:** Rock’s transactional entities and attributes.
- **Qualification:** Data Views and their filter trees.
- **Presentation and action:** Reports, grids, Lava fields, Dynamic Report blocks, workflows, and exports.
- **Scheduled capture:** persisted Data Views, metrics, and persisted datasets.
- **Analytical models:** BI fact and dimension views populated by jobs.
- **External delivery:** Power BI or another licensed reporting platform.

Do not collapse these layers into one opaque query unless there is a demonstrated need. Separating them makes ownership, performance, security, and data-quality failures easier to locate. [Intro to Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/intro-to-reports), [Intro to BI](https://community.rockrms.com/documentation/church-management/reporting/power-bi/intro-to-bi)

## Data Views

A Data View should be treated as a reusable definition of qualifying records. Its entity type determines what kind of records it returns and which filters are available. Data Views can reference other Data Views, and Rock’s reporting interface exposes their categories, run details, filter summaries, results, and known consumers such as other Data Views, Reports, and group syncs. [Add a Data View](https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view)

Before changing a Data View, inspect:

- its entity type;
- its complete filter tree, including nested Data Views;
- whether grouped conditions mean all or any conditions must match;
- its category and description;
- its persistence settings and interval;
- whether nested filters use persisted results;
- its recent run duration and usage;
- every visible downstream consumer.

This inspection is required because a seemingly local reporting correction can change Reports, workflow behavior, synchronized groups, and other automations. [Data View Overview](https://community.rockrms.com/rocku/reporting/data-view-overview), [Add a Data View](https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view)

Prefer composition over duplication. If a stable population already exists, reference that Data View and add only the new criterion. This keeps shared logic in one place, but it also increases the need to inspect downstream dependencies before editing the shared definition. [Add a Data View](https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view)

Preview results are useful for checking examples, but the documented editor preview shows only the first 15 returned rows. It is not a complete population audit. Validate counts and known included and excluded records through an appropriate read-only inspection before approving consequential changes. [Add a Data View](https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view)

## Reports

A Rock Report selects an entity type and may use a Data View as its record source. It then separately defines its fields, sort order, and optional result-row limit. Give each Report a description that states its intended use, population, grain, and important exclusions. [Create a Report](https://community.rockrms.com/documentation/church-management/reporting/reports/create-a-report)

A field can be included in the Report but hidden from the on-screen grid while remaining available in the Excel export. Use this for legitimate supplemental export data, but include hidden fields in the security review because invisibility in the grid does not remove the data from the report. [Create a Report](https://community.rockrms.com/documentation/church-management/reporting/reports/create-a-report)

Lava fields can customize presentation, but every source field referenced by that Lava must already be included in the Report. A Lava report field cannot read the value of another Lava report field. Prefer a standard report field when it already provides the required result; use Lava when the display genuinely requires composition or custom formatting. [Use Lava in Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/use-lava-in-reports)

Rock records a Report’s run duration, execution count, and most recent run date. Use these measures to identify slow reports, reports that may no longer be used, and candidates for redesign or persistence. They do not by themselves prove business value or safe deletion; first confirm consumers and ownership. [Intro to Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/intro-to-reports)

Entity-appropriate grid actions can make Report results operational—for example, by enabling communication or export. Treat the availability of an action as a capability, not authorization to execute it. Confirm the audience, population, and requested action before sending, exporting, or launching a workflow. [Intro to Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/intro-to-reports)

## Report Security

Report access must be reviewed independently from ordinary entity access. Rock’s documentation warns that a person who can access a Report can see all data returned by it, including data they might not be able to access elsewhere in Rock. The report author is therefore responsible for limiting both the returned population and access to the Report. [Secure Report Data](https://community.rockrms.com/documentation/church-management/reporting/reports/secure-report-data)

For every report containing sensitive data:

1. Identify the intended roles.
2. Review the Report’s security.
3. Review the page and block security through which it is delivered.
4. Inspect all visible, hidden, and export-only fields.
5. Test as an intended non-administrator.
6. Test as a user who should be denied.
7. Do not treat administrator access as proof that the intended role has access.

Filtering by a safe configuration boundary, such as an intentionally selected group type, can reduce exposure, but it is not a substitute for securing the Report itself. [Secure Report Data](https://community.rockrms.com/documentation/church-management/reporting/reports/secure-report-data)

## Dynamic Reports And Custom Reporting Blocks

The Dynamic Report block renders a selected Report and can expose selected filters from its underlying Data View. This allows one Report definition to accept viewer-controlled criteria instead of requiring a separate Report for every campus or similar dimension. [Dynamic Report Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block)

For each exposed filter, the block independently controls:

- whether the filter is visible;
- whether the viewer may change its criteria;
- whether the viewer may toggle it off.

Supported filters can also be initialized through URL parameters. Review URL-driven filters as untrusted user input and confirm that changing or disabling an exposed filter cannot escape the intended population or security boundary. [Dynamic Report Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block)

Use the Dynamic Data block only when Data Views and Reports cannot meet the requirement or when a substantially different presentation is required. The block can execute SQL or a stored procedure, impose a timeout, and render results as a grid or Lava template. That flexibility also moves responsibility for query cost, schema coupling, output encoding, authorization, and responsive behavior to the implementer. [Dynamic Data Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-data-block)

When a Lava Entity command is sufficient, prefer it over direct SQL. Entity command parameters such as `where` must be wrapped in single quotes. If `id` is provided, Rock ignores `where`, `dataview`, and `dynamicparameters`; inspect that precedence when a query returns an unexpected single record. [Lava Entity command](https://community.rockrms.com/lava/commands/entity-commands)

Official training also cautions that simplified SQL-in-Lava examples are teaching examples. Production tools should return only required fields, enforce authorization, account for business logic and query cost, and use cache objects or entity commands when appropriate. [RockIQ Rapid Fire Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=1490s)

## Persistence, Metrics, And Snapshot Layers

Persistence exchanges freshness for speed. A persisted Data View is recalculated at its configured interval by the Update Persisted Dataviews job, allowing consumers to reuse the saved qualifying IDs rather than calculating the filters for every request. The result can be stale by as much as the configured interval. [Persist Data Views](https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views)

If a persisted Data View references child Data Views and is configured to use their persisted results, its practical freshness is constrained by the child with the longest persistence interval. A Report using a persisted top-level Data View can load faster because Rock uses the already-calculated top-level population rather than reevaluating the nested filters during that report request. [Persist Data Views](https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views), [Persist Data Views in Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/persist-data-views-in-reports)

Do not enable persistence for a workflow or audience where current membership is required at the moment of action. If persistence is appropriate, document:

- the acceptable staleness window;
- the recalculation job;
- the persistence interval;
- nested persisted dependencies;
- the consumer’s behavior when the persisted result is late or missing.

Metrics provide another scheduled capture layer. Rock metrics can use manual, SQL, Data View, or Lava sources. SQL-, Data View-, and Lava-backed metrics can be calculated according to their configured schedule when the Calculate Metrics job runs, and they can also be calculated on demand without disrupting that schedule. [Intro to Metrics](https://community.rockrms.com/documentation/church-management/reporting/metrics/intro-to-metrics), [Calculate Metrics](https://community.rockrms.com/documentation/church-management/reporting/metrics/calculate-metrics)

A reviewed community pattern is to calculate expensive operational queries off-hours, store repeatable MetricValue rows, and visualize the history later instead of recalculating all operational history on each dashboard load. Persisted datasets can serve a similar role for expensive journey analytics. These are design patterns to validate against the installed Rock version and local workload. [Metrics discussion](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp), [Persisted-dataset discussion](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

Once metric values exist, the Metric Detail block can chart them and control chart style, date range, and series combination. The displayed chart is downstream of the capture process; a correct chart configuration cannot repair missing or incorrectly partitioned MetricValue rows. [View Metric Charts](https://community.rockrms.com/documentation/church-management/reporting/metrics/view-metric-charts)

## Business Intelligence

Rock’s BI layer is optimized for analytical speed rather than live transactional reporting. The documented analytics model uses fact views for measured events and dimension views for descriptive slicing. The views exposed to BI tools use names beginning with `Analytics`; the underlying analytics source tables are not a complete reporting representation and should not be queried directly as though they were the published model. [Intro to BI](https://community.rockrms.com/documentation/church-management/reporting/power-bi/intro-to-bi)

Analytics data is snapshot data. Rock’s Process BI Analytics job must be scheduled and run at least once before the BI reports can contain data. Its enabled processes determine which domains are populated, including documented person, family, campus, financial transaction, attendance, and giving-unit analytics. [Use the BI Job](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job)

Administrators may create multiple Process BI Analytics job instances, enabling different processes on different schedules. Use this when one domain needs more frequent refreshes than others, but document which job owns each process so that a domain is not accidentally disabled or assumed to be real-time. [Use the BI Job](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job)

Rock’s date dimension supports filtering and comparison by properties such as year, month, quarter, and fiscal calendar. Person and family attributes can be added to BI models and selected attributes can track history. Calendar dimension changes can have broad effects; the official documentation specifically warns that an improperly narrowed start date can exclude older people from age-based results. [Customize Data Models](https://community.rockrms.com/documentation/church-management/reporting/power-bi/customize-data-models)

For Power BI cloud refresh, Rock documents the on-premises data gateway as an automation path between the Rock SQL Server and the cloud service. Current provider requirements, supported gateway placement, credentials, and licensing must be verified before implementation. [Use the On-Premises Data Gateway](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-on-premises-data-gateway)

When embedding a BI report in Rock:

- verify the current external BI license and embedding model;
- secure the Rock page and block for the intended roles;
- test as an intended licensed viewer;
- test as a denied viewer;
- verify the displayed data’s refresh timestamp;
- do not infer external licensing from the existence of Rock `Page`, `Block`, or `Auth` records.

Rock-side security and external licensing are separate gates. [BI Embed Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report), [Use the On-Premises Data Gateway](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-on-premises-data-gateway)

## SQL Reporting Patterns

SQL should be an escalation path, not the default starting point. Prefer Data Views, Reports, metrics, cache objects, and entity commands when they meet the requirement. Direct SQL can bypass model-level validation and business behavior and is more tightly coupled to the installed schema. The public ONE&ALL SQL library makes the same caution explicit, but its examples are license-gated and should not be copied without a separate rights and implementation review. [ONE&ALL Rock SQL Library](https://github.com/ONE-ALL-Church/Rock-SQL-Library)

Three community-reviewed SQL patterns are supported by this evidence pack:

- **Window aggregates:** Use `OVER` with `PARTITION BY` when each detail row must retain its identity while also showing grouped context such as a transaction total, detail count, or percentage. [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions)
- **Ranking functions:** `ROW_NUMBER`, `RANK`, `DENSE_RANK`, and `NTILE` can add per-person sequence, ordering, or bucket analysis without procedural post-processing. Validate ordering ties and partitions explicitly. [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions)
- **Grouping sets:** Use grouping sets when one result requires multiple aggregation levels, such as detail totals plus higher-level rollups, without maintaining separate aggregation queries. Validate the local schema and SQL dialect before production use. [Grouping Sets](https://www.triumph.tech/resources/grouping-sets)

Pivot-style queries can turn repeated row values into side-by-side comparison columns. Use this pattern only when the audience truly needs a cross-tab. If categories are unstable or numerous, a normal grouped result may be easier to maintain. The supplied pivot guidance requires local verification and should be treated as a community pattern, not production-ready SQL. [Pivot Pattern](https://www.triumph.tech/resources/pivot-patterns)

Before approving any SQL-backed report, verify:

- the exact Rock version and schema;
- the row grain and join cardinality;
- parameter handling;
- authorization;
- query timeout and expected cost;
- representative records and empty results;
- totals against a simpler independent calculation;
- whether a model, Data View, metric, or persisted layer would be safer.

## Data Integrity And Reporting Quality

A report should expose source-data defects rather than hide them with display logic. Duplicates, missing values, stale attributes, or mismatched identifiers should be surfaced as source-data issues with an owner and correction process. [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1)

Before changing records because a report appears wrong:

1. Identify the exact entity and field.
2. Define the affected population.
3. Identify the authoritative source and owner.
4. Check duplicate and alias risk.
5. Trace the field into Data Views, Reports, attributes, exports, and automations.
6. Define a repeatable correction rule.
7. Test known positive and negative examples.
8. Separate cleanup, merge, verification, and governance work because they carry different permission and audit requirements.
9. Verify downstream reporting after any authorized correction.

This operational method is supported by RockU guidance, but bulk changes still require local live verification and explicit change authorization. [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity), [Data Integrity follow-up](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1)

## Domain Reporting Workflows

### Registration grain

Rock distinguishes a registration from its registrants: one registration may contain multiple registrants, while account, fee, and payment information is managed separately. A dashboard must state whether it counts registration records, registrant records, or distinct people. [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

A reviewed community dashboard pattern recommends defining confirmed and wait-list predicates once, applying them consistently to all charts, and reconciling mutually exclusive segments to the confirmed-registrant population. Many-to-many categories should be disclosed rather than forced to equal a unique-person total. This pattern requires local configuration and live verification. [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

### Communication audiences and delivery health

Communication lists are groups of a specific type. Membership may be maintained manually or synchronized from Data Views, so recipient troubleshooting must inspect the underlying group and its synchronization configuration. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

A reviewed organizational pattern recommends refreshing Data View-backed list membership immediately before a send and comparing the group count with the source count. This is not universal Rock behavior and requires live verification before use. It also does not authorize sending. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

Provider delivery and engagement events are most useful when summarized against the Rock communication and person context that produced the message. Operational reports should expose delivery health without unnecessarily reproducing raw provider-event detail. [Community communications integration discussion](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5)

Rock v19’s Unsubscribe Report can show the recipient, send and unsubscribe timing, communication type or topic, and sender. Use these dimensions to investigate patterns and coach senders rather than assigning every unsubscribe to a single cause. [v19 features at 11:54](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=714s)

### Schedule dates and operational snapshots

Rock v19 materializes recurring iCal occurrences into `ScheduleDate` rows for date-oriented SQL and Lava queries. On v19, use those generated occurrences rather than inventing a second recurrence-expansion process. Verify that the required rows have been generated in the target instance before relying on them. [3 Underrated Features at 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)

Rock v19 Connections can expose list, board, grid, and operational snapshot views with active, unassigned, due-soon, and overdue measures. The available views are configured on the connection type, so missing views are first a configuration question rather than proof of missing data. [Connections overview](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=50s)

## Version And Authority Caveats

Most supplied official documentation was hydrated from the Rock v19 documentation branch. Confirm the installed Rock version before applying configuration paths or expecting fields, jobs, blocks, or models to exist.

Explicit v19 evidence in this guide includes:

- the Unsubscribe Report;
- materialized `ScheduleDate` occurrences;
- the Lava `contains` enhancement;
- Connections navigation views;
- the registration-versus-registrant guidance as supplied in the v19 documentation pack;
- communication-list documentation supplied in v19 scope.

Rock v19 adds a `contains` parameter to the Lava `where` filter for partial matching. Confirm current case, field-type, and performance behavior before using it in broad queries. [v19 features at 18:00](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1080s)

Official documentation and approved official claims carry the highest authority in this guide. RockU guidance provides confirmed operational framing. Community panels, Triumph resources, recipes, and organizational contributions are examples or patterns and require adaptation. Source-code excerpts are immutable implementation evidence from the supplied commit, not proof of installed behavior.

## Troubleshooting Decision Tree

### A Data View returns the wrong records

1. Confirm the Data View entity type.
2. Read the full filter tree and identify all “all” versus “any” groups.
3. Inspect nested Data Views and their entity relationships.
4. Check whether the Data View or a child uses persisted results.
5. Compare known included and excluded examples.
6. Inspect source fields, attributes, aliases, and duplicate risk.
7. Review downstream consumers before editing.
8. If the installed filter component or schema is uncertain, stop and perform a bounded read-only live review. [Add a Data View](https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view), [Persist Data Views](https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views)

### A Report is slow

1. Inspect the Report’s recorded run duration and usage.
2. Open its source Data View and inspect that Data View’s run duration.
3. Identify nested Data Views and expensive filters.
4. Confirm whether the freshness requirement permits persistence.
5. If persistence is already enabled, verify the recalculation job and interval.
6. Check the row limit and remove fields not needed for display, export, or Lava.
7. Escalate to a bounded SQL or persisted-dataset design only when native optimization is insufficient. [Intro to Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/intro-to-reports), [Persist Data Views in Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/persist-data-views-in-reports)

### Results are correct but stale

1. Determine whether the source is live, persisted, metric-based, BI-based, or externally cached.
2. For a persisted Data View, check its interval and nested persisted dependencies.
3. For a metric, check the metric schedule and Calculate Metrics job.
4. For BI, check the owning Process BI Analytics job and its enabled processes.
5. For external BI, check the gateway and dataset refresh.
6. Report the verified “as of” time; do not describe snapshot data as current. [Persist Data Views](https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views), [Use the BI Job](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job)

### A Report exposes unexpected sensitive data

1. Stop distributing or exporting the result.
2. Inspect visible and hidden Report fields.
3. Review Report, page, and block security.
4. Test as the intended role and a denied user.
5. Review the source Data View for populations or group types that should be excluded.
6. Do not assume ordinary entity permissions will filter Report rows. [Secure Report Data](https://community.rockrms.com/documentation/church-management/reporting/reports/secure-report-data)

### A Dynamic Report filter does not behave as expected

1. Confirm that the selected Report uses the expected Data View.
2. Inspect whether the filter is visible, configurable, and toggleable.
3. Check whether the filter belongs to the top-level or nested Data View.
4. Validate the supported URL parameter name and value format.
5. Test with no URL parameters before testing prepopulation.
6. Verify that disabling the filter cannot broaden access beyond the intended population. [Dynamic Report Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block)

### A Lava Entity query ignores its filters

1. Check whether `id` is supplied.
2. If it is, remove it when the desired behavior depends on `where`, `dataview`, or `dynamicparameters`.
3. Ensure parameter values such as `where` are enclosed in single quotes.
4. Confirm the entity and requested fields.
5. Stop and use a bounded read-only test if the installed Lava version is uncertain. [Lava Entity command](https://community.rockrms.com/lava/commands/entity-commands)

### A BI report is empty or missing a domain

1. Confirm that Process BI Analytics is scheduled.
2. Confirm that it has completed at least once.
3. Inspect whether the required domain process is enabled.
4. Check whether another BI job instance owns that process.
5. Verify the external dataset or gateway refresh after Rock’s job completes.
6. Confirm that the report uses published `Analytics` views rather than incomplete source tables. [Use the BI Job](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job), [Intro to BI](https://community.rockrms.com/documentation/church-management/reporting/power-bi/intro-to-bi)

### Dashboard totals disagree

1. Name the grain of every metric.
2. Define each population once.
3. Check joins for one-to-many or many-to-many multiplication.
4. Compare totals with a simpler independent query or Rock surface.
5. Test a multi-record example, an excluded example, and a recent example.
6. Confirm snapshot timestamps are aligned.
7. Label non-additive measures instead of forcing them to reconcile. [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations), [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

## Agent Task Recipes

### Recipe: Create a reusable operational Report

**Outcome:** One governed population definition and one Report that presents it without duplicating filter logic.

1. Define the entity grain and intended audience.
2. Locate an existing Data View that exactly matches the population, or create a clearly described one.
3. Validate known included and excluded records.
4. Inspect persistence and downstream consumers.
5. Create the Report with the matching entity type and selected Data View.
6. Add only required fields, sorting, and a justified row limit.
7. Mark supplemental fields as export-only only when needed.
8. Apply Report security.
9. Test the grid, export, and available actions as the intended role.
10. Record the owner, purpose, and freshness expectation.

**Inspect:**

- Data View consumers.
- hidden export fields.
- run duration.
- Report, page, and block security.

**Do not assume:**

- preview rows represent the full population;
- ordinary entity security will constrain Report results;
- the ability to communicate or export authorizes the action.

**Stop when:**

- the population lacks an agreed definition;
- sensitive-field access cannot be bounded;
- the change would alter shared consumers without owner review.

[Create a Report](https://community.rockrms.com/documentation/church-management/reporting/reports/create-a-report), [Secure Report Data](https://community.rockrms.com/documentation/church-management/reporting/reports/secure-report-data)

### Recipe: Convert duplicated Reports into one Dynamic Report

**Outcome:** One Report supports controlled viewer-selected criteria.

1. Identify Reports that differ only by a dimension such as campus.
2. Consolidate their shared population logic into one Data View.
3. Leave the viewer-controlled criterion at a safe default.
4. Create or select one Report using that Data View.
5. Add a Dynamic Report block and select the Report.
6. Expose only the intended filters.
7. Set visibility, configurability, and toggle behavior separately.
8. Test default, modified, disabled, and URL-initialized states.
9. Test as intended and denied roles.
10. Remove duplicates only after confirming no downstream consumers remain.

**Do not assume:**

- every Data View filter is safe to expose;
- URL initialization is an authorization boundary;
- a nested filter is controlled at the same level as a top-level filter.

[Dynamic Report Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block)

### Recipe: Introduce persistence for a slow Data View

**Outcome:** Faster consumer performance with an explicitly accepted freshness window.

1. Measure the current Data View and Report run times.
2. Identify consumers and their maximum acceptable staleness.
3. Inspect nested Data Views and current persistence settings.
4. Choose an interval no longer than the accepted staleness window.
5. Confirm the Update Persisted Dataviews job is present and operating in the target instance.
6. Enable persistence in an approved test scope.
7. Compare persisted and live results using known examples.
8. Measure the consumer again.
9. Document the interval, job dependency, owner, and rollback condition.
10. Recheck after one complete recalculation cycle.

**Stop when:**

- the consumer requires current membership at action time;
- a nested interval makes the effective freshness unacceptable;
- the recalculation job cannot be verified.

[Persist Data Views](https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views)

### Recipe: Diagnose an empty BI dashboard

**Outcome:** Identify whether the failure is Rock population, job processing, external refresh, licensing, or authorization.

1. Record the expected domain and freshness.
2. Check whether Process BI Analytics has run successfully.
3. Confirm the domain process is enabled.
4. Identify any separate job instance responsible for that process.
5. Verify that the required `Analytics` views contain the expected bounded sample.
6. Check the external dataset or gateway refresh.
7. Verify external licensing and user entitlement.
8. Verify Rock page and block authorization.
9. Compare the dashboard timestamp with the Rock job completion time.
10. Report the failing layer without claiming the whole pipeline is verified.

**Do not assume:**

- a successful Rock job proves the cloud dataset refreshed;
- a visible embedded page proves the user is properly licensed;
- administrator access proves role access.

[Use the BI Job](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job), [Use the On-Premises Data Gateway](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-on-premises-data-gateway)

### Recipe: Validate a registration analytics dashboard

**Outcome:** Every displayed total has an explicit grain and reconciled population.

1. Label measures as registrations, registrants, or distinct people.
2. Define confirmed and wait-list predicates once.
3. Apply those predicates consistently to every component.
4. Test a multi-person registration.
5. Test a wait-list registrant.
6. Test a recent registrant near the reporting boundary.
7. Reconcile mutually exclusive segments to the confirmed population.
8. Identify many-to-many categories and label them non-additive.
9. Align historical pace comparisons by the same event stage when using that community pattern.
10. Test permissions, empty states, Lava errors, browser errors, filters, and responsive layout in the rendered page.

**Stop when:**

- local staff, serving, campus, source, or department definitions are undocumented;
- the target instance cannot verify the required groups, attributes, or hierarchy;
- exact source deployment is confirmed but rendered authorization and totals remain untested.

[Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations), [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

## Known Gaps And Live Verification

The evidence pack does not establish the following for any arbitrary Rock installation:

- installed Rock version and schema;
- installed plugins or custom Data View filters;
- actual Data View, Report, metric, job, page, block, or authorization configuration;
- BI licensing, tenant configuration, gateway health, or external refresh status;
- whether v19-only features are installed and configured;
- whether community SQL, pivot, dashboard, workflow, or metric patterns fit the local schema;
- whether a specific Data View’s persisted population is current;
- whether rendered dashboards enforce the intended role access;
- whether source-data cleanup rules have an authorized owner;
- whether provider events are available or linked consistently;
- whether community-contributed connection, workflow, group-history, or DefinedValue patterns apply locally.

These questions require a separate, bounded, read-only live review. That review should confirm only public-safe conclusions and must not publish raw records, private identifiers, SQL output, credentials, or organization-specific evidence.

The community contributions about DefinedValue source mismatches, inherited group metric categories, connection-status history, workflow persistence before SQL, historical group snapshots, SQL metric backfills, communication-list count reconciliation, and Helix dashboard validation remain local patterns requiring live verification. They should not be promoted into universal Rock behavior from this pack alone.

## Source Map

### Official Rock documentation and release material

- [Reporting documentation index](https://community.rockrms.com/documentation/church-management/reporting)
- [Add a Data View](https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view)
- [Persist Data Views](https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views)
- [Intro to Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/intro-to-reports)
- [Create a Report](https://community.rockrms.com/documentation/church-management/reporting/reports/create-a-report)
- [Use Lava in Reports](https://community.rockrms.com/documentation/church-management/reporting/reports/use-lava-in-reports)
- [Secure Report Data](https://community.rockrms.com/documentation/church-management/reporting/reports/secure-report-data)
- [Dynamic Report Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block)
- [Dynamic Data Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-data-block)
- [Intro to Metrics](https://community.rockrms.com/documentation/church-management/reporting/metrics/intro-to-metrics)
- [Calculate Metrics](https://community.rockrms.com/documentation/church-management/reporting/metrics/calculate-metrics)
- [View Metric Charts](https://community.rockrms.com/documentation/church-management/reporting/metrics/view-metric-charts)
- [Intro to BI](https://community.rockrms.com/documentation/church-management/reporting/power-bi/intro-to-bi)
- [Use the BI Job](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job)
- [Customize Data Models](https://community.rockrms.com/documentation/church-management/reporting/power-bi/customize-data-models)
- [Use the On-Premises Data Gateway](https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-on-premises-data-gateway)
- [Lava Entity command](https://community.rockrms.com/lava/commands/entity-commands)
- [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)
- [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)
- [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ)
- [3 Underrated Features Churches Are Overlooking](https://www.youtube.com/watch?v=edanHiYSDIM)
- [Connections Helps Prevent Your People from Falling Through the Cracks](https://www.youtube.com/watch?v=7rxTGLLhlrU)

### RockU operational guidance

- [Data View Overview](https://community.rockrms.com/rocku/reporting/data-view-overview)
- [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity)
- [Data Integrity follow-up](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1)
- [BI Overview](https://community.rockrms.com/rocku/business-intelligence-bi/bi-overview)
- [BI Job](https://community.rockrms.com/rocku/business-intelligence-bi/bi-job)
- [BI Embed Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report)

### Community-reviewed patterns

- [Data Analytics Hub panel](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz)
- [Grouping Sets](https://www.triumph.tech/resources/grouping-sets)
- [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions)
- [Pivot Pattern](https://www.triumph.tech/resources/pivot-patterns)
- [Reporting Dashboard recipe](https://community.rockrms.com/recipes/397)
- [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

### Immutable implementation evidence

- [DataViewFilter model at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)
- [Attendance Data View filter at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)
- [Data View integration tests at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs)