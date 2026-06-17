---
id: authored-tv-apps
title: TV Apps
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# TV Apps

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [TV Apps index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock TV Apps let a Rock instance serve living-room applications for Apple TV and Roku by combining Rock-managed application records, Rock-managed page records, Lava-rendered XML, platform-specific shells, media commands, remote authentication, and interaction tracking. Treat a TV app as a specialized CMS surface: the shell runs on the device, but the page content, navigation targets, media URLs, personalization, context, and some operational settings come from Rock.

The two supported platform families are similar in concept but different in markup and runtime behavior:

- Apple TV uses TVML and the Rock Apple TV shell. Rock’s Apple TV documentation states that Apple TV support requires Rock v14 or later and is designed around TVML applications linked to Rock ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- Roku uses Roku SceneGraph XML and Rock’s Roku shell. Roku support was introduced in Rock v16.7, and the documentation describes a Rock-managed Roku application with Lava-powered SceneGraph pages ([Roku Docs](https://community.rockrms.com/developer/roku-docs), [GitHub Spotlight v16.7 note](https://www.triumph.tech/resources/github-spotlight-1042024)).

For an agent doing real Rock work, the most important operational model is:

1. Identify the TV application record.
2. Confirm its API key, page-view tracking settings, and authentication page.
3. Inspect the start/root page and every page GUID used by commands.
4. Validate the page markup as TVML or SceneGraph, not HTML.
5. Confirm the Lava merge fields and commands used by the page.
6. Confirm media URLs are directly playable by the platform.
7. Confirm remote authentication works through `RemoteAuthenticationSession`, the Remote Authentication block, and the selected site.
8. Confirm caching is appropriate for personalized content.
9. Confirm interaction records are being written only when desired.

Do not treat TV Apps as mobile apps, web pages, or generic API endpoints. They overlap with all three, but they have their own device shells, command attributes, XML dialects, caching behavior, media limitations, and remote-auth flow. Apple TV pages are TVML documents; Roku pages are SceneGraph content whose outer page component should be `Rock:Page` for initial focus behavior ([Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages), [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

## 2. Scope And Terminology

This guide covers Rock-powered TV applications for Apple TV and Roku. It focuses on configuration, data model, navigation, page rendering, Lava, styling, controls, authentication, media playback, operational checks, troubleshooting, and agent task recipes. It does not replace Apple’s TVML documentation, Roku’s SceneGraph reference, Rock’s REST API documentation, or source-code review. It tells agents how to connect those sources into an operational Rock mental model.

Key terms:

- **TV App**: A Rock-managed application configuration used by a platform shell. In Apple TV documentation it is described as a Rock Apple TV app builder/application; in Roku documentation it is a Roku application similar to a site with multiple pages ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).
- **Shell**: The compiled Apple TV or Roku application installed on the device. It contacts Rock, loads app/page content, executes commands, handles media playback, and manages device-specific behavior.
- **TVML**: Apple’s XML-like markup language for tvOS template-based interfaces. Rock Apple TV pages must render valid TVML ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- **SceneGraph**: Roku’s XML-based UI language. Rock Roku pages render SceneGraph content, with Rock-provided custom components such as `Rock:Page`, `Rock:Button`, `Rock:ContentNode`, and `Rock:FocusGroup` ([Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started), [Roku Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)).
- **Lava**: Rock’s templating language. TV pages use Lava to produce TVML or SceneGraph dynamically. Lava can also produce custom XML APIs, but Lava webhooks have security exposure that must be handled carefully ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).
- **Remote Authentication**: A code-based sign-in pattern where the TV device displays or passes a verification code, and a web page with Rock’s Remote Authentication block authorizes the session. Source code landmarks include `RemoteAuthenticationSession`, `RemoteAuthenticationSessionService`, and `RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs` ([RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthentication block code](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)).
- **Context**: App-level state, often Campus, that can be set by commands and read by Lava. Apple TV documentation says contexts are stored across viewing sessions; Roku utility documentation says Roku context is set for the lifetime of the app until closed, so agents must verify platform-specific persistence in the live instance before relying on it ([Apple TV Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context), [Roku Utility Commands](https://community.rockrms.com/developer/roku-docs/commands/utility)).
- **Interaction/Page View**: Usage tracking written when page views or media interactions are enabled and not suppressed. Application settings expose page-view tracking and retention, while navigation/media commands can affect interaction behavior ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).

## 3. TV Apps Mental Model

A Rock TV app is best understood as a remote-rendered, device-native content surface.

The device shell is not a browser. It does not render Rock CMS HTML. It expects platform markup. Apple TV expects TVML templates and Apple TV styling rules; Roku expects SceneGraph nodes and Roku focus/navigation patterns. Rock contributes the server-side CMS record, Lava merge fields, API connection, commands, page cache metadata, media playback parameters, interaction tracking, and remote-auth infrastructure.

The normal flow is:

1. The shell launches with compiled or demo configuration.
2. The shell connects to Rock using an API key and application identity.
3. The shell loads a configured page, often a start screen or root page.
4. Rock renders that page’s TVML or SceneGraph using Lava.
5. The shell parses the XML and shows device-native UI.
6. User focus/selection triggers commands embedded in markup.
7. Commands navigate to another Rock TV page, play media, set/clear context, log in/out, or perform utility behavior.
8. Media playback and page views may write interactions.
9. Personalized pages must consider login state, person-specific cache keys, and navigation-stack cleanup after login/logout.

The mental model differs from web CMS in four important ways.

First, markup validity is unforgiving. A web browser may tolerate malformed HTML. A TV shell parsing TVML or SceneGraph may fail, show a blank screen, display an error shell, or fall back to a previous cached page. Agents should inspect rendered markup, not just saved Lava.

Second, focus is part of the interface contract. Apple TV generally provides more built-in focus behavior. Roku requires explicit focus planning, and Rock provides `Rock:FocusGroup` to handle common vertical/horizontal focus flows because Roku applications do not provide the same automatic focus management expected from Apple TV ([Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

Third, navigation is command-driven. Pages are linked by platform controls that include command attributes. On Roku, commands are executed by setting `rockCommand` and command-specific fields on `Rock:Button` or `Rock:ContentNode`; multiple commands can be comma-separated for paired actions such as setting context and pushing a page ([Roku Commands](https://community.rockrms.com/developer/roku-docs/commands)). Apple TV uses analogous Rock command attributes on TVML elements for personal, navigation, media, utility, and demo behaviors ([Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript)).

Fourth, TV app personalization is high risk for caching mistakes. A public cached page should not contain person-specific data. Roku navigation supports `rockPageCacheControl` values such as public and personal caching, and Roku pages expose cacheability settings such as Public, Private, No-Cache, and No-Store ([Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)). Apple TV pages also expose cacheability concepts in the page editor according to the adding-content walkthrough ([Apple TV Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)).

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. **Rock source code and model definitions** for entity fields, method behavior, generated API routes, and block implementation. Examples: `RemoteAuthenticationSession`, `RemoteAuthenticationSessionService`, `RemoteAuthenticationSessionExtensions`, `RemoteAuthentication.ascx.cs`, `AppleTvApplicationSettings`, and `RokuTvApplicationSettings` ([RemoteAuthenticationSession source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthenticationSessionService source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs), [AppleTvApplicationSettings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/AppleTvApplicationSettings.cs), [RokuTvApplicationSettings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/RokuTvApplicationSettings.cs)).
2. **Official Rock developer docs** for supported configuration fields, command semantics, platform guidance, and version notes ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Roku Docs](https://community.rockrms.com/developer/roku-docs)).
3. **Rock API and Lava docs** for integration surfaces, webhooks, Lava command behavior, and security warnings ([Rock API Documentation](https://community.rockrms.com/api-docs), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).
4. **Release notes and ecosystem records** for version caveats, such as Roku being added in v16.7 ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)).
5. **Platform documentation** for TVML and SceneGraph behavior. Rock’s docs explicitly point Apple TV builders to Apple TVML documentation and Roku builders to Roku SceneGraph reference and samples ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)).
6. **Community examples and recipes** only after official and source-code records have been exhausted.

When this guide says “verify in the live instance,” inspect the actual Rock instance before concluding behavior. TV app records, page GUIDs, API keys, auth pages, cache settings, block attributes, routes, security, and markup can vary by organization and by Rock version.

For live verification, agents should inspect:

- Admin Tools > CMS Configuration > Apple TV Apps or the equivalent TV app administration area available in the target Rock version.
- Admin Tools > CMS Configuration > Roku Apps or the equivalent Roku application administration area available in the target Rock version.
- The exact application record’s settings.
- The exact page record’s rendered content, cacheability, max age, max shared age, and security.
- Any Remote Authentication page and block attributes.
- API key person/security configuration.
- Interactions created during test navigation and playback.
- The source code for the deployed Rock version if behavior differs from current `develop`.

## 5. Core Configuration And Data Model

### Apple TV Application Configuration

The Apple TV application setup flow starts in Rock under Admin Tools > CMS Configuration > Apple TV Apps according to the creating-app documentation ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). The application fields called out by the source pack include:

- **Name**: Private Rock-side application name. It does not have to match the App Store name.
- **Description**: Optional internal description.
- **Application Styles**: Global style definitions available across the application.
- **Enable Page Views**: Whether page interaction data should be recorded.
- **API Key**: The API key used by the TV shell to access Rock.
- **Page View Retention Period**: The number of days to retain page-view interaction data.
- **Application Script**: Source code exposes `ApplicationScript` on `AppleTvApplicationSettings`; the Apple docs warn that TVMLKit JS docs are generally less useful because builders should not normally modify the application JavaScript ([AppleTvApplicationSettings source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/AppleTvApplicationSettings.cs), [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).

The Apple settings class in source code includes `ApplicationScript`, `ApplicationStyles`, and API key-related state; verify exact property names and persisted attribute mapping against the deployed Rock version before building automation that updates application records directly ([AppleTvApplicationSettings source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/AppleTvApplicationSettings.cs)).

### Roku Application Configuration

The Roku application page describes a Rock-managed application used to manage TV content ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Its settings include:

- **Enable Page Views**: Whether page interactions should be written for application usage.
- **Page View Retention Duration**: Days to retain written page interactions.
- **API Key**: API key used to securely connect the Roku application.
- **Authentication Page**: A website authentication page used for remote authentication in the TV application.

Source code for `RokuTvApplicationSettings` includes `ApiKeyId` and `RockComponents` ([RokuTvApplicationSettings source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/RokuTvApplicationSettings.cs)). If an agent is reconciling a Roku app record from the database, verify where these values are stored in the current Rock version: site attributes, application settings JSON, or another TV-specific table/attribute surface.

### TV Page Configuration

Apple TV pages must produce valid TVML. Roku pages must produce valid SceneGraph content.

Apple TV page documentation lists Lava merge fields available to page content, including `CurrentPerson`, `Context`, `Campuses`, `SiteStyles`, `CurrentPage`, `CurrentPersonCanEdit`, `CurrentPersonCanAdministrate`, `PageParameter`, `TvShellVersion`, and `DeviceData` ([Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

Roku page documentation lists these configuration options ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)):

- **Show in Menu**: Available for Lava-built menus. The Roku shell does not use it automatically.
- **Scenegraph Content**: SceneGraph content to display. Each page should use `Rock:Page` as the outer-most component to set initial focus.
- **Cacheability Type**: Public, Private, No-Cache, or No-Store.
- **Max Age**: Maximum cache duration.
- **Max Shared Age**: Maximum duration in shared caches.

The Apple adding-content walkthrough includes page creation fields such as page name, description, TVML, and cacheability ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)). Verify the live page editor for exact field labels because Rock UI labels and storage can shift by version.

### Remote Authentication Data Model

Remote authentication is backed by `RemoteAuthenticationSession`, which source code maps to the `RemoteAuthenticationSession` table and connects optionally to `Site` and `AuthorizedPersonAlias` ([RemoteAuthenticationSession source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)). The migration creates the table with fields including `Code`, `AuthorizedPersonAliasId`, `SiteId`, and standard Rock model fields ([AddRemoteAuthenticationSession migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs)).

The service behavior in source is operationally important:

- A new session is started with client IP, throttle settings, device unique identifier, code issue date, and code lifetime.
- Codes are generated with a fixed length in source (`GeneratedCodeLength = 6` in the excerpted service).
- Verification looks for an active session matching the unique identifier and code, ordered by most recent session start.
- Source extensions filter sessions by code lifetime, current active status, and sessions created today for throttling/selection behavior ([RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs), [RemoteAuthenticationSessionExtensions](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)).

The Remote Authentication block exposes a site attribute, Lava-configurable header/footer/success content, and a code expiration duration according to source snippets ([RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)). Agents should inspect the block instance on the live authentication page for the selected site, code expiration duration, and message Lava.

## 6. Primary Entities And Relationships

### Application To Page

A TV application owns or references TV pages. The shell loads pages by GUID through commands. For Roku, navigation commands use `rockPageGuid` and can include optional query-string parameters ([Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)). For Apple TV, TV pages expose `PageParameter`, `CurrentPage`, and TV shell/device merge fields, implying the page render pipeline includes page identity, route/query context, and shell/device state ([Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

Operational implication: when troubleshooting a missing page, do not search by title alone. Extract the GUID from the command attribute, locate that page in Rock, verify it belongs to or is reachable by the TV app, and render it with the same parameters.

### Application To API Key

Both Apple TV and Roku application settings include API key configuration ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). The API key is not a decorative setting; it is part of the connection contract between the shell and Rock. Agents should verify:

- The API key exists and is active.
- The API key is assigned to an appropriate person/security context.
- The API key’s permissions are no broader than needed.
- The API key is the one compiled into or configured by the shell/demo app.
- The app is using HTTPS endpoints.
- API key rotation has been coordinated with app deployment or demo settings.

Rock’s API docs identify API v1 as legacy and API v2 as newer, but TV shell behavior must be verified from the deployed Rock TV code and shell implementation rather than assumed from general API docs ([Rock API Documentation](https://community.rockrms.com/api-docs)).

### Application To Authentication Page

Roku has an explicit **Authentication Page** application setting. The docs describe it as a website authentication page used to remotely authenticate into the TV application ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Apple TV sign-in setup instructs administrators to create an external page, add the Remote Authentication block, configure the site that represents the TV app, and use that page URL or a route for the sign-in experience ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)).

Operational implication: authentication failure may be caused by any of these, not just the login button:

- The TV app has no login/authentication page configured.
- The Remote Authentication block points to the wrong site.
- The device is generating a session for one site while the web page verifies another.
- The verification code expired.
- The user is not logged into the website page.
- The person’s authentication component does not allow the needed remote authentication method.
- The API key does not permit the shell to create/check sessions.
- Cache or navigation stack exposes stale login pages after successful login.

### RemoteAuthenticationSession To Person And Site

`RemoteAuthenticationSession` has optional relationships to `Site` and `AuthorizedPersonAlias` in source configuration ([RemoteAuthenticationSession source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)). During a successful flow, the session begins unauthenticated and later records the person alias that authorized it. Verify the exact live fields when diagnosing historical login attempts: `Code`, `DeviceUniqueIdentifier`, `ClientIpAddress`, `AuthenticationIpAddress`, `SessionStartDateTime`, `SessionEndDateTime`, `AuthorizedPersonAliasId`, `SiteId`, and standard Rock audit fields are the fields to look for based on source snippets and generated client models ([RemoteAuthenticationSession client model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Client/CodeGenerated/RemoteAuthenticationSession.cs)).

### Page To Interaction

Page views and media watch progress can write interactions. Application settings decide whether page views are enabled and how long to retain them. Navigation commands can suppress interactions, and media commands use interaction GUID/watch-map fields for resume and progress behavior ([Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media), [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).

When analytics look wrong, inspect both settings and command-level suppression. A healthy page render does not guarantee interaction writes are enabled.

## 7. Common TV Apps Workflows

### Create A New Apple TV App

1. Confirm Rock version is v14 or later because the Apple TV docs state that Apple TV functionality requires Rock v14+ ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
2. Create the application under Admin Tools > CMS Configuration > Apple TV Apps ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)).
3. Set the internal name and description.
4. Configure global application styles if the app has shared colors, text styles, or template-specific rules.
5. Decide whether to enable page views and set retention.
6. Select or create the API key used by the shell.
7. Create the start/root page using valid TVML.
8. Add navigation commands to push or replace pages.
9. Add media commands for video/audio playback.
10. Add remote-auth pages if personalization is needed.
11. Test with the Rock Core/demo app and demo key if applicable ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app)).
12. Validate launch image, app icons, top shelf images, and parallax assets before App Store submission ([App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons), [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image), [Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image), [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)).

### Create A New Roku App

1. Confirm Rock is v16.7 or later for Roku support ([Roku Docs](https://community.rockrms.com/developer/roku-docs), [GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-1042024)).
2. Follow the Roku getting-started process and request a development application from the Core team as documented ([Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)).
3. Create/configure the Roku application in Rock.
4. Set page-view tracking and retention.
5. Select the API key.
6. Set the authentication page if login is needed.
7. Create the root page with `Rock:Page` as the outer component.
8. Use SceneGraph components and Rock-provided controls for commands.
9. Use `Rock:FocusGroup` where directional focus would otherwise be ambiguous.
10. Use `RowList` for rows of media/content, especially for scrollable content shelves ([RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist), [Roku Tips](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks)).
11. Test on a Roku device or development shell with real network conditions.
12. Confirm remote auth and media playback before production release.

### Add A Menu Or Navigation Surface

For Apple TV, choose a TVML template that naturally supports the desired navigation. The adding-content walkthrough starts with a main template and menu bar for the start screen ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)). For Roku, `Show in Menu` is metadata only; the shell does not consume it automatically, so create menu markup in Lava by querying or otherwise listing the pages you want to expose ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

Agent checks:

- Every menu item has a valid target page GUID.
- Personalized targets use personal/private/no-store caching.
- Context-changing menu items set context before navigation if needed.
- Default focus points at the first useful item.
- Back navigation makes sense after login/logout and after deep links.

### Add Media Playback

Apple TV and Roku both expose media commands for video/audio and both document that YouTube content cannot be played directly in TV applications ([Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media)). Agents should verify the media URL is a direct stream/file URL supported by the target platform, not just a browser page.

For resume behavior, both Apple TV and Roku media docs describe `rockWatchMap` and `rockInteractionGuid` behavior. Use an existing interaction GUID plus watch map to append progress to an existing interaction; use watch map without an interaction GUID only when you want resume positioning while allowing a new interaction to be written ([Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media)).

### Add Remote Sign-In

Use a Remote Authentication page rather than forcing users through a TV keyboard. Apple’s sign-in walkthrough specifically positions remote sign-in as a way to authenticate from a mobile device or computer ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)). Roku’s personal login command requires an application login page before using the command because that setting configures the QR code ([Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)).

Agent checks:

- TV application has an authentication/login page configured.
- Website page exists, has a route, and is reachable publicly if users need it from phones.
- Remote Authentication block is configured to the TV app’s site.
- Code expiration duration is appropriate.
- Login success page and timeout page GUIDs are valid.
- Navigation stack is cleared after successful login if the app could otherwise back-navigate to anonymous content.
- Logout behavior clears person state and updates UI.

## 8. Apple TV Deep Dive

### Apple TV Platform Contract

Rock Apple TV is a TVML-based extension of Rock. The app builder lets administrators create and test TVML templates without custom native programming, but the runtime is still Apple TVML, not HTML ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs), [Building Your First App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app)).

Agents should keep three constraints in mind:

- Do not treat TVML as HTML. The Apple TV tips page explicitly warns that TVML and its styling are not HTML/CSS even when they look familiar ([Apple TV Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)).
- Avoid custom behavior outside documented templates unless verified on a device. The templates page warns that custom work outside Div Template can be tricky because each template processes elements differently ([Apple TV Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)).
- Do not assume JavaScript is an app-builder surface. The Apple TV docs point to TVMLKit JS for context but say builders generally should not update the app JavaScript ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).

### Apple TV Pages And Merge Fields

Apple TV page content must render valid TVML. The important merge fields are:

- `CurrentPerson`
- `Context`
- `Campuses`
- `SiteStyles`
- `CurrentPage`
- `CurrentPersonCanEdit`
- `CurrentPersonCanAdministrate`
- `PageParameter`
- `TvShellVersion`
- `DeviceData`

Use these fields to render personalized UI, campus-specific media, admin affordances, version-specific markup, and device-specific diagnostics ([Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

Operational pattern for safe Lava:

```liquid
{% assign campus = Context.Campus %}
{% if CurrentPerson %}
  {% assign greetingName = CurrentPerson.NickName %}
{% else %}
  {% assign greetingName = 'Guest' %}
{% endif %}
```

Then use those values inside valid TVML. Do not emit raw HTML into a TVML document.

### Apple TV Templates

Apple TV templates are opinionated. Use the template that matches the content shape rather than forcing a web layout into TVML.

Common choices:

- **Main/Menu Bar Template**: Start screens, top-level navigation, and app home experiences. The adding-content walkthrough uses a main template and menu bar pattern for a start screen ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)).
- **Catalog Template**: Categories on one side and related content on the other; useful for series, ministries, campuses, or content groupings ([Catalog Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/catalog-template)).
- **List Template**: Lists of items inside a category, such as favorite messages or messages in a series ([List Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/list-template)).
- **Product Template**: Detail page for a message or media item, including metadata, related content, speakers, or supporting material ([Product Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-template)).
- **Showcase Template**: Row of images with associated descriptions and focus enlargement ([Showcase Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/showcase-template)).
- **One Up Template**: Full-screen image browsing with left/right navigation and caption behavior ([One Up Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/one-up-template)).
- **Alert Template**: Required user messages, sign-in prompts, timeout notices, or critical state ([Alert Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/alert-template)).

If a requested design cannot be built reliably in TVML, state that plainly and propose a platform-fitting template. Apple’s reference gallery is useful for inspiration, but the docs warn that some reference layouts may require native implementation rather than TVML alone ([Apple TV References](https://community.rockrms.com/developer/apple-tv-docs/styling/references)).

### Apple TV Commands

Apple TV docs group commands into demo, personal, navigation, media, and utility categories ([Apple TV JavaScript](https://community.rockrms.com/developer/apple-tv-docs/javascript)). The agent’s job is usually not to edit JavaScript; it is to place supported command attributes in valid TVML controls and confirm the shell handles them.

Important command families:

- **Personal commands**: login/logout. Login requires configured login page GUIDs for displaying login information, timeout behavior, and success behavior ([Apple TV Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)).
- **Media commands**: play video/audio, with watch-map and interaction behavior ([Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).
- **Demo commands**: show/update/clear demo settings when the app is compiled with demo support ([Apple TV Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)).
- **Context/utility commands**: set and clear context, especially Campus ([Apple TV Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context)).

### Apple TV Testing And Demo Key

The Apple TV testing doc describes requesting a demo key and using the Rock Core app on Apple TV to point the demo shell at a Rock application ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app)). For agents, this means local Rock changes can often be tested before App Store/TestFlight publication, but only if the demo settings are correct.

Testing checklist:

- Confirm the demo key points at the intended Rock instance.
- Restart the app after changing demo settings if the instructions require it.
- Clear demo settings before testing compiled production configuration.
- Test anonymous home, login page, successful login, timeout, logout, media playback, and error handling.
- Test light and dark themes if the app uses theme-dependent styles.
- Test with actual media URLs, not browser preview URLs.

### Apple TV Application Images

Apple TV app assets are not cosmetic afterthoughts; they affect launch, App Store, top shelf, and focus behavior.

From the Apple TV application image docs:

- App icons use layered assets for parallax; in-app icon sizes include 400x240 and 800x480, and the App Store icon uses 1280x768 ([App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons)).
- Top shelf images include wide and standard sizes; wide sizes include 2320x720 and 4640x1440, while standard top shelf includes 1920x720 and 3840x1440 ([Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image)).
- Launch images are static and include 1920x1080 and 3840x2160 sizes ([Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image)).
- Parallax images are layered images used for focus depth and motion ([Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)).

Agents should verify exact asset requirements against Apple’s current tvOS submission docs before final publication because platform submission rules can change.

## 9. Roku Deep Dive

### Roku Platform Contract

Roku in Rock is a SceneGraph-driven TV app surface introduced in v16.7 ([Roku Docs](https://community.rockrms.com/developer/roku-docs)). Roku development in Rock is similar to building a website in that you create an application and multiple Lava-driven pages, but the markup language is SceneGraph XML rather than HTML ([Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)).

The Roku docs direct developers to Roku’s SceneGraph reference and samples for built-in components ([Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)). Use Rock docs for Rock-specific controls and commands; use Roku docs for native SceneGraph node behavior.

### Roku Pages

A Roku page is a Rock page-like unit that renders SceneGraph content. Page settings include `Show in Menu`, `Scenegraph Content`, `Cacheability Type`, `Max Age`, and `Max Shared Age` ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).

The page content should have `Rock:Page` as the outer-most component. This matters because `Rock:Page` provides initial focus support. The `Rock:Page` control extends Roku’s `Group` and exposes an `initialFocus` field whose value is the ID of the item that should receive focus when the page appears ([Roku Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)).

A practical pattern:

```xml
<Rock:Page initialFocus="watchLatest">
  <Label text="Messages" />
  <Rock:Button
    id="watchLatest"
    text="Watch Latest"
    rockCommand="pushPage"
    rockPageGuid="00000000-0000-0000-0000-000000000000" />
</Rock:Page>
```

Replace the GUID with a real page GUID and verify the attribute casing expected by the deployed shell.

### Roku Commands

Roku commands execute through `rockCommand` on applicable Rock controls, especially `Rock:ContentNode` and `Rock:Button` ([Roku Commands](https://community.rockrms.com/developer/roku-docs/commands), [Roku Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button), [Roku Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)).

Command families:

- **Navigation**: `pushPage`, `replacePage`, `popPage`, `clearNavigationStack` ([Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).
- **Media**: video/audio playback and interaction/watch-map behavior ([Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media)).
- **Utility**: `setContext`, `clearContext` ([Roku Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)).
- **Personal**: login/logout-related commands ([Roku Personal](https://community.rockrms.com/developer/roku-docs/commands/personal)).

Roku supports multiple commands by comma-separating command names. This is useful when setting context and navigating in one selection ([Roku Commands](https://community.rockrms.com/developer/roku-docs/commands)). Use this sparingly. If two commands depend on each other, test the order on a real device.

### Roku Navigation Caching

Roku navigation command parameters include:

- `rockPageGuid`: Target page GUID, optionally with query-string parameters.
- `rockPageCacheControl`: Cache behavior for the target page. The docs describe options such as public and personal cache forms, with optional seconds values.
- `rockPageShowLoading`: Whether to show loading behavior.
- `rockPageSuppressInteraction`: Whether to suppress interaction writes ([Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)).

Use `personal` cache control for person-specific pages. Use no-store/no-cache page settings when content changes often or contains sensitive per-person data. Use public caching only for anonymous, non-sensitive, shared content such as a public message list.

### Roku Focus Management

Roku focus must be engineered. Rock’s `Rock:FocusGroup` extends `LayoutGroup` and handles vertical or horizontal focus among children. The docs state that as of 2024 Roku does not provide the same built-in focus management pattern Apple TV developers may expect ([Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

Use `Rock:FocusGroup` when:

- A row of buttons should respond to left/right.
- A vertical menu should respond to up/down.
- A group of custom controls needs predictable focus traversal.
- A page has multiple sections and focus would otherwise disappear or jump unexpectedly.

Do not use focus groups as a substitute for page structure. Start with `Rock:Page initialFocus`, then group directional sections.

### Roku RowList

`RowList` is the most important Roku layout node for shelves of media/content. The docs describe it as a horizontal list pattern that can support vertical and horizontal scrollability ([Roku RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)). Parameters include item size, row count, row heights, row item sizes, spacing, row label display, and focus animation styles.

Data binding structure:

- A root `ContentNode` is assigned to the RowList content field.
- Each child `ContentNode` under the root represents a row.
- Each row contains child `ContentNode` items.
- Row data can include a title.
- Item data can include image URL fields such as poster URL.

Agent checks for RowList bugs:

- Root content node exists.
- Rows are nested correctly.
- Items are nested under rows, not directly under the RowList.
- Each item has the fields the item template expects.
- Poster URLs are absolute or resolvable by Roku.
- Row/item sizes fit the target display.
- Focus lands on the RowList or a useful first item.

### Roku Layout Guardrails

The Roku layout docs warn that many Roku layouts do not include default item templates and recommend caution when selecting SceneGraph elements because the Rock approach tries to avoid custom BrightScript components ([Roku Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes)). The tips page is concise but important: keep layouts simple and use layout controls such as RowList for media/content selection ([Roku Tips](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks)).

For agents, this means the recommended fix for a messy Roku page is usually simplification, not adding more custom SceneGraph complexity.

## 10. Security And Authentication Deep Dive

### API Key Security

TV applications use API keys to connect to Rock. Apple and Roku application settings both expose API key configuration ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).

Guardrails:

- Use a dedicated API key for each TV app/environment.
- Do not reuse a high-privilege admin API key.
- Verify the key’s person/security context.
- Rotate keys deliberately with shell/demo app update coordination.
- Treat app config and demo keys as sensitive.
- Do not expose API keys through Lava-rendered markup, public pages, logs, or screenshots.

### Remote Authentication Flow

Remote authentication has two halves:

- The TV shell starts or checks a remote authentication session and displays a code/QR-driven login page.
- The user visits a website page containing the Remote Authentication block, enters the code, and authorizes the session while logged in.

Apple TV documentation instructs creating an external page with the Remote Authentication block and selecting the TV application site in block settings ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)). Roku personal login documentation says the app must define a login page before using the login command, and the command can specify login page, timeout page, success page, timeout duration, check duration, and navigation-stack clearing behavior ([Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)).

Source-code landmarks:

- `RemoteAuthenticationSessionService.StartRemoteAuthenticationSession(...)` creates a session with client IP, device unique identifier, code issue date, and code lifetime ([service source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)).
- `VerifyRemoteAuthenticationSession(...)` checks active session, code, code issue date, code lifetime, and device unique identifier ([service source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)).
- `RemoteAuthenticationSessionExtensions` filters sessions by code and active lifetime ([extensions source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)).
- `RemoteAuthentication.ascx.cs` defines the block, site selector, Lava header/footer/success content, and code expiration duration ([block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)).

### Remote Auth Component Selection

Rock includes a remote-auth field type and picker that lists active authentication components requiring remote authentication while excluding the PIN authentication entity type in the excerpted source ([RemoteAuthsPicker](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/RemoteAuthsPicker.cs), [RemoteAuthsFieldType](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Field/Types/RemoteAuthsFieldType.cs)). If a remote auth method is missing from configuration, inspect:

- Whether the authentication component is active.
- Whether it has `RequiresRemoteAuthentication`.
- Whether it is intentionally excluded.
- Whether the field’s Obsidian/WebForms implementation is being used in the current admin UI.

### Page Security And Sensitive Data

TV pages can render `CurrentPerson`, `Context`, page parameters, and device data. If a page includes private information, it must not be publicly cached. Combine page security, cache settings, and command cache control.

For Lava APIs, Rock’s Lava API documentation gives an explicit security warning: Lava webhook endpoints do not inherently secure the Lava they run, so be careful about exposed data ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). If an agent finds a TV app pulling XML from Lava webhooks instead of TV page records, treat those endpoints as public unless live security proves otherwise.

Security checklist:

- Anonymous pages render only anonymous-safe data.
- Personalized pages require login or defensively branch on `CurrentPerson`.
- Page cache settings do not leak person-specific data.
- API key permissions are scoped.
- Remote auth block is on an appropriate external page.
- Login success clears navigation stack where needed.
- Logout removes person state from the UI.
- Lava commands enabled for any webhook are minimal.
- Sensitive media URLs are not exposed to anonymous users unless intentionally public.

## 11. Styling And Controls Deep Dive

### Apple TV Styling

Apple TV styling resembles CSS but is not full CSS and should follow Apple’s design language rather than trying to recreate a web brand pixel-for-pixel. The TV Text Style docs emphasize that Apple TV apps are not HTML and should align with Apple TV design patterns ([TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)).

Styling areas:

- **Text styles**: Use TV text style values such as body, callout, caption, footnote, headline, title variants, and related platform-defined styles. Verify exact accepted values in Apple TV docs and the deployed shell ([TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)).
- **Font weight and family**: Use documented TVML style support rather than web font assumptions.
- **Theme media queries**: Style light/dark theme differences with TV template media queries ([Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries)).
- **Page theme**: Some templates accept a theme value such as light/dark, while the user’s system preference may drive the default ([Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes)).
- **Built-in images**: tvOS exposes built-in image libraries and SF Symbols; custom embedded resources can also be used, and references omit file extensions for app resources ([Built in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)).
- **Custom Rock controls**: `RockLabel` and `RockStackView` expose styling surfaces for custom controls ([RockLabel](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rocklabel), [RockStackView](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rockstackview)).

### Apple TV Custom Controls

TVML is powerful but limited; Rock provides custom controls where needed ([Control Reference](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference)).

The `rockCountdown` control can display a live countdown, use Lava-generated date values, and integrate with scheduled content. The docs warn that scheduled-content shortcode logic has overhead and may need caching for heavily visited pages ([Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown)).

Use countdown controls for:

- Service countdowns.
- Event start times.
- Live stream pre-roll screens.
- Time-sensitive campaign launches.

Verify date timezone handling in the rendered TVML. A countdown bug is often a date-format or timezone bug rather than a control bug.

### Roku Controls

Rock provides custom SceneGraph controls to attach Rock command behavior:

- `Rock:Button` extends Roku Button and adds `rockCommand` plus command parameter fields ([Roku Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button)).
- `Rock:ContentNode` extends ContentNode and adds `rockCommand` plus command parameter fields ([Roku Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)).
- `Rock:Page` extends Group and represents the page root with `initialFocus` ([Roku Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)).
- `Rock:FocusGroup` extends LayoutGroup for vertical/horizontal focus management ([Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).

Roku control guidance:

- Use Rock controls when the element needs to execute Rock commands.
- Use native SceneGraph controls for passive display.
- Keep command attributes close to the selectable item.
- Assign stable IDs to focus targets.
- Prefer fewer, clearer focus groups over deeply nested focus zones.
- Test with the Roku remote, not just markup inspection.

## 12. Related Rock Areas: Api Integrations, Lava, Cms, Security, Media, Mobile

### API Integrations

TV Apps depend on Rock API access through configured API keys. Rock’s API documentation distinguishes API v1 and API v2 and links to broader API resources ([Rock API Documentation](https://community.rockrms.com/api-docs)). For TV Apps, do not assume a generic REST pattern until you inspect the shell and deployed code. Use the app configuration and TV-specific source landmarks first.

### Lava

Lava is the rendering engine for TV pages. It can query content, branch on login/context, generate XML, build page parameters, and expose media metadata. Lava can also create webhook-based XML APIs for Apple TV or Roku, but Rock’s Lava API docs warn that webhook Lava has no built-in security on execution and can expose data if misused ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).

Agent Lava rules:

- Output valid XML for the platform.
- Escape dynamic text appropriately.
- Avoid emitting empty required attributes.
- Cache expensive Lava only when safe.
- Do not expose person data through public cache.
- Verify enabled Lava commands on webhook Defined Values before trusting data access.

### CMS

TV applications are CMS-adjacent. They use applications/sites, pages, routes, assets, and content structures, but the output is not HTML. Agents familiar with Rock CMS should transfer concepts like pages, security, routes, Lava, and interactions, but not HTML blocks or browser assumptions.

### Security

Security includes API keys, page security, remote authentication, Lava command exposure, and cache behavior. Remote auth source code and field types are core landmarks ([RemoteAuthenticationSession source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthsFieldType](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Field/Types/RemoteAuthsFieldType.cs)).

### Media

TV Apps are often media-first. Media commands can play audio/video and write watch interactions. YouTube is explicitly unsupported for direct playback in both Apple TV and Roku docs ([Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media)). Use direct playable URLs and confirm platform codec/container support.

### Mobile

Mobile matters mainly for authentication and shared patterns. Apple TV built-in images docs compare custom resources to Rock Mobile custom resources ([Built in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)). Remote authentication usually happens from a phone or computer. Do not confuse TV Apps with Rock Mobile apps; their markup, runtime, and submission processes differ.

## 13. Administration And Operational Guardrails

Operational guardrails:

- Keep separate app records for development, staging, and production when possible.
- Use separate API keys by environment.
- Keep page-view retention intentional; long retention may create unnecessary interaction storage, while short retention may undermine analytics.
- Avoid public caching on pages that render `CurrentPerson`, person-specific context, or private media.
- Treat app demo keys and API keys as secrets.
- Keep TV pages small enough to render reliably.
- Avoid huge images; Apple TV tips warn large images can slow loading ([Apple TV Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)).
- Avoid SVG in Apple TV markup; the tips page notes SVG images are unsupported ([Apple TV Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)).
- Do not build around WebView behavior on tvOS; Apple TV tips note there is no WebView implementation in tvOS ([Apple TV Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)).
- Keep Roku layouts simple and use RowList for media/content selection ([Roku Tips](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks)).
- Track GitHub issues for Roku feature requests/bugs through the docs’ useful links page ([Roku Useful Links](https://community.rockrms.com/developer/roku-docs/resources/useful-links)).

Operational checks before release:

- App launches from cold start.
- Root page renders anonymous.
- All navigation targets load.
- Back behavior is acceptable.
- Login code displays.
- Remote auth web page authorizes the device.
- Login timeout page appears after expiration.
- Login success page appears after authorization.
- Logout clears personalized UI.
- Media playback starts.
- Media resume works if implemented.
- Page interactions write when enabled.
- Suppressed interactions do not write.
- Cache headers match page sensitivity.
- Light/dark themes are legible.
- Images load from public/CDN paths usable by the device.
- Device logs show no parse errors.

## 14. Developer, API, Lava, And Source-Code Landmarks

Use these source-code landmarks when the docs are not enough:

- `Rock/Tv/Classes/AppleTvApplicationSettings.cs`: Apple TV app settings, including application script/styles and API key-related configuration ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/AppleTvApplicationSettings.cs)).
- `Rock/Tv/Classes/RokuTvApplicationSettings.cs`: Roku app settings, including `ApiKeyId` and `RockComponents` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/RokuTvApplicationSettings.cs)).
- `Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs`: remote auth entity, table mapping, site/person alias relationships, REST generation attributes ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)).
- `Rock/Model/Security/RemoteAuthenticationSessionService.cs`: start/verify remote auth sessions, code generation, throttling behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)).
- `Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs`: query filters for active sessions and code matching ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)).
- `RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs`: Remote Authentication block attributes and submission behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)).
- `Rock/Web/UI/Controls/Pickers/RemoteAuthsPicker.cs`: picker for remote auth components ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/RemoteAuthsPicker.cs)).
- `Rock/Field/Types/RemoteAuthsFieldType.cs`: field type for remote auth component selection ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Field/Types/RemoteAuthsFieldType.cs)).
- `Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs`: generated API v2 model endpoint for remote authentication sessions ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)).
- `Rock.Rest/Controllers/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs`: generated classic REST controller ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Controllers/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)).
- `Rock.Migrations/.../202201111342049_AddRemoteAuthenticationSession.cs`: migration introducing the remote authentication session table ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs)).

Use these documentation landmarks:

- Apple TV root docs ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- Apple TV app creation ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)).
- Apple TV pages and merge fields ([TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).
- Apple TV sign-in ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)).
- Apple TV media commands ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).
- Roku root docs ([Roku Docs](https://community.rockrms.com/developer/roku-docs)).
- Roku applications ([Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).
- Roku pages ([Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).
- Roku commands ([Commands](https://community.rockrms.com/developer/roku-docs/commands)).
- Roku resources and controls ([Resources](https://community.rockrms.com/developer/roku-docs/resources)).
- Lava APIs ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).
- Rock API docs ([API Documentation](https://community.rockrms.com/api-docs)).

## 15. Reporting, Analytics, And Model Map

TV App reporting usually depends on interactions. Application settings control whether page views are written and how long they are retained for both Apple TV and Roku ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Media commands can write media-related interactions and watch maps ([Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media)).

Reporting questions agents should answer with live inspection:

- Is page-view tracking enabled on the TV application?
- What is the retention period?
- Are navigation commands suppressing interactions?
- Are media commands writing new interactions or appending to existing ones?
- Are anonymous and authenticated interactions distinguishable?
- Does the interaction component/channel/entity type used by the TV shell match reporting assumptions?
- Are watch maps stored in the expected interaction data field?
- Are page GUIDs stable enough for reporting over time?
- Are old interactions being purged by retention policy?

Model map guidance:

- `RemoteAuthenticationSession` belongs to the Core domain and is not the same as an interaction. It tracks remote auth code/session state ([RemoteAuthenticationSession source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)).
- TV page analytics should be traced through interaction-related entities in the deployed Rock instance.
- If the source pack is thin on exact interaction entity types for TV page views, inspect the live database and source for the current Rock version instead of inventing a model path.
- For media resume, inspect the interaction GUID and watch map passed to the media command, then verify the resulting interaction row.

## 16. Version And Release Caveats

Known version anchors from the source pack:

- Apple TV functionality requires Rock v14 or greater according to the Apple TV docs ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- Roku was introduced in Rock v16.7 according to Roku docs and release ecosystem records ([Roku Docs](https://community.rockrms.com/developer/roku-docs), [GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)).
- Remote authentication session migration appears under Version 13.0 / 1.13.1 migration path in source, so remote-auth infrastructure predates the Apple TV v14 documentation requirement ([AddRemoteAuthenticationSession migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs)).
- Roku docs refer to focus-management limitations “as of 2024,” so verify current Roku shell behavior if working on a later Rock version ([Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)).
- API docs describe API v1 as legacy and API v2 as newer; do not assume TV shell endpoints without checking deployed source/shell behavior ([API Documentation](https://community.rockrms.com/api-docs)).

When upgrading Rock:

- Re-test TV page rendering because parser behavior or shell expectations may change.
- Re-test remote authentication because session lifetime, throttles, or auth component behavior may change.
- Re-test media playback because platform media support and Rock media commands may change.
- Re-test interaction reporting because write/suppression behavior may change.
- Re-test Roku focus behavior and custom controls.
- Re-test Apple TV theme and template behavior.
- Review release notes for TV, media, Lava, API, interaction, and security changes.

## 17. Implementation Playbooks

### Playbook: Anonymous Sermon Library

Goal: Public TV app showing sermon series and messages.

Use:

- Apple TV: Catalog/List/Product templates.
- Roku: RowList shelves and product/detail pages.
- Lava queries for public media/content records.
- Public caching for anonymous lists if no private data is included.
- Media commands for playback.
- Interactions enabled for page/media analytics.

Checks:

- Media URLs are direct and platform-playable.
- YouTube links are not used as playback URLs.
- Page cache is public only for anonymous-safe pages.
- Detail pages do not expose private speaker/person data.
- Playback writes interactions if analytics are required.

Sources: [Apple TV Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates), [Roku RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media).

### Playbook: Campus Selection

Goal: Let viewer choose a campus and personalize content.

Use:

- Context commands to set `Campus`.
- Lava reads `Context.Campus`.
- Navigation command pushes campus-specific page.
- Clear context command for reset/change campus.

Apple TV docs describe context as able to store Rock entities by friendly name and ID/GUID, commonly Campus ([Apple TV Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context)). Roku utility commands provide `setContext` and `clearContext` ([Roku Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)).

Checks:

- Context key matches entity friendly name expected by Lava.
- Context value is valid ID or GUID for that entity.
- If platform persistence matters, verify whether context persists after app restart on the specific platform/version.
- Personalized campus page uses safe cache settings.

### Playbook: Remote Login With Personalized Home

Goal: User logs in from phone/computer and TV shows personalized home.

Use:

- Website page with Remote Authentication block.
- TV app authentication/login page setting.
- Login command with login page, timeout page, success page.
- Success page that greets `CurrentPerson`.
- Navigation stack clearing after login.

Checks:

- Remote Authentication block site matches TV app.
- Verification code appears and is accepted.
- Code expiration is long enough for real users.
- Timeout page appears.
- Success page does not public-cache person data.
- Back button cannot reveal stale anonymous/login screens if that matters.

Sources: [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page), [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal), [RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs).

### Playbook: Live Event Countdown

Goal: Show countdown until service/live stream.

Use:

- Apple TV `rockCountdown`.
- Lava date formatting from a schedule or event.
- Short cache if schedule lookup is expensive.
- Completed command or post-countdown page if supported by the deployed shell.

Checks:

- Date is in expected ISO/timezone format.
- Countdown matches local event time on device.
- Page cache does not keep stale dates too long.
- Fallback content appears if no occurrence is found.

Source: [Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown).

### Playbook: Roku Media Shelves

Goal: Roku home with rows of media.

Use:

- `Rock:Page initialFocus`.
- `RowList` with root content node, row content nodes, and item content nodes.
- Item poster URLs and command fields.
- `Rock:ContentNode` items when selecting a row item should execute a command.

Checks:

- RowList content hierarchy is correct.
- Posters load on device.
- Focus starts on the RowList or first row item.
- Selecting an item plays media or navigates to detail.
- Layout is simple and not dependent on custom BrightScript.

Sources: [Roku RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist), [Roku Tips](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks), [Roku Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node).

## 18. Troubleshooting Decision Tree

### App Does Not Launch Or Shows Wrong Content

1. Is the installed shell pointed at the expected Rock instance?
2. Is demo mode active when production settings were expected, or vice versa? For Apple TV, review demo key/testing setup ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app), [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)).
3. Is the API key valid and assigned to the app?
4. Does the root/start page exist?
5. Is the root/start page valid TVML or SceneGraph?
6. Does the page render anonymous, or does Lava assume `CurrentPerson` exists?
7. Are cache settings returning stale content?

### Page Is Blank

1. Render the saved Lava output and inspect the final XML.
2. Confirm platform dialect: TVML for Apple TV, SceneGraph for Roku.
3. Check for unescaped characters in dynamic text.
4. Check for missing required root element. Roku should use `Rock:Page` as outer page content ([Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)).
5. Check for invalid image/media URLs.
6. Check device logs for parse errors.
7. Temporarily replace page content with a minimal valid page. If that works, reintroduce sections incrementally.

### Roku Focus Does Not Move

1. Does the page have `Rock:Page initialFocus` pointing at an existing ID?
2. Are controls focusable?
3. Are horizontal/vertical controls wrapped in `Rock:FocusGroup`?
4. Is `layoutDirection` correct for the desired movement?
5. Are there nested groups causing focus traps?
6. Test with a real Roku remote.

Source: [Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group).

### Navigation Button Does Nothing

1. Is the selectable control a Rock command-capable control such as `Rock:Button` or `Rock:ContentNode` on Roku?
2. Is `rockCommand` spelled correctly?
3. Is the command supported by that platform?
4. Is `rockPageGuid` a real page GUID?
5. If multiple commands are comma-separated, does either command fail alone?
6. Is the page target valid and accessible?
7. Is loading suppressed or hidden by a cached previous page?

Sources: [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands), [Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation).

### Media Does Not Play

1. Is the URL a direct platform-playable media URL?
2. Is it a YouTube URL? If so, replace it; both Apple TV and Roku docs say YouTube playback is not supported ([Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Roku Media](https://community.rockrms.com/developer/roku-docs/commands/media)).
3. Is HTTPS required by the platform or deployment?
4. Does the media server support range requests and correct content type?
5. Are captions or alternate streams supported by the target platform?
6. Are command attributes complete?
7. Are interaction/watch-map fields malformed?

### Remote Login Fails

1. Does the TV app have a login/authentication page configured?
2. Does the login command include valid login, timeout, and success page GUIDs?
3. Does the website authentication page exist and load publicly?
4. Is the Remote Authentication block on that page?
5. Does the block point to the correct TV app site?
6. Is the code expired?
7. Does `RemoteAuthenticationSession` show a session for the device unique identifier and code?
8. Does `AuthorizedPersonAliasId` get populated after the user submits the code?
9. Are IP throttles preventing new sessions?
10. Does the shell poll often enough and long enough?

Sources: [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page), [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal), [RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs).

### Analytics Missing

1. Is page-view tracking enabled on the app?
2. Is retention set long enough?
3. Does navigation command suppress interactions?
4. Are media commands writing or appending to interactions?
5. Is the user anonymous or authenticated?
6. Are reports looking at the right interaction channel/component/entity?
7. Has cleanup removed old interactions?

Sources: [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Roku Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands).

## 19. Agent Task Recipes

### Recipe: Audit A TV App Configuration

Collect:

- Platform: Apple TV or Roku.
- Rock version.
- Application record name, GUID/ID if available.
- API key ID/person.
- Page-view enabled flag.
- Retention days.
- Authentication page.
- Root/start page.
- Global styles/components.
- All page GUIDs referenced by commands.
- Cache settings for each page.
- Media URL sources.
- Remote auth block page and attributes.

Report:

- Configuration summary.
- Security concerns.
- Cache concerns.
- Broken page references.
- Missing auth pieces.
- Media risks.
- Version caveats.
- Live checks still needed.

### Recipe: Trace A Page GUID

1. Search TV page records for the GUID.
2. Confirm platform and parent application.
3. Render the page with relevant query parameters.
4. Inspect final XML.
5. Check merge fields used.
6. Check page cache settings.
7. Check page security.
8. Check commands pointing out from the page.
9. Check whether page writes interactions.
10. Test device navigation.

### Recipe: Validate Remote Auth In Data

Inspect:

- `RemoteAuthenticationSession` rows created during a test.
- `Code`.
- `DeviceUniqueIdentifier`.
- `ClientIpAddress`.
- `AuthenticationIpAddress`.
- `SessionStartDateTime`.
- `SessionEndDateTime`.
- `SiteId`.
- `AuthorizedPersonAliasId`.

Expected flow:

- New session row appears when TV login starts.
- Code matches displayed code.
- Authorized alias is empty before web authorization.
- Authorized alias is populated after successful web authorization.
- Session remains active within lifetime.
- Shell detects success and navigates to success page.

Use source behavior as a guide, but verify fields and timestamps in the deployed database ([RemoteAuthenticationSession source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)).

### Recipe: Review A Roku Page For Focus

Check:

- `Rock:Page` exists as page root.
- `initialFocus` references an actual control ID.
- Horizontal controls are grouped.
- Vertical controls are grouped.
- IDs are unique.
- Buttons have enough width for labels.
- RowList has valid content hierarchy.
- Back navigation path is clear.

### Recipe: Review Apple TV Markup

Check:

- Document root is valid TVML.
- Template matches content type.
- Dynamic text is escaped.
- Images are supported formats, not SVG.
- No WebView assumptions.
- Theme styles are valid.
- Text overflow is handled.
- Large images are compressed/resized.
- Commands are valid for the shell.
- Media URLs are not YouTube links.

Sources: [Apple TV Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips), [Apple TV Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates).

### Recipe: Decide Cache Policy

Use public cache only when:

- Page is anonymous.
- Content is identical for all users.
- No person/campus-sensitive data is included.
- Stale content is acceptable for the configured duration.

Use personal/private/no-store behavior when:

- Page uses `CurrentPerson`.
- Page uses person-specific watch progress.
- Page contains private media.
- Page uses auth state.
- Page uses context that should not leak across viewers.
- Page changes frequently.

Verify actual headers and CDN behavior in the live environment.





















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `14`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Rock Roku pages display custom Lava-driven content as part of the application and render SceneGraph-oriented output rather than normal Rock CMS HTML. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| official | behavior | Apple TV pages in Rock must output valid TVML and can use Rock-provided Lava merge fields such as CurrentPerson, Context, Campuses, SiteStyles, and CurrentPage. | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) |
| official | configuration | A Rock Apple TV app is created as a Rock-managed TV application record under CMS configuration, with Rock-side settings that are distinct from the App Store name. | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) |
| official | configuration | A Rock Roku application includes configuration such as page-view tracking, page-view retention duration, and API key settings, so Roku troubleshooting should start with the application record before page Lava. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| official | implementation_pattern | Rock Apple TV documentation groups JavaScript command behavior as a core part of building TV applications, so TV app guidance should treat commands as part of navigation, media, utility, and demo workflows. | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| official | implementation_pattern | Roku commands are executed by setting a rockCommand and command-specific parameters on supported controls, and multiple commands can be chained by separating command names with commas. | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| official | source_summary | Rock Apple TV is documented as a set-top extension of Rock RMS for TVML applications linked to Rock, and the Apple TV functionality requires Rock version 14 or greater. | [source](https://community.rockrms.com/developer/apple-tv-docs) |
| official | source_summary | Rock Roku documentation describes Roku support as a way to extend Rock-powered digital ministry to Roku TV through Rock-managed Roku integration. | [source](https://community.rockrms.com/developer/roku-docs) |
| release-note-confirmed | release_caveat | Triumph's GitHub Spotlight for the v17.0.29 pre-alpha notes that the Roku TV app feature was added for Rock v16.7, making Roku coverage version-sensitive. | [source](https://www.triumph.tech/resources/github-spotlight-1042024) |
| community-reviewed | operational_guidance | MAUI-related Rock Mobile guidance should include styling, border, shadow, animation, toast, and performance behavior because those are visible app-design surfaces, not only build-system concerns. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |
| community-reviewed | operational_guidance | Compatibility support can reduce migration risk by allowing existing Xamarin Forms-style content to run while teams move selected content blocks or pages toward MAUI-native behavior. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |
| More |  | 2 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->









































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->





















## 20. Source Map And Dependency Notes

### Release Notes And Community Examples

Version context matters for TV Apps because Apple TV and Roku behavior depends on both Rock server features and shell/runtime expectations. Use Rock release notes as the release authority before assuming that a TV app setting, remote-auth behavior, API route, or security hardening exists in the target instance ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Community examples are useful as examples only. A TV-related question or recipe can help an agent recognize a pattern, but it should not override official Apple TV/Roku docs, release notes, or source code. For cross-surface questions such as API access, event data, external links, or login behavior, the Rock Q&A developing area is a useful signal that real implementers hit the issue, but the answer must still be verified against current docs and the live instance ([Developing for Rock Q&A](https://community.rockrms.com/ask/developing)).

Primary TV sources:

- Apple TV root docs: [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs).
- Apple TV app creation: [Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app).
- Apple TV testing: [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app).
- Apple TV content/page creation: [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content), [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages).
- Apple TV sign-in: [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page).
- Apple TV context: [Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context).
- Apple TV templates: [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates).
- Apple TV styling: [Styling](https://community.rockrms.com/developer/apple-tv-docs/styling), [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style), [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries), [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes), [Built in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images).
- Apple TV media/personal/demo commands: [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands), [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands).
- Roku root docs: [Roku Docs](https://community.rockrms.com/developer/roku-docs).
- Roku getting started: [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started).
- Roku app settings: [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications).
- Roku pages: [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages).
- Roku commands: [Commands](https://community.rockrms.com/developer/roku-docs/commands), [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Media](https://community.rockrms.com/developer/roku-docs/commands/media), [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility), [Personal](https://community.rockrms.com/developer/roku-docs/commands/personal).
- Roku controls/layout: [Controls](https://community.rockrms.com/developer/roku-docs/resources/controls), [Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button), [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node), [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group), [Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page), [Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes), [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist).
- Roku support links: [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources), [Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks), [Useful Links](https://community.rockrms.com/developer/roku-docs/resources/useful-links).

Related dependencies:

- API integrations: [Rock API Documentation](https://community.rockrms.com/api-docs).
- Lava APIs and security warning: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api).
- Roku v16.7 release context: [GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024).
- Remote authentication source: [RemoteAuthenticationSession](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs), [RemoteAuthenticationSessionExtensions](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs), [Remote Authentication block](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs).
- TV app settings source: [AppleTvApplicationSettings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/AppleTvApplicationSettings.cs), [RokuTvApplicationSettings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Tv/Classes/RokuTvApplicationSettings.cs).

Dependency notes for agents:

- TV Apps depend on API integrations for shell-to-Rock connectivity.
- TV Apps depend on Lava for dynamic XML rendering.
- TV Apps depend on CMS concepts for applications, pages, routes, styles, and content organization.
- TV Apps depend on Security for API keys, page access, and remote authentication.
- TV Apps depend on Media for playback URLs, watch maps, and interaction tracking.
- TV Apps overlap with Mobile mainly through remote authentication and shared resource concepts, but they are separate runtime surfaces.
