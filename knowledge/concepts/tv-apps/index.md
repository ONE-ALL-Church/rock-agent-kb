---
id: concept-tv-apps
title: TV Apps
generated: true
last_built: 2026-07-17T05:35:04+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - api-integrations
  - lava
  - cms
  - security
  - media
  - mobile
---

# TV Apps

Apple TV and Roku developer documentation for Rock-powered TV applications, pages, commands, controls, styling, media, authentication, and app operations.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.

## How To Think About This Area

- `TV Apps` spans api-integrations, lava, cms, security, media, mobile. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_developer, rock_lava_docs, triumph_resources, rock_api_docs.
- Related tags found in source records: lava, api, development, obsidian, security, mobile, sql, workflow.
- Source detail types include: developer_doc, rock_lava_docs, triumph_resources.

## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

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
| community-reviewed | operational_guidance | Rock Mobile's move toward .NET MAUI should be treated as an evolution from Xamarin Forms rather than an unrelated app platform. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |
| community-reviewed | source_summary | This RockCast episode adds public-safe context for the Rock Mobile transition from Xamarin Forms toward .NET MAUI. It describes MAUI as a close successor with compatibility support, newer styling and animation options, performance improvements, and a release path that lets existing apps test compatibility before fully moving new content blocks to MAUI-native behavior. _(live verification recommended)_ | [source](https://shows.acast.com/rock-cast/episodes/episode-143-special-edition-braden-cohen) |

## Source Coverage

- `rock_api_docs`: 1
- `rock_developer`: 77
- `rock_lava_docs`: 1
- `rock_model_map`: 12
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| 👋 Roku Docs | rock_developer | ## 👋Welcome *Extend your digital ministry to Roku TV.* When we introduced support for Apple TV applications in 2022, one question kept coming up: "What about Roku?" With Roku’s vast user base, we knew we had to meet this need. Staying true to our mission of empowering organizations to deliver content seamlessly across platforms, we’ve developed comprehensive Roku integration for Rock. Designed to expand the reach of... | [source](https://community.rockrms.com/developer/roku-docs) |
| Focus Group | rock_developer | Manage vertical or horizontal focus in your Roku application. *Extends* [*LayoutGroup*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/layoutgroup.md) ## Description Unfortunately, as of 2024, focus management is not built into Roku applications (like we are used to with Apple TV). This control handles three simple things automatically for you: 1. Display views vertically/horizontally. 2.... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| Roku Resources | rock_developer | * [SceneGraph Reference](https://developer.roku.com/en-gb/docs/references/references-overview.md) - Roku documentation for all the built-in SceneGraph components. * [Roku Samples](https://github.com/rokudev/samples) - A repository of Roku sample applications/SceneGraph. | [source](https://community.rockrms.com/developer/roku-docs/resources/roku-resources) |
| Pages | rock_developer | *Display custom, Lava-driven content as a subset of your application.* ## Page Settings When creating or editing a Roku page, you have access to the following configuration options. Page configuration options ### Show in Menu Whether or not this page should be used in navigation menus. Note, this is not actually utilized anywhere in the Roku shell, but instead empowers you to create navigation menus in Lava. ###... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| Media | rock_developer | The commands below are related to the playback of media within the app. Note You cannot play YouTube content in a Roku TV application. ## Notes Both of the media commands below share some common functionality as it relates to working with `MediaElements`. Here are some things you should know. To set the resume location from an existing interaction provide the map from the interaction using the `rockWatchMap`... | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| 📚 Resources | rock_developer | [Controls](/documentation/roku-docs/resources/controls) [Layout Nodes](/documentation/roku-docs/resources/layout-nodes) [Roku Resources](/documentation/roku-docs/resources/roku-resources) [Tips and Tricks](/documentation/roku-docs/resources/tips-and-tricks) [Useful Links](/documentation/roku-docs/resources/useful-links) | [source](https://community.rockrms.com/developer/roku-docs/resources) |
| Apple TV Docs | rock_developer | Rock Apple TV is a set top extension of Rock RMS. This site is the documentation for building Apple TVML applications that are linked to Rock. Warning To use Apple TV functionality within Rock, you must be on Rock version 14 or greater. ### Apple TVML Documentation [Apple's TVML documentation site](https://developer.apple.com/documentation/tvml) is the primary reference for writing TVML for your application. This... | [source](https://community.rockrms.com/developer/apple-tv-docs) |
| Controls | rock_developer | Roku applications are built with an XML language named [SceneGraph](https://developer.roku.com/docs/developer-program/core-concepts/scenegraph-xml/overview.md). Most of your application will be comprised with the built-in SceneGraph components. This section covers the custom components provided with Roku. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| 💻 Getting Started | rock_developer | Get your first application up and running. Developing a Roku application in Rock is similar to building a website. You create an application (site) with multiple pages, each featuring dynamic content powered by Lava. These pages can be linked together to create a seamless, interconnected experience. The main difference is that, unlike websites where you write in HTML, Roku uses a more technical XML-based language... | [source](https://community.rockrms.com/developer/roku-docs/getting-started) |
| Media Commands | rock_developer | The commands below are related to the playback of media within the app. Note You cannot play YouTube content in an Apple TV application. ([Why?](https://medium.com/bpxl-craft/apple-tv-a-world-without-webkit-5c428a64a6dd)) ## Notes Both of the media commands below share some common functionality as it relates to working with `MediaElements`. Here are some things you should know. 1. To set the resume location from an... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) |
| Applications | rock_developer | *Learn how to create a Roku application in Rock to manage your TV content.* ## Application Settings When creating or editing a Roku application, you have access to the following configuration options. ### Enable Page Views Whether (or not) page interactions should be written to track the usage of your application. ### Page View Retention Duration The duration (in days) to retain the page interactions that are... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| 📱Building Your First App | rock_developer | *Go from hopelessness to a beautiful Apple TV app efficiently and gracefully.* Before diving in, let's break down some of the basics. Rock Apple TV provides a way for you to quickly make beautiful TV apps, using an Apple language known as [TVML](https://developer.apple.com/documentation/tvml). The Rock Apple TV app builder gives you an easy way to create and test these templates. Let's get started! | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Lava Application](../../model-map/models/lava-application.md) | CMS | 19.2.0 | 44 | 16 | 29 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Lava Endpoint](../../model-map/models/lava-endpoint.md) | CMS | 19.2.0 | 52 | 23 | 36 | 13 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Lava Shortcode](../../model-map/models/lava-shortcode.md) | CMS | 19.2.0 | 48 | 20 | 31 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Media Account](../../model-map/models/media-account.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Media Element](../../model-map/models/media-element.md) | CMS | 19.2.0 | 54 | 24 | 37 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Media Folder](../../model-map/models/media-folder.md) | CMS | 19.2.0 | 53 | 21 | 38 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Remote Authentication Session](../../model-map/models/remote-authentication-session.md) | Core | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.2.0 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.2.0 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Subguides

### Apple TV

Keywords: `apple tv, tvml, tv-template, theme, media queries, commands, controls, sign in page`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Apple TV Docs | rock_developer | Rock Apple TV is a set top extension of Rock RMS. This site is the documentation for building Apple TVML applications that are linked to Rock. Warning To use Apple TV functionality within Rock, you must be on Rock version 14 or greater. ### Apple TVML Documentation [Apple's TVML documentation site](https://developer.apple.com/documentation/tvml) is the primary reference for writing TVML for your application. This... | [source](https://community.rockrms.com/developer/apple-tv-docs) |
| Media Commands | rock_developer | The commands below are related to the playback of media within the app. Note You cannot play YouTube content in an Apple TV application. ([Why?](https://medium.com/bpxl-craft/apple-tv-a-world-without-webkit-5c428a64a6dd)) ## Notes Both of the media commands below share some common functionality as it relates to working with `MediaElements`. Here are some things you should know. 1. To set the resume location from an... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) |
| 📱Building Your First App | rock_developer | *Go from hopelessness to a beautiful Apple TV app efficiently and gracefully.* Before diving in, let's break down some of the basics. Rock Apple TV provides a way for you to quickly make beautiful TV apps, using an Apple language known as [TVML](https://developer.apple.com/documentation/tvml). The Rock Apple TV app builder gives you an easy way to create and test these templates. Let's get started! | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app) |
| TV Text Style | rock_developer | TVML offer's several different ways to style text. One thing that should be noted is that Apple TV apps are not HTML. The styling of apps should be more consistent with the [Apple Design Language](https://developer.apple.com/design/human-interface-guidelines/tvos/overview/themes/) vs creating highly custom branded apps. Below are some of the design patterns for text that will help you know what's available. ## Text... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) |
| Themes | rock_developer | There are two major themes in Apple TV *Light* and *Dark*. For the most part the individual will select their theme and the app will respond to it. Your styles have can [media queries](/documentation/apple-tv-docs/styling/media-queries) to style the page differently depending on the theme. You can also define a theme for a specific page. Doing so kicks in Apple's built in theme characteristics. Below is the sample... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) |
| Adding Content | rock_developer | Let's add some content to our application. Note This article is a section in the [Building Your First App](https://appletv.rockrms.com/building-your-first-app) walkthrough, so if you skipped here, some parts may be in reference to earlier sections of that. This article will still cover the ins and outs of creating a page and adding TVML content to it. ## Adding Content to the Start Screen Let's add some basic... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content) |
| Creating An App | rock_developer | Creating a TV application from scratch. ### Creating an Application In your Rock instance, go ahead and navigate to `Admin Tools > CMS Configuration > Apple TV Apps`. Once there, create a new site. Let's break this down. **Name** - the name of your application. This is private to your Rock Instance, and isn't what it has to be named when published to the App Store. **Description** - An optional description of the... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) |
| Built in Images | rock_developer | tvOS comes with several image resource libraries built into the operating system. These include files for common use cases needed in building TV apps. Links to the various libraries are below in order by usefulness. * Button Icons * Miscellaneous Icons * Movie Rating Icons * TV Rating Icons You also have access to any of the [SF... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images) |
| Apple TV+ | rock_developer | * [Apple TV Docs](/documentation/apple-tv-docs) * 📱Building Your First App + [📱Building Your First App](/documentation/apple-tv-docs/building-your-first-app) + [Creating An App](/documentation/apple-tv-docs/building-your-first-app/creating-an-app) + [Testing Your App](/documentation/apple-tv-docs/building-your-first-app/testing-your-app) + [Adding... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-tv) |
| Media Queries | rock_developer | ## Theme You can style dependent on the current theme using the snippet below. ``` <style> @media tv-template and (tv-theme:light) { .foo { color: rgba(0,0,0); } } @media tv-template and (tv-theme:dark) { .foo { color: rgba(255,255,255); } } </style> ``` | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries) |

### Roku

Keywords: `roku, brightscript, scenegraph, rowlist, focus group, roku applications, roku pages`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| 👋 Roku Docs | rock_developer | ## 👋Welcome *Extend your digital ministry to Roku TV.* When we introduced support for Apple TV applications in 2022, one question kept coming up: "What about Roku?" With Roku’s vast user base, we knew we had to meet this need. Staying true to our mission of empowering organizations to deliver content seamlessly across platforms, we’ve developed comprehensive Roku integration for Rock. Designed to expand the reach of... | [source](https://community.rockrms.com/developer/roku-docs) |
| Focus Group | rock_developer | Manage vertical or horizontal focus in your Roku application. *Extends* [*LayoutGroup*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/layoutgroup.md) ## Description Unfortunately, as of 2024, focus management is not built into Roku applications (like we are used to with Apple TV). This control handles three simple things automatically for you: 1. Display views vertically/horizontally. 2.... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| Roku Resources | rock_developer | * [SceneGraph Reference](https://developer.roku.com/en-gb/docs/references/references-overview.md) - Roku documentation for all the built-in SceneGraph components. * [Roku Samples](https://github.com/rokudev/samples) - A repository of Roku sample applications/SceneGraph. | [source](https://community.rockrms.com/developer/roku-docs/resources/roku-resources) |
| Pages | rock_developer | *Display custom, Lava-driven content as a subset of your application.* ## Page Settings When creating or editing a Roku page, you have access to the following configuration options. Page configuration options ### Show in Menu Whether or not this page should be used in navigation menus. Note, this is not actually utilized anywhere in the Roku shell, but instead empowers you to create navigation menus in Lava. ###... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| Media | rock_developer | The commands below are related to the playback of media within the app. Note You cannot play YouTube content in a Roku TV application. ## Notes Both of the media commands below share some common functionality as it relates to working with `MediaElements`. Here are some things you should know. To set the resume location from an existing interaction provide the map from the interaction using the `rockWatchMap`... | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| 📚 Resources | rock_developer | [Controls](/documentation/roku-docs/resources/controls) [Layout Nodes](/documentation/roku-docs/resources/layout-nodes) [Roku Resources](/documentation/roku-docs/resources/roku-resources) [Tips and Tricks](/documentation/roku-docs/resources/tips-and-tricks) [Useful Links](/documentation/roku-docs/resources/useful-links) | [source](https://community.rockrms.com/developer/roku-docs/resources) |
| Controls | rock_developer | Roku applications are built with an XML language named [SceneGraph](https://developer.roku.com/docs/developer-program/core-concepts/scenegraph-xml/overview.md). Most of your application will be comprised with the built-in SceneGraph components. This section covers the custom components provided with Roku. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| 💻 Getting Started | rock_developer | Get your first application up and running. Developing a Roku application in Rock is similar to building a website. You create an application (site) with multiple pages, each featuring dynamic content powered by Lava. These pages can be linked together to create a seamless, interconnected experience. The main difference is that, unlike websites where you write in HTML, Roku uses a more technical XML-based language... | [source](https://community.rockrms.com/developer/roku-docs/getting-started) |
| Applications | rock_developer | *Learn how to create a Roku application in Rock to manage your TV content.* ## Application Settings When creating or editing a Roku application, you have access to the following configuration options. ### Enable Page Views Whether (or not) page interactions should be written to track the usage of your application. ### Page View Retention Duration The duration (in days) to retain the page interactions that are... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| ⚡ Commands | rock_developer | ## Overview Executing commands in your Roku TV application. You can execute commands by specifying a `rockCommand` and the necessary parameters to an applicable control (such as the Rock [ContentNode](/documentation/roku-docs/resources/controls/content-node) and [Button](/documentation/roku-docs/resources/controls/button)). ### Multiple Commands Typically, commands will be fired one at a time. There may be cases... | [source](https://community.rockrms.com/developer/roku-docs/commands) |

### Security And Authentication

Keywords: `security, sign in, remote auth, api key, application, page security`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Applications | rock_developer | *Learn how to create a Roku application in Rock to manage your TV content.* ## Application Settings When creating or editing a Roku application, you have access to the following configuration options. ### Enable Page Views Whether (or not) page interactions should be written to track the usage of your application. ### Page View Retention Duration The duration (in days) to retain the page interactions that are... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| Creating a Sign-in Page | rock_developer | Create a seamless sign-in from a mobile device or computer, and cut out the clunky TV keyboard. Note This article is a section in the [Building Your First App](/documentation/apple-tv-docs/building-your-first-app) walkthrough, so if you skipped here, some parts may be in reference to earlier sections of that. This article will still cover the ins and outs of creating a sign-in page. ### Setting up the server In your... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) |

### Styling And Controls

Keywords: `styling, theme, media queries, controls, focus group, button, layout nodes, rowlist`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Focus Group | rock_developer | Manage vertical or horizontal focus in your Roku application. *Extends* [*LayoutGroup*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/layoutgroup.md) ## Description Unfortunately, as of 2024, focus management is not built into Roku applications (like we are used to with Apple TV). This control handles three simple things automatically for you: 1. Display views vertically/horizontally. 2.... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| Controls | rock_developer | Roku applications are built with an XML language named [SceneGraph](https://developer.roku.com/docs/developer-program/core-concepts/scenegraph-xml/overview.md). Most of your application will be comprised with the built-in SceneGraph components. This section covers the custom components provided with Roku. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| TV Text Style | rock_developer | TVML offer's several different ways to style text. One thing that should be noted is that Apple TV apps are not HTML. The styling of apps should be more consistent with the [Apple Design Language](https://developer.apple.com/design/human-interface-guidelines/tvos/overview/themes/) vs creating highly custom branded apps. Below are some of the design patterns for text that will help you know what's available. ## Text... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) |
| Themes | rock_developer | There are two major themes in Apple TV *Light* and *Dark*. For the most part the individual will select their theme and the app will respond to it. Your styles have can [media queries](/documentation/apple-tv-docs/styling/media-queries) to style the page differently depending on the theme. You can also define a theme for a specific page. Doing so kicks in Apple's built in theme characteristics. Below is the sample... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) |
| Button | rock_developer | *Extends* [*Button*](https://developer.roku.com/docs/references/scenegraph/widget-nodes/button.md) ## Description In order to properly handle commands, we extended the Roku Button with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:Button rockCommand="pushPage" rockPageGuid="4443b83e-86c9-4e35-9637-13b8991856ed" /> ``` | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/button) |
| Content Node | rock_developer | *Extends* [*Content Node*](https://developer.roku.com/docs/references/scenegraph/control-nodes/contentnode.md) ## Description In order to properly handle commands, we extended the Roku Content Node with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:ContentNode rockCommand="pushPage"... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node) |
| Built in Images | rock_developer | tvOS comes with several image resource libraries built into the operating system. These include files for common use cases needed in building TV apps. Links to the various libraries are below in order by usefulness. * Button Icons * Miscellaneous Icons * Movie Rating Icons * TV Rating Icons You also have access to any of the [SF... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images) |
| Layout Nodes | rock_developer | Although Roku has many different layouts, very few have default item templates. Be cautious when picking your SceneGraph elements as we try to avoid custom BrightScript components. | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes) |
| Page | rock_developer | The standard control that is used for your page content. *Extends* [*Group*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/group.md) ## Description This is a group of views that represents an entire page of content. ## Field \| Field \| Type \| Description \| \| --- \| --- \| --- \| \| initialFocus \| string \| The ID of the item you want to be focused when the page comes into view. \| ## Examples ```... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/page) |
| Apple TV+ | rock_developer | * [Apple TV Docs](/documentation/apple-tv-docs) * 📱Building Your First App + [📱Building Your First App](/documentation/apple-tv-docs/building-your-first-app) + [Creating An App](/documentation/apple-tv-docs/building-your-first-app/creating-an-app) + [Testing Your App](/documentation/apple-tv-docs/building-your-first-app/testing-your-app) + [Adding... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-tv) |


## Lava Capability References

This concept depends on the generated Lava capability layer. Agents should use the stable guidance first, then verify syntax and behavior against the official source and the live Rock instance.

- Reference index: [../lava/lava-reference-index.md](../lava/lava-reference-index.md)
- Safety matrix: [../lava/lava-safety-matrix.md](../lava/lava-safety-matrix.md)
- Agent usage examples: [../lava/lava-agent-usage-examples.md](../lava/lava-agent-usage-examples.md)
- Machine-readable rows: [agent/lava-capabilities.jsonl](../../../agent/lava-capabilities.jsonl)

## Rebuild Dependencies

- Source records: `144`
- Lava capability source records: `53`
- Approved claims: `14`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
