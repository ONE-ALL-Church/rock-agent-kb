---
id: authored-api-integrations
title: API And Integrations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# API And Integrations

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [API And Integrations index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock RMS integration work is not a single feature area. It is a set of overlapping surfaces that expose Rock data and behavior to external systems, browser clients, mobile shells, TV applications, Lava endpoints, workflows, and now agent tools. An agent working on API or integration tasks must identify which surface is involved before diagnosing behavior or recommending implementation.

The core public API surfaces are:

- **REST API v1**, the long-standing Web API surface available under `/api/...`, documented through Swagger in a Rock instance and described in the Rock REST developer guide. Rock's community API portal now labels API v1 as legacy while still useful and reliable for many existing integrations. See the API portal and REST guide: [API Documentation](https://community.rockrms.com/api-docs), [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).
- **REST API v2**, introduced as a newer API pattern starting in Rock v17, designed around explicit execution security and code-generated CRUDS endpoints. It uses routes such as `/api/v2/models/...` and action-specific routes such as `/api/v2/models/workflows/actions/launch/{workflowTypeId}`. See [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns) and the demo v2 docs at [Rock Rest API v2](https://rock.rocksolidchurchdemo.com/api/v2/docs/index).
- **Lava Webhooks**, configured with Defined Types and Defined Values, which let Rock render a Lava template in response to an HTTP request. They are powerful and easy to create, but the official Lava API documentation warns that they do not provide security by default. See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).
- **Lava REST Endpoint**, a remote-Lava endpoint that accepts Lava and returns rendered output. It should be treated as highly sensitive because anyone with the endpoint and API key can cause Lava to run as the linked API user. It is HTTPS-only according to the remote Lava documentation. See [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava).
- **Helix Lava Applications and Lava Endpoints**, a newer application framework that uses HTMX and server-rendered Lava endpoints under `/api/v2/lava-app/1/{application-slug}/{endpoint-slug}`. These endpoints include explicit endpoint/application security modes, HTTP methods, enabled Lava commands, cache settings, rate limit fields in current view models, and observability metadata. See [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications), [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications), [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints), and [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability).
- **Workflow Webhooks and Workflow Launch APIs**, which allow external or API-triggered events to activate Rock workflows. These are operationally useful for low-code integrations, but must be secured and tested because workflows often hold sensitive data and can execute SQL/Lava/actions. See the community example [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453) and source-code route details in [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs).
- **Lava Web Request command**, which lets Lava call outside HTTP APIs. It supports methods, headers, parameters, body content, basic authentication, expected response content type, and a named return variable. See [Web Request](https://community.rockrms.com/lava/commands/web-request-commands).
- **Specialized integrations**, including Mailgun webhooks, SMS transport pipeline webhooks, Roku/Apple TV/mobile application API keys, Azure Document Intelligence keys for check scanning, push notification service-account configuration, Auth0/OIDC login mapping, and Spark Data API usage in some mobile controls. These are integration surfaces, but each has its own configuration and security model.

The most important operational rule is: **do not treat "API access" as a single permission**. Rock has several layers of security:

- An API key or authenticated cookie identifies the caller.
- REST controller/action authorization determines whether a caller may execute an endpoint.
- Entity security may still apply to the specific record being accessed.
- API v2 distinguishes ordinary execute permission from unrestricted execute permission.
- Lava/webhook surfaces can bypass or concentrate access in ways that require stricter template, role, and data controls.
- CORS only affects browser cross-origin calls. It does not secure the API against server-side callers.
- IdKey, Guid, PersonActionIdentifier, and security grants reduce exposure of raw IDs, but they do not replace authorization checks.

For agents, the right first move is usually to classify the integration:

1. Is the caller a browser, server, Rock page, mobile shell, TV shell, workflow, Lava template, or agent tool?
2. Is the target a REST v1 route, REST v2 model/action route, Lava webhook, Lava Application endpoint, remote Lava endpoint, workflow webhook, or external API?
3. Which identity is executing: logged-in person, API user/person, application API key, workflow context, Lava author context, or anonymous/public user?
4. Which permissions are checked: REST action execute, unrestricted execute, entity view/edit, workflow type view, Lava Application execute, endpoint execute, block security, file/document security, or custom action verb?
5. Which data model is involved, and can the Model Map or source code confirm property names, table names, obsolete status, and endpoint behavior?

If a fact is instance-specific, inspect the live Rock instance instead of assuming. Check `Home > Security > REST Keys`, `Home > Security > REST Controllers`, `Home > Security > REST CORS Domains`, `Admin Tools > General Settings > Defined Types`, Lava Application and Lava Endpoint detail blocks, the Model Map, relevant block settings, workflow type security, integration transport attributes, and exception logs.

## 2. Scope And Terminology

This guide covers API and integration concepts across Rock RMS, with emphasis on agent-usable diagnosis and implementation. It includes REST APIs, API authentication, CORS, OData, Swagger/API docs, Lava Webhooks, remote Lava, Helix Lava Applications, workflow launch paths, webhooks, external API calls from Lava, Model Map usage, source-code landmarks, and version caveats.

It does not replace the full Rock administration manuals, API reference, security guide, workflow guide, Lava command reference, or source code. It is a synthesis layer for agents that need to reason across those sources.

### API

In Rock, "API" can mean several things. The most common meaning is the REST API available through HTTP routes. It can also refer to API-style Lava webhooks, Helix Lava endpoints, mobile/TV application endpoints, and external third-party APIs called from Rock.

When a user says "API," an agent must clarify by context rather than assuming. For example:

- "Swagger fails" usually means the REST API documentation/test surface.
- "External Squarespace calendar can't call Rock" may involve REST authentication, CORS, or a public iCal feed.
- "Webhook to workflow" means a Defined Type/Defined Value route that launches a workflow, not a REST controller.
- "Lava endpoint" may mean an older Lava Webhook or a newer Helix Lava Endpoint.
- "API key" may mean a Rock REST key, a Roku/Apple TV application key, a Mailgun API key, an Azure Document Intelligence key, a Firebase service account, or a third-party key stored for Lava Web Request usage.

### REST API v1

REST API v1 is Rock's classic REST surface. Rock's API portal labels it legacy but still available for reference and testing. The API v1 demo docs are exposed through Swagger at [Rock REST API Documentation](https://rock.rocksolidchurchdemo.com/api/docs/index), and the broader developer guide explains authentication, CORS, OData, and API controller discovery at [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

The v1 API is commonly used by older integrations, external scripts, check scanners, financial statement tooling, and internal Rock UI components.

### REST API v2

REST API v2 is the newer pattern introduced starting in Rock v17. The developer coding standards state that v2 endpoints are secure by default and require explicit authorization to execute. They introduce execution security actions such as `EXECUTE_READ`, `EXECUTE_WRITE`, `EXECUTE_UNRESTRICTED_READ`, and `EXECUTE_UNRESTRICTED_WRITE` rather than relying on only View/Edit semantics for endpoint execution. See [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns).

The v2 pattern includes generated CRUDS controllers for models decorated for REST code generation and custom action controllers for operations such as workflow launch. Source examples include [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs) and [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs).

### OData

OData is a query syntax used by the REST API to filter, sort, paginate, and shape returned data. The REST guide identifies OData as the method for retrieving data with query options and notes pagination and return shaping as key concerns. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api). When using OData against a live instance, inspect the instance's Swagger/API docs and test the exact route because entity models, security, and version behavior vary.

### Swagger / API Docs

Swagger is the interactive documentation/testing UI for REST API routes. Rock's API portal links to demo API v1 and v2 Swagger-style documentation surfaces using `admin` / `admin` for the demo site. See [API Documentation](https://community.rockrms.com/api-docs).

If Swagger shows browser errors such as "Failed to fetch" with CORS/network/scheme hints, distinguish between API server behavior, browser-origin restrictions, URL scheme, proxy/TLS issues, and Swagger page configuration. Community Q&A records describe this failure shape, but they are not authoritative resolution docs; treat them as symptoms to investigate in the live instance. See [Problem with API Calls](https://community.rockrms.com/ask/developing/2842).

### REST Key / Authorization Token

The REST guide describes authorization tokens as a way for an application to access the REST API without a specific user login. In the Rock UI, REST keys are created at `Home > Security > REST Keys`. After creation, permissions must be granted to define what the key can do. The same guide warns that anyone with the token can perform allowed API operations until it is revoked, and the token does not expire automatically. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

Use "REST key" for the Rock UI object and "authorization token" for the HTTP credential. In practice, agents should inspect the REST key's associated person/API user and its authorization rows before using or expanding it.

### CORS

CORS is a browser mechanism that lets a web page on one origin call resources on another origin if the server allows it. Rock lets administrators configure allowed cross-domain access at `Home > Security > REST CORS Domains`, according to the REST guide. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

CORS is not authentication. It does not protect server-to-server calls. It only governs whether browsers allow a page to read cross-origin responses.

### Lava Webhook

A Lava Webhook is a Defined Value under the `Lava Webhook` Defined Type. Rock matches incoming requests to the configured value based on HTTP verb and URL path. The matched Lava template can render JSON, XML, HTML, text/calendar, or other content depending on response settings. The official Lava API documentation explicitly warns that these webhooks do not have security by default, so any exposed data and enabled commands must be reviewed carefully. See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).

### Lava Application / Lava Endpoint

A Lava Application is a Helix framework object that groups endpoint logic and shared application configuration. A Lava Endpoint is an executable unit inside a Lava Application. The endpoint has fields such as name, description, slug, HTTP method, security mode, code template, enabled Lava commands, and caching settings. Current view models also expose rate limit fields and active state. See [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications), [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications), [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints), and [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts).

### Webhook To Workflow

A workflow webhook maps an HTTP request into a Workflow Type. The community Monday.com recipe shows the practical pattern: create workflow attributes such as `RawBody`, use a special `WebhookResponse` attribute key to send a response, configure a Defined Value under a workflow webhook defined type, use Lava in a request-processing field to accept or reject requests, and map webhook values into workflow attributes. See [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453).

Because that recipe is community-contributed and not core-reviewed, verify field names, paths, and response behavior in the live Rock instance and source code for the installed version.

### Model Map

The Model Map is a Rock example/admin tool that describes Rock model classes, categories, properties, methods, XML comments, database table names, and obsolete status. It is useful for agents because it reduces guessing about model properties and table relationships. Source-code snippets show the Model Map block builds categories from registered entity types and types decorated with `IncludeForModelMapAttribute`, and creates model/property/method bags from reflection and XML comments. See [Model Map](https://community.rockrms.com/ModelMap), [ModelMap.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Example/ModelMap.cs), and [IncludeForModelMapAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Data/IncludeForModelMapAttribute.cs).

## 3. API And Integrations Mental Model

A Rock integration is best understood as five questions:

1. **Who is calling?**
2. **What endpoint surface is being called?**
3. **What identity and permissions are used?**
4. **What data or behavior is being exposed?**
5. **What operational controls exist around it?**

### Caller Types

A browser caller is constrained by CORS, cookies, SameSite behavior, JavaScript visibility, and user session state. If a public website on a separate domain calls Rock directly from JavaScript, the request may need CORS configuration, but it also exposes any API token included in client-side code. The remote Lava documentation specifically warns against exposing endpoint/API key pairs in visible JavaScript because the key can be reused to run arbitrary Lava as the linked API user. See [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava).

A server caller, such as a middleware service, SquareSpace backend function, Zapier-like connector, or custom application, avoids browser CORS but must still authenticate and pass security checks. Server-side callers are generally better for sensitive API tokens.

A Rock page caller may use the current logged-in user's cookie or internal endpoint patterns. Some Rock UI components call API endpoints to populate item pickers, person badges, metric charts, and other dynamic content. The REST guide notes that Rock itself uses the REST API internally. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

A Lava caller can call external APIs using the Web Request command or can produce API responses through Lava Webhooks and Lava Applications. Lava has high power, especially when entity, SQL, modify, delete, or HTTP response commands are enabled. The Rock architecture docs warn that Lava authors often have access to data beyond the current person, so the Lava author must intentionally enforce access. See [Rock Architecture](https://community.rockrms.com/developer/developer-codex/coding-standards/rock-architecture) and [Web Request](https://community.rockrms.com/lava/commands/web-request-commands).

A mobile or TV shell caller may use application-specific API keys and remote authentication flows. Roku application settings include an API Key and an Authentication Page. Apple TV docs describe application creation and remote sign-in pages. See [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Apple TV Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), and [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page).

An agent tool caller can be a Rock AI Agent skill/tool implemented in Lava or C#. It should use IdKeys, security checks, narrowly shaped return objects, and explicit tool security. See [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools), [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools), [Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/get-tools), and [List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools).

### Endpoint Surface Types

REST v1 exposes classic controllers and is discoverable through `Home > Security > REST Controllers` and the instance API docs. Use it when an existing integration depends on it or the installed Rock version lacks equivalent v2 endpoints.

REST v2 exposes model controllers and action controllers. Generated controllers follow patterns such as:

- `GET /api/v2/models/lavaendpoints/{id}`
- `POST /api/v2/models/lavaendpoints`
- `PUT /api/v2/models/lavaendpoints/{id}`
- `PATCH /api/v2/models/lavaendpoints/{id}`
- `DELETE /api/v2/models/lavaendpoints/{id}`

The source snippet for Lava Endpoint v2 CRUD shows authentication, secured execution actions, excluded irrelevant security actions, response annotations, action GUIDs, and `CrudEndpointHelper`. See [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs).

Lava Webhooks route through `/Webhooks/Lava.ashx/...` or `/webhooks/lava.ashx/...` depending on casing and route normalization. The official Lava API example shows a request such as `/Webhooks/Lava.ashx/myapp/home` matching a Defined Value value such as `myapp/home`, optionally filtered by verb and regular-expression-style path variables. See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).

Helix Lava Endpoints route through `/api/v2/lava-app/1/{application-slug}/{endpoint-slug}`. When called from a Lava Application Content block, a caret shorthand can be used, such as `^/{application-slug}/{endpoint-slug}`. See [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints).

Workflow webhook endpoints are different from REST workflow action endpoints. A webhook-to-workflow configuration accepts an external request and starts a configured workflow, while REST v2 workflow actions expose explicit API routes such as `/api/v2/models/workflows/actions/launch/{workflowTypeId}`. See [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453) and [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs).

### Identity And Permission Chain

For REST token access, Rock maps the token to an API user/person and then evaluates endpoint and entity permissions. A common external-site issue is that the caller can make an API call while logged in to Rock but fails externally because the browser session identity is gone and no REST key/API user has been configured. A community Q&A answer recommends creating a person/API user and assigning API access for external site calls, while also noting that public calendar data may be available through an iCal feed. Treat that as practical community guidance, then verify current docs and instance settings. See [API from external site](https://community.rockrms.com/ask/developing/2641).

For REST v2, the execute action controls whether the endpoint may be called. The v2 API pattern distinguishes:

- `EXECUTE_READ`: caller may execute read behavior and per-entity security should be checked.
- `EXECUTE_WRITE`: caller may execute write behavior and per-entity security should be checked.
- `EXECUTE_UNRESTRICTED_READ`: caller may execute read behavior without additional per-entity security checks inside that endpoint.
- `EXECUTE_UNRESTRICTED_WRITE`: caller may execute write behavior without additional per-entity security checks inside that endpoint.

The official v2 API patterns page says only actions that make sense should be shown for an endpoint, and irrelevant actions should be excluded to keep administrator choices obvious. See [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns).

For Lava Applications, application-level security includes standard View/Edit/Administrate plus application execute verbs. Endpoint security mode can check the endpoint Execute verb or defer to application View/Edit/Administrate-style execute settings. The source enum confirms endpoint security mode values for endpoint execute and application view/edit/administrate. See [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications), [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints), and [LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs).

For blocks, the page framework handles whether the block is visible, but block code must still check authorization before exposing edit/action behavior. Use `IsUserAuthorized(...)` on blocks and `IsAuthorized(...)` on securable entities. See [Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks).

For public identifiers, avoid raw integer IDs in query strings, hidden fields, agent tool results, and client-visible payloads. Prefer IdKey, Guid, or PersonActionIdentifier depending on the use case, and still re-check authorization. See [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Code Security](https://community.rockrms.com/developer/developer-codex/coding-standards/code-security), and [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools).

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. **Installed Rock instance state** for anything configurable or security-sensitive.
2. **Source code for the installed version** for exact routes, attributes, security checks, field names, migrations, and bug behavior.
3. **Official Rock developer docs, Lava docs, Admin docs, and API docs** for intended usage and concepts.
4. **Release notes and tech bulletins** for version-specific caveats.
5. **Model Map** for model names, properties, methods, table names, obsolete status, and entity categories.
6. **RockU/RX sessions** for conceptual learning and historical context.
7. **Community recipes/Q&A** for examples and symptom patterns, but only after official/source material and only with validation.

This guide cites community recipes and Q&A when they illustrate real operational patterns, but those records are not authoritative. The iCal webhook recipe, Monday.com workflow webhook recipe, Auth0 association recipe, and API troubleshooting Q&A should be treated as examples to inspect and adapt, not as guaranteed-safe implementation instructions. Community recipe pages themselves warn that recipes are not reviewed or endorsed by the Rock core team. See [Lava Webhook to Create an iCal (.ics) File](https://community.rockrms.com/recipes/540), [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453), and [Auth0 Integration to associate users](https://community.rockrms.com/recipes/232).

When a fact is likely to drift, inspect live Rock:

- REST keys and user/person mapping.
- REST controller/action authorization.
- CORS domain list.
- API docs generated for that instance.
- Lava Webhook Defined Type and Defined Values.
- Lava Application and Lava Endpoint records.
- Enabled Lava commands on an endpoint/webhook.
- Workflow Type status, security, attributes, activities, and logs.
- ExceptionLog and interaction/observability data.
- Installed version, plugin version, mobile shell version, and release branch.
- Model Map entry for the target model.
- Source-code class for the installed version.

## 5. Core Configuration And Data Model

### REST Keys

Path: `Home > Security > REST Keys`.

Purpose: create authorization tokens for API access without a browser login session.

Agent checks:

- Identify the REST key name and associated person/API user.
- Confirm the key is still needed.
- Confirm it has not been shared into client-side code, public repositories, screenshots, or workflow logs.
- Confirm its authorization rows are scoped to required controllers/actions only.
- Confirm whether unrestricted v2 execute actions are granted; if so, justify why per-entity security may be bypassed.
- Confirm whether the key has a rotation/revocation procedure. The REST guide states tokens do not expire automatically, so manual revocation matters. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

### REST Controllers And REST Actions

Path: `Home > Security > REST Controllers`.

Purpose: discover and secure available REST controllers and actions.

Model Map records identify `Rest Controller` and `Rest Action` as CMS-category Rock models. See [Model Map](https://community.rockrms.com/ModelMap). Source-code v2 controllers use `RestControllerGuid` and `RestActionGuid` attributes, which tie code routes to stable Rock records. See [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs) and [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs).

Agent checks:

- Locate the controller by route, model, or action name.
- Inspect the action's security verbs.
- Confirm inherited/global authorization behavior if action-specific rows are absent.
- For v2 generated endpoints, look for `Secured`, `ExcludeSecurityActions`, and helper behavior in source.
- For action endpoints, inspect explicit entity/workflow security checks in the controller code.

### REST CORS Domains

Path: `Home > Security > REST CORS Domains`.

Purpose: allow browser applications on other domains to call Rock REST API resources.

CORS should be configured only for trusted browser origins. Do not use `*` unless the installed Rock UI explicitly supports and recommends it for a safe case; otherwise inspect the exact origin list and application architecture.

Agent checks:

- Is the caller browser-based? If not, CORS is probably irrelevant.
- Is the request origin exactly the domain configured? Scheme, host, and port matter.
- Is the request URL `http` or `https`? Browser error messages may reject unsupported schemes.
- Does the API call still need a token/cookie? CORS does not authenticate.
- Are sensitive tokens embedded in JavaScript? If yes, redesign around server-side proxy or public-safe endpoint.

See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) and the symptom record [Problem with API Calls](https://community.rockrms.com/ask/developing/2842).

### Lava Webhook Defined Type

Path: `Admin Tools > General Settings > Defined Types > Lava Webhook`.

Purpose: map HTTP requests to Lava templates.

Core configuration fields and concepts from the Lava API documentation and community examples:

- Defined Value **Value**: route pattern after the Lava webhook handler, for example `myapp/home` or `createIcsFile`.
- Optional HTTP **Method/Verb**: GET, POST, PUT, DELETE, etc. If no verb is configured, verify live behavior; the docs indicate matching can include the verb and URL.
- **Description**: operational purpose and owner.
- **Template**: Lava rendered for the response.
- **Enabled Lava Commands**: the command allowlist available to the template.
- **Response Content Type**: output MIME type, such as JSON, XML, HTML, or `text/calendar`.
- Route variables: URL matching can expose variables to Lava, such as a path segment named `seriesId`.
- Merge fields: the docs identify variables such as relative URL and raw URL; inspect the Defined Type help text and installed docs for the full variable list.

See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api) and the practical `text/calendar` example in [Lava Webhook to Create an iCal (.ics) File](https://community.rockrms.com/recipes/540).

Agent checks:

- Does the route expose public data?
- Does the template enforce security if needed?
- Are dangerous Lava commands enabled?
- Are query-string/body parameters sanitized and validated?
- Does the response content type match client expectations?
- Is the webhook discoverable or guessable?
- Is the route intended for GET? If it mutates data, use a non-GET method and add CSRF/replay/signature controls where applicable.
- Is there rate limiting, caching, or monitoring? Older Lava Webhooks may lack newer Helix controls.

### Workflow Webhook Defined Type

The source pack includes a community recipe for Workflow Webhook setup, not a full official documentation excerpt. Treat exact UI labels as live-instance facts to verify. The Monday.com recipe indicates:

- Define a Workflow Type for the request.
- Add a text attribute such as `RawBody` to store the incoming body.
- Add an attribute with exact key `WebhookResponse` when a response body must be returned.
- Configure a Defined Value under the Workflow Webhook type.
- Use a request-processing Lava expression to accept/reject requests.
- Map webhook variables into workflow attributes.

See [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453). It cites source code for `LaunchWorkflow.ashx`; inspect the installed version if response behavior matters.

Agent checks:

- Is the workflow type active?
- Does the workflow type have secure View permissions?
- Are attributes configured with exact keys expected by the handler?
- Does the request-processing Lava safely validate source, signature, board ID, token, or shared secret?
- Is the raw body stored only where appropriate?
- Is any response data safe for the external caller?
- Are workflow logs/attribute values retaining sensitive payloads longer than necessary?

### Lava Applications

Path depends on Rock version and Helix installation, but the docs describe Lava Applications under the Helix area.

Application fields from official docs:

- **Name**: friendly internal name.
- **Description**: documentation for the application.
- **Slug**: part of endpoint routing.
- **Configuration** or configuration rigging: JSON converted into a dynamic object available to backend endpoints and frontend content blocks. It is intended for relatively static configuration; for dynamic structures, the docs recommend a Persisted Dataset. See [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications).

Application security:

- Standard View/Edit/Administrate.
- Execute View, Execute Edit, Execute Administrate.
- New Lava Applications are given default manage access for `RSR - Lava Application Developers` and `RSR - Rock Administration` according to the docs.
- Default entity View access is overridden for Lava Applications, so security must be configured intentionally. See [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications).

### Lava Endpoints

Endpoint fields from official docs and source view models:

- **Name**
- **Description**
- **Slug**
- **HTTP Method**
- **Security Mode**
- **Code Template**
- **Enabled Lava Commands**
- **Caching Settings**
- **Active state**
- **Rate limit period duration seconds**
- **Rate limit requests per period**
- **Attributes / attribute values**
- **IdKey**

See [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints), [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts), and [LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs).

Endpoint route:

```text
/api/v2/lava-app/1/{application-slug}/{endpoint-slug}
```

Content-block shorthand:

```text
^/{application-slug}/{endpoint-slug}
```

Agent checks:

- Is the endpoint active?
- Does method match the caller?
- Does security mode check endpoint execute or application-level execute?
- Are enabled Lava commands minimal?
- Does the template validate all input server-side?
- Are GET endpoints read-only?
- Do cache headers match sensitivity?
- Are rate limits configured where available?
- Are observability traces available for latency and database-call analysis?

### External Integration Attributes And Block Settings

Some integrations are configured as block settings or transport attributes rather than central API keys.

Examples from the source pack:

- Mailgun integration gained separate API key and HTTP webhook signing key support in release-note records for v15.4/v16.1, with behavior improved in v15.5 when the signing key was missing. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes) and [MailgunCopyApiKeyToHttpWebhookSigningKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/192_MailgunCopyApiKeyToHttpWebhookSigningKey.cs).
- Azure Document Intelligence for mobile check scanning uses a Document Intelligence endpoint and API key in the Financial Batch Detail block settings. See [Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail) and [Check Scanning](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail/check-scanning).
- Roku Applications include an API Key and Authentication Page. See [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications).
- Apple TV applications include API key-style app configuration and remote sign-in setup. See [Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) and [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page).
- SMS transport plugins can implement `ISmsPipelineWebhook` and expose `SmsPipelineWebhookPath` so the SMS Pipeline block can display the webhook URL for remote service setup. See [Extending Communication Transports](https://community.rockrms.com/developer/303---blast-off/extending-communication-transports).

## 6. Primary Entities And Relationships

### RestController And RestAction

`RestController` represents a REST controller exposed by Rock. `RestAction` represents an action under a controller. Model Map classifies both under CMS. See [Model Map](https://community.rockrms.com/ModelMap).

Relationships to inspect:

- Controller/action records in Rock security UI.
- Source-code `RestControllerGuid` and `RestActionGuid` attributes.
- Authorization records tied to controller/action/entity type/action.
- API docs generated from controller metadata.

Operationally, a REST route is not sufficiently described by URL alone. Agents should connect the route to its controller, action, security verbs, and implementation.

### LavaApplication And LavaEndpoint

`Lava Endpoint` is a CMS model in Model Map. See [Model Map](https://community.rockrms.com/ModelMap). The Helix docs describe a Lava Application as the container and endpoints as the units of logic. Routes are built from application slug and endpoint slug, with HTTP method contributing to uniqueness. See [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications).

Relationships:

- Lava Application has many Lava Endpoints.
- Application configuration rigging is available to endpoint templates.
- Endpoint security can be checked at endpoint level or application-level mode.
- Endpoint observability uses endpoint and application names as trace attributes. See [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability).
- Endpoint records can have attributes and attribute values in current view models. See [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts).

### Person, UserLogin, REST Key, And Person Token

API authentication commonly resolves to a person or user. For external authentication integrations, UserLogin records bind a person to an authentication provider identity. The Auth0 recipe describes a case where Auth0-created logins were not automatically associated to existing persons, resulting in new users. Use that as a symptom pattern, but verify against current Auth0/OIDC code and configuration. See [Auth0 Integration to associate users](https://community.rockrms.com/recipes/232) and [OidcClientTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Security/OidcClientTests.cs).

`Person Token` is a Core model in Model Map. See [Model Map](https://community.rockrms.com/ModelMap). The security docs distinguish PersonActionIdentifier as a purpose-bound token for a specific action and IdKey as a shorter non-raw-ID identifier appropriate for public-facing blocks. See [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security).

Agent checks:

- Do not expose raw `Person.Id`, `Group.Id`, or other integer IDs to agents, public clients, or query strings when IdKey/Guid can be used.
- Do not treat Guid or IdKey as authorization. Still check rights.
- For one-click or person-specific actions, inspect whether PersonActionIdentifier is the appropriate pattern rather than a general login token.

### WorkflowType, Workflow, Workflow Attributes

Workflow Type defines the process; Workflow is an instance. The advanced entity guide explains that workflow instances are activated from a Workflow Type and can have attribute values set before processing. See [Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide).

REST v2 workflow launch source shows the API route accepts a workflow type identifier and request options, checks workflow type existence and active state, checks View security unless unrestricted write execute is granted, optionally checks related entity View security, sets attribute values, and processes the workflow immediately or in background depending on request options. See [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs) and [launchWorkflowOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts).

Workflow launch options include:

- Attribute values keyed by workflow attribute key.
- Name.
- Immediate behavior.
- Wait behavior, where waiting also forces immediate launch according to the view model snippet. See [launchWorkflowOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts).

### Attribute And AttributeValue

Attributes are central to Rock extensibility. API integrations frequently use attributes to store external IDs, API keys, endpoint URLs, workflow payload fields, transport settings, and custom entity metadata. The developer docs show loading attributes, adding display/edit controls with security, collecting edit values, saving entity changes and attribute values in a transaction. See [Attributes](https://community.rockrms.com/developer/303---blast-off/attributes).

Agent checks:

- Is the secret stored in an AttributeValue? Confirm field type and visibility.
- Is the Attribute scoped to EntityType, EntityTypeQualifierColumn, and EntityTypeQualifierValue correctly?
- Is `IsPersistedValueDirty` relevant for reporting or computed values?
- Are attribute values saved in the same transaction as entity changes when consistency matters?
- Are sensitive attribute values included in API responses, Lava output, logs, or agent tool result objects?

### BinaryFile, Document Type, And File Security

Integrations often expose files: giving statements, generated ICS files, check images, imported documents, or webhook payload attachments. The advanced entity guide notes that BinaryFileType controls security requirements, storage provider, and caching behavior. See [Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide).

Release notes mention security hardening for document type and file linkage in recent versions. If an API returns files, inspect the live Document Type, File Type, BinaryFileType, storage provider, public/private flags, and route authorization rather than assuming file links are safe. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Interaction, Analytics, And Observability Entities

API and integration usage can be tracked as interactions, page views, observability traces, or custom logs.

Lava's `interactionwrite` command can write interactions with channel, component, entity, operation, summary, related entity, campaign/source/medium/content/term, person alias, and custom fields. See [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write).

Roku application settings include page view tracking and retention duration. See [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications).

Helix Lava Endpoint calls include observability activity names and attributes for endpoint/application, with HTTP method already present. See [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability).

## 7. Common API And Integrations Workflows

### External Site Reads Public Calendar Data

Best path:

1. Determine whether the data is already public.
2. Check whether an iCal feed exists for calendar/event data.
3. If only public display data is needed, prefer a public feed or carefully scoped public endpoint over authenticated REST from browser JavaScript.
4. If authenticated data is required, use a server-side integration layer with a REST key/API user.
5. Configure CORS only if a browser origin must call Rock directly.
6. Scope REST permissions to read-only endpoints and entity View access.
7. Avoid exposing tokens to the client.

The community Q&A for external SquareSpace calendar access notes that an API user/person may be needed and that public calendar data may have an iCal feed. Use that as practical guidance, but verify in the installed instance. See [API from external site](https://community.rockrms.com/ask/developing/2641).

### External System Sends A Webhook To Rock

Choose the endpoint pattern:

- Use Workflow Webhook when the desired outcome is a low-code workflow process.
- Use Lava Webhook when the desired outcome is a simple template-rendered response and security needs are minimal or custom-handled.
- Use Helix Lava Endpoint when the endpoint is part of a Rock-rendered HTMX application or needs stronger endpoint/application controls.
- Use custom REST v2 endpoint when compiled C# validation, service-layer logic, structured API docs, or integration-grade security is needed.

Operational checklist:

- Require POST for mutation.
- Validate source with a signature, shared secret, allowlist, or provider-specific signing key when available.
- Store raw payload only when needed.
- Normalize external IDs into attributes or custom tables.
- Make the workflow idempotent.
- Return a narrow success/error response.
- Log enough to trace delivery without retaining secrets.
- Add replay protection for high-risk operations.

The Monday.com recipe illustrates request-body capture and response attributes, but it must be adapted with security validation. See [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453).

### Rock Calls An External API From Lava

Use Lava Web Request for lightweight integrations when Lava is appropriate and the external call does not require complex retry, queueing, or secret management.

Configuration concepts from the Web Request docs:

- URL.
- Parameters.
- Headers.
- Method.
- Basic authentication.
- Body.
- Request content type.
- Response content type.
- Return variable name.
- Timeout considerations.

See [Web Request](https://community.rockrms.com/lava/commands/web-request-commands).

Agent checks:

- Is the `webrequest` Lava command enabled where the template runs?
- Is the external API key hidden from public output?
- Is the request body valid JSON/XML/form data?
- Are headers formatted correctly for the installed Lava parser?
- Is the command written in a parser-compatible style? Community Q&A records a failure where splitting the command across lines was suspected. Treat this as version/template-specific and test in the live Lava environment. See [webrequest not running??](https://community.rockrms.com/ask/developing/2708).
- Is the external call suitable for a page request, or should it be queued/backgrounded?
- Are failures visible in logs or output during testing?

### Create A Custom API With Lava Webhook

Use this for:

- Lightweight read-only JSON/XML feeds.
- Calendar file generation.
- TV/Roku-style content feeds.
- Internal tools where security is controlled by network/route and data sensitivity is low.
- Rapid prototypes that will later become Lava Applications or REST endpoints.

Avoid this for:

- Sensitive person/finance/check-in data.
- Complex write operations.
- Public endpoints requiring strong authentication.
- Heavy SQL or high-volume traffic.
- Anything where unrestricted Lava commands are needed.

The official Lava API page warns that Lava Webhooks have no built-in security. See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).

### Build A Helix HTMX Application

Use Lava Applications when building a dynamic Rock web experience where server-rendered HTML snippets update portions of a page. The Helix overview describes HTMX-driven partial updates and Lava Applications as a better structure than ad hoc Lava Webhooks for this use case. See [Overview](https://community.rockrms.com/developer/helix/overview).

Implementation flow:

1. Create a Lava Application with name, description, slug, and optional static JSON configuration.
2. Configure application security for developers/admins and execute roles.
3. Add endpoints with distinct slug/method combinations.
4. Set endpoint security mode deliberately.
5. Choose method semantics: GET for reads, POST/PUT/DELETE for mutations.
6. Enable only required Lava commands.
7. Add server-side input validation. Client-side validation is useful but not sufficient. See [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation).
8. Use `hx-get`, `hx-post`, etc. from a Lava Application Content block with caret shorthand when appropriate.
9. Add loading indicators for user feedback. See [Loading Indicator](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator).
10. Monitor observability traces and database behavior. See [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability).

### Launch A Workflow Through REST v2

Use the v2 workflow action endpoint when compiled API semantics are preferable to generic webhook matching.

Source-code route:

```text
POST /api/v2/models/workflows/actions/launch/{workflowTypeId}
```

The source indicates:

- The endpoint is authenticated.
- It requires write execute security.
- Read execute actions are excluded from the UI for this write operation.
- Workflow Type View security is checked unless unrestricted write is granted.
- Related entity View security is checked when an entity is provided and supports security, unless unrestricted write is granted.
- If the workflow type is inactive, the request is rejected.
- Attribute values can be supplied by workflow attribute key.
- Immediate/wait options affect processing mode.

See [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs) and [launchWorkflowOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts).

Version caveat: Rock v18.2 release notes report a fix for an error that prevented the Workflows Action Launch API endpoint from functioning. If this endpoint fails on a pre-fix version, inspect release notes and installed patch level. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

## 8. REST API Deep Dive

### Route Discovery

Use instance-generated API docs and `Home > Security > REST Controllers` first. The public demo API docs are helpful for exploration, but the installed instance's routes may differ by version, plugins, and security configuration. See [API Documentation](https://community.rockrms.com/api-docs), [Rock REST API Documentation](https://rock.rocksolidchurchdemo.com/api/docs/index), and [Rock Rest API v2](https://rock.rocksolidchurchdemo.com/api/v2/docs/index).

For v2 source inspection, look under:

- `Rock.Rest/v2/Models/CodeGenerated/*Controller.CodeGenerated.cs`
- `Rock.Rest/v2/Models/Actions/*ActionsController.cs`
- `Rock.Rest/Utility/ApiModelMapper.cs`
- `Rock.ViewModels/Rest/...`
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/...`

The v2 source pack shows `ApiModelMapper` for copying properties from API models into target instances. See [ApiModelMapper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Utility/ApiModelMapper.cs).

### CRUDS Pattern

The v2 API patterns documentation says the code generator can create CRUDS endpoints for models decorated with `CodeGenerateRest`, and generated code uses `CrudEndpointHelper` so controller code remains lean. See [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns).

Typical generated operations:

- Get single item.
- Create item.
- Full update.
- Partial update.
- Delete.
- Search/list behavior where generated.

Do not assume every model has every operation. The docs indicate generation can be limited, such as read-only. Confirm in source and API docs.

### Identifier Handling

Source snippets for generated v2 controllers document identifiers as Id, Guid, or IdKey. See [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs).

Agent guidance:

- Use IdKey for public/agent-facing identifiers where supported.
- Use Guid for stable integration references when IdKey is unavailable.
- Use integer Id only in internal trusted contexts or when a route requires it.
- Always verify authorization for the resolved entity.

### OData Querying

The REST guide presents OData as the way to retrieve data with query examples, pagination data, and return shaping. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

Practical OData checks:

- Test `$filter` against the exact model property name from Swagger/Model Map.
- Use `$select` to reduce payload size and avoid exposing unnecessary fields.
- Use `$top`/pagination controls rather than pulling large tables.
- Use `$orderby` for stable pagination.
- Check whether the route enforces security before or after filtering.
- Avoid building OData strings from unsanitized user input.
- Do not expose sensitive fields merely because the API returns them.

If a property causes serialization or setter errors, inspect the model and installed version. A community Q&A record describes a Schedule API browser exception involving `FriendlyScheduleText` in v12.8. Treat this as a symptom of model serialization/client behavior, not a universal fact. See [REST API for Schedules](https://community.rockrms.com/ask/developing/2710).

### API v2 Security Actions

The v2 API pattern is secure by default. An endpoint with `[Secured]` requires explicit authorization. If core staff roles need access out of the box, a migration should add default security. If the endpoint is intended for third-party use, it can remain deny-all until an administrator grants access. See [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns).

Interpretation for agents:

- `EXECUTE_READ` and `EXECUTE_WRITE` mean the endpoint can be executed and should check per-entity security.
- `EXECUTE_UNRESTRICTED_READ` and `EXECUTE_UNRESTRICTED_WRITE` mean the endpoint can execute without per-entity security checks inside that endpoint.
- `ExcludeSecurityActions` should hide irrelevant actions.
- New custom security actions require high-level approval according to the coding standards page.
- If an API user has unrestricted write, treat the token as high-risk.

### API v2 Generated Controller Example

The Lava Endpoints v2 generated controller demonstrates the pattern:

- `RoutePrefix("api/v2/models/lavaendpoints")`.
- `Authenticate`.
- `Secured` with read or write execute actions.
- `ExcludeSecurityActions` for irrelevant actions.
- Response metadata.
- `RestActionGuid`.
- `CrudEndpointHelper`.
- `IsSecurityIgnored` set when the current person has unrestricted execute. See [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs).

Agents should use this as a source-code landmark when diagnosing why a v2 endpoint returns unauthorized, ignores entity security, or exposes actions in the security UI.

## 9. API Authentication Deep Dive

### Cookie Authentication

The REST guide says the REST API can be configured to allow access based on an HTTP cookie or authorization token. Cookie authentication is useful for Rock UI components and same-site browser workflows. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

Use cookie/session auth when:

- The caller is a logged-in Rock user in the browser.
- The operation should run as the current person.
- The request is same-origin or CORS/cookie settings are intentionally configured.
- The endpoint performs current-person security checks.

Avoid relying on cookie auth when:

- The caller is an external server.
- The user may not be logged in.
- The request is cross-domain and browser cookie policies interfere.
- A background service needs stable credentials.

### REST Authorization Token

Use REST keys for server-to-server integrations and external tools that need stable access. The REST guide states tokens are created under `Home > Security > REST Keys` and then require security permissions. It also states they can be used until revoked. See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api).

Operational rules:

- One token per integration, not one shared global token.
- Name keys with owner, system, purpose, and creation date.
- Associate to a least-privileged API user/person.
- Grant only needed controllers/actions.
- Prefer read execute over unrestricted read.
- Prefer write execute only for required operations.
- Document where the token is stored.
- Rotate on staff/vendor change or suspected exposure.
- Revoke unused keys.

### API Key Purpose

The source pack includes `ApiKeyPurpose` enum metadata indicating Rock has a concept for intended API key purpose in security enums. See [ApiKeyPurpose.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Security/ApiKeyPurpose.cs). The excerpt is thin, so agents should inspect installed source/UI before making claims about current enum values or UI behavior.

### Browser JavaScript And Token Exposure

Do not embed high-privilege Rock REST keys or remote Lava API keys in client-side JavaScript. Remote Lava docs specifically warn that visible JavaScript can expose the endpoint and API key, allowing others to send Lava that runs as the linked API user. See [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava).

Safer alternatives:

- Public read-only endpoint with no secrets and strict output.
- Server-side proxy that holds the token.
- Same-origin authenticated user session with endpoint security.
- OAuth/OIDC or external login flow when appropriate.
- Static export/cache for non-sensitive public data.

### External Identity Providers

Rock supports external authentication integrations such as Auth0 and OIDC. The source pack includes a community Auth0 association recipe and OIDC tests showing behavior around matching claims such as subject, email, given name, and family name. See [Auth0 Integration to associate users](https://community.rockrms.com/recipes/232) and [OidcClientTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Security/OidcClientTests.cs).

Agent checks:

- Which authentication component is configured?
- Which claim maps to the external unique user identity?
- Does Rock match existing persons by email, username, or configured logic?
- Are duplicate UserLogin records being created?
- Is the provider prefix visible in UserLogin?
- Is account linking automatic or action-based?
- Are new users being created unintentionally?
- Are claims trusted and verified by signature/issuer/audience?

### Remote Authentication For TV Apps

Apple TV/Roku flows may use a remote authentication page so users can sign in from a phone/computer instead of typing on a TV. Apple TV docs describe creating an external page with a Remote Authentication block and connecting it to a TV application. Roku application settings include an Authentication Page. See [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) and [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications).

Agent checks:

- Is the application site selected correctly?
- Is the authentication page a website page, not a mobile/TV page?
- Are timeout and success pages configured?
- Is the application API key correct?
- Are page routes public enough for login but not exposing private data?
- Are interactions/page views configured intentionally?

## 10. Webhooks Deep Dive

### Webhook Design Principles

A webhook endpoint should be:

- Narrow: one provider event family per endpoint when possible.
- Authenticated: signature/shared secret/provider validation.
- Idempotent: repeated delivery should not duplicate side effects.
- Observable: logs should identify delivery without leaking secrets.
- Asynchronous when needed: respond quickly and process heavy work in background.
- Versioned: route or payload handling should tolerate provider schema changes.
- Fail-safe: reject unknown event types and invalid payloads.

### Lava Webhook Matching

The Lava API docs describe matching by HTTP verb and URL path after the webhook handler. If the Defined Value includes a verb, it is used as a filter; otherwise behavior should be verified in the installed instance. The URL can use pattern matching and expose path variables to Lava. See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).

Example conceptual route:

```text
GET /Webhooks/Lava.ashx/series/123?simple=true
```

Possible Defined Value pattern:

```text
series/{seriesId}
```

Template variables can then include the relative URL, raw URL, query parameters/body values, and route variables. Inspect the installed Defined Type help text for the complete list.

### Response Content Types

Lava Webhooks can produce non-HTML output when content type is configured. The iCal recipe uses `text/calendar` for downloadable `.ics` content and enables Rock Entity command access for event data. See [Lava Webhook to Create an iCal (.ics) File](https://community.rockrms.com/recipes/540).

Common response types:

- `application/json` for JSON APIs.
- `application/xml` or `text/xml` for XML feeds.
- `text/html` for HTML snippets.
- `text/plain` for simple responses.
- `text/calendar` for ICS files.

Agent checks:

- Does the content type match the client?
- Does the response include appropriate file/download headers if needed?
- Is dynamic content escaped for the target format?
- Are date/time values timezone-correct?
- Are line endings/encoding correct for calendar or XML formats?
- Is the response cacheable?

### Workflow Webhook Response

The Monday.com recipe indicates a `WebhookResponse` workflow attribute key can send a response body back to the webhook caller, based on source-code behavior. See [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453).

Because the source pack only includes a recipe excerpt, verify in live/source:

- Exact handler path.
- Exact Defined Type name.
- Supported variables.
- Whether `WebhookResponse` is still the expected key.
- How status codes are set.
- Whether response is returned before or after workflow completion.
- What happens on workflow errors.

### Mailgun Webhooks

Release notes and source migration records show Mailgun integration changes around API keys and HTTP webhook signing keys. The operational point is that Mailgun's API key and webhook signing key may be separate values, and older configurations may have copied or fallen back between them. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes) and [MailgunCopyApiKeyToHttpWebhookSigningKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/192_MailgunCopyApiKeyToHttpWebhookSigningKey.cs).

Agent checks:

- Which Rock version is installed?
- Does the Mailgun transport have both API key and HTTP webhook signing key attributes?
- Is the signing key missing?
- Are exceptions logged about missing signing key?
- Are opens/clicks/bounces being tracked?
- Is the inbound route reachable from Mailgun?
- Is the webhook signature validation succeeding?
- Has the organization rotated Mailgun keys recently?

### SMS Pipeline Webhooks

Rock v12.1 added `ISmsPipelineWebhook` support so SMS transports can identify the path to their pipeline webhook and show a full URL in the SMS Pipeline block. See [Extending Communication Transports](https://community.rockrms.com/developer/303---blast-off/extending-communication-transports).

Agent checks:

- Which SMS transport is active?
- Does it implement the webhook interface?
- What webhook URL does the SMS Pipeline block display?
- Does the remote SMS provider point to that URL?
- Are inbound message signatures/verification tokens configured?
- Are errors logged in communication transport logs or ExceptionLog?

## 11. Related Rock Areas: Security, Workflows, Lava, Model Map

### Security

Security is the core dependency for API work. Use:

- `IsUserAuthorized(...)` for block action checks.
- `IsAuthorized(...)` for entity-level checks.
- Standard security actions: View, Edit, Administrate, Approve where applicable.
- Custom action verbs when a feature needs separate authorization.
- API v2 execute actions for endpoint execution.
- IdKey/Guid/PersonActionIdentifier for safer identifiers.
- Server-side validation for all externally supplied values.

See [Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Code Security](https://community.rockrms.com/developer/developer-codex/coding-standards/code-security), and [Helix Security](https://community.rockrms.com/developer/helix/overview/security).

### Workflows

Workflows are ideal for orchestration, approvals, notifications, and low-code business processes. They are risky when used as unauthenticated webhooks or when workflow Lava/SQL handles untrusted input.

Use workflows for:

- Intake from external webhooks.
- Human review.
- Notifications.
- Attribute-based branching.
- Simple integrations where idempotency is manageable.

Use custom REST/native code for:

- Complex validation.
- High-volume writes.
- Transactional consistency across many entities.
- Strong API contracts.
- Versioned integration payloads.
- Advanced authentication/signature verification.

See [Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide), [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs), and [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453).

### Lava

Lava can:

- Render dynamic API responses.
- Call external APIs with Web Request.
- Execute entity/SQL/modify/delete/workflow commands when enabled.
- Write interactions.
- Power Helix endpoints and UI fragments.
- Create agent tools in Rock's AI Agent framework.

Lava risks:

- Overexposed data.
- SQL injection.
- Secret leakage.
- Expensive page-time external calls.
- Hidden command access in public templates.
- Missing current-person security checks.
- GET requests that modify data.

See [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava), [Web Request](https://community.rockrms.com/lava/commands/web-request-commands), [Helix Lava Commands](https://community.rockrms.com/developer/helix/lava-commands), and [Helix Security](https://community.rockrms.com/developer/helix/overview/security).

### Model Map

Model Map helps agents:

- Confirm model names.
- Confirm property names before writing OData filters or API payloads.
- Inspect obsolete status.
- Understand table names.
- Find methods and XML comment summaries.
- Avoid guessing relationships.

Source-code snippets show the Model Map block uses `EntityTypeCache.All()`, includes entity types and `IncludeForModelMap` classes, groups them into categories, and builds property/method bags. See [ModelMap.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Example/ModelMap.cs), [ModelMapModelBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapModelBag.cs), and [IncludeForModelMapAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Data/IncludeForModelMapAttribute.cs).

## 12. Administration And Operational Guardrails

### Least Privilege

For every integration:

- Create a dedicated API user/person.
- Create a dedicated key.
- Grant only required endpoints/actions.
- Avoid unrestricted execute unless required.
- Limit entity security to required records/types.
- Disable or delete stale keys.
- Document owner and rotation path.

### Secret Handling

Secrets include:

- REST keys.
- Mailgun API keys.
- Mailgun webhook signing keys.
- Azure Document Intelligence keys.
- Roku/Apple TV app API keys.
- Firebase service accounts.
- Auth0/OIDC client secrets.
- External API keys used by Lava Web Request.
- Webhook shared secrets.

Do not place secrets in:

- Public Lava output.
- Client-side JavaScript.
- Query strings.
- Screenshots.
- Workflow logs unless encrypted/masked.
- Agent-visible tool results.
- Git repositories.
- Public Defined Value descriptions.

### Input Validation

Validate:

- HTTP method.
- Content type.
- Signature/shared secret.
- Required fields.
- Field types and ranges.
- IdKey/Guid format.
- Entity existence.
- Entity authorization.
- Date/time timezone.
- Enumerated values.
- External IDs.
- Payload size.

Helix form validation docs explicitly state client-side validation is not enough and server-side validation is required because endpoints can be accessed directly. See [Form Validation](https://community.rockrms.com/developer/helix/forms-controls/form-validation).

### Method Semantics

Use:

- GET for reads only.
- POST for create/execute operations.
- PUT/PATCH for updates.
- DELETE for deletes where supported.
- Avoid GET for mutation because cross-site links and prefetch behavior can trigger it.

Helix security docs specifically warn against using GET for modifying data. See [Helix Security](https://community.rockrms.com/developer/helix/overview/security).

### Caching

Cache only when safe:

- Public static-ish content can be cached.
- Personalized content should not be public-cacheable.
- API responses with secrets or person data should generally not be cached by browsers/CDNs.
- Lava Endpoint cache settings should match data sensitivity.
- Generated calendar files may be cacheable only if the event data is public and not personalized.

### Rate Limiting And Load

Current Lava Endpoint view models expose rate limit request count and period duration fields. See [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts). Verify the live UI and installed version before relying on this feature operationally.

For high-volume integrations:

- Prefer queued/background processing.
- Avoid heavy Lava/SQL in public endpoints.
- Add idempotency keys.
- Use pagination.
- Use OData selection/projection.
- Cache lookups.
- Monitor observability and database performance.

### Observability

For Lava Applications, observability activity names include endpoint and application, and attributes include endpoint/application names. See [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability).

For REST/custom code, inspect:

- ExceptionLog.
- Rock logs.
- API response codes.
- Web server logs.
- New Relic/observability traces if configured.
- Workflow logs.
- Communication logs.
- Interaction records.

## 13. Developer, API, Lava, And Source-Code Landmarks

### REST And API Source

Key paths:

- [Rock.Rest/Utility/ApiModelMapper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Utility/ApiModelMapper.cs)
- [Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs)
- [Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs)
- [Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts)

Use these to confirm route prefixes, authentication attributes, security attributes, response models, request bags, and helper behavior.

### Lava Application Source

Key paths:

- [Rock.Enums/Cms/LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)
- [Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)
- [Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)
- [Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointDetailOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointDetailOptionsBag.d.ts)

Use these to confirm endpoint field availability, enum values, options, and client models.

### Model Map Source

Key paths:

- [Rock.Blocks/Example/ModelMap.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Example/ModelMap.cs)
- [Rock.ViewModels/Blocks/Example/ModelMap/ModelMapInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapInitializationBox.cs)
- [Rock.ViewModels/Blocks/Example/ModelMap/ModelMapCategoryBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapCategoryBag.cs)
- [Rock.ViewModels/Blocks/Example/ModelMap/ModelMapModelBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapModelBag.cs)
- [Rock.ViewModels/Blocks/Example/ModelMap/ModelMapPropertyBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapPropertyBag.cs)
- [Rock.Data/IncludeForModelMapAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Data/IncludeForModelMapAttribute.cs)

Use these to understand what Model Map includes and why a non-entity type might appear.

### Security And Workflow Source

Key paths:

- [Rock.Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs)
- [Rock.Tests.Integration/Security/SecurityRoleTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Security/SecurityRoleTests.cs)
- [Rock.Tests.Integration/Security/OidcClientTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Security/OidcClientTests.cs)
- [Rock.Tests.Integration/Rest/ControllersTests/AuthControllerTests.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Rest/ControllersTests/AuthControllerTests.cs)

Use these for security migration behavior, OIDC matching behavior, and auth controller test context.

### Integration-Specific Source

Key path:

- [Rock.Plugin/HotFixes/192_MailgunCopyApiKeyToHttpWebhookSigningKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/192_MailgunCopyApiKeyToHttpWebhookSigningKey.cs)

Use this to understand historical Mailgun key migration behavior.

## 14. Reporting, Analytics, And Model Map

### API Usage Reporting

Rock does not have one universal "API usage report" across all surfaces in the source pack. Agents should inspect available data by surface:

- REST: web server logs, observability, ExceptionLog, controller/action security audit, custom logging.
- Lava Application endpoints: observability traces with endpoint/application attributes. See [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability).
- Lava Webhooks: web server logs, ExceptionLog, custom interaction writes, workflow logs if they activate workflows.
- Workflow webhooks: workflow instances, workflow logs, attribute values, exception logs.
- Mobile/TV apps: interactions/page views if enabled, retention settings, application-specific analytics. See [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications).
- Lava-generated interactions: `interactionwrite` command output. See [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write).

### Model Map Use Cases

Use Model Map before writing:

- OData filters.
- API payloads.
- Lava Entity commands.
- SQL queries.
- Agent tools.
- Workflow attribute mappings.
- Documentation about model relationships.

Model Map can show:

- Model category.
- Model name.
- Table name.
- Summary/example.
- Properties.
- Methods.
- Obsolete status and obsolete message.

Source-code records confirm Model Map extracts XML comments and reflection metadata. See [ModelMapModelBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapModelBag.cs), [ModelMapPropertyBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapPropertyBag.cs), and [ModelMapXmlCommentBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapXmlCommentBag.cs).

## 15. Version And Release Caveats

### API v2 Starts In v17 Pattern

The official API Patterns page states that the new v2 API pattern was introduced starting in Rock v17. See [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns).

Implication: On v16 and earlier, do not assume v2 routes or execute security actions exist. On v17+, inspect which routes are present and whether the installed minor version includes the specific endpoint.

### Workflow Action Launch API Fix In v18.2

Release notes state that v18.2 fixed an error that prevented the Workflows Action Launch API endpoint from functioning. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Implication: If `/api/v2/models/workflows/actions/launch/{workflowTypeId}` fails unexpectedly, confirm the exact installed version and patch level before spending time on payload syntax.

### DataView Endpoint Permission Fix In v17.5

Release notes state that v17.5 fixed a DataView endpoint permission issue where a model's `./DataView/{id}` endpoint checked permissions on the wrong entity, often causing permission denied even when the person or API key had explicit DataView permission. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Implication: If DataView-backed model endpoints return unauthorized on older v17 builds, check whether the instance predates v17.5 and whether the permission rows are actually correct.

### Mailgun API Key And Webhook Signing Key

Release notes include entries for separate Mailgun API key and HTTP webhook signing key values in v15.4/v16.1 and an improvement in v15.5 around fallback/logging when the signing key is missing. See [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Source migration records show historical copying behavior. See [MailgunCopyApiKeyToHttpWebhookSigningKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/192_MailgunCopyApiKeyToHttpWebhookSigningKey.cs).

Implication: For Mailgun tracking issues, inspect version, transport attributes, exception logs, and signing key value.

### Helix And Lava Applications

Helix docs describe Lava Applications, endpoints, HTMX, endpoint security, validation, loading indicators, observability, and roadmap items. Some docs present Helix as an upcoming/evolving project, while source records include v19-era Lava Endpoint view models. See [Overview](https://community.rockrms.com/developer/helix/overview), [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications), and [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints).

Implication: Verify whether the site uses core Helix, a plugin version, or a specific Rock version. Asset paths and feature availability can differ.

### Mobile And Shell Caveats

Mobile docs include version requirements for controls and shell updates. Some mobile controls use external APIs such as Spark Data API for Bible content, while financial check scanning uses Azure Document Intelligence. See [Bible Audio](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/bible-audio), [Bible Reader](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/bible-reader), [Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail), and [Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements).

Implication: When an API integration exists inside mobile, verify both Rock core version and mobile shell version.

## 16. Implementation Playbooks

### Playbook A: Server-To-Server REST Read Integration

Use when an external backend needs to read Rock data.

1. Identify exact data and model.
2. Use Model Map to confirm model/property names.
3. Use API docs to find v2 route if available; otherwise use v1 route.
4. Create or identify a dedicated API user/person.
5. Create a dedicated REST key.
6. Grant read execute only on required controller/action.
7. Grant entity View access only where needed.
8. Test with a server-side HTTP client.
9. Add pagination and `$select`.
10. Log response code and correlation ID, not token or full sensitive payload.
11. Document owner, route, key location, and rotation path.

### Playbook B: Browser Public Data Feed

Use when a public website needs non-sensitive data.

1. Check if Rock already exposes a public feed, such as calendar iCal.
2. If not, create a public-safe Lava Webhook or Helix endpoint.
3. Use GET only if read-only.
4. Return only fields required for display.
5. Configure response content type.
6. Configure CORS only for exact trusted origins if browser fetch is required.
7. Do not include REST keys in browser JavaScript.
8. Add cache headers if data is public and can be stale briefly.
9. Monitor usage and errors.

### Playbook C: Webhook To Workflow Intake

Use when a provider event should start a Rock workflow.

1. Create a Workflow Type dedicated to the provider/event.
2. Add attributes for external event ID, raw payload if needed, parsed fields, processing status, and response body if needed.
3. Configure workflow security before exposing endpoint.
4. Add idempotency check by external event ID.
5. Configure Workflow Webhook Defined Value.
6. Add request filter/validation Lava.
7. Map request variables into workflow attributes.
8. Test invalid signature, duplicate event, malformed JSON, and valid event.
9. Confirm response body and status code behavior.
10. Monitor workflow instances and errors.

### Playbook D: Lava Application Endpoint

Use when building Rock internal UI with HTMX/Lava.

1. Create Lava Application with slug and configuration.
2. Grant developer/admin security.
3. Add endpoint with method and slug.
4. Choose security mode.
5. Enable only needed Lava commands.
6. Write endpoint template with server-side validation.
7. Use IdKey/Guid in parameters.
8. Use POST/PUT/DELETE for mutations.
9. Add loading indicator and validation summary.
10. Monitor observability for endpoint latency and database call patterns.

### Playbook E: Custom REST v2 Endpoint

Use when compiled code is needed.

1. Confirm the feature belongs in REST v2 and not a Lava endpoint/workflow.
2. Define request/response view models.
3. Use service-layer boundaries from Rock coding standards. See [Service Layers](https://community.rockrms.com/developer/developer-codex/coding-standards/service-layers).
4. Add authentication.
5. Add `[Secured]` actions appropriate to read/write and restricted/unrestricted semantics.
6. Exclude irrelevant security actions.
7. Check entity security unless intentionally unrestricted.
8. Use IdKey/Guid for external identifiers where possible.
9. Add migrations for default permissions if core Rock needs the endpoint.
10. Add tests, including unauthorized and per-entity security cases.
11. Confirm generated API docs.

### Playbook F: Agent Tool For Rock Data

Use when exposing Rock actions to AI Agents.

1. Group related tools into a Skill.
2. Secure the Skill/tool before attaching to an agent.
3. Use Lava Tools for simple low-code operations; Native Tools for complex logic, external APIs, or heavy database work. See [Native Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools).
4. Never return raw integer IDs to the model; use IdKey. See [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools).
5. Use helper methods to load entities and check security.
6. Shape result objects narrowly.
7. Sanitize returned attribute values.
8. Use cursor pagination when per-item security must be checked. See [List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools).
9. Add guardrails for write actions and communications.
10. Test unauthorized, missing, ambiguous, and high-volume cases.

## 17. Troubleshooting Decision Tree

### API Call Returns 401/Unauthorized

Check:

1. Is the caller authenticated?
2. Is the token present and correctly named/formatted?
3. Is the REST key active and mapped to the expected person/API user?
4. Does the person/API user have execute permission on the REST action?
5. For v2, is the required action `EXECUTE_READ`, `EXECUTE_WRITE`, unrestricted read, or unrestricted write?
6. Does entity-level security also deny access?
7. For workflow launch, does the caller have View on the Workflow Type unless unrestricted write is granted? See [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs).
8. For DataView endpoints on older versions, is the instance affected by the v17.5 permission bug? See [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Browser Shows CORS / Failed To Fetch

Check:

1. Does the URL use `http` or `https`?
2. Is the API host reachable from the browser?
3. Is TLS valid?
4. Is the page origin configured under REST CORS Domains?
5. Is the exact scheme/host/port allowed?
6. Does preflight request succeed?
7. Are credentials/cookies needed, and are browser cookie policies blocking them?
8. Is the call from Swagger using the correct base URL?
9. If the same call works in Postman but not browser, focus on CORS/scheme/cookie/preflight rather than server-side authorization alone.

See [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) and symptom context in [Problem with API Calls](https://community.rockrms.com/ask/developing/2842).

### Works In Postman But Not Browser

Likely causes:

- Browser CORS.
- Missing cookie/session in browser.
- Different headers.
- Preflight failure.
- JavaScript token exposure blocked by design.
- Serialization issue triggered by browser/SWAGGER route shape.
- Mixed content or invalid scheme.

Inspect network tab and server logs. Compare headers and URL exactly.

### Lava Webhook Returns Wrong Template Or 404

Check:

1. Defined Type is `Lava Webhook`.
2. Defined Value value matches path after `/Webhooks/Lava.ashx/`.
3. Method/verb matches.
4. Regex/path variables are correct.
5. The site route/casing/rewrite is not altering path.
6. Template compiles.
7. Required Lava commands are enabled.
8. Errors are not swallowed by production error settings.

### Lava Web Request Fails Silently Or Returns Empty Result

Check:

1. Is `webrequest` command enabled in that Lava context?
2. Is syntax valid for installed Rock/Lava version?
3. Are command parameters on a parser-compatible line/format?
4. Is URL absolute and reachable from the Rock server?
5. Is TLS/certificate valid from the server?
6. Are headers formatted correctly?
7. Is auth token valid?
8. Is request method correct?
9. Is response content type JSON/XML/HTML matching actual response?
10. Is timeout too short?
11. Does ExceptionLog contain details?

See [Web Request](https://community.rockrms.com/lava/commands/web-request-commands) and [webrequest not running??](https://community.rockrms.com/ask/developing/2708).

### Workflow Webhook Does Not Start Workflow

Check:

1. Defined Value is active.
2. Request filter/process Lava returns true.
3. URL includes expected route/filter values.
4. HTTP method matches provider.
5. Workflow Type is active.
6. Workflow Type security permits launch.
7. Required workflow attributes exist.
8. Attribute keys match exactly.
9. Payload size is accepted.
10. Workflow errors are logged.
11. Provider received expected status/response.

### REST v2 Workflow Launch Fails

Check:

1. Installed version includes v18.2 fix if applicable.
2. Route is `/api/v2/models/workflows/actions/launch/{workflowTypeId}`.
3. `workflowTypeId` is valid Id, Guid, or IdKey.
4. Workflow Type exists.
5. Workflow Type is active.
6. Caller has execute write on action.
7. Caller has View on Workflow Type unless unrestricted write.
8. Related entity exists and View security passes unless unrestricted write.
9. Attribute value keys match workflow attribute keys.
10. Immediate/wait options are valid.

See [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs).

### Mailgun Webhook Tracking Fails

Check:

1. Installed Rock version.
2. API key attribute.
3. HTTP webhook signing key attribute.
4. Mailgun route configuration.
5. Mailgun signing key from provider.
6. ExceptionLog for missing key message.
7. Whether fallback behavior applies to installed version.
8. Inbound requests reach Rock.
9. Communication transport is active.

See [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

## 18. Agent Task Recipes

### Recipe: Find The Right API Route

1. Identify the model/action from the user request.
2. Search instance API docs.
3. Check `Home > Security > REST Controllers`.
4. Use Model Map for model/property names.
5. For v2, inspect `Rock.Rest/v2/Models/CodeGenerated` or `Actions`.
6. Confirm route, method, auth, security actions, and response shape.
7. Report exact route and required permissions.

### Recipe: Audit A REST Key

1. Locate key in `Home > Security > REST Keys`.
2. Identify person/API user.
3. List allowed controllers/actions.
4. Identify unrestricted permissions.
5. Check entity security for target records.
6. Check last known use if logs exist.
7. Recommend least-privilege changes and rotation if needed.

### Recipe: Diagnose External Website API Failure

1. Determine browser vs server caller.
2. If browser, inspect CORS and token exposure.
3. If server, inspect auth header/token.
4. Test route with same method and headers.
5. Verify REST action security.
6. Verify entity security.
7. Check API docs and ExceptionLog.
8. Prefer public feed or server proxy if sensitive token would otherwise be exposed.

### Recipe: Review A Lava Webhook Before Launch

1. Confirm purpose and owner.
2. Confirm route and method.
3. Verify no sensitive data is exposed publicly.
4. Review enabled Lava commands.
5. Review input validation.
6. Review output content type.
7. Review caching.
8. Test malformed, missing, unauthorized, and valid requests.
9. Add monitoring/logging.
10. Document rollback/disable path.

### Recipe: Build A Safe Agent Tool

1. Define tool purpose and allowed user roles.
2. Use IdKey for all entity identifiers.
3. Use helper methods to resolve and check security.
4. Return narrow result objects.
5. Sanitize attribute values.
6. Use pagination.
7. Add explicit guardrails for writes.
8. Test with unauthorized current person.
9. Test missing/invalid IdKey.
10. Document terms and date/time assumptions.

See [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools), [Get Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/get-tools), and [List Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools).



















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `30`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| community-reviewed | operational_guidance | Provider event data should be summarized into operational reports that help staff understand delivery health without exposing unnecessary raw event detail. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| community-reviewed | operational_guidance | Email delivery and engagement events are more useful when they are tied back to the Rock communication record or person context that generated the message. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) |
| community-reviewed | operational_guidance | When applying staff training and operational readiness ideas from Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| community-reviewed | operational_guidance | When applying reporting, analytics, and measurement ideas from Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| community-reviewed | operational_guidance | When applying Rock operations and administration ideas from Escaping the Complexity Trap, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-209-escaping-the-complexity-trap) |
| community-reviewed | operational_guidance | the v19 Updates and Shaping Ministry Culture in 2026 episode gives public operational perspective on staff training and operational readiness; use it to frame questions for staff process review rather than as authoritative configuration guidance. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) |
| community-reviewed | operational_guidance | When applying ministry process design ideas from Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) |
| community-reviewed | operational_guidance | the Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team episode gives public operational perspective on ministry process design; use it to frame questions for staff process review rather than as authoritative configuration guidance. _(live verification recommended)_ | [source](https://community.rockrms.com/connect/rock-cast-episode-197) |
| community-reviewed | operational_guidance | Staff may need a web-facing companion experience even when the primary community surface is mobile, especially for moderation, support, and repeated communication work. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) |
| community-reviewed | operational_guidance | AI should be treated as an assistive ministry operations layer: useful for drafting, summarizing, classifying, and routing work, but still requiring human judgment and local policy before action. _(live verification recommended)_ | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| More |  | 18 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `7`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Episode 147: Change is Inevitable, Community is Essential: Navigating Both in Today's World Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-147-navigating-rapid-change-and-our-need-for-communi) | approved_for_public_distillation | 3 | media-insight:73ec0ec8f79d120c |
| [Episode 197: Volunteers, Stewardship, & Shaping Your Digital Team Transcript Insight](https://community.rockrms.com/connect/rock-cast-episode-197) | approved_for_public_distillation | 3 | media-insight:3c8731057b505d28 |
| [Escaping the Complexity Trap \| Ep 209 Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-209-escaping-the-complexity-trap) | approved_for_public_distillation | 3 | media-insight:5696d2af5b6df33b |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/9NB6vpGBo0) | approved_for_public_distillation | 3 | media-insight:72c3c82fab79c57b |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) | approved_for_public_distillation | 3 | media-insight:efa1de0c74bcd9f0 |
| [Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight](https://www.triumph.tech/resources/ai-in-digital-ministry) | approved_for_public_distillation | 3 | media-insight:8a313536a2a7f5bf |
| [v19 Updates and Shaping Ministry Culture in 2026 \| Ep 206 Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-206-v19-updates-and-shaping-ministry-culture-in-2026) | approved_for_public_distillation | 3 | media-insight:6671826b3cf1f7de |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->



















## 19. Source Map And Dependency Notes

Primary official/developer sources:

- [API Documentation](https://community.rockrms.com/api-docs): Rock API portal, v1/v2 demo links, shared API resources.
- [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api): REST overview, authorization, REST keys, CORS, OData, controller discovery.
- [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns): v2 API security model, code generation, endpoint security actions.
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api): Lava Webhook routing, variables, command considerations, security warning.
- [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava): remote Lava endpoint and API key exposure warning.
- [Web Request](https://community.rockrms.com/lava/commands/web-request-commands): external HTTP calls from Lava.
- [Lava Applications](https://community.rockrms.com/developer/helix/lava-applications), [Applications](https://community.rockrms.com/developer/helix/lava-applications/applications), [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints), [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability): Helix endpoint model.
- [Helix Security](https://community.rockrms.com/developer/helix/overview/security): endpoint access, validation, method semantics, SQL safety.
- [Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Code Security](https://community.rockrms.com/developer/developer-codex/coding-standards/code-security): Rock authorization and public-facing security.
- [Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide): entity references including Workflow and BinaryFile concepts.
- [Attributes](https://community.rockrms.com/developer/303---blast-off/attributes): Attribute/AttributeValue programming pattern.
- [Model Map](https://community.rockrms.com/ModelMap): model metadata reference.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): version caveats.

Primary source-code landmarks:

- [ApiModelMapper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Utility/ApiModelMapper.cs)
- [LavaEndpointsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LavaEndpointsController.CodeGenerated.cs)
- [WorkflowsActionsController.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/WorkflowsActionsController.cs)
- [launchWorkflowOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Rest/Models/Workflows/launchWorkflowOptionsBag.d.ts)
- [LavaEndpointSecurityMode.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Cms/LavaEndpointSecurityMode.cs)
- [lavaEndpointBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts)
- [ModelMap.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Example/ModelMap.cs)
- [IncludeForModelMapAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Data/IncludeForModelMapAttribute.cs)
- [MailgunCopyApiKeyToHttpWebhookSigningKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/192_MailgunCopyApiKeyToHttpWebhookSigningKey.cs)
- [HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs)

Community examples used as non-authoritative operational patterns:

- [Lava Webhook to Create an iCal (.ics) File](https://community.rockrms.com/recipes/540)
- [Webhook to Workflow - an Example from Monday.com](https://community.rockrms.com/recipes/453)
- [Auth0 Integration to associate users](https://community.rockrms.com/recipes/232)
- [API from external site](https://community.rockrms.com/ask/developing/2641)
- [REST API for Schedules](https://community.rockrms.com/ask/developing/2710)
- [webrequest not running??](https://community.rockrms.com/ask/developing/2708)
- [Problem with API Calls](https://community.rockrms.com/ask/developing/2842)

Dependency topics:

- **Security**: required for every API, webhook, Lava, workflow, and agent-tool decision.
- **Workflows**: required for webhook-to-workflow and workflow launch endpoints.
- **Lava**: required for Lava Webhooks, Lava Applications, Web Request, Remote Lava, and many low-code integrations.
- **Model Map**: required for reliable model/property/entity discovery before writing filters, payloads, SQL, or agent tool schemas.
