---
id: concept-content-personalization
title: Content And Personalization
generated: true
last_built: 2026-07-30T02:06:15+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - cms
  - lava
  - security
  - communications
  - media
  - workflows
  - people
---

# Content And Personalization

Content channels, assets, structured content, adaptive messages, personalization, segments, website content operations, and publishing workflows.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Content And Personalization` spans cms, lava, security, communications, media, workflows. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_rocku, rock_lava_docs, rock_recipes, rock_core_release_notes, triumph_resources.
- Related tags found in source records: operations, usage, admin, lava, workflow, api, development, sql.
- Source detail types include: documentation_article, recipe, rock_lava_docs, training, triumph_resources.

## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | The Tools > Content screen can limit the channel list to channels with pending items, while a selected channel's items can be filtered by status, date range, or title. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items) |
| official | behavior | A church can selectively publish content to the Content Library, where it is stored in a Spark-hosted cloud environment and can be downloaded into another church's Rock instance. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/intro-to-the-content-library) |
| official | behavior | In Rock 19.0, the Asset Manager under Admin Tools > CMS Configuration manages files and folders in configured storage providers, including cloud storage and the Rock server. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager) |
| official | behavior | Rock can personalize website content for visitors who are not logged in by using available browsing-session and visitor signals. | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization) |
| official | behavior | The Content Channel Item Self Update job evaluates Lava stored in a content channel item attribute and writes the result to another item attribute; the Lava output must be compatible with the target attribute's field type. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items) |
| official | behavior | With view tracking enabled on the adaptivemessage Lava command, an adaptation stops displaying to a viewer after its configured saturation count is reached within the configured day range. | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages) |
| official | behavior | Rock includes a File Manager block under Admin Tools > CMS Configuration > File Manager that supports uploading and deleting files and managing directories. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/file-manager) |
| official | behavior | Request Filters can personalize content without identifying the visitor by evaluating request context such as site, new-or-returning status, device type, query parameters, cookies, browser version, IP range, IP-derived location, and visit day or time. | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters) |
| official | behavior | Changing a Content Channel's Content Library license affects only later uploads; items already uploaded retain the license assigned when they were uploaded. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library) |
| official | behavior | A required Media Watch attribute can prevent submission of a workflow form until the participant has watched the configured percentage of its single assigned video; progress counts unique watched seconds, so seeking ahead does not satisfy the requirement. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-digital-media-in-workflows) |
| official | behavior | A content channel item can use items from other channels as children; each child can belong to multiple parents and can have child items of its own. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-content-channel-child-items) |
| official | behavior | A person must satisfy every configured filter area in a personalization segment, while conditions within an individual area can use either Any or All matching logic. | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments) |
| official | behavior | A Content Channel Item is displayed no earlier than its Start date and can be automatically removed from display by assigning an Expire date. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item) |
| official | behavior | Rock can automatically create a Content Channel Item for a video uploaded to a video service provider, allowing the video to be published and its engagement tracked within Rock. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media) |
| official | behavior | Rock ranks trending content collection items by dividing each item's interactions during the configured Trending Window by the item's age in days, with the age divisor capped at the window length. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/trending-content) |
| official | behavior | A channel feed uses the default RSS Lava template unless TemplateId selects another Lava Templates defined value; Count limits returned items and defaults to 10, while EnableDebug exposes the template's available merge fields. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds) |
| official | behavior | Adaptive Messages centralize multiple message adaptations behind one Lava command and can select variants using personalization data, date windows, view counts, and optional saturation limits. | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages) |
| official | behavior | When a content channel uses approvals, only users with Approval permission can set a content item's approval status. | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items) |
| More |  | 83 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_core_release_notes`: 2
- `rock_documentation`: 73
- `rock_lava_docs`: 1
- `rock_model_map`: 12
- `rock_recipes`: 1
- `rock_rocku`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Content Channels | rock_documentation | [Intro to Content Channels](/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels?Version=v19.0) [Channel Types](/documentation/digital-publishing/content-management/content-channels/channel-types?Version=v19.0) [Use Content Channels](/documentation/digital-publishing/content-management/content-channels/use-content-channels?Version=v19.0) [Add a Content Channel... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels) |
| Content Component | rock_documentation | [Intro to Content Components](/documentation/digital-publishing/content-management/content-component/intro-to-content-components?Version=v19.0) [Content Component Templates](/documentation/digital-publishing/content-management/content-component/content-component-templates?Version=v19.0) [Configure Content... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component) |
| Personalization Segments | rock_documentation | [Intro to Personalization Segments](/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments?Version=v19.0) [Use Request Filters](/documentation/digital-publishing/personalization/personalization-segments/use-request-filters?Version=v19.0) [Configure Site for... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments) |
| Personalize Content Channel Items | rock_documentation | Often, content is published to your site using Content Channel Items. Rock provides a built-in way to show, hide or prioritize Content Channel Items based on whether the person viewing them meets the criteria of the personalization segments or request filters you've created. Personalization for Content Channel Items is enabled at the Content Channel level under `Admin Tools > CMS Configuration > Content Channels`.... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items) |
| Content Management | rock_documentation | SECTIONS [Content Channels](?Version=v19.0#content-channels) [Content Collections](?Version=v19.0#content-collections) [Dynamic Content](?Version=v19.0#dynamic-content) [Content Component](?Version=v19.0#content-component) [Content Library](?Version=v19.0#content-library) [Digital Media](?Version=v19.0#digital-media) [Social Networks](?Version=v19.0#social-networks) [Asset Manager... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management) |
| Content Collections | rock_documentation | [Intro to Content Collections](/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections?Version=v19.0) [Content Collection View](/documentation/digital-publishing/content-management/content-collections/content-collection-view?Version=v19.0) [Set Up Content... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections) |
| Dynamic Content | rock_documentation | [Intro to Dynamic Content](/documentation/digital-publishing/content-management/dynamic-content/intro-to-dynamic-content?Version=v19.0) [Manage Content Items](/documentation/digital-publishing/content-management/dynamic-content/manage-content-items?Version=v19.0) [Add Content Items](/documentation/digital-publishing/content-management/dynamic-content/add-content-items?Version=v19.0) | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content) |
| Intro to Content Components | rock_documentation | In Rock there are lots of ways to put content onto a page. For example, in this guide we have articles covering HTML content blocks and Content Channel blocks. Another option is content components. Content components can be thought of as a marriage between HTML blocks and Content Channel blocks. They're a blend of content and style. Website designers can create great looking templates and define which elements of... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components) |
| Manage Content Items | rock_documentation | While it's possible to add new content items on the channel configuration page (`Admin Tools > CMS Configuration > Content Channels`), most of your staff won't have access to these screens. For staff, it's easier for them to add their content under `Tools > Content`. On this screen they will see a list of each content channel they have *View* access to. Clicking one of the items will display the content items for... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items) |
| Intro to Content Collections | rock_documentation | Let's say you have a content channel for blog posts, and a content channel for sermons. You can group those two content channels together under a single collection, known as a *Content Collection*. Content collections put the content for those channels in one place, unlocking the ability to search for content across both channels at once. So, if you have a blog post about finances and a sermon about finances, a... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections) |
| Content Library | rock_documentation | [Intro to the Content Library](/documentation/digital-publishing/content-management/content-library/intro-to-the-content-library?Version=v19.0) [Library Viewer](/documentation/digital-publishing/content-management/content-library/library-viewer?Version=v19.0) [Set Up The Content Library](/documentation/digital-publishing/content-management/content-library/set-up-the-content-library?Version=v19.0) | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library) |
| Intro to Dynamic Content | rock_documentation | Rock's advanced dynamic content tools allow you to extend the application without having to write any code. That’s kind of a big deal, right? You can customize Rock for your organization without any programming knowledge! We're going to talk about how to manage content that is added to content channels, then dive into how to set those content channels up. But first - a quick overview of the components that make up... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/intro-to-dynamic-content) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.2.0 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.2.0 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.2.0 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.2.0 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Personalization Segment](../../model-map/models/personalization-segment.md) | CMS | 19.2.0 | 52 | 21 | 36 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Event Calendar Content Channel](../../model-map/models/event-calendar-content-channel.md) | Event | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
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

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 19.3 | CMS | Fixed the Content Channel Item List block to show the add and delete options for individuals with Edit access to the content channel, rather than requiring Edit access on the Content Channel Item entity itself. Fixes: #6914 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | CMS | Fixed an issue where the Content Channel Item View block and the InteractionContentChannelItemWrite Lava command logged interactions using the Content Channel entity type instead of the Content Channel Item entity type. This caused interactions to be misclassified and not tracked correctly. Fixes: #6263 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Content Channels

Keywords: `content channel, content item, structured content`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Content Channels | rock_documentation | [Intro to Content Channels](/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels?Version=v19.0) [Channel Types](/documentation/digital-publishing/content-management/content-channels/channel-types?Version=v19.0) [Use Content Channels](/documentation/digital-publishing/content-management/content-channels/use-content-channels?Version=v19.0) [Add a Content Channel... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels) |
| Content Component | rock_documentation | [Intro to Content Components](/documentation/digital-publishing/content-management/content-component/intro-to-content-components?Version=v19.0) [Content Component Templates](/documentation/digital-publishing/content-management/content-component/content-component-templates?Version=v19.0) [Configure Content... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component) |
| Content Management | rock_documentation | SECTIONS [Content Channels](?Version=v19.0#content-channels) [Content Collections](?Version=v19.0#content-collections) [Dynamic Content](?Version=v19.0#dynamic-content) [Content Component](?Version=v19.0#content-component) [Content Library](?Version=v19.0#content-library) [Digital Media](?Version=v19.0#digital-media) [Social Networks](?Version=v19.0#social-networks) [Asset Manager... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management) |
| Content Collections | rock_documentation | [Intro to Content Collections](/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections?Version=v19.0) [Content Collection View](/documentation/digital-publishing/content-management/content-collections/content-collection-view?Version=v19.0) [Set Up Content... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections) |
| Dynamic Content | rock_documentation | [Intro to Dynamic Content](/documentation/digital-publishing/content-management/dynamic-content/intro-to-dynamic-content?Version=v19.0) [Manage Content Items](/documentation/digital-publishing/content-management/dynamic-content/manage-content-items?Version=v19.0) [Add Content Items](/documentation/digital-publishing/content-management/dynamic-content/add-content-items?Version=v19.0) | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content) |
| Intro to Content Components | rock_documentation | In Rock there are lots of ways to put content onto a page. For example, in this guide we have articles covering HTML content blocks and Content Channel blocks. Another option is content components. Content components can be thought of as a marriage between HTML blocks and Content Channel blocks. They're a blend of content and style. Website designers can create great looking templates and define which elements of... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components) |
| Manage Content Items | rock_documentation | While it's possible to add new content items on the channel configuration page (`Admin Tools > CMS Configuration > Content Channels`), most of your staff won't have access to these screens. For staff, it's easier for them to add their content under `Tools > Content`. On this screen they will see a list of each content channel they have *View* access to. Clicking one of the items will display the content items for... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items) |
| Intro to Content Collections | rock_documentation | Let's say you have a content channel for blog posts, and a content channel for sermons. You can group those two content channels together under a single collection, known as a *Content Collection*. Content collections put the content for those channels in one place, unlocking the ability to search for content across both channels at once. So, if you have a blog post about finances and a sermon about finances, a... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections) |
| Content Library | rock_documentation | [Intro to the Content Library](/documentation/digital-publishing/content-management/content-library/intro-to-the-content-library?Version=v19.0) [Library Viewer](/documentation/digital-publishing/content-management/content-library/library-viewer?Version=v19.0) [Set Up The Content Library](/documentation/digital-publishing/content-management/content-library/set-up-the-content-library?Version=v19.0) | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library) |
| Intro to Dynamic Content | rock_documentation | Rock's advanced dynamic content tools allow you to extend the application without having to write any code. That’s kind of a big deal, right? You can customize Rock for your organization without any programming knowledge! We're going to talk about how to manage content that is added to content channels, then dive into how to set those content channels up. But first - a quick overview of the components that make up... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/intro-to-dynamic-content) |

### Asset Manager

Keywords: `asset manager, asset, file, image`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Asset Manager System | rock_documentation | [Intro to the Asset Manager](/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager?Version=v19.0) [Set Up Storage Provider](/documentation/digital-publishing/content-management/asset-manager-system/set-up-storage-provider?Version=v19.0) [View Asset Manager](/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager?Version=v19.0) [Add... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system) |
| Add Content | rock_documentation | You might be wondering, when should I use the asset manager and when should I use a file attribute? The difference is subtle. File attributes are best used to attach files to content channel items or people where you don't care about the details of where the file is stored (this is all handled for you in the file type setup). Using the asset manager gives you much more control of where and how the file will be... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content) |
| Intro to the Asset Manager | rock_documentation | The Asset Management system gives you first class integration between your Rock system and a remote cloud storage system (such as Azure or Amazon S3). With the Asset field type, you can add an attribute to existing things (such as a Content Channel, Person, Group, etc.) and give your content editors the ability to select files and images stored in your cloud accounts. ## Suggested Videos *... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager) |
| View Asset Manager | rock_documentation | You can view and manage the files in the Asset Manager under `Admin tools > CMS Configuration > Asset Manager`. This block allows you to view and manage documents in the providers you have configured. Think of this as your file manager for your cloud storage and Rock server. 1. **Add and delete folders**- From here you can add or delete folders in the asset manager. 2. **Folder tree** - The folder tree shows parent... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager) |
| Set Up Storage Provider | rock_documentation | Note **Access**Before you get started, you'll need to set up your Asset Storage Provider. Amazon S3, Google Cloud Storage, Azure Cloud Storage and your local Server File System are currently supported out of the box. More asset storage providers may be available in the Rock Shop. The asset provider is configured under `Admin tools > System Settings > Asset Storage Providers.` This page is where you will configure... | [source](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/set-up-storage-provider) |

### Adaptive Messages

Keywords: `adaptive message, adaptive messages, personalization`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Intro to Adaptive Messages | rock_documentation | Being able to personalize content is great but what if you want to vary a particular personalized message slightly, based on nuances within the data or a period of time? *Adaptive Messages* take content personalization to the next level, allowing you to tailor messages based on differences in an individual’s data, view counts, and date ranges. Building on the foundation of *Personalization Segments*, *Adaptive... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages) |
| Set Up Adaptive Messages | rock_documentation | Let’s look at how to set this up for the Adaptive Message example described in the [last article](/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages). We’ll assume you’ve already created Personalization Segments for the first three groups of people mentioned in the last article. No need to create a segment for the default group. Simply include a fallback message directly... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages) |
| Adaptive Messages | rock_documentation | [Intro to Adaptive Messages](/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages?Version=v19.0) [Set Up Adaptive Messages](/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages?Version=v19.0) | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages) |

### Personalization And Segments

Keywords: `personalization, segment, segments, audience`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Personalization Segments | rock_documentation | [Intro to Personalization Segments](/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments?Version=v19.0) [Use Request Filters](/documentation/digital-publishing/personalization/personalization-segments/use-request-filters?Version=v19.0) [Configure Site for... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments) |
| Personalize Content Channel Items | rock_documentation | Often, content is published to your site using Content Channel Items. Rock provides a built-in way to show, hide or prioritize Content Channel Items based on whether the person viewing them meets the criteria of the personalization segments or request filters you've created. Personalization for Content Channel Items is enabled at the Content Channel level under `Admin Tools > CMS Configuration > Content Channels`.... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items) |
| Personalization | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Personalization Segments](?Version=v19.0#personalization-segments) [Localization](?Version=v19.0#localization) ### Overview Articles [Intro to Personalization](/documentation/digital-publishing/personalization/overview/intro-to-personalization?Version=v19.0) ### Personalization Segments Articles [Intro to Personalization... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization) |
| Update Personalization Job | rock_documentation | The *Update Personalization Data* job keeps the people returned by your personalization segment up to date and accurate. The job adds or removes people from the list based on whether they currently meet the conditions of the segment. If you ever need to check the current list of who meets the conditions of a segment, just click the ` ` button on the *Personalization Segments* page located at `Admin Tools > CMS... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job) |
| Intro to Personalization Segments | rock_documentation | As we mentioned earlier, personalization segments let you filter content based on something about the person (think Data View) or based on a person's browsing history. We have data about people in Rock, so it's only natural we would personalize content using Rock data. For instance, you might want information on baptisms to display only if the person visiting your site has not been baptized. As an extension of that,... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments) |
| Personalize Using Lava | rock_documentation | Using [Lava](https://community.rockrms.com/Lava) you can personalize content in many places, such as the *HTML Content* block. But you're not limited to blocks. Personalization can also be used in communications too, so feel free to personalize content within an email. There are two ways to get personalization using Lava. The first is the... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava) |
| Localization | rock_documentation | [Intro to Localization](/documentation/digital-publishing/personalization/localization/intro-to-localization?Version=v19.0) [Localize Phone Numbers](/documentation/digital-publishing/personalization/localization/localize-phone-numbers?Version=v19.0) [Localize Dates & Times](/documentation/digital-publishing/personalization/localization/localize-dates-times?Version=v19.0) [Localize... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/localization) |
| Intro to Adaptive Messages | rock_documentation | Being able to personalize content is great but what if you want to vary a particular personalized message slightly, based on nuances within the data or a period of time? *Adaptive Messages* take content personalization to the next level, allowing you to tailor messages based on differences in an individual’s data, view counts, and date ranges. Building on the foundation of *Personalization Segments*, *Adaptive... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages) |
| Configure Site for Personalization | rock_documentation | The last step in getting Rock ready for personalization is to update your site's settings under `Admin Tools > Websites`. For each site that you want to work with, check the box for *Enable Personalization*. While you're there, you'll also want to check the box for *Enable Visitor Tracking*, which we'll talk more about in the next article. | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization) |
| Intro to Personalization | rock_documentation | Churches need to focus on getting the right content to the right people, both during the weekend and throughout the week. That's why Rock's personalization features are critical to your digital strategy. They enable you to have content on your site that is dynamic and custom tailored for the person viewing it. This ensures visitors to your site are seeing relevant content personalized for them, even when the person... | [source](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization) |


## Rebuild Dependencies

- Source records: `92`
- Approved claims: `101`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
