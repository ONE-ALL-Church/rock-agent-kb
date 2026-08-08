---
id: authored-roku
title: Roku Apps
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Roku Apps

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Roku Apps index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Roku Apps in Rock RMS are Lava-driven TV applications that render Roku SceneGraph XML instead of web HTML. The practical model is close to Rock CMS: an application acts like the site boundary, pages act like application routes or screens, Lava produces the dynamic markup, and Rock-provided SceneGraph components add command-aware behavior for navigation, authentication, media playback, page loading, context, and interaction tracking. The official Roku documentation positions this feature as a way to bring Rock-managed media and personalized content to Roku devices, and notes that Roku support was introduced in Rock v16.7 ([Roku Docs](https://community.rockrms.com/developer/roku-docs)).

For operational work, treat every Roku app as a CMS surface plus an API surface plus a TV-device shell. A working page must satisfy all three:

- Rock must have a configured Roku application with a valid API key and appropriate authentication page settings ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).
- Rock must have Roku pages whose SceneGraph content is valid XML and whose outer component is normally `Rock:Page` so focus can be initialized ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page)).
- The generated SceneGraph must be usable on a Roku device, which means focus handling, supported media formats, image URLs, command parameters, caching, and authenticated-person behavior all need to be tested on device or in the Roku development workflow, not just in a browser.

The most important agent rule is this: do not reason about Roku pages as HTML pages. Lava is still the templating language, and Rock entities, attributes, commands, and filters are still relevant, but the rendered output is SceneGraph XML consumed by a TV application. HTML assumptions about links, CSS, JavaScript, browser history, pointer interaction, form submission, and responsive layout do not transfer directly. Rock’s custom Roku controls extend Roku SceneGraph nodes so that Rock-specific commands can be attached to buttons and content nodes ([Controls](https://community.rockrms.com/developer/roku-docs/resources/controls), [Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button), [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)).

For implementation work, start with a small page set:

1. A home page with a `Rock:Page` root and deterministic initial focus.
2. A media list page using a simple layout such as `RowList`.
3. A detail or playback trigger using `playVideo` or `playAudio`.
4. A login page and success/timeout pages if personalized content is required.
5. A utility path for setting context values, such as campus, audience, series, or language.

For debugging, inspect the real generated SceneGraph, the Rock page configuration, the application API/auth settings, interaction records, exception logs, media URLs, cache headers, and current-person state. If a behavior depends on an implementation detail not present in the source pack, verify it in the live Rock instance or the Rock source tree rather than assuming.

## 2. Scope And Terminology

This guide covers Rock-powered Roku applications documented under Rock’s Roku developer documentation, especially getting started, applications, pages, commands, controls, focus handling, media playback, layout nodes, RowList resources, and related Lava/API/security concerns. The source pack is focused on Roku v1 developer documentation, public Rock Lava documentation, Rock API documentation, a Rock source repository record, and selected source-code snippets.

A **Roku App** in this guide means a Rock-managed TV application configured through Rock’s Roku feature set. The official getting-started material compares this to building a website: there is an application boundary and multiple pages, but the page content is SceneGraph XML rather than HTML ([Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)).

A **Roku application** is the Rock configuration object that holds application-level settings such as page-view tracking, page-view retention, API key, and authentication page ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). This is not the same as a single Roku page.

A **Roku page** is a unit of custom Lava-driven SceneGraph content within the Roku application. Pages can be connected through commands, cached according to page settings, and passed context or query-string values ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

**SceneGraph** is Roku’s XML-based UI framework. Rock Roku pages output SceneGraph XML. Rock’s documentation points developers to Roku’s SceneGraph reference and samples for built-in Roku nodes ([Controls](https://community.rockrms.com/developer/roku-docs/resources/controls), [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)).

**Lava** is Rock’s templating language. In Roku pages, Lava is used to generate SceneGraph rather than HTML. Lava can read Rock data, transform values, conditionally render content, execute enabled commands, and build XML structures ([Lava](https://community.rockrms.com/lava), [Entity](https://community.rockrms.com/lava/commands/entity-commands)).

**Rock controls** in the Roku documentation are custom SceneGraph components prefixed with `Rock:`. They extend Roku nodes and expose Rock command fields. Important controls include `Rock:Page`, `Rock:Button`, `Rock:ContentNode`, and `Rock:FocusGroup` ([Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)).

**Commands** are Rock-specific actions attached to controls through `rockCommand`. Commands cover navigation, media playback, utility context, and personal login/logout behavior ([Commands](https://community.rockrms.com/developer/roku-docs/commands)).

**Context** means key/value state set in the Roku app for the life of the application session. The utility commands include `setContext` and `clearContext` ([Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)).

**CurrentPerson** means the Rock person associated with the authenticated TV app session. Roku pages can use the current person in Lava merge fields when available ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

**Interactions** are Rock analytics records. Roku pages and media playback may write page or media interactions depending on application/page/command settings. Related Lava commands can also write interactions from custom templates ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write)).

## 3. Roku Apps Mental Model

Think of a Rock Roku app as a dynamic XML application server for a TV shell. Rock owns application configuration, data access, personalization, page definitions, and generated SceneGraph. Roku owns rendering, remote-control input, focus behavior, media playback, device constraints, and SceneGraph component behavior. The Rock-provided Roku shell bridges those worlds by loading pages from Rock and interpreting Rock command metadata embedded in Rock controls.

The mental model has five layers.

The first layer is **application identity and trust**. The Roku application needs an API key to securely connect back to Rock. The application can also define an authentication page used for remote login flows ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Agents should treat the API key as a secret and verify it has the narrowest practical access needed in the live environment. The source pack does not include the exact database table, admin route, or API-key permission model for Roku applications, so inspect the live instance or source code before making security-impacting changes.

The second layer is **page routing and page content**. A Roku page is the object that stores the SceneGraph content. The content can contain Lava, and the rendered output should be valid SceneGraph. Pages are connected by `pushPage`, `replacePage`, `popPage`, and stack-clearing navigation commands ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

The third layer is **data composition**. Lava can query entities, inspect attributes, use filters, call commands, and build personalized content. This means a Roku screen can show content channel items, media elements, calendar/event data, personalization-driven recommendations, or current-person-specific lists. However, Lava command availability is security-controlled; commands must be enabled in the relevant context or globally where appropriate ([Lava Commands](https://community.rockrms.com/lava/commands), [Entity](https://community.rockrms.com/lava/commands/entity-commands), [Attributes](https://community.rockrms.com/lava/filters/attribute-filters)).

The fourth layer is **focus and command execution**. TV apps do not have mouse-like navigation. A screen that looks visually correct can still be unusable if focus starts on the wrong node or cannot move predictably. `Rock:Page` provides `initialFocus`, and `Rock:FocusGroup` helps with vertical or horizontal focus movement because Roku does not provide the Apple TV-style focus behavior many teams expect ([Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page), [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

The fifth layer is **analytics, cache, and playback continuity**. Application settings can enable page views and define retention. Page settings define cacheability. Navigation commands can set cache-control behavior and suppress interactions. Media commands can work with existing watch maps and interaction GUIDs to resume playback or append to existing watch history ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Media](https://community.rockrms.com/developer/roku-docs/commands/media)).

For an agent, the key operational insight is that Roku pages are not “static templates.” They are live Rock data projections with TV-specific interaction constraints. A page can fail because of invalid XML, disabled Lava commands, a missing current person, a bad API key, an unsupported media format, a cache mismatch, missing focus IDs, expired login verification, security enforcement on attributes, or a CDN serving stale personalized XML. Troubleshooting should walk through those layers in order.

## 4. Source Authority And How To Use This Guide

Use this guide as a synthesis of the supplied source pack, not as a substitute for live verification. The most authoritative source for Roku-specific behavior in the pack is the official Rock Roku documentation under `community.rockrms.com/developer/roku-docs`, including the getting-started, applications, pages, commands, controls, and resources pages ([Roku Docs](https://community.rockrms.com/developer/roku-docs)).

Use the official Roku documentation for built-in SceneGraph node behavior. Rock’s Roku resources page points to the Roku SceneGraph reference and Roku sample repository ([Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)). If a question is about the underlying Roku node, such as `RowList`, `LayoutGroup`, `Button`, `ContentNode`, or `Group`, prefer Roku’s own reference after checking Rock’s extension behavior.

Use Rock’s Lava documentation for Lava syntax, command security, entity queries, caching, attributes, interaction logging, personalization, remote Lava, and API-building patterns ([Lava](https://community.rockrms.com/lava), [Lava Commands](https://community.rockrms.com/lava/commands), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). Roku pages rely heavily on Lava, but only enabled Lava commands should be assumed available.

Use Rock’s API documentation when the issue crosses into REST/API access, API keys, or external integration boundaries. The API documentation distinguishes API v1 as legacy and API v2 as newer, and links to broader API references ([API Documentation](https://community.rockrms.com/api-docs)). The source pack does not include a Roku-specific REST endpoint reference, so inspect the live instance, generated API docs, or source for exact routes.

Use source-code snippets in the pack as landmarks, not full implementation proof. The provided `LavaApplication` source snippets show that Rock has a `LavaApplication` model/service area and that a save hook adds base security to new applications, but the snippets are not enough to fully define the Roku application data model ([LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs), [LavaApplicationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplicationService.cs)). For exact entity columns, authorization defaults, and service behavior, inspect the current source branch and the live database schema.

Use release-note/community records as secondary evidence. A Triumph Tech GitHub Spotlight record notes the new Roku TV app feature under v16.7, but official Rock Roku documentation is the stronger citation for the same caveat ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024), [Roku Docs](https://community.rockrms.com/developer/roku-docs)).

When this guide says “verify in the live instance,” inspect one or more of these surfaces:

- The Roku application configuration screen.
- The Roku page configuration screen.
- The rendered SceneGraph XML for the page, if accessible.
- The Rock exception list.
- The Tools > Interactions area or the underlying `Interaction` records.
- The media element record and resolved media URLs.
- The current Rock source branch for classes under `Rock/Model/CMS/LavaApplication`.
- The API docs exposed by the specific Rock instance.
- Roku device logs or development tooling.

## 5. Core Configuration And Data Model

The supplied pack identifies two primary Rock configuration surfaces: Roku applications and Roku pages.

### Application Configuration

A Roku application is the container for TV app configuration. The official Applications page lists these settings: Enable Page Views, Page View Retention Duration, API Key, and Authentication Page ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).

**Enable Page Views** controls whether page interactions should be written for application usage tracking. Operationally, this is an analytics and storage decision. Enable it when the organization needs page-level usage reporting for the Roku app. Disable it for internal testing, high-volume diagnostics, or privacy-sensitive surfaces where page tracking has not been approved.

**Page View Retention Duration** defines how long page interactions are retained, in days. Agents should align this with the organization’s analytics retention policy. If retention is too short, long-term engagement reports will be incomplete. If retention is too long, interaction tables may grow unnecessarily. Verify whether retention is enforced by a Rock job, application logic, or cleanup process in the live instance before promising an exact purge schedule.

**API Key** is used by the Roku application to securely connect to Rock. Treat it as a credential. Do not embed it in public documentation, screenshots, or client-visible pages. If a Roku app suddenly cannot load data, verify whether the API key exists, is active, belongs to the expected user or integration identity, has required permissions, and has not been rotated.

**Authentication Page** is a website authentication page used for remote authentication in the TV application. The login command depends on this application-level setting because the QR-code flow uses it ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)). Agents should verify that the configured page is reachable over HTTPS, supports the intended auth flow, and does not expose a staff-only or admin-only experience to TV users.

The source snippets identify `Rock.Model.LavaApplication` as a source-code landmark. The save hook snippet indicates base security is added when a new application is saved ([LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)). Do not infer all Roku-specific fields from that snippet alone. For exact field names, inspect the model, migrations, block/view-model code, and database schema in the Rock version being administered.

### Page Configuration

A Roku page stores SceneGraph content and page-level behavior. The official Pages page lists Show in Menu, Scenegraph Content, Cacheability Type, Max Age, and Max Shared Age ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

**Show in Menu** indicates whether a page should be used in navigation menus. The Roku shell does not automatically use this setting; it exists so Lava-authored menus can decide which pages to include ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)). Agents should not assume toggling it changes the shell navigation. If a menu is wrong, inspect the Lava that builds the menu.

**Scenegraph Content** is the XML-based UI content rendered on the Roku device. It can contain Lava. Each page should normally use `Rock:Page` as the outer component so the page can set initial focus ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page)).

**Cacheability Type** controls page response caching. The documented types are Public, Private, No-Cache, and No-Store. Public content may be cached by shared network caches such as CDNs. Private content may be cached only by the application. No-Cache requires revalidation before reuse. No-Store prevents caching ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

**Max Age** is the maximum time the item will be cached. **Max Shared Age** is the maximum time it can be cached in a shared cache ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)). Agents should match these fields to the personalization and update frequency of the page. Public caching is appropriate for stable anonymous catalog screens. Private or personal cache strategies are safer for current-person screens, watch-progress screens, giving-related calls to action, and campus-specific pages.

### Lava Merge Fields

The Pages documentation states that Roku pages have Lava merge fields including `CurrentPerson` and `Context` ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)). The hydrated excerpt is truncated after `Context`, so do not assume the full list from the pack. In a live Rock instance, inspect the page editor debug output if available, render a diagnostic page in a non-production app, or inspect the Roku page rendering code to enumerate exact merge fields.

A safe diagnostic pattern is to create a protected development-only Roku page that renders harmless labels for the presence or absence of expected merge fields:

```xml
<Rock:Page initialFocus="homeBtn">
  <Label text="Current person: {% if CurrentPerson %}yes{% else %}no{% endif %}" />
  <Label text="Campus context: {{ Context.Campus | Escape }}" />
  <Rock:Button id="homeBtn" text="Home" rockCommand="popPage" />
</Rock:Page>
```

Before using this pattern, verify the exact casing expected by Roku SceneGraph fields and the exact shape of `Context` in the live implementation. Do not render sensitive values.

## 6. Primary Entities And Relationships

The source pack does not include a complete model map for Roku-specific entities. It does, however, identify the following conceptual entities and relationships.

A **Lava/Roku application** is the top-level configuration object. Source-code landmarks point to `Rock.Model.LavaApplication` and `LavaApplicationService` ([LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs), [LavaApplicationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplicationService.cs)). It owns application settings such as API key, authentication page, and page-view tracking. Verify exact table names, keys, and relationships in the live schema.

A **Roku page** belongs to or is associated with a Roku application. The page stores SceneGraph content and page-level caching/menu behavior ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)). Verify whether pages are stored in the same generic Lava application page model or a Roku-specific table in the Rock version being used.

A **Rock person** can become the `CurrentPerson` for a TV app session after login. Login is handled through the personal command flow, not through an HTML form on the Roku page ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)). Pages can use current-person data in Lava, subject to security.

A **context key/value pair** is stored for the lifetime of the TV application session and is set or cleared with utility commands ([Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)). Context is useful for campus, audience, language, selected series, or other session-level filters.

A **media element** may be referenced by media commands. The Media command documentation discusses `MediaElements`, `rockVideoMediaElementGuid`, `rockInteractionGuid`, and `rockWatchMap` ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). For exact relationships between Roku playback, Rock media elements, and interaction records, inspect media-related source and live interaction rows.

An **interaction** records page views, media plays, watch progress, or custom analytics. Roku application settings can enable page interactions, navigation commands can suppress page interaction writes, and media commands can append to existing watch maps ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Media](https://community.rockrms.com/developer/roku-docs/commands/media)). Rock Lava also provides interaction-write commands for custom interaction logging ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).

A **content source** might be a Content Channel Item, Media Element, Event Item, Group, Adaptive Message, or any Rock entity that Lava can access. The Roku docs do not prescribe a single content model. Agents should identify the organization’s chosen content source before editing templates.

A practical relationship map:

```text
Roku Application
  owns application settings
  uses API key
  references website authentication page
  contains or scopes Roku Pages
  may write page interactions

Roku Page
  belongs to application
  stores SceneGraph content with Lava
  exposes menu/cache settings
  renders Rock controls and Roku SceneGraph nodes
  can use CurrentPerson and Context merge fields

Rock Control
  extends Roku SceneGraph node
  exposes rockCommand and command parameter fields
  triggers navigation/media/utility/personal behavior

Media Command
  plays URL or MediaElement-derived media
  may read/write Interaction watch map
  may depend on CurrentPerson for personalized tracking

Lava Template
  queries Rock data
  transforms values
  renders SceneGraph XML
  must obey enabled command/security rules
```

## 7. Common Roku Apps Workflows

### Build A First App

The official getting-started path begins with requesting a development application from the Core team through a request form. The docs state that the Core team responds with instructions for getting a development application onto the system ([Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)). For an agent, this means a missing “create app” surface might not be a local configuration mistake; the app package or development shell may not yet be provisioned.

A minimum first app workflow:

1. Confirm Rock version is v16.7 or later, because Roku support was introduced in v16.7 ([Roku Docs](https://community.rockrms.com/developer/roku-docs)).
2. Confirm the organization has the Roku development application/shell installed or provisioned.
3. Create or locate the Roku application configuration in Rock.
4. Set API key, authentication page if login is needed, and page-view tracking settings.
5. Create a home page with valid `Rock:Page` SceneGraph.
6. Add one button or content node that triggers a navigation command.
7. Test on Roku hardware or the approved Roku development workflow.
8. Add media playback only after navigation and focus are stable.

### Add A Page

Use the official [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) and [Roku documentation](https://community.rockrms.com/developer/roku-docs) as the page contract. Verify the rendered XML, focus target, command parameters, cache behavior, and navigation on the target Rock version and a real Roku shell.

A page addition is not complete when the page record exists. It must be addressable, focusable, and reachable.

Checklist:

- Page has a stable name and GUID.
- `Show in Menu` is set according to whether Lava-built menus should include it.
- SceneGraph content has a `Rock:Page` outer component.
- `initialFocus` references a real focusable node ID.
- Any `rockCommand` parameters point to valid page GUIDs, media URLs, or context values.
- Cache settings match personalization needs.
- Lava commands required by the page are enabled in the appropriate context.
- The generated XML is valid after Lava renders with anonymous and authenticated users.

### Build A Menu

Because `Show in Menu` is not automatically consumed by the Roku shell, menus are Lava work. The page setting only gives authors a flag to use ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)). Agents should inspect the menu-building template. If the menu does not update after toggling Show in Menu, search for cached menu Lava, page query filters, hard-coded page GUIDs, or stale CDN/app cache.

A menu item should normally render as a `Rock:ContentNode` or `Rock:Button` with a navigation command. For richer layouts, render content nodes under a `RowList`.

### Add Login

The login workflow uses the Personal command. The application must define a Login page before using the login command, because that setting is used to configure the QR code ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)). The command can include page GUIDs for login display, timeout, and success.

A login-ready app needs:

- Application Authentication Page configured.
- Roku login page that includes the required SceneGraph node IDs used by the shell.
- Timeout page.
- Success page.
- A command trigger such as `Rock:Button rockCommand="login"`.
- A post-login navigation decision: remain in place, go home, or route to a personalized screen.
- Clear navigation stack behavior chosen intentionally to avoid back navigation to pre-login or other-user data.

The docs identify two special IDs used on the login page: `lgnQrPoster`, which receives the login-page URL plus verification code, and `lgnCodeLabel`, which receives the verification code text ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)). Verify exact casing and node types in the live app before troubleshooting QR display.

### Play Media

The Media commands handle video and audio. The docs explicitly state YouTube content cannot be played in a Roku TV application ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). For video, use direct MP4 or HLS URLs where supported by Roku and Rock’s command contract. If using Rock Media Elements, use the media element fields and watch-map behavior documented for the command.

A playback-ready item should have:

- A playable direct URL or valid media element reference.
- A supported file/stream format.
- Poster/artwork URLs accessible by Roku.
- Metadata fields where supported.
- Watch map and interaction GUID if resuming or appending to existing watch data.
- A fallback if the current person is anonymous.
- A non-YouTube source.

### Personalize Content

Personalized Roku pages can use `CurrentPerson`, attributes, entity queries, personalization segments, adaptive messages, and context. Rock’s Personalize Lava command can show content based on personalization segments and request filters ([Personalize](https://community.rockrms.com/lava/commands/personalize-commands)). Adaptive Message can retrieve matching message adaptations for a person in Rock v17.0+ ([Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands)).

Do not use public/shared caching for XML that includes current-person data unless the command or cache strategy explicitly personalizes the URL. Use page-level Private/No-Store or command-level personal cache options as appropriate.

## 8. Roku Getting Started Deep Dive

Rock’s getting-started documentation frames Roku development as similar to website development with one major change: the output language is SceneGraph XML instead of HTML ([Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)). This comparison is useful but incomplete. A Rock website page is usually rendered by a browser with HTML, CSS, JavaScript, links, forms, and browser navigation. A Roku page is rendered by a Roku SceneGraph engine with focusable nodes, remote-control navigation, media playback constraints, and TV-safe layout expectations.

The getting-started process has three practical phases: provisioning, page construction, and device validation.

### Provisioning

The docs say to request a development application from the Core team through the linked request form, after which instructions are provided for getting the development application on the system ([Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)). Agents should confirm whether the target environment already has that development app installed. If not, local page edits may be correct but untestable.

Provisioning questions to answer:

- Which Rock version is running?
- Is it at least v16.7?
- Is the Roku feature enabled or installed in this instance?
- Is the Roku application shell available to the organization?
- Which Rock environment is the development app pointing to?
- Is the environment publicly reachable over HTTPS from Roku devices?
- Is the API key present and active?
- Is media hosted in a way Roku devices can access?

### Page Construction

A first page should be intentionally boring. The goal is to verify the full pipeline.

Example structure:

```xml
<Rock:Page initialFocus="watchBtn">
  <Label text="Welcome" />
  <Rock:Button
    id="watchBtn"
    text="Watch Latest"
    rockCommand="pushPage"
    rockPageGuid="REPLACE-WITH-PAGE-GUID"
    rockPageShowLoading="true" />
</Rock:Page>
```

This is not meant to be pasted blindly. Verify field casing against Roku SceneGraph conventions and the live Rock renderer. The official `Rock:Page` documentation shows the `initialFocus` field and a `Rock:Button` child that pushes another page ([Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page)). The Button documentation shows that `Rock:Button` extends Roku’s Button and adds `rockCommand` plus command parameter fields ([Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button)).

### Device Validation

A page is not done until it is tested with TV navigation. Validate:

- Page loads without XML parse errors.
- Initial focus appears where expected.
- Remote up/down/left/right movement is predictable.
- Back behavior matches the navigation stack design.
- Loading indicators appear only when useful.
- Anonymous state renders safely.
- Authenticated state renders with correct person.
- Media starts, pauses, resumes, and exits cleanly.
- Interactions are written or suppressed as intended.
- Cached pages update according to their settings.

The official tips page says to keep layouts simple and use layout controls such as RowList for media/content selection ([Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks)). For first builds, this is more than style advice. Simpler SceneGraph lowers the chance of broken focus, missing templates, poor device performance, and difficult BrightScript debugging.

## 9. Roku Commands Deep Dive

Commands are how Rock-specific actions are triggered from Roku SceneGraph. A command is attached to an applicable Rock control with `rockCommand`; the control also carries the command-specific parameters ([Commands](https://community.rockrms.com/developer/roku-docs/commands)). `Rock:Button` and `Rock:ContentNode` are the primary documented controls for command handling ([Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button), [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)).

### Multiple Commands

Rock supports multiple commands on a single control by separating command names with commas. The official example combines `setContext` and `pushPage` so a selection stores context and then navigates ([Commands](https://community.rockrms.com/developer/roku-docs/commands)).

Use this sparingly. Multiple commands are useful when a single user action has an obvious compound meaning, such as “choose campus and continue.” They are risky when commands have ordering assumptions, failure modes, or security implications. If a page behaves unpredictably, split the action into simpler steps during debugging.

A common pattern:

```xml
<Rock:ContentNode
  title="Rancho Campus"
  rockCommand="setContext, pushPage"
  rockContextKey="Campus"
  rockContextValue="REPLACE-WITH-CAMPUS-GUID"
  rockPageGuid="REPLACE-WITH-NEXT-PAGE-GUID" />
```

### Navigation Commands

Navigation commands manage the app’s page stack ([Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

`pushPage` pushes a new page onto the navigation stack. Use this when the Back button should return to the previous screen.

Important parameters:

- `rockPageGuid`: page GUID to load, with optional query-string parameters.
- `rockPageCacheControl`: command-level cache behavior. The docs include Public, Personal, and Private semantics, with optional seconds such as `public:600` or `personal:600`.
- `rockPageShowLoading`: whether to show a loading screen while the page loads. Default is false.
- `rockPageSuppressInteraction`: whether to suppress writing an interaction record. Default is false.

Use `pushPage` for drill-in flows such as Home > Series > Episode Detail.

`replacePage` replaces the top page on the stack while keeping the rest of the stack intact ([Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)). Use this when changing tabs, filters, or variants where Back should not step through every intermediate state.

`popPage` returns to the previous page. Use this for explicit “Back” controls if needed, though Roku’s remote back behavior should also be tested.

`clearNavigationStack` clears the navigation stack. Use this after login/logout or a major state reset when prior screens may contain stale or unauthorized data. The login command also has a navigation stack clearing option ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

### Cache Control In Navigation

There are two caching surfaces: page settings and command-level page cache control. Page settings define default HTTP cache behavior for the page. Command-level `rockPageCacheControl` can influence how a navigation request is cached ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

A practical cache policy:

- Use public caching for anonymous, stable catalog data.
- Use personal caching for pages where the URL should vary by logged-in person.
- Use private/no-store behavior for sensitive personalized pages.
- Use short max ages for frequently updated media lists.
- Avoid long shared-cache durations while developing.
- Suppress interactions only for utility screens, loading redirects, or pages that would distort analytics.

### Utility Commands

The utility commands are `setContext` and `clearContext` ([Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)).

`setContext` stores a key/value pair for the lifetime of the application session. Use it for state that should be available across pages without repeatedly adding query-string values. Examples include campus, selected ministry, content category, language, selected audience, or a preferred media filter.

`clearContext` removes a context value by key. Use it when leaving a scoped experience or switching identities.

Operational guidance:

- Use stable keys such as `Campus`, `Audience`, `Language`, or `Series`.
- Prefer GUIDs or IDs that match real Rock records, not display names.
- Validate context values before using them in SQL or entity queries.
- Do not store secrets in context.
- Clear context on logout if it could affect another user.

### Media Commands

The media commands are `playVideo` and `playAudio` ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). The docs explicitly state that YouTube content cannot be played in a Roku TV application. Use direct media files or streams that Roku supports, such as MP4 or HLS where documented for the command.

Shared media behavior:

- `rockWatchMap` can set the resume location from an existing interaction.
- `rockInteractionGuid` plus `rockWatchMap` can append to an existing interaction’s watch map.
- If `rockWatchMap` is provided without `rockInteractionGuid`, it can be used for resume position, but a new interaction is written with a fresh watch map ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)).

Video parameters shown in the pack include `rockVideoUrl`, `rockVideoMediaElementGuid`, `rockInteractionGuid`, and `rockWatchMap` ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). The excerpt is truncated and appears to contain a typo in the media element parameter type. Verify the current official page or source for the complete parameter list before building a generator that emits every supported field.

A safe media item should be generated from a known valid media source:

```xml
<Rock:ContentNode
  title="{{ item.Title | Escape }}"
  hdposterurl="{{ item.ImageUrl | Escape }}"
  rockCommand="playVideo"
  rockVideoUrl="{{ item.VideoUrl | Escape }}" />
```

Before using that pattern, verify exact property casing for `title`, `hdposterurl`, and the command fields in the target Roku app.

### Personal Commands

The Personal documentation covers login behavior and references logout behavior ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)). Login allows an individual to authenticate to the TV application. Before using `rockCommand="login"`, the application must have a Login page configured because that setting is used for the QR code.

Login command parameters identified in the pack:

- `rockLoginPageGuid`: page used to show login information.
- `rockLoginTimeoutPageGuid`: page shown after the login period expires.
- `rockLoginSuccessPageGuid`: page shown after successful login.
- `rockLoginTimeoutDuration`: timeout in seconds, defaulting to 600.
- `rockLoginCheckDuration`: seconds between server checks, defaulting to 5.
- `rockLoginClearNavigationStack`: whether to clear navigation stack after successful login, defaulting to true ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

The login page must include specific IDs the shell updates because platform limitations prevent a normal merge-field-only approach. The documented IDs are `lgnQrPoster` for the QR image and `lgnCodeLabel` for the verification code label ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

## 10. Roku Controls Deep Dive

Rock’s custom Roku controls extend Roku SceneGraph nodes and add Rock-specific fields. Most of the app still uses built-in SceneGraph components; the Rock controls provide command handling, focus/page behavior, and convenience around Rock app semantics ([Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)).

### Rock:Page

`Rock:Page` is the standard outer control for page content. It extends Roku’s `Group` node and represents the full page of content ([Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page)). Its documented field is `initialFocus`, a string containing the ID of the item to focus when the page appears.

Use `Rock:Page` at the outermost level of each Roku page unless you have verified a specific exception in source or official docs. A page without deterministic initial focus may load but feel broken to TV users.

Example pattern:

```xml
<Rock:Page initialFocus="primaryAction">
  <Poster uri="{{ HeaderImageUrl | Escape }}" width="1280" height="300" />
  <Label text="{{ PageTitle | Escape }}" />
  <Rock:Button
    id="primaryAction"
    text="Watch"
    rockCommand="playVideo"
    rockVideoUrl="{{ VideoUrl | Escape }}" />
</Rock:Page>
```

Do not assume browser-style tab order. Explicit focus is part of the screen contract.

### Rock:Button

`Rock:Button` extends Roku’s Button and adds `rockCommand` plus fields for the command parameters, such as `rockVideoUrl` ([Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button)). Use it for explicit command actions: login, play, continue, back, switch campus, open a detail page.

Button guidance:

- Every actionable button should have a stable `id` if it may receive focus.
- Use short TV-readable text.
- Attach only the command fields needed for that action.
- Avoid large dynamic labels that may overflow.
- Test focus visual state and remote activation on device.

### Rock:ContentNode

`Rock:ContentNode` extends Roku’s ContentNode and adds `rockCommand` plus command parameter fields ([Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)). It is especially useful inside data-driven lists such as RowList content. A content node can represent an item and carry the command to execute when selected.

Use `Rock:ContentNode` for generated rows/items. For example, a row item can carry title, image, and playback or navigation parameters.

```xml
<Rock:ContentNode
  id="episode-{{ item.Id }}"
  title="{{ item.Title | Escape }}"
  hdposterurl="{{ item.PosterUrl | Escape }}"
  rockCommand="pushPage"
  rockPageGuid="{{ DetailPageGuid }}?ItemId={{ item.Id }}" />
```

Validate that item IDs create valid XML IDs. If IDs can contain invalid characters, normalize them.

### Rock:FocusGroup

`Rock:FocusGroup` manages vertical or horizontal focus movement and extends Roku’s `LayoutGroup` ([Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)). The docs state that, as of 2024, focus management is not built into Roku apps in the way Apple TV developers might expect. `Rock:FocusGroup` handles layout direction and directional focus management for vertical or horizontal orientation.

Use a horizontal focus group when left/right should move among sibling controls. Use a vertical focus group when up/down should move among sibling controls.

Design guidance:

- Keep focus groups small and predictable.
- Avoid deeply nested focus groups until basic navigation is proven.
- Match layout direction to remote direction.
- Use visible focus indicators where supported, such as `showFocusFootprint` in documented examples.
- Test both entry and exit from each focus group.

### Built-In SceneGraph Nodes

Rock does not replace Roku SceneGraph. The Controls page says most of the app is composed of built-in SceneGraph components, and Rock’s Roku Resources page links to Roku’s SceneGraph reference and sample repository ([Controls](https://community.rockrms.com/developer/roku-docs/resources/controls), [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)). For nodes not documented by Rock, use Roku’s own docs.

Agents should distinguish between Rock fields and Roku fields. `rockCommand` is Rock-specific. Fields such as `width`, `height`, `uri`, `title`, `hdposterurl`, and layout parameters may be Roku node fields. If the node fails to render, verify the field belongs to that node and has the expected type.

## 11. Roku Layouts And Resources Deep Dive

The official Layout Nodes page warns that Roku has many layouts, but few have default item templates, and advises caution when picking SceneGraph elements because the Rock approach tries to avoid custom BrightScript components ([Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes)). This has strong implementation implications: choose simple, well-documented layouts first, and do not introduce custom component complexity unless the screen cannot be built with standard nodes.

### RowList

`RowList` is the primary layout node documented in the source pack. It creates horizontally scrollable rows and supports vertical and horizontal scrollability ([RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)). The docs list parameters including:

- `itemSize`: size of the RowList element.
- `numRows`: number of visible rows.
- `rowHeights`: heights for rows.
- `rowItemSize`: item width/height for rows.
- `rowItemSpacing`: spacing between items in each row.
- `RowSpacings`: spacing between rows.
- `showRowLabel`: whether row labels should be shown.
- `vertFocusAnimationStyle`: vertical focus animation style.
- `rowFocusAnimationStyle`: horizontal focus animation style.

Row data binding includes `title` for the row label. Item data binding includes `hdposterurl` for the item image ([RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)).

The required structure is a single root `ContentNode` in the RowList content field. Under that root, each child `ContentNode` represents a row, and row children represent items ([RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)).

Conceptual structure:

```xml
<RowList id="mediaRows" numRows="3">
  <Rock:ContentNode role="content">
    <Rock:ContentNode title="Latest Messages">
      <Rock:ContentNode
        title="Message Title"
        hdposterurl="https://example.org/poster.jpg"
        rockCommand="playVideo"
        rockVideoUrl="https://example.org/video.m3u8" />
    </Rock:ContentNode>
  </Rock:ContentNode>
</RowList>
```

Treat this as a structure guide, not a guaranteed complete snippet. Verify required templates, field casing, and supported item fields in the current Roku implementation.

### Layout Simplicity

The official Tips and Tricks page is brief but important: keep layouts simple and use layout controls such as RowList for media/content selection ([Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks)). For agents, “simple” means:

- Fewer nested containers.
- Fewer custom templates.
- Reusable dimensions.
- Predictable focus movement.
- Minimal per-item dynamic markup.
- Avoiding layout-dependent Lava branches where possible.

Complexity should be moved into data preparation rather than SceneGraph structure. For example, build a clean array of rows/items in Lava, then render a straightforward RowList.

### Roku Resources

Rock’s Roku Resources page points to Roku’s SceneGraph reference and Roku sample repository ([Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)). Use those when a question is about Roku-native behavior:

- Which fields a node supports.
- Which media formats are supported by Roku.
- How focus is expected to behave for a built-in node.
- How content nodes bind to visual item templates.
- Device-specific limitations.

### Useful Links And Feedback

The Useful Links page points developers to feature requests, GitHub issues, and community chat for Roku development feedback ([Useful Links](https://community.rockrms.com/developer/roku-docs/resources/useful-links)). For operational triage, use official issue trackers for suspected platform bugs and community chat for ambiguous implementation patterns, but do not treat community chat as authoritative without confirming in docs/source/live behavior.

## 12. Related Rock Areas: Api Integrations, Lava, Cms, Security, Media, Tv Apps

Roku Apps sit at the intersection of several Rock areas. Agents need enough working knowledge of each to avoid misdiagnosis.

### API Integrations

The Roku application uses an API key to connect securely to Rock ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Rock’s API docs identify API v1 as legacy and API v2 as newer, with shared API resources and a Lava API guide ([API Documentation](https://community.rockrms.com/api-docs)). The source pack does not expose exact Roku endpoints, so verify the live API docs or source before changing integrations.

Common API checks:

- Is the Rock base URL reachable from Roku devices?
- Is HTTPS valid?
- Is the API key active?
- Is the API key tied to the expected user/security role?
- Does the key have access to pages, media, and authentication endpoints?
- Are WAF/CDN rules blocking Roku user agents or API paths?

### Lava

Lava is the authoring layer for dynamic Roku SceneGraph. Rock’s Lava docs explain output markup, tags, filters, shortcodes, and commands ([Lava](https://community.rockrms.com/lava)). In Roku, Lava should generate XML-safe output. Escape user/content values that appear in XML attributes. Avoid raw HTML fragments unless they are intentionally converted to valid SceneGraph text or attributes.

Lava commands are powerful and security-sensitive. Rock’s Lava Commands getting-started page explains that commands must be enabled and can bypass normal business logic/security if misused ([Lava Commands](https://community.rockrms.com/lava/commands)). The `LavaCommandsPicker` source snippet shows Rock dynamically lists available Lava commands through `Rock.Lava.LavaHelper.GetLavaCommands()` ([LavaCommandsPicker.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/LavaCommandsPicker.cs)). For a Roku page, verify which commands are enabled in that rendering context.

High-value Lava commands and filters for Roku:

- `entity` commands for content lookup ([Entity](https://community.rockrms.com/lava/commands/entity-commands)).
- `cache` for expensive shared data, with care around personalization ([Cache](https://community.rockrms.com/lava/commands/cache-commands)).
- attribute filters for custom content fields ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)).
- array filters for building row/item structures ([Arrays](https://community.rockrms.com/lava/filters/array-filters)).
- date/numeric filters for display formatting ([Date Filters](https://community.rockrms.com/lava/filters/date-filters), [Numeric Filters](https://community.rockrms.com/lava/filters/numeric-filters)).
- `interactionwrite` variants for custom analytics ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write)).
- `personalize` and `adaptivemessage` for personalized screens ([Personalize](https://community.rockrms.com/lava/commands/personalize-commands), [Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands)).

### CMS

Roku Apps are closely related to CMS concepts: applications, pages, content, media, personalization, and interactions. The source snippets include CMS LavaApplication model/service files, which are likely relevant to exact implementation ([LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)). If an agent needs to report on existing Roku app configuration, inspect CMS/Lava application records, page records, security auth rows, and related blocks.

### Security

Security has multiple layers:

- API key security.
- Application/page security.
- Lava command enablement.
- Entity command `securityenabled` behavior.
- Attribute security.
- Authentication page security.
- Cache privacy.
- Interaction data retention.

The Attributes docs note that Rock v17 increased attribute-level security enforcement and v17.5 added a third parameter to bypass attribute-level security checks when appropriate ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)). Do not bypass security in Roku templates just to make a page render. If a page needs restricted data, verify the intended access model.

The Lava Commands docs warn that enabled commands can bypass built-in security and business logic ([Lava Commands](https://community.rockrms.com/lava/commands)). SQL and remote Lava are especially sensitive. The SQL command docs warn about injection risk when Lava variables are inserted into SQL and explain SQL parameters ([SQL](https://community.rockrms.com/lava/commands/sql-commands)). Remote Lava docs warn against exposing endpoint/API-key combinations in client-side code ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

### Media

Roku media playback should use direct supported media sources, not YouTube ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). If media is stored in Rock Media Elements, verify the resolved URL, file type, authorization requirements, CDN behavior, and watch-map interaction records.

### TV Apps

The source pack indicates Rock previously introduced Apple TV support, and Roku support followed to extend digital ministry to Roku devices ([Roku Docs](https://community.rockrms.com/developer/roku-docs)). Do not assume Apple TV implementation details transfer to Roku. The Focus Group docs explicitly call out that Roku focus management differs from Apple TV expectations ([Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

## 13. Administration And Operational Guardrails

### Version Gate

Confirm the Rock version before doing any Roku work. The official Roku Docs page states Roku was introduced in Rock v16.7 ([Roku Docs](https://community.rockrms.com/developer/roku-docs)). If the instance is earlier than v16.7, the feature may not exist. If the instance is much newer, verify whether docs or source have changed since the source pack.

### Environment Separation

Use separate development, staging, and production Roku applications where possible. A Roku app can expose production media, current-person data, and interaction writes. Testing with a production API key can pollute analytics or expose sensitive content. If the same Roku shell can point to different Rock environments, document the mapping.

### Secret Handling

API keys should be rotated and scoped. Do not place API keys in Lava comments, public repo files, screenshots, exported docs, or diagnostic labels. If a device is lost or a development app was shared broadly, rotate the key and verify the old key no longer works.

### Cache Policy

Cache policy is one of the highest-risk Roku app settings because TV apps often show personalized media progress, login state, recommendations, and campus-specific content. Use page-level cache settings and command-level cache controls intentionally ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

Guardrails:

- Public cache only for anonymous, non-sensitive, broadly shared content.
- Personal cache for user-specific content when supported.
- Private/no-store for sensitive screens.
- Short shared cache for high-change content.
- Cache busting during launch/debug.
- No public caching of pages that include `CurrentPerson`.

### Interaction Tracking

If Enable Page Views is on, page interactions are written ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Navigation commands can suppress page interaction writes ([Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)). Media commands can write or append watch interactions ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)).

Operational checks:

- Verify interactions are written only for meaningful screens.
- Exclude loading/redirect/utility pages where they would distort reports.
- Confirm retention duration.
- Confirm watch-map behavior for resume features.
- Check Rock exceptions if interaction writes fail.

### Lava Command Policy

Keep Lava command enablement narrow. The command picker source shows Rock exposes a list of Lava commands dynamically ([LavaCommandsPicker.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/LavaCommandsPicker.cs)). The Lava Commands docs explain commands must be enabled and can carry security risk ([Lava Commands](https://community.rockrms.com/lava/commands)).

For Roku pages:

- Prefer entity commands over raw SQL.
- Avoid SQL unless a measured need exists.
- Avoid remote Lava and webrequest commands unless reviewed.
- Do not enable write commands for display-only pages.
- Document every non-default command enabled for Roku templates.

### Content Governance

Roku app content should have ownership. Define who owns:

- Home page rows.
- Featured media.
- Series/episode metadata.
- Images/posters.
- Login copy.
- Personalized recommendations.
- Analytics review.
- Release testing.

A technical page can render correctly and still be operationally wrong if stale media, bad artwork, or incorrect audience targeting is used.

## 14. Developer, API, Lava, And Source-Code Landmarks

Use the following landmarks when investigating or extending Roku apps.

### Official Roku Docs

- Entry point: [Roku Docs](https://community.rockrms.com/developer/roku-docs)
- First app workflow: [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)
- Application settings: [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)
- Page settings: [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)
- Command overview: [Commands](https://community.rockrms.com/developer/roku-docs/commands)
- Navigation: [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)
- Media: [Media](https://community.rockrms.com/developer/roku-docs/commands/media)
- Utility: [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)
- Personal: [Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)
- Controls: [Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)
- Layout nodes: [Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes)
- RowList: [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)

### Rock Lava Docs

- Lava overview: [Lava](https://community.rockrms.com/lava)
- Command security: [Lava Commands](https://community.rockrms.com/lava/commands)
- Entity queries: [Entity](https://community.rockrms.com/lava/commands/entity-commands)
- Attributes: [Attributes](https://community.rockrms.com/lava/filters/attribute-filters)
- Cache: [Cache](https://community.rockrms.com/lava/commands/cache-commands)
- SQL: [SQL](https://community.rockrms.com/lava/commands/sql-commands)
- Interactions: [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write)
- Content item interactions: [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)
- Intent interactions: [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)
- Personalization: [Personalize](https://community.rockrms.com/lava/commands/personalize-commands)
- Adaptive messages: [Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands)
- Remote Lava: [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)
- Lava API: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

### API Docs

Use the API docs for broader integration work and exact API version references ([API Documentation](https://community.rockrms.com/api-docs)).

### Source-Code Landmarks

The source pack includes these relevant source files:

- `Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs` for application save/security behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs)).
- `Rock/Model/CMS/LavaApplication/LavaApplicationService.cs` for application service behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplicationService.cs)).
- `Rock/Web/UI/Controls/Pickers/LavaCommandsPicker.cs` for Lava command picker behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/LavaCommandsPicker.cs)).

These are landmarks only. The source pack does not include enough source to document every Roku renderer, API endpoint, table, or shell behavior.

## 15. Reporting, Analytics, And Model Map

Roku analytics primarily involve page views and media interactions.

Application-level Enable Page Views controls whether page interactions are written ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Page View Retention Duration controls how long those interactions are retained. Navigation commands can suppress page interaction writes for specific page loads ([Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

Media interactions are more nuanced. The media docs explain watch-map behavior and how `rockInteractionGuid` and `rockWatchMap` affect resume and append behavior ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). Agents should verify actual `Interaction` records in the live database or Tools > Interactions when diagnosing resume or analytics issues.

Rock’s general Lava interaction commands provide additional context. `interactionwrite` can write a custom interaction with channel, component, operation, summary, related entity, campaign, source, medium, content, term, and data fields ([Interaction Write](https://community.rockrms.com/lava/commands/interaction-write)). `interactioncontentchannelitemwrite` writes content channel item interactions and documents limits such as operation length and summary length ([Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)). `interactionintentwrite` writes intent interactions for a defined interaction intent value ([Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).

A reporting model should answer:

- Which Roku application produced the interaction?
- Which page or media item was viewed?
- Was the viewer anonymous or authenticated?
- Which person alias is attached?
- Which content channel item or media element is related?
- Was the interaction a page view, play, resume, complete, or custom event?
- Is watch-map data present?
- Is campaign/source/medium populated?
- Are page interactions suppressed for utility screens?
- Are retention settings deleting expected history?

Model map caveat: the source pack does not include a complete model map for Roku application/page entities. For authoritative reporting, inspect the live schema and Rock model files for `LavaApplication`, Roku page models, interaction channel/component relationships, media element relationships, and any Defined Values used as channel type medium values.

## 16. Version And Release Caveats

Roku support was introduced in Rock v16.7 ([Roku Docs](https://community.rockrms.com/developer/roku-docs)). A secondary release commentary source also notes a new Roku TV app feature under v16.7 ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)). Treat v16.7 as the minimum feature gate from the provided sources.

Lava engine behavior matters. Rock v13 introduced Fluid as a newer Lava engine, and Rock documentation warns that DotLiquid support is ending with v17 ([About Lava Fluid](https://community.rockrms.com/lava/fluid), [Lava](https://community.rockrms.com/lava)). Roku templates with older Lava syntax should be tested under the actual Lava engine used by the target Rock version.

Attribute security changed around v17/v17.5. The Attributes docs note increased attribute security enforcement in v17 and a v17.5 parameter for bypassing attribute-level security checks when appropriate ([Attributes](https://community.rockrms.com/lava/filters/attribute-filters)). If a Roku page stopped showing attribute values after an upgrade, check attribute security before changing template logic.

Lava commands have version-specific availability. Examples from the source pack:

- Calendar Events command v12.0, with campus IDs v13.0 ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events)).
- Event Scheduled Instance command v12.0, with campus IDs v13.0 ([Event Scheduled Instance](https://community.rockrms.com/lava/commands/event-scheduled-instance)).
- Interaction Content Channel Item Write v11.0, campaign/source/medium/content/term v12.0 ([Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)).
- Interaction Intent Write v16.4 ([Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write)).
- Adaptive Message v17.0 ([Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands)).
- Set Culture v18.0 ([Set Culture](https://community.rockrms.com/lava/commands/setculture-commands)).
- Print ZPL v19.0, generally unrelated to Roku but relevant to command availability checks ([Print ZPL](https://community.rockrms.com/lava/commands/print-zpl)).

Roku focus caveat: the Focus Group docs say that as of 2024, focus management is not built into Roku applications in the way Apple TV developers may expect ([Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)). If newer Roku or Rock versions improve this, verify in current docs/source.

Media caveat: YouTube playback is not supported in Roku TV applications according to the Media docs ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)). Do not propose a YouTube URL as a direct Roku media source unless the platform documentation changes and the live app proves it.

## 17. Implementation Playbooks

### Playbook: Create A Minimal Roku Home Page

Follow the official [Roku documentation](https://community.rockrms.com/developer/roku-docs), [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), and [Lava Commands](https://community.rockrms.com/lava/commands) guidance. Verify API access, command enablement, rendered SceneGraph XML, initial focus, navigation, and exception logs in the target app before extending the page.

Goal: prove app connectivity, page rendering, focus, and navigation.

Steps:

1. Confirm Rock v16.7+.
2. Confirm Roku application exists and has API key.
3. Create a Roku page named Home.
4. Set conservative cache behavior while testing, such as no-store/private depending on available settings.
5. Add `Rock:Page` with `initialFocus`.
6. Add one `Rock:Button`.
7. Point the button to a second test page with `pushPage`.
8. Load on Roku device.
9. Verify initial focus and navigation.
10. Check Rock exceptions.

Template concept:

```xml
<Rock:Page initialFocus="nextPage">
  <Label text="Roku Test Home" />
  <Rock:Button
    id="nextPage"
    text="Open Test Page"
    rockCommand="pushPage"
    rockPageGuid="REPLACE-WITH-TEST-PAGE-GUID"
    rockPageShowLoading="true" />
</Rock:Page>
```

### Playbook: Build A Media Row

Goal: render media items in a RowList and play a selected item.

Steps:

1. Identify source entity: Media Elements, Content Channel Items, or custom records.
2. Query source data with Lava entity commands or other approved data access.
3. Produce row content nodes under a single content root.
4. Attach `playVideo` or detail-page navigation to each item.
5. Use direct MP4/HLS URLs, not YouTube.
6. Validate image URLs and media URLs from a Roku-accessible network.
7. Test playback and back behavior.
8. Verify interactions and watch maps if enabled.

Use `RowList` structure from the official RowList page as the source of truth ([RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)).

### Playbook: Add Campus Selection

Goal: let viewers choose a campus and carry it across pages.

Steps:

1. Decide context key, such as `Campus`.
2. Render campus choices as buttons or content nodes.
3. Use `rockCommand="setContext, pushPage"`.
4. Set `rockContextKey="Campus"` and `rockContextValue` to the campus GUID or ID.
5. On subsequent pages, read `Context.Campus` in Lava after verifying exact merge-field shape.
6. Use safe filtering. Do not inject context directly into SQL.
7. Add a “change campus” action that clears or replaces context.

Source basis: multiple commands and utility context commands ([Commands](https://community.rockrms.com/developer/roku-docs/commands), [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)).

### Playbook: Add Login

Goal: authenticate a viewer and show personalized content.

Steps:

1. Confirm application Authentication Page is configured.
2. Create login, success, and timeout Roku pages.
3. On the login page, include nodes with IDs `lgnQrPoster` and `lgnCodeLabel`.
4. Add a login button with `rockCommand="login"`.
5. Provide `rockLoginPageGuid`, `rockLoginTimeoutPageGuid`, and `rockLoginSuccessPageGuid`.
6. Decide timeout/check durations.
7. Keep `rockLoginClearNavigationStack` true unless there is a documented reason not to.
8. On success, render `CurrentPerson`-aware content.
9. Test anonymous, success, timeout, and logout paths.

Source basis: Personal command docs ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

### Playbook: Tune Caching

Goal: improve performance without leaking personalized content.

Steps:

1. Classify each page: anonymous catalog, shared detail, personalized detail, login, media progress, utility.
2. Use public/shared caching only for anonymous shared pages.
3. Use personal/private/no-store behavior for personalized pages.
4. Set short max ages during launch.
5. Test cache invalidation after editing a page.
6. Test with two users to confirm no cross-user data leak.
7. Inspect response headers if accessible.
8. Document final cache settings.

Source basis: page cacheability settings and navigation cache controls ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

## 18. Troubleshooting Decision Tree

### App Does Not Load

Check version first. If Rock is earlier than v16.7, Roku support is outside the documented minimum ([Roku Docs](https://community.rockrms.com/developer/roku-docs)).

Then check:

- Is the Roku development/application shell provisioned?
- Is the Rock URL reachable over HTTPS from the Roku device?
- Is the API key configured and active?
- Is the application pointing to the correct Rock environment?
- Is a firewall/CDN/WAF blocking requests?
- Are there Rock exceptions during app load?
- Has the app package been updated after configuration changes?

### Page Loads Blank

Check generated SceneGraph.

- Does Lava render valid XML?
- Does the page have a `Rock:Page` root?
- Does `initialFocus` reference a real node?
- Are dynamic values escaped?
- Are required fields missing?
- Is a Lava command disabled?
- Is the page cached with stale content?
- Does the Roku device log an XML or component error?

### Focus Is Broken

Use the focus layer.

- Does `Rock:Page initialFocus` point to a focusable node?
- Are IDs unique?
- Is the target node visible/enabled?
- Should sibling controls be wrapped in `Rock:FocusGroup`?
- Is `layoutDirection` set to match expected remote movement?
- Are nested focus groups trapping focus?
- Is the layout too complex?

Source basis: `Rock:Page` initialFocus and `Rock:FocusGroup` focus management ([Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page), [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

### Navigation Goes To The Wrong Page

Check command parameters.

- Is `rockCommand` spelled correctly?
- Is `rockPageGuid` the correct page GUID?
- Are query-string parameters valid?
- Are multiple commands ordered as expected?
- Is context from an earlier selection still set?
- Is `replacePage` used where `pushPage` was intended?
- Is a stale cached page rendering old GUIDs?

### Menu Does Not Update

Remember Show in Menu is not automatically used by the shell ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

Check:

- Which Lava builds the menu?
- Does the query filter by Show in Menu?
- Is the menu hard-coded?
- Is the page/application cache stale?
- Is the menu rendered for anonymous vs authenticated users differently?
- Are disabled Lava commands preventing menu queries?

### Login QR Does Not Show

Check application and page configuration.

- Is Authentication Page configured on the application?
- Does the login command run?
- Does the login page include `lgnQrPoster`?
- Does it include `lgnCodeLabel`?
- Is the authentication website page reachable externally?
- Is the timeout too short?
- Are server checks failing?
- Are API key permissions sufficient?

Source basis: Personal command docs ([Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

### Authenticated Content Does Not Personalize

Check current-person state.

- Did login complete?
- Is `CurrentPerson` available in the Roku page merge fields?
- Is the page using public cache?
- Is `rockPageCacheControl` personal/private where needed?
- Did the navigation stack clear after login?
- Are attributes blocked by security?
- Are entity commands running with expected security settings?

Source basis: page merge fields, navigation caching, attribute security ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Attributes](https://community.rockrms.com/lava/filters/attribute-filters)).

### Video Does Not Play

Check media source.

- Is the source YouTube? If yes, replace it; YouTube is not supported by the Roku TV app per docs ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)).
- Is the URL direct and publicly/device accessible?
- Is the format MP4 or HLS where expected?
- Is the certificate valid?
- Does the URL require cookies or browser auth?
- Is `rockVideoUrl` populated after Lava render?
- If using MediaElement GUID, does it resolve to playable media?
- Does Roku log a playback error?

### Resume Does Not Work

Check watch-map state.

- Is `rockWatchMap` present?
- Is `rockInteractionGuid` present when appending to an existing interaction?
- Is a new interaction being created instead of appending?
- Is the current person anonymous?
- Are interactions enabled?
- Does the prior interaction still exist after retention cleanup?

Source basis: Media command notes ([Media](https://community.rockrms.com/developer/roku-docs/commands/media)).

### Interactions Are Missing Or Excessive

Check analytics settings.

- Is Enable Page Views enabled?
- Is `rockPageSuppressInteraction` true?
- Are utility/loading pages writing interactions?
- Are media commands writing separate interactions?
- Is retention deleting older records?
- Are invalid person aliases causing exceptions?
- Are custom Lava interaction commands enabled and functioning?

Source basis: application page views, navigation suppression, Lava interaction commands ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write)).

## 19. Agent Task Recipes

### Recipe: Inventory Existing Roku App

1. Locate Roku/Lava application records.
2. Record application name, GUID/ID, API key presence, auth page, page-view setting, retention.
3. List pages with GUIDs, names, Show in Menu, cache settings.
4. Identify pages using `CurrentPerson`, `Context`, media commands, login, or SQL.
5. Identify enabled Lava commands.
6. Check recent exceptions.
7. Check recent interactions.
8. Produce a map of page links by scanning `rockPageGuid` references.
9. Flag public-cached personalized pages.
10. Flag YouTube media URLs.

### Recipe: Review A Roku Page For Safety

Inspect:

- XML validity after Lava render.
- `Rock:Page` root.
- `initialFocus`.
- `rockCommand` names.
- Page GUID references.
- Media URL sources.
- Cache settings.
- Lava command usage.
- Attribute security bypasses.
- SQL usage.
- Current-person data.
- Interaction suppression.

Report findings by severity: security/cache leaks first, broken rendering second, analytics inaccuracies third, maintainability last.

### Recipe: Convert A Static Media List To Dynamic RowList

1. Identify content source and required fields.
2. Use entity command or approved data source.
3. Build rows in Lava.
4. Render one RowList content root.
5. Use `Rock:ContentNode` for rows/items.
6. Attach `playVideo` or `pushPage`.
7. Escape dynamic XML attribute values.
8. Set a conservative cache policy.
9. Test focus and playback.
10. Verify interactions.

### Recipe: Diagnose A Cache Leak

1. Load personalized page as User A.
2. Record rendered identifying content.
3. Sign out or use separate device/session as User B.
4. Load same page.
5. If User A content appears, inspect page Cacheability Type, Max Age, Max Shared Age, command-level `rockPageCacheControl`, CDN cache key, and whether the URL varies by person.
6. Switch to private/no-store or personal cache behavior.
7. Purge shared cache.
8. Retest with both users.

### Recipe: Add A Safe Diagnostic Page

Create a development-only Roku page that shows non-sensitive state:

- App/environment label.
- Whether `CurrentPerson` is present.
- Selected context keys.
- Current time.
- A button to test navigation.
- A button to clear context.

Do not show API keys, tokens, person IDs, email addresses, or sensitive attributes. Remove or lock down the page before production launch.

### Recipe: Validate Post-Upgrade Roku Behavior

After a Rock upgrade:

1. Confirm Roku pages render.
2. Confirm Lava engine behavior.
3. Check attribute access changes.
4. Check enabled Lava commands.
5. Verify login QR flow.
6. Verify media playback.
7. Verify interactions and watch maps.
8. Verify cache behavior.
9. Review release notes for Roku, Lava, API, CMS, media, and security changes.
10. Update internal docs with changed behavior.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `16`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Rock Roku pages display custom Lava-driven content as part of the application and render SceneGraph-oriented output rather than normal Rock CMS HTML. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| official | behavior | In Rock Roku layouts, a FocusGroup arranges its child views horizontally or vertically and automatically moves focus left/right for horizontal groups or up/down for vertical groups. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| official | behavior | For Roku media playback, supplying a prior watch map sets the resume position; including its interaction GUID also appends progress to that interaction, while omitting the GUID creates a new interaction with a new watch map beginning from the resumed position. | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| official | configuration | A Rock Roku application includes configuration such as page-view tracking, page-view retention duration, and API key settings, so Roku troubleshooting should start with the application record before page Lava. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| official | configuration | A Rock Roku application can reference a website authentication page that supports remote authentication within the TV application. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| official | configuration | Roku page caching can be configured as public, application-private, revalidated on every load, or disabled; separate maximum-age settings control application and shared-cache retention. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| official | implementation_pattern | When selecting SceneGraph layout elements for a Rock Roku application, account for the fact that most Roku layouts lack default item templates and prefer built-in elements where possible to avoid custom BrightScript components. | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes) |
| official | implementation_pattern | A Rock Roku page's SceneGraph content should use `Rock:Page` as its outermost component so the page can define which content receives initial focus. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| official | implementation_pattern | Roku commands are executed by setting a rockCommand and command-specific parameters on supported controls, and multiple commands can be chained by separating command names with commas. | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| official | implementation_pattern | Rock Roku applications use Roku's SceneGraph XML language and are composed primarily from built-in SceneGraph components, supplemented by Rock-provided custom components. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| official | operational_guidance | Beginning Roku development with Rock requires contacting the Rock Core team to obtain a development application setup. | [source](https://community.rockrms.com/developer/roku-docs) |
| official | recipe | Starting Roku development with Rock requires requesting a development application from the Rock Core team through the designated request form; the team then provides setup instructions. | [source](https://community.rockrms.com/developer/roku-docs/getting-started) |
| More |  | 4 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `1`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Dashboard Design Part 1 Transcript Insight](https://www.triumph.tech/resources/dashboard-design-part-1) | approved_for_public_distillation | 3 | media-insight:22ee135c5240caf2 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

### Release Notes And Community Examples

Use Rock release notes to verify the installed-version boundary before assuming a Roku app setting, page rendering behavior, Lava command surface, media command, cache behavior, or security rule exists in the target instance ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Roku documentation has explicit version framing, so release notes and live Rock version should be checked before relying on source snippets from `develop`.

Community examples and Q&A are useful as examples only. They can reveal real implementation problems around API calls, Lava-rendered XML, login behavior, media playback, or cache behavior, but they are not the source of truth for Roku app behavior. Use them after official Roku docs, release notes, source-code landmarks, and live instance inspection have already established the authoritative path ([Developing for Rock Q&A](https://community.rockrms.com/ask/developing)).

Primary Roku sources:

- [Roku Docs](https://community.rockrms.com/developer/roku-docs): entry point, platform purpose, v16.7 introduction.
- [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started): app/page mental model and development app request path.
- [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications): application settings.
- [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages): page settings, SceneGraph content, cacheability, merge-field references.
- [Commands](https://community.rockrms.com/developer/roku-docs/commands): command model and multiple-command syntax.
- [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation): page stack commands and navigation cache/interaction parameters.
- [Media](https://community.rockrms.com/developer/roku-docs/commands/media): video/audio playback, YouTube caveat, media element/watch-map behavior.
- [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility): context commands.
- [Personal](https://community.rockrms.com/developer/roku-docs/commands/personal): login flow, login pages, timeout/check durations, QR/code IDs.
- [Controls](https://community.rockrms.com/developer/roku-docs/resources/controls): custom Rock SceneGraph controls.
- [Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button): Rock command-aware button.
- [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node): Rock command-aware content node.
- [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group): directional focus helper.
- [Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page): page control and initial focus.
- [Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes): layout selection caution.
- [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist): RowList parameters and content-node structure.
- [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources): Roku SceneGraph reference and samples.
- [Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks): simple-layout guidance.
- [Useful Links](https://community.rockrms.com/developer/roku-docs/resources/useful-links): feedback and issue/community pointers.

Related Rock sources:

- [Lava](https://community.rockrms.com/lava): Lava basics and engine/version caveats.
- [Lava Commands](https://community.rockrms.com/lava/commands): command enablement and security.
- [Entity](https://community.rockrms.com/lava/commands/entity-commands): data access through Lava.
- [Attributes](https://community.rockrms.com/lava/filters/attribute-filters): attribute access and security caveats.
- [Cache](https://community.rockrms.com/lava/commands/cache-commands): Lava cache behavior.
- [SQL](https://community.rockrms.com/lava/commands/sql-commands): SQL command risk and parameters.
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api): Lava-generated API surfaces and webhook caution.
- [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava): remote Lava endpoint and API-key exposure risk.
- [API Documentation](https://community.rockrms.com/api-docs): Rock API v1/v2 orientation.
- [Interaction Write](https://community.rockrms.com/lava/commands/interaction-write), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), and [Interaction Intent Write](https://community.rockrms.com/lava/commands/interaction-intent-write): analytics-writing commands.
- [Personalize](https://community.rockrms.com/lava/commands/personalize-commands) and [Adaptive Message](https://community.rockrms.com/lava/commands/adaptivemessage-commands): personalization options.
- [About Lava Fluid](https://community.rockrms.com/lava/fluid): Fluid engine transition.

Source-code landmarks:

- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock): official source repository record.
- [LavaApplication.SaveHook.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplication.SaveHook.cs): application save/security landmark.
- [LavaApplicationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CMS/LavaApplication/LavaApplicationService.cs): application service landmark.
- [LavaCommandsPicker.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/LavaCommandsPicker.cs): Lava command picker landmark.

Dependency notes:

- Depends on **api-integrations** for API key, Rock API, route, and external access questions.
- Depends on **lava** for template syntax, commands, filters, security, caching, and data access.
- Depends on **cms** for content channels, pages, personalization, application/page governance, and rendered content.
- Depends on **security** for API keys, auth pages, command enablement, entity/attribute access, and cache privacy.
- Depends on **media** for Media Elements, playable URLs, HLS/MP4 handling, posters, captions, and watch interactions.
- Depends on **tv-apps** for Roku device behavior, SceneGraph, focus, app packaging, and TV UX validation.

Final review requirement: this guide is draft material. Before treating it as authoritative for a production Rock instance, verify exact entity names, database columns, admin routes, endpoint routes, current source behavior, and device behavior in the target Rock version.
