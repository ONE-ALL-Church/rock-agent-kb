---
id: authored-platform-configuration
title: Platform Configuration
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "57adb97ba7387f60137bea4f4a182f63a2eda9670cf28466f17e3349da5f5497"
---

# Platform Configuration

## Agent Summary

Platform configuration is a cross-cutting concern. Attributes extend entities with organization-specific data; Defined Types provide controlled sets of reusable values; categories organize configuration and presentation; entity types identify the kind of record being configured; campuses connect organizational sites to locations, schedules, status, type, and optional attributes. The supplied evidence supports these areas unevenly: attributes and campuses have current v19 documentation, while global attributes and general system settings have only routing-level evidence and therefore remain documented gaps. [Attributes documentation](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes) [Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

For agent work:

1. Identify the owning entity and operational outcome before changing configuration.
2. Separate the attribute definition from each entity’s stored attribute value.
3. Confirm that a Defined Value belongs to the Defined Type expected by every selector, workflow, and report.
4. Treat categories as scoped organizational and presentation structures, not interchangeable global folders.
5. Trace campus behavior through the campus, named location, schedule, block, and downstream workflow that consumes it.
6. Preserve security boundaries on attributes, pages, blocks, APIs, AI agents, skills, and tools.
7. Verify version-sensitive behavior against the installed build and current release notes.
8. Test the actual consuming surface. A saved configuration record does not prove that a form, report, mobile block, workflow, or embedded dashboard behaves correctly.

## Scope And Boundaries

This guide covers the evidence-supported configuration surfaces for:

- Attributes and attribute values.
- Defined Types and Defined Values.
- Categories and entity types.
- Campuses and campus attributes.
- Cross-domain configuration patterns involving reporting, AI agents, Lava tools, workflows, communications, registration, check-in, and upgrades.

This guide does not replace the owning guides for people, groups, workflows, CMS, security, Data Views, reports, check-in, communications, or event registration. It identifies their platform-level configuration dependencies and then routes detailed operational work back to those domains.

The evidence pack does not directly document the behavior, scope, storage, or administration of global attributes or general system settings. Their existence is visible in the official Attributes documentation index, but unsupported details must not be inferred from the index title. Those areas are therefore listed under **Known Gaps And Live Verification**. [Attributes documentation index](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes)

## Mental Model

Use this configuration chain:

1. **Entity type:** Identifies the kind of Rock record being extended or acted upon. Supplied source-code evidence shows entity types represented with names and friendly names, and shows entity-type-aware security grants that match an entity’s type before granting an action. This is implementation evidence from a specific commit, not proof of any installation’s current configuration. [Entity Types view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesBag.cs) [Entity type security rule](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)

2. **Attribute definition:** Describes custom data attached to an entity. The supplied developer documentation shows that attributes can be added at runtime and that entity-handling blocks can load, display, edit, and save their values. [Developer documentation: Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)

3. **Attribute value:** Stores the value for a particular attribute and entity. An immutable source excerpt demonstrates joins from `AttributeValue` to `Attribute`, `FieldType`, `EntityType`, and—when the entity is a Defined Value—to `DefinedValue` and `DefinedType`. This establishes the implementation relationships shown by that code, but not the contents of a live database. [Defined Value attribute-value query](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)

4. **Defined Type and Defined Value:** A Defined Type owns an ordered set of Defined Values. Supplied source code retrieves values by Defined Type and orders them by the value’s order and then its text. [DefinedValueService implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/DefinedValue/DefinedValueService.cs)

5. **Category:** Organizes attributes for administration or presentation. On the Person Profile, attributes are displayed by category, an attribute can belong to more than one category, and the Attribute Values block can be placed on different profile tabs. Category compatibility still depends on the owning entity type. [Extended Attributes Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab) [Display Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes)

6. **Consumer:** A form, block, workflow, report, mobile screen, integration, or agent uses the configuration. Validate this final consumer because field support, block settings, security, caching, version, and downstream joins can alter visible behavior.

When a request starts with a proposed screen, workflow, or automation, first restate the underlying problem and generate several distinct approaches. Treat the proposed implementation as requirements evidence rather than automatically accepting it as the solution. [Approved claim `claim:9ad17cb08b8955d0d3ec`](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=747s)

## Attributes And Attribute Values

### Choose the owning entity first

An attribute must be attached to the entity whose records actually own the data. For example, the documented campus procedure creates an Entity Attribute with an Entity Type of `Campus`; its value then appears on Campus Details. That procedure specifically says campus attributes do not require qualifier-field or qualifier-value entries. Do not generalize that qualifier rule to other entity types. [Add Attributes to Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses)

Before creating an attribute, record:

- The business meaning of the value.
- The owning entity type.
- The field type required by the consuming surfaces.
- Whether qualifiers narrow the attribute’s scope.
- The category or categories used to present it.
- Who may view, edit, or administer it.
- Which forms, blocks, workflows, reports, integrations, or agents will consume it.
- Whether existing records need values or whether a default is sufficient.

Do not create the same concept on several entity types merely to make it convenient for one report. If ownership is unclear, stop and resolve it before introducing competing sources of truth.

### Separate the definition from stored values

The attribute definition and an entity’s value are distinct. The supplied implementation query joins the value to its attribute definition and field type, and then uses the value’s `EntityId` to associate it with a Defined Value in that particular query. An agent diagnosing attribute data should therefore inspect both configuration and stored values instead of assuming that a visible label describes how the data is stored. [Defined Value attribute-value query](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)

For developer-owned blocks, the official developer guide shows an explicit lifecycle:

1. Load the entity’s attributes.
2. Add display controls with the appropriate view authorization.
3. Add edit controls, optionally with edit authorization.
4. Read edited values.
5. Save the entity and its attribute values together in a transaction.

That sequence is implementation guidance for custom development. It should not be treated as evidence that an installed custom block follows it correctly. [Developer documentation: Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)

### Present attributes intentionally

On the Person Profile’s Extended Attributes area, only attributes with values are displayed, and attributes are grouped under category headers. Users with Administrate access to the attribute block can reorder them, while editing values is initiated from the category header. [Extended Attributes Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab)

A Person Attribute can belong to more than one category. An Attribute Values block can be placed in a zone on different Person Profile tabs and configured for a specific category. Consequently, “the attribute exists” does not prove that it is visible on a particular page: inspect the attribute’s categories, the page’s blocks, each block’s category setting, and the current person’s authorization. [Display Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes)

### Account for channel-specific support

The mobile Attribute Values block displays and edits attributes selected by category and entity type, but editing is limited to field types supported by the mobile shell. Its category list can include categories that are incompatible with the selected entity type; the administrator is responsible for choosing a compatible pair. It can also use an attribute’s abbreviated name when configured to do so. [Mobile Attribute Values block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)

Do not assume that a web-editable attribute is mobile-editable. Verify the current supported-field-type list and test the actual mobile shell.

### Attribute release issues

The supplied release records identify category and attribute defects that matter during diagnosis:

- Rock v19.1 fixed multiple attribute-editing blocks whose Category dropdown showed Global Attribute categories instead of categories for the attribute’s actual entity type. [Rock Core release notes](https://www.rockrms.com/releasenotes)
- Rock v17.2 fixed a Content Channel Type Detail issue that showed incorrect or unrelated categories while editing Content Channel Item attributes. [Rock Core release notes](https://www.rockrms.com/releasenotes)
- The supplied v19.3 release-note excerpt reports fixes involving indexed Person Attribute Values, Defined Value attributes on Event Items, and inherited Group Member attributes created during group copying. These are version-specific defects, not general attribute behavior. [Rock Core release notes](https://www.rockrms.com/releasenotes)

When a category or value behaves unexpectedly, establish the exact Rock version before redesigning the configuration around what may be a fixed defect.

## Defined Types And Values

### Use the type as the controlled vocabulary boundary

A Defined Type owns its Defined Values. The supplied implementation retrieves values by `DefinedTypeId` and returns them in configured order, with the value text used as a secondary ordering key. [DefinedValueService implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/DefinedValue/DefinedValueService.cs)

Treat that ownership as part of the data contract:

- A selector should return values from the intended Defined Type.
- A stored reference should resolve to a value from that same type.
- Reports and workflows should join or interpret the stored value consistently.
- Ordering should be verified where the consuming surface depends on it.
- Renaming, disabling, replacing, or deleting a value should be evaluated against every consumer.

Supplied source code contains deletion checks that can refuse removal of Defined Types or Defined Values when referenced by other records. The excerpt does not enumerate every possible dependency, so a successful or refused deletion must be evaluated in the installed version rather than predicted from this guide. [DefinedTypeService deletion check](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/CodeGenerated/DefinedTypeService.CodeGenerated.cs) [DefinedValueService deletion checks](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs)

### Defined Value attributes

The supplied immutable SQL excerpts show attributes scoped to the `Rock.Model.DefinedValue` entity type, including a pattern that qualifies those attributes by `DefinedTypeId`. They also show how stored values can be associated with each Defined Value and its owning Defined Type. This is implementation evidence from the referenced commit, not a universal configuration prescription. [Defined Type attributes query](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql) [Defined Value attribute-value query](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)

A reviewed community pattern uses a Defined Value attribute as a seasonal visibility switch:

1. Keep stable options in one Defined Type.
2. Add a boolean or similarly scoped attribute to its values.
3. Filter the workflow selector by that attribute.
4. Update the switches as part of the seasonal runbook.
5. Verify the rendered dropdown after each update.

This is a community pattern requiring local verification, not documented universal Rock behavior. The local field type, qualifier, data source, caching, and form implementation must be inspected before adoption. [Model Map](https://community.rockrms.com/ModelMap) [Rock U workflows](https://community.rockrms.com/rocku/workflows)

### Detect source mismatches

Another reviewed community pattern warns that a workflow selector may accept a value from one Defined Type even though an attribute or downstream report expects another. Submission success alone would not prove semantic consistency.

Inspect:

- The attribute’s field type and configuration.
- Any qualifier identifying the expected Defined Type.
- The selector’s SQL, Lava, or other data source.
- The raw storage format used by the Attribute Value.
- Workflow actions that copy or transform the value.
- Report joins to `DefinedValue` and `DefinedType`.
- Existing records created before the current configuration.

Do not “fix” the report by joining to whichever Defined Type happens to produce a label. Resolve which source is authoritative, assess existing data, and then align capture and reporting. This contribution explicitly requires live verification. [Model Map](https://community.rockrms.com/ModelMap) [Rock U workflows](https://community.rockrms.com/rocku/workflows)

### API and automation boundary

At the supplied immutable commit, Rock’s generated v2 model controllers expose authenticated endpoints for Defined Types, Defined Values, and Entity Types. Their item lookup accepts an ID, GUID, or IdKey, while read and write operations have separate security actions. This describes the referenced implementation only; endpoint availability and authorization must be confirmed in the installed build. [Defined Types controller](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/DefinedTypesController.CodeGenerated.cs) [Defined Values controller](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/DefinedValuesController.CodeGenerated.cs)

For agent-facing context, pass IdKeys rather than raw integer identifiers. Keep parameters explicit and sanitized so an agent does not have to infer the intended entity or vocabulary. [Approved claim `claim:57e32b4d554a759231a1`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s)

## Categories And Entity Types

### Categories are scoped configuration

Categories organize attributes and other supported records, but a category name alone does not establish compatibility. Person attributes can be assigned to multiple categories for display, while the mobile Attribute Values block exposes a category list that may include entries incompatible with its selected entity type. [Display Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes) [Mobile Attribute Values block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)

When choosing or troubleshooting a category, verify:

1. The category’s intended entity or feature scope.
2. The attribute’s entity type and qualifiers.
3. The block or screen’s selected category.
4. The block’s selected or contextual entity type.
5. View, edit, and Administrate permissions.
6. The installed version’s known category defects.

A category appearing in a dropdown is not proof that it is valid for the current entity. Rock v19.1 specifically fixed dropdowns that showed Global Attribute categories instead of categories for the attribute’s actual entity type. [Rock Core release notes](https://www.rockrms.com/releasenotes)

### Entity types are infrastructure, not free-form labels

The supplied source implementation represents an entity type with a technical name, friendly name, identifier, security status, and optional detail-link template. Another excerpt shows security grants that match an object’s entity type before granting an action. These details explain why entity-type selection affects attributes, security, navigation, and API behavior. They do not prove which types, permissions, or plugins exist in a particular installation. [Entity Types view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesBag.cs) [Entity type security rule](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)

Do not create, delete, or substitute an entity type merely because its friendly name resembles the requested record. The supplied implementation includes extensive reference checks before deleting an Entity Type, including references from attributes, authorization records, providers, and AI-related records. The excerpt is incomplete, so dependency analysis remains mandatory. [EntityTypeService deletion checks](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/CodeGenerated/EntityTypeService.CodeGenerated.cs)

## Campuses And Global Settings

### Campus configuration

Rock uses campuses for organizational sites. In a single-campus configuration, campus selection is generally hidden; when a block requires a campus, the single configured campus is automatically used, while an optional campus value can remain blank. [Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

Campuses are maintained under `Admin Tools > Settings > Campuses`. The v19 documentation requires a named location with a Location Type of `Campus` before it can be assigned to a campus. An online campus still requires a location of that type. [Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

The documented Campus Details surface includes name, active state, description, status, type, opened and closed dates, code, leader, location, phone, URL, schedules, topics, and legacy service times. Important operational distinctions include:

- A campus can be created as inactive while configuration and communications are prepared.
- Campus Status and Campus Type use predefined Defined Types. Rock ships documented default values, and the supplied documentation says those shipped values should not be deleted, although their names can be changed and additional values can be added.
- Campus schedules can be associated directly with a campus and may be consumed by blocks such as Service Metrics Entry.
- Campus topics associate an email address with a topic whose type is a Defined Value.
- Service Times is marked legacy in the supplied v19 documentation, which directs administrators toward Campus Schedules for longer-term support.
- When upgrading from an older version without Status and Type configuration, the documentation describes automatic assignments. Verify the actual post-upgrade records rather than assuming the migration produced the intended organizational classification.

[Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

### Campus attributes

To add campus-specific data:

1. Open `Admin Tools > Settings > Entity Attributes`.
2. Add an attribute.
3. Select `Campus` as the Entity Type.
4. Configure the attribute without a qualifier field or qualifier value.
5. Save it.
6. Configure attribute security if needed.
7. Set and verify a value on Campus Details.

[Add Attributes to Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses)

### Room capacity and schedule availability

A reviewed community contribution distinguishes room capacity from schedule availability in check-in configuration. It reports that a room’s soft capacity threshold belongs to the Location, while schedule availability is expressed through the group-location relationship and its linked schedules. The recommended preflight compares the group, group location, physical location, threshold, and schedule link before a production change.

Treat this as a community implementation pattern requiring local schema and configuration verification. Do not assume a capacity change is limited to one service time when the same room is reused. [Model Map](https://community.rockrms.com/ModelMap) [Rock U Check-In Manager](https://community.rockrms.com/rocku/check-in/check-in-manager-1)

### Global attributes and system settings

The supplied official Attributes index links to a Global Attributes topic, establishing that the topic exists in the v19 documentation hierarchy. The evidence pack does not supply the topic’s answer-bearing content, nor does it supply direct documentation for general system settings. This guide therefore does not assert their storage rules, precedence, caching, security behavior, administration routes, or supported values. [Attributes documentation index](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes)

Any task involving a global attribute or system setting must inspect the current official article and installed configuration before proposing a change.

## Analytics And Reporting Configuration

The following are reviewed community operating patterns, not universal requirements.

Rock metrics can provide scheduled historical capture: expensive values can be calculated off-hours, stored repeatedly, and visualized later without recomputing the full operational query on every dashboard load. The approved claim includes a bounded read-only verification of the `Metric`, `MetricValue`, and `Schedule` surfaces in one connected instance; that verification does not establish another installation’s job configuration or data quality. [Approved claim `claim:00ccd91253b6bea7c870`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp)

Expensive journey analytics can similarly be calculated into a persisted dataset on a schedule. The approved claim includes bounded verification that the inspected installation had a `PersistedDataset` surface with refresh, schedule, result, cache, Lava-command, and build-script fields. Confirm the installed schema and actual schedule before depending on the pattern. [Approved claim `claim:01d746f9a6bc23a6d503`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

Analytics-enabled tables can act as a snapshot layer for daily engagement counts or trends consumed by external reporting tools. This can reduce repeated reconstruction of operational history, but the design still needs clear metric definitions, a refresh policy, security, and a reconciliation path back to Rock. The supporting approved claim was live-verified only at the feature-surface level in one instance. [Approved claim `claim:a5f0a54f29d226cec5fc`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz)

When embedding Power BI or a similar report in Rock, enforce both sides of access:

- Put the Rock page and blocks behind appropriate Rock security roles.
- Confirm the external provider’s licensing and access requirements.
- Test with authorized and unauthorized representative accounts.
- Do not infer external BI licensing from Rock’s page authorization.

The approved claims include bounded verification of Rock `Page`, `Block`, and `Auth` surfaces, but explicitly do not verify external licensing. [Approved claim `claim:60d40983fd53c0173dd9`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) [Approved claim `claim:ffba67d8847c47e68ea6`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz)

## AI Agents, Lava Tools, And Extensions

Rock’s agent model separates agents, skills, and tools, with configuration and security boundaries at each layer. Chat versus MCP and Internal versus Public are separate choices. Expose only tools authorized for the current person and agent. [Approved claim `claim:b4fb38224ff8452078f3`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s)

Prompt context can include Rock’s core prompt, an organization prompt, agent instructions, skill instructions, and current-person context. Keep each layer concise, add instructions when testing demonstrates a need, and pass IdKeys instead of raw integer identifiers. [Approved claim `claim:57e32b4d554a759231a1`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s)

For custom tools:

- Use clear verb-and-entity names.
- Shape results intentionally—for example, Lookup, List, Get, Summary, Insights, AvailableAttributes, or AddOrUpdate.
- Bound results so unnecessary records do not consume the model’s context.
- Make parameters explicit and sanitized.
- For Lava tools, return structured `AgentToolResult` values and use the dedicated filters for instructions, compact history, metadata, and Rock reference routes.
- Inspect built-in tool logs for calls, inputs, and results during debugging.

[Approved claim `claim:60c2bcd25e1cce4efef4`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s) [Approved claim `claim:4b7b8d0b0379ceb7587f`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s)

Do not expose arbitrary runtime SQL generation and execution to an agent. The approved guidance distinguishes that unsafe capability from reviewed static SQL inside a narrowly secured Lava tool. [Approved claim `claim:c3921cb1d8b61e06c713`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s)

Rock-side skills and tools provide platform capabilities, while an external harness may hold organization-specific business rules. Govern and version both layers; do not assume MCP tools contain local process policy. [Approved claim `claim:538f1a4e0ad7c90f7c5a`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=909s)

When work must survive a conversation, have the agent produce a durable file or handoff artifact rather than leaving the result only in transient chat. [Approved claim `claim:679a38216f2b07097624`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=713s)

For community plugins and themes, configuration work includes packaging, review, distribution through the Rock Shop path, and uninstall behavior—not only local code changes. [Packaging Plugins and Themes](https://community.rockrms.com/developer/packaging-plugins-themes)

## Cross-Domain Version 19 Configuration

The following behaviors are specifically scoped to Rock v19 in the approved evidence and must be checked against the installed build.

### Experience modes

Rock v19 begins the organization-wide Essentials and Trailblazer experience-mode rollout. The selected mode changes visible pages, settings, and help content. Supported settings screens can preview both levels, but not every block is necessarily mode-aware. Do not diagnose a missing option until the organization mode, screen preview, block version, and permissions have been checked. [Approved claim `claim:1eb3f0a262c65737970a`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=96s)

### CAPTCHA

Rock v19 introduces built-in proof-of-work CAPTCHA with organization-level and block-level controls. Confirm whether each exposed form is configured for visible, invisible, or disabled behavior, then test every public entry path. [Approved claim `claim:5073aebf878a8fbe7c63`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=155s)

### Check-in

The v19 Check-In Manager roster uses real-time updates so attendance state changes can appear without a manual refresh. If updates lag, inspect browser connectivity, block version, and local check-in configuration. [Approved claim `claim:7df4b8c20f9419a30a5a`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=262s)

### Event registration

When several v19 registrant-eligibility rules are enabled, a registrant must satisfy all selected criteria. Test combined age, gender, grade, and Data View rules with representative people before opening registration. [Approved claim `claim:1d4e4b914d16049aee7c`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=445s)

The v19 Prevent Duplicate Registrants option blocks a matched person from being registered twice. Its warning can reveal that a person is already registered to someone who knows sufficient matching details, so evaluate the disclosure risk before enabling it for a sensitive event. [Approved claim `claim:33a7cc3b7e0626ec5cc1`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=357s)

### Communications and workflows

The v19 Communication Wizard distinguishes personal or need-to-know messages from bulk or marketing messages. Block settings can customize the labels and descriptions, so local wording should help senders classify messages consistently. [Approved claim `claim:809519cf51bf3b32119f`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=627s)

A v19 SMS Pipeline send action can save its response so the automated message appears in Communication History, the person’s history, and SMS Conversations. Enable this deliberately when auditability is needed and account for the additional retained history. [Approved claim `claim:c8435f854b9e7075ab76`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=684s)

The v19 Unsubscribe Report can show recipient, send and unsubscribe timing, communication type or topic, and sender. Use those fields to investigate patterns and coach senders rather than assigning every unsubscribe to one cause. [Approved claim `claim:147ee6dbc7db220dc7ba`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=714s)

Rock v19 adds workflow actions for Rock Chat channel and direct messages. Before operational use, verify Rock Chat configuration, recipient resolution, workflow security, and actual delivery. [Approved claim `claim:f8380a3e786ab33df98f`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1056s)

### Person merge and record provenance

The v19 merge interface surfaces last-modified time and actor information. Treat recency as one review signal, not proof that a record is correct. [Approved claim `claim:f39e0cab003d876835c1`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=845s)

A requester without merge permission can ask to be notified when the reviewed merge completes, preserving separation between requesting and authorizing a merge. [Approved claim `claim:b81391274ac89ca6c69f`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=902s)

If a merge changes the surviving last name, v19 can add the former value to Previous Last Names. Verify local field visibility and data-handling policy before relying on that continuity. [Approved claim `claim:23c173130e89f0eba735`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=963s)

External person-entry blocks can assign record sources, and v19 can show that source in duplicate details. Configure and test the source on each entry block used for duplicate investigation. [Approved claim `claim:5d80cd1847429a0181d0`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=790s)

### Schedules, diagnostics, and Lava

Rock v19 materializes recurring iCal occurrences into `ScheduleDate` rows. Date-based SQL and Lava work should use those generated dates instead of inventing another recurrence-expansion process. Confirm the installed schema and date generation before migrating a query. [Approved claim `claim:4c4098a035a5ca256bfe`](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)

The v19 Page Load Time diagnostic can expose page-debug timing traces without separate observability setup. Use it to identify slow page components, then corroborate intermittent or infrastructure-wide problems with broader telemetry. [Approved claim `claim:091606bd3b8b0472392a`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s)

Rock v19 adds a `contains` parameter to the Lava `where` filter for partial field matching. Confirm current case behavior, type behavior, and query performance before applying it to broad data sets. [Approved claim `claim:524be15ef7a48290a72a`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1080s)

## Change Management And Operational Governance

Self-hosted operators own their Rock patch cadence. Supported dot releases can include security fixes and should not be treated as optional without review. Confirm supported branches and read current release notes immediately before an upgrade. [Approved claim `claim:e78d41d7fefc84b6e9e7`](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s)

Major-version and patch-release validation are different scopes. Large releases can accumulate broad functional change, while later patches may correct post-release defects. The historical community claim supporting this distinction requires current live verification before use in an upgrade decision. [Approved claim `claim:900a195ee6880a693f27`](https://shows.acast.com/rock-cast/episodes/episode-33-rock-73-and-new-rx2018-tracks)

Prepare users as part of configuration deployment:

- Before exposing staff to a changed Rock interface, prepare and distribute a short targeted video. [Approved claim `claim:c9c1fa08cb0434d501e6`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1714s)
- For the redesigned v19 Connections experience, show active connectors the interface and provide brief training before deployment. [Approved claim `claim:07a75e5ff71510d708de`](https://www.youtube.com/watch?v=edanHiYSDIM&t=91s)
- Rock’s LMS can assign curricula by staff role and track completion, subject to installed-version configuration and permissions. [Approved claim `claim:91be2ad338eb6b1cdaed`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1983s)
- Train and activate staff before expecting them to train volunteers. [Approved claim `claim:c8c3a60f71790dd3616d`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s)
- Correct Rock training reduces the risk of teams adopting disconnected tools that fragment workflows and the system of record. [Approved claim `claim:4b083dda9f0d9ccc4aff`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2042s)

## Version And Authority Caveats

- The core attributes and campus administration excerpts are official documentation labeled v19.0.
- The v19 feature claims come from approved official Rock media. They remain release-sensitive and should be checked against current written documentation and the installed build.
- The category fixes are version-specific release-note evidence. A defect fixed in one version should not be generalized to every version.
- Source-code observations refer only to immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They explain implementation relationships but do not prove live schema, configuration, plugin state, or permissions.
- Analytics recommendations are community-reviewed operating patterns. Some carry a bounded, public-safe read-only verification of feature surfaces in one connected instance; none proves another installation’s schedules, values, security, or output.
- Defined Value seasonal gating, source-mismatch diagnosis, and room-capacity preflights are reviewed community contributions requiring live verification.
- External BI access depends on both Rock authorization and the external provider’s licensing. The evidence verifies only the existence of relevant Rock-side security surfaces in the reviewed instance.
- The hydrated release page included newer release headings, including an alpha release, but headings and source summaries are not sufficient evidence for feature guidance. This guide does not promote them into current behavior.
- No new live-instance verification was performed for this synthesis.

## Troubleshooting Decision Tree

### An attribute exists but is not visible

1. Confirm the attribute’s owning entity type.
2. Confirm the current record is that entity type.
3. Check whether the current display only shows attributes that have values.
4. Inspect the attribute’s category assignments.
5. Inspect the Attribute Values block’s selected category and entity context.
6. Check view, edit, and Administrate authorization.
7. If this is mobile, verify that the field type is supported by the mobile shell.
8. Check the installed version for relevant attribute or category fixes.
9. Stop when visibility, editability, and persistence have been verified with an authorized representative user.

[Extended Attributes Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab) [Mobile Attribute Values block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)

### A category dropdown shows unrelated categories

1. Record the Rock version and exact editing block.
2. Confirm the attribute’s entity type and qualifiers.
3. Confirm the intended category’s scope.
4. Check whether the installation includes the v19.1 fix for Global Attribute categories appearing in unrelated attribute editors.
5. For Content Channel Item attributes, check the v17.2 category fix.
6. Do not reclassify attributes merely to work around a known version defect.

[Rock Core release notes](https://www.rockrms.com/releasenotes)

### A workflow stores a value but the report shows the wrong label

1. Identify the attribute and expected Defined Type.
2. Inspect the selector’s actual data source.
3. Resolve the stored value to its Defined Value and owning Defined Type.
4. Compare workflow transformations and report joins.
5. Sample records from before and after configuration changes.
6. Decide which Defined Type is authoritative.
7. Stop before bulk correction until the affected records and downstream consumers are bounded.

This follows a reviewed community pattern requiring live verification. [Model Map](https://community.rockrms.com/ModelMap)

### Seasonal options are missing or still selectable

1. Confirm the form uses the intended Defined Type.
2. Inspect the visibility attribute on every relevant Defined Value.
3. Inspect the selector’s filter.
4. Check caching or persisted output used by the form.
5. Render the form as a representative user.
6. Confirm retired options are absent and new options are selectable.

This follows a reviewed community pattern requiring live verification. [Rock U workflows](https://community.rockrms.com/rocku/workflows)

### A campus selector is absent or chooses a campus automatically

1. Count the active, configured campuses.
2. If there is one campus, account for documented single-campus behavior.
3. Determine whether the consuming block requires a campus or treats it as optional.
4. Inspect the block, page context, and record being edited.
5. Verify that unexpected behavior is not caused by permission or experience-mode differences.

[Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

### A campus cannot use the intended location

1. Verify the named location exists.
2. Verify its Location Type is `Campus`.
3. Confirm the correct location is selected on Campus Details.
4. For an online campus, do not omit the location; verify the chosen location is the intended association.
5. Stop when the campus saves and the consuming surface resolves the expected location.

[Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

### Check-in room capacity or availability is wrong

1. Identify the exact check-in group, group location, location, and schedule.
2. Inspect the room threshold separately from schedule linkage.
3. Determine whether the location is reused at other times.
4. Verify the expected schedule is linked through the group-location configuration.
5. Review downstream check-in behavior before changing a shared location threshold.
6. Stop before mutation if the local schema or installed block differs from the reviewed community pattern.

[Model Map](https://community.rockrms.com/ModelMap) [Rock U Check-In Manager](https://community.rockrms.com/rocku/check-in/check-in-manager-1)

### A dashboard is slow

1. Identify whether the page recalculates historical operational data on every request.
2. Determine whether a Rock metric, persisted dataset, or analytics snapshot can answer the same bounded question.
3. Establish refresh frequency and acceptable staleness.
4. Schedule expensive computation outside peak use where appropriate.
5. Validate the stored result against the operational source.
6. Use v19 Page Load Time traces for page-component diagnosis when applicable.
7. Corroborate intermittent or infrastructure-wide findings with broader telemetry.

[Approved claim `claim:01d746f9a6bc23a6d503`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) [Approved claim `claim:091606bd3b8b0472392a`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s)

### An embedded BI report is inaccessible or overexposed

1. Check Rock page and block authorization.
2. Test an authorized Rock account.
3. Test an unauthorized Rock account.
4. Check the external BI identity and license.
5. Confirm that embedding does not bypass the intended external access boundary.
6. Stop when both Rock authorization and provider access are independently demonstrated.

[Approved claim `claim:60d40983fd53c0173dd9`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)

### The v19 Check-In Manager roster does not update live

1. Confirm the installed version and block version.
2. Confirm the attendance change was committed.
3. Check browser connectivity.
4. Inspect local check-in configuration.
5. Compare behavior in another supported browser or session.
6. Do not diagnose the problem as general database latency without broader evidence.

[Approved claim `claim:7df4b8c20f9419a30a5a`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=262s)

### A v19 registration rejects an apparently eligible person

1. List every enabled eligibility rule.
2. Remember that all selected criteria must be satisfied.
3. Evaluate age, gender, grade, and Data View results separately.
4. Test representative people at each boundary.
5. Re-test the combined rule set.
6. Stop before opening registration if expected boundary cases still fail.

[Approved claim `claim:1d4e4b914d16049aee7c`](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=445s)

### An agent chooses the wrong tool or returns too much data

1. Check whether the tool name clearly expresses a verb and entity.
2. Check parameter names, descriptions, and sanitization.
3. Replace broad results with a bounded result shape.
4. Review the agent, skill, and tool authorization layers.
5. Inspect built-in tool logs for the actual call, input, and result.
6. Remove open-ended SQL execution capability.
7. Re-test with the current-person security context.

[Approved claim `claim:60c2bcd25e1cce4efef4`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s) [Approved claim `claim:c3921cb1d8b61e06c713`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s)

## Agent Task Recipes

### Recipe: Add and verify a campus attribute

**Outcome:** A secured campus attribute is visible and stores the intended value on Campus Details.

1. Define the value’s purpose and confirm Campus is the correct owner.
2. Open `Admin Tools > Settings > Entity Attributes`.
3. Add an attribute with Entity Type `Campus`.
4. Leave the qualifier field and value empty, as directed by the campus documentation.
5. Configure the field type and presentation details supported by the requirement.
6. Save the attribute.
7. Configure attribute security.
8. Open Campus Details and set a test value.
9. Verify visibility and editability as representative authorized and unauthorized users.
10. Record downstream consumers that rely on the value.

**Do not assume:**

- Saving the definition creates values for existing campuses.
- Administrative access implies every user can view or edit the value.
- Web support proves mobile support.

[Add Attributes to Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses)

### Recipe: Place person attributes on a profile tab

**Outcome:** A selected category of Person Attributes appears in the intended profile location.

1. Confirm that the attributes belong to the Person entity.
2. Assign the intended category or categories.
3. Use the Admin Toolbar and Zone Editor to add an Attribute Values block to the intended profile tab.
4. Configure the block for the specific category.
5. Review block authorization.
6. Test a person with populated values.
7. Test the edit path with a permitted user.
8. Test the view path with a user who should not edit.
9. Remember that the Extended Attributes area may omit attributes without values.

**Stop when:**

- The correct attributes appear in the intended location.
- Editing persists the values.
- Unauthorized access is denied.

[Display Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes)

### Recipe: Audit a Defined Value source mismatch

**Outcome:** Capture, storage, and reporting use the same intentional Defined Type.

1. Identify the affected workflow attribute or form field.
2. Record the expected Defined Type.
3. Inspect the selector’s SQL, Lava, or other data source.
4. Resolve sample stored values to their Defined Values and parent Defined Types.
5. Inspect workflow actions that copy or transform the value.
6. Inspect downstream joins and filters.
7. Classify existing mismatches by source and date.
8. Choose the authoritative Defined Type with the process owner.
9. Prepare separate capture and historical-data corrections.
10. Re-test submission and reporting before rollout.

**Stop when:**

- The authoritative source is ambiguous.
- Existing data impact is unbounded.
- A correction would require production writes not separately approved.

This is a reviewed community recipe requiring live verification. [Model Map](https://community.rockrms.com/ModelMap)

### Recipe: Operate seasonal Defined Value options

**Outcome:** A stable vocabulary exposes only the intended seasonal options.

1. Confirm the options are stable enough to remain in one Defined Type.
2. Define or verify a scoped visibility attribute on its Defined Values.
3. Update the attribute for the coming season.
4. Inspect the form’s selector filter.
5. Refresh any relevant cached or persisted output.
6. Render the form as a representative user.
7. Verify retired options are absent.
8. Verify newly enabled options submit and report correctly.
9. Add this verification to the recurring seasonal runbook.

**Do not assume:**

- A changed Defined Value attribute immediately changes a cached form.
- Hidden options cannot remain in historical records.
- A successfully submitted value came from the intended Defined Type.

This is a reviewed community recipe requiring live verification. [Rock U workflows](https://community.rockrms.com/rocku/workflows)

### Recipe: Stage a campus

**Outcome:** A campus is configured without prematurely exposing it as active.

1. Create the required named location with Location Type `Campus`.
2. Create the campus as inactive.
3. Assign its name, code, status, type, dates, leader, location, contact details, and URL as applicable.
4. Associate the intended campus schedules.
5. Configure topics and campus attributes only where required.
6. Avoid building new dependencies on legacy Service Times.
7. Test downstream blocks and reports with the campus inactive.
8. Prepare staff and public communication.
9. Activate only after the dependent surfaces have been verified.

[Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses)

### Recipe: Move an expensive dashboard calculation to scheduled storage

**Outcome:** The dashboard reads a verified stored result instead of rebuilding all history on every request.

1. Define the decision the dashboard supports.
2. Measure or reproduce the expensive calculation.
3. Choose a Rock metric, persisted dataset, or analytics snapshot based on the required output.
4. Set an acceptable refresh interval.
5. Schedule the calculation away from peak use where appropriate.
6. Store enough context to reconcile the result to its operational source.
7. Compare several stored results with direct calculations.
8. Update the dashboard to read the stored layer.
9. Monitor refresh failures and data age.
10. Retain a documented fallback for stale or missing results.

**Do not assume:**

- Stored means correct.
- A schedule exists merely because the schema supports one.
- One organization’s verified schema proves the same feature is configured elsewhere.

[Approved claim `claim:00ccd91253b6bea7c870`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp) [Approved claim `claim:01d746f9a6bc23a6d503`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

### Recipe: Secure an embedded BI report

**Outcome:** Only appropriately authorized and licensed users can open the embedded report.

1. Identify the Rock page and block that host the report.
2. Define the Rock roles that should have access.
3. Apply and inspect page and block authorization.
4. Identify the external BI license and identity requirements.
5. Test an authorized, licensed user.
6. Test an authorized but unlicensed user.
7. Test an unauthorized Rock user.
8. Confirm that report links or embed behavior do not create a bypass.
9. Document both Rock-side and provider-side ownership.

**Stop when:**

- External licensing is unknown.
- Anonymous or unauthorized access cannot be ruled out.
- Testing covered only an administrator account.

[Approved claim `claim:60d40983fd53c0173dd9`](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)

### Recipe: Preflight a v19 configuration change

**Outcome:** A version-sensitive feature is enabled with its dependencies and risks tested.

1. Confirm the installed Rock version and relevant block version.
2. Read the current documentation and release notes for that build.
3. Identify organization-level, block-level, security, provider, and workflow dependencies.
4. Build representative success, denial, and boundary cases.
5. Test the feature in the actual consuming surface.
6. Review privacy and disclosure effects, especially duplicate-registration warnings and retained communication history.
7. Prepare brief staff training for changed interfaces.
8. Obtain the appropriate operational approval.
9. Deploy in a bounded window.
10. Verify visible behavior and retained records after deployment.

[Approved v19 feature walkthrough](https://www.youtube.com/watch?v=c-wycR9HEuQ)

### Recipe: Design a bounded Rock agent tool

**Outcome:** An authorized tool performs one clear task and returns a controlled result.

1. Define the underlying task and current-person authorization boundary.
2. Decide whether the capability belongs in a Rock tool, Rock skill, or external organization skill.
3. Name the tool with a clear verb and entity.
4. Define explicit, sanitized parameters.
5. Use IdKeys rather than raw integer identifiers in agent context.
6. Choose a bounded result shape.
7. For Lava, return a structured `AgentToolResult`.
8. Use reviewed static logic where database access is necessary; do not expose arbitrary SQL execution.
9. Enable only the tool required for the agent and audience.
10. Exercise success, empty, invalid, unauthorized, and oversized-result cases.
11. Inspect tool logs for calls, inputs, and outputs.
12. Version the tool and associated business-rule instructions.

[Approved claim `claim:4b7b8d0b0379ceb7587f`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s) [Approved claim `claim:b4fb38224ff8452078f3`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s)

### Recipe: Plan a Rock upgrade as configuration change

**Outcome:** The upgrade covers technical validation, security maintenance, and staff adoption.

1. Confirm the supported branches and current release notes.
2. Separate major-version test scope from patch-release test scope.
3. Inventory affected pages, blocks, workflows, integrations, attributes, categories, registrations, communications, and check-in surfaces.
4. Test with non-administrator roles as well as administrators.
5. Re-test previously affected version-specific defects.
6. Prepare short targeted training for visible workflow changes.
7. Assign role-based training where the configured LMS supports it.
8. Train staff before volunteer rollout.
9. Apply the upgrade through the organization’s controlled release process.
10. Verify the installed build and representative workflows after deployment.

[Approved claim `claim:e78d41d7fefc84b6e9e7`](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s) [Approved claim `claim:c9c1fa08cb0434d501e6`](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1714s)

## Known Gaps And Live Verification

- **Global attributes:** The evidence pack supplies only an official documentation index link, not the answer-bearing Global Attributes article. Verify scope, precedence, security, caching, value access, and administration in current documentation and the installed version.
- **System settings:** No direct source excerpt documents the system-settings surface. Do not infer setting names, defaults, storage, or impact.
- **Defined Type administration UI:** The pack supports model relationships and selected implementation behavior, but not a complete current administrative walkthrough.
- **Category administration:** The evidence supports attribute grouping, multi-category Person Attributes, entity compatibility, and selected bug fixes, but not every category-capable entity or security rule.
- **Mobile field support:** The mobile block is limited to supported field types, but the supplied pack does not enumerate the current list.
- **Community recipes:** Seasonal Defined Value gating, Defined Type mismatch diagnosis, and room-capacity preflights require validation against the installed schema and configuration.
- **Analytics:** Confirm jobs, schedules, refresh status, security, data age, and reconciliation in the target installation. Feature-surface verification from another instance is not sufficient.
- **External BI:** Rock-side page authorization does not verify external licensing, tenant configuration, identity mapping, or embed policy.
- **Version 19 features:** Confirm the installed build, block generation, permissions, and local configuration before relying on any v19 behavior.
- **Experience modes:** The evidence does not enumerate every mode-aware page or block.
- **Schedule dates:** Verify that recurring dates are being materialized correctly before replacing existing recurrence logic.
- **AI agents:** Confirm feature availability, provider configuration, current-person authorization, logging, tool exposure, and the location of organization-specific policies.
- **Plugins and themes:** The supplied evidence establishes packaging and Rock Shop distribution guidance but does not document a particular package’s install or uninstall implementation.
- **Live verification boundary:** No new live-instance inspection occurred for this guide. Only the public-safe conclusions embedded in approved claims were used.

## Source Map

### Official documentation and training

- [Attributes](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes) — official v19 documentation index.
- [Extended Attributes Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab) — Person Profile attribute grouping, visibility, editing, and administration.
- [Display Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes) — Attribute Values block placement and category configuration.
- [Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses) — official campus documentation index.
- [Manage Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses) — v19 campus administration and single-campus behavior.
- [Add Attributes to Campuses](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses) — campus attribute procedure and security.
- [Mobile Attribute Values block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values) — category, entity-type, naming, and field-support boundaries.
- [Developer documentation: Attributes](https://community.rockrms.com/developer/303---blast-off/attributes) — attribute loading, display, editing, authorization, and saving in custom blocks.
- [Packaging Plugins and Themes](https://community.rockrms.com/developer/packaging-plugins-themes) — packaging, Rock Shop review, and uninstall considerations.
- [Rock Core release notes](https://www.rockrms.com/releasenotes) — version-specific fixes and release context.

### Official recordings supporting approved claims

- [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ) — experience modes, CAPTCHA, check-in, registration, communications, person merge, diagnostics, workflows, and Lava.
- [3 Underrated Features Churches Are Overlooking](https://www.youtube.com/watch?v=edanHiYSDIM) — Connections rollout, CAPTCHA, Check-In Manager, and materialized schedule dates.
- [AI Summit: The Community’s First Look at Rock’s AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8) — agent, skill, tool, security, prompt, Lava, result-shaping, and SQL boundaries.
- [RockIQ Rapid Fire Q&A from the AI Summit](https://www.youtube.com/watch?v=dpYJiOAiJYM) — Rock-side capability versus organization-specific external skills.
- [AI Voice Models & the Hidden Costs of Untrained Staff](https://www.youtube.com/watch?v=bu5nPeAVCAo) — durable artifacts, training videos, LMS assignments, staff activation, and shadow-tool risk.
- [The Vatican on AI and Grandmasters on Ministry](https://www.youtube.com/watch?v=pvgZLvcfmFQ) — patch governance and problem-first solution design.

### Reviewed community evidence

- [Rock metrics and dashboard history](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp)
- [Persisted journey analytics](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)
- [Embedded BI security](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)
- [Analytics snapshot layers](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz)
- [Rock-native and external BI decision patterns](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz)
- [Historical major-release context](https://shows.acast.com/rock-cast/episodes/episode-33-rock-73-and-new-rx2018-tracks)
- [Model Map](https://community.rockrms.com/ModelMap) and [Rock U workflows](https://community.rockrms.com/rocku/workflows) — supporting routes for community Defined Value and check-in configuration patterns; live verification remains required.

### Immutable implementation evidence

All source observations below refer to commit `471fd303d111b2e46218228dbc1e93dba8856fa3`.

- [Defined Value attribute-value query](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)
- [Defined Type attributes query](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)
- [DefinedTypeService](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/DefinedType/DefinedTypeService.cs)
- [DefinedValueService](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/DefinedValue/DefinedValueService.cs)
- [EntityTypeService](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/EntityType/EntityTypeService.cs)
- [Entity type security rule](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)
- [Defined Types v2 controller](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/DefinedTypesController.CodeGenerated.cs)
- [Defined Values v2 controller](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/DefinedValuesController.CodeGenerated.cs)
- [Entity Types v2 controller](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/EntityTypesController.CodeGenerated.cs)