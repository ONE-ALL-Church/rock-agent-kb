---
id: authored-mobile
title: Rock Mobile
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "3c7b0a1fd48d121e5a004909e5827ced63f3776ca4ce24b7f72c1046ad7fee69"
---

# Rock Mobile

## Agent Summary

Rock Mobile is a native mobile extension of Rock RMS. A working implementation spans four distinct layers:

1. **Rock Core** supplies data, authentication, APIs, configuration and server-processed content.
2. **The Application** defines pages, blocks, XAML, navigation, branding and other organization-controlled settings.
3. **The Mobile Shell** provides native navigation, authentication, API access and platform capabilities on iOS and Android.
4. **Publishing** compiles and distributes shell releases through the app stores; this is separate from deploying application content from Rock. [Mobile Docs](https://community.rockrms.com/developer/mobile-docs) [Mobile Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon)

For agent work, establish the Rock Core version and Mobile Shell version before selecting a feature or control. Documentation marks minimum shell requirements with `M` and minimum Rock Core requirements with `C`; a feature can require both. Then determine whether a requested change belongs to deployable application content or requires a new store release. [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)

Use dynamic Content blocks when content must be fresh or personalized. Static Content block output is included in the deployed application bundle, requires another deploy to change, and processes Lava without `CurrentPerson`. Escape all dynamic strings before inserting them into XAML. [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content) [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

Treat mobile check-in as a configured check-in channel, not an independent attendance system. Confirm normal check-in first, configure virtual kiosk devices and campus boundaries, connect the launcher to the intended devices, configuration and areas, and test the identity, availability and label-printing paths. [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview) [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

## Scope And Boundaries

This guide covers the evidence-supported Rock Mobile application lifecycle:

- Application creation, navigation and deployment
- XAML, Lava and the Content block
- Commands, command parameters and selected controls
- Shell and platform compatibility
- Mobile check-in configuration and participant flow
- Push notifications and selected publishing-sensitive features
- App Factory, developer accounts, store assets and Android signing
- Rock Mobile release and .NET MAUI migration practices
- The mobile-facing Outreach Toolbox evidence supplied for Rock v19
- A community-reviewed workflow pattern for slow background processing

The guide does not define Rock’s underlying API, general CMS architecture, check-in configuration model or security authorization system in full. Those topics own their broader behavior. Here they appear only where they directly affect a mobile implementation.

The supplied evidence does not verify any particular organization’s current application, store account, shell build, page permissions, notification transport or check-in setup. Some mobile check-in claims include a reviewed, public-safe read-only conclusion confirming that the relevant structural configuration surfaces exist, but that conclusion does not prove that a specific launcher, campus boundary or app is configured correctly.

## Mental Model

### Shell, application and core are separate compatibility surfaces

The Shell is the native runtime. It handles navigation, authentication, API calls and other platform work. The Application contains the organization’s pages, blocks, content and visual configuration. Rock Core is the server to which the shell connects. A page can therefore fail because of its application markup, the shell’s capabilities, the Rock server version, connectivity or configuration. [Mobile Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon)

Never use “the app version” as an unqualified compatibility answer. Record at least:

- Rock Core version
- Mobile Shell version
- iOS or Android version
- Phone or tablet
- Whether the application deployment is current
- Whether the change requires store publishing

The documentation’s `M` and `C` tags describe minimum Mobile Shell and Rock Core versions respectively. They can appear at the block, component or setting level. [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)

### Deploying is not publishing

Deploying from the Rock application page distributes application configuration, pages, blocks and bundled content. After a normal configuration or static-content change, deploy again and reload the app. Dynamic Content blocks are the documented exception: their content can refresh from the server without a new deployment. [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)

Publishing distributes a compiled shell through Apple or Google. Shell upgrades and native resources compiled into the shell require the publishing path. Store approval is external to Rock, so a completed Rock deployment is not evidence that a store update was submitted, approved or installed. [App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory) [Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources)

### XAML declares views; commands provide behavior

XAML describes native page structure and controls. Commands are bindable actions that can be invoked by buttons, gestures, menus, behaviors and other compatible views. A command parameter supplies the target or input. Because the same command structure is reusable, the agent should reason about the action independently from the control that triggers it. [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)

### Dynamic content crosses a trust and context boundary

The Content block renders XAML and can process Lava. With Dynamic Content enabled, Rock retrieves fresh content on each page initialization. With it disabled, content is bundled into the deployed application and requires another deploy to change. Lava still runs in the static case, but `CurrentPerson` is unavailable. Server-side Lava also depends on the relevant block settings and enabled Lava commands. [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

This means freshness, identity context and markup safety must be treated separately:

- Dynamic does not automatically mean the required Lava commands are enabled.
- A signed-in shell does not give static Content block Lava a `CurrentPerson`.
- A valid Lava result is not necessarily valid XAML.
- A page context must be passed and configured before a Content block can use its context entity.

## Application Configuration And Deployment

Create or select mobile applications under **Admin Tools > CMS Configuration > Mobile Applications**. A new application starts from an application record in Rock, after which pages and blocks are added through its Application page. [Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app)

The documented application types are:

- **Flyout:** the common configuration, with a slide-out navigation panel.
- **Tabbed:** appropriate when the app has a small set of top-level destinations.
- **Blank:** removes flyout and tab navigation and is reserved for a specific need.

The internal Application Name identifies the application in Rock; it does not set the public store name. Application settings also define orientation, foundational pages, an API key and homepage routing behavior. [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)

For Flyout applications, the default XAML includes a menu-items binding that incorporates pages marked for navigation. Lava is not supported in Flyout XAML; adding it can crash the app at launch. Homepage Routing Logic is a different context: it supports client-side Lava and must output a valid mobile page GUID. It can route a person toward login or onboarding based on the available shell variables. [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration)

Treat the mobile API key as a credential. The documented publishing guidance recommends a complex organization-specific value composed of letters and numbers because some special characters do not compile successfully during App Factory publishing. Changing the API key after store deployment disrupts installed clients and should be coordinated through the publishing provider. Do not expose the key in documentation, logs or screenshots. [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration) [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)

To test an application:

1. Confirm its Application page shows a successful deployment.
2. Connect the Rock Mobile Core test app using the application ID, the Rock server’s public API URL and the configured API key.
3. Launch and exercise the application on the intended device types and platforms.
4. After deployable changes, deploy again and reload the app.
5. Do not expect an unexposed localhost installation to be reachable from the mobile shell. [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)

## Content, XAML And Lava

A Content block renders the XAML placed in its Content setting. Mobile pages can be assembled from layouts, standard MAUI controls and Rock Mobile controls. Multiple child elements need an appropriate containing layout. The current layout choice must also account for the shell generation because Shell v6 moved Rock Mobile from Xamarin Forms to .NET MAUI. [Adding Content](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/adding-content) [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

### Dynamic versus static content

Use **Dynamic Content = Yes** when a page must retrieve current server content on each initialization. Use static content only when bundling and deploy-controlled updates are intentional. Static Content block changes require a new Rock application deployment, and its Lava has no `CurrentPerson` context. [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

Before relying on personalization, inspect:

- Dynamic Content
- Process Lava on Server
- Enabled Lava Commands
- Authentication state
- The block’s Context Entity Type
- The page’s matching context parameter
- The actual parameter supplied by the navigation command

The Content block supports entity context when the block entity type and the page’s context parameter name agree. The documentation recommends passing context by GUID. A missing or invalid context should produce a bounded fallback instead of assuming the entity exists. [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

### Escaping XAML-producing Lava

Rock Mobile documentation identifies which Lava filters can execute locally in the shell. When Lava outputs XAML, escape titles, names, user-entered strings, URLs and other values that can contain markup-sensitive characters such as ampersands or quotes. URL parameters must also be encoded for their destination. [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

A reviewed community pattern extends that rule operationally: test the page with punctuation-bearing names, titles and URLs, because one unescaped record can make an otherwise valid template fail to parse. Treat that as a troubleshooting practice, not a claim that every failure is an escaping problem.

## Commands

Rock Mobile and .NET MAUI use commands for most actions and events. A control commonly exposes a `Command` property and a `CommandParameter`; some controls expose multiple named command properties. A command used by a button can also be attached to another compatible trigger, such as a gesture. [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)

Command parameters have several supported shapes:

- A direct scalar value for a command that accepts shorthand input
- A typed parameter object
- Nested `Parameter` values for query-string-like input
- A XAML-extension shorthand form
- A collection of `CommandReference` items for an aggregate operation

The shorthand form is compact but does not support parameter arrays. When the shorthand value contains commas, the documented pattern encloses that value appropriately so the parser does not split it as separate properties. [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)

Commands are broadly reusable, but their context requirements differ. The `Callback` command is documented as functioning only in Content-derived blocks, while page-overlay commands require page context. Deeply nested action controls can lose the expected binding context; in those cases, use an explicit named reference to the parent binding context rather than assuming the nested object inherits the right command source. [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)

`CommandReference` represents a command and its parameter so one command can be supplied to another structure. Its `CommandParameter` became the default content property in Mobile Shell v3. [Command Reference](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/command-reference)

Shell v7 adds two useful command-triggering mechanisms:

- `EventToCommandBehavior` links a named control event, such as a text-change event, to a command. [Event To Command Behavior](https://community.rockrms.com/developer/mobile-docs/essentials/controls/behaviors/event-to-command-behavior)
- `ExecuteCommand` runs a command during initialization, optionally after a delay or repeatedly. Its settings include `Enabled`, `Delay`, `Repeat`, `RepeatCount`, `StartWithExecution`, `Command` and `CommandParameter`. An unlimited repeating action should be intentional and should have a clear lifecycle. [Execute Command](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls/execute-command)

## Controls

Rock Mobile provides content controls, developer controls, behaviors, effects and XAML extensions in addition to underlying MAUI controls. The supplied evidence lists controls for content, media, context, forms, responsive layout, navigation helpers, QR display, embedded web content and other mobile experiences. Availability still depends on the documented `M` and `C` requirements for the particular control. [Content Controls](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls) [Developer Controls](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls)

### Platform and device adaptation

The legacy `Rock:OnDevicePlatform` and `Rock:OnDeviceType` extensions can select property values or entire nodes for a platform or device class. Both are deprecated in Rock Mobile v6 and later because .NET MAUI provides built-in XAML extensions for those cases. Do not copy legacy syntax into a v6+ page without checking the current MAUI form. [On Device Platform](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform) [On Device Type](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-type)

`PaletteColor` makes named application colors available in XAML, allowing controls to use the configured application palette instead of repeating literal colors. [Palette Color](https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color)

### Context menus

A Rock Mobile context menu can attach native menu behavior to many controls. Its structure consists of `Menu`, `MenuGroup` and `MenuAction`; actions can invoke commands and pass parameters. iOS exposes more of the documented native menu behavior than Android, including some title and system-icon capabilities. Test both platforms and do not infer Android parity from an iOS result. [Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu)

A context menu can conflict with other tap recognizers. The documented attached click-command properties allow a normal tap action and a long-press menu to coexist. Opening the menu immediately on click is supported when the menu is attached to a button. [Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu)

### Borders and migration-era controls

Shell v6 introduced `StyledBorder` as a CSS-compatible wrapper around MAUI’s `Border`. The older `Frame` and Rock `StyledView` remain present but are deprecated in the migration guidance. Prefer `StyledBorder` when CSS compatibility is required in a v6+ implementation, but verify the shell minimum before rendering it to older clients. [Styled Border](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/styled-border) [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

### Web views

Rock’s `WebView` wraps the MAUI control and adds an initial activity indicator. Its content is isolated from the native page: an action inside the web view cannot directly initiate native shell navigation. The embedded page should include a viewport meta tag, and the WebView must not be placed inside a `ScrollView`, where its content can be clipped. A blank iframe on iOS may be a CORS failure whose error is not visibly surfaced. [Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)

### Platform-specific visual effects

The documented Blur Effect is an iOS visual effect with a minimum Mobile Shell v4 requirement. Controls with their own background need a transparent background for the blur to show correctly, and removing shadow effects is recommended. Treat it as an iOS enhancement with a deliberate non-iOS experience. [Blur Effect](https://community.rockrms.com/developer/mobile-docs/essentials/controls/effects/blur-effect)

Shell chrome—including status, navigation and tab bars—has specific CSS properties. Some properties are platform- or shell-version-specific; for example, selected and unselected tab colors require Mobile Shell v2, while documented iOS navigation-bar transparency and blur require v4. [Shell Components](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/shell-components)

## Mobile Check-In

Mobile check-in is a contactless flow that runs on a participant’s mobile device. It uses Rock’s existing check-in configuration and can hand completed selections to a configured iPad kiosk for label printing by displaying a QR code. [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview)

### Prerequisites and configuration

Before enabling the mobile channel, verify:

1. The public site is served over HTTPS.
2. The Google API key required for geofencing is configured.
3. The underlying groups, locations, schedules and check-in configuration already work through normal check-in.
4. Each campus has an appropriate virtual device using the check-in kiosk device type.
5. Each device has the intended campus geofence and relevant campus locations.
6. Campuses requiring different boundaries use separate device records.
7. The Mobile Check-in Launcher enables the correct devices and lists the correct check-in configuration, theme and areas for the campuses served by that page. [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview) [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

A reviewed read-only conclusion in the evidence pack confirmed the structural presence of launcher settings for devices, configuration, theme, areas, identification and fallback messages, along with kiosk-device and schedule-related records. It did not verify any particular launcher instance or geofence.

An immutable public source snapshot also models kiosk resolution as matching a kiosk from location or campus selection, then returning availability and a message. When available, the resulting configuration contains the kiosk, template and enabled areas. This is implementation evidence, not proof of an installed configuration. [KioskResolutionBag at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs) [KioskAvailabilityBag at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskAvailabilityBag.cs)

### Participant flow

The participant flow follows the normal check-in sequence:

1. Identify the person, using login, phone lookup or another configured identity step.
2. Choose the family members or individual checking in.
3. Select eligible check-in options and complete the transaction.
4. Display the QR code when a label-printing handoff is needed.
5. Scan the QR code at the configured kiosk to print labels. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in) [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview)

Both family and individual flows are supported by the supplied approved claims. On first use, identity confirmation occurs before selection. When the same device is recognized later, the returning-user experience can begin closer to the selection step. Do not describe device recognition as a replacement for all identity or security checks. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

The QR code is the label-printing bridge, not the check-in transaction itself. If the participant adds selections after completing check-in, the QR payload can be updated rather than requiring an independent label-handoff workflow for each change. This behavior still needs end-to-end verification with the target kiosk and printer environment. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

### Availability and fallback states

The participant can encounter fallback screens when:

- No device matches the location or campus
- The participant is outside the configured geofence
- No service is currently available within the check-in window
- No eligible check-in option is available

The launcher’s fallback and prompt text can be customized and can use Lava. Write early-flow copy without assuming Rock already knows the person’s identity. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in) [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

## Mobile Engagement And Background Work

When a mobile or web content process depends on slow external work, a community-reviewed implementation pattern uses a Rock workflow to own orchestration rather than blocking the interface. The workflow exposes explicit processing states, retries and completion checks; only a completed and verified output should be linked into public pages or mobile content. [Media Watch community example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)

This is an implementation pattern, not a guarantee that a specific provider, workflow action or mobile block is installed. Before adopting it, verify the available workflow actions, provider authentication, retry behavior, failure states and who can publish the completed result.

## Outreach Toolbox

Official release material presents Outreach Toolbox as a Rock v19 signed-in mobile experience for maintaining personal outreach contacts and scheduled prayer or connection touchpoints. Its dashboard can surface people due for relationship-care actions. [Outreach Toolbox in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4) [Outreach dashboard overview](https://www.youtube.com/shorts/c6T9Ha13jKE)

The supplied evidence describes:

- Onboarding choices for assignment days and reminder preferences
- Configurable jobs that determine reminder time-of-day values
- Contact-specific prayer and connection cadences
- Completed-touchpoint history
- Periodic pulse updates
- Configurable milestone prompts

Before ministry use, verify current shell support, page placement, authentication requirements, block settings, permissions to view contact data, job scheduling and actual push delivery in the target environment. The release material is not evidence that the feature is enabled or authorized in a particular app. [Outreach Toolbox in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4)

## Push Notifications

Rock Mobile push notifications can target individuals, communication lists or everyone with the app installed, including recipients who are not signed in. The open action can link to a mobile page or show communication details; a page destination must belong to the mobile application. [Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)

Push delivery requires both publishing-time and Rock-side configuration. The documented setup includes the provider service-account configuration, the communication transport and medium, the app’s notification-permission request and the recipient device state. Do not expose service-account material in tickets, documentation or test output.

The app can request permission automatically or invoke the `EnablePushNotifications` command from a user action. If permission was requested but notifications are disabled, the app can direct the user to application settings. Core v15.2 introduced an updated service integration that may require coordinated service-account configuration but not necessarily a store shell update. [Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)

## App Publishing

The official mobile documentation describes App Factory as the service used to compile the shell and publish Rock Mobile apps to Apple and Google stores. Publishing covers native shell releases; it is distinct from deploying application pages and content from Rock. [App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory) [Mobile Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon)

### Developer-account ownership and access

Current App Factory documentation requires organizations to host the app under their own Apple and Google developer accounts and grant the App Factory team the access needed to publish. Owning the accounts gives the organization store control but also makes it responsible for renewals, agreements, policy changes, verification and other account maintenance. The same documentation notes that older apps hosted under provider accounts can be delisted after the service relationship ends. [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts)

Store review also requires working app credentials. The documented process uses separate Apple-review and Google-review logins, kept active for initial publishing and later shell updates. These accounts can be limited demo accounts without special Rock permissions. Supply credentials only through the provider’s approved secure channel. [Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins)

### Store listing and graphics

The iOS product page includes the app name, icon, subtitle, screenshots, description, keywords, update notes, categories, support URL and other metadata. The documented app name and subtitle limits are 30 characters each. The support URL is required and must lead to real contact information. App Factory can generate default icons and screenshots, but requested branding and featured screens should be reviewed before submission. [App Store Product Page](https://community.rockrms.com/developer/mobile-docs/app-factory/app-store-product-page)

The supplied App Factory graphics requirements include:

- Launch image: `2048×2048`, with a `720×1440` safe area
- iOS icon: `1024×1024`, with no transparent pixels
- Android background and foreground icon layers, store icon, notification icon and feature graphic
- Store previews for the specified iPhone, iPad, Android phone and Android tablet formats

Treat these as the supplied documentation snapshot and confirm the current submission template before producing final assets, because store requirements can change. [Store Graphics & Icons](https://community.rockrms.com/developer/mobile-docs/app-factory/store-graphics-icons)

### Android signing

The Android keystore signs the app and establishes continuity between releases. Updates must use the same signing identity. If an existing app is being replaced, the original keystore may be required; without it, and absent a supported signing arrangement, publishing a new store application may be necessary. Do not share or expose a keystore. [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)

New Android publications use Android App Bundles, and the documented App Factory process enrolls apps in Play App Signing. Verify the live console state instead of assuming enrollment from the existence of a bundle file. [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)

### Compiled image resources

App Factory can compile selected images into the shell. This avoids network loading and visual pop-in but increases the application download size. Those assets are not processed by the server or CDN, so optimize them before submission. Changing them requires provider coordination and another store update. [Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources)

The documented resource URI incorporates the compiled filename. Escape the filename when producing it through Lava, and account for the provider’s filename normalization. Do not use compiled resources for frequently changing imagery. [Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources)

### In-app giving

As of Mobile Shell v7, Rock Mobile documentation identifies native giving controls. An embedded web view is another possible integration, but store approval and configuration remain the responsibility of the submitting organization, its support partner and the giving provider. The supplied documentation also describes Apple nonprofit-verification and payment-policy requirements; if native or WebView giving is unsuitable, it directs the app to an external-browser flow. Confirm current store policy and provider requirements at submission time. [In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving)

## Mobile Releases

### Core and shell compatibility

A newer Rock Core version does not prove that a feature is available in the installed shell, and a newer shell does not prove that the server supports the feature. Check both documented version tags. [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)

The shell is designed for forward compatibility with later Rock Core versions where possible, but it still needs periodic store updates to target supported iOS and Android versions. The supplied Android guidance recommends an annual update cadence and says an update is needed at least every one to two years to avoid Play availability problems as target-API requirements advance. [Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements)

The release-note snapshot supplied with this guide includes Rock Mobile releases through v19.4, dated August 28, 2026. Release notes also declare minimum operating-system and Rock versions for major shell releases. Use the current release entry applicable to the installed build, not merely the newest entry on the page. [Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)

### Xamarin Forms to .NET MAUI

Mobile Shell v5 and earlier use Xamarin Forms; v6 and later use .NET MAUI. Much XAML remains recognizable, but the migration includes breaking layout and control behavior that must be tested. [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

Evidence-supported migration risks include:

- Complex `StackLayout` behavior
- Scrolling inside unconstrained layouts
- Width and height requests
- Changes involving the Xamarin Community Toolkit
- Gradient transparency
- The `Zone` control’s move from `StackLayout` to `Grid`
- Deprecation of `Frame` and `StyledView`
- The move from safe-area effects toward MAUI-era behavior
- Legacy platform and device XAML extensions

A reviewed community pattern recommends treating these as separate migration recipes rather than performing one blanket textual conversion. Inventory each pattern, preserve intentional expansion with a suitable layout, bound scrolling content, gate MAUI-only controls when old shells remain in service and visually test actual pages on both shell generations. This operational pattern still requires target-app verification. [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

Legacy styling documentation applies to applications targeting Rock versions before 17 or Mobile Shell versions before 6. Do not mix legacy and current styling instructions without recording the target versions. [Legacy Styling](https://community.rockrms.com/developer/mobile-docs/styling/legacy)

### Release-specific behavior

Release notes are evidence for behavior in the stated release, not every earlier shell. For example, the supplied v19.1 records fixes for Android external links and Android audio behavior. If those symptoms occur, identify the installed shell before concluding that the documented fix is present. [Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes)

## Version And Authority Caveats

- **Official documentation** describes intended configuration and supported behavior, subject to its `M` and `C` version gates.
- **Release notes** describe additions and fixes for named releases. They do not prove that a device has installed that release.
- **RockU check-in material** supplies operational guidance. Several approved claims were accompanied by a reviewed read-only structural check, but no particular organization’s launcher or geofence was certified.
- **Public source excerpts** are pinned to immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They clarify implementation shapes but do not establish an installation’s version, configuration or runtime outcome.
- **Community-reviewed patterns** in this guide are examples for troubleshooting and orchestration. They are not universal product guarantees.
- **Outreach Toolbox material** is official release-oriented evidence centered on Rock v19, but current shell compatibility, authentication, placement, jobs and permissions must be verified before rollout.
- **Store policies and graphics requirements** can change independently of Rock. Reconfirm them during an actual submission.
- **Live verification was not performed for this synthesis.** Any installation-dependent conclusion belongs in a separate bounded, read-only review.

## Troubleshooting Decision Tree

### Changes do not appear in the app

1. Identify whether the changed item is dynamic Content block output, static content, page configuration, branding or a compiled shell resource.
2. If it is dynamic content, reload the page and verify the server-rendering settings.
3. Otherwise, check the Application page’s deployment status, deploy the change and reload the app.
4. If the change is a compiled image or shell capability, verify that a store update was published and installed.
5. Stop when the device is confirmed to be running the intended deployment and shell; do not keep editing content to compensate for a stale client. [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app) [Image Resources](https://community.rockrms.com/developer/mobile-docs/app-factory/image-resources)

### The test shell cannot connect

1. Confirm the application is deployed and shows a successful status.
2. Recheck the Application ID, public API URL and API key.
3. Confirm the server is publicly reachable; a normal device cannot connect directly to localhost.
4. Check whether the API key changed after the client was configured.
5. Stop before rotating a published application’s API key without provider coordination. [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)

### The app crashes immediately after opening

1. Inspect Flyout XAML for Lava; Lava is not supported there.
2. Confirm Homepage Routing Logic returns a valid mobile page GUID.
3. Check whether the rendered page includes a control unavailable in the installed shell.
4. Validate generated XAML and escape dynamic attribute values.
5. Reproduce on both iOS and Android if platform-specific markup is present. [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration) [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)

### Personalized content is blank or anonymous

1. Check whether the Content block is static; static Lava has no `CurrentPerson`.
2. Verify Dynamic Content and Process Lava on Server.
3. Inspect enabled Lava commands.
4. Confirm that the shell user is authenticated.
5. If the block uses entity context, verify the entity type, page parameter name and passed GUID.
6. Provide a safe missing-context state instead of dereferencing a null entity. [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

### One record causes a XAML page to fail

1. Capture the type of value that differs: title, name, URL, query parameter or user-entered text.
2. Escape the value for XAML.
3. URL-encode values placed in a URL or query string.
4. Test ampersands, apostrophes, quotes, commas and other punctuation.
5. Confirm that the required Lava filter is available in the actual processing context. [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

### A command does nothing

1. Verify the command exists in the installed shell.
2. Confirm that the triggering control exposes the expected command property.
3. Validate the parameter shape accepted by that command.
4. If shorthand syntax contains commas, check its quoting.
5. For nested action panels, menus or templates, explicitly reference the parent binding context.
6. Check whether the command requires a Content-derived block or page context.
7. Stop when the command works in a minimal control; then restore surrounding nesting one layer at a time. [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)

### A WebView is blank, clipped or cannot navigate natively

1. Confirm the source page is reachable from the device.
2. Add the mobile viewport meta tag to the embedded page.
3. Remove the WebView from any containing `ScrollView`.
4. If an iframe is blank on iOS, investigate CORS against the API domain.
5. Do not expect JavaScript or links inside the WebView to invoke native shell commands directly. [Web View](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/web-view)

### A page layout breaks after moving to Shell v6

1. Identify the original shell and confirm the target is v6 or later.
2. Inventory `StackLayout`, expansion options, scrolling containers, hard size requests, `Zone`, `Frame`, `StyledView`, safe-area effects and legacy platform extensions.
3. Replace only the pattern being tested; do not apply an undifferentiated search-and-replace.
4. Use constrained grid regions where scrolling or expansion requires them.
5. Use a v6-compatible border control where appropriate.
6. Render and visually inspect every affected page on representative phone and tablet layouts. [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

### A context menu works differently on Android

1. Identify whether the missing behavior is an iOS-only title, system icon or native-menu feature.
2. Verify the action command and parameter independently of its icon or presentation.
3. Add an Android-safe visual alternative.
4. Test tap and long-press behavior separately when another recognizer is attached. [Context Menu](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls/context-menu)

### Push notifications are not arriving

1. Confirm the app has been through notification-capable publishing configuration.
2. Verify the Rock communication transport and push medium.
3. Confirm the provider service-account configuration is current without exposing it.
4. Check whether the device was asked for permission and whether permission is currently enabled.
5. Verify the recipient scope and the mobile-page destination.
6. If using the updated service integration, confirm the applicable Rock Core requirement and provider coordination.
7. Test actual delivery on both target platforms; a queued communication is not proof of device receipt. [Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)

### Mobile check-in cannot find a kiosk

1. Confirm HTTPS and the geofencing API prerequisite.
2. Verify location permission and the participant’s current campus or boundary.
3. Inspect the virtual kiosk device type, campus geofence and associated campus locations.
4. Confirm that the launcher enables that device.
5. If campus boundaries differ, confirm separate device records exist.
6. Test campus selection as well as location-based resolution when the configured experience offers both. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

### Mobile check-in finds a kiosk but says no service is available

1. Confirm normal check-in works for the same configuration.
2. Check current schedules and check-in windows.
3. Verify the launcher’s selected configuration and areas.
4. Confirm the person or family has an eligible option.
5. Inspect the configured fallback message so it accurately explains the current stage.
6. Retry only after correcting the configuration or entering a valid time window. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

### Check-in completes but labels do not print

1. Confirm attendance/check-in completion separately from printing.
2. Verify that the QR code represents the latest completed selections.
3. Confirm the scanning device is the intended configured kiosk.
4. Test the kiosk-to-printer path using ordinary check-in.
5. Scan the mobile QR code and verify the print response on the kiosk.
6. Do not repeat the check-in transaction merely to regenerate the label handoff. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

### A store update cannot replace the existing Android app

1. Confirm the package and store listing being replaced.
2. Resolve ownership of the original signing keystore.
3. Check Play App Signing state in the live Google Play account.
4. Coordinate the required signing material through an approved secure channel.
5. If the signing identity cannot be recovered or transferred, stop and evaluate a new store application rather than attempting an unsigned replacement. [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)

### The app is unavailable on newer Android devices

1. Identify the installed store build and its target API.
2. Compare it with the current Google Play requirement.
3. Check the latest supported Rock Mobile shell.
4. Request, publish and verify a shell update.
5. Adopt a recurring review cadence rather than waiting for delisting. [Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements)

### Outreach Toolbox is missing or reminders do not fire

1. Confirm the installed Rock and Mobile Shell versions support the intended experience.
2. Verify the user is signed in.
3. Confirm page placement and access authorization.
4. Inspect the relevant block settings and contact-data permissions.
5. Check onboarding selections, assignment days and reminder preferences.
6. Verify the configured jobs and their time-of-day values.
7. Test an actual push notification on the target device.
8. Stop before treating a scheduled job run as proof of notification delivery. [Outreach Toolbox in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4)

## Agent Task Recipes

### Recipe: Create and test a minimal mobile application

**Outcome:** A deployed application opens in the Rock Mobile Core test shell.

1. Create the application under Mobile Applications.
2. Select Flyout or Tabbed navigation unless the use case specifically requires Blank.
3. Configure an organization-specific alphanumeric API key.
4. Create or open the homepage.
5. Add one Content block with minimal valid XAML.
6. Deploy the application.
7. Connect the test shell using the Application ID, public API URL and API key.
8. Launch on at least one target device.

**Inspect:**

- Deployment status
- Correct application ID
- Public reachability
- Shell and Core versions

**Do not assume:**

- Saving automatically deploys
- A localhost server is reachable
- The Rock application name becomes the store name

**Stop when:**

- The intended deployed page renders in the test shell. [Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app) [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app)

### Recipe: Build personalized Content block output safely

**Outcome:** A mobile page displays current, identity-aware or entity-aware content without malformed XAML.

1. Enable Dynamic Content when fresh server output or `CurrentPerson` is required.
2. Configure server-side Lava processing and only the Lava commands needed.
3. For entity context, select the entity type and define the matching page parameter.
4. Pass the entity GUID through the navigation command.
5. Handle missing authentication or context explicitly.
6. Escape all dynamic XAML text.
7. URL-encode query values.
8. Test signed-out, signed-in, missing-context and punctuation-heavy records.

**Do not assume:**

- Static content has `CurrentPerson`
- Authentication alone establishes block entity context
- Valid Lava output is valid XAML

**Stop when:**

- Each context state renders a deliberate page rather than an exception. [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content) [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)

### Recipe: Add a command-driven interaction

**Outcome:** A control executes a supported command with a validated parameter.

1. Check the command’s `M` and `C` requirements.
2. Confirm whether it needs block or page context.
3. Start with a minimal button or equivalent control.
4. Supply the simplest supported parameter form.
5. If the parameter is structured, use the documented typed object.
6. If nested controls lose the binding, reference the parent binding context explicitly.
7. Test the action and its cancellation or failure path.
8. Move the working command into the final gesture, menu or behavior.

**Inspect:**

- Command availability
- Parameter type
- Binding context
- Target page, URL or entity

**Stop when:**

- The action and its failure state work in the intended nesting context. [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands)

### Recipe: Migrate a page from Shell v5 to v6+

**Outcome:** The page renders correctly on .NET MAUI without silently breaking retained older clients.

1. Record the current and target shell versions.
2. Inventory migration-sensitive layouts, controls, effects and extensions.
3. Separate layout, scrolling, sizing, control and styling changes.
4. Replace deprecated controls only where the target shell supports the replacement.
5. If both generations must remain active, render only markup compatible with the requesting shell.
6. Verify the actual shell-version value used by the target environment before writing a version gate.
7. Deploy the shared content.
8. Test an old-shell client and a v6+ client separately.
9. Visually inspect phone and tablet layouts.

**Do not assume:**

- Removing an expansion suffix preserves expansion
- A text replacement proves visual compatibility
- A marketing version string matches the runtime shell-version format

**Stop when:**

- Each supported shell receives parseable markup and the important layouts are visually verified. [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

### Recipe: Prepare mobile check-in

**Outcome:** A participant can identify, select, complete check-in and hand labels to a kiosk.

1. Validate ordinary check-in for the target groups, locations, schedules and configuration.
2. Confirm HTTPS and geofencing prerequisites.
3. Create a virtual check-in kiosk device for each distinct campus boundary.
4. Configure campus geofences and relevant locations.
5. Configure the launcher’s devices, check-in configuration, theme and valid areas.
6. Review identity, welcome-back and fallback copy.
7. Test first-time identification.
8. Test a recognized returning device.
9. Test family and individual selection.
10. Test outside-boundary, closed-window and no-option states.
11. Complete check-in and scan the QR code at the label kiosk.
12. Add a selection and verify the updated handoff.

**Do not assume:**

- A launcher record proves its selections are correct
- A successful check-in proves printing
- A generated QR code proves kiosk scanning or printer output

**Stop when:**

- Attendance and label printing are independently verified through the intended route. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

### Recipe: Prepare an App Factory publication

**Outcome:** The publishing provider has a reviewable, secure and complete submission package.

1. Confirm ownership and active status of the Apple and Google developer accounts.
2. Complete current account agreements, renewals and verification.
3. Grant only the publishing access required by the documented process.
4. Create separate, limited Rock review logins for the two stores.
5. Confirm the desired shell version and its Core and OS requirements.
6. Prepare the store name, subtitle, description, categories, support URL, screenshots and graphics.
7. Resolve Android signing continuity before attempting replacement.
8. Identify compiled resources and optimize them before submission.
9. Provide secrets and credentials only through approved secure channels.
10. Submit through the provider workflow.
11. Read back submission, review and release status from both stores.
12. Install the released build and verify its shell version and core journeys.

**Do not assume:**

- Provider receipt means store submission
- Store submission means approval
- Approval means release
- Release means the target device installed the update

**Stop when:**

- Both stores and representative devices show the intended released build. [App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory) [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts) [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore)

### Recipe: Validate push notifications

**Outcome:** A real target device receives and opens a notification through the intended route.

1. Verify publishing-time notification configuration.
2. Confirm the Rock transport, medium and provider configuration.
3. Request notification permission through the intended app experience.
4. Confirm the device reports notifications enabled.
5. Send to a bounded test recipient.
6. Verify receipt while signed in.
7. Where required, verify receipt while signed out.
8. Open the notification and confirm the mobile-page or detail action.
9. Test both platforms before broad release.

**Stop when:**

- Receipt and open behavior are observed on the target devices. [Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications)

### Recipe: Orchestrate slow media or content work

**Outcome:** Slow processing completes asynchronously and only verified output reaches public mobile content.

1. Define explicit queued, processing, retry, failed and completed states.
2. Start the work through a workflow rather than holding the mobile interface open.
3. Record bounded retry behavior and a terminal failure state.
4. Poll or receive the provider’s completion result.
5. Validate the resulting asset.
6. Link it into mobile or web content only after completion.
7. Surface failure or review-needed status to an operator.

**Do not assume:**

- A provider accepted the job because a request returned successfully
- A generated URL points to a complete, public-safe asset
- Workflow completion automatically publishes content

**Stop when:**

- The verified output is linked or the workflow reaches a visible terminal failure state. [Media Watch community example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)

### Recipe: Validate Outreach Toolbox for ministry use

**Outcome:** Authorized signed-in users can see and complete intended outreach actions, and reminders arrive.

1. Establish the target Core and Shell versions.
2. Confirm the mobile feature and pages are installed.
3. Verify signed-in routing.
4. Review block settings and data visibility.
5. Configure or validate assignment days and reminder preferences.
6. Inspect the jobs that control reminder timing.
7. Test prayer and connection cadence records.
8. Complete a touchpoint and confirm history.
9. Test milestone or pulse behavior that is intentionally enabled.
10. Verify an actual reminder on a target device.

**Stop when:**

- The intended user can complete the full authorized workflow and receive the expected reminder. [Outreach Toolbox in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4)

## Known Gaps And Live Verification

A bounded, read-only target-instance review is still required to answer any of the following:

- Which Mobile Shell and Rock Core versions are actually in service
- Whether every target device has installed the intended store build
- Which application pages, blocks, navigation settings and permissions are active
- Whether Dynamic Content, server Lava and enabled-command settings match the intended context
- The runtime format of any shell-version variable used for conditional XAML
- Whether provider or plugin-specific blocks are installed
- Whether mobile check-in devices, boundaries, locations, schedules, configurations and areas are correct
- Whether ordinary check-in works for the same operational scope
- Whether QR scanning and label printing work on the intended kiosk and printer
- Whether push transports, service credentials and device permissions are current
- Whether Outreach Toolbox pages, jobs, authorization and notification delivery are active
- Whether Apple and Google accounts, agreements, review credentials and signing assets remain valid
- Whether current store policies or graphics templates differ from the supplied documentation snapshot
- Whether a reported issue reproduces on the exact platform, OS and shell combination

The evidence pack does not include a reviewed live conclusion for a specific app’s configuration, deployment, store status or physical-device behavior. Do not convert documentation, a clean deployment status, a scheduled job, a generated QR code or a store submission into a claim of end-to-end completion.

## Source Map

### Official Rock Mobile documentation

- [Mobile Docs](https://community.rockrms.com/developer/mobile-docs) — platform scope and support routes
- [Mobile Lexicon](https://community.rockrms.com/developer/mobile-docs/lexicon) — shell, application, core, deploy and publishing concepts
- [Creating An App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/creating-an-app) — application creation
- [App Configuration](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/app-configuration) — navigation, pages, API key, Flyout XAML and routing
- [Adding Content](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/adding-content) — pages, blocks and XAML
- [Deploying Your App](https://community.rockrms.com/developer/mobile-docs/building-your-first-app/deploying-your-app) — deployment and test-shell connection
- [Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content) — dynamic content, Lava and entity context
- [Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava) — local Lava capability and escaping
- [Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands) — command binding and parameters
- [Content Controls](https://community.rockrms.com/developer/mobile-docs/essentials/controls/content-controls) — control catalog
- [Developer Controls](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls) — developer-control catalog
- [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies) — `M` and `C` compatibility tags
- [Migrating to .NET MAUI](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6) — Shell v6 migration
- [Shell Update Requirements](https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements) — operating-system and store cadence
- [App Factory](https://community.rockrms.com/developer/mobile-docs/app-factory) — publishing service and review process
- [Developer Accounts](https://community.rockrms.com/developer/mobile-docs/app-factory/developer-accounts) — account ownership and provider access
- [Android Keystore](https://community.rockrms.com/developer/mobile-docs/app-factory/android-keystore) — Android signing continuity
- [Push Notifications](https://community.rockrms.com/developer/mobile-docs/app-factory/push-notifications) — notification configuration and permission flow
- [In-App Giving](https://community.rockrms.com/developer/mobile-docs/app-factory/in-app-giving) — shell v7 giving and publishing caveats
- [Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes) — release-specific requirements, additions and fixes

### Official RockU and release media

- [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview) — prerequisites, participant flow and label handoff
- [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) — virtual devices, boundaries and launcher configuration
- [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in) — family, individual, returning-user and fallback flows
- [Outreach Toolbox in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4) — signed-in outreach experience, cadence and reminders
- [Outreach dashboard overview](https://www.youtube.com/shorts/c6T9Ha13jKE) — due outreach and prayer actions

### Community-reviewed example

- [Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr) — workflow orchestration pattern for slow background processing

### Immutable implementation evidence

- [KioskResolutionBag](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs) — kiosk resolution result at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`
- [KioskAvailabilityBag](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskAvailabilityBag.cs) — availability and resolved configuration at the same commit
