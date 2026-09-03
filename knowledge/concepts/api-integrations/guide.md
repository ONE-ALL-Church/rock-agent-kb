---
id: authored-api-integrations
title: API And Integrations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "41fb72e73790f98002daa7d22627b532534879662d1a6a6aa7fc14e602e082a2"
---

# API And Integrations

## Agent Summary

Rock provides several integration surfaces with different contracts and security boundaries:

- **API v1** is Rock’s classic REST API and is now described as legacy.
- **API v2**, introduced in Rock v17, is recommended for new integrations and starts with controller access denied until an administrator grants explicit permissions.
- **REST authentication** can use an existing Rock user session cookie or an `Authorization-Token`. External applications commonly use administratively managed REST Keys.
- **Lava APIs and webhooks** can provide narrowly tailored output, but Lava webhooks do not add security by default.
- **Helix Lava Endpoints** are directly callable application work units. Their HTTP method, security, inputs, enabled Lava commands, caching, and behavior must be reviewed as an API contract.
- **Provider webhooks** should authenticate callbacks where the provider supports it, correlate useful events with Rock communication or person context, and expose bounded operational reporting rather than unnecessary raw payloads.
- **AI and MCP integrations** should operate through managed Rock tools and permissions. They should never receive unrestricted database access or an arbitrary SQL execution capability.

An agent should identify the exact integration surface, authenticated identity, controller or endpoint, target Rock version, intended read/write scope, and independent readback before recommending production use. The primary API references are Rock’s [API documentation hub](https://community.rockrms.com/api-docs), [v19 API introduction](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api), and [API security guide](https://community.rockrms.com/documentation/supporting-rock/data/api/secure-the-api).

## Scope And Boundaries

This guide covers REST API v1 and v2, REST authentication and controller permissions, OData in the classic REST API, Lava webhooks and remote Lava, Helix Lava Endpoints, provider callbacks, API observability, and the integration boundary for Rock’s developing AI-agent and MCP features.

It does not replace the owning guides for:

- Rock security inheritance, person authorization, or security-role design.
- Lava language syntax and command-specific behavior.
- Workflow configuration.
- Entity relationships and field definitions in the Model Map.
- Communication-provider administration.
- Provider-specific retry, retention, or event-delivery guarantees.
- Installation-specific controller, plugin, webhook, or endpoint configuration.

No organization’s installed configuration is implied by this guide. Two approved claims include bounded read-only verification performed on June 9, 2026: one confirmed the inspected Lava webhook handler’s security surface, and another confirmed the installed Helix endpoint/application surface. Those observations reinforce the inspection workflow but do not establish that another installation has the same configuration or that any particular endpoint is correctly secured.

Community contributions in this guide are labeled as patterns. They require target-version and live-environment validation before use.

## Mental Model

Treat every integration as a chain of independently reviewable boundaries:

1. **Caller** — the browser, server process, provider, application, or agent making the request.
2. **Credential and identity** — the session cookie, REST Key, OAuth token, provider signature, or other authentication mechanism.
3. **Route** — the exact API controller, Lava webhook, Helix endpoint, or block action being called.
4. **Authorization** — whether that identity may invoke the route and, where applicable, view or edit the affected entities.
5. **Input contract** — HTTP method, route values, query parameters, headers, body, identifiers, and validation.
6. **Rock behavior** — controller, Lava, workflow, or managed code that enforces business rules and performs the operation.
7. **Response contract** — the smallest result the caller needs.
8. **Verification** — logs, observability, a safe API read, refreshed UI, or another independent readback proving what persisted.

Authentication only identifies or establishes the caller. It does not prove that the caller has the correct authorization, that entity-level checks occurred, that a write was shaped safely, or that the intended state persisted.

Likewise, an HTTP success response is evidence that a request completed, not necessarily that every intended field or relationship was stored. Agents should verify consequential writes through an independent read path.

## REST API

Rock’s REST services support internal Rock features and external applications. The API can retrieve and modify Rock data over HTTP, while the available entities, operations, and security depend on the installed version and controller configuration. Rock’s current documentation recommends API v2 for new integrations because it offers expanded capabilities and improved consistency. API v1 remains the classic, legacy surface. ([API documentation hub](https://community.rockrms.com/api-docs); [Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api))

### API v1

API v1 is the classic REST API. Its documentation describes entity queries in the form:

```text
{RockSiteUrl}/api/{EntityName}?{ODataQuery}
```

The target installation’s REST Controllers page is the authoritative inventory for exposed controllers. The classic API documentation also describes cross-domain access, OData querying, pagination, and return-data shaping. ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api))

Do not infer that an entity model automatically has every read or write operation an integration needs. Inspect the actual controller documentation and permissions on the target version.

### API v2

Rock introduced the v2 API pattern in v17. Current documentation describes these standard operations:

- `GET` retrieves an item or executes another read.
- `POST` creates an item.
- `PUT` performs a full update and requires all relevant property values.
- `PATCH` performs a partial update of the specified properties.
- `DELETE` removes an item.

Rock recommends using the help text and testing facilities in the installed API v2 documentation to confirm each operation’s contract. ([Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api); [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns))

API v2 is secure by default: access is denied until an administrator explicitly authorizes it. Its controller actions distinguish ordinary read/write access from unrestricted access:

- **Execute Read** permits reads while retaining applicable entity-security checks.
- **Execute Write** permits writes while retaining applicable entity-security checks.
- **Execute Unrestricted Read** permits reads without entity-security checks.
- **Execute Unrestricted Write** permits writes without entity-security checks.
- **Administrate** controls administration of the controller and its security.

Unrestricted actions are materially different from ordinary execution permissions and should not be granted merely to make an integration error disappear. ([Secure the API](https://community.rockrms.com/documentation/supporting-rock/data/api/secure-the-api); [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns))

### OData And Response Shaping

The classic REST documentation supports OData query strings for retrieving matching entities. An agent should identify the entity, then explicitly bound and shape the result rather than requesting an unnecessarily broad object graph. ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api))

The evidence pack does not establish that every v1 OData expression, navigation property, or behavior is identical in API v2. Confirm the installed controller’s documentation before translating a v1 query into a v2 integration.

### Partial And Relationship Writes

Rock’s official v19 documentation distinguishes `PUT` as a full update from `PATCH` as a partial update. A reviewed community pattern therefore recommends `PATCH` when an API v2 integration owns only a bounded set of fields. Before using that pattern, inspect the target operation and Model Map, test on a non-production record, and read back only the fields the integration intended to change. ([Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api); reviewed community pattern: [API v2 documentation](https://community.rockrms.com/api-docs))

Relationship and navigation properties require additional caution. A reviewed community report found that sending partial `Schedules` navigation objects while creating a `GroupLocation` could create unintended related records rather than link the desired records. That is a target-version troubleshooting pattern, not universal API behavior. Keep generated REST create payloads to confirmed fields unless relationship behavior has been tested, and verify related rows independently after the write. ([Rock REST controller source landmark](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs))

Another reviewed community pattern warns that a successful `GroupMember` create may not return a response body containing the new identifier. For an idempotent registration loader, read back the active member by the intended group, person, and role before linking another record to it. Verify the final links and absence of unintended duplicates. This pattern also requires target-version live verification. ([Rock REST controller source landmark](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs))

## API Authentication And Authorization

Rock REST requests require authorization. The approved authentication claim identifies two supported approaches:

- An HTTP cookie associated with an existing Rock user session.
- An `Authorization-Token` supplied with subsequent API requests.

([Approved claim `claim:2cb25390d2b5f4ffeb6f`](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api))

For external applications and scripts, Rock’s v19 documentation directs administrators to `Admin Tools > Settings > REST Keys`. A REST Key has a name, optional description, generated key value, and active state. The key is passed with API requests so Rock can determine the caller and allowed operations. ([REST Keys](https://community.rockrms.com/documentation/supporting-rock/data/api/rest-keys))

The classic REST documentation states that authorization tokens remain usable until explicitly revoked. Store them privately, never place them in a public repository, and plan for revocation as part of the integration lifecycle. Administrative navigation labels differ between older developer documentation and current v19 documentation, so use the path present in the installed version. ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api); [REST Keys](https://community.rockrms.com/documentation/supporting-rock/data/api/rest-keys))

For every REST integration, record and review:

- The integration’s owner and operational purpose.
- The exact target environment and base URL.
- The authenticated session or REST Key.
- The controller and operations required.
- Whether access is read-only or write-capable.
- Whether entity-security checks remain active.
- Where the secret is stored.
- How the credential will be revoked or replaced.
- The independent verification used after writes.

### Browser And Cross-Domain Calls

A browser request can fail even when the same authenticated call succeeds from a server-side client. For classic REST cross-domain access, Rock documents an allowlist managed through its REST CORS Domains settings. CORS approval tells the browser that the calling origin may access the resource; it does not replace request authentication or controller authorization. ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api))

Do not place an authorization token into public browser source merely to resolve a browser-only failure. Move sensitive calls to a trusted server-side component or otherwise redesign the boundary.

## Lava APIs And Webhooks

Rock’s official Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava. The same guidance warns that Lava webhooks do not include security by default. ([Approved claim `claim:410bf6750e90b7193262`](https://community.rockrms.com/lava/lava-api))

This changes the default agent posture: a working Lava webhook is not necessarily a secured webhook. Before recommending it for production, inspect at least:

- The configured route or value.
- The allowed HTTP method.
- The Lava template.
- Every enabled Lava command.
- Inputs from the query string, form, headers, cookies, or body.
- Whether it reads or mutates data.
- The response content type and returned fields.
- The explicit caller-authentication or request-validation design.
- Logging and bounded failure behavior.

A June 9, 2026 bounded read-only review confirmed that the inspected Lava webhook handler selected active configured values by URL and method, loaded the template and enabled commands, and rendered Lava without an explicit permission check in that inspected handler path. This is a reviewed public-safe conclusion supporting the default-security warning; it does not establish the configuration of another installation.

### Remote Lava

Rock’s remote Lava endpoint accepts Lava input and returns rendered output. Official guidance warns that exposing both this endpoint and an API key in browser-visible JavaScript would allow someone with those values to submit Lava that runs as the user linked to the key. The documented endpoint requires HTTPS, but HTTPS does not make a browser-embedded credential private. Rock recommends a trusted server-side caller unless the endpoint has been carefully secured. ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava))

Enabled Lava commands define a meaningful part of the endpoint’s capability. Do not enable entity, SQL, workflow, web-request, delete, or modify capabilities simply because a copied template references them. Review and enable only commands required by the bounded task.

### Community Webhook Example

A community recipe demonstrates a Lava webhook that returns an iCalendar file with the `text/calendar` content type and accepts event or calendar details as parameters. The recipe itself explicitly warns that community recipes are not reviewed or endorsed by the Rock core team. Use it only as an example of response shaping, not as proof of an approved security design. Its use of `GET` is suitable for its documented content-generation pattern; it should not be generalized to mutations. ([Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file))

## Helix Lava Endpoints

Helix Lava Endpoints are the fundamental application work units called from a client. Before changing an application flow, inspect the endpoint’s name, description, slug, HTTP method, security mode, template behavior, enabled Lava commands, and caching configuration. ([Approved claim `claim:d35ed98aadeaabd2cf1e`](https://community.rockrms.com/developer/helix/lava-applications/endpoints))

The documented full route pattern is:

```text
/api/v2/lava-app/1/{application-slug}/{endpoint-slug}
```

Inside a Lava Application Content block, a caret-prefixed route can refer to the application and endpoint slugs:

```text
^/{application-slug}/{endpoint-slug}
```

The endpoint documentation describes `GET` as the normal read/display method and warns against using it to edit database data. `POST` is the general write method, while `PUT` is commonly associated with replacement and `DELETE` with removal. ([Helix Lava Application Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints))

Treat every Helix endpoint as directly callable outside its intended front end. Validate every input, enforce the current caller’s applicable view or edit rights, avoid `GET` for mutations, and sanitize query and body values before using them in SQL. ([Approved claim `claim:72d56e7ee7ef0be4b92e`](https://community.rockrms.com/developer/helix/overview/security))

Documented endpoint merge fields include request method, query-string values, form fields, headers, cookies, and caller/server network information. `Body` and `RawBody` are documented for v19 and later and are unavailable on `GET`. JSON or XML bodies may be converted into objects. Their availability does not make their contents trusted. ([Helix Lava Application Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints))

### Rendering And Caching

Rock v18 introduced `renderlavaendpoint`, which renders a specified Lava Endpoint during the initial page load. If no method is supplied, the command assumes `GET`. Because this bypasses a later client fetch, the agent must still verify that the referenced endpoint method and security match the operation. ([Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint))

For Obsidian clients, Rock documents `cachePromise` as a way to cache an in-flight Promise and then the serialized result, preventing identical controls from issuing duplicate requests while the first request is still pending. Cache keys and expiration must reflect the data’s actual scope and freshness requirements. ([Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls))

### Observability

Rock records observability activities for Lava Endpoint calls using the endpoint and application names and includes the HTTP method in the activity. Use this data to identify slow endpoints and excessive database activity. Observability proves that calls occurred and provides performance evidence; it does not prove correct authorization or persisted state. ([Helix Lava Application Observability](https://community.rockrms.com/developer/helix/lava-applications/observability))

### Public UI Integration Boundary

A reviewed community pattern recommends against using a full Rock page inside an iframe as the long-term contract for a public concierge interface. Content Security Policy `frame-ancestors` rules can block embedding, while iframe sandboxing can change origin and authentication behavior. Prefer a page-hosted Lava Application Content block, a purpose-built Helix endpoint, or a small server-side adapter that returns only approved public fields. Keep authenticated forms and mutations behind separately tested routes. This remains a community pattern requiring live browser and target-site verification. ([Helix endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints); [CSP `frame-ancestors`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors))

## Provider Webhooks And Operational Reporting

Provider callbacks are most useful when they update or illuminate Rock-owned operational context. Reviewed community guidance recommends tying email delivery and engagement events back to the Rock communication or person context that generated the message. It also recommends summarizing provider events into staff-facing operational reports rather than exposing unnecessary raw event detail. ([Approved claim `claim:fb85d514f4ed765acad4`](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5#t=177); [approved claim `claim:cd52138ec6ca3848cae9`](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5#t=103))

A provider integration should therefore separate:

- **Ingress evidence:** the callback was received and passed the configured authenticity checks.
- **Correlation:** the event maps to the relevant Rock communication, recipient, or person context.
- **State interpretation:** the provider event is translated into an operationally meaningful status.
- **Reporting:** staff can see delivery health without receiving raw provider payloads.
- **Exception handling:** unmatched or invalid events are diagnosable without exposing sensitive details.

Rock v16.1 release notes added separate Mailgun values for the API key and HTTP webhook signing key. Installations using Mailgun should verify that the signing key—not merely the outbound API credential—is configured for webhook validation. ([Rock v16.1 release notes](https://www.rockrms.com/releasenotes))

For SMS transport development, Rock v12.1 added `ISmsPipelineWebhook` and its `SmsPipelineWebhookPath`, allowing the SMS Pipeline block to display a transport’s corresponding webhook URL. This identifies the callback location; it does not by itself establish authentication or provider configuration. ([Extending Communication Transports](https://community.rockrms.com/developer/303---blast-off/extending-communication-transports))

## AI, MCP, And Custom Integration Tools

Rock’s reviewed pre-release MCP design uses OAuth so the external harness holds and renews the access token without exposing a general Rock API key to the language model. Administrators must still verify client authorization, scope, renewal, and revocation behavior in the released implementation. ([Approved claim `claim:2a2a9fc94666d58b0e4f`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s))

The pre-release design also applies Rock permission checks as the person using the agent, including MCP access, rather than granting unrestricted administrative access. This must be verified against the shipped version and each enabled tool. ([Approved claim `claim:2a7ef23854b5dd315c7d`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s))

Rock’s developing agent model separates agents, skills, and tools, with configuration and security boundaries at each layer. Chat versus MCP and Internal versus Public are separate design choices. Only tools authorized for both the current person and agent should be exposed to the model. ([Approved claim `claim:b4fb38224ff8452078f3`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s))

### Managed Data Access

Do not give an AI integration unrestricted direct database access. Route reads and writes through managed Rock code that enforces authorization and business rules. Treat model-generated SQL as unsafe for general-purpose operational access. ([Approved claim `claim:a181b9ddd5b0e689895b`](https://www.youtube.com/watch?v=mYTaGxYMyyQ&t=557s))

The reviewed AI Summit guidance distinguishes an open-ended SQL execution capability from reviewed static SQL inside a narrowly secured Lava tool. Even the latter remains bounded by the tool’s permissions, inputs, expected result shape, and operational review. ([Approved claim `claim:c3921cb1d8b61e06c713`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s))

### Tool Contracts

Custom tools should use clear verb-and-entity names and intentional result shapes such as Lookup, List, Get, Summary, Insights, AvailableAttributes, and AddOrUpdate. Explicit parameters and bounded results help the model select the correct tool without filling its context with unnecessary data. ([Approved claim `claim:60c2bcd25e1cce4efef4`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s))

Lava tools should:

- Return structured `AgentToolResult` values.
- Use the dedicated filters for instructions, compact history, metadata, and Rock reference routes.
- Declare and sanitize parameters explicitly.
- Use built-in tool logs to inspect calls, inputs, and results during debugging.

([Approved claim `claim:4b7b8d0b0379ceb7587f`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s))

Prompt context is layered across Rock’s core prompt, organization prompt, agent instructions, skill instructions, and current-person context. Keep each layer concise, add instructions when testing demonstrates a need, and pass IdKeys rather than raw integer identifiers. ([Approved claim `claim:57e32b4d554a759231a1`](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s))

Rock-side skills and tools provide platform capabilities, while an external harness can hold organization-specific business rules governing their use. Version and govern both layers; do not assume that MCP tools alone contain local policy. ([Approved claim `claim:538f1a4e0ad7c90f7c5a`](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=909s))

A reviewed community pattern for public AI search recommends keeping the action-route registry separate from the semantic-search corpus. A route registry may contain approved handoffs to login, giving, registration, or other actions, while fuzzy retrieval should contain only bounded, public, answerable content. Exact actions should return to the approved Rock page, form, or workflow boundary. This pattern requires organization-specific content review and live verification. ([Helix security](https://community.rockrms.com/developer/helix/overview/security))

## Model Map And Source-Code Landmarks

Use the installed API documentation to identify callable routes and operations. Use the Model Map to understand model names, properties, relationships, obsolete status, and associated table information. Neither proves that a controller is enabled, that the authenticated identity is authorized, or that a relationship can be safely updated through a particular payload.

At immutable Rock commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, the public Model Map implementation represents model details including names, properties, methods, obsolete status, and table names. Its builder reflects registered model types and combines code documentation with database schema information. This is implementation evidence for that commit, not proof of an installation’s schema or version. ([ModelMapModelBag.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Example/ModelMap/ModelMapModelBag.cs); [ModelMapBuilder.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/model-map-builder/ModelMapBuilder.cs))

The same commit includes `ApiModelMapper`, an implementation utility for copying mapped API-model properties into target instances. Its existence does not establish the behavior of any specific endpoint or justify submitting arbitrary model properties. ([ApiModelMapper.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/Utility/ApiModelMapper.cs))

## Version And Authority Caveats

- API v2 was introduced in Rock v17. The administrative API articles in this pack are for v19.0. Confirm behavior against the installed version. ([API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns); [Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api))
- API v1 remains available as the classic API but is identified by Rock as legacy. Do not assume v1 and v2 routes, permissions, payloads, or query behavior are interchangeable. ([API documentation hub](https://community.rockrms.com/api-docs))
- Rock v19.5 fixed an error in the Group Locations v2 search endpoint when retrieving full objects. Include the exact patch level when diagnosing that symptom. ([Rock release notes](https://www.rockrms.com/releasenotes))
- `renderlavaendpoint` is documented for v18 and later. Endpoint request `Body` and `RawBody` merge fields are documented for v19 and later. ([Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint); [Helix endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints))
- Rock v18.1 added a separate server-side Google API Key global attribute for requests such as geocoding and routing. It is distinct from the client-side JavaScript key. Verify which key a particular integration expects. ([Rock release notes](https://www.rockrms.com/releasenotes))
- The AI-agent and MCP claims are drawn from reviewed official summit and podcast material describing developing or pre-release behavior. The supplied release notes label Rock v20.0 as alpha. Verify the shipped version before treating those designs as available production behavior. ([Rock release notes](https://www.rockrms.com/releasenotes))
- Community recipes and contribution patterns are examples, not statements of universal Rock behavior.
- Public GitHub evidence is authoritative only for the supplied immutable commit. Links to `develop` in community patterns are mutable and require a commit-specific source review before implementation.

## Troubleshooting Decision Tree

### The API request is rejected with an authorization error

1. Confirm the target environment and exact base URL.
2. Identify whether the caller is using a session cookie or `Authorization-Token`.
3. If using a REST Key, verify that the key is active without exposing its value.
4. Confirm the exact controller and operation.
5. For v2, inspect whether the identity has Execute Read or Execute Write as appropriate.
6. Check entity-level access before considering an unrestricted permission.
7. Confirm that the route exists in the installed API documentation.
8. Stop if the only proposed fix is a broad or unrestricted grant without an explained need. ([REST Keys](https://community.rockrms.com/documentation/supporting-rock/data/api/rest-keys); [Secure the API](https://community.rockrms.com/documentation/supporting-rock/data/api/secure-the-api))

### A request works in a server client but fails in a browser

1. Compare the exact method, URL, headers, body, and authenticated identity.
2. Determine whether the browser request crosses origins.
3. Check the installed REST CORS Domains configuration for the calling origin.
4. Inspect the browser’s CORS and network error separately from Rock authorization.
5. Do not expose a REST Key in client-visible code.
6. If the browser would need a secret, move the call behind a trusted server-side adapter. ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api); [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava))

### A v2 update cleared or changed fields the integration did not own

1. Determine whether the integration used `PUT` or `PATCH`.
2. Inspect the installed operation help and current Model Map.
3. Compare the submitted payload with a pre-write snapshot.
4. Read the entity back through an independent path.
5. If the integration owns only selected fields, test the documented partial-update operation on a non-production record.
6. Do not retry the same full payload until omitted/defaulted properties are understood. ([Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api))

### A relationship write created unexpected related records

1. Stop further writes.
2. Capture the exact target version, route, and payload without recording credentials.
3. Read back the primary entity and relationship records.
4. Determine whether partial navigation objects were submitted.
5. Verify that any unexpected records are accidental and unreferenced before proposing cleanup.
6. Retest with a scalar-only payload or the owning application/block action in a safe environment.
7. After approved cleanup, read back both the entity and relationship state. This is a reviewed community pattern requiring live verification. ([Rock REST controller source landmark](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs))

### A create request succeeds but no new identifier is returned

1. Treat the response as confirmation of request completion, not proof of the created record’s identity.
2. Read back using the smallest stable combination of intended identifying fields.
3. Require exactly one expected match before linking another record.
4. If zero or multiple matches exist, stop rather than guessing.
5. Make retries idempotent by reusing the one proven existing match.
6. Verify the final relationship independently. This is a reviewed community pattern requiring target-version testing. ([Rock REST controller source landmark](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs))

### A Lava webhook is reachable more broadly than expected

1. Assume no default Lava-webhook security.
2. Inspect the active route, method, template, and enabled Lava commands.
3. Identify every accepted query, form, header, cookie, and body value.
4. Determine whether the webhook exposes data or performs mutations.
5. Verify the explicit caller-authentication or signature-validation mechanism.
6. Remove unneeded commands and returned fields.
7. Stop production use if authentication, input validation, or caller authorization cannot be demonstrated. ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api); approved claim `claim:410bf6750e90b7193262`)

### A Helix endpoint behaves differently from its front end

1. Call the endpoint contract directly in a safe context; do not assume the UI is its security boundary.
2. Confirm application slug, endpoint slug, and HTTP method.
3. Inspect endpoint and application security settings.
4. Compare query, form, header, cookie, and body inputs with those sent by the UI.
5. Verify current-person view or edit rights.
6. Sanitize and validate all values before any SQL or entity operation.
7. Inspect endpoint observability for method, timing, and excessive database work.
8. Read back persisted data independently after writes. ([Helix endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints); [Helix security](https://community.rockrms.com/developer/helix/overview/security); [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability))

### Provider events arrive but staff cannot interpret delivery health

1. Verify that the callback passed the provider’s configured authenticity check.
2. Determine whether it correlates to a Rock communication, recipient, or person context.
3. Separate matched events from invalid or unmatched events.
4. Map only operationally meaningful status into staff reporting.
5. Keep unnecessary raw payload fields out of routine reports.
6. For Mailgun on applicable versions, verify that the HTTP webhook signing key is distinct from the API key. ([Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5); [Rock release notes](https://www.rockrms.com/releasenotes))

### An AI tool can access more data or actions than expected

1. Disable or withhold the tool from the agent until its boundary is understood.
2. Identify the current person, agent, skill, tool, and channel: Chat or MCP, Internal or Public.
3. Confirm that authorization is enforced by managed Rock code.
4. Check whether the tool contains open-ended SQL or unrestricted data access.
5. Inspect tool parameters, enabled commands, result shape, and logs.
6. Replace raw integer identifiers with IdKeys where supported.
7. Verify the released version’s OAuth, scope, permission, and revocation behavior.
8. Stop if safe operation depends on trusting model instructions instead of enforced authorization. ([AI Summit](https://www.youtube.com/watch?v=UvW68dZBcJ8); [RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM))

## Agent Task Recipes

### Recipe: Preflight A REST Integration

**Outcome:** A documented, least-privilege integration contract ready for safe testing.

1. Record the target Rock environment and version.
2. Open the installed API v1 or v2 documentation.
3. Identify the exact controller, route, and operation.
4. Identify the caller’s session or REST Key without copying the secret into notes.
5. Classify the task as read-only, create, partial update, full replacement, or delete.
6. Inspect controller permissions and applicable entity security.
7. Define the smallest request and response fields.
8. Prepare a non-production or otherwise safe test record.
9. Define the independent readback and rollback expectation before sending a write.
10. Stop before production if unrestricted access is the only known way to make the call succeed.

**Inspect:**

- Installed API documentation.
- REST Key active state.
- Controller security.
- Model Map for relevant properties and relationships.
- Version-specific release notes.

**Do not assume:**

- A matching model name guarantees an exposed route.
- Authentication grants controller or entity access.
- v1 and v2 have identical behavior.
- An HTTP success proves the intended persisted state.

([API documentation](https://community.rockrms.com/api-docs); reviewed community preflight pattern; [Secure the API](https://community.rockrms.com/documentation/supporting-rock/data/api/secure-the-api))

### Recipe: Configure And Review A REST Key

**Outcome:** An active external credential with a named owner, bounded permissions, and a revocation plan.

1. In the installed administration UI, navigate to REST Keys.
2. Create or locate a clearly named key for one integration purpose.
3. Add a description identifying its operational owner and use.
4. Verify the active state.
5. Grant only the controller operations the integration requires.
6. Store the token in an approved secret store, never public source or browser code.
7. Test the narrowest read operation first.
8. Test writes only after defining readback and rollback.
9. Record how the key will be revoked or replaced.

**Stop when:**

- The integration’s owner is unknown.
- A shared general-purpose key is proposed.
- The secret would be exposed to public client code.
- The requested permission cannot be tied to a required operation.

([REST Keys](https://community.rockrms.com/documentation/supporting-rock/data/api/rest-keys); [The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api))

### Recipe: Perform A Bounded API v2 Partial Update

**Outcome:** Only the integration-owned fields are changed and independently verified.

1. Confirm that the installed endpoint supports `PATCH`.
2. Read the target record and retain a bounded pre-write comparison.
3. Identify exactly which fields the integration owns.
4. Exclude navigation objects and unrelated properties unless their behavior is explicitly tested.
5. Submit the partial update against a safe record.
6. Read the entity back through a separate request or UI.
7. Compare the intended fields and confirm unrelated fields remain unchanged.
8. Stop if the endpoint normalizes, ignores, or changes properties unexpectedly.
9. Promote the pattern only after target-version validation.

**Do not assume:**

- `PUT` is safe for a partial object.
- Omitted values are preserved by a full-update operation.
- Relationships behave like scalar properties.

([Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api); reviewed community PATCH pattern)

### Recipe: Review A Lava Webhook Before Production

**Outcome:** A bounded webhook with an explicit security and input contract.

1. Locate the active webhook configuration.
2. Record its route, method, purpose, and expected callers.
3. Inspect the complete Lava template.
4. List every enabled Lava command and remove any not required.
5. Enumerate every input and define validation for its type, size, and allowed values.
6. Determine whether the webhook returns data, activates a workflow, or mutates entities.
7. Define and test caller authentication or request verification.
8. Confirm the response content type and remove unnecessary fields.
9. Exercise valid, missing, malformed, unauthorized, and replayed requests in a safe environment.
10. Inspect logs without retaining secrets or unnecessary raw payloads.
11. Stop if protection relies only on an obscure URL.

([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api); [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava))

### Recipe: Review A Helix Application Flow

**Outcome:** The exact endpoint work units, permissions, methods, and performance risks are understood before modification.

1. Identify the Lava Application and every endpoint used by the client flow.
2. Inspect each endpoint’s name, description, application slug, endpoint slug, and method.
3. Inspect endpoint or application security according to the configured security mode.
4. Review the template and enabled Lava commands.
5. List all query, form, header, cookie, body, and configuration inputs.
6. Confirm caller view or edit rights for every affected entity.
7. Verify that no `GET` endpoint mutates state.
8. Inspect caching settings for user-specific or stale data risk.
9. Review endpoint observability for timing and excessive database calls.
10. Test direct invocation as well as the intended client flow.
11. Independently read back any state changes.

**Stop when:**

- The endpoint is considered safe only because the UI hides it.
- Inputs reach SQL without sanitization.
- The caller’s entity permissions are not enforced.
- Cache scope could mix data between callers.

([Helix endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints); [Helix security](https://community.rockrms.com/developer/helix/overview/security); [Observability](https://community.rockrms.com/developer/helix/lava-applications/observability))

### Recipe: Build A Provider Event Health Report

**Outcome:** Staff can understand delivery health in Rock context without seeing unnecessary raw provider data.

1. List the provider event types with operational meaning.
2. Define the configured authenticity check for callbacks.
3. Define how each valid event correlates to a Rock communication, recipient, or person context.
4. Separate matched, unmatched, invalid, and processing-failed events.
5. Map events to concise operational states.
6. Build a bounded report or data view using the Rock-side communication fields needed by staff.
7. Exclude credentials, signatures, full raw bodies, and unrelated provider metadata.
8. Test a known event through receipt, correlation, state update, and report display.
9. Define an exception-review process for unmatched events.

**Do not assume:**

- Receipt means authenticity.
- Provider status has already been tied to the correct Rock record.
- Raw detail is more useful than a bounded operational summary.

([Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5); approved claims `claim:cd52138ec6ca3848cae9` and `claim:fb85d514f4ed765acad4`)

### Recipe: Approve An AI Or MCP Tool Boundary

**Outcome:** A tool exposes one managed Rock capability with bounded inputs, results, and authorization.

1. Record the shipped Rock version and feature status.
2. Identify whether the integration is Chat or MCP and Internal or Public.
3. Identify the current-person, agent, skill, and tool authorization layers.
4. Give the tool a clear verb-and-entity name.
5. Define explicit sanitized parameters and use IdKeys where supported.
6. Route data operations through managed Rock code.
7. Remove arbitrary SQL, unrestricted database access, and unused Lava commands.
8. Shape the smallest structured result needed by the model.
9. Verify OAuth client, token scope, renewal, and revocation behavior if using MCP.
10. Exercise allowed, denied, malformed, and excessive-result cases.
11. Inspect built-in tool logs for calls, inputs, and results.
12. Confirm that organization policy is versioned in the appropriate Rock or external-harness layer.
13. Stop if security depends on the prompt telling the model not to misuse an available capability.

([AI Summit](https://www.youtube.com/watch?v=UvW68dZBcJ8); [RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM); approved claims `claim:2a2a9fc94666d58b0e4f`, `claim:2a7ef23854b5dd315c7d`, `claim:4b7b8d0b0379ceb7587f`, `claim:60c2bcd25e1cce4efef4`, and `claim:c3921cb1d8b61e06c713`)

## Known Gaps And Live Verification

The evidence pack does not verify:

- The installed Rock version, patch level, API inventory, REST Keys, controller grants, CORS domains, or plugins of a target organization.
- A universal request or response schema for every v1 or v2 route.
- Universal navigation-property behavior for generated REST endpoints.
- Provider-specific retry schedules, replay handling, retention, or complete webhook-signature procedures.
- A single default authentication mechanism for Lava webhooks.
- Production availability or final authorization behavior for the pre-release AI and MCP design.
- That community-described BlockActions, Entity Searches, relationship-write patterns, public-search designs, or iframe alternatives apply unchanged to another installation.
- The correctness of any particular Helix endpoint, despite one bounded review confirming that the endpoint/application surface existed in the inspected instance.
- The security of any particular Lava webhook, despite one bounded review confirming the handler behavior described in the approved claim.
- Production configuration from public GitHub source. Source establishes implementation at a commit, not installed state.

Before production use, perform a separate bounded review that:

1. Confirms the target environment and installed Rock version.
2. Inventories the exact controller, webhook, endpoint, block action, or tool.
3. Verifies the authenticated identity and least-privilege authorization.
4. Inspects installed schema and Model Map only as needed.
5. Tests malformed and unauthorized requests.
6. Uses a non-production record or otherwise approved test scope for writes.
7. Reads consequential changes back independently.
8. Records only public-safe conclusions if the result will enter a public knowledge base.

If a version-dependent route, property, permission, provider setting, or failure cannot be verified, mark it as an unresolved live gap rather than inferring behavior from its name.

## Source Map

### Official Documentation And Release Evidence

- [API Documentation](https://community.rockrms.com/api-docs) — API v1/v2 classification and shared API resources.
- [Intro to the Rock API](https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api) — v19 API purposes, v1/v2 administration, and operation semantics.
- [Secure the API](https://community.rockrms.com/documentation/supporting-rock/data/api/secure-the-api) — v1/v2 controller administration and v2 execution permissions.
- [REST Keys](https://community.rockrms.com/documentation/supporting-rock/data/api/rest-keys) — v19 REST Key creation and active-state guidance.
- [The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) — classic REST authentication, CORS, controller discovery, and OData.
- [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns) — v17+ v2 security and code-generation patterns.
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api) — custom Lava APIs and default-security warning.
- [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava) — remote rendering, HTTPS, and browser-secret risks.
- [Helix Lava Application Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) — route, method, security, inputs, commands, and caching.
- [Helix Security](https://community.rockrms.com/developer/helix/overview/security) — direct-call threat model, authorization, validation, and SQL sanitization.
- [Helix Observability](https://community.rockrms.com/developer/helix/lava-applications/observability) — endpoint activity naming and performance inspection.
- [Render Lava Endpoint](https://community.rockrms.com/lava/commands/render-lava-endpoint) — v18 initial-page rendering behavior.
- [Caching API Calls](https://community.rockrms.com/developer/obsidian/caching-api-calls) — in-flight and result caching for Obsidian API calls.
- [Extending Communication Transports](https://community.rockrms.com/developer/303---blast-off/extending-communication-transports) — v12.1 SMS webhook-path interface.
- [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security) — IdKey guidance and postback identifier validation.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — Mailgun signing-key separation, server-side Google API key, v19.5 API correction, and v20 alpha status.

### Approved Claim Sources

- `claim:410bf6750e90b7193262` — Lava APIs and lack of default Lava-webhook security.
- `claim:d35ed98aadeaabd2cf1e` — Helix endpoints as inspectable application work units.
- `claim:cd52138ec6ca3848cae9` — bounded provider-event operational reporting.
- `claim:fb85d514f4ed765acad4` — correlating delivery events with Rock communication or person context.
- `claim:2a2a9fc94666d58b0e4f` — planned MCP OAuth token handling.
- `claim:2a7ef23854b5dd315c7d` — planned current-person permission enforcement.
- `claim:2cb25390d2b5f4ffeb6f` — REST session-cookie and `Authorization-Token` authentication.
- `claim:4b7b8d0b0379ceb7587f` — structured Lava tool results and tool logging.
- `claim:538f1a4e0ad7c90f7c5a` — governance of Rock-side and external-harness skill layers.
- `claim:57e32b4d554a759231a1` — prompt layering and IdKey guidance.
- `claim:60c2bcd25e1cce4efef4` — tool naming and bounded result shapes.
- `claim:72d56e7ee7ef0be4b92e` — Helix input, method, permission, and SQL-sanitization requirements.
- `claim:a181b9ddd5b0e689895b` — managed Rock access instead of direct AI database access.
- `claim:b4fb38224ff8452078f3` — agent, skill, tool, channel, and security boundaries.
- `claim:c3921cb1d8b61e06c713` — prohibition on model-generated arbitrary SQL execution.

### Community Patterns And Examples

- [Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540/lava-webhook-to-create-an-ical-ics-file) — response-shaping example; not core-endorsed.
- Reviewed ONE&ALL patterns — REST permission preflight, API v2 partial-update safety, relationship-write caution, create-readback-link workflows, update-surface selection, BlockAction readback, public Helix integration boundaries, and separation of public search memory from action routes. Each is example-level evidence requiring target-version live verification.

### Immutable Source Evidence

- Rock commit [`471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3) — bounded implementation evidence for API-model mapping and Model Map structure. It is not evidence of an installation’s version or configuration.