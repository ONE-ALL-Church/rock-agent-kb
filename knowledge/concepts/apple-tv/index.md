---
id: concept-apple-tv
title: Apple TV Apps
generated: true
last_built: 2026-06-18T19:35:10+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - api-integrations
  - lava
  - cms
  - security
  - media
  - tv-apps
---

# Apple TV Apps

Apple TV developer documentation for Rock-powered TVML applications, pages, content, sign-in, media commands, styling, themes, images, templates, testing, and operational guardrails.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.

## How To Think About This Area

- `Apple TV Apps` spans api-integrations, lava, cms, security, media, tv-apps. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_developer, rock_community_site, triumph_resources, rock_lava_docs, rock_api_docs, sparkdevnetwork_rock.
- Related tags found in source records: development, api, lava, obsidian, community, documentation, usage, security.
- Source detail types include: developer_doc, rock_lava_docs, triumph_resources.

## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

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

## Source Coverage

- `rock_api_docs`: 1
- `rock_community_site`: 19
- `rock_developer`: 57
- `rock_lava_docs`: 1
- `rock_model_map`: 12
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Apple TV+ | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-tv) |
| Application Images | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images) |
| Control Styling | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling) |
| 👨‍💻 Developer | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/developer) |
| 💻 Javascript | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| Apple Fitness | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-fitness) |
| Apple Podcasts | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-podcasts) |
| Apple TV Docs | rock_developer | Rock Apple TV is a set top extension of Rock RMS. This site is the documentation for building Apple TVML applications that are linked to Rock. Warning To use Apple TV functionality within Rock, you must be on Rock version 14 or greater. Apple TVML Documentation Apple's TVML documentation site is the primary reference for writing TVML for your application. This site will inform you about the extensions we've written... | [source](https://community.rockrms.com/developer/apple-tv-docs) |
| TV Text Style | rock_developer | TVML offer's several different ways to style text. One thing that should be noted is that Apple TV apps are not HTML. The styling of apps should be more consistent with the Apple Design Language vs creating highly custom branded apps. Below are some of the design patterns for text that will help you know what's available. Text Styles <?xml version="1.0" encoding="UTF-8"?> <document> <descriptiveAlertTemplate>... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.1.8 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.1.8 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.1.8 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.1.8 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.1.8 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.1.8 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.1.8 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.1.8 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.1.8 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection](../../model-map/models/content-collection.md) | CMS | 19.1.8 | 49 | 21 | 34 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection Source](../../model-map/models/content-collection-source.md) | CMS | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable scraped Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Building Your First Apple TV App

Keywords: `creating an app, adding content, tv pages, testing your app, app images, templates`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Application Images | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images) |
| Control Styling | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/control-reference/control-styling) |
| App Icons | rock_developer | The icon for the TV app will be used in two places: inside the app and in the Apple TV App Store. These icons are create using three different layers to create a Parallax effect. More Info Note Each of the icon sizes below will need to be delivered as separate layers with the foreground layers in PNG format and background layer in JPG format. In App Icons The app icon will need to be created in three different... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons) |
| Adding Content | rock_developer | Let's add some content to our application. Note This article is a section in the Building Your First App walkthrough, so if you skipped here, some parts may be in reference to earlier sections of that. This article will still cover the ins and outs of creating a page and adding TVML content to it. Adding Content to the Start Screen Let's add some basic content to our application, in particular, we will use our Start... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content) |
| 📱Building Your First App | rock_developer | Go from hopelessness to a beautiful Apple TV app efficiently and gracefully. Before diving in, let's break down some of the basics. Rock Apple TV provides a way for you to quickly make beautiful TV apps, using an Apple language known as TVML . The Rock Apple TV app builder gives you an easy way to create and test these templates. Let's get started! | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app) |
| TV Pages | rock_developer | Content The content for your page must be valid TVML. The following Lava merge fields are available to you. CurrentPerson - Information on the current person logged into the TV App. Context - Any context objects. Campuses - Listing of all campuses. SiteStyles - This variable allows you to apply the global site styles to your page. CurrentPage - This field allows you to get the default RockPage information about the... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages) |
| Creating An App | rock_developer | Creating a TV application from scratch. Creating an Application In your Rock instance, go ahead and navigate to Admin Tools > CMS Configuration > Apple TV Apps . Once there, create a new site. Let's break this down. Name - the name of your application. This is private to your Rock Instance, and isn't what it has to be named when published to the App Store. Description - An optional description of the application.... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app) |
| Parallax Images | rock_developer | Using Parallax images in your application. What are parallax images? "Layered images are at the heart of the Apple TV user experience. The system combines layered images, transparency, scaling, and motion to produce a sense of realism and vigor that evokes a personal connection as people interact with onscreen content. Parallax Effect Parallax is a subtle visual effect the system uses to convey depth and dynamism... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images) |

### Apple TV Sign-In And Authentication

Keywords: `sign in, remote authentication, personal commands, api key, authentication`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Creating a Sign-in Page | rock_developer | Create a seamless sign-in from a mobile device or computer, and cut out the clunky TV keyboard. Note This article is a section in the Building Your First App walkthrough, so if you skipped here, some parts may be in reference to earlier sections of that. This article will still cover the ins and outs of creating a sign-in page. Setting up the server In your Rock instance, we're going to need to set up a Remote... | [source](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page) |
| Personal Commands | rock_developer | Login This allow for an individual to login to the TV Application. Important Be sure that your application has defined a Login page before using this command. That setting is used to configure the QR code. <menuItem rockCommand="login" rockLoginPageGuid="0C64D387-0A87-ECAA-48A5-B38A62CC704C" rockLoginTimeoutPageGuid="E6F3553B-6270-04AD-4882-F6A99FB3875D"... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands) |

### Apple TV JavaScript Commands

Keywords: `javascript, media commands, personal commands, demo commands, commands`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| 💻 Javascript | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| Media Commands | rock_developer | The commands below are related to the playback of media within the app. Note You cannot play YouTube content in an Apple TV application. ( Why? ) Notes Both of the media commands below share some common functionality as it relates to working with MediaElements . Here are some things you should know. To set the resume location from an existing interaction provide the map from the interaction using the rockWatchMap... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands) |
| Personal Commands | rock_developer | Login This allow for an individual to login to the TV Application. Important Be sure that your application has defined a Login page before using this command. That setting is used to configure the QR code. <menuItem rockCommand="login" rockLoginPageGuid="0C64D387-0A87-ECAA-48A5-B38A62CC704C" rockLoginTimeoutPageGuid="E6F3553B-6270-04AD-4882-F6A99FB3875D"... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands) |
| Demo Commands | rock_developer | There are a set of commands that allow a TV app to change the configuration of the server and application that it points to. For these commands to work the application has to be compiled with support for demo mode. Show Demo This command brings up the demo mode screen. This screen allows you to enter a code to retrieve the demo settings from the Triumph server. <menuItem rockCommand="showDemo"> <title>Demo</title>... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands) |
| Commands | rock_developer | Multiple Commands Typically, commands will be fired one at a time. There may be cases where you'll want to fire two commands at once. For instance you may want to set a context value and also navigate to a different page. Below is a sample <buttonLockup rockCommand="setContext, pushPage" rockPageGuid="0406785c-2c00-4553-931f-cbca5c338796?GroupId=12" rockContextKey="Campus"... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands) |
| Navigation Commands | rock_developer | The commands below are used to show and hides pages on the screen. Push Page Pushes a new page onto the navigation stack. <menuItem rockCommand="pushPage" rockPageGuid="0406785c-2c00-4553-931f-cbca5c338796?GroupId=12"> <title>Product Page</title> </menuItem> Additional options include the following parameters. Parameter Type Description rockPageGuid String The GUID of the page to load with optional query string... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands) |
| Utility Commands | rock_developer | Set Context Sets the application context using the give key/value. <buttonLockup rockCommand="setContext" rockContextKey="Campus" rockContextValue="FC0001DF-4F5E-45F3-B0EA-A780AF75E7E9"> <title>Glendale Campus</title> </buttonLockup> Parameters for this command include: Parameter Type Description rockContextKey string The key for the context. rockContextValue string The value to store for the context. Clear Context... | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/utility-commands) |

### Apple TV Styling

Keywords: `styling, themes, media queries, tv text style, built in images, parallax images`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Apple TV+ | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-tv) |
| Apple Fitness | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-fitness) |
| Apple Podcasts | rock_developer | Apple TV Docs 📱Building Your First App 📱Building Your First App Creating An App Testing Your App Adding Content Tips TV Pages Application Images Application Images App Icons Top Shelf Image Launch Image Parallax Images Context Templates Templates Licensing List Template Alert Template Descriptive Alert Template Div Template Main Template Parade Template Catalog Template Compilation Template Menu Bar Template One Up... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/references/apple-podcasts) |
| TV Text Style | rock_developer | TVML offer's several different ways to style text. One thing that should be noted is that Apple TV apps are not HTML. The styling of apps should be more consistent with the Apple Design Language vs creating highly custom branded apps. Below are some of the design patterns for text that will help you know what's available. Text Styles <?xml version="1.0" encoding="UTF-8"?> <document> <descriptiveAlertTemplate>... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style) |
| Built in Images | rock_developer | tvOS comes with several image resource libraries built into the operating system. These include files for common use cases needed in building TV apps. Links to the various libraries are below in order by usefulness. Button Icons Miscellaneous Icons Movie Rating Icons TV Rating Icons You also have access to any of the SF symbols . Similar to Rock Mobile, Apple TV offers the ability to utilize custom resources. By... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/built-in-images) |
| Themes | rock_developer | There are two major themes in Apple TV Light and Dark . For the most part the individual will select their theme and the app will respond to it. Your styles have can media queries to style the page differently depending on the theme. You can also define a theme for a specific page. Doing so kicks in Apple's built in theme characteristics. Below is the sample markup for this and how the page differs when in dark and... | [source](https://community.rockrms.com/developer/apple-tv-docs/styling/themes) |
| 🎨 Styling | rock_developer | Getting Started Styling Tips TV Text Style Media Queries Themes Built in Images References | [source](https://community.rockrms.com/developer/apple-tv-docs/styling) |


## Lava Capability References

This concept depends on the generated Lava capability layer. Agents should use the stable guidance first, then verify syntax and behavior against the official source and the live Rock instance.

- Reference index: [../lava/lava-reference-index.md](../lava/lava-reference-index.md)
- Safety matrix: [../lava/lava-safety-matrix.md](../lava/lava-safety-matrix.md)
- Agent usage examples: [../lava/lava-agent-usage-examples.md](../lava/lava-agent-usage-examples.md)
- Machine-readable rows: [agent/lava-capabilities.jsonl](../../../agent/lava-capabilities.jsonl)

## Rebuild Dependencies

- Source records: `144`
- Lava capability source records: `53`
- Approved claims: `9`
- Community-reviewed contributions: `0`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
