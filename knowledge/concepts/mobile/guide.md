---
id: authored-mobile
title: Rock Mobile
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Rock Mobile

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Rock Mobile index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock Mobile is the native mobile application layer for Rock RMS. It is not simply a responsive website wrapper. A Rock Mobile app is a configured mobile application in Rock Core, rendered by a native shell, populated by Rock pages, blocks, XAML layouts, commands, controls, styling, content, authentication, and API-backed data. The official mobile documentation describes it as a native mobile extension of Rock RMS for applications linked to Rock ([Mobile Docs](https://community.rockrms.com/developer/mobile-docs)).

For agent work, the most important mental model is this:

- Rock Core stores the mobile app configuration, pages, blocks, content, colors, API connection details, and deployment bundle.
- The Rock Mobile shell is the compiled native app distributed through iOS and Android app stores, usually through App Factory.
- XAML defines much of the mobile UI surface.
- Commands define behavior: navigation, browser opening, app actions, clipboard, reload, calendar integration, haptics, and other native or Rock-specific interactions.
- Controls provide reusable visual and behavioral elements such as WebView, Context Menu, ExecuteCommand, cards, media players, countdowns, forms, and other XAML surfaces.
- Blocks bridge Rock feature areas into the mobile app: CMS, check-in, communication, connection, core, CRM, events, finance, groups, prayer, reminders, security, and workflow.
- Deployment publishes server-side mobile configuration changes so devices can load the updated app bundle at launch or refresh ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).
- Shell updates are separate from Rock configuration deploys. Shell updates are required for new native shell capabilities, platform SDK compliance, and store availability ([Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements)).

An agent diagnosing or implementing Rock Mobile should always separate four layers before making conclusions:

1. **Core data/configuration**: application record, page tree, block settings, app colors, API key, push/giving/auth settings, security permissions, Rock version.
2. **Deployed mobile bundle**: whether the current app configuration has been deployed, whether dynamic content bypasses deployment, whether the device has pulled the latest bundle.
3. **Native shell version**: whether the installed app shell supports the command/control/block property being used.
4. **Device/platform behavior**: iOS versus Android differences, OS minimums, WebView scaling, safe area, push permissions, app store review credentials, and MAUI migration behavior.

Most mobile failures are not “the app is broken.” They are mismatches between those layers: a block requiring a newer shell, a Core feature requiring a newer Rock server, a page changed but not deployed, a WebView missing mobile viewport markup, an Android keystore or store-account issue, a push transport configuration gap, an iOS-only behavior difference, or a command introduced in a later shell than the app currently uses.

When source material is thin, do not invent internal database behavior. Inspect the live Rock instance: mobile application configuration under Admin Tools > CMS Configuration, page/block settings, API key assignment, security authorization, defined communication transports and mediums, mobile deployment status, Rock server version, app shell version, and any relevant logs or app-store/App Factory records.

## 2. Scope And Terminology

This guide covers Rock Mobile as represented in the source pack: mobile shell concepts, XAML, commands, controls, blocks, app configuration, App Factory publishing concerns, release caveats, OS requirements, and related areas such as API, check-in, CMS, and security.

The guide does not attempt to reproduce every mobile block reference page because the pack mostly includes index-level hydrated records for many block groups rather than full block property details. Where the source pack only proves that a block family exists, this guide says what to inspect in a live Rock instance or the official block page rather than inventing block settings.

Use these terms consistently:

**Application**  
The configured Rock Mobile app in Rock. It includes mobile pages, blocks, branding, configuration, and visual settings. The mobile lexicon describes the application as the collection of mobile blocks, content, branding, and configurable areas ([Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon)).

**Core**  
The Rock server powering the mobile app. Core provides APIs, data, blocks, authentication, content, deployment bundles, and server-version-dependent behavior ([Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon)).

**Shell**  
The compiled native iOS/Android app. Shell version determines which native commands, controls, MAUI behavior, OS SDK support, and native capabilities are available. Some docs mark features with mobile-shell badges such as `M v7.0` ([Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)).

**App Factory**  
The publishing service for Rock Mobile apps. App Factory handles compiling and publishing apps to the stores, and is the normal path for churches that do not compile and publish native shells themselves ([App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory)).

**Deploy**  
A Rock-side action that publishes configuration, pages, blocks, and content for app users. It is not the same as an app-store shell update. Deployment is required after many server-side mobile configuration changes ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).

**Device Type**  
The app’s device context, usually Phone or Tablet, used by Rock Mobile to choose appropriate layouts ([Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon)).

**XAML**  
The markup used to define Rock Mobile native layouts and controls. Agents should treat XAML as native UI markup, not as HTML. CSS support exists but is constrained by .NET MAUI styling support ([Styling](https://community.rockrms.com/developer/mobile-docs/styling)).

**Command**  
An executable action attached to a control or behavior. Commands are commonly bound to `Command` properties and may accept a parameter. The docs emphasize that command structure is consistent enough that a command used by a button can be reused by other command-capable controls or gestures ([Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)).

**Control**  
A XAML visual or behavioral element. Rock Mobile supplies controls such as WebView, Context Menu, ExecuteCommand, CommandReference, cards, media controls, and extensions.

**Block**  
A Rock feature unit rendered on a mobile page. Blocks exist across CMS, check-in, communication, connection, core, CRM, events, finance, groups, prayer, reminders, security, and workflow areas as shown by the mobile developer navigation ([Developers](https://community.rockrms.com/developer/mobile-docs/developers)).

**Dynamic Content**  
A mobile content behavior where selected content changes can appear without a new deploy. The deployment docs specifically distinguish normal app changes requiring deployment from dynamic content that can update without redeploying ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).

## 3. Rock Mobile Mental Model

Rock Mobile is a three-part system: Rock Core configuration, native shell runtime, and device/platform environment.

### Rock Core Configuration

A mobile app begins in Rock under Admin Tools > CMS Configuration > Mobile Applications. The first-app guide says to create or select a mobile application from that area ([Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app)). The app configuration then determines application type, orientation, pages, API key, flyout XAML, and homepage routing logic ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)).

The Core side owns:

- Mobile application record.
- Application type: blank, flyout, or tabbed.
- Lock orientation setting.
- Mobile page tree.
- Page blocks and block settings.
- API key used by the mobile app.
- Flyout XAML for navigation.
- Homepage routing logic.
- Palette colors and styling values.
- Content and dynamic content.
- Push-notification configuration.
- Communication transport and mediums.
- Auth/login configuration and security rules.
- Deployment state.

If an agent changes mobile pages, block settings, application colors, app configuration, or navigation, assume a deploy is required unless the change is explicitly a dynamic content path ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).

### Native Shell Runtime

The shell is the native app that interprets the deployed mobile configuration and renders pages. The shell includes native dependencies and features. Commands, controls, and behaviors can require a specific shell version. The Core & Shell Dependencies doc explains that features may be tagged with a mobile shell requirement (`M`) and/or a Rock Core requirement (`C`) ([Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)).

Agent rule: never assume a feature is available because the Rock server was upgraded. Confirm both:

- Rock Core version.
- Installed shell version in App Factory records, release notes, device app version, or app-store build metadata.

A shell update is not normally required for every Rock-side content change, but it is required when the app needs new native capabilities, bug fixes in the shell, MAUI changes, OS support, store compliance, or feature tags that exceed the current shell version.

### Device And Platform Environment

Rock Mobile runs in iOS and Android contexts. Some features are platform-specific or behave differently across platforms. The Context Menu docs explicitly warn that Android limitations mean some menu features are richer on iOS and not every property translates to Android ([Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu)). The WebView docs warn that WebView content is contained and cannot control the native shell or native page ([Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)).

The MAUI migration is a major mental-model shift. Rock Mobile V6 moved from Xamarin Forms to .NET MAUI because Xamarin Forms support ended in May 2024. The migration guide highlights layout changes, scrolling, request sizing, removal or replacement of older elements, safe-area padding, and shell-update forcing as topics that can affect existing apps ([Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)).

### Deployment Flow

A typical Rock Mobile configuration change flows this way:

1. Admin or developer updates mobile app configuration, pages, blocks, XAML, colors, or content.
2. The application page shows deployment status.
3. The admin clicks Deploy.
4. Rock produces a new deployed bundle.
5. The app pulls the latest deployment when opened at the splash/launch screen or when reloaded under the documented testing flow.
6. Dynamic content may update without a new deployment if the relevant content block is configured for that behavior ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).

If a device does not reflect changes, inspect deployment status first, then whether the device has reloaded from the splash/launch process, then whether the changed content is dynamic or non-dynamic, then shell/Core version compatibility.

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. Official Rock Mobile developer docs and Rock Mobile release notes.
2. Rock Core source-code or generated model/view-model records.
3. Official Rock docs, RockU, Model Map, and release notes when present in the pack.
4. Community recipes only as examples, never as authoritative behavior.

This source pack is strongest for:

- Mobile app creation and configuration.
- Deployment behavior.
- Shell/Core dependency concept.
- App Factory publishing concerns.
- OS version requirements.
- MAUI migration.
- Commands and a subset of controls.
- Release-note feature and bug history.
- Check-in view-model/source-code landmarks from Rock Core.
- Push notifications, app-store metadata, Android keystore, Rock logins, image resources, in-app giving.
- Block family coverage via official mobile docs navigation.

This source pack is thin for:

- Full property tables for every mobile block.
- Complete command parameter definitions for all commands.
- Exact database table relationships for mobile application records.
- Current App Factory operational policies beyond the hydrated docs.
- Exact source-code implementation for Rock Mobile shell internals.
- Full Model Map records.

When a fact needs live verification, inspect the live Rock instance rather than guessing. Common live checks include:

- Admin Tools > CMS Configuration > Mobile Applications.
- Specific mobile application detail page.
- Application type, orientation, API key, page list, flyout XAML, homepage routing.
- Page/block tree and block settings.
- Deployment status and last deploy time.
- Dynamic Content settings.
- Rock server version.
- Mobile shell version/build in App Factory or store metadata.
- Security permissions on pages, blocks, APIs, communication features, and content channels.
- Communication transports, push medium settings, Firebase/service-account configuration.
- Person/device/push notification records if troubleshooting push delivery.
- Exception log and communication history.
- App-store review credentials and developer-account invitations.

Community recipes in the pack demonstrate real-world patterns, such as live captions/translation via a mobile layout and WebView-style integration ([Recipe 469](https://community.rockrms.com/recipes/469)) or a countdown-driven refresh/redirect pattern ([Recipe 402](https://community.rockrms.com/recipes/402)). Treat these as examples to adapt after security and performance review; the recipe pages themselves warn that community recipes are not reviewed or endorsed by the Rock core team.

## 5. Core Configuration And Data Model

### Creating The Mobile Application

The official first-app guide starts under Admin Tools > CMS Configuration > Mobile Applications, where a user can create a new app or open an existing one ([Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app)). Agents should not assume mobile apps live under the normal website page tree. Mobile applications have their own configuration surface.

Minimum implementation checklist:

- Confirm the mobile application record exists.
- Capture the application identifier used by the Rock Mobile Core app testing flow.
- Confirm the app’s API URL.
- Confirm the app’s API key.
- Confirm application type.
- Confirm page tree and homepage.
- Confirm deploy status.

The source pack references “Application Id,” “API URL,” “API Key,” and “Rock Core App Connection” in the deployment/testing doc headings ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)). If those values are needed operationally, inspect the app’s deployment/testing documentation panel in the live Rock UI.

### Application Type

The App Configuration doc lists these application types:

- Blank, marked by the docs as not recommended.
- Flyout, marked by the docs as recommended.
- Tabbed ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)).

Operational interpretation:

- Use **Flyout** when you want a common mobile app navigation pattern with a menu, many pages, and flexible growth.
- Use **Tabbed** when the primary app experience is a small set of persistent top-level destinations.
- Avoid **Blank** unless a custom shell/navigation strategy has been intentionally designed and tested.

When troubleshooting navigation, application type matters. A flyout problem may be in Flyout XAML, page registration, page security, shell version, or a page’s root XAML. Release notes mention a v2.1 fix for Flyout Shell behavior when `ListItem` was not the root XAML element ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

### Lock Orientation

The App Configuration doc includes Lock Orientation as a configuration area ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)). The source pack does not provide the full option list. In a live instance, inspect whether orientation is unlocked, portrait-locked, landscape-locked, or otherwise represented. For most church mobile apps, portrait should be the default expectation unless tablet/kiosk or media-display workflows demand another orientation.

Agent check:

- If layout works on one device but breaks on another, verify orientation settings.
- If a tablet layout is not used, verify device type and orientation.
- If the shell rotates unexpectedly, verify app config and native shell behavior.

### Application Pages

Application pages are the mobile page tree. The App Configuration doc lists Application Pages as a core configuration area ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)). The source pack does not include a database schema for mobile pages, so agents should inspect the live page list in the mobile application record.

For each page, capture:

- Page name.
- Page GUID/identifier if linking through commands, push notifications, or redirects.
- Page route or order if visible.
- Blocks on page.
- Security authorization.
- Phone layout XAML.
- Tablet layout XAML.
- Whether the page is native-block-based or URL/WebView-style.
- Query string dependencies.
- Required shell/Core versions for blocks and controls.

Release notes for v3.0 mention support for pages displaying a URL instead of native Rock blocks ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). If a mobile page behaves like a website wrapper, verify whether it is configured as a URL page, as a WebView control inside XAML, or as a native mobile block page.

### API Key

The App Configuration and Deploying docs both point to API Key as part of mobile configuration/testing ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration), [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)). The source pack does not enumerate the exact API permissions required. Do not assume an API key is valid because it is present.

Agent checks:

- Confirm the API key field is populated.
- Confirm the key belongs to the intended Rock user or API identity.
- Confirm that identity has only the permissions required by the app.
- Verify page and block authorization separately from API key presence.
- If a mobile app loads but data calls fail, inspect Rock security, API endpoint authorization, exception logs, and the specific block action/API endpoint.

### Flyout XAML

Flyout XAML is a configuration section in the official app configuration doc ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)). It defines the flyout navigation surface. Because XAML is interpreted by the mobile shell, failures can come from syntax, missing controls, unsupported shell version, invalid bindings, security-hidden pages, or root-element assumptions.

When editing or diagnosing Flyout XAML:

- Validate that page references point to mobile app pages, not website pages.
- Confirm referenced icons or image resources exist and are available in the deployed bundle or compiled shell.
- Confirm command bindings match the current shell.
- Confirm required controls are supported by shell version.
- Test both iOS and Android if the flyout includes context menus, platform-specific layout, or native effects.
- Redeploy after XAML changes.

### Homepage Routing Logic

The App Configuration doc lists Homepage Routing Logic ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)). The pack does not include the full syntax. In a live app, inspect whether routing is based on login state, page parameters, campus, app state, or custom Lava/XAML logic. For agents, homepage routing is a high-risk area because it can make the app appear blank, send unauthenticated users into restricted pages, or break app-store review credentials.

Operational checks:

- Test signed-out launch.
- Test signed-in launch.
- Test app-store review login accounts.
- Test locked/non-confirmed account behavior if using login.
- Test launch after a push notification deep link.
- Test after logout.
- Test with no network or slow network if possible.

### Palette Colors And Styling Values

The Palette Color XAML extension lets XAML reference named application palette colors. The source pack lists color names available as of Rock Server 1.12.5, including `Text-Color`, `Heading-Color`, `Background-Color`, `App-Primary`, `App-Secondary`, `App-Success`, `App-Info`, `App-Danger`, `App-Warning`, `App-Light`, `App-Dark`, and `App-Brand` ([Palette Color](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color)).

Use palette references when XAML needs to follow app branding without hardcoding hex values. For live troubleshooting:

- Inspect application colors in the mobile app configuration.
- Inspect the active `Mobile Style Framework`; Standard, Blended, and Legacy modes materially change how much of the app can respond to dark mode.
- Confirm CSS and XAML color references use the same intended palette names.
- Prefer semantic interface and accent values such as `Interface-Strongest`, `Interface-Softest`, `Primary-Strong`, and `Primary-Soft` over hardcoded white/black/brand colors when the surface must survive light and dark appearances ([Colors](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/colors), [Migrating](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/migrating)).
- Confirm dark mode behavior on iOS and Android. Release notes record a v4.0 fix for a dark-mode picker color issue in `BibleBrowser` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- Confirm shell version if a color property is ignored. Release notes record a v7.0 fix where `Tag.TextColor` was not respected ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

For detailed dark-mode x-ray fields, CSS/XAML examples, shell chrome checks, and screenshot evidence rules, use [Rock Mobile CSS X-Ray Design Resource](resources/css-xray-design-resource.md#dark-mode-and-color-scheme-workflow).

## 6. Primary Entities And Relationships

The source pack does not provide full Rock database schema records for Rock Mobile application tables. The relationships below are operationally useful but should be verified in a live Rock instance or Model Map before writing SQL, migrations, or automation.

### Mobile Application Relationship Map

The official [Rock Mobile documentation](https://community.rockrms.com/developer/mobile-docs) and [Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes) define the supported shell and publishing surface. Use the version-matched Model Map and live app configuration to verify exact page, block, API-key, security, communication, and deployment relationships before changing records.

A Rock Mobile implementation typically includes:

- **Mobile Application**: top-level app configuration.
- **Pages**: mobile app pages attached to the application.
- **Blocks**: feature blocks placed on pages.
- **Layouts/XAML**: phone/tablet layout markup for pages, flyout, and custom content.
- **API key**: identity for app/Core communication.
- **Deployment bundle**: published state consumed by devices.
- **Content entities**: content channels, structured content, media, workflows, events, groups, prayer requests, communications, depending on blocks.
- **Security entities**: users, roles, authorization rules, login records.
- **Communication entities**: transports, mediums, push subscriptions/device identifiers.
- **Store/app publishing records**: App Factory, Apple, Google, keystore, developer accounts.

Before making data changes, locate the specific records in Rock UI or Model Map. Do not infer table names from mobile docs alone.

### Page, Block, And Security Relationships

A mobile page can host one or more mobile blocks. Each block may read and write Rock data. Page security and block-specific security both matter. If a block fails only for anonymous users or only for a specific role, inspect:

- Page authorization.
- Block authorization.
- Entity-specific security, such as content channel item visibility, group access, finance account visibility, or workflow type security.
- API key user permissions.
- Current person context after login.

The mobile developer navigation lists Security as a block family ([Security Blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security)), and the broader mobile docs list login, Auth0, and Entra under CMS login ([Developers](https://community.rockrms.com/developer/mobile-docs/developers)). The pack does not include full login/Auth0/Entra pages, so verify login provider details in live configuration.

### Check-In Source-Code Landmarks

The source pack includes multiple Rock Core view-model files for check-in. These are not mobile-shell internals, but they are useful for understanding next-generation check-in data exchanged by blocks and APIs.

Key source-code landmarks:

- `CheckInSecurityCodesSettingsBag` configures security-code length and format. The code comments state that Rock generates alpha-numeric characters first, then alphabetic, then numeric, and total length is the sum of all configured counts ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs), [TypeScript source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/checkInSecurityCodesSettingsBag.d.ts)).
- `CheckInKioskFeaturesSettingsBag` includes kiosk features such as allowing checkout at kiosk, enabling presence, and allowing removal of “Can Check-in” relationships without supervisor login for next-gen check-in ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInKioskFeaturesSettingsBag.cs)).
- `KioskConfigurationBag` contains kiosk details, check-in template, and enabled areas for a kiosk startup payload ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/KioskConfigurationBag.cs)).
- `SavedKioskConfigurationBag` stores campus, template, kiosk device, area ids, and theme-like saved configuration details in browser local storage for web kiosk configuration retrieval ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SavedKioskConfigurationBag.cs)).
- `ActiveAttendanceBag` tracks a minimal attendance record with encrypted identifiers for attendance, group, location, and status ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ActiveAttendanceBag.cs)).
- `ReprintAttendanceBag` contains person name, security code, group, location, schedule, and attendance identifiers needed to reprint labels ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ReprintAttendanceBag.cs)).
- `PrintResponseBag` returns new labels, legacy labels, and error messages for print operations ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/PrintResponseBag.cs)).
- `EditFamilyResponseBag`, `SaveFamilyOptionsBag`, and `SaveFamilyResponseBag` describe registration/edit-family payloads and outcomes, including SMS toggles, address display requirements, family attributes, relationship choices, grade-prompt rules, and whether check-in after registration is allowed ([EditFamilyResponseBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs), [SaveFamilyOptionsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyOptionsBag.cs), [SaveFamilyResponseBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyResponseBag.cs)).
- `GetScheduledLocationsResponseBag` returns schedules and scheduled group-location items for selection ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/GetScheduledLocationsResponseBag.cs)).
- `LocationStatusItemBag` indicates whether a location is currently open or closed ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/LocationStatusItemBag.cs)).
- `SubscribeToRealTimeResponseBag` includes identifier mappings used when subscribing to real-time check-in messages ([C# source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SubscribeToRealTimeResponseBag.cs)).

These records matter when an agent is diagnosing mobile check-in or proximity attendance because they show the operational shape of kiosk configuration, attendance state, label printing, scheduled location selection, and family registration. They do not prove every UI behavior. Verify the relevant block action, Rock version, and app shell in the live instance.

## 7. Common Rock Mobile Workflows

### Build A First App

Use the official sequence:

1. Create the mobile application in Admin Tools > CMS Configuration > Mobile Applications ([Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app)).
2. Configure application type, orientation, pages, API key, flyout XAML, and homepage routing ([App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)).
3. Add content/pages/blocks using mobile-compatible blocks.
4. Deploy the app.
5. Test using the Rock Mobile Core app connection details, including Application Id, API URL, and API Key as applicable ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).

Agent implementation guardrail: after every configuration change, record whether a deploy is required and whether the device must reload.

### Change A Page Or Block

Workflow:

1. Identify mobile application.
2. Identify page.
3. Identify block instance.
4. Inspect block settings and required shell/Core tags.
5. Make the change.
6. Deploy unless it is dynamic content.
7. Reload app from splash/launch or test workflow.
8. Test signed-out and signed-in if security or personalization is involved.
9. Test iOS and Android for native controls, WebView, context menu, push, or media behavior.

### Add A WebView Integration

The WebView control embeds a web page in a mobile app page and wraps the platform WebView with an initial activity indicator ([Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)). The docs warn that WebView content is contained and cannot affect the native shell or native page. Therefore, a WebView button cannot directly run a native Rock Mobile navigation command unless bridged by a supported mechanism not present in this source pack.

Agent checklist:

- Confirm the external page is mobile-responsive.
- Add a mobile viewport meta tag to the web page as the WebView docs recommend ([Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)).
- Do not place WebView in layout conditions where it has no explicit size or collapses invisibly.
- Confirm authentication/session expectations.
- Verify iOS and Android rendering.
- Verify external content does not visually fight native navigation bars or tab bars. The in-app giving doc makes a similar warning for embedded giving pages ([In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)).
- Confirm privacy/security implications for third-party content.

Community examples include embedding live captions/translation into Rock Mobile ([Recipe 469](https://community.rockrms.com/recipes/469)). Treat that as a pattern, not a guarantee of best practice.

### Configure Push Notifications

The push-notification doc describes mobile push as a communication path that can target individuals, communication lists, or everyone with the app installed, even if not signed in ([Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)). It lists major areas: authoring notifications, configuration, service account JSON, communications, communication transport, communication mediums, setting up the app, sending, alternative methods, and personal device ID.

Operational flow:

1. Confirm the shell/app was built with push capability through App Factory.
2. Configure the required service account JSON or provider credentials in Rock.
3. Confirm communication transport exists and is active.
4. Confirm communication medium is configured.
5. Confirm the mobile app setup is completed.
6. Confirm devices have requested and granted notification permissions.
7. Send a test push to a known person/device.
8. Inspect communication records and any exception logs.
9. Test open actions: Link to Mobile Page or Show Details. The push doc notes that Link to Mobile Page should reference a mobile app page, not a non-mobile site page, and can include query strings ([Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)).

Release caveats:

- v2.2 fixed an iOS push-notification delivery issue under a specific settings combination ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added ability to detect push-notification state in XAML and an app value indicating whether push permission had been requested ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

### Publish Or Update Through App Factory

App Factory exists because compiling and publishing native apps requires platform expertise ([App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory)). App Factory can publish under either the organization’s Apple/Google developer accounts or Triumph Tech’s accounts, depending on the arrangement ([Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

Publishing checklist:

- Decide whose developer accounts host the app.
- If using organization-owned accounts, invite App Factory with required Apple/Google access.
- If using Triumph-hosted accounts, understand delisting risk if the subscription ends; the Developer Accounts doc notes apps hosted under Triumph accounts may be delisted after subscription end ([Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).
- Provide app-store product metadata: app name, icon, subtitle, screenshots, description, promotional text, keywords, categories, support URL, marketing URL, copyright ([App Store Product Page](https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page)).
- Provide Android keystore if replacing an existing Android app. The Android Keystore doc states updates must be signed consistently and losing the keystore can mean losing update access unless Play App Signing applies ([Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)).
- Provide app-store review Rock login credentials. The Rock Logins doc says app stores require credentials for review and recommends separate Apple and Google review logins with no special permissions beyond demo access ([Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins)).
- Provide image resources to compile into shell if needed, knowing those require store updates to change ([Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources)).
- Confirm in-app giving compliance if native or WebView giving is present ([In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)).

### Upgrade From Xamarin Forms To MAUI

Rock Mobile V6 is the MAUI transition. The migration doc explains that Xamarin Forms lost Microsoft support in May 2024 and that V6 moved to .NET MAUI for support, performance, SDK access, features, controls, and bug fixes ([Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)).

Migration workflow:

1. Inventory all custom XAML.
2. Inventory custom CSS and Downhill classes.
3. Inventory platform-specific extensions such as Rock’s legacy `OnDevicePlatform`, deprecated in V6 and later in favor of built-in MAUI platform support ([On Device Platform](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform)).
4. Check layout behavior, scrolling, `WidthRequest`, `HeightRequest`, old `Frame`/`StyledView` usage, Zone control usage, and safe-area padding topics from the migration doc ([Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)).
5. Test pages on iOS and Android.
6. Test push, login, media, WebView, flyout/tab navigation, and dynamic content.
7. Review release notes for known v6/v7 follow-up fixes.

## 8. Commands Deep Dive

Commands are the behavior layer of Rock Mobile. The docs frame commands as a shared structure used by .NET MAUI and Rock Mobile for actions and events. A control exposes a `Command` property or specialized command property; the command may accept a parameter; and the same command pattern can be reused across different command-capable contexts ([Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)).

### Command Binding Pattern

Confirm command names, binding context, and parameter contracts against the official [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands) reference for the deployed shell version. The example below is a pattern only; verify it on the target page and both supported platforms.

A typical command pattern is:

```xml
<Button
    Text="Open"
    Command="{Binding OpenBrowser}"
    CommandParameter="https://example.org" />
```

This is an original example following the documented command model, not a copied source example. The exact command names and parameter types must be confirmed against the command reference and shell version.

Agent checks:

- Is the command name correct for the current shell?
- Is the command exposed by the current binding context?
- Does the control support the `Command` property or a named command property?
- Does the command require a structured parameter object?
- Does the command require a mobile page GUID, route, URL, or query string?
- Was the page deployed after adding the command?
- Is the failure platform-specific?

### CommandReference

`CommandReference` lets a command be passed as a parameter to another command or object. The source pack says it has `Command` and `CommandParameter` properties, and in mobile shell v3.0 the command parameter became the default content property ([Command Reference](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/command-reference)). This is important when composing commands such as aggregate or multi-step command flows.

Use cases:

- Set context, then navigate.
- Run a command from a menu action.
- Pass a command into a reusable control.
- Combine state mutation and UI feedback.

Version caveat: if syntax using child content for `CommandParameter` fails, verify shell version is at least the version where that behavior was introduced.

### ExecuteCommand Control

`ExecuteCommand` was added in shell v7.0. It is a developer control that executes a command on initialization and can delay or repeat execution. The docs list properties including `Delay`, `Enabled`, `Repeat`, `RepeatCount`, `StartWithExecution`, `Command`, and `CommandParameter` ([Execute Command](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/execute-command)). The v7.0 release notes also record the new ExecuteCommand control ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Use cases:

- Delayed reload.
- Periodic state refresh.
- Deferred navigation after rendering.
- Timed UI state changes.
- Lightweight polling where a block does not provide native refresh behavior.

Guardrails:

- Avoid unbounded repeats unless the page is designed for it.
- Consider battery and network cost.
- Do not use `ExecuteCommand` to hide a server-side data problem.
- Confirm it does not run repeatedly after navigation or page resume in a way that causes duplicate writes.
- Confirm shell v7.0 or later.

### Commands From Release Notes

The release notes establish a timeline for several command capabilities:

- v2.0 added `WriteInteraction`, allowing an interaction write after an action ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v2.0 added logout parameter syntax for reload or navigation after logout ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added `AddEventToCalendar` for device calendar insertion ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added `SetViewProperty` for changing a view property in response to an action ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added `PerformHapticFeedback` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added `MapAddress` to open an address or coordinates in a native mapping app ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added a command to open application settings ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v4.0 added `ReloadPage` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v4.0 added toast functionality used by `ShowToast` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v7.0 added `CopyToClipboard` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v7.0 fixed `AddEventToCalendar` behavior ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v7.0 fixed a MAUI popup overlay issue for `ShowPopUp` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Agent rule: if a command does not work, check the shell version before debugging XAML. A v3.0 command will not be reliable in a v2.x shell; a v7.0 command such as `CopyToClipboard` or `ExecuteCommand` requires v7.0.

### Operational Command Troubleshooting

Use the official [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands) reference and [Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes), then inspect the target page's deployed XAML, binding context, parameters, security, shell version, and platform logs. A command that works in preview or one operating system is not proof that the production bundle is correct.

Use this branch:

1. **Command does nothing**
   - Verify shell supports command.
   - Verify binding context exposes command.
   - Verify control supports command property.
   - Verify parameter type and syntax.
   - Check page deployed.
   - Check app reloaded.

2. **Command runs on one platform only**
   - Check platform limitations.
   - Check OS permissions.
   - Check release notes for platform-specific fixes.
   - Test latest shell.

3. **Navigation command opens wrong page**
   - Confirm mobile page GUID/route, not website page.
   - Check query string.
   - Check security.
   - Check homepage routing after login/logout.

4. **Command writes duplicate records**
   - Check repeated triggers.
   - Check `ExecuteCommand` repeat settings.
   - Check page lifecycle/resume behavior.
   - Check button double-tap prevention or command enabled state.

5. **Popup/toast/media command has visual issues**
   - Check MAUI shell version.
   - Check v7.0 popup fix.
   - Check dark mode and safe area.
   - Check whether command is called before page render completes.

## 9. Controls Deep Dive

Controls are the XAML building blocks for Rock Mobile UI. They may wrap MAUI controls, add Rock-specific behavior, or expose native capabilities.

### WebView

Rock’s WebView control wraps the standard WebView and adds an initial activity indicator until the page loads ([Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)). It should generally be used instead of the plain MAUI WebView according to the docs. Important constraints:

- WebView content is contained.
- WebView content cannot affect the app shell or native page.
- A web page embedded in WebView should include a mobile viewport meta tag.
- WebView layout must have enough size to render; if a WebView appears blank, inspect parent layout sizing first.

Operational uses:

- External giving page fallback.
- Live captions or translations.
- Legacy web content.
- Third-party integrations.
- Temporary migration bridge while native blocks are built.

Risks:

- Inconsistent authentication.
- Poor mobile scaling.
- Navigation conflict with native bars/tabs.
- External content downtime.
- App-store review concerns.
- Accessibility gaps.

### Context Menu

The Context Menu control family supports native context menus attached to many controls. The docs identify `Menu`, `MenuAction`, and `MenuGroup` as the main pieces and warn that iOS has richer native support than Android ([Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu)).

Use context menus for:

- Secondary actions.
- Share/copy/save actions.
- Content item actions.
- Admin or leader-only quick actions.
- More options without cluttering the primary mobile layout.

Guardrails:

- Do not hide primary user flows inside context menus.
- Test Android; not all iOS menu properties translate.
- Keep menu actions permission-aware.
- Use clear labels and icons if supported.
- Verify commands attached to `MenuAction`.

### PaletteColor XAML Extension

The Palette Color extension lets XAML use named app colors ([Palette Color](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color)). Use it instead of hardcoded colors when the color is part of the app brand or semantic palette.

Operational pattern:

```xml
<Label
    Text="Welcome"
    TextColor="{Rock:PaletteColor App-Primary}" />
```

This example is short and follows the documented pattern. Confirm namespace usage in the live XAML context.

### OnDevicePlatform And MAUI Platform Support

The Rock-specific On Device Platform extension is deprecated in Rock Mobile V6 and later because .NET MAUI has a built-in XAML platform extension ([On Device Platform](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform)). Agents should flag legacy `OnDevicePlatform` usage during MAUI migration.

Use platform-specific values carefully:

- Prefer shared layout when possible.
- Use platform-specific adjustments for native spacing, safe area, menu behavior, and visual polish.
- Test both iOS and Android.
- Avoid platform forks that create unmaintainable duplicate UI.

### Cards And Styling

The source pack includes official card pages for card elements and CSS card styling ([Elements of a Card](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/cards/elements-of-a-card), [Styling Cards With CSS](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/cards/styling-cards-with-css)). Hydrated excerpts are navigation-heavy rather than property-rich, so agents should use the official pages for exact card structure.

Practical guidance:

- Use cards for repeated content items, not as a universal layout wrapper.
- Keep tap targets large enough for mobile.
- Avoid over-nesting.
- Use palette and Downhill classes consistently.
- Verify card content does not overflow on smaller phones.
- Verify text color in light/dark mode.

### Behaviors

The behaviors docs are present as a mobile controls category ([Behaviors](https://community.rockrms.com/developer/mobile-docs/essentials/controls/behaviors)). Release notes for v7.0 specifically add `EventToCommandBehavior`, which triggers a command when a specified event occurs ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). This is useful when a control event needs to invoke command logic without custom shell code.

Agent checks:

- Confirm shell v7.0 for `EventToCommandBehavior`.
- Confirm event name is valid for the target control.
- Confirm command is available in binding context.
- Avoid event loops where command changes the property that re-triggers the event.

### Media Controls

Release notes add or modify media controls over time:

- v2.0 added a new `MediaPlayer` control with improved on-screen controls and common UI between devices ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v2.0 added `MediaProgressBar` for better media-progress compatibility than a plain slider ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v3.0 added support for transport media controls on lock screens ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v7.0 added `AllowsPictureInPicturePlayback` to `MediaPlayer` ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v7.0 fixed crashes caused by `PlayAudio` and `PlayVideo` media commands ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Operational media checks:

- Verify stream URLs.
- Verify app transport/security requirements.
- Test background and lock-screen behavior.
- Test Android full-screen player behavior; v2.0 fixed a case where screen elements partially showed through full-screen media on Android ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- Test PiP only on shell v7.0+ and supported devices.

### Form Fields And Responsive Inputs

The source pack includes legacy form-fields styling and a v4.0 release note for responsive memo fields in mobile workflows ([Form Fields](https://community.rockrms.com/developer/mobile-docs/styling/legacy/styling-components/form-fields), [Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). When workflows render poorly, distinguish:

- Form field block settings.
- Mobile shell version.
- CSS class support.
- MAUI layout behavior.
- Keyboard overlap/safe-area behavior.
- Memo/long-text responsiveness.

## 10. Mobile Releases Deep Dive

### Release Version Table

The OS Version Requirements doc provides minimum OS requirements by shell version ([OS Version Requirements](https://community.rockrms.com/developer/mobile-docs/developers/os-version-requirements)):

| Shell | Release Date | Android SDK | Android Version | iOS Version |
|---|---:|---:|---:|---:|
| v7.0 | 07/16/2025 | 25 | 7.1 | 14.0 |
| v6.0 | 10/20/2024 | 25 | 7.1 | 12.0 |
| v5.0 | 10/31/2023 | 25 | 7.1 | 12.0 |
| v4.1 | 05/09/2023 | 25 | 7.1 | 12.0 |
| v4.0 | 02/03/2023 | 25 | 7.1 | 12.0 |
| v3.0 | 06/17/2022 | 23 | 6.0 | 12.0 |
| v2.2 | 01/19/2022 | 23 | 6.0 | 12.0 |
| v2.1 | 12/15/2021 | 23 | 6.0 | 12.0 |
| v2.0 | 09/15/2021 | 23 | 6.0 | 12.0 |
| v1.0 | 08/24/2020 | 23 | 6.0 | 8.0 |

Agent warning: do not confuse “Android SDK” in this table with current Google Play target API requirements. The shell update requirements doc says Google updates Android/API policy over time and existing apps must target recent API levels within policy windows or may become unavailable to new users on newer OS versions ([Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements)). Verify current App Factory guidance and app-store policy before release planning.

### v7.0

Rock Mobile v7.0, released July 16, 2025, is the latest shell version in this source pack. Highlights include:

- ExecuteCommand control.
- CopyToClipboard command.
- EventToCommandBehavior.
- Anchor-based navigation support that scrolls to a specific element when the page loads.
- Proximity Attendance using BLE beacon detection for check-in/check-out.
- Chat View block.
- Tabler Icons support.
- MediaPlayer PiP property.
- AddEventToCalendar fix.
- Tag TextColor fix.
- Html FollowHyperlinks fix.
- ShowPopUp MAUI overlay fix.
- Group Schedule Signup scheduled location fix.
- Workflow Entry form result message fix ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Operational significance:

- If implementing command automation, prefer v7.0 where possible.
- If using proximity attendance, verify BLE permissions, beacon setup, check-in configuration, Core version requirements, and device platform behavior.
- If troubleshooting MAUI popup or hyperlink behavior, v7.0 may contain relevant fixes.
- iOS minimum rises to 14.0 in v7.0 ([OS Version Requirements](https://community.rockrms.com/developer/mobile-docs/developers/os-version-requirements)).

### v6.0

v6.0, released October 20, 2024, is the MAUI transition version. Release notes list a minimum Rock version of v12.6 in the hydrated release-note excerpt and include broad design-system updates for mobile blocks ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). The migration doc explains the move from Xamarin Forms to .NET MAUI ([Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)).

Operational significance:

- Expect layout differences.
- Audit deprecated controls.
- Re-test scrolling, sizing, safe-area padding, and old styling.
- Expect design-system changes across mobile blocks.

### v5.0 And Earlier

The source pack includes fewer detailed records for v5.0, but release notes show ongoing CMS, communication, connection, core, CRM, group, mobile, and reminders changes ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). If working on a v5.0 or earlier app, assume MAUI migration is pending and plan a deeper regression pass.

### v4.0

v4.0, released February 3, 2023, added:

- Custom ScrollView with optional native iOS bounce disabling.
- Responsive Memo fields in mobile workflows.
- ReloadPage command.
- Toast functionality for ShowToast.
- Mobile-related user preferences.
- Dark-mode picker fix for BibleBrowser ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

### v3.0

v3.0, released June 17, 2022, added many foundational commands and blocks:

- Mobile Connection blocks for managing Connection Requests, requiring Rock Server v13.0.
- Add To Group mobile block.
- AddEventToCalendar.
- SetViewProperty.
- CommandReference default content node behavior.
- PrayForRequest command.
- PerformHapticFeedback.
- MapAddress.
- Command to open application settings.
- Push-notification detection in XAML.
- URL page support.
- Transport media controls.
- Login, registration, and onboarding improvements requiring Rock Server v13.0 for some features ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

### v2.x

v2.0 added MediaPlayer, Bible controls, Expander, RadioButtonList, WriteInteraction, logout parameter syntax, and MediaProgressBar. v2.1 and v2.2 include important iOS fixes for launch, iOS 15 rendering, tab-bar colors, onboarding crash, notifications, and iOS 12 launch behavior ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Operational significance: if a site still runs v2.x, expect many modern controls and fixes to be unavailable.

## 11. Related Rock Areas: Api, Check In, Cms, Security

### API

Rock Mobile depends on Core APIs. The pack proves API URL and API key are part of deployment/testing and app configuration ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app), [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)). It does not enumerate API endpoints or authorization rules.

Agent API checklist:

- Confirm API URL points to the intended Rock instance.
- Confirm SSL/TLS is valid.
- Confirm API key is active.
- Confirm API identity has correct permissions.
- Confirm endpoints used by blocks are allowed.
- Confirm CORS or transport issues only if a web layer is involved; native app calls may differ from browser calls.
- Check Rock exception logs for API errors.
- Check app shell version if the API payload shape changed.

### Check-In

Mobile check-in appears as an official block family ([Check-in Blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in)). v6.0 added the check-in block, and v7.0 added Proximity Attendance with BLE beacon detection plus check-in bug fixes ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Agent check-in tasks should inspect:

- Check-in configuration template.
- Kiosk configuration.
- Areas.
- Groups and locations.
- Schedules.
- Attendance records.
- Presence settings.
- Security code settings.
- Label printing configuration.
- Family registration/edit settings.
- Check-in page parameters.
- Proximity Attendance beacon configuration if applicable.
- Shell version and Rock Core version.

The source-code view-models give concrete check-in payload landmarks, including security-code settings, kiosk features, active attendance, scheduled locations, label printing, family editing, and real-time subscriptions ([CheckInSecurityCodesSettingsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs), [KioskConfigurationBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/KioskConfigurationBag.cs)).

### CMS

CMS is central to Rock Mobile. The mobile docs list CMS blocks such as Content, Content Channel Item View, Content Collection View, Daily Challenge Entry, Hero, Lava Item List, Login, Profile Details, Register, Structured Content View, Workflow Entry, and Voice Agent ([CMS Blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms)). The release notes include many CMS changes, commands, controls, and fixes ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).

Agent CMS checklist:

- Confirm content channel item status and dates.
- Confirm content security.
- Confirm Lava output is valid XAML where used.
- Confirm dynamic content setting.
- Confirm deployment after non-dynamic changes.
- Confirm login and registration block requirements.
- Confirm shell/Core tags for block settings.
- Confirm media and image URLs.

### Security

Security is relevant at several layers:

- Rock page/block authorization.
- API key identity.
- Person login and authentication provider.
- App-store review logins.
- Push notification targeting.
- Android keystore ownership.
- Developer-account access.
- Giving compliance.
- External WebView content.

The Android Keystore doc is a security-critical source: the signing key prevents unauthorized app updates and may be required when replacing an existing Android app ([Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)). The Rock Logins doc says app-store review credentials should remain active and do not need special permissions ([Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins)). The Developer Accounts doc warns about account ownership and App Factory access arrangements ([Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

Agent security rule: do not grant broad admin permissions to solve a mobile failure until the failing page/block/API/security path has been isolated.

## 12. Administration And Operational Guardrails

### Deployment Guardrails

- After app configuration changes, deploy.
- After page/block changes, deploy unless explicitly dynamic content.
- After color changes, deploy.
- After flyout XAML changes, deploy.
- After dynamic content changes, verify whether dynamic content is enabled and whether deploy is bypassed.
- After deploy, reload app to force latest bundle retrieval ([Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)).

### Shell Update Guardrails

The shell update requirements doc says Rock Mobile aims to keep shell versions compatible with future Rock Core versions so organizations are not required to update until they need latest additions, but OS and store policies still force occasional shell updates ([Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements)).

Maintain:

- Current shell version.
- Current Rock Core version.
- Minimum supported iOS/Android versions.
- Store policy deadlines.
- App Factory update path.
- Regression checklist for MAUI and platform behavior.
- Test accounts.

### App Store Guardrails

From App Store Product Page docs, collect and maintain:

- App name.
- Icon.
- Subtitle.
- Screenshots.
- Description.
- Promotional text.
- Keywords.
- What’s New text.
- Ratings/reviews strategy.
- Categories.
- Support URL.
- Marketing URL.
- Copyright ([App Store Product Page](https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page)).

The app name has a store metadata limit of 30 characters according to the source excerpt. Verify current Apple and Google policies before final submission because store metadata rules can change.

### Developer Account Guardrails

If hosted under the organization’s accounts:

- Keep Apple Developer and Google Play accounts active.
- Keep billing and legal agreements current.
- Maintain App Factory access.
- Use least privilege but enough publishing access.
- Preserve ownership continuity.

If hosted under Triumph accounts:

- Understand subscription dependency and possible delisting after subscription end ([Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)).

### Android Keystore Guardrails

- Treat keystore as a critical secret.
- Store in controlled password vault.
- Document alias/password ownership.
- Confirm Play App Signing status.
- If replacing an existing Android app, obtain original keystore early.
- Never email keystore casually.
- Verify App Factory’s secure transfer process ([Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)).

### Image Resource Guardrails

Image resources compiled into the shell improve performance and avoid network pop-in, but they increase app size and require store updates to change ([Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources)).

Use compiled resources for:

- Splash-critical brand assets.
- Frequently used static icons.
- Assets that must appear immediately.
- Assets not expected to change often.

Use network/CDN assets for:

- Event images.
- Sermon graphics.
- Rotating campaign art.
- Content team-managed media.
- Assets that benefit from server/CDN optimization.

### In-App Giving Guardrails

As of shell v7.0, Rock Mobile has native controls for in-app giving, according to the in-app giving doc ([In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)). WebView giving may be possible, but the doc warns that approval and configuration responsibility belongs to the submitting church/support partner/giving platform, and Apple approval may require nonprofit registration through Benevity ([In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)).

Agent checks:

- Confirm shell v7.0 if using native giving controls.
- Confirm giving platform compliance.
- Confirm Apple/Google submission requirements.
- Confirm Benevity registration status if Apple requires it.
- Confirm WebView page styling does not conflict with native navigation.
- Confirm finance security and account availability.
- Confirm test transactions in non-production mode when possible.

## 13. Developer, API, Lava, And Source-Code Landmarks

### XAML And Lava

Rock Mobile XAML can be generated or influenced by Lava in mobile blocks and layouts. The source pack includes mobile docs topics tagged with Lava and a community recipe using Lava schedule logic to choose between a countdown and an online-service button ([Recipe 402](https://community.rockrms.com/recipes/402)). Use Lava carefully because invalid output can produce invalid XAML.

Agent Lava checks:

- Render Lava output in a safe test context.
- Confirm XML escaping for dynamic text.
- Confirm date/time formatting.
- Confirm GUIDs/page references.
- Confirm anonymous versus authenticated Lava context.
- Confirm performance of Lava queries or commands.
- Avoid heavy SQL in mobile page render paths.

### Styling

Rock Mobile supports CSS-style classes, but the styling docs warn that XAML styling is first-class in .NET MAUI, CSS has a supporting role, not all web CSS properties are supported, and CSS property behavior in .NET MAUI differs from the web ([Styling](https://community.rockrms.com/developer/mobile-docs/styling)).

For selector targeting and design-audit work, use the concept resource [Rock Mobile CSS X-Ray Design Resource](resources/css-xray-design-resource.md). It gives a capture schema for page/block/app x-ray data, a selector ladder for `.ios`, `.android`, `.phone`, `.tablet`, `.page-*`, `.block-*`, control selectors, inherited selectors, and explicit XAML `StyleClass` hooks, plus Downhill utility-family notes grounded in Rock's public `Rock.DownhillCss` source. It now also includes a dedicated [dark mode and color-scheme workflow](resources/css-xray-design-resource.md#dark-mode-and-color-scheme-workflow) that ties Rock Mobile Colors, Style Framework migration, shell chrome, hardcoded color scans, and light/dark screenshot verification together. For block-specific selector callouts recovered from official docs screenshots, use [Rock Mobile Block Selector Image Audit](resources/block-selector-image-audit.md) and the machine-readable [mobile-block-selector-xray.jsonl](mobile-block-selector-xray.jsonl).

Agent styling checks:

- Prefer XAML styling for precise layout.
- Use Downhill/CSS classes for consistency where supported.
- Verify CSS properties are supported in MAUI.
- Check legacy styling pages when maintaining older apps.
- Verify design-system changes in v6.0.
- Test dark mode and platform differences, including shell chrome, WebView/HTML surfaces, form controls, tags/buttons/cards, image assets, and platform-specific iOS/Android behavior.

### Source-Code Landmarks

Use GitHub source snippets as deeper implementation landmarks, especially for check-in and Obsidian view-model payloads:

- Check-in security code configuration: [C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs), [TypeScript](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/checkInSecurityCodesSettingsBag.d.ts)
- Check-in kiosk features: [C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInKioskFeaturesSettingsBag.cs)
- Kiosk startup configuration: [C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/KioskConfigurationBag.cs)
- Web kiosk details: [C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/WebKioskBag.cs)
- Active attendance: [C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ActiveAttendanceBag.cs)
- Scheduled locations: [C#](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/GetScheduledLocationsResponseBag.cs)
- Reprint attendance and labels: [ReprintAttendanceBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ReprintAttendanceBag.cs), [PrintResponseBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/PrintResponseBag.cs)
- Family edit/save payloads: [EditFamilyResponseBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs), [SaveFamilyOptionsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyOptionsBag.cs), [SaveFamilyResponseBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyResponseBag.cs)

Do not assume develop-branch source exactly matches a production instance. Always verify Rock version and installed code.

## 14. Reporting, Analytics, And Model Map

### Interaction Tracking

v2.0 added `WriteInteraction`, a command that writes a new interaction after a person performs an action ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). Use this for intentional analytics events, but do not over-instrument every tap.

Agent checks:

- Confirm interaction channel/component naming.
- Confirm person context.
- Confirm anonymous behavior.
- Confirm duplicate writes are not caused by repeated command triggers.
- Confirm retention/reporting expectations.

### Mobile Preferences

v4.0 added mobile-related user preferences ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)). If behavior differs between users on the same app version, inspect relevant user preferences where exposed in Rock.

### Communication Reporting

Push notifications use the Rock communication system. Inspect:

- Communication history.
- Recipients.
- Medium.
- Transport.
- Send status.
- Exceptions.
- Device identifiers/personal device IDs, where exposed by push documentation ([Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)).

### Check-In Reporting

For mobile check-in and proximity attendance, inspect:

- Attendance records.
- Attendance status.
- Group.
- Location.
- Schedule.
- Security code.
- Presence status if enabled.
- Label print response/errors.
- Scheduled location state.

The view-model source shows how active attendance, reprint attendance, scheduled locations, and location status are represented in next-gen check-in payloads ([ActiveAttendanceBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ActiveAttendanceBag.cs), [ReprintAttendanceBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ReprintAttendanceBag.cs), [LocationStatusItemBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/LocationStatusItemBag.cs)).

### Model Map

This pack does not include full Model Map records for mobile application entities. Before writing SQL or automation against mobile app records, verify:

- Entity names.
- Table names.
- Foreign keys.
- Attribute-backed configuration.
- Page/block storage tables.
- Deployment bundle storage.
- API key storage.
- Communication transport/medium schema.
- Device/push subscription schema.

Use the live Rock Model Map or database metadata rather than deriving database names from UI labels.

## 15. Version And Release Caveats

### Core And Shell Tags

The Core & Shell Dependencies doc explains that some items require specific mobile shell versions (`M`) and some require specific Rock Core versions (`C`) ([Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)). Agents must check both.

Examples from the source pack:

- `ExecuteCommand` requires mobile shell v7.0 ([Execute Command](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/execute-command)).
- `CommandReference` default content property behavior starts in mobile shell v3.0 ([Command Reference](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/command-reference)).
- Some v3.0 login, registration, onboarding, and connection features require Rock Server v13.0 according to release notes ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- v6.0 release notes list a minimum Rock version of v12.6 in the hydrated excerpt ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- Native in-app giving controls are described as available as of shell v7.0 ([In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)).

### MAUI Caveats

V6 MAUI migration can affect:

- Layout behavior.
- Scrolling.
- Width/height requests.
- Xamarin Community Toolkit usage.
- Gradient transparency.
- Zone control.
- Old `Frame`/`StyledView`.
- Safe area padding.
- Shell update forcing ([Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)).

### Platform Caveats

- Context menus are more feature-complete on iOS than Android ([Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu)).
- iOS dark mode has had control-specific fixes ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- iOS push delivery had version-specific fixes ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- iOS minimum version rises to 14.0 in v7.0 ([OS Version Requirements](https://community.rockrms.com/developer/mobile-docs/developers/os-version-requirements)).
- Android app availability can depend on Google target API policies, not just minimum OS support ([Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements)).

## 16. Implementation Playbooks

### Playbook: Add A New Native Mobile Page

1. Open the mobile application.
2. Add a page under Application Pages.
3. Choose phone/tablet layout strategy.
4. Add mobile-compatible blocks.
5. Configure block settings.
6. Set page security.
7. Add navigation entry in Flyout XAML or tab configuration.
8. Verify any command/control shell requirements.
9. Deploy.
10. Test on iOS and Android.
11. Test signed-out and signed-in if relevant.

### Playbook: Add A Push Notification Campaign

1. Confirm push is configured through App Factory and Rock.
2. Confirm service account JSON/provider configuration.
3. Confirm communication transport and medium.
4. Confirm target audience.
5. Choose Open Action: mobile page link or detail display.
6. If linking to a page, use a mobile page and correct query string ([Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)).
7. Send to internal test device.
8. Verify notification receipt, tap behavior, and communication record.
9. Send production campaign.

### Playbook: Add In-App Giving

1. Confirm shell v7.0+ for native giving controls ([In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)).
2. Confirm Rock finance/giving configuration.
3. Confirm platform submission requirements.
4. Confirm Apple nonprofit/Benevity requirements if applicable.
5. Choose native controls or WebView path.
6. If WebView, style page to avoid conflict with native nav.
7. Test app-store review credentials.
8. Test giving flow with non-production/test mode when possible.
9. Coordinate App Factory submission metadata.

### Playbook: Prepare For Shell Update

1. Identify current shell version.
2. Identify target shell version.
3. Review OS minimum changes.
4. Review release notes between versions.
5. Audit custom XAML and CSS.
6. If moving to v6+, run MAUI migration review.
7. Confirm App Factory account access and store credentials.
8. Confirm review Rock logins are active.
9. Test build on iOS and Android.
10. Deploy Rock-side changes if required.
11. Submit store update.

### Playbook: Diagnose “Change Not Showing”

1. Confirm whether the changed item is configuration, page, block, color, XAML, or dynamic content.
2. If not dynamic content, confirm Deploy was clicked.
3. Confirm deployment completed.
4. Restart/reload app to pull latest deployment.
5. Confirm device points to correct API URL/application.
6. Confirm page is not cached or routed elsewhere.
7. Confirm user has security access.
8. Confirm shell supports the changed command/control/block property.
9. Test on another device.

### Playbook: Diagnose WebView Blank Screen

1. Confirm URL loads in mobile browser.
2. Confirm HTTPS/certificate.
3. Confirm WebView has explicit layout space.
4. Confirm the page has mobile viewport meta tag ([Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)).
5. Confirm authentication/session behavior.
6. Confirm external page is not blocking embedding or mobile user agents.
7. Test iOS and Android.
8. Check Rock exception logs only if the WebView content is hosted by Rock.

## 17. Troubleshooting Decision Tree

### App Does Not Launch

- Check shell version and OS minimums.
- Check device OS.
- Check app-store build.
- Check iOS launch fixes if on old v2.x shells.
- Check API URL reachability.
- Check app-store review credentials only if failure occurs during review.
- Check Rock availability and SSL.

### App Launches But Shows Old Content

- Was the app deployed?
- Was the changed content dynamic?
- Did the app reload after deploy?
- Is the device pointed at the correct application ID/API URL?
- Is homepage routing sending the user to another page?
- Is security hiding the updated block?

### Page Is Blank

- Invalid XAML.
- Block exception.
- Missing shell feature.
- Missing Core feature.
- WebView sizing problem.
- Page security.
- Homepage routing issue.
- API key or authorization issue.
- Missing deploy.

### Button Or Action Does Nothing

- Command unsupported in shell.
- Wrong binding context.
- Missing command parameter.
- Invalid page GUID/URL.
- Command attached to wrong property.
- Disabled control.
- Platform permission denied.
- Page not deployed.

### Push Notification Not Received

- Device permission not granted.
- Push permission not requested.
- Service account/provider missing.
- Transport inactive.
- Medium misconfigured.
- Person/device not registered.
- Target audience empty.
- iOS shell version has known issue.
- App not built with push capability.
- Communication send failed.

### Push Opens Wrong Page

- Open Action references non-mobile page.
- Wrong mobile page GUID.
- Missing query string.
- Target page requires login.
- Homepage routing overrides deep link.
- User lacks page authorization.

### WebView Looks Wrong

- Missing viewport meta tag.
- Page not mobile responsive.
- CSS conflicts with native nav.
- WebView container size wrong.
- External page uses unsupported features.
- Authentication redirect inside WebView.
- Platform-specific rendering issue.

### Check-In Fails

- Wrong configuration template.
- Kiosk not configured.
- Areas missing.
- Schedules inactive.
- Locations closed.
- Page parameters not applied; v7.0 fixed a check-in page parameter loading issue ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- Family mode edge case; v7.0 fixed an error for families with only one person ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
- Security code settings wrong.
- Label printing error.
- Presence setting causing pending state.
- Shell/Core mismatch.

### MAUI Upgrade Regression

- Layout changed.
- Scroll behavior changed.
- Width/height request behavior changed.
- Deprecated controls.
- Safe area padding.
- Legacy platform extension.
- Popup overlay bug fixed in v7.0.
- CSS property unsupported in MAUI.

## 18. Agent Task Recipes

### Recipe: Inventory A Mobile App

Collect:

- Mobile application name and identifier.
- Application type.
- Orientation setting.
- API URL.
- API key identity.
- Pages.
- Homepage routing.
- Flyout/tab XAML.
- Blocks by page.
- Security by page/block.
- Deployment status.
- Shell version.
- Rock Core version.
- Push configuration.
- Giving configuration.
- App Factory account ownership.
- Store metadata status.

### Recipe: Determine Whether A Feature Can Be Used

1. Find official docs page.
2. Look for `M` shell tag.
3. Look for `C` Core tag.
4. Check release notes.
5. Confirm live shell version.
6. Confirm live Rock version.
7. Confirm OS minimum impact.
8. Test in Rock Mobile Core app or staging shell.

### Recipe: Add Analytics To A Tap

1. Verify `WriteInteraction` is available in shell v2.0+ ([Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)).
2. Define interaction naming.
3. Attach command to tap target.
4. Prevent duplicate triggers.
5. Deploy.
6. Test as anonymous and authenticated user.
7. Verify interaction record/report.

### Recipe: Modernize Legacy Platform XAML

1. Search XAML for legacy Rock OnDevicePlatform usage.
2. Confirm app is v6+ MAUI.
3. Replace with MAUI built-in platform extension where appropriate.
4. Verify CSS alternative if styling-only.
5. Test iOS and Android.
6. Deploy.

The deprecation basis is the On Device Platform doc ([On Device Platform](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform)).

### Recipe: Review App Store Readiness

1. App name within current store limits.
2. Icon provided.
3. Screenshots current.
4. Description and promotional text current.
5. Keywords and categories selected.
6. Support URL works.
7. Marketing URL works if used.
8. Copyright correct.
9. Review logins active.
10. Developer account access confirmed.
11. Android keystore secured.
12. Push/giving disclosures ready.

Use App Store Product Page, Rock Logins, Developer Accounts, and Android Keystore docs as primary sources ([App Store Product Page](https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page), [Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins), [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts), [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `21`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | configuration | In Rock Mobile's Content block, Dynamic Content pulls fresh content from the server on each page initialization; static content is bundled into the shell, requires a deploy to update, and processes Lava without `CurrentPerson` context. | [source](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content) |
| official | implementation_pattern | Rock Mobile documentation marks which Lava filters can run locally in the shell; in XAML-producing Lava, escape user-entered text, URLs, and other strings that may contain characters such as `&` or `'`. | [source](https://community.rockrms.com/developer/mobile-docs/essentials/lava) |
| official | release_caveat | Outreach Toolbox is presented as a Rock Mobile v19 signed-in experience for maintaining personal outreach contacts and scheduled prayer or connection touchpoints. Verify current mobile-shell support, page placement and authentication requirements before rollout. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4) |
| official | release_caveat | The Outreach Toolbox dashboard can surface people due for outreach and prayer touchpoints, helping a signed-in user see today's relationship-care actions. Verify current mobile availability and permissions before relying on it operationally. | [source](https://www.youtube.com/shorts/c6T9Ha13jKE) |
| official | release_caveat | Rock Mobile compatibility is two-dimensional: documentation uses `M` tags for minimum Mobile Shell versions and `C` tags for minimum Rock Core versions, and a feature may require both. | [source](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies) |
| official | release_caveat | Outreach Toolbox onboarding lets a signed-in person choose assignment days and reminder preferences, while configurable jobs define reminder time-of-day values. Test job scheduling and push-notification delivery in the target mobile environment. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4) |
| official | release_caveat | Moving a Rock Mobile app from shell V5 or earlier to V6 or later changes the framework from Xamarin Forms to .NET MAUI; much XAML remains similar, but documented breaking layout behavior must be tested and adapted. | [source](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6) |
| official | release_caveat | Outreach Toolbox can track contact-specific prayer and connection cadences, completed touchpoint history and periodic pulse updates, with configurable milestone prompts. Review who can see the contact data and which block settings are enabled before ministry use. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4) |
| rocku-confirmed | configuration | The Mobile Check-in Launcher page should enable the virtual kiosk devices and list the check-in configuration and areas that are valid for the campuses served by that page. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| rocku-confirmed | operational_guidance | Mobile check-in should be designed around an initial identity step, such as login or phone lookup, followed by a returning-user experience that can begin closer to the check-in selection screen when the device is recognized. | [source](https://community.rockrms.com/rocku/check-in/using-mobile-check-in) |
| rocku-confirmed | operational_guidance | Mobile check-in block text can be customized and Lava-enabled, but copy should account for where the visitor is in the flow because Rock may not know the person's identity on early screens. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| rocku-confirmed | operational_guidance | Treat each mobile check-in device record like a virtual kiosk: use the check-in kiosk device type, configure the campus geofence, associate the relevant campus locations, and create separate devices when campuses need distinct boundaries. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| More |  | 9 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

### Primary Official Mobile Docs

- [Mobile Docs](https://community.rockrms.com/developer/mobile-docs): Rock Mobile concept entry point.
- [Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon): basic terms such as application, App Factory, Core, deploy, device type, Downhill CSS, publishing.
- [Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app): where mobile applications are created in Rock.
- [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration): application type, orientation, pages, API key, flyout XAML, homepage routing.
- [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app): deployment, testing, application ID, API URL, API key, Rock Core app connection.
- [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies): shell/Core version tags.
- [OS Version Requirements](https://community.rockrms.com/developer/mobile-docs/developers/os-version-requirements): shell release dates and minimum OS table.
- [Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6): Xamarin-to-MAUI migration.

### Commands And Controls

- [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands): command model.
- [Command Reference](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/command-reference): command-as-parameter model.
- [Execute Command](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/execute-command): v7.0 timed/repeated command execution.
- [Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu): native context menu controls and platform caveats.
- [Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view): embedded web content and containment limits.
- [Palette Color](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color): XAML access to palette colors.
- [On Device Platform](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform): legacy platform extension deprecated in V6+.
- [Styling](https://community.rockrms.com/developer/mobile-docs/styling): CSS/MAUI styling caveats.
- [Rock Mobile CSS X-Ray Design Resource](resources/css-xray-design-resource.md): practical selector-targeting schema and Downhill utility summary for mobile UI design/audit work.
- [Rock Mobile Block Selector Image Audit](resources/block-selector-image-audit.md): block-specific selector and settings clues recovered from official block documentation screenshots and style-class tables.
- [Elements of a Card](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/cards/elements-of-a-card) and [Styling Cards With CSS](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/cards/styling-cards-with-css): card source pages.

### Blocks

- [Developers](https://community.rockrms.com/developer/mobile-docs/developers): mobile developer navigation and block families.
- [CMS](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms)
- [Check-in](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in)
- [Communication](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication)
- [Connection](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection)
- [Core](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core)
- [CRM](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm)
- [Events](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events)
- [Finance](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance)
- [Groups](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups)
- [Prayer](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/prayer)
- [Reminders](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders)
- [Security](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security)

### App Factory And Store Operations

- [App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory): publishing service context.
- [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts): account ownership and invitations.
- [Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements): store/OS update pressure.
- [App Store Product Page](https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page): app-store metadata.
- [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore): Android signing and ownership.
- [Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources): compiled shell image resources.
- [Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications): push configuration and sending.
- [Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins): app-store review credentials.
- [In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving): native/WebView giving and approval caveats.

### Release Notes

- [Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes): command/control/block additions, MAUI changes, bug fixes, version dates, minimums.

### Source-Code Landmarks

- [CheckInSecurityCodesSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs)
- [CheckInKioskFeaturesSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInKioskFeaturesSettingsBag.cs)
- [KioskConfigurationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/KioskConfigurationBag.cs)
- [WebKioskBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/WebKioskBag.cs)
- [ActiveAttendanceBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ActiveAttendanceBag.cs)
- [GetScheduledLocationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/GetScheduledLocationsResponseBag.cs)
- [ReprintAttendanceBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ReprintAttendanceBag.cs)
- [PrintResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/PrintResponseBag.cs)
- [EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs)
- [SaveFamilyOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyOptionsBag.cs)
- [SaveFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyResponseBag.cs)
- [SavedKioskConfigurationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SavedKioskConfigurationBag.cs)
- [SubscribeToRealTimeResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SubscribeToRealTimeResponseBag.cs)
- [LocationStatusItemBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/LocationStatusItemBag.cs)

### Community Examples

- [Add live captions & translation to your Rock Mobile app](https://community.rockrms.com/recipes/469): third-party caption/translation integration pattern.
- [Mobile App Countdown to Page Refresh or Redirect](https://community.rockrms.com/recipes/402): schedule-aware countdown and redirect pattern.

Community recipes should be reviewed for security, performance, maintainability, and current Rock compatibility before implementation.
