---
id: authored-lava
title: Lava
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "29b9e588f224b149b839ef0c2ff0394d257edaff043f6b9e5b262aa946d1cbac"
---

# Lava

## Agent Summary

Lava is Rock’s Liquid-based templating layer for turning merge fields into formatted output, applying filters, controlling flow with tags, and invoking explicitly enabled commands. It appears across CMS blocks, workflows, communications, mobile content, TV applications, APIs, reporting surfaces, Helix applications and AI tools. The available merge fields, commands, security context and required output format vary by execution surface. [Lava Reference](https://community.rockrms.com/lava)

Treat every Lava task as five linked decisions:

1. Identify the rendering surface and its authenticated person or system context.
2. Inspect the merge fields and input values actually available there.
3. distinguish presentation-only filters and tags from commands that read, write, call external systems or cause physical effects.
4. Enable only the commands that surface needs.
5. Validate both the rendered output and any resulting state under the intended role.

Lava commands can bypass parts of Rock’s normal security and business logic. HTML blocks begin with no commands enabled unless configured, and write-capable commands require especially narrow authorization and verification. [Lava Commands](https://community.rockrms.com/lava/commands)

## Scope And Boundaries

This guide covers Lava syntax, filters, commands, shortcodes, remote rendering, workflow use, Rock Mobile and TV output, Helix, reporting patterns and Lava-backed AI tools.

It does not replace the owning guides for CMS architecture, workflow design, SQL, security, communications, event registration, check-in, LMS or external BI platforms. When Lava participates in one of those systems, this guide covers the Lava boundary: inputs, rendering context, command authorization, output contract and verification.

The evidence pack supports examples of community implementation patterns. Those examples are not statements of universal Rock behavior. Unless a community record is explicitly marked otherwise, reproduce the behavior on the target Rock version and configuration before adopting it.

## Mental Model

A useful model is:

```text
rendering surface
    → runtime identity and merge fields
    → Lava template
        → output expressions
        → filters
        → control-flow tags
        → enabled commands
        → shortcodes
    → context-specific output
    → visible result or side effect
```

Output expressions such as `{{ Person.NickName }}` insert values. Filters transform a value through a pipeline. Tags such as `assign`, `if` and `for` manage variables and flow. Shortcodes hide a larger Lava template behind a compact interface. Commands reach beyond formatting and may retrieve entities, execute SQL, call a web service, start a workflow, modify data or trigger another effect. [Lava Reference](https://community.rockrms.com/lava)

The final output is not always HTML. Rock Mobile Lava can produce XAML, Apple TV pages must produce valid TVML, Roku pages produce SceneGraph-oriented content, and `printzpl` sends ZPL to a printer without producing visible page output. [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava), [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages), [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl)

Security belongs to the whole render path, not merely the template text. The same Lava may behave differently when rendered by an anonymous CMS page, an authenticated block, a scheduled workflow, a REST key, a mobile shell or a Helix endpoint.

## Core Syntax And Engine

Rock bases Lava on Liquid and extends it with Rock-specific filters, commands, entity access and merge fields. Basic templates combine output expressions, assignments, conditions and loops. [Lava Reference](https://community.rockrms.com/lava)

```liquid
{% assign hour = 'Now' | Date:'H' %}

{% if CurrentPerson %}
  Hello {{ CurrentPerson.NickName }}.
{% elseif hour < 12 %}
  Good morning.
{% else %}
  Welcome.
{% endif %}
```

Do not assume a person merge field exists merely because the template renders in a person-aware test surface. An anonymous page, job, remote endpoint or bundled mobile template may have a different identity context.

### Fluid and DotLiquid

Rock introduced the Fluid engine in v13. The transition documentation describes DotLiquid as the historical engine and marks support as ending with v17. Fluid is intended to improve performance and align the platform with newer framework work. [About Lava Fluid](https://community.rockrms.com/lava/fluid), [Lava Reference](https://community.rockrms.com/lava)

Migration differences documented by Rock include:

- Fluid include parameters require commas.
- Array sorting should use `OrderBy`; entity-command sorting remains a separate command parameter.
- Fluid’s `Sort` behavior is case-sensitive, with `SortNatural` offered for natural sorting.
- Nested comment tags are unsupported.
- Conditions should use `and`, not `&&`.
- Unrecognized backslash escape sequences can fail, which is significant for regular expressions.
- Mixed quote usage can change parsing.
- Some differences were corrected in later versions, including items marked fixed in v17 or v19. [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)

Historical Fluid verification mode rendered Lava through both engines and recorded differences as exceptions. Because this meant executing a template twice, Rock warned administrators to consider templates with write operations or other side effects before enabling that mode. Engine selection and restart instructions are historical, version-sensitive administration guidance; inspect the current target version before applying them. [About Lava Fluid](https://community.rockrms.com/lava/fluid)

Fluid also introduced the `lava` tag in v13.7. Inside that tag, most content is treated as logic and explicit `echo` statements produce text. It is useful for logic-heavy regions but is available only under Fluid. [Lava Tag](https://community.rockrms.com/lava/tags/lava-tags)

## Filters

Filters transform the value on their left and can be chained. Rock’s filter families include text, date, numeric, color, array, person, attribute and other filters. [Lava Filters](https://community.rockrms.com/lava/filters)

```liquid
{{ CurrentPerson.NickName | Upcase }}
{{ 'Now' | Date:'dddd, MMMM d, yyyy' }}
{{ CurrentPerson | Attribute:'Employer' }}
{{ Person.PhoneNumbers | Size }}
```

A filter does not automatically make its input trustworthy or appropriate for the output format. Escape values at the output boundary, especially when producing XAML, URLs or command parameters.

### Text and output encoding

Rock’s official Mobile guidance marks filters that can run locally in the shell. When Lava produces XAML, user-entered text, content titles, URLs and other strings containing characters such as `&` or `'` must be escaped for the position where they are inserted. [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

A reviewed community pattern recommends testing names, titles and URLs containing punctuation rather than validating only simple values. URL components should be encoded as URL data, while XAML attribute content should be escaped as markup. This pattern still requires verification in the target shell and template. [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

### Dates and time zones

At the supplied immutable Rock source revision, Lava date-filter tests state that local `DateTime` values are interpreted in Rock’s configured organization time zone, which may differ from the server time zone. UTC values or `DateTimeOffset` values are safer when an explicit offset matters. This is an implementation observation, not proof of any installation’s configured time zone. [DateFilterTests at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests/Lava/Filters/DateFilterTests.cs)

Rock v19 also materializes recurring iCal occurrences into `ScheduleDate` rows. For v19 date-based SQL or Lava queries, use those generated occurrences instead of creating a second recurrence-expansion process. [3 Underrated Features, 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)

### Person, attributes and personalization

Attribute filters can return formatted, raw or object-oriented representations depending on the field type and requested option. Workflow attributes are commonly accessed with the workflow object and an attribute key. Fields that support Lava are identified in Rock’s workflow interface with `{{ Lava }}` help notation. [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

For personalization, Rock documents two approaches: the `personalize` command, using a segment or request-filter key, and the `PersonalizationItems` person filter for conditional logic. Both can be used outside ordinary CMS blocks, including communications, when the rendering context supplies the necessary person data. [Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava)

### `where` and short-link caveats

Rock v19 adds a `contains` parameter to the Lava `where` filter for partial field matching. Confirm current case, type and performance behavior before applying it to broad collections. [New Features Coming to v19, 18:00](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1080s)

`CreateShortLink`, available from v8, accepts optional settings in this order: token, site ID, overwrite, random length, category ID and pinned flag. Invalid values can fall back to defaults; an empty URL or the absence of a shortening-enabled site returns an empty string. Because the filter creates persistent records, verify the site and every optional position before bulk communication use. [Other Filters](https://community.rockrms.com/lava/filters/other-filters)

## Commands

Commands perform operations beyond ordinary value transformation. Rock’s documented command catalog includes read, write, HTTP, workflow, personalization, rendering, scripting and physical-output operations. Availability is controlled by the rendering surface’s enabled-command list. [Lava Commands](https://community.rockrms.com/lava/commands)

Commands can bypass Rock’s built-in security and business logic. Enable only the commands required by the template. Treat edit access to an Advanced HTML block as privileged because the block can combine markup, Lava, context and configured commands. During review, inspect page security, block security, enabled commands, query-string and context inputs, and whether rendered output exposes sensitive entity data. [Lava Commands](https://community.rockrms.com/lava/commands), [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)

### Entity retrieval

Entity commands retrieve Rock entities with parameters such as `id`, `ids`, `where`, `dataview`, sorting, offsets and limits. Parameter values such as `where` must be enclosed in single quotes. If `id` is supplied, Rock ignores `where`, `dataview` and `dynamicparameters`. [Entity Command](https://community.rockrms.com/lava/commands/entity-commands)

```liquid
{% person where:'LastName == "Rivera"' limit:'10' %}
  {% for person in personItems %}
    {{ person.FullName }}
  {% endfor %}
{% endperson %}
```

Keep result sets bounded and return only necessary properties. A community-reviewed troubleshooting pattern notes that `where:` becomes a rendered Dynamic LINQ expression; blank IDs, unescaped quotes and assembled expressions can therefore fail before any row is returned. Inspect the fully rendered expression when troubleshooting, and verify any proposed fallback lookup against the target system before using it. [Entity Command](https://community.rockrms.com/lava/commands/entity-commands)

The administrative `taglist` command, available from v8, lists registered Lava commands on the server and can help discover plugin-provided entity command names. Registration does not mean a command is enabled on a particular block or endpoint. [Tag List](https://community.rockrms.com/lava/commands/taglist-commands)

### SQL, Execute and Web Request

The supplied RockU SQL material demonstrates both queries and statement-style updates, but production selection must be stricter than a teaching example. Prefer cache objects or entity commands when appropriate, return only needed fields, enforce authorization, and consider business logic and query cost before choosing SQL. [SQL Command](https://community.rockrms.com/rocku/lava/sql-command), [RockIQ Q&A, 24:50](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=1490s)

Never give an AI agent an open-ended capability to generate and execute arbitrary SQL. Rock’s AI Summit distinguishes reviewed static SQL inside a narrowly secured Lava tool from arbitrary runtime SQL, which can bypass Rock security and business logic. [AI Summit, 71:20](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s)

The `execute` command can run server-side code and import libraries, making it a privileged code-execution surface rather than a formatting convenience. [Execute Command](https://community.rockrms.com/rocku/lava/execute-command)

At the supplied immutable source revision, `WebRequestBlock` implements `ILavaSecured`, checks authorization during rendering and declares `WebRequest` as its required permission key. That source observation does not show whether any specific block or endpoint has enabled the command. [WebRequestBlock at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Lava/Blocks/WebRequestBlock.cs)

### Modify and delete

Rock v18 documents `modifyentity` for updating or creating one entity and `deleteentity` for deleting one entity. `modifyentity` accepts an integer, GUID or IdKey; `id:'0'` creates a new entity. Both commands expose security controls and result merge fields. Their documentation warns that the Person entity does not itself apply the security checks described for secured entities. [Modify Entity](https://community.rockrms.com/lava/commands/modify-entity), [Delete Entity](https://community.rockrms.com/lava/commands/delete-entity)

For every write:

1. Resolve the intended record using a stable identity.
2. Check the command result’s success state.
3. Capture the returned canonical identifier immediately.
4. Read the saved entity back.
5. Stop before dependent writes if the parent write failed.

Community evidence reports that, in some renders, an invalid modify operation can leave an object tracked and make later saves fail with the earlier validation error. It also reports that a database transaction rollback should not be assumed to reset that render context. This is a troubleshooting hypothesis that needs reproduction on the target Rock version. If encountered, isolate the failing create, stop immediately after failure and begin subsequent work in a new render. [Entity Command](https://community.rockrms.com/lava/commands/entity-commands)

### Workflow activation

From v7, `workflowactivate` treats keys beyond its command parameters as workflow or activity attribute keys. Each supplied value must use the field type’s stored-value format. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)

Treat those extra parameters as a schema contract. Compare the rendered keys with the target workflow and activity attribute keys, and verify the created workflow’s stored values. Do not assume an unknown or misspelled key will produce a sufficiently visible warning. This verification practice is community-contributed and instance-dependent. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)

### Rendering and physical effects

Rock v18’s `renderlavaendpoint` command processes a named Lava endpoint during the initial page render, avoiding a second on-load HTMX request. Caret routes such as `^/application/endpoint` are supported; the method defaults to GET and can be set explicitly. [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint)

Rock v19’s `printzpl` command renders enclosed ZPL and sends it directly to a configured Zebra printer identified by a device or IP address. It produces no visible page output. Invalid ZPL can cause printer errors or unexpected labels, so rendering the command is a physical action, not a preview. [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl)

## Shortcodes

Shortcodes replace a compact tag with a larger Lava template, allowing specialists to package complex behavior for simpler reuse. Rock defines two types: inline and block. [Lava Shortcodes](https://community.rockrms.com/documentation/digital-publishing/websites/web-design-frameworks/lava-shortcodes), [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes)

An inline shortcode has no closing tag:

```liquid
{[ media-card id:'example-key' ]}
```

A block shortcode receives enclosed content and requires a matching end tag:

```liquid
{[ callout tone:'info' ]}
  Registration opens next week.
{[ endcallout ]}
```

Choose the type before publishing it. Rock warns that changing an established shortcode from inline to block or vice versa breaks existing callers. Shortcode records can also define parameters and enabled commands, so review them as executable shared components rather than harmless text macros. [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes), [LavaShortcodeBag at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeBag.d.ts)

If a database field stores Lava or shortcode markup, direct output may display the markup literally. A reviewed community pattern uses an explicit processing step such as `RunLava` only when execution is intentional. Before doing so, inspect who can edit the stored value, the surface’s enabled commands and whether the output is public. [Other Filters](https://community.rockrms.com/lava/filters/other-filters)

## Execution Contexts And Output Contracts

### Advanced HTML and communications

Advanced HTML blocks are privileged CMS surfaces. Review both authorship and runtime access, including page and block authorization, inputs and command enablement. A successful administrator preview does not establish anonymous or staff-role access. [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)

Lava can personalize communications, but communication rendering has its own merge-field and delivery context. Test with representative recipients, missing values and the current communication surface. The new communication wizard is a significant sender and template-management workflow change, so do not transplant steps from legacy communication training without confirming the target Rock version. [Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava), [Communication Wizard preview](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/EplO7L1lJ7)

### Rock Mobile

In Rock Mobile’s Content block, Dynamic Content is fetched from the server each time the page initializes. Static content is bundled into the shell, requires deployment to change, and processes Lava without `CurrentPerson`. [Mobile Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

Before relying on identity, fresh database values or server-only filters, inspect:

- Dynamic Content.
- Whether Lava is processed on the server.
- Enabled commands.
- The intended context entity.
- Whether the target filter can execute locally in the shell.
- The shell version and final XAML validity.

Community guidance for migrations recommends placing shell-version branching inside the XAML fragment that the shell actually downloads and testing the observed `Device.ShellVersion` format. That behavior requires verification on both old and new target shells. [Mobile Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

### TV applications

Apple TV pages must output valid TVML. Rock documents merge fields including `CurrentPerson`, `Context`, `Campuses`, `SiteStyles` and `CurrentPage` for that surface. [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

Roku pages render Lava-driven application content as SceneGraph-oriented output, not ordinary Rock CMS HTML. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

Do not validate either surface with an HTML-only preview. Validate the exact output grammar and the target application.

## Remote Lava And APIs

Rock documents a remote Lava REST endpoint that accepts Lava and returns rendered output. It is HTTPS-only. If browser-visible JavaScript contains the endpoint and API key, a visitor can reuse that key to submit other Lava that runs as the person linked to the key. Rock therefore recommends a carefully restricted endpoint and generally favors server-side callers over exposed browser code. [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)

Rock also documents Defined Value-backed Lava webhooks for custom APIs, including Apple TV and Roku examples. That webhook mechanism does not include security by default. Routes can match URL and HTTP method, request data becomes available to the template, and each Defined Value specifies enabled commands. Treat every such route as public unless a separately verified control protects it. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

For a remote Lava surface:

- Keep credentials out of browser-delivered code.
- Bind execution to the least-privileged identity available.
- Restrict methods and route matching.
- Enable only necessary commands.
- Bound query sizes and output fields.
- Avoid returning raw entity objects or sensitive fields.
- Test anonymous access explicitly.
- Record the expected response content type and schema.

## Helix And Lava Applications

Helix combines HTMX, Lava Applications, Lava Commands and Control Shortcodes as an evolution of Lava-driven web development. [Helix Overview](https://community.rockrms.com/developer/helix/overview)

The Lava Application Content block automatically registers HTMX. Templates hosted by that block can call an application endpoint with a caret route such as `^/application-slug/endpoint-slug` instead of hard-coding `/api/v2/lava-app/1/...`. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

Community-contributed Helix patterns recommend:

- Render a useful initial page on the server, then use HTMX for enhancement.
- Keep the page shell responsible for filters, navigation, loading indicators and the initial target.
- Return only inner result rows or cards from an active-search endpoint.
- Keep pagination, sorting and filtering in one explicit server contract.
- Allowlist filter enums, sort columns, directions and page sizes.
- Parameterize text input and bound results.
- Load shared scripts and styles in the host shell rather than assuming endpoint fragments can register assets.
- Reapply browser-held UI state after HTMX swaps, or encode that state in request parameters.
- Put crawl-critical metadata in the initial host response rather than an HTMX fragment.
- Keep authorization server-side; HTMX attributes are presentation behavior.
- Test direct endpoint access separately from the hosted page.

These are reviewed community patterns, not guarantees of every Helix version. Verify them against the target application, endpoint security mode and browser route. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

Endpoint security must be checked independently at the page, block, endpoint and parent Lava Application layers. A community report notes that a visible page and block can coexist with an endpoint failure when inherited application-level execution authorization is missing. Do not treat administrator override as proof that anonymous or staff access is configured. [Helix Overview](https://community.rockrms.com/developer/helix/overview)

Also inspect each endpoint’s enabled-command allowlist. A command working in another block does not prove that it is enabled for this endpoint. Use read-only methods for read endpoints, and verify CSRF protection and authorization for any state-changing route. This operational checklist is community-contributed and requires live confirmation. [Lava Commands](https://community.rockrms.com/developer/helix/lava-commands)

## Workflows And Lava

Workflow fields marked with `{{ Lava }}` receive workflow-specific merge fields. Workflow attributes can be read by key, while the workflow, current activity, current action, global attributes and action-specific merge fields may also be available. [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

Triggered workflows and jobs may have no `CurrentPerson`. Rock’s documentation states that attribute authorization is still applied; without a current person, attributes may require `All Users – Allow View` unless the template deliberately supplies another authorized person context. Assigning an administrator as `CurrentPerson` materially changes the security context and should not be used as a casual workaround. [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

Community workflow patterns add several verification points:

- Confirm an attribute’s field type and object shape before chaining properties. A Person attribute requested as an object may already return a Person rather than a PersonAlias wrapper.
- Use the raw stored value when a Single-Select attribute holds an internal ID but displays a label.
- For rerunnable modify-entity deployments, resolve a parent by a stable key, write it, re-query its canonical ID and only then create children.
- Capture `ModifyResult.Object.Id` or its GUID immediately, check success and stop on failure.
- Re-query a saved workflow action type before attaching form fields to its persisted form ID.
- Treat workflow action component settings as instance-specific configuration and verify their attribute identifiers in the target version and plugin set.
- Read back final workflow attributes, action settings and child relationships before connecting a live trigger.

These patterns require target-instance schema and behavior verification. [Entity Command](https://community.rockrms.com/lava/commands/entity-commands), [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

## Reporting And Persisted Results

Community-reviewed guidance treats Rock metrics as a capture layer for values calculated on a schedule and visualized later. Persisted datasets can similarly move expensive historical analytics out of the page request so a dashboard does not recalculate the full history on every load. These are implementation patterns, not a claim that every query should be persisted. [Dashboard design session](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp), [Journey dashboard session](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

Use persistence when the measure is repeatable, historical calculation is expensive, and users do not require transaction-level freshness. State the dataset’s grain, refresh schedule and failure behavior. For v19 recurring schedules, consume materialized `ScheduleDate` occurrences instead of expanding iCal rules again. [3 Underrated Features, 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)

If external BI content is embedded in a Rock page, comply with the external platform’s licensing and place the Rock page behind appropriate roles. Page visibility does not replace external licensing, and administrator visibility does not prove staff-role access. [Data Analytics Hub panel](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz)

## Lava-Backed AI Tools

Rock’s agent model separates agents, skills and tools, with configuration and security boundaries at each layer. Chat versus MCP and Internal versus Public are separate decisions. Expose only tools authorized for the current person and selected agent. [AI Summit, 24:01](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s)

Lava tools should:

- Use clear verb-and-entity names such as Lookup, List, Get, Summary, Insights, AvailableAttributes or AddOrUpdate.
- Declare explicit, sanitized parameters.
- Return bounded, intentionally shaped data rather than large raw records.
- Return structured `AgentToolResult` values.
- Use the dedicated filters for instructions, compact history content, metadata and Rock reference routes.
- Use built-in tool logs to inspect calls, inputs and results. [AI Summit, 67:34](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s), [AI Summit, 87:48](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s)

Prompt context is layered across Rock’s core prompt, organization prompt, agent instructions, skill instructions and current-person context. Keep each layer concise, add instructions when testing demonstrates a need, and pass IdKeys rather than raw integer identifiers. [AI Summit, 76:13](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s)

## Version And Authority Caveats

- Fluid was introduced in v13; the `lava` tag is documented for Fluid beginning in v13.7. [About Lava Fluid](https://community.rockrms.com/lava/fluid), [Lava Tag](https://community.rockrms.com/lava/tags/lava-tags)
- Rock marks DotLiquid support as ending with v17. Migration differences have fixes distributed across v17 and v19, so do not apply an old compatibility list without matching the installed version. [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)
- `workflowactivate` behavior in this pack is scoped from v7. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)
- `taglist` and `CreateShortLink` are documented from v8. [Tag List](https://community.rockrms.com/lava/commands/taglist-commands), [Other Filters](https://community.rockrms.com/lava/filters/other-filters)
- Modify Entity, Delete Entity and Render Lava Endpoint are documented for v18. [Modify Entity](https://community.rockrms.com/lava/commands/modify-entity), [Delete Entity](https://community.rockrms.com/lava/commands/delete-entity), [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint)
- `printzpl`, materialized `ScheduleDate` occurrences and the `where` filter’s `contains` option are v19 material. [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl), [v19 feature preview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1080s)
- Official documentation describes supported behavior. Immutable source excerpts clarify implementation at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, but do not establish an installation’s version or configuration.
- RockU and official presentations are training evidence; version-sensitive implementation should be checked against current written documentation.
- Community contributions and recipes are examples. Items marked as needing live verification must be reproduced before being treated as target-instance behavior.

## Troubleshooting Decision Tree

### Lava renders blank or a merge field is missing

1. Identify the exact surface: CMS, workflow, job, communication, endpoint, mobile shell or TV application.
2. Confirm whether the expected merge field exists there.
3. Check anonymous versus authenticated execution and the actual `CurrentPerson`.
4. For workflow attributes, verify the attribute key, requested representation and field type.
5. For Rock Mobile, determine whether the content is static, dynamic, local or server-processed.
6. Test missing-data branches explicitly. [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows), [Mobile Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

### A parser error points at an innocent-looking line

1. Inspect preceding output expressions and filter arguments.
2. Check for an unclosed quote, missing delimiter or incomplete filter parameter.
3. Check Fluid-specific rules: include commas, `and` instead of `&&`, unsupported nested comments and invalid escapes.
4. Reduce nested assignments and conditions to small independently rendered blocks.
5. Retest using the target engine and surface. Community reports note that parsing may fail later than the malformed expression, so the reported line may be downstream of the cause. [Fluid Differences](https://community.rockrms.com/lava/fluid/differences)

### An entity command returns no rows or fails before iteration

1. Confirm the command is registered and enabled on this surface.
2. If `id` is present, remove expectations that `where`, `dataview` or `dynamicparameters` will also apply.
3. Ensure parameter values such as `where` are enclosed in single quotes.
4. Inspect the fully rendered Dynamic LINQ expression.
5. Check blank identifiers, quote escaping and types.
6. Add a small limit and test a literal stable lookup.
7. Stop if the only proposed workaround is an unbounded query. [Entity Command](https://community.rockrms.com/lava/commands/entity-commands)

### A modify command appears to succeed but data is unchanged

1. Resolve and display the intended entity identity in a safe diagnostic context.
2. Check `ModifyResult.Success`, validation errors and the returned object.
3. Capture the canonical ID immediately.
4. Read the saved record back.
5. For person updates, verify that an alias, anonymous match or workflow-created record was resolved to the intended Person.
6. Preserve existing attribute values when conditional paths omit fields.
7. Stop before writing children when the parent result is blank or unverified. [Modify Entity](https://community.rockrms.com/lava/commands/modify-entity)

### A later write fails with an earlier validation error

1. Stop the render after the first failed modify command.
2. Do not assume a transaction rollback cleared the render’s tracked state.
3. Move experimental or risky creates into a separate render.
4. Retry only after validating the failed entity’s required fields.
5. Reproduce the behavior on the target version before classifying it as a change-tracker issue. This symptom comes from reviewed community evidence, not official universal behavior. [Modify Entity](https://community.rockrms.com/lava/commands/modify-entity)

### A workflow starts but submitted values are missing

1. Compare each extra `workflowactivate` key with the target workflow and activity attribute keys.
2. Confirm each value uses the field type’s stored format.
3. Remove obsolete parameters and create missing attributes intentionally.
4. Inspect the created workflow’s stored values.
5. Verify raw versus formatted values for selections and object fields. [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)

### A shortcode displays as raw text

1. Confirm the shortcode is registered and its type matches the caller’s syntax.
2. Determine whether the value is being treated as stored text rather than a template.
3. If execution is intentional, inspect edit permissions and enabled commands before applying `RunLava`.
4. Test the result under anonymous and intended authenticated roles.
5. Stop if untrusted editors can supply executable Lava. [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes), [Other Filters](https://community.rockrms.com/lava/filters/other-filters)

### A Helix endpoint works for administrators but not its audience

1. Test as anonymous, intended role and administrator.
2. Inspect page, block, endpoint and parent Lava Application authorization.
3. Check the endpoint security mode.
4. Check the endpoint’s enabled-command allowlist.
5. Verify the route from both the hosted Content block and direct endpoint path.
6. Do not use administrator success as access proof. This layered preflight includes community-derived checks that require target-instance confirmation. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

### An HTMX fragment loses scripts, styles or UI state

1. Determine whether the dependency belongs in the host shell.
2. Do not assume endpoint-rendered JavaScript or stylesheet commands register usable assets.
3. Keep endpoint output focused on replaceable inner content.
4. Reapply local UI state after `htmx:afterSwap`, or send it as request state.
5. Verify first render, swap, refresh and back navigation.
6. Test direct endpoint rendering and the hosted page separately. These checks are community patterns requiring live verification. [Helix Overview](https://community.rockrms.com/developer/helix/overview)

### Rock Mobile content is stale, anonymous or invalid XAML

1. Check whether the Content block is static or dynamic.
2. Confirm whether Lava runs locally or on the server.
3. Do not expect `CurrentPerson` in bundled static content.
4. Check whether every filter used is supported in the shell.
5. Escape markup-sensitive text and encode URL components.
6. Validate XAML with punctuation-heavy test records.
7. Test the actual shell versions in scope. [Mobile Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content), [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

### A remote Lava route exposes more than intended

1. Treat a Defined Value Lava webhook as unsecured until a separate control is verified.
2. Inspect route and method matching.
3. Review the execution identity and all enabled commands.
4. Remove credentials from browser-visible code.
5. Bound data access and response fields.
6. Test anonymous calls and unexpected methods.
7. Stop if the route can accept arbitrary Lava under a privileged key. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)

## Agent Task Recipes

### Recipe: Review an existing Lava surface safely

**Outcome:** A bounded risk assessment without changing the target.

1. Identify the page, block, workflow action, endpoint, mobile block or other owner.
2. Record the Rock version, rendering engine and intended audience.
3. Inspect page, block, application and endpoint authorization where applicable.
4. List inputs: merge fields, page parameters, query strings, request body, headers, cookies and stored values.
5. List enabled commands and classify each as read, write, external call, code execution or physical effect.
6. Identify the expected output grammar.
7. Test missing values and the intended identities without enabling additional commands.

**Inspect:**

- Edit permissions.
- Runtime identity.
- Command allowlist.
- Sensitive entity exposure.
- Input escaping.
- Query bounds.
- Side effects.

**Stop when:**

- The owner surface is unknown.
- Version applicability is unresolved.
- Testing would send, print, write or call an external service without authorization.

Sources: [Lava Commands](https://community.rockrms.com/lava/commands), [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)

### Recipe: Build a bounded read-only entity view

**Outcome:** A limited list using an Entity command.

1. Confirm the entity command name with current documentation or `taglist`.
2. Enable only Rock Entity access on the owning surface.
3. Choose one lookup strategy: `id`, `where` or Data View.
4. Quote command parameters correctly.
5. Add sorting and a strict result limit.
6. Render only the required properties.
7. Test no-result, one-result and maximum-result cases.
8. Verify audience authorization independently.

**Do not assume:**

- `where` still applies when `id` is supplied.
- A registered command is enabled.
- Entity access automatically enforces every business rule.
- A working administrator view is audience-safe.

Sources: [Entity Command](https://community.rockrms.com/lava/commands/entity-commands), [Tag List](https://community.rockrms.com/lava/commands/taglist-commands)

### Recipe: Prepare a Lava entity write

**Outcome:** An idempotent, verifiable single-entity change plan.

1. Confirm Modify Entity is available on the target version.
2. Resolve the target by a stable identifier.
3. Separate create and update paths.
4. Supply values in each property or attribute’s required stored format.
5. Execute one parent write.
6. Check `ModifyResult.Success`.
7. Capture the canonical returned ID or GUID immediately.
8. Read the entity back.
9. Only then perform dependent writes.
10. Render a bounded diagnostic summary without private data.

**Stop when:**

- The target identity is ambiguous.
- Validation fails.
- The canonical ID is blank.
- Required security checks are absent.
- A later write would depend on an unverified object.

Sources: [Modify Entity](https://community.rockrms.com/lava/commands/modify-entity), [Lava Commands](https://community.rockrms.com/lava/commands)

### Recipe: Preflight a workflow activation

**Outcome:** A workflow is activated with verified attribute values.

1. Identify the target workflow type and activity.
2. Enumerate the workflow and activity attribute keys.
3. Map each submitted input to exactly one key.
4. Convert each value to the field type’s stored format.
5. Remove parameters with no matching attribute.
6. Activate one controlled workflow.
7. Read back its stored attributes and rendered state.
8. Test the downstream action that consumes each critical value.

**Inspect:**

- Attribute key spelling.
- Raw versus formatted values.
- Person versus PersonAlias object shape.
- Trigger/job security when no `CurrentPerson` exists.

Sources: [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands), [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)

### Recipe: Publish a reusable shortcode

**Outcome:** A stable shortcode contract for content authors.

1. Decide whether the shortcode is inline or block.
2. Choose a unique, descriptive tag name.
3. Define explicit parameters and defaults.
4. Keep enabled commands to the minimum.
5. Document the output and accepted content.
6. Test omitted, valid and malformed parameters.
7. Test anonymous and intended authenticated contexts.
8. Search existing templates before making any type or parameter-breaking change.

**Do not assume:**

- Stored shortcode text will execute automatically.
- A shortcode is safe because its caller is short.
- Changing inline versus block type is backward compatible.

Sources: [Lava Shortcodes](https://community.rockrms.com/documentation/digital-publishing/websites/web-design-frameworks/lava-shortcodes), [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes)

### Recipe: Build a read-only Helix active-search page

**Outcome:** A server-rendered page enhanced with bounded HTMX filtering.

1. Render a useful first result set through the Lava Application Content block.
2. Keep the filter shell, target and loading state in the host response.
3. Use a caret route for the results endpoint.
4. Allowlist filters, sort columns, direction and page size.
5. Parameterize text search and bound the query.
6. Return only inner rows or cards from the partial endpoint.
7. Carry filter, sort and pagination state through one request contract.
8. Test anonymous, intended-role and administrator access.
9. Test first render, swaps, empty results, pagination and browser navigation.
10. Inspect console errors and responsive overflow.

**Stop when:**

- Parent application authorization is unresolved.
- A read endpoint requires write commands.
- The endpoint returns sensitive message bodies or person-level details beyond its stated purpose.
- Direct endpoint access exposes more than the hosted page.

Sources: [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block), [Helix Overview](https://community.rockrms.com/developer/helix/overview)

### Recipe: Validate a Rock Mobile Lava block

**Outcome:** Correct, fresh and valid mobile output for the supported shells.

1. Decide whether the content must be dynamic or can be bundled.
2. Confirm local versus server Lava processing.
3. List required merge fields and commands.
4. Check local-shell filter support.
5. Escape every user, title and URL value for its XAML position.
6. Put any required shell-version gate inside the rendered fragment.
7. Test anonymous and authenticated states.
8. Test punctuation-heavy content.
9. Validate both old and new shells when supporting a migration window.
10. Confirm whether a deployment is required for future edits.

Sources: [Mobile Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content), [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

### Recipe: Design a Lava-backed AI tool

**Outcome:** A narrow tool the model can select and use without excessive access.

1. Name the tool with a clear verb and entity.
2. Define explicit parameters and sanitize them.
3. Enforce current-person and agent authorization.
4. Prefer cache or entity access over SQL when it fits the task.
5. If static SQL is necessary, review it and keep it bounded.
6. Return a structured `AgentToolResult`.
7. Include only fields needed for the task.
8. Use dedicated filters for instructions, history, metadata and Rock references.
9. Exercise the tool with allowed, denied, empty and maximum-size inputs.
10. Inspect built-in tool logs for calls, inputs and results.

**Do not assume:**

- Internal means unrestricted.
- Chat and MCP should expose the same tools.
- The model should generate SQL.
- More context improves tool selection.

Sources: [AI Summit, 24:01](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s), [AI Summit, 67:34](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s), [AI Summit, 87:48](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s)

## Known Gaps And Live Verification

The evidence pack does not establish any reader’s installed Rock version, engine, plugins, command registrations, block settings, endpoint security, roles, schema customizations, mobile shell versions, printer configuration or external licensing. Verify those locally before implementation.

Live checks are specifically required for:

- The selected Lava engine and remaining DotLiquid compatibility issues.
- Command registration and enabled-command lists on each block, shortcode, webhook and endpoint.
- Page, block, endpoint and parent Lava Application authorization.
- `CurrentPerson` and other merge-field availability in the actual render path.
- Workflow attribute keys, field types, stored values and component setting identifiers.
- Entity-search and Dynamic LINQ behavior under target data and permissions.
- Modify/delete command behavior, validation and dependent writes.
- Community-reported change-tracker failures after an invalid modify command.
- Helix configuration rigging, which community guidance recommends storing as valid non-null JSON such as `{}` when empty.
- HTMX asset loading, sanitizer behavior, partial rendering, SEO metadata and browser state.
- Rock Mobile shell-version values and supported local filters.
- Apple TV TVML, Roku SceneGraph, mobile XAML and printer ZPL validity.
- Remote REST keys, webhook exposure, methods, rate controls and response data.
- Persisted dataset refresh schedules and dashboard metric reconciliation.
- External BI licensing.
- Final communication, workflow PDF, mobile, TV and dashboard rendering.

A successful source upload or file-content write is not proof of deployment. Community guidance recommends exact content or hash readback followed by separate rendered validation under unauthorized, intended-role and administrator contexts. That procedure itself must be adapted to the target deployment surface. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

## Source Map

### Official Lava documentation

- [Lava Reference](https://community.rockrms.com/lava) — language overview, tags, filters, commands, shortcodes and Fluid direction.
- [About Lava Fluid](https://community.rockrms.com/lava/fluid) and [Fluid Differences](https://community.rockrms.com/lava/fluid/differences) — engine transition and compatibility.
- [Entity Command](https://community.rockrms.com/lava/commands/entity-commands) — entity retrieval parameters and precedence.
- [Modify Entity](https://community.rockrms.com/lava/commands/modify-entity) and [Delete Entity](https://community.rockrms.com/lava/commands/delete-entity) — v18 write operations and security warnings.
- [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands) — workflow attribute parameters and stored formats.
- [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint) — v18 initial-render endpoint inclusion.
- [Print ZPL](https://community.rockrms.com/lava/commands/print-zpl) — v19 printer output.
- [Tag List](https://community.rockrms.com/lava/commands/taglist-commands) — registered-command discovery.
- [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava) and [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api) — remote execution and unsecured webhook caveat.
- [Types of Shortcodes](https://community.rockrms.com/lava/shortcodes/types-of-shortcodes) — inline and block contracts.

### Official product and developer documentation

- [Lava Shortcodes](https://community.rockrms.com/documentation/digital-publishing/websites/web-design-frameworks/lava-shortcodes)
- [Lava Tips for Workflows](https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows)
- [Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava)
- [Helix Overview](https://community.rockrms.com/developer/helix/overview)
- [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)
- [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)
- [Mobile Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)
- [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)
- [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

### Official training and release context

- [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)
- [SQL Command](https://community.rockrms.com/rocku/lava/sql-command)
- [Execute Command](https://community.rockrms.com/rocku/lava/execute-command)
- [AI Summit](https://www.youtube.com/watch?v=UvW68dZBcJ8)
- [RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM)
- [v19 feature preview](https://www.youtube.com/watch?v=c-wycR9HEuQ)
- [v19 ScheduleDate discussion](https://www.youtube.com/watch?v=edanHiYSDIM)

### Immutable implementation evidence

- [DynamicShortcodeBlock at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Lava/Core/Shortcodes/DynamicShortcodeBlock.cs)
- [WebRequestBlock at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Lava/Blocks/WebRequestBlock.cs)
- [DateFilterTests at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests/Lava/Filters/DateFilterTests.cs)
- [LavaShortcodeBag at commit 471fd30](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeBag.d.ts)

### Reviewed community patterns

- [Journey dashboard session](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) — persisted analytics and Lava dashboard presentation.
- [Dashboard design session](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp) — metrics, historical data and decision-focused dashboards.
- [Data Analytics Hub panel](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) — Rock-native reporting versus external BI.
- [VS Code Lava preview recipe](https://community.rockrms.com/recipes/456) — community development workflow with identity, command and JavaScript caveats.
- Organization-contributed Helix, workflow, endpoint, mobile, dashboard and deployment patterns in the supplied evidence pack are examples requiring target-instance verification unless explicitly identified as already verified public-safe conclusions.