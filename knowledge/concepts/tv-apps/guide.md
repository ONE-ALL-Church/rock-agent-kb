---
id: authored-tv-apps
title: TV Apps
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "add2a8bebb93622e020a7c84cd33a765e3c265f6bd57f15bd6c47f00059ec54a"
---

# TV Apps

## Agent Summary

Rock supports Rock-managed applications for Apple TV and Roku. In both platforms, an application behaves conceptually like a site containing pages: Rock stores application-level configuration, Lava produces platform-specific page content, and the client shell interprets commands for navigation, authentication, media playback, and other actions. Apple TV pages produce TVML; Roku pages produce SceneGraph-oriented XML rather than normal Rock CMS HTML. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) [Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started) [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

Use this operating order:

1. Confirm that the installed Rock version supports the target platform.
2. Inspect the Rock application record before changing page Lava.
3. Confirm the page produces valid markup for the target shell.
4. Inspect commands, command parameters, focus behavior, and caching separately.
5. Treat remote authentication as a coordinated website-page, application-setting, TV-page, and client-shell workflow.
6. Test on the actual target client before declaring the application operational.

Apple TV functionality requires Rock 14 or later. Roku was introduced in Rock 16.7, so Roku availability is version-sensitive. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) [Roku Docs](https://community.rockrms.com/developer/roku-docs) [GitHub Spotlight: 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)

## Scope And Boundaries

This guide covers the supplied evidence for:

- Rock-managed Apple TV and Roku application records.
- TVML and SceneGraph page rendering.
- Lava merge fields exposed to TV pages.
- Navigation, context, authentication, and media commands.
- Apple TV themes, text styling, and image resources.
- Roku controls, focus management, and layout nodes.
- Page-view configuration, page caching, remote authentication, and operational troubleshooting.

This guide does not establish App Store or Roku Channel Store submission procedures, shell packaging or signing, certificate management, vendor review requirements, API-key rotation procedures, or a complete inventory of every command and control. Those subjects require additional evidence or live inspection.

TV apps depend on adjacent Rock capabilities. Keep data access and custom APIs in the API and Lava concepts, general page administration in CMS, credentials and authorization in security, media-provider behavior in media, and shell packaging in the appropriate platform-specific deployment documentation. Rock’s Lava API documentation names Apple TV and Roku as possible custom API consumers, but it also warns that Lava webhooks have no security by default. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

## Mental Model

| Layer | Apple TV | Roku | Primary inspection |
|---|---|---|---|
| Rock application | Rock-managed TV application/site with application settings | Rock-managed Roku application/site with application settings | Version, API key, authentication page, interaction settings |
| Rock page | Lava-backed page that must render valid TVML | Lava-backed page that must render SceneGraph content | Markup validity, merge fields, caching |
| Client structure | TVML templates and controls | SceneGraph components plus Rock-provided controls | Template/control compatibility |
| Interaction | `rockCommand` attributes interpreted by the shell | `rockCommand` plus command-specific fields on supported controls | Control support, command name, parameters |
| Identity | Remote Authentication website page coordinated with TV login pages | Remote Authentication website page coordinated with Roku login commands and pages | Site association, code flow, timeout and success routes |
| Media | Shell playback commands for direct media resources | Shell playback commands for direct media resources | URL format, metadata, Media Element and watch-map parameters |

The application record is not merely a label. It holds settings used by the shell and related workflows. A page is not ordinary HTML: its Lava output must be valid for the platform renderer. Finally, a visible control is not automatically actionable; the shell only performs an action when a supported control carries a valid command and the parameters required by that command. [Creating an Apple TV App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands)

## Apple TV

### Application configuration

Apple TV is documented as a set-top extension of Rock for TVML applications linked to Rock. An administrator creates the Rock-side application under `Admin Tools > CMS Configuration > Apple TV Apps`. The application’s Rock name is private to the Rock instance and does not have to match the eventual App Store name. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) [Creating an Apple TV App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)

The documented application settings include:

- Name and optional description.
- Global application styles.
- Whether page views should be recorded.
- An API key used by the application.
- The page-view retention period.
- An authentication page used by the remote sign-in workflow.

Saving a new application creates a Start Screen. The Start Screen is intended to be the application’s home page and cannot be deleted. Inspect these application settings before diagnosing page content, because an incorrect API key, authentication page, or interaction setting cannot be repaired solely by editing TVML. [Creating an Apple TV App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app)

The supplied immutable Rock source also shows Apple TV application settings for application JavaScript, global styles, and an API key. This is implementation evidence from the referenced commit, not proof that every installed version exposes an identical editor or stores identical settings. [AppleTvApplicationSettings.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Tv/Classes/AppleTvApplicationSettings.cs)

### Pages and Lava output

Every Apple TV page must render valid TVML. The documented page context includes these Lava merge fields:

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

Use `SiteStyles` when a page should incorporate the application’s global styles. Use person, permission, parameter, device, theme, and shell-version fields only for behavior their documented values directly support; their presence does not prove that a particular person, permission, device capability, or shell feature is available in the current request. [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

The Start Screen and other pages can use Lava to conditionally render TVML. For example, navigation can display a login choice when `CurrentPerson` is absent and a profile choice when a person is present. The resulting document must still be valid TVML after Lava finishes rendering. [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)

Apple TV page settings include cacheability behavior. The documented modes are Public, Private, No-Cache, and No-Store. Public content may be stored in shared caches; Private content is limited to the client-side cache; No-Cache requires revalidation before a stored response is reused; and No-Store prevents storage. Select the mode according to the rendered content, especially when output depends on identity or other personalized values. [Adding Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)

### Commands

Commands are a core part of Rock’s Apple TV application model. The documented JavaScript command surface covers navigation, media, utility, and demo workflows, and inspected Rock TV templates have used `rockCommand` attributes for navigation, login, logout, and media playback. The exact page template and shell version still need to be checked before reusing a command pattern. [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript)

Treat the application JavaScript as shell infrastructure rather than an ordinary page customization point. The Apple TV overview directs developers primarily to TVML and notes that the application JavaScript should not normally be updated. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)

## Roku

### Application configuration

Rock’s Roku support uses Rock-managed applications and pages to deliver Roku content. The documented model resembles a website—one application with linked pages—but pages emit SceneGraph XML instead of HTML. Roku development may also require obtaining a development application from the Rock Core team through the process linked by the official getting-started documentation. Verify that this process is still current before treating it as a deployment entitlement. [Roku Docs](https://community.rockrms.com/developer/roku-docs) [Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)

The Roku application record includes:

- Enable Page Views.
- Page View Retention Duration.
- API Key.
- Authentication Page.

The Authentication Page setting refers to the website page used for remote authentication. It is distinct from the Roku page displayed by a `login` command. Begin Roku troubleshooting at this application record before changing page Lava. [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### Pages and SceneGraph output

A Roku page displays custom Lava-driven content and renders SceneGraph-oriented XML. Each page should use `Rock:Page` as its outermost component; this wrapper also provides the page’s initial-focus setting. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Rock Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)

The documented Roku page merge fields are:

- `CurrentPerson`
- `Context`
- `Campuses`
- `CurrentPage`
- `CurrentPersonCanEdit`
- `CurrentPersonCanAdministrate`
- `PageParameter`
- `TvShellVersion`

The page’s Show in Menu setting is not automatically consumed by the Roku shell. It exists so page Lava can use the setting when constructing navigation. A page marked for the menu will not appear unless the application’s Lava actually renders it into a menu or other navigation control. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

Roku pages also expose cache configuration:

- Public permits shared caching such as a CDN.
- Private limits caching to the application.
- No-Cache checks the item on each load and may reuse the last copy when it has not changed.
- No-Store prevents caching.
- Max Age controls the item’s cache duration.
- Max Shared Age controls its duration in a shared cache.

Do not use shared caching for person-specific output unless the full request and response behavior has been reviewed for identity isolation. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

## Security And Authentication

### Remote authentication architecture

The documented sign-in pattern avoids entering credentials with a TV remote:

1. Create an external website page.
2. Place a Remote Authentication block on that page.
3. Associate the block with the TV application’s site.
4. configure a route or URL to that page.
5. Select that website page as the TV application’s Authentication Page.
6. Create a TV-platform login page that displays the generated QR code and security code.
7. Connect a login command to login, timeout, and success TV pages.
8. Test the complete flow while already signed in and while signed out on the website.

For Apple TV, the login page receives `{ authQrCodeUrl }` and `{ authCode }` placeholders. These use single braces and are not ordinary double-brace Lava output. The login command identifies the Apple TV login, timeout, and success pages. [Creating an Apple TV Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page)

For Roku, the `login` command requires the application’s login configuration and accepts TV-page identifiers for the login display, timeout destination, and success destination. The documented default timeout is 600 seconds, and the default interval between authentication checks is five seconds. Clearing the navigation stack after successful login defaults to true so Back does not return to earlier impersonalized content. [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

The Roku login page has two shell-recognized view IDs:

- `lgnQrPoster`, whose image URI is populated with the login URL and verification code.
- `lgnCodeLabel`, whose text is populated with the verification code.

These identifiers are shell contracts, not Lava merge fields. A visually correct login page that omits or changes them will not receive those values through the documented mechanism. [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### Source-code observation

At the supplied immutable Rock commit, remote authentication creates a six-character code, records a device unique identifier, and verifies an active session by code, issue time, lifetime, and matching device identifier. This explains why a code copied from a different or expired session may fail, but it does not establish the configured lifetime or throttle values of a particular Rock installation. [RemoteAuthenticationSessionService.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Security/RemoteAuthenticationSessionService.cs) [RemoteAuthenticationSessionExtensions.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Security/RemoteAuthenticationSessionExtensions.cs)

The same commit describes the Remote Authentication block as a web-site block that authenticates a person to a remote system with a short-lived security code. Its initialization requires a currently authenticated website person before authentication can proceed. Treat that as implementation evidence for the referenced commit and verify the installed block version and configuration during a live review. [RemoteAuthentication.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Tv/RemoteAuthentication.cs)

### API and webhook boundary

An application API key and a Lava webhook are separate security concerns. The presence of an API key on the TV application record does not automatically secure an independently configured Lava webhook. Rock’s Lava API guide explicitly says Lava webhooks do not include security by default and advises care with exposed data. It also explains that webhook requests are matched to configured templates by HTTP verb and URL and that each Defined Value controls the Lava commands available to its template. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

Before exposing TV data through a Lava webhook, inspect:

- The exact URL and permitted HTTP verb.
- The template’s returned fields.
- The enabled Lava commands.
- Whether output contains person, financial, attendance, security, or other sensitive data.
- What compensating access control exists outside the default webhook behavior.

Do not infer authorization from obscurity, an unadvertised URL, or the TV application’s separate API-key field.

## Styling And Controls

### Apple TV themes and text

Apple TV supports Light and Dark themes. The user generally selects the theme, the application can respond with TVML media queries, and an individual page can explicitly declare a theme. Theme-aware rules use `tv-template` with `tv-theme:light` or `tv-theme:dark`. [Apple TV Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) [Apple TV Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries)

Apple TV pages are not HTML pages. The documented styling guidance favors Apple’s TV design patterns and exposes TVML text styles, font weights, inline emphasis, font families, and text shadows. Because text shadows can be clipped when the wrapper is too small, validate them in the actual TV layout rather than assuming browser-like overflow. [Apple TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)

### Apple TV images and icons

tvOS supplies built-in image resources, including button, miscellaneous, movie-rating, and TV-rating icons, along with supported SF Symbols. A custom resource embedded in the Apple TV shell can be referenced like a system resource; the documentation says to omit its file extension when referencing it. Shell embedding is a packaging concern and is not accomplished merely by placing a file in page TVML. [Apple TV Built-in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images)

The documented app-icon design uses three visual layers for the parallax effect. The supplied sizes are 400×240 pixels for the in-app 1× icon, 800×480 for the in-app 2× icon, and 1280×768 for the App Store icon. Foreground layers are PNG and the background layer is JPG. These asset specifications do not, by themselves, establish the complete current App Store submission package. [Apple TV App Icons](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons)

For parallax content images, the Rock documentation specifies a directly hosted LCR file. An indirect URL may be rendered as a flat image, and LSR files are not supported by the documented workflow. [Apple TV Parallax Images](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images)

### Roku controls, focus, and layout

Most Roku application structure uses built-in SceneGraph components. Rock adds custom components where it needs Rock-specific behavior. In particular, Rock’s `Button` and `ContentNode` extend the corresponding SceneGraph controls with `rockCommand` and command-parameter fields. [Roku Controls](https://community.rockrms.com/developer/roku-docs/resources/controls) [Rock Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button) [Rock Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)

`Rock:Page` represents a page-level group and exposes `initialFocus`, which names the control that should receive focus when the page appears. Set that field to an actual control ID in the rendered SceneGraph. [Rock Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)

The Rock `FocusGroup` arranges child views horizontally or vertically and manages directional focus among them. The documentation describes this as filling a focus-management gap as of 2024: horizontal groups handle left/right movement and vertical groups handle up/down movement. Treat the date as a historical documentation qualifier and verify current shell behavior before assuming the limitation remains unchanged. [Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)

`RowList` is suited to horizontally scrollable content organized into rows. Its content structure requires one root `ContentNode`, child nodes for rows, and child item nodes within each row. Configuration includes item size, row count, row heights, item sizes and spacing, row spacing, labels, and focus-animation styles. Rock’s guidance recommends simple layouts and identifies `RowList` as a useful media or content-selection pattern. [Roku RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist) [Roku Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks)

Roku offers many SceneGraph layouts, but relatively few provide default item templates. Rock’s documentation recommends caution when choosing SceneGraph elements and aims to avoid unnecessary custom BrightScript components. [Roku Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes)

## Commands And Media Operations

### Roku command dispatch

A Roku command is executed by placing `rockCommand` and the command-specific parameters on a supported control such as `Rock:Button` or `Rock:ContentNode`. Multiple commands can be executed from one control by separating their names with commas. A documented use case is setting context and then navigating to a page. [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands)

Keep command parameters on the same actionable control unless the control’s documentation says otherwise. A command name without its required page, media, context, or login fields is incomplete.

### Navigation and context

Roku’s documented navigation commands include:

- `pushPage` to add a page to the navigation stack.
- `replacePage` to replace the top page while retaining the rest of the stack.
- `popPage` to remove the top page.
- `clearNavigationStack` to remove all pages except the root.

Page-navigation parameters can include the target page with query parameters, cache-control behavior, whether to show a loading screen, and whether to suppress writing an interaction. The documented command-level cache choices include Public, Personal, and Private. Personal caching varies the URL by the logged-in person; Public does not. [Roku Navigation Commands](https://community.rockrms.com/developer/roku-docs/commands/navigation)

The `setContext` command stores a keyed context value for the lifetime of the application until it closes. `clearContext` removes the value for the specified key. When chaining context and navigation, confirm that the destination page reads the same key from `Context`. [Roku Utility Commands](https://community.rockrms.com/developer/roku-docs/commands/utility)

### Media playback and watch state

Apple TV and Roku provide commands to play video and audio. The documented direct formats are MP4 or HLS for video and MP3 for audio. Both platform guides state that YouTube content cannot be played through these TV application media commands. [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) [Roku Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

Media commands can carry:

- A direct media URL.
- A Rock Media Element identifier when the resource is a Rock Media Element.
- Related entity information.
- Resume behavior.
- Title, subtitle, artwork, and description.
- An existing interaction identifier.
- A watch map.
- For Roku video, a live-stream indicator.

For an existing interaction, providing its watch map supplies the resume position. Providing both the interaction identifier and watch map appends to that interaction. Providing a watch map without the interaction identifier uses the prior position for resume but creates a new interaction with a new watch map. [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) [Roku Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

## Version And Authority Caveats

- Apple TV functionality is documented for Rock 14 and later. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs)
- Roku was introduced in Rock 16.7. [Roku Docs](https://community.rockrms.com/developer/roku-docs)
- The supplied Triumph release note independently places the Roku addition at Rock 16.7, but it is release-note evidence rather than the primary configuration reference. [GitHub Spotlight: 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024)
- The developer articles in the evidence pack report documentation version `1.0.0`; that article version must not be confused with the installed Rock version or TV shell version.
- Statements drawn from the Rock developer documentation describe documented product behavior. They do not prove that a particular installation has the necessary version, site records, blocks, keys, routes, pages, or shell package.
- Source-code observations in this guide are pinned to commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They clarify that implementation only and should not be generalized to a different release without comparison.
- The approved claims include a bounded read-only review that found TV application administration surfaces and command patterns in one connected installation. That supports the existence of those surfaces and patterns but does not establish another organization’s configuration or a working device deployment.
- The 2024 focus-management statement is historical documentation. Re-test it against the target Roku shell and current documentation.
- No community contribution was supplied for this guide, so no community pattern is presented as official behavior.

## Troubleshooting Decision Tree

### The TV application administration feature is missing

1. Identify the target platform.
2. Confirm the installed Rock version: Apple TV requires Rock 14 or later; Roku requires Rock 16.7 or later.
3. Confirm that the expected TV application administration blocks and site types exist in the installed package.
4. Confirm the operator has permission to view and administer the relevant CMS configuration pages.
5. For Roku development, verify whether the current Core-team development-application process is required and has been completed.
6. Stop page-level debugging until the application record can be opened. [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) [Roku Docs](https://community.rockrms.com/developer/roku-docs) [Roku Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)

### A page is blank, rejected, or never appears

1. Confirm that the page belongs to the intended TV application.
2. Render the Lava and inspect the final output, not just the template source.
3. For Apple TV, validate the result as TVML.
4. For Roku, validate it as SceneGraph XML and confirm `Rock:Page` is the outermost component.
5. Check for missing or malformed data emitted through Lava.
6. Inspect page cache settings to rule out an older response.
7. Test the page in the target shell; browser rendering is not equivalent to TVML or SceneGraph rendering. [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

### A Roku page marked “Show in Menu” is absent

1. Confirm that the page setting is enabled.
2. Inspect the Lava that constructs the menu.
3. Confirm that the page collection and Show in Menu value are actually read by that Lava.
4. Confirm that the resulting SceneGraph contains an actionable menu item.
5. Do not assume the Roku shell creates menus automatically from the setting. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

### Roku focus does not move or starts on the wrong item

1. Confirm the rendered page has an outer `Rock:Page`.
2. Check that `initialFocus` exactly matches a rendered control ID.
3. Confirm the target control is present and focusable.
4. For a horizontal or vertical group, verify the `FocusGroup` orientation.
5. For a `RowList`, verify the required root, row, and item `ContentNode` hierarchy.
6. Reduce the page to a simple layout before introducing additional SceneGraph or custom BrightScript components. [Rock Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page) [Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) [Roku RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)

### A command does nothing

1. Confirm that the element is a control documented to support `rockCommand`.
2. Check the exact command name.
3. Check every required command-specific parameter.
4. For navigation, verify the destination page belongs to the application and that any query parameters are valid.
5. For chained Roku commands, verify comma separation and validate each command independently before recombining them.
6. Inspect whether stale cached markup still contains an older command.
7. Test in the actual shell version because a valid attribute in documentation does not prove support in an older client. [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands) [Rock Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button) [Rock Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)

### Remote sign-in shows no QR code or code

1. Confirm the application record points to the intended external website Authentication Page.
2. Confirm that page contains the Remote Authentication block.
3. Confirm the block is associated with the correct TV application site.
4. Confirm the person can reach the website route.
5. For Apple TV, verify the login page contains the single-brace `{ authQrCodeUrl }` and `{ authCode }` placeholders.
6. For Roku, verify the page contains controls with IDs `lgnQrPoster` and `lgnCodeLabel`.
7. Confirm the login command targets the correct login, timeout, and success TV pages. [Creating an Apple TV Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### A remote-authentication code is rejected

1. Confirm the website user is authenticated.
2. Confirm the code belongs to the currently displayed device session.
3. Retry with a newly generated code to eliminate expiration.
4. Confirm the website Remote Authentication block is associated with the same TV application site.
5. Check the configured expiration and throttling settings in the installed block.
6. Inspect server logs or the block’s returned error without exposing codes or session records.
7. Stop before modifying authentication records directly. At the supplied source commit, verification depends on an active session, matching code timing, and the device unique identifier. [RemoteAuthentication.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Tv/RemoteAuthentication.cs) [RemoteAuthenticationSessionService.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Security/RemoteAuthenticationSessionService.cs)

### Media does not start

1. Confirm the command is attached to a supported actionable control.
2. Confirm that video uses a direct MP4 or HLS resource, or that audio uses a direct MP3 resource.
3. Do not use a YouTube page URL.
4. Confirm the TV device can reach the media URL.
5. Remove optional Media Element, interaction, watch-map, artwork, and related-entity parameters and test direct playback.
6. Add metadata and tracking parameters back one group at a time.
7. For live Roku video, verify the live-stream parameter and source behavior. [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) [Roku Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

### Playback starts at the wrong position or creates a new interaction

1. Confirm whether the intended outcome is resume-only or appending to an existing interaction.
2. For resume-only, inspect the supplied watch map.
3. To append, supply both the existing interaction identifier and its watch map.
4. If only the watch map is supplied, expect the documented behavior to use its position while creating a new interaction.
5. Confirm that the correct Rock Media Element identifier is supplied when Rock-managed watch tracking is expected. [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) [Roku Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

### A page shows stale or another context’s content

1. Determine whether the rendered output varies by person, context, query parameter, or authentication state.
2. Inspect the page’s cacheability type, Max Age, and Max Shared Age where applicable.
3. Inspect command-level cache control on Roku navigation.
4. Do not use Public caching for personalized output without a reviewed isolation design.
5. Clear or bypass the relevant cache in a controlled test.
6. Re-render with two distinct test contexts and confirm they cannot receive each other’s output. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Roku Navigation Commands](https://community.rockrms.com/developer/roku-docs/commands/navigation) [Adding Apple TV Content](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content)

## Agent Task Recipes

### Recipe: Create an Apple TV application skeleton

**Outcome:** A Rock-managed Apple TV application with a valid Start Screen and explicitly reviewed application settings.

1. Confirm Rock 14 or later.
2. Open `Admin Tools > CMS Configuration > Apple TV Apps`.
3. Create the application with an internal name and optional description.
4. Review global styles, page-view tracking, retention, API key, and Authentication Page.
5. Save and open the generated Start Screen.
6. Add the smallest valid TVML document that the target shell can render.
7. Test the Start Screen in the target Apple TV client.

**Inspect:**

- Installed Rock and shell versions.
- The generated Start Screen.
- Final TVML after Lava rendering.
- Page cacheability.

**Do not assume:**

- The Rock-side name becomes the App Store name.
- Saving the Rock record packages or publishes an App Store application.
- Browser-valid markup is valid TVML.

**Stop when:**

- The application record and Start Screen exist, and the target client renders the minimal page. [Creating an Apple TV App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)

### Recipe: Build a Roku content page

**Outcome:** A Roku page whose rendered SceneGraph loads with deterministic initial focus.

1. Confirm Rock 16.7 or later and an available Roku development shell.
2. Open the intended Roku application record and review its application settings.
3. Create a page with the required name and cache settings.
4. Render a `Rock:Page` as the outer component.
5. Add one focusable `Rock:Button` with a unique ID.
6. Set `initialFocus` to that ID.
7. Validate the post-Lava SceneGraph.
8. Load the page on the Roku client and test directional focus.

**Inspect:**

- Application API and authentication settings.
- Final SceneGraph structure.
- Focusable control IDs.
- Cacheability and age settings.

**Do not assume:**

- Show in Menu creates navigation automatically.
- HTML or TVML can be reused as SceneGraph.
- A visible component is focusable.

**Stop when:**

- The page renders on the target Roku client and initial focus lands on the intended control. [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Rock Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)

### Recipe: Add Roku navigation with application context

**Outcome:** Selecting one control sets a context value and opens a destination page that reads it.

1. Choose a context key and bounded value.
2. Confirm the destination page reads that key from `Context`.
3. Place `setContext` on a supported Rock control and test it independently.
4. Place `pushPage` on a supported control and test the destination independently.
5. Combine the commands with comma-separated names.
6. Keep the context and navigation parameters on the actionable control.
7. Test a fresh application session and a session where the context is changed.
8. Add `clearContext` to the appropriate reset path.

**Inspect:**

- Exact context key spelling.
- Destination page identifier and parameters.
- Navigation cache control.
- Whether the page output varies by person or context.

**Do not assume:**

- Context survives after the application closes.
- Public caching is safe for context-dependent output.
- Two individually failing commands will work when chained.

**Stop when:**

- The destination renders the selected context, and clearing the context removes it. [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands) [Roku Utility Commands](https://community.rockrms.com/developer/roku-docs/commands/utility) [Roku Navigation Commands](https://community.rockrms.com/developer/roku-docs/commands/navigation)

### Recipe: Configure remote TV sign-in

**Outcome:** A person can authenticate on a website and the TV client transitions to the configured success page.

1. Create an external website page containing the Remote Authentication block.
2. Associate the block with the intended TV application site.
3. Give the page a reachable route.
4. Select that website page as the application’s Authentication Page.
5. Create distinct TV pages for login display, timeout, and success.
6. Add the platform-specific QR-code and code placeholders or recognized Roku control IDs.
7. Add a `login` command with the three TV-page destinations.
8. Test QR navigation, manual-code entry, timeout, success, and Back behavior.
9. Test while signed out of the website and while already signed in.

**Inspect:**

- Website authentication state.
- Site association on the Remote Authentication block.
- Application Authentication Page.
- Code expiration and check interval.
- Navigation-stack clearing after success.

**Do not assume:**

- The application API key secures the website Remote Authentication page.
- The website Authentication Page and TV login-display page are the same page.
- A code from one device session can authenticate another.

**Stop when:**

- A newly created device session authenticates through the website and the same TV client reaches the success page without exposing prior anonymous content through Back navigation. [Creating an Apple TV Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### Recipe: Add tracked media playback with resume

**Outcome:** A supported media resource plays and resumes according to an explicitly selected interaction strategy.

1. Choose a direct MP4 or HLS video URL, or a direct MP3 audio URL.
2. Prove playback with only the command and direct URL.
3. If the resource is a Rock Media Element, add its identifier.
4. Add title, subtitle, artwork, and description as needed.
5. Decide whether to resume from prior state or append to an existing interaction.
6. For resume-only, pass the prior watch map.
7. To append, pass both the prior interaction identifier and watch map.
8. Test first play, interrupted play, resumed play, and completion.
9. Confirm whether a new or existing interaction was expected.

**Inspect:**

- Media format and reachability.
- Media Element association.
- Resume flag.
- Interaction identifier and watch map.
- Live-stream treatment for Roku when applicable.

**Do not assume:**

- A YouTube URL can be passed to the media command.
- A watch map alone appends to the original interaction.
- Playback success proves tracking success.

**Stop when:**

- Playback, metadata, resume position, and interaction behavior independently match the intended outcome. [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) [Roku Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

### Recipe: Make an Apple TV page theme-aware

**Outcome:** One TVML page remains legible in both Light and Dark themes.

1. Apply global application styles through the documented site-style mechanism.
2. Add Light and Dark `tv-template` media-query rules for colors that need to change.
3. Use documented TVML text styles before introducing custom font choices.
4. Test the page in both user-selected themes.
5. If declaring a page-specific theme, retest all text, imagery, badges, and focus states.
6. Validate shadows and overlays for clipping.

**Inspect:**

- `SiteStyles` output.
- Light and Dark contrast.
- Text wrapper dimensions.
- Image and overlay behavior under focus.

**Do not assume:**

- HTML/CSS behavior transfers directly to TVML.
- A page-specific theme fixes hard-coded colors.
- Simulator appearance proves the final television presentation.

**Stop when:**

- The target client renders readable text and recognizable focus states in both themes. [Apple TV Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) [Apple TV Media Queries](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries) [Apple TV Text Style](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style)

## Known Gaps And Live Verification

The evidence does not establish:

- Current App Store or Roku Channel Store submission, signing, packaging, or review requirements.
- How the current Roku development-application request process applies to a specific organization.
- API-key creation, scope, rotation, revocation, or storage procedures.
- A complete Apple TV or Roku command inventory.
- The installed schema, blocks, routes, site records, or shell versions of an arbitrary Rock instance.
- Whether a particular media provider permits or produces compatible direct streams.
- Current behavior of every Roku SceneGraph control or focus mechanism.
- Accessibility behavior, overscan behavior, remote-control ergonomics, or performance on specific TV hardware.
- Successful end-to-end deployment to a physical Apple TV or Roku device.
- Security controls added outside the default Lava webhook mechanism.

A bounded live review should therefore verify:

1. Exact Rock version and installed TV components.
2. Exact TV application record and site type.
3. Application API key and Authentication Page configuration without exposing the key.
4. Page ownership, security, routes, and final rendered markup.
5. Enabled Lava commands and returned fields for any TV-facing webhook.
6. Target shell version and device reachability.
7. Login, timeout, logout, and navigation-stack behavior.
8. Public, private, person-specific, and shared-cache behavior.
9. Media playback, resume, and interaction writes.
10. Physical-device rendering, focus, and remote-control navigation.

Do not describe the app as live, authenticated, published, or device-verified until those exact outcomes have been observed.

## Source Map

| Guide area | Primary evidence | Authority and use |
|---|---|---|
| Apple TV platform and minimum version | [Apple TV Docs](https://community.rockrms.com/developer/apple-tv-docs) | Official documentation; approved claim `claim:49b86c70fc03c6969d42` |
| Apple TV application record | [Creating an Apple TV App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) | Official configuration guidance; approved claim `claim:30ff6291c1d3a92fea69` |
| Apple TV pages and merge fields | [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) | Official behavior; approved claim `claim:5bd2b6b4cac279be5e13` |
| Apple TV command model | [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript) | Official implementation pattern; approved claim `claim:29f4e0bbc81c08861367` |
| Apple TV styling and assets | [Styling](https://community.rockrms.com/developer/apple-tv-docs/styling), [Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes), [Built-in Images](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images) | Official platform-specific guidance |
| Roku platform and version | [Roku Docs](https://community.rockrms.com/developer/roku-docs), [GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-1042024) | Official overview plus release-note confirmation; approved claims `claim:669456b72f0978dc418a` and `claim:52b50da71870c1d611da` |
| Roku application record | [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) | Official configuration guidance; approved claim `claim:a43c6281e5328e7cac68` |
| Roku pages | [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) | Official behavior; approved claim `claim:563e520ec15928e19628` |
| Roku commands | [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands) | Official implementation pattern; approved claim `claim:9398f3fb18e8a79c0e4d` |
| Authentication | [Apple TV Sign-in Page](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page), [Roku Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal) | Official workflow documentation |
| Remote-auth implementation | [RemoteAuthentication.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Tv/RemoteAuthentication.cs), [RemoteAuthenticationSessionService.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Security/RemoteAuthenticationSessionService.cs) | Immutable public source excerpts; implementation evidence only |
| Media playback | [Apple TV Media Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands), [Roku Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media) | Official command documentation |
| Lava webhook security | [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api) | Official security warning; approved claim `claim:410bf6750e90b7193262` |