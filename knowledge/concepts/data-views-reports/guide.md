---
id: authored-data-views-reports
title: Data Views And Reports
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Data Views And Reports

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Data Views And Reports index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock RMS reporting is not one feature. It is a layered reporting system made from reusable filters, rendered reports, dynamic page blocks, SQL-backed tools, analytics tables, metrics, and external business intelligence surfaces. The best operational mental model is:

1. **Data Views define record sets.**
2. **Reports define columns over those record sets.**
3. **Dynamic Report blocks expose Reports on pages with runtime filtering.**
4. **Dynamic Data blocks expose SQL or other custom data shapes when a standard Report is not enough.**
5. **Business Intelligence uses Rock's analytics-friendly data model and Power BI tooling for leadership analysis.**
6. **Model Map, source code, and live database inspection are the backstop when the UI does not explain the data path.**

Rock's official reporting training frames reporting around Data Views, Reports, Dynamic Data blocks, SQL, and Dynamic Report blocks, which is the right architecture for agents to follow when choosing an implementation path ([RockU Reporting](https://community.rockrms.com/rocku/reporting)). The official reporting manual says Data Views do most of the filtering work and can target many Rock entity types, including people, groups, financial transactions, metrics, page views, and other records ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

For agents doing real Rock work, the most important rule is: **separate the question into record selection, display, delivery, and governance.** A request like "show me lapsed givers by campus" might require a Data View, a Report, a Dynamic Report block, a SQL query, an analytics table, a finance-specific entity join, or a Power BI model. Do not jump directly to SQL just because the request sounds analytical. Do not force a Data View when the desired output needs grouped totals, window functions, ranking, or cross-year comparison. The right tool depends on the shape of the output.

Use this guide as a decision manual:

- Use a **Data View** when the core task is "which records qualify?"
- Use a **Report** when the task is "show columns for records from a Data View."
- Use a **Dynamic Report block** when staff need page-based access, filtering, and interaction with a Report.
- Use a **Dynamic Data block** when the data shape is aggregate, unioned, heavily joined, dashboard-like, or not naturally represented as one entity list.
- Use **Lava entity commands** when you need CMS/page output and can stay within permission-aware entity access.
- Use **Lava SQL** only where SQL is explicitly enabled and governed, using parameters and timeouts where supported; Rock's Lava SQL docs warn that interpolation can create SQL injection risk and note versioned SQL-parameter and timeout support ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)).
- Use **Power BI / BI** when the organization needs repeatable executive analysis, external visualization, or analysis across purpose-built BI models. RockU's BI series covers BI overview, models, template, job, financial transaction, attendance, family, and embedded report topics, while warning that embedded report licensing has cost and must be handled correctly ([Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi), [BI Embed Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report)).
- Use **Model Map and source code** when the entity relationship is unclear. The Model Map identifies reporting models such as `Analytics Dim Campus` in the Reporting category ([Model Map](https://community.rockrms.com/ModelMap)); source code exposes how filters, override bags, cache behavior, and related data views actually work.

The most common operational failures are not "bad reports." They are usually one of these:

- The wrong entity type was chosen for the Data View.
- A nested filter group used "any" when it needed "all", or the reverse.
- A related Data View filter silently evaluates a child entity and joins back in a way the author did not expect.
- A Report column uses a field type or Lava expression that assumes data exists when it may be null.
- The Dynamic Report block or page security exposes a Report but not the underlying Data View, or hides the Report but leaves a Dynamic Data page available.
- SQL or Lava SQL ignores Rock cache, authorization, injection safety, or database performance.
- Finance reporting mixes transactions, transaction details, accounts, giving groups, registration payments, and analytics fact tables without validating the church's business definition.
- Attendance reporting mixes attendance records, schedules, campuses, occurrence dates, check-in configuration, and person aliases without validating exactly which attendance population is being measured.
- BI dashboards are trusted without verifying the BI job, model refresh, dataset credentials, Power BI licensing, and local version compatibility.

When a fact is instance-specific, inspect the live Rock instance instead of assuming. At minimum, inspect the `DataView`, `DataViewFilter`, `Report`, `ReportField`, `Block`, `Page`, `Attribute`, `AttributeValue`, relevant analytics tables, and the specific entity tables involved. For performance or correctness, compare UI results, generated SQL when available, and direct read-only SQL counts.

## 2. Scope And Terminology

This guide covers Rock RMS Data Views, Reports, Dynamic Reports, Dynamic Data blocks, SQL-backed reporting, BI reporting, analytics model discovery, and the operational practices agents should use when building or troubleshooting reporting in a live Rock instance.

It intentionally treats "reporting" as a system, not as a single menu. Rock's official training page includes reporting strategy, Data View overview, filter groups, weaving Data Views, post-filter transformations, Reports, reporting security, other reporting options, and Dynamic Report blocks ([RockU Reporting](https://community.rockrms.com/rocku/reporting)). The official reporting manual also describes Data Views and Reports as part of a broader set of reporting tools, with version notes for Dynamic Data, Dynamic Reports, Data View caching, and measurement classifications ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

### Core Terms

**Data View**

A Data View is a reusable definition of a filtered set of Rock records. It has an entity type, name, description, category, root filter, child filter tree, and result set. The official manual describes Data Views as the bulk of reporting work and states that they can target many entity types, not just people and groups ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

For agents, treat a Data View as a queryable "who/what qualifies" object. It should be named in business language, categorized for reuse, and secured according to the sensitivity of both its filter logic and its resulting records.

**Data View Filter**

A Data View Filter is a node in the Data View filter tree. In source code, `DataViewFilter` stores an expression type, parent relationship, data filter component entity type, and selection value ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)). A filter can be a leaf component, an "all" group, or an "any" group. The source-code model maps this to `FilterExpressionType.Filter`, `GroupAll`, and `GroupOr`.

**Filter Group**

A filter group is a Data View Filter node that contains child filters. It determines whether all child conditions must match or whether any child condition may match. In UI terms, this is the "all vs any" distinction. In code terms, the filter tree is recursive and is evaluated into a LINQ expression; the logic class throws if it cannot resolve the component or expression, which is an important correctness guard ([DataViewFilter.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs)).

**Related Data View**

A related Data View filter lets one entity be filtered by another entity's Data View. For example, a Person Data View may use an Attendance Data View to select people with matching attendance records. Rock source includes an `AttendanceDataViewFilter` that evaluates an Attendance Data View, selects `PersonAliasId`, and returns people whose aliases match those attendance rows ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)). This pattern also appears for group locations, group types, benevolence requests/results, steps, and connection requests in the provided source snippets.

**Report**

A Report is a display definition built on a Data View. The Data View determines which records are included; the Report determines which columns, field types, links, Lava output, and visibility options are shown. RockU treats Reports as a separate reporting topic after Data Views and filter concepts ([RockU Reports](https://community.rockrms.com/rocku/reporting/reports)).

**Report Field**

A Report Field is a configured column on a Report. Depending on the field type, it may show a model property, attribute value, calculated output, link, address part, Lava expression, or other field-specific data. Exact available field types vary by Rock version and installed components, so inspect the live Report editor and `ReportField` records before assuming.

**Dynamic Report Block**

A Dynamic Report block is a page block that renders a Report in a runtime context. It is commonly used when staff need to filter, export, interact with, or reuse a Report on a page. RockU notes a version caveat: in v7, filtering can apply on multiple Data Views rather than only the top-level Data View ([Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)). Verify the current block settings in the target Rock instance because Dynamic Report behavior and block technology have changed across versions.

**Dynamic Data Block**

A Dynamic Data block is a flexible reporting/display block often used for SQL-backed or custom-shaped output. The official reporting manual's update notes mention Dynamic Data blocks as a way to craft display of filtered data and note multiple version changes to Dynamic Data settings ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Use this when a standard Data View plus Report cannot express the required output shape.

**SQL Lava Command**

The Lava SQL command runs SQL from Lava and returns results into a Lava variable. The official Lava docs show read and write patterns, warn about SQL injection, state that command statements need explicit handling, and mention versioned SQL parameter and timeout support in v9.0 and v12.0 ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)). Treat Lava SQL as privileged execution.

**Business Intelligence / BI**

BI is Rock's path for analytical data modeling and leadership-ready analysis, often involving Power BI. RockU's BI section covers overview, models, a Power BI template, a BI job, financial transaction report, attendance report, family report, and embedded reports ([Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi)). The hydrated pack only includes public bounded excerpts for these videos, so exact setup details must be verified against the current Rock BI manual, installed Rock version, and Power BI tenant configuration.

**Analytics Tables**

Rock includes analytics-oriented tables and models such as `AnalyticsFactFinancialTransaction`, `AnalyticsDimFamilyHeadOfHousehold`, `AnalyticsDimFamilyCurrent`, and `AnalyticsDimPersonCurrent` in community finance-reporting examples ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391)). A Triumph resource notes an `Analytics Source Giving Unit` table introduced in v12.5 for faster giving analytics, but because the hydrated excerpt is thin, verify exact table names and behavior in the live database and official release notes before relying on it ([Giving Unit Analytics](https://www.triumph.tech/resources/giving-unit-analytics), [Release Notes](https://www.rockrms.com/releasenotes)).

**Model Map**

The Model Map is a discovery aid for Rock models. The provided record identifies `Analytics Dim Campus` as a Reporting-category model ([Model Map](https://community.rockrms.com/ModelMap)). Use Model Map as a starting point, then verify against the target database schema and Rock source for the installed version.

## 3. Data Views And Reports Mental Model

### The Layered Stack

Think of Rock reporting as a stack:

1. **Entity model**: Rock tables, EF models, relationships, attributes, defined values, categories, pages, blocks, and jobs.
2. **Filter components**: Reusable code components that know how to build expressions for a specific entity type.
3. **Data Views**: Saved filter trees over one entity type.
4. **Reports**: Column definitions over a Data View.
5. **Blocks and pages**: UI locations where Reports, Dynamic Reports, Dynamic Data blocks, HTML/Lava, and embedded BI are shown.
6. **Delivery surfaces**: Staff pages, dashboards, emails, workflows, exports, REST/API, BI dashboards, and external tools.
7. **Governance**: Security, categories, naming, performance monitoring, cache behavior, and review.

This stack follows Rock's own reporting taxonomy: official training separates Data Views, Reports, Dynamic Report blocks, other reporting options, BI, and SQL/Lava surfaces rather than treating "reporting" as one feature ([RockU Reporting](https://community.rockrms.com/rocku/reporting), [Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

This stack matters because each layer can fail independently. A Report can be correct but hidden by page security. A Data View can be correct but slow. A Dynamic Report can render a stale or unexpectedly filtered subset. A BI report can look polished but be based on an old refresh. A SQL report can be fast but bypass Rock's authorization and cache assumptions.

### Record Set vs Presentation

Agents should always ask: "Is this task about selecting records or presenting records?"

A Data View answers "which records?" Examples:

- Which people are adults and active?
- Which groups are of a certain type?
- Which attendance records happened in a schedule/date/campus range?
- Which financial transactions match a fund, date range, and transaction type?
- Which pages or reports exist in a category?

A Report answers "what columns should be shown for each qualifying record?" Examples:

- Show name, campus, age, connection status, email, and last attended date for people.
- Show group name, group type, active status, location, and leader for groups.
- Show transaction date, amount, account, giving group, and batch for financial transactions.

A Dynamic Data block answers "what custom result grid or display does this page need?" Examples:

- Group totals by campus and month.
- Compare current-year and prior-year giving.
- Show a dashboard of multiple reporting tool types.
- Union Reports, Data Views, pages, and Power BI links into one finder.

The community "Reporting Dashboard" recipe is useful as an example of why this distinction matters. It describes a real organization with standard Rock Reports, Data Views, pages with dynamic reporting blocks, and embedded Power BI reports, and centralizes them so staff can find the right tool ([Reporting Dashboard](https://community.rockrms.com/recipes/397)). That does not make the recipe official or universally safe, but the problem pattern is common.

### Data View Composition

Data Views can be composed through:

- Filter groups: all/any grouping.
- Related Data View filters: use one entity Data View to filter another entity.
- Reusable nested Data Views: one Data View can rely on another through a component.
- Runtime overrides: Dynamic Reports and query builders may override selected filters.
- Persisted values or caching: depending on version and configuration.

Source code confirms that `DataViewFilterOverrides` are keyed by filter GUID and can include a set of Data View IDs that should ignore persisted values ([DataViewFilterOverrides.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilterOverrides.cs)). It also shows a `ShouldUpdateStatics` flag, which indicates that execution can be instrumented or counted in some contexts. Verify in the live version how run counts, last-run dates, persisted values, and cache statistics are maintained.

### Related Data View Semantics

Related Data Views are powerful but easy to misunderstand. They do not magically join all fields. Each related filter component implements a specific relationship path.

Examples from the source pack:

- Person by Attendance Data View: evaluates attendance rows, selects `PersonAliasId`, and matches against person aliases ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)).
- Group by Location Data View: evaluates locations, then returns groups associated with matching group locations ([LocationDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs)).
- Group by Group Type Data View: evaluates group types and returns groups whose `GroupTypeId` matches ([GroupTypeDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/GroupTypeDataViewFilter.cs)).
- Benevolence Request by Benevolence Result Data View: evaluates result rows and maps them back to requests ([BenevolenceResultDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/BenevolenceRequest/BenevolenceResultDataViewFilter.cs)).
- Connection Request by Person Data View: source metadata describes matching requests where the requester is the same person as people returned from another Data View ([ConnectionRequest PersonDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/PersonDataViewFilter.cs)).

When troubleshooting a related Data View, inspect the source component or live component settings. Do not assume the relationship path. A person-to-attendance path through `PersonAliasId` behaves differently from a direct `PersonId` join. A group-to-location path may depend on group locations, not campus. A connection request path may match requester, not connector, assigned person, opportunity, or group member unless the component says so.

### "All" vs "Any" Is Usually The Bug

Nested filter groups are the easiest way to create plausible but wrong reports. A common pattern is:

- Group A: all of these conditions must be true.
- Group B inside A: any of these status values may be true.
- Group C inside A: any of these campuses may be true.

If the author instead puts all statuses and campuses in one "any" group, the Data View may return anyone who matches either a status or a campus, not both a status and a campus. If the author puts multiple mutually exclusive values in an "all" group, the Data View may return zero rows.

Rock's official reporting manual includes sections on "Any vs All" and filter groups, making this a first-class concept rather than an edge case ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

### Data View Caching And Persisted Values

Rock's reporting manual update notes say Rock 17.0 implemented caching logic in Data Views to improve performance ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Source snippets show `DataViewFilterCache.ClearByParentId` calls after filter changes, suggesting filter tree cache invalidation occurs when filter parent relationships change ([DataViewFilter.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs)). Source snippets also show query arguments can include database timeout seconds and overrides ([DataViewGetQueryArgs.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewGetQueryArgs.cs)).

Agents should treat caching as version- and context-dependent. For a live instance:

- Inspect the Data View edit page for any persisted/cached-result options.
- Inspect job configuration if Data View persistence is maintained by a job.
- Inspect `DataViewPersistedValue` or similarly named tables only after verifying they exist in that version.
- Compare raw live query results to UI results if stale results are suspected.
- Check whether a Dynamic Report or API call is using filter overrides that intentionally ignore persisted values.

### Reports Are Not Security Boundaries By Themselves

A Report's visibility depends on multiple layers: Report security, Data View security, page/block security, entity security, and any SQL/Lava permissions. The RockU Reporting section includes a "Reporting Security" training topic ([RockU Reporting](https://community.rockrms.com/rocku/reporting)). Community dashboard recipes also show that staff may have access to many reporting surfaces and that a central finder should consider what the current user can access ([Reporting Dashboard](https://community.rockrms.com/recipes/397)).

For agents, never assume that hiding a navigation item secures the underlying report. Verify:

- Report authorization.
- Data View authorization.
- Page authorization.
- Block authorization.
- SQL command availability on Lava/HTML blocks.
- Dynamic Data block access.
- REST/API access to relevant entities.
- Whether exported files or cached BI embeds expose data to a broader audience.

## 4. Source Authority And How To Use This Guide

Use sources in this order of authority:

1. **Installed Rock instance**: live UI, database schema, current version, installed plugins, configured blocks, jobs, security, and actual data.
2. **Official Rock documentation and RockU**: reporting manual, Lava docs, training pages, BI training pages.
3. **Rock source code for the installed version**: not just `develop`, unless the instance is actually running equivalent code.
4. **Model Map**: quick discovery of model categories and names.
5. **Release notes and version update notes**: especially for behavior that changed across versions.
6. **Community recipes and partner resources**: useful examples and patterns, but not authoritative and not necessarily reviewed or safe for every instance.
7. **Public SQL libraries**: useful as examples, but license, compatibility, and local data definitions must be checked.

The provided source pack includes official docs, RockU training pages, community recipes, a Model Map record, partner resources, GitHub source snippets, and a public SQL library record. Community recipe pages themselves include a disclaimer that recipes are contributed and not reviewed or endorsed by the Rock core team ([Reporting Tool Finder](https://community.rockrms.com/recipes/264), [Data View Finder](https://community.rockrms.com/recipes/262)). Treat recipes as examples of possible implementations, not instructions to paste into production.

### How Agents Should Use This Guide

Use this guide for:

- Choosing a reporting implementation pattern.
- Diagnosing why a Data View or Report returns unexpected rows.
- Auditing reporting security.
- Mapping related Rock entities for a reporting request.
- Deciding when to use SQL, Lava, Dynamic Data, Reports, or BI.
- Writing safe implementation playbooks.
- Creating task recipes for future agents.

Anchor each task in the official reporting manual and RockU reporting pages first, then use source code, Model Map, and live inspection for version-specific behavior ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331), [RockU Reporting](https://community.rockrms.com/rocku/reporting)).

Do not use this guide as a substitute for live verification. When this guide says "inspect," do the inspection in the target Rock instance. When source material is from `develop`, compare it to the installed Rock version. When a community recipe references SQL or block settings, evaluate performance and security before using it.

### Citation Policy

Inline links point to the provided source URLs. The guide does not reproduce long passages from sources. When a source only provides a short public excerpt, this guide cites it for topic coverage and tells agents what to verify live. When source snippets include code behavior, this guide synthesizes the behavior without copying the source.

## 5. Core Configuration And Data Model

### Data View Configuration

A typical Data View configuration includes:

- **Name**: human-readable business name.
- **Description**: explanation of inclusion/exclusion criteria and intended use.
- **Category**: hierarchical organization. The official manual emphasizes categories as part of reporting strategy because reusable Data Views become hard to find without organization ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).
- **Entity Type**: the Rock entity being filtered, such as Person, Group, Attendance, Financial Transaction, Metric, Page, Data View, Report, or another model.
- **Transform / Post-filter behavior**: version- and entity-specific transformation options. RockU includes "Post Filter Transformation" as a training topic ([RockU Reporting](https://community.rockrms.com/rocku/reporting)).
- **Filter Tree**: a root group and child filters using "all" or "any" logic.
- **Security**: who can view, edit, and administrate.
- **Results Block**: in the UI, Data View results may be rendered in a separate block, which matters for workflow launches and security configuration ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).
- **Usage References**: the official manual notes that the Data View page can show other Data Views, Reports, or group syncs using the Data View, which is essential before changing a shared filter ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).
- **Persisted/Cached Behavior**: version-specific. Rock 17.0 documentation notes Data View caching improvements ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

When creating or auditing a Data View, agents should record:

- Entity type and why it was selected.
- Inclusion logic in plain English.
- Exclusion logic in plain English.
- Whether results are expected to change over time.
- Whether the view is intended for reuse.
- Known dependent Reports, group syncs, blocks, workflows, or BI tooling.
- Expected approximate row count.
- Security sensitivity.
- Owner or ministry area.
- Test cases.

### Data View Filter Data Model

Source snippets define `DataViewFilter` as a Reporting-domain model with key properties ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)):

- `ExpressionType`: filter, all group, or any group.
- `ParentId`: parent filter node, nullable for root.
- `EntityTypeId`: the filter component used for leaf filters.
- `Selection`: serialized component-specific configuration.

The source comments also warn that `DataViewFilter` is not only used by Data Views. It can be used by content channel filters and registration instance group placement, so an orphan-looking `DataViewFilter` row may not actually be orphaned ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)). This is a critical operational note for cleanup agents: do not delete filter rows merely because they do not join to `DataView`.

The logic class resolves a filter component from `EntityTypeId`, builds a LINQ expression, and throws when required metadata is missing or a filter expression cannot be determined ([DataViewFilter.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs)). When a Data View fails, inspect:

- Missing or invalid `EntityTypeId`.
- Uninstalled plugin filter components.
- Serialized `Selection` values that no longer deserialize.
- Filter components moved or renamed during upgrade.
- Entity type mismatch between Data View and filter component.
- Deleted referenced Data Views, groups, categories, attributes, defined values, schedules, campuses, or pages.

### Data View Query Arguments And Overrides

Source snippets show that query execution can receive arguments such as database context, sort property, filter overrides, and database timeout seconds ([DataViewGetQueryArgs.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewGetQueryArgs.cs)). `DataViewFilterOverrides` are keyed by filter GUID, can ignore persisted values for selected Data View IDs, and include a flag about updating statistics ([DataViewFilterOverrides.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilterOverrides.cs)).

Operational meaning:

- Dynamic pages may not run the exact saved Data View; they may override filter values at runtime.
- A Data View count in the editor may differ from a Dynamic Report output if runtime filters are applied.
- Persisted values may be bypassed in some contexts.
- Timeouts can be relevant for expensive Data Views.
- Sort can be applied outside the saved filter definition.

When troubleshooting, collect the full execution context:

- Saved Data View definition.
- Any filter override values from block settings or query string.
- Report columns.
- Block settings.
- Page parameters.
- Current user permissions.
- Whether persisted/cached results are used.
- Database timeout setting if exposed.
- Runtime date/time and timezone.

### Report Configuration

A typical Report includes:

- **Name**.
- **Description**.
- **Category**.
- **Data View**.
- **Fields / Columns**.
- **Show in grid / export options**.
- **Field-specific settings**.
- **Security**.
- **Usage context**: direct Tools > Reports, Dynamic Report block, dashboards, workflows, exports, or other pages.

RockU treats Reports as a distinct layer on top of Data Views, and the Dynamic Report Block lesson documents the page/block runtime layer where a Report can be exposed ([RockU Reports](https://community.rockrms.com/rocku/reporting/reports), [Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)).

A Report should usually be named after its audience and decision, not just its table. For example, "Kids Ministry - Active Check-in Eligible Children" is more useful than "Children." The Data View should hold selection logic; the Report should hold display logic. Avoid duplicating business filters in Lava columns unless there is no better place.

### Dynamic Report Block Configuration

Dynamic Report block settings vary by version and block implementation, but agents should inspect:

- Selected Report.
- Available runtime filters.
- Whether multiple Data Views can be filtered in the current version. RockU notes this capability in v7 ([Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)).
- Grid settings, paging, export options, and actions.
- Pre/Post HTML or Lava hooks if present.
- Page parameters that feed filters.
- Security of the page and block.
- Whether the block exposes workflow launch, person actions, or communication tools.

Community examples show Dynamic Report blocks being extended for specialized visualization. The Dynamic Report Maps recipe requires a Data View and Report, then adds a map display over the first four report columns, with latitude and longitude generated using address field parts ([Dynamic Report Maps](https://community.rockrms.com/recipes/240)). Treat that as a pattern: Dynamic Reports can be made interactive, but the column contract and client-side code become part of the report's dependency surface.

### Dynamic Data Block Configuration

Dynamic Data block configuration varies by version, but commonly includes:

- SQL or data source.
- Parameter handling.
- Lava template/output.
- Grid options.
- Cache settings.
- Security.
- Page parameters.
- Pre/Post HTML.
- Export or paging options.

The official reporting manual update notes mention Dynamic Data blocks and versioned setting updates ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Community examples use Dynamic Data for a Reporting Tool Finder that searches Reports, Dynamic Reports, Dynamic Data blocks, Power BI reports, and other custom reporting tools ([Reporting Tool Finder](https://community.rockrms.com/recipes/264)). Use Dynamic Data when the data shape crosses reporting tool types or requires SQL aggregation.

### Lava SQL Configuration

Rock's Lava SQL command can select rows into a result variable, use a custom return variable, run command statements, use parameters in versions where supported, and configure timeouts in versions where supported ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)). It is powerful and risky.

Agents should inspect:

- Whether the block has SQL enabled.
- Whether the Lava context allows the SQL command.
- Whether variables are parameterized or interpolated.
- Whether the query can write data.
- Whether cache flush is required after writes. The official docs state direct SQL updates are not automatically known by cache manager ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)).
- Whether timeout is configured.
- Whether the page is secured to a narrow administrative group.
- Whether the SQL touches PII, finance, attendance, or security-sensitive records.

## 6. Primary Entities And Relationships

### `DataView`

Represents a saved filter definition over a Rock entity type. Inspect:

- `Id`, `Guid`.
- `Name`, `Description`.
- `CategoryId`.
- `EntityTypeId`.
- `DataViewFilterId` or root filter reference, depending on schema.
- Persisted/cached settings, if present in the installed version.
- Audit fields.

Relationships:

- One Data View has one root `DataViewFilter` tree.
- One Data View may be referenced by many Reports.
- One Data View may be referenced by other Data View filters.
- One Data View may be used by group syncs, pages, blocks, workflows, or custom code.
- One Data View may have persisted values or statistics depending on version/configuration.

The official manual notes that Data Views can show where they are used by other Data Views, Reports, and group syncs ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Use that before editing shared Data Views.

### `DataViewFilter`

Represents a filter tree node. Key source-code concepts include expression type, parent, filter component entity type, and selection data ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)).

Relationships:

- Parent/child self-reference.
- Leaf filters reference a data filter component through `EntityTypeId`.
- `Selection` stores serialized component settings.
- A root filter is referenced by a Data View or other feature that uses the filter infrastructure.

Operational checks:

- If a Data View returns wrong results, inspect the tree structure, not just visible UI labels.
- If a filter fails after upgrade, inspect component entity type and selection serialization.
- If cleaning old filters, remember Data View Filters may belong to content channels or registration group placement, not only Data Views ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)).

### `Report`

Represents a saved display definition over a Data View. Inspect:

- `Id`, `Guid`.
- `Name`, `Description`.
- `CategoryId`.
- `DataViewId`.
- Security.
- Audit fields.

Relationships:

- One Report belongs to one Data View.
- One Report has many Report Fields.
- One Report may be rendered in Tools > Reports, Dynamic Report blocks, dashboards, pages, or other custom reporting surfaces.

### `ReportField`

Represents a configured Report column. Inspect:

- Field type.
- Name/title.
- Order.
- Visibility such as show in grid/export.
- Serialized field configuration.
- Lava content, links, field-specific settings.
- Attribute references.
- Address part references.
- Person/Group/Entity property references.

In the Dynamic Report Maps recipe, the Report must expose latitude and longitude columns in specific positions and with show-in-grid enabled for the map code to work ([Dynamic Report Maps](https://community.rockrms.com/recipes/240)). That illustrates a general principle: Report column order and visibility can become an API contract for downstream client-side code, exports, workflows, or integrations.

### `Category`

Categories organize Data Views and Reports. The official reporting manual emphasizes Data View categories as part of reporting strategy because reusable reporting assets need to be findable ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

Operational guidance:

- Do not put every reporting object in one shared category.
- Use ministry or domain categories for staff-facing Reports.
- Use technical/admin categories for backend Data Views.
- Use prefix conventions for deprecated, experimental, or ownerless items.
- Secure categories where inheritance matters, but verify item-level security.

### `Block` And `Page`

Reports and dashboards often live on pages through blocks. For reporting work, inspect:

- Page route and title.
- Page security.
- Block type.
- Block settings.
- Block security.
- Zone placement.
- Page parameters.
- Lava/SQL enablement.
- Caching settings.
- Interaction tracking if the page is used for recent-report dashboards.

Community reporting dashboard patterns often discover Reports, Data Views, dynamic reporting pages, and embedded Power BI pages together ([Reporting Dashboard](https://community.rockrms.com/recipes/397), [Reporting Tool Finder](https://community.rockrms.com/recipes/264)). Agents auditing a reporting ecosystem should query both reporting tables and page/block configuration.

### `Attribute` And `AttributeValue`

Attributes are often used in Reports and Data Views. They may attach to Person, Group, Financial Account, Page, Block, Workflow, Connection Request, or custom entities. When a Data View filter or Report column references an attribute:

- Verify `Attribute.EntityTypeId` and optional entity-type qualifier columns.
- Verify field type.
- Verify `AttributeValue.EntityId` meaning.
- Verify security.
- Verify whether value is stored as text, JSON, GUID, key, or serialized field-type data.
- Verify whether the attribute value needs cache refresh after direct SQL writes.

### Person And Alias

Person reporting often needs `Person`, `PersonAlias`, families, connection status, record status, age, campus, email, phone, and attributes. Attendance reporting often links through `PersonAliasId`, not directly through `PersonId`, as shown in the Attendance Data View filter source ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)).

Operational checks:

- Use `PersonAlias` when joining attendance, financial transactions, interactions, or other alias-based tables.
- Deduplicate by `Person.Id` when the report should show one person per row.
- Preserve deceased/inactive/archived exclusions if the business question requires active people only.
- Check record type and record status.
- For household reports, inspect family group roles and analytics family tables.

### Attendance

Attendance reporting may involve:

- `Attendance`.
- `AttendanceOccurrence`.
- `PersonAlias`.
- `Group`.
- `GroupType`.
- `Schedule`.
- `Location`.
- Campus.
- Check-in areas/configuration.
- Attendance analytics tables if present.
- Dynamic Data or BI models.

RockU BI includes an attendance report topic ([BI Attendance Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report)). Source code confirms related Data View filters can select people from Attendance Data Views using aliases ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)).

Do not assume "attended" means "checked in." Inspect whether the report counts:

- Person-level attendance.
- Family-level attendance.
- First-time attendance.
- Check-in attendance only.
- Group attendance.
- Weekend service attendance.
- RSVP or registration attendance.
- Did-not-attend rows.
- Occurrence counts versus unique people.
- Schedules or campus-specific occurrences.

### Finance

Finance reporting may involve:

- `FinancialTransaction`.
- `FinancialTransactionDetail`.
- `FinancialAccount`.
- `FinancialBatch`.
- `PersonAlias`.
- Giving group / family.
- Transaction type defined values.
- Currency, refunds, reversals, fees, pledges, scheduled transactions.
- Analytics fact/dim tables.

Community finance examples use `AnalyticsFactFinancialTransaction`, `AnalyticsDimFamilyHeadOfHousehold`, `AnalyticsDimFamilyCurrent`, and `AnalyticsDimPersonCurrent` for giving by age/generation analysis ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391)). RockU BI also includes a financial transaction report topic ([BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)).

Finance reporting must define:

- Contribution vs non-contribution.
- Registration payments included or excluded.
- Refunds and reversals.
- Soft credits.
- Giving unit logic.
- Date basis: transaction date, batch date, created date, settled date.
- Campus basis: person campus, family campus, transaction campus, account campus, group campus.
- Account tree inclusion.
- Donor privacy and security.

### Analytics Models

Analytics models are optimized for reporting and BI. The provided sources point to analytics facts and dimensions in community SQL, RockU BI models, and Model Map reporting categories ([Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi), [Model Map](https://community.rockrms.com/ModelMap)).

Use analytics tables when:

- The query is read-heavy and leadership-facing.
- The entity relationship is already denormalized into a reporting model.
- Direct transactional joins are too slow.
- The metric aligns with Rock's analytics definitions.

Verify live:

- Table names.
- Refresh job.
- Last refresh time.
- Row counts.
- Version-specific schema.
- Whether the analytics table includes archived/deceased/inactive records.
- Whether current vs historical dimensions are being used correctly.

## 7. Common Data Views And Reports Workflows

### Workflow 1: Build A Staff List Report

Use when the output is a list of records staff can filter, sort, export, or act on.

1. Define the decision.
2. Choose the entity type.
3. Build a Data View with reusable selection logic.
4. Create a Report with staff-facing columns.
5. Place it on a Dynamic Report block if page access is needed.
6. Secure the Data View, Report, page, and block.
7. Test with expected included and excluded records.
8. Record owner, category, and intended use.

This pattern matches Rock's documented separation between reusable Data Views and staff-facing Reports, with Dynamic Report blocks used when the report needs a page surface ([Data View Overview](https://community.rockrms.com/rocku/reporting/data-view-overview), [RockU Reports](https://community.rockrms.com/rocku/reporting/reports), [Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)).

Example: "Active adult members and attendees by campus" should usually be a Person Data View with person status filters and campus filters, then a Report with name, campus, connection status, email, age, and last attendance if needed.

### Workflow 2: Build A Ministry Dashboard

Use when staff need one central page to find or compare many reporting tools.

1. Inventory Data Views, Reports, Dynamic Report pages, Dynamic Data pages, and BI embeds.
2. Decide which audiences should see which tools.
3. Prefer permission-aware retrieval if possible.
4. Use Dynamic Data if the result needs to union multiple object types.
5. Add search, type, owner, category, description, and last-used metadata.
6. Avoid exposing hidden tools through a finder.
7. Test as multiple users.

Community examples include a Reporting Dashboard that centralizes Reports, Data Views, page-based tools, and Power BI reports ([Reporting Dashboard](https://community.rockrms.com/recipes/397)) and a Reporting Tool Finder using a Dynamic Data block and SQL to find multiple reporting surfaces ([Reporting Tool Finder](https://community.rockrms.com/recipes/264)). Treat them as design inspiration and inspect security carefully before implementing.

### Workflow 3: Build A Data View Finder

Use when Data Views have grown too numerous to manage.

1. Create a Data View over the Data View entity, if available in the target version.
2. Filter to meaningful records, such as existing IDs or non-archived categories.
3. Create a Report with name, description, category, created date, last run, run count, usage, and edit link.
4. Secure to reporting administrators.
5. Add owner and review status attributes if the organization needs governance.

The community Data View Finder recipe uses a Dynamic Report approach to search Data Views and view usage-like metadata such as name, description, links, dates, and run counts ([Data View Finder](https://community.rockrms.com/recipes/262)). Verify the exact available fields in the target Rock version.

### Workflow 4: Build A Report Finder

Use when staff cannot find the right Report.

1. Query Reports and their categories.
2. Query pages with Dynamic Report, Dynamic Data, and embedded BI blocks.
3. Include Report/Data View owner and description fields where available.
4. Include page route and ministry category.
5. Respect security for the current user.
6. Add favorite/recent behavior only if interaction tracking and user preferences are understood.
7. Avoid hardcoding page locations unless the organization has a stable reporting page convention.

The Reporting Tool Finder recipe explicitly searches standard Reports and pages that house reporting tools, including Power BI, but warns that local page organization may require customization ([Reporting Tool Finder](https://community.rockrms.com/recipes/264)).

### Workflow 5: Convert A One-Off SQL Request Into A Governed Report

Use when leadership asks for a report that starts as SQL.

1. Write the business definition in plain language.
2. Check whether a Data View plus Report can satisfy it.
3. If aggregate/comparison logic is needed, create SQL in a read-only development context.
4. Validate row counts against known UI records.
5. Parameterize dates, campuses, accounts, and thresholds.
6. Decide whether output belongs in Dynamic Data, a stored procedure, Power BI, or an exported analysis.
7. Secure the page and block.
8. Document assumptions and verification queries.
9. Schedule review for schema/version changes.

Community finance recipes demonstrate SQL-heavy cases where Data Views may not be enough, such as giving by age bands or lapsed givers ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [SQL for Lapsed Givers](https://community.rockrms.com/recipes/109)). Use those as examples of when complex analytics may require SQL, not as copy-paste sources.

### Workflow 6: Build A BI Report

Use when analysis must be visual, recurring, leadership-facing, or cross-domain.

1. Verify Rock version and BI feature availability.
2. Locate current Rock BI manual and release notes.
3. Verify BI models and analytics tables exist in the live instance.
4. Verify the BI job is configured and recently successful.
5. Use the official Power BI template only if it matches the instance version; RockU BI pages reference a Rock RMS v7 `.pbit` template in multiple training records ([BI Template](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template)).
6. Configure credentials and refresh in Power BI.
7. Validate totals against Rock UI and direct SQL.
8. Configure embed licensing and permissions if embedding. RockU notes embedded report licensing has cost and refers readers to the BI manual ([BI Embed Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report)).
9. Document refresh cadence and owner.

## 8. Data Views Deep Dive

### Choosing The Entity Type

The entity type is the first irreversible design choice. Pick the entity that represents one row of the desired result.

Use **Person** when each row should be a person.

Use **Group** when each row should be a group.

Use **Group Member** when each row should be a membership relationship.

Use **Attendance** when each row should be an attendance record.

Use **Financial Transaction** when each row should be a transaction.

Use **Financial Transaction Detail** when each row should be an account-level transaction detail.

Use **Data View** when each row should be a Data View.

Use **Report** when each row should be a Report.

Use **Page** or **Block** when building administrative finders.

The official manual says Data Views are not limited to people or groups and can be written for many Rock data types ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Agents should resist defaulting to Person. If the request is "families who gave," the row might be a family/giving group, not a person. If the request is "attendance by month," the row might be an attendance fact, not a person. If the request is "active small groups with leaders," the row might be a group, not a group member.

### Filter Tree Design

A maintainable Data View has a shallow, named mental structure:

- Root: all required business conditions.
- Nested "any" group: acceptable values for one field.
- Nested "all" group: compound subcondition.
- Related Data View filter: separate entity relationship logic.
- Exclusions: explicit and documented.

Example pattern:

- All:
  - Record Type is Person.
  - Record Status is Active.
  - Any:
    - Connection Status is Member.
    - Connection Status is Attendee.
  - Any:
    - Campus is A.
    - Campus is B.
  - Age Classification is Adult.

This shape is easy to explain, test, and reuse.

### Naming And Description

Good Data View names are stable and business-oriented:

- `People - Active Adult Members and Attendees`
- `Attendance - Weekend Services Last 8 Weeks`
- `Finance - Contribution Transactions Current Fiscal Year`
- `Groups - Active Small Groups With Public Finder Enabled`
- `Data Views - Reporting Admin Inventory`

Descriptions should include:

- Purpose.
- Inclusion criteria.
- Exclusion criteria.
- Owner.
- Intended Reports or pages.
- Date logic.
- Sensitive data warning.
- Version caveat if relevant.

### Categories And Ownership

A reporting category tree should answer "who owns this and where would an agent find it?"

Possible category layout:

- Reporting
  - Admin
  - Finance
  - Attendance
  - Groups
  - Kids
  - Care
  - Communications
  - BI
  - Deprecated
  - Experimental

Agents should not create new root categories casually. Match the organization's existing category taxonomy. If categories are chaotic, create a governance report first rather than reorganizing production assets blindly.

### Security

Data View security should be based on:

- Sensitivity of result set.
- Sensitivity of filter logic.
- Whether downstream Reports expose the data.
- Whether the Data View is used by group syncs, workflows, or public pages.
- Whether finance, minors, attendance, care, benevolence, or communications data is involved.

Use Rock's reporting-security training as the first citation, then verify the live Data View, Report, page, and block rules because each layer can expose or hide a different surface ([Reporting Security](https://community.rockrms.com/rocku/reporting/reporting-security)).

Operational checks:

- Verify who can view Data View results.
- Verify who can edit the Data View.
- Verify who can view dependent Reports.
- Verify who can access pages that render dependent Reports.
- Verify whether API endpoints expose Data View or Report records.
- Verify inherited category permissions.

### Related Data Views

Related Data View filters allow entity bridging. They are useful when a filter component exists for the relationship path, but they can be expensive and opaque.

Source examples show a common implementation pattern:

1. Resolve the referenced child Data View.
2. Evaluate child entity query.
3. Select keys from child entity.
4. Filter parent entity by matching keys.

The Attendance Data View filter for Person evaluates Attendance rows and maps back to Person through aliases ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)). Group/Location tests verify related Data View filters return groups with matching related locations and exclude groups without matching locations ([LocationDataViewDataFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs)). Step tests verify person filtering based on related Step Data Views ([StepDataViewDataFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs)).

When using related Data Views:

- Name both Data Views clearly.
- Test each child Data View independently.
- Test the parent Data View with known positive and negative examples.
- Inspect source or component description for join path.
- Avoid deep chains unless necessary.
- Monitor performance.
- Consider SQL or analytics tables if the relationship is too complex.

### Post-Filter Transformations

RockU includes "Post Filter Transformation" in reporting training ([RockU Reporting](https://community.rockrms.com/rocku/reporting)). The official reporting manual also includes a section on post-filter transformations ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Use these carefully because they can change what the Data View returns after base filtering.

Agents should verify in the live version:

- Which transformations are available.
- Whether they change entity type or record identity.
- Whether Reports built on the Data View expect transformed rows.
- Whether transformations affect caching/persistence.
- Whether the result is still suitable for group syncs or workflows.

### Data View Usage Before Editing

Before changing a shared Data View:

1. Open the Data View and inspect built-in usage references if available.
2. Query Reports where `DataViewId` equals the target.
3. Query other Data View Filters whose selection references the target Data View GUID/ID.
4. Query block settings for the Data View or dependent Report.
5. Query group sync configuration if relevant.
6. Query workflow/action settings if the Data View is used for automation.
7. Search Lava templates, SQL library, and repo files if the organization stores code externally.
8. Check last run and run count if available.

The official manual says the Data View page can show other Data Views, Reports, and group syncs using it ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Use that, but do not assume it catches every custom SQL, Lava, or plugin reference.

### Testing Data Views

Rock's own integration tests include a test that iterates all Data Views, builds queries with a database timeout, and evaluates IDs to ensure they execute ([DataViewTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs)). Agents can adapt that mindset operationally:

- Test every edited Data View after change.
- Test the result count.
- Test example included records.
- Test example excluded records.
- Test dependent Reports.
- Test page rendering.
- Test as intended user, not only admin.
- Capture elapsed time for expensive views.
- Check exception logs after test.
- Check database CPU if the query is large.

### Common Data View Anti-Patterns

**One giant Data View for everything**

Symptoms: deep nested filters, multiple related Data Views, unclear ownership, reused by many unrelated Reports.

Fix: split into named reusable Data Views with documented purpose.

**Report-specific business logic hidden in Data View name only**

Symptoms: Data View named "Active Leaders" but no description; filters include old ministry-specific assumptions.

Fix: add description, owner, and test cases.

**Using Person when the row should be family/giving group/group member**

Symptoms: duplicates, missing household context, inconsistent totals.

Fix: choose correct entity or use SQL/analytics tables.

**Any/all mistakes**

Symptoms: too many rows, zero rows, inconsistent inclusion.

Fix: redraw the filter tree in plain English, then rebuild groups.

Rock's official reporting manual and RockU training both make filter grouping a core Data View concept, so treat these anti-patterns as failures in documented Data View design rather than merely naming/style issues ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331), [Data View Filter Groups](https://community.rockrms.com/rocku/reporting/data-view-filter-groups)).

**Deep related Data View chains**

Symptoms: slow execution, timeouts, hard debugging.

Fix: simplify, materialize through analytics/persisted data, or use governed SQL.

**Editing shared Data Views without impact review**

Symptoms: unrelated reports change.

Fix: inspect usage references before editing; copy first if needed.

**Security only on page**

Symptoms: Report is hidden in nav but accessible via Tools > Reports or API.

Fix: secure Data View, Report, page, block, and SQL surfaces.

## 9. Reports Deep Dive

### What Reports Are Good At

Reports are best for row-based display over a Data View. Use Reports for:

- Staff lists.
- Exportable grids.
- Simple columns.
- Links to records.
- Attribute display.
- Basic calculated fields.
- Page-rendered Dynamic Reports.
- Workflow launch surfaces.
- Communication/action lists.

Reports are not ideal for:

- Multi-entity aggregate dashboards.
- Multi-row-per-entity rollups.
- Complex financial calculations.
- Window functions.
- Cross-year comparisons.
- Custom visualizations with strict client-side contracts.
- BI-grade executive analytics.

For these, consider Dynamic Data, SQL, analytics tables, or Power BI.

### Report Field Design

Each Report column should have a clear purpose. Avoid adding every available field. For operational reports, prioritize:

- Identity: name, ID, campus, category.
- Status: active/inactive, connection status, group status, approved/unapproved.
- Context: group, schedule, account, source, owner.
- Date: created, modified, last attended, transaction date, review date.
- Action: edit link, profile link, workflow launch, dashboard link.
- Verification: count or diagnostic fields for admin Reports.

RockU's Reports lesson is the right source for the Report layer; community Dynamic Report examples show why field order and column contracts become operational dependencies once reports are embedded or extended ([RockU Reports](https://community.rockrms.com/rocku/reporting/reports), [Dynamic Report Maps](https://community.rockrms.com/recipes/240)).

Use Lava fields sparingly and document them. A Lava column can solve display problems but can also hide business logic, create slow per-row execution, and complicate exports.

### Data View And Report Separation

Good separation:

- Data View: active adults at selected campuses.
- Report: name, campus, email, phone, age, connection status.

Bad separation:

- Data View: broad active people.
- Report field Lava: hide people not in selected campus.
- Result: UI count, export, workflow actions, and downstream filters may disagree.

Put inclusion/exclusion logic in the Data View when possible. Put presentation logic in Report fields.

### Dynamic Report Runtime Filters

Dynamic Report blocks can expose filter controls so staff can adjust Data View criteria at runtime. RockU notes a v7 capability around filtering multiple Data Views, not only the top-level Data View ([Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)). This is powerful, but it means the saved Data View is not always the exact executed query.

Troubleshooting runtime filters:

- Capture page URL and query string.
- Capture block settings.
- Capture current user.
- Capture selected filter values.
- Compare saved Data View count to Dynamic Report count.
- Inspect whether overrides use filter GUIDs.
- Inspect whether persisted values are ignored.
- Test with default filters and then with user-selected filters.

### Reports As Page Contracts

When Reports feed custom JavaScript, maps, exports, or integrations, the Report becomes an API contract. The Dynamic Report Maps recipe requires the first four visible columns to be in a specific order and includes latitude/longitude derived from address field parts ([Dynamic Report Maps](https://community.rockrms.com/recipes/240)). If another admin reorders or hides those columns, the map can break.

For reports used as contracts:

- Add a description warning.
- Add field names that make dependency clear.
- Restrict edit permissions.
- Add test instructions.
- Prefer a dedicated Report rather than reusing a staff-facing Report.
- Consider Dynamic Data with explicit SQL aliases for stable output.

### Report Security

Report security should be checked alongside:

- Data View security.
- Category security.
- Page security.
- Block security.
- Entity security.
- Export permissions.
- Lava/SQL permissions.
- BI embed permissions.

A staff member might not see Tools > Reports but still access a Dynamic Report page. Another might access a Report but not the underlying Data View editor. Another might export sensitive columns from a grid. Always test as the target role.

### Report Inventory And Governance

Large Rock instances accumulate many Reports. Community recipes describe real organizations with dozens or hundreds of reporting tools and the need for search/finder dashboards ([Reporting Dashboard](https://community.rockrms.com/recipes/397), [Data View Finder](https://community.rockrms.com/recipes/262)). Agents should propose governance once reporting sprawl appears.

Governance fields to track:

- Owner.
- Ministry.
- Status: active, deprecated, draft.
- Last reviewed.
- Sensitivity.
- Source Data View.
- Dependent pages.
- Validation method.
- Expected refresh cadence.
- Business definition.

## 10. Business Intelligence Deep Dive

### What BI Adds

Business Intelligence adds model-driven, visual, repeatable analysis. RockU describes BI as helping analyze data and present actionable information to leaders ([Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi)). The BI training sequence includes:

- BI Overview.
- BI Models.
- BI Template.
- BI Job.
- BI Financial Transaction Report.
- BI Attendance Report.
- BI Family Report.
- BI Embed Report.

These topics indicate a complete pipeline: model, template, scheduled job, domain reports, and embedding ([Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi)).

### Community Analytics Practice Signals

Approved Data Analytics Hub recordings add three practical signals to the official BI material:

- Treat analytics as a shared ministry practice, not just a tooling choice. A hub-style format lets churches compare dashboards, BI tools, ministry processes, attendance-flow models, and Rock connection workflows against real operating examples ([Data Analytics Hub launch](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Kmgx1xlRV)).
- A reporting layer can make Rock data easier to analyze without changing operational records. One community architecture uses extracted Rock and third-party data, SQL/dbt-style modeling, and Tableau reporting; a lighter version can keep reporting objects inside the Rock database while still pointing BI tools only at curated reporting tables or views ([North Point analytics presentation](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/2Rl3KLqlj4)).
- Start with Rock-native reporting when the output is operational, security-sensitive, or person-actionable. Move to BI when the question needs complex joins, third-party sources, high-level KPI analysis, or broader visual exploration; if BI is embedded back into Rock, page security and external BI licensing still both matter ([BI versus Rock panel](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz)).

### BI Model Layer

BI models should be treated as a curated reporting layer, not just raw tables. Before building a BI report:

- Identify the target model/fact/dimension tables.
- Confirm row grain.
- Confirm refresh process.
- Confirm date dimensions and campus dimensions.
- Confirm current vs historical dimension behavior.
- Confirm soft-deleted/archived/inactive handling.
- Validate totals against Rock UI.

The provided Model Map record identifies `Analytics Dim Campus` as a Reporting-category model ([Model Map](https://community.rockrms.com/ModelMap)). Community SQL examples also use analytics dimensions and facts for finance analysis ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391)).

### BI Job

RockU includes a BI Job training page ([BI Job](https://community.rockrms.com/rocku/business-intelligence-bi/bi-job)). The source pack does not provide the job settings, so agents must inspect the live Rock instance.

Inspect:

- Job name.
- Job type/class.
- Schedule.
- Last successful run.
- Last run duration.
- Exception logs.
- Attributes/settings.
- Target tables/models.
- Whether the job is enabled.
- Whether it conflicts with database maintenance or peak check-in windows.

### Power BI Template

Several BI RockU pages reference a Rock RMS v7 Power BI template file (`Rock RMS v7.pbit`) ([BI Template](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template), [BI Attendance Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report), [BI Family Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report), [BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)). Because this pack's references are public excerpts and may be old, verify:

- Current Rock BI manual.
- Current downloadable template.
- Rock version compatibility.
- Power BI Desktop version.
- Gateway or database connection method.
- Dataset refresh configuration.
- Authentication and least privilege.
- Whether the template's SQL expects old table names or columns.

### Embedded Reports

RockU's BI Embed Report page explicitly notes that embedded report licensing has cost and refers to the Rock BI manual for correct Power BI licensing ([BI Embed Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report)). Agents should never assume embedding is already licensed or permitted.

Verify:

- Power BI tenant licensing.
- Workspace permissions.
- Embed method.
- Whether viewers need Power BI licenses.
- Whether Rock page security matches Power BI report security.
- Whether row-level security is configured.
- Whether report URLs or tokens can leak.
- Whether cached screenshots or exports expose protected data.

### BI Finance Reports

Finance BI must align with finance definitions. The RockU BI series includes a financial transaction report topic ([BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)). Community examples show finance analysis can become complex, using analytics tables and explicit definitions for contribution type, current/prior giving, age bands, generational bands, and giving leaders ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391)).

Before publishing finance BI:

- Reconcile totals to Finance > Giving Analytics or equivalent local finance reports.
- Confirm registration payments included/excluded.
- Confirm pledge handling.
- Confirm refunds/reversals.
- Confirm account hierarchy.
- Confirm giving group logic.
- Confirm date basis.
- Confirm campus assignment.
- Confirm donor privacy.

### BI Attendance Reports

The BI series includes an Attendance Report topic ([BI Attendance Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report)). Attendance BI must define row grain and inclusion:

- Unique people or attendance events.
- Adults, children, volunteers, all attendees.
- Weekend service, ministry event, group attendance, check-in.
- Schedule and campus mapping.
- First-time vs returning.
- Date range and timezone.
- Did-not-attend records.

Validate attendance BI against a small known date/campus/service before trusting trends.

### BI Family Reports

The BI series includes a Family Report topic ([BI Family Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report)). Family BI must define:

- Family group type.
- Head of household logic.
- Giving leader logic if finance-related.
- Campus inheritance.
- Children/adults.
- Current vs historical household membership.
- Duplicate or merged records.
- Inactive or archived families.
- Address selection.

Community finance examples use family head-of-household analytics tables to connect giving units to person/family context ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349)).

## 11. Related Rock Areas: Sql, Model Map, Lava, Finance, Attendance

### SQL

SQL is the escape hatch for complex reporting. Use it when:

- The output requires aggregates.
- The output uses window functions.
- The output needs temporary tables or multi-step logic.
- The output unions multiple entity types.
- The output needs a specialized dashboard.
- A Data View would be too slow or too opaque.

Triumph's SQL window functions resource points to using SQL window functions for aggregates, ranking, and `LAG`-style analysis in complex reports ([SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions)). Treat that as a technique pointer, then write and test SQL against the local schema.

Triumph's grouping-sets resource adds a related reporting pattern: use SQL rollups when one report needs multiple aggregation levels, but label summary rows clearly and validate the syntax against the local Rock database before production use ([Grouping Sets](https://www.triumph.tech/resources/grouping-sets)).

Use SQL cautiously:

- Start read-only.
- Use parameters.
- Avoid string concatenation with user input.
- Add date bounds.
- Avoid `SELECT *`.
- Validate indexes and execution time.
- Avoid running heavy SQL during check-in or giving import windows.
- Do not write production data unless explicitly authorized.
- Remember direct SQL writes bypass Rock cache awareness; the Lava docs warn that cache manager will not know about direct SQL updates ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)).

### Model Map

Use Model Map to discover Rock's entity/model surface. The provided Model Map record identifies a reporting-category analytics model ([Model Map](https://community.rockrms.com/ModelMap)). Model Map is a starting point, not the final authority. For live work:

- Compare Model Map to installed schema.
- Inspect EF model/source for relationships.
- Inspect `INFORMATION_SCHEMA.COLUMNS` when writing SQL.
- Inspect foreign keys, indexes, and data volume.
- Prefer official model names and entity relationships over guessed table joins.

The SQL Model Map community recipe builds a searchable model/table reference using Lava and SQL, with strong security requirements: put it somewhere limited to users with SQL access, secure the page, and enable SQL/cache on an HTML block ([SQL Model Map QoL Reference](https://community.rockrms.com/recipes/526/sql-model-map-qol-reference)). Use that pattern only in admin contexts.

### Lava

Lava is used in Reports, Dynamic Data blocks, HTML content, emails, workflows, and pages. Reporting-related Lava surfaces include:

- Entity commands.
- SQL command.
- Web request command.
- Filters.
- Shortcodes.
- Report field Lava.
- Dynamic Data templates.
- Page title Lava on Dynamic Data blocks, according to reporting manual update notes ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

The SQL Lava command can return results into variables, use custom return names, run command statements, and in later versions use parameters/timeouts ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)). RockU also has a SQL Command training page ([RockU SQL Command](https://community.rockrms.com/rocku/lava/sql-command)).

Lava safety rules:

- Prefer entity commands when they satisfy the need.
- Use SQL only in secured blocks.
- Parameterize inputs where supported.
- Do not interpolate query string values into SQL.
- Avoid per-row heavy SQL in Report columns.
- Use caching intentionally.
- Document cache expiration.
- Avoid writes from page-rendered Lava unless explicitly approved.

### Finance

Finance reporting is high-risk because the same data can answer different business questions. A giving report may measure donors, giving units, transactions, transaction details, accounts, batches, or finance analytics facts. Community examples show finance SQL often uses analytics fact/dim tables and explicit current/prior date logic ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [SQL for Lapsed Givers](https://community.rockrms.com/recipes/109)).

Finance report checklist:

- Confirm transaction type value for contributions in the target instance.
- Confirm account inclusion.
- Confirm registration payments treatment.
- Confirm refunds/reversals.
- Confirm anonymous gifts.
- Confirm giving group/giving leader logic.
- Confirm date basis.
- Confirm campus logic.
- Confirm security.
- Confirm finance owner approval.

### Attendance

Attendance reports are often wrong because "attendance" is overloaded. Attendance may refer to:

- Check-in attendance.
- Group attendance.
- Service attendance.
- Volunteer attendance.
- Event registration attendance.
- Attendance occurrence.
- Unique attending people.
- Total attendance rows.
- Family attendance.
- First attendance.

The source-code Attendance Data View filter maps attendance rows to persons through `PersonAliasId` ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)). For attendance reports, always inspect alias joins and occurrence relationships.

Attendance report checklist:

- Define event/ministry.
- Define date range.
- Define schedules.
- Define campuses.
- Define group/group type.
- Define person inclusion.
- Define unique vs total.
- Confirm timezone.
- Confirm test date with known attendance.
- Validate against Rock UI.

## 12. Administration And Operational Guardrails

### Reporting Governance

A reporting ecosystem needs governance once staff depend on it.

Minimum governance:

- Category taxonomy.
- Naming convention.
- Owner field.
- Description requirement.
- Security review.
- Performance review.
- Deprecation process.
- Review cadence.
- Dashboard/finder for inventory.
- Change log for shared Data Views.

Community recipes for Data View Finder and Reporting Dashboard exist because real Rock instances accumulate enough reporting assets to need search and organization ([Data View Finder](https://community.rockrms.com/recipes/262), [Reporting Dashboard](https://community.rockrms.com/recipes/397)).

### Security Guardrails

Apply least privilege to:

- Tools > Data Views.
- Tools > Reports.
- Report categories.
- Data View categories.
- Dynamic Report pages.
- Dynamic Data pages.
- HTML blocks with SQL enabled.
- Lava SQL command usage.
- BI embed pages.
- Power BI workspace.
- SQL connection credentials.
- API access.

Special sensitivity:

- Finance.
- Children/minors.
- Attendance.
- Care/benevolence.
- Health or prayer details.
- Background check or security data.
- Giving and donor segmentation.
- Communications lists.

### Performance Guardrails

Reporting can affect production performance. Watch for:

- Deep nested related Data Views.
- Unbounded date ranges.
- Person Data Views over every person with multiple related filters.
- SQL with no date bounds.
- SQL using scalar functions per row.
- Cross applies over large fact tables.
- Lava SQL per row.
- Reports that export huge grids.
- BI refresh during peak hours.
- Missing or stale statistics.
- Parallel SQL issues.

A Triumph resource on MAXDOP describes troubleshooting high database CPU/worker usage where slow check-in and failed attendance saves were symptoms, and notes jobs, Data Views, and Reports were part of the investigation path ([What is MAXDOP](https://www.triumph.tech/resources/what-is-maxdop)). The operational takeaway is not "change MAXDOP first"; it is "reporting load can be part of database health and should be investigated with measured evidence."

Performance checklist:

- Capture execution time.
- Capture row count.
- Capture query plan for SQL reports.
- Check Data View run time.
- Check exception logs.
- Check database CPU during execution.
- Test outside peak ministry hours first.
- Add date/campus/account parameters.
- Prefer analytics tables for heavy historical analysis.
- Use caching where appropriate.
- Retire unused heavy reports.

### Database Maintenance

A community Azure SQL maintenance recipe notes that Rock's Database Maintenance job runs nightly and warns against blindly accepting Azure index suggestions because Rock maintains indexes as needed; it discusses index/statistics maintenance as performance context ([How to Maintain your Azure SQL Database](https://community.rockrms.com/recipes/259)). Treat this as community guidance requiring DBA review.

For reporting performance, inspect:

- Rock Database Maintenance job status.
- SQL statistics recency.
- Fragmentation where relevant.
- Long-running queries.
- Blocking.
- Query Store if enabled.
- Database tier/resource utilization.
- BI job schedule.
- Check-in and giving windows.

### Change Control

Before changing a shared reporting asset:

1. Snapshot current definition.
2. List dependencies.
3. Test copy if possible.
4. Validate result count.
5. Validate known included/excluded records.
6. Validate dependent Reports.
7. Validate security as target user.
8. Communicate owner approval.
9. Record change.

Never edit a widely used Data View during a live event without a rollback plan.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Data Filter Components

Data filter components are code classes that know how to build query expressions. Source snippets show components exported as `DataFilterComponent` with metadata names and entity type GUIDs, such as the Attendance Data View filter ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)).

Agents should inspect component source when:

- UI label is unclear.
- Related Data View behavior is unexpected.
- A filter fails after upgrade.
- A Data View returns too many/few rows.
- A plugin filter component is involved.

### `DataViewFilter.Logic`

The logic file builds expressions from filter definitions and throws exceptions for invalid metadata or missing components ([DataViewFilter.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs)). This explains why Data View failures may show as component/entity resolution errors rather than SQL errors.

Troubleshooting source-code landmarks:

- `ExpressionType`.
- `EntityTypeId`.
- Component lookup.
- `Selection` deserialization.
- Child filter recursion.
- Filter overrides.

### Obsidian Filter Bags

Rock's newer UI surfaces serialize filter trees into bags for Obsidian controls. Source snippets define `DataViewFilterBag` with GUID, expression type, component data, and child filters in TypeScript and C# ([dataViewFilterBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Reporting/dataViewFilterBag.d.ts), [DataViewFilterBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Reporting/DataViewFilterBag.cs)).

Operational meaning:

- UI editing may transform filter data between server model and client bag.
- If a filter UI fails, inspect API payloads and component data.
- GUIDs are important for overrides.
- Component data is serialized as strings; type conversion bugs can happen.

### Save Hooks And Cache

`DataViewFilter.SaveHook` clears filter cache by parent ID after relevant changes ([DataViewFilter.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs)). This supports the operational point that Data View filter structure is cached and should invalidate on changes. If results look stale after direct database edits, use Rock UI saves or cache-clearing procedures rather than assuming the database row change is enough.

### Tests As Operational Models

Rock integration tests verify that Data Views can execute and that related Data View filters return expected records ([DataViewTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs), [LocationDataViewDataFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs), [StepDataViewDataFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs)). Agents can borrow the testing style even without running the test suite:

- Iterate the target Data Views.
- Build query.
- Execute with timeout.
- Record count/time.
- Capture exceptions.
- Validate positive/negative fixtures.

### API And Entity Commands

The source snippets indicate models such as `DataViewFilter` are code-generated for REST (`CodeGenerateRest`) ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)). Lava entity commands can query entities and are used in community reporting dashboard snippets to retrieve accessible Reports and Data Views ([Reporting Dashboard](https://community.rockrms.com/recipes/397)). Verify current API security before using REST or entity commands for reporting inventory.

## 14. Reporting, Analytics, And Model Map

### Reporting Strategy

RockU begins its reporting section with strategy, then moves through Data Views, Reports, security, other options, and Dynamic Report blocks ([RockU Reporting](https://community.rockrms.com/rocku/reporting)). A good reporting strategy should answer:

- Who owns reporting?
- Which decisions do reports support?
- Which domains need governed definitions?
- Which reports are official?
- Which reports are exploratory?
- Which data is sensitive?
- Which assets are reusable?
- Which assets are deprecated?
- Which outputs need BI?

### Analytics Tables vs Transactional Tables

Use transactional tables for operational precision and analytics tables for reporting efficiency when definitions match.

Transactional table examples:

- Person.
- Group.
- Attendance.
- FinancialTransaction.
- FinancialTransactionDetail.

Analytics model examples from source pack:

- `AnalyticsFactFinancialTransaction`.
- `AnalyticsDimPersonCurrent`.
- `AnalyticsDimFamilyHeadOfHousehold`.
- `AnalyticsDimFamilyCurrent`.
- `Analytics Dim Campus`.

Community SQL examples use analytics tables for finance summaries and household/giving leader context ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391)). Model Map identifies analytics campus as reporting category metadata ([Model Map](https://community.rockrms.com/ModelMap)).

### Metrics And Measurement Classifications

The official reporting manual update notes mention Measurement Classifications in Rock 17.0 as defining metric purposes and helping Rock interpret metric data ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). The source pack does not provide details beyond that, so agents should inspect current documentation and live settings.

For metric reporting, verify:

- Metric definition.
- Measurement classification.
- Source value type.
- Schedule/frequency.
- Campus/entity partitioning.
- Manual vs automated entry.
- Historical changes.
- Dashboard usage.

### Model Discovery Process

When a report requires unfamiliar data:

1. Search the Rock UI for the feature's admin pages.
2. Inspect Model Map for candidate models.
3. Inspect source code for model names and relationships.
4. Inspect live schema columns.
5. Inspect sample rows.
6. Find how Rock UI retrieves/displays the same data.
7. Build a small query.
8. Validate against UI.
9. Only then build the report.

The SQL Model Map recipe shows the value of a searchable table/column reference, but it also emphasizes securing such a tool to SQL-capable admins ([SQL Model Map QoL Reference](https://community.rockrms.com/recipes/526/sql-model-map-qol-reference)).

## 15. Version And Release Caveats

### Rock Version Matters

Reporting behavior changes across Rock versions. The official reporting manual includes update notes from early versions through 18.1, including Dynamic Report block documentation, Dynamic Data block setting changes, Data View caching logic in Rock 17.0, and Measurement Classifications ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)).

Before making assertions, inspect:

- Installed Rock version.
- Current reporting manual for that version.
- Release notes.
- Block type version: Web Forms vs Obsidian.
- Plugin versions.
- Database schema.

### Dynamic Report Filtering

RockU's Dynamic Report Block page notes a v7 caveat about filtering on multiple Data Views rather than only the top-level Data View ([Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)). For current instances, verify the block settings and behavior live.

### Lava SQL Parameters And Timeout

The Lava SQL docs identify SQL parameters as a v9.0 feature and timeout as a v12.0 feature ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)). For older versions, do not assume parameter or timeout support. For newer versions, still verify syntax in the installed docs.

### Data View Caching

Rock 17.0 update notes mention implemented caching logic in Data Views ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331)). Source snippets from `develop` show cache clearing for filter parent IDs and override support for ignoring persisted values ([DataViewFilter.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs), [DataViewFilterOverrides.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilterOverrides.cs)). Verify the target version's actual cache/persistence behavior.

### BI Template Version

RockU BI pages reference a `Rock RMS v7.pbit` template ([BI Template](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template)). Do not assume that template is current for a modern instance. Verify current BI manual and downloadable template.

### Analytics Source Giving Unit

A Triumph resource says a new table in version 12.5 improves giving analytics by avoiding slower query functions ([Giving Unit Analytics](https://www.triumph.tech/resources/giving-unit-analytics)). Because the provided hydration lacks detail, verify exact table name, schema, and release notes in the live instance before using it.

### Source Code Branch Caveat

The source snippets are from `SparkDevNetwork/Rock` `develop`. They are useful for architecture but may differ from a production instance running a released version. When exact behavior matters, inspect the tag/branch matching the installed Rock version.

## 16. Implementation Playbooks

### Playbook A: Create A New Data View And Report

1. Write the business question.
2. Identify the row entity.
3. Search existing Data Views.
4. If an existing Data View matches exactly, reuse it.
5. If an existing Data View almost matches but has other dependencies, copy it.
6. Create a clear name and description.
7. Place it in the right category.
8. Build filter tree with all/any groups.
9. Test count and sample records.
10. Create Report.
11. Add only needed fields.
12. Add links/actions if required.
13. Secure Data View and Report.
14. Place on Dynamic Report page if needed.
15. Test as target user.
16. Record owner and review date.

Use the official Data View and Report lessons as the baseline process, then check Dynamic Report behavior only if the output is being published through a block/page ([Data View Overview](https://community.rockrms.com/rocku/reporting/data-view-overview), [RockU Reports](https://community.rockrms.com/rocku/reporting/reports), [Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)).

### Playbook B: Fix A Data View Returning Too Many Rows

1. Capture expected definition.
2. Capture actual row count.
3. Identify example row that should be excluded.
4. Inspect root filter group expression.
5. Inspect nested any/all groups.
6. Inspect related Data View filters independently.
7. Inspect runtime overrides if executed through a Dynamic Report.
8. Check whether persisted/cached results are stale.
9. Modify a copy first if shared.
10. Validate excluded example is gone.
11. Validate included examples remain.

### Playbook C: Fix A Data View Returning Zero Rows

1. Identify whether any individual filter returns rows.
2. Check mutually exclusive filters in an all group.
3. Check date ranges and timezone.
4. Check deleted referenced values.
5. Check entity type mismatch.
6. Check related Data View child results.
7. Check filter component after upgrades.
8. Check security if results differ by user.
9. Check exception logs.
10. Rebuild filters one at a time.

### Playbook D: Build A Finance Giving Report

1. Get finance owner's definition.
2. Define transaction types.
3. Define account scope.
4. Define date basis.
5. Define campus basis.
6. Define giving unit logic.
7. Decide Data View/Report vs SQL/BI.
8. If using SQL, start with read-only direct query.
9. Validate totals against trusted finance report.
10. Add parameters.
11. Secure to finance-approved roles.
12. Document exclusions such as registration payments.
13. Schedule review.

Community finance examples show why this rigor matters: giving by age/generation analysis uses analytics transaction facts and family/head-of-household dimensions, not just a simple transaction grid ([Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391)).

### Playbook E: Build An Attendance Report

1. Define attendance domain.
2. Define row grain.
3. Define unique vs total.
4. Define schedules and campuses.
5. Define date range.
6. Define person population.
7. Choose Data View/Report, SQL, or BI.
8. Validate with a known date/service.
9. Check alias joins.
10. Secure if minors are included.
11. Document assumptions.

The source-code Attendance Data View filter reinforces that person attendance filters may join through aliases ([AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs)).

### Playbook F: Build A Reporting Inventory Dashboard

1. Inventory Reports.
2. Inventory Data Views.
3. Inventory pages with Dynamic Report blocks.
4. Inventory pages with Dynamic Data blocks.
5. Inventory embedded Power BI pages.
6. Include category, owner, description, security, route, created date, modified date, last run if available.
7. Respect current user access.
8. Add search and type filters.
9. Add "favorite" or recent-viewed only after validating interaction tracking.
10. Secure admin version separately from staff version.

Community examples include a Reporting Dashboard and Reporting Tool Finder that centralize report discovery ([Reporting Dashboard](https://community.rockrms.com/recipes/397), [Reporting Tool Finder](https://community.rockrms.com/recipes/264)).

### Playbook G: Retire A Report Or Data View

1. Identify owner.
2. Inspect usage references.
3. Check last run/interaction if available.
4. Search pages/blocks/workflows/Lava/SQL.
5. Rename with deprecated prefix or move to deprecated category.
6. Wait through review window.
7. Remove page links.
8. Delete only after dependencies are cleared.
9. Keep a record of what replaced it.

Do not delete `DataViewFilter` rows directly. Source comments warn filters are used outside Data Views, including content channel filters and registration group placement ([DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs)).

## 17. Troubleshooting Decision Tree

### Symptom: Report Shows No Rows

Check:

1. Does the underlying Data View show rows in Tools > Data Views?
2. Does the current user have permission?
3. Does the Report reference the intended Data View?
4. Are runtime filters applied on the Dynamic Report block?
5. Are date filters relative to today/timezone?
6. Did a referenced category/value/group/campus get deleted?
7. Does a related child Data View return rows?
8. Did a filter component fail after upgrade?
9. Are cached/persisted results stale?
10. Is there an exception in logs?

Start with the Data View result set, then move outward to Report and Dynamic Report block context because Rock documents those as separate reporting surfaces ([Data View Overview](https://community.rockrms.com/rocku/reporting/data-view-overview), [RockU Reports](https://community.rockrms.com/rocku/reporting/reports), [Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block)).

### Symptom: Report Shows Too Many Rows

Check:

1. Any/all filter groups.
2. Missing active/deceased/archived exclusions.
3. Person vs group member row grain.
4. Related Data View join path.
5. Runtime filter overrides.
6. Report field filtering hidden in display.
7. Duplicate rows from one-to-many relationships.
8. Security: admin sees more than target user.
9. Date bounds.
10. Campus/account scope.

### Symptom: Report Is Slow

Check:

1. Data View execution time.
2. Deep related Data View chains.
3. Unbounded date ranges.
4. Large exports.
5. Lava per-row logic.
6. SQL scans.
7. Missing date/campus/account filters.
8. Analytics table alternative.
9. Database CPU/worker pressure.
10. Maintenance/statistics health.

The MAXDOP resource is an example of database-level investigation after checking jobs, Data Views, and Reports during performance symptoms ([What is MAXDOP](https://www.triumph.tech/resources/what-is-maxdop)).

### Symptom: Dynamic Report Differs From Data View Editor

Check:

1. Block runtime filters.
2. Multiple Data View filter capability in the block/version.
3. Query string parameters.
4. Current user security.
5. Persisted value usage.
6. Data View filter overrides.
7. Report columns with conditional Lava.
8. Page-specific context.
9. Cached block output.
10. Export vs grid settings.

### Symptom: BI Dashboard Is Wrong

Check:

1. BI job last success.
2. Dataset refresh time.
3. Power BI credentials.
4. Model/table version compatibility.
5. Date/campus filters.
6. Row-level security.
7. Rock UI reconciliation.
8. Analytics table refresh.
9. Current vs historical dimensions.
10. Template version.

### Symptom: Lava SQL Report Is Unsafe

Check:

1. SQL enabled on block.
2. Page/block security.
3. User input interpolation.
4. Parameter use.
5. Timeout use.
6. Write statements.
7. Cache flush after writes.
8. PII/finance/minor exposure.
9. Error output leaking SQL.
10. Audit trail.

Rock's Lava SQL docs explicitly warn about SQL injection and direct SQL write/cache implications ([SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands)).

### Symptom: Data View Fails After Upgrade

Check:

1. Installed Rock version.
2. Filter component entity type exists.
3. Plugin installed/enabled.
4. Selection string deserializes.
5. Referenced IDs/GUIDs still exist.
6. Obsidian component data migration.
7. Cache invalidation.
8. Exception logs.
9. Source-code changes between versions.
10. Rebuild filter on a copy if necessary.

## 18. Agent Task Recipes

### Recipe: Answer "What Does This Report Actually Show?"

1. Find the Report.
2. Record Report ID, name, category.
3. Open its Data View.
4. Translate filter tree into plain English.
5. List Report columns.
6. Inspect Dynamic Report block if page-rendered.
7. Run count as admin and target user.
8. Identify sensitive fields.
9. Cite dependent Data Views.
10. Return a concise definition and caveats.

### Recipe: Answer "Can I Change This Data View?"

1. Find Data View.
2. Inspect usage panel.
3. Query dependent Reports.
4. Query dependent Data View filters.
5. Query blocks/pages.
6. Query group syncs/workflows if relevant.
7. Check last run/count.
8. Identify owner.
9. Recommend edit, copy, or deprecate.
10. Do not change until owner/risk is clear.

### Recipe: Build "People Who Attended X But Not Y"

1. Create child Attendance Data View for X.
2. Create child Attendance Data View for Y.
3. Create Person Data View using related Attendance Data View filter for X.
4. Add exclusion for people related to Y if supported.
5. Verify alias behavior.
6. Test known people.
7. If Data View cannot express exclusion cleanly, use SQL with `PersonAlias`.
8. Validate against attendance UI.

### Recipe: Build "Lapsed Givers"

1. Get finance definition of lapsed.
2. Define annual amount threshold.
3. Define current inactivity window.
4. Define prior comparable period.
5. Exclude registration payments if required.
6. Use analytics tables or SQL if comparing periods.
7. Validate with finance owner.
8. Secure report.
9. Document date logic.

Community lapsed giver and giving age-band recipes show this category often requires SQL and explicit period comparison ([SQL for Lapsed Givers](https://community.rockrms.com/recipes/109), [Report on Giving by Age Bands](https://community.rockrms.com/recipes/349)).

### Recipe: Build "Where Are Our Reporting Tools?"

1. Create admin inventory page.
2. Include Reports and Data Views.
3. Include pages with Dynamic Report blocks.
4. Include pages with Dynamic Data blocks.
5. Include embedded BI pages.
6. Add search.
7. Include route, category, owner, description.
8. Respect security or clearly label admin-only.
9. Add review status.
10. Use community finder recipes as patterns, not direct production code ([Reporting Dashboard](https://community.rockrms.com/recipes/397), [Reporting Tool Finder](https://community.rockrms.com/recipes/264)).

### Recipe: Validate A BI Finance Dashboard

1. Identify dashboard filters.
2. Identify source model/table.
3. Check BI job last success.
4. Check Power BI dataset refresh.
5. Run Rock UI finance report for same dates/accounts.
6. Run direct read-only SQL if needed.
7. Compare totals.
8. Investigate differences by transaction type, account, campus, refunds, registration payments, and giving group.
9. Document reconciliation.
10. Get finance owner signoff.

### Recipe: Audit Reporting Security

1. List Data Views by category.
2. List Reports by category.
3. List Dynamic Report pages.
4. List Dynamic Data pages.
5. List HTML blocks with SQL enabled.
6. List BI embed pages.
7. Test as representative users.
8. Flag finance/minor/care/attendance reports.
9. Verify exports.
10. Produce remediation list.

### Recipe: Diagnose Slow Reporting

1. Identify exact report/page.
2. Measure load time.
3. Measure Data View execution time.
4. Check row count.
5. Inspect filters.
6. Check SQL/Lava columns.
7. Check related Data Views.
8. Check database CPU/worker waits.
9. Test with narrower date range.
10. Recommend Data View simplification, caching, analytics table, SQL optimization, or BI.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `556`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | operational_guidance | Data Views should be treated as reusable record-set definitions: they answer which records qualify before a Report, Dynamic Report block, workflow, or other consumer decides how to display or act on those records. | [source](https://community.rockrms.com/rocku/reporting/data-view-overview) |
| rocku-confirmed | operational_guidance | Data integrity work should start from the exact entity and field being corrected, then identify the owner, source of truth, duplicate risk, and reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| rocku-confirmed | operational_guidance | People and reporting guides should distinguish cleanup, merge, verification, and governance tasks because each has different audit and permission requirements. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| rocku-confirmed | operational_guidance | Before changing a Data View, identify its entity type, filter tree, category, persistence behavior, and downstream consumers so a reporting fix does not break reports, syncs, or automations. | [source](https://community.rockrms.com/rocku/reporting/data-view-overview) |
| rocku-confirmed | operational_guidance | For reporting agents, data integrity issues should be surfaced as source-data problems, not hidden by report logic that masks duplicates, missing values, or stale attributes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| rocku-confirmed | source_summary | Data View Overview strengthens the reporting guide by reinforcing Data Views as reusable qualifying-record definitions whose filters, persistence, and consumers must be checked before edits. | [source](https://community.rockrms.com/rocku/reporting/data-view-overview) |
| rocku-confirmed | source_summary | Data Integrity adds operational guidance for cleanup and reporting quality: define correction rules, test known examples, and document ownership before data changes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| rocku-confirmed | source_summary | Data Integrity adds guidance for people and reporting work: prove the source of truth, understand cleanup ownership, and verify downstream reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| rocku-confirmed | operational_guidance | For AI, automation, and responsible tool use, BI Financial Transaction Report should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report) |
| rocku-confirmed | operational_guidance | The Extending Groups RockU lesson provides training context for ministry process design; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/extending-groups) |
| rocku-confirmed | operational_guidance | For reporting, analytics, and measurement, Rock Media Analytics should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/cms/rock-media-analytics) |
| rocku-confirmed | operational_guidance | The Pledges RockU lesson provides training context for reporting, analytics, and measurement; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/pledges) |
| More |  | 544 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `76`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Assign Statement Transcript Insight](https://community.rockrms.com/rocku/lava/assign-statement) | approved_for_public_distillation | 1 | media-insight:446c751591a992b1 |
| [Attendance Analytics Transcript Insight](https://community.rockrms.com/rocku/check-in/attendance-analytics) | approved_for_public_distillation | 3 | media-insight:e066ef3153b2cc3d |
| [BI Attendance Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report) | approved_for_public_distillation | 1 | media-insight:b32a4e808360fabc |
| [BI Embed Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report) | approved_for_public_distillation | 3 | media-insight:5fc8b3a315612c59 |
| [BI Family Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report) | approved_for_public_distillation | 3 | media-insight:26c55120b777db34 |
| [BI Financial Transaction Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report) | approved_for_public_distillation | 3 | media-insight:a815728575995f92 |
| [BI Job Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-job) | approved_for_public_distillation | 2 | media-insight:1783ed2aacc57cc3 |
| [BI Models Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-models) | approved_for_public_distillation | 3 | media-insight:10e310226ed0945a |
| More |  | 68 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

### Official And Training Sources

- [RockU Reporting](https://community.rockrms.com/rocku/reporting): reporting strategy, Data Views, filter groups, Reports, security, other options, and Dynamic Report blocks.
- [Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6/331): official reporting manual, Data View configuration, categories, usage references, Dynamic Data updates, Data View caching, measurement classifications, version notes.
- [RockU Reports](https://community.rockrms.com/rocku/reporting/reports): Report training topic.
- [Dynamic Report Block](https://community.rockrms.com/rocku/reporting/dynamic-report-block): Dynamic Report training and v7 filtering caveat.
- [SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands): SQL command behavior, return variables, command statements, injection warning, parameters, timeout, cache caveat.
- [RockU SQL Command](https://community.rockrms.com/rocku/lava/sql-command): training example for SQL Lava.
- [Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi): BI training sequence.
- [BI Overview](https://community.rockrms.com/rocku/business-intelligence-bi/bi-overview), [BI Models](https://community.rockrms.com/rocku/business-intelligence-bi/bi-models), [BI Template](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template), [BI Job](https://community.rockrms.com/rocku/business-intelligence-bi/bi-job), [BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report), [BI Attendance Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report), [BI Family Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report), [BI Embed Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report): BI topic coverage; exact implementation details must be verified in current BI manual and live Rock/Power BI configuration.

### Source-Code Landmarks

- [DataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs): filter model, expression type, parent, component entity type, selection, note about non-Data-View uses.
- [DataViewFilter.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs): expression generation and error behavior.
- [DataViewFilter.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs): cache clearing after filter changes.
- [DataViewGetQueryArgs.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewGetQueryArgs.cs): query context, sort, overrides, timeout.
- [DataViewFilterOverrides.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilterOverrides.cs): filter overrides, ignore persisted values, statistics flag.
- [AttendanceDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs): Person filtering from Attendance Data View through aliases.
- [LocationDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs): Group filtering from Location Data View.
- [GroupTypeDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/GroupTypeDataViewFilter.cs): Group filtering from Group Type Data View.
- [BenevolenceResultDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/BenevolenceRequest/BenevolenceResultDataViewFilter.cs): related Data View pattern for benevolence.
- [ConnectionRequest PersonDataViewFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/PersonDataViewFilter.cs): connection request matching to requester person Data View.
- [DataViewTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs): all-Data-Views execution test pattern.
- [LocationDataViewDataFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs): related Data View test pattern for group locations.
- [StepDataViewDataFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs): related Data View test pattern for person steps.
- [DataViewFilterBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Reporting/DataViewFilterBag.cs) and [dataViewFilterBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Reporting/dataViewFilterBag.d.ts): Obsidian serialized filter tree shape.

### Community And Partner Pattern Sources

- [Reporting Dashboard](https://community.rockrms.com/recipes/397): pattern for centralizing Reports, Data Views, dynamic report pages, and Power BI report pages.
- [Data View Finder](https://community.rockrms.com/recipes/262): pattern for searching and reviewing Data Views.
- [Reporting Tool Finder](https://community.rockrms.com/recipes/264): pattern for finding Reports, Dynamic Reports, Dynamic Data blocks, Power BI reports, and custom tools.
- [Dynamic Report Maps](https://community.rockrms.com/recipes/240): pattern showing Report column contracts and Dynamic Report client-side extension.
- [Report on Giving by Age Bands](https://community.rockrms.com/recipes/349), [Giving by Generational Age Bands](https://community.rockrms.com/recipes/391), [SQL for Lapsed Givers](https://community.rockrms.com/recipes/109), [SQL: Givers by Amount and Monthly Consistency](https://community.rockrms.com/recipes/206): finance SQL examples that illustrate when standard Data Views may not be enough.
- [Room Management Daily Email Reports](https://community.rockrms.com/recipes/198): reporting delivery pattern through workflow/email/PDF, with plugin prerequisites to verify.
- [SQL Model Map QoL Reference](https://community.rockrms.com/recipes/526/sql-model-map-qol-reference): model/table discovery pattern requiring strict admin security.
- [Giving Unit Analytics](https://www.triumph.tech/resources/giving-unit-analytics): partner note about faster giving analytics in v12.5; verify live schema and release notes.
- [Release Notes](https://www.rockrms.com/releasenotes): official release-history source to confirm version-specific reporting, analytics, Dynamic Data, and Data View behavior.
- [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions): partner technique pointer for advanced SQL reporting.
- [Grouping Sets](https://www.triumph.tech/resources/grouping-sets): partner technique pointer for multi-level SQL rollups in reporting.
- [What is MAXDOP](https://www.triumph.tech/resources/what-is-maxdop): partner performance-troubleshooting context involving database CPU and reporting workloads.
- [ONE-ALL-Church/Rock-SQL-Library](https://github.com/ONE-ALL-Church/Rock-SQL-Library): public SQL example repository; license and compatibility must be reviewed before reuse.

### Dependencies On Other Guides

This guide depends on deeper domain guides for:

- **SQL**: query safety, indexing, parameters, Query Store, performance, read-only audit posture.
- **Model Map**: model discovery, entity relationships, schema verification.
- **Lava**: entity commands, SQL command, filters, security, caching.
- **Finance**: transaction model, giving groups, accounts, batches, refunds, pledge, donor privacy.
- **Attendance**: attendance occurrence model, person aliases, schedules, check-in, groups, campuses.

These dependencies reflect Rock's own reporting source split: official reporting docs cover report construction, while SQL/Lava, BI, model discovery, finance, and attendance sources define the domain-specific meaning of the data being reported ([RockU Reporting](https://community.rockrms.com/rocku/reporting), [SQL Lava command](https://community.rockrms.com/lava/commands/sql-commands), [Business Intelligence BI](https://community.rockrms.com/rocku/business-intelligence-bi), [Model Map](https://community.rockrms.com/ModelMap)).

When a reporting task crosses one of these domains, use the domain guide plus this reporting guide. Reporting is the delivery layer; the domain guide defines the business meaning.
