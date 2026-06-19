---
id: authored-obsidian-development
title: Obsidian Development
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Obsidian Development

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Obsidian Development index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Obsidian is Rock RMS's modern web UI development stack for building blocks, controls, grids, and field type experiences. For practical agent work, the most important distinction is this: an Obsidian feature is rarely "just a page." It is usually a coordinated contract between C# server code, TypeScript browser code, generated view models or bags, Rock security checks, block configuration, entity data, and the browser runtime. The official developer documentation describes Obsidian as primarily core-team-oriented and still subject to change, while noting that some portions, especially grids, are useful outside core development as well ([Obsidian](https://community.rockrms.com/developer/obsidian)).

When an agent is asked to inspect, extend, troubleshoot, or migrate Obsidian work, start by identifying the surface:

- A block is the page-level Rock unit that provides server logic and, normally, a client component ([Blocks](https://community.rockrms.com/developer/obsidian/blocks)).
- A C# block owns server-side logic, database access, authorization decisions, configuration, initialization data, and block actions ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).
- A TypeScript `.obs` component owns browser rendering, reactive state, form interaction, client validation, grid configuration, and calls back to C# actions when data must be saved or loaded ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)).
- A grid is a client-heavy table control with paging, filtering, sorting, export, actions, and column definitions; the standard Obsidian grid performs client-side filtering and sorting, so all row data needed for that grid is sent to the browser before it renders ([Grids](https://community.rockrms.com/developer/obsidian/grids)).
- A field type describes how a value is viewed, edited, filtered, and configured. Modern work should prefer Universal Field Types where possible because they move UI-specific behavior out of the C# field type and leave the field type to express data and logic ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types), [Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types)).
- Obsidian is not WebForms with a different file extension. Whole-page postback assumptions, response-mutating Lava behavior, and server-rendered control assumptions often fail or require redesign ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).

The operational rule for agents is to avoid guessing from the visible UI alone. If an Obsidian block misbehaves, inspect the server block, the client component, the generated bags, the entity security model, block attributes, page routes, browser console, network calls, and the Rock version. Release notes show repeated Obsidian fixes across blocks, field types, grid exports, selectors, security, and performance, so a symptom may be caused by configuration, code, data shape, security, version behavior, or a known fixed bug ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Use this guide as an operational manual, not as a substitute for source review. When it says "inspect," verify in the target Rock instance or repository branch. When it cites release notes, compare the target instance version. When it references source paths, confirm the path on the branch being modified because Obsidian is actively evolving.

## 2. Scope And Terminology

This guide covers Obsidian development in Rock RMS, with emphasis on block development, list/detail block patterns, grid columns and filters, field types, UI controls, browser bus messaging, development environment, plugin considerations, Lava interaction, security, and troubleshooting.

The term "Obsidian" in this guide means Rock's browser-side application framework and related server-side block infrastructure for modern web blocks. The official entry page states that much of the material is written for core development, not all plugin development, and that the documentation is a work in progress ([Obsidian](https://community.rockrms.com/developer/obsidian)). Agents should therefore classify guidance into three buckets:

- Stable public concept: ideas like server/client block separation, grids, field type responsibilities, and form validation.
- Core-oriented implementation pattern: paths such as `Rock.JavaScript.Obsidian/Framework/Controls`, `Rock.JavaScript.Obsidian/Framework/FieldTypes`, and core code generation.
- Instance- or version-specific behavior: exact block settings, registered block types, generated model names, release fixes, and available developer tooling.

A "block" is the Rock unit placed on a page. In Obsidian, the server part is C# and is required; the client part can be Obsidian, Rock Mobile, or another framework, and for web blocks it is normally an `.obs` component ([Blocks](https://community.rockrms.com/developer/obsidian/blocks)).

A "block action" is the communication path from browser code back to server code. It functions like a block-scoped API. The browser component uses it when a user clicks save, deletes a row, reloads data, validates server-derived state, or performs an operation that must run inside Rock's server-side context ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

A "bag" is a data transfer object used to pass structured data between server and client. The source pack references view model and bag usage through TypeScript imports such as `PublicAttributeBag`, `ListItemBag`, grid definition bags, field editor option bags, and block-specific view option bags in the Rock source repository ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

A "detail block" displays one entity, usually with a standardized view/edit layout, labels, badges, and custom actions. The block developer supplies data and options; the shared detail component controls the layout so detail blocks remain visually consistent ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)).

A "list block" displays records for an entity, typically using a grid. Core development can use the Code Generator for a vanilla list block; the docs explicitly warn that this core code generator is not currently available to plugins ([Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks)).

A "field type" is the recipe for how a field works. It is not the field value itself. It provides behavior for display, editing, filtering, and configuration ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)). The Model Map identifies Field Type as a Rock model in the Core category, which is a reminder that field types participate in Rock's broader entity and attribute model, not only UI rendering ([Model Map](https://community.rockrms.com/ModelMap)).

A "Universal Field Type" is a newer pattern intended to avoid WebForms-specific coupling by moving UI behavior out of the C# field type and treating the field type as data and logic that can be consumed by different UI frameworks ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types)).

A "grid column" is a component-level definition that tells the Obsidian grid how to display, sort, filter, export, or act on a field. Standard columns include text, boolean, date, date-time, currency, number, person, label, reorder, security, select, edit, delete, copy, attribute, and custom columns ([Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns)).

A "browser bus" is a single-page pub-sub interface. It passes messages between components on the same page through a custom browser event named `rockMessage`; it does not cross tabs or browsers ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)).

## 3. Obsidian Development Mental Model

Think of an Obsidian feature as a layered contract.

At the bottom is the Rock data model. Entities, attributes, field types, security rules, defined values, groups, workflows, communications, locations, assets, and other models remain server-side Rock concepts. Obsidian does not remove the need to understand those entities. It changes how a page interacts with them.

Above the data model is the C# block. The C# block retrieves data, checks authorization, resolves block/page configuration, constructs initial view models, exposes block actions, and controls what the browser may request. The block should not be treated as a passive JSON endpoint. It runs inside Rock's security and context model and should be the enforcement point for operations that touch data.

Above the C# block is the TypeScript `.obs` component. The component renders markup, tracks reactive state, calls block actions, owns browser-side validation state, configures grids, composes controls, and responds to user input. The official component structure page frames an Obsidian component as a file with template markup at the root and script setup logic for imports, props/events, and behavior ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)).

Above the component are framework controls. Controls include pickers, text boxes, forms, grid columns, field editors, modal components, security editors, and reusable UI widgets. Controls may make API calls, consume security grants, or rely on generated view model types. Agents must not assume that a visible picker is "just HTML"; it may be backed by Rock-specific security and server contracts ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)).

Alongside all of that is generated or shared TypeScript model data. Source snippets show imports such as `@Obsidian/ViewModels/Utility/publicAttributeBag`, `@Obsidian/ViewModels/Utility/listItemBag`, and block-specific bags under `@Obsidian/ViewModels/Blocks/...` ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). These generated bags are often the strongest clue about the expected JSON shape. When an Obsidian screen fails at runtime because a property is missing or has the wrong type, inspect the bag definitions and the C# code that builds them.

The key runtime loop is:

1. Rock renders the page and block shell.
2. The C# block supplies initialization data and references the component.
3. The browser loads the Obsidian component and its dependencies.
4. The component renders using initial data.
5. User actions update local state, call block actions, publish browser bus messages, open modals, or update grids.
6. Server actions validate permissions and data, perform operations, and return updated bags or result statuses.
7. The component updates state without a full page reload.

This loop explains why WebForms assumptions break. Lava filters that mutate response headers, redirects, or metadata can be unreliable after an Obsidian action because the original page response has already been sent and later interactions are not full page reloads ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).

It also explains why null handling matters. C# developers often use `null` as a value; JavaScript and TypeScript also have `undefined`, including missing JSON properties. The Obsidian docs call this distinction out because a property omitted from JSON is not the same as a property explicitly set to `null` or an empty string ([Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined)). For agents, this means a bug may not be a failed query at all; it may be a serialization shape mismatch.

## 4. Source Authority And How To Use This Guide

Prefer sources in this order:

1. Current Rock source code for the exact branch and version being modified.
2. Official Rock developer documentation for the Obsidian area.
3. Official release notes and tech bulletins for version behavior.
4. Rock Model Map and API documentation for entity/API orientation.
5. RockU or official training, when available in the source pack.
6. Community examples, partner spotlights, or recipes only as supporting evidence.

The official Obsidian developer documentation is authoritative for concepts but openly caveated as work in progress and core-team oriented ([Obsidian](https://community.rockrms.com/developer/obsidian)). Therefore, do not use this guide to assert that a pattern is supported for every plugin or every Rock version. Use it to decide what to inspect.

For core development, the source pack points to important paths in the public Rock repository:

- `Rock.Blocks` for C# block implementations.
- `Rock.JavaScript.Obsidian.Blocks/src/...` for Obsidian block components.
- `Rock.JavaScript.Obsidian/Framework/Controls` for shared controls, per the UI control documentation ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)).
- `Rock.JavaScript.Obsidian/Framework/FieldTypes` for field type browser handlers and components, as shown in source snippets for `addressField.partial.ts`, `assessmentTypesField.partial.ts`, `securityRoleField.partial.ts`, and related component files ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
- `Rock.JavaScript.Obsidian.Blocks/src/<Area>/tsconfig.json` files that reference framework projects such as controls, core, directives, enums, field types, libs, page state, system GUIDs, templates, utility, and validation rules ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

For plugin development, use the plugin documentation and verify the current `rock-dev-tool` behavior. The official plugin page says plugin development is driven by `rock-dev-tool`, while warning that specific Rock versions referenced by the tool may not all be available and should be checked against published package versions ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)). Do not copy core paths into a plugin without adapting namespace, build, packaging, and registration conventions.

For release caveats, use Rock release notes first. The source pack includes release-note records for fixes in Obsidian field configuration, grid exports, block registration visibility, Workflow List performance, picker behavior, memo HTML rendering, Group Attendance ID resolution, Location hierarchy validation, and more ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Agents should always compare the target instance version before diagnosing a symptom as custom code failure.

For field type entity awareness, use the Model Map as metadata, then verify the actual database schema and model class in the target version ([Model Map](https://community.rockrms.com/ModelMap)). The source pack only gives compact metadata for Field Type; it does not provide enough detail to infer all relationships.

For API work, use the Rock API documentation and inspect the exact API version. The API docs identify API v1 as legacy and API v2 as the faster newer API surface, but block actions are not the same thing as general-purpose public REST API endpoints ([API Documentation](https://community.rockrms.com/api-docs)).

## 5. Core Configuration And Data Model

Obsidian configuration exists at several levels. Agents should identify which level is involved before editing anything.

Block Type configuration determines what kind of block can be placed on a page. If a newly added Obsidian block type does not appear in the Page Zone Editor, compare the instance version with the release note that fixed a startup visibility issue for newly added Obsidian block types in v18.2 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). In a live instance, inspect the Block Type record, its path/component references, assembly/class information, category, cache state, and whether the Rock server was restarted or caches were cleared after deployment.

Block instance attributes determine behavior for a block placed on a page. In Obsidian, settings that once used WebForms custom settings may be implemented through `IHasCustomActions`, which returns custom action metadata and points to a separate `.obs` component for the configuration screen ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions)). In a live instance, inspect the block's attributes, attribute values, page, zone, block type, security, and any custom action component URL.

Page and route configuration determine how the block receives URL parameters and whether it can resolve entity keys. The release notes include an Obsidian Group Attendance Detail fix related to resolving a selected group by Guid or IdKey when Predictive Ids are disabled ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). That kind of issue is not just a UI bug; it sits at the boundary between route values, entity identifiers, site settings, and server-side entity lookup. In a live instance, inspect route parameters, page parameters, site settings for predictive IDs, and the block action or initialization code that resolves the entity.

Field Type configuration determines how attributes behave. A field type can define how to view, edit, filter, and configure a value ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)). For Obsidian, configuration values usually move across the browser/server boundary as string dictionaries or structured bags. Source snippets for field type components show patterns such as `configurationValues`, `ConfigurationKey`, `modelValue`, `update:modelValue`, conversion helpers, and watchers ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). When a field type behaves incorrectly, inspect the C# field type, TypeScript field type handler, edit component, configuration component, serialized configuration values, public/private configuration visibility, and the attribute using that field type.

Universal Field Type configuration deserves special care. Release notes show a v18.1 bug fix where editing configuration settings of Universal field types from inside an Obsidian block could store raw JSON for some configuration setting types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If an attribute's configuration values look like JSON where a scalar value is expected, compare the instance version and reproduce in a non-production environment.

Grid configuration is split between server data/definition and browser column/filter/action setup. The grid reference identifies `Data` as required and able to be either direct grid data or a function/promise, `Definition` as containing field/action/feature metadata, `keyField` as the unique row identifier needed by many advanced features, and `personKeyField` as the field containing a person key when applicable ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid)). In a live or source inspection, verify that the grid rows contain stable keys, that action URLs or block actions exist, and that the row shape matches the columns.

Security configuration may appear in block-level authorization, entity authorization, security grants, and grid columns. The UI control documentation describes security grants as a way for blocks to grant controls access to specific entities, entity types, or related data ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)). The `SecurityColumn` opens the standard security editor modal for an item, with configurable item title and disabled state ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)). In a live instance, verify both whether the user can see the page/block and whether the server action allows the operation.

Person preferences can store per-person UI state. The Creating Blocks documentation includes person preference sections for preference providers and collections ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). Source snippets for `LoginHistory/types.partial.ts` include a `PreferenceKey` for a sliding date range and `GridSettingsOptions`, illustrating that grid state or filter preferences may be preserved in typed client/server contracts ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). When a grid "remembers" an unexpected filter, inspect person preferences and any preference key constants.

## 6. Primary Entities And Relationships

The source pack does not provide a full database schema for Obsidian, and Obsidian is partly a framework rather than a single entity. Treat the following as a relationship map to guide inspection.

Page contains zones. Zones contain block instances. A block instance references a Block Type. A Block Type identifies the server-side C# block and, for Obsidian blocks, the client component or component file information. The C# block decides what data and actions to expose. The `.obs` component renders that block and calls actions. If a block appears on one page but not another, inspect Page, Layout, Site, Zone, Block, BlockType, and security.

Block attributes are Rock attributes attached to a block instance. Attribute definitions are backed by field types. Attribute values store configuration for a block instance. For custom administrate behavior, an Obsidian block may use `IHasCustomActions` and a separate `.obs` component to present settings ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions)). If a setting UI saves but behavior does not change, inspect the attribute value row, server cache, block action result, and whether the TypeScript component is reading the same configuration key the server writes.

Entity attributes are dynamic fields attached to Rock entities. In grids, `AttributeColumns` provides a placeholder for dynamic attribute value columns ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns)). `RockFieldColumn` allows one Rock field value to be displayed but is described as internal to Rock and not for plugin use ([RockFieldColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/rockfieldcolumn)). If dynamic attributes do not show in a list block, inspect whether the server includes attribute field definitions, whether the client includes `AttributeColumns`, whether the user has access to view the attributes, and whether the row data includes formatted values.

Field Type is a core model, and field type behavior spans C# and TypeScript. The field type is the behavior definition; the field or attribute value is the stored data ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types), [Model Map](https://community.rockrms.com/ModelMap)). In source snippets, field type handlers extend `FieldTypeBase`, return edit/configuration components, parse JSON values, convert string booleans, and expose text display values ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). If a field value displays one way in WebForms and another in Obsidian, inspect whether the field type has an Obsidian implementation or Universal Field Type support.

Grid rows are browser-side data objects. A grid column maps to row fields through properties such as `field`, `sortField`, export value functions, quick filter value functions, and custom templates ([Standard Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/standard-columns)). Advanced row operations require stable keys. If sorting duplicates rows, compare with the release note that fixed the Obsidian Dynamic Data block lacking a reliable unique key ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Person records are often represented through person bags or fields. `PersonColumn` requires the field to be added through the server-side `.AddPersonField()` method so all required values are present ([PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn)). If a person column lacks avatars, links, hover info, sorting, or detail text, inspect the server grid builder and row shape rather than only the client template.

Security entities may be edited from a grid through `SecurityColumn`, but actual permissions are server-controlled ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)). If a user sees a security button but cannot make changes, inspect entity authorization, item-specific security, block/page authorization, and whether the row has a disabled field such as the column's default disabled field.

## 7. Common Obsidian Development Workflows

### Build A New Core List Block

For a core list block, start with the official list block pattern. The docs describe list blocks as standardized blocks that display records for a particular entity and say the Code Generator can create a vanilla list block for core blocks ([Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks)). The same page warns that the core Code Generator is not currently available to plugins, so do not plan plugin work around it without verifying current tooling.

Operational steps:

1. Identify the entity and whether the list should use standard entity services, custom queries, or a performance-specific query path.
2. Generate or inspect the C# block, view model/bag classes, and `.obs` component.
3. Decide row identity. Pick a stable `keyField`; many grid features depend on it ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid)).
4. Decide columns. Use specialized columns where possible: `TextColumn`, `BooleanColumn`, `DateColumn`, `DateTimeColumn`, `NumberColumn`, `CurrencyColumn`, `PersonColumn`, `LabelColumn`, `EditColumn`, `DeleteColumn`, `SecurityColumn`, `SelectColumn`, `ReorderColumn`, or `AttributeColumns` ([Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns)).
5. Decide filters. Use standard filters when field type and row data allow it: boolean, date, number, text, or pick-existing value ([Filters](https://community.rockrms.com/developer/obsidian/grid-reference/filters)).
6. Decide actions. Grid actions may include add, edit, delete, reorder, bulk operations, export, or custom row actions.
7. Validate row count and payload size. The Obsidian grid's normal filtering and sorting are client-side; do not send huge datasets casually ([Grids](https://community.rockrms.com/developer/obsidian/grids)).
8. Test with realistic permissions, realistic record counts, and realistic custom attributes.

If the block needs custom columns, verify whether the data path supports them. Release notes show that the Obsidian Communication List block disabled custom columns because they were incompatible with that block's high-performance query ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). That is a useful precedent: not every list block can support every standard grid affordance.

### Build A Detail Block

Use the detail block pattern when the primary task is viewing and editing one entity. The official detail block docs describe a standardized entity display with edit capability, labels, badges, and custom actions ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)). The developer provides what should be displayed; the shared detail block component owns the layout.

Operational steps:

1. Identify the entity key source: page parameter, route value, block setting, selected row, or created record.
2. Load the entity in the C# block and check authorization before sending data to the browser.
3. Build a view bag that contains display values, editable values, labels, badges, panel actions, and any field definitions.
4. Use standardized detail layout features instead of custom page layout when the block is meant to match Rock detail patterns.
5. Implement save actions on the C# side, including concurrency, validation, authorization, and audit behavior where applicable.
6. Use `RockForm` and standard field components for browser-side validation and consistent UI ([Form Validation](https://community.rockrms.com/developer/obsidian/form-validation)).
7. If the block has administrate settings, consider `IHasCustomActions` with a separate `.obs` settings component ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions)).
8. Test create, edit, cancel, save, validation failure, unauthorized user, deleted/missing entity, and stale route parameter behavior.

When detail behavior differs by Rock version, check release notes. The source pack includes examples: Location Detail now prevents self or child location as parent in v18.3; Group Requirement Type Detail had attribute values loading/saving fixed in v18.3; Note Type Detail changed unsupported manual approval UI; Communication Template Detail was added in v17.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Add A Custom Block Settings Screen

If the block needs a richer configuration surface than simple block attributes, use the `IHasCustomActions` pattern. The docs compare it to the older WebForms `RockBlockCustomSettings` style and say to create a separate `.obs` file for the configuration screen ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions)).

Operational checks:

- The server block implements `IHasCustomActions`.
- The action is only returned when the current user has the appropriate edit or administrate permission.
- The custom action bag points to the correct component file URL.
- The `.obs` component loads in the administrate context.
- Save actions validate input server-side.
- Attribute keys and configuration keys are consistent across C# and TypeScript.
- Saved values are visible in the block instance attributes or relevant configuration store.
- The block refreshes configuration after save or clearly requires page reload if that is the established pattern.

Do not expose administrate configuration actions to users who only have View access. Release notes show at least one block was changed so View-only users see grid data plus a note that Administrate access is required for changes, which is a good operational pattern for read-only states ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Convert WebForms Behavior To Obsidian

Conversion is not one-to-one. WebForms controls often embed UI behavior, server postback behavior, and data conversion in a single server-side control. Obsidian separates those responsibilities. For field types, the docs call legacy WebForms coupling a major reason for the Universal Field Type pattern ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types)).

Conversion checklist:

- Identify WebForms-only APIs, postbacks, view state, server controls, and response mutations.
- Move page interaction into `.obs` components.
- Move data access and security into C# block actions.
- Replace server-side control rendering with standard Obsidian controls where available.
- Replace WebForms field type UI methods with Obsidian field type handlers or Universal Field Type data contracts.
- Revisit Lava usage that changes response headers, redirects, or meta tags because those operations may not work in Obsidian interactions ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).
- Re-test authorization. Browser-side state must not become the enforcement point.
- Re-test null, empty string, and missing property behavior because JSON and TypeScript semantics differ from C# ([Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined)).

### Troubleshoot An Existing Obsidian Screen

Use a top-down and bottom-up pass.

Top-down:

1. Confirm Rock version.
2. Confirm page, block type, block instance, and site.
3. Confirm current user's permissions.
4. Reproduce in the browser and inspect console/network.
5. Identify the component and server block.
6. Inspect block actions and payloads.
7. Inspect row/entity/attribute data.
8. Compare with release notes.

Bottom-up:

1. Inspect the entity and field values.
2. Inspect field type and configuration.
3. Inspect server bag construction.
4. Inspect generated TypeScript view model types.
5. Inspect `.obs` props, watchers, computed values, and event emits.
6. Inspect grid column definitions, filters, and key fields.
7. Inspect browser bus messages if multiple components interact.
8. Inspect cache or person preferences if state persists unexpectedly.

## 8. Blocks Deep Dive

The official block documentation divides a block into server and client parts. The C# server part is required and contains logic to view, edit, and interact with the person viewing the page; it does not handle UI. The client part handles UI and direct interaction, and can be Obsidian or another framework ([Blocks](https://community.rockrms.com/developer/obsidian/blocks)).

### C# Block Responsibilities

The C# block should be treated as the authoritative layer for:

- Loading data from Rock services or repositories.
- Resolving page parameters and block settings.
- Checking authorization.
- Constructing initialization bags.
- Defining block actions.
- Enforcing server-side validation.
- Saving changes.
- Returning updated state or error results.
- Providing security grants to controls when needed.
- Reading and writing person preferences when the block supports persistent user state.
- Handling block lifecycle events such as updates where applicable ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

Do not rely on the TypeScript component to enforce access rules. A user can inspect and modify browser requests. Every block action that reads sensitive data or mutates data must validate permission server-side.

### TypeScript Component Responsibilities

The `.obs` component should be treated as the browser interaction layer. The component structure docs describe a component as containing the template, imports, props/events, and logic ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)). In practice, component responsibilities include:

- Rendering the visible UI.
- Managing reactive state.
- Receiving initialization data.
- Calling block actions.
- Handling loading, empty, error, and validation states.
- Composing standard controls.
- Configuring grids.
- Responding to browser bus messages.
- Emitting events to parent components.
- Translating browser-friendly values into server action payloads.

Source snippets show common imports from Vue, Obsidian utilities, controls, view models, validation rules, enum definitions, and generated bags ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). Use those imports as clues to the expected layer. If a component imports `ValidationRules`, it may own client-side validation. If it imports generated view model bags, it likely expects a server contract. If it imports a picker, inspect the picker's configuration and security requirements.

### Block Actions

Block actions are the block-scoped communication mechanism from TypeScript to C#. The Creating Blocks page describes them as the API-like mechanism that allows TypeScript to communicate with C# when, for example, a user saves a change ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

Operationally, block actions should:

- Receive minimal, explicit payloads.
- Validate the current user and entity access.
- Validate the payload independently of browser validation.
- Handle missing or stale records.
- Return typed results.
- Avoid leaking sensitive exception details.
- Be idempotent where possible.
- Return updated bags if the UI needs to refresh without a full reload.

For agents, a block action failure should be investigated as a server problem first, not a browser problem. Inspect server logs, network response, exception details in development, action method names, action registration, payload shape, authentication, anti-forgery or security token behavior if present, and authorization.

### BlockCrumbs And Navigation Context

The Creating Blocks documentation includes BlockCrumbs as a block concept ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). Use them as part of page navigation and entity context. If breadcrumbs are wrong or missing, inspect how the block identifies the current entity, how it sets crumb labels, and whether the page route supplies enough context.

### Boxes, Bags, And Entities

The Creating Blocks page explicitly calls out "Boxes and Bags and Entities" ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). The practical meaning is that agents should keep domain entities separate from transport objects. Do not send full entity objects to the browser when a smaller bag is appropriate. Do not let browser bags become persistence models without server validation.

Typical pattern:

- Entity: the server-side Rock model, usually loaded through a service.
- Bag/ViewModel: the server-to-client shape, often generated or shared.
- Box: a wrapper or payload shape used by block infrastructure or actions.
- Component state: the browser's reactive version of the data.

When bugs appear after a refactor, check whether a property was renamed in one layer but not the others.

### Detail Blocks

Detail blocks have a standardized feature set. The docs emphasize that the developer can turn features on and off, but the layout itself is not up to the block developer because a shared detail component controls standardization ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)).

Detail block agents should inspect:

- Entity loading method.
- Edit mode state.
- Save/cancel path.
- Labels and badges.
- Panel actions.
- Custom actions.
- Component instance block behavior if used.
- Validation rules.
- Authorization and security.
- Field type rendering.
- Attribute value loading/saving.

If a detail block "looks wrong," distinguish between allowed configuration and unsupported layout customization. If all detail blocks changed, inspect shared detail components or styling; if one detail block changed, inspect that block's supplied metadata.

### List Blocks

List blocks usually display records for an entity and commonly use grids. The official docs call them mostly standard and "cookie cutter" for core development ([Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks)). That standardization is useful, but it can hide performance and security issues.

List block agents should inspect:

- The query source and whether it loads all rows.
- Grid row keys.
- Grid definition and actions.
- Attribute columns.
- Person fields.
- Security column behavior.
- Row-level edit/delete permissions.
- Whether bulk operations use selected row keys.
- Export behavior.
- Custom columns and whether the data source can support them.
- Person preferences for saved filters or date ranges.

When row counts are large, remember that standard Obsidian grid filtering and sorting happen in the browser after all data is sent ([Grids](https://community.rockrms.com/developer/obsidian/grids)). If performance is poor, do not only tune browser rendering; inspect server payload size, query shape, generated fields, dynamic attributes, and whether the block needs a server-side paging/filtering design.

### Custom Actions

`IHasCustomActions` is the replacement pattern for special configuration or administrate actions that need a custom Obsidian UI. The source pack's official page says to implement the interface and create a separate `.obs` file for the configuration screen ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions)).

Use custom actions for real block-specific configuration workflows. Do not use them as a general escape hatch for normal page actions. Normal user actions usually belong inside the block component or grid actions; administrate/configuration actions belong behind administrate permission checks.

### Person Preferences

The Creating Blocks documentation includes person preferences, preference providers, and preference collections ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). Agents should consider person preferences when UI state persists after clearing browser storage or using a different browser. If only one user sees an odd filter or date range, inspect person preferences.

## 9. Grid Reference Deep Dive

The Obsidian grid is powerful but easy to misuse. The grid documentation says it handles table display plus paging, filtering, exporting, and more, while also warning that client-side filtering and sorting require all data to be sent to the browser before rendering ([Grids](https://community.rockrms.com/developer/obsidian/grids)).

### Grid Architecture

A grid has several conceptual pieces:

- Data: row objects and possibly supporting metadata.
- Definition: field definitions, action URLs, and feature data ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid)).
- Columns: components that display row data.
- Filters: UI and matching logic for narrowing rows.
- Grid state: current sort, filters, selected rows, page, and action state.
- Actions: grid-level and row-level operations.
- Key fields: stable identifiers needed for advanced behavior.

The grid reference says `Data` is required and can be an object or a function returning data, including a promise. `Definition` contains grid definition information. `keyField` identifies each row and is not always required for display, but many advanced features need it. `personKeyField` identifies a person key when the grid represents person records ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid)).

### Standard Column Properties

Most columns share standard properties and templates. The Standard Columns page lists properties such as `name`, `title`, `field`, quick filter behavior, sort behavior, filter behavior, export behavior, visibility priority, classes, width, and templates ([Standard Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/standard-columns)). The exact property list should be verified against current docs or source, but the key operational idea is stable:

- `name` identifies the column.
- `title` displays in the header.
- `field` points to the row property.
- Quick filter, sort, filter, and export properties may override default behavior.
- Templates allow custom rendering.

When a grid displays correctly but exports or filters incorrectly, inspect export and quick-filter values. Display formatting is not automatically the same as sort/filter/export value.

### TextColumn

`TextColumn` displays a plain text string from a row field and provides defaults for formatting, skeleton display, and export ([TextColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/textcolumn)). Use it for ordinary text values where no special formatting or action is required.

Troubleshooting:

- Blank cell: inspect `field` name and row data.
- Filter mismatch: inspect quick filter value or column filter.
- Encoded HTML: do not switch to raw HTML casually; inspect whether the field type or release version handles HTML as intended. Release notes mention a v18.3 fix where Memo Fields configured to allow HTML displayed tags as encoded text in Obsidian blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### BooleanColumn

`BooleanColumn` displays a boolean true value as a checkmark and leaves false blank ([BooleanColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/booleancolumn)). Use it for simple true/false state, but confirm the row value is an actual boolean or consistently converted value. If the server sends `"True"`, `"False"`, `1`, `0`, or `null`, inspect how the column and row model handle conversion.

### DateColumn And DateTimeColumn

`DateColumn` displays a short date value ([DateColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/datecolumn)). `DateTimeColumn` displays short date and time and includes a `showSeconds` option for seconds ([DateTimeColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/datetimecolumn)). For agents, date troubleshooting requires checking:

- Server time zone.
- Browser locale.
- Serialized date format.
- Whether the value represents date-only or date-time.
- Whether sorting uses raw date or formatted text.
- Whether export should include local or server time.

### NumberColumn, CurrencyColumn, And NumberBadgeColumn

`NumberColumn` formats numeric values using the browser's current locale for separators ([NumberColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/numbercolumn)). `CurrencyColumn` formats values as currency ([CurrencyColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/currencycolumn)). `NumberBadgeColumn` displays a number inside a colored badge based on configured ranges ([NumberBadgeColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/numberbadgecolumn)).

Operational checks:

- Confirm numeric values are numbers, not strings with commas or currency symbols.
- Confirm null and empty values are expected.
- Confirm range boundaries for badge coloring.
- Confirm export uses numeric values where downstream Excel use matters.
- Confirm locale expectations if display differs by browser.

### LabelColumn

`LabelColumn` displays a pill label and can map values to text, CSS classes, or colors ([LabelColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/labelcolumn)). Use it for status values where color or style communicates category. Do not use it as the only status indicator if accessibility or export matters; ensure text remains meaningful without color.

Troubleshooting:

- Wrong label text: inspect `textSource` or row value.
- Wrong color: inspect `classSource` or `colorSource`.
- Sort order wrong: inspect sort value, not only displayed text.
- Export wrong: inspect export value.

### HighlightDetailColumn

`HighlightDetailColumn` displays a primary value in emphasis and optional detail text below it ([HighlightDetailColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/highlightdetailcolumn)). Use it when a list row needs a scan-friendly title plus secondary description, such as a name and description. If detail text is missing, inspect `detailField` and row data.

### PersonColumn

`PersonColumn` displays a cell as a person with standardized formatting options. The docs note that the field must be added with `.AddPersonField()` so the grid has all required values ([PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn)). This is a critical server/client contract. A client-only row object with just a name string is not enough for full person behavior.

Properties include behaviors around detail display, avatar visibility, last-name-first display, linking, and hover info, with version-specific mention of `alwaysShowAvatar` in v18.3 ([PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn)). If avatar behavior differs by version, inspect the target Rock version and current source.

### ButtonColumn, EditColumn, DeleteColumn, CopyColumn

`ButtonColumn` displays a single icon button and calls an action when clicked ([ButtonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/buttoncolumn)). `EditColumn` displays an edit button and can keep the button disabled while an async click handler resolves ([EditColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/editcolumn)). `DeleteColumn` displays a delete button, normally prompts for confirmation, and supports disabling confirmation or disabling per row ([DeleteColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/deletecolumn)). `CopyColumn` copies row-derived text to the browser clipboard ([CopyColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/copycolumn)).

Operational guardrails:

- Edit and delete click handlers must not be the only authorization layer.
- Delete should normally require confirmation unless a larger workflow already confirms.
- Row-disabled callbacks should reflect server authorization where possible.
- Copy values may contain sensitive tokens or URLs; confirm that copying is appropriate.
- Async handlers should handle errors and reset disabled/loading states.

### SelectColumn

`SelectColumn` displays checkboxes for selecting rows for bulk actions ([SelectColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/selectcolumn)). Bulk operations require stable row keys. If selected rows change after sorting/filtering, inspect `keyField` and row identity. Bulk actions must re-check server permission for every selected row.

### ReorderColumn

`ReorderColumn` supports drag-and-drop row ordering and calls `onOrderChanged` with the moved item and the item it was placed before, or null when dropped at the end ([ReorderColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/reordercolumn)). Agents should verify:

- The row list is already visually updated when the callback runs.
- Server persistence handles ordering safely.
- Concurrent reorders are handled or disallowed.
- The user has permission to reorder.
- The server saves the correct order field or relationship.
- A failed save rolls back or reloads the grid.

Because reorder often maps to SQL order fields or relationship ordering, do not infer persistence from UI movement.

### SecurityColumn

`SecurityColumn` opens the standard security editor modal for the row item ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)). It supports item title and disabled state. Use it when row items have securable entities and the current user may manage security. Verify that the row identifies the entity type and entity key the security editor needs. If the modal opens for the wrong item, inspect row data and item title/key mapping.

### AttributeColumns And RockFieldColumn

`AttributeColumns` is a placeholder that tells the grid where to place dynamic entity attribute columns ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns)). It does not behave like a normal single column. Use it when the server provides attribute field definitions and values.

`RockFieldColumn` displays a single Rock field value but is described as internal and not for plugin use ([RockFieldColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/rockfieldcolumn)). Agents working on plugins should avoid adopting internal-only columns unless current plugin guidance explicitly supports it.

### Generic Column

`Column` is the generic custom display option, with template-based formatting ([Column](https://community.rockrms.com/developer/obsidian/grid-reference/columns/column)). Use it when standard columns cannot express the display. Prefer standard columns for common data types because they already provide sorting, filtering, skeleton, export, and consistent visual behavior.

### Filters

The filter reference describes standard filters for boolean, date, number, text, and pick-existing values, and states that custom filters consist of a popup component that builds a filter value plus a row-matching function ([Filters](https://community.rockrms.com/developer/obsidian/grid-reference/filters)). Agents should always distinguish:

- Display value: what the user sees.
- Filter value: what the filter compares.
- Quick filter value: what global search uses.
- Sort value: what ordering uses.
- Export value: what leaves Rock.

A custom display template does not automatically produce correct filter/sort/export behavior.

## 10. Field Types Deep Dive

Field types are one of the highest-risk Obsidian areas because they sit between stored values, configuration, multiple UI frameworks, filtering, reporting, and attributes.

The Creating Field Types documentation says field types provide four high-level functions: viewing, editing, filtering, and configuring behavior ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)). It also warns that the documentation is work in progress and not final truth. Treat field type work as source-first.

### Field Type Responsibilities

A field type should answer:

- How is the stored value converted into display text?
- How is the value edited?
- How is the value filtered?
- How is the field configured?
- Which configuration values are public to the browser?
- Which configuration values remain private/server-side?
- How are stored values serialized?
- How are empty, null, and invalid values handled?

In Obsidian, field type TypeScript handlers commonly extend a base field type, return edit/configuration components, and convert stored string values into browser-usable values. Source snippets show patterns such as `getTextValue`, `getEditComponent`, `getConfigurationComponent`, `ConfigurationKey`, lazy-loaded components, JSON parsing, and conversion helpers ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

### Universal Field Types

Universal Field Types were introduced to reduce framework coupling. The official docs say legacy field types are tightly integrated with WebForms, and Universal Field Types remove UI functionality from the C# field type so it can work across UI frameworks and platforms ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types)).

Agent guidance:

- Prefer Universal Field Type patterns for new plugin work when current Rock version supports them.
- Do not put browser UI assumptions into C# field type logic.
- Treat C# as data/configuration/logic and TypeScript as UI rendering.
- Validate configuration values on the server even if the Obsidian component restricts choices.
- Check release notes for Universal Field Type fixes before diagnosing custom code. v18.1 fixed some configuration settings edited inside Obsidian blocks storing raw JSON ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Core Field Type Patterns

The Core Field Type Patterns page says its content is mainly relevant to core team custom field types and that plugins and new core field types should use Universal Field Type patterns where possible ([Core Field Type Patterns](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns)). Use this page to understand existing core code, not as default plugin architecture.

Core patterns include:

- Edit component receives current value and configuration values.
- Component converts string values to useful browser types.
- Component watches incoming props and updates internal state.
- Configuration component emits updated configuration dictionaries.
- Some configuration changes require server updates.
- Configuration properties may drive dependent options.

Source snippets for `assessmentTypesFieldComponents.ts` illustrate these ideas: configuration values are converted to booleans and numbers, watchers synchronize props into internal refs, and `update:modelValue` emits a changed dictionary only when values actually change ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). That pattern prevents unnecessary updates and reduces accidental postbacks or save churn.

### Converting Core Field Types

The Converting Core Field Types page is a step-by-step guide for building an Obsidian field type and references tasks such as enabling support, creating the Obsidian field type, converting values for database/client, testing, and adding to the field type gallery ([Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types)). For agents, the key takeaway is that field type conversion involves multiple files. Do not patch only a component and assume the field type is complete.

Conversion inspection checklist:

- C# field type supports Obsidian or Universal behavior.
- TypeScript field type handler exists.
- Edit component exists if users can edit values.
- Configuration component exists if behavior can be configured.
- Filter behavior exists if the field participates in grids/reporting.
- Value conversion works both database-to-client and client-to-database.
- Field Type Gallery includes a test/demo if core contribution requires it.
- Tests cover empty, null, invalid, default, and configured values.

### Field Type Gallery

Source snippets include `Rock.JavaScript.Obsidian.Blocks/src/Example/FieldTypeGallery/types.partial.ts` and `utils.partial.ts`, where field components contain a name, initial value, field type GUID, and configuration values, and helper logic builds `PublicAttributeBag` structures ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). The gallery is useful because it exercises field types in a controlled UI. If a field type works in one custom block but not in the gallery, inspect the block. If it fails in the gallery too, inspect the field type implementation.

### Configuration Values

Field type configuration values often cross the browser boundary as strings. The field type docs distinguish configuration values and public/private behavior ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)). Source snippets show configuration dictionaries where keys map to string values such as `"True"`, `"False"`, empty strings, numeric strings, or JSON strings ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

Agent checks:

- Is the value stored as a string?
- Does TypeScript convert to boolean/number/object before use?
- Does TypeScript convert back to the expected string representation before emit?
- Are missing values defaulted correctly?
- Are private configuration values withheld from the browser?
- Does the server understand the emitted value shape?

### Common Field Type Failure Modes

Field does not render:

- Inspect whether an Obsidian edit/view component exists.
- Inspect component lazy import path.
- Inspect generated bundle/build.
- Inspect browser console for component import failure.
- Inspect field type GUID and registration.

Field renders but saves wrong value:

- Inspect `modelValue` watch logic.
- Inspect conversion from internal object to stored string.
- Inspect server-side validation and value normalization.
- Inspect whether empty string, null, and undefined are handled differently.

Configuration UI saves but has no effect:

- Inspect emitted `update:modelValue`.
- Inspect configuration key names.
- Inspect block or attribute value persistence.
- Inspect whether the component reads `configurationValues` or `configurationProperties`.
- Inspect server cache.

Picker does not show searchable enhanced mode:

- Compare with v18.3 release note fixing Single-Select Defined Value attributes with "Enhanced for Long Lists" in Obsidian blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Inspect the field type's enhancement configuration.
- Inspect picker props.

Memo HTML displays encoded tags:

- Compare with v18.3 release note fixing Memo Fields configured to allow HTML in Obsidian blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Inspect field configuration and sanitization expectations.
- Do not render raw HTML without confirming intended security behavior.

Note Type picker missing in an Obsidian block:

- Compare with v16.1 release note fixing Note Type Field Type in Following Event Type Detail Obsidian block ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Inspect field type support and block-specific field inclusion.

## 11. Development Environment Deep Dive

The Core Development Environment page says VS Code provides a rich development experience for Obsidian even though the whole Rock solution is not worked on there; `Rock.code-workspace` in the repository root acts roughly like a workspace file for the Obsidian projects ([Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment)). The same docs discuss building and Visual Studio 2019/2022 for the broader solution.

### Core Development Setup

For core development, expect a two-editor workflow:

- Visual Studio handles the C# solution and server debugging.
- VS Code handles Obsidian TypeScript projects, workspace configuration, linting, and browser debugging.
- `Rock.code-workspace` should be opened in VS Code so debugger and project settings are available ([Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code)).
- TypeScript project references connect block areas to framework projects, as shown in source snippets for area `tsconfig.json` files ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

Agents should inspect the exact repository instructions before issuing build commands. This guide does not assume a specific local build command because the source pack does not include the full build docs.

### VS Code Debugging

The debugging page explains that VS Code can attach debugging tools to Obsidian code and that the Rock workspace includes debugger configurations ([Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code)). It also describes setting up Chrome for remote debugging.

Operational debugging workflow:

1. Open the correct Rock workspace.
2. Start or attach the Rock web application in development.
3. Launch Chrome with remote debugging configured as required by the workspace.
4. Start the appropriate VS Code debug configuration.
5. Set breakpoints in the `.obs` or TypeScript files.
6. Reproduce the browser action.
7. Inspect props, emitted events, block action payloads, and component state.
8. Use browser network tools for server action responses.
9. Use server debugger/logs for C# action behavior.

If breakpoints do not bind, inspect source maps, build output, workspace path mapping, and whether the browser loaded a cached bundle.

### Plugin Development Setup

The Plugin Development page says `rock-dev-tool` drives plugin development and reduces setup time, while warning that not all referenced Rock versions may be available and pointing developers to package versions for availability checks ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)). It covers directory structure, installing the tool, creating environments, creating plugins, converting repositories, special considerations, WebForms blocks, HTTP handlers, building Obsidian, supported files, partial files, library files, code generation, packaging, importing packages, and pre-release changes.

Agent guidance for plugin work:

- Verify the plugin's target Rock version before generating or packaging.
- Verify whether the plugin uses Obsidian, WebForms, or both.
- Keep namespaces, paths, and build config plugin-specific.
- Do not assume core-only code generator features work for plugins.
- Confirm package import behavior in a development Rock instance before advising production deployment.
- Inspect generated files rather than relying on memory of older `rock-dev-tool` output.

### File Types And Naming

Obsidian uses `.obs` files instead of a framework-standard extension. The UI control docs say this file extension is intentional and allows Rock to change the underlying framework later without renaming files ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)). This is why editor configuration matters.

The App Laws page provides naming conventions: type names in PascalCase, interfaces prefixed with `I`, functions and variables/properties in camelCase, filenames in `camelCase.ts`, and directory names in PascalCase ([App Laws](https://community.rockrms.com/developer/obsidian/app-laws)). Agents should follow local source patterns and current lint rules.

### Build And Type Checking

Source snippets show TypeScript project references from block areas into Obsidian framework projects ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). That implies changes in shared controls or field types can affect many block areas. When modifying framework code, run the relevant TypeScript build, lint, and tests for the touched area and at least one consumer block area. When modifying one block component, run the block area's build and any tests available for that block.

If the source pack is thin for a build command, inspect the repository's package scripts, workspace file, and CI definitions in the live checkout.

## 12. Related Rock Areas: Developer Resources, Api Integrations, Security, Cms, Platform Configuration, Workflows

### Developer Resources

Obsidian lives under Rock Developer Resources. The official developer docs include pages for component structure, app laws, forms, blocks, UI controls, field types, browser bus, caching API calls, grids, and grid reference ([Obsidian](https://community.rockrms.com/developer/obsidian)). Agents doing Rock development should treat those pages as the conceptual index, then move to source code for exact implementation.

### API Integrations

Block actions are not general public REST APIs, but they behave like a block-scoped API between browser and server. The broader Rock API docs distinguish API v1 as legacy and API v2 as newer/faster, and point to shared API resources ([API Documentation](https://community.rockrms.com/api-docs)). For integrations, decide whether the work belongs in:

- A block action for page-specific interaction.
- A Rock REST API endpoint for external integration.
- Lava API for controlled Lava-driven data exposure.
- A server job or workflow action for backend automation.
- A plugin API endpoint.

Do not expose sensitive operations through a browser block action just because the UI needs them. The server action remains reachable by authenticated users who can load the block, so authorization and input validation are mandatory.

### Security

Security intersects Obsidian at every layer:

- Page and block view permissions.
- Block administrate permissions.
- Entity authorization.
- Security grants to controls.
- Security editor modals via `SecurityColumn`.
- API/block action authorization.
- Field type configuration privacy.
- Route and identifier safety.
- Release-note security changes.

The UI control docs discuss security grants for controls needing controlled access to entities or entity types ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)). `SecurityColumn` exposes a standard security editor button for grid rows ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)). Release notes also show workflow type view permission hardening and registration template security changes in recent releases ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent guardrail: never treat "button hidden" as security. Hidden buttons improve UX; server actions enforce security.

### CMS

Obsidian blocks live on Rock pages and therefore participate in CMS concerns: sites, layouts, pages, routes, zones, block placement, themes, assets, and Lava. Release notes include CMS-related Obsidian fixes such as Signature Document List display and Signature Document Template Detail PDF viewer additions ([Rock Core Release Notes](https://www.rockrms.com/releasenotes), [GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)).

When troubleshooting CMS-adjacent Obsidian behavior, inspect:

- Site theme and scripts.
- Page route and parameters.
- Page-level Lava.
- Block placement and zone.
- Asset paths and file access.
- Browser cache and bundle URL.
- Whether the page is internal or external site.

### Platform Configuration

Obsidian behavior can be affected by platform settings such as predictive IDs, security settings, field type configuration, defined types, system communications, asset storage, and caching. The release note for Group Attendance Detail and Predictive IDs is a concrete example ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agents should inspect system settings when a block behaves differently across sites or environments.

### Workflows

Workflows use field types, forms, Lava, security, and entity relationships, so Obsidian workflow blocks can surface many framework issues. Release notes include a v19.1 fix for Obsidian Workflow List timing out when loading workflows assigned to groups with many members ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). They also reference Workflow Entry in the Defined Value picker enhanced list fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

For workflow-related Obsidian issues, inspect:

- Workflow type security.
- Workflow attribute field types.
- Assigned groups and member counts.
- Block filters.
- Lava in workflow actions.
- User permissions.
- Version-specific fixes.

## 13. Administration And Operational Guardrails

### Version First

Always record the Rock version before diagnosing an Obsidian issue. The source pack shows Obsidian-related fixes in v16.1, v17.1, v18.1, v18.2, v18.3, and v19.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Symptoms can be version bugs, not local configuration mistakes.

Minimum version checks:

- Core version.
- Target module version if release notes separate module behavior.
- Whether the target release is general, beta, or pre-alpha.
- Whether a fix exists in a later release.
- Whether a plugin targets a specific Rock package version.

### Security First

For any mutating Obsidian work, verify:

- Page authorization.
- Block authorization.
- Entity authorization.
- Block action authorization.
- Security grants.
- Whether the browser receives private configuration.
- Whether route IDs are guessable or protected.
- Whether Predictive IDs are enabled or disabled when relevant.

### Payload Size And Grid Performance

Because standard Obsidian grids sort and filter client-side, row count matters ([Grids](https://community.rockrms.com/developer/obsidian/grids)). Agents should treat grids with thousands of rows as performance-sensitive.

Operational checks:

- How many rows are returned?
- How many columns and dynamic attributes are included?
- Are person fields adding large nested data?
- Are custom columns forcing expensive server joins?
- Is export enabled for large sets?
- Are filters client-side only?
- Is a server-side query design needed?

The Communication List block's high-performance query disabling custom columns is a useful warning that performance-specific list blocks may not support every grid customization ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Configuration Hygiene

Use consistent key names. In TypeScript field type source, configuration keys are often centralized in a `ConfigurationKey` enum or const enum ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). Follow that pattern. Avoid string literals spread across components.

When configuration saves incorrectly:

- Inspect raw stored value.
- Inspect emitted dictionary.
- Inspect server conversion.
- Inspect version-specific field type fixes.
- Inspect whether the component is using `null`, `undefined`, or empty string differently.

### Lava Guardrails

Lava in Obsidian has limits. Lava operations that try to alter the HTTP response, such as redirects or meta tags, may not work from Obsidian actions because the page response has already been sent ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)). Agents should recommend Obsidian-native navigation or server action responses rather than response-mutating Lava when working inside an Obsidian interaction.

### Admin UI Expectations

Obsidian should usually behave like modern Rock admin UI:

- Clear loading states.
- Clear empty states.
- Clear validation messages.
- Disabled actions while promises resolve.
- View-only mode where users can inspect but not mutate.
- Consistent detail block layout.
- Consistent grid column behavior.
- Confirmation for destructive actions.

Use `RockForm`, `RockFormField`, and standard input components for form behavior where possible ([Form Validation](https://community.rockrms.com/developer/obsidian/form-validation)).

## 14. Developer, API, Lava, And Source-Code Landmarks

Use these landmarks when navigating Obsidian work.

Official developer documentation:

- Obsidian index: [Obsidian](https://community.rockrms.com/developer/obsidian)
- Core development environment: [Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment)
- VS Code debugging: [Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code)
- Plugin development: [Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)
- Null and undefined: [Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined)
- Component structure: [Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure)
- Form validation: [Form Validation](https://community.rockrms.com/developer/obsidian/form-validation)
- Blocks: [Blocks](https://community.rockrms.com/developer/obsidian/blocks)
- Creating blocks: [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)
- Detail blocks: [Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)
- List blocks: [Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks)
- Custom administrate actions: [Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions)
- UI controls: [Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)
- Field types: [Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)
- Core field type patterns: [Core Field Type Patterns](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns)
- Converting field types: [Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types)
- Universal field types: [Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types)
- Browser bus: [Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)
- Caching API calls: [Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls)
- Grids: [Grids](https://community.rockrms.com/developer/obsidian/grids)
- Grid reference: [Grid Reference](https://community.rockrms.com/developer/obsidian/grid-reference)
- Grid properties: [Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid)
- Columns: [Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns)
- Filters: [Filters](https://community.rockrms.com/developer/obsidian/grid-reference/filters)
- Misc notes: [Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes)
- App laws: [App Laws](https://community.rockrms.com/developer/obsidian/app-laws)

Source-code repository:

- Rock source repository: [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)
- Example list block reference mentioned by docs: [ObsidianGalleryList](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Example/ObsidianGalleryList.cs)
- Field type examples in `Rock.JavaScript.Obsidian/Framework/FieldTypes`, including security role, block template, address, assessment types, asset, and picker-backed fields ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
- Example field type gallery files in `Rock.JavaScript.Obsidian.Blocks/src/Example/FieldTypeGallery` ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
- Area TypeScript references in `Rock.JavaScript.Obsidian.Blocks/src/<Area>/tsconfig.json` ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

API and Lava:

- API docs: [API Documentation](https://community.rockrms.com/api-docs)
- Lava with Obsidian: [Lava With Obsidian](https://community.rockrms.com/lava/obsidian)

Release and model metadata:

- Release notes: [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Model Map: [Model Map](https://community.rockrms.com/ModelMap)

## 15. Reporting, Analytics, And Model Map

Obsidian itself is not primarily a reporting engine, but it interacts with reporting through grids, filters, field types, exports, model metadata, and dynamic attributes.

### Grid Reporting Behavior

A grid can behave like a lightweight reporting surface because users can filter, sort, page, select, and export. However, because the standard grid does client-side filtering and sorting, it is not a substitute for server-side reporting over large datasets ([Grids](https://community.rockrms.com/developer/obsidian/grids)).

Use grids for operational list views when:

- Row count is bounded.
- Data can be safely sent to the browser.
- Filters are simple.
- Export size is reasonable.
- Users need interactive sorting and quick filtering.

Use server-side reports, data views, SQL-backed blocks, or specialized queries when:

- Row count is high.
- Data is sensitive and should not all be sent to browser.
- Filters are complex or permission-dependent.
- Export must reflect server-side paging/filtering.
- Query performance requires indexes or aggregation.

### Field Types And Filtering

Field types define filtering behavior ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)). For reporting or grid filters, inspect the field type's filter implementation, not only the displayed edit component. A field type may display nicely but fail to filter if it lacks a filter component or row matching function.

### Model Map Use

The source pack's Model Map record identifies Field Type as a Core model ([Model Map](https://community.rockrms.com/ModelMap)). Use Model Map as an orientation layer when an agent needs to understand where a concept belongs in Rock's entity system. Then verify:

- Actual model class in source.
- Database table and columns.
- EntityType registration.
- Attribute relationships.
- Security support.
- REST API exposure if needed.

### Export Caveats

Release notes include a fix for Obsidian grid exports failing when export titles contained Excel-invalid worksheet characters or exceeded Excel worksheet name length ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If export fails, inspect:

- Export title.
- Column export values.
- Special characters.
- Hidden or dynamic columns.
- Field types returning objects instead of scalar text.
- Browser console and server logs.
- Rock version.

## 16. Version And Release Caveats

Obsidian is actively evolving. The source pack includes release notes and partner spotlight records across v16 through v19. Use release notes as diagnostic input, not trivia.

Notable caveats from the source pack:

- v16.1 fixed Note Type Field Type not showing in the Following Event Type Detail Obsidian block ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v16.7 added a PDF viewer to the Obsidian Signature Document Template Detail block, according to the GitHub Spotlight record ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)).
- v16.10 included fixes to Obsidian Registration Entry payment plan behavior and Assessment Type Detail editing of Valid Duration in a community spotlight summary ([GitHub Spotlight 12/6/2024](https://www.triumph.tech/resources/github-spotlight-1262024)).
- v17.1 added an Obsidian Communication Template Detail block for viewing and editing communication templates and laying groundwork for versioned templates ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v17.2/v18.0 spotlight records mention an Obsidian Communication List block with enhanced status display and improved data loading ([GitHub Spotlight 7/18/2025](https://www.triumph.tech/resources/github-spotlight-7182025)).
- v17.4 spotlight records mention Device List filtering and a Communication Entry Wizard justify-text fix ([GitHub Spotlight 8/7/2025](https://www.triumph.tech/resources/github-spotlight-872025)).
- v18.1 added Obsidian Communication Detail and Communication List blocks, disabled unsupported custom columns in the high-performance Communication List query, and fixed Universal field type configuration editing from Obsidian blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v18.2 fixed Signature Document List display and newly added Obsidian block types failing to appear in Page Zone Editor after startup ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v18.3 fixed Memo Field HTML rendering, enhanced long-list Defined Value picker behavior in Obsidian blocks, Location Detail self/child parent saves, Group Requirement Type attribute value loading/saving, Group Attendance Detail behavior when Predictive IDs are disabled, and other Obsidian-adjacent issues ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v19.1 fixed Workflow List timeout behavior for workflows assigned to groups with many members ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

When a user reports an issue, do not stop at "fixed in later version." Provide a practical branch:

- If the instance is below the fixed version, recommend upgrade path or workaround verification.
- If the instance is at or above the fixed version, inspect local configuration, plugin override, cache, custom block code, and data.
- If the release note references a GitHub issue, inspect the issue and commit for exact scope when available.
- If the instance is on beta or pre-alpha, check whether behavior changed again in later releases.

## 17. Implementation Playbooks

### Playbook: Create A Safe Obsidian List Block

Use when building a new administrative list.

1. Define the entity and purpose.
2. Confirm row count expectations.
3. Decide whether client-side grid behavior is acceptable.
4. Create or inspect C# list block.
5. Build a minimal row bag, not a full entity dump.
6. Include a stable row key.
7. Add standard columns first.
8. Add specialized columns only where their server data requirements are met.
9. Add filters intentionally.
10. Add actions with server permission checks.
11. Add empty/loading/error states.
12. Test with no rows, one row, many rows, unauthorized user, view-only user, and admin user.
13. Test sorting, filtering, export, and bulk actions.
14. Compare against release notes for grid or field type bugs.

Use the grid docs and reference pages for row data, definition, columns, and filters ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid), [Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns), [Filters](https://community.rockrms.com/developer/obsidian/grid-reference/filters)).

### Playbook: Add A Person Column Correctly

Use when a list needs a person cell.

1. On the server, add the person field with the expected helper, such as `.AddPersonField()` as documented for `PersonColumn`.
2. Confirm row data includes all values required by the person display.
3. In the component, use `PersonColumn` with field name, optional detail field, link behavior, avatar behavior, and hover behavior.
4. Test with missing photo, deceased/inactive statuses if relevant, privacy restrictions, and users without access to profile.
5. Verify sort/export values.

Do not send a plain full name string and expect full `PersonColumn` behavior ([PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn)).

### Playbook: Add Dynamic Attribute Columns

Use when a list needs entity attributes.

1. Confirm the entity supports attributes.
2. Load attribute definitions the current user may view.
3. Include `AttributeFieldDefinitionBag[]` or current equivalent in the server data.
4. Add row values for each attribute.
5. Place `AttributeColumns` where dynamic columns should appear.
6. Verify filter behavior for each attribute field type.
7. Verify export behavior.
8. Test attributes with empty values, private values, HTML values, picker values, and large text.

Use `AttributeColumns` for dynamic columns and avoid internal-only `RockFieldColumn` in plugin work unless current docs permit it ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns), [RockFieldColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/rockfieldcolumn)).

### Playbook: Build A Field Type Edit Component

Use when implementing or converting a field type.

1. Identify stored value format.
2. Identify display text behavior.
3. Identify edit control.
4. Identify configuration values.
5. Identify filter behavior.
6. Create or update TypeScript field type handler extending the local base pattern.
7. Lazy-load large edit/configuration components when consistent with source patterns.
8. Convert string configuration values to proper browser types.
9. Watch incoming `modelValue` and configuration props.
10. Emit normalized values.
11. Test null, empty, invalid, and configured values.
12. Add gallery coverage if required for core work.

Use field type docs for conceptual responsibilities and source files for exact current patterns ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types), [Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types), [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

### Playbook: Diagnose A Broken Picker

1. Identify whether the picker is a standard control, field type edit component, or custom component.
2. Inspect configuration values.
3. Inspect required rule and `showBlankItem` behavior; the Misc Notes page says these two settings interact for picker requiredness and deselection ([Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes)).
4. Inspect item source: defined values, entity query, API call, or configuration property.
5. Inspect security grants if the picker reads protected data.
6. Inspect enhanced/long-list configuration.
7. Compare with release notes for picker fixes, especially Defined Value enhanced list behavior in v18.3 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
8. Test required, optional, deselect, preselected value, inactive value, and unauthorized value cases.

### Playbook: Add Browser Bus Interaction

Use browser bus only for page-local communication. The Browser Bus docs state it is a single-page pub-sub interface, built around `document.addEventListener()` and `document.dispatchEvent()` with the event name `rockMessage`, and does not communicate across tabs or browsers ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)).

Steps:

1. Define a message name with a specific purpose.
2. Decide payload shape.
3. Subscribe in components that need to react.
4. Unsubscribe on component cleanup if the API requires it.
5. Publish after the relevant action.
6. Avoid using browser bus for security-sensitive enforcement.
7. Avoid using browser bus where parent/child props and emits are clearer.
8. Test multiple block instances on the same page.

### Playbook: Cache Repeated API Calls

The Caching API Calls page describes the problem of multiple identical controls eagerly making the same async API call, and the need for both promise-level in-memory caching while a request is pending and storage after results return ([Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls)).

Use this pattern when:

- Multiple instances of a control request identical reference data.
- The data is safe to cache client-side.
- Staleness is acceptable or bounded.
- The request is expensive enough to matter.

Verify:

- Cache key includes all parameters that affect results.
- Pending promise is shared.
- Failed promise does not poison cache permanently.
- Security context is included or the data is public to the current user.
- Cache invalidation exists if data can change during the session.

## 18. Troubleshooting Decision Tree

### Symptom: Block Does Not Appear In Page Zone Editor

Check Rock version. v18.2 fixed newly added Obsidian block types failing to appear after initial startup ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Then inspect:

- Block Type registration.
- C# class and assembly.
- Component file path.
- Category.
- Cache state.
- Server restart.
- Build/deploy output.
- Plugin package import.
- Whether the block is internal/core-only.

### Symptom: Block Renders Blank

Inspect:

- Browser console errors.
- Network requests for JS bundles and component files.
- Server logs.
- Block action initialization response.
- Missing required props.
- Null vs undefined data shape ([Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined)).
- Component import paths.
- TypeScript build output.
- User permissions.
- Entity route parameter.

### Symptom: Save Button Does Nothing

Inspect:

- Browser click handler.
- Form validation state.
- `RockForm` and field validation errors ([Form Validation](https://community.rockrms.com/developer/obsidian/form-validation)).
- Disabled/loading state.
- Network request.
- Block action registration.
- Server authorization.
- Server validation response.
- Console promise rejection.

### Symptom: Save Succeeds But Data Does Not Change

Inspect:

- Server action result.
- Database/entity value.
- Attribute value storage.
- Cache.
- Component state update.
- Whether save response returns new data.
- Whether page reload shows updated data.
- Configuration key mismatch.
- Version-specific field type configuration fixes.

### Symptom: Grid Is Slow

Inspect:

- Row count.
- Payload size.
- Dynamic attributes.
- Person fields.
- Custom columns.
- Client-side filtering/sorting assumption ([Grids](https://community.rockrms.com/developer/obsidian/grids)).
- Server query.
- Browser render time.
- Export settings.
- Whether server-side paging/filtering is needed.

### Symptom: Grid Sort Duplicates Or Moves Wrong Rows

Inspect:

- `keyField`.
- Unique row keys.
- Row object identity.
- Sort value.
- Grid state.
- Release notes for Dynamic Data unique key fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Symptom: Grid Export Fails

Inspect:

- Export title and Excel worksheet restrictions.
- Rock version; release notes include a fix for invalid Excel worksheet names in Obsidian grid exports ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Column export values.
- Dynamic columns.
- Field type values.
- Browser download errors.
- Server logs.

### Symptom: Field Type Displays Raw JSON

Inspect:

- Field type display conversion.
- Universal Field Type configuration.
- Whether the stored value is expected JSON.
- v18.1 Universal field type configuration fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- TypeScript `getTextValue`.
- Configuration component emits.

### Symptom: Picker Cannot Be Cleared

Inspect:

- Required rule.
- `showBlankItem`.
- Misc Notes guidance on picker requiredness and deselection ([Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes)).
- Field type configuration.
- Component props.
- Server validation.

### Symptom: Lava Redirect Or Meta Tag Does Not Work

If the operation happens inside an Obsidian interaction, inspect whether the page response has already been sent. The Lava docs say response-mutating filters such as redirects and meta tags are often unsupported in Obsidian blocks because actions do not reload the whole page ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).

Use Obsidian navigation or explicit client-side response handling instead.

### Symptom: Security Modal Opens But User Cannot Save

Inspect:

- Current user's Administrate/Edit permission.
- Entity security.
- Block security.
- `SecurityColumn` disabled field.
- Security grants.
- Server logs.
- Whether the row maps to the correct entity ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)).

### Symptom: Works For Admin But Not Staff

Inspect:

- Page View permission.
- Block View/Edit/Administrate.
- Entity authorization.
- Field-level security.
- Security grants.
- API/block action permission.
- Workflow type permissions if workflow-related.
- Whether the UI hides actions or server rejects them.

## 19. Agent Task Recipes

### Recipe: Identify The Source Files Behind A Visible Obsidian Block

1. Record page URL, block name, and visible UI text.
2. In Rock admin, inspect the page's block instance and Block Type.
3. Record C# block class, category, and component path.
4. Find the C# block under `Rock.Blocks` or plugin block path.
5. Find the `.obs` component under `Rock.JavaScript.Obsidian.Blocks/src/...` or plugin Obsidian path.
6. Find generated view model bags referenced by imports.
7. Inspect block actions.
8. Inspect block attributes and custom actions.
9. Compare target version with release notes.

### Recipe: Determine Whether A Bug Is Version-Related

1. Record exact Rock version.
2. Search release notes for block name, field type, grid, module, and symptom.
3. If a later release fixes it, inspect whether the fix applies exactly.
4. If the instance is below the fix, recommend upgrade or targeted workaround.
5. If the instance includes the fix, inspect custom overrides, plugin code, cache, data, and configuration.
6. If the release note is vague, inspect linked GitHub issue or source diff when available.

Use official release notes as the first release source ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Recipe: Review An Obsidian Pull Request

Focus on defects:

- Does every block action validate authorization?
- Does the browser receive only necessary data?
- Are null/undefined/empty states handled?
- Are field type configuration values normalized?
- Does the grid have stable keys?
- Is client-side grid row count acceptable?
- Are filters/sort/export values correct?
- Are destructive actions confirmed?
- Are async buttons disabled while pending?
- Are standard controls used instead of custom UI where appropriate?
- Are plugin paths and core paths kept separate?
- Are release caveats considered?
- Are tests or gallery coverage included for field types?

### Recipe: Audit A Block For Security

1. Identify all block actions.
2. For each action, identify data read/write scope.
3. Confirm server-side authorization.
4. Confirm entity-level authorization.
5. Confirm page/block permissions.
6. Inspect security grants.
7. Inspect whether private configuration values are sent to browser.
8. Inspect route parameters and entity identifiers.
9. Test as admin, staff, view-only, and unauthorized user.
10. Confirm hidden buttons are not the only protection.

### Recipe: Audit A Grid For Operational Readiness

1. Count expected rows.
2. Estimate payload size.
3. Confirm `keyField`.
4. Confirm row fields match columns.
5. Confirm quick filter values.
6. Confirm sort values.
7. Confirm export values.
8. Confirm dynamic attributes.
9. Confirm person fields are added server-side when using `PersonColumn`.
10. Confirm permissions for edit/delete/security/reorder.
11. Test export title and invalid characters.
12. Test large row count in a realistic browser.

### Recipe: Decide Whether To Use Browser Bus

Use browser bus when:

- Two independent components on the same page must communicate.
- Parent/child props are not a natural fit.
- The message is page-local.
- The interaction is not security enforcement.

Do not use browser bus when:

- A server action should own the state.
- Components have a clear parent/child relationship.
- The message must cross browser tabs.
- The message must persist.
- The message controls authorization.

The browser bus is page-local only ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

This guide synthesizes the provided source pack. The strongest sources are the official Obsidian developer pages, Rock release notes, and source-code snippets from `SparkDevNetwork/Rock`.

Primary dependencies:

- Obsidian depends on Developer Resources for core docs and conventions ([Obsidian](https://community.rockrms.com/developer/obsidian)).
- Blocks depend on server-side C# block logic, TypeScript components, block actions, generated bags, security, and page/block configuration ([Blocks](https://community.rockrms.com/developer/obsidian/blocks), [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).
- Detail blocks depend on standardized detail layout and developer-supplied labels, badges, actions, and entity data ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)).
- List blocks depend on grids, row keys, column definitions, filters, actions, and performance-aware data loading ([Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks), [Grids](https://community.rockrms.com/developer/obsidian/grids)).
- Grids depend on `Data`, `Definition`, key fields, columns, filters, grid state, and browser-side processing ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid), [Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns), [Filters](https://community.rockrms.com/developer/obsidian/grid-reference/filters)).
- Field types depend on stored values, configuration values, C# field type behavior, TypeScript handlers, edit/configuration components, filtering behavior, and public/private configuration rules ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types), [Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types)).
- UI controls depend on `.obs` files, framework controls, security grants, and correct development environment support ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)).
- Forms depend on `RockForm`, `RockFormField`, input components, validation rules, and component-owned validation display ([Form Validation](https://community.rockrms.com/developer/obsidian/form-validation)).
- Browser messaging depends on the page-local browser bus and should not be treated as cross-tab or server communication ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)).
- Lava depends on page response timing; response-mutating Lava behavior may not work after Obsidian interactions ([Lava With Obsidian](https://community.rockrms.com/lava/obsidian)).
- Plugin work depends on `rock-dev-tool`, target Rock package versions, plugin-specific paths, packaging, and import behavior ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)).
- Version behavior depends on release notes and should be verified against the target instance ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Thin or verification-required areas:

- The source pack does not provide full C# source snippets for block base classes, block action attributes, grid builder APIs, security grant APIs, or generated bag classes. Inspect the target Rock source branch before writing exact code.
- The source pack does not provide full Model Map details for Block, BlockType, Page, Attribute, AttributeValue, or FieldType relationships. Inspect the target database schema, model classes, and Model Map before making schema claims.
- The source pack does not provide current `rock-dev-tool` command output. Verify installed tool version and target package availability before giving exact plugin commands.
- The source pack provides bounded excerpts, not full documentation pages. For implementation, open the official docs and source files on the current branch.
- Release records in this pack include compact summaries. For high-risk fixes, inspect linked issues and commits where available.

The safest agent posture is source-first, version-aware, and permission-aware: identify the block, inspect the server and client contracts, verify configuration and security in the live instance, compare with release notes, and only then recommend or implement a change.
