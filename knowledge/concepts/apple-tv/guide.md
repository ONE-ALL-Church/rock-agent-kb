---
id: authored-apple-tv
title: Apple TV Apps
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Apple TV Apps

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Apple TV Apps index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock Apple TV Apps are Rock-managed tvOS applications built around Apple TVML, Rock-hosted TV pages, Lava-rendered content, app-level styles, Rock-specific shell commands, and optional remote authentication. The official Rock Apple TV documentation describes the feature as a Rock RMS set-top extension and explicitly says Rock Apple TV functionality requires Rock version 14 or greater ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). Treat that version requirement as the first operational gate. If a live instance is below v14, do not attempt to configure the feature without first confirming whether the relevant blocks, pages, entities, and shell support exist in that environment.

The central mental model is simple: Rock stores an Apple TV app definition, app-level settings, pages, styles, and TVML. The Apple TV shell retrieves those pages and interprets the TVML. Lava can run inside the TV page content, so Rock data can shape the final TVML output before it reaches the device. Navigation and behavior are driven by Rock-specific `rockCommand` attributes embedded in TVML elements, while Apple TV layout and presentation remain constrained by TVMLKit and tvOS behavior ([Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands), [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

For agents doing real Rock work, the most important distinction is that Apple TV pages are not web pages. TVML is XML-like markup consumed by tvOS. Rock pages can be rendered with Lava, but the final result must still be valid TVML. HTML assumptions, browser CSS assumptions, WebView assumptions, SVG expectations, and normal web navigation assumptions will lead to broken screens or shell parse errors. The Rock docs warn against treating TVML as HTML and call out limitations such as no tvOS WebView, no SVG support, and limited CSS-like styling ([Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)).

The practical build path is:

1. Confirm Rock version and Apple TV feature availability.
2. Create or inspect the Apple TV app record under `Admin Tools > CMS Configuration > Apple TV Apps`.
3. Configure app-level fields such as name, description, application styles, page view tracking, API key, retention period, and login page where available in the installed version ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)).
4. Build the Start Screen and additional TV pages with valid TVML.
5. Use app-level `SiteStyles` and page-level styles consistently.
6. Use `rockCommand` attributes for navigation, media playback, context changes, login, logout, and utility actions.
7. Test through the Rock Core Apple TV app demo-key flow or a compiled shell that points to the correct Rock app ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app), [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)).
8. Add remote authentication only after the external Rock page, Remote Authentication block, Apple TV login page, timeout page, and success page are all understood and wired correctly ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page), [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)).
9. Verify analytics, interactions, retention, API key scope, and sensitive Lava output before production release.

Apple TV work crosses several Rock areas: CMS configuration, Site and Page concepts, Lava, API security, media delivery, interaction analytics, Rock security, remote authentication, and TV app shell behavior. An agent should not treat it as a standalone content-editing task. Every TV page is both a content surface and an integration endpoint.

## 2. Scope And Terminology

This guide covers Rock-powered Apple TV Apps: app records, pages, TVML content, Lava merge fields, app images, templates, Rock-specific TV commands, sign-in, remote authentication, media playback, styling, themes, source-code landmarks, operations, troubleshooting, and implementation playbooks.

It does not attempt to replace Apple’s TVMLKit documentation. The Rock Apple TV docs point to Apple TVML documentation as the primary source for the underlying TVML language, while Rock’s docs explain Rock-specific extensions and build patterns ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). When a question is about core TVML syntax, valid template nesting, tvOS focus behavior, or App Store packaging, verify against Apple’s current tvOS documentation and the compiled Apple TV shell being used. When a question is about Rock app records, Rock commands, Lava merge fields, remote authentication, or Rock media interaction behavior, use the Rock sources and live Rock instance.

Key terms:

`Apple TV App`
A Rock-managed TV app definition. Rock’s walkthrough calls it a site created under `Admin Tools > CMS Configuration > Apple TV Apps`, with app-level settings such as name, description, styles, page view behavior, API key, and retention ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). The Obsidian view model for the app detail block exposes fields such as `apiKey`, `applicationJavascript`, `applicationStyles`, `attributes`, `name`, `pageViewRetentionPeriod`, and `showApplicationJavascript` ([AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)).

`TV Page`
A Rock page-like record whose content must render as valid TVML. The docs describe TV pages as supporting Lava merge fields including `CurrentPerson`, `Context`, `Campuses`, `SiteStyles`, `CurrentPage`, edit/admin flags, `PageParameter`, `TvShellVersion`, and `DeviceData` ([TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

`TVML`
Apple’s XML-based markup language for tvOS templates. Rock Apple TV pages output TVML, not HTML. CSS-like styling exists but is limited and interpreted by TVMLKit rather than a browser ([Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips), [Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)).

`TV Shell`
The Apple TV app runtime that retrieves Rock TV pages, interprets TVML, processes Rock commands, manages navigation, handles media playback, and supports shell-specific behavior. The docs expose a `TvShellVersion` Lava value for page rendering decisions ([TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

`RockTvApp`
A JavaScript wrapper around Apple’s native App class. It exists to make shell behavior more resilient around network issues and parse errors, supports app lifecycle events, exposes a reload method, and provides app state and helper functions ([RockTvApp](https://community.rockrms.com/developer/apple-tv-docs/developer/rocktvapp)).

`rockCommand`
A Rock-specific TVML attribute used to invoke shell actions such as page navigation, media playback, context changes, login/logout, demo mode, or utility behavior. Multiple commands can be comma-separated for cases such as setting context and navigating in a single selection ([Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands)).

`Context`
A persisted app context key/value store in the TV framework. The docs describe storing any Rock entity in context by friendly name as the key and Id or Guid as the value, commonly for Campus selection. Context persists across viewing sessions and is accessible in page Lava through `Context` ([Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context)).

`Remote Authentication`
A passwordless-style authentication flow that lets the user sign into the TV app through another device or browser rather than typing credentials with the TV remote. Rock includes a Remote Authentication block under TV apps and a `RemoteAuthenticationSession` model for the session records ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page), [RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs), [RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)).

`Application Styles`
Global styles configured on the app record and injected into TV page styling with the `SiteStyles` Lava merge field ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)).

`Demo Key`
A testing mechanism that points the Rock Core Apple TV app at a configured Rock Apple TV app without publishing a dedicated app through TestFlight or the App Store ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app), [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)).

## 3. Apple TV Apps Mental Model

Think of a Rock Apple TV App as a Rock CMS site whose page content is rendered for a tvOS shell rather than a browser. The user’s Apple TV does not browse normal Rock HTML pages. It asks Rock for TVML documents. Rock renders those documents from stored page content, Lava, context, page parameters, app settings, current person state, and device data. The shell then parses the TVML, builds a tvOS interface, and handles user interactions through Rock-defined commands.

The normal request path looks like this:

1. The TV shell launches with compiled or demo-mode settings that identify the Rock server and app.
2. The shell requests the app’s configured starting page.
3. Rock evaluates the page content as TVML plus Lava.
4. The final TVML includes Apple templates, controls, images, text, styles, and `rockCommand` attributes.
5. The shell parses the TVML into tvOS views.
6. When a user selects a menu item, lockup, button, or command-bearing element, the shell executes the `rockCommand`.
7. The command may navigate, present a modal, play media, set context, clear context, log in, log out, follow content, remove content, pray for a request, or perform demo-shell behavior depending on the command family ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands), [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands), [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)).

The Rock data model gives the app a CMS-like structure, but the experience model is closer to a media app. The screen is navigated with a remote. Focus state matters. Highlight behavior matters. Large TV images and legible text matter more than dense content. Apple’s templates carry strong layout opinions, and the Rock docs caution that heavy customization outside the Div Template can be difficult because templates have their own behavior, scrolling, animation, and element handling ([Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)).

The agent mental model should include four layers:

**Layer 1: Rock configuration**
This includes the Apple TV app record, app-level fields, pages, app styles, API key, page view tracking, retention period, login page settings, routes, and block configuration. These are inspected in Rock admin and, when needed, in the database or source.

**Layer 2: TVML document generation**
Each TV page’s content must become valid TVML. Lava can branch by person, campus, context, device, page parameter, or shell version. This is powerful but dangerous: malformed XML or invalid TVML can break the screen. Agents should validate the rendered output, not just the stored template.

**Layer 3: TV shell behavior**
The shell interprets Rock commands, caches or fetches pages, plays media, handles login, and manages navigation stack state. The docs describe navigation commands such as push, replace, present modal, pop, dismiss modal, and clear navigation stack ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)). When a symptom occurs on-device, inspect both the Rock-rendered output and shell-level behavior.

**Layer 4: tvOS and Apple constraints**
Apple TV is not a browser. Some designs cannot be reproduced with TVML alone. The Rock styling references include examples from Apple TV+, Fitness, Podcasts, and Arcade, but the references page warns that some observed app layouts may depend on native implementation details outside TVML ([References](https://community.rockrms.com/developer/apple-tv-docs/styling/references)). Agents should not promise that every Apple TV app design can be rebuilt in Rock TVML.

A reliable agent approach is to trace any issue in this order:

1. Is the app record configured and reachable?
2. Is the requested TV page found by GUID or start-page configuration?
3. Does Rock render valid TVML?
4. Are Lava merge fields and page parameters producing expected values?
5. Are image and media URLs absolute or otherwise resolvable by the Apple TV shell?
6. Is the `rockCommand` spelled and parameterized correctly?
7. Is the command supported by the shell version on the device?
8. Is authentication, context, caching, or API key behavior changing the output?
9. Is the problem a tvOS limitation rather than a Rock issue?

## 4. Source Authority And How To Use This Guide

Use this guide as a synthesized operating manual, not as a substitute for live verification. The most authoritative sources for Apple TV Apps in Rock are:

1. Rock’s Apple TV developer docs for feature behavior, walkthroughs, templates, commands, styling, sign-in, images, and testing ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
2. Rock source code for exact model fields, block behavior, REST controller behavior, generated view models, and implementation details ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
3. Rock API and Lava documentation for integration and endpoint patterns that feed TV apps ([API Documentation](https://community.rockrms.com/api-docs), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).
4. Release notes and community technical updates for version caveats, especially when TV app areas change across v16, v17, and later ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)).
5. Apple’s tvOS and TVMLKit documentation for underlying platform rules, App Store packaging, template validity, image assets, focus behavior, and media playback constraints.

The source pack includes many hydrated excerpts whose content is mostly navigation chrome. Where a hydrated excerpt is thin, this guide uses the compact source summaries and GitHub snippets as coverage metadata. If a claim is not strongly supported by a source record, the guide says what to inspect in a live Rock instance instead of inventing behavior.

Authority levels for common tasks:

`Use official Rock Apple TV docs first` for app setup, page authoring, commands, styling, templates, testing, and sign-in. These pages are the closest thing to a product manual.

`Use source code first` for exact entity properties, block attributes, REST security, generated view model fields, migration history, and current implementation behavior. For example, the Remote Authentication model and service source are better authority than a tutorial when diagnosing session behavior ([RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)).

`Use live Rock inspection` when the question depends on a specific instance: app IDs, page GUIDs, routes, block settings, API keys, security roles, enabled Lava commands, file URLs, CDN settings, site attributes, shell version, interactions, media element data, or data retention.

`Use Apple docs and device testing` when the question depends on tvOS behavior: whether a template supports a layout, whether a style property works, whether an image format is accepted, whether a media stream plays, and whether App Store assets meet current Apple requirements.

This guide cites sources inline. Use the links as audit trails. Because Rock and tvOS evolve, verify version-specific behavior in the installed Rock version and on a real Apple TV or simulator before treating an implementation as production-ready.

## 5. Core Configuration And Data Model

### Apple TV App Record

The app record is created in Rock at `Admin Tools > CMS Configuration > Apple TV Apps` according to the official setup walkthrough ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). The walkthrough describes creating a new site for the TV application, which means agents should expect the Apple TV app to participate in Rock’s site/page ecosystem rather than being a completely separate module.

The documented app fields include:

`Name`
Private name inside the Rock instance. The docs distinguish this from the eventual App Store name, so do not assume the Rock name is user-facing in Apple distribution ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)).

`Description`
Optional internal description. Use it to document app purpose, owner, deployment status, and production/test distinction.

`Application Styles`
Global TVML styles available across the app. The styling docs show that TV page styles can include `{{ SiteStyles }}` to inject configured site-wide styles into a page’s `<style>` block ([Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)).

`Enable Page Views`
Controls whether interaction data is recorded for page views. Treat this as both an analytics and privacy setting. If enabled, confirm retention and reporting expectations.

`API Key`
The key the app uses to access the Rock server during testing and likely shell operation. The docs mention configuring the API key on the app record ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). Agents should inspect the actual configured key, its person/user association, permissions, and whether it is production-appropriate. Never expose API keys in documentation output.

`Page View Retention Period`
Controls how long page view data is retained. The Obsidian app detail view model exposes `pageViewRetentionPeriod`, confirming this is represented in the current UI contract ([AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)).

`Application Javascript`
The generated Obsidian view model includes `applicationJavascript` and `showApplicationJavascript` ([AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)). The Apple TV docs caution that TVMLKit JS documentation is of lesser use because app JavaScript generally should not be updated ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). Treat app JavaScript as a shell-level surface and avoid modifying it unless the installed Rock version, app shell, and source behavior are understood.

`Attributes` and `Attribute Values`
The app detail view model includes attributes and public attribute bags, which means app records can have attributes exposed through the detail block contract ([AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)). In a live instance, inspect defined attributes on the app entity before assuming what custom metadata exists.

### TV Page Record

TV page content must be valid TVML, with Lava evaluated by Rock before the shell receives it ([TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)). The setup walkthrough describes adding content to the Start Screen and creating pages with page name, description, TVML, and cacheability type ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)).

The generated page detail view model includes attributes and attribute values, and imports `RockCacheabilityBag`, confirming the current UI contract includes cacheability-related configuration ([AppleTvPageBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts)). When diagnosing page caching, inspect both:

1. The page’s configured cacheability type in the Apple TV page detail UI.
2. Any command-level cache instruction such as `rockPageCacheControl` on navigation commands ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)).

### Page List Block Options

The generated page list options view model includes `defaultPageIdKey` and `isBlockVisible`, with visibility tied to an `ApplicationId` query parameter according to the source comment ([AppleTvPageListOptionsBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts)). If the Apple TV page list appears blank or hidden in admin, verify the query string includes the application identifier expected by the installed block.

### Remote Authentication Data Model

Remote authentication is backed by a `RemoteAuthenticationSession` entity. The model source maps it to the `RemoteAuthenticationSession` table, places it in the Core domain, disables normal entity security for read-only generated REST endpoints, and relates it optionally to `Site` and `AuthorizedPersonAlias` ([RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)). The migration that added the table in the v13-era migration folder created columns including `Code`, `AuthorizedPersonAliasId`, `SessionStartDateTime`, `SessionAuthenticatedDateTime`, `SessionEndDateTime`, `ClientIpAddress`, `AuthenticationIpAddress`, `DeviceUniqueIdentifier`, and `SiteId` ([AddRemoteAuthenticationSession migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs)).

Important live-verification note: the migration excerpt shows `DeviceUniqueIdentifier` with a 45-character max length when the table was introduced, while the current model excerpt includes remarks explaining that passwordless identifiers can be email addresses or phone numbers and need email-length capacity ([AddRemoteAuthenticationSession migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs), [RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)). In a real instance, inspect `INFORMATION_SCHEMA.COLUMNS` or the model/migration history for the installed version before assuming the exact column length.

Remote authentication sessions are service-managed. The service starts sessions by validating IP throttle limits, generating a usable code, storing client IP, code, session start time, and device unique identifier, then adding the record ([RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)). Verification looks for an active session with matching code, issue date, code lifetime, and device unique identifier, ordered by latest session start ([RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)). Extension methods filter active sessions and sessions matching a code within lifetime windows ([RemoteAuthenticationSessionExtensions](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)).

### Lava Endpoint And API Context

Rock’s Lava API documentation describes using a Lava webhook to return output from a Lava template, including XML APIs for Apple TV or Roku channels, and warns that these webhooks do not inherently provide security around running Lava ([Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)). This is relevant to Apple TV Apps because agents may be tempted to build supplemental XML endpoints for TV content. If using Lava endpoints, configure security deliberately and expose only intended data. The generated enum `LavaEndpointSecurityMode` lists security modes such as endpoint execute and application-level view/edit/administrate semantics, but live configuration must be inspected on the endpoint or defined value in the installed version ([LavaEndpointSecurityMode source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)).

## 6. Primary Entities And Relationships

### Apple TV App To Site

The setup docs tell administrators to create a new site under Apple TV Apps ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). In practical Rock terms, that means the app behaves like a specialized CMS site. Agents should inspect the `Site` record or the Apple TV app detail page for:

- Name and description.
- Site/app GUID.
- API key.
- App styles.
- Start page.
- Login page settings.
- Page view tracking.
- Retention period.
- Routes.
- Security and edit permissions.
- App attributes.

Do not assume the Apple TV app’s App Store identity, bundle identifier, or compiled-shell configuration is stored entirely in Rock. The Rock app record describes the Rock-hosted content and server-side behavior; Apple distribution metadata may live in Apple Developer/App Store Connect and the native shell project.

### Apple TV App To TV Pages

A TV app owns or lists TV pages. The Apple TV Page List options source suggests the page list block expects an `ApplicationId` query parameter and has a default page identifier key ([AppleTvPageListOptionsBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts)). The walkthrough says to open the Start Screen under the app and edit content there ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)).

Each page should be treated as a renderable endpoint:

- It has a stable identifier or GUID used by commands.
- It may accept query string parameters.
- It may read persisted app context.
- It may branch on `CurrentPerson`.
- It may include `SiteStyles`.
- It may be cacheable or personalized.
- It returns TVML.

### TV Pages To Lava Merge Fields

The TV Pages docs list the merge fields available to page content: current person, context, campuses, site styles, current page, edit/admin booleans, page parameters, shell version, and device data ([TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)).

Operational implications:

`CurrentPerson` may be null or anonymous. Always branch for signed-out users before rendering personalized collections.

`Context` persists across viewing sessions. It may not match the logged-in person’s campus unless you implement that logic.

`Campuses` can support campus pickers, campus-specific media, or location-aware content.

`SiteStyles` is the bridge between app-level styles and page-level TVML.

`PageParameter` enables page reuse but can create cache hazards if public cache is used.

`TvShellVersion` should be used when a page relies on command or control features introduced in later shell versions.

`DeviceData` is useful for diagnostics, support, and device-specific behavior. Inspect the actual structure rendered in your installed shell before depending on any specific property.

### TV Pages To Commands

Commands are embedded on TVML elements with `rockCommand`. Navigation commands use parameters such as `rockPageGuid` and may accept query string parameters appended to the GUID ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)). Utility commands use parameters such as `rockContextKey` and `rockContextValue` for context operations ([Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands)). Personal commands use login, logout, and related page GUIDs ([Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)). Media commands use media parameters and support watch-map behavior for resume tracking and interaction linkage ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).

A single element can fire multiple commands by separating command names with commas. The docs give the example of setting a context value and pushing a page from one selected element ([Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands)). Use this pattern carefully because it couples state mutation and navigation. If a page appears with the wrong context, inspect command order, context value, and whether context persisted from a prior session.

### Remote Authentication Session To Site And Person Alias

The source model configures optional relationships from `RemoteAuthenticationSession` to `Site` and `AuthorizedPersonAlias` ([RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)). This means a session can be scoped to a site and eventually connected to the authorized person alias. When diagnosing sign-in:

- Identify the session by code, device identifier, site, or timestamp.
- Confirm `SessionStartDateTime` is present.
- Confirm it has not expired according to configured code lifetime.
- Confirm `AuthorizedPersonAliasId` is populated after successful authentication.
- Confirm `SessionAuthenticatedDateTime` and `SessionEndDateTime` semantics in the installed code.
- Confirm `ClientIpAddress` and `AuthenticationIpAddress` are expected.
- Confirm `DeviceUniqueIdentifier` matches the shell flow.

The REST v2 generated controller exposes read endpoints for `RemoteAuthenticationSession` behind authentication and an unrestricted-read security action, with entity security ignored in the helper ([RemoteAuthenticationSessionsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)). Do not expose this data casually. Even read-only session data can reveal authentication state and identifiers.

## 7. Common Apple TV Apps Workflows

### Create A New App

Use this workflow when a ministry wants a new Apple TV presence or a dev/test app.

1. Confirm Rock version is v14 or higher as required by the Apple TV docs ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
2. Navigate to `Admin Tools > CMS Configuration > Apple TV Apps`.
3. Create the app/site record.
4. Set an internal `Name` and optional `Description`.
5. Add `Application Styles` only after deciding global typography, colors, spacing, and common classes.
6. Decide whether to enable page views.
7. Configure the API key. Use a dedicated integration identity where possible.
8. Set page view retention.
9. Save the app.
10. Open the app’s Start Screen and begin with a conservative template such as Main Template or Stack Template ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content), [Main Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/main-template), [Stack Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/stack-template)).

Live checks:

- Confirm the app has a GUID or identifier used by the shell.
- Confirm the Start Screen renders valid TVML.
- Confirm all image URLs are reachable by Apple TV.
- Confirm app styles are injected only where `{{ SiteStyles }}` appears.
- Confirm API key permissions are narrow enough for the app.

### Add A Content Page

Use this workflow when adding a series page, message detail page, category page, campus selection page, or alert page.

1. In the Apple TV app, create a new page.
2. Give it a clear page name and description.
3. Choose the page’s cacheability type deliberately ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)).
4. Write TVML content.
5. Add a `<head><style>` block if the page needs page-local styles.
6. Include `{{ SiteStyles }}` if the page should inherit app styles ([Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)).
7. Use Lava for dynamic data only after a static TVML skeleton works.
8. Save and test by navigating from another page with `rockCommand="pushPage"` and `rockPageGuid`.
9. If using page parameters, test with and without parameters.
10. If using personalization, test signed out and signed in.

Live checks:

- Render the page output and validate it as XML/TVML.
- Confirm no unescaped text breaks XML.
- Confirm null Lava values do not create invalid attributes.
- Confirm dynamic collections do not create empty template sections that tvOS rejects.
- Confirm caching does not leak personalized output.

### Build A Campus Selector

Use context commands and Lava context access.

1. Render a page listing campuses from `Campuses` or a verified entity query.
2. For each campus, add a selectable element with `rockCommand="setContext, pushPage"` if selecting should immediately navigate.
3. Set `rockContextKey="Campus"`.
4. Set `rockContextValue` to the campus Guid or Id expected by your Lava lookup.
5. Push a page that reads `Context.Campus` ([Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context), [Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands), [Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands)).

Do not assume campus context follows the logged-in person. The context docs explicitly distinguish campus context from a person’s campus and recommend checking context first, then optionally falling back to signed-in-person data ([Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context)).

### Add Login

Use remote authentication.

1. Create an external Rock page.
2. Add the Remote Authentication block.
3. Configure the block’s Site setting to the Apple TV app/site ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)).
4. Configure or inspect the block’s header content, footer content, success message, and code expiration duration in the installed version. The source block defines these attributes and uses Lava editors for content ([RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)).
5. Add a route or stable URL to that external page.
6. Create a TV login page that displays the remote login URL, QR code, or code fields expected by the shell.
7. Configure the app’s login page setting if present.
8. Add a menu item or button with `rockCommand="login"` and the required page GUIDs.
9. Add logout UI with the logout command.

Live checks:

- Confirm the Remote Authentication block URL works in a browser.
- Confirm the TV login page receives the merge fields documented by the login flow.
- Confirm code expiration is long enough for TV use but short enough for security.
- Confirm sessions are scoped to the correct site.
- Confirm login success and timeout pages exist and are valid TVML.

### Play Media

Use media commands rather than custom JavaScript.

1. Confirm the media URL is playable on tvOS.
2. Do not use YouTube content; Rock’s media command docs state YouTube content cannot be played inside an Apple TV application ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).
3. Choose video or audio command.
4. Supply media metadata and watch-map values according to the command docs.
5. If resuming an existing interaction, provide the watch map from that interaction.
6. If appending to an existing interaction, provide both the interaction GUID and watch map.
7. Test start, pause, resume, completion, and replay.

Live checks:

- Confirm media file format, streaming protocol, and certificate compatibility on Apple TV.
- Confirm content is not behind an authentication scheme unsupported by tvOS.
- Confirm interactions are written only when expected.
- Confirm watch-map behavior does not create duplicate or fragmented interactions.

## 8. Building Your First Apple TV App Deep Dive

The official first-app walkthrough frames Rock Apple TV as a way to build TVML apps linked to Rock without requiring custom programming ([Building Your First App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app)). For agents, the walkthrough is useful but should be turned into a repeatable implementation process with verification gates.

### Step 1: Confirm Preconditions

Before creating anything:

- Rock version must be v14 or greater for Apple TV functionality according to the docs ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- The Apple TV Apps admin pages must exist.
- The user must have administrative access to CMS configuration.
- A testing method must be available: Rock Core Apple TV demo mode, TestFlight, simulator, or compiled shell.
- A media strategy must exist for video/audio URLs.
- Image assets must meet tvOS sizes and formats.
- Security expectations must be clear before API keys and remote authentication are configured.

If any precondition fails, stop and inspect the live instance. Do not author pages in isolation and assume they can be launched.

### Step 2: Create The App

The documented navigation is `Admin Tools > CMS Configuration > Apple TV Apps` ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). Create a new app/site. Set an internal name that distinguishes environment and purpose, such as `Weekend Messages Apple TV - Test` or `Apple TV Production`.

Configure only essential fields at first:

- Name.
- Description.
- API key.
- Page view tracking decision.
- Retention period.
- Minimal application styles.

Avoid heavy global styles in the first pass. TVML template behavior can be surprising, and global styles can make troubleshooting harder.

### Step 3: Create The Start Screen

The official content walkthrough uses the Start Screen and suggests the Main Template as a good starting point ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content), [Main Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/main-template)). The Main Template is suited to a landing page with a strong background and a menu bar near the bottom. It works well for a simple app with options like Latest Message, Series, Search, Campus, and Sign In.

A practical Start Screen should include:

- A small number of high-value options.
- A background image sized for TV.
- A login or account option if personalization exists.
- A fallback alert or error page for missing content.
- A demo or diagnostics option only in non-production builds.

Use static TVML first. Then add Lava.

### Step 4: Add Content Pages

Choose templates based on content shape:

- Use Stack Template for rows of categories, carousels, grids, or shelves ([Stack Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/stack-template)).
- Use Product Template for an individual message, teaching, or media item with metadata and related content ([Product Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-template)).
- Use Product Bundle Template for a series landing page with related messages or episodes ([Product Bundle Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-bundle-template)).
- Use List Template for a single category’s item list, such as favorites or messages in one series ([List Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/list-template)).
- Use Catalog Template for grouped categories where selecting a group changes related content ([Catalog Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/catalog-template)).
- Use Alert or Descriptive Alert Template for errors, sign-in states, terms, or long text ([Alert Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/alert-template), [Descriptive Alert Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/descriptive-alert-template)).
- Use Div Template only when other templates cannot achieve the layout. The docs warn that it lacks built-in layout and relies on positioning/alignment styles ([Div Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/div-template)).

### Step 5: Wire Navigation

Use navigation commands:

`pushPage`
Use for normal drill-down navigation. Provide `rockPageGuid` and optional query string parameters ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)).

`replacePage`
Use when the current page should be replaced rather than pushed. This is useful for login success, timeout, or state-driven pages where back navigation would be confusing.

`presentModal`
Use for alerts, confirmations, or temporary overlays.

`popPage`
Use to move back in the navigation stack.

`dismissModal`
Use to close a modal.

`clearNavigationStack`
Use when returning home or resetting after login/logout.

When combining navigation with context, use multiple commands. Example: selecting a campus may set `Campus` context and then push a campus-specific page ([Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands), [Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands)).

### Step 6: Add Images

Apple TV images are operationally important. The application-image docs split them into app icons, top shelf, launch image, and parallax images ([Application Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images)).

Asset requirements from the docs include:

- App icons use layered parallax assets, with in-app sizes of 800x480 @2x and 400x240 @1x, plus an App Store icon size of 1280x768 ([App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons)).
- Top Shelf Wide sizes are 2320x720 @1x and 4640x1440 @2x; older Top Shelf sizes are 1920x720 @1x and 3840x1440 @2x ([Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image)).
- Launch images are static, not layered, and require 1920x1080 @1x and 3840x2160 @2x ([Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image)).
- Parallax images use layered assets to create focus depth and motion ([Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)).

For content images, the tips docs warn against huge images because they slow loading; they also note SVG images are unsupported ([Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)). Use JPG/PNG/Web-safe formats accepted by tvOS, compress aggressively enough for performance, and test on real hardware.

### Step 7: Test The App

The official testing docs describe requesting a demo key, installing the Rock Core Apple TV app, entering the key in the Demo tab, and restarting the app so it points at the configured application ([Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app)). Demo commands also exist in the shell for showing, clearing, and updating demo mode, but require the application to be compiled with demo support ([Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)).

A complete test pass should include:

- Cold launch.
- Start Screen load.
- Navigation to every top-level item.
- Back navigation.
- Modal open/dismiss.
- Login flow.
- Logout flow.
- Media playback.
- Resume playback.
- Context selection.
- Signed-out personalization fallback.
- Broken/missing image fallback.
- Network failure behavior.
- Parse error behavior.
- Theme light/dark behavior.
- Cache behavior after content changes.
- Demo reset.

## 9. Apple TV Sign-In And Authentication Deep Dive

Apple TV sign-in exists because entering credentials with a remote is poor UX. Rock’s sign-in guide uses a Remote Authentication block on an external Rock page and configures TVML to initiate login from the Apple TV side ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)).

### Server Setup

The documented setup is:

1. Create a new external page.
2. Add the Remote Authentication block.
3. Configure the block setting so it is tied to the Apple TV site/app.
4. Copy the page URL or create a route.
5. Test the URL in a browser ([Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)).

The source block is categorized under `TV > TV Apps` and described as authenticating an individual for a remote system ([RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)). Its configurable block attributes include:

- `Site`: optional site tied to remote authentication.
- `Header Content`: Lava template shown above the code entry.
- `Footer Content`: Lava template shown below.
- `Success Message`: Lava template shown after successful authentication.
- `Code Expiration Duration`: timeout value for authentication code validity.

The markup includes a security code text box, submit button, notification box, and header/footer literals ([RemoteAuthentication markup](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx)). The code-behind supports an `AuthCode` page parameter that attempts authentication directly when present, otherwise it sets up the page for manual code entry ([RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)).

### TVML Setup

The personal commands docs define the login command. The command requires a configured login page in the application because that setting is used to configure the QR code ([Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)). The login command accepts page GUID parameters for:

- Login page.
- Timeout page.
- Success page.

Agents should create all three pages before exposing the login command. The login page should explain what to do, render the code or QR information provided by the shell, and fit comfortably on a TV. The timeout page should provide a retry action. The success page should redirect or offer account-aware next steps.

### Session Lifecycle

Source code shows the service starts a remote authentication session by checking IP throttle limits, generating a usable code, setting client IP, code, start time, and device unique identifier, then adding the session ([RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)). Verification looks for an active matching session by lifetime, code, and device unique identifier ([RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)). Extension methods filter sessions created today, sessions using a code, and active sessions ([RemoteAuthenticationSessionExtensions](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)).

Operationally, a sign-in failure can come from:

- Wrong site selected on the Remote Authentication block.
- Login command missing required page GUIDs.
- App missing configured login page.
- Expired code.
- Code entered for the wrong device unique identifier.
- IP throttle exceeded.
- Remote Authentication page inaccessible externally.
- Lava in header/footer/success message failing.
- User not actually logged into Rock on the browser device.
- Session not linked to `AuthorizedPersonAliasId`.
- Clock skew affecting code issue/lifetime comparisons.
- Cached login page showing stale code data.
- API key or shell version mismatch.

### Security Guardrails

Remote authentication touches identity. Apply these guardrails:

- Keep code lifetimes short enough to reduce replay risk but long enough for real users.
- Confirm daily IP throttle settings in the installed version before public launch.
- Do not include sensitive personal data on the TV login page before the user is authenticated.
- Use HTTPS for the Rock page.
- Use stable routes rather than copy-pasted internal admin URLs.
- Audit `RemoteAuthenticationSession` rows during testing.
- Confirm failed attempts show generic errors and do not disclose whether a code exists.
- Clear sessions or understand session end behavior after logout.
- Keep the Remote Authentication page’s Rock security appropriate for signed-in users who authenticate the TV.

The REST controller for remote authentication sessions is generated as a read-only API behind authentication and unrestricted-read security; do not grant broad API users access unless they need it ([RemoteAuthenticationSessionsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)).

## 10. Apple TV JavaScript Commands Deep Dive

Rock Apple TV commands are declarative command attributes inside TVML. They let content authors trigger shell behaviors without writing custom JavaScript. The commands docs note that commands normally fire one at a time but can be combined by comma-separating command names ([Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands)).

### Navigation Commands

Navigation commands show and hide pages in the Apple TV shell ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)).

`pushPage`
Adds a new page to the navigation stack. Use it for normal drill-down from home to category to item detail. The required parameter is `rockPageGuid`, and the docs show that query string parameters can be appended to the page GUID. Use this for pages that take `GroupId`, `ContentChannelItemId`, `SeriesGuid`, or similar parameters, but verify the receiving page reads `PageParameter`.

`replacePage`
Replaces the current page. Use for state transitions where going back would be invalid, such as after login success, retrying a timed-out code, or changing a start page after context selection.

`presentModal`
Shows a modal. Use for alerts, confirmations, and short messages.

`popPage`
Returns to the prior page.

`dismissModal`
Closes a modal.

`clearNavigationStack`
Resets navigation. Use sparingly, usually for returning home, completing login, or handling logout.

`rockPageCacheControl`
The navigation docs describe cache control options for loaded pages, including public caching with an optional seconds value and personal caching that appends the logged-in person’s guid to the URL ([Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)). Use public caching only for truly non-personal output. Use personal caching when output changes by user. If content changes are not appearing, inspect both page cacheability and command-level cache control.

### Media Commands

Media commands handle playback of video and audio ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)). The docs explicitly state YouTube content cannot be played in an Apple TV application, so agents should not try to fix YouTube playback with markup changes.

The most important media concept is watch-map handling. The docs describe `rockWatchMap` and `rockInteractionGuid` behavior:

- Supplying a watch map from an existing interaction can set resume location.
- Supplying both interaction GUID and watch map can append to an existing watch map.
- Supplying a watch map without an interaction GUID uses it for resume location but writes a new interaction with a fresh watch map ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).

Operationally, this means media playback is not just a player launch. It can write or update interaction state. When troubleshooting duplicate views or resume problems, inspect interaction records, media element references, watch-map payloads, and whether the command is passing an existing interaction GUID.

### Personal Commands

Personal commands cover login and logout ([Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)).

`login` requires login-related page GUIDs and depends on the app having a login page configured. Use it only after the remote authentication server page is working.

`logout` should clear the signed-in state. After logout, test pages that use `CurrentPerson` to ensure they render signed-out content rather than stale personalized data.

### Utility Commands

Utility commands include context, DOM-style state changes, and user/content actions ([Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands)).

`setContext`
Stores a context value. Required parameters include `rockContextKey` and `rockContextValue`.

`clearContext`
Clears the context value for the provided key.

`toggleAttribute`
Marked TV v2.0 in the docs and used to change object styles on the DOM ([Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands)). Before using it, verify the shell version with `TvShellVersion`.

`follow`
Follow behavior depends on the target entity/content support in the installed shell. Verify exact parameters in the live docs or source before using.

`removeItem`
Likely removes an item from a UI collection or personal list depending on parameters. Verify in live shell behavior.

`prayForRequest`
Intended for prayer request interaction. Verify the data model, permissions, and UI expectations before exposing it.

### Demo Commands

Demo commands let a demo-capable app change server/application settings. The docs say the app must be compiled with demo mode support ([Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)).

`showDemo` opens the demo mode screen.

`clearDemo` clears demo settings and returns to compiled settings.

`updateDemo` updates demo settings from a code entered in the demo screen.

Use demo commands only in testing or support contexts. A production app should not expose demo controls to normal users.

## 11. Apple TV Styling Deep Dive

Rock Apple TV styling is CSS-like but not browser CSS. The styling docs show that styles are placed at the top of the TVML document inside the `<head><style>` section, and that classes and IDs can be used in normal CSS-like syntax ([Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)). The same docs show that app-wide styles can be injected with `{{ SiteStyles }}`.

### Style Placement

A page should generally follow this structure:

- XML declaration if needed.
- `<document>`.
- `<head>`.
- `<style>`.
- `{{ SiteStyles }}` when global styles are desired.
- Page-specific style rules.
- Template content.

Avoid burying style in repeated dynamic sections unless there is a specific need. Repeated style blocks can make rendered TVML harder to inspect.

### Global Styles

Use app-level `Application Styles` for classes reused across pages:

- Standard title classes.
- Metadata text classes.
- Lockup image sizing.
- Focus/highlight behavior.
- Theme-specific colors.
- Common margins.
- Content row spacing.

Use page-level styles for page-specific layout and template quirks. If a page does not include `{{ SiteStyles }}`, app-level styles will not apply according to the styling docs ([Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)).

### Text Styling

TVML supports text styles, font weights, bold/italic/strike tags, font families, and text shadows according to the TV Text Style page headings and summary ([TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)). The docs also warn that Apple TV app styling should align with Apple’s design language rather than highly customized web-like branding ([TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)).

Agents should prefer TV text styles such as body, callout, caption, footnote, headline, title variants, and subtitle variants over manually setting every font size. If a title overflows, fix content length, max lines, or highlight behavior rather than shrinking everything globally.

### Themes And Media Queries

Apple TV has light and dark themes. The themes docs say users generally choose the theme and the app responds; page styles can use media queries to adapt to light or dark, and a specific page can define a theme on the template ([Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes)). The media query docs show theme-specific style blocks using `@media tv-template and (tv-theme:light)` and `@media tv-template and (tv-theme:dark)` ([Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries)).

Practical rules:

- Always test in light and dark.
- Avoid hardcoded white text unless the background is controlled.
- Avoid relying on blurred background darkness if images vary.
- Use theme queries for text and badge colors.
- If forcing a template theme, document why.

### Built-In Images And Resources

tvOS includes built-in image resource libraries such as button icons, miscellaneous icons, movie ratings, TV ratings, and SF Symbols. The built-in images docs also describe custom embedded shell resources and warn that file extensions should not be included when referencing resources because tvOS removes file extensions ([Built in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)).

Use built-in resources for standard controls where possible. For example, a play action should look like a play action. Avoid over-branding common icons.

### Rock Custom Controls

Rock provides custom controls for cases where TVML alone is insufficient ([Control Reference](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference)).

`rockCountdown`
Displays a live countdown and can change appearance when it reaches zero. The countdown docs show it can be driven by a `startDateTime` value and can use Lava to compute dates or scheduled content. The docs warn that the scheduled content shortcode can add overhead and should be cached for heavy traffic ([Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown)).

`RockStackView`
A layout element within custom controls. Supported style concepts include background color, tint color, interitem spacing, margin, width, border radius, and layout direction values such as horizontal or vertical ([RockStackView](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rockstackview)).

`RockLabel`
The primary text element inside custom controls. Supported style concepts include background color, tint color, font color, margin, width, font size, font weight, and TV text style ([RockLabel](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rocklabel)).

### Styling Pitfalls

Common styling failures:

- Treating TVML as HTML.
- Using unsupported CSS properties.
- Using SVG images.
- Using image URLs with unsupported patterns.
- Overloading TV pages with huge images.
- Assuming text overflow works like web CSS.
- Depending on template behavior that Apple changes.
- Applying global styles too broadly.
- Designing for desktop density rather than TV distance.
- Copying layouts from native Apple apps that TVML cannot reproduce.

The tips docs directly call out TVML/HTML confusion, no WebView, no SVG images, large image performance problems, and compression/CDN considerations ([Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)).

## 12. Related Rock Areas: Api Integrations, Lava, Cms, Security, Media, Tv Apps

### API Integrations

Apple TV Apps may use Rock API access through the configured app API key. The Rock API resource page distinguishes API v1 as classic and now legacy, and API v2 as newer and designed to do more ([API Documentation](https://community.rockrms.com/api-docs)). For Apple TV work, the API key setting on the app record should be treated as an integration credential. Confirm:

- Which person or user login owns the API key.
- Which REST endpoints it can access.
- Whether it needs read-only or write permissions.
- Whether it can read personal data.
- Whether it can write interactions or media activity.
- Whether it is safe for production shell distribution.

Do not use an admin API key for convenience.

### Lava

TV page content can use Lava. This is the main way dynamic Rock data becomes TVML. The TV Pages docs list Apple TV page merge fields, and the Lava API docs describe how Lava can also back XML APIs for Apple TV or Roku-like channels ([TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)).

Lava guardrails:

- Escape XML-sensitive values.
- Handle nulls.
- Limit query sizes.
- Cache expensive scheduled content.
- Avoid exposing private data to unauthenticated TV pages.
- Keep personalization pages out of public CDN caching.
- Verify enabled Lava commands on endpoints or pages.

### CMS

Apple TV app records and pages live in the CMS configuration area. Treat routes, sites, pages, attributes, and security as CMS concerns. If a page does not appear in the Apple TV admin UI, inspect the ApplicationId query parameter and page list block options ([AppleTvPageListOptionsBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts)).

### Security

Security exists at multiple layers:

- Rock admin access to edit the app.
- API key scope.
- Page security.
- Remote Authentication block security.
- Lava command availability.
- REST endpoint permissions.
- Media URL access.
- Personalized caching behavior.
- Interaction and analytics data access.

Remote authentication source code and REST controller source are important landmarks when diagnosing identity behavior ([RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs), [RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [RemoteAuthenticationSessionsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)).

### Media

Media commands and watch maps connect Apple TV playback to Rock interactions ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)). Inspect MediaElements, interaction records, watch maps, file storage, CDN, and stream compatibility when media symptoms occur.

### TV Apps

Apple TV is part of Rock’s TV app surface. A Triumph technical update noted a new Roku TV app feature in v16.7, showing that Rock’s TV app ecosystem continues to evolve beyond Apple TV ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)). When building shared content logic, consider whether it should be Apple-specific TVML, shared Lava data, or reusable media APIs that can support Roku or future TV apps.

## 13. Administration And Operational Guardrails

### Ownership

Every Apple TV app should have:

- Business owner.
- Technical owner.
- Content owner.
- API key owner.
- Media owner.
- App Store or distribution owner.
- Support contact.

Document these in the app description, an internal runbook, or a repository file.

### Environment Separation

Use separate app records for development/test and production. Do not point demo testing at production pages until changes have passed validation. Keep API keys distinct. Keep app names clear.

### API Key Hygiene

API keys should be:

- Dedicated to the TV app.
- Least-privilege.
- Rotatable.
- Documented outside public TVML.
- Removed from screenshots and support logs.
- Tested after rotation.

### Caching And Personalization

Cache decisions are a common source of bad behavior. Page cacheability and command-level `rockPageCacheControl` can interact ([Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content), [Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)). Use public caching only for pages whose TVML does not vary by user, context, device, or sensitive parameters. Use personal cache behavior or no caching for pages with `CurrentPerson`.

### Analytics And Retention

If `Enable Page Views` is on, confirm:

- What interaction data is written.
- How long it is retained.
- Whether page view retention is configured.
- Whether media interactions are separate from page views.
- Whether dashboards exist.
- Whether privacy policies cover TV usage.

The app detail view model exposes `pageViewRetentionPeriod`, confirming retention is part of app configuration ([AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)).

### Image Operations

Keep a checklist of required app images:

- In-app icons.
- App Store icon.
- Top Shelf Wide.
- Top Shelf legacy if needed.
- Launch images.
- Parallax content images.

Use the official size pages for asset verification ([App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons), [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image), [Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image), [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)).

### Release Gate

Before publishing or promoting to production:

- All pages render valid TVML.
- All navigation commands work.
- Login/logout works.
- Media playback works on real Apple TV hardware.
- Light/dark themes are legible.
- API key is production-ready.
- Page views and retention are configured.
- No test demo controls are exposed.
- No sensitive Lava data is exposed.
- All images are production assets.
- Support runbook exists.

## 14. Developer, API, Lava, And Source-Code Landmarks

Use these source landmarks when the admin UI or docs are not enough.

`Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts`
Current Obsidian UI contract for Apple TV app detail fields, including API key, application JavaScript, styles, attributes, name, page view retention period, and show-application-JavaScript flag ([AppleTvAppBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)).

`Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts`
Current Obsidian UI contract for Apple TV page detail. The import of `RockCacheabilityBag` is a useful source clue for cacheability behavior ([AppleTvPageBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts)).

`Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts`
Page list options, including app/page identifier behavior and visibility tied to `ApplicationId` query parameter ([AppleTvPageListOptionsBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts)).

`RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs`
Remote Authentication block attributes and server-side page flow ([RemoteAuthentication block source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)).

`Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs`
Remote Authentication session entity, relationships to site and person alias, REST generation flags, and property metadata ([RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)).

`Rock/Model/Security/RemoteAuthenticationSessionService.cs`
Session start and verification behavior, including code generation, throttling, active session lookup, and device identifier matching ([RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)).

`Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs`
Queryable filters for created-today, code matching, and active session windows ([RemoteAuthenticationSessionExtensions](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)).

`Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs`
Generated REST endpoints and security annotations for remote authentication session reads ([RemoteAuthenticationSessionsController source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)).

`Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts`
Security mode enum for Lava endpoints, useful when Apple TV data is produced through Lava webhook endpoints ([LavaEndpointSecurityMode source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)).

## 15. Reporting, Analytics, And Model Map

Apple TV app reporting can involve at least three data families:

1. Page views from Apple TV pages when enabled.
2. Media interactions and watch maps from media commands.
3. Remote authentication sessions.

The app-level `Enable Page Views` field controls whether page view interaction data is recorded according to the app setup docs ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)). The `Page View Retention Period` field controls how long that data is retained. In a live instance, inspect the app detail UI and underlying interaction tables to confirm actual storage behavior.

Media commands can write or update interactions through watch-map behavior ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)). A reporting agent should distinguish page view events from media watch events. A user opening a message detail page is not the same as a user playing the message, resuming playback, or completing it.

Remote authentication reporting comes from `RemoteAuthenticationSession`. Useful fields include code, authorized person alias, session start, authentication time, end time, client IP, authentication IP, device identifier, and site ([RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs), [AddRemoteAuthenticationSession migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs)). Use this for sign-in troubleshooting, not broad engagement reporting.

Model-map tasks to perform in a live instance:

- Find the Apple TV app/site record.
- List TV pages for the app.
- Inspect page GUIDs used by commands.
- Inspect page cacheability.
- Inspect app attributes.
- Inspect enabled page view tracking and retention.
- Inspect interaction records for page views.
- Inspect media interaction records and watch maps.
- Inspect remote authentication sessions by site and date.
- Inspect API key identity and permissions.

When source material is thin, do not invent table names beyond those confirmed by source. Use the Rock Model Map or live schema inspection to find the exact entity/table for Apple TV app and page records in the installed version.

## 16. Version And Release Caveats

The top-level Apple TV docs require Rock v14 or greater for Apple TV functionality ([Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)). That is the clearest version caveat in the source pack.

Other caveats:

- Remote Authentication table creation appears in a v13-era migration path, but Apple TV functionality itself is documented as v14+ ([AddRemoteAuthenticationSession migration](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.1/202201111342049_AddRemoteAuthenticationSession.cs), [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)).
- Top Shelf image formats differ by tvOS generation: Top Shelf Wide was introduced in tvOS v10.0, while the older Top Shelf size applied to tvOS v9.0 and older according to the image docs ([Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image)).
- Utility command `toggleAttribute` is marked TV v2.0 in the docs, so verify shell version before relying on it ([Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands)).
- Menu Bar Template docs warn navigation with that template will not work with the current shell version referenced by the docs ([Menu Bar Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/menu-bar-template)). Before using it, test in the actual shell version.
- Triumph’s 2024 technical update notes Roku TV app feature work in v16.7, which is not Apple TV behavior but indicates TV app surfaces continue to evolve ([GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)).
- API v1 is described as legacy on the API resource page, while API v2 is positioned as newer ([API Documentation](https://community.rockrms.com/api-docs)). For any custom integration that feeds Apple TV, prefer current API guidance.

Agents should always record:

- Rock version.
- TV shell version from `TvShellVersion`.
- Apple TV hardware/tvOS version.
- Whether app is demo-mode or compiled production.
- Whether using Rock Core app, TestFlight app, or production App Store app.

## 17. Implementation Playbooks

### Playbook: Weekend Messages App

Goal: Build a basic app for latest message, series archive, and sign-in.

1. Create Apple TV app record.
2. Configure API key and page views.
3. Add global styles for titles, subtitles, lockups, and metadata.
4. Create Start Screen using Main Template.
5. Add `Latest Message` item with `pushPage`.
6. Add `Series` item with `pushPage`.
7. Add `Sign In` item with `login`.
8. Create Latest Message page using Product Template.
9. Create Series list page using Stack Template.
10. Create Series detail page using Product Bundle Template.
11. Create Message detail page using Product Template.
12. Add media command to play video.
13. Test watch-map behavior.
14. Add signed-in favorites later using List Template.

Verify:

- Latest message query returns one item.
- Empty content renders an alert page.
- Media is not YouTube.
- All images fit TV.
- Signed-out state works.
- Login flow works.

### Playbook: Campus-Aware App

Goal: Let households choose a campus and see campus-specific content.

1. Create Campus Selector page.
2. Render campus options from `Campuses`.
3. Use `setContext` with `rockContextKey="Campus"`.
4. Push home or campus page after context set.
5. In content pages, read `Context.Campus`.
6. If no context exists, show selector or choose fallback.
7. If signed in, optionally use person campus only after checking context first.

Verify:

- Context persists across app restart.
- Clear context path exists.
- Campus value format matches Lava lookup.
- Page cache does not ignore campus differences.

### Playbook: Remote Login

Goal: Use browser/mobile authentication for Apple TV.

1. Create external Rock page.
2. Add Remote Authentication block.
3. Configure block Site.
4. Add route.
5. Open route in browser.
6. Create TV login, timeout, and success pages.
7. Configure app login page setting.
8. Add login command to TV menu.
9. Add logout command.
10. Test with signed-out and signed-in Rock browser sessions.
11. Inspect `RemoteAuthenticationSession` rows during testing.

Verify:

- Correct site ID.
- Code lifetime.
- Device identifier match.
- Authorized person alias set after success.
- Timeout page renders.
- Logout clears `CurrentPerson`.

### Playbook: Media Resume

Goal: Resume videos from prior watch location.

1. Identify MediaElement or media source.
2. Render media page with playback command.
3. Include interaction/watch-map data when resuming.
4. Include `rockInteractionGuid` only when appending to an existing interaction.
5. Test pause and resume.
6. Inspect interaction records.
7. Confirm new plays do not overwrite unrelated interactions.

Verify:

- Resume point correct.
- New interaction behavior matches expectation.
- Completion behavior recorded.
- Replaying from beginning is possible.

### Playbook: Production Readiness Audit

1. Inventory app settings.
2. Export page list and GUIDs.
3. Validate every page’s rendered TVML.
4. Validate all image URLs.
5. Validate all media URLs.
6. Validate API key permissions.
7. Validate page view retention.
8. Validate remote authentication.
9. Validate signed-in/signed-out state.
10. Validate cache behavior.
11. Validate demo controls absent.
12. Validate App Store assets.

## 18. Troubleshooting Decision Tree

### App Does Not Launch

Check:

1. Rock version is v14+.
2. Shell points to correct Rock server.
3. Demo key or compiled settings are correct.
4. API key is valid.
5. Start Screen exists.
6. Start Screen TVML renders without errors.
7. Rock server is reachable over HTTPS.
8. Network, certificate, and CDN are accessible from Apple TV.

If the shell shows parse errors, retrieve the rendered TVML and validate it. Do not debug the stored Lava alone.

### Page Is Blank

Check:

1. The command points to the correct page GUID.
2. Query string parameters are valid.
3. Lava does not return empty required elements.
4. Template supports the element structure.
5. Images are reachable.
6. Cache is not serving stale or wrong content.
7. Signed-in-only content has a signed-out fallback.
8. Theme colors are not hiding text.

### Navigation Does Not Work

Check:

1. `rockCommand` spelling.
2. Required command parameters.
3. Multiple command formatting.
4. Page GUID.
5. Optional query string.
6. Shell version support.
7. Template-specific limitations. For Menu Bar Template, verify current shell support because docs warn navigation does not work with the current shell version they reference ([Menu Bar Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/menu-bar-template)).

### Sign-In Fails

Check:

1. App has login page configured.
2. Login command includes login, timeout, and success page GUIDs.
3. Remote Authentication block exists.
4. Block Site setting points to the Apple TV app.
5. Remote Authentication page route works.
6. Code is not expired.
7. User is signed into Rock in browser.
8. Device unique identifier matches session.
9. IP throttle not exceeded.
10. Session row exists and becomes authorized.
11. Success page renders valid TVML.

### Media Will Not Play

Check:

1. Media is not YouTube ([Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)).
2. URL is HTTPS and reachable by Apple TV.
3. File/stream format is tvOS compatible.
4. Certificate is valid.
5. Command uses correct video/audio command.
6. Required parameters are present.
7. MediaElement data is valid.
8. CDN does not block Apple TV user agents.
9. Signed URLs have not expired.

### Resume Does Not Work

Check:

1. Existing interaction has watch map.
2. `rockWatchMap` is passed.
3. `rockInteractionGuid` is passed only when appending.
4. New interaction creation behavior matches docs.
5. Person is signed in if resume is user-specific.
6. Cache is not serving stale watch-map data.

### Styles Do Not Apply

Check:

1. Styles are in `<head><style>`.
2. Page includes `{{ SiteStyles }}` if relying on global styles.
3. Selector matches class or id.
4. Property is supported by TVML.
5. Theme media query matches current theme.
6. Template allows the style on that element.
7. Custom controls use supported Rock control styles.

### Images Do Not Render

Check:

1. URL reachable from Apple TV.
2. Format supported.
3. Not SVG.
4. Image dimensions reasonable.
5. No file extension issue for embedded tvOS resources.
6. CDN query strings supported.
7. HTTPS certificate valid.
8. App assets meet required sizes.

## 19. Agent Task Recipes

### Recipe: Inspect An Existing Apple TV App

1. Open Apple TV app detail in Rock.
2. Record name, description, API key identity, page views, retention, app styles, login page.
3. List all TV pages and GUIDs.
4. Open Start Screen.
5. Render and validate TVML.
6. Search for `rockCommand`.
7. Map every command to a target page, media action, context action, or personal action.
8. Identify pages using `CurrentPerson`, `Context`, `PageParameter`, or `DeviceData`.
9. Identify public vs personalized pages.
10. Report risks and unknowns.

### Recipe: Diagnose A Broken Button

1. Identify the element.
2. Read its `rockCommand`.
3. Confirm command family.
4. Confirm required parameters.
5. Confirm multiple-command syntax.
6. Confirm target page/media/context exists.
7. Test target page directly.
8. Check shell version.
9. Check cache.
10. Check rendered TVML.

### Recipe: Add A New Page Safely

1. Create page with static TVML first.
2. Test navigation.
3. Add styles.
4. Add Lava data.
5. Add null/empty fallback.
6. Add cacheability.
7. Add command from source page.
8. Test signed out.
9. Test signed in.
10. Inspect rendered output.

### Recipe: Review For Security

1. Identify API key and owner.
2. List pages using `CurrentPerson`.
3. List pages using Lava entity commands or APIs.
4. Inspect page cacheability.
5. Inspect command cache controls.
6. Inspect Remote Authentication block route.
7. Inspect remote session REST access if enabled.
8. Confirm no secrets in TVML.
9. Confirm no private data in public pages.
10. Confirm retention settings.

### Recipe: Review For Performance

1. List all images and sizes.
2. Check for huge images.
3. Check for SVG.
4. Check dynamic Lava loops.
5. Check scheduled content shortcodes.
6. Check cacheability.
7. Check media URL performance.
8. Test cold launch.
9. Test page transitions.
10. Test on real Apple TV hardware.
















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `9`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Apple TV pages in Rock must output valid TVML and can use Rock-provided Lava merge fields such as CurrentPerson, Context, Campuses, SiteStyles, and CurrentPage. | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) |
| official | configuration | A Rock Apple TV app is created as a Rock-managed TV application record under CMS configuration, with Rock-side settings that are distinct from the App Store name. | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) |
| official | implementation_pattern | Rock Apple TV documentation groups JavaScript command behavior as a core part of building TV applications, so TV app guidance should treat commands as part of navigation, media, utility, and demo workflows. | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| official | source_summary | Rock Apple TV is documented as a set-top extension of Rock RMS for TVML applications linked to Rock, and the Apple TV functionality requires Rock version 14 or greater. | [source](https://community.rockrms.com/developer/apple-tv-docs) |
| community-reviewed | operational_guidance | MAUI-related Rock Mobile guidance should include styling, border, shadow, animation, toast, and performance behavior because those are visible app-design surfaces, not only build-system concerns. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |
| community-reviewed | operational_guidance | Compatibility support can reduce migration risk by allowing existing Xamarin Forms-style content to run while teams move selected content blocks or pages toward MAUI-native behavior. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |
| community-reviewed | operational_guidance | Rock Mobile's move toward .NET MAUI should be treated as an evolution from Xamarin Forms rather than an unrelated app platform. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |
| community-reviewed | source_summary | This RockCast episode adds public-safe context for the Rock Mobile transition from Xamarin Forms toward .NET MAUI. It describes MAUI as a close successor with compatibility support, newer styling and animation options, performance improvements, and a release path that lets existing apps test compatibility before fully moving new content blocks to MAUI-native behavior. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->
















## 20. Source Map And Dependency Notes

### Release Notes And Community Examples

Use Rock release notes to verify the installed-version boundary before assuming an Apple TV app setting, remote-auth behavior, API route, Lava endpoint security rule, or Obsidian admin block behavior exists in the target instance ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Apple TV documentation also has explicit version framing, so release notes and live Rock version should be checked before using source snippets from `develop`.

Community examples and Q&A are useful as implementation signals only. They can reveal real integration problems around API calls, login behavior, event data, or external links, but they are not the source of truth for Apple TV app behavior. Use them as examples after official Apple TV docs, release notes, source-code landmarks, and live instance inspection have already established the authoritative path ([Developing for Rock Q&A](https://community.rockrms.com/ask/developing)).

Primary Apple TV sources:

- [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs): top-level feature description, v14+ requirement, TVML positioning, and issue tracker reference.
- [Building Your First App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app): first-app walkthrough entry point.
- [Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app): app creation fields and admin navigation.
- [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app): demo key and Rock Core app testing flow.
- [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content): Start Screen, page creation, TVML, and cacheability.
- [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages): TV page content rules and Lava merge fields.
- [Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips): TVML limitations, no WebView, no SVG, image performance, QR and overflow considerations.
- [Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context): persisted context, campus context, set/clear behavior.
- [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page): remote authentication setup.

Template sources:

- [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)
- [List Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/list-template)
- [Alert Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/alert-template)
- [Descriptive Alert Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/descriptive-alert-template)
- [Div Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/div-template)
- [Main Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/main-template)
- [Parade Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/parade-template)
- [Catalog Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/catalog-template)
- [Compilation Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/compilation-template)
- [Menu Bar Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/menu-bar-template)
- [One Up Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/one-up-template)
- [Product Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-template)
- [Product Bundle Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-bundle-template)
- [Rating Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/rating-template)
- [Showcase Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/showcase-template)
- [Stack Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/stack-template)

Command sources:

- [Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands)
- [Navigation Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands)
- [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)
- [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)
- [Utility Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands)
- [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)

Styling and image sources:

- [Styling](https://community.rockrms.com/developer/apple-tv-docs/styling)
- [Getting Started](https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started)
- [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)
- [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries)
- [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes)
- [Built in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)
- [Application Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images)
- [App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons)
- [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image)
- [Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image)
- [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)

Control sources:

- [Control Reference](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference)
- [Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown)
- [Control Styling](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling)
- [RockStackView](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rockstackview)
- [RockLabel](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rocklabel)

Related Rock sources:

- [API Documentation](https://community.rockrms.com/api-docs)
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)
- [GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)

Source-code dependencies to verify in live work:

- [AppleTvAppBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvAppDetail/appleTvAppBag.d.ts)
- [AppleTvPageBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts)
- [AppleTvPageListOptionsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts)
- [RemoteAuthentication block](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Tv/RemoteAuthentication.ascx.cs)
- [RemoteAuthenticationSession model](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/RemoteAuthenticationSession/RemoteAuthenticationSession.cs)
- [RemoteAuthenticationSessionService](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionService.cs)
- [RemoteAuthenticationSessionExtensions](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)
- [RemoteAuthenticationSessionsController](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/RemoteAuthenticationSessionsController.CodeGenerated.cs)
- [LavaEndpointSecurityMode](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)

Dependency notes:

- `api-integrations`: needed for API key behavior, REST access, and custom data feeds.
- `lava`: needed for dynamic TVML rendering and Lava webhook APIs.
- `cms`: needed for app/site/page/route configuration.
- `security`: needed for API key scope, remote authentication, endpoint access, and personalized output.
- `media`: needed for playback commands, MediaElement behavior, interaction records, and watch maps.
- `tv-apps`: needed for Apple TV shell behavior, TVML pages, demo mode, and cross-TV-app patterns.
