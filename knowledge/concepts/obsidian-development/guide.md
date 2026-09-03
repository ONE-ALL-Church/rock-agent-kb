---
id: authored-obsidian-development
title: Obsidian Development
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "fd91366745658cc24f13adfe38fc3211252b67244c6db801dcf4a7008d25c5c4"
---

# Obsidian Development

## Agent Summary

Treat an Obsidian feature as a client-server system, not as a browser-only component. The required C# block owns server logic, data access, authorization, and block actions. The Obsidian client renders the interface, exchanges JSON with the server, and may be omitted only for a web block that returns static HTML without interaction. Block-action endpoints retain the block’s settings and normal security enforcement, but each action is stateless and must validate its input and authorization independently. ([Blocks](https://community.rockrms.com/developer/obsidian/blocks), [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks))

For agent-led implementation:

1. Identify whether the work targets Rock core or a plugin; documented core patterns do not automatically apply to plugins. ([Obsidian](https://community.rockrms.com/developer/obsidian))
2. Keep authorization, validation, persistence, and sensitive-data decisions on the server.
3. Define explicit JSON contracts between C# and TypeScript, including `null` and omitted-property behavior.
4. Set stable row identity before enabling advanced grid actions.
5. Prefer Universal Field Types for plugins and, when possible, new core field types.
6. Build with type checking before release; do not treat a successful watch compilation or action response as complete verification. ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development))

## Scope And Boundaries

This guide covers Obsidian blocks, list and detail patterns, custom actions, UI-control security grants, grids and filters, field types, TypeScript component behavior, Browser Bus communication, API-call caching, development environments, debugging, and relevant WebForms migration concerns.

Related topics remain in their owning concepts:

- General REST API design belongs under API integrations.
- Page and block placement, themes, and broader CMS configuration belong under CMS.
- Authorization policy and security administration belong under security.
- Workflow behavior belongs under workflows.
- An installation’s schema, plugin inventory, page permissions, block registration, and saved data require separate live verification.

The supplied developer documentation is explicitly described as a work in progress. Some pages target core development and may describe behavior that changes or is not yet implemented exactly as written. Determine version and plugin applicability before adopting a pattern. ([Obsidian](https://community.rockrms.com/developer/obsidian))

## Mental Model

An Obsidian block has three operational layers:

1. **C# block:** Loads data, evaluates permissions, applies business rules, and returns initialization data.
2. **TypeScript component:** Renders the interface and handles browser interaction.
3. **Block actions:** Carry JSON requests from the client to stateless C# handlers and return JSON results.

The server component is always required. The client is normally present but can be omitted for a static, non-interactive web block. Block-action routing supplies the server handler with the current block settings and normal block security context. ([Blocks](https://community.rockrms.com/developer/obsidian/blocks))

Initialization and action payloads should use deliberate transfer models. The documentation describes bags as the normal cross-boundary data shape and boxes for specific block contracts, including initialization and some list/detail operations. Return usable error information in the initialization contract instead of depending on an exception to produce a visitor-facing result. ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks))

Client visibility is not authorization. Hiding a control in TypeScript can improve the interface, but a caller can still construct a request. Every block action must revalidate the incoming data and recheck authorization because the server call is stateless and cannot rely on a previous C# instance or client state. ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks))

## Blocks

### Block Initialization And Actions

Use the initialization response to send the client the data and capabilities it needs to render. Use block actions for later operations such as loading, saving, deleting, or invoking a custom command. Both directions use JSON contracts. ([Blocks](https://community.rockrms.com/developer/obsidian/blocks))

For every action:

- Validate required identifiers and submitted values.
- Load the authoritative record on the server.
- Recheck authorization for the requested operation.
- Apply business rules and persistence on the server.
- Return a structured success or failure result.
- Never accept a client-provided permission flag as proof of authorization.

These checks are required even when initialization already hid or disabled the corresponding client control. ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks))

### List Blocks

Core development can use the Code Generator to scaffold a basic list block and then customize it. The documented generator is not available for plugin list blocks, so plugin developers must begin from an applicable plugin pattern rather than assuming the core generator can create their files. ([Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks))

A list block commonly sends a grid definition during initialization and retrieves its row data through a block action. Security checks, record filtering, ordering, and attribute loading remain server responsibilities; the simplified examples in the documentation do not imply those steps are optional in a real block. ([Grids](https://community.rockrms.com/developer/obsidian/grids))

### Detail Blocks And WebForms Migration

Detail blocks use a standardized component that can render an entity, editing controls, labels, badges, security controls, and developer-supplied actions. The developer configures supported features and supplies entity metadata and actions; the standardized component controls the overall layout. ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks))

Every detail block should enforce one of these models:

- **Entity security:** Authorize against the entity being displayed or changed.
- **CMS security:** Use the block’s permissions to control access to the entity operation.

When replacing a WebForms detail block that did not enforce entity-specific security, begin with CMS security and review the effective page and block permissions. Do not preserve an unsecured legacy behavior merely because the old block allowed it. ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks))

Generated code requires a save-boundary review. The initial save handler treats every selected property as writable. If a property such as `IsSystem` was included only to control client behavior, remove it from the saveable-property list so it cannot be unintentionally written back to the database. ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks))

### Custom Configuration Actions

A block that needs a custom configuration screen can implement `IHasCustomActions`. The documented pattern is to return an administrate-only custom action whose component URL points to a separate `.obs` template, then expose block actions that load and save the custom settings. ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions))

The server must decide whether the action is returned based on administration access. The client template is presentation, not the permission boundary. Validate the settings again in the save action.

### UI Controls And Security Grants

A block can grant a child control narrowly scoped API access:

1. Create a server-side security grant with rules for the appropriate entities, entity types, and authorization actions.
2. Put the encoded grant token in the block configuration sent to the browser.
3. Reconstruct and provide the grant in the client component tree.
4. Inject the token in the child control and include it in API requests.
5. Expose or use the documented renewal path because grant tokens expire after one hour by default. ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls))

An endpoint receiving a grant token must reconstruct the grant and evaluate it alongside the current person’s ordinary authorization. For a single-entity read or mutation, return an unauthorized response when neither path grants the required action. For list operations, omit inaccessible entities. Use the authorization action appropriate to the operation rather than treating a view grant as permission to edit. ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls))

## Components, Forms, And TypeScript Contracts

An Obsidian component contains its template, imports, typed properties and events, and setup logic. A property default applies only when the parent omits the property. If the parent explicitly passes `null`, the component receives `null`; the default is not substituted. ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure))

Values that must cause the template to update should be reactive `ref` or `computed` values. Changing an ordinary variable does not notify the template to render again. ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure))

Model JSON states precisely:

```ts
type ExampleModel = {
    property?: string | null;
};
```

Use `?` when the server may omit the property and include `null` when the server may explicitly send a null value. A truthiness test groups `undefined`, `null`, and an empty string together; use explicit comparisons when those states require different behavior. ([Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined))

### Form Validation

Input controls report rule-validation results through their internal `RockFormField`. When the nearest `RockForm` is submitted, the form blocks submission and shows its standard validation notice if any field is invalid; otherwise, it emits the submit event. ([Form Validation](https://community.rockrms.com/developer/obsidian/form-validation))

A form can also be submitted programmatically by binding its `submit` prop and setting the bound value to `true`. After validation finishes, the form resets the value to `false`; it emits the submit event only when submission may proceed. ([Form Validation](https://community.rockrms.com/developer/obsidian/form-validation))

For most pickers, `showBlankItem` controls whether the current selection can be cleared. The `required` validation rule independently determines whether the form may be submitted without a value. Do not use one as a substitute for the other. ([Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes))

## Grid Reference

### Data Loading, Paging, And Row Identity

A Grid can receive data directly or through a function. If the function returns a Promise, the Grid waits for it asynchronously. Set the Grid’s key field to the row property that uniquely identifies each row whenever selection, editing, deletion, reordering, or another advanced feature depends on row identity. ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid))

Filtering, sorting, and paging occur in the browser. The complete row set must therefore be transferred before rendering; reducing the page size does not reduce the amount of data sent to the client. Treat large result sets as a payload and browser-performance concern, not merely a pagination concern. ([Grids](https://community.rockrms.com/developer/obsidian/grids))

### Standard Column Behavior

For standard columns, slot templates for formatting, condensed rendering, headers, and loading skeletons take precedence over their corresponding component properties. If no condensed component is configured, `condensedComponent` falls back to `formatComponent`. `hideOnScreen` keeps a column available to exports or other processing while hiding it visually; `excludeFromExport` removes it from exported output. ([Standard Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/standard-columns))

Use the narrowest column type that matches the required behavior:

- `TextColumn` renders the field as plain text and adds no column-specific properties. ([TextColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/textcolumn))
- `BooleanColumn` shows a checkmark for `true` and an empty cell otherwise. It supplies standard `formatComponent` and `exportValue` defaults and adds no custom properties. ([BooleanColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/booleancolumn))
- `NumberColumn` formats values using the browser’s current locale, including locale-specific thousands and decimal separators. ([NumberColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/numbercolumn))
- `CurrencyColumn` formats a value as currency and supplies default formatting, skeleton, and export behavior without custom properties. ([CurrencyColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/currencycolumn))
- `DateColumn` renders a short date and supplies default formatting, skeleton, quick-filter, and export behavior without custom properties. ([DateColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/datecolumn))
- `DateTimeColumn` displays a short date plus hour and minutes by default; `showSeconds` adds seconds. ([DateTimeColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/datetimecolumn))
- `HighlightDetailColumn` renders its primary field in bold. Set `detailField` to a secondary row-property name to display supporting text; omit it or set it to `false` to leave that area empty. ([HighlightDetailColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/highlightdetailcolumn))
- A generic `Column` can render custom cell markup through its format template using the current row. ([Column](https://community.rockrms.com/developer/obsidian/grid-reference/columns/column))

### Labels And Number Badges

`LabelColumn` can translate a raw value through `textSource`. The translated text then becomes the lookup key for `classSource` or `colorSource`. `classSource` maps text to standard label suffixes, while `colorSource` maps text to CSS background colors. ([LabelColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/labelcolumn))

`NumberBadgeColumn` displays a number in a badge and tests the value against inclusive minimum and maximum ranges to choose its color. When ranges overlap, precedence is `danger`, `warning`, `success`, `info`, then `hidden`; consequently, a matching color range can override a hide range. ([NumberBadgeColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/numberbadgecolumn))

### Attribute, Person, And Rock Field Columns

`AttributeColumns` is a placeholder that determines where dynamically generated entity-attribute columns appear. Its `attributes` property receives the attribute definitions to display. It does not inherit standard column properties, but it supports an attribute filter and a skeleton component for loading. ([AttributeColumns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns))

A `PersonColumn` requires the server-side grid builder to add the person field through `AddPersonField()` so the client receives everything needed to render the person. In the documented Rock 17 behavior, `showAsLink` can link the displayed person to the person detail page, but the column does not verify that the viewer is authorized to access that page. Treat link rendering and target-page authorization as separate concerns. ([PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn))

`RockFieldColumn` requires an attribute definition and uses it to format a Rock field value. It is documented as an internal Rock column and should not be used by plugins. ([RockFieldColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/rockfieldcolumn))

### Action And Utility Columns

- `SelectColumn` renders row-selection checkboxes so grid actions can operate on multiple rows. ([SelectColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/selectcolumn))
- `EditColumn` calls its handler with the row key. The handler may return a Promise, in which case the edit button remains disabled until the Promise settles. The column provides default name, formatter, header and item classes, and width. ([EditColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/editcolumn))
- `DeleteColumn` asks for confirmation before calling its handler by default. `disableConfirmation` bypasses the prompt, `rowDisabled` can disable deletion for a specific row, and a Promise-returning handler keeps the button disabled until completion. ([DeleteColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/deletecolumn))
- `ButtonColumn` renders one icon button and requires an icon CSS class and handler. The handler receives the row key and current grid state and may be synchronous or asynchronous. ([ButtonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/buttoncolumn))
- `CopyColumn` copies text to the browser clipboard. It uses the row value named by `field` unless `valueToCopy` computes the text from the row, column definition, and grid state. ([CopyColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/copycolumn))
- `ReorderColumn` renders a drag handle. After a move, `onOrderChanged` receives the moved row and the row now following it, or `null` when the row moved to the end. The callback may persist the change, return `false` to cancel it, or return a Promise that blocks further reordering until completion. ([ReorderColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/reordercolumn))
- `SecurityColumn` opens Rock’s standard security editor for the row item. By default, a true `isSecurityDisabled` row value disables the control; `disabledField` can select another row field. ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn))

### Filters And Person Grid Actions

Standard filters exist for boolean, date, numeric, and text values, along with a filter that lets a person choose one or more unique values already present in the column. The text filter performs substring matching. A custom filter combines a popup component that constructs the filter value with a predicate that receives each row and that value and decides whether the row matches. ([Filters](https://community.rockrms.com/developer/obsidian/grid-reference/filters))

A Person grid that does not inherit from `RockListBlockType` must provide block actions for creating entity sets and communications if it wants the corresponding default grid actions. Its grid definition must identify a Person key field using an IdKey or GUID. ([Grids](https://community.rockrms.com/developer/obsidian/grids))

## Field Types

### Public And Private Representations

A field type supplies behavior for viewing, editing, filtering, and configuration. Values and configuration can have private server representations and public representations sent to clients. Before transmitting either kind of data, convert it into a safe public form. An identifier may be expanded into a client-friendly object when the interface needs display information, with a corresponding conversion back to the stored representation. ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types))

Public configuration keys and their meanings are compatibility contracts with remote consumers such as Rock Mobile. Renaming a key, changing its meaning, or changing its representation can break existing clients even if the local Obsidian component is updated at the same time. ([Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types))

If the public display and edit representations differ, client formatting methods must accept either form. An unsaved edit value can reach a formatting method that normally receives the display representation. ([Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types))

### Universal Field Types

Universal Field Types keep UI code out of the C# field-type implementation. The server supplies structured data, and the client framework renders the appropriate picker or editor. Item, tree, and search picker implementations using this pattern also receive Data View filtering support. This is the preferred documented direction for plugins and, where possible, new core field types. ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types), [Core Field Type Patterns](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns))

For plugin endpoints serving Universal Tree Item Picker or Search Picker data, the approved version-scoped guidance says to accept POST input from the request body and use an `api/v2/plugins/{organization-code}/...` route. The `api/v2` prefix supplies the camel-cased response properties expected by Obsidian clients, while the organization segment avoids plugin route collisions. The supplied claim is scoped to Rock 2.0 and must be rechecked for the target version. ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types))

### Core Field Type Conversion

To make a core field type available in Obsidian:

1. Declare Obsidian platform support on the C# field type.
2. Expose the field type’s GUID through the generated field-type system GUIDs.
3. Create the TypeScript field-type implementation.
4. Import and register it in the Obsidian field-type index.
5. Test compatible configuration and value behavior across equivalent WebForms and Obsidian attribute blocks. ([Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types))

The immutable source snapshot supplied with this guide shows current implementation examples that import `FieldTypeBase`, define configuration-key enums, and lazy-load edit or configuration components. These files are implementation examples at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, not proof of a target installation’s version or configuration. ([Security Role field implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/securityRoleField.partial.ts), [Address field implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/addressField.partial.ts))

### Configuration Updates

When a configuration change is entirely client-side, emit the updated model value. When the change affects options or other data derived by the server, also request a configuration refresh. Configuration properties provided to a configuration component are one-way inputs; changing them locally does not update the server. ([Core Field Type Patterns](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns))

Rock 18.1 release notes record a fix for editing some Universal Field Type configuration settings inside an Obsidian block, where raw values could be stored as JSON. Rock 16.1 release notes record a separate fix for a Note Type Field Type missing from an Obsidian detail block. These are historical fixes, not evidence that every version or installation is unaffected. ([Rock Release Notes](https://www.rockrms.com/releasenotes))

## Browser Bus

The Browser Bus is a page-local publish-subscribe mechanism backed by DOM events. A message published by one bus instance can be received by another instance on the same page, including plain JavaScript integrated with the page. Messages do not cross browser tabs and do not reach another user’s browser. ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus))

Use a block-configured bus when messages should automatically identify their originating block and block type. Use a generic bus when there is no block context or the message is not intended to originate from a specific block. Subscriptions can listen broadly or narrow messages by block or block type. ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus))

Do not use the Browser Bus as a persistence mechanism, server event channel, cross-tab synchronization layer, or authorization boundary.

## Caching API Calls

`cachePromise` wraps a Promise-returning operation. Concurrent calls through the same wrapper reuse the in-flight Promise; later calls reuse the serialized result until expiration. The default expiration is one minute. ([Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls))

To cache a request:

1. Import the utility from `@Obsidian/Utility/cache`.
2. Call `cachePromise` with a unique cache key.
3. Supply a function that returns the request Promise.
4. Optionally set an expiration.
5. Invoke the returned function instead of issuing the request directly. ([Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls))

The evidence does not establish cache invalidation rules for a particular business operation. Choose keys and expiration only after determining the data’s freshness requirements.

## Development Environment

### Core Development

Core `.obs` development is supported in Visual Studio Code rather than the Visual Studio editor. Open the repository’s `Rock.code-workspace`; it supplies expected editor settings, recommended extensions, debugger configurations, and watch tasks for the Obsidian framework and block projects. The normal documented workflow uses the “Watch All Obsidian” task to build and watch controls and blocks. ([Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment))

Cross-package imports should use aliases such as `@Obsidian/...`. Relative imports are reserved for files in the same package or directory. Core additions must respect the documented package hierarchy: a package may depend on packages above it, but direct or indirect cycles are prohibited. Block developers may import from any of the documented Obsidian packages. ([App Laws](https://community.rockrms.com/developer/obsidian/app-laws))

### Plugin Development

In a `rock-dev-tool` arrangement, the development environment owns the runnable Rock installation and selected Rock version. Each plugin remains a separate source repository and can be attached to multiple environments to test against different Rock versions. ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development))

For a plugin:

- `npm run build` performs TypeScript type checking before compilation and asset copying to RockWeb.
- `npm run watch` continuously recompiles changed files without type checking.

Use watch mode for feedback during development, but run the checked build before treating the client code as release-ready. ([Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development))

### Debugging

The Rock VS Code workspace provides separate debugger configurations for the Obsidian Framework and Obsidian Blocks projects. Each project has a configuration that opens a new browser and one that attaches to an existing browser. ([Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code))

Attaching to an existing Chrome session requires Chrome to be launched with remote debugging enabled on port `9222`. If attach mode cannot connect, verify how Chrome was launched before changing application code. ([Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code))

## Version And Authority Caveats

- This guide is generated from approved claims and bounded source excerpts and still requires maintainer review.
- The Obsidian developer documentation states that it is a work in progress; behavior may change or may not yet be implemented as described. ([Obsidian](https://community.rockrms.com/developer/obsidian))
- Some documentation is explicitly core-oriented. Confirm that file layout, generator support, API routing, and registration steps apply before using them in a plugin. ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls))
- `PersonColumn.showAsLink` behavior in this evidence is scoped to Rock 17. ([PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn))
- The supplied Universal Field Type plugin-route claim is scoped to Rock 2.0 and should not be generalized without version confirmation. ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types))
- Rock 18.1 and 16.1 release-note entries describe historical fixes; they do not establish the state of an unverified installation. ([Rock Release Notes](https://www.rockrms.com/releasenotes))
- The supplied GitHub examples are fixed to commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They show source implementation at that commit, not installed configuration.
- In older `.ts` components, a Vue compiler message reported only as `SyntaxError 15` indicates missing whitespace between attributes. The documentation says this numeric-error problem is not expected for newer `.obs` files. ([Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes))

## Troubleshooting Decision Tree

### A Block Action Is Visible But Returns Unauthorized

1. Confirm the server action checks the current person’s ordinary authorization.
2. If a child control needs delegated access, confirm the block created and provided a security grant.
3. Confirm the control injected the current token and included it in the request.
4. Confirm the endpoint reconstructs the grant and checks the authorization action needed for this operation.
5. Check whether the one-hour default token lifetime requires renewal.
6. Stop when authorization succeeds through an intentional rule; do not bypass the server check or trust client visibility. ([Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls))

### A Save Reports Success But The Intended Values Do Not Persist

1. Reload through an independent read path rather than trusting the action’s success response.
2. Compare the submitted JSON contract with the server action’s accepted model.
3. Check server-side normalization, defaults, omitted properties, and fields ignored by the save handler.
4. For a generated detail block, inspect the saveable-property list for both missing intended fields and UI-only fields that should have been removed.
5. Confirm the action reloaded and authorized the intended entity.
6. If the behavior depends on installed schema or configuration, perform a bounded live readback. The independent-readback practice is a reviewed community pattern, not a universal guarantee about every block action. ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks), [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks))

### A Grid Action Targets The Wrong Row Or Has No Row Key

1. Confirm the Grid’s key field names a property that uniquely identifies each row.
2. Confirm every row includes that property.
3. Confirm the action handler expects the same key representation.
4. For `PersonColumn`, confirm the server used `AddPersonField()`.
5. For Person default actions outside `RockListBlockType`, confirm the grid definition uses an IdKey or GUID and that the required entity-set and communication actions exist. ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid), [Grids](https://community.rockrms.com/developer/obsidian/grids), [PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn))

### A Grid Is Slow Even With A Small Page Size

1. Measure or inspect the total row count, not only the configured page size.
2. Confirm whether the complete result set is being transferred to the browser.
3. Reduce or constrain the server result set if the business requirement permits.
4. Reassess attribute payloads and other per-row data.
5. Stop when the initial transfer and browser work are acceptable; changing only client page size does not reduce the payload. ([Grids](https://community.rockrms.com/developer/obsidian/grids))

### A Template Does Not Update After A Value Changes

1. Determine whether the value is an ordinary variable.
2. Move template-driving state into a reactive `ref` or `computed` value.
3. Confirm the template reads that reactive value.
4. Check whether the parent passed `null`, omitted the property, or supplied a different value than expected. ([Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure))

### A Picker Can Be Cleared Or Submitted Unexpectedly

1. Inspect `showBlankItem` to determine whether the selection can be cleared.
2. Inspect the `required` rule to determine whether an empty value blocks submission.
3. Treat these as independent settings.
4. Submit through the nearest `RockForm` and verify whether its validation notice appears. ([Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes), [Form Validation](https://community.rockrms.com/developer/obsidian/form-validation))

### A Field Type Displays Correctly But Fails During An Unsaved Edit

1. Compare the public display and public edit representations.
2. Pass representative values from both forms through `getTextValue` and related formatting methods.
3. Update those methods to handle either representation.
4. Confirm the conversion back to the private stored representation.
5. Recheck public configuration-key compatibility before changing the contract. ([Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types), [Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types))

### VS Code Cannot Attach To Chrome

1. Confirm the correct Framework or Blocks attach configuration was selected.
2. Confirm Chrome was launched with remote debugging enabled.
3. Confirm the configured port is `9222`.
4. Restart Chrome through the correctly configured launch path if necessary.
5. Stop when the debugger attaches; do not treat an ordinary Chrome session as attach-enabled. ([Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code))

### An Older Component Fails With `SyntaxError 15`

1. Confirm the failing source is an older `.ts` component rather than a newer `.obs` file.
2. Inspect adjacent template attributes for missing whitespace.
3. Correct the attribute separation and rebuild.
4. If the error remains, treat the numeric code as insufficient evidence for another diagnosis. ([Misc Notes](https://community.rockrms.com/developer/obsidian/misc-notes))

## Agent Task Recipes

### Recipe: Implement A Secure Block Action

**Outcome:** A server action that accepts client data without trusting client state.

1. Define a typed request and response contract.
2. Validate required values and identifier formats.
3. Load the authoritative entity in the action.
4. Evaluate the current person’s authorization for the exact operation.
5. Apply business rules and persist the change.
6. Return a structured result.
7. Invoke the action from TypeScript and handle both success and failure.
8. Verify the result through a fresh read when persistence is material. ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks))

**Do not assume:**

- A hidden control prevents unauthorized requests.
- Authorization checked during initialization remains valid.
- A previous C# block instance retains state.
- A success response proves that all submitted values were persisted.

**Stop when:**

- Unauthorized requests are rejected.
- Invalid data is rejected.
- The intended result is confirmed through an independent read.

### Recipe: Scaffold And Harden A Detail Block

**Outcome:** A standardized detail block with an explicit write boundary.

1. Choose entity or CMS security.
2. If replacing an unsecured WebForms block, start with CMS security and review effective page permissions.
3. Generate the core detail block and related view models when the core generator is available.
4. Include properties needed for rendering or UI decisions.
5. Remove UI-only properties from the saveable-property list.
6. Confirm the entity metadata required by the detail component.
7. Build and run the boilerplate before adding custom logic.
8. Test view, edit, unauthorized access, validation failure, and save readback. ([Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks))

**Inspect:**

- Security mode
- Effective block and page permissions
- Saveable properties
- Attribute support
- Entity key and type metadata

### Recipe: Build A Grid With Reliable Actions

**Outcome:** A grid whose filters, exports, and actions operate on the intended rows.

1. Bound the server query to an acceptable total result size.
2. Build the grid definition and row data.
3. Set a unique key field.
4. Choose typed columns for standard data and a generic `Column` only for custom markup.
5. Configure `hideOnScreen` and `excludeFromExport` independently.
6. Add filters, selection, edit, delete, security, copy, or reorder columns as needed.
7. For asynchronous handlers, return their Promises so controls remain disabled while work is pending.
8. Test row identity after sorting and filtering.
9. Test export behavior separately from on-screen visibility. ([Grid](https://community.rockrms.com/developer/obsidian/grid-reference/grid), [Standard Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns/standard-columns))

**Do not assume:**

- Paging reduces data transfer.
- A person link proves access to the destination.
- A hidden column is excluded from export.
- A visual delete confirmation replaces server authorization.

### Recipe: Add A Core Field Type To Obsidian

**Outcome:** A registered core field type with compatible server and client representations.

1. Declare Obsidian platform support in the C# field type.
2. Expose its GUID through the field-type system GUID definitions and generation process.
3. Create the TypeScript field implementation and components.
4. Import and register the implementation in the field-type index.
5. Define safe public value and configuration representations.
6. Implement conversion back to the private stored representations where required.
7. Ensure formatting functions accept both display and unsaved edit representations.
8. Test equivalent attribute configuration and editing through WebForms and Obsidian blocks.
9. Add an example to the field-type gallery when following the documented core workflow. ([Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types))

**Stop when:**

- The type appears where expected.
- Configuration round-trips correctly.
- Values edited in either interface are reflected in the other after refresh.
- No public contract exposes unsafe private data.

### Recipe: Create A Universal Plugin Picker

**Outcome:** A plugin field type whose C# implementation supplies structured picker data without owning UI code.

1. Select the item, tree, or search picker pattern.
2. Define single- or multi-selection behavior.
3. Return the structured items or selected-item representations required by the pattern.
4. For tree or search data, implement the version-appropriate plugin API endpoint.
5. Under the supplied Rock 2.0 guidance, accept POST input from the request body and use an `api/v2/plugins/{organization-code}/...` route.
6. Apply ordinary authorization and any required grant evaluation in the endpoint.
7. Verify display, editing, stored-value conversion, and Data View filtering. ([Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types))

**Do not assume:**

- The version-scoped route remains correct for every Rock version.
- Universal rendering removes the need for server authorization.
- A working picker proves stored-value compatibility.

### Recipe: Add A Custom Block Settings Screen

**Outcome:** An administrate-only `.obs` settings interface backed by block actions.

1. Implement `IHasCustomActions`.
2. Return the custom action only when the caller can administrate the block.
3. Point its component URL to the dedicated `.obs` settings template.
4. Add a block action to load the current settings and required options.
5. Add a block action to validate and save changes.
6. Recheck administration authorization inside the save action.
7. Reload the settings independently after saving. ([Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions))

### Recipe: Coordinate Same-Page Blocks With Browser Bus

**Outcome:** One block reacts to an event from another block on the same page.

1. Obtain a block Browser Bus when the source block identity should be attached automatically.
2. Choose a message name and typed data contract.
3. Subscribe broadly or constrain the subscription by block or block type.
4. Publish after the source operation reaches the state the subscriber needs.
5. Unsubscribe according to the component lifecycle.
6. Test on one page.
7. Verify that no requirement depends on cross-tab or cross-user delivery. ([Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus))

**Stop when:**

- The intended same-page subscriber responds.
- Unrelated block instances do not respond when the subscription is scoped.
- No persistence or security decision depends on the message.

### Recipe: Cache A Read Request

**Outcome:** Concurrent callers share one in-flight request and reuse its result for a bounded period.

1. Import `cachePromise` from `@Obsidian/Utility/cache`.
2. Choose a key unique to the request and all inputs that affect its result.
3. Wrap the Promise-returning request function.
4. Set an expiration when the one-minute default is inappropriate.
5. Call the wrapper from all consumers.
6. Test concurrent calls and post-expiration behavior. ([Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls))

**Do not assume:**

- The cache is an authorization boundary.
- One key is safe for requests with different inputs.
- The default expiration satisfies the data’s freshness requirement.

### Recipe: Verify A Community-Suggested Block-Action Save Path

**Outcome:** A proposed operational save path is evaluated without treating one organization’s experience as universal Rock behavior.

1. Identify the installed block, its version, action key, current initialization payload, and required permissions.
2. Confirm from applicable source or runtime metadata that the action is intended to own the relationship or configuration.
3. Read the current state.
4. Submit the smallest authorized change.
5. Read the state again through an independent source.
6. Compare the persisted relationships and normalized values with the intended result.
7. Roll the finding into public guidance only after a public-safe review.

A reviewed community example applies this workflow to check-in GroupLocation and Schedule relationships and recommends using the applicable Schedule Builder save action rather than assuming a scalar entity update replaces a navigation collection. This remains a community pattern requiring version, block, permission, and persistence verification; keep its detailed procedure with the check-in concept. ([CheckInScheduleBuilder source reference](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs))

## Known Gaps And Live Verification

No live Rock instance was reviewed for this guide. Before applying it to an installation, verify:

- Installed Rock version and patch level.
- Whether the target block or field type is core or plugin-owned.
- Whether the documented component, column property, generator, and route exist in that version.
- Block registration, page placement, settings, and effective permissions.
- Entity, CMS, and security-grant authorization behavior.
- Actual initialization and block-action contracts.
- Total grid payload size and browser performance with representative data.
- Public and private field-type conversions, including remote-client compatibility.
- Universal Field Type configuration behavior on versions affected by or predating the Rock 18.1 fix.
- `PersonColumn.showAsLink` behavior outside the documented Rock 17 scope.
- Plugin API route casing and request-body behavior outside the supplied Rock 2.0 scope.
- Independent persistence readback after any material block-action save.
- Whether a community-suggested action path applies to the installed block and schema.

A successful build, watch compilation, HTTP response, or visible control is not by itself proof of correct permissions, persistence, compatibility, or installed behavior.

## Source Map

### Official Developer Documentation

- [Obsidian](https://community.rockrms.com/developer/obsidian) — documentation maturity and core-versus-plugin caveats.
- [Blocks](https://community.rockrms.com/developer/obsidian/blocks) and [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) — client-server architecture, JSON exchange, actions, state, and security.
- [Creating List Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks) and [Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks) — scaffolding, standardized block patterns, permissions, and save boundaries.
- [Implementing IHasCustomActions](https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions) — custom settings actions.
- [Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls) — `.obs` controls and security grants.
- [Obsidian Component Structure](https://community.rockrms.com/developer/obsidian/obsidian-component-structure), [Form Validation](https://community.rockrms.com/developer/obsidian/form-validation), [Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined), and [App Laws](https://community.rockrms.com/developer/obsidian/app-laws) — component, form, typing, import, and package rules.
- [Grids](https://community.rockrms.com/developer/obsidian/grids) and [Grid Reference](https://community.rockrms.com/developer/obsidian/grid-reference) — grid architecture, data loading, actions, columns, and filters.
- [Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types), [Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types), [Core Field Type Patterns](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns), and [Universal Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/universal-field-types) — field contracts, conversions, configuration, and universal patterns.
- [Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus) and [Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls) — page-local messaging and Promise caching.
- [Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment), [Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code), and [Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development) — build, watch, debugging, and environment separation.

### Release Evidence

- [Rock Release Notes](https://www.rockrms.com/releasenotes) — historical Rock 18.1 Universal Field Type configuration fix and Rock 16.1 Note Type Field Type visibility fix.

### Immutable Implementation Evidence

- [Field Type Gallery types](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Example/FieldTypeGallery/types.partial.ts)
- [Field Type Gallery utilities](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Example/FieldTypeGallery/utils.partial.ts)
- [Security Role field](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/securityRoleField.partial.ts)
- [Address field](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/addressField.partial.ts)

These files describe implementation at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`; they do not establish a live installation’s configuration.

### Reviewed Community Patterns

- Independent readback after a block-action save.
- Verification of relationship-specific action paths before substituting a generic entity update.
- Bounded checks of block identity, authorization, current state, and persisted state.

These are operational examples rather than official Rock behavior and require live verification before use.