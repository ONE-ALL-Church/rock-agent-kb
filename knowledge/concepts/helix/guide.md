---
id: authored-helix
title: Helix
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Helix

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Helix index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Helix is Rock RMS's application-building layer for interactive, server-rendered Lava experiences. It combines HTMX-style partial page updates, Lava Applications, Lava Endpoints, Lava Commands, and Lava form/control shortcodes into a way to build richer Rock pages without writing a custom C# block for every workflow. The official overview describes Helix as the next evolution of Lava for web development and frames it around four technologies: HTMX, Lava Applications, Lava Commands, and Control Shortcodes ([Helix Overview](https://community.rockrms.com/developer/helix/overview)).

For an agent doing real Rock work, the practical mental model is:

1. A **Lava Application** is the named container and route namespace.
2. A **Lava Endpoint** is the unit of backend behavior. It has a slug, HTTP method, security mode, Lava code template, optional command enablement, and cache settings ([Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)).
3. A **Lava Application Content** block is the recommended frontend host. It registers HTMX and exposes application configuration to the block template ([Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)).
4. HTMX attributes such as `hx-get`, `hx-post`, `hx-target`, and `hx-swap` call Lava Endpoints and replace part of the page with endpoint output ([HTMX Syntax Style Guides](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides)).
5. Security must be designed at the endpoint level. Users can call endpoints directly with tools outside the rendered page, so frontend hiding, IdKey obfuscation, and UI-only checks are not enough ([Security](https://community.rockrms.com/developer/helix/overview/security)).
6. Production-readiness depends on route discipline, command minimization, server-side validation, observability review, database-call control, and clear ownership.

Helix is not just "Lava with AJAX." It changes the operational risk profile of Lava. Traditional Lava often renders once during page load. Helix lets users trigger server-side Lava repeatedly through HTTP calls. That makes stale assumptions, unsafe query-string parameters, overbroad enabled commands, and expensive entity loops much more dangerous. Treat every endpoint like a small API backed by Rock security, Rock data, and Lava.

Release status matters. Older Helix documentation still refers to plugin installation and limited beta, but Rock release notes state that core Helix support for Lava Applications was added in Rock v18.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). The FAQ also notes that Helix is now in core ([FAQ](https://community.rockrms.com/developer/helix/overview/faq)). In a live Rock instance, always verify the installed Rock version, whether Helix is core or plugin-provided, and whether the relevant admin pages, blocks, shortcodes, and endpoints exist before assuming a feature path.

## 2. Scope And Terminology

This guide covers the Helix concept area: HTMX integration, Lava Applications, Lava Endpoints, Lava Application Content blocks, forms and controls, endpoint security, observability, operational guardrails, source-code landmarks, and related Rock areas such as Lava, API integrations, CMS, workflows, forms, and reporting.

Use the following terms consistently:

**Helix**
The umbrella concept for Rock's modern Lava-driven interactive web application approach. The developer docs present it as a project combining HTMX, Lava Applications, Lava Commands, and Control Shortcodes ([Helix](https://community.rockrms.com/developer/helix)).

**HTMX**
A client-side library that uses HTML attributes to issue HTTP requests and swap server-rendered responses into the DOM. In Helix, HTMX usually calls Lava Endpoints and receives HTML fragments.

**Lava Application**
A CMS model and configuration container for related endpoints. It has fields such as name, description, slug, active state, configuration rigging, and security settings. The model map identifies Lava Application as a CMS model ([Model Map](https://community.rockrms.com/ModelMap)), and the generated view model exposes name, description, slug, active state, and configuration rigging ([LavaApplicationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs)).

**Lava Endpoint**
An endpoint row belonging to a Lava Application. It is selected by application slug, endpoint slug, and HTTP method. It runs a Lava code template and returns the response body.

**Slug**
The route segment used to address an application or endpoint. The application slug and endpoint slug together form the practical route. Official docs use examples such as `group-toolbox` for an application and `my-groups` for an endpoint ([Applications](https://community.rockrms.com/developer/helix/lava-applications/applications), [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications)).

**Configuration Rigging**
Application-level JSON converted into an object available to backend endpoint Lava and frontend content-block Lava. It is intended for stable configuration, not dynamic data. If dynamic data is needed, the docs recommend a persisted dataset instead ([Applications](https://community.rockrms.com/developer/helix/lava-applications/applications)).

**Lava Application Content Block**
The frontend block intended to host Helix UI. It can link to a Lava Application, register HTMX, provide convenience styling/features, and render an initial Lava template ([Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)).

**Lava Form**
A Helix form wrapper represented with `<lava-form>` tags. It exists because Rock's WebForms page model normally has a single page-level form, while HTMX and HTML form behavior assume independent forms ([Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)).

**Control Shortcodes**
Lava shortcodes that render common form controls with Rock-style markup and validation conventions. Official Helix examples include a `textbox` shortcode and a `campuspicker` shortcode ([Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls)).

**Security Mode**
The endpoint setting controlling how access is evaluated. Source-code enums list `Endpoint Execute`, `Application View`, `Application Edit`, and `Application Administrate` ([LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs), [lavaEndpointSecurityMode.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)).

## 3. Helix Mental Model

Helix is best understood as "server-rendered interaction endpoints inside Rock."

A standard Lava page builds markup when the page renders. Helix keeps that strength but makes parts of the page addressable after initial load. A user clicks a button, changes a field, or submits a form. HTMX sends an HTTP request. Rock routes the request to a Lava Endpoint. The endpoint runs Lava, checks configured security, optionally uses enabled Lava Commands, and returns markup or another response body. HTMX swaps the response into the target part of the DOM.

A minimal flow looks like this:

```text
User action
  -> HTMX request from a Lava Application Content block
  -> application slug + endpoint slug + HTTP method match
  -> endpoint security check
  -> endpoint Lava code template executes
  -> optional entity/query/modify commands run if enabled
  -> response returned
  -> HTMX swaps response into target element
```

The "server-rendered fragments" part is essential. Helix does not require a JavaScript SPA architecture. It also does not remove the need for backend design. Each endpoint is a miniature backend surface.

The most important operational distinction is this: **the rendered UI is not the security boundary**. If a user can inspect a request in browser dev tools, they can repeat or alter that request outside the page. The security guidance explicitly warns that endpoint requests can be intercepted and replayed through tools such as curl or Postman, and therefore endpoint code must validate input and authorize the action itself ([Security](https://community.rockrms.com/developer/helix/overview/security)).

A good Helix application therefore has three layers:

1. **Page shell**: Rock page, Lava Application Content block, initial markup, layout, and target containers.
2. **Interaction endpoints**: small endpoint templates with explicit HTTP methods, security mode, validation, command enablement, and response shape.
3. **Data and domain rules**: entity queries, workflows, persisted datasets, attributes, groups, people, content channels, interactions, or other Rock systems used by the endpoint.

Do not use Helix as an excuse to build an entire unmanaged product inside Lava. The customizing guidance recommends staying as low on the customization pyramid as practical and warns that Lava Applications may be the wrong tool when custom models are needed, endpoint count grows very large, or the app becomes fragile ([Customizing Rock](https://community.rockrms.com/developer/helix/overview/customizing-rock)).

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. **Rock release notes** for version availability and shipped behavior.
2. **Official Helix developer docs** for intended configuration and authoring patterns.
3. **Rock source-code snippets** for enums, model fields, generated API surfaces, migrations, and implementation landmarks.
4. **Lava documentation** for command behavior, filters, shortcodes, observability tags, and security caveats.
5. **Model Map** for entity category and model existence.
6. **Community recipes and vendor resources** for examples only, never as authoritative security or performance guidance.

The source pack contains some version tension. For example, the plugin installation page still describes Helix as limited beta and plugin-based ([Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation)), while release notes say Lava Application support entered core in Rock v18.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)) and the FAQ says Helix is now in core ([FAQ](https://community.rockrms.com/developer/helix/overview/faq)). When this guide says "verify in a live instance," inspect the actual Rock version, installed packages, admin pages, block types, database tables, and source build rather than relying on stale documentation.

For source-code-backed facts, prefer the current branch cited in the pack, but verify against the exact Rock version running in production. The source files in the pack point to `develop`, and the generated docs mention changes by commit and date in `docs/cms/lava-applications.md` ([Rock docs source](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/cms/lava-applications.md)). Production instances may lag behind or run a maintenance branch.

## 5. Core Configuration And Data Model

### Lava Application Configuration

A Lava Application is configured with these core fields in the developer docs:

| Field | Purpose | Agent notes |
| --- | --- | --- |
| Name | Friendly admin name | Choose a name that groups related endpoints and helps Magnus/editor workflows. |
| Description | Documentation for maintainers | Put intent, owner, data surfaces, and risk notes here. |
| Slug | Application route segment | Use stable lowercase route naming. Changing it can break HTMX calls. |
| Configuration | JSON rigging object | Use for stable app-level values, not live dynamic data. |

The official Applications page states that configuration rigging is JSON converted into a dynamic object available in backend endpoints and frontend content blocks. It can be read through `ConfigurationRigging.[PropertyKey]` and is not meant to be a dynamic structure ([Applications](https://community.rockrms.com/developer/helix/lava-applications/applications)).

Source-code view models and migrations add useful implementation details. The application bag exposes `Name`, `IsActive`, `Description`, `Slug`, and `ConfigurationRigging` ([LavaApplicationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs)). The TypeScript bag exposes the same conceptual fields plus attributes and attribute values ([lavaApplicationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts)). The migration creates `LavaApplication` columns including `Name`, `Description`, `IsSystem`, `IsActive`, `SecurityMode`, `Slug`, `AdditionalSettingsJson`, `ConfigurationRiggingJson`, audit fields, GUID, and foreign key fields ([AddLavaApplications.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)).

Operationally, agents should inspect:

- Whether the application is active.
- Whether the slug matches all HTMX references.
- Whether configuration rigging is valid JSON.
- Whether any values in configuration rigging are environment-specific.
- Whether the security verbs match intended maintainers and runtime users.
- Whether the application was imported from plugin-era Helix or created in core.

### Lava Endpoint Configuration

The Endpoints docs identify these endpoint fields:

| Field | Purpose | Agent notes |
| --- | --- | --- |
| Name | Friendly endpoint name | Use action-oriented names such as `Group Search Results` or `Update Preference`. |
| Description | Maintainer documentation | Include request shape, response shape, commands, and security assumptions. |
| Slug | Endpoint route segment | Combine with application slug and HTTP method. |
| HTTP Method | Request method match | Use GET for read-only rendering; POST, PUT, DELETE for state changes. |
| Security Mode | Runtime access check | Choose endpoint-specific or application-inherited security. |
| Code Template | Lava body | Keep small and observable. |
| Enabled Lava Commands | Command allow-list | Enable only what the endpoint needs. |
| Caching Settings | Endpoint cache behavior | Use only where response varies safely. |

The source enum for HTTP method defines `Get`, `Post`, `Put`, and `Delete` ([LavaEndpointHttpMethod.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointHttpMethod.cs), [lavaEndpointHttpMethod.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointHttpMethod.ts)). The security enum defines endpoint execute and three application-based options ([LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)).

The migration creates a `LavaEndpoint` table with fields visible in the snippet such as `Name`, `Description`, `LavaApplicationId`, `Slug`, `IsSystem`, `EnabledLavaCommands`, `IsActive`, and `AdditionalSettingsJson` ([AddLavaApplications.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)). Because the source excerpt is bounded, inspect the full migration or live database schema before relying on the complete column list.

### Content Block Configuration

The Lava Application Content block is the recommended frontend integration point. The docs identify these settings:

| Setting | Purpose |
| --- | --- |
| Name | Block name, useful for editing and Magnus association |
| Application | Optional but recommended link to the target Lava Application |
| Lava Template | Initial content rendered when the block loads |

When the content block is linked to an application, the application's configuration rigging object is shared with the Lava template ([Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)). The docs recommend using the caret route notation, such as:

```html
<button
  class="btn btn-primary"
  hx-get="^/application-slug/endpoint-slug"
  hx-target=".results">
  Load
</button>
```

The `^` means the route is associated with a Lava Application, simplifying the route compared with the full API route ([Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)).

## 6. Primary Entities And Relationships

At the Rock data level, Helix centers on two CMS entities:

```text
LavaApplication
  has many LavaEndpoint

LavaEndpoint
  belongs to LavaApplication
```

The source docs describe `LavaApplication` as the namespace and `LavaEndpoint` rows as the individual routes within that namespace. Each endpoint has its own route pattern, security, and Lava body ([docs/cms/lava-applications.md](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/cms/lava-applications.md)). The service method `GetByLavApplicationId` returns endpoints belonging to a specified application ID, confirming the direct relationship in source ([LavaEndpointService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaEndpoint/LavaEndpointService.cs)).

The practical route identity is not only the URL text. The Lava Applications docs state that endpoints can share the same route when the HTTP methods differ, meaning route uniqueness is determined by the slug path plus method ([Lava Applications](https://community.rockrms.com/developer/helix/lava-applications)).

Security relationships are also important:

- Applications have standard Rock entity verbs such as View, Edit, and Administrate, according to the Applications docs ([Applications](https://community.rockrms.com/developer/helix/lava-applications/applications)).
- Newly added Lava Applications receive base security entries for Rock administrators and the Lava Application Developers role in the save hook snippet ([LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)).
- Endpoints can check their own Execute verb or rely on application-level verbs, depending on endpoint security mode ([Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)).

Agents should inspect the following when troubleshooting relationships:

- `LavaApplication.Id`, `Guid`, `Slug`, `IsActive`.
- `LavaEndpoint.LavaApplicationId`, `Slug`, `HttpMethod`, `IsActive`, `SecurityMode`.
- Auth rows for the application and endpoint.
- Whether the block references the intended application.
- Whether multiple endpoints share a slug with different HTTP methods.
- Whether a stale page/block template points to an old slug.

## 7. Common Helix Workflows

### Read-Only Partial Refresh

Use case: load filtered groups, upcoming events, prayer items, campus-specific content, or a detail panel without reloading the page.

Pattern:

1. Page loads with a Lava Application Content block.
2. Initial Lava template renders controls and an empty target.
3. A button, link, select, or form triggers `hx-get`.
4. Endpoint validates query-string parameters.
5. Endpoint runs read-only Lava and returns an HTML fragment.
6. HTMX swaps that fragment into the target.

Operational checks:

- Use `GET` only for read-only actions.
- Keep endpoint command enablement read-only where possible.
- Use `hx-target` that points to a stable container.
- Avoid returning a full page shell.
- Use observability to inspect database calls.

### State-Changing Action

Use case: update a preference, remove a following record, mark a task complete, trigger a workflow, or save form input.

Pattern:

1. Use `POST`, `PUT`, or `DELETE`, not `GET`.
2. Put controls inside `<lava-form>` if using Helix validation.
3. Validate on the client for usability and again in endpoint Lava for security.
4. Check CurrentPerson authorization against the specific entity or action.
5. Enable only the required modifying Lava Commands.
6. Return a narrow success/failure fragment.
7. Log or observe meaningful operations.

The security docs specifically warn not to use GET for modifications because links can initiate GET requests too easily ([Security](https://community.rockrms.com/developer/helix/overview/security)). The form validation docs state validation only applies to POST, PUT, and DELETE calls, not GET ([Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)).

### Admin Utility

A community recipe shows Helix used for managing Following records. It combines a Lava Application, a webpage, a Page Parameter Filter block, a Lava Application Content block, and HTML Content blocks for styling/scripts ([Manage Following records with Helix](https://community.rockrms.com/recipes/497)). Treat community recipes as examples, not best-practice authority. The recipe itself includes a community disclaimer and emphasizes updating entity type IDs to match the local Rock instance.

Agent checks for admin utilities:

- Confirm the utility is internal-only.
- Confirm endpoint Execute permission is restricted.
- Confirm entity IDs and entity type IDs match the live instance.
- Confirm modifying commands are enabled only on the endpoint that needs them.
- Confirm the endpoint does not expose records the actor cannot administrate.
- Confirm there is a rollback or audit path for destructive operations.

### Guided Search Or Finder

Helix is well-suited for server-rendered search/finder tools, especially where filters map to Rock groups, content channels, events, or persisted datasets. Triumph describes a guided group finder powered by Helix with a multi-step guided form, group details page, and high-performance results page ([Triumph Guided Group Finder](https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix)). Treat this as implementation evidence that the pattern is viable, not as a source for internal Rock behavior.

Recommended shape:

- Use one endpoint for initial results.
- Use separate endpoints for filter changes, detail panels, and join/contact actions.
- Cache only public, non-personalized fragments.
- Keep filters explicit and validate all values.
- Prefer GUIDs or IdKeys in public URLs.
- Verify group security and campus/season filters in live data.

## 8. Overview And Roadmap Deep Dive

The official overview positions Helix as a way to overcome the "render once at page load" limitation of traditional Lava by using HTMX to refresh parts of a page without full reloads ([Helix Overview](https://community.rockrms.com/developer/helix/overview)). The same overview frames Lava Applications as the way to obtain and organize the server-side endpoints needed by HTMX.

The roadmap page is explicitly speculative. It lists possible future ideas such as more recipes, more form controls, animation and drag-drop simplification, a toast framework, Real-time Engine use cases, idiomorph support, Hyperscript or Alpine.js support, and client-side templates powered by the Rock v2 Search API ([Roadmap](https://community.rockrms.com/developer/helix/overview/roadmap)). Do not plan production work as if those roadmap items exist. For each roadmap-adjacent feature, inspect the live instance and source branch.

Version caveats:

- The Helix landing page in the pack still says early alpha, while release notes say core support arrived in v18.1 ([Helix](https://community.rockrms.com/developer/helix), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- The plugin installation page still mentions limited beta and the Helix/Magnus plugin relationship ([Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation)).
- The FAQ says Helix is now in core and that Rock Mobile support is not available through the plugin because Rock Mobile is a closed framework in that context ([FAQ](https://community.rockrms.com/developer/helix/overview/faq)).
- Rock v19.1 release notes add `Body` and `RawBody` merge fields to Lava Applications ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

For agents, the roadmap implication is simple: design Helix apps with stable primitives that exist now. Do not depend on future toast, drag-drop, idiomorph, Alpine, or Real-time Engine integration unless the live instance proves it.

## 9. HTMX Deep Dive

HTMX is the interaction layer. Helix includes HTMX in Rock when using the Lava Application Content block, so authors can add attributes to HTML elements rather than writing custom JavaScript for common request/swap behavior ([Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)).

Common attributes:

| Attribute | Use |
| --- | --- |
| `hx-get` | Read-only endpoint request |
| `hx-post` | Create/action endpoint request |
| `hx-put` | Update endpoint request |
| `hx-delete` | Delete endpoint request |
| `hx-target` | Element that receives the response |
| `hx-swap` | How the response replaces or modifies target content |
| `hx-validate` | Validation-related behavior on controls, used in Helix form patterns |

The Helix syntax style guide recommends formatting HTMX-heavy markup with one attribute per line and putting CSS classes first for readability ([Syntax Style Guides](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides)). A practical house style:

```html
<a
  class="btn btn-sm btn-primary"
  hx-post="^/group-toolbox/join?GroupGuid={{ group.Guid }}"
  hx-target="closest .group-card"
  hx-swap="outerHTML">
  Join
</a>
```

Do not duplicate `hx-swap` on the same element. The source example in the docs excerpt shows a duplicate attribute; treat that as a documentation/example issue to avoid, because duplicate HTML attributes produce ambiguous behavior.

HTMX inheritance matters. The tips page notes that many HTMX attributes can inherit from parent elements and that this can be powerful but surprising ([Tips](https://community.rockrms.com/developer/helix/strategies/tips)). When debugging, inspect parent containers for inherited `hx-*` attributes before changing the endpoint.

HTMX troubleshooting checklist:

- Open browser dev tools and inspect the console.
- Inspect the Network request: URL, method, request headers, query string, body, response code, response body.
- Confirm `hx-target` matches an element present at request time.
- Confirm the response fragment is valid for the swap mode.
- Confirm parent elements are not contributing inherited attributes unexpectedly.
- Confirm the Lava Application Content block registered HTMX.
- Confirm the endpoint method matches the HTMX method.
- Confirm the caret route syntax is valid for the block context.
- Confirm the endpoint returns a fragment rather than a full page or login page.

## 10. Lava Applications Deep Dive

A Lava Application groups related endpoints behind a stable application slug. The docs describe this as a simplification for HTMX applications that need multiple server-side endpoints returning snippets ([Lava Applications](https://community.rockrms.com/developer/helix/lava-applications)).

Use a Lava Application when:

- A Rock admin/developer can express the behavior safely in Lava.
- The app fits existing Rock entities and does not need custom database models.
- The behavior is more interactive than a static Lava page.
- A custom C# block would be too much overhead.
- Endpoint count remains manageable.
- The security model is clear and testable.

Avoid or reconsider Lava Applications when:

- You need custom models or complex persistence.
- You expect dozens of endpoints and complicated state transitions.
- You need a heavily tested domain layer.
- You need advanced client-side behavior beyond the current Helix primitives.
- The endpoint must handle high traffic with strict latency budgets and complex queries.
- The team cannot safely maintain Lava Commands, endpoint security, and validation.

The Customizing Rock guidance gives concrete warning signs: custom models, 50+ endpoints, and development that feels complex or fragile ([Customizing Rock](https://community.rockrms.com/developer/helix/overview/customizing-rock)).

### Configuration Rigging Strategy

Use configuration rigging for stable settings:

```json
{
  "ResultsPageSize": 12,
  "DefaultCampusGuid": "00000000-0000-0000-0000-000000000000",
  "AllowedGroupTypeGuids": [
    "00000000-0000-0000-0000-000000000000"
  ]
}
```

Good uses:

- Page size.
- Known defined value GUIDs.
- Content channel GUIDs.
- Group type GUIDs.
- Feature flags for stable behavior.
- Environment-specific text or route names.

Poor uses:

- User-specific state.
- Frequently changing lists.
- Live search data.
- Secrets.
- API keys.
- Authorization rules that should be stored in Rock security.

If dynamic data is needed, the docs recommend a persisted dataset rather than configuration rigging ([Applications](https://community.rockrms.com/developer/helix/lava-applications/applications)). If secrets are needed, use the appropriate Rock secure configuration or integration pattern and verify with the live instance; do not place secrets in frontend-accessible block configuration.

### Application Security

Lava Applications behave like Rock entities with security verbs. The Applications docs mention standard verbs such as View, Edit, and Administrate, plus endpoint-related security options ([Applications](https://community.rockrms.com/developer/helix/lava-applications/applications)). The source save hook adds base security for administrators and the Lava Application Developers role on new applications ([LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)).

Agents should check:

- Who can view the application configuration.
- Who can edit endpoints.
- Who can administrate the application.
- Whether endpoint security mode references application permissions.
- Whether a page's block security conflicts with endpoint security.
- Whether unauthenticated users can call public endpoints intentionally.
- Whether security inherited from plugin-era migration is still appropriate.

## 11. Lava Endpoints Deep Dive

Endpoints are the core unit of work. The docs call them the fundamental units that encapsulate logic called from the client ([Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)).

### Routing

The practical route uses:

```text
/application-slug/endpoint-slug
```

Inside a Lava Application Content block, use the caret shorthand:

```html
<div
  hx-get="^/people-search/results?CampusGuid={{ campus.Guid }}"
  hx-target=".people-search-results">
</div>
```

The docs state the caret marks the route as associated with a Lava Application ([Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)). If the caret shorthand fails, inspect the rendered HTML, content block type, app selection, and the full request URL in dev tools.

The source docs mention a request routing model in which requests route to a Lava Application router and matching endpoint, while other Lava can call endpoints through `renderlavaendpoint` ([docs/cms/lava-applications.md](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/cms/lava-applications.md)). Verify exact route prefixes in the live Rock version, because docs and source snippets may differ by branch.

### HTTP Methods

Endpoint methods are `GET`, `POST`, `PUT`, and `DELETE` in source ([LavaEndpointHttpMethod.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointHttpMethod.cs)).

Use them this way:

| Method | Use |
| --- | --- |
| GET | Read-only fragments and queries |
| POST | Create, submit, trigger, or action endpoints |
| PUT | Update an existing entity/state |
| DELETE | Delete/remove action |

Do not modify data in GET endpoints. The security docs explicitly call this out as unsafe because GET requests can be initiated from cross-site links and are easier to trigger accidentally ([Security](https://community.rockrms.com/developer/helix/overview/security)).

### Security Modes

Source and docs identify these modes:

| Mode | Meaning |
| --- | --- |
| Endpoint Execute | Check the Execute verb on the specific endpoint |
| Application View | Use application-level View permission |
| Application Edit | Use application-level Edit permission |
| Application Administrate | Use application-level Administrate permission |

The Endpoints docs describe Endpoint Execute as checking whether `CurrentPerson` can run the endpoint, while application modes use application permissions to reduce administrative overhead ([Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)). The enum values are confirmed in source ([LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)).

Use Endpoint Execute for public or sensitive actions where individual endpoint authorization matters. Use application-level modes for consistent internal tools with clear app-level roles. Do not use broad application permissions for destructive endpoints unless every user with that permission should run every destructive action.

### Enabled Lava Commands

Endpoint code templates can enable Lava Commands. The Lava Commands docs emphasize that commands can bypass built-in security and business logic, so they must be enabled intentionally ([Getting Started With Lava Commands](https://community.rockrms.com/lava/commands)). Endpoint-level command enablement should be minimal.

Common command risk levels:

| Command family | Risk |
| --- | --- |
| Entity read | Medium: can expose data and create expensive queries |
| SQL | High: injection and performance risks |
| Modify Entity | High: data integrity risks |
| Delete Entity | Very high: destructive |
| DB Transaction | High: batching changes can magnify errors |
| HTTP Response | Medium: response control can affect clients |
| Web Request | Medium/high: outbound calls, secrets, timeouts |
| Workflow Activate | Medium/high: can trigger side effects |

The Helix Lava Commands page now points authors to the main Lava documentation for command details, including Delete Entity, Modify Entity, DB Transaction, HTTP Response, and Render Lava Endpoint ([Lava Commands](https://community.rockrms.com/developer/helix/lava-commands)).

### Merge Fields And Request Body

Endpoint Lava commonly uses query-string values, current person context, application configuration, and request body values. Rock v19.1 release notes state that Body and RawBody merge fields were added to Lava Applications ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). The source docs also mention the Body/RawBody change as a 2026-03-10 commit ([docs/cms/lava-applications.md](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/cms/lava-applications.md)).

Before writing an endpoint that depends on `Body` or `RawBody`, verify the live version includes the feature. In older versions, a JSON POST may not expose request body data as expected.

## 12. Forms And Controls Deep Dive

Rock's WebForms architecture creates a form mismatch. HTMX and HTML expect independent forms, but ASP.NET WebForms has one large page form. Helix introduces `<lava-form>` as an independent form abstraction to support validation and avoid nested form problems ([Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)).

### Lava Form Pattern

Use `<lava-form>` around related controls and actions:

```html
<lava-form>
  {[ textbox name:'lastname' label:'Last Name' value:'' isrequired:'true' ]}

  <button
    class="btn btn-primary"
    hx-post="^/people-search/save"
    hx-target=".form-response">
    Save
    <img
      src="/Assets/Images/Spinners/small-circle-light.svg"
      class="htmx-indicator">
  </button>

  <div class="form-response"></div>
</lava-form>
```

This is an illustrative pattern. Verify exact shortcode parameters in the live instance by checking `Admin Tools > CMS Configuration > Lava Shortcodes` and the Helix category, as recommended by the Using Form Controls docs ([Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls)).

### Control Shortcodes

The provided controls reduce verbose Rock form-control markup. The docs show that a textbox can be rendered with a shortcode rather than hand-authored control markup, and that more complex controls such as campus pickers are available ([Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls)).

Do not edit shipped Helix shortcodes in place. The docs warn that modifying them is discouraged because future updates may overwrite changes ([Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls)). For custom needs:

- Create a new shortcode.
- Put it in an appropriate category.
- Use project-specific naming.
- Document parameters.
- Enable only necessary Lava Commands.
- Prefer wrapping common label/control markup through a shared base control pattern.

The Creating New Controls docs state that most new controls are developed from the `rock-control` base shortcode and that common parameters include label-style information and control configuration ([Creating New Controls](https://community.rockrms.com/developer/helix/forms-controls/creating-new-controls)). The general Lava shortcode documentation explains choosing inline vs block shortcodes based on the amount and shape of data passed ([Authoring Shortcodes](https://community.rockrms.com/lava/shortcodes/authoring-shortcodes)).

### Validation

Helix form validation applies only inside `<lava-form>` tags and only for POST, PUT, and DELETE calls. It does not run for GET ([Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)).

Validation pattern:

- Use native HTML5 validation attributes.
- Provide validation messages with the convention expected by Helix controls.
- Use `<lava-validationsummary />` inside the `<lava-form>` when a custom summary location is needed.
- Always duplicate critical validation server-side in endpoint Lava.

The docs explicitly warn that client-side validation is not enough because endpoints can be accessed directly ([Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)).

### Loading Indicators

HTMX supports loading indicators, and Helix provides spinner paths. For Rock v18 or later, the docs show spinner assets under `/Assets/Images/Spinners/...`; for plugin-era Helix, paths are under `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/...` ([Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)).

Agent checks:

- If spinner images 404, verify Rock version and plugin/core path.
- Keep button indicators small.
- Do not make the indicator shift layout.
- Use `htmx-indicator` class.
- For long-running results, use a larger indicator near the target region.

## 13. Security And Observability Deep Dive

### Security Principles

The Helix security page is direct: endpoints can be accessed outside the frontend, parameters can be modified, and endpoint authors must validate input and secure data access ([Security](https://community.rockrms.com/developer/helix/overview/security)).

Security rules for agents:

1. Treat every endpoint as an API.
2. Do not trust query-string IDs.
3. Prefer GUIDs or IdKeys over sequential integer IDs in public routes.
4. Do not rely on GUIDs or IdKeys as the only control.
5. Check the actor's right to view or modify the specific entity.
6. Use GET only for read-only operations.
7. Validate all query-string and body inputs.
8. Sanitize SQL inputs or avoid SQL entirely.
9. Enable only required Lava Commands.
10. Return only the data needed by the UI fragment.
11. Test direct endpoint access while logged out, logged in as a low-privilege user, and logged in as the intended role.

Attribute security also matters. Lava attribute filters gained additional security considerations around Rock v17.5, including an optional parameter to bypass attribute-level security checks. The docs warn to use bypassing only when appropriate because it skips a safeguard ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)). In Helix, this is especially important because endpoint output may be called dynamically and exposed outside the initial page context.

### Observability

The Helix Observability docs state that each Lava Endpoint call has an observability activity named with the endpoint and application, and that root activity attributes include `rock.lava_endpoint` and `rock.lava_application`; the HTTP method is already part of the activity ([Observability](https://community.rockrms.com/developer/helix/lava-applications/observability)).

Operationally, use observability to answer:

- Which endpoint is slow?
- Which HTTP method is being called?
- Which application owns the endpoint?
- How many database calls does the endpoint trigger?
- Did a UI change increase endpoint latency?
- Are users repeatedly triggering an expensive endpoint?
- Are errors isolated to one endpoint or application?

Lava also has an `observe` command, available since v16.3 according to the Lava docs, that wraps contained Lava in an observability activity and allows custom tags ([Observe](https://community.rockrms.com/lava/tags/observe)). Use it inside complex endpoint templates to separate expensive sub-operations, but avoid over-instrumenting every trivial line.

Example pattern:

```liquid
{% observe name:'Group Finder Query' app-feature:'group-finder' app-feature-version:'1' %}
  {% group where:'GroupTypeId == {{ groupTypeId }}' limit:'25' %}
    ...
  {% endgroup %}
{% endobserve %}
```

Verify the organization tag prefix and tag naming conventions locally. The docs recommend organization-prefixed tags in the observe command ([Observe](https://community.rockrms.com/lava/tags/observe)).

## 14. Strategies And Limitations Deep Dive

The Strategies section currently contains tips, related entities, and limitations. The related-entities page is marked as writing in progress in the source pack, so do not infer hidden behavior from it ([Related Entities](https://community.rockrms.com/developer/helix/strategies/related-entities)).

Known documented limitations:

- Lava `{% javascript %}` and `{% stylesheet %}` commands do not work in Helix endpoint-rendered fragments because they rely on `RockPage`, and dynamic partial updates do not have that page execution context ([Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)).

Practical implications:

- Put required page JavaScript and CSS in the page shell, theme, asset bundle, or a stable HTML Content block.
- Do not expect an endpoint fragment to register scripts/styles with the full page.
- Keep endpoint output as markup and data, not asset registration.
- If an endpoint returns markup that depends on JavaScript initialization, verify that the necessary initializer runs after HTMX swaps.
- Use HTMX lifecycle events only when necessary and document them in the page shell.

The Tips docs recommend using browser dev tools and checking HTMX attribute inheritance ([Tips](https://community.rockrms.com/developer/helix/strategies/tips)). That should be the first debugging branch for most broken interactions.

## 15. Related Rock Areas: Lava, Api Integrations, Security, Cms, Workflows, Forms, Htmx, Observability

### Lava

Helix is built on Lava. Agents must know Lava output tags, tags, filters, entity commands, commands, and shortcodes. The Lava reference describes Lava as Rock's templating language and notes the transition away from DotLiquid support around v17 ([Lava](https://community.rockrms.com/lava)). Verify the active Lava engine and syntax compatibility in the live instance.

### API Integrations

Helix endpoints are not the same as Rock REST API v1/v2. Rock's API documentation distinguishes API v1 and API v2 resources and links to Lava API concepts ([API Documentation](https://community.rockrms.com/api-docs)). Use Rock API for external integrations when appropriate; use Helix for Rock-hosted interactive pages. Do not expose Helix endpoints as public integration APIs without a full security and compatibility review.

### Security

Rock security applies at multiple layers: page/block security, application security, endpoint security, entity security, attribute security, command enablement, and custom Lava checks. Never assume one layer covers all cases.

### CMS

Lava Applications are CMS models. Source records and Model Map place Lava Application in the CMS category ([Model Map](https://community.rockrms.com/ModelMap)). Admin pages and blocks for Lava Applications should be managed as CMS configuration.

### Workflows

Helix can trigger workflows if the appropriate Lava Commands or endpoint logic are enabled. Use this for bounded actions, not as an unreviewed business-process engine. If an endpoint triggers workflow activation, verify workflow security, input attributes, and idempotency.

### Forms

Helix forms solve the WebForms nested-form issue through `<lava-form>`, control shortcodes, and validation conventions ([Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)).

### HTMX

HTMX controls request/response behavior through attributes. Debug with browser dev tools, not by staring only at Lava, and verify `hx-*` request/target/swap behavior against the Helix HTMX docs ([HTMX](https://community.rockrms.com/developer/helix/htmx)).

### Observability

Helix endpoint calls are observable, and custom `observe` spans can be added inside Lava. Use these before optimizing blindly ([Observability](https://community.rockrms.com/developer/helix/lava-applications/observability), [Observe](https://community.rockrms.com/lava/tags/observe)).

## 16. Administration And Operational Guardrails

Use this checklist before shipping a Helix application:

| Area | Guardrail |
| --- | --- |
| Ownership | Application description names owner, purpose, and support path. |
| Version | Installed Rock version supports required features. |
| Route stability | Slugs are final and references are searched before changes. |
| Security | Endpoint modes are intentional and tested directly. |
| Commands | Each endpoint enables only required commands. |
| Validation | Client and server validation both exist for writes. |
| Observability | Slow or complex endpoints are observable. |
| Caching | Cache settings do not leak personalized data. |
| Accessibility | Controls have labels, validation messages, and predictable focus behavior. |
| Failure handling | Endpoint returns useful error fragments. |
| Upgrade path | Plugin/core differences are documented. |
| Source control | Magnus or other export path captures application and endpoint content where available. |

Use separate environments:

- Develop in a non-production Rock instance.
- Test with realistic data volume.
- Test as anonymous, low-privilege, intended user, and admin.
- Promote with documented steps.
- Verify post-deploy endpoints and observability.

If Magnus is used, the docs say it allows editing applications and endpoints in VS Code and helps group front-end content blocks with backend endpoints ([Magnus](https://community.rockrms.com/developer/helix/lava-applications/magnus)). Verify Magnus installation and sync behavior locally; do not assume every Lava Application is source-controlled.

## 17. Developer, API, Lava, And Source-Code Landmarks

Key source-code and documentation landmarks:

| Landmark | Why it matters |
| --- | --- |
| [docs/cms/lava-applications.md](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/cms/lava-applications.md) | Source documentation for mental model, commits, Body/RawBody note, RenderLavaEndpoint notes. |
| [LavaApplicationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaApplicationDetail/LavaApplicationBag.cs) | Confirms exposed app detail fields. |
| [lavaApplicationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts) | Confirms Obsidian frontend bag fields. |
| [LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs) | Shows base security added for admins and Lava Application Developers. |
| [LavaApplicationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplicationService.cs) | Shows cache-assisted GUID lookup. |
| [LavaEndpointService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaEndpoint/LavaEndpointService.cs) | Shows endpoint lookup by LavaApplicationId. |
| [LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs) | Source enum for endpoint security modes. |
| [LavaEndpointHttpMethod.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointHttpMethod.cs) | Source enum for endpoint HTTP methods. |
| [LavaApplicationsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaApplicationsController.CodeGenerated.cs) | Generated API v2 model surface for Lava Applications. |
| [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs) | Generated API v2 model surface for Lava Endpoints. |
| [AddLavaApplications.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs) | Migration table/field creation and plugin cleanup context. |
| [Lava Commands](https://community.rockrms.com/lava/commands) | Command enablement and security caveats. |
| [Render Lava Endpoint](https://community.rockrms.com/page/3761) | Endpoint rendering command reference, linked from Helix/Lava docs. Verify full details live. |

The generated API controllers show authenticated CRUD model endpoints for Lava Applications and Endpoints under `api/v2/models/lavaapplications` and `api/v2/models/lavaendpoints`, with secured read/write actions in the snippets ([LavaApplicationsController](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaApplicationsController.CodeGenerated.cs), [LavaEndpointsController](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs)). These are model-management APIs, not the same thing as calling a Lava Endpoint route for HTMX interaction.

## 18. Reporting, Analytics, And Model Map

Model Map identifies Lava Application as a CMS model ([Model Map](https://community.rockrms.com/ModelMap)). The generated model services include queryable attribute support for both LavaApplication and LavaEndpoint in code-generated service files ([LavaApplicationService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/LavaApplicationService.CodeGenerated.cs), [LavaEndpointService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/LavaEndpointService.CodeGenerated.cs)).

Reporting opportunities:

- List all Lava Applications and endpoints.
- Identify inactive applications with active endpoints.
- Identify endpoints with modifying commands enabled.
- Identify public or broadly executable endpoints.
- Identify endpoints using SQL command.
- Identify endpoints without descriptions.
- Identify duplicate slug/method patterns.
- Identify endpoints modified recently.
- Identify application configuration rigging containing environment-specific values.
- Correlate observability traces with endpoint names and applications.

Potential report fields to inspect in a live instance:

```text
LavaApplication.Id
LavaApplication.Name
LavaApplication.Slug
LavaApplication.IsActive
LavaApplication.SecurityMode
LavaApplication.ConfigurationRiggingJson
LavaEndpoint.Id
LavaEndpoint.Name
LavaEndpoint.LavaApplicationId
LavaEndpoint.Slug
LavaEndpoint.IsActive
LavaEndpoint.EnabledLavaCommands
LavaEndpoint.AdditionalSettingsJson
```

Because the bounded source excerpt does not show the full endpoint schema, inspect `INFORMATION_SCHEMA.COLUMNS`, the model class, or the full migration in the exact Rock version before writing production SQL.

## 19. Version And Release Caveats

Known version facts from the source pack:

| Version | Fact | Source |
| --- | --- | --- |
| v16.3 | `observe` Lava tag documented as available. | [Observe](https://community.rockrms.com/lava/tags/observe) |
| v17 | Lava docs discuss ending DotLiquid support with v17. | [Lava](https://community.rockrms.com/lava) |
| v17.5 | Attribute security behavior and bypass parameter discussed. | [Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters) |
| v18.1 | Core release notes say Helix support for Lava Applications was added to core. | [Rock Core Release Notes](https://www.rockrms.com/releasenotes) |
| v18+ | Loading indicator docs use `/Assets/Images/Spinners/...` paths. | [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| plugin-era Helix | Spinner paths under `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/...`. | [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| v19.1 | Body and RawBody merge fields added to Lava Applications. | [Rock Core Release Notes](https://www.rockrms.com/releasenotes) |

Caveats:

- Some docs still describe Helix as alpha/beta or plugin-based. Verify against live version.
- Release notes in the pack say v19.1 is beta as of May 20, 2026. Treat v19.1 features as version-dependent.
- Source snippets point to the `develop` branch. Production may differ.
- Model Map excerpt is minimal. Use live model/entity inspection for exact reporting.
- Community recipes may be written for Rock 16.6 or plugin Helix and may not match core Helix behavior exactly ([Manage Following records with Helix](https://community.rockrms.com/recipes/497)).

## 20. Implementation Playbooks

### Playbook A: Build A Read-Only Results Panel

1. Create a Lava Application with name, description, slug, and stable configuration rigging.
2. Create a GET endpoint named `Results`.
3. Use Endpoint Execute or Application View security depending on audience.
4. Enable only read commands needed for the query.
5. Add a Lava Application Content block to the page.
6. Link the block to the application.
7. Render filter controls and an empty result container.
8. Use `hx-get="^/app-slug/results"` and `hx-target`.
9. Validate all query-string values in the endpoint.
10. Return only the result fragment.
11. Test as intended and unintended users.
12. Inspect observability for database call count and latency.

### Playbook B: Build A Safe Update Form

1. Create or reuse a Lava Application.
2. Create a PUT or POST endpoint for the update.
3. Set Endpoint Execute security for precise control.
4. Enable only required modify commands.
5. Wrap controls in `<lava-form>`.
6. Use control shortcodes where possible.
7. Add client validation for usability.
8. Add server-side validation in endpoint Lava.
9. Use GUID or IdKey identifiers where possible.
10. Check actor permission against the target entity.
11. Return a success or validation-error fragment.
12. Test direct endpoint calls with altered parameters.

### Playbook C: Convert A Static Lava Page To Helix

1. Identify the interactive parts only.
2. Keep static page shell in the content block.
3. Split each interaction into a small endpoint.
4. Keep GET endpoints read-only.
5. Move shared constants into configuration rigging.
6. Move dynamic reusable data into persisted datasets or normal Rock entities.
7. Add loading indicators.
8. Add observability around expensive subqueries.
9. Remove endpoint reliance on `{% javascript %}` and `{% stylesheet %}`.
10. Test the page with JavaScript console and network tools open.

### Playbook D: Audit An Existing Helix App

1. Inventory applications and endpoints.
2. Confirm live Rock version and plugin/core status.
3. Review descriptions for ownership and purpose.
4. Review all slugs and page references.
5. Review endpoint HTTP methods.
6. Review endpoint security mode.
7. Review enabled Lava Commands.
8. Review endpoint code for SQL, entity security bypass, attribute security bypass, and modification logic.
9. Test direct access.
10. Review observability.
11. Document findings and recommended fixes.

## 21. Troubleshooting Decision Tree

### The button does nothing

Check browser console first. The Helix tips page recommends dev tools because HTMX configuration errors often surface there ([Tips](https://community.rockrms.com/developer/helix/strategies/tips)).

Then inspect:

- Is HTMX loaded?
- Is the block a Lava Application Content block?
- Is the element inside markup rendered after page load?
- Is the `hx-*` attribute valid?
- Is another parent `hx-*` attribute inherited unexpectedly?
- Is JavaScript blocked by a page error?

### The request is sent but endpoint is not found

Check:

- Application slug.
- Endpoint slug.
- Caret notation.
- HTTP method.
- Endpoint active state.
- Application active state.
- Whether route changed during migration.
- Whether the full endpoint route differs in this Rock version.

### The endpoint returns login markup or unauthorized

Check:

- CurrentPerson context.
- Page/block security versus endpoint security.
- Endpoint Security Mode.
- Endpoint Execute permission.
- Application View/Edit/Administrate permission if inherited.
- Anonymous access expectations.
- Whether the request is cross-site or missing auth cookies.

### The endpoint works in UI but fails when called directly

This usually means the UI is supplying hidden context that the endpoint assumes. Fix the endpoint, not only the UI.

Check:

- Required parameters.
- Body parsing.
- CSRF or auth expectations.
- Server-side validation.
- Explicit entity authorization.
- Error handling for missing values.

### Validation does not run

Check:

- Controls are inside `<lava-form>`.
- Method is POST, PUT, or DELETE.
- Required validation attributes are present.
- Validation summary is inside `<lava-form>`.
- Shortcode output includes expected IDs and messages.
- GET requests are not expected to validate ([Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)).

### Spinner does not show

Check:

- `htmx-indicator` class exists.
- Image path matches core v18+ or plugin-era path.
- Request is long enough to see it.
- CSS does not hide it permanently.
- The indicator is inside or associated with the triggering element.

### Endpoint is slow

Check observability for endpoint activity name and database calls ([Observability](https://community.rockrms.com/developer/helix/lava-applications/observability)).

Then inspect:

- Entity command loops.
- Missing `limit`.
- Missing pagination.
- Attribute prefetch patterns.
- Security checks on large entity result sets.
- Repeated endpoint calls from HTMX triggers.
- Cache eligibility.
- SQL command performance.
- Nested calls to Render Lava Endpoint.
- External web requests and timeout behavior.

### Endpoint modifies wrong data

Stop using the endpoint until reviewed.

Check:

- Identifier source.
- GUID/IdKey mapping.
- CurrentPerson authorization.
- Entity type IDs in configuration.
- Live instance entity IDs versus copied recipe IDs.
- HTTP method.
- Server-side validation.
- Enabled modify/delete commands.
- Whether multiple endpoints share a slug with different methods.

## 22. Agent Task Recipes

### Recipe: Find The Endpoint Behind A Button

1. Inspect the rendered element.
2. Read `hx-get`, `hx-post`, `hx-put`, or `hx-delete`.
3. Note the application slug and endpoint slug.
4. Note the HTTP method.
5. Find the Lava Application by slug.
6. Find the Lava Endpoint by slug and method.
7. Check active state, security mode, enabled commands, and code template.
8. Test the request in browser dev tools.
9. Review observability using endpoint/application names.

### Recipe: Determine Whether A Helix App Is Public-Safe

1. Identify every endpoint.
2. Mark each endpoint read-only or write/destructive.
3. Confirm GET endpoints do not modify data.
4. Confirm public endpoints expose only public data.
5. Confirm identifiers use GUIDs or IdKeys where appropriate.
6. Confirm direct endpoint calls cannot access unauthorized records.
7. Confirm SQL input is sanitized or removed.
8. Confirm no sensitive attribute security bypass exists.
9. Confirm cache settings cannot leak personalized fragments.
10. Document residual risk.

### Recipe: Upgrade A Plugin-Era Helix App

1. Verify current Rock version.
2. Verify whether Helix is core, plugin, or both.
3. Inventory plugin asset paths.
4. Replace spinner paths if moving to Rock v18+ core asset paths.
5. Verify Lava Application tables and endpoints migrated.
6. Verify Magnus or source export still works.
7. Verify security rows after migration.
8. Test routes and caret notation.
9. Test Body/RawBody only if the version supports them.
10. Remove plugin assumptions from documentation.

### Recipe: Review A Community Recipe Before Use

1. Read the recipe as an example, not an authority.
2. Verify Rock version compatibility.
3. Replace all entity type IDs with live instance values.
4. Replace all group, role, page, block, and defined value IDs with live values.
5. Review enabled Lava Commands.
6. Review endpoint Execute permissions.
7. Run in a non-production environment.
8. Test with a low-privilege account.
9. Add observability.
10. Document rollback.

### Recipe: Add Observability To A Complex Endpoint

1. Find the slow logical block.
2. Wrap only that block with `{% observe %}`.
3. Use a stable name.
4. Add organization-prefixed tags.
5. Escape tag values if dynamic.
6. Compare traces before/after.
7. Remove noisy instrumentation if it does not help.





















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `4`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms' single-page form model, which matters when validating or troubleshooting nested form behavior. | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | risk | Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| official | source_summary | Helix is a Rock web-development surface that combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. | [source](https://community.rockrms.com/developer/helix/overview) |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->









































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->





















## 23. Source Map And Dependency Notes

Primary Helix docs:

- [Helix](https://community.rockrms.com/developer/helix)
- [Overview](https://community.rockrms.com/developer/helix/overview)
- [Customizing Rock](https://community.rockrms.com/developer/helix/overview/customizing-rock)
- [Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation)
- [FAQ](https://community.rockrms.com/developer/helix/overview/faq)
- [Roadmap](https://community.rockrms.com/developer/helix/overview/roadmap)
- [Security](https://community.rockrms.com/developer/helix/overview/security)

HTMX:

- [HTMX](https://community.rockrms.com/developer/helix/htmx)
- [Learning More](https://community.rockrms.com/developer/helix/htmx/learning-more)
- [Syntax Style Guides](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides)

Lava Applications:

- [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications)
- [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications)
- [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)
- [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)
- [Magnus](https://community.rockrms.com/developer/helix/lava-applications/magnus)
- [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability)

Forms and controls:

- [Forms & Controls](https://community.rockrms.com/developer/helix/forms-controls)
- [Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)
- [Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls)
- [Creating New Controls](https://community.rockrms.com/developer/helix/forms-controls/creating-new-controls)
- [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)
- [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)

Strategies:

- [Strategies](https://community.rockrms.com/developer/helix/strategies)
- [Tips](https://community.rockrms.com/developer/helix/strategies/tips)
- [Related Entities](https://community.rockrms.com/developer/helix/strategies/related-entities)
- [Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)

Related Lava and API docs:

- [Lava](https://community.rockrms.com/lava)
- [Lava Commands](https://community.rockrms.com/lava/commands)
- [Helix Lava Commands](https://community.rockrms.com/developer/helix/lava-commands)
- [Observe](https://community.rockrms.com/lava/tags/observe)
- [Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)
- [Entity Command](https://community.rockrms.com/lava/commands/entity-commands)
- [Cache Command](https://community.rockrms.com/lava/commands/cache-commands)
- [Web Request Command](https://community.rockrms.com/lava/commands/web-request-commands)
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
- [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)
- [API Documentation](https://community.rockrms.com/api-docs)

Release, model, source, and examples:

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- [Model Map](https://community.rockrms.com/ModelMap)
- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)
- [Rock source docs for Lava Applications](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/cms/lava-applications.md)
- [Manage Following records with Helix](https://community.rockrms.com/recipes/497)
- [Triumph Guided Group Finder](https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix)

Dependency notes:

- Helix depends heavily on Lava competence. Agents should understand entity commands, filters, shortcodes, and command security before editing endpoints.
- Helix depends on Rock CMS configuration. Page/block placement and security still matter.
- Helix depends on Rock security. Endpoint mode is necessary but not sufficient for entity-level authorization.
- Helix depends on HTMX behavior. Browser dev tools are part of the normal troubleshooting workflow.
- Helix depends on observability for production confidence. Endpoint-level traces should be reviewed for non-trivial apps.
- Helix may depend on Magnus for practical source editing in some environments, but Magnus presence and behavior must be verified live.
- Helix version behavior must be verified in the live Rock instance, especially around core/plugin status, Body/RawBody merge fields, spinner asset paths, and endpoint route handling.
