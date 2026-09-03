---
id: authored-helix
title: Helix
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "3f491523f1f74bdf50c552bbdb164b386550c469eb83cff08949ba18dbe17387"
---

# Helix

## Agent Summary

Helix is Rock’s server-driven web-development surface for building interactive pages with HTMX, Lava Applications, endpoint-executed Lava, Lava Commands, and form-control shortcodes. A typical Helix interaction begins in a Lava Application Content block, sends an HTMX request to a Lava Endpoint, and replaces part of the current page with the endpoint’s rendered response. Because endpoints can expose data or perform mutations, treat every endpoint as independently callable and subject it to explicit authorization, input-validation, data-integrity, and performance review. [Helix overview](https://community.rockrms.com/developer/helix/overview) [Helix security](https://community.rockrms.com/developer/helix/overview/security)

For an existing application, inspect the application and endpoint records before changing its page markup. Record the application slug and configuration, then inspect each endpoint’s slug, HTTP method, security mode, code template, enabled Lava commands, caching configuration, and active state. The same application and endpoint slugs may identify more than one endpoint when the HTTP methods differ. [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications) [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

Do not infer readiness from a successful administrator test. Verify the installed Rock version or plugin packaging, anonymous and intended-role access, mutation behavior, server-side validation, rendered page behavior, and observability data. A reviewed read-only installation probe confirmed that Lava Applications and Lava Endpoints are secured entities with endpoint metadata and authorization records, but that conclusion does not prove any particular endpoint is configured correctly.

## Scope And Boundaries

This guide covers:

- Helix’s operational model and maturity caveats.
- HTMX calls from Rock pages.
- Lava Applications, configuration rigging, content blocks, and endpoints.
- HTTP methods, request merge fields, and endpoint responses.
- Lava Forms, control shortcodes, validation, and loading indicators.
- Application and endpoint security.
- Endpoint observability.
- Development strategies, limitations, and production-readiness checks.
- Reviewed community implementation patterns, clearly separated from official behavior.

Detailed Lava syntax and command-specific semantics belong in the [official Lava documentation](https://community.rockrms.com/lava). Domain-specific data models—such as communications, attendance, registration, groups, workflows, or AI retrieval—belong in their owning concepts. This guide addresses only the Helix boundary around those domains.

The evidence pack contains no reviewed live result for a specific endpoint, page, role, plugin installation, cache policy, rate limit, or production deployment. Those conditions must be checked in the target installation under **Known Gaps And Live Verification**.

## Mental Model

A Helix application is best understood as a server-rendered request loop:

```text
Page request
  -> Lava Application Content block renders the initial interface
  -> HTMX-enabled element issues GET, POST, PUT, or DELETE
  -> application slug + endpoint slug + HTTP method select an endpoint
  -> endpoint authorization and server-side validation must pass
  -> enabled Lava commands and endpoint template perform the work
  -> endpoint returns an HTML fragment or response instructions
  -> HTMX replaces or updates the selected page region
```

The Lava Application is the organizing and security boundary. Its endpoints are the individual work units. The Content block is the preferred page-hosted front end: it registers HTMX and lets templates use the caret route form, such as `^/application-slug/endpoint-slug`, instead of hard-coding the complete API path. [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications) [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

This loop has three separate security layers:

1. Whether the application or endpoint permits the caller to execute it.
2. Whether the endpoint independently validates every query, form, header, and body value.
3. Whether the caller may view or modify the particular entity selected by those values.

An opaque identifier such as an IdKey or GUID can reduce easy guessing, but it does not replace the third check. [Helix security](https://community.rockrms.com/developer/helix/overview/security)

## Overview And Roadmap

Helix extends Lava-driven pages beyond a single render at page load. HTMX supplies partial-page requests and replacement; Lava Applications organize the server-side endpoints; Lava Commands can read, modify, delete, transact, or shape HTTP responses when enabled; and control shortcodes reduce the markup required for Rock-style forms. [Helix overview](https://community.rockrms.com/developer/helix/overview) [Lava Commands](https://community.rockrms.com/developer/helix/lava-commands)

Helix should sit only as high in the customization stack as the application requires. The official customization guidance identifies three signals that a Lava Application may have outgrown the approach:

- It requires custom models.
- It is approaching or exceeding 50 endpoints.
- Development has become complex and fragile.

At that point, assess a purpose-built custom solution instead of continuing to expand the Lava Application. [Customizing Rock](https://community.rockrms.com/developer/helix/overview/customizing-rock)

The published roadmap is not a commitment. It lists ideas such as additional recipes and controls, simplified animation and drag-and-drop, toast support, real-time use cases, alternative DOM-morphing or client scripting integrations, and client-side templates. Do not design a production dependency around any roadmap item until the target Rock release or installed package proves it exists. [Helix roadmap](https://community.rockrms.com/developer/helix/overview/roadmap)

## HTMX

The Helix Content block registers HTMX, allowing ordinary HTML elements to describe their request and replacement behavior through attributes. A typical element identifies:

- The method and caret route, such as `hx-get` or `hx-post`.
- The destination region through `hx-target`.
- Optional replacement behavior through attributes such as `hx-swap`.
- Optional progress behavior through `hx-indicator`.

Use one HTML attribute per line and put the CSS `class` attribute first. This style is official readability guidance, not a runtime requirement. [HTMX syntax style guide](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides)

When an interaction behaves unexpectedly:

- Inspect the browser console for HTMX diagnostics.
- Confirm that `hx-target` resolves to the intended element.
- Walk up the DOM and inspect inherited HTMX attributes on ancestor elements.
- Confirm that the element’s method matches the configured endpoint method.
- Inspect the returned fragment rather than assuming the initial page template produced the faulty markup.

HTMX attribute inheritance is useful but can cause unexpected behavior when a parent’s settings silently affect a descendant. [Helix strategies: tips](https://community.rockrms.com/developer/helix/strategies/tips)

External HTMX examples may illustrate the framework, but their server-side assumptions do not automatically describe Lava Applications. Translate them through Rock’s Content block, endpoint routing, security, and Lava execution model. [HTMX learning resources](https://community.rockrms.com/developer/helix/htmx/learning-more)

## Lava Applications

A Lava Application groups related endpoints and provides a shared namespace, configuration, and security boundary. Its documented settings include:

- **Name:** the administrative label.
- **Description:** documentation for maintainers.
- **Slug:** the route segment used to identify the application.
- **Configuration rigging:** optional JSON converted into a dynamic object available to endpoint and linked Content block templates.

Templates read configuration properties through `ConfigurationRigging`. The official guidance treats this configuration as static application rigging; use a Persisted Dataset when the required structure is dynamic. [Application configuration](https://community.rockrms.com/developer/helix/lava-applications/applications)

Applications use Rock’s standard View, Edit, and Administrate verbs for management and add Execute View, Execute Edit, and Execute Administrate for endpoint execution patterns. The documentation also describes initialization behavior that grants application-management access to the Lava Application Developers and Rock Administration roles when a new application is created. Immutable Rock source at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` shows the save hook adding View, Edit, and Administrate authorization records for those roles. Treat that code as implementation evidence for that commit, then verify the installed version and actual authorization records. [Application security](https://community.rockrms.com/developer/helix/lava-applications/applications) [Application save hook](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)

### Lava Application Content block

The recommended page-hosted front end is the Lava Application Content block. It registers HTMX and supplies Helix conveniences and styling. Its documented configuration includes a block name, an optional linked application, and the initial Lava template. Linking the application also makes its configuration rigging available to the template. [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

Within the Content block, prefer:

```html
hx-get="^/application-slug/endpoint-slug"
```

The caret identifies a Lava Application route. The documented complete route is:

```text
/api/v2/lava-app/1/{application-slug}/{endpoint-slug}
```

Use the complete route only when the integration genuinely operates outside the Content block boundary and its authentication and exposure have been reviewed. A working request made through an authenticated staff page is not proof that the complete route is a safe public API. [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block) [Helix security](https://community.rockrms.com/developer/helix/overview/security)

### Editing with Magnus

The Magnus plugin supports editing Lava Applications and their endpoints in Visual Studio Code. Because a Content block can link to an application, Magnus can keep the front-end template and back-end endpoint files together during development. Verify that Magnus is installed and configured for the target packaging model before relying on this workflow. [Magnus](https://community.rockrms.com/developer/helix/lava-applications/magnus)

## Lava Endpoints

Endpoints are the application work units called by the client. Before changing an interaction, inspect the endpoint’s name, description, slug, method, security mode, code template, enabled Lava commands, and caching settings. The endpoint documentation says its cache configuration controls how CDNs and browsers may cache the response. Do not assume a response is uncached merely because its content appears dynamic. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

### Routing and HTTP methods

An endpoint match depends on its application slug, endpoint slug, and HTTP method. Two endpoints can therefore share the same slug route when they listen for different methods. The documented methods are GET, POST, PUT, and DELETE. Immutable Rock enums at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` contain those four method values. [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications) [HTTP-method enum](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Cms/LavaEndpointHttpMethod.cs)

Use the methods according to the endpoint’s intended effect:

- Use GET to retrieve content without changing data.
- Use POST for general creation or mutation.
- Use PUT when replacing or updating an existing resource fits the contract.
- Use DELETE for removal.
- Never use GET for a mutation.

The last rule is security-critical because GET requests can be initiated from cross-site links. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) [Helix security](https://community.rockrms.com/developer/helix/overview/security)

### Security modes

The endpoint’s security mode selects the authorization scope used for execution. The documentation and immutable enum identify these modes:

- Endpoint Execute.
- Application View.
- Application Edit.
- Application Administrate.

The first uses authorization on the endpoint itself; the application modes delegate the execution decision to the corresponding application-level pattern. Inspect the selected mode and the relevant authorization entries rather than checking only page or block security. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) [Security-mode enum](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)

### Request merge fields

The endpoint documentation identifies these request-related merge fields:

- `RawUrl`
- `Method`
- `QueryString`
- `RemoteAddress`
- `RemoteName`
- `ServerName`
- `Form`
- `Headers`
- `Cookies`

For Rock 19 and later, the approved claim and developer documentation also identify `Body` and `RawBody`. `Body` converts JSON or XML into objects, while `RawBody` preserves the request body as a string. Neither provides a request body for GET. Rock’s release notes specifically list the addition in 19.1, so verify the exact minor release before depending on it. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) [Rock release notes](https://www.rockrms.com/releasenotes)

Every value from these merge fields remains untrusted input. Validate its presence, type, allowed values, length, and relationship to the current caller before reading or modifying data. Sanitize or parameterize any value used in SQL. [Helix security](https://community.rockrms.com/developer/helix/overview/security)

### Enabled commands and endpoint responses

An endpoint exposes only the Lava commands selected in its Enabled Lava Commands setting. Inspect that allowlist before diagnosing a command failure or authorizing an endpoint for a broader audience. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

The HTTP Response command, documented for Rock 18.0, can return HTMX response headers that redirect, retarget content, trigger an event, reload the page, or update browser history. It can also change the HTTP status from the default successful status. [HTTP Response](https://community.rockrms.com/lava/commands/http-response)

When one endpoint performs several dependent writes, the DB Transaction command can group them so a failure rolls the changes back rather than leaving only part of the operation committed. Its documentation begins at Rock 18.0 and identifies a context-isolation addition at 19.3; verify the installed command behavior before using version-specific options. [DB Transaction](https://community.rockrms.com/lava/commands/db-transaction)

For content needed during the initial page render, the Rock 18.0 `renderlavaendpoint` command can execute an endpoint and inject its output without an additional HTMX request. Its method defaults to GET unless specified. Do not use that default to invoke a mutating endpoint. [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint)

## Forms And Controls

### Lava Forms

HTML and HTMX normally treat forms as independent units, but ASP.NET WebForms uses one page-wide form. Helix introduces `<lava-form>` as a logical form boundary so form behavior and validation can work without adding invalid nested HTML forms. Use this model when diagnosing validation or submission behavior inside a Rock page. [Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)

### Control shortcodes

Helix supplies Lava shortcodes for common controls. For example, a textbox or campus picker can be expressed through a shortcode instead of manually reproducing Rock’s label, wrapper, validation, identifier, and input markup. Installed controls can be inspected under `Admin Tools > CMS Configuration > Lava Shortcodes` in the Helix category. The documentation warns against editing the supplied controls directly because later updates may overwrite those changes. [Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls)

For a new reusable control, the documented pattern starts from the `rock-control` base shortcode. Common parameters include `label`, `isrequired`, `type`, `validationmessage`, and a unique `id`; the control’s actual input markup is placed inside the base shortcode. Decide whether the control is broadly reusable or project-specific before treating it as a toolkit extension. [Creating New Controls](https://community.rockrms.com/developer/helix/forms-controls/creating-new-controls)

### Validation

Helix client-side validation applies only to controls within `<lava-form>` and is processed for POST, PUT, and DELETE—not GET. It can use native HTML validation attributes, and a custom field message can be supplied in an element whose identifier follows `rfv-{control id}`. A `<lava-validationsummary />` can place the summary at a chosen location inside the Lava Form. Supplied Helix control shortcodes generate much of this convention automatically. [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)

Client-side validation is only a usability layer. The endpoint must repeat all security and integrity validation because a caller can bypass the page and invoke the endpoint directly. [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation) [Helix security](https://community.rockrms.com/developer/helix/overview/security)

### Loading indicators

A submitting control can contain its own element with the `htmx-indicator` class. For a form-level indicator, place the indicator inside the Lava Form and set the submitting control’s `hx-indicator` to the form selector. [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)

Spinner paths depend on packaging:

- Rock 18 or later core examples use `/Assets/Images/Spinners/`.
- The Helix plugin uses `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/`.

Inspect the installed packaging and confirm the asset returns successfully rather than switching paths based only on the page’s age. [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)

## Security And Observability

### Endpoint security review

Treat every endpoint as directly callable outside its intended front end. For each endpoint:

1. Identify whether it reads, writes, deletes, starts a workflow, or exposes person-backed data.
2. Inspect its endpoint or application execution mode and authorization assignments.
3. Test the intended caller rather than relying on administrator access.
4. Validate and allowlist query, form, header, and body values.
5. Prefer IdKeys or GUIDs over easily guessed numeric identifiers where practical.
6. Independently verify the caller’s right to view or edit the selected entity.
7. Keep mutations off GET.
8. Sanitize or parameterize values before SQL use.
9. Keep Enabled Lava Commands no broader than the template requires.
10. Review caching so private or user-specific responses are not exposed through an inappropriate cache policy.

The first eight checks come directly from the official security and endpoint guidance. The command and caching checks follow from the endpoint’s documented configuration surface. [Helix security](https://community.rockrms.com/developer/helix/overview/security) [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

A reviewed read-only installation probe found secured Lava Application and Lava Endpoint entity types and authorization rows for both. It also found endpoint metadata for method, security, enabled commands, caching, rate limiting, activity, and additional settings. This is evidence that agents should inspect those surfaces; it is not evidence that another installation exposes identical controls or that any existing endpoint is secure.

### Observability

Each Lava Endpoint call creates an observability activity named with both the endpoint and application names. The root activity records `rock.lava_endpoint` and `rock.lava_application`, and the HTTP method is available through an existing activity attribute. Use those fields to isolate a route and compare methods when investigating errors or latency. [Endpoint observability](https://community.rockrms.com/developer/helix/lava-applications/observability)

Monitor endpoint traces during development to identify slow execution and excessive database calls. Rock’s broader observability system can expose page, block, database-transaction, and job timing. [Endpoint observability](https://community.rockrms.com/developer/helix/lava-applications/observability) [Intro to Observability](https://community.rockrms.com/documentation/supporting-rock/data/observability/intro-to-observability)

Rock 19.0 documentation places observability configuration under `Admin Tools > Settings > System Configuration`. It includes feature selection for traces, metrics, and logs; provider endpoint and protocol; headers; trace level; span and attribute limits; optional SQL statement collection; and targeted-query diagnostics. It also instructs administrators to confirm that the Observability HTTP module is active. Targeted query data can include parameter values and stack traces, so enable it only for a bounded investigation and review the possibility of personally identifiable information before collection. [Configure Observability](https://community.rockrms.com/documentation/supporting-rock/data/observability/configure-observability)

## Strategies And Limitations

The `{% javascript %}` and `{% stylesheet %}` Lava commands do not work in Helix endpoint templates. Endpoint output is injected dynamically, and RockPage is not available to coordinate or reliably deduplicate those resources. Load required assets through a page, theme, block, or another verified host boundary instead of expecting an endpoint fragment to register them. [Helix limitations](https://community.rockrms.com/developer/helix/strategies/limitations) [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

The official Related Entities strategy page contains only a “writing in progress” notice in the supplied evidence. No operational behavior can be established from that title, so this guide intentionally makes no claim about a related-entity feature. [Related Entities](https://community.rockrms.com/developer/helix/strategies/related-entities)

### Reviewed community patterns

The following are reviewed community patterns, not guarantees of Rock core behavior. Each requires adaptation and live verification:

- **Public page boundary:** Prefer a page-hosted Content block, purpose-built endpoint, or bounded read-only adapter over treating a complete Rock page inside an iframe as the long-term integration contract. Keep authentication, person-backed forms, verification, workflow activation, and mutations behind explicit review and testing. [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block) [Endpoint security](https://community.rockrms.com/developer/helix/overview/security)
- **Active search:** Render a useful first view on the server, then use caret routes inside the Content block for subsequent filters. Test anonymous and intended-role access separately; a successful staff-session request does not establish public safety. [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)
- **Server-owned result state:** A reviewed pattern places sort and direction values in the returned result fragment so filtering, sorting, and refresh requests share one server contract. Nullable columns receive an explicit blank bucket in the server-side ordering. This is a community design pattern, not built-in Helix behavior.
- **Read-only dashboards:** Keep read endpoints separate from mutation endpoints. Domain-specific joins and status rules require evidence from the owning models, and rows without the owning domain record should not receive actions that depend on that record.
- **Communication search:** An immutable public recipe separates the filter shell from the results endpoint, allowlists enum and page-size inputs, parameterizes text search, pages before recipient aggregation, and keeps message bodies and recipient details out of the initial view. [Communication History Active Search](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/communication-history-active-search)
- **Public AI retrieval:** A reviewed pattern separates a broad approved-route registry from a smaller search corpus, keeping authenticated, payment, registration, private-media, and staff-only material out of public semantic retrieval. This is an application architecture recommendation, not a Helix core feature.
- **Rendered validation:** Exact source readback and successful rendering are separate gates. A reviewed dashboard pattern tests an unauthorized visitor, the intended role, and an administrator; checks known data invariants and representative rows; exercises filters and empty states; inspects Lava and console errors; and measures responsive overflow. [Public dashboard recipe source](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)
- **Community recipes:** The public Following-management recipe demonstrates a page composed from a Lava Application, Content block, endpoint, filter block, and supplemental page assets. Rock explicitly warns that community recipes are not reviewed or endorsed by the core team, so inspect their security, identifiers, commands, and version assumptions before adoption. [Manage Following records with Helix](https://community.rockrms.com/recipes/497)

## Version And Authority Caveats

- Rock’s core release notes say Lava Application support was added to core in Rock 18.1. [Rock release notes](https://www.rockrms.com/releasenotes)
- The Helix landing page still describes Helix as early alpha, while the plugin-installation page describes a limited beta requiring both the Helix and Magnus plugins. The FAQ says Helix is now in core. These pages reflect different lifecycle or packaging moments; do not combine them into one installation rule. [Helix landing page](https://community.rockrms.com/developer/helix) [Plugin installation](https://community.rockrms.com/developer/helix/overview/plugin-installation) [Helix FAQ](https://community.rockrms.com/developer/helix/overview/faq)
- Spinner assets and several Lava commands are documented from Rock 18.0, while the release note places core Lava Application support in 18.1. Verify the actual feature and asset availability in the installed build.
- Developer documentation labels `Body` and `RawBody` as Rock 19+, while release notes specifically list their addition in 19.1. Use the exact minor version as the deployment gate. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) [Rock release notes](https://www.rockrms.com/releasenotes)
- Rock 19.5 release notes describe a fix for non-administrators being unable to run an endpoint when the Lava Application Developer role was inactive. Include exact patch level and role state when diagnosing similar authorization failures. [Rock release notes](https://www.rockrms.com/releasenotes)
- The supplied Content block claim carries a `2.0` version tag whose meaning is not established by the excerpt. Do not interpret it as a Rock core version without separate evidence.
- The supplied GitHub source observations use immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They describe that implementation snapshot, not the target installation.
- Roadmap items are ideas, not released behavior.
- Community contributions and recipes are examples. They require security, schema, performance, and rendered-page review before use.

## Troubleshooting Decision Tree

### An HTMX action does nothing or updates the wrong region

1. Confirm the page uses a Lava Application Content block or otherwise loads HTMX.
2. Inspect the browser console for HTMX errors.
3. Confirm the element’s `hx-get`, `hx-post`, `hx-put`, or `hx-delete` value.
4. Confirm `hx-target` matches an existing element at request time.
5. Walk up the DOM and inspect inherited HTMX attributes.
6. Inspect the network response and returned fragment.
7. Stop when the request reaches the intended endpoint and consistently replaces the intended element. [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block) [Helix tips](https://community.rockrms.com/developer/helix/strategies/tips)

### The endpoint returns not found or the wrong handler runs

1. Record the application slug, endpoint slug, and request method.
2. Confirm both records are active in the target installation.
3. Confirm the endpoint is attached to the expected application.
4. Compare the request method with the endpoint method.
5. Check for another endpoint using the same slug with a different method.
6. From a Content block, test the caret route; outside it, inspect the documented complete route.
7. Stop when the route and method identify one intended endpoint. [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications) [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

### A user is denied while an administrator succeeds

1. Identify the exact user or role being tested; do not use administrator override as evidence.
2. Inspect the endpoint security mode.
3. If it uses Endpoint Execute, inspect authorization on that endpoint.
4. If it uses an application mode, inspect the corresponding application execution authorization.
5. Inspect the application’s management security separately from execution security.
6. Record Rock’s exact patch version and whether the Lava Application Developer role is active, because Rock 19.5 fixed a related non-administrator failure.
7. Stop when the intended role succeeds and an unauthorized role is still denied. [Application security](https://community.rockrms.com/developer/helix/lava-applications/applications) [Endpoint security modes](https://community.rockrms.com/developer/helix/lava-applications/endpoints) [Rock release notes](https://www.rockrms.com/releasenotes)

### Form validation is skipped or nested-form behavior is inconsistent

1. Confirm the inputs are inside `<lava-form>`.
2. Confirm the request uses POST, PUT, or DELETE; Helix validation is not processed on GET.
3. Check native HTML validation attributes.
4. For custom controls, confirm the validation message element follows `rfv-{control id}`.
5. Confirm any validation summary is inside the Lava Form.
6. Invoke the endpoint directly with invalid input and confirm server-side rejection.
7. Stop only when both the browser and direct endpoint request enforce the required rules. [Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation)

### Body or RawBody is empty or unavailable

1. Confirm the request is not GET.
2. Record the installed Rock minor version.
3. Treat developer documentation’s Rock 19+ label and the 19.1 release note as a reason to verify exact availability.
4. Confirm the client actually sent a body and inspect its content type.
5. Use `Body` when object conversion is expected and `RawBody` when the original string is required.
6. Stop when the endpoint receives the expected representation without depending on an unsupported version. [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) [Rock release notes](https://www.rockrms.com/releasenotes)

### A loading spinner is missing

1. Confirm the indicator has the `htmx-indicator` class.
2. For a form-wide indicator, confirm `hx-indicator` targets the Lava Form.
3. Determine whether the installation uses core Rock 18+ assets or the Helix plugin.
4. Test the appropriate asset path directly.
5. Confirm the request lasts long enough for the indicator state to be visible.
6. Stop when the indicator appears for the intended request and disappears after completion. [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator)

### Endpoint-injected styles or scripts do not load

1. Inspect the endpoint for `{% javascript %}` or `{% stylesheet %}`.
2. Remove the assumption that those commands can register assets from a Helix fragment.
3. Move the dependency to a verified page, theme, or block-level loading boundary.
4. Retest both the initial render and later fragment replacements.
5. Stop when the dependency is loaded once through a supported host and the fragment works without endpoint-side resource registration. [Helix limitations](https://community.rockrms.com/developer/helix/strategies/limitations)

### An endpoint is slow or makes excessive database calls

1. Locate its observability activity using the endpoint and application names.
2. Confirm the recorded HTTP method.
3. Compare total execution time and database activity across representative requests.
4. Inspect repeated or unexpectedly expensive database calls.
5. Use targeted query diagnostics only for a bounded investigation and review whether parameters contain personal data.
6. Retest after each change.
7. Stop when representative traces meet the application’s defined performance target without unsafe diagnostic collection. [Endpoint observability](https://community.rockrms.com/developer/helix/lava-applications/observability) [Configure Observability](https://community.rockrms.com/documentation/supporting-rock/data/observability/configure-observability)

### Sorting or filtering resets after refresh

1. Confirm whether state exists only in browser-side variables.
2. As a reviewed community pattern, have the server-rendered result fragment emit current sort and direction values.
3. Include those values in filter and refresh requests.
4. Have sortable headers send the next sort and direction explicitly.
5. Define ordering for null or blank values.
6. Retest filtering, sorting, manual refresh, and auto-refresh together.
7. Stop when all requests use one documented server-side state contract. [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

## Agent Task Recipes

### Recipe: Inspect an existing Helix application before changing it

**Outcome:** A bounded map of the current application flow and its security-sensitive surfaces.

1. Record the installed Rock version and whether Helix is core- or plugin-provided.
2. Inspect the Lava Application’s name, description, slug, configuration rigging, activity state, and security.
3. Identify every linked Lava Application Content block.
4. Inventory the application’s endpoints by name, slug, method, and activity state.
5. For each endpoint, record security mode, enabled commands, caching, code-template purpose, and any exposed rate-limit or CSRF setting.
6. Trace each page action to its endpoint and target element.
7. Identify which endpoints read, mutate, delete, or launch other work.
8. Review representative observability activities before altering behavior.

**Inspect:**

- Application and endpoint authorization.
- Method and route collisions.
- Input sources.
- Entity-level permission checks.
- Cache policy.
- Database activity.

**Do not assume:**

- Page security protects the endpoint.
- Administrator success proves role access.
- A staff-session route is suitable for public use.
- Settings observed in another installation exist here.

**Stop when:**

- Every page action maps to one endpoint and method.
- Every mutation has an explicit security and validation boundary.
- Unknown installed-state questions are recorded for live verification.

Sources: [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications), [Lava Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints), and [Endpoint observability](https://community.rockrms.com/developer/helix/lava-applications/observability).

### Recipe: Build a read-only HTMX result fragment

**Outcome:** A page-hosted query interaction that returns only authorized display content.

1. Create or select a Lava Application with a documented name, description, and slug.
2. Add a GET endpoint for the result fragment.
3. Configure its security mode for the intended audience.
4. Enable only the Lava commands required to read and render the result.
5. Validate and allowlist all query values.
6. Check the caller’s right to view each protected entity.
7. Add a Lava Application Content block and link it to the application.
8. Render useful initial content.
9. Add the HTMX request using a caret route and an explicit target.
10. Test empty, invalid, unauthorized, and representative result states.
11. Inspect endpoint traces and database calls.

**Do not assume:**

- IdKeys or GUIDs provide authorization.
- Read-only behavior makes private fields safe to expose.
- A default cache policy is appropriate for person-specific output.

**Stop when:**

- Anonymous and authenticated behavior matches the intended audience.
- The endpoint performs no mutation.
- Returned fields and cache behavior have been reviewed.
- Observability shows acceptable database work.

Sources: [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block), [Helix security](https://community.rockrms.com/developer/helix/overview/security), and [Endpoint observability](https://community.rockrms.com/developer/helix/lava-applications/observability).

### Recipe: Build a validated mutation form

**Outcome:** A non-GET endpoint that rejects unauthorized or invalid direct calls as well as invalid browser submissions.

1. Place the controls inside `<lava-form>`.
2. Prefer supplied Helix control shortcodes where they meet the requirement.
3. Add native validation rules and clear validation messages.
4. Use POST, PUT, or DELETE according to the operation.
5. Configure endpoint or application execution security.
6. Enable only the commands needed for the mutation.
7. Repeat every validation rule in the endpoint.
8. Resolve the target entity from validated input.
9. Verify the caller’s edit rights to that entity.
10. Parameterize or sanitize any SQL inputs.
11. If multiple writes must succeed together, assess the DB Transaction command.
12. Return an appropriate status or HTMX response instruction.
13. Test the endpoint directly with missing, malformed, unauthorized, and tampered input.

**Inspect:**

- Security mode and authorization entries.
- Enabled Lava Commands.
- Request body availability for the installed version.
- Transaction behavior.
- Response status and rendered error state.

**Stop when:**

- Direct calls cannot bypass validation or authorization.
- GET cannot trigger the mutation.
- Partial failure cannot leave unacceptable data state.
- Success and error responses are visible and traceable.

Sources: [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation), [Helix security](https://community.rockrms.com/developer/helix/overview/security), [DB Transaction](https://community.rockrms.com/lava/commands/db-transaction), and [HTTP Response](https://community.rockrms.com/lava/commands/http-response).

### Recipe: Render endpoint content on first paint

**Outcome:** Endpoint-generated content appears during the initial page render without a second request or avoidable layout shift.

1. Confirm the installed version supports `renderlavaendpoint`.
2. Select a read-safe endpoint for the initial render.
3. Invoke it with the caret route.
4. Specify the method when it is not GET.
5. Do not rely on the default GET method for any mutation.
6. Compare the initial output with the later HTMX-rendered fragment.
7. Confirm authorization behaves consistently in both contexts.
8. Measure whether the extra-request and layout-shift problem is resolved.

**Stop when:**

- The initial content is present in the first render.
- The endpoint remains authorized and non-mutating for its chosen method.
- Later HTMX updates preserve the same output contract.

Source: [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint).

### Recipe: Validate a rendered Helix dashboard

**Outcome:** Evidence that source targeting, authorization, data semantics, interaction behavior, and responsive layout all work in the actual page context.

1. Confirm the saved application, endpoint, and Content block source matches the intended source.
2. Open the rendered page as an unauthorized visitor.
3. Test as the intended role.
4. Test as an administrator, but record that result separately.
5. Assert known totals or invariants and representative rows.
6. Exercise each filter, sort, refresh, and empty state.
7. Inspect visible errors, hidden Lava error surfaces, network failures, and console errors.
8. Test narrow and wide layouts for clipped labels, unintended internal scrolling, and unbounded horizontal overflow.
9. Inspect endpoint traces for representative requests.

**Do not assume:**

- Source equality proves rendered behavior.
- Administrator access proves intended-role access.
- A successful HTTP response proves correct data semantics.
- Desktop rendering proves responsive readiness.

**Stop when:**

- All audience states, invariants, interactions, and layout checks pass independently.

This recipe is based on a reviewed community task pattern and requires installation-specific verification. [Public dashboard recipe source](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

### Recipe: Decide whether to replace a Lava Application

**Outcome:** A documented decision to retain Helix or move to a purpose-built solution.

1. Count the application’s endpoints.
2. Identify whether the requested design requires custom models.
3. Assess whether ordinary changes are becoming complex or fragile.
4. Review security, deployment, testing, and maintenance costs.
5. If custom models, approximately 50 or more endpoints, or persistent fragility are present, compare a purpose-built implementation.
6. Keep the application in Helix only when its operational boundaries remain understandable and supportable.

**Stop when:**

- The selected approach has a clear ownership, security, testing, and maintenance model.

Source: [Customizing Rock](https://community.rockrms.com/developer/helix/overview/customizing-rock).

## Known Gaps And Live Verification

No target installation was examined for this guide. Before changing or approving a Helix application, perform a bounded read-only review of:

- The exact Rock version and patch.
- Whether Helix is supplied by core, the historical plugin, or another package.
- Magnus installation and configuration when that workflow is required.
- Application and endpoint schema present in the installation.
- Active applications, endpoints, and Content blocks.
- Actual slug-and-method route matches.
- Application and endpoint authorization records.
- Intended-role and anonymous execution results.
- Enabled Lava Commands.
- Cache, rate-limit, CSRF, and additional endpoint settings exposed by that version.
- `Body` and `RawBody` behavior on the installed minor version.
- Spinner asset availability.
- Observability configuration, provider delivery, and endpoint activities.
- Database-call volume for representative requests.
- Direct-call rejection for invalid and unauthorized mutations.
- Rendered-page behavior, including responsive layout and console errors.

Additional evidence gaps remain:

- The Related Entities documentation supplied no usable behavior beyond a work-in-progress notice.
- The roadmap does not establish release dates or committed features.
- The Content block claim’s `2.0` version label is ambiguous.
- Historical alpha, beta-plugin, and core-release documentation has not been reconciled into a single current packaging matrix.
- Mobile availability is mentioned only in a historically worded FAQ and is not established as current behavior.
- Reviewed community patterns have not been proven against an arbitrary installation.
- The connected-instance verification in the evidence pack confirmed relevant tables and authorization surfaces, but not the correctness of any specific application or endpoint.

## Source Map

### Official Helix documentation

- [Helix](https://community.rockrms.com/developer/helix) — lifecycle language and high-level feature positioning.
- [Overview](https://community.rockrms.com/developer/helix/overview) — HTMX, Lava Applications, Lava Commands, and control shortcodes.
- [Customizing Rock](https://community.rockrms.com/developer/helix/overview/customizing-rock) — customization boundaries and exit signals.
- [Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation) — historical plugin and Magnus requirements.
- [FAQ](https://community.rockrms.com/developer/helix/overview/faq) — core-status and historical mobile statements.
- [Roadmap](https://community.rockrms.com/developer/helix/overview/roadmap) — noncommitted future ideas.
- [Security](https://community.rockrms.com/developer/helix/overview/security) — direct-call, validation, authorization, method, and SQL guidance.
- [HTMX](https://community.rockrms.com/developer/helix/htmx) — HTMX topic index.
- [HTMX Syntax Style Guides](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides) — markup formatting.
- [HTMX Learning More](https://community.rockrms.com/developer/helix/htmx/learning-more) — external learning and example caveats.
- [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications) — application and endpoint model.
- [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications) — configuration rigging and application security.
- [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block) — HTMX registration and caret routes.
- [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) — endpoint settings, methods, merge fields, caching, and limitations.
- [Magnus](https://community.rockrms.com/developer/helix/lava-applications/magnus) — VS Code editing workflow.
- [Endpoint Observability](https://community.rockrms.com/developer/helix/lava-applications/observability) — endpoint activity naming and attributes.
- [Forms & Controls](https://community.rockrms.com/developer/helix/forms-controls) — forms topic index.
- [Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) — WebForms and Lava Form boundary.
- [Using Form Controls](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls) — supplied shortcodes.
- [Creating New Controls](https://community.rockrms.com/developer/helix/forms-controls/creating-new-controls) — `rock-control` extension pattern.
- [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation) — client-side validation conventions.
- [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) — HTMX indicators and versioned asset paths.
- [Strategies](https://community.rockrms.com/developer/helix/strategies) — strategy topic index.
- [Tips](https://community.rockrms.com/developer/helix/strategies/tips) — console diagnostics and inherited attributes.
- [Limitations](https://community.rockrms.com/developer/helix/strategies/limitations) — RockPage-dependent command limitation.
- [Related Entities](https://community.rockrms.com/developer/helix/strategies/related-entities) — documented evidence gap.

### Supporting official documentation

- [Lava Commands](https://community.rockrms.com/developer/helix/lava-commands)
- [HTTP Response](https://community.rockrms.com/lava/commands/http-response)
- [DB Transaction](https://community.rockrms.com/lava/commands/db-transaction)
- [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint)
- [Rock Observability](https://community.rockrms.com/documentation/supporting-rock/data/observability)
- [Intro to Observability](https://community.rockrms.com/documentation/supporting-rock/data/observability/intro-to-observability)
- [Configure Observability](https://community.rockrms.com/documentation/supporting-rock/data/observability/configure-observability)
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- [Lava Application Model Map](https://community.rockrms.com/ModelMap)

### Immutable implementation evidence

- [Lava endpoint security modes](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)
- [Lava endpoint HTTP methods](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Cms/LavaEndpointHttpMethod.cs)
- [Lava Application save hook](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)
- [Lava Applications implementation notes](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/docs/cms/lava-applications.md)
- [Rock 18 Lava Application migration](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2018.0/Version%2018.0/202505072235453_AddLavaApplications.cs)

### Community examples

- [Manage Following records with Helix](https://community.rockrms.com/recipes/497) — unendorsed community recipe requiring independent review.
- [Communication History Active Search](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/communication-history-active-search) — immutable read-only search pattern.
- [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard) — immutable source for the reviewed rendered-validation pattern.