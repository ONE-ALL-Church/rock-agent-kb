---
id: authored-lava
title: Lava
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Lava

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Lava index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Lava is Rock RMS's Liquid-based template language for turning Rock data, merge fields, page context, request data, and command output into rendered text, HTML, CSS, JSON, XML, labels, workflow launches, analytics records, and API responses. In practice, Lava is not just a display language. It is the connective layer used by CMS pages, communications, workflows, shortcodes, mobile blocks, remote render endpoints, Lava webhooks, Helix-style applications, and agent tools.

An agent working in Rock should treat Lava as a privileged execution surface. A Lava template might only print `{{ CurrentPerson.NickName }}`, or it might query entities, run SQL, call external APIs, write interaction records, launch workflows, update data through Helix-era commands, send printer instructions, or expose data through a webhook. Rock's Lava command documentation explicitly separates ordinary Lava syntax from enabled commands because commands can bypass ordinary application screens, security assumptions, and business workflows when enabled in the wrong context ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)).

The operational model is:

1. Identify where the Lava runs.
2. Inspect the merge fields available in that context.
3. Inspect which Lava commands are enabled in that context.
4. Determine whether the template is read-only, write-capable, remote-call-capable, or response-controlling.
5. Verify the current Rock version and Lava engine.
6. Prefer entity commands and documented filters for normal reads.
7. Use SQL only when entity commands cannot express the query cleanly, and parameterize all user-influenced values.
8. Use shortcodes to standardize reusable patterns, but treat shortcode type, scope behavior, parameters, and enabled commands as part of the contract.
9. Use caching, observability, and debugging tools deliberately.
10. Validate production-facing Lava against security, performance, and version caveats before relying on it.

The most important version caveat is the transition from DotLiquid to Fluid. Rock introduced Fluid in v13 and moved toward ending DotLiquid support by v17. The Fluid migration affects include syntax, sorting behavior, variable naming, comments, null comparisons, escaping, and other edge cases ([About Lava Fluid](https://community.rockrms.com/lava/fluid), [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)). Agents should never assume old Lava syntax is safe in a modern instance. First inspect the Global Attribute named `Lava Engine Liquid Framework`, the Rock version, and recent exceptions.

The most important security caveat is that command enablement matters. HTML blocks, Communication Entry blocks, shortcodes, webhooks, and global defaults can each grant different command access ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). If a template can run `sql`, `webrequest`, entity commands with `securityenabled:'false'`, workflow activation, HTTP response commands, or Helix data-modification commands, it must be reviewed as executable application logic.

The most important maintenance caveat is that Lava is distributed across many storage locations: block settings, content channel item content, system communications, workflow action values, defined values, shortcodes, theme files, includes, mobile block templates, API webhook templates, and plugin-provided shortcodes or commands. To troubleshoot Lava, do not only inspect the visible page. Follow the context back to the block, shortcode, include file, workflow, communication, Defined Type, or mobile block that actually owns the template.

## 2. Scope And Terminology

This guide covers Lava syntax, filters, commands, shortcodes, remote Lava, Lava APIs, Fluid migration, security, operational checks, source-code landmarks, and agent-oriented playbooks. It focuses on concepts and operational use, not on exhaustive filter-by-filter syntax for every built-in filter. When the source pack gives command parameters or entity relationships, those are included. When the source material is thin, the guide says what to inspect in a live Rock instance.

Use these terms consistently:

**Lava**  
Rock's Liquid-based template language. It renders variables, evaluates tags, applies filters, executes enabled commands, and expands shortcodes. Rock's public Lava reference describes it as a Liquid-derived engine extended for Rock-specific use ([Lava Reference](https://community.rockrms.com/lava)).

**Output markup**  
The `{{ ... }}` syntax that evaluates an expression and writes the result into the rendered output.

**Tag**  
The `{% ... %}` syntax used for logic, control flow, variable assignment, includes, raw blocks, and some command-like constructs. Examples include `if`, `for`, `assign`, `capture`, `include`, `raw`, and Fluid's `lava` tag ([Lava Reference](https://community.rockrms.com/lava), [Include](https://community.rockrms.com/lava/tags/include-tags), [Raw](https://community.rockrms.com/lava/tags/raw-tags)).

**Filter**  
A transformation applied with pipe syntax, such as `{{ value | Date:'MMM d' }}` or `{{ Person | Attribute:'BaptismDate' }}`. Filters format values, convert types, access Rock attributes, serialize data, manipulate arrays, and more.

**Command**  
A Lava block or tag that performs a larger operation, often involving Rock data, SQL, HTTP calls, caching, workflows, interactions, search, printing, or other system behavior. Commands must be enabled in the running context before they can be used ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)).

**Entity command**  
A generated command for querying Rock entities such as `person`, `group`, `contentchannelitem`, `registrationinstance`, or plugin entities. The registered command names can be discovered with the administrative `taglist` command if available ([Tag List](https://community.rockrms.com/lava/commands/taglist-commands), [Entity](https://community.rockrms.com/lava/commands/entity-commands)).

**Shortcode**  
A reusable Lava template invoked with `{[ shortcode ... ]}` syntax. Rock supports inline shortcodes and block shortcodes. Shortcodes are configured in `Admin Tools > CMS Configuration > Lava Shortcodes` ([Intro to Shortcodes](https://community.rockrms.com/lava/shortcodes/intro-to-shortcodes), [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes), [Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).

**Inline shortcode**  
A shortcode with no closing tag. It accepts parameters and renders output. It is appropriate for compact, self-contained functionality such as an embed or formatter.

**Block shortcode**  
A shortcode with a start tag and end tag. It receives the content between those tags through `blockContent` and can parse nested configuration sections ([The Power of Shortcode Blocks](https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks)).

**Fluid**  
The newer Lava engine introduced in Rock v13. It is faster and more standards-aligned than DotLiquid, but some syntax and behavior differs ([About Lava Fluid](https://community.rockrms.com/lava/fluid), [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)).

**DotLiquid**  
The older Lava engine. Source material says support was ending with Rock v17; agents should verify a live instance's engine setting rather than assuming it is already fully migrated ([Lava Reference](https://community.rockrms.com/lava), [About Lava Fluid](https://community.rockrms.com/lava/fluid)).

**Merge fields**  
Variables made available by the current context. Examples include `CurrentPerson`, `Person`, `Campuses`, `PageParameter`, `Workflow`, `Body`, `Headers`, or block-specific values. Debug mode in many Lava-enabled contexts can expose available fields.

**Context**  
The execution environment for a Lava template: a CMS block, communication, workflow action, shortcode, remote render endpoint, webhook, mobile block, or tool. Context controls merge fields, command enablement, security, and available request data.

## 3. Lava Mental Model

Think of Lava as a small program that Rock merges into a larger runtime context.

A minimal output expression looks like this:

```liquid
Hello {{ CurrentPerson.NickName }}.
```

That expression reads from the current merge field dictionary and writes text. A slightly safer version guards the missing-person case:

```liquid
{% if CurrentPerson %}
Hello {{ CurrentPerson.NickName }}.
{% else %}
Hello.
{% endif %}
```

This pattern captures the three layers of Lava:

1. **Data**: values supplied by Rock, the page, a block, a workflow, request data, an entity command, SQL, or another template.
2. **Logic**: tags such as `if`, `case`, `for`, `assign`, `capture`, and `include`.
3. **Transformation**: filters such as `Date`, `AsInteger`, `ToJSON`, `Attribute`, `Escape`, `Split`, `Join`, `OrderBy`, and many others.

Commands add a fourth layer: **side effects and external access**. For example, an entity command reads Rock entities; `sql` can run database statements; `webrequest` can call remote systems; `workflowactivate` can create or modify workflows; interaction commands write analytics; `printzpl` sends printer output; `stylesheet` injects CSS into the page header ([Entity](https://community.rockrms.com/lava/commands/entity-commands), [SQL](https://community.rockrms.com/lava/commands/sql-commands), [Web Request](https://community.rockrms.com/lava/commands/web-request-commands), [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands), [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl), [Stylesheet](https://community.rockrms.com/lava/commands/stylesheet-commands)).

For agents, the key question is not "does this Lava render?" It is "what authority does this Lava have?"

A page with a plain HTML block and no enabled commands may only read merge fields and format values. A page with `RockEntity`, `Sql`, `WebRequest`, and `WorkflowActivate` enabled can read broad data, run queries, call external systems, and launch workflows. A Lava webhook may be reachable without user session assumptions and must be treated like an API surface ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). A remote Lava endpoint tied to a REST key runs as the person associated with that key, so exposing the key in client-side JavaScript gives outsiders a way to run Lava under that identity ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava), [Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456)).

The mental model for safe work is therefore:

- **Render-only Lava**: output, tags, filters, local formatting.
- **Read Lava**: entity commands, search commands, read-only SQL.
- **External Lava**: web requests, remote rendering, third-party API integrations.
- **Write Lava**: interaction write, workflow activation, data-modifying SQL, modify/delete entity commands, printer commands, HTTP response control.
- **Reusable Lava**: shortcodes, includes, theme assets, mobile templates, API templates.

Each layer requires a different review threshold.

## 4. Source Authority And How To Use This Guide

Use sources in this priority order:

1. **Official Lava documentation** for core syntax, commands, filters, shortcodes, Fluid migration, and remote/API features.
2. **Rock release notes and tech bulletins** for version-specific behavior changes and current caveats.
3. **Rock source-code and generated view models** for entity fields, block APIs, configuration bags, and implementation landmarks.
4. **RockU training** for conceptual reinforcement and examples.
5. **Developer docs** for mobile, Helix, Obsidian, and AI-agent usage.
6. **Community recipes** for patterns and examples, with review before production use.

The source pack contains public excerpts rather than full documentation. This guide synthesizes those excerpts and citations. It does not replace a live inspection of a Rock instance.

When an agent is doing real work, use this guide as an operational map, then verify these items live:

- Rock version and release channel.
- Lava engine setting.
- Enabled commands in the actual block, shortcode, communication, webhook, or global defaults.
- Merge fields available in that specific context.
- Entity command names, especially for plugins.
- Security roles and REST key identity for remote execution.
- Shortcode records, active state, tag type, scope behavior, parameters, enabled commands, and categories.
- Exception list entries for Lava parse errors, legacy syntax warnings, Fluid verification mismatches, SQL errors, or security-denied command usage.
- Whether source URLs have newer documentation than the provided pack.

Do not treat community recipes as endorsed core behavior. Recipe pages include a disclaimer that community submissions are not reviewed or endorsed by the Rock core team and may carry performance or security risk; use them as examples to adapt, not as authority ([Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456), [Lava Shortcode for Placement Groups on Check In](https://community.rockrms.com/recipes/386), [Address Format Lava Shortcode](https://community.rockrms.com/recipes/467)).

## 5. Core Configuration And Data Model

### Lava Engine Liquid Framework

The primary engine setting is the Global Attribute named `Lava Engine Liquid Framework`, located at `Admin Tools > General Settings > Global Attributes` according to the Fluid transition documentation ([About Lava Fluid](https://community.rockrms.com/lava/fluid)). In Rock v13, the documented options were:

- `DotLiquid`
- `Fluid`
- `DotLiquid (with Fluid verification)`

Verification mode runs Lava through both engines and logs differences or problems as exceptions. This is useful during migration, but it has an operational caveat: templates may execute twice. If a template writes data, sends requests, logs interactions, activates workflows, prints labels, or changes state, double execution can create duplicate side effects. Before enabling verification in production, search for write-capable Lava and either disable those paths during testing or verify idempotence.

Agent inspection steps:

1. Open the Global Attribute value for `Lava Engine Liquid Framework`.
2. Check whether Rock has already moved beyond the v13-era options.
3. Inspect the Exception List for Fluid verification errors.
4. Find templates referenced in exception details.
5. Remediate syntax differences.
6. Restart Rock only when the setting change requires it and a maintenance window is acceptable.

### Default Enabled Lava Commands

Rock supports a Global Attribute named `Default Enabled Lava Commands`, used where individual block settings do not exist or are impractical ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)). This is a high-impact setting. If broad commands such as `Sql`, `RockEntity`, `WebRequest`, or write commands are globally enabled, many Lava contexts may inherit authority the author did not explicitly request.

Agent inspection steps:

1. Inspect `Default Enabled Lava Commands`.
2. Record whether it is empty, minimal, or broad.
3. Identify contexts that rely on defaults.
4. Prefer enabling commands on the narrowest block or shortcode that needs them.
5. If reducing defaults, test communications, workflows, and CMS pages that depend on inherited commands.

### HTML Block Command Enablement

HTML blocks expose a block setting for enabled Lava commands. Official docs state HTML blocks do not have commands enabled by default ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)). When diagnosing a Lava block:

1. Open block settings.
2. Inspect enabled commands.
3. Compare the template's actual command usage.
4. Remove unused commands.
5. Confirm cache duration and output caching settings if the block is expensive.
6. Use debug mode, if available, to inspect merge fields.

### Communication Entry Command Enablement

Communication Entry also has command enablement considerations. The command documentation calls out that staff-facing internal use and public or toolbox-originated communication use may need different command availability ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)). Agents should be careful when enabling commands in communications because email/SMS templates often include recipient-specific data and can be rendered many times.

Checklist:

- Confirm whether the communication is internal-only, public-entry, scheduled, or automated.
- Verify whether command output is recipient-specific.
- Avoid SQL or entity queries that run once per recipient unless cached or precomputed.
- Escape user-entered values in HTML, links, XML, JSON, and mobile contexts.
- Inspect communication send logs and exceptions after changes.

### Lava Shortcode Entity

Rock's source model defines `LavaShortcode` as a CMS entity. The source-code snippet for `Rock/Model/CMS/LavaShortCode/LavaShortCode.cs` identifies fields that agents should inspect or populate: `Name`, `Description`, `Documentation`, active/system flags, `TagName`, `Markup`, `TagType`, `EnabledLavaCommands`, `Parameters`, `ShortcodeScopeBehavior`, and related `Categories` ([LavaShortCode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.cs)). The Obsidian view-model snippets mirror many of these fields, including `enabledCommands`, `parameters`, `shortcodeScopeBehavior`, `tagName`, and `tagType` ([LavaShortcodeBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaShortcodeDetail/LavaShortcodeBag.cs), [lavaShortcodeBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeBag.d.ts)).

Operational meaning of key fields:

- `Name`: Human-readable display name.
- `TagName`: The token used in `{[ tagname ]}`. It must be unique; the detail block source validates duplicate tag names ([LavaShortcodeDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeDetail.cs)).
- `TagType`: Inline or block. Changing it later breaks callers because block and inline invocation syntax differ ([Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes)).
- `Markup`: The Lava template that executes when the shortcode is expanded.
- `Parameters`: Declared keys and defaults. Source docs warn that uppercase keys may not be set by callers as expected; use lowercase keys ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).
- `EnabledLavaCommands`: Commands available inside the shortcode even if the source block did not enable them ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).
- `ShortcodeScopeBehavior`: Controls whether variables in the shortcode are isolated from or shared with surrounding Lava. Release notes describe this as a v19.1 addition; older docs mention a v12-era `Variable Scope Context`, so verify the actual field label and behavior in the live version ([Rock Core Release Notes](https://www.rockrms.com/releasenotes), [Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).
- `Categories`: Used for grouping and filtering shortcodes in the admin UI. Source code shows shortcode list blocks loading and displaying category associations ([LavaShortcodeList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeList.cs)).

### Lava Shortcode Cache

The model logic snippet shows `LavaShortcode` implements cache behavior through `LavaShortcodeCache`, with update hooks when the entity changes ([LavaShortCode.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.Logic.cs)). If a shortcode change appears not to render immediately, inspect:

- Whether the shortcode record saved successfully.
- Whether Rock cache was updated.
- Whether the calling block has output caching.
- Whether the `cache` Lava command wraps the shortcode output.
- Whether the page, browser, or CDN has cached output.
- Whether the shortcode is system-defined and overwritten by update behavior.

### Lava Webhooks

Lava API/webhook templates are configured through a Defined Type according to the Lava API documentation. Incoming requests are matched to Defined Values by path and optionally by HTTP verb, with regular expression support for URL matching. The template can access request-derived variables such as query/body data, headers, cookies, and route variables, and each Defined Value can specify enabled Lava commands ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).

Agent inspection steps:

1. Navigate to `Admin Tools > General Settings > Defined Types`.
2. Locate the Lava webhook Defined Type used by the instance.
3. Inspect each Defined Value: value/path, verb, enabled flag, template, commands, response content type, and any security-related attributes.
4. Verify whether route matching uses regex.
5. Test GET/POST/body/header handling with non-sensitive data.
6. Confirm the endpoint does not expose private data without authentication or signature validation.

### Remote Lava REST Endpoint

Remote Lava takes a Lava template as input and returns rendered output. The docs warn that using it from browser JavaScript can expose endpoint and API key details; the request runs as the person associated with the API key ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)). A community VS Code recipe shows the same identity caveat for remote preview tooling and notes that some commands may be restricted on the endpoint ([Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456)).

Agent inspection steps:

- Identify the REST key or API key.
- Open the person profile associated with that REST key.
- Inspect security roles and account confirmation.
- Verify whether remote execution is server-side only.
- Do not expose keys in public JavaScript.
- Confirm which commands are blocked or enabled for the endpoint in that Rock version.

## 6. Primary Entities And Relationships

### LavaShortcode

`LavaShortcode` is the central entity for reusable `{[ ... ]}` tags. Source code places it in the CMS domain and maps it to the `LavaShortcode` table ([LavaShortCode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.cs)). It relates to:

- `Category`: many-to-many association for organizing shortcodes.
- `Attribute` / `AttributeValue`: shortcode entity attributes can exist because the detail block loads qualified attributes.
- `LavaShortcodeCache`: runtime cache object.
- Admin blocks: `Lava Shortcode List` and `Lava Shortcode Detail`.
- Invocation sites: HTML blocks, content items, communications, workflows, mobile templates, webhooks, and other Lava-enabled areas.

Operational relationship:

```text
LavaShortcode
  has TagName
  has TagType
  has Markup
  has Parameters
  has EnabledLavaCommands
  has ShortcodeScopeBehavior
  belongs to zero or more Categories
  may have entity attributes
  is cached by LavaShortcodeCache
  is invoked by content using {[ tagname ... ]}
```

### Block, Page, Site, Theme, And Include Files

Lava often lives in block settings but can delegate to files through `include`. The include tag can read a file and use its content as a template. A single `~` maps to application root; `~~` maps to the current theme directory ([Include](https://community.rockrms.com/lava/tags/include-tags)). This matters because the visible block may only contain:

```liquid
{% include '~~/Assets/Lava/PageNav.lava' %}
```

An agent must then inspect the theme asset file, not only the block's content. In a multi-site Rock environment, `~~` depends on the current theme, so the same include path can resolve differently across sites.

### Entity Commands And Rock Models

The entity command system exposes Rock model types as Lava commands. The command name is the lower-case entity name, such as `person` or `group`, and the default iterator is `<entityName>Items` ([Entity](https://community.rockrms.com/lava/commands/entity-commands)). Plugin entities can register additional commands. The `taglist` administrative command can list registered Lava commands and is especially useful for discovering plugin entity command names ([Tag List](https://community.rockrms.com/lava/commands/taglist-commands)).

For live verification:

- Use Model Map for fields and relationships where available.
- Use `taglist` only in a safe admin context.
- Confirm entity type names in `EntityType`.
- Check whether plugin commands are present.
- Verify security behavior for the queried entity.

### Attribute And AttributeValue

Attributes are core to Rock extensibility and Lava access. Use the `Attribute` filter rather than legacy direct property-style attribute access. For example:

```liquid
{{ Person | Attribute:'BaptismDate' }}
```

The attribute filter can return formatted values or properties of object-valued attributes. Global attributes use `'Global' | Attribute:'Key'`, and system settings can be accessed with `'SystemSetting' | Attribute:'Key'` in specialized contexts ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)). Rock v17 increased attribute security enforcement, and v17.5 added a third optional parameter to bypass attribute security when explicitly appropriate; verify the live version and data sensitivity before using that bypass ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent rule: if a template uses `.AttributeValues`, `securityenabled:'false'`, or `Attribute:'Key','',false`, treat it as an intentional security bypass and document why it is acceptable.

### Workflow, Workflow Type, Activity Type, And Attributes

`workflowactivate` can launch a workflow or activate an activity on an existing workflow. It exposes `Workflow`, `Activity`, and `Error` variables inside the command block, and extra command key/value pairs are interpreted as workflow or activity attribute values ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)). The command requires workflow type and activity type identifiers; the documentation says these can be found on the workflow configuration screen.

Operational relationship:

```text
WorkflowType
  defines Workflow
  contains ActivityType definitions
  contains Workflow Attributes

Workflow
  instance launched by workflowactivate
  can receive attribute values from command parameters

Activity
  instance activated by workflowactivate
  can receive activity attribute values
```

Verify attribute stored values for each field type before setting them from Lava. The source pack points to workflows-and-Lava documentation for field type stored values, but that page is not hydrated here; inspect the live field type and workflow action behavior rather than guessing.

### Interaction Records

Lava can write interactions through multiple commands:

- `interactionwrite` for general interaction logging.
- `interactioncontentchannelitemwrite` for content channel item interactions.
- `interactionintentwrite` for intent interactions.

These commands relate Lava output to Rock's analytics/engagement model. They commonly accept operation, summary, person alias, UTM-like campaign/source/medium/content/term fields, and entity/channel/component identifiers depending on command ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).

Operational checks:

- Verify the person alias is correct.
- Avoid logging duplicate interactions if a template is cached, rerendered, or executed under Fluid verification.
- Confirm the target channel/intent/content item IDs.
- Use summary and operation consistently for reporting.
- Test high-traffic pages for write volume.

### Devices And Printers

The `printzpl` command can send ZPL instructions to Zebra label printers. It can target a configured Rock `Device` by `deviceid` or a printer IP address, optionally including a port ([Print ZPL](https://community.rockrms.com/lava/commands/print-zpl)). This is a side-effecting command. It does not render visible page output; it sends the processed ZPL to the printer.

Operational checks:

- Verify printer device records and network reachability.
- Validate ZPL with test labels.
- Avoid executing in preview or Fluid verification contexts if duplicate prints would matter.
- Ensure only trusted staff contexts enable this command.
- Sanitize user-provided label text to avoid malformed ZPL.

### Search Index Documents

The `search` command uses Rock Universal Search and returns search result documents. It supports parameters such as `query`, `entities`, `fieldcriteria`, `criteriasearchtype`, `searchtype`, `limit`, `offset`, and `iterator` ([Search](https://community.rockrms.com/lava/commands/search-commands)). Search command reliability depends on Universal Search configuration and index freshness.

Operational checks:

- Verify the index exists and is current.
- Verify entity types included in search.
- Use `limit` and `offset` for predictable pagination.
- Use `iterator` to avoid variable collisions in larger templates.

## 7. Common Lava Workflows

### Rendering Personalized CMS Content

Typical use:

```liquid
{% if CurrentPerson %}
<p>Welcome, {{ CurrentPerson.NickName }}.</p>
{% else %}
<p>Welcome.</p>
{% endif %}
```

Agent checks:

- Is `CurrentPerson` available in this context?
- Does the page allow anonymous users?
- Is output escaped where needed?
- Is block caching enabled in a way that could leak one user's name to another?
- If caching is used, is personalization protected with a two-pass cache pattern or moved outside the cached fragment?

The cache documentation describes a two-pass pattern using `raw` to cache expensive data while preserving later personalized merge behavior ([Cache](https://community.rockrms.com/lava/commands/cache-commands), [Raw](https://community.rockrms.com/lava/tags/raw-tags)).

### Querying Rock Entities

Basic entity command pattern:

```liquid
{% group where:'GroupTypeId == 25' sort:'Name' iterator:'groups' securityenabled:'false' %}
  {% for group in groups %}
    {{ group.Name }}<br>
  {% endfor %}
{% endgroup %}
```

Agent checks:

- Is `RockEntity` enabled?
- Is the entity command name correct?
- Does `id` override other selection parameters?
- Is `securityenabled:'false'` justified?
- Does the query need `limit`, `offset`, `select`, `include`, or `disableattributeprefetch` for performance?
- Are attribute values prefetched only when needed?
- Does `where` include user input? If so, prefer safer patterns or validate inputs.

The entity docs recommend disabling security when the author is confident it is not needed because security checks can affect performance, but that is a review decision, not a default ([Entity](https://community.rockrms.com/lava/commands/entity-commands)).

### Building A Dynamic Report Page

A common pattern combines Page Parameter Filter, Dynamic Data, entity commands, SQL, shortcodes, and campus/person filters. Community examples use Lava and SQL to add "All Campuses" behavior or person-specific default campus logic ([Slicker Campus Filters](https://community.rockrms.com/recipes/393)). Use recipes as patterns, then verify the live data model.

Agent checks:

- Which page parameters are public?
- Are parameter values validated?
- Is SQL parameterized?
- Does the page respect campus security expectations?
- Are result counts limited?
- Is the output cached appropriately?
- Does the page work when no filter is selected?

### Launching A Workflow From Lava

Use `workflowactivate` when a rendered action should create or advance a workflow:

```liquid
{% workflowactivate workflowtype:'21' requester:'{{ CurrentPerson.PrimaryAlias.Guid }}' %}
  {% if Error %}
    {{ Error }}
  {% else %}
    Created request #{{ Workflow.Id }}.
  {% endif %}
{% endworkflowactivate %}
```

Agent checks:

- Is `WorkflowActivate` enabled?
- Is the workflow type ID stable in this instance?
- Would a GUID be safer than an integer ID?
- Are workflow attributes supplied in the stored format expected by their field type?
- Can the template execute multiple times?
- Should the action be moved behind a form, endpoint, or Helix flow for better validation?

### Creating A Lava API Or Webhook

Lava APIs are configured as Defined Values and respond with the rendered Lava template. The docs warn that these webhooks do not inherently provide security, so agents must design the security model explicitly ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).

Agent checks:

- Defined Type and Defined Value path.
- HTTP method/verb.
- Route regex behavior.
- Template content.
- Enabled commands.
- Response content type.
- Header and body handling.
- Authentication, token, signature, or IP restrictions.
- Rate limiting or abuse risk.
- Sensitive fields in output.

A community iCal recipe shows a Lava webhook returning `text/calendar` and enabling Rock Entity to generate `.ics` output from event information ([Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file)). Treat that as a useful pattern, then validate response headers and access controls.

### Formatting Data With Shortcodes

Shortcodes are ideal when staff need a simple token but the implementation requires detailed Lava. Examples from community recipes include address formatting, pagination, countdowns, copy-link widgets, media embeds, translations, placement group labels, and attendance summaries ([Address Format Lava Shortcode](https://community.rockrms.com/recipes/467), [Content Pagination Shortcode](https://community.rockrms.com/recipes/242), [Countdown Timer - Shortcode](https://community.rockrms.com/recipes/505), [Easy Copy Url Shortcode](https://community.rockrms.com/recipes/408), [SoundCloud Shortcode](https://community.rockrms.com/recipes/509), [Lava Shortcode for Placement Groups on Check In](https://community.rockrms.com/recipes/386), [Lava shortcode to show last group attendance](https://community.rockrms.com/recipes/290)).

Agent checks:

- Is it inline or block?
- Are parameter keys lowercase?
- Are defaults documented?
- Are commands enabled only inside the shortcode when needed?
- Does it return safe HTML/JSON/text?
- Does it need isolated or shared scope?
- Does it handle empty/missing input?
- Does it work under Fluid?
- Is the recipe code adapted to local entity IDs and security requirements?

### Calling External APIs

The `webrequest` command supports REST-like requests, parameters, headers, method, basic authentication, body, request content type, response content type, return variable, and timeout ([Web Request](https://community.rockrms.com/lava/commands/web-request-commands)). It defaults response parsing toward JSON but can handle XML or HTML depending on parameterization.

Agent checks:

- Is `WebRequest` enabled?
- Are secrets stored in Global Attributes or secured settings rather than hard-coded?
- Is the request server-side?
- Is user input encoded?
- Is timeout appropriate?
- Is failure handled?
- Is response structure inspected with `ToJSON` during development only?
- Is external call volume safe for page traffic?

### Adding Page-Level CSS

The `stylesheet` command places CSS in the page header and can accept an `id` to avoid duplicate insertion. It also has parameters such as `compile`, `import`, and cache duration, though docs recommend not relying on LESS compile because deprecation is expected ([Stylesheet](https://community.rockrms.com/lava/commands/stylesheet-commands)).

Agent checks:

- Prefer theme or page-level CSS files for durable styling.
- Use `stylesheet` for contextual CSS that depends on Lava values.
- Use `id` when the same template may render multiple times.
- Avoid heavy dynamic CSS on high-traffic pages.
- Verify the result after a full page reload.

## 8. Commands Deep Dive

### Command Enablement

Commands are not automatically available everywhere. The official command guide emphasizes explicit enablement and notes default commands for contexts without individual settings ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)). Agents should classify enabled commands by risk:

**Low-risk display/support commands**

- `Cache`
- `Stylesheet`
- `Search` if search output is not sensitive
- `SetCulture`

**Data-read commands**

- `RockEntity` / entity commands
- `Sql` read-only usage
- `AdaptiveMessage`
- `Calendar Events`
- `Event Scheduled Instance`

**External/system commands**

- `WebRequest`
- `PrintZPL`
- `HTTP Response`
- `Render Lava Endpoint`

**Write-capable commands**

- `WorkflowActivate`
- `InteractionWrite`
- `InteractionContentChannelItemWrite`
- `InteractionIntentWrite`
- `ModifyEntity`
- `DeleteEntity`
- `DBTransaction`
- data-modifying `Sql`

The list of available commands changes by version and plugins. Use `taglist` in an admin context when command names are uncertain ([Tag List](https://community.rockrms.com/lava/commands/taglist-commands)).

### Entity Command

The entity command is the primary read mechanism for Rock data. It provides a consistent command pattern for model entities ([Entity](https://community.rockrms.com/lava/commands/entity-commands)).

Important parameters and behavior:

- `where`: Filters entities with a query expression.
- `id`: Retrieves one entity and takes precedence over `where`, `dataview`, and `dynamicparameters`.
- `ids`: Retrieves a list by IDs.
- `dataview`: Uses a Rock Data View as the source filter.
- `entitysearch`: v17-era search selection; verify syntax live.
- `expression`: Fluid-era expression support from v13.
- `sort`: Sort order.
- `limit`: Maximum rows.
- `offset`: Rows to skip.
- `dynamicparameters`: Pulls query string values into command parameters.
- `iterator`: Overrides the default `<entityName>Items` variable.
- `count`: Returns count behavior; verify exact output variable in live docs.
- `securityenabled`: Controls entity security checks; person command defaults differ because person model has different security behavior.
- `lazyloadenabled`: Fluid-era lazy loading behavior from v13.
- `include`: Eager-loads related data; v13 Fluid.
- `select`: Projects fields; v13 Fluid.
- `selectmany`: Flattens related collections; v13 Fluid.
- `groupby`: Groups results; v13 Fluid.
- `disableattributeprefetch`: v15 parameter for attribute prefetch behavior.
- `prefetchattributes`: v15 parameter for loading selected attributes.

Operational guidance:

- Use `id` for direct retrieval and do not mix it with `where`.
- Use `iterator` in complex templates to prevent variable collisions.
- Use `limit` by default on public pages.
- Use `select` for large collections where only a few fields are needed.
- Use `securityenabled:'false'` only when the page's audience and data sensitivity are reviewed.
- Avoid `dynamicparameters` unless query string input is constrained and safe.
- For plugins, confirm command names with `taglist`.

### SQL Command

The `sql` command executes SQL and returns results to a Lava variable. It supports reads, writes, parameters, custom return variable names, command statements, timeout, and aggregate functions ([SQL](https://community.rockrms.com/lava/commands/sql-commands)).

Key parameters:

- `return`: Changes the result variable from default `results`.
- `statement:'command'`: Used when executing non-query SQL and returning affected row count.
- Arbitrary parameter pairs: Passed into SQL as named parameters except reserved names such as `statement` and `return`.
- `timeout`: v12-era support for command timeout.

Safe pattern:

```liquid
{% assign requestedLastName = PageParameter.LastName | Trim %}

{% sql return:'people' lastName:'{{ requestedLastName }}' timeout:'30' %}
SELECT [Id], [NickName], [LastName]
FROM [Person]
WHERE [LastName] = @lastName
ORDER BY [LastName], [NickName]
{% endsql %}

{% for person in people %}
  {{ person.NickName }} {{ person.LastName }}<br>
{% endfor %}
```

Operational warnings:

- SQL injection is the primary risk. Use parameters for user-influenced values.
- Data-changing statements can run if command usage and context permit it.
- The docs state destructive statements are possible through Lava SQL; do not enable `Sql` casually ([SQL](https://community.rockrms.com/lava/commands/sql-commands)).
- If SQL changes data directly, Rock cache may not know about the change; clear relevant cache explicitly.
- Data-modifying Lava may execute twice under Fluid verification.
- Public pages should not run unbounded SQL.
- Use Rock's reporting SQL command block for admin investigation, but note the source code shows selection-query handling and rollback behavior for disallowed modifications depending on settings ([SqlCommand.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx.cs), [SqlCommand.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx)).

### Cache Command

The `cache` command stores rendered output in Rock's memory cache. It supports keys, duration, two-pass rendering, tags, and max cache size ([Cache](https://community.rockrms.com/lava/commands/cache-commands)).

Key parameters:

- `key`: Cache key.
- `duration`: Cache duration.
- `twopass`: Render cached output through Lava again.
- `tags`: Comma-delimited cache tags for grouped invalidation.
- `maxcachesize`: Limit for cache item size.

Use cache when:

- Entity/SQL queries are expensive.
- External calls are slow.
- Public content changes infrequently.
- Search or content lists are reused often.

Avoid or carefully design cache when:

- Output contains `CurrentPerson`.
- Output contains security-dependent data.
- The template writes interactions, workflows, or database changes.
- The cache key does not include all inputs that affect output.
- Large HTML or JSON payloads would consume significant memory.

For personalization, use two-pass caching carefully: cache the expensive shared part, preserve user-specific Lava with `raw`, and render it on the second pass ([Cache](https://community.rockrms.com/lava/commands/cache-commands), [Raw](https://community.rockrms.com/lava/tags/raw-tags)).

### Web Request Command

The `webrequest` command calls remote HTTP endpoints and returns parsed results. It supports URL, query parameters, headers, HTTP method, basic authentication, body, request/response content types, custom return variable, and timeout ([Web Request](https://community.rockrms.com/lava/commands/web-request-commands)).

Agent pattern:

```liquid
{% capture requestBody %}
{
  "email": {{ CurrentPerson.Email | ToJSON }},
  "source": "rock"
}
{% endcapture %}

{% assign requestBody = requestBody | Trim | StripNewLines %}

{% webrequest
  url:'https://example.invalid/api'
  method:'POST'
  body:'{{ requestBody }}'
  requestcontenttype:'application/json'
  responsecontenttype:'JSON'
  timeout:'8000'
  return:'apiResult' %}
{% endwebrequest %}
```

Checks:

- Do not expose secrets in client-side source.
- Store secrets in secure attributes or settings.
- Serialize JSON with `ToJSON` instead of hand-concatenating user input.
- Handle non-200 responses; source excerpts show successful processing around HTTP OK in source code, but exact current behavior should be verified in the live version ([WebRequestBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WebRequestBlock.cs)).
- Set a timeout for page-render paths.
- Cache only safe responses.

### Workflow Activate Command

`workflowactivate` launches workflows or activates activities. Key parameters include `workflowtype`, `workflowid`, `workflowname`, and `activitytype`; additional key/value pairs map to workflow/activity attributes ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)).

Use it for:

- Creating internal requests from page actions.
- Triggering follow-up processes.
- Launching approval workflows.
- Adding activity to an existing workflow.

Avoid it when:

- A public anonymous page can trigger unbounded workflows.
- Attribute values are user-provided and unvalidated.
- Duplicate execution would create duplicate work.
- A full workflow entry form would be safer and more auditable.

### Interaction Write Commands

Use these for analytics records:

- `interactionwrite`: general-purpose interaction logging.
- `interactioncontentchannelitemwrite`: content channel item interactions.
- `interactionintentwrite`: intent interactions.

The content and intent write commands support optional UTM-style fields in addition to core identifiers ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).

Agent checks:

- Do not write interactions from cached output unless intentional.
- Include enough fields to make reporting useful.
- Avoid logging private data in summary or data fields.
- Verify defined values and intent IDs.
- Confirm person alias mapping.

### Search Command

Use `search` to query Universal Search from Lava. Parameters include `query`, `entities`, `fieldcriteria`, `criteriasearchtype`, `searchtype`, `limit`, `offset`, and `iterator` ([Search](https://community.rockrms.com/lava/commands/search-commands)).

Use search when:

- The user-facing behavior is search-like.
- Multiple entity types or indexed fields matter.
- Ranking is more important than exact relational filtering.

Prefer entity commands or SQL when:

- Exact predicates are required.
- Security and data joins must be explicit.
- Search index freshness is uncertain.
- You need transactional or real-time data.

### Adaptive Message Command

`adaptivemessage` retrieves personalized adaptive messages. It supports message mode and category mode. Parameters include `messagekey`, `adaptationspermessage`, `categoryid`, `maxadaptations`, and `trackviews` ([Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands)).

Agent checks:

- Confirm Adaptive Message configuration.
- Verify attributes such as call-to-action fields exist on adaptations.
- Decide whether `trackviews` should write analytics.
- Handle zero matching adaptations.
- Do not cache personalized results broadly.

### Set Culture Command

`setculture` controls culture/locale behavior for specific filters. It applies to conversion and formatting filters such as `AsDateTimeUtc`, `AsDateTime`, `AsDecimal`, `AsDouble`, `AsInteger`, `Date`, `Format`, and `FormatAsCurrency`. The docs warn not to nest `setculture` blocks ([Set Culture](https://community.rockrms.com/lava/commands/setculture-commands)).

Use it when:

- A public page must format dates/numbers consistently.
- A webhook returns machine-readable dates.
- A multi-language context needs deterministic parsing.

Check:

- Culture codes supported by the running framework.
- Whether values are stored as strings or typed values.
- Whether browser/server culture is otherwise affecting output.

### Stylesheet Command

`stylesheet` injects CSS into the header and supports `id`, `compile`, `import`, and cache duration. The docs recommend avoiding reliance on LESS compile because deprecation is expected ([Stylesheet](https://community.rockrms.com/lava/commands/stylesheet-commands)).

Use it for:

- Lava-dependent CSS values.
- One-off page-specific styles.
- Avoiding inline style blocks in the body.

Do not use it as a substitute for maintaining theme CSS when the style is stable.

### Print ZPL Command

`printzpl` sends ZPL to a Zebra printer by Rock device ID or IP address. It accepts `deviceid` and `ipaddress`, and the Lava inside the block is merged before sending ([Print ZPL](https://community.rockrms.com/lava/commands/print-zpl)).

Checks:

- Device/IP target.
- Network path.
- Printer language compatibility.
- Duplicate execution risk.
- Malformed ZPL risk.
- User input escaping.

### Observe Tag/Command

`observe` wraps contained Lava in an observability activity with a required `name` and optional tag parameters. It can group timing and database-call details for performance investigation ([Observe](https://community.rockrms.com/lava/tags/observe)).

Use it when:

- A page or shortcode is slow.
- You need to measure expensive entity/SQL blocks.
- You want feature/version tags around a Lava fragment.

Check:

- Values in observe tags should be escaped if they can contain quotes.
- Remove or minimize noisy observability on stable high-traffic templates unless the instance expects it.

### Tag List Command

`taglist` lists registered Lava commands on the server and helps discover plugin-provided entity command names ([Tag List](https://community.rockrms.com/lava/commands/taglist-commands)). Use it only in admin contexts because it reveals system capabilities.

### Helix Commands And Data Modification

The Helix developer docs point Lava authors toward newer commands for deleting entities, modifying entities, DB transactions, HTTP responses, and render endpoints, now documented in Lava command pages ([Lava Commands](https://community.rockrms.com/developer/helix/lava-commands), [Helix](https://community.rockrms.com/developer/helix)). The Helix overview says the platform is early alpha in the hydrated source, so agents must verify current stability and version before building production workflows on it.

Operational rule: any Lava that modifies entities or controls HTTP responses should be reviewed like application code, with authorization, validation, logging, rollback behavior, and tests.

## 9. Filters Deep Dive

Filters transform values. They are often safer than commands because they do not usually perform broad side effects, but some filters expose data or security-sensitive behavior. Always inspect filter input, output context, and version.

### Attribute Filter

The `Attribute` filter is the correct way to access Rock attributes in modern Lava ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)).

Common patterns:

```liquid
{{ CurrentPerson | Attribute:'BaptismDate' }}
{{ CurrentPerson | Attribute:'Mentor','LastName' }}
{{ 'Global' | Attribute:'OrganizationName' }}
{{ 'SystemSetting' | Attribute:'SomeSpecialKey' }}
```

Important behaviors:

- The first parameter is the attribute key.
- A second qualifier can access a property of an object-valued attribute.
- Global attributes use the string `'Global'`.
- System settings use `'SystemSetting'` in specialized contexts.
- `.AttributeValues` can be looped for inspection but may bypass normal security checks.
- Rock v17+ tightened attribute security; v17.5 added an explicit bypass parameter.

Agent checks:

- Is the attribute key correct?
- Does the entity have attributes loaded?
- Is the attribute value formatted or raw?
- Is the attribute field type object-valued?
- Is security bypass used?
- Does the output expose sensitive data?

### Legacy Attribute Syntax

A community recipe explains "legacy Lava" as old attribute access that treated attributes like direct properties. The modern pattern uses `Attribute` filter syntax. The recipe recommends finding warnings in the Exception List and tracing them back to page blocks, workflows, or other locations ([Finding and Fixing Legacy Lava](https://community.rockrms.com/recipes/107)).

Agent remediation path:

1. Inspect Exception List for legacy Lava warnings.
2. Open occurrence details.
3. Identify source location: page block, workflow, communication, etc.
4. Replace direct attribute-like access with `| Attribute:'Key'`.
5. Test under Fluid.
6. Search other stored templates for the same pattern.
7. Do not run bulk replacements without reviewing field/property ambiguity.

### Date Filters

The source pack includes unit and integration test snippets for date filters. Rock tests note that Lava date filters assume local `DateTime` values are expressed in the configured Rock organization timezone, not necessarily the server's local timezone ([DateFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests/Lava/Filters/DateFilterTests.cs), [DateFilterTests integration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Filters/DateFilterTests.cs)).

Operational guidance:

- Prefer UTC or `DateTimeOffset` for machine-readable values.
- Use `AsDateTimeUtc` when converting to UTC.
- Use `setculture` when parsing ambiguous date strings.
- Avoid ambiguous strings like `01/02/2020` unless culture is controlled.
- For webhooks, output ISO-like formats when possible.
- Verify organization timezone in Global Attributes/System Settings before diagnosing date offsets.

### Person Filters

Person-related filters can derive campus, address, tokens, and other person-specific values. Source test snippets show `NearestCampus` behavior and person token restrictions tied to account protection profile settings ([PersonFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Filters/PersonFilterTests.cs)). The exact filter list should be checked in current Lava docs or live docs, but operationally:

- Person filters may depend on sample/live data such as addresses, geocoding, campuses, and account protection settings.
- Token-creating filters are security-sensitive.
- Campus filters can exclude campuses lacking needed geocode data depending on the filter.
- Do not expose person tokens on public pages without confirming account protection behavior.

### Text Filters

Text filters transform strings, encode output, manipulate case, pluralize, strip newlines, and prepare JSON/body content. Source snippets include text filter tests and webrequest docs show `Trim` plus `StripNewLines` for request body preparation ([TextFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests/Lava/Filters/TextFilterTests.cs), [Web Request](https://community.rockrms.com/lava/commands/web-request-commands)).

Agent guidance:

- Use `Escape` in mobile text strings and contexts where quotes or ampersands can break markup ([Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)).
- Use `ToJSON` for JSON values.
- Use `UrlEncode` or equivalent filters where URL parameters are built; verify exact filter name live if not in source pack.
- Use `Trim` and `StripNewLines` for compact request bodies.
- Avoid using text filters to patch unsafe SQL; use SQL parameters.

### Array And Sorting Filters

Fluid changes sorting behavior. The Fluid differences doc says array sorting with old sort direction parameters should move to `OrderBy`, while entity command sorting remains a separate command capability. Fluid's `Sort` is case-sensitive, and `SortNatural` may be preferable for human-friendly ordering ([Fluid Differences](https://community.rockrms.com/lava/fluid/differences)).

Agent checks:

- Is the value an entity command result, array, or string split?
- Is sorting case-sensitive?
- Does the template run under Fluid?
- Should `OrderBy` be used instead of old `Sort` syntax?
- Are nulls handled consistently?

### JSON Filters

Source examples use `ToJSON` and `FromJSON` patterns in community recipes and webrequest docs. These are important for safe API output and request bodies ([Web Request](https://community.rockrms.com/lava/commands/web-request-commands), [Address Format Lava Shortcode](https://community.rockrms.com/recipes/467)).

Agent guidance:

- Use `ToJSON` for string values inside JSON.
- Return JSON from webhooks with a proper response content type.
- Avoid manually quoting user input.
- Validate whether `FromJSON` is available and enabled in the current version before relying on it.

### Culture-Affected Filters

`setculture` only affects a specific list of filters: date/time conversions, numeric conversions, date formatting, general formatting, and currency formatting ([Set Culture](https://community.rockrms.com/lava/commands/setculture-commands)). If another filter's output seems culture-sensitive, verify live rather than assuming `setculture` controls it.

### Mobile Lava Filters

Rock Mobile docs say filters available for local mobile-shell processing are marked in docs with compatible shell version, and recommend `Escape` for Lava text strings in mobile applications, especially user-entered values or values containing `&` or quotes ([Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)). Agents should distinguish:

- Server-rendered Lava in mobile blocks.
- Client-processed Lava when `Process Lava On Client` is enabled.
- Merge fields available locally: `PageParameter`, `CurrentPerson`, `Device`, `PageValues`, `AppValues`, `DeviceTheme`, and server-provided variables, depending on configuration.
- Mobile-specific commands such as `setpagevalue` and `setappvalue`, if available in the live version.

## 10. Shortcodes Deep Dive

### Why Shortcodes Exist

Shortcodes replace complex Lava with a concise tag. They make content easier for staff to use and standardize templates across pages, communications, and workflows ([Intro to Shortcodes](https://community.rockrms.com/lava/shortcodes/intro-to-shortcodes)).

Good shortcode use cases:

- Embedding media with safe defaults.
- Formatting addresses, dates, links, or cards.
- Rendering reusable panels or layout fragments.
- Generating pagination controls.
- Showing scheduled content.
- Wrapping complicated SQL/entity logic for staff.
- Adding analytics or interactions consistently.
- Providing mobile or CMS patterns that should not be hand-coded repeatedly.

Poor shortcode use cases:

- One-off code that is clearer inline.
- Logic that needs formal validation, audit, or transactions.
- A place to hide unsafe SQL.
- Public writes without authorization.
- Complex applications better served by Helix, blocks, workflows, or custom plugins.

### Inline Versus Block

Inline shortcodes have no closing tag and are suited to small parameter-driven output. Block shortcodes use a closing tag and receive the enclosed content. The docs stress that changing shortcode type later breaks callers, so choose deliberately ([Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes)).

Choose inline when:

- All configuration fits in a few parameters.
- No repeated child sections are needed.
- No large HTML content is passed.
- Staff should use it like a formatter or embed.

Choose block when:

- The user passes rich HTML/content.
- The shortcode needs nested configuration.
- Repeating child items are needed.
- The content itself should be rendered inside a wrapper.

### Shortcode Configuration Fields

In `Admin Tools > CMS Configuration > Lava Shortcodes`, inspect:

- `Name`
- `Tag Name`
- `Categories`
- `Active`
- `Tag Type`
- `Description`
- `Documentation`
- `Shortcode Markup`
- `Parameters`
- `Enabled Lava Commands`
- `Variable Scope Context` or `Shortcode Scope Behavior`, depending on version
- Entity attributes if present

The source model and view models confirm many of these fields, including `ShortcodeScopeBehavior` ([LavaShortCode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.cs), [LavaShortcodeDetailOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaShortcodeDetail/LavaShortcodeDetailOptionsBag.cs)).

### Parameters

Parameter keys should be lowercase. The authoring docs warn that uppercase keys can behave unexpectedly and return defaults rather than caller-provided values ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).

Parameter design rules:

- Use lowercase keys.
- Provide safe defaults.
- Document type and allowed values.
- Convert booleans with `AsBoolean`.
- Validate IDs before use.
- Treat all parameters as untrusted unless only admins can call the shortcode.
- Do not interpolate parameters directly into SQL.
- If a parameter controls CSS/HTML, restrict allowed values.

### Enabled Commands Inside Shortcodes

A shortcode can enable commands internally, independent of the block that calls it ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)). This is useful because callers do not need broad command access, but it also means a harmless-looking shortcode can run SQL or entity queries.

Agent review:

- Open the shortcode record, not just the calling page.
- Inspect `Enabled Lava Commands`.
- Confirm commands are required by markup.
- Remove unused commands.
- For `Sql`, verify parameterization.
- For `RockEntity` with security disabled, document why.
- For write commands, review authorization and duplicate execution.

### Block Content

Block shortcodes receive enclosed content as `blockContent`. Rock runs Lava across block content by default; passing a parameter `disablelavamerge:'true'` can disable that behavior ([The Power of Shortcode Blocks](https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks)).

Agent checks:

- Does `blockContent` contain user-entered HTML?
- Should Lava inside the content be executed?
- Could executing nested Lava expose data or enable command-like effects?
- Is `disablelavamerge` documented for callers?
- Does the shortcode escape or trust block content?

### Block Configuration

Block shortcodes can parse nested configuration using `[[ itemname parameter:'value' ]] ... [[ enditemname ]]` syntax. Rock removes parsed configuration from `blockContent` and exposes variables to the template ([The Power of Shortcode Blocks](https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks)).

Use this for structured repeating items such as map markers, tabs, slides, or cards. Keep documentation clear because staff must know the nested shape.

### Passing Objects

Rock v10+ supports passing Lava variables as shortcode parameters by omitting quotes. Dot notation for nested object expressions has limitations in this context ([Passing in Objects](https://community.rockrms.com/lava/shortcodes/passing-in-objects)).

Good pattern:

```liquid
{% group where:'GroupTypeId == 25' iterator:'groups' %}
  {[ group_list groups:groups ]}
{% endgroup %}
```

Avoid relying on:

```liquid
{[ group_list groups:ParentObject.groups ]}
```

unless verified in the current version and context.

### Scope Behavior

Shortcode variable scope is version-sensitive. The authoring docs describe a `Variable Scope Context` with isolated/shared options, and v19.1 release notes describe a new `Shortcode Scope Behavior` property that controls whether variables inside a shortcode are isolated or shared with surrounding Lava ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent guidance:

- Prefer isolated scope for most shortcodes.
- Use shared scope only when the shortcode intentionally returns values to surrounding Lava.
- Test nested shortcode behavior; v19.1 release notes mention a fix for nested shortcodes inheriting outer `blockContent` unintentionally ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Check live version because labels and implementation may differ across v12-v19.

### Shortcode Source-Code Landmarks

Use these source files when code-level confirmation is needed:

- `Rock/Model/CMS/LavaShortCode/LavaShortCode.cs`: entity fields and table mapping ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.cs)).
- `Rock/Model/CMS/LavaShortCode/LavaShortCode.Logic.cs`: cache update behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.Logic.cs)).
- `Rock.Blocks/Cms/LavaShortcodeDetail.cs`: admin detail behavior, options, duplicate tag validation ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeDetail.cs)).
- `Rock.Blocks/Cms/LavaShortcodeList.cs`: list initialization and category handling ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeList.cs)).
- `Rock.Lava/Core/Shortcodes/DynamicShortcodeBlock.cs`: block shortcode implementation class ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Lava/Core/Shortcodes/DynamicShortcodeBlock.cs)).
- `Dev Tools/Sql/CodeGen_LavaShortCodeMigrationSql.sql`: migration helper for shortcode records, useful for understanding deployment/export patterns ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/CodeGen_LavaShortCodeMigrationSql.sql)).

## 11. Related Rock Areas: Cms, Workflows, Sql, Security

### CMS

Lava is deeply integrated into CMS. It appears in HTML blocks, themes, include files, content channel item templates, shortcodes, stylesheets, page parameters, public pages, and internal admin pages. CMS agents should always trace:

```text
Page -> Layout -> Zone -> Block -> Block Settings -> Lava Template
                                    -> Shortcodes
                                    -> Include Files
                                    -> Enabled Commands
                                    -> Cache Settings
```

For content channel pages, also inspect:

```text
Content Channel -> Content Channel Type -> Item Attributes -> Item Content -> Detail/List Blocks -> Lava
```

When a page output is wrong, the visible page is the symptom, not necessarily the source.

### Workflows

Workflows use Lava in action attributes, forms, notifications, entry blocks, and `workflowactivate` calls. Workflow attribute values often use stored internal representations, not display labels. The `workflowactivate` docs explicitly warn that attribute value types matter ([Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)).

Agent checks:

- Workflow Type ID or Guid.
- Activity Type ID or Guid.
- Attribute keys and field types.
- Stored value format.
- Lava commands enabled in workflow context.
- Whether template runs as a staff user, system job, or public submitter.
- Whether output is sent externally.

Release notes also include workflow security hardening around workflow type view permissions in v19.1, so agents should verify workflow visibility and permissions on modern versions ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### SQL

SQL in Lava is powerful and dangerous. Use it when entity commands are insufficient, but keep it parameterized, bounded, and reviewed. The source-code snippet for the admin SQL Command block shows Rock distinguishes selection queries from commands and can roll back disallowed modifications depending on configuration, but that block behavior is not the same as arbitrary Lava SQL in a page ([SqlCommand.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx.cs), [SQL](https://community.rockrms.com/lava/commands/sql-commands)).

SQL guardrails:

- Never concatenate raw page parameters into SQL.
- Use SQL command parameters.
- Use `TOP`, filters, or pagination.
- Avoid writes from public pages.
- Clear Rock cache after direct writes.
- Test read-only first.
- Prefer Rock services/plugins for complex writes.
- Log and document data-modifying SQL.

### Security

Security is the recurring theme across Lava:

- Command enablement controls capability.
- Entity commands can bypass security with `securityenabled:'false'`.
- Attribute filters can bypass attribute security with an explicit parameter in newer versions.
- Remote Lava runs as a REST key's person.
- Lava webhooks may not enforce security by default.
- Shortcodes can hide enabled commands.
- Mobile client-side Lava has different data availability and escaping risks.
- Fluid verification may double-execute side effects.

Important source anchors: [Getting Started With Lava Commands](https://community.rockrms.com/lava/commands), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api), [Attributes](https://community.rockrms.com/lava/filters/attribute-filters), [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava).

## 12. Administration And Operational Guardrails

### Pre-Change Checklist

Before changing Lava in production:

1. Identify the storage location.
2. Export or record the current template.
3. Identify all shortcodes and includes it depends on.
4. Inspect enabled commands.
5. Inspect cache settings.
6. Check current Rock version.
7. Check current Lava engine.
8. Search the Exception List for related errors.
9. Decide whether the change affects anonymous users, staff, communications, workflows, APIs, or mobile.
10. Test with representative people, campuses, permissions, and missing-data scenarios.

### Command Review Checklist

For each enabled command, ask:

- Is it actually used?
- Does it read sensitive data?
- Does it write data?
- Does it call external systems?
- Does it depend on user input?
- Does it bypass security?
- Does it run per recipient or per page view?
- Does it execute in cached output?
- Could it execute twice?
- Is failure handled?

Remove unused commands. Narrow broad defaults.

### Performance Checklist

Look for:

- Entity commands without `limit`.
- SQL without filters.
- Per-row entity or SQL calls inside loops.
- Attribute access on large collections without prefetch decisions.
- External web requests on page render.
- Adaptive/personalized content without caching strategy.
- Search queries without limits.
- Shortcodes used many times per page.
- Nested shortcodes and blockContent rendering.
- Large cached payloads.

Use `observe` around suspected slow sections when available ([Observe](https://community.rockrms.com/lava/tags/observe)).

### Caching Checklist

For every cached Lava fragment:

- Does key include all inputs?
- Does output contain person-specific data?
- Does output depend on security?
- Does output depend on current date/time?
- Does output write interactions or launch workflows?
- Are tags used for invalidation?
- Is duration appropriate?
- Is the payload large?
- Is two-pass rendering needed?

### Exception List Checklist

Use exceptions to find:

- Fluid verification mismatches.
- Parse errors.
- Legacy Lava warnings.
- SQL errors.
- Null reference issues.
- Missing command authorization.
- Shortcode save/display errors.
- Webrequest failures.
- Attribute security denials.

A community recipe on legacy Lava highlights Exception List tracing as a practical way to locate old attribute syntax in pages or workflows ([Finding and Fixing Legacy Lava](https://community.rockrms.com/recipes/107)).

### Remote Execution Checklist

For remote Lava and Lava Runner-style tooling:

- Verify REST key person.
- Verify roles and security.
- Verify allowed commands.
- Do not expose key in public source.
- Use server-side proxy if needed.
- Avoid side-effect commands during preview.
- Remember `CurrentPerson` may be the key person, not the human developer ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava), [Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456)).

## 13. Developer, API, Lava, And Source-Code Landmarks

### Official Lava Documentation

Primary official entry points:

- [Lava Reference](https://community.rockrms.com/lava)
- [Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)
- [Entity Command](https://community.rockrms.com/lava/commands/entity-commands)
- [SQL Command](https://community.rockrms.com/lava/commands/sql-commands)
- [Web Request Command](https://community.rockrms.com/lava/commands/web-request-commands)
- [Cache Command](https://community.rockrms.com/lava/commands/cache-commands)
- [Shortcodes Intro](https://community.rockrms.com/lava/shortcodes/intro-to-shortcodes)
- [Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)
- [Fluid](https://community.rockrms.com/lava/fluid)
- [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)

### RockU

RockU Lava training covers concept videos for what Lava is, filters, `if`, `for`, `assign`, entity commands, SQL, web requests, execute command, and shortcodes ([RockU Lava](https://community.rockrms.com/rocku/lava)). Use this for onboarding, not as the final authority for version-specific behavior.

### Mobile Developer Docs

Mobile docs are relevant when Lava is used in Rock Mobile blocks or client processing. The mobile Lava page describes local-client availability, escaping recommendations, page/device/app values, and mobile-specific Lava commands ([Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)). Mobile block docs such as Event Item Occurrence List By Audience Lava show blocks with query parameters, block configuration, Lava templates, merge fields, and enabled commands ([Event Item Occurrence List By Audience Lava](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava)).

### Helix

Helix connects Lava, HTMX, forms, controls, endpoints, observability, and data-modifying Lava commands. The hydrated source describes it as early alpha and points command docs back to the Lava documentation ([Helix](https://community.rockrms.com/developer/helix), [Lava Commands](https://community.rockrms.com/developer/helix/lava-commands)). Verify current stability, plugin version, and production support before using.

### AI Agent Lava Tools

Rock developer docs describe Lava tools for AI agents. A Lava tool has name, description, prompt/template, and parameters; it can use entity commands or SQL and return data to the agent ([Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)). Agent-oriented guidance:

- Tool name and description are routing metadata; write them precisely.
- Prompt is executable Lava; review enabled commands.
- Parameters are untrusted inputs; validate and parameterize.
- Return structured JSON where possible.
- Keep tools narrow and auditable.
- Avoid write-capable tools unless explicitly required.

### Source Files

Use source-code snippets for implementation details:

- Entity shortcode model: [LavaShortCode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.cs)
- Shortcode cache logic: [LavaShortCode.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.Logic.cs)
- Shortcode detail block: [LavaShortcodeDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeDetail.cs)
- Shortcode list block: [LavaShortcodeList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeList.cs)
- Web request block: [WebRequestBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WebRequestBlock.cs)
- SQL command admin block: [SqlCommand.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx.cs)
- Date filter tests: [DateFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests/Lava/Filters/DateFilterTests.cs)
- Person filter tests: [PersonFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Filters/PersonFilterTests.cs)
- Text filter tests: [TextFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests/Lava/Filters/TextFilterTests.cs)
- Lava endpoint security enum: [LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)

## 14. Reporting, Analytics, And Model Map

### Reporting With Lava

Lava supports reporting through:

- Entity commands.
- SQL command.
- Search command.
- Dynamic Data blocks with Lava parameters.
- Shortcodes for reusable report UI.
- Page Parameter Filter blocks.
- Content channels and item lists.
- Metrics dashboards via community patterns.

Community recipes show practical reporting patterns: pagination shortcodes for custom lists, campus filters for dynamic reports, attendance summary shortcodes, and metrics history dashboards ([Content Pagination Shortcode](https://community.rockrms.com/recipes/242), [Slicker Campus Filters](https://community.rockrms.com/recipes/393), [Lava shortcode to show last group attendance](https://community.rockrms.com/recipes/290), [Metrics History, Maintenance & Dashboard(s)](https://community.rockrms.com/recipes/380)). Adapt these only after reviewing SQL, entity IDs, command enablement, and performance.

### Analytics With Interaction Commands

Use interaction commands to write analytics records from Lava. Choose the most specific command:

- Use `interactioncontentchannelitemwrite` when the interaction belongs to a content channel item.
- Use `interactionintentwrite` when tracking intent taxonomy.
- Use `interactionwrite` for custom/general channels.

Use consistent `operation`, `summary`, UTM fields, and entity IDs to make later reports meaningful ([Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write), [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write)).

### Model Map

The source pack references Model Map through community shortcode examples, such as the address formatter recipe pointing users to the Location model for fields ([Address Format Lava Shortcode](https://community.rockrms.com/recipes/467)). When an agent needs fields or relationships:

1. Open Model Map in the live Rock instance.
2. Search the entity type.
3. Verify property names and navigation properties.
4. Check whether attributes are separate from properties.
5. Use entity command `select` or SQL only after confirming fields.
6. If plugin models are involved, use `taglist`, Model Map, or source code.

Do not infer property names from UI labels alone.

## 15. Version And Release Caveats

### Fluid Migration

Rock v13 introduced Fluid, with DotLiquid eventually going away. The source pack says support for DotLiquid was ending with v17 ([About Lava Fluid](https://community.rockrms.com/lava/fluid), [Lava Reference](https://community.rockrms.com/lava)). Agents should verify the current live version and global engine setting.

Common Fluid differences from the source pack:

- Variables cannot start with a number; docs note this was fixed in v17 for a specific case, but avoid numeric-leading variable names anyway.
- Include parameter passing requires commas.
- Array sort direction should use `OrderBy` rather than old `Sort` direction syntax.
- `Sort` is case-sensitive in Fluid; use `SortNatural` where appropriate.
- Include scope behavior changed.
- Mixed single/double quote usage can parse differently.
- Nested comments are not supported in the same way.
- Use `and` instead of `&&`.
- Unrecognized escape sequences can error, especially in regex; use `capture` for regex expressions.
- Empty output tag behavior changed, with fixes noted in v17.
- `Split` behavior around empty/null values changed, with fixes noted in v17.
- Null comparisons are more consistent.
- `forloop.rindex` and `rindex0` discrepancy was fixed in v19 according to the differences page and release notes ([Fluid Differences](https://community.rockrms.com/lava/fluid/differences), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v10

Passing objects into shortcodes requires Rock v10 or above ([Passing in Objects](https://community.rockrms.com/lava/shortcodes/passing-in-objects)). System setting attribute access is documented as v10.3+ ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)).

### v11-v12

Interaction write commands and UTM-style parameters appear around v11/v12 in the docs ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)). SQL parameters are documented as v9 and timeout as v12 ([SQL](https://community.rockrms.com/lava/commands/sql-commands)). Authoring docs mention v12-era scope settings for shortcodes ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).

### v13

Fluid is introduced, and entity command parameters such as `expression`, `lazyloadenabled`, `include`, `select`, `selectmany`, and `groupby` are Fluid-era features ([About Lava Fluid](https://community.rockrms.com/lava/fluid), [Entity](https://community.rockrms.com/lava/commands/entity-commands)). The `lava` tag is documented as v13.7 and Fluid-only ([Lava Tag](https://community.rockrms.com/lava/tags/lava-tags)).

### v15

Entity command attribute prefetch parameters are documented around v15 ([Entity](https://community.rockrms.com/lava/commands/entity-commands)). Other attribute return values are documented v15.0+ ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)).

### v16

`observe` is documented as v16.3, and `interactionintentwrite` as v16.4 ([Observe](https://community.rockrms.com/lava/tags/observe), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).

### v17

`adaptivemessage` is documented as v17.0, entity search as v17, and the Fluid/DotLiquid transition is central around this version ([Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands), [Entity](https://community.rockrms.com/lava/commands/entity-commands), [Lava Reference](https://community.rockrms.com/lava)). Attribute security changed in v17 and v17.5 added bypass control ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v18

`setculture` is documented as v18.0 ([Set Culture](https://community.rockrms.com/lava/commands/setculture-commands)).

### v19

`printzpl` is documented as v19.0 ([Print ZPL](https://community.rockrms.com/lava/commands/print-zpl)). v19.1 release notes mention:

- Shortcode Scope Behavior property.
- refreshed Lava Shortcode List and Detail blocks using Obsidian UI components.
- shortcode save error-message fix.
- Fluid vs DotLiquid `forloop.rindex/rindex0` discrepancy fix.
- field comparison enhancements.
- security setting fixes for some Lava commands.
- nested shortcode `blockContent` leakage fix.
- date object versus string comparison fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Because v19.1 was marked beta in the hydrated release notes, verify the production version and release channel before relying on v19.1 behavior.

## 16. Implementation Playbooks

### Playbook: Add A Safe Read-Only Entity List

1. Define the audience and data sensitivity.
2. Confirm the target entity and fields in Model Map.
3. Add or edit an HTML block.
4. Enable only `RockEntity`.
5. Use `iterator`, `limit`, `sort`, and `securityenabled` intentionally.
6. Escape or format output.
7. Add cache only if output is not person/security-specific.
8. Test anonymous, staff, and no-result cases.

Template shape:

```liquid
{% group where:'IsActive == true' sort:'Name' limit:'50' iterator:'groups' %}
  {% if groups and groups != empty %}
    <ul>
    {% for group in groups %}
      <li>{{ group.Name | Escape }}</li>
    {% endfor %}
    </ul>
  {% else %}
    <p>No groups found.</p>
  {% endif %}
{% endgroup %}
```

Verify exact `where` syntax and property names live.

### Playbook: Replace Unsafe SQL With Parameterized SQL

1. Identify all user-influenced values.
2. Convert them into command parameters.
3. Reference parameters with `@name` in SQL.
4. Add `timeout`.
5. Add `return` to avoid collisions.
6. Add `TOP` or filters.
7. Test with quotes, empty values, and unexpected input.

Unsafe pattern:

```liquid
WHERE [LastName] = '{{ PageParameter.LastName }}'
```

Safer pattern:

```liquid
{% sql return:'rows' lastName:'{{ PageParameter.LastName | Trim }}' timeout:'30' %}
SELECT TOP 50 [Id], [NickName], [LastName]
FROM [Person]
WHERE [LastName] = @lastName
{% endsql %}
```

SQL parameter support is documented in the SQL command guide ([SQL](https://community.rockrms.com/lava/commands/sql-commands)).

### Playbook: Build A Reusable Shortcode

1. Decide inline or block.
2. Choose a lowercase tag name.
3. Write the staff-facing description.
4. Write technical documentation with examples.
5. Define lowercase parameters and defaults.
6. Write markup using only needed commands.
7. Enable commands inside the shortcode, not broadly in caller blocks.
8. Set isolated scope unless sharing is required.
9. Assign categories.
10. Test in an HTML block, communication, and any target context.
11. Test under Fluid and with missing parameters.
12. Document version requirements.

Use official shortcode docs as the baseline ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes), [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes)).

### Playbook: Diagnose A Broken Shortcode

1. Identify the exact shortcode invocation.
2. Open `Admin Tools > CMS Configuration > Lava Shortcodes`.
3. Confirm the shortcode is active.
4. Confirm tag name and tag type.
5. Inspect parameters and defaults.
6. Inspect enabled commands.
7. Inspect scope behavior.
8. Check for nested shortcodes and `blockContent`.
9. Check Exception List.
10. Verify whether caller uses object passing, and whether Rock version supports it.
11. Test with a minimal invocation.
12. Clear block/cache if stale output persists.

### Playbook: Migrate DotLiquid Lava To Fluid

1. Check `Lava Engine Liquid Framework`.
2. If appropriate, enable verification mode during a low-risk window.
3. Inspect exceptions.
4. Search for known differences:
   - numeric-leading variable names
   - include calls without commas
   - `&&`
   - nested comments
   - regex escapes
   - old array sort direction syntax
   - mixed quotes
   - empty output tags
   - split/null edge cases
5. Fix templates in the owning locations.
6. Review side-effecting Lava before verification mode because it may run twice.
7. Move to Fluid only after exceptions are resolved and key workflows/pages are tested.

Use Fluid docs and differences as the primary source ([About Lava Fluid](https://community.rockrms.com/lava/fluid), [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)).

### Playbook: Create A Lava Webhook

1. Define the API contract: path, method, inputs, output content type.
2. Configure the Lava webhook Defined Value.
3. Add a template with explicit request parsing.
4. Enable only required commands.
5. Add authentication or signature validation if sensitive.
6. Validate request body and query parameters.
7. Return structured JSON/XML/text/calendar as needed.
8. Test with missing/invalid inputs.
9. Log enough for diagnostics without exposing secrets.
10. Document the endpoint and owning team.

Use the Lava API docs as the authority and community iCal recipe only as an example ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api), [Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file)).

### Playbook: Add Remote Lava Preview Tooling

1. Decide whether remote rendering is necessary.
2. Create or select a REST key with minimal roles.
3. Confirm the key's person record and security.
4. Configure the tool server-side.
5. Do not expose keys in browser JavaScript.
6. Test `CurrentPerson` behavior.
7. Avoid side-effecting commands in preview templates.
8. Document command restrictions.

Use official remote Lava warnings and the VS Code recipe caveats ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava), [Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456)).

### Playbook: Add Interaction Analytics

1. Choose the specific command.
2. Identify entity/channel/intent IDs.
3. Decide person alias source.
4. Define operation and summary taxonomy.
5. Add UTM fields where useful.
6. Avoid duplicate writes from caching or repeated render.
7. Test reporting output.
8. Monitor volume.

Use interaction command docs ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).

## 17. Troubleshooting Decision Tree

### The Lava Renders Blank

Check:

1. Is the merge field available in this context?
2. Is the variable name correct and case-correct?
3. Is the entity command returning rows?
4. Did `id` override `where` unintentionally?
5. Is the shortcode active?
6. Is an include file path resolving?
7. Is output hidden by CSS?
8. Is security filtering all results?
9. Is the template cached with old empty output?
10. Is the Fluid engine treating null/empty differently?

### The Command Says It Is Not Authorized

Check:

1. Is the command enabled in the block?
2. Is it enabled in the shortcode if used inside a shortcode?
3. Is it inherited from default enabled commands?
4. Did v19.1 command security fixes alter behavior?
5. Is the command name correct?
6. Is the template executing in a context that disallows that command, such as remote Lava?
7. Does the current user or REST key person have needed security?

Sources: [Getting Started With Lava Commands](https://community.rockrms.com/lava/commands), [Rock Core Release Notes](https://www.rockrms.com/releasenotes), [Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456).

### Entity Query Returns The Wrong Rows

Check:

1. Property names in Model Map.
2. `where` expression syntax.
3. Whether `id` is present.
4. Whether query string `dynamicparameters` overrides values.
5. Security filtering.
6. `limit` and `offset`.
7. Campus/status filters.
8. Whether attributes are properties or require `Attribute` filter.
9. Fluid expression differences.

### SQL Errors

Check:

1. Is `Sql` enabled?
2. Is syntax valid in SQL Server?
3. Are parameters declared on the command line?
4. Are reserved names used as parameter names?
5. Is timeout too low?
6. Is a non-query statement missing required command-style configuration?
7. Is user input directly interpolated?
8. Are permissions or DB restrictions blocking the operation?
9. Did direct SQL require cache clearing?

Source: [SQL](https://community.rockrms.com/lava/commands/sql-commands).

### Fluid Migration Errors

Check known differences:

- Missing commas in include calls.
- `&&` instead of `and`.
- Nested comments.
- Regex backslash escaping.
- Sort/OrderBy differences.
- Single quote inside single-quoted strings.
- Variable names starting with numbers.
- Split/null/empty behavior.
- `forloop.rindex`/`rindex0` behavior before fixes.

Source: [Fluid Differences](https://community.rockrms.com/lava/fluid/differences).

### Shortcode Output Leaks Or Variables Collide

Check:

1. Shortcode scope behavior.
2. Nested shortcode behavior.
3. `blockContent` handling.
4. Whether caller and shortcode use the same variable names.
5. v19.1 nested blockContent fix status.
6. Whether the shortcode uses shared scope intentionally.

Sources: [Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes), [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Page Shows Another Person's Data

Check immediately:

1. Block cache duration.
2. Lava `cache` command key.
3. Output cache containing `CurrentPerson`.
4. Two-pass cache implementation.
5. CDN/proxy cache.
6. Security-disabled entity commands.
7. Remote Lava identity.
8. Whether current person was hardcoded during testing.

Sources: [Cache](https://community.rockrms.com/lava/commands/cache-commands), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava).

### Web Request Fails

Check:

1. `WebRequest` enabled.
2. URL reachable from Rock server.
3. TLS requirements.
4. Method.
5. Headers.
6. Body content type.
7. Response content type.
8. Timeout.
9. Authentication.
10. Whether endpoint returns non-200 responses.
11. Whether JSON body is valid.

Sources: [Web Request](https://community.rockrms.com/lava/commands/web-request-commands), [WebRequestBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WebRequestBlock.cs).

### Mobile Lava Breaks

Check:

1. Is Lava processed server-side or client-side?
2. Is the filter available locally in the shell version?
3. Are strings escaped?
4. Are `PageParameter`, `CurrentPerson`, `Device`, `PageValues`, `AppValues`, or `DeviceTheme` available?
5. Are quotes or ampersands breaking markup?
6. Are mobile-specific commands available?

Source: [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava).

## 18. Agent Task Recipes

### Recipe: Inventory Lava Risk On A Page

Output fields:

- Page ID / route.
- Site / layout / theme.
- Blocks containing Lava.
- Include paths.
- Shortcodes used.
- Enabled commands per block.
- Shortcode enabled commands.
- Cache settings.
- Security bypasses.
- SQL usage.
- Web requests.
- Workflow/interaction/write commands.
- Exceptions linked to page.
- Recommended remediation.

### Recipe: Review A Shortcode For Production

Inspect:

- `Name`
- `TagName`
- `TagType`
- `IsActive`
- `IsSystem`
- `Categories`
- `Documentation`
- `Markup`
- `Parameters`
- `EnabledLavaCommands`
- `ShortcodeScopeBehavior`
- Entity attributes
- Call sites
- Version requirements
- Security bypasses
- Cache behavior

Decision:

- Keep as-is.
- Narrow commands.
- Fix parameters.
- Add documentation.
- Convert to block/inline only if no callers exist or all callers can be updated.
- Replace SQL with entity command or parameterized SQL.
- Add tests or staging validation.

### Recipe: Find Legacy Attribute Lava

Process:

1. Search Exception List for legacy Lava warnings.
2. Record example syntax.
3. Locate source page/workflow/block.
4. Search stored templates for the same pattern.
5. Replace with `| Attribute:'Key'`.
6. Verify real entity property names are not accidentally changed.
7. Retest under Fluid.

Source pattern: [Finding and Fixing Legacy Lava](https://community.rockrms.com/recipes/107).

### Recipe: Safely Use `securityenabled:'false'`

Use only when:

- The page audience is trusted, or data is public by design.
- Entity-level security checks are not needed for the intended output.
- The template does not expose sensitive fields.
- The reason is documented.
- Performance benefit is real.

Inspect:

- Entity type.
- Page permissions.
- Block permissions.
- Caller identity.
- Attributes exposed.
- Related entity data exposed through `include` or navigation properties.

Source: [Entity](https://community.rockrms.com/lava/commands/entity-commands), [Attributes](https://community.rockrms.com/lava/filters/attribute-filters).

### Recipe: Create A Staff-Friendly Link Copy Shortcode

Pattern from community recipe: a shortcode can generate a copyable public URL for staff workflows, such as registration or forms ([Easy Copy Url Shortcode](https://community.rockrms.com/recipes/408)).

Agent adaptation:

- Use inline shortcode.
- Parameters: `input`, `label`, `buttontext`, `class`.
- No enabled commands unless the shortcode itself looks up records.
- Escape input into HTML attributes.
- If generating URLs from registration or form entities, verify page routes and public access.
- Test internal and public contexts.

### Recipe: Add A Translation Shortcode

Community patterns include client-side translation pairs in Defined Types and API-backed translation with caching ([The Rosetta Stone](https://community.rockrms.com/recipes/536), [Cognitive Services Translator](https://community.rockrms.com/recipes/368)). For production:

- Decide static translation table versus external translation API.
- Store language preference on the right entity.
- Avoid translating sensitive content externally unless approved.
- Cache API translations.
- Escape JavaScript output.
- Handle dynamic DOM updates only if needed.
- Verify accessibility and staff maintenance path.
- Review command enablement and API keys.

### Recipe: Generate Labels With Lava

For direct Zebra printing:

- Enable `PrintZPL` only in trusted staff contexts.
- Use `deviceid` for configured Rock devices when possible.
- Validate ZPL.
- Avoid duplicate execution.
- Escape dynamic text.
- Test printer output physically.

Source: [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl).

For check-in label merge fields with shortcodes, community examples show placement group lookup patterns, but entity IDs and group hierarchy are local and must be verified ([Lava Shortcode for Placement Groups on Check In](https://community.rockrms.com/recipes/386)).

### Recipe: Build An Agent Lava Tool

Using developer docs for AI-agent Lava tools ([Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools)):

- Name: specific action, not generic.
- Description: tells the agent when to call it.
- Parameters: typed, required only when necessary.
- Prompt: Lava template with parameterized SQL or entity commands.
- Output: JSON with stable keys.
- Commands: minimal.
- Security: same review as any Lava endpoint.
- Failure: include status and message fields.

Recommended output shape:

```json
{
  "status": "success",
  "data": [],
  "warnings": []
}
```

If a tool writes data, require explicit user intent and return the created/updated entity IDs.























<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `81`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Rock Roku pages display custom Lava-driven content as part of the application and render SceneGraph-oriented output rather than normal Rock CMS HTML. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| official | behavior | Apple TV pages in Rock must output valid TVML and can use Rock-provided Lava merge fields such as CurrentPerson, Context, Campuses, SiteStyles, and CurrentPage. | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) |
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| official | source_summary | Helix is a Rock web-development surface that combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. | [source](https://community.rockrms.com/developer/helix/overview) |
| rocku-confirmed | operational_guidance | Advanced HTML blocks are powerful CMS surfaces because they can combine markup, Lava, context, and sometimes enabled commands; treat edit access as privileged. | [source](https://community.rockrms.com/rocku/cms/advanced-html-block) |
| rocku-confirmed | risk | When reviewing an Advanced HTML block, inspect page/block security, enabled Lava commands, query-string or context inputs, and whether the output exposes sensitive entity data. | [source](https://community.rockrms.com/rocku/cms/advanced-html-block) |
| rocku-confirmed | source_summary | Advanced HTML Block adds public-safe guidance for CMS security and Lava review: block authorship is privileged, and agents should inspect enabled commands, context inputs, and page/block authorization. | [source](https://community.rockrms.com/rocku/cms/advanced-html-block) |
| rocku-confirmed | operational_guidance | For Rock operations and administration, If Statements should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/lava/if-statements) |
| rocku-confirmed | operational_guidance | For ministry process design, Communication Templates should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-templates) |
| rocku-confirmed | operational_guidance | The Communication Templates [Legacy] RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-templates-legacy) |
| rocku-confirmed | operational_guidance | The Communication Templates RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-templates) |
| rocku-confirmed | operational_guidance | For ministry process design, Communication Templates [Legacy] should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/communication/communication-templates-legacy) |
| More |  | 69 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->









































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `21`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Advanced HTML Block Transcript Insight](https://community.rockrms.com/rocku/cms/advanced-html-block) | approved_for_public_distillation | 2 | media-insight:2cf056c2b84e6365 |
| [Assign Statement Transcript Insight](https://community.rockrms.com/rocku/lava/assign-statement) | approved_for_public_distillation | 1 | media-insight:446c751591a992b1 |
| [BI Template Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-template) | approved_for_public_distillation | 3 | media-insight:22fb0ca5319b94a9 |
| [Communication Templates Transcript Insight](https://community.rockrms.com/rocku/communication/communication-templates) | approved_for_public_distillation | 3 | media-insight:4ca253d09a443da7 |
| [Communication Templates [Legacy] Transcript Insight](https://community.rockrms.com/rocku/communication/communication-templates-legacy) | approved_for_public_distillation | 3 | media-insight:66b971954eb3655e |
| [Entity Commands Transcript Insight](https://community.rockrms.com/rocku/lava/entity-commands) | approved_for_public_distillation | 2 | media-insight:d361c226caa0b789 |
| [Episode 185: Special Edition Lava Class Panel Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-185-special-edition-lava-class-panel) | approved_for_public_distillation | 3 | media-insight:914097c1d178331e |
| [Execute Command Transcript Insight](https://community.rockrms.com/rocku/lava/execute-command) | approved_for_public_distillation | 1 | media-insight:ec199a83a2123233 |
| More |  | 13 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->























## 19. Source Map And Dependency Notes

### Core Lava

- [Lava Reference](https://community.rockrms.com/lava): primary concept page for Lava syntax, tags, shortcodes, and Helix pointer.
- [RockU Lava](https://community.rockrms.com/rocku/lava): training map covering filters, statements, entity commands, SQL, web request, execute command, and shortcodes.
- [About Lava Fluid](https://community.rockrms.com/lava/fluid): engine transition and Global Attribute workflow.
- [Fluid Differences](https://community.rockrms.com/lava/fluid/differences): migration differences between DotLiquid and Fluid.

### Commands

- [Getting Started With Lava Commands](https://community.rockrms.com/lava/commands): command enablement and security framing.
- [Tag List](https://community.rockrms.com/lava/commands/taglist-commands): command discovery.
- [Entity](https://community.rockrms.com/lava/commands/entity-commands): entity query command and parameters.
- [SQL](https://community.rockrms.com/lava/commands/sql-commands): SQL execution, parameters, writes, timeout.
- [Cache](https://community.rockrms.com/lava/commands/cache-commands): memory cache, two-pass rendering, tags.
- [Web Request](https://community.rockrms.com/lava/commands/web-request-commands): external HTTP calls.
- [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands): workflow launch/activity activation.
- [Search](https://community.rockrms.com/lava/commands/search-commands): Universal Search from Lava.
- [Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands): adaptive messages.
- [Set Culture](https://community.rockrms.com/lava/commands/setculture-commands): culture-scoped formatting.
- [Stylesheet](https://community.rockrms.com/lava/commands/stylesheet-commands): page header CSS.
- [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl): Zebra label printing.
- [Observe](https://community.rockrms.com/lava/tags/observe): observability wrapper.
- [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write): analytics writes.

### Filters And Tags

- [Attributes](https://community.rockrms.com/lava/filters/attribute-filters): attribute access, global attributes, system settings, attribute security.
- [Include](https://community.rockrms.com/lava/tags/include-tags): include file paths and `~`/`~~` resolution.
- [Raw](https://community.rockrms.com/lava/tags/raw-tags): suppress Lava processing.
- [Lava Tag](https://community.rockrms.com/lava/tags/lava-tags): Fluid-only logic-focused syntax.

### Shortcodes

- [Intro to Shortcodes](https://community.rockrms.com/lava/shortcodes/intro-to-shortcodes): shortcode purpose.
- [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes): inline versus block.
- [Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes): configuration, parameters, enabled commands, admin location.
- [The Power of Shortcode Blocks](https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks): `blockContent`, nested configuration, `disablelavamerge`.
- [Passing in Objects](https://community.rockrms.com/lava/shortcodes/passing-in-objects): object passing and limitations.

### API, Remote, Mobile, Helix, Agents

- [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava): remote render endpoint and API key warning.
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api): Lava webhooks, route matching, request variables, commands.
- [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava): mobile Lava contexts, escaping, client processing.
- [Helix](https://community.rockrms.com/developer/helix): Lava applications, HTMX, forms, early-alpha caveat in source pack.
- [Helix Lava Commands](https://community.rockrms.com/developer/helix/lava-commands): command pointer for modify/delete/transaction/response/render endpoint docs.
- [Lava Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/lava-tools): agent custom tools using Lava.

### Release Notes And Source Code

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): v19.1 Lava fixes and shortcode scope behavior.
- [LavaShortCode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.cs): shortcode entity fields.
- [LavaShortCode.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaShortCode/LavaShortCode.Logic.cs): shortcode cache update.
- [LavaShortcodeDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeDetail.cs): admin detail block behavior.
- [LavaShortcodeList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/LavaShortcodeList.cs): admin list block behavior.
- [DynamicShortcodeBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Lava/Core/Shortcodes/DynamicShortcodeBlock.cs): block shortcode implementation.
- [WebRequestBlock.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WebRequestBlock.cs): webrequest implementation landmark.
- [SqlCommand.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx.cs): admin SQL command behavior.
- [DateFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests/Lava/Filters/DateFilterTests.cs): date/timezone assumptions.
- [PersonFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Filters/PersonFilterTests.cs): person filter behavior examples.
- [TextFilterTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests/Lava/Filters/TextFilterTests.cs): text filter testing landmark.
- [LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs): endpoint security enum landmark.

### Community Pattern Sources

Use these for examples only and verify locally:

- [Run Lava within VS Code and Preview Results](https://community.rockrms.com/recipes/456)
- [Lava Shortcode for Placement Groups on Check In](https://community.rockrms.com/recipes/386)
- [Address Format Lava Shortcode](https://community.rockrms.com/recipes/467)
- [Content Pagination Shortcode](https://community.rockrms.com/recipes/242)
- [Show Until, Show After Lava Shortcodes](https://community.rockrms.com/recipes/160)
- [Default Connectors Quick Reference List](https://community.rockrms.com/recipes/480)
- [The Rosetta Stone - Translate anything](https://community.rockrms.com/recipes/536)
- [Cognitive Services Translator](https://community.rockrms.com/recipes/368)
- [Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file)

Dependencies for this guide are `cms`, `workflows`, `sql`, and `security`. Lava work that touches any of those areas should be reviewed with the same care as application code, because in Rock those boundaries often meet inside a single template.
