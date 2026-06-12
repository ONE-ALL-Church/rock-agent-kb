---
id: authored-platform-configuration
title: Platform Configuration
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Platform Configuration

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Platform Configuration index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Platform configuration is the layer of Rock RMS where administrators and developers shape the system without changing the core database schema. It includes attributes, attribute values, defined types, defined values, categories, entity types, campuses, global attributes, system settings, and the repeating configuration patterns used across people, groups, workflows, CMS, reporting, security, operations, and integrations.

For agent work, the most important rule is this: do not treat configuration records as labels only. Many of them are active data-model participants. A defined value may be referenced by attendance, benevolence, groups, addresses, workflows, or custom attributes. An entity type may be referenced by attributes, audit records, security, AI agent anchors, provider components, and many other model records. Rock source snippets show deletion checks in generated services for `DefinedValue`, `DefinedType`, and `EntityType`, which means these records often cannot be safely removed just because they look unused in an admin screen ([DefinedValueService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs), [DefinedTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedTypeService.CodeGenerated.cs), [EntityTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/EntityTypeService.CodeGenerated.cs)).

The operational center of this guide is the attribute system. Rock’s developer documentation describes attributes as a major extensibility mechanism that can be added at runtime or implemented in code ([Developer 303 Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)). Attributes define extra fields for entities; attribute values store the entity-specific value. The core relationship is:

- `Attribute` defines what can be stored.
- `FieldType` defines how the value is edited, validated, formatted, and sometimes interpreted.
- `AttributeValue` stores the actual value for an entity instance.
- `EntityType` determines what kind of object the attribute applies to.
- `EntityTypeQualifierColumn` and `EntityTypeQualifierValue` narrow the attribute to a subset of that entity type when the entity type supports scoped configuration.
- `Category` organizes attributes, defined values, and other configurable objects.
- `DefinedType` and `DefinedValue` provide reusable controlled vocabularies.
- `Campus` is an organizational context used by people, groups, reports, connections, mobile context, and content targeting.
- Global attributes and system settings provide instance-wide configuration accessible to Lava and code.

Agents doing real Rock work should start from the live object and the configured entity type. If a user asks why a field is missing, why a picker shows the wrong values, why Lava returns an unexpected string, why a report is filtering by the wrong campus, or why a workflow attribute cannot be saved, inspect the `Attribute`, `FieldType`, `AttributeValue`, `EntityType`, qualifier columns, categories, security, and version-specific release notes before changing configuration. Rock v17 and later increased attribute security behavior, and Rock v17.5 added an optional Lava parameter to bypass attribute-level security checks where appropriate ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). Use that as a diagnostic clue, not as a default workaround.

## 2. Scope And Terminology

This guide covers platform configuration concepts that are reused across Rock RMS. It is not limited to one admin page. The scope includes:

- Entity types and the concept of entities.
- Core entity properties versus attributes.
- Entity attributes, global attributes, and attribute values.
- Field types and field attributes.
- Defined types and defined values.
- Categories and entity-specific category behavior.
- Campuses and campus context.
- System settings and global settings.
- Configuration patterns across People, Groups, Workflows, CMS, Security, Data Views, Reports, and Operations.
- Developer, API, Lava, Obsidian, mobile, and source-code landmarks.
- Operational checks and troubleshooting paths.

RockU’s Core Concepts section frames these ideas as foundational to how Rock organizes data, with separate training entries for entities, properties and attributes, custom attributes, defined types, campuses, categories for defined values, jobs, CSS icons, automations, and note types ([RockU Core Concepts](https://community.rockrms.com/rocku/core-concepts)). The training pages in the supplied source records are thin in extract form, so this guide uses them mainly as topic authority and relies more heavily on official developer docs, Lava docs, release notes, model-map records, and source-code snippets where those provide deeper operational detail.

Key terms:

**Entity**  
A Rock model object that represents a row or configured object in the system. Examples include `Person`, `Group`, `DefinedValue`, `Campus`, `Workflow`, `ConnectionRequest`, `ContentChannelItem`, and many others. RockU includes “What is an Entity” as a core concept topic ([What is an Entity](https://community.rockrms.com/rocku/core-concepts/what-is-an-entity)).

**Entity Type**  
A configuration record that identifies a model or component type. Rock source shows `EntityTypeService.Get(string entityName)` looking up entity types by name and `EntityTypeService.Get(Type type, bool createIfNotFound, PersonAlias personAlias)` creating one from a .NET type when requested ([EntityTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/EntityType/EntityTypeService.cs)). Entity types are used by attributes, security, audit, notes, components, REST endpoints, and UI blocks.

**Property**  
A built-in field on a model. For example, a person’s first name or a defined value’s value is part of the model itself. Properties are usually stored as table columns and are enforced by the model.

**Attribute**  
A configurable field definition attached to an entity type or to global configuration. Attributes let administrators and developers extend objects without adding custom database columns. Rock’s Lava docs call attributes a key extensibility feature ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

**Attribute Value**  
The stored value for a particular attribute on a particular entity instance. The Rock Model Map identifies “Attribute Value” as a Core model ([Model Map](https://community.rockrms.com/ModelMap)). Source snippets show `AttributeValue` joined to `Attribute`, `FieldType`, and target entities such as `DefinedValue` in SQL utility views ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).

**Field Type**  
The type of editor and value semantics used by an attribute or defined type. Developer docs distinguish field types from field attributes: a field type provides UI and value handling, while a field attribute configures a field type ([Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further)).

**Defined Type**  
A named collection of defined values. Defined types provide controlled vocabularies. Source code shows `DefinedValueService.GetByDefinedTypeId()` returning values for a defined type ordered by order and then value ([DefinedValueService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedValue/DefinedValueService.cs)).

**Defined Value**  
A selectable value within a defined type. Defined values can themselves have attributes. Source utility SQL demonstrates attributes attached to `Rock.Model.DefinedValue` and scoped by defined type ([View_DefinedTypeAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)).

**Category**  
A configuration organizer. Categories can apply to attributes, defined values, content, financial objects, notes, groups, and other entity types depending on configuration. Category selection must match the configured entity type; release notes document bugs where attribute category pickers showed unrelated categories in some versions ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

**Campus**  
An organizational location or campus context. Campuses are a RockU core concept ([Campuses](https://community.rockrms.com/rocku/core-concepts/campuses)) and are used in people records, groups, connections, reports, mobile context, filtering, and routing.

**Global Attribute**  
An instance-wide attribute value available to Lava and code. Lava docs include a Global Attributes section and note system settings support beginning with Rock v10.3 ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

**System Setting**  
A system-level configuration value. Some system settings are exposed through Lava and admin UI. Because naming and storage can vary by version, inspect the live admin page, `Attribute`, `AttributeValue`, and Rock settings tables before assuming exact storage.

## 3. Platform Configuration Mental Model

Rock platform configuration is best understood as a layered model.

At the bottom are core models and table columns. These are the durable, compiled entities in Rock source code: `Person`, `Group`, `DefinedType`, `DefinedValue`, `EntityType`, `Campus`, `Attribute`, `AttributeValue`, `Category`, and many more. These model properties are generally visible in source, REST endpoints, model map, or database schema. Agents should prefer these as the most authoritative layer when checking relationships.

Above the model layer are entity type records. An entity type record tells Rock, “this configurable thing refers to this model or component class.” Source code shows entity type lookup by full type name and creation from a .NET `Type` when enabled ([EntityTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/EntityType/EntityTypeService.cs)). Entity type records also have UI-facing metadata in Obsidian view models, including `id`, `name`, `friendlyName`, `isCommon`, `isSecured`, `indexDocumentUrl`, and a `linkUrlLavaTemplate` for generating detail links ([EntityTypesBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesBag.cs), [entityTypesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesBag.d.ts)).

Above entity types are attributes. An attribute is not merely a UI field. It is a field definition with a key, name, description, field type, optional default, order, security, categories, public flag, entity type, and optional qualifiers. The exact live columns should be verified in the `Attribute` table or Model Map for the installed Rock version. In practice, agents commonly inspect:

- `Attribute.Id`
- `Attribute.Guid`
- `Attribute.Key`
- `Attribute.Name`
- `Attribute.Description`
- `Attribute.EntityTypeId`
- `Attribute.EntityTypeQualifierColumn`
- `Attribute.EntityTypeQualifierValue`
- `Attribute.FieldTypeId`
- `Attribute.DefaultValue`
- `Attribute.Order`
- category associations
- security records
- whether the attribute is active/public/required, if those fields exist in the installed version

Attribute values are stored separately. This separation matters because a field can exist without values, values can exist without being visible in a particular block, and old values can remain after an attribute’s field type or qualifier changes. The Model Map identifies `Attribute Value` as a Core model ([Model Map](https://community.rockrms.com/ModelMap)). The supplied source SQL joins `AttributeValue` to `Attribute`, `FieldType`, `DefinedValue`, and `DefinedType`, showing the practical reporting shape: value row, attribute definition, field type metadata, and target entity ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).

Above attributes are consuming surfaces: admin screens, Lava, workflow forms, Obsidian blocks, mobile blocks, reports, APIs, and custom code. Each surface may apply its own filtering. For example, the mobile Attribute Values block displays and edits attribute values by category and entity type, but only supports field types that are supported in the mobile shell; the docs explicitly warn that category lists may show broad categories and that the implementer must ensure entity type and attribute compatibility ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)). This is a recurring operational pattern: the attribute exists globally in the configuration layer, but each block decides which attributes it can use.

The most reliable mental model for agents is:

1. Identify the target entity instance.
2. Identify its entity type.
3. Identify the attribute definition by key, GUID, or name.
4. Confirm the attribute’s entity type and qualifier match the target.
5. Confirm the field type and field configuration.
6. Confirm category, public flag, and block include/exclude settings.
7. Confirm security.
8. Confirm the value row and raw stored value.
9. Confirm the consuming surface’s version-specific behavior.

## 4. Source Authority And How To Use This Guide

Use source authority in this order when making operational decisions:

1. **Live Rock instance evidence**  
   For a real task, inspect the specific record, block, attribute, entity type, value, category, security rule, route, or workflow instance in the live Rock database or admin UI. This guide cannot know local customizations.

2. **Rock source code**  
   Source-code snippets from `SparkDevNetwork/Rock` are high authority for compiled behavior, generated service relationships, REST endpoints, deletion checks, and model/view-model properties. The repository is the registered source repository in the pack ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

3. **Official developer docs and Lava docs**  
   Developer docs provide implementation guidance for attributes, field types, Obsidian grids, mobile controls, API patterns, and agent tools ([Developer 303 Attributes](https://community.rockrms.com/developer/303---blast-off/attributes), [Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further), [Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

4. **Official release notes**  
   Release notes are critical for version caveats. Several platform-configuration behaviors changed or were fixed in v17.2, v18.2, v18.3, and v19.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

5. **RockU and official documentation books**  
   RockU gives conceptual authority; documentation books provide operational UI patterns, especially where configuration crosses into modules like Engagement or Connections ([RockU Core Concepts](https://community.rockrms.com/rocku/core-concepts), [Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).

6. **Model Map**  
   Model Map confirms model existence and category, but the supplied excerpt is compact. Use it as a navigation anchor and verify detailed fields in source or live schema ([Model Map](https://community.rockrms.com/ModelMap)).

7. **Community recipes and partner posts**  
   Recipes can demonstrate practical patterns, but the recipe page itself warns that community recipes are not reviewed or endorsed by the Rock core team. Use them as examples and validate performance, security, and version fit before applying ([Slicker Campus Filters](https://community.rockrms.com/recipes/393), [Event Specific Custom Check-In Success Messages](https://community.rockrms.com/recipes/385)).

When this guide says “inspect,” it means verify in the live instance before changing configuration. Rock instances differ by version, plugins, migrations, custom entity types, custom field types, security, and local conventions.

## 5. Core Configuration And Data Model

### Entity Types

Entity types are the backbone of platform configuration. They connect a row in configuration to a model or component type. Source code shows entity type lookup by name and by .NET type, and optional creation when a type is not already registered ([EntityTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/EntityType/EntityTypeService.cs)).

In administrative and API contexts, entity type records commonly expose:

- `Id`
- `Guid`
- `Name`, usually a fully qualified class name for models, such as `Rock.Model.DefinedValue`
- `FriendlyName`
- flags such as whether the type is an entity or common type
- security-related metadata
- optional index/documentation URL
- optional Lava link template for generating detail links

The Obsidian entity type list view model includes fields such as `friendlyName`, `id`, `indexDocumentUrl`, `isCommon`, `isSecured`, `linkUrlLavaTemplate`, and `name` ([entityTypesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesBag.d.ts)). The options bag includes an edit authorization flag, reinforcing that entity type editing is security-sensitive ([EntityTypesOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesOptionsBag.cs)).

Operational implications:

- Do not delete or rename entity types casually.
- If an attribute is missing, confirm its `EntityTypeId` points to the right entity type.
- If an entity type looks duplicated or stale, inspect by `Name`, `Guid`, and references before modifying.
- If an API, Lava command, block, or plugin uses entity type by GUID, changing labels may not affect behavior; changing records may.
- If a custom component is not available as an entity type, verify whether its assembly is loaded and whether entity type registration has run.

### Attributes

An attribute definition describes a field that can be attached to an entity type, sometimes narrowed by qualifiers. Rock’s developer docs show that custom blocks can load an entity’s attributes, add display/edit controls through `AttributeValuesContainer`, and save values through attribute APIs ([Developer 303 Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)).

Attributes usually matter in three places:

- **Definition**: field key, name, entity type, field type, categories, default, security, qualifier, configuration.
- **Value**: actual stored value for one entity instance.
- **Consumption**: UI block, Lava template, workflow, report, API, mobile app, or custom code that renders or uses the value.

An attribute’s `Key` is operationally important. Lava filters access attributes by key, not just display name. Community examples also rely on exact keys when reading group or group type attributes in templates ([Event Specific Custom Check-In Success Messages](https://community.rockrms.com/recipes/385)). If the key changes, Lava and code references can break even if the display name still looks correct.

### Attribute Values

Attribute values store the actual data. The supplied SQL source shows the common relationship:

- `AttributeValue.AttributeId` joins to `Attribute.Id`
- `Attribute.FieldTypeId` joins to `FieldType.Id`
- `Attribute.EntityTypeId` joins to `EntityType.Id`
- `AttributeValue.EntityId` points to the target entity row
- `AttributeValue.Value` stores the raw value
- `AttributeValue.Guid` provides stable identity

That source file specifically lists defined value attributes by joining `AttributeValue` to `DefinedValue` and `DefinedType` where the attribute entity type is `Rock.Model.DefinedValue` ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).

Operational implications:

- A missing value row does not always mean the attribute is misconfigured; the entity may be using the default value.
- A value row can exist even if the consuming block does not show the attribute because of category, public flag, qualifier, security, or field-type support.
- Raw stored values may be GUIDs, IDs, booleans, delimited lists, XML/JSON-like strings, Lava content, or plain text depending on field type.
- For field types that point to entities, prefer raw value plus resolved object inspection.
- When bulk editing or SQL auditing, always interpret value format by field type.

### Field Types

Field types determine editing controls and stored-value conventions. Developer docs explain that a field type provides the UI to edit a value and can be used in custom blocks and custom attributes; a field attribute configures a field type ([Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further)).

The workflow Lava docs include a field-type storage overview and emphasize understanding internal storage. For example, the docs explain that a workflow attribute of type Person may store a person alias GUID when accessed as raw value, and that field types vary in whether they can be used to query object properties and attributes ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).

Operational implications:

- Do not assume displayed value equals stored value.
- For Lava links or API payloads, use raw values when the target page or API expects an identifier.
- For UI display, use formatted values or object properties as appropriate.
- In mobile, verify field type support before expecting an attribute editor to render. The mobile Attribute Values block and Attribute Value Editor both warn that only supported field types are editable in the mobile shell ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values), [Mobile Attribute Value Editor](https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor)).

### Defined Types And Defined Values

Defined types provide lists of values. Defined values belong to a defined type. Source code shows retrieval by defined type ID or GUID, ordered by `Order` and then value ([DefinedValueService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedValue/DefinedValueService.cs)).

Defined values can have attributes. The SQL utility file for defined type attributes shows attributes for `Rock.Model.DefinedValue` scoped by `EntityTypeQualifierColumn = 'DefinedTypeId'` and `EntityTypeQualifierValue = t.Id`, which means a defined value attribute can be configured to apply only to values within a particular defined type ([View_DefinedTypeAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)).

Operational implications:

- A defined value can be both a selectable option and a mini-configured object with its own attributes.
- When a defined value appears in Lava as an object, its properties and attributes may be accessible if the field type supports object resolution.
- Do not delete defined values without checking references. Generated source shows many model references can block deletion ([DefinedValueService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs)).
- If a defined value picker is hard to use for long lists, check version. v19.1 release notes include a fix for single-select defined value attributes configured as enhanced long lists in Obsidian blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Categories

Categories organize configuration records and often control which attributes appear in blocks. The Engagement documentation shows a concrete pattern: connection request attributes can be assigned to categories, and signup blocks can include or exclude specific categories; uncategorized attributes may appear under a default “Attributes” tab when other categories exist ([Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).

Categories are entity-type-sensitive. Release notes record bugs where category dropdowns showed unrelated categories:

- v17.2 fixed unrelated categories appearing when editing Content Channel Item attributes from the Content Channel Type Detail block ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v19.1 fixed multiple attribute editing blocks where category dropdowns included Global Attribute categories instead of categories for the actual attribute entity type ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Operational implications:

- If categories look wrong in an attribute editor, check Rock version before assuming local configuration corruption.
- If an attribute is not shown in a block, inspect included and excluded categories.
- If category filtering is used for public forms, confirm that sensitive attributes are not included by category accident.
- If mobile blocks display attributes by category, verify category and entity type compatibility manually ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)).

### Campuses

Campuses serve as organizational context. They are not just location labels. Campus can affect person home context, group membership, connection request routing, report filters, mobile context, and content targeting.

The mobile Campus Context Picker lets a mobile app present campus choices allowed for a person and sends the selected campus with every request. If no context is set, the docs say the current person’s home campus is used ([Campus Context Picker](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/campus-context-picker)).

Operational implications:

- Campus filters should distinguish “all campuses,” “current person’s campus,” “selected context campus,” and “home campus.”
- Multi-campus reports should explicitly define what happens when no campus parameter is supplied.
- Mobile and web context may differ if campus context picker state is active.
- Community recipes can illustrate campus filtering patterns but require local validation. The Slicker Campus Filters recipe demonstrates adding an “All Campuses” option and defaulting to current person campus in dynamic report patterns, but it is community-contributed and must be reviewed for security and performance ([Slicker Campus Filters](https://community.rockrms.com/recipes/393)).

### Global Attributes And System Settings

Global attributes and system settings provide instance-wide values. Lava docs include sections for Global Attributes and System Settings and note system settings support beginning with Rock v10.3 ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

Global configuration has high blast radius. A value may be used by:

- Lava templates.
- CMS content.
- Workflow actions.
- Scheduled jobs.
- Communication templates.
- Mobile app configuration.
- Blocks.
- External integrations.
- Custom plugins.

Operational implications:

- Before changing a global attribute, search for its key in Lava, content channels, workflow actions, block settings, and code.
- Confirm whether the value is cached and whether a cache flush or app restart is required.
- Verify whether the setting is environment-specific. Production, staging, and development may need different URLs, API keys, campus IDs, or feature flags.
- For address behavior, release/partner notes mention a v16.10-era system setting around default address state selection, but the supplied Triumph source is a secondary partner summary and should be verified against official release notes and the live System Settings page before relying on exact wording ([Triumph GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-12202024)).

## 6. Primary Entities And Relationships

This section gives agents a practical relationship map. Use it as a starting point, then verify in the installed version.

### Attribute Relationship Map

`Attribute` relates to:

- `EntityType` through `EntityTypeId`.
- `FieldType` through `FieldTypeId`.
- `Category` through attribute-category assignment records.
- target entity scope through `EntityTypeQualifierColumn` and `EntityTypeQualifierValue`.
- `AttributeValue` through `AttributeValue.AttributeId`.
- security records through Rock authorization relationships.
- field configuration records or serialized configuration, depending on field type and version.

`AttributeValue` relates to:

- `Attribute` through `AttributeId`.
- a target entity through `EntityId`.
- formatted display through the attribute’s field type.
- raw value through `Value`.
- stable identity through `Guid`.

The official SQL utility for defined values demonstrates this shape in a reporting context ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).

### Defined Type Relationship Map

`DefinedType` relates to:

- many `DefinedValue` records.
- a possible `FieldTypeId`, based on source code that can retrieve defined types by field type ID ([DefinedTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedType/DefinedTypeService.cs)).
- attributes on the defined type itself through queryable attribute support in generated source ([DefinedTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedTypeService.CodeGenerated.cs)).
- other model records that reference the defined type. Generated deletion checks show, for example, `GroupType.GroupStatusDefinedTypeId` can block deletion ([DefinedTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedTypeService.CodeGenerated.cs)).

`DefinedValue` relates to:

- one `DefinedType` through `DefinedTypeId`.
- attributes scoped to `Rock.Model.DefinedValue`, often qualified by `DefinedTypeId`.
- many consuming models through specific foreign keys. Generated deletion checks list many examples such as attendance and benevolence references ([DefinedValueService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs)).
- Lava object resolution when used by field types that support object output ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### Entity Type Relationship Map

`EntityType` relates to:

- attributes through `Attribute.EntityTypeId`.
- audit records through `Audit.EntityTypeId`.
- authorization/security records.
- notes and note types.
- components, providers, workflows, commands, and plugin records.
- REST v2 model endpoints.
- UI blocks and view models.
- security grants.

Source code shows an `EntityTypeSecurityGrantRule` that grants access when an object’s entity type matches the configured entity type ID, including both `IEntity` and cached entity cases ([EntityTypeSecurityGrantRule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)). This means entity types participate directly in security decisions.

### Category Relationship Map

`Category` can relate to many entity types. The exact category model fields and join tables should be verified in the live schema, but operationally categories often:

- organize attributes on admin screens.
- determine tab grouping.
- drive include/exclude block settings.
- categorize defined values.
- categorize content, financial objects, notes, groups, or workflows.
- affect user-visible forms.

The Engagement docs provide a concrete example: connection request attribute categories are created under Attribute Categories with entity type “Connection Request,” assigned to attributes, and then used by signup block settings ([Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Campus Relationship Map

`Campus` can relate to:

- people and families through home campus or family context.
- groups through campus assignment.
- connection opportunities and requests.
- schedules and locations in some module contexts.
- reports and page parameters.
- mobile request context.
- content targeting and Lava templates.
- global settings and default organization context.

Do not assume one campus field controls all campus behavior. Inspect the consuming entity and block.

## 7. Common Platform Configuration Workflows

### Add A Person Attribute

Use this workflow when a ministry wants a new person-level field.

1. Define the purpose. Decide whether the field is operational, pastoral, reporting, public, sensitive, temporary, or integration-owned.
2. Confirm the target entity type is `Person`, not `PersonAlias`, `Group`, `GroupMember`, or `Family` unless that is the real data owner.
3. Navigate to the Entity Attributes admin surface in the live Rock instance.
4. Create the attribute with a stable key. Avoid spaces and future-breaking names. Prefer keys that describe meaning, not one campaign.
5. Choose the correct field type. Use controlled field types for controlled values rather than free text.
6. Assign a category if the attribute should appear with related fields.
7. Set security. If the value is sensitive, configure attribute-level authorization and verify behavior under a non-admin test account.
8. Set public visibility only if it is intended for public forms or external display.
9. Save and test on a person profile or block that displays person attributes.
10. Test Lava access using debug mode and the `Attribute` filter ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).
11. If using the attribute in Data Views or Reports, verify query behavior and whether the field type supports the needed filtering.

RockU has training entries for Person Attributes, Family Attributes, and Bookmarked Attributes in the Individuals in Rock section ([Person Attributes](https://community.rockrms.com/rocku/individuals-in-rock/person-attributes), [Family Attributes](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes), [Bookmarked Attributes](https://community.rockrms.com/rocku/individuals-in-rock/bookmarked-attributes)). The hydrated excerpts are mostly navigation metadata, so use live UI and official docs for exact steps.

### Add A Connection Request Attribute

Connection request attributes are a good example of entity attributes crossing into public forms. The Engagement documentation says to set up these attributes under Entity Attributes with entity type “Connection Request,” and it describes using categories and public flags to control signup block display ([Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).

Operational workflow:

1. Confirm whether the attribute belongs to the request, the person, the connection type, or the opportunity.
2. Create the attribute for entity type `Connection Request`.
3. If the signup block should show only selected attributes, create an Attribute Category for entity type `Connection Request`.
4. Assign the new attribute to that category.
5. Configure the signup block to include or exclude the right categories.
6. If using public forms, set the public flag appropriately and confirm the signup block’s public/non-public behavior.
7. Submit a test request as an unauthenticated or low-privilege user.
8. Inspect the created `ConnectionRequest` and `AttributeValue`.
9. Confirm staff-facing detail blocks show the value.
10. Confirm workflows triggered from the request can read the raw or formatted value as needed.

### Add Attributes To Defined Values

Defined value attributes are useful when a controlled vocabulary item needs metadata. Examples include a school defined value with grade-range attributes, a ministry area value with display color, or a campus-related value with integration IDs.

The source SQL for defined type attributes shows a canonical pattern: attributes for entity type `Rock.Model.DefinedValue` scoped by `EntityTypeQualifierColumn = 'DefinedTypeId'` and qualifier value equal to a defined type’s ID ([View_DefinedTypeAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)).

Workflow:

1. Identify the defined type.
2. Create an attribute for entity type `Defined Value`.
3. Qualify it to the specific defined type if the UI supports qualifier configuration.
4. Choose field type and category.
5. Edit each defined value and enter its attribute values.
6. In Lava, resolve the defined value object and then read its attributes. The attribute docs show the pattern of returning an object from an attribute and then accessing its properties or attributes ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).
7. In reports, join `DefinedValue`, `DefinedType`, `Attribute`, and `AttributeValue` as needed, using the official SQL utility as a relationship example ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).

### Configure A Campus-Aware Report

Campus-aware reports are common and easy to get subtly wrong. A community recipe demonstrates one pattern: a Page Parameter Filter using a single-select campus field, an “All Campuses” option, and Dynamic Data Lava/SQL logic to default to the current person’s campus ([Slicker Campus Filters](https://community.rockrms.com/recipes/393)). Because this is a community recipe, treat it as a pattern, not an official guarantee.

Workflow:

1. Decide the campus source: selected page parameter, current person home campus, mobile campus context, group campus, opportunity campus, or all campuses.
2. Decide whether “All Campuses” is allowed.
3. If using Dynamic Data SQL, parameterize safely and avoid injecting raw Lava strings into SQL.
4. If using a page parameter, define what happens when it is absent.
5. If using current person campus, test with a person who has no campus.
6. If using mobile campus context, verify the Campus Context Picker behavior and fallback to home campus ([Campus Context Picker](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/campus-context-picker)).
7. Test with users who can see one campus, multiple campuses, and no campus.
8. Confirm security does not expose cross-campus data unintentionally.

### Add Mobile Site Attributes

Rock mobile docs say custom entity attributes for mobile sites are available as of Rock v16.8 and can be configured under System Settings > Entity Attributes for mobile site use ([Custom Site Attributes](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes)).

Workflow:

1. Confirm Rock version is v16.8 or later.
2. Identify the mobile site or application entity.
3. Create custom attributes for the relevant site entity type.
4. Assign values on the Mobile Application Detail block or equivalent live UI.
5. Access the attributes in mobile Lava/XAML content using the site object and attribute keys.
6. Test in the mobile shell.
7. Confirm field types are supported by the mobile surface if the value is editable, not just read.

### Use Attributes In Custom Blocks

Developer docs show the WebForms `AttributeValuesContainer` pattern for adding display and edit controls to custom blocks, including loading attributes on view/edit and saving attribute values ([Developer 303 Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)). For Obsidian, the `AttributeColumns` component provides a placeholder for dynamic attribute-value columns in grids ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns)).

Workflow:

1. Confirm the block’s entity type.
2. Load attributes for the entity before display.
3. Render display controls or edit controls according to authorization.
4. Validate required fields and field-type-specific constraints.
5. Save attribute values using Rock’s attribute APIs.
6. For list grids, request attribute field definitions and place `AttributeColumns` where dynamic columns should appear.
7. Test with attributes of multiple field types.
8. Test security with users who can view the entity but not all attributes.

## 8. Attributes And Attribute Values Deep Dive

### Attribute Definition Fields

The exact columns vary by Rock version, but agents should normally inspect:

- `Id`: local numeric identifier.
- `Guid`: stable identifier.
- `Name`: display label.
- `Key`: programmatic key used in Lava and code.
- `Description`: admin/help text.
- `EntityTypeId`: target entity type.
- `EntityTypeQualifierColumn`: optional qualifier column.
- `EntityTypeQualifierValue`: optional qualifier value.
- `FieldTypeId`: field type used for editing and formatting.
- `DefaultValue`: default raw value.
- `Order`: display order.
- `IsRequired`, `IsGridColumn`, `IsMultiValue`, `IsPublic`, or similar flags where present.
- field configuration values.
- categories.
- security.

Do not invent exact field names for a live system. Inspect the model, schema, or admin UI.

### Qualifiers

Qualifiers narrow an attribute to a subset of an entity type. Defined value attributes are a clear example: attributes can apply to `Rock.Model.DefinedValue`, but only to values belonging to a specific defined type. The source SQL checks `EntityTypeQualifierColumn = 'DefinedTypeId'` and `EntityTypeQualifierValue = t.Id` ([View_DefinedTypeAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)).

Other common qualifier patterns may include group type, workflow type, block type, content channel type, registration template, or connection type. Verify the expected qualifier column for the target entity.

Troubleshooting qualifier issues:

- Attribute exists but does not appear: qualifier column/value may not match.
- Attribute appears on too many objects: qualifier may be blank or too broad.
- Attribute values exist but block ignores them: block may load only attributes matching a specific qualifier.
- New attribute value cannot be found in SQL: `EntityId` may point to a different entity than expected.

### Raw Values Versus Formatted Values

The Lava workflow docs emphasize raw values. A Person workflow attribute’s raw value may be a person alias GUID, not a person ID or display name ([Workflows and Lava](https://community.rockrms.com/lava/workflows)). The attribute filter docs show accessing attributes directly, accessing object properties through qualifiers, and returning an object for further property/attribute access ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

Practical rules:

- Use formatted value for display.
- Use raw value for identifiers, links, API calls, comparisons, and SQL joins.
- Use object output when you need properties or nested attributes.
- For multi-select fields, inspect delimiter and stored format.
- For defined values, inspect whether stored value is ID, GUID, or another field-type-specific token.
- For person fields, inspect whether value is person alias GUID, person GUID, or ID.

### Attribute Security

Rock v17 increased security enforcement on attributes, requiring them to honor security rules of their associated entity. The Lava docs note a third optional parameter added in Rock v17.5 to bypass attribute-level security checks ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

Operational approach:

1. Reproduce as the affected user, not as an admin.
2. Confirm the user can view the base entity.
3. Confirm the user can view the attribute definition.
4. Confirm the user can view attribute value.
5. Confirm whether the consuming Lava/block/API applies attribute security.
6. Check version-specific behavior.
7. Use bypass only when the template or code is in a trusted context and the data is appropriate to expose.

Never treat a Lava security bypass as a generic fix. It may expose sensitive data.

### Attribute Categories

Attribute categories can control display grouping and inclusion. The Engagement docs show connection request attributes grouped into category tabs, with uncategorized attributes falling under a generic tab when categorized attributes exist ([Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).

Category pitfalls:

- Wrong entity type category selected.
- Category shown due to a version bug.
- Attribute category exists but block configured to exclude it.
- Attribute uncategorized and therefore displayed under a default group.
- Mobile block category selection not compatible with selected entity type.

Version caveat: v19.1 fixed attribute editing blocks showing Global Attribute categories in the wrong category dropdown ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Attribute Values In Lava

Use Lava debug mode where available to inspect available merge fields and attributes. The attribute docs describe using debug to see available attributes ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

Common patterns:

```liquid
{{ CurrentPerson | Attribute:'BaptismDate' }}
```

Use this for a formatted string value.

```liquid
{{ Workflow | Attribute:'Person','RawValue' }}
```

Use this when the internal identifier is needed, such as building a link or passing a value to another page. The workflow docs explain why raw value matters for person-type workflow attributes ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).

```liquid
{% assign school = CurrentPerson | Attribute:'School','Object' %}
{{ school.Value }}
{{ school | Attribute:'Grades' }}
```

Use object output when the attribute points to an object that has its own properties or attributes. The attribute docs provide this “attribute of an attribute” pattern for defined values ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### Attribute Values In Mobile

The mobile Attribute Values block displays and edits attributes based on category and entity type. Its settings include:

- Category.
- Use Abbreviated Names.
- Entity Type.
- Styling.

The docs warn that the category list may include broad categories and that the selected entity type and attribute must be compatible. They also warn that only field types supported by the mobile shell can be edited ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)).

The mobile Attribute Value Editor is a developer-level control that decides which UI to show for a given attribute value; normal use is looping through an entity’s attributes and building one editor per attribute. The docs again warn that only a subset of field types is supported ([Mobile Attribute Value Editor](https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor)).

## 9. Defined Types And Values Deep Dive

Defined types are the structured lists that keep Rock configuration consistent. They are more than dropdown options. A defined type can control group statuses, attendance values, communication preferences, location types, categories, icons, workflow options, and custom ministry vocabularies.

### Defined Type Fields To Inspect

In a live instance, inspect:

- `Id`
- `Guid`
- `Name`
- `Description`
- `Category`
- `Order`
- `FieldTypeId`, if present
- system/protected flags, if present
- values
- attributes
- security
- references from other model records

Source code confirms `DefinedTypeService.GetByFieldTypeId()` exists and orders by `Order`, so field type association can be part of defined type behavior ([DefinedTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedType/DefinedTypeService.cs)).

### Defined Value Fields To Inspect

In a live instance, inspect:

- `Id`
- `Guid`
- `DefinedTypeId`
- `Value`
- `Description`
- `Order`
- active/enabled/system flags, if present
- attributes
- category assignments, if supported
- references in model tables

Source code confirms defined values are retrieved by defined type and ordered by `Order`, then by value ([DefinedValueService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedValue/DefinedValueService.cs)).

### Deletion And Reference Safety

Generated service code checks whether a defined value is assigned to many other model records before deletion. The supplied snippet includes attendance and benevolence examples, and the full generated file likely contains many more references ([DefinedValueService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs)).

Before deleting or merging defined values:

1. Search direct foreign keys in the schema.
2. Search attributes that store defined value IDs or GUIDs.
3. Search Lava templates and workflows by defined value GUID and value text.
4. Check whether the value is system-defined.
5. Confirm whether historical records should retain the old value.
6. Prefer disabling or renaming only after confirming downstream behavior.
7. If replacing, migrate references explicitly and preserve auditability.

### Defined Value Attributes

Defined value attributes let each option carry metadata. For example:

- Display color.
- Icon class.
- Sort group.
- External system code.
- Ministry owner.
- Campus mapping.
- Eligibility rules.
- Lava template content.

The official attribute Lava docs demonstrate that a defined value returned as an object can expose its own properties and attributes ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). The source SQL utility shows how to list defined value attribute values by joining `DefinedType`, `DefinedValue`, `Attribute`, `FieldType`, and `AttributeValue` ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).

### Categorizing Defined Values

RockU includes a “Categorize Defined Values” core concept topic ([Categorize Defined Values](https://community.rockrms.com/rocku/core-concepts/categorize-defined-values)). The supplied excerpt is not detailed enough to assert exact UI behavior across versions. In a live instance, inspect whether the defined type supports categories, whether values are assigned to categories, and whether the consuming picker or block honors those categories.

Use categorization when:

- A long list needs grouping.
- A workflow or report should include only part of a defined type.
- Values need administrative organization.
- UI pickers should narrow by category.

Avoid categorization when:

- The consuming field type ignores categories.
- Categories would create hidden filtering rules that future admins will miss.
- The list is short and category maintenance creates more complexity than value.

## 10. Categories And Entity Types Deep Dive

### Entity Type As A Configuration Boundary

Entity type is the first boundary for categories and attributes. A category for `Connection Request` attributes is not the same as a category for global attributes, content channel item attributes, defined values, or group attributes. Release notes show that incorrect category lists in attribute editors have been real bugs, not just user confusion ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

When creating or troubleshooting categories:

1. Identify the target entity type.
2. Confirm the category is assigned to that entity type.
3. Confirm the attribute or item is assigned to that category.
4. Confirm the block consumes categories for that entity type.
5. Confirm version-specific bugs do not affect the picker.

### Entity Type Security

Entity types can participate in security. The source `EntityTypeSecurityGrantRule` grants permission when the object’s entity type ID matches the configured entity type ID for the requested action ([EntityTypeSecurityGrantRule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)).

Implications:

- Security grants can be broad if applied by entity type.
- A user may be allowed to view all entities of a type in a certain context.
- Cached entities and normal entities can both be evaluated.
- If a security rule is behaving broadly, inspect whether it is entity-type-based rather than entity-instance-based.

### Entity Type List And Editing

Obsidian view models expose entity type metadata and an edit authorization option ([entityTypesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesBag.d.ts), [entityTypesOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesOptionsBag.d.ts)). For agents, this means the UI may show entity type records but editing should be treated as administrative.

Before editing entity type records:

- Confirm why editing is needed.
- Check whether the record is system-created.
- Check references from attributes, audit, security, notes, components, and APIs.
- Check whether name/friendly name changes affect block settings or user-facing selectors.
- Avoid changing GUIDs.

### Category Version Caveats

Two release-note items are especially relevant:

- Rock v17.2 fixed Content Channel Type Detail behavior where content channel item attribute category lists included incorrect or unrelated categories ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Rock v19.1 fixed multiple attribute editing blocks where category dropdowns included Global Attribute categories instead of categories for the actual entity type ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Troubleshooting branch:

- If the wrong categories appear only in a specific block, check release notes and block type.
- If wrong categories appear everywhere, inspect category entity type assignments.
- If categories are correct but attributes do not display, inspect block include/exclude settings.
- If categories are correct but mobile shows unexpected attributes, inspect mobile field type support and entity type/category compatibility.

## 11. Campuses And Global Settings Deep Dive

### Campus As Context

Campuses are a core concept in RockU ([Campuses](https://community.rockrms.com/rocku/core-concepts/campuses)). In operations, campus is context, ownership, routing, filtering, and sometimes security-adjacent data.

Common campus-bearing records include:

- Person or family home campus.
- Groups.
- Group members through group context.
- Connection opportunities and requests.
- Registrations.
- Attendance and check-in configuration paths.
- Reports and page parameters.
- Content and mobile app context.

Always determine the domain-specific campus field. Do not assume the person’s home campus is the same as the group campus, event campus, connection request campus, or selected campus context.

### Campus Context In Mobile

The mobile Campus Context Picker displays campus choices allowed for a person and sends the selected campus with every request. If no context value is set, the current person’s home campus is used ([Campus Context Picker](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/campus-context-picker)).

Mobile check-in is a high-risk example of campus configuration crossing device, location, and public-flow behavior. A reviewed RockU Mobile Check-in Configuration transcript insight says to treat each mobile check-in device record like a virtual kiosk, configure the campus geofence, associate the relevant campus locations, and use separate devices when campuses need distinct boundaries ([Mobile Check-in Configuration, 00:44](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)).

Agent checks:

- Is the user authenticated?
- Which campuses are allowed for the person?
- Is a campus context already selected?
- Is the block reading selected context or home campus?
- What happens for users with no home campus?
- Does the page behave differently after changing campus context?

### Campus Filters In Reports

The Slicker Campus Filters recipe demonstrates a practical report pattern with Page Parameter Filter and Dynamic Data blocks, including an “All Campuses” option and current-person default ([Slicker Campus Filters](https://community.rockrms.com/recipes/393)). Because recipes are community-contributed and not core-reviewed, use the pattern cautiously.

Good campus filter design:

- Always define null behavior.
- Always define “all” behavior.
- Use IDs consistently.
- Avoid text matching campus names.
- Respect user authorization.
- Do not concatenate unsanitized page parameters into SQL.
- Test with inactive campuses if the report should exclude them.
- Test physical versus online campuses if campus type matters.

### Global Attributes

Global attributes are useful for:

- organization identity.
- URLs.
- communication defaults.
- API endpoints.
- feature flags.
- theme values.
- campus-independent settings.
- integration configuration.
- default content.

Lava docs include global attributes as part of the attribute filter documentation ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). In a live instance, inspect the exact key and storage.

Operational guardrails:

- Use stable keys.
- Document ownership and intended consumers.
- Do not store secrets in globally visible attributes unless Rock’s security model and consumers are appropriate.
- Search references before renaming.
- Check cache behavior after changing.
- Keep environment-specific values out of portable migration scripts unless intentionally parameterized.

### System Settings

System settings are instance-level configuration. Lava docs note system settings support from Rock v10.3 onward ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). The exact setting list is version-dependent.

Agent workflow for system setting questions:

1. Identify the setting by UI label, key, or behavior.
2. Confirm Rock version.
3. Inspect System Settings UI.
4. Inspect source/release notes if behavior changed by version.
5. Search Lava/workflows/blocks if setting is referenced.
6. Change in staging first when possible.
7. Validate all consuming areas after change.

## 12. Related Rock Areas: People, Groups, Workflows, Cms, Security, Data Views, Reports, Operations

### People

People are heavily extended by attributes. RockU includes Person Attributes, Family Attributes, and Bookmarked Attributes topics ([Person Attributes](https://community.rockrms.com/rocku/individuals-in-rock/person-attributes), [Family Attributes](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes), [Bookmarked Attributes](https://community.rockrms.com/rocku/individuals-in-rock/bookmarked-attributes)).

Agent considerations:

- Decide whether data belongs to `Person`, family group, `GroupMember`, known relationship, note, tag, or assessment.
- Avoid storing operational state in person attributes when a workflow, connection request, or group member attribute is more appropriate.
- Treat sensitive person attributes as security-sensitive.
- For profile display, confirm bookmarked/profile attribute settings and security.
- For reporting, confirm attribute values are loaded and queryable.

### Groups

Groups and group types often use attributes for configuration. The check-in success message recipe uses group type and group attributes to choose Lava templates for check-in output ([Event Specific Custom Check-In Success Messages](https://community.rockrms.com/recipes/385)). That pattern demonstrates how attributes can make group behavior configurable per group or group type.

Agent considerations:

- Group type attributes configure a category of groups.
- Group attributes configure one group.
- Group member attributes configure a person’s role or state within a group.
- Check-in, event, and connection workflows may read attributes at different levels.
- Attribute keys used in Lava must match exactly.
- Community Lava that runs stored templates should be reviewed for trust boundary and security.

### Workflows

Workflow attributes are central to workflow state and forms. The workflow Lava docs emphasize raw values and field-type storage formats ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).

Agent considerations:

- Workflow attributes may store identifiers differently than display values.
- Forms may show only selected attributes.
- Workflow action logic may depend on attribute keys.
- Person attributes and workflow attributes are different scopes.
- Attribute of type Attribute had a save bug fixed in v18.2, affecting scenarios such as Page Parameter Filter block filters ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### CMS

CMS configuration uses attributes in content channel types, content channel items, sites, blocks, and Lava. A release note for v17.2 specifically mentions category selection issues when editing Content Channel Item attributes from Content Channel Type Detail ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent considerations:

- Content channel item attributes may be scoped by content channel type.
- Category picker bugs can affect setup in certain versions.
- Lava templates may read attributes by key.
- Interaction tracking and content item entity type behavior can be version-sensitive; release notes mention content channel item interaction entity type fixes nearby in the supplied excerpt ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Mobile site attributes became configurable as custom entity attributes in v16.8 ([Custom Site Attributes](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes)).

### Security

Security intersects with platform configuration in several ways:

- Entity type security grants.
- Attribute-level security.
- Public flags for attributes.
- Block authorization.
- API endpoint authorization.
- Category-driven exposure.
- Lava security bypass behavior in trusted contexts.

Source code shows entity type security grants by entity type ID ([EntityTypeSecurityGrantRule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)). Lava docs note stronger attribute security in v17 and a bypass parameter in v17.5 ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). REST v2 generated controllers require authentication and use secured actions such as `EXECUTE_READ`, `EXECUTE_UNRESTRICTED_READ`, `EXECUTE_WRITE`, and `EXECUTE_UNRESTRICTED_WRITE` ([DefinedTypesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DefinedTypesController.CodeGenerated.cs), [DefinedValuesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DefinedValuesController.CodeGenerated.cs), [EntityTypesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/EntityTypesController.CodeGenerated.cs)).

### Data Views

Data Views often filter on properties, attributes, defined values, and campuses. Attribute filters can be slower or more complex than property filters. For high-volume queries:

- Prefer native properties when the data is core and frequently queried.
- Use attributes when extensibility is the correct tradeoff.
- Verify whether the attribute is queryable.
- Check field type storage before filtering.
- Inspect generated SQL or performance plans for large reports.
- Avoid broad attribute joins without selective predicates.

### Reports

Reports combine properties, attributes, defined values, categories, and campuses. Good report design:

- Resolve defined values by ID or GUID, not display text, when possible.
- Display friendly values but filter on stable identifiers.
- Include campus behavior explicitly.
- Document whether inactive values/campuses are included.
- Use categories only if the report logic expects them.
- Avoid assuming attribute defaults produce value rows.

### Operations

Operational platform configuration includes jobs, automations, system settings, global attributes, integrations, and release upgrades. RockU includes Jobs and Automations as core concept topics ([Jobs](https://community.rockrms.com/rocku/core-concepts/jobs), [Automations](https://community.rockrms.com/rocku/core-concepts/automations)).

Agent considerations:

- Jobs may read global attributes and system settings.
- Automations may depend on entity attributes.
- Upgrades may change block behavior around attributes or categories.
- Caches may delay visible changes.
- Generated services can block deletion even when UI references are not obvious.
- Release notes should be checked before diagnosing category or attribute editor issues.

## 13. Administration And Operational Guardrails

### Naming

Use stable names and keys:

- Attribute display names can be friendly.
- Attribute keys should be stable and code-safe.
- Defined type names should be clear and unique.
- Defined value labels should be user-facing but not overloaded.
- Categories should include the domain if ambiguity is likely.
- Global attribute keys should avoid generic names such as `Url`, `Token`, or `Enabled`.

Avoid renaming keys used by Lava, workflows, API integrations, reports, or plugins unless you have a migration plan.

### Change Management

Before changing platform configuration:

1. Identify current consumers.
2. Record current values.
3. Confirm target Rock version.
4. Test in staging when possible.
5. Use a low-risk pilot object.
6. Verify with a non-admin account.
7. Check logs or exceptions.
8. Document the change.

For high-blast-radius changes such as global attributes, system settings, defined values used by many modules, or entity type edits, treat the change as production-impacting.

### Public Exposure

Attributes may appear publicly through forms, CMS, mobile, Lava, APIs, reports, or profile pages.

Before marking an attribute public or placing it in a public category:

- Confirm the data is safe to expose.
- Test unauthenticated access.
- Test authenticated non-staff access.
- Inspect block settings for public/non-public filtering.
- Confirm Lava templates do not bypass security accidentally.
- Verify mobile behavior separately.

The Engagement docs describe using public flags and included/excluded categories for connection signup attributes ([Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).

### Deletion

Deleting configuration records is risky.

For attributes:

- Check whether values exist.
- Check Lava and code references by key and GUID.
- Check workflow action references.
- Check block settings.
- Check reports and data views.
- Consider disabling/hiding instead of deleting.

For defined values:

- Check generated service references.
- Check attributes storing the value.
- Check historical records.
- Check reporting dependencies.
- Consider inactive status rather than deletion if the value has history.

For entity types:

- Avoid deletion unless you know exactly why it exists.
- Generated source shows many possible references, including attributes and audit records ([EntityTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/EntityTypeService.CodeGenerated.cs)).

### Version Awareness

Always record:

- Rock version.
- Block type and whether it is WebForms or Obsidian.
- Mobile shell version when relevant.
- Plugin versions.
- Whether issue happens in admin, public site, mobile, API, or Lava.

Several known fixes affect platform configuration:

- v16.8 custom mobile site attributes ([Custom Site Attributes](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes)).
- v17 attribute security enforcement and v17.5 Lava bypass parameter ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).
- v17.2 content channel item attribute category dropdown fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v18.2 Attribute Editor fix for attributes designed to store other attributes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v19.1 attribute editing category dropdown fix and defined value picker long-list fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 14. Developer, API, Lava, And Source-Code Landmarks

### Developer Attributes

The Developer 303 Attributes page shows how custom blocks can render and save attribute values using `AttributeValuesContainer`, loading attributes on view/edit and saving values on save ([Developer 303 Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)).

Landmark concepts:

- `LoadAttributes()`
- display controls
- edit controls
- authorization-aware rendering
- saving attribute values
- runtime versus code-defined attributes

### Field Types And Field Attributes

The Extending Rock page distinguishes field types from field attributes and describes custom field type creation, configuration, edit controls, formatting, entity methods, persistence, registration, well-known GUIDs, and migrations ([Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further)).

Agent rule: if a built-in field type almost fits but not quite, first inspect field configuration options. Only recommend custom field types when the value semantics, UI, formatting, or persistence truly require custom code.

### Lava Attribute Filters

The Lava attribute filter docs cover:

- finding attributes through debug mode.
- reading attributes by key.
- returning object properties.
- attribute security in v17.5+.
- nested attribute access.
- looping over attributes.
- global attributes.
- system settings.
- other return values.
- key/value pair attributes.

Use this page as the primary Lava authority for attribute access ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### Workflow Lava

The Workflows and Lava page is especially important for raw values and field type internal storage. It explains that raw values may be the identifiers needed for links or page parameters and gives a field type storage overview ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).

### Obsidian Attribute Columns

The Obsidian `AttributeColumns` grid component is a placeholder column where dynamic attribute columns are placed. It accepts attribute field definitions and provides filtering/skeleton behavior ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns)).

Use this when diagnosing why attribute columns do or do not appear in an Obsidian grid.

### Mobile Controls

Mobile landmarks:

- Attribute Values block: category/entity-type based attribute display/edit, abbreviated names, styling, limited field type support ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)).
- Attribute Value Editor: developer-level control for rendering the right UI per attribute, limited field type support ([Mobile Attribute Value Editor](https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor)).
- Custom Site Attributes: v16.8+ mobile site custom attributes ([Custom Site Attributes](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes)).
- Campus Context Picker: sends selected campus context with every request, falls back to current person home campus if none set ([Campus Context Picker](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/campus-context-picker)).

### REST v2

Generated REST v2 controllers exist for defined types, defined values, and entity types:

- `api/v2/models/definedtypes` ([DefinedTypesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DefinedTypesController.CodeGenerated.cs)).
- `api/v2/models/definedvalues` ([DefinedValuesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DefinedValuesController.CodeGenerated.cs)).
- `api/v2/models/entitytypes` ([EntityTypesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/EntityTypesController.CodeGenerated.cs)).

The snippets show authentication and secured actions. Agents should not assume API access is available just because a model endpoint exists. Confirm authorization, REST settings, security actions, and whether unrestricted read/write permissions are required.

### Agent Tooling For Attributes

Rock developer docs include AvailableAttributes tools for AI agents. The page distinguishes retrieving attribute definitions from retrieving actual values and notes that an add operation may need available attributes even when no existing entity exists ([AvailableAttributes Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools)).

Agent implication: when constructing add/update payloads, first retrieve available attribute definitions, including keys and expected data types. Do not infer valid attributes from existing values only.

## 15. Reporting, Analytics, And Model Map

### Model Map

The supplied Model Map record identifies Attribute Value as a Core model ([Model Map](https://community.rockrms.com/ModelMap)). Use Model Map to confirm model existence and category, then use source code or live schema for field-level detail.

### SQL Relationship Patterns

The supplied SQL archive files are useful landmarks:

- `View_DefinedValuesAttributeValues.sql` lists each defined value’s attribute values by joining `AttributeValue`, `Attribute`, `EntityType`, `FieldType`, `DefinedValue`, and `DefinedType` ([View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)).
- `View_DefinedTypeAttributes.sql` lists defined type attributes by looking for attributes on `Rock.Model.DefinedValue` qualified by `DefinedTypeId` ([View_DefinedTypeAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)).
- Code generation SQL for defined values and entity types demonstrates that GUID constants are important in source and migrations ([CodeGen_SystemGuid_DefinedValue.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/CodeGen_SystemGuid_DefinedValue.sql), [CodeGen_SystemGuid_EntityType.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/CodeGen_SystemGuid_EntityType.sql)).

### Reporting Rules

When reporting on attributes:

- Join attribute values by `AttributeId`, not by display name.
- Filter attributes by `Key` or `Guid`, not just `Name`.
- Include entity type and qualifiers to avoid same-key collisions.
- Treat missing value rows separately from blank values.
- Resolve raw values according to field type.
- Include default values only if the report intentionally treats defaults as stored values.
- Use left joins when entities may not have values.
- Avoid wide joins over all attributes unless necessary.

When reporting on defined values:

- Use `DefinedTypeId` or defined type GUID to scope values.
- Avoid relying only on value text; labels can change.
- Include inactive/system flags if relevant.
- Include order for display.
- Join attributes only when metadata is needed.

When reporting on campuses:

- Define campus source explicitly.
- Include inactive campuses only if historical reporting requires it.
- Avoid conflating campus type, campus status, and campus assignment.
- Test all-campus behavior.

## 16. Version And Release Caveats

### Rock v10.3+

Lava docs note System Settings support beginning with Rock v10.3 ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). If a template depends on system setting access, verify the installed version and exact key.

### Rock v15.0+

Lava docs mention other return values beginning with Rock v15.0 ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). If a Lava template uses newer return-value options, verify version before backporting.

### Rock v16.8+

Mobile custom site attributes are documented as available as of v16.8 ([Custom Site Attributes](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes)). If a mobile app cannot read site attributes on an older Rock version, version may be the cause.

### Rock v17 And v17.5+

Rock v17 increased attribute security enforcement, and v17.5 added a third optional Lava parameter to bypass attribute-level security checks ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)). If Lava that used to show an attribute now returns blank or fails under non-admin users, inspect attribute security and version changes.

### Rock v17.2

Release notes document a fix for incorrect or unrelated categories appearing when editing Content Channel Item attributes from the Content Channel Type Detail block ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If a CMS attribute category picker looks wrong on an older v17 branch, check this caveat.

### Rock v18.2

Release notes document a fix where the Attribute Editor did not correctly save configuration changes for an Attribute designed to store other Attributes, affecting scenarios such as Page Parameter Filter block filters ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If a filter attribute’s configuration will not persist, check version.

### Rock v18.3

Release notes include fixes around registrant attributes and group placement filter accessibility in large attribute lists, plus the v18.2 attribute editor issue appears in the hydrated release excerpt context ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If event/group placement screens behave badly with many attributes, check release notes.

### Rock v19.1

Release notes document:

- Category dropdowns in multiple attribute editing blocks no longer include Global Attribute categories for the wrong entity type.
- Single-select Defined Value attributes configured as “Enhanced for Long Lists” display the searchable enhanced experience in Obsidian blocks such as Workflow Entry and Event Registration ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

If users report wrong attribute categories or hard-to-use defined value pickers in Obsidian blocks, verify whether the instance is before or after v19.1.

## 17. Implementation Playbooks

### Playbook: Audit An Attribute Before Editing

1. Identify attribute by key, GUID, and name.
2. Inspect entity type.
3. Inspect qualifier column/value.
4. Inspect field type.
5. Inspect categories.
6. Inspect security.
7. Count attribute values.
8. Inspect non-empty values.
9. Search Lava/templates/workflows/block settings for key and GUID.
10. Check data views/reports.
11. Check API/integration references.
12. Make change in staging if possible.
13. Test display, edit, Lava, report, and security behavior.

### Playbook: Create A Safe Defined Type

1. Define purpose and owner.
2. Decide whether values are user-facing, system-facing, or integration-facing.
3. Choose a clear name and description.
4. Add values with stable order.
5. Add descriptions where admins need context.
6. Add attributes only if each value needs metadata.
7. Decide whether categories are useful.
8. Test picker behavior in the consuming field type.
9. Document whether values may be renamed, disabled, or deleted.
10. Use GUIDs for code/migration references.

### Playbook: Replace A Defined Value

1. Identify old and new value IDs/GUIDs.
2. Check generated deletion blockers by trying safe UI validation or inspecting references.
3. Search model foreign keys.
4. Search attribute values that store the old value.
5. Search Lava and workflows.
6. Decide whether historical records should keep old value.
7. If replacing, migrate references explicitly.
8. Disable old value if deletion is unsafe.
9. Test reports and filters.
10. Document the change.

### Playbook: Diagnose Missing Attribute In A Block

1. Confirm the block supports attributes.
2. Confirm entity type.
3. Confirm qualifier.
4. Confirm category include/exclude settings.
5. Confirm public flag if public form.
6. Confirm field type support.
7. Confirm attribute security.
8. Confirm user authorization.
9. Confirm value exists or default applies.
10. Check release notes for category or editor bugs.
11. Test with admin and affected user.

### Playbook: Diagnose Lava Attribute Output

1. Enable Lava debug where available.
2. Confirm object contains attributes.
3. Confirm attribute key.
4. Confirm current user security.
5. Check formatted versus raw value.
6. If field type points to object, test object output.
7. If object output fails, verify field type supports property access.
8. Inspect raw stored value in `AttributeValue`.
9. Check version-specific attribute security behavior.

### Playbook: Build A Campus-Aware Workflow Or Report

1. Define campus source.
2. Define default campus behavior.
3. Define all-campus behavior.
4. Define no-campus behavior.
5. Use stable campus IDs/GUIDs.
6. Include inactive campuses only by intent.
7. Test with users from multiple campuses.
8. Test security.
9. For mobile, test selected campus context and home campus fallback ([Campus Context Picker](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/campus-context-picker)).
10. Document the behavior in the block/report/workflow description.

## 18. Troubleshooting Decision Tree

### Attribute Does Not Appear

Check:

1. Is the attribute active and saved?
2. Is the entity type correct?
3. Is the qualifier correct?
4. Is the attribute assigned to a category excluded by the block?
5. Is it uncategorized when the block only shows selected categories?
6. Is the public flag required?
7. Does the current user have permission?
8. Does the block support the field type?
9. Is this mobile, where field type support is limited?
10. Is the Rock version affected by category dropdown bugs?
11. Is the attribute on the related object, not the object being displayed?

### Attribute Appears With Wrong Category

Check:

1. Category entity type.
2. Attribute category assignments.
3. Whether the editor block has a known version bug.
4. Rock v17.2 for Content Channel Item category picker behavior.
5. Rock v19.1 for Global Attribute categories appearing in unrelated attribute editing blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
6. Browser/cache/admin UI refresh.

### Lava Attribute Returns Blank

Check:

1. Attribute key spelling.
2. Object availability.
3. Attribute loaded on object.
4. Attribute value exists.
5. Default value behavior.
6. Attribute security.
7. v17+ attribute security enforcement.
8. Whether raw value is needed.
9. Whether object output is needed.
10. Whether field type supports property access.

### Defined Value Picker Is Hard To Use

Check:

1. Field type configuration.
2. Whether enhanced long-list behavior is enabled.
3. Whether the block is Obsidian.
4. Rock v19.1 release notes for defined value picker enhanced long-list fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
5. Whether categories can narrow the list.
6. Whether the defined type has too many values for the chosen UI.

### Defined Value Cannot Be Deleted

Check:

1. Generated service deletion blockers.
2. Direct model references.
3. Attribute values storing the value.
4. Historical records.
5. Workflows and Lava.
6. Whether value is system-defined.
7. Whether disabling is safer than deletion.

Source code shows generated deletion checks for many defined value references ([DefinedValueService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs)).

### Entity Type Cannot Be Deleted Or Edited Safely

Check:

1. Attributes referencing it.
2. Audit records.
3. Authorization/security records.
4. AI agent or provider references.
5. Component registrations.
6. REST/model usage.
7. Notes and categories.
8. Whether it is system-generated.

Generated source shows `EntityTypeService.CanDelete()` checks many model references, including attributes and audit ([EntityTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/EntityTypeService.CodeGenerated.cs)).

### Campus Filter Shows Wrong Data

Check:

1. Which campus field is being filtered.
2. Whether “all campuses” is represented by null, zero, blank, or omitted parameter.
3. Whether current person campus is used as default.
4. Whether selected mobile campus context overrides home campus.
5. Campus type/status filters.
6. User security.
7. SQL/Lava parameter safety.
8. Inactive or online campuses.

### Mobile Attribute Editing Fails

Check:

1. Attribute entity type.
2. Category compatibility.
3. Mobile field type support.
4. Mobile shell version.
5. Attribute Values block settings.
6. Attribute Value Editor usage.
7. User security.
8. Whether the attribute is display-only in that surface.

Mobile docs repeatedly warn that only supported field types can be edited ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values), [Mobile Attribute Value Editor](https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor)).

## 19. Agent Task Recipes

### Recipe: Find Available Attributes For An Add Or Update Operation

Use when constructing an agent tool, API payload, or data-entry action.

1. Identify the entity type.
2. If updating, load the existing entity.
3. If adding, initialize the entity context enough to determine available attributes.
4. Retrieve attribute definitions, not values.
5. Capture key, name, field type, required status, default, qualifiers, and allowed values.
6. Ask for or construct values in the correct raw format.
7. Submit values by key or expected API shape.
8. Re-read the entity and verify stored values.

The AvailableAttributes developer docs explicitly distinguish available attribute definitions from actual values and note the add-operation case where no existing entity exists ([AvailableAttributes Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools)).

### Recipe: Explain A Platform Configuration Object To A User

Return:

- What it is.
- Where it is configured.
- Which entity type it applies to.
- Which records consume it.
- Whether it stores values or only definitions.
- Whether changing it affects historical data.
- What to inspect before editing.
- Version caveats.

### Recipe: Safely Answer “Can We Delete This?”

For attributes:

- Count values.
- Search references.
- Check security/public use.
- Check workflows and Lava.
- Prefer disable/hide if uncertain.

For defined values:

- Check model references and generated deletion blockers.
- Check stored attribute values.
- Check historical reporting.
- Prefer inactive/renamed state if history matters.

For entity types:

- Treat deletion as exceptional.
- Inspect all references.
- Avoid deletion of system or source-created entity types.

### Recipe: Build A Source-Backed Explanation

When answering a configuration question:

1. Cite official docs for concept.
2. Cite source code for model/API/deletion behavior.
3. Cite release notes for version caveat.
4. Cite community recipe only as an example.
5. State what must be inspected live.

Example: For a missing content channel item attribute category, cite the release note and then instruct inspection of the live content channel type, attribute entity type, qualifier, and category assignment ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Recipe: Triage Attribute Security

1. Reproduce as affected user.
2. Reproduce as admin.
3. Check base entity view permission.
4. Check attribute authorization.
5. Check block authorization.
6. Check Lava security behavior.
7. Check Rock version.
8. Decide whether to adjust security, template context, or data placement.

Use the v17/v17.5 Lava docs as the version anchor ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### Recipe: Convert A Free-Text Attribute To A Defined Value

1. Inventory existing text values.
2. Normalize spelling/case.
3. Create defined type and values.
4. Create replacement attribute with defined value field type.
5. Map old values to defined values.
6. Migrate values in staging.
7. Update Lava/reports/forms.
8. Hide old attribute after validation.
9. Keep old data until retention/review is complete.
10. Delete only after references are gone and stakeholders approve.

### Recipe: Diagnose Attribute Field Type Mismatch

1. Inspect field type on the attribute.
2. Inspect raw stored values.
3. Compare stored format with workflow Lava field type docs.
4. Confirm consuming block supports that field type.
5. For mobile, verify supported field type list.
6. If data was stored with the wrong field type, plan migration before switching type.
7. Test old values after field type change.



















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `78`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | operational_guidance | Rock plugin and theme packaging guidance frames the Rock Shop as the distribution path for community extensions, so plugin work should include packaging, review, and uninstall behavior rather than only local code changes. | [source](https://community.rockrms.com/developer/packaging-plugins-themes) |
| community-reviewed | operational_guidance | Rock metrics are a useful capture layer for dashboard history because they can run off-hours, store repeatable values, and support later visualization without repeatedly recalculating expensive operational queries. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp) |
| community-reviewed | operational_guidance | For dashboard speed, expensive journey analytics can be calculated into a persisted dataset on a schedule rather than recalculating all historical engagement data on each page load. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) |
| community-reviewed | operational_guidance | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Rock's analytics-enabled tables can be used as a snapshot layer for engagement-style metrics, allowing external reporting tools to query daily counts or trends without repeatedly reconstructing every operational detail. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz) |
| community-reviewed | operational_guidance | When BI reports are embedded back into Rock, teams still need to honor external licensing and put report pages behind appropriate Rock security roles. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) |
| community-reviewed | implementation_pattern | A Rock Check-in implementation can involve process mapping and extended troubleshooting, not only enabling the check-in feature. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-47-special-edition-lee-peterson) |
| community-reviewed | implementation_pattern | A Rock discovery process should include ministry stakeholders early because it can reveal workflows, data handoffs, and manual spreadsheet work that staff may not have formalized. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-84-special-edition-with-red-rocks) |
| community-reviewed | operational_guidance | External BI tools become more useful when questions require complex modeling, multiple source systems, high-level KPI reporting, or visualization patterns that are difficult to keep performant inside Rock alone. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) |
| community-reviewed | operational_guidance | Migration plans should identify which system is the trusted source of truth for person, contribution, check-in, and event data before expanding to optional ministry workflows. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/podcast-episode-111-special-edition-with-tim-dear) |
| community-reviewed | operational_guidance | Contributor-authored KB material should aim for accessible explanations that church staff can use, not only developer-oriented technical detail. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-91-special-edition-with-cullen-mccoy) |
| community-reviewed | operational_guidance | For member surveys, public or shared results should avoid direct personal identifiers and return church-specific data in aggregated form so teams learn from patterns without turning the study into a person-level accountability list. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz) |
| More |  | 66 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `18`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Episode 111: Special Edition with Tim Dear Transcript Insight](https://shows.acast.com/rock-cast/episodes/podcast-episode-111-special-edition-with-tim-dear) | approved_for_public_distillation | 3 | media-insight:05f4fce834300a65 |
| [Episode 33: Rock 7.3 and New RX2018 Tracks Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-33-rock-73-and-new-rx2018-tracks) | approved_for_public_distillation | 4 | media-insight:6b5ce810e2795435 |
| [Episode 37: Special Edition Garrett Johnson Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-37-special-edition-garrett-johnson) | approved_for_public_distillation | 3 | media-insight:97a12ee26ba9575f |
| [Episode 40: v8 and more team updates Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) | approved_for_public_distillation | 3 | media-insight:6e8d02135da566a7 |
| [Episode 47: Special Edition Lee Peterson Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-47-special-edition-lee-peterson) | approved_for_public_distillation | 2 | media-insight:a11e091aa9800728 |
| [Episode 84: Special Edition with Red Rocks Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-84-special-edition-with-red-rocks) | approved_for_public_distillation | 3 | media-insight:40920b5275ce640a |
| [Episode 91: Special Edition with Cullen McCoy Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-91-special-edition-with-cullen-mccoy) | approved_for_public_distillation | 2 | media-insight:f609e5067739f62b |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) | approved_for_public_distillation | 3 | media-insight:21c296e1bd9698dc |
| More |  | 10 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->



















## 20. Source Map And Dependency Notes

Primary official and source-code records used:

- RockU Core Concepts establishes entities, attributes, defined types, campuses, categories, jobs, automations, note types, and related configuration as foundational topics ([RockU Core Concepts](https://community.rockrms.com/rocku/core-concepts)).
- Developer 303 Attributes documents runtime and code-backed attributes and block-level display/edit patterns ([Developer 303 Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)).
- Lava Attribute Filters documents attribute access, debug discovery, object return, global attributes, system settings, and v17/v17.5 security behavior ([Attribute Lava Filters](https://community.rockrms.com/lava/filters/attribute-filters)).
- Workflows and Lava documents raw attribute values and field-type internal storage considerations ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).
- Extending Rock Even Further documents the distinction between field types and field attributes and custom field type implementation concepts ([Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further)).
- Mobile Attribute Values, Attribute Value Editor, Custom Site Attributes, and Campus Context Picker document mobile-specific attribute and campus behavior ([Mobile Attribute Values Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values), [Mobile Attribute Value Editor](https://community.rockrms.com/developer/mobile-docs/essentials/controls/form-fields/attribute-value-editor), [Custom Site Attributes](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/custom-site-attributes), [Campus Context Picker](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/campus-context-picker)).
- Obsidian AttributeColumns documents dynamic attribute columns in grids ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns)).
- AvailableAttributes Tools documents agent-tool handling of attribute definitions versus values ([AvailableAttributes Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/availableattributes-tools)).
- Release notes provide version caveats for category dropdown fixes, attribute editor fixes, defined value picker behavior, and related platform changes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Engagement documentation provides an operational example of connection request attributes, categories, public flag usage, and signup block configuration ([Engagement Documentation](https://community.rockrms.com/documentation/bookcontent/39)).
- Model Map identifies Attribute Value as a Core model ([Model Map](https://community.rockrms.com/ModelMap)).
- Source files provide model/API/security/deletion relationship evidence:
  - [View_DefinedValuesAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql)
  - [View_DefinedTypeAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql)
  - [DefinedTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedType/DefinedTypeService.cs)
  - [DefinedValueService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/DefinedValue/DefinedValueService.cs)
  - [EntityTypeService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/EntityType/EntityTypeService.cs)
  - [DefinedTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedTypeService.CodeGenerated.cs)
  - [DefinedValueService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/DefinedValueService.CodeGenerated.cs)
  - [EntityTypeService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/EntityTypeService.CodeGenerated.cs)
  - [EntityTypeSecurityGrantRule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/SecurityGrantRules/EntityTypeSecurityGrantRule.cs)
  - [DefinedTypesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DefinedTypesController.CodeGenerated.cs)
  - [DefinedValuesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DefinedValuesController.CodeGenerated.cs)
  - [EntityTypesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/EntityTypesController.CodeGenerated.cs)
  - [EntityTypesBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesBag.cs)
  - [entityTypesBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesBag.d.ts)

Community and secondary records used as examples only:

- Slicker Campus Filters demonstrates a report pattern for campus page parameters and “All Campuses,” but it is community-contributed and should be validated before production use ([Slicker Campus Filters](https://community.rockrms.com/recipes/393)).
- Event Specific Custom Check-In Success Messages demonstrates group and group type attributes used to customize check-in Lava output, but it is community-contributed and should be reviewed for security and performance ([Event Specific Custom Check-In Success Messages](https://community.rockrms.com/recipes/385)).
- Triumph’s GitHub Spotlight is secondary release commentary and should be confirmed against official release notes and the live instance before relying on exact system-setting behavior ([Triumph GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-12202024)).

Dependency topics for deeper guides:

- People: person, family, bookmarked, profile, and sensitive attributes.
- Groups: group type, group, group member attributes, check-in, and placement.
- Workflows: workflow attributes, field types, form entry, raw values.
- CMS: content channel attributes, site attributes, Lava, interactions.
- Security: authorization, public flags, entity type grants, attribute security.
- Data Views: attribute filters, queryable attribute values, performance.
- Reports: campus filters, defined values, dynamic data, SQL safety.
- Operations: release notes, migrations, jobs, cache, global settings, and deletion safety.
