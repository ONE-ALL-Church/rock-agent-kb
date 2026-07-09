---
id: concept-content-personalization
title: Content And Personalization
generated: true
last_built: 2026-07-09T20:56:23+00:00
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
- The strongest source families in this build are: rock_documentation, rock_rocku, triumph_resources, rock_lava_docs, rock_recipes, rock_core_release_notes.
- Related tags found in source records: operations, usage, admin, lava, workflow, api, development, sql.
- Source detail types include: documentation_article, recipe, rock_lava_docs, training, triumph_resources.

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
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.1.8 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.1.8 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.1.8 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.1.8 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.1.8 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.1.8 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Personalization Segment](../../model-map/models/personalization-segment.md) | CMS | 19.1.8 | 52 | 21 | 36 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Event Calendar Content Channel](../../model-map/models/event-calendar-content-channel.md) | Event | 19.1.8 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.1.8 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection](../../model-map/models/content-collection.md) | CMS | 19.1.8 | 49 | 21 | 34 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Collection Source](../../model-map/models/content-collection-source.md) | CMS | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 17.5 | CMS | Fixed an issue where the Content Channel Item View block and the InteractionContentChannelItemWrite Lava command logged interactions using the Content Channel entity type instead of the Content Channel Item entity type. This caused interactions to be misclassified and not tracked correctly. Fixes: #6263 | [source](https://www.rockrms.com/releasenotes) |
| 18.2 | CMS | Fixed a security issue affecting multiple blocks that interact with Content Channels, where individuals with only View permissions could delete content items. The delete option is now correctly limited to those with Edit access. Fixes: #6538 | [source](https://www.rockrms.com/releasenotes) |

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
| No matched records |  |  |  |

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
- Approved claims: `0`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
