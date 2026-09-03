---
id: authored-roku
title: Roku Apps
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "692a9e2e363a64d1bcc3e5685934418c1e59419b4d642478315b564b44cd5911"
---

# Roku Apps

## Agent Summary

Rock’s Roku support provides a Rock-managed way to deliver digital ministry content through a Roku TV application. A Roku application is organized much like a website: an application contains pages, pages render dynamic content through Lava, and commands connect controls to navigation, playback, context, and authentication behavior. The output is Roku SceneGraph XML rather than normal CMS HTML. Roku support was introduced in Rock v16.7. [Roku Docs](https://community.rockrms.com/developer/roku-docs) [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)

For most investigations, work from the outside inward:

1. Confirm that the Rock version and Roku development application are applicable.
2. Inspect the Roku application record, especially its API key, authentication page, page-view settings, and retention setting.
3. Inspect the target page’s SceneGraph content and cache settings.
4. Confirm that the page is rooted in `Rock:Page` and has a valid initial-focus target.
5. Inspect the actionable control, its `rockCommand`, and every parameter required by that command.
6. If the command plays media, validate the resource format and the interaction/resume inputs.
7. If a custom Lava webhook or API participates in the flow, review its exposure separately; Lava webhooks do not provide security by default. [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Commands](https://community.rockrms.com/developer/roku-docs/commands) [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

Do not treat a valid page template as proof that the installed Roku shell can load it, that authentication works, that media is reachable from a device, or that tracking is being written. Those outcomes require testing against the applicable installation and Roku client.

## Scope And Boundaries

This guide covers the evidence-supported Rock Roku surfaces:

- Obtaining a development application.
- Application configuration.
- Lava-driven SceneGraph pages.
- Page and navigation caching.
- Rock-provided SceneGraph controls.
- Initial focus and directional focus groups.
- Navigation, utility, personal, video, and audio commands.
- Media resume and interaction behavior.
- RowList structure and layout selection.
- Lava API security boundaries.
- Operational troubleshooting and verification.

Rock’s Roku documentation describes the integration as a way to create and manage Roku apps backed by Rock content. It does not establish that every Rock installation already has a configured application, valid credentials, published pages, reachable media, or a working device package. [Roku Docs](https://community.rockrms.com/developer/roku-docs)

This guide also distinguishes two kinds of “commands”:

- A Roku command is named in a control’s `rockCommand` field and is interpreted by the Roku application.
- A Lava command runs while Rock renders a Lava template and can expose or modify Rock data according to its own configuration.

The supplied evidence supports Roku command behavior and the general Lava webhook security warning. It does not establish that any particular Lava command is enabled for a Roku page or webhook. [Commands](https://community.rockrms.com/developer/roku-docs/commands) [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

Authentication, general API design, Lava authoring, CMS administration, media-provider configuration, and broader TV-app architecture remain owning topics of their respective guides.

## Mental Model

A Rock Roku experience has four operational layers:

1. **Application configuration.** The application record holds settings such as the API key, website authentication page, page-view tracking, and page-view retention.
2. **Page generation.** Each Roku page contains Lava-driven SceneGraph content. Lava evaluates on the Rock side and produces SceneGraph-oriented output for the TV application.
3. **SceneGraph controls and layout.** Built-in Roku SceneGraph nodes form most of the interface. Rock-provided controls add integration behavior such as commands and focus management.
4. **Command execution.** Supported controls carry a `rockCommand` and command-specific fields. The Roku shell interprets those values to navigate, manage context, authenticate a person, or play media. [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Controls](https://community.rockrms.com/developer/roku-docs/resources/controls) [Commands](https://community.rockrms.com/developer/roku-docs/commands)

A useful diagnostic chain is:

`application record → page settings → rendered SceneGraph → focusable control → rockCommand → external dependency`

The external dependency might be another page, a media URL, an authentication page, or a Rock endpoint. Begin at the application record because an incorrect API key, authentication page, or tracking setting can affect the experience before page Lava becomes relevant. This ordering is supported by approved claim `claim:a43c6281e5328e7cac68`.

## Getting Started And Application Configuration

Rock’s documented onboarding path requires contacting the Rock Core team through the designated development-application request form. The Core team then supplies setup instructions. Do not assume that installing or upgrading Rock alone provisions a development Roku application. [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started)

Before authoring pages, inspect these application settings:

- **Enable Page Views:** Controls whether page interactions are written for application-usage tracking.
- **Page View Retention Duration:** Sets how many days those page interactions are retained.
- **API Key:** Connects the Roku application to Rock.
- **Authentication Page:** References a website page used for remote authentication inside the TV application. [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)

Treat these settings independently. Enabling page views does not demonstrate that interactions are being written. Having an authentication page selected does not demonstrate that the QR flow succeeds. The application API key also must not be treated as evidence that a separate custom Lava webhook is protected.

For an initial setup review:

1. Confirm Rock v16.7 or later.
2. Confirm that a development application was supplied through the documented onboarding process.
3. Inspect the application record.
4. Record whether tracking is intended and what retention period is configured.
5. Confirm that an API key is configured without exposing its value.
6. If login is required, confirm that a website authentication page is selected.
7. Continue to page inspection only after the application-level prerequisites are understood. [Roku Docs](https://community.rockrms.com/developer/roku-docs) [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)

## Page Authoring And Caching

A Roku page displays custom, Lava-driven content within the application. Its SceneGraph content is not ordinary Rock CMS HTML. Every page should use `Rock:Page` as the outermost component so the page can identify the element that receives initial focus. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)

A minimal structural pattern is:

```xml
<Rock:Page initialFocus="primaryAction">
    <Rock:Button
        id="primaryAction"
        text="Continue"
        rockCommand="pushPage"
        rockPageGuid="{{ destinationPageGuid }}" />
</Rock:Page>
```

The placeholder must be replaced with a valid page identifier supplied through an appropriate configuration or Lava value. The important structural requirements are that `Rock:Page` owns the page content and that `initialFocus` matches the ID of an actual focusable child.

The documented page merge fields include:

- `CurrentPerson`
- `Context`
- `Campuses`
- `CurrentPage`
- `CurrentPersonCanEdit`
- `CurrentPersonCanAdministrate`
- `PageParameter`
- `TvShellVersion`

These fields make it possible for page Lava to vary SceneGraph output based on the current person, application context, campus data, page information, page parameters, permissions, or shell version. Their availability does not prove that any specific value is populated for a given request. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

The **Show in Menu** setting is not automatically used by the Roku shell. It exists so page authors can build their own navigation menus in Lava. An enabled setting therefore does not, by itself, explain whether a menu item is visible. Inspect the Lava that selects and renders menu pages. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

Page-level cacheability supports four documented modes:

- **Public:** The response can be stored by shared network caches such as a CDN.
- **Private:** The response can be cached only by the application.
- **No-Cache:** The page is revalidated on each load and may reuse the previous item when it has not changed.
- **No-Store:** The page is not cached.
- **Max Age:** Controls application-cache retention.
- **Max Shared Age:** Controls shared-cache retention. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

Navigation commands expose a separate `rockPageCacheControl` field with documented `Public`, `Personal`, and `Private` choices. `Public` and `Personal` can include a seconds suffix such as `:600`; personal caching varies the requested URL by the logged-in person. The evidence does not define precedence between navigation-command cache control and page-record cache settings. When stale or cross-person output is suspected, inspect both surfaces and verify the final behavior on the applicable shell and delivery path. [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)

## SceneGraph Controls And Focus

Rock Roku applications use Roku’s SceneGraph XML language. Most of an application should be composed from Roku’s built-in SceneGraph components, with Rock-provided custom components used where Rock integration behavior is needed. [Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)

The evidence pack covers four Rock controls:

- **`Rock:Page`:** Represents the full page and provides the `initialFocus` field.
- **`Rock:Button`:** Extends Roku’s Button with `rockCommand` and command-specific fields.
- **`Rock:ContentNode`:** Extends Roku’s ContentNode with `rockCommand` and command-specific fields.
- **`Rock:FocusGroup`:** Extends LayoutGroup to arrange children and manage directional focus. [Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page) [Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button) [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node) [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)

Use a Button when the interface exposes an explicit action. Use a ContentNode when command metadata belongs to an item in a content hierarchy or list. In either case, setting only `rockCommand` is insufficient when the selected command requires additional fields.

`Rock:FocusGroup` supports two documented orientations:

- `layoutDirection="horiz"` arranges children horizontally and manages left/right focus.
- `layoutDirection="vert"` arranges children vertically and manages up/down focus. [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)

Example:

```xml
<Rock:Page initialFocus="firstAction">
    <Rock:FocusGroup layoutDirection="horiz">
        <Rock:Button
            id="firstAction"
            text="Browse"
            rockCommand="pushPage"
            rockPageGuid="{{ browsePageGuid }}" />
        <Rock:Button
            id="secondAction"
            text="Search"
            rockCommand="pushPage"
            rockPageGuid="{{ searchPageGuid }}" />
    </Rock:FocusGroup>
</Rock:Page>
```

When focus fails, first confirm that the `initialFocus` ID exists and is focusable. Then confirm that the surrounding FocusGroup orientation matches the intended remote-control direction.

## Roku Command Model

Commands execute when an applicable control supplies:

- A `rockCommand`.
- Every parameter required by that command.

Rock documents `Rock:Button` and `Rock:ContentNode` as applicable command-bearing controls. Multiple commands can be placed in one `rockCommand` value by separating command names with commas. [Commands](https://community.rockrms.com/developer/roku-docs/commands)

For example, a single control can set context and then navigate:

```xml
<Rock:ContentNode
    rockCommand="setContext, pushPage"
    rockContextKey="Campus"
    rockContextValue="{{ selectedCampusValue }}"
    rockPageGuid="{{ destinationPageGuid }}" />
```

Comma chaining is documented, but the supplied evidence does not independently establish failure handling, rollback behavior, or whether later commands run after an earlier command fails. Do not assume that a chain is transactional. If order or partial execution matters, test the exact chain in the applicable Roku shell.

The documented command categories are:

- Navigation
- Media
- Utility
- Personal [Commands](https://community.rockrms.com/developer/roku-docs/commands)

## Navigation Commands

Rock documents four navigation operations:

- **`pushPage`:** Adds a page to the navigation stack.
- **`replacePage`:** Replaces the top page while retaining the rest of the stack.
- **`popPage`:** Removes the top page.
- **`clearNavigationStack`:** Removes every page except the root page. [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)

Both `pushPage` and `replacePage` accept:

- `rockPageGuid`, including optional query-string parameters.
- `rockPageCacheControl`.
- `rockPageShowLoading`, which defaults to `false`.
- `rockPageSuppressInteraction`, which defaults to `false`. [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)

Choose the stack operation according to the intended Back-button behavior:

- Use `pushPage` when the current page should remain beneath the destination.
- Use `replacePage` when returning to the current page would be undesirable.
- Use `popPage` to return by removing the current page.
- Use `clearNavigationStack` when the flow should return to a clean root-level state.

These are navigation semantics, not proof that the destination exists or is accessible. Validate the destination page, its parameters, and its rendered SceneGraph separately.

## Application Context Commands

The utility command set provides:

- **`setContext`:** Stores a key and value for the lifetime of the application, until it is closed.
- **`clearContext`:** Removes the context value identified by a key. [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)

Example:

```xml
<Rock:ContentNode
    rockCommand="setContext"
    rockContextKey="Campus"
    rockContextValue="{{ selectedCampusValue }}" />
```

A page can access application context through its documented `Context` merge field. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

When context-dependent content is wrong:

1. Inspect the exact key used by `setContext`.
2. Compare it with the key read by page Lava.
3. Confirm that the expected value was selected.
4. Check whether `clearContext` ran.
5. Restart the application when testing lifetime behavior, because the documented context lifetime ends when the application closes. [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility)

## Remote Authentication And Personal Commands

A Rock Roku application can reference a website authentication page for remote authentication in the TV application. The personal login command depends on that application-level page because it is used to configure the QR-code flow. [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

The login control supports:

- `rockLoginPageGuid`: The Roku page that displays login information.
- `rockLoginTimeoutPageGuid`: The page shown when the login period expires.
- `rockLoginSuccessPageGuid`: The page shown after successful authentication.
- `rockLoginTimeoutDuration`: Timeout in seconds; documented default is 600 seconds.
- `rockLoginCheckDuration`: Interval between authentication-status checks; documented default is five seconds.
- `rockLoginClearNavigationStack`: Whether the stack is cleared after login; documented default is `true`. [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

The login page uses specific SceneGraph IDs because the platform cannot use normal merge fields for these values:

- `lgnQrPoster`: Receives the login-page URI with the verification code appended.
- `lgnCodeLabel`: Receives the verification-code text. [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

A login flow can therefore fail even when the command itself is present. Inspect the application’s website authentication page, the Roku login page, the required SceneGraph IDs, the timeout/success destinations, and the polling interval.

The personal-command documentation also describes logout behavior with:

- `rockLogoutPageGuid`: The destination after logout.
- `rockLogoutClearNavigationStack`: Whether to clear the stack before logout; documented default is `true`. [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

Clearing the navigation stack after login or logout reduces the chance of returning to content generated for the previous person or anonymous state. It does not replace correct page caching and personalization controls.

## Media Playback And Watch Progress

Rock documents `playVideo` and `playAudio` commands. Video resources must be directly playable MP4 or HLS resources. YouTube content cannot be played by the Rock Roku TV application. Audio resources are documented as MP3 files. [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

A basic video control follows this pattern:

```xml
<Rock:ContentNode
    rockCommand="playVideo"
    rockVideoUrl="{{ directVideoUrl }}"
    rockVideoEnableResume="true"
    rockVideoTitle="{{ title }}" />
```

Documented video metadata and behavior fields include:

- Direct video URL.
- Rock media-element identifier.
- Related entity type and entity identifiers.
- Resume enablement, defaulting to `true`.
- Title, subtitle, artwork URL, and description.
- Interaction GUID and watch map.
- A live-stream flag that tells the player to treat the resource as live and jump to live. [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

The audio command similarly supports a direct MP3 URL, media-element association, related-entity information, resume behavior, metadata, an interaction GUID, and a watch map. [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

Resume and tracking inputs have distinct effects:

- Supplying an existing `rockWatchMap` sets the resume position.
- Supplying both `rockWatchMap` and `rockInteractionGuid` appends progress to the existing interaction.
- Supplying a watch map without an interaction GUID resumes from the previous position but creates a new interaction with a new watch map beginning at that resumed location. [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

Do not assume that enabling resume proves tracking continuity. Inspect whether the media is associated with a Rock Media Element, whether the correct interaction GUID was supplied, and whether the prior watch map belongs to the intended playback history.

The supplied media table contains at least one apparent documentation inconsistency around a media-element field’s type or description. Confirm the currently installed shell’s expected field contract before relying on that row for implementation.

## Layout Nodes And RowList

Rock recommends keeping Roku layouts simple and using layout controls such as RowList for media or content selection. Most Roku layouts do not provide default item templates, so element selection should favor built-in SceneGraph components where possible and avoid unnecessary custom BrightScript components. [Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks) [Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes)

RowList is designed for horizontally scrollable series of items and supports vertical and horizontal scrolling across its rows and items. Its documented configuration includes item size, visible-row count, row heights, per-row item size and spacing, row spacing, row-label visibility, and focus-animation styles. Row data can supply a title, while item data can supply `hdposterurl`. [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)

Its required content hierarchy is:

1. One root ContentNode for the RowList’s `content` field.
2. One child ContentNode per row.
3. Child ContentNodes beneath each row for its items. [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)

Example structure:

```xml
<RowList id="mediaRows">
    <Rock:ContentNode role="content">
        <Rock:ContentNode id="featuredRow" title="Featured">
            <Rock:ContentNode id="featuredItem" />
        </Rock:ContentNode>
        <Rock:ContentNode id="recentRow" title="Recent">
            <Rock:ContentNode id="recentItem" />
        </Rock:ContentNode>
    </Rock:ContentNode>
</RowList>
```

When a RowList is blank or malformed, inspect the hierarchy before changing layout measurements. A missing root content node, row node, or item node can invalidate the intended data structure.

For additional platform-level behavior, use Roku’s [SceneGraph reference](https://developer.roku.com/en-gb/docs/references/references-overview.md) and [Roku sample applications](https://github.com/rokudev/samples). Those resources describe Roku’s platform; Rock-specific behavior should still be verified against Rock’s Roku controls and command documentation. [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources)

## Security And API Guardrails

Rock identifies Roku channels as one use case for custom APIs built with Lava. The documented Lava webhook mechanism matches a request to a configured template and renders that template, but it does not include security by default. Each webhook configuration also determines which Lava commands are available to its template. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

The evidence pack includes a reviewed, public-safe conclusion from a separate read-only inspection: the inspected Lava webhook path matched configured requests and rendered enabled Lava without an explicit permission check in that handler path. That conclusion reinforces the official warning but does not establish the configuration of any other installation. This is approved claim `claim:410bf6750e90b7193262`.

When a Roku implementation uses a custom Lava endpoint:

- Identify the endpoint separately from the normal Roku application API-key configuration.
- Inspect how requests are authenticated or otherwise constrained.
- Review the data returned by the template.
- Review every enabled Lava command.
- Assume neither page permissions nor the Roku application API key automatically protects the custom webhook.
- Do not expose endpoint secrets, API keys, person data, or raw payloads in diagnostic output.
- Stop before enabling commands or changing endpoint configuration unless the change is explicitly authorized.

The existence of an API key on the Roku application record and the absence of default security on Lava webhooks are both documented facts, but the supplied evidence does not establish how they interact in a particular implementation. Verify that boundary live.

## Version And Authority Caveats

Roku support was introduced in Rock v16.7 according to Rock’s Roku documentation. A Triumph GitHub Spotlight for a v17.0.29 pre-alpha also reports that the Roku TV app feature was added for Rock v16.7. Roku guidance is therefore version-sensitive. [Roku Docs](https://community.rockrms.com/developer/roku-docs) [Triumph GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-1042024)

Authority boundaries:

- Rock’s Roku developer documentation is the primary authority for application settings, pages, controls, commands, layouts, and media behavior.
- The approved claims are the factual spine of this draft.
- The Triumph article is release-note-confirmed secondary evidence for the v16.7 introduction.
- The supplied live-verification conclusions are bounded observations from one read-only review and are not universal configuration claims.
- No immutable Roku-specific source-code excerpt was supplied. The nearest supplied Rock source match, [`LavaCommandsPicker.cs`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Web/UI/Controls/Pickers/LavaCommandsPicker.cs), only shows how core Rock enumerates Lava commands for an administrative picker; it is not implementation evidence for Roku behavior.
- No community contribution or recipe was supplied for this concept.
- No device-level Roku test was supplied.
- The documentation excerpts are marked version 1.0.0, but the evidence does not map every field or command to specific Rock or Roku-shell releases.

Before applying this guide to an installation, confirm the Rock version, installed TV/Roku components, Roku shell version, and relevant page or command fields.

## Troubleshooting Decision Tree

### The Roku application cannot connect to Rock

1. Confirm that the installation is on Rock v16.7 or later.
2. Confirm that the organization received the documented development-application setup.
3. Inspect the Roku application record before inspecting page Lava.
4. Confirm that an API key is configured without exposing it.
5. Determine whether the failure concerns the normal Roku integration or a separate custom Lava endpoint.
6. If a Lava webhook is involved, review its authentication and enabled commands separately because webhook security is not provided by default.
7. Stop when confirming connectivity would require changing credentials or exposing a secret. [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

### A page is blank or does not render as expected

1. Confirm that the page contains SceneGraph-oriented output rather than CMS HTML.
2. Confirm that `Rock:Page` is the outermost component.
3. Inspect Lava conditions and the available merge fields used by the page.
4. Check required page parameters and application context values.
5. Inspect page cacheability, maximum age, and maximum shared age.
6. If navigation supplied `rockPageCacheControl`, inspect that setting separately.
7. Validate the rendered result in the applicable Roku shell; a successful Lava render alone does not prove device compatibility. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation)

### Remote focus starts nowhere or moves in the wrong direction

1. Confirm that the page’s outer component is `Rock:Page`.
2. Confirm that `initialFocus` matches the ID of a real focusable child.
3. Check for duplicate or missing IDs.
4. If a FocusGroup is used, confirm `horiz` for left/right movement or `vert` for up/down movement.
5. Confirm that the intended controls are children of the relevant FocusGroup.
6. Stop when the markup is structurally correct but device behavior has not been reproduced; record a shell/device verification gap. [Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page) [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)

### Selecting a button or content item does nothing

1. Confirm that the element is a supported Rock command-bearing control.
2. Inspect the exact `rockCommand` value.
3. Confirm that every required command-specific field is present.
4. If commands are comma-chained, test each command individually before testing the chain.
5. For navigation, verify the destination page identifier and optional parameters.
6. Do not assume a command chain is transactional or that all commands execute after one fails. [Commands](https://community.rockrms.com/developer/roku-docs/commands) [Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button) [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node)

### Back navigation returns to the wrong screen

1. Determine whether the action should push, replace, pop, or clear.
2. Inspect whether `pushPage` was used where `replacePage` was intended.
3. Inspect login or logout stack-clearing settings.
4. Confirm whether a command chain also changed the navigation stack.
5. Retest the exact route from the root page. [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation) [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### Personalized content is stale or appears for the wrong person

1. Inspect the page’s cacheability type.
2. Inspect Max Age and Max Shared Age.
3. Inspect navigation-level `rockPageCacheControl`.
4. Determine whether a personalized request should use personal or private caching rather than public caching.
5. Inspect whether the navigation stack was cleared after login or logout.
6. Confirm the current person and context values used by the page.
7. Do not claim resolution until the behavior is retested across the relevant anonymous and authenticated states. [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation) [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### The QR login flow does not complete

1. Confirm that the application record references a website authentication page.
2. Confirm that the login command points to a Roku login page.
3. Confirm that the page contains `lgnQrPoster` and `lgnCodeLabel`.
4. Inspect timeout, polling, success-page, and timeout-page settings.
5. Confirm that the success and timeout destinations exist.
6. Test the website authentication page independently.
7. Stop when further testing requires changing authentication configuration or using a real account without authorization. [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications) [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal)

### Video or audio does not play

1. Reject YouTube URLs for this command path.
2. Confirm that video is a directly playable MP4 or HLS resource, or that audio is an MP3 resource.
3. Confirm that the Roku device can reach the URL.
4. Inspect the correct command-specific URL field.
5. If the content is live, inspect the live-stream flag.
6. If a Rock Media Element is involved, inspect the media-element association.
7. Treat format, hosting, authorization, and device reachability as separate checks. [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

### Playback resumes but creates a new interaction

1. Confirm that `rockWatchMap` is present.
2. Confirm that the prior `rockInteractionGuid` is also present.
3. If only the watch map was supplied, expect resume behavior with a new interaction and fresh watch map.
4. Confirm that the supplied interaction belongs to the intended playback history.
5. Verify the resulting tracking behavior rather than inferring it from the command markup. [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media)

### A RowList has no rows or items

1. Confirm that the RowList has one root ContentNode assigned to the `content` role.
2. Confirm that each row is represented by a child ContentNode.
3. Confirm that each row contains item ContentNodes.
4. Inspect row titles and item `hdposterurl` values when used.
5. Only after validating the hierarchy, inspect sizes, spacing, visible-row count, and focus-animation settings. [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist)

## Agent Task Recipes

### Recipe: Prepare A Roku Development Readiness Review

**Outcome:** A bounded determination of whether page development can begin.

1. Confirm the target Rock version.
2. Verify that Roku support is applicable to that version.
3. Confirm whether a development application was requested from the Rock Core team.
4. Inspect the application record for API-key presence, authentication page, page-view tracking, and retention duration.
5. Record missing prerequisites without displaying secrets.
6. Stop before requesting credentials, changing configuration, or submitting an external request unless authorized.

**Inspect:**

- Rock version.
- Development-application status.
- Application settings.
- Intended authentication and tracking behavior.

**Do not assume:**

- An upgrade provisions a Roku development application.
- A populated API-key field proves connectivity.
- A selected authentication page proves QR login.

Sources: [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started), [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications).

### Recipe: Author A Focusable Roku Page Skeleton

**Outcome:** A SceneGraph page with a valid page root and deterministic initial focus.

1. Start with `Rock:Page` as the outermost component.
2. Add a focusable Rock control with a unique ID.
3. Set `initialFocus` to that exact ID.
4. Add only the command fields required for the first interaction.
5. Place directional groups inside `Rock:FocusGroup` when automatic left/right or up/down movement is required.
6. Render the Lava and inspect the resulting SceneGraph.
7. Test focus behavior in the applicable Roku shell.

**Inspect:**

- Root component.
- Unique control IDs.
- Initial-focus target.
- FocusGroup orientation.
- Command-specific parameters.

**Stop when:**

- The output renders correctly but no Roku shell or device test is available; record that verification gap.

Sources: [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page), [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group).

### Recipe: Build And Validate A Navigation Action

**Outcome:** A control that produces the intended navigation-stack behavior.

1. Decide whether the destination should be pushed, replace the current page, pop the current page, or clear to root.
2. Add the chosen command to a Rock Button or ContentNode.
3. For push or replace, supply the destination page identifier and any required query parameters.
4. Decide whether a loading screen should be shown.
5. Decide whether navigation should suppress its interaction record.
6. Review navigation-level cache control.
7. Test the Back-button path from the root through the destination.

**Do not assume:**

- `pushPage` and `replacePage` produce the same Back behavior.
- A valid page identifier means the page renders successfully.
- Navigation cache control replaces review of page-level caching.

Sources: [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation), [Commands](https://community.rockrms.com/developer/roku-docs/commands).

### Recipe: Add Campus Or Other Application Context

**Outcome:** A selected value remains available to pages until the application closes or the context is cleared.

1. Choose a stable context key.
2. Add `setContext` to the selection control.
3. Supply the selected value.
4. If navigation should immediately follow, comma-chain `setContext` and `pushPage`.
5. Read the value from the page’s `Context` merge field.
6. Add an explicit `clearContext` path when the selection must be reset.
7. Test application-close behavior separately.

**Do not assume:**

- A context value persists after the application closes.
- Comma-chained commands provide transactional rollback.

Sources: [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility), [Commands](https://community.rockrms.com/developer/roku-docs/commands), [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages).

### Recipe: Configure A Remote Login Journey

**Outcome:** A Roku login page displays a verification code and routes correctly on success or timeout.

1. Confirm that the application has a website authentication page.
2. Create or identify the Roku page that will display login information.
3. Add SceneGraph elements with IDs `lgnQrPoster` and `lgnCodeLabel`.
4. Configure the login control’s login-page, timeout-page, and success-page identifiers.
5. Review the timeout duration and polling interval.
6. Decide whether successful login should clear the navigation stack.
7. Test anonymous start, QR display, successful authentication, timeout, and Back behavior.

**Inspect:**

- Website authentication page.
- Required SceneGraph IDs.
- Success and timeout destinations.
- Stack-clearing behavior.
- Cache behavior for anonymous and personalized pages.

**Stop when:**

- Testing requires an unapproved authentication change or use of another person’s account.

Sources: [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal).

### Recipe: Configure Resumable Media Playback

**Outcome:** A directly playable media resource starts correctly and uses the intended interaction history.

1. Reject YouTube as an input for the Rock Roku playback command.
2. Supply a direct MP4 or HLS URL for video, or MP3 for audio.
3. Add title, subtitle, artwork, and description when required.
4. Associate the Rock Media Element and related entity when applicable.
5. Decide whether resume should be enabled.
6. For resume-only behavior, supply the prior watch map.
7. To append progress to the prior interaction, supply both the watch map and interaction GUID.
8. Mark live video with the documented live-stream field when applicable.
9. Test playback, resume position, and resulting interaction behavior separately.

**Do not assume:**

- A browser-playable URL is reachable or playable on Roku.
- A watch map alone appends to the prior interaction.
- Resume enablement proves tracking.

Sources: [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media).

### Recipe: Review A Roku-Related Lava Endpoint

**Outcome:** A public-safe inventory of the endpoint’s exposure, template, and enabled capabilities.

1. Identify whether the Roku flow actually uses a custom Lava webhook.
2. Record its route and purpose without exposing secrets.
3. Inspect how requests are authenticated or constrained.
4. Review the response template for sensitive data.
5. Inventory enabled Lava commands.
6. Confirm whether the endpoint relies on any organization-specific configuration.
7. Report unprotected or over-capable exposure as a security risk.
8. Stop before enabling commands, changing security, rotating keys, or editing the template unless explicitly authorized.

**Do not assume:**

- The Roku application API key protects the Lava webhook.
- Page security automatically applies to the webhook.
- Another installation shares the inspected configuration.

Sources: [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api), approved claim `claim:410bf6750e90b7193262`.

## Known Gaps And Live Verification

The evidence pack does not establish:

- Whether a particular installation has Roku support installed and configured.
- The exact administrative route used to manage Roku application and page records.
- The installed Roku shell version or its compatibility with every documented field.
- How page-record cache settings and navigation-command cache control interact when both are supplied.
- Failure ordering or rollback behavior for comma-chained Roku commands.
- Device-specific focus behavior beyond the documented FocusGroup rules.
- The complete field contract for media-element identifiers; the supplied media table contains an apparent type or description inconsistency.
- Media host compatibility, authorization behavior, codec requirements, or device reachability beyond the documented MP4, HLS, and MP3 guidance.
- Whether page views or media interactions are actually being written in a target installation.
- Whether a configured website authentication page completes the QR flow.
- Whether a custom Lava webhook is protected in a target installation.
- Packaging, Roku developer-account, signing, sideloading, store-submission, publication, or deployment procedures.
- A full inventory of Rock-provided Roku controls or layout nodes beyond those directly supported by this pack.
- Any physical Roku-device verification.

A bounded live review should therefore confirm:

1. Rock and TV-shell versions.
2. Installed application and page-management surfaces.
3. Application-record configuration.
4. Rendered SceneGraph for representative anonymous and authenticated pages.
5. Initial and directional focus on the target Roku client.
6. Navigation-stack behavior.
7. Authentication success, timeout, logout, and cache transitions.
8. Direct media playback and resume behavior.
9. Page-view and media-interaction creation when tracking is intended.
10. Security controls around every custom Lava endpoint.

Do not include raw configuration values, API keys, organization-specific identifiers, person data, SQL results, or unreviewed instance evidence in a public guide.

## Source Map

- **Overview, version introduction, and development-application requirement:** [Roku Docs](https://community.rockrms.com/developer/roku-docs), [Getting Started](https://community.rockrms.com/developer/roku-docs/getting-started), approved claims `claim:003a9c4612c20c61b9f4`, `claim:ac1a7656566fe397bb04`, and `claim:52b50da71870c1d611da`.
- **Application settings, tracking, API key, and remote authentication page:** [Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications), approved claims `claim:a43c6281e5328e7cac68` and `claim:d67d29d2e4b62513a89b`.
- **Page content, merge fields, outer page control, and caching:** [Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages), [Page Control](https://community.rockrms.com/developer/roku-docs/resources/controls/page), approved claims `claim:563e520ec15928e19628`, `claim:6ff04ce9f309e8163832`, and `claim:f1a329c4eb4099f7fa88`.
- **Command model and comma chaining:** [Commands](https://community.rockrms.com/developer/roku-docs/commands), approved claim `claim:9398f3fb18e8a79c0e4d`.
- **Navigation stack and navigation-level cache control:** [Navigation](https://community.rockrms.com/developer/roku-docs/commands/navigation).
- **Application context:** [Utility](https://community.rockrms.com/developer/roku-docs/commands/utility).
- **Login and logout flow:** [Personal Commands](https://community.rockrms.com/developer/roku-docs/commands/personal).
- **Media formats, playback, resume, and interactions:** [Media Commands](https://community.rockrms.com/developer/roku-docs/commands/media), approved claims `claim:48551097f44d6d7860ae` and `claim:c1b03d50f87ed2b41b40`.
- **SceneGraph and Rock controls:** [Controls](https://community.rockrms.com/developer/roku-docs/resources/controls), [Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button), [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node), approved claim `claim:b850114f9e68b1d54b0c`.
- **Focus behavior:** [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group), approved claim `claim:84305ad4d42aafc22e6d`.
- **Layout selection and RowList:** [Layout Nodes](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes), [RowList](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist), [Tips and Tricks](https://community.rockrms.com/developer/roku-docs/resources/tips-and-tricks), approved claim `claim:49c04d8f25f6c5546bb4`.
- **Platform references and support routes:** [Roku Resources](https://community.rockrms.com/developer/roku-docs/resources/roku-resources), [Useful Links](https://community.rockrms.com/developer/roku-docs/resources/useful-links).
- **Custom Lava API security:** [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api), approved claim `claim:410bf6750e90b7193262`.
