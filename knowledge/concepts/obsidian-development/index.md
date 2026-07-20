---
id: concept-obsidian-development
title: Obsidian Development
generated: true
last_built: 2026-07-20T05:21:56+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - developer-resources
  - api-integrations
  - security
  - cms
  - platform-configuration
  - workflows
---

# Obsidian Development

Obsidian block development, grid reference, custom actions, field types, browser bus, TypeScript patterns, development environment, and migration from WebForms blocks.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.

## How To Think About This Area

- `Obsidian Development` spans developer-resources, api-integrations, security, cms, platform-configuration, workflows. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_developer, rock_lava_docs, rock_core_release_notes, rock_model_map, triumph_resources, sparkdevnetwork_rock.
- Related tags found in source records: development, api, lava, obsidian, operations, releases, sql, model-map.
- Source detail types include: developer_doc, rock_lava_docs, triumph_resources.

## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | An Obsidian grid CopyColumn renders a button that copies text to the browser clipboard; it uses the row value identified by the column's field setting unless valueToCopy is supplied to compute the text from the row, column definition, and grid state. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/copycolumn) |
| official | behavior | In an Obsidian grid, SelectColumn renders row-selection checkboxes that allow grid actions to operate on multiple selected rows. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/selectcolumn) |
| official | behavior | In an Obsidian grid, DateColumn renders the value of its configured field as a short-form date and supplies defaults for formatting, skeleton display, quick-filter values, and exported values; it adds no column-specific properties. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/datecolumn) |
| official | behavior | The Obsidian Browser Bus is a page-local publish-subscribe mechanism backed by DOM events; its messages do not cross browser tabs or reach another user's browser. | [source](https://community.rockrms.com/developer/obsidian/browser-bus) |
| official | behavior | For an Obsidian plugin, `npm run build` performs TypeScript type checking before compiling and copying assets to RockWeb, whereas `npm run watch` continuously recompiles changed files without type checking. | [source](https://community.rockrms.com/developer/obsidian/plugin-development) |
| official | behavior | Obsidian block clients exchange JSON data with their C# server component and invoke block actions through endpoints that retain the block's settings and normal security enforcement. | [source](https://community.rockrms.com/developer/obsidian/blocks) |
| official | behavior | When NumberBadgeColumn ranges overlap, the effective precedence from highest to lowest is danger, warning, success, info, then hidden; therefore a matching color range can override a configured hide range. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/numberbadgecolumn) |
| official | behavior | The Obsidian grid SecurityColumn displays a per-row control that opens Rock's standard security editor for the corresponding item. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn) |
| official | behavior | The Obsidian grid EditColumn invokes its optional click callback with the row key; the callback may be synchronous or return a Promise, in which case the edit button stays disabled until that Promise settles. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/editcolumn) |
| official | behavior | In an Obsidian grid, HighlightDetailColumn renders its primary field in bold and can render a secondary row-property value beneath it when detailField names that property; omitting detailField or setting it to false leaves the secondary area empty. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/highlightdetailcolumn) |
| official | behavior | In an Obsidian grid, BooleanColumn renders a checkmark when its bound value is true and leaves the cell empty otherwise. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/booleancolumn) |
| official | behavior | DeleteColumn can disable deletion per row through rowDisabled, and when its onClick callback returns a Promise, the delete button stays disabled until that Promise resolves. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/deletecolumn) |
| official | behavior | Obsidian grids provide standard column filters for boolean, date, numeric, and text values, plus a filter that lets a person select one or more values from the column's unique existing values; the text filter uses substring matching. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/filters) |
| official | behavior | In an Obsidian grid column, the format, condensed, header, and skeleton templates take precedence over their corresponding rendering component properties; condensedComponent falls back to formatComponent when no condensed component is specified. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/standard-columns) |
| official | behavior | Obsidian grids perform filtering, sorting, and paging in the browser, so the complete row set must be transferred before rendering; configuring a smaller page size does not reduce the amount of data sent to the client. | [source](https://community.rockrms.com/developer/obsidian/grids) |
| official | behavior | Obsidian's ReorderColumn renders a drag handle that lets a user move a row to a different position in the grid. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/reordercolumn) |
| official | behavior | In an Obsidian grid, CurrencyColumn formats the cell value as currency and supplies default formatting, loading-skeleton, and export-value behavior without adding column-specific properties. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/currencycolumn) |
| official | behavior | In an Obsidian grid, TextColumn renders the field value as plain text and introduces no properties beyond the standard column properties. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/textcolumn) |
| More |  | 56 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_api_docs`: 1
- `rock_core_release_notes`: 28
- `rock_developer`: 47
- `rock_lava_docs`: 1
- `rock_model_map`: 12
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Creating Blocks | rock_developer | Obsidian blocks are made up of multiple parts that all work together to display data to and interact with the individual. ## Anatomy of an Obsidian Block The parts that make up an Obsidian block are the C# Block, the TypeScript Component and then the Block Actions. At a high level, the C# Block provides the server-level logic and database access required to render the block on the web page. The TypeScript Component... | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| Columns | rock_developer | [Standard Columns](/documentation/obsidian/grid-reference/columns/standard-columns) [AttributeColumns](/documentation/obsidian/grid-reference/columns/attributecolumns) [BooleanColumn](/documentation/obsidian/grid-reference/columns/booleancolumn) [ButtonColumn](/documentation/obsidian/grid-reference/columns/buttoncolumn) [Column](/documentation/obsidian/grid-reference/columns/column)... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns) |
| Creating Detail Blocks | rock_developer | A detail block is a term used to identify a very specific type of block. These blocks show an entity on screen with an Edit button that allows for editing one or more values of the entity. Detail blocks also have labels, badges, and custom actions defined by the block developer. ## Detail Block Anatomy Detail blocks have a very specific look and feature set. These are meant to be standardized so that we can adjust... | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks) |
| Creating List Blocks | rock_developer | These are also mostly standard, cookie cutter blocks and typically just display a list of records for a particular entity. Use the Code Generator tool to create a vanilla List block and then modify it as needed: Important The Code Generator tool is currently only available to core blocks, not plugins. If you want to look at an example of an Obsidian List block you can review the... | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks) |
| Grid Reference | rock_developer | [Grid](/documentation/obsidian/grid-reference/grid) [Columns](/documentation/obsidian/grid-reference/columns) [Filters](/documentation/obsidian/grid-reference/filters) | [source](https://community.rockrms.com/developer/obsidian/grid-reference) |
| HighlightDetailColumn | rock_developer | A general column that displays a value in bold, with a description below it. ## Example This is an example from the checkInLabelList block. ``` <HighlightDetailColumn name="name" title="Name" field="name" detailField="description" :filter="textValueFilter" visiblePriority="xs" /> ``` ## Properties Example of standard PersonColumn This column provides default values for the following standard properties: *... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/highlightdetailcolumn) |
| Browser Bus | rock_developer | ## Overview The browser bus is a basic pub-sub interface within a single page. If you publish a message to one instance of the bus it will be available to any other instance on the same page. The browser bus will not communicate with other browsers on the same page or even other tabs within the same browser. This uses `document.addEventListener()` and `document.dispatchEvent()` with a single custom event name of... | [source](https://community.rockrms.com/developer/obsidian/browser-bus) |
| Debugging Obsidian in VS Code | rock_developer | *Using VS Code's debugger with Obsidian, and setting up to attach it to an existing Chrome instance.* ## Running VS Code's Debugger Visual Studio Code (VS Code) has some debugging tools built into it that are very similar to some of the developer tools built into your browser. By using these debugging tools, you gain access to breakpoints within the editor, making debugging that little bit easier. To run the debug... | [source](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code) |
| Core Field Type Patterns | rock_developer | *Some of the common patterns utilized in Obsidian Field Types* Note This section is only relevant for the core team when creating a new custom field type. Plugins and, whenever possible, new core field types should use the new Universal Field Type pattern. ## Obsidian Edit Component For the most part, the Edit Component is usually the simple one. It takes the current value and configuration values in via the... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns) |
| Converting Core Field Types | rock_developer | *Step-by-Step guide to Building an Obsidian Field Type* Here we'll be going over the practical steps of building a field type because it involves multiple files and it can be difficult to remember some of the steps or where some of the files reside. We will not be diving much into concepts or patterns that you need to implement. For those, you can find you can look at the [Creating Field... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types) |
| Universal Field Types | rock_developer | The current (legacy) field types are all tightly integrated with WebForms. This has made converting them to Obsidian a real chore. So we knew we needed to come up with a new pattern so that we don't have to go through this again in the future. What we have landed on is a concept called "Universal Field Types". We call then "universal" because they are meant to work on any UI framework or platform without requiring... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types) |
| Obsidian Component Structure | rock_developer | ## Overview ### File Format An Obsidian component is essentially an HTML file with some sugar sprinkled into the <script> tag for you. The HTML markup used as the template is, conveniently, stored in a <template> tag at the root level. There are 4 major parts that make up the component. 1. HTML Template (🟥) 2. Imports (🟦) 3. Properties and Events (🟧) 4. Logic (🟩) The HTML markup used as the template is,... | [source](https://community.rockrms.com/developer/obsidian/obsidian-component-structure) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Field Type](../../model-map/models/field-type.md) | Core | 19.2.0 | 41 | 14 | 26 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.2.0 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.2.0 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.2.0 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.2.0 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.2.0 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.2.0 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection](../../model-map/models/content-collection.md) | CMS | 19.2.0 | 49 | 21 | 34 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 18.1 | Core | Fixed editing configuration settings of Universal field types from inside an Obsidian block. This only affected some configuration setting types which might cause the raw value to be stored as JSON. | [source](https://www.rockrms.com/releasenotes) |
| 16.1 | Core | Fixed issue of Note Type Field Type not showing up in Following Event Type Detail Obsidian block. Fixes: #5605 | [source](https://www.rockrms.com/releasenotes) |
| 19.3 | Event | Fixed inline attribute editors (such as adding a new Defined Value) on the Event Detail block returning an HTTP 401 by adding the Event Calendar Item attribute field type rules to the security grant. Fixes: #6881 | [source](https://www.rockrms.com/releasenotes) |
| 17.1 | Communication | Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface. | [source](https://www.rockrms.com/releasenotes) |
| 19.3 | Core | Fixed an issue where Obsidian blocks like the Page Menu could disappear after a full WebForms postback. Fixes: #6871 | [source](https://www.rockrms.com/releasenotes) |
| 19.3 | Core | Fixed File and Binary File attributes not showing a View link when displayed read-only in Obsidian blocks, such as the new Connections Request docked panel. Fixes: #6883 | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Workflow | Fixed an issue where the Obsidian Workflow List block would time out when loading workflows assigned to groups with many members. | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Core | Fixed an issue in Obsidian blocks where Memo Fields configured to allow HTML displayed the HTML tags as encoded text instead of rendering the formatted content within the block. Fixes: #6718 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Core | Fixed an issue in the Defined Value picker component where Single-Select Defined Value attributes configured with "Enhanced for Long Lists" did not display the searchable enhanced experience in Obsidian blocks (e.g., Workflow Entry and Event Registration), requiring manual scrolling through values. Fixes: #6658 #6705 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Core | Fixed an issue in the Obsidian Location Detail block that allowed a Location to be saved with itself (or a child Location) as its parent. This caused the Location tree to fail when loading nested Locations. Fixes: #6669 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Group | Fixed an issue in the Obsidian Group Requirement Type Detail block that caused Attribute Values to not load or save correctly when editing a requirement type. This prevented individuals from configuring or updating Group Requirement Types as expected. Fixes: #6642 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Group | Fixed an issue where the Obsidian Group Attendance Detail Block did not function correctly when Predictive Ids were disabled. The block now correctly resolves the selected group using either the Group Guid or IdKey and prevents an unintended group from loading when Disable Predictive Ids is checked in Site settings. Fixes: #6687 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Blocks

Keywords: `block, blocks, creating blocks, list block, detail block`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Creating Blocks | rock_developer | Obsidian blocks are made up of multiple parts that all work together to display data to and interact with the individual. ## Anatomy of an Obsidian Block The parts that make up an Obsidian block are the C# Block, the TypeScript Component and then the Block Actions. At a high level, the C# Block provides the server-level logic and database access required to render the block on the web page. The TypeScript Component... | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| Creating Detail Blocks | rock_developer | A detail block is a term used to identify a very specific type of block. These blocks show an entity on screen with an Edit button that allows for editing one or more values of the entity. Detail blocks also have labels, badges, and custom actions defined by the block developer. ## Detail Block Anatomy Detail blocks have a very specific look and feature set. These are meant to be standardized so that we can adjust... | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks) |
| Creating List Blocks | rock_developer | These are also mostly standard, cookie cutter blocks and typically just display a list of records for a particular entity. Use the Code Generator tool to create a vanilla List block and then modify it as needed: Important The Code Generator tool is currently only available to core blocks, not plugins. If you want to look at an example of an Obsidian List block you can review the... | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks) |
| Implementing IHasCustomActions | rock_developer | ## Overview If your block needs special configuration settings (similar to the webforms `RockBlockCustomSettings` class use to provide), you'll want to implement the `IHasCustomActions` interface and create a separate .obs file to handle displaying the configuration screen. Implement a IHasCustomActions.GetCustomActions(...) method similar to this straightforward example, replacing the ComponentFileUrl with the... | [source](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions) |
| Blocks | rock_developer | ## Overview A block is made usually made up of two parts: a server part and a client part. The first part is the server part and is written in C#. This part is always required. This contains any logic required to view, edit, and otherwise interact with the person viewing the page. This does not handle any UI, just the logic required to provide the information to the UI. The second part is the client part. It can... | [source](https://community.rockrms.com/developer/obsidian/blocks) |

### Grid Reference

Keywords: `grid, grid reference, columns, filters`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Columns | rock_developer | [Standard Columns](/documentation/obsidian/grid-reference/columns/standard-columns) [AttributeColumns](/documentation/obsidian/grid-reference/columns/attributecolumns) [BooleanColumn](/documentation/obsidian/grid-reference/columns/booleancolumn) [ButtonColumn](/documentation/obsidian/grid-reference/columns/buttoncolumn) [Column](/documentation/obsidian/grid-reference/columns/column)... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns) |
| Grid Reference | rock_developer | [Grid](/documentation/obsidian/grid-reference/grid) [Columns](/documentation/obsidian/grid-reference/columns) [Filters](/documentation/obsidian/grid-reference/filters) | [source](https://community.rockrms.com/developer/obsidian/grid-reference) |
| HighlightDetailColumn | rock_developer | A general column that displays a value in bold, with a description below it. ## Example This is an example from the checkInLabelList block. ``` <HighlightDetailColumn name="name" title="Name" field="name" detailField="description" :filter="textValueFilter" visiblePriority="xs" /> ``` ## Properties Example of standard PersonColumn This column provides default values for the following standard properties: *... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/highlightdetailcolumn) |
| SecurityColumn | rock_developer | Displays a security button that will open the standard Security editor modal for the item. ## Example ``` <SecurityColumn /> ``` ## Properties This column provides default values for the following standard properties: * name * formatComponent * headerClass * itemClass * width Type: string \| ((row: Record<string, unknown>, grid: IGridState) => string) Optional ### itemTitle Type: string \| ((row: Record<string,... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn) |
| AttributeColumns | rock_developer | This is a special placeholder column that informs the grid where to place dynamic columns that will hold the entity attribute values. ## Example ``` <AttributeColumns :attributes="attributeFields" /> ``` ## Attributes This column does not inherit any of the standard column properties. \| Property \| Type \| Default \| Description \| \| --- \| --- \| --- \| --- \| \| attributes \| AttributeFieldDefinitionBag[] \| [] \| A... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns) |
| BooleanColumn | rock_developer | Displays a boolean value as a checkmark if the value is `true`, otherwise the cell is blank. ## Example ``` <BooleanColumn name="isSystem" title="Is System" field="isSystem" visiblePriority="xs" /> ``` ## Properties This column provides default values for the following standard properties: * formatComponent * exportValue This column defines no additional properties. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/booleancolumn) |
| ButtonColumn | rock_developer | A column that displays a single button with an icon on it. ## Example ``` <ButtonColumn name="customAction" iconClass="fa fa-lightbulb" @click="onCustomAction" /> ``` ## Properties This column provides default values for the following standard properties: * headerClass * itemClass * width * formatComponent ## action Type: (key: string, grid: IGridState) => (void \| Promise<void>) Required Called when the button has... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/buttoncolumn) |
| Column | rock_developer | A generic column definition that can be used to display custom information in the cell. ``` <Column name="firstName" title="First Name"> <template #format="{ row }"> <div><strong>{{ row.firstName }}</strong></div> </template> </Column> ``` ## Properties This column defines no additional properties. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/column) |
| CopyColumn | rock_developer | Displays a copy button and places a string of text onto the browser clipboard when the button is clicked. By default this will get a string from the field specified by the `field` property. ## Example ``` <CopyColumn :field="linkUrl" /> ``` ## Properties This column provides default values for the following standard properties: * headerClass * itemClass * width * name * formatComponent ## valueToCopy Type: (row:... | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/copycolumn) |
| CurrencyColumn | rock_developer | Displays a cell value formatted as a currency. ## Example ``` <CurrencyColumn name="amount" title="Amount" field="amount" /> ``` ## Properties This column provides default values for the following standard properties: * formatComponent * skeletonComponent * exportValue This column does not define any additional properties. | [source](https://community.rockrms.com/developer/obsidian/grid-reference/columns/currencycolumn) |

### Field Types

Keywords: `field type, field types, creating field types`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Core Field Type Patterns | rock_developer | *Some of the common patterns utilized in Obsidian Field Types* Note This section is only relevant for the core team when creating a new custom field type. Plugins and, whenever possible, new core field types should use the new Universal Field Type pattern. ## Obsidian Edit Component For the most part, the Edit Component is usually the simple one. It takes the current value and configuration values in via the... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns) |
| Converting Core Field Types | rock_developer | *Step-by-Step guide to Building an Obsidian Field Type* Here we'll be going over the practical steps of building a field type because it involves multiple files and it can be difficult to remember some of the steps or where some of the files reside. We will not be diving much into concepts or patterns that you need to implement. For those, you can find you can look at the [Creating Field... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types) |
| Universal Field Types | rock_developer | The current (legacy) field types are all tightly integrated with WebForms. This has made converting them to Obsidian a real chore. So we knew we needed to come up with a new pattern so that we don't have to go through this again in the future. What we have landed on is a concept called "Universal Field Types". We call then "universal" because they are meant to work on any UI framework or platform without requiring... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types) |
| Creating Field Types | rock_developer | Important This is a work in progress. No other developers should be taking this as final truth yet. ## Introduction Field types have become rather complex. This document aims to provide understanding for how field types work and the various methods that are used to provide different functionality. ## Functionality At a high level, a field type provides 4 pieces of functionality: 1. Viewing a value. 2. Editing a... | [source](https://community.rockrms.com/developer/obsidian/creating-field-types) |

### Development Environment

Keywords: `development environment, debugging, vscode, typescript`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Debugging Obsidian in VS Code | rock_developer | *Using VS Code's debugger with Obsidian, and setting up to attach it to an existing Chrome instance.* ## Running VS Code's Debugger Visual Studio Code (VS Code) has some debugging tools built into it that are very similar to some of the developer tools built into your browser. By using these debugging tools, you gain access to breakpoints within the editor, making debugging that little bit easier. To run the debug... | [source](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code) |
| Core Development Environment | rock_developer | This page discusses things you should have configured in your environment for core development. Before you begin writing Obsidian code you will want to configure your development environment. Many things will be enforced by ESLint once it is enabled, but a few things you will want to configure in your editor. ### Visual Studio Code VS Code provides a rich development experience for Obsidian. While you can't work... | [source](https://community.rockrms.com/developer/obsidian/core-development-environment) |


## Rebuild Dependencies

- Source records: `91`
- Approved claims: `74`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
