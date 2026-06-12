---
id: authored-developer-resources
title: Rock Developer Resources
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Rock Developer Resources

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Rock Developer Resources index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock Developer Resources is not a single documentation area. It is a layered ecosystem for building, extending, packaging, migrating, testing, and operating custom Rock RMS functionality. The official developer landing page organizes the path as Quickstart, Developer 101, Developer 202, Developer 303, then specialized books for Developer Codex, Obsidian, Helix, AI Agents, Mobile, Apple TV, Roku, packaging, Slingshot migration, and utility references such as Dynamic LINQ, Rock Branches, RealTime Visualizer, SQL Style Guide, and release notes ([Developer Resources](https://community.rockrms.com/developer)).

For an agent doing real Rock work, the core mental model is:

1. Use **Quickstart** and **Developer 101** when the work is about blocks, block settings, page placement, input, security, entity load/save, validation, grids, breadcrumbs, dates, files, person aliases, and the older WebForms-style developer path ([Quickstart Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks), [Developer 101](https://community.rockrms.com/developer/101---launchpad)).
2. Use **Developer 202** when custom persistent data is involved: custom models, services, Entity Framework, migrations, plugin schema, and system data setup ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data), [The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)).
3. Use **Developer 303** when the request moves beyond blocks into jobs, workflow actions, data view filters, REST API usage, security, logging, RealTime, performance, communication transports, and advanced extension points ([Developer 303](https://community.rockrms.com/developer/303---blast-off), [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)).
4. Use **Developer Codex** as the standard of record for coding standards, naming, service layer boundaries, migrations, generated code, security posture, compatibility, testing, peer review, hotfixes, and Obsidian conversion practices ([Developer Codex](https://community.rockrms.com/developer/developer-codex), [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards)).
5. Use **Obsidian** when the UI is modern Rock web UI: C# block classes, TypeScript components, block actions, generated bags, grids, field types, `.obs` files, security grants, and plugin development tooling ([Obsidian](https://community.rockrms.com/developer/obsidian), [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks), [Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)).
6. Use **Helix** when the extension should be Lava/HTMX driven instead of C#/Obsidian: Lava Applications, Lava Endpoints, HTMX partial updates, form controls, loading states, endpoint security, observability, and Magnus workflows ([Helix Overview](https://community.rockrms.com/developer/helix/overview), [Helix Security](https://community.rockrms.com/developer/helix/overview/security)).
7. Use **AI Agents** when building Rock-native agent instructions, skills, context anchors, Lava tools, native tools, tool parameters, and debugging support ([AI Agents](https://community.rockrms.com/developer/ai-agents)).
8. Use **Mobile, Apple TV, and Roku docs** when the target surface is not the standard web UI. These platforms have their own shells, page models, markup languages, app settings, authentication flows, media behavior, and publishing requirements ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs), [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Roku Docs](https://community.rockrms.com/developer/roku-docs)).
9. Use **release notes and source code** to resolve version-specific behavior. Developer docs may be drafts or work in progress; release notes and source snippets often reveal what actually shipped in v17, v18, v19, or the current `develop` branch ([Release Notes](https://www.rockrms.com/releasenotes), [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
10. Use **Model Map, API docs, Dynamic LINQ, RealTime Visualizer, and SQL Style Guide** as operational references when inspecting live data, building filters, diagnosing event channels, writing migrations, or choosing entity properties ([Model Map](https://community.rockrms.com/ModelMap), [API Documentation](https://community.rockrms.com/api-docs), [Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax), [RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer), [SQL Style Guide](https://community.rockrms.com/developer/sql-style-guide)).

The guide should be treated as a draft synthesis. Before making production changes, inspect the live Rock instance for installed Rock version, installed plugins, enabled feature flags, actual block types, block attributes, page routes, security rules, Lava commands, jobs, workflows, and schema. When source material is thin or draft-labeled, this guide calls out what must be verified.

## 2. Scope And Terminology

This guide covers the developer-facing resources around Rock RMS customization and extension. It is not a replacement for the end-user manuals or admin books. It focuses on how an agent should reason about development work: what source to trust, which subsystem owns the behavior, what configuration fields matter, what database entities are likely involved, and what live checks prevent false confidence.

**Rock RMS** is the open-source church management, CMS, relationship management, and application platform maintained by Spark Development Network ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). In developer work, "Rock" can mean the running web application, the database schema, the source repository, the official community documentation, the mobile shell, TV app shells, or plugin ecosystem. Always clarify which layer is being changed.

**Block** means a unit of UI/functionality placed on a Rock page, layout, or site. Older blocks are commonly WebForms `.ascx` blocks. Newer blocks are often Obsidian blocks with a server C# class and a client TypeScript component ([Developer 101](https://community.rockrms.com/developer/101---launchpad), [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

**Obsidian** is Rock's modern web UI development pattern. It separates the C# server block, TypeScript client component, and block actions that allow browser-side interactions to call server logic ([Obsidian](https://community.rockrms.com/developer/obsidian), [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

**Helix** is the Lava/HTMX application model. It brings HTMX, Lava Applications, Lava Commands, and control shortcodes together for dynamic Rock web development without requiring full C#/Obsidian work ([Helix Overview](https://community.rockrms.com/developer/helix/overview)). Source records and release snippets indicate Helix moved from plugin/beta status into core in the v18 era, but live instances may still have plugin remnants or version-specific path differences ([Helix FAQ](https://community.rockrms.com/developer/helix/overview/faq), [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)).

**Lava Application** is a Helix concept for grouping Lava-driven application behavior. Source snippets show a `LavaApplication` model with fields such as `Name`, `Description`, `IsSystem`, `IsActive`, `SecurityMode`, `Slug`, `AdditionalSettingsJson`, and `ConfigurationRiggingJson` in the v18 migration path ([AddLavaApplications source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)). The Obsidian generated view model exposes related client-facing fields such as `attributes`, `attributeValues`, `configurationRigging`, `description`, `idKey`, `isActive`, `name`, and `slug` ([lavaApplicationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts)).

**Lava Endpoint** is a Helix endpoint surface. Source snippets show endpoint fields for `cacheControlHeaderSettings`, `codeTemplate`, `enableCrossSiteForgeryProtection`, `enabledLavaCommands`, `httpMethod`, `isActive`, rate limit duration/request settings, `securityMode`, and `slug` ([lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)). Security modes include Endpoint Execute, Application View, Application Edit, and Application Administrate ([lavaEndpointSecurityMode.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)). HTTP methods include GET, POST, PUT, and DELETE ([lavaEndpointHttpMethod.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointHttpMethod.ts)).

**Plugin** means deployable custom code and assets packaged for Rock. Plugin work may involve WebForms blocks, Obsidian blocks, handlers, migrations, system data, and packaging. Obsidian plugin development is documented around `rock-dev-tool` ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)). Rock Shop packaging is covered separately under packaging plugins and themes ([Packaging Plugins And Themes](https://community.rockrms.com/developer/packaging-plugins-themes)).

**Theme** means a CMS model and asset set used to style Rock sites. The Model Map record identifies `Theme` as a CMS model, and release notes include a v18.2 fix around cloned theme type display requiring server reboot before the fix ([Model Map](https://community.rockrms.com/ModelMap), [Release Notes](https://www.rockrms.com/releasenotes)).

**Agent** in Rock's AI docs means a Rock-enabled digital assistant configured through instructions, skills, and tools. An agent can use Lava tools or native tools, but must be constrained for safety, input validation, and understandable behavior ([AI Agents](https://community.rockrms.com/developer/ai-agents)).

**Model Map** is the live model/property explorer in Rock. Dynamic LINQ docs explicitly recommend using Admin Tools > Settings > Model Map to inspect fields such as `Guid`, `Age`, and `AgeClassification` for an entity like Person before writing expressions ([Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)).

## 3. Rock Developer Resources Mental Model

Rock developer work is best understood as five overlapping layers.

### Layer 1: Platform and runtime

At the bottom is the running Rock application: ASP.NET, SQL Server, Entity Framework, Rock services, scheduled jobs, migrations, blocks, Lava, API endpoints, security authorization, and cache. Work at this layer is version-sensitive. A plugin that behaves correctly on v16 may need changes for v18 Helix or v19 Obsidian UI behavior. Before changing anything, inspect:

- Rock version and installed hotfixes.
- Installed plugins and plugin versions.
- Whether the relevant block is WebForms, Obsidian, Helix/Lava, mobile, Apple TV, or Roku.
- Database schema and migrations already applied.
- Security roles and explicit authorization rules.
- Whether the issue is code behavior, configuration, cache, data quality, or version drift.

Developer 101, 202, 303, Codex, and release notes are the main references for this layer ([Developer 101](https://community.rockrms.com/developer/101---launchpad), [The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration), [Developer 303](https://community.rockrms.com/developer/303---blast-off), [Developer Codex](https://community.rockrms.com/developer/developer-codex), [Release Notes](https://www.rockrms.com/releasenotes)).

### Layer 2: UI technology choice

Rock now has multiple UI paths. The correct path depends on the problem.

Use **WebForms blocks** when maintaining older plugin or core blocks. Developer 101 and 202 examples still reference `.ascx`, `.ascx.cs`, hidden fields, `RockBlock`, `RockContext`, `DataTextBox`, breadcrumbs, page navigation, and entity services ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data)).

Use **Obsidian** when building or replacing modern web blocks. Obsidian blocks are split into C# block logic, TypeScript component rendering, and block actions. The server sends "bags" and the client renders. Block actions become the contract for updates, saves, deletes, custom actions, and grid actions ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

Use **Helix** when the work is better served by server-driven partial updates, Lava templates, and HTMX. Helix is strong for forms, guided flows, search results, content partials, and cases where C#/TypeScript would be too heavy. Helix increases the need for explicit endpoint security, validation, rate limits, Lava command control, CSRF settings, and cache decisions ([Helix Overview](https://community.rockrms.com/developer/helix/overview), [Helix Security](https://community.rockrms.com/developer/helix/overview/security)).

Use **Mobile** when the target is native Rock Mobile. Mobile docs cover XAML-like markup, native blocks, controls, app configuration, App Factory, authentication, and platform store ownership ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs), [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

Use **TV app docs** when the target is Apple TV or Roku. Apple TV uses TVML and Rock-specific extensions; Roku uses SceneGraph XML plus Rock controls and commands ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)).

### Layer 3: Data model and persistence

Rock data work usually involves built-in entities, custom entities, attributes, defined values, content channels, interactions, workflows, groups, financial entities, check-in entities, security records, and plugin tables. The safest process is:

1. Identify the entity or table.
2. Use Model Map for properties and relationships.
3. Use the source code or generated model when Model Map is insufficient.
4. Use `INFORMATION_SCHEMA` or live schema inspection before writing SQL in a live instance.
5. Use Entity Framework and service classes for code changes unless a migration or SQL script is explicitly appropriate.
6. For custom plugin schema, include migrations and system data setup.

Developer 202 introduces custom entities and migrations, while Dynamic LINQ docs remind developers to inspect Model Map when writing expressions ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data), [The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration), [Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)).

### Layer 4: Security and operational guardrails

Security is not an afterthought in Rock development. Developer 303 calls out block security order, entity parent authority, block security actions, entity type security, custom action verbs, PersonActionIdentifier, and IdKey usage for public-facing Obsidian blocks ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)). Helix security docs stress that endpoints can be called directly outside the intended frontend, so every parameter must be validated and every action authorized ([Helix Security](https://community.rockrms.com/developer/helix/overview/security)). API docs separate API v1 as legacy and API v2 as the newer path, both requiring appropriate auth and endpoint review ([API Documentation](https://community.rockrms.com/api-docs)).

Operationally, agents must distinguish:

- Preview vs production.
- Local build success vs deployed package success.
- Installed plugin state vs source repo state.
- Current page render vs cached result.
- Block-level security vs entity-level security.
- Public UI access vs endpoint/API access.
- Staff-only UI assumptions vs direct HTTP calls.

### Layer 5: Release and branch reality

Rock docs may describe current, draft, future, plugin, or core behavior. The Rock Branches page notes that `develop` is the next major version and can be unstable, while `pre-alpha-release` is periodically merged from develop and used for early testing ([Rock Branches](https://community.rockrms.com/developer/rock-branches)). Release notes show v19.1 beta and v18.3 alpha content as of May 20, 2026, including security hardening and Obsidian fixes ([Release Notes](https://www.rockrms.com/releasenotes)). Therefore:

- Do not assume a doc page applies to the live instance.
- Check the installed Rock version.
- Check whether the doc page says draft, limited beta, plugin, core, v14+, v16, v18, or v19.
- Use source snippets when the question depends on exact field names or enum values.
- Use release notes for behavior changes and regressions.

## 4. Source Authority And How To Use This Guide

Use sources in this order when they conflict:

1. **Live Rock instance**: database rows, block settings, page routes, security records, workflow/job state, plugin versions, logs, and rendered UI.
2. **Source code for the exact deployed version**: C# models, migrations, Obsidian generated bags, enum definitions, block classes, jobs, and plugin code.
3. **Official Rock developer docs and RockU**: Developer Codex, 101/202/303, Obsidian, Helix, AI Agents, Mobile, TV docs, API docs, Lava docs, Model Map.
4. **Release notes and technical bulletins**: version caveats, security changes, fixes, and behavior changes.
5. **Community, partner, and recipe material**: useful examples but lower authority unless confirmed in live Rock or source.

The source pack includes a mix of hydrated excerpts, source-code snippets, compact source records, and release-note records. This guide synthesizes them, but it should not be used as the final authority for unverified live behavior.

When using this guide for a task, an agent should first classify the task:

- **Configuration task**: inspect the current block/page/site/app/job/endpoint settings and compare to the relevant docs.
- **Code task**: identify the technology path and exact files: WebForms, Obsidian, Helix, plugin, migration, mobile, TV, API, workflow action, job, or data view filter.
- **Data task**: identify the entity/table, relationship path, security model, and migration implications.
- **Troubleshooting task**: reproduce the symptom, inspect logs, check security, check cache, check version caveats, and then trace the owning code path.
- **Publication or packaging task**: separate package build, import, migration execution, app store publishing, Rock Shop submission, and production rollout.

When the docs are thin, this guide says to verify. For example, several Mobile Docs source records list large navigation structures but do not include detailed per-block behavior in the source pack. For those areas, inspect the live mobile block configuration and the current mobile shell documentation before making implementation claims ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs)).

## 5. Core Configuration And Data Model

Rock developer work repeatedly touches these configuration surfaces.

### Pages, layouts, sites, and blocks

Classic Rock web UI is page-based. Blocks are placed on pages or layouts, and pages live under sites. Developer 101 teaches where blocks live, how they work, how to secure them, and how to load/store data ([Developer 101](https://community.rockrms.com/developer/101---launchpad)). Developer 202 examples show migrations adding pages, adding block types, adding block instances, and adjusting page properties such as breadcrumb display ([The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)).

When working with page/block configuration, inspect:

- `Page` record: name, route, parent, layout, site, breadcrumb behavior.
- `BlockType`: path or component identity, category, GUID, supported site types, attributes.
- `Block`: block instance, zone, order, name, attribute values, page/layout/site placement.
- Security: page, block, block action, entity type, and parent authority.
- Cache: page output, Lava cache, endpoint cache, browser cache, and Rock cache.

### Attributes and defined values

Rock uses attributes heavily for extensibility and configuration. Block settings are often attributes on `BlockType` or `Block`. Developer Codex source snippets show migrations adding or updating block type attributes with stable GUIDs, field type GUIDs, keys, labels, descriptions, order, and defaults ([Content Channel Item List migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2019.0/Version%2019.0/202603202309228_AddContentChannelItemListBlockSettings.cs)). The Checkr migration snippet shows `RockMigrationHelper.AddOrUpdateBlockTypeAttribute` used to add `core.CustomActionsConfigs` and `core.EnableDefaultWorkflowLauncher` attributes to a block type ([Checkr migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Checkr/Migrations/10_CustomActionsConfigsAttributes.cs)).

For attribute work, verify:

- EntityTypeId and EntityId.
- Attribute key vs name vs GUID.
- FieldType and configuration values.
- AttributeValue storage and inheritance.
- Whether values are cached.
- Whether the attribute is for a block type, block instance, entity, workflow, group type, or global attribute.
- Whether security exists on the attribute itself.

### Custom entities and services

Developer 202 introduces code-first custom entities and service classes. The pattern is: add a project, build a model, create a service class, wire blocks to load and save entities, add pages/block setup, and create migrations for schema/system data ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data)). In the sample path, permanent GUID constants are generated and then used by migrations so pages, blocks, and block types are stable across installs.

For custom entity work, verify:

- Table name and schema.
- Primary key and GUID columns.
- `IsSystem`, `ForeignId`, `ForeignGuid`, `ForeignKey` if the model follows Rock conventions.
- Audit fields.
- EntityType registration.
- Service class namespace.
- Security support.
- Whether generated code or Model Map must be refreshed.
- Migrations for table creation and system data.

### Lava Applications and Lava Endpoints

Helix introduces data structures for Lava Applications and endpoints. Source snippets show `LavaApplication` being added through a v18 migration and converting from plugin migrations into core-aware state checks ([AddLavaApplications source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)). The client bag exposes application `attributes`, `attributeValues`, `configurationRigging`, `description`, `idKey`, `isActive`, `name`, and `slug` ([lavaApplicationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts)).

A Lava Endpoint has security, HTTP, rate limit, cache, command, and code template fields in its generated bag ([lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)). Security modes are enumerated as endpoint execute, application view, application edit, and application administrate ([lavaEndpointSecurityMode.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)). HTTP methods are GET, POST, PUT, and DELETE ([lavaEndpointHttpMethod.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointHttpMethod.ts)).

For live verification, inspect the Lava Application and Lava Endpoint rows, their attributes, security mode, enabled Lava commands, CSRF setting, rate limits, cache settings, and endpoint slug. Do not infer endpoint exposure from the frontend alone.

### Mobile and TV app configuration

Mobile, Apple TV, and Roku are not ordinary web pages. Mobile apps are linked to Rock and managed through mobile-specific app configuration, blocks, controls, authentication, and App Factory publishing ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs)). App Factory developer-account docs distinguish hosting under the organization’s own Apple/Google developer accounts versus Triumph developer accounts; ending subscription may delist apps hosted under Triumph accounts, and organization-owned accounts require inviting App Factory publishing access ([Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

Apple TV app setup is under Admin Tools > CMS Configuration > Apple TV Apps and includes fields such as Name, Description, Application Styles, Enable Page Views, API Key, and Page View Retention Period ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). Roku application settings include Enable Page Views, Page View Retention Duration, API Key, and Authentication Page ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Roku pages include Show in Menu, SceneGraph Content, cacheability, max age, and max shared age ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

## 6. Primary Entities And Relationships

The source pack does not provide a full schema dump, so this section describes likely entity relationships and what to verify in live Rock.

### Page, block, and block type

A block instance belongs to a page, layout, or site placement and references a block type. A block type defines the implementation and attribute schema. A block instance stores configured values. Migrations commonly call helper methods to add pages, update block types, add block instances, and update attributes ([The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)).

Inspect live:

- `Page.Guid`, `Page.Id`, parent, layout, site, route.
- `BlockType.Guid`, name, path/component, category.
- `Block.Guid`, `BlockTypeId`, placement.
- Block attribute values.

### Person and PersonAlias

Developer 101 includes a section on PersonAlias vs Person ([Developer 101](https://community.rockrms.com/developer/101---launchpad)). In Rock, PersonAlias is often the durable relationship key for historical records where a person can merge or change. When writing queries or custom code, inspect the entity’s foreign key: if it stores `PersonAliasId`, do not join directly to `Person.Id` unless the relationship requires it.

### Attribute, AttributeValue, DefinedType, DefinedValue

Attributes provide custom fields and configuration. Defined Types and Defined Values provide reusable option sets. Obsidian release notes include fixes around Defined Value picker behavior in Obsidian blocks, which signals that field types and enhanced picker modes can vary by version ([Release Notes](https://www.rockrms.com/releasenotes)). For any attribute problem, inspect the Attribute record, FieldType, AttributeQualifier values, and AttributeValue rows.

### Workflow and workflow actions

Developer 303 covers custom workflow actions, and release notes include workflow security hardening in v18.3/v19.1 bulletins ([Developer 303](https://community.rockrms.com/developer/303---blast-off), [Release Notes](https://www.rockrms.com/releasenotes)). For workflow work, inspect:

- WorkflowType security.
- WorkflowActionType configuration.
- EntityType for custom actions.
- Lava, SQL, or API permissions used by actions.
- Workflow logs/history.
- Whether a workflow was manually run, launched by block, launched by job, or triggered by event.

### LavaApplication and LavaEndpoint

The v18 migration source indicates `LavaApplication` includes name, description, system/active flags, security mode, slug, settings JSON, configuration rigging JSON, audit fields, GUID, and foreign keys ([AddLavaApplications source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)). Lava Endpoint bags expose endpoint code template, HTTP method, CSRF, enabled Lava commands, cache settings, rate limits, security mode, and slug ([lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)).

Live verification should inspect table names and columns in the installed Rock version because the source pack represents `develop`, and live instances may be v17/v18/v19 with plugin-core transition history.

### Interaction and analytics

Apple TV media commands refer to watch map and interaction behavior for resume and playback tracking ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)). Roku and Apple TV application settings include page view tracking and retention settings ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). RealTime Visualizer docs reference attendance and achievement channels through `Rock.RealTime.Topics.EntityUpdatedTopic` ([RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer)).

When diagnosing analytics, inspect interaction records, interaction channels, page view retention, application settings, and scheduled cleanup jobs.

### Theme

The Model Map source identifies `Theme` as a CMS model ([Model Map](https://community.rockrms.com/ModelMap)). Release notes mention a v18.2 fix where cloned theme type display could be wrong until server reboot ([Release Notes](https://www.rockrms.com/releasenotes)). For theme issues, inspect theme row, theme type, site assignments, compiled CSS/assets, cache, and whether the instance is before or after the fix.

## 7. Common Rock Developer Resources Workflows

### Choose the correct developer path

Start by asking what surface owns the work:

- Web page with old `.ascx` block: Developer 101/202/303.
- Web page with `.obs` or generated TypeScript bags: Obsidian.
- Lava endpoint or HTMX partial update: Helix.
- Agent skill/tool/instructions: AI Agents.
- Native mobile screen: Mobile Docs.
- Apple TV screen: Apple TV Docs.
- Roku screen: Roku Docs.
- Plugin/theme package: Packaging Plugins and Themes.
- Migration from old CMS: Slingshot.
- Expression/filter/query: Dynamic LINQ, Lava docs, Model Map.
- Real-time display: RealTime Visualizer and source code.
- SQL script or migration: SQL Style Guide and Developer Codex migrations.

### Build a basic custom block

For older/tutorial style work:

1. Follow Quickstart for fetching data and block setup ([Quickstart Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks)).
2. Use Developer 101 for block input, security, validation, entity loading/saving, Grid/GridFilter, breadcrumbs, dates, files, PersonAlias vs Person, and naming conventions ([Developer 101](https://community.rockrms.com/developer/101---launchpad)).
3. If storing custom data, move to Developer 202 patterns for model, service, and migration ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data)).
4. If advanced background or automation behavior is needed, use Developer 303 for jobs, workflow actions, data view filters, API, and logging ([Developer 303](https://community.rockrms.com/developer/303---blast-off)).

### Build an Obsidian block

1. Confirm whether the block is core or plugin. Obsidian docs warn that much documentation is core-focused and may require translation for plugins ([Obsidian](https://community.rockrms.com/developer/obsidian)).
2. Set up the environment: Obsidian docs reference `Rock.code-workspace`, VS Code for Obsidian projects, and Visual Studio for the broader Rock solution ([Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment)).
3. Define the C# block, TypeScript component, and block actions ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).
4. Use generated view models/bags when model changes or block contracts change ([Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)).
5. For lists, understand that Obsidian grids send all row data to the browser for client-side sorting/filtering, so large row counts can be a serious performance issue ([Grids](https://community.rockrms.com/developer/obsidian/grids)).
6. For detail blocks, use standardized detail block patterns instead of inventing layout ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)).

### Build a Helix application

1. Confirm Rock version and whether Helix is core or installed as plugin. Plugin docs mention Helix and Magnus plugins, while FAQ says Helix is now in core ([Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation), [FAQ](https://community.rockrms.com/developer/helix/overview/faq)).
2. Model the application as Lava Applications, endpoints, content blocks, HTMX interactions, forms, and controls ([Helix Overview](https://community.rockrms.com/developer/helix/overview)).
3. Treat every endpoint as externally callable. Validate all input and authorize every action ([Helix Security](https://community.rockrms.com/developer/helix/overview/security)).
4. Use endpoint fields intentionally: HTTP method, security mode, CSRF, enabled Lava commands, rate limits, cache settings, and slug ([lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)).
5. Use HTMX loading indicators and version-specific asset paths: v18+ uses `/Assets/Images/Spinners/...`; plugin Helix uses `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/...` ([Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)).
6. Avoid Lava commands that require `RockPage` in dynamic Helix updates, such as `{% javascript %}` and `{% stylesheet %}`, because RockPage is not available during partial updates ([Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)).

### Package and deploy a plugin or theme

1. Use plugin development docs and `rock-dev-tool` for Obsidian plugin setup when applicable ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)).
2. Use packaging docs for Rock Shop packaging, migrations, install/uninstall behavior, and theme/plugin deliverables ([Packaging Plugins And Themes](https://community.rockrms.com/developer/packaging-plugins-themes)).
3. Use migrations for schema/system data and ensure all GUIDs are stable.
4. Test package import into a clean Rock instance.
5. Verify database changes, block types, pages, attributes, security, and uninstall behavior.
6. Do not assume local file placement equals installed behavior.

### Diagnose a broken developer feature

Use this branch sequence:

1. Confirm version and deployment surface.
2. Reproduce the symptom in the real UI/API/app.
3. Check security first if behavior differs by user.
4. Check logs and network calls.
5. Check block settings and attributes.
6. Check cache and compiled assets.
7. Check source code and release notes.
8. If data-dependent, query the exact rows and relationships.
9. If migration-dependent, inspect migration history and system data GUIDs.
10. If docs are draft/thin, verify in live source or installed package.

## 8. Developer Codex Deep Dive

The Developer Codex is the closest thing to a standards manual for Rock development. Its table of contents covers coding standards, naming conventions, code styles, service layers, namespaces, security, architecture, blocks, JavaScript, defined types/values, migrations, committing code, code generation, testing, hotfixes, standard tools, feature branches, roles, peer reviews, Obsidian conversion, release process, SQL formatting, UI standards, logging, installation, compatibility, API patterns, and performance ([Developer Codex](https://community.rockrms.com/developer/developer-codex), [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards)).

### Naming and database conventions

Database naming conventions include the rule that fields ending in `Id` must be integer IDs. If a non-integer identifier is needed, use a `Key` suffix instead. Properties referencing another entity should be fully qualified, such as `InteractionChannelId` rather than `ChannelId`, and "Data View" should be two words in prose but not in parameter/class/method identifiers ([Database Naming Conventions](https://community.rockrms.com/developer/developer-codex/coding-standards/naming-conventions/database-naming-conventions)).

For agents, this means:

- Do not introduce ambiguous foreign key names in custom models.
- Prefer `EntityNameId` for integer FK fields.
- Use `Guid`, `IdKey`, or `ForeignKey` intentionally.
- Match existing naming in the target module.
- When adding columns, search for generated code and migration patterns before inventing names.

### Service layer boundaries

The Codex distinguishes data service, client service, block layer, and client layer. The client layer page emphasizes that mobile and Obsidian clients are separate applications running on different devices from the server, so final formatting/rendering belongs client-side while data access and authorization remain server-side ([Client Layer](https://community.rockrms.com/developer/developer-codex/coding-standards/service-layers/client-layer)).

For agents:

- Do not put database queries in TypeScript.
- Do not trust client-side hidden values.
- Let server code shape a safe view model.
- Keep block actions narrow and authorized.
- Avoid duplicating query/business logic across blocks when a service belongs in a shared layer.

### Code generator and model changes

The Codex states that model changes require running the code generator. With Obsidian TypeScript files also generated, there is a sequence: build Rock, handle manual edits if removing properties breaks generated classes, run Model Generation, then generate Obsidian view models as needed ([Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)).

For live work:

- If a model field was added but not visible in TypeScript bags, check whether generated files were refreshed.
- If a migration was added but Model Map does not show the field, check deployment and cache.
- If removing a property, inspect generated classes before build.
- Treat generated files as part of the contract, not optional artifacts.

### Migrations

The Codex lists three migration classes: standard EF migrations, migration rollups/data migrations, and hotfix/plugin migrations ([Writing Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations)). Standard EF migrations are tightly ordered and require coordination through the developer migration token ([Standard EF Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/standard-ef-migrations)). Hotfix changes with migrations should avoid model changes, use plugin hotfix migrations, and then ensure develop receives equivalent normal EF migration or rollup handling to avoid duplicate execution issues ([Hotfix Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/hotfix-changes), [Plugin Hotfix Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/plugin-hotfix-migrations)).

For agents:

- Never write a migration without identifying the target branch/version.
- Make migrations idempotent when they may run in mixed plugin/core states.
- Use stable GUIDs for system data.
- Use `RockMigrationHelper` where appropriate.
- Keep schema migrations separate from data cleanup when possible.
- Confirm rollback/down behavior when packaging.
- In hotfix contexts, identify whether the same data change will run again on upgrade.

### Obsidian Chop, Swap, Sneak

The Codex defines conversion strategies for replacing WebForms blocks with Obsidian blocks. "Chop" replaces old block types and instances and removes the old block type/files. "Swap" replaces instances but keeps the old block type for a period. "Sneak" introduces a new Obsidian block for limited early production use before broader replacement ([Obsidian Chop, Swap, Sneak](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak)).

The process page says conversion complexity depends on whether block type attribute keys and underlying values match, and whether the old block was previously swapped or sneaked ([Process to Chop or Swap](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak/process-to-chop-or-swap)). Source code confirms a post-update job can replace WebForms blocks with Obsidian blocks using configured block type GUID replacement pairs, migration strategy `Swap` or `Chop`, a testing-only keep-old-blocks flag, and ignored attribute keys for validation ([PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs)).

For agents:

- Before replacing a block, compare block type attribute keys and values.
- Inventory all block instances on pages/layouts/sites.
- Confirm supported site types.
- Preserve GUID intent if the conversion strategy requires it.
- Run conversion in a clone/test instance first.
- Verify block instance settings after replacement.
- Check whether old block type should remain available.

### Testing and peer review

The Codex states that the developer owns code quality, that verification during development is distinct from testing, and that testing may become a separate task depending on size/complexity ([Testing](https://community.rockrms.com/developer/developer-codex/coding-standards/testing)). Peer review docs emphasize code clarity, common abstractions, naming, maintainability, and constructive pushback ([Suggestions on How to Peer Review](https://community.rockrms.com/developer/developer-codex/coding-standards/peer-reviews/suggestions-on-how-to-peer-review), [For the Reviewer](https://community.rockrms.com/developer/developer-codex/coding-standards/peer-reviews/for-the-reviewer)).

Agent review checklist:

- Does the code follow Rock naming and service layer patterns?
- Are migrations ordered, idempotent where needed, and GUID-stable?
- Does security happen server-side?
- Are public endpoints protected against direct calls?
- Does the UI avoid large client payloads?
- Are generated files updated?
- Is compatibility preserved?
- Is the release branch correct?

### Compatibility

The compatibility page warns developers to be careful about public/protected declarations because public API becomes a breaking-change surface; internal/private can be safer when broader access is unnecessary ([Tips for Maintaining Compatibility](https://community.rockrms.com/developer/developer-codex/coding-standards/maintaining-compatibility/tips-for-maintaining-compatibility)).

For agents, this means avoid exposing plugin internals publicly unless the extension point is deliberate. In Rock core work, a public method may become a third-party dependency.

## 9. Developer 101 Launchpad Deep Dive

Developer 101 is the primary "learn blocks and built-in data" path. The source pack identifies its chapters: basic blocks, input values, person preferences, block security, validation, loading entities, saving entities, Grid/GridFilter, breadcrumbs, block configuration slide-out bar, dates/times, files/images, UI toolkit, PersonAlias vs Person, extension methods, internal features, and naming conventions ([Developer 101](https://community.rockrms.com/developer/101---launchpad)).

### What 101 is for

Use 101 when the work is a standard Rock web feature and the questions are:

- How does a block receive input?
- How is a block configured?
- How is access secured?
- How do I load an entity?
- How do I save an entity?
- How do I validate user input?
- How do I use a grid?
- How do I add breadcrumbs?
- How do dates, files, and images behave?
- Should I use Person or PersonAlias?

### Operational pattern

For an agent implementing or debugging a 101-level block:

1. Identify the block type and page placement.
2. Inspect block settings and attributes.
3. Identify input sources: query string, route parameters, postback fields, block settings, context entity, person preferences.
4. Load entities using the appropriate service and `RockContext`.
5. Validate both UI input and entity validation rules.
6. Save through Rock service patterns and `SaveChanges`.
7. Navigate or update UI according to the existing block convention.
8. Check block security before showing actions.
9. Add breadcrumbs only if the block owns the detail context.
10. Verify behavior under unauthorized, missing entity, invalid ID, and new entity paths.

### PersonAlias vs Person

When dealing with attendance, interactions, workflows, finance, history, and many audit-like relationships, PersonAlias is often the stable reference. Do not convert to Person blindly. Verify the model property and intended historical behavior in Model Map or source.

### Security

101 covers securing blocks, while 303 goes deeper into Rock security. At 101 level, the agent should still inspect:

- Whether the page is public.
- Whether the block is public.
- Whether edit/admin actions are secured separately.
- Whether entity security is inherited from parent authority.
- Whether query string IDs expose sensitive records.

For public-facing blocks, prefer GUID or IdKey patterns over raw integer IDs, consistent with 303 security guidance ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)).

## 10. Developer 202 Ignition Deep Dive

Developer 202 is the custom data and migration layer. It covers common entities, advanced entity guide, saving custom data, data migration, and migration helper methods ([The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)).

### Saving custom data

The Saving Custom Data chapter uses a sample plugin with a custom entity and custom list/detail blocks. The operational pattern is:

1. Add a plugin/application project.
2. Build a model class.
3. Build a service class.
4. Build a detail block.
5. Build a list block.
6. Add page and block setup.
7. Generate permanent GUIDs for constants.
8. Use migrations to create schema and system data ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data)).

The docs mention `DataTextBox` automatically validating based on model attributes such as max length. Agents should still validate server-side and not rely only on UI controls.

### Migrations in 202

The Data Migration chapter explains that Rock finds migration classes in plugin assemblies at startup, determines which have not run, and calls `Up()`. Migrations are ordered, can require a minimum Rock version, and can include SQL plus helper methods for pages, blocks, attributes, entities, and other system data ([The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)).

A safe migration playbook:

1. Assign permanent GUIDs for pages, blocks, block types, attributes, and defined values.
2. Create schema first.
3. Add entity type records if required.
4. Add block types and pages.
5. Add block instances.
6. Add attributes and default values.
7. Add security intentionally.
8. Add idempotent guards if migration may run against partially installed data.
9. Write `Down()` only if uninstall/rollback is expected to be supported.
10. Test on a clean database and an upgrade database.

### Data migration helper methods

The source pack references `RockMigrationHelper` as the place to find helper methods ([The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)). In a live codebase, inspect helper method signatures before writing or modifying migrations. Helper APIs can vary by Rock version.

### Agent cautions

Do not invent schema details from examples. The sample project is instructional. For real work, inspect the target plugin/core code and database schema. If changing existing custom data, identify whether it is core-owned, plugin-owned, organization-owned, or one-off local customization.

## 11. Developer 303 Blast-Off Deep Dive

Developer 303 is the advanced developer manual. Its source pack navigation includes custom Rock jobs, workflow actions, data view filters, adding projects to RockWeb, blocks, exception handling, context-aware blocks, attributes, extending models, performance, REST API, Rock security, logging engine, RealTime engine, data views, communication transports, JavaScript/partial postbacks, currency, and patterns in Rock ([Developer 303](https://community.rockrms.com/developer/303---blast-off)).

### Jobs

Use custom jobs for scheduled or background tasks. Agent checks:

- Job class attributes and category.
- Job settings/attributes.
- Command timeout.
- Idempotency.
- Logging and failure behavior.
- Whether it deletes itself after a one-time migration.
- Whether it can run concurrently.
- Whether it should page through records.

The Obsidian replacement source shows a one-time post-update job pattern that reads configured attributes, performs replacements, then deletes itself ([PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs)).

### Workflow actions

Use custom workflow actions when the logic belongs in workflow orchestration. Agent checks:

- Action attribute configuration.
- Entity type registration.
- Safe handling of workflow attributes.
- PersonAlias vs Person usage.
- Idempotent retries.
- Logging of user-visible errors vs technical exceptions.
- Security context.

### Data view filters and Dynamic LINQ

Data view filters and entity search often intersect with Dynamic LINQ. Use Model Map to inspect available entity properties, then write expressions that match the expected Dynamic LINQ syntax ([Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)). Do not confuse Lava filters with Dynamic LINQ `where` parameters.

### REST API

Rock API docs identify API v1 as legacy and API v2 as newer. Demo links exist for both, but live instances require actual authentication, authorization, and endpoint review ([API Documentation](https://community.rockrms.com/api-docs)). For API work:

- Identify API version.
- Confirm auth method.
- Confirm endpoint permissions.
- Use IdKey/GUID where appropriate.
- Avoid exposing raw IDs in public workflows.
- Validate payloads.
- Check rate limits and logging.

### Security

Developer 303's Rock Security page includes block security order, entity parent authority, block security actions, entity type security, custom action verbs, PersonActionIdentifier, and IdKey guidance for public-facing Obsidian blocks starting with v14 ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)).

Agent rules:

- Hidden fields are not security.
- Client IDs are not authorization.
- Public links should not expose sequential IDs.
- PersonActionIdentifier is action-scoped identity, not a general security token.
- Entity security and block security are related but distinct.
- Every custom action verb needs explicit authorization logic.

## 12. Obsidian Deep Dive

Obsidian docs are explicitly work-in-progress and often core-team oriented. The top-level page warns that not everything written is guaranteed to work exactly as described or be implemented, and that plugin developers must use judgment when translating core patterns ([Obsidian](https://community.rockrms.com/developer/obsidian)).

### Anatomy of an Obsidian block

An Obsidian block has:

- **C# block**: server logic, database access, authorization, initial data shaping.
- **TypeScript component**: browser rendering and interaction handling.
- **Block actions**: server endpoints exposed to the component for operations such as save, delete, custom actions, and loading updates ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

Operationally, the C# block should own data access and security. The TypeScript component should own presentation and user interaction. Block actions should be narrow contracts with validated input.

### Component structure

Obsidian component docs describe a component as an HTML-like file with a template and script section, with imports, properties/events, logic, and template markup ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)). The docs also identify `.obs` files as the Obsidian component extension, chosen to abstract the underlying framework ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)).

Agent checks for component work:

- Imported controls and directives.
- Props and emitted events.
- Reactive state.
- Watchers and computed values.
- API/action calls.
- Type definitions and generated bags.
- Null vs undefined handling.
- Security grant usage when controls require server-side authorization.

### Core development environment

Obsidian core development references `Rock.code-workspace` in the repository root, VS Code for Obsidian projects, and Visual Studio 2019/2022 for broader Rock solution work ([Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment)). Debugging docs cover attaching VS Code debugging to Chrome with remote debugging ([Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code)).

For plugin work, use the plugin docs rather than assuming core paths apply.

### Plugin development

Obsidian plugin development is driven by `rock-dev-tool`. The docs say the tool reduces setup time and helps create the right environment, but warn that not all referenced Rock versions may be available and point developers to the NuGet package version list for published versions ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)).

Plugin docs cover directory structure, installing the tool, creating environments, creating plugins, converting repositories, WebForms blocks, HTTP handlers, building Obsidian, supported files, partial files, library files, code generation, list/detail blocks, packaging, importing packages, and pre-release changes ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)).

### Detail blocks

Detail blocks show an entity with edit support, labels, badges, and custom actions. The docs emphasize standardized layout: developers provide content and actions, but the detail block component owns visual layout ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)).

Agents should not invent custom detail layouts unless the existing system calls for it. Use the standard detail component patterns, then test view/edit/new/deleted/not-found/unauthorized states.

### Grids

Obsidian grids provide table-like display with paging, filtering, exporting, and client-side sorting/filtering. The docs warn that all row data is sent to the browser, so a grid with 10,000 rows sends 10,000 rows even if page size is 500 ([Grids](https://community.rockrms.com/developer/obsidian/grids)). The grid reference lists many column types, including attribute, boolean, button, copy, currency, date, date-time, delete, edit, label, number, person, reorder, security, select, and text columns ([Grid Reference](https://community.rockrms.com/developer/obsidian/grid-reference)).

Agent rules for grids:

- Do not use client-side grid for unbounded data.
- Filter server-side before sending data.
- Avoid sensitive hidden columns in row data.
- Verify export behavior.
- Verify row action security.
- Use column types consistent with data semantics.
- For large data, consider server paging/API patterns instead of Obsidian grid defaults.

### Field types and UI controls

Core field type docs say older core field type patterns are mostly for the core team and that plugins and new core field types should use the newer Universal Field Type pattern when possible ([Core Field Type Patterns](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns)). UI control docs are also core-oriented, with different paths and APIs for plugins ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)).

Before creating a field type, inspect the current docs and source for the version. Field types are cross-cutting and can affect attributes, workflows, Obsidian controls, validation, and serialization.

### Lava with Obsidian

Lava docs warn that some Lava filters/commands that modify HTTP response data, such as redirects or meta tags, may not work in Obsidian blocks because Obsidian actions do not reload the whole page and the response has already been sent ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)). Agents should not assume legacy Lava page behavior works inside Obsidian action flows.

## 13. Helix Deep Dive

Helix is described as the next evolution of Lava web development, integrating HTMX, Lava Applications, Lava Commands, and Control Shortcodes ([Helix Overview](https://community.rockrms.com/developer/helix/overview)). The important operational distinction is that Helix lets a Rock developer build dynamic server-driven experiences using Lava and HTMX without committing to full C#/Obsidian development, but it also creates endpoint and data integrity responsibilities.

### Plugin vs core status

The plugin installation page says Helix was in limited beta and used two plugins: Helix and Magnus ([Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation)). The FAQ says Helix is now in core ([FAQ](https://community.rockrms.com/developer/helix/overview/faq)). Source code shows `AddLavaApplications` as a v18 migration that converts from a plugin with multiple migrations and includes idempotent checks for partial prior states ([AddLavaApplications source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)).

Agent rule: verify installed Rock version and installed plugins before diagnosing Helix. A v18+ instance may use core paths; an older or transitional instance may use plugin paths and plugin assets.

### Lava Applications

A Lava Application groups a Helix app. Source snippets show fields for name, description, active/system flags, security mode, slug, settings JSON, configuration rigging JSON, audit fields, GUID, and foreign keys ([AddLavaApplications source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)). The generated Obsidian bag exposes attributes, attribute values, configuration rigging, description, idKey, active flag, name, and slug ([lavaApplicationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts)).

Verify in live:

- Application slug uniqueness.
- Active state.
- Security mode and security rules.
- Attribute values.
- Configuration rigging.
- Endpoints under the application.
- Pages/content blocks that call those endpoints.

### Lava Endpoints

Lava Endpoints are callable surfaces. Generated bags expose code template, HTTP method, CSRF, enabled Lava commands, cache control, rate limiting, security mode, slug, attributes, attribute values, and active flag ([lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)). Security modes are Endpoint Execute, Application View, Application Edit, and Application Administrate ([lavaEndpointSecurityMode.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)). HTTP methods are GET, POST, PUT, and DELETE ([lavaEndpointHttpMethod.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointHttpMethod.ts)).

Endpoint guardrails:

- Use GET only for safe reads.
- Use POST/PUT/DELETE for mutations and protect with CSRF where applicable.
- Use the narrowest security mode.
- Enable only required Lava commands.
- Validate all input, even if frontend controls appear constrained.
- Rate-limit public or high-cost endpoints.
- Use cache settings intentionally.
- Return minimal data.
- Test with direct HTTP calls, not just the intended UI.

### HTMX and partial updates

Helix uses HTMX for dynamic partial updates. The overview frames HTMX as the answer to Lava's traditional page-load-only execution model ([Helix Overview](https://community.rockrms.com/developer/helix/overview)). Learning More points to HTMX resources and galleries ([Learning More](https://community.rockrms.com/developer/helix/htmx/learning-more)).

Agent checks:

- `hx-get`, `hx-post`, target, swap, trigger, and indicator behavior.
- Whether the endpoint returns valid partial markup.
- Whether forms include required hidden fields/tokens.
- Whether validation errors render into the correct target.
- Whether browser back/refresh behavior is acceptable.
- Whether repeated clicks or slow responses create duplicate writes.

### Loading indicators

Helix loading docs describe HTMX loading indicator patterns and warn about path differences: Rock v18+ uses `/Assets/Images/Spinners/...`; plugin Helix uses `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/...` ([Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)). This is a concrete version caveat agents should check when an indicator works in one environment but not another.

### Limitations

Helix limitations include Lava commands that require `RockPage`, specifically `{% javascript %}` and `{% stylesheet %}`, because dynamic partial updates do not have the full RockPage render context ([Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)). Lava With Obsidian has a similar principle for response-modifying operations in Obsidian ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).

### Security

Helix security docs emphasize that endpoints may be accessed directly with tools such as curl or Postman, with modified parameters, so input validation and authorization must be explicit ([Helix Security](https://community.rockrms.com/developer/helix/overview/security)). For public Helix apps, use GUIDs or IdKeys where possible and never rely on the UI to hide unauthorized operations.

## 14. AI Agents Deep Dive

Rock AI Agents docs are for developers fluent in Lava, SQL, or C# who are building agents and tools inside Rock ([AI Agents](https://community.rockrms.com/developer/ai-agents)). The source pack navigation includes:

- Agents.
- Agent instructions.
- Context anchors.
- Writing custom tools.
- Types of tools.
- Lava tools: lookup, list, get, insight.
- Native tools: lookup, list, get, add/update, available attributes, summary, Rock Tool Helper, tool parameters, gotchas.
- Debugging tools.
- Skills and creating skills ([AI Agents](https://community.rockrms.com/developer/ai-agents)).

### Mental model for Rock agents

An agent is not just a chat interface. It is a configured actor with instructions, context, and tool access. The safety model depends on:

- Clear system instructions.
- Scoped skills.
- Tool descriptions that state what the tool can and cannot do.
- Parameter schemas.
- Validation before reads/writes.
- Authorization checks.
- Audit/logging.
- Conservative default behavior.
- Human review for high-impact changes.

### Lava tools vs native tools

Lava tools can be faster to create for Rock-aware querying and templating, but they inherit Lava command risks and must be constrained. Native tools can provide stronger typed contracts, better validation, and deeper integration, but require C# implementation and deployment. When choosing:

- Use Lava tools for read-heavy, low-risk, narrow queries where the output is simple and bounded.
- Use native tools for writes, sensitive data, complex authorization, business logic, or reusable system behavior.
- Do not let agent tools execute arbitrary Lava or SQL unless the environment explicitly permits that and the tool is locked down.

### Agent instructions and context anchors

Agent instructions should encode operational boundaries. Context anchors should give stable references to Rock areas, pages, groups, workflows, data views, or procedures. Do not overload the context window with broad documentation. Provide the minimal durable context needed for safe execution.

### Tool design checklist

For every custom Rock agent tool:

- Name the operation narrowly.
- Define input parameters with types and descriptions.
- Validate required parameters.
- Resolve IDs safely using GUID/IdKey/natural key lookups.
- Check authorization.
- Return structured output.
- Limit row counts.
- Avoid exposing secrets.
- Log writes.
- Make write operations idempotent when possible.
- Provide dry-run mode for risky writes.
- Document failure branches.

### Live verification

The AI Agents source pack is broad but not hydrated deeply beyond navigation and terminology. Before building production tools, inspect current AI Agents docs for the installed Rock version, the actual tool APIs, and any security bulletins.

## 15. Mobile Docs Deep Dive

Rock Mobile is a native mobile extension of Rock RMS, with documentation for building mobile applications linked to Rock ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs)). The source pack navigation shows major areas: building first app, app configuration, adding content, deploying app, lexicon, essentials, advanced topics, animations, blocks, controls, styling, and many domain block categories.

### Mobile is not web

Do not treat mobile pages as normal Rock web pages. Mobile has its own shell, markup/control model, native navigation, authentication flows, and platform publishing concerns. Blocks are mobile blocks, not necessarily web blocks. Styling and layout use mobile-specific controls and CSS-like mechanisms documented under Mobile Docs.

### App Factory and developer accounts

App Factory publishing can use either the organization’s own Apple/Google developer accounts or Triumph developer accounts. If the app is hosted under Triumph accounts and the App Factory subscription ends, the docs warn that apps may be delisted after a period. If hosted under organization accounts, the organization retains store control but must provide App Factory access for publishing ([Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

Operational checks:

- Who owns the Apple developer account?
- Who owns the Google Play account?
- Is App Factory publishing on behalf of the org?
- Are invitations still valid?
- Are certificates/profiles/current store assets accessible?
- What happens if subscription or publishing relationship changes?

### Mobile block categories

The source pack includes Mobile blocks across CMS, Check-in, Communication, Connection, Core, CRM, Events, Finance, Groups, Prayer, Reminders, and Security ([CMS](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms), [Check-in](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in), [Communication](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication), [Connection](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection), [Core](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core), [CRM](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm), [Events](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events), [Finance](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance), [Groups](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups), [Prayer](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/prayer), [Reminders](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders), [Security](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security)).

Because the hydrated excerpts mostly show navigation, verify block-specific settings in the current docs and live instance before making claims. Inspect the mobile page, block type, attribute values, authentication state, and shell version.

### Controls and styling

Mobile docs include behavior controls, card elements, card styling with CSS, legacy borders, and legacy form field styling ([Behaviors](https://community.rockrms.com/developer/mobile-docs/essentials/controls/behaviors), [Elements of a Card](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/cards/elements-of-a-card), [Styling Cards With CSS](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/cards/styling-cards-with-css), [Borders](https://community.rockrms.com/developer/mobile-docs/styling/legacy/borders), [Form Fields](https://community.rockrms.com/developer/mobile-docs/styling/legacy/styling-components/form-fields)). Treat "legacy" styling docs as version-sensitive and verify whether the current shell still uses the same styling system.

## 16. TV App Docs Deep Dive

Rock supports Apple TV and Roku app development as platform extensions linked to Rock.

### Apple TV

Apple TV docs state Rock Apple TV is a set-top extension for building TVML applications linked to Rock, and warn that Apple TV functionality requires Rock version 14 or greater ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). Apple TV apps use TVML, not HTML, and the docs point to Apple TVML documentation as the main language reference while documenting Rock extensions.

Creating an app happens under Admin Tools > CMS Configuration > Apple TV Apps. Configuration fields include:

- Name.
- Description.
- Application Styles.
- Enable Page Views.
- API Key.
- Page View Retention Period ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)).

Testing can use a demo key and the Rock community app on Apple TV to point to the custom application without publishing through the App Store/TestFlight ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app)).

Adding content involves TV pages and TVML templates. Apple TV docs cover templates, controls, JavaScript commands, styling, and app images ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content), [Apple TV Developer](https://community.rockrms.com/developer/apple-tv-docs/developer)).

Apple TV styling is not ordinary web styling. TVML has Apple-centric text styles, theme behavior, media queries, built-in images, and parallax images. Docs cover light/dark themes, theme media queries, built-in tvOS assets, TV text styles, and parallax image layers ([Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes), [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries), [Built in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images), [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style), [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)).

Apple TV media commands include video/audio playback. Docs note that YouTube content cannot be played in an Apple TV application and describe interaction/watch-map behavior for resume tracking ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).

### Roku

Roku docs describe Rock Roku integration for creating and managing Roku apps that deliver media to Roku TV ([Roku Docs](https://community.rockrms.com/developer/roku-docs)). Roku development is similar to building a website in that an application contains pages powered by Lava, but the interface is XML-based SceneGraph rather than HTML ([Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)).

Roku application settings include:

- Enable Page Views.
- Page View Retention Duration.
- API Key.
- Authentication Page ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).

Roku page settings include:

- Show in Menu.
- SceneGraph Content.
- Cacheability Type.
- Max Age.
- Max Shared Age ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

Each Roku page should use an outer `Rock:Page` component to set initial focus, and the page has Lava merge fields available such as current person and context according to the page docs ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

Roku controls are built on SceneGraph. Rock provides custom controls, while most UI still uses built-in SceneGraph components ([Roku Controls](https://community.rockrms.com/developer/roku-docs/resources/controls), [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)). The Focus Group control handles vertical/horizontal layout and directional focus management because Roku does not provide the same built-in focus behavior developers may expect from Apple TV ([Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

Roku docs also link feature requests, GitHub issues, and community chat for operational feedback ([Useful Links](https://community.rockrms.com/developer/roku-docs/resources/useful-links)).

## 17. Packaging Plugins And Themes Deep Dive

Packaging Plugins and Themes is the developer book for packaging custom plugins and themes for Rock Shop distribution and community reuse ([Packaging Plugins And Themes](https://community.rockrms.com/developer/packaging-plugins-themes)). The source pack does not include hydrated detail for this section, so verify current docs before performing packaging work.

A practical packaging model:

1. **Identify deliverables**: assemblies, `.ascx` blocks, Obsidian compiled assets, HTTP handlers, Lava templates, images, CSS/JS, theme files, migrations, documentation.
2. **Assign ownership namespace**: organization/plugin namespace, folder paths, category names, GUID constants.
3. **Create install migrations**: schema, entity types, block types, pages, attributes, defined values, security, default data.
4. **Create uninstall behavior**: determine whether user data should remain, be disabled, or be removed.
5. **Build package**: use the current packaging tool/process.
6. **Import into clean Rock**: verify migrations, files, block registration, pages, attributes, and security.
7. **Import into upgrade Rock**: verify existing settings and data are preserved.
8. **Test uninstall/rollback if supported**.
9. **Document version requirements**.
10. **Confirm Rock Shop metadata and licensing**.

For Obsidian plugins, use Obsidian plugin development docs and `rock-dev-tool` setup before packaging ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)). For themes, verify the `Theme` model and release notes for theme-related caveats ([Model Map](https://community.rockrms.com/ModelMap), [Release Notes](https://www.rockrms.com/releasenotes)).

Packaging should never rely on manual page edits only. If a package installs pages/blocks/attributes, those changes should be represented in migrations or package metadata so a clean install is reproducible.

## 18. Quickstart Tutorials Deep Dive

Quickstart Tutorials are the entry path for creating, configuring, connecting, customizing, and securing first blocks ([Developer Resources](https://community.rockrms.com/developer), [Quickstart Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks)). The source pack shows sections for fetching data, blocks, configurable blocks, connecting blocks, customizing and securing blocks, and appendices for setup ([Appendix](https://community.rockrms.com/developer/quickstart-tutorials/appendix)).

### Environment setup

The Quickstart appendix covers new developer environment setup, including SQL Server, Visual Studio, and a SQL login such as `RockUser` ([Appendix - New Developer Environment Setup](https://community.rockrms.com/developer/quickstart-tutorials/appendix/appendix---new-developer-environment-setup)). The Codex installation checklist adds a more standards-oriented environment list, including SQL Server Developer Edition, SSMS, Visual Studio 2022 for Rock v14 and newer, and useful extensions ([Installation Checklist](https://community.rockrms.com/developer/developer-codex/coding-standards/installation-checklist)).

For agents, do not assume local developer setup matches docs. Inspect local connection strings, SQL version, Visual Studio/build tooling, Node/tooling for Obsidian, and plugin tool versions.

### Quickstart block workflow

Quickstart is useful for a narrow first block:

1. Fetch data.
2. Render data in a block.
3. Add configurable block attributes.
4. Connect blocks through query string, route, or context.
5. Add security and customization.
6. Move to 101 once block logic needs real entity load/save, validation, grid behavior, or breadcrumbs.

### Avoid overfitting to tutorial code

Tutorials are learning code. Production code must follow Codex standards, security, service layers, and migration practices. If building for modern Rock, consider whether Obsidian or Helix is the better UI target instead of copying older WebForms patterns.

## 19. Slingshot Migration Deep Dive

Slingshot is Rock's migration tool for moving data from an existing CMS into Rock. It works in two broad steps: pull data from the old system into a `.slingshot` file, then import that file into Rock ([About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)). It is designed to be simple, fast, trackable, and usable without deep database expertise, but it is not a complete replacement for migration planning and cleanup ([Slingshot](https://community.rockrms.com/developer/slingshot)).

### What Slingshot does well

Slingshot can:

- Export/import supported record types.
- Bundle data into a portable migration file.
- Track migration progress.
- Limit record types and date ranges.
- Use a Foreign System Key to distinguish files containing the same kind of data.
- Move data faster than manual migration for supported systems ([About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)).

### What Slingshot does not eliminate

The docs explicitly warn that imported data may need cleanup and configuration afterward. Attendance, for example, may be imported but still require configuration before analytics use ([About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)).

Post-import checks:

- Families and individuals.
- Duplicate people.
- Addresses and phones.
- Contributions and batches.
- Groups and group types.
- Attendance and schedules.
- Attribute mapping.
- Foreign system keys.
- Photos/files.
- Historical records.
- Analytics readiness.
- Security/privacy for migrated data.

### Source-system specifics

The Specifics of Migration page notes that every CMS exposes different export/import data. For Church Community Builder, Slingshot can import families, individuals, contributions, groups, and attendance, with many individual fields. It also lists data that may require individual API calls or may not be available through API/export ([Specifics of Migration](https://community.rockrms.com/developer/slingshot/specifics-of-migration)).

Agent migration rule: never promise a field will migrate without checking the source-system-specific Slingshot docs, export file, source API limits, and a test import.

## 20. Utility And Reference Pages Deep Dive

### Dynamic LINQ Syntax

Dynamic LINQ is used by multiple Rock features, including Entity Search and related filtering expressions. Docs recommend using Model Map to inspect entity properties before writing expressions ([Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)). Expressions include where, grouping, select, select many, and ordering. Some contexts may disable grouping/select/select many/ordering.

Agent checks:

- Identify the feature consuming the expression.
- Inspect the entity in Model Map.
- Confirm whether attributes are available in that context.
- Test with a small expression.
- Avoid Lava filter syntax in Dynamic LINQ.
- Confirm null behavior and type conversion.

### RealTime Visualizer

RealTime Visualizer listens to Rock RealTime topic/channel pairs. Messages sent to topic A/channel 1 are not received by clients listening to topic B/channel 1 or topic A/channel 2. The block can listen to many topic/channel combinations, but available channels may be dynamically created and not shown in the configuration UI ([RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer)).

The docs focus on `Rock.RealTime.Topics.EntityUpdatedTopic` for attendance and achievement examples, and explain that themes and templates control visual presentation ([RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer)).

Agent checks:

- Topic name.
- Channel name.
- Source code or docs for dynamic channel construction.
- Theme defined value.
- Template settings.
- CSS customization.
- Client connection and authorization.
- Whether the producer actually publishes the event.

### Rock Branches

Rock follows Gitflow. `develop` is the next major version and unstable. `pre-alpha-release` is periodically merged from develop and deployed to early sites; it may be tagged after successful use, but still carries risk ([Rock Branches](https://community.rockrms.com/developer/rock-branches)).

Agent branch rules:

- Do not develop production plugin changes against an arbitrary branch without checking target Rock version.
- Use release branches/tags for production compatibility.
- Use `develop` only for next-version work.
- Use release notes to map features/fixes to versions.
- When diagnosing a discrepancy, ask whether source code comes from `develop` while the instance runs a stable release.

### SQL Style Guide

Rock SQL style guidance includes uppercase keywords, bracketed table/field names, explicit JOIN clauses, and WHERE clauses for filters only ([SQL Style Guide](https://community.rockrms.com/developer/sql-style-guide)). Use this style for migrations, scripts, and community-shared SQL.

Agent SQL rules:

- Inspect schema before writing SQL.
- Use bracketed names.
- Use parameterized SQL in application code.
- Avoid ad hoc string concatenation.
- Use transactions for multi-step writes when appropriate.
- Include a read-only preview query before destructive updates.
- Separate data repair from schema migration unless tightly coupled.

### Design System

The Design System page points to a Rock RMS component library based on Figma components and styles ([Design System](https://community.rockrms.com/developer/design-system)). The source pack is thin, so verify current Figma/component guidance before designing or implementing UI.

### Developer Radar

The Developer Radar page says the old Community Developer group has been retired and directs developers to the `#develop` chat channel and RockCast podcast for developer announcements ([Developer Radar](https://community.rockrms.com/developer/CommunityDeveloperSubscribe)).

## 21. Related Rock Areas: Api Integrations, Lava, Helix, Obsidian, Mobile, Plugins, Themes, Migration, Security, Cms, Tv Apps

### API Integrations

API docs identify API v1 as legacy and API v2 as the newer API surface, with shared resources for API documentation, API concept tours, and creating APIs with Lava ([API Documentation](https://community.rockrms.com/api-docs)). For integrations:

- Prefer API v2 for new work when supported.
- Confirm endpoint availability in the installed Rock version.
- Use least-privilege API keys/users.
- Inspect rate limits and logging.
- Avoid raw SQL exposure through API-like Lava endpoints.
- Use Lava APIs only when security and validation are explicit.

### Lava

Lava is central to CMS, Helix, TV pages, mobile content, workflows, and dynamic expressions. Lava docs warn that response-modifying filters/commands may not work in Obsidian because the full page response has already been sent ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)). Helix has similar limitations for `javascript` and `stylesheet` commands in partial updates ([Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)).

### Helix

Helix is best for Lava/HTMX applications and dynamic server-rendered flows. It intersects with Lava Applications, Lava Endpoints, forms, controls, Magnus, observability, and security ([Helix Overview](https://community.rockrms.com/developer/helix/overview)).

### Obsidian

Obsidian is best for modern web UI blocks with TypeScript and C# server contracts. It intersects with generated bags, block actions, grids, field types, security grants, and plugin tooling ([Obsidian](https://community.rockrms.com/developer/obsidian)).

### Mobile

Mobile apps use native mobile shell patterns and app store publishing. Verify shell version, App Factory arrangement, block settings, and mobile-specific controls ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs), [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

### Plugins and themes

Plugins package code and system data. Themes package design assets and CMS theme behavior. Verify packaging docs, migration behavior, and version requirements ([Packaging Plugins And Themes](https://community.rockrms.com/developer/packaging-plugins-themes), [Model Map](https://community.rockrms.com/ModelMap)).

### Migration

Slingshot handles CMS migration but does not remove cleanup, mapping, or analytics configuration work ([Slingshot](https://community.rockrms.com/developer/slingshot), [About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)).

### Security

Security spans block security, entity security, API auth, Lava endpoint security, workflow type security, document type security, mobile auth, TV API keys, and agent tools. Release notes include security hardening around workflow type view permissions and document type view permissions ([Release Notes](https://www.rockrms.com/releasenotes)).

### CMS

CMS includes pages, sites, blocks, themes, content channels, Lava, interactions, and TV apps. CMS-related source snippets show block settings migrations and theme/model references ([Content Channel Item List migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2019.0/Version%2019.0/202603202309228_AddContentChannelItemListBlockSettings.cs), [Model Map](https://community.rockrms.com/ModelMap)).

### TV Apps

Apple TV uses TVML and requires Rock v14+ ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). Roku uses SceneGraph and Rock-specific controls/commands ([Roku Docs](https://community.rockrms.com/developer/roku-docs), [Roku Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)).

## 22. Administration And Operational Guardrails

### Version guardrails

Always inspect Rock version before applying docs:

- Apple TV requires v14+ ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- IdKey guidance for public-facing Obsidian blocks starts with v14 in the 303 security docs ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)).
- RealTime engine references include v16 in Developer 303 navigation ([Developer 303](https://community.rockrms.com/developer/303---blast-off)).
- Helix asset paths differ for plugin Helix vs Rock v18+ ([Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)).
- Roku docs include v16.7 metadata in the source pack.
- Release notes show v19.1 beta and v18.3 alpha as of May 20, 2026 ([Release Notes](https://www.rockrms.com/releasenotes)).

### Security guardrails

For any developer task:

- Check current person/user context.
- Check block/page/entity authorization.
- Check endpoint authorization.
- Check direct-call behavior.
- Avoid raw integer IDs in public URLs.
- Use GUIDs or IdKeys where appropriate.
- Do not trust hidden fields.
- Validate all posted input.
- Treat Lava/SQL/API tools as privileged.
- Add audit/logging for writes.

### Data guardrails

Before writes:

- Inspect schema.
- Preview affected rows.
- Back up if operating outside normal migrations.
- Use transactions for multi-step changes.
- Keep cleanup and feature changes separate.
- Verify result counts.
- Check caches and UI after writes.
- Record exact GUIDs and IDs used.

### Migration guardrails

- Migrations must be ordered.
- Standard EF migrations require coordination.
- Hotfix migrations need rollup handling.
- Plugin migrations should support clean install and upgrade.
- Avoid duplicate data changes on hotfix-to-major upgrade.
- Test against clean and existing databases.
- Use stable GUIDs.

### UI guardrails

- Obsidian grids should not receive unbounded row sets.
- Helix partial updates should handle loading/error states.
- Mobile/TV apps need device/shell testing.
- Apple TV and Roku styling are platform-specific.
- Cache settings can hide configuration changes.

### Communication guardrails

For developer announcements, the old Community Developer group is retired; use `#develop` chat and RockCast for current community developer announcements ([Developer Radar](https://community.rockrms.com/developer/CommunityDeveloperSubscribe)).

## 23. Developer, API, Lava, And Source-Code Landmarks

Use these landmarks when orienting a task:

- Developer landing page: [Developer Resources](https://community.rockrms.com/developer)
- Developer Codex: [Developer Codex](https://community.rockrms.com/developer/developer-codex)
- Coding standards: [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards)
- Naming/database conventions: [Database Naming Conventions](https://community.rockrms.com/developer/developer-codex/coding-standards/naming-conventions/database-naming-conventions)
- Migrations: [Writing Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations)
- Code generator: [Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)
- Quickstart: [Quickstart Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks)
- 101: [Developer 101](https://community.rockrms.com/developer/101---launchpad)
- 202 custom data: [Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data)
- 202 migrations: [The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration)
- 303: [Developer 303](https://community.rockrms.com/developer/303---blast-off)
- 303 security: [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)
- Obsidian: [Obsidian](https://community.rockrms.com/developer/obsidian)
- Obsidian block anatomy: [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)
- Obsidian grids: [Grids](https://community.rockrms.com/developer/obsidian/grids)
- Obsidian plugin development: [Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)
- Helix: [Helix Overview](https://community.rockrms.com/developer/helix/overview)
- Helix security: [Helix Security](https://community.rockrms.com/developer/helix/overview/security)
- Helix limitations: [Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)
- AI Agents: [AI Agents](https://community.rockrms.com/developer/ai-agents)
- Mobile: [Mobile Docs](https://community.rockrms.com/developer/mobile-docs)
- Apple TV: [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)
- Roku: [Roku Docs](https://community.rockrms.com/developer/roku-docs)
- Slingshot: [Slingshot](https://community.rockrms.com/developer/slingshot)
- API: [API Documentation](https://community.rockrms.com/api-docs)
- Lava with Obsidian: [Lava With Obsidian](https://community.rockrms.com/lava/obsidian)
- Dynamic LINQ: [Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)
- SQL style: [SQL Style Guide](https://community.rockrms.com/developer/sql-style-guide)
- RealTime: [RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer)
- Branches: [Rock Branches](https://community.rockrms.com/developer/rock-branches)
- Release notes: [Release Notes](https://www.rockrms.com/releasenotes)
- Source repository: [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)

## 24. Reporting, Analytics, And Model Map

### Model Map

Model Map is the first stop for understanding entity properties in a live Rock instance. Dynamic LINQ docs explicitly tell users to navigate to Admin Tools > Settings > Model Map and inspect an entity such as Person to see fields available for workflows, Lava, or Entity Search ([Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)). The source pack includes a Model Map record identifying `Theme` as a CMS model ([Model Map](https://community.rockrms.com/ModelMap)).

Agent pattern:

1. Identify entity category.
2. Open Model Map.
3. Confirm field names, types, navigation properties, and attributes.
4. Use those names in Dynamic LINQ, Lava entity commands, reports, or code.
5. If Model Map is insufficient, inspect source model and database schema.

### Reporting and Dynamic LINQ

Dynamic LINQ where expressions can filter on properties and attributes. Example docs include boolean and ID comparisons, and warn not to confuse Dynamic LINQ where parameters with Lava's `where` filter ([Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)).

Agent reporting checks:

- Is the filter evaluated in SQL, Dynamic LINQ, Lava, or client code?
- Are attributes available?
- Are nulls handled?
- Are IDs correct for the environment?
- Does the expression require quoting or type conversion?
- Is grouping/select/order allowed?

### Analytics and interactions

TV app page views and media interactions can create analytics data if enabled and retained ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)). Slingshot migration docs warn that imported attendance may need configuration before analytics use ([About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)).

Analytics troubleshooting:

- Confirm tracking is enabled.
- Confirm retention duration.
- Confirm interaction channel/entity mapping.
- Confirm cleanup jobs have not removed data.
- Confirm imported data is mapped to expected schedules/groups/locations.
- Confirm dashboards use the expected source table.

### RealTime visualization

For live dashboards, RealTime Visualizer uses topic/channel subscriptions and themes/templates ([RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer)). If a visualizer is blank, inspect whether the producer is emitting messages, the channel name is correct, and the client is authorized/connected.

## 25. Version And Release Caveats

### Draft and work-in-progress docs

Developer 303 is labeled draft in the source pack ([Developer 303](https://community.rockrms.com/developer/303---blast-off)). Obsidian docs warn they are work-in-progress and not guaranteed to describe final behavior ([Obsidian](https://community.rockrms.com/developer/obsidian)). Helix related entities page is explicitly writing-in-progress ([Related Entities](https://community.rockrms.com/developer/helix/strategies/related-entities)).

Agent rule: cite draft docs for orientation, not final proof. Verify in source and live instance.

### Rock v14

Apple TV requires Rock v14+ ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). Developer 303 notes IdKey guidance for v14 Obsidian blocks, especially public-facing blocks ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)). Visual Studio 2022 is listed for Rock v14 and newer in the installation checklist ([Installation Checklist](https://community.rockrms.com/developer/developer-codex/coding-standards/installation-checklist)).

### Rock v16

Developer 303 navigation references Rock RealTime Engine v16 ([Developer 303](https://community.rockrms.com/developer/303---blast-off)). Roku docs source metadata includes v16.7. Verify live support for Roku features before using them.

### Rock v17

Release notes include v17.1 adding an Obsidian Communication Template Detail block for viewing/editing communication templates and laying groundwork for versioned template management ([Release Notes](https://www.rockrms.com/releasenotes)). Obsidian chop/swap process metadata includes v17 in the source pack.

### Rock v18

Helix v18+ path differences appear in loading indicator docs ([Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)). Source code shows Lava Applications added through v18 migration code and handling plugin-to-core transition state ([AddLavaApplications source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)). Release notes include v18.2 theme clone display fix and v18.3 alpha security/Obsidian fixes ([Release Notes](https://www.rockrms.com/releasenotes)).

### Rock v19

Release notes show Rock v19.1 beta released May 20, 2026, with broad module notes and security bulletins ([Release Notes](https://www.rockrms.com/releasenotes)). Source code snippets include v19 migrations adding block settings for Content Item List ([Content Channel Item List migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2019.0/Version%2019.0/202603202309228_AddContentChannelItemListBlockSettings.cs)).

### Branch caveat

The source snippets are from the `develop` branch. `develop` may be ahead of released Rock and unstable ([Rock Branches](https://community.rockrms.com/developer/rock-branches)). Do not assume `develop` source fields exist in a production instance.

## 26. Implementation Playbooks

### Playbook: Add a new configurable block setting

1. Identify block type and technology: WebForms or Obsidian.
2. Check existing block type attributes.
3. Choose field type and key following naming standards.
4. Add migration with `RockMigrationHelper.AddOrUpdateBlockTypeAttribute`.
5. Add default value.
6. Read setting in block code.
7. Update generated bags if Obsidian and required.
8. Test existing block instances.
9. Verify no migration duplicates in hotfix/rollup paths.
10. Check release notes if touching core block settings.

Reference pattern: source migration adding Content Item List block settings ([Content Channel Item List migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2019.0/Version%2019.0/202603202309228_AddContentChannelItemListBlockSettings.cs)).

### Playbook: Build a safe Lava Endpoint

1. Create/identify Lava Application.
2. Create endpoint slug.
3. Select HTTP method.
4. Select the narrowest security mode.
5. Enable only required Lava commands.
6. Enable CSRF for mutation endpoints.
7. Add rate limits for public/high-cost calls.
8. Configure cache only for safe, non-personal data.
9. Validate all input.
10. Return minimal HTML/JSON.
11. Test direct calls with missing, invalid, unauthorized, and malicious parameters.
12. Inspect logs.

References: Helix overview/security and endpoint source fields ([Helix Overview](https://community.rockrms.com/developer/helix/overview), [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)).

### Playbook: Replace a WebForms block with Obsidian

1. Inventory old block type GUID and all instances.
2. Inventory new Obsidian block type GUID.
3. Compare block type attribute keys and values.
4. Decide chop, swap, or sneak.
5. If complex, use the post-update replacement job pattern.
6. Configure GUID replacement pairs.
7. Configure migration strategy.
8. Decide whether old blocks are kept only for testing.
9. Run in test.
10. Verify page/layout/site placements.
11. Verify block settings migrated.
12. Verify security and custom action behavior.
13. Verify old block type removal/retention matches strategy.

References: Codex chop/swap/sneak and replacement job source ([Obsidian Chop, Swap, Sneak](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak), [Process to Chop or Swap](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak/process-to-chop-or-swap), [PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs)).

### Playbook: Create a custom entity/plugin data model

1. Define model and table.
2. Follow naming conventions.
3. Add service class.
4. Add migration to create table.
5. Add entity type/system data.
6. Add pages, block types, block instances if UI is included.
7. Add attributes and security.
8. Generate GUID constants.
9. Build and run generated code steps if model changes require them.
10. Test clean install and upgrade.
11. Verify Model Map.

References: Developer 202 and Codex model generation ([Saving Custom Data](https://community.rockrms.com/developer/202---ignition/saving-custom-data), [The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration), [Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)).

### Playbook: Build a Roku page

1. Confirm Roku application exists.
2. Confirm API key and authentication page.
3. Create page.
4. Set Show in Menu according to intended Lava-driven navigation.
5. Write SceneGraph content.
6. Use outer `Rock:Page`.
7. Use available Lava merge fields.
8. Configure cacheability/max age.
9. Test focus navigation.
10. Use Rock controls such as Focus Group where needed.
11. Test on device/emulator.

References: Roku Getting Started, Applications, Pages, Controls, Focus Group ([Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

### Playbook: Build an Apple TV app page

1. Confirm Rock v14+.
2. Create Apple TV app under CMS Configuration.
3. Configure name, description, styles, API key, page view tracking, retention.
4. Use demo key for testing.
5. Create page and TVML content.
6. Use Apple-appropriate templates and text styles.
7. Configure app images and parallax assets.
8. Avoid unsupported media such as YouTube playback.
9. Test light/dark themes and media queries.
10. Verify interactions/watch map if media tracking is used.

References: Apple TV Docs, Creating An App, Testing, Adding Content, Media Commands ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app), [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content), [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).

## 27. Troubleshooting Decision Tree

### The block does not render

1. Is it WebForms, Obsidian, Helix, Mobile, Apple TV, or Roku?
2. Is the block type installed and active?
3. Is the block instance placed on the expected page/layout/site?
4. Is the current user authorized to view the page and block?
5. Are required block settings missing?
6. Did a migration fail?
7. Are compiled assets missing?
8. Is the route/page correct?
9. Is the browser/API returning an error?
10. Does release note/source indicate version mismatch?

### The Obsidian block renders but actions fail

1. Inspect network request.
2. Check block action name and route.
3. Check server logs.
4. Validate input bag shape.
5. Check IdKey/GUID resolution.
6. Check authorization in the action.
7. Check generated TypeScript/C# view models.
8. Check null vs undefined behavior.
9. Check Lava response-modifying assumptions if Lava is involved.

References: Obsidian block anatomy and Lava with Obsidian ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks), [Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).

### The Helix endpoint behaves differently than the UI

1. Call endpoint directly.
2. Check security mode.
3. Check CSRF setting.
4. Check enabled Lava commands.
5. Check input validation.
6. Check rate limit.
7. Check cache control.
8. Check whether endpoint uses raw IDs.
9. Check whether endpoint assumes frontend-only access.
10. Check plugin/core path differences.

References: Helix security and endpoint source ([Helix Security](https://community.rockrms.com/developer/helix/overview/security), [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)).

### The grid is slow

1. Count rows sent to browser.
2. Check whether filtering is server-side.
3. Check columns and nested data.
4. Check export behavior.
5. Check attribute columns.
6. Consider server paging or a narrower query.
7. Avoid using Obsidian client-side grid for unbounded data.

Reference: Obsidian grids ([Grids](https://community.rockrms.com/developer/obsidian/grids)).

### The migration failed

1. Identify migration type: EF, plugin, hotfix, rollup/data.
2. Check Rock version requirement.
3. Check migration history.
4. Check duplicate GUIDs.
5. Check partially applied schema/data.
6. Check if a plugin-to-core transition exists.
7. Check SQL syntax/style.
8. Check helper method availability for the installed version.
9. Check transaction behavior.
10. Restore/test before retrying on production.

References: Developer 202 migrations and Codex migration rules ([The Data Migration](https://community.rockrms.com/developer/202---ignition/the-data-migration), [Writing Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations)).

### The TV app page is blank

Apple TV:

1. Confirm Rock v14+.
2. Confirm app API key.
3. Confirm demo key points to correct app.
4. Validate TVML.
5. Check page cache settings.
6. Check media URL compatibility.
7. Check app styles and theme mode.
8. Check page view/auth requirements.

Roku:

1. Confirm application settings.
2. Confirm API key.
3. Confirm authentication page if needed.
4. Validate SceneGraph XML.
5. Confirm outer `Rock:Page`.
6. Check focus management.
7. Check cacheability.
8. Test direct page response.

References: Apple TV and Roku docs ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

## 28. Agent Task Recipes

### Recipe: Answer "Where is this configured?"

1. Identify the named thing: page, block, app, endpoint, workflow, job, data view, mobile block, TV page, plugin.
2. Use the relevant docs to determine likely admin path.
3. Inspect live Rock for actual row/setting.
4. Report exact path, entity, GUID/IdKey if known, and security/cache caveats.
5. If docs are thin, say what must be inspected.

### Recipe: Review a Rock PR

1. Identify target Rock version/branch.
2. Identify technology surface.
3. Check naming conventions.
4. Check service layer boundaries.
5. Check generated code.
6. Check migration correctness.
7. Check security.
8. Check performance.
9. Check compatibility/public API.
10. Check tests/verification.
11. Check release notes if behavior changes user-facing contracts.

References: Codex coding standards, peer review, compatibility, testing ([Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards), [Suggestions on How to Peer Review](https://community.rockrms.com/developer/developer-codex/coding-standards/peer-reviews/suggestions-on-how-to-peer-review), [Tips for Maintaining Compatibility](https://community.rockrms.com/developer/developer-codex/coding-standards/maintaining-compatibility/tips-for-maintaining-compatibility), [Testing](https://community.rockrms.com/developer/developer-codex/coding-standards/testing)).

### Recipe: Diagnose "Works for admin but not staff"

1. Check page security.
2. Check block security.
3. Check block action security.
4. Check entity security.
5. Check endpoint security mode.
6. Check workflow type view/execute permissions.
7. Check API key/user permissions.
8. Check parent authority inheritance.
9. Check release-note security hardening.
10. Verify with the affected user/person.

References: 303 security, Helix security, release notes ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [Release Notes](https://www.rockrms.com/releasenotes)).

### Recipe: Build a source-backed answer

1. Start with official docs.
2. Use release notes for version changes.
3. Use source snippets for exact enum/field names.
4. Use Model Map/live schema for installed instance.
5. Cite docs inline.
6. State live verification requirements where behavior depends on installed version or configuration.

### Recipe: Build a Rock agent tool

1. Define a narrow use case.
2. Choose Lava tool or native tool.
3. Identify required data and permissions.
4. Design parameters.
5. Validate inputs.
6. Resolve entities safely.
7. Check authorization.
8. Limit output.
9. Add dry-run if write-capable.
10. Log writes.
11. Test with allowed, denied, missing, malformed, and high-volume cases.

Reference: AI Agents docs ([AI Agents](https://community.rockrms.com/developer/ai-agents)).
















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `26`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms' single-page form model, which matters when validating or troubleshooting nested form behavior. | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | implementation_pattern | Rock Apple TV documentation groups JavaScript command behavior as a core part of building TV applications, so TV app guidance should treat commands as part of navigation, media, utility, and demo workflows. | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| official | implementation_pattern | An Obsidian block combines a C# block, a TypeScript component, and block actions, so developer guidance should connect server logic, client UI, and action endpoints instead of treating a block as one file. | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| official | implementation_pattern | Roku commands are executed by setting a rockCommand and command-specific parameters on supported controls, and multiple commands can be chained by separating command names with commas. | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| official | operational_guidance | Rock plugin and theme packaging guidance frames the Rock Shop as the distribution path for community extensions, so plugin work should include packaging, review, and uninstall behavior rather than only local code changes. | [source](https://community.rockrms.com/developer/packaging-plugins-themes) |
| official | risk | Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| official | source_summary | Rock's Obsidian documentation is primarily written for the core developer team, but some sections such as Grids are published for broader public reading and require judgment when translating them to plugin development. | [source](https://community.rockrms.com/developer/obsidian) |
| official | source_summary | Helix is a Rock web-development surface that combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. | [source](https://community.rockrms.com/developer/helix/overview) |
| community-reviewed | implementation_pattern | A Rock Check-in implementation can involve process mapping and extended troubleshooting, not only enabling the check-in feature. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-47-special-edition-lee-peterson) |
| community-reviewed | operational_guidance | Rock Mobile development is part of the same product ecosystem as the core web platform, so mobile guidance should be routed alongside core profile, UX, and app-development context. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-94-special-edition-with-jay-nestle) |
| community-reviewed | operational_guidance | Contributor-authored KB material should aim for accessible explanations that church staff can use, not only developer-oriented technical detail. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-91-special-edition-with-cullen-mccoy) |
| More |  | 14 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->
















## 29. Source Map And Dependency Notes

### Community Examples And Q&A

Community examples are useful for spotting real developer pain, but they are not official behavior contracts. Treat the developing Q&A surface as a prompt for live verification and source inspection, not as final implementation authority. For example, the Rock Q&A developing area includes API and custom-development questions that can point an agent toward the right domain, but the agent still needs to validate the answer against official docs, source code, release notes, and the target instance before changing production behavior ([Developing for Rock Q&A](https://community.rockrms.com/ask/developing)).

Use community examples only after the authoritative chain is clear: official developer docs, current release notes, source-code landmarks, Model Map or live schema, then community examples as supporting context. If a Q&A answer conflicts with Developer Codex, source code, or installed-version behavior, prefer the stronger source and document the conflict.

This guide depends primarily on the following source families.

### Official developer docs

- [Developer Resources](https://community.rockrms.com/developer): top-level map for developer books, platform apps, and resources.
- [Developer Codex](https://community.rockrms.com/developer/developer-codex): standards, architecture, migrations, testing, review, compatibility.
- [Developer 101](https://community.rockrms.com/developer/101---launchpad): blocks and built-in entity work.
- [Developer 202](https://community.rockrms.com/developer/202---ignition/saving-custom-data): custom data and migrations.
- [Developer 303](https://community.rockrms.com/developer/303---blast-off): advanced jobs, workflow actions, filters, API, security, logging, RealTime.
- [Obsidian](https://community.rockrms.com/developer/obsidian): modern web UI development.
- [Helix](https://community.rockrms.com/developer/helix/overview): Lava/HTMX applications.
- [AI Agents](https://community.rockrms.com/developer/ai-agents): Rock-native agent tooling.
- [Mobile Docs](https://community.rockrms.com/developer/mobile-docs): Rock Mobile applications.
- [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs): TVML apps.
- [Roku Docs](https://community.rockrms.com/developer/roku-docs): Roku SceneGraph apps.
- [Slingshot](https://community.rockrms.com/developer/slingshot): migration tool.
- [API Documentation](https://community.rockrms.com/api-docs): API v1/v2 and shared resources.

### Official reference pages

- [Dynamic LINQ Syntax](https://community.rockrms.com/developer/dynamic-linq-syntax)
- [RealTime Visualizer](https://community.rockrms.com/developer/realtime-visualizer)
- [Rock Branches](https://community.rockrms.com/developer/rock-branches)
- [SQL Style Guide](https://community.rockrms.com/developer/sql-style-guide)
- [Design System](https://community.rockrms.com/developer/design-system)
- [Model Map](https://community.rockrms.com/ModelMap)
- [Release Notes](https://www.rockrms.com/releasenotes)

### Source-code landmarks

- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)
- [LavaEndpointSecurityMode TypeScript enum](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)
- [LavaEndpointHttpMethod TypeScript enum](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointHttpMethod.ts)
- [LavaApplicationBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts)
- [LavaEndpointBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)
- [AddLavaApplications migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)
- [WebForms-to-Obsidian replacement job](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs)
- [ContentChannelItemList block settings migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2019.0/Version%2019.0/202603202309228_AddContentChannelItemListBlockSettings.cs)

### Dependency notes

This guide depends on related topic guides for API integrations, Lava, Helix, Obsidian, Mobile, Plugins, Themes, Migration, Security, CMS, and TV Apps. It intentionally does not duplicate every API endpoint, Lava command, mobile control, TVML template, or Obsidian grid column reference. Instead, it tells agents where to look, what to verify, and how to avoid common operational mistakes.

The most important review items before publishing this guide are:

- Verify the current status of Helix core/plugin behavior in the target Rock versions.
- Verify current packaging plugin/theme procedures.
- Refresh Mobile block-specific details from current docs because the source pack excerpts are mostly navigation.
- Verify AI Agents tool APIs and security model against the installed Rock version.
- Confirm release-note caveats for v18/v19 against the actual target environment.
- Confirm source-code snippets from `develop` against stable release branches before using exact fields in production guidance.
