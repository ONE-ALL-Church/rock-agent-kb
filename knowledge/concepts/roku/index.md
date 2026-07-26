---
id: concept-roku
title: Roku Apps
generated: true
last_built: 2026-07-26T00:28:45+00:00
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

# Roku Apps

Roku developer documentation for Rock-powered SceneGraph applications, pages, commands, controls, focus handling, media playback, layout nodes, resources, and operational guardrails.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.

## How To Think About This Area

- `Roku Apps` spans api-integrations, lava, cms, security, media, tv-apps. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_developer, rock_lava_docs, triumph_resources, rock_api_docs, sparkdevnetwork_rock.
- Related tags found in source records: development, lava, cms, workflow, api, obsidian, security, sql.
- Source detail types include: developer_doc, rock_lava_docs.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Dashboard Design Part 1 Transcript Insight | data and reporting | 00:12 | Start dashboard work by naming the decision or story the dashboard should support, then choose charts that make that comparison legible instead of simply placing available Rock data on screen. | [source](https://www.triumph.tech/resources/dashboard-design-part-1) |
| Dashboard Design Part 1 Transcript Insight | giving and reporting | 00:31 | For giving dashboards that compare connection status, bar-style comparisons are usually easier to read than pie or donut charts because small categories and relative sizes stay visible. | [source](https://www.triumph.tech/resources/dashboard-design-part-1) |
| Dashboard Design Part 1 Transcript Insight | implementation workflow | 09:47 | Prototype dashboards in a fast visual tool before writing Lava or blocks so the team can validate the story, chart type, and audience insight before implementation friction narrows the design. | [source](https://www.triumph.tech/resources/dashboard-design-part-1) |
| SQL Window Functions Transcript Insight | data and reporting | 01:18 | Window functions are useful in Rock SQL reporting when each detail row needs aggregate context, such as total transaction amount, detail count, or percent-of-gift alongside the original transaction-detail row. | [source](https://www.triumph.tech/resources/sql-window-functions) |
| SQL Window Functions Transcript Insight | SQL patterns | 03:30 | Use OVER with PARTITION BY as a row-preserving alternative to GROUP BY when a report needs grouped calculations without collapsing the result set. | [source](https://www.triumph.tech/resources/sql-window-functions) |
| SQL Window Functions Transcript Insight | SQL patterns | 07:40 | Ranking window functions such as row number, rank, dense rank, and n-tile can add ordering, per-person sequence, or bucket analysis to Rock reports without procedural post-processing. | [source](https://www.triumph.tech/resources/sql-window-functions) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | AI and automation | 00:00 | AI should be treated as an assistive ministry operations layer: useful for drafting, summarizing, classifying, and routing work, but still requiring human judgment and local policy before action. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | staff training | 03:12 | Public guidance should frame AI adoption around responsible enablement, including data boundaries, staff training, review expectations, and clear ownership of final decisions. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | data and reporting | 03:36 | For Rock-adjacent automation, agents should verify source data and system state rather than treating generated AI output as an authoritative record. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Grouping Sets Transcript Insight | data and reporting | 00:00 | Grouping sets can simplify Rock SQL reports that need multiple aggregation levels, such as detail totals plus higher-level rollups, without maintaining separate queries for each level. | [source](https://www.triumph.tech/resources/grouping-sets) |
| Grouping Sets Transcript Insight | report design | 00:45 | Use grouping-set style reporting when staff need both granular rows and summary rows in one report surface, but label rollup rows clearly so agents and users do not confuse them with ordinary records. | [source](https://www.triumph.tech/resources/grouping-sets) |
| Grouping Sets Transcript Insight | implementation workflow | 01:33 | Because grouping sets are a SQL-level technique, public KB guidance should route users to validation against the local schema and SQL dialect before copying a community pattern into production. | [source](https://www.triumph.tech/resources/grouping-sets) |
| Pivot Pattern Transcript Insight | data and reporting | 00:00 | Pivot-style SQL patterns help Rock reports turn repeated row values into comparison columns when staff need a cross-tab view rather than a long list of records. | [source](https://www.triumph.tech/resources/pivot-patterns) |
| Pivot Pattern Transcript Insight | report design | 03:32 | Before using a pivot pattern, confirm the report audience needs side-by-side category comparison; if the categories are unstable or too numerous, a normal grouped result may be easier to maintain. | [source](https://www.triumph.tech/resources/pivot-patterns) |
| Pivot Pattern Transcript Insight | implementation workflow | 03:32 | Treat community pivot examples as patterns to adapt, not final production SQL, because Rock field names, entity relationships, and reporting requirements vary by instance. | [source](https://www.triumph.tech/resources/pivot-patterns) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

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
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| official | risk | Rock's Roku TV application cannot play YouTube content; its video command expects a directly playable MP4 or HLS resource instead. | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| official | source_summary | Rock Roku documentation describes Roku support as a way to extend Rock-powered digital ministry to Roku TV through Rock-managed Roku integration. | [source](https://community.rockrms.com/developer/roku-docs) |
| release-note-confirmed | release_caveat | Triumph's GitHub Spotlight for the v17.0.29 pre-alpha notes that the Roku TV app feature was added for Rock v16.7, making Roku coverage version-sensitive. | [source](https://www.triumph.tech/resources/github-spotlight-1042024) |

## Source Coverage

- `rock_api_docs`: 1
- `rock_developer`: 20
- `rock_lava_docs`: 53
- `rock_model_map`: 12
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 5

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Focus Group | rock_developer | Manage vertical or horizontal focus in your Roku application. *Extends* [*LayoutGroup*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/layoutgroup.md) ## Description Unfortunately, as of 2024, focus management is not built into Roku applications (like we are used to with Apple TV). This control handles three simple things automatically for you: 1. Display views vertically/horizontally. 2.... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| 👋 Roku Docs | rock_developer | ## 👋Welcome *Extend your digital ministry to Roku TV.* When we introduced support for Apple TV applications in 2022, one question kept coming up: "What about Roku?" With Roku’s vast user base, we knew we had to meet this need. Staying true to our mission of empowering organizations to deliver content seamlessly across platforms, we’ve developed comprehensive Roku integration for Rock. Designed to expand the reach of... | [source](https://community.rockrms.com/developer/roku-docs) |
| Controls | rock_developer | Roku applications are built with an XML language named [SceneGraph](https://developer.roku.com/docs/developer-program/core-concepts/scenegraph-xml/overview.md). Most of your application will be comprised with the built-in SceneGraph components. This section covers the custom components provided with Roku. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| Roku Resources | rock_developer | * [SceneGraph Reference](https://developer.roku.com/en-gb/docs/references/references-overview.md) - Roku documentation for all the built-in SceneGraph components. * [Roku Samples](https://github.com/rokudev/samples) - A repository of Roku sample applications/SceneGraph. | [source](https://community.rockrms.com/developer/roku-docs/resources/roku-resources) |
| 📚 Resources | rock_developer | [Controls](/documentation/roku-docs/resources/controls) [Layout Nodes](/documentation/roku-docs/resources/layout-nodes) [Roku Resources](/documentation/roku-docs/resources/roku-resources) [Tips and Tricks](/documentation/roku-docs/resources/tips-and-tricks) [Useful Links](/documentation/roku-docs/resources/useful-links) | [source](https://community.rockrms.com/developer/roku-docs/resources) |
| 💻 Getting Started | rock_developer | Get your first application up and running. Developing a Roku application in Rock is similar to building a website. You create an application (site) with multiple pages, each featuring dynamic content powered by Lava. These pages can be linked together to create a seamless, interconnected experience. The main difference is that, unlike websites where you write in HTML, Roku uses a more technical XML-based language... | [source](https://community.rockrms.com/developer/roku-docs/getting-started) |
| RowList | rock_developer | The RowList Node component within SceneGraph is used to create a horizontal list of items. This component is ideal for displaying a series of elements that can be scrolled horizontally. This layout accepts an unlimited amount of vertical and horizontal scrollability. \| Parameter \| Type \| Description \| \| --- \| --- \| --- \| \| itemSize \| vector2d \| The size of the RowList element. \| \| numRows \| int \| Specifies the... | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist) |
| Pages | rock_developer | *Display custom, Lava-driven content as a subset of your application.* ## Page Settings When creating or editing a Roku page, you have access to the following configuration options. Page configuration options ### Show in Menu Whether or not this page should be used in navigation menus. Note, this is not actually utilized anywhere in the Roku shell, but instead empowers you to create navigation menus in Lava. ###... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| Applications | rock_developer | *Learn how to create a Roku application in Rock to manage your TV content.* ## Application Settings When creating or editing a Roku application, you have access to the following configuration options. ### Enable Page Views Whether (or not) page interactions should be written to track the usage of your application. ### Page View Retention Duration The duration (in days) to retain the page interactions that are... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| Layout Nodes | rock_developer | Although Roku has many different layouts, very few have default item templates. Be cautious when picking your SceneGraph elements as we try to avoid custom BrightScript components. | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes) |
| Button | rock_developer | *Extends* [*Button*](https://developer.roku.com/docs/references/scenegraph/widget-nodes/button.md) ## Description In order to properly handle commands, we extended the Roku Button with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:Button rockCommand="pushPage" rockPageGuid="4443b83e-86c9-4e35-9637-13b8991856ed" /> ``` | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/button) |
| Content Node | rock_developer | *Extends* [*Content Node*](https://developer.roku.com/docs/references/scenegraph/control-nodes/contentnode.md) ## Description In order to properly handle commands, we extended the Roku Content Node with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:ContentNode rockCommand="pushPage"... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.2.0 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.2.0 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.2.0 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.2.0 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.2.0 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.2.0 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection](../../model-map/models/content-collection.md) | CMS | 19.2.0 | 49 | 21 | 34 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection Source](../../model-map/models/content-collection-source.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Roku Getting Started

Keywords: `getting started, applications, pages, scenegraph, lava`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| 💻 Getting Started | rock_developer | Get your first application up and running. Developing a Roku application in Rock is similar to building a website. You create an application (site) with multiple pages, each featuring dynamic content powered by Lava. These pages can be linked together to create a seamless, interconnected experience. The main difference is that, unlike websites where you write in HTML, Roku uses a more technical XML-based language... | [source](https://community.rockrms.com/developer/roku-docs/getting-started) |
| Pages | rock_developer | *Display custom, Lava-driven content as a subset of your application.* ## Page Settings When creating or editing a Roku page, you have access to the following configuration options. Page configuration options ### Show in Menu Whether or not this page should be used in navigation menus. Note, this is not actually utilized anywhere in the Roku shell, but instead empowers you to create navigation menus in Lava. ###... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| Applications | rock_developer | *Learn how to create a Roku application in Rock to manage your TV content.* ## Application Settings When creating or editing a Roku application, you have access to the following configuration options. ### Enable Page Views Whether (or not) page interactions should be written to track the usage of your application. ### Page View Retention Duration The duration (in days) to retain the page interactions that are... | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |

### Roku Commands

Keywords: `commands, navigation, media, utility, personal`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Dashboard Design Part 1 Transcript Insight | data and reporting | 00:12 | Start dashboard work by naming the decision or story the dashboard should support, then choose charts that make that comparison legible instead of simply placing available Rock data on screen. | [source](https://www.triumph.tech/resources/dashboard-design-part-1) |
| Dashboard Design Part 1 Transcript Insight | giving and reporting | 00:31 | For giving dashboards that compare connection status, bar-style comparisons are usually easier to read than pie or donut charts because small categories and relative sizes stay visible. | [source](https://www.triumph.tech/resources/dashboard-design-part-1) |
| Dashboard Design Part 1 Transcript Insight | implementation workflow | 09:47 | Prototype dashboards in a fast visual tool before writing Lava or blocks so the team can validate the story, chart type, and audience insight before implementation friction narrows the design. | [source](https://www.triumph.tech/resources/dashboard-design-part-1) |
| SQL Window Functions Transcript Insight | data and reporting | 01:18 | Window functions are useful in Rock SQL reporting when each detail row needs aggregate context, such as total transaction amount, detail count, or percent-of-gift alongside the original transaction-detail row. | [source](https://www.triumph.tech/resources/sql-window-functions) |
| SQL Window Functions Transcript Insight | SQL patterns | 03:30 | Use OVER with PARTITION BY as a row-preserving alternative to GROUP BY when a report needs grouped calculations without collapsing the result set. | [source](https://www.triumph.tech/resources/sql-window-functions) |
| SQL Window Functions Transcript Insight | SQL patterns | 07:40 | Ranking window functions such as row number, rank, dense rank, and n-tile can add ordering, per-person sequence, or bucket analysis to Rock reports without procedural post-processing. | [source](https://www.triumph.tech/resources/sql-window-functions) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | AI and automation | 00:00 | AI should be treated as an assistive ministry operations layer: useful for drafting, summarizing, classifying, and routing work, but still requiring human judgment and local policy before action. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | staff training | 03:12 | Public guidance should frame AI adoption around responsible enablement, including data boundaries, staff training, review expectations, and clear ownership of final decisions. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Video: AI's Role in Digital Ministry with Jon Edmiston Transcript Insight | data and reporting | 03:36 | For Rock-adjacent automation, agents should verify source data and system state rather than treating generated AI output as an authoritative record. | [source](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Grouping Sets Transcript Insight | data and reporting | 00:00 | Grouping sets can simplify Rock SQL reports that need multiple aggregation levels, such as detail totals plus higher-level rollups, without maintaining separate queries for each level. | [source](https://www.triumph.tech/resources/grouping-sets) |
| Grouping Sets Transcript Insight | report design | 00:45 | Use grouping-set style reporting when staff need both granular rows and summary rows in one report surface, but label rollup rows clearly so agents and users do not confuse them with ordinary records. | [source](https://www.triumph.tech/resources/grouping-sets) |
| Grouping Sets Transcript Insight | implementation workflow | 01:33 | Because grouping sets are a SQL-level technique, public KB guidance should route users to validation against the local schema and SQL dialect before copying a community pattern into production. | [source](https://www.triumph.tech/resources/grouping-sets) |
| Pivot Pattern Transcript Insight | data and reporting | 00:00 | Pivot-style SQL patterns help Rock reports turn repeated row values into comparison columns when staff need a cross-tab view rather than a long list of records. | [source](https://www.triumph.tech/resources/pivot-patterns) |
| Pivot Pattern Transcript Insight | report design | 03:32 | Before using a pivot pattern, confirm the report audience needs side-by-side category comparison; if the categories are unstable or too numerous, a normal grouped result may be easier to maintain. | [source](https://www.triumph.tech/resources/pivot-patterns) |
| Pivot Pattern Transcript Insight | implementation workflow | 03:32 | Treat community pivot examples as patterns to adapt, not final production SQL, because Rock field names, entity relationships, and reporting requirements vary by instance. | [source](https://www.triumph.tech/resources/pivot-patterns) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Media | rock_developer | The commands below are related to the playback of media within the app. Note You cannot play YouTube content in a Roku TV application. ## Notes Both of the media commands below share some common functionality as it relates to working with `MediaElements`. Here are some things you should know. To set the resume location from an existing interaction provide the map from the interaction using the `rockWatchMap`... | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| ⚡ Commands | rock_developer | ## Overview Executing commands in your Roku TV application. You can execute commands by specifying a `rockCommand` and the necessary parameters to an applicable control (such as the Rock [ContentNode](/documentation/roku-docs/resources/controls/content-node) and [Button](/documentation/roku-docs/resources/controls/button)). ### Multiple Commands Typically, commands will be fired one at a time. There may be cases... | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| Navigation | rock_developer | Used to navigate between different sections of content. ## Push Page Pushes a page on to the navigation stack. ``` <Rock:ContentNode title = "Push Page" rockCommand="pushPage" rockPageGuid="4c294b37-fcc1-4432-87ff-3ce73f14a482" /> ``` \| Parameter \| Type \| Description \| \| --- \| --- \| --- \| \| rockPageGuid \| String \| The GUID of the page to load with optional query string parameters. \| \| rockPageCacheControl \| String \|... | [source](https://community.rockrms.com/developer/roku-docs/commands/navigation) |
| Personal | rock_developer | Commands that relate to the Current Person. ## Login Allows for an individual to login to the TV Application. Important Be sure that your application has defined a Login page before using this command. That setting is used to configure the QR code. ``` <Rock:Button rockCommand="login" rockLoginPageGuid="0C64D387-0A87-ECAA-48A5-B38A62CC704C" rockLoginTimeoutPageGuid="E6F3553B-6270-04AD-4882-F6A99FB3875D"... | [source](https://community.rockrms.com/developer/roku-docs/commands/personal) |
| Utility | rock_developer | Useful commands to use around the application. ## Set Context Sets a context for the lifetime of the application (until closed). ``` <Rock:ContentNode title = "Set Context" rockCommand="setContext" rockContextKey="Campus" rockContextValue="4c294b37-fcc1-4432-87ff-3ce73f14a482" /> ``` ## Clear Context Clears the specified context provided by the key. ``` <Rock:ContentNode title = "Clear Context"... | [source](https://community.rockrms.com/developer/roku-docs/commands/utility) |

### Roku Controls

Keywords: `controls, button, content node, focus group, page, focus`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Focus Group | rock_developer | Manage vertical or horizontal focus in your Roku application. *Extends* [*LayoutGroup*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/layoutgroup.md) ## Description Unfortunately, as of 2024, focus management is not built into Roku applications (like we are used to with Apple TV). This control handles three simple things automatically for you: 1. Display views vertically/horizontally. 2.... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| Controls | rock_developer | Roku applications are built with an XML language named [SceneGraph](https://developer.roku.com/docs/developer-program/core-concepts/scenegraph-xml/overview.md). Most of your application will be comprised with the built-in SceneGraph components. This section covers the custom components provided with Roku. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| Button | rock_developer | *Extends* [*Button*](https://developer.roku.com/docs/references/scenegraph/widget-nodes/button.md) ## Description In order to properly handle commands, we extended the Roku Button with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:Button rockCommand="pushPage" rockPageGuid="4443b83e-86c9-4e35-9637-13b8991856ed" /> ``` | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/button) |
| Content Node | rock_developer | *Extends* [*Content Node*](https://developer.roku.com/docs/references/scenegraph/control-nodes/contentnode.md) ## Description In order to properly handle commands, we extended the Roku Content Node with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:ContentNode rockCommand="pushPage"... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node) |
| Page | rock_developer | The standard control that is used for your page content. *Extends* [*Group*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/group.md) ## Description This is a group of views that represents an entire page of content. ## Field \| Field \| Type \| Description \| \| --- \| --- \| --- \| \| initialFocus \| string \| The ID of the item you want to be focused when the page comes into view. \| ## Examples ```... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/page) |

### Roku Layouts And Resources

Keywords: `layout nodes, rowlist, roku resources, tips and tricks, useful links`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Focus Group | rock_developer | Manage vertical or horizontal focus in your Roku application. *Extends* [*LayoutGroup*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/layoutgroup.md) ## Description Unfortunately, as of 2024, focus management is not built into Roku applications (like we are used to with Apple TV). This control handles three simple things automatically for you: 1. Display views vertically/horizontally. 2.... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| Controls | rock_developer | Roku applications are built with an XML language named [SceneGraph](https://developer.roku.com/docs/developer-program/core-concepts/scenegraph-xml/overview.md). Most of your application will be comprised with the built-in SceneGraph components. This section covers the custom components provided with Roku. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| Roku Resources | rock_developer | * [SceneGraph Reference](https://developer.roku.com/en-gb/docs/references/references-overview.md) - Roku documentation for all the built-in SceneGraph components. * [Roku Samples](https://github.com/rokudev/samples) - A repository of Roku sample applications/SceneGraph. | [source](https://community.rockrms.com/developer/roku-docs/resources/roku-resources) |
| 📚 Resources | rock_developer | [Controls](/documentation/roku-docs/resources/controls) [Layout Nodes](/documentation/roku-docs/resources/layout-nodes) [Roku Resources](/documentation/roku-docs/resources/roku-resources) [Tips and Tricks](/documentation/roku-docs/resources/tips-and-tricks) [Useful Links](/documentation/roku-docs/resources/useful-links) | [source](https://community.rockrms.com/developer/roku-docs/resources) |
| RowList | rock_developer | The RowList Node component within SceneGraph is used to create a horizontal list of items. This component is ideal for displaying a series of elements that can be scrolled horizontally. This layout accepts an unlimited amount of vertical and horizontal scrollability. \| Parameter \| Type \| Description \| \| --- \| --- \| --- \| \| itemSize \| vector2d \| The size of the RowList element. \| \| numRows \| int \| Specifies the... | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes/rowlist) |
| Layout Nodes | rock_developer | Although Roku has many different layouts, very few have default item templates. Be cautious when picking your SceneGraph elements as we try to avoid custom BrightScript components. | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes) |
| Button | rock_developer | *Extends* [*Button*](https://developer.roku.com/docs/references/scenegraph/widget-nodes/button.md) ## Description In order to properly handle commands, we extended the Roku Button with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:Button rockCommand="pushPage" rockPageGuid="4443b83e-86c9-4e35-9637-13b8991856ed" /> ``` | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/button) |
| Content Node | rock_developer | *Extends* [*Content Node*](https://developer.roku.com/docs/references/scenegraph/control-nodes/contentnode.md) ## Description In order to properly handle commands, we extended the Roku Content Node with an additional `rockCommand` field. It also has fields for all of the different command parameters (such as `rockVideoUrl`). ## Examples ``` <Rock:ContentNode rockCommand="pushPage"... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node) |
| Useful Links | rock_developer | A page containing some useful information and links. ## Feature Requests Have an idea to improve the Roku application development in Rock? Submit your feature requests on our [Ideas](https://community.rockrms.com/ideas) Page. We value your feedback and are always looking for ways to make the experience better! ## GitHub Issues If you run into any bugs or want to track the status of current issues, visit our GitHub... | [source](https://community.rockrms.com/developer/roku-docs/resources/useful-links) |
| Page | rock_developer | The standard control that is used for your page content. *Extends* [*Group*](https://developer.roku.com/docs/references/scenegraph/layout-group-nodes/group.md) ## Description This is a group of views that represents an entire page of content. ## Field \| Field \| Type \| Description \| \| --- \| --- \| --- \| \| initialFocus \| string \| The ID of the item you want to be focused when the page comes into view. \| ## Examples ```... | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/page) |


## Lava Capability References

This concept depends on the generated Lava capability layer. Agents should use the stable guidance first, then verify syntax and behavior against the official source and the live Rock instance.

- Reference index: [../lava/lava-reference-index.md](../lava/lava-reference-index.md)
- Safety matrix: [../lava/lava-safety-matrix.md](../lava/lava-safety-matrix.md)
- Agent usage examples: [../lava/lava-agent-usage-examples.md](../lava/lava-agent-usage-examples.md)
- Machine-readable rows: [agent/lava-capabilities.jsonl](../../../agent/lava-capabilities.jsonl)

## Rebuild Dependencies

- Source records: `92`
- Lava capability source records: `53`
- Approved claims: `16`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
