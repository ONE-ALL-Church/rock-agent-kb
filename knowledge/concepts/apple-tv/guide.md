---
id: authored-apple-tv
title: Apple TV Apps
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "36991b0283d96e45ef721418b8716542ddedb18f14b94ae950794b74c944ebc4"
---

# Apple TV Apps

## Agent Summary

Rock Apple TV provides Rock-managed pages, Lava data, styles, authentication, media playback commands, and other shell commands for TVML applications. The documented feature requires Rock 14 or later. Use Apple’s TVML documentation for the underlying markup and Rock’s Apple TV documentation for Rock-specific behavior. Avoid modifying the application JavaScript unless a separately reviewed requirement makes that necessary. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)

For an operational task, identify five things before editing:

1. The exact Rock TV application record.
2. The page and TVML template involved.
3. The installed Rock and TV shell versions.
4. Whether the workflow depends on authentication, context, interaction tracking, or demo-mode support.
5. Whether any response depends on live configuration that has not yet been inspected.

A typical application flow is:

1. Rock stores the TV application settings.
2. A Rock Apple TV page renders Lava into valid TVML.
3. The Apple TV shell displays that TVML.
4. Elements carrying Rock commands ask the shell to navigate, authenticate, update context, or play media.
5. Rock may record page views, authentication sessions, or media interactions when the related settings and parameters are present. [Creating an App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript)

## Scope And Boundaries

This guide covers the evidence-supported Rock Apple TV workflows for:

- Creating and configuring a TV application.
- Building TVML pages with Lava.
- Choosing cache behavior.
- Using persistent application context.
- Implementing remote sign-in and logout.
- Using media, personal, navigation-adjacent, utility, and demo commands.
- Selecting templates and Rock-specific controls.
- Styling text, themes, and custom controls.
- Preparing icons, launch images, Top Shelf images, and parallax images.
- Testing through Rock’s documented demo workflow.
- Evaluating Lava webhook APIs used by TV applications.

The guide does not cover App Store submission, certificate management, shell compilation, Apple developer-account administration, native tvOS development, or a complete API integration design. Those subjects are not sufficiently described in the supplied evidence.

Do not treat TVML as HTML. The documented environment has no WebView, styling is more limited than browser CSS, SVG support is described inconsistently across the supplied Rock pages, and individual TVML templates can process elements differently. [Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips) [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)

No community contribution or private draft was used as an authority for this guide.

## Mental Model

Treat a Rock Apple TV implementation as four connected layers:

1. **Rock application configuration** — The TV application is a Rock-managed site record with settings such as application styles, API key, page-view behavior, retention, and authentication page. Its internal Rock name does not have to match its eventual App Store name. [Creating an App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)

2. **Rock pages and Lava** — Each TV page must render valid TVML. Lava can personalize that markup from the current person, application context, campus data, page data, device information, theme, and other supplied merge fields. [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

3. **TVML presentation** — Apple templates define the main layout and interaction model. Styles resemble CSS but use TVML and tvOS properties, themes, resources, and focus behavior. Template behavior is not interchangeable with browser layout behavior. [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)

4. **Rock shell commands** — Markup elements can carry `rockCommand` attributes for operations such as login, logout, page replacement, media playback, context changes, and demo configuration. The exact page template and shell version still need inspection before changing an existing implementation. [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands) [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)

This separation matters during troubleshooting. A failure can originate in Rock configuration, Lava output, TVML validity, shell capabilities, command parameters, remote assets, or an unverified installation-specific setting.

## Creating And Configuring An Application

Create a Rock-managed Apple TV application under `Admin Tools > CMS Configuration > Apple TV Apps`. The record is distinct from the name and metadata later used in the App Store. The documented configuration includes:

- **Name** — Rock’s internal name for the application.
- **Description** — Optional internal description.
- **Application Styles** — Global styles available throughout the application.
- **Enable Page Views** — Controls whether page-view interaction data is recorded.
- **API Key** — The key the application will use to access the server while testing.
- **Page View Retention Period** — Number of days to retain page views; an empty value is documented as indefinite retention.
- **Authentication Page** — The external Rock page containing the Remote Authentication block.

Saving a new application generates a Start Screen. The documented Start Screen cannot be deleted and is intended to serve as the application home page. [Creating an App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)

Do not infer the active application from its display name alone. Before editing, inspect the application’s pages, settings, start page, authentication page, styles, API key field, page-view setting, and retention configuration.

A reviewed read-only verification included in the evidence pack confirmed that one Rock installation exposed TV Application List, Apple TV Application Detail, Apple TV Page Detail, and TV Page List administration surfaces, as well as a TV site with default-page, login-page, and page-view settings. This confirms that the management surface exists in an observed installation; it does not establish another installation’s configuration.

## Pages, Lava, And Cache Behavior

### Page content and merge fields

Every Apple TV page must produce valid TVML after Lava has rendered. Rock documents these page merge fields:

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
- `TvAppTheme`
- `IsDemoModeEnabled`

These fields let the page respond to the signed-in person, persistent context, page parameters, permission checks, shell version, device characteristics, application theme, and demo state. `DeviceData` can include the device type, manufacturer, model, name, operating-system version, platform, and identifier. Do not publish a real device identifier in documentation or diagnostic output. [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

Use `SiteStyles` when the page should receive the application’s global style definitions. Use `CurrentPersonCanEdit` and `CurrentPersonCanAdministrate` only as the documented descriptions indicate: signals about the current person’s access to the page. Do not infer broader authorization from either value.

### Creating page content

The documented editor allows an agent to give a page a name, an optional description, TVML content, and a cacheability type. The Start Screen can use a `mainTemplate`, menu items, Lava conditions based on `CurrentPerson`, and rotating background images. Those examples demonstrate supported composition patterns, not a requirement that every start page use the same structure. [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)

Render the final Lava result mentally or in a controlled test before deciding that the stored template is valid. A syntactically valid Lava template can still emit invalid TVML.

### Cacheability

Rock documents four page cacheability choices:

- **Public** — Permits storage in a shared cache.
- **Private** — Limits caching to the client.
- **No-Cache** — Requires revalidation before a local copy is reused.
- **No-Store** — Prevents local storage and is intended for sensitive content.

Choose the setting from the sensitivity and freshness requirements of the rendered page. Do not assume that a template edit will immediately appear on a device without inspecting the page’s cacheability and confirming which application configuration the shell is using. [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)

## Application Context

The Rock TV framework can persist a Rock entity as application context across viewing sessions. The context key is the entity’s friendly name, and the value can be its identifier or GUID. The documented common use is Campus, but the mechanism is not limited to Campus. Pages can read the result through `Context`, such as `Context.Campus`. [Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context)

Rock documents Set Context and Clear Context as utility commands. The supplied evidence does not include their complete parameter reference, so retrieve the exact command contract before generating production markup.

Campus context is separate from a signed-in person’s campus. The documented precedence is:

1. Use an existing Campus context if one has been set.
2. If no Campus context exists, use the signed-in person’s campus when appropriate.

Do not silently overwrite an explicit TV context merely because a person signs in. [Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context)

## Sign-In, Logout, And Remote Authentication

### Server-side setup

Rock’s remote sign-in pattern avoids entering credentials with the TV keyboard:

1. Create an external Rock web page.
2. Add a Remote Authentication block to that page.
3. Configure the block for the site representing the TV application.
4. Make the page reachable by a suitable URL or route.
5. Set that page as the TV application’s Authentication Page. [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)

The current `develop` implementation at immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` describes the block as authenticating a remote system through a short-lived security code, supports it on a web site, and returns a warning when the external visitor is not authenticated. This is source-code evidence, not proof that the same implementation is installed in a particular Rock environment. [Remote Authentication source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Tv/RemoteAuthentication.cs)

### TV-side login flow

A login command can specify:

- `rockLoginPageGuid` — Page that displays the login information.
- `rockLoginTimeoutPageGuid` — Page shown when the attempt expires.
- `rockLoginSuccessPageGuid` — Page shown after successful login.
- `rockLoginTimeoutDuration` — Documented default of 600 seconds.
- `rockLoginCheckDuration` — Documented default polling interval of five seconds.
- `rockLoginClearNavigationStack` — Documented default of `true`.

The login page receives `authQrCodeUrl` and `authCode`. These are shell-supplied fields written with single braces, such as `{ authCode }`, rather than Lava’s double braces. The keys are case-sensitive. [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)

The login page should present the QR code, the manual sign-in URL, and the manual code. The timeout destination should give the viewer a deterministic route back to a safe page. The success destination can return to the Start Screen or show a personalized confirmation. [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)

The immutable source snapshot shows remote-session verification filtering for an active code and the expected device identifier. Use that only as an implementation observation when diagnosing a matching failure; do not assume an installation runs this commit. [Remote authentication session service](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Security/RemoteAuthenticationSessionService.cs)

### Logout and navigation state

The logout command accepts a destination page through `rockLogoutPageGuid`. Its navigation-stack clearing option defaults to `true`. The login command likewise defaults to clearing the stack after success so that using Back does not expose earlier impersonalized content. [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)

Do not disable stack clearing without explicitly testing the Back-button journey before login, after login, after logout, and after timeout.

## JavaScript And Rock Commands

Rock documents commands as a core application mechanism spanning navigation, personal actions, media, utility behavior, and demo workflows. In page templates, the normal integration surface is the Rock command attributes placed on TVML controls. Modifying the application JavaScript itself is discouraged by the official overview. [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript) [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)

Use this command-handling sequence:

1. Identify the exact user action and destination.
2. Select the documented command category.
3. Confirm that the chosen TVML element supports the needed interaction.
4. Supply only parameters documented for that command.
5. Verify all referenced page GUIDs belong to the same intended TV application.
6. Test success, timeout, Back-button, and failure behavior on the target shell.

A reviewed read-only template inspection included in the evidence pack observed `rockCommand` attributes for navigation, login, logout, and media playback in one installation. That observation confirms a real command surface but does not validate the exact template, parameters, or shell version in another installation.

## Media Playback And Interaction Progress

Rock’s media commands support:

- Video from MP4 or HLS sources.
- Audio from MP3 sources.
- Optional title, subtitle, artwork, and description metadata.
- Related entity information.
- Rock Media Element association for watch tracking.
- Resume behavior and interaction watch maps.

The documented Apple TV application cannot play YouTube content through these media commands. [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)

The interaction parameters have materially different outcomes:

- Supplying `rockWatchMap` establishes the prior viewing position.
- Supplying both `rockWatchMap` and `rockInteractionGuid` appends progress to the existing interaction.
- Supplying `rockWatchMap` without `rockInteractionGuid` uses the prior stopping point but creates a new interaction and new watch map from that point.

The video command uses `rockVideoUrl` for MP4 or HLS content. The audio command uses `rockAudioUrl` for MP3 content. Resume is documented as enabled by default through the corresponding enable-resume option. [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)

Before wiring playback, decide whether the desired outcome is merely playback, resume from a known position, append to an existing interaction, or start a new interaction from a prior position. Do not add an interaction GUID reflexively; it changes the tracking result.

## Templates And Rock-Specific Controls

### Choosing a TVML template

Rock’s template library presents screenshots and TVML derived from Apple’s TVML Catalog sample so builders can evaluate layouts without compiling the sample application. Templates can apply custom animation, focus, scrolling, and element-processing behavior. Customization can be difficult even with the flexible Div Template. [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)

Evidence-supported examples include:

- **Alert Template** — Presents important information and an action. Rock’s example calls for at least a description and a button. [Alert Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/alert-template)
- **Catalog Template** — Presents groups along the left and related images or content on the right. [Catalog Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/catalog-template)
- **Product Template** — Presents detailed information with related items; the Rock example notes system-theme behavior and a dark default when a background image is present. [Product Template](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-template)

Choose a template whose native structure already matches the journey. Do not assume that markup working in one template will behave the same way in another.

The supplied template library includes Apple sample-code licensing terms. Review those terms before redistributing sample-derived code or assets. [Template Licensing](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/licensing)

### Custom Rock controls

Rock documents custom controls for cases where TVML alone cannot consistently produce the intended behavior. [Control Reference](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference)

The documented countdown control can:

- Display a live countdown from `startDateTime`.
- Control the visibility of days, hours, minutes, and seconds with `Always`, `Automatic`, or `Hidden`.
- Display a completed panel and message.
- Execute a configured command when the countdown completes.
- Avoid immediately executing that command when the page initializes too close to completion through `completedCommandSecondThreshold`.

Rock recommends still providing completed content even when a completion command exists. The documentation also warns that the `scheduledcontent` Lava shortcode adds processing overhead and suggests caching when a heavily visited page uses it. [Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown)

`RockStackView` is the layout element used within custom controls and supports documented properties including background and tint colors, inter-item spacing, margin, width, border radius, and horizontal or vertical layout. `RockLabel` is the primary text element within custom controls and supports properties including color, margin, width, font size, font weight, and `tv-text-style`. [RockStackView](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rockstackview) [RockLabel](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rocklabel)

## Styling, Themes, And Text

### TVML styling model

TVML styling resembles a restricted CSS model but is not browser CSS. Rock recommends aligning with Apple’s tvOS design language instead of forcing a heavily customized web-style interface. [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)

Predefined `tv-text-style` values documented by Rock include:

- `body`
- `callout`
- `caption1`
- `caption2`
- `footnote`
- `headline`
- `subhead`
- `subtitle1`
- `subtitle2`
- `subtitle3`
- `title1`
- `title2`
- `title3`

Text can also use documented font weights from `ultralight` through `black`, selected font families, and inline `<b>`, `<i>`, and `<strike>` tags. [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)

A text shadow is defined by horizontal offset, vertical offset, blur radius, and color. The surrounding element can clip the shadow vertically, so keep the shadow close to the text and test it in the actual template. [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)

### Light and dark themes

Apple TV has documented Light and Dark themes. Normally the person’s theme selection controls the result. TVML media queries can branch on `tv-theme:light` and `tv-theme:dark`, and a page template can declare a specific theme when the design requires it. [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries)

Test both themes even when a page declares one explicitly. Images, badges, shadows, and foreground colors can respond differently from text.

### Built-in resources and references

tvOS provides resource libraries for button, miscellaneous, movie-rating, and TV-rating icons. Rock also documents access to SF Symbols and shell-embedded custom resources. When referencing an embedded custom resource, omit the file extension because tvOS removes extensions from resource names. Rock’s example also uses `resource://overlay-checkmark` as an image overlay. [Built-in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)

The styling reference gallery is inspiration only. Rock explicitly warns that some referenced layouts may rely on native behavior that TVML cannot reproduce. [Styling References](https://community.rockrms.com/developer/apple-tv-docs/styling/references)

## Application Images

### App icons

A Rock Apple TV app icon uses three separate layers to create the tvOS parallax effect. Each size must be delivered as separate layers:

- Foreground layers: PNG.
- Background layer: JPG.

Required documented dimensions are:

- In-app @1x: 400 × 240 pixels.
- In-app @2x: 800 × 480 pixels.
- App Store: 1280 × 768 pixels.

Do not flatten the three icon layers into a single file when preparing the icon package. [App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons)

### Parallax content images

For parallax content inside the application, host an LCR file and reference its direct URL as the image source. Rock warns that a non-direct URL renders as a flat image and that LSR files do not work for this use. [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)

### Launch images

Launch images are static, contain no layers, and are intended to bridge the brief period before the first screen appears. The documented sizes are:

- @1x: 1920 × 1080 pixels.
- @2x: 3840 × 2160 pixels. [Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image)

### Top Shelf images

Static Top Shelf images are PNG files and are not layered. Rock documents:

- Top Shelf Wide: 2320 × 720 at @1x and 4640 × 1440 at @2x.
- Standard Top Shelf: 1920 × 720 at @1x and 3840 × 1440 at @2x.

The source describes Top Shelf Wide as introduced in tvOS 10 and the standard dimensions as the tvOS 9-and-earlier form. Treat those statements as historical applicability notes and verify current Apple packaging requirements before delivery. [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image)

## Testing And Demo Mode

Rock documents a demo-key workflow that can point the Rock community Apple TV shell at a Rock application without first publishing through TestFlight or the App Store:

1. Submit the Apple TV demo request form.
2. Receive a demo key.
3. Install the Rock community application identified in the documentation as Rock Core.
4. Open its Demo area.
5. Enter the key.
6. Restart the application. [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app)

This workflow depends on the current availability of the demo-request service and community shell. Verify both before planning a testing milestone around them.

Demo commands work only when the shell was compiled with demo-mode support:

- `showDemo` opens the demo configuration screen.
- `clearDemo` removes demo settings and restores the compiled settings.
- `updateDemo` updates settings from the code entered on the demo screen and should not be used elsewhere. [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)

A successful preview is not proof that authentication, media tracking, caching, or final packaged assets work in the production shell. Test those behaviors separately.

## Lava APIs And Security

Rock documents Lava webhooks as one way to create a custom XML API for an Apple TV or Roku channel. Incoming requests are matched to a configured Lava Webhook Defined Value by HTTP verb and URL, after which Rock renders the selected Lava template. The Defined Value controls which Lava commands are enabled for that template. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

The same official source explicitly warns that Lava webhooks do not include security by default. Operationally, treat a webhook response as exposed until an independently verified protection controls access. Inspect:

- The exact URL and allowed HTTP verb.
- The matched Defined Value.
- The Lava template.
- Every enabled Lava command.
- All returned person, financial, group, attendance, or other sensitive data.
- Any separately implemented security layer and its failure behavior.

Do not infer endpoint safety from an API key field on the TV application, an authenticated Rock administration session, an obscure URL, or the absence of a link in the TV interface.

A reviewed read-only verification supplied with the evidence confirmed that one inspected Lava webhook handler matched active definitions by URL and method and rendered the configured template without an explicit permission check in that handler path. This reinforces the official warning but does not establish the configuration of another Rock installation.

## Version And Authority Caveats

- The official overview says Apple TV functionality requires Rock 14 or later. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)
- The evidence does not map every command, property, or control to a specific Rock 14+ point release or TV shell version.
- The text-overflow guidance is labeled “TV 2.0” in the supplied Tips article, but the evidence does not map that label to a Rock release. Verify shell applicability before depending on its modal overflow behavior. [Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)
- Top Shelf size notes reference tvOS 9 and 10 historically; current Apple packaging requirements were not independently verified for this guide. [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image)
- The remote-authentication source observations come from the immutable Rock `develop` commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They describe that commit, not every released or installed Rock version.
- The evidence includes reviewed public-safe conclusions from a bounded read-only instance inspection. Those conclusions demonstrate observed surfaces and template patterns, not universal configuration.
- The Rock styling galleries are references, not proof that a native-app layout can be reproduced in TVML. [Styling References](https://community.rockrms.com/developer/apple-tv-docs/styling/references)
- The template examples include Apple sample-derived material with separate licensing terms. [Template Licensing](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/licensing)
- No live test of the reader’s application, device, shell, media provider, authentication route, webhook, or App Store package occurred for this guide.

## Troubleshooting Decision Tree

### The application or Start Screen does not load

1. Confirm the installed Rock version is 14 or later.
2. Confirm the exact TV application exists under Apple TV Apps.
3. Inspect its generated Start Screen and default-page configuration.
4. Render the page’s Lava and verify that the result is valid TVML.
5. Confirm the testing shell points to the intended application rather than compiled or stale demo settings.
6. Inspect the page cacheability setting.
7. Stop when resolution requires changing the shell package or an unverified production setting.

Sources: [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) [Creating an App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

### A page is blank, malformed, or rejected

1. Inspect the final TVML after Lava rendering, not only the stored template.
2. Confirm that the selected template accepts the elements being emitted.
3. Check Lava conditions involving `CurrentPerson`, `Context`, or page parameters.
4. Remove assumptions based on HTML, browser CSS, SVG, or WebView behavior.
5. Test the page in both Light and Dark themes.
6. If the same markup works in another template, do not assume equivalence; compare each template’s supported structure.

Sources: [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates) [Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips)

### Login shows no QR code or manual code

1. Confirm that the external Rock page contains a Remote Authentication block.
2. Confirm that the block is associated with the intended TV application site.
3. Confirm that the application’s Authentication Page points to that external page.
4. Confirm that the login command references the intended login, timeout, and success pages.
5. Confirm the page uses the case-sensitive `{ authQrCodeUrl }` and `{ authCode }` fields with single braces.
6. Confirm the person is authenticated on the external Rock site.
7. If the current installation follows the inspected source implementation, investigate code lifetime and device-identifier matching.
8. Stop before exposing authentication session records or identifiers in public diagnostics.

Sources: [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands) [Remote Authentication source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Tv/RemoteAuthentication.cs)

### Back navigation exposes the pre-login or personalized page unexpectedly

1. Inspect `rockLoginClearNavigationStack`.
2. Inspect `rockLogoutClearNavigationStack`.
3. Unless the journey requires otherwise, retain the documented default of `true`.
4. Test Back navigation after successful login, timeout, logout, and failed authentication.
5. Verify the success and logout destination pages.

Source: [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)

### Video or audio does not play

1. Confirm the command is `playVideo` or `playAudio`.
2. Confirm video uses a direct MP4 or HLS source.
3. Confirm audio uses a direct MP3 source.
4. Reject YouTube as a supported source for these commands.
5. Inspect the exact media URL and metadata parameters.
6. If Rock watch tracking is expected, inspect the Media Element and related-entity parameters.
7. Test the same media without interaction parameters to separate playback failure from tracking failure.

Source: [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)

### Playback resumes incorrectly or creates duplicate interactions

1. Determine whether the intended outcome is resume only, append to an existing interaction, or create a new interaction from a prior position.
2. For resume position, inspect `rockWatchMap`.
3. To append progress, verify both `rockWatchMap` and `rockInteractionGuid`.
4. If a new interaction is intended, omit `rockInteractionGuid`.
5. Inspect whether resume has been explicitly disabled.
6. Retest with a known prior stopping point.

Source: [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)

### Colors or badges disappear in one theme

1. Determine whether the page follows the system theme or declares its own.
2. Inspect Light and Dark media-query branches.
3. Check foreground colors, badge tint, image contrast, and text shadows in both themes.
4. Keep shadows close to text if vertical clipping occurs.
5. Do not treat a reference-gallery screenshot as proof that TVML can reproduce the layout.

Sources: [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries) [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)

### A parallax image is flat or missing

1. Confirm the asset is an LCR file.
2. Confirm the image source is a direct link to that file.
3. Reject an LSR file for this workflow.
4. For app icons, confirm three separate layers with PNG foregrounds and a JPG background.
5. Confirm the dimensions for the intended @1x, @2x, or App Store use.
6. For shell-embedded resources, remove the file extension from the resource name.

Sources: [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images) [App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons) [Built-in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)

### A template change does not appear

1. Confirm the shell points to the intended application.
2. Inspect the page’s cacheability type.
3. Confirm whether demo settings or compiled settings are active.
4. Restart the application when using the documented demo-key workflow.
5. Use `clearDemo` only when the intended outcome is to restore compiled settings.
6. Make a controlled cacheability change only after confirming that freshness, not malformed TVML, is the issue.

Sources: [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content) [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app) [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)

### Demo commands do not work

1. Confirm the shell was compiled with demo-mode support.
2. Use `showDemo` to enter the documented demo screen.
3. Use `updateDemo` only within that screen.
4. Confirm the demo key and restart flow.
5. Use `clearDemo` to return to compiled settings.
6. Stop if the demo service or Rock Core application is no longer available; current availability requires separate verification.

Sources: [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands) [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app)

### A countdown immediately navigates or starts media

1. Inspect `completedCommand`.
2. Inspect `completedCommandSecondThreshold`.
3. Determine how many seconds remained when the control initialized.
4. Provide a completed panel even when a completion command is present.
5. Test initial loads immediately before and after the target time.

Source: [Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown)

### A Lava webhook exposes more data than expected

1. Identify the exact Lava Webhook Defined Value matched by the request URL and verb.
2. Inspect the complete template output.
3. Inventory every enabled Lava command.
4. Verify the protection mechanism independently; Rock documents no default webhook security.
5. Remove unnecessary data and commands before considering the endpoint ready.
6. Stop immediately if person or other sensitive data is reachable without the intended control.

Source: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

## Agent Task Recipes

### Recipe: Create a minimal Rock Apple TV application

**Outcome:** A Rock-managed application with a valid Start Screen and documented baseline settings.

1. Confirm Rock 14 or later.
2. Open `Admin Tools > CMS Configuration > Apple TV Apps`.
3. Create the application record with an internal name and description.
4. Review Application Styles, Enable Page Views, API Key, Page View Retention Period, and Authentication Page.
5. Save the record.
6. Open the generated Start Screen.
7. Add a minimal supported TVML template.
8. Render any Lava and validate the final TVML.
9. Select cacheability from the page’s sensitivity and freshness requirements.
10. Test through the exact target or demo shell.

Inspect:

- Application identity.
- Start Screen.
- Global styles.
- Tracking and retention settings.
- Authentication page.
- Final rendered TVML.

Do not assume:

- The Rock name is the App Store name.
- The API key secures a Lava webhook.
- A saved template is valid after Lava renders.
- A preview proves production-shell behavior.

Stop when:

- The installed version is below Rock 14.
- The target application is ambiguous.
- The task requires changing an unreviewed production key or shell package.

Sources: [Creating an App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

### Recipe: Add a cache-aware TVML page

**Outcome:** A new page that emits valid TVML and uses an intentional cache policy.

1. Select the TVML template that most closely matches the journey.
2. Create the page from the intended application.
3. Give it a clear internal name and description.
4. Write TVML using only supported elements for the selected template.
5. Add Lava using documented page merge fields.
6. Render the Lava output with anonymous and signed-in states where relevant.
7. Validate the rendered output as TVML.
8. Choose Public, Private, No-Cache, or No-Store.
9. Add navigation to the page through a documented Rock command.
10. Test focus, Back navigation, Light and Dark themes, and cached reload behavior.

Inspect:

- `CurrentPerson` branches.
- `Context` dependencies.
- Page parameters.
- `SiteStyles`.
- Theme-dependent styles.
- Sensitive output.

Do not assume:

- HTML elements or browser CSS work.
- Template behavior is portable.
- Public caching is appropriate for personalized content.

Sources: [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content) [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates)

### Recipe: Implement remote sign-in

**Outcome:** A viewer can authenticate from a phone or computer by scanning a QR code or entering a short code.

1. Create an external Rock web page.
2. Add the Remote Authentication block.
3. Associate the block with the intended TV application site.
4. Establish the external URL or route.
5. Set that page as the application’s Authentication Page.
6. Create the TV login page.
7. Display `{ authQrCodeUrl }`, `{ authCode }`, and the external page URL.
8. Create a timeout page with a clear route home.
9. Select a success page.
10. Add the `login` command with the login, timeout, and success page GUIDs.
11. Retain navigation-stack clearing unless the tested journey requires otherwise.
12. Test QR, manual-code, timeout, failure, success, and Back-button paths.

Inspect:

- External-page reachability.
- Block-to-site association.
- Authentication Page setting.
- Case-sensitive single-brace fields.
- All destination GUIDs.
- Navigation-stack behavior.

Do not assume:

- Lava double braces work for the auth fields.
- A visible QR image proves authentication completion.
- A code remains valid beyond the configured lifetime.
- Source behavior from `develop` matches the installed release.

Stop when:

- The site or destination page is ambiguous.
- Testing would expose a real authentication code or device identifier.
- Production routing changes require separate authorization.

Sources: [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)

### Recipe: Add tracked video or audio playback

**Outcome:** A supported media file plays with intentional resume and interaction behavior.

1. Select `playVideo` for MP4 or HLS, or `playAudio` for MP3.
2. Supply the direct media URL.
3. Add title, subtitle, artwork, and description when required.
4. Associate the Rock Media Element and related entity when watch tracking requires them.
5. Decide the interaction outcome before adding resume parameters.
6. Add `rockWatchMap` when a prior resume position is required.
7. Add `rockInteractionGuid` only when progress must append to that existing interaction.
8. Test initial playback.
9. Stop partway through and retest resume.
10. Verify whether the expected interaction was appended or newly created.

Inspect:

- Media format.
- Media URL.
- Resume setting.
- Watch map.
- Interaction GUID.
- Media Element association.

Do not assume:

- YouTube is supported.
- A watch map alone appends to the old interaction.
- Successful playback proves tracking succeeded.

Source: [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands)

### Recipe: Build a theme-safe styling pass

**Outcome:** Text, badges, images, and focus states remain legible in both Light and Dark themes.

1. Start with predefined `tv-text-style` values.
2. Add font weight or family only where the design requires it.
3. Add Light and Dark media-query branches.
4. Inspect badge tint and image contrast in each theme.
5. Add text shadows only when necessary.
6. Keep shadow offsets and blur close enough to avoid wrapper clipping.
7. Test system-selected themes.
8. Test any page-level theme override.
9. Test focus and highlighted states with the remote.

Inspect:

- Text contrast.
- Badge tint.
- Image contrast.
- Focused and unfocused states.
- Shadow clipping.
- Template-specific behavior.

Do not assume:

- Browser CSS support.
- A native-app reference layout is reproducible in TVML.
- A single theme test is sufficient.

Sources: [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries)

### Recipe: Prepare the application image package

**Outcome:** A delivery set contains the documented icon, launch, Top Shelf, and optional parallax assets.

1. Create three-layer app icons.
2. Export PNG foreground layers and a JPG background layer.
3. Export icon sets at 400 × 240, 800 × 480, and 1280 × 768.
4. Export static launch images at 1920 × 1080 and 3840 × 2160.
5. If Top Shelf assets are required, export the documented standard or wide PNG sizes.
6. If content parallax is required, produce an LCR file.
7. Host the LCR at a direct URL.
8. Verify that no LSR file was substituted.
9. Test focus, parallax, and launch appearance in the target shell.
10. Reconfirm current Apple packaging requirements before final submission.

Inspect:

- Dimensions.
- Layer count.
- Foreground and background formats.
- Direct LCR URL.
- Target tvOS applicability.

Do not assume:

- Flattened icons retain parallax.
- LSR works in place of LCR.
- Historical Top Shelf dimensions are current App Store requirements.

Sources: [App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons) [Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image) [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image) [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)

### Recipe: Test through demo mode

**Outcome:** The community shell loads the intended Rock application configuration for bounded testing.

1. Verify that the demo-request form and Rock Core application remain available.
2. Request a demo key.
3. Install or open Rock Core on Apple TV.
4. Open the Demo screen.
5. Enter the key.
6. Restart the application.
7. Confirm the loaded application identity.
8. Test page rendering, navigation, themes, authentication, and media separately.
9. Use `clearDemo` when the intended outcome is to restore compiled settings.

Inspect:

- Demo-mode support.
- Application identity.
- `IsDemoModeEnabled`.
- Cache behavior.
- Compiled versus demo settings.

Do not assume:

- Demo success proves App Store packaging.
- Demo support exists in every compiled shell.
- Clearing settings is reversible without knowing the compiled destination.

Sources: [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app) [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands)

### Recipe: Review a Lava API before connecting it to Apple TV

**Outcome:** The agent can state what a Lava webhook exposes and whether its protection has been verified.

1. Resolve the exact request URL and HTTP verb.
2. Identify the matching Lava Webhook Defined Value.
3. Read the complete Lava template.
4. Inventory its request inputs and output fields.
5. Inventory every enabled Lava command.
6. Identify any person or sensitive data that can be returned.
7. Verify the actual security layer outside the webhook.
8. Test unauthorized behavior with a bounded, read-only request.
9. Record only a public-safe conclusion.
10. Stop before launch if the endpoint relies on default webhook security.

Inspect:

- URL and verb matching.
- Defined Value status.
- Template output.
- Enabled commands.
- Authentication and authorization behavior.

Do not assume:

- Lava webhooks are secured by default.
- An application API key automatically protects the webhook.
- One installation’s handler behavior proves another installation’s state.

Source: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

## Known Gaps And Live Verification

Before treating an implementation as ready, verify these installation-specific or current-state questions:

- The installed Rock version and exact TV shell version.
- Whether Apple TV administration surfaces and required blocks are installed and accessible.
- The exact application record, Start Screen, default page, login page, and authentication page.
- Current application styles, page-view setting, retention period, and API-key configuration.
- The final TVML emitted by every Lava branch.
- The complete parameter contract for Set Context, Clear Context, and any navigation commands not reproduced in the supplied evidence.
- Whether persistent context survives and clears as intended in the target shell.
- Remote Authentication block permissions, route exposure, code lifetime, throttling, and installed implementation.
- The apparent tension between the Tips article’s general statement that SVG images are unsupported and the Personal Commands article’s description of the generated authentication QR code as SVG. Test the auth QR in the exact shell rather than resolving this by assumption. [Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips) [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands)
- Media URL accessibility, encoding, HLS compatibility, provider behavior, and watch-interaction writes.
- Demo-key service and Rock Core availability.
- Current Apple requirements for App Store icons, Top Shelf assets, launch assets, and native packaging.
- Template-specific focus, scrolling, animation, and overflow behavior.
- Whether the documented “TV 2.0” overflow enhancements apply to the installed shell.
- Any shell-embedded custom image resources and their extension-free names.
- Every Lava webhook’s actual security, enabled commands, and returned data.
- App Store submission, certificates, provisioning, and production-shell deployment, which are outside this evidence pack.

Do not represent any of these checks as completed unless the exact application, environment, device, and result were observed.

## Source Map

| Area | Authority and source |
|---|---|
| Platform scope, Rock 14+, TVML boundary, JavaScript caution | Official Rock documentation: [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) |
| Initial application workflow | Official Rock documentation: [Building Your First App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app) |
| Application record and settings | Official Rock documentation: [Creating an App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) |
| Page creation and cacheability | Official Rock documentation: [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content) |
| Page merge fields and TVML requirement | Official Rock documentation: [TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) |
| Persistent entity and Campus context | Official Rock documentation: [Context](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/context) |
| Remote sign-in walkthrough | Official Rock documentation: [Creating a Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) |
| Login and logout command parameters | Official Rock documentation: [Personal Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands) |
| Remote Authentication implementation observation | Immutable public source at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`: [RemoteAuthentication.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Tv/RemoteAuthentication.cs) |
| Remote-session matching observation | Immutable public source at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`: [RemoteAuthenticationSessionService.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Security/RemoteAuthenticationSessionService.cs) |
| Command families | Official Rock documentation: [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| Media playback, resume, and interactions | Official Rock documentation: [Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) |
| Demo command behavior | Official Rock documentation: [Demo Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands) |
| Demo testing workflow | Official Rock documentation: [Testing Your App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app) |
| Template behavior and customization warning | Official Rock documentation: [Templates](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates) |
| Alert, Catalog, and Product template purposes | Official Rock documentation: [Alert](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/alert-template), [Catalog](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/catalog-template), and [Product](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-template) |
| Template licensing | Official Rock-hosted license record: [Licensing](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/licensing) |
| Rock-specific controls and countdown | Official Rock documentation: [Control Reference](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference) and [Countdown](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/countdown) |
| Custom-control styling | Official Rock documentation: [RockStackView](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rockstackview) and [RockLabel](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling/rocklabel) |
| Text styles and shadows | Official Rock documentation: [TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) |
| Themes and media queries | Official Rock documentation: [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) and [Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries) |
| Built-in and shell resources | Official Rock documentation: [Built-in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images) |
| Styling-reference limitations | Official Rock documentation: [References](https://community.rockrms.com/developer/apple-tv-docs/styling/references) |
| App icon layers and sizes | Official Rock documentation: [App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons) |
| Content parallax format | Official Rock documentation: [Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images) |
| Launch image sizes | Official Rock documentation: [Launch Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image) |
| Top Shelf sizes and historical applicability | Official Rock documentation: [Top Shelf Image](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image) |
| TVML operational tips and overflow behavior | Official Rock documentation: [Tips](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips) |
| Optional Lava APIs and default-security warning | Official Rock Lava documentation: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api) |