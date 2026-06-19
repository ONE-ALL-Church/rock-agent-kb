---
id: authored-content-personalization
title: Content And Personalization
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Content And Personalization

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Content And Personalization index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock RMS content and personalization work is best understood as a layered publishing system. The core layer is structured content: content channel types define reusable schemas, content channels apply those schemas to a real publishing surface, and content channel items are the individual pieces of content that editors create, approve, schedule, display, secure, index, personalize, and syndicate. Rock’s official Content Channels documentation frames this as the main way to publish repeatable, structured website content without building custom C# features for every ministry need ([Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels), [Intro to Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels)).

For agents doing real Rock work, the practical questions are usually not “what is content?” but:

- Which entity owns the content: page HTML, content channel item, content component, media element, file asset, calendar event, or communication?
- Which staff surface owns entry and approval: `Admin Tools > CMS Configuration`, `Tools > Content`, a page block configuration, an external provider, or a workflow?
- Which display surface consumes it: Content Channel View, Content Channel Item View, Content Collection View, Content Component, HTML Content, Lava, RSS, media player shortcode, or a custom block?
- Which audience rules apply: security authorization, content item status, start/expire dates, campus context, personalization segment, request filter, adaptive message saturation, or manual Lava logic?
- Which operational dependency makes the content appear: cache, site personalization setting, visitor tracking, `Update Personalization Data`, `Index Content Collections`, media sync, storage provider permissions, or Lava template behavior?

Rock’s personalization features sit on top of the publishing layer. Personalization segments classify known people by Rock data or browsing behavior; request filters classify visits by request characteristics; anonymous visitor tracking can personalize based on cookies; content channel items can be shown, hidden, or prioritized when channel personalization is enabled; Lava can call personalization directly; adaptive messages can choose among message variants with saturation rules ([Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization), [Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments), [Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages)).

Agents should treat this area as both CMS and data operations. A content bug may be caused by content status, dates, block filters, Lava, page routing, security, missing attribute values, stale personalization data, missing visitor tracking, a collection index that has not run, media provider configuration, file storage permissions, or a version-specific bug. Before changing configuration, inspect the live Rock instance, note the exact channel, block, item, page, site, segment, request filter, and job involved, and confirm the target Rock version against current release notes.

This guide is a synthesis of official Rock documentation, RockU training metadata, Lava documentation, release-note records, GitHub source snippets, and one community recipe. It is a draft guide and should be reviewed against a live Rock instance before being used for destructive or public-facing changes.

## 2. Scope And Terminology

“Content and personalization” in Rock covers several related but distinct systems:

- **Content Channel Type**: A reusable schema for dynamic content. It defines structural behavior and attributes available to channels and items. Rock ships with several examples and also supports universal channel types for one-off structured channels ([Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/channel-types), [Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types)).
- **Content Channel**: A configured publishing container based on a content channel type. Examples include blog, announcements, devotionals, podcasts, sermons, promotions, or resource libraries ([Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels)).
- **Content Channel Item**: A single item inside a content channel, such as one blog post, message, promo, podcast episode, article, or resource ([Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item)).
- **Content Component**: A page-level structured content pattern that combines editor-friendly fields with designer-controlled Lava output. Content components are useful when editors need to populate designed page sections without editing raw HTML ([Content Component](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component), [Intro to Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components)).
- **Content Collection**: A search/index surface that aggregates multiple content channels and calendars so users can search and filter across them ([Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections), [Intro to Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections)).
- **Content Library**: A feature for sharing and downloading content between Rock instances through a library viewer and channel-level library settings ([Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library), [Set Up The Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library)).
- **Asset Manager**: A file-management interface and asset field integration for files stored on the Rock server or remote/cloud storage providers such as Azure or Amazon S3 ([Asset Manager System](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system), [Intro to The Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager)).
- **Digital Media**: Rock’s media publishing and analytics features, including media accounts, media elements, media folders, media player Lava shortcode, workflow integration, and content channel item publishing ([Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media), [Intro to Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media)).
- **Personalization Segment**: A rule-backed audience definition based on person data or browsing history. It is used to personalize pages, channel items, Lava output, and adaptive messages ([Intro to Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments)).
- **Request Filter**: A personalization filter based on request characteristics such as IP range or query string parameters, not necessarily a known person ([Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters)).
- **Adaptive Message**: A personalization feature that selects a message adaptation based on segments, request filters, dates, and saturation behavior ([Intro to Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages), [Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages)).
- **Lava**: Rock’s templating layer. Lava renders content channel items, content components, social tags, personalization commands, interaction logging commands, media shortcodes, and many other dynamic outputs ([Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)).

This guide focuses on content channels, asset management, adaptive messages, personalization, structured content operations, and the dependencies agents must check when troubleshooting or implementing publishing workflows. It references related Rock areas where they directly affect content behavior: CMS pages and blocks, Lava, security, communications, media, workflows, people data, reporting, and model/API surfaces.

## 3. Content And Personalization Mental Model

Think of Rock content as five cooperating pipelines.

First, the **schema pipeline** decides what information editors can store. Content channel types and content channel item attributes define the fields. Universal channel types let an organization avoid creating a custom type when only one channel needs the structure ([Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types)). Content component templates define reusable page-section fields and Lava output ([Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/content-component-templates), [Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates)).

Second, the **editorial pipeline** decides who enters content and how it moves toward publication. Staff can add content from administrative channel configuration or from `Tools > Content`; the latter is generally the staff-facing path because it shows channels the current user can view and supports pending-item management ([Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items), [Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item)). Channel settings determine whether statuses, approvals, priority, date behavior, summary fields, child items, tags, and RSS apply.

Third, the **rendering pipeline** decides where content appears. A Content Channel View block can list channel items using a Lava template and status filter ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)). A Content Channel Item View block can display one item, often via query string or route data. Content Collection View can search across multiple sources with indexing ([Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view)). Content components render a configured page section using component templates. RSS feeds use `GetChannelFeed.ashx?ChannelId=X` when the channel enables RSS and can use Lava templates from defined Lava templates ([Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds)).

Fourth, the **audience pipeline** decides whether the current viewer should see content. Basic filters include item status, start and expire dates, block settings, page/site security, and Lava conditionals. Personalization adds site-level enablement, visitor tracking, personalization segments, request filters, channel-level personalization, and adaptive messages ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization), [Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items)).

Fifth, the **measurement pipeline** records and analyzes content interaction. Content channel item interactions can be logged by blocks and Lava commands; content collections use interactions for trending calculations; media features track plays and engagement ([Trending Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/trending-content), [Intro to Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)). Release notes matter here because Rock fixed a bug where content channel item interactions were logged under the wrong entity type in some paths; verify the target Rock version before trusting analytics for historical comparisons ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agents should avoid treating these pipelines independently. A page can have a correct content item and still show nothing because the site has personalization disabled, the item is expired, the block is filtering by status, the collection index is stale, the current person fails a segment, the request filter key is wrong, a Lava template expects an attribute that is missing, or security was hardened in a later release.

## 4. Source Authority And How To Use This Guide

Use this guide as an operational synthesis, not as a replacement for the live Rock instance.

Authority order for decision-making:

1. **Live Rock instance**: Always wins for current configuration, enabled plugins, block settings, actual entity IDs, security, job schedules, attributes, and data.
2. **Official Rock documentation**: Primary source for intended configuration and user-facing behavior, especially the Digital Publishing Content Management and Personalization guides ([Content Management](https://community.rockrms.com/documentation/digital-publishing/content-management), [Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization)).
3. **RockU training**: Useful for workflow orientation and demonstrations, especially content channel, content component, asset manager, media, and content library training topics ([Content Channel Types and Content Channels](https://community.rockrms.com/rocku/content-channels/content-channel-types-and-content-channels)).
4. **Release notes**: Required for version caveats, security fixes, bug fixes, and migration-impacting changes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
5. **GitHub source-code snippets and model/API records**: Useful for implementation landmarks, API route names, controller/service existence, and block behavior, but agents should verify against the deployed Rock version and not assume `develop` branch code exactly matches production ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
6. **Community recipes and vendor articles**: Useful for patterns and examples, but lower authority. Community recipes explicitly warn that they are not reviewed or endorsed by the Rock core team ([Content Channels With Slugs](https://community.rockrms.com/recipes/128)). Vendor articles can explain operational strategy but should not be treated as product specification ([Structured Content Rock Upgrade](https://www.triumph.tech/resources/structured-content-rock-upgrade)).

When the source pack is thin, this guide states what to inspect rather than inventing behavior. For example, the pack confirms that adaptive message model and API controllers exist, and that adaptive message adaptation segments have their own controller/service, but it does not provide the full entity schema. Agents should inspect `Admin Tools > Adaptive Message`, the model map if available, the database schema, or the deployed source before making field-level assumptions.

## 5. Core Configuration And Data Model

The content and personalization configuration surface is distributed across CMS configuration, websites, general settings, tools, jobs, and page blocks.

Core configuration paths from the source pack:

- `Admin Tools > CMS Configuration > Content Channels`: Create and manage content channels; enable personalization for a content channel; enable Content Library features; configure channel behavior ([Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels), [Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items), [Set Up The Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library)).
- `Admin Tools > CMS Configuration > Content Collections`: Create collections that combine channels and calendars for search and filtering ([Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections)).
- `Admin Tools > CMS Configuration > Content Component Templates`: Create reusable content component templates with Lava output ([Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates)).
- `Admin Tools > CMS Configuration > Asset Manager`: Manage files in configured providers and file-manager roots ([View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager)).
- `Admin Tools > CMS Configuration > Personalization Segments`: Manage segment definitions and inspect current segment membership ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)).
- `Admin Tools > CMS Configuration > Request Filters`: Manage request-based filters and keys ([Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters)).
- `Admin Tools > Websites`: Enable personalization and visitor tracking for each site ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization)).
- `Admin Tools > System Settings > System Configuration`: Configure visitor cookie persistence length for anonymous visitor personalization; the source record states the default cookie length is 365 days ([Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors)).
- `Admin Tools > General Settings > Defined Types > Lava Templates`: Manage feed templates used by content channel RSS feed endpoints ([Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds)).
- `Admin Tools > General Settings > Attribute Categories`: Used by content component item attribute setup when categories are matched to template names or scoped more broadly ([Add Content Component Item Attributes](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes)).
- `Tools > Content`: Staff-facing content entry and approval surface for channels the current user can view ([Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items)).
- `Tools > Interactions`: Operational surface referenced by Lava interaction logging docs for viewing interaction session summaries ([Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)).

Core entities implied or confirmed by source pack:

- `ContentChannelType`: Defines reusable content structure.
- `ContentChannel`: Represents an actual channel instance.
- `ContentChannelItem`: Represents a published item.
- Content channel item parent/child relationships: Items can have child items from other channels; one item can have multiple parents, and child items can have children ([Add Content Channel Child Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-content-channel-child-items)).
- `Attribute` and `AttributeValue`: Used for channel, item, component, person, group, media, asset, and many other structured fields.
- `BinaryFile` and file types: Used by file attributes and image/file handling; file type configuration affects storage and image processing ([Understand File Types](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/understand-file-types)).
- Asset provider and file manager configuration: Source code for `Rock.Blocks/Cms/FileAssetManager.cs` confirms the File Asset Manager block browses and manages local or remote/cloud files, with settings such as asset provider enablement, file manager enablement, height mode, root folder, browse mode, file editor page, zip uploader, and security grant token ([FileAssetManager.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/FileAssetManager.cs)).
- `PersonalizationSegment`: Inferred from docs and segment configuration path.
- `RequestFilter`: Inferred from docs and request filter configuration path.
- `PersonAliasPersonalization`: Official docs state the `Update Personalization Data` job updates this table, linking a person alias to a segment with a personalization type field ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)).
- `AdaptiveMessage`: Source snippets confirm model, service, REST v1 controller, and REST v2 endpoints exist for adaptive messages ([AdaptiveMessageService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageService.CodeGenerated.cs), [AdaptiveMessagesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs)).
- `AdaptiveMessageAdaptationSegment`: Source snippets confirm service and REST v2 endpoints for adaptation-to-segment relationships ([AdaptiveMessageAdaptationSegmentService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageAdaptationSegmentService.CodeGenerated.cs), [AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs)).
- `MediaElement`: Digital media docs say content channels that publish media need an item attribute of type `Media Element` ([Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media), [Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items)).
- `Interaction`: Used for content views, content collection trending, media analytics, and explicit Lava interaction writes.

For agents, the most important data-model move is to identify the exact entity boundary before making a change. A “hero image not showing” could be a content channel item image attribute, an asset attribute, a binary file attribute, a media element thumbnail, a content component field, an HTML editor inline asset, or a Lava-generated file URL. The operational inspection path differs for each.

## 6. Primary Entities And Relationships

Content channel types, channels, and items form the backbone.

A **content channel type** defines the reusable pattern. It can determine item date behavior, whether a content field is HTML or code-oriented, and what attributes are available to channels and items. Official docs use examples like website ads, blogs, and other structured publishing needs ([Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/channel-types)). When a single channel needs unique fields, a universal channel type can be used and the channel can define its own item attributes ([Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types)).

A **content channel** implements that type. It owns settings such as name, description, content entry behavior, channel-specific attributes, item attributes, security, RSS enablement, library enablement, and personalization enablement. The source pack does not provide the complete content channel field list; inspect the live edit screen in `Admin Tools > CMS Configuration > Content Channels` for exact fields in the deployed version ([Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels)).

A **content channel item** contains content. Official docs identify common item fields such as title, status, priority if enabled, dates based on channel type, content body, summary text, and attributes ([Add Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items)). Agents should inspect the channel type and channel attribute configuration before assuming an item has image, summary, author, speaker, campus, topic, media, URL, or call-to-action fields.

A **child item relationship** connects content items across channels. Rock’s podcast implementation is given as an example: series items can have message items as children, allowing each side to own its own attributes while still forming a combined publishing experience. A single item can belong to more than one parent, and nested child relationships are possible ([Add Content Channel Child Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-content-channel-child-items)). Agents should verify parent/child direction in the UI or database before fixing a “missing episode” or “series not showing item” problem.

A **content collection** references channels and calendars rather than replacing them. The official setup article says collections do not require restructuring content channels or calendars; they aggregate existing sources and can include the same content in more than one collection ([Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections)). Collection display depends on indexing and block settings. Attribute filters may come from content channel item attributes ([Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view)).

A **content component** is page/block scoped. It is not merely an HTML block and not exactly a content channel list. Designers build templates with fields and Lava; editors fill the fields. Attribute scoping can apply to an individual component, a component template, or all content components ([Intro to Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components), [Add Content Component Item Attributes](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes)).

An **asset** relationship may be attribute-backed or editor-inserted. The asset manager docs distinguish file attributes from asset manager usage: file attributes are better when the file simply belongs to an entity and storage details should be abstracted by file type setup, while asset manager gives more direct control over where and how files are stored and can select existing provider files ([Add Content](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content)).

A **personalization segment** relationship ultimately affects people or visitors. The update job maintains segment membership for person aliases in `PersonAliasPersonalization` ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)). Anonymous personalization relies on visitor tracking and cookies rather than a known person record ([Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors)).

An **adaptive message adaptation** relates a base message to one or more audience conditions. The source pack confirms an `AdaptiveMessageAdaptationSegment` model/service/controller exists; use the live UI or model map to verify exact fields such as message, adaptation, segment, order, dates, view limits, and fallback behavior before performing direct API or SQL operations ([AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs)).

## 7. Common Content And Personalization Workflows

### Create a structured content channel

Start with the publishing need, not the UI.

1. Identify the repeated content pattern: announcements, sermons, events, resources, blog posts, devotionals, landing-page promos, ministry cards, classes, or podcasts.
2. Decide whether an existing content channel type fits. Use a universal channel type for a one-off channel when the structure belongs to the channel itself ([Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types)).
3. Define item attributes for every field editors should manage separately: image, topic, author, speaker, campus, ministry, call-to-action URL, button text, media element, series, downloadable asset, resource type, or sort value.
4. Configure security before onboarding editors. Ensure staff have view/edit/approval rights appropriate to the content surface ([Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content)).
5. Add test content from `Tools > Content` if the workflow is staff-facing, not only from admin configuration ([Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items)).
6. Add a Content Channel View block to the target page and render items with Lava ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)).
7. Verify the output as an anonymous visitor, a logged-in staff user, and a target audience member if personalization or security applies.

### Publish a content item

When adding an item, inspect:

- Title.
- Status and approval behavior.
- Priority, if enabled by the channel.
- Date fields, which depend on channel type.
- Content body editor type.
- Summary text if available.
- Attributes and required fields.
- Personalization segment/request filter assignments if channel personalization is enabled.
- Parent/child relationships if applicable.
- Slug or route-related fields if used by the site.

The official docs note that content can be entered from the admin channel screen or from `Tools > Content`; operationally, prefer the staff surface for normal editorial work because it aligns better with permissions and approval workflows ([Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item), [Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items)).

### Display a list of channel items

Use Content Channel View when the page needs a listing. Key block settings from official docs include channel, status, and format/Lava template ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)). The Lava format generally iterates through `Items`; verify available merge fields with Rock’s debug tools in a non-production-safe context if needed. If using a detail page, configure the block’s linked detail page and route behavior.

### Display a single channel item

The source pack references showing a single item and community slug patterns. For official implementation, inspect the Content Channel Item View block in the live instance and the page route. For slug-style URLs, a community recipe describes using `item.PrimarySlug` where available and falling back to `?Item={{ item.Id }}` in listing links, plus a route such as `message/{slug}` on the detail page ([Content Channels With Slugs](https://community.rockrms.com/recipes/128)). Because this is a community recipe and may be version-dependent, verify the deployed Rock version exposes `PrimarySlug` to Lava. Release notes in the source pack also indicate `PrimarySlug` and `ItemGlobalKey` were added to Lava fields in a later release; check the exact version before relying on those fields ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Aggregate content into a collection

Create a content collection when users need one search/filter surface across multiple channels or calendars. Official docs say collections can include any number of content channels and calendars and the same content can belong to multiple collections ([Intro to Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections), [Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections)). Add a Content Collection View block for search, filters, year filtering, and trending features ([Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view)). Run or verify the `Index Content Collections` job when results are stale ([Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections)).

### Add personalization to channel items

Enable personalization at multiple levels:

1. In `Admin Tools > Websites`, enable personalization for the site; enable visitor tracking if anonymous/history-based personalization is expected ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization)).
2. Define personalization segments and request filters ([Intro to Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments), [Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters)).
3. Run or verify `Update Personalization Data` for person-based segment membership ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)).
4. Enable personalization on the content channel under `Admin Tools > CMS Configuration > Content Channels` ([Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items)).
5. Assign segments/request filters to items.
6. Verify as a known matching person, a known non-matching person, and an anonymous visitor if applicable.

### Use adaptive messages

Use adaptive messages when multiple personalized variants compete for the same message slot and simple nested Lava personalization would become hard to reason about. Official docs describe adaptive messages as an extension of personalization segments that can account for data nuance, view counts, and date ranges ([Intro to Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages)). Setup happens under `Admin Tools > Adaptive Message` according to the source pack ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages)). Include a fallback message for users who do not match specific adaptations. Use saturation settings to avoid repeatedly showing the same message.

## 8. Content Channels Deep Dive

Content channels are Rock’s primary structured publishing tool. They let organizations avoid brittle raw HTML patterns by separating data entry from presentation. The official dynamic content documentation describes the system as three components: channel types, channels, and channel items ([Intro to Dynamic Content](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/intro-to-dynamic-content)).

### Channel type strategy

Choose or create channel types carefully. A channel type should represent a reusable schema, not a single content item. If several ministries need the same pattern, define a channel type. If only one channel needs a custom field set, use a universal channel type and place the fields at the channel/item level ([Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types)).

Good channel type candidates:

- Sermon/message series.
- Podcast series and episodes.
- Blog posts.
- Website promotions.
- Resource articles.
- Ministry landing-page cards.
- Devotionals.
- Staff-authored articles.
- Location-specific notices.

Poor channel type candidates:

- One static paragraph.
- One-off landing-page copy that does not need reuse.
- Highly designed page sections better served by content components.
- Binary files that are not content records.
- Content whose lifecycle is really an event registration, workflow, or communication.

### Channel configuration

A content channel is where the type becomes operational. Inspect:

- Name and description.
- Channel type.
- Item date behavior inherited or controlled by type.
- Whether priorities are enabled.
- Whether approvals/statuses are used.
- Whether RSS is enabled.
- Whether personalization is enabled.
- Whether library sharing is enabled.
- Item attributes and channel attributes.
- Security rules.
- Tags or categories if configured.
- Any linked pages or channel-specific settings in the live version.

The source pack does not include a full field-by-field channel edit screen. Agents should open the live channel and record the exact field names before making instructions or migration plans.

### Item lifecycle

Content channel items typically move through draft/pending/approved or similar statuses depending on channel configuration. Official docs say if approvals are enabled and the user has approval rights, the user can set approval status ([Add Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items)). Items also respect dates: start and expire behavior affects whether items appear. For dynamic start/expire scenarios, Rock has a Self Update feature that can show or remove items based on attributes and a job rather than manual date maintenance ([Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items)).

Agents should not assume a missing item is deleted. Check:

- Item exists in channel.
- Status matches block filter.
- Current date is within item dates.
- Channel type date mode supports the expected dates.
- Current user can view the channel and item.
- Block is pointed to the expected channel.
- Lava template is not filtering it out.
- If collection-based, index includes the item.
- If personalized, current visitor matches the required segment/filter.

### Display and Lava

The Content Channel View block is the workhorse listing block. Official docs identify the channel, status, and format/Lava template settings ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)). Custom templates often begin by iterating through `Items`. Use `LinkedPages.DetailPage` or the block’s linked page merge fields only after verifying available merge fields in the deployed version.

Use Lava to:

- Render item titles, summaries, attributes, and images.
- Build detail links.
- Add social metadata.
- Render media player shortcodes.
- Apply conditional logic.
- Log interactions when the block does not naturally load the item.
- Personalize sections with `personalize` or `PersonalizationItems`.

Avoid putting business rules in Lava when they belong in structured fields, segments, request filters, security, or workflows. Lava is powerful, but heavy filtering in templates is difficult for editors to inspect and can become invisible operational debt.

### RSS and feeds

Rock can publish content through `GetChannelFeed.ashx?ChannelId=X` when RSS is enabled for the channel. The endpoint requires `ChannelId`; the default RSS template can be replaced by passing `TemplateId` for a Lava template configured under defined types ([Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds)). Agents troubleshooting feeds should check:

- Channel RSS enablement.
- Correct `ChannelId`.
- Item statuses and dates.
- Template ID and Lava validity.
- Public accessibility and security.
- Absolute URLs for media/images.
- Caching/CDN behavior if used.

### Security

Content channel security includes standard verbs such as view, edit, and administrate, and the content channel area also references `Interact` as a distinct right in official docs ([Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content)). Do not collapse security and personalization into one concept. Security determines permission; personalization determines relevance or prioritization. A hidden personalized item may still be visible to administrators; a secured item should not be exposed just because it matches a segment.

Release notes include a high-severity CMS security fix in v18.2 where blocks interacting with content channels allowed users with only View permissions to delete content items; the delete option is now limited to Edit access ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). For any instance below or near that version, verify patch status before delegating content management to broad groups.

## 9. Asset Manager Deep Dive

The Asset Manager gives Rock first-class integration with files stored on the Rock server or remote/cloud storage providers. Official docs mention Azure and Amazon S3 as examples and describe the Asset field type as a way for editors to select files and images stored in configured cloud accounts ([Intro to The Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager)).

### Asset Manager vs file attributes

Use a **file attribute** when the file belongs to an entity and editors should not care where it is stored. File type configuration handles storage concerns. This fits profile documents, item image uploads, forms, and entity-owned attachments.

Use an **asset attribute** or Asset Manager workflow when editors need to browse and choose existing files from a provider, place files into a managed folder structure, or coordinate with media/design teams that upload assets outside the content item edit screen ([Add Content](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content)).

Use the **HTML editor asset path** when an editor needs to insert an existing asset into rich content. Be careful: inline editor usage can become harder to migrate, resize, personalize, or audit than structured attributes.

### Viewing and managing assets

Official docs place the Asset Manager at `Admin tools > CMS Configuration > Asset Manager`, where users can manage files in configured providers and server folders. The UI supports operations such as adding/deleting folders, viewing a folder tree, uploading, selecting, downloading, renaming, and deleting files ([View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager)).

Source-code snippets for `FileAssetManager` confirm the block is categorized under CMS, is intended to browse and manage server or remote/cloud files, and has configuration for asset provider enablement, file manager enablement, height mode, root folder defaulting to `~/Content`, browse mode, file editor page, zip uploader, and security grant behavior ([FileAssetManager.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/FileAssetManager.cs)). Because source snippets are from the `develop` branch, verify block attributes in the target instance before writing exact admin instructions.

### Storage provider setup

The source pack includes a setup article record for storage providers but not the full hydrated body ([Set Up Storage Provider](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/set-up-storage-provider?Version=v19.0)). Agents should inspect:

- Which providers are configured.
- Provider credentials and scopes.
- Root paths/container/bucket names.
- Whether public or signed URLs are expected.
- Whether CDN rewriting occurs.
- Whether Rock server can read/write/list/delete.
- Security grants and block permissions.
- File type configuration for binary files.

Do not move or delete provider files without confirming whether content items, HTML blocks, structured content, media records, or external pages reference them.

### Image and file performance

Rock’s file type documentation highlights image sizing and performance, including serving images at appropriate dimensions ([Understand File Types](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/understand-file-types)). Agents should prefer structured image attributes plus predictable Lava filters/URLs over ad hoc full-size images in HTML content. Check:

- File type image settings.
- Whether the field stores a binary file, asset reference, URL, or media element.
- Whether templates request thumbnails/resized images.
- Whether images are compressed.
- Whether Open Graph/social images use the correct aspect and public URL.
- Whether CDN and cache layers reflect the latest asset.

### Structured content file behavior

GitHub source snippets show Rock has structured content image and attachment block data classes and renderers under `Rock/Cms/StructuredContent/BlockTypes/`, including `ImageData`, `ImageDataFile`, `ImageRenderer`, `ImageChangeHandler`, and `AttachmentDataFile` ([ImageRenderer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageRenderer.cs), [ImageChangeHandler.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageChangeHandler.cs), [AttachmentDataFile.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/AttachmentDataFile.cs)). One snippet notes that removed structured-content image files are not simply marked temporary for cleanup because copied structured content can share the same binary file reference. Operationally, agents should avoid “cleaning up unused files” based only on one content item edit history; inspect references across templates and copied content.

## 10. Adaptive Messages Deep Dive

Adaptive Messages are for audience-aware message selection when simple personalized Lava blocks become too complex. The official docs introduce them as a way to tailor messages based on person data, view counts, and date ranges, building on personalization segments ([Intro to Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages)).

### When to use adaptive messages

Use adaptive messages when:

- Several segment-specific variants compete for the same placement.
- A viewer may match more than one segment.
- You need a fallback message.
- You need to limit repeated exposure using saturation.
- Date windows matter.
- The message is reused across pages or communications.
- Content authors need a managed configuration surface rather than nested Lava.

Do not use adaptive messages when:

- The content should be permanently secured from a group.
- A simple one-segment conditional in Lava is sufficient.
- The content is a full structured item needing editorial fields, dates, child relationships, or collection indexing.
- The logic belongs in a workflow or communication recipient query.

### Setup model

The setup article places configuration at `Admin Tools > Adaptive Message` and describes adding a base message plus specific adaptations for target segments. It also says no segment is needed for the default group; include a fallback message directly in the adaptive message configuration ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages)).

Saturation is an important operational setting. The source pack states saturation prevents repeatedly showing the same message and can define maximum views and a timeframe in days before a message is considered saturated ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages)). Agents should inspect the live adaptive message edit screen for exact labels and behavior.

### Entity and API landmarks

Source-code snippets confirm:

- `AdaptiveMessageService` exists and inherits `Service<AdaptiveMessage>` ([AdaptiveMessageService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageService.CodeGenerated.cs)).
- REST v1 controller exists at `Rock.Rest/Controllers/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs` ([AdaptiveMessagesController v1](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Controllers/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs)).
- REST v2 model endpoint route prefix is `api/v2/models/adaptivemessages`, with generated get/post/put patterns protected by authentication and unrestricted read/write security actions in the snippet ([AdaptiveMessagesController v2](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs)).
- `AdaptiveMessageAdaptationSegmentService` exists for relationships between adaptations and segments ([AdaptiveMessageAdaptationSegmentService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageAdaptationSegmentService.CodeGenerated.cs)).
- REST v2 route prefix for adaptation segments is `api/v2/models/adaptivemessageadaptationsegments` ([AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs)).
- A migration fixed the adaptive message `CallToAction` attribute key for a specific attribute GUID in the v17.0 migration path ([FixAdaptiveMessagesAttributeKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.0/202501171949509_FixAdaptiveMessagesAttributeKey.cs)).
- Another migration updated an adaptive messages category tree view header ([UpdateAdaptiveMessagesCategoryTreeViewHeader.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.1/202504180307181_UpdateAdaptiveMessagesCategoryTreeViewHeader.cs)).

Because these snippets are generated and from `develop`, agents should use them as landmarks, not as a promise that the deployed instance exposes identical routes or security behavior. Verify REST controllers, API auth, entity fields, and enabled endpoints in the live Rock version.

### Troubleshooting adaptive messages

If an adaptive message displays the wrong variant:

1. Confirm site personalization is enabled if the message depends on personalization behavior.
2. Confirm viewer identity: known person, anonymous visitor, or test account.
3. Confirm the person belongs to the expected personalization segment.
4. Run or inspect `Update Personalization Data`.
5. Confirm request filter conditions, including query string and IP behavior.
6. Check date windows on adaptations.
7. Check saturation counts and timeframes.
8. Check adaptation order/priority in the UI.
9. Check fallback message.
10. Check Lava command or block placement if rendering is via Lava.
11. Check cache.

If the message never displays, also verify that the adaptive message key or identifier used by Lava/block configuration matches the configured message, and inspect server exceptions.

## 11. Personalization And Segments Deep Dive

Rock personalization lets content respond to person data, browsing behavior, and request characteristics. Official docs emphasize showing the right content to the right people, including when a visitor is not logged in ([Intro to Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization)).

### Site-level prerequisites

Personalization is not globally effective just because segments exist. For each site, go to `Admin Tools > Websites` and enable personalization. If browsing behavior or anonymous visitor personalization is expected, enable visitor tracking too ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization)).

Anonymous visitors depend on a browser cookie. The source pack states anonymous visitor tracking uses a cookie, default persistence is 365 days, and the length can be changed under `Admin Tools > System Settings > System Configuration` via `Visitor Cookie Persistence Length` ([Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors)). Agents should verify local privacy/cookie consent requirements and the deployed site’s cookie behavior before recommending anonymous personalization broadly.

### Segment types

Official docs describe segments as filtering content based on something about the person, similar conceptually to a Data View, or based on browsing history ([Intro to Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments)). Examples include baptism status, next-step class completion, page visits, and registration gaps.

Operationally, segment rules depend on data quality. If a segment targets “male” or “female,” a person with unknown gender will not match, as the troubleshooting docs note ([Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization)). Agents should inspect the actual person record and the segment rule before assuming the personalization engine is wrong.

### Request filters

Request filters operate on the visit rather than the known person. Official docs list examples such as IP address ranges and query string parameters. They are configured at `Admin Tools > CMS Configuration > Request Filters`. Each filter has a name and key; the key should avoid spaces and special characters because it is used in Lava and personalization references ([Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters)).

Request filters are useful for:

- Campaign-specific landing-page messages based on query string.
- Internal-network or campus-network notices based on IP.
- A/B or source-specific content when URLs include parameters.
- Temporary operational banners for specific request contexts.

Request filters are not identity or security. Do not use a query string request filter to protect private content.

### Update Personalization Data job

The `Update Personalization Data` job keeps people returned by personalization segments current. Official docs state it adds or removes people from lists based on current segment conditions and updates `PersonAliasPersonalization` ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)). If a known person is not matching a segment:

- Check the segment’s current membership from the Personalization Segments page.
- Check the job’s last run, status, and exception messages.
- Check whether the underlying person data changed after the last run.
- Check whether the segment is active.
- Check whether the segment rule depends on browsing behavior that requires visitor tracking.
- Check whether the person has the expected person alias.

### Personalizing content channel items

Official docs say content channel item personalization is enabled at the content channel level under `Admin Tools > CMS Configuration > Content Channels` by checking `Enable Personalization`. Once enabled, items can be assigned personalization segments and request filters. Rock can show, hide, or prioritize items based on matching conditions ([Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items)).

When troubleshooting personalized content items, agents should check both the channel and the item. An item with segments assigned may do nothing if the channel itself has not enabled personalization, and a personalized channel may still show generic content if the item has no segment/filter assignment or fallback behavior.

### Personalizing with Lava

Official docs describe two Lava approaches: the `Personalize` command and the `PersonalizationItems` approach. The `Personalize` command can show content based on a segment key or request filter key and can be used in emails as well as blocks ([Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava)). Use Lava personalization when:

- The content is a small conditional section.
- The condition needs to live inside an HTML Content block or communication.
- The content is not a full content channel item.
- The rule is simple and auditable.

Use channel-level personalization or adaptive messages when:

- There are multiple competing items.
- Editors need to manage variants.
- Saturation or ordering matters.
- The personalized content should be part of a reusable publishing workflow.

## 12. Related Rock Areas: Cms, Lava, Security, Communications, Media, Workflows, People

### CMS

Content lives inside the broader CMS system: sites, pages, blocks, layouts, routes, themes, HTML Content blocks, content channel blocks, content collection blocks, and content components. A content problem may be caused by page routing or block placement rather than the content item itself. The source pack’s navigation shows the content management docs live under Digital Publishing alongside Websites, Website Fundamentals, Manage Pages, Sites, Landing Pages, HTML Content Block, Block Context, and Web Design Frameworks ([Content Management](https://community.rockrms.com/documentation/digital-publishing/content-management)).

### Lava

Lava is the display and glue layer. It renders channel lists, detail pages, feed templates, content components, social metadata, personalization, media players, and interactions. The official Content Channel View docs explicitly point to Lava format templates and iteration over items ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)). Content component template docs recommend using `{{ 'Lava' | Debug }}` in the Display Lava field to inspect available properties and attributes during template development ([Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates)).

Use Lava carefully in production. Do not leave debug output visible. Avoid direct SQL Lava in public pages unless reviewed for performance and security. Prefer structured attributes over parsing HTML.

### Security

Security governs access. Personalization governs relevance. Content channels have security verbs, including special content interactions; page/block security still applies; release notes include security fixes around content channel delete behavior ([Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Always test as:

- Anonymous visitor.
- Authenticated normal person.
- Target segment person.
- Editor.
- Approver.
- Administrator.

### Communications

The docs say personalization Lava can be used in communications, including email ([Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava)). This means content and personalization logic can cross from CMS into outbound messaging. Agents should verify whether the merge context in communications includes the same person, site, request, or visitor data expected by a page. A request filter based on URL query string may not make sense in an email render context.

### Media

Digital media can automatically create content channel items when a media element is added to a folder, and publishing media through content channel items requires an item attribute of type `Media Element` ([Intro to Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media), [Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media)). Source snippets also show content channel item list view models that request and return linked media elements ([GetLinkedMediaElementsRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsRequestBag.cs), [GetLinkedMediaElementsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsResponseBag.cs), [LinkedMediaElementBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/LinkedMediaElementBag.cs)). Verify in the live instance whether linked media features are available on the target block/version.

### Workflows

Digital media docs include media use in workflows, and self-update content channel items use job-driven changes ([Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media), [Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items)). Workflows may create content, approve content, update attributes, notify editors, or publish media. Agents should inspect workflow triggers and history when content changes unexpectedly.

### People

Personalization depends heavily on people data. Person attributes, data views, demographic fields, connection statuses, group membership, registrations, interactions, and browsing history may all feed segments. When a user says “this person should match,” inspect the actual person record, aliases, segment membership, and the update job before changing the segment.

## 13. Administration And Operational Guardrails

Use these guardrails before making changes.

### Public content safety

For a public knowledge base or public site, do not publish private implementation notes, local paths, credentials, raw transcripts, private SQL, evidence screenshots with sensitive data, or staff-only operational context. Keep public content contributor-focused and review generated content before launch.

### Change management

Before changing a content channel, component template, adaptive message, request filter, or personalization segment:

- Record the current configuration.
- Identify pages/blocks using it.
- Identify content items affected.
- Identify whether the change is public-facing.
- Check whether the change affects anonymous visitors.
- Check whether caching or jobs must be refreshed.
- Test with representative users.
- Avoid direct SQL writes unless explicitly approved and rollback is prepared.

### Security review

For channel management access:

- Confirm who can view channels in `Tools > Content`.
- Confirm who can edit items.
- Confirm who can approve items.
- Confirm delete access is limited appropriately, especially on versions affected by content channel security release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Confirm public channels do not expose private attributes through Lava debug or JSON APIs.
- Confirm RSS feeds do not publish private content.
- Confirm asset URLs are not exposing private files.

### Job monitoring

Monitor:

- `Update Personalization Data`: keeps segment membership current ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)).
- `Index Content Collections`: refreshes collection search indexes; official troubleshooting says it runs overnight by default, but verify schedule in the live instance ([Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections)).
- Media sync/import jobs if media content items are created from provider uploads.
- Any workflow or self-update jobs affecting channel item dates/statuses ([Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items)).

### Cache and indexing

A correct configuration may not appear immediately if:

- Block output is cached.
- Content component item cache duration is set; the configure docs mention an item cache duration setting ([Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components)).
- Collection index has not run.
- Browser cache/CDN cache holds old assets.
- Personalization membership has not refreshed.
- Visitor cookie state differs between test sessions.

### Editorial quality

Prefer structured fields over raw HTML for repeatable content. A vendor article from Triumph describes operational problems caused by HTML-based content channel items and argues for structured content to reduce inconsistent formatting and copy/paste errors ([From Chaos to Clarity](https://www.triumph.tech/resources/structured-content-rock-upgrade)). Treat that as implementation strategy rather than product specification, but the principle aligns with Rock’s structured content model.

## 14. Developer, API, Lava, And Source-Code Landmarks

### REST and model landmarks

The source pack includes generated controllers and services for adaptive messages. These are useful for developers and agents working with APIs:

- REST v2 adaptive messages route prefix: `api/v2/models/adaptivemessages` in the generated controller snippet ([AdaptiveMessagesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs)).
- REST v2 adaptive message adaptation segments route prefix: `api/v2/models/adaptivemessageadaptationsegments` ([AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs)).
- REST v1 adaptive message controller exists under `Rock.Rest/Controllers/CodeGenerated` ([AdaptiveMessagesController v1](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Controllers/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs)).
- Service classes exist for `AdaptiveMessage` and `AdaptiveMessageAdaptationSegment` ([AdaptiveMessageService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageService.CodeGenerated.cs), [AdaptiveMessageAdaptationSegmentService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageAdaptationSegmentService.CodeGenerated.cs)).

Generated source indicates unrestricted read/write security actions on some endpoints, but agents must verify API security and enabled endpoints on the actual deployed Rock version. Never expose admin API instructions publicly without reviewing security.

### Content Channel Item Personal List Lava block

Source snippets show a Web Forms block named `Content Channel Item Personal List Lava` that displays content items for the current person using Lava. It has block attributes for content channel, max items, detail page, and Lava template. Its query filters items created by the current person and can optionally filter by channel ([ContentChannelItemPersonalListLava.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs)). This is a useful landmark when troubleshooting “my submitted content” surfaces, but verify whether the block is present and used in the target version/site.

### File Asset Manager block

`FileAssetManager` is an Obsidian block categorized under CMS for browsing/managing files. The snippet identifies block-level settings such as file manager and asset provider enablement, root folder, browse mode, file editor page, zip uploader, and security grant token ([FileAssetManager.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/FileAssetManager.cs)). Use it as a source-code landmark for Asset Manager behavior.

### Structured content block types

Structured content source snippets show block types for images and attachments. `ImageRenderer` renders from either file URL or URL; `ImageChangeHandler` tracks new and old binary file IDs and contains a caution about copied structured content sharing file references ([ImageRenderer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageRenderer.cs), [ImageChangeHandler.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageChangeHandler.cs)). This is important for agents doing cleanup or migration work.

### Lava interaction logging

The `interactioncontentchannelitemwrite` Lava command logs an interaction for a specified content channel item. The docs list parameters including `contentchannelitemid`, `operation`, `summary`, `personaliasid`, and campaign fields such as source/medium/content/term in later versions ([Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)). Operational cautions:

- `contentchannelitemid` is required.
- Default operation is `View`.
- Operation length is limited; docs state longer values are truncated.
- Summary defaults to current page title if blank and has a length limit.
- Person alias can default to the current person.
- Release notes include a fix for misclassified entity type logging; verify version before relying on interaction analytics ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 15. Reporting, Analytics, And Model Map

Content reporting usually depends on interactions, attributes, statuses, dates, and indexes.

### Content item reporting

Useful questions:

- How many items exist by channel and status?
- Which items are pending approval?
- Which items are expiring soon?
- Which items lack required structured attributes?
- Which items have no image or invalid asset reference?
- Which items are personalized and to which segments?
- Which items are orphaned from expected parent/child relationships?
- Which items are included in collections?
- Which items have RSS enabled through their channel?

Use live Rock reporting tools, Data Views, SQL read-only checks, or model map references. The provided source pack does not include a full model map for content channels, so field-level reporting should be verified in the live schema.

### Content collection analytics

Content collections support search and trending. Official docs say trending uses interactions in the collection’s trending window: Rock counts views/interactions in the specified window and factors item age up to the window ([Trending Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/trending-content)). If trending looks wrong:

- Verify interactions are being logged.
- Verify the item is in the collection index.
- Verify the trending window.
- Verify item age and publish date.
- Verify the version is not affected by interaction logging bugs.
- Verify bots or internal users are not skewing interactions.

### Media analytics

Digital media docs say Rock can access data about plays, engagement, and effectiveness and can create content channel items from provider uploads ([Intro to Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media)). For reporting, distinguish:

- Content item view interactions.
- Media play interactions.
- Media watch percentage/engagement.
- Page visits.
- Campaign UTM fields.
- Person-known vs anonymous interactions.

### Personalization reporting

For segment reporting:

- Inspect current segment membership from the Personalization Segments page.
- Inspect `PersonAliasPersonalization` if using database/model checks ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)).
- Compare membership after running `Update Personalization Data`.
- Check anonymous visitor behavior separately because cookie-based visitor state is not the same as person alias membership.

For adaptive message reporting, the source pack does not include the full reporting model. Inspect the live entity/model map and interaction records for how adaptive message views are stored in the deployed version.

## 16. Version And Release Caveats

Version caveats matter in this area because content rendering, Lava fields, security, interactions, indexing, and adaptive message setup have all changed over time.

Known caveats from the source pack:

- **Content channel delete security**: Release notes include a v18.2 CMS security fix where multiple content-channel-related blocks allowed users with only View permissions to delete content items. The delete option is now limited to users with Edit access ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **Interaction logging entity type**: Release notes include a fix for Content Channel Item View and `InteractionContentChannelItemWrite` logging interactions using the Content Channel entity type instead of Content Channel Item. Verify the exact fixed version on the release notes page for the deployed branch before comparing interaction history ([Rock Core Release Notes](https://www.rockrms.com/releasenotes), [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)).
- **Content collection indexing and large attributes**: Release notes mention a fix for indexing exceptions when a content channel item had an attribute value larger than Lucene’s maximum field size, even if that attribute was not selected for indexing ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **Content channel type attribute deletion**: Release notes mention a fix for deleting Content Channel Type attributes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **Content channel item Lava fields**: Release notes mention `PrimarySlug` and `ItemGlobalKey` being added to Lava fields. Verify availability before using slug templates in older Rock versions ([Rock Core Release Notes](https://www.rockrms.com/releasenotes), [Content Channels With Slugs](https://community.rockrms.com/recipes/128)).
- **Adaptive message attribute key migration**: Source snippets show a v17.0 migration that changed an adaptive message attribute key to `CallToAction` for a specific GUID ([FixAdaptiveMessagesAttributeKey.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%20117.0/202501171949509_FixAdaptiveMessagesAttributeKey.cs)). If the link path differs in GitHub because of URL escaping or branch layout, search the repository for `FixAdaptiveMessagesAttributeKey`.
- **Adaptive message category header migration**: Source snippets show a v17.1 migration updating a category tree view header to `Adaptive Messages` ([UpdateAdaptiveMessagesCategoryTreeViewHeader.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.1/202504180307181_UpdateAdaptiveMessagesCategoryTreeViewHeader.cs)).
- **Release timeline**: The hydrated release page includes Rock v19.1 released June 11, 2026 and v18.3 beta released June 9, 2026. Always verify current release status before planning upgrades or documentation for a live organization ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agents should not assume the source pack’s `develop` branch source snippets match a production Rock instance. Confirm the deployed version, applied migrations, plugin overrides, and whether the block is Web Forms or Obsidian.

## 17. Implementation Playbooks

### Playbook: Build a ministry resource library

1. Define resource types: articles, sermon clips, downloadable PDFs, videos, devotionals, or external links.
2. Decide whether one content channel type can serve all resources or whether separate channels should be aggregated through a content collection.
3. Add item attributes: resource type, topic, audience, ministry, campus, hero image, summary, media element, downloadable asset, call-to-action URL, author/speaker, and publish date.
4. Create content channels under `Admin Tools > CMS Configuration > Content Channels`.
5. Use `Tools > Content` for editor entry and approval.
6. Create a content collection under `Admin Tools > CMS Configuration > Content Collections` if multiple channels/calendars need unified search ([Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections)).
7. Add Content Collection View block to the public page ([Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view)).
8. Enable attribute filters for the fields users should filter by.
9. Run/verify `Index Content Collections`.
10. Verify search, filters, trending, mobile layout, anonymous access, and performance.

### Playbook: Convert HTML-heavy channel items to structured content

1. Inventory fields currently embedded in HTML: headings, images, buttons, dates, speaker, summary, categories, and links.
2. Create structured item attributes for each reusable field.
3. Build or revise Lava templates to render structured attributes consistently.
4. Migrate a small sample manually.
5. Validate output visually and through source inspection.
6. Migrate the rest using a scripted or manual process only after backup and review.
7. Keep old HTML content available until output parity is confirmed.
8. Train editors to use fields rather than paste formatted HTML.

This aligns with the operational argument that structured content reduces formatting inconsistency and editor fragility ([From Chaos to Clarity](https://www.triumph.tech/resources/structured-content-rock-upgrade)).

### Playbook: Add personalized homepage promos

1. Enable site personalization and visitor tracking under `Admin Tools > Websites` ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization)).
2. Create segments for known audiences.
3. Create request filters for campaign URLs or network-specific variants.
4. Run `Update Personalization Data`.
5. Enable personalization on the homepage promo content channel ([Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items)).
6. Assign segments/request filters to promo items.
7. Configure ordering or prioritization in the display block.
8. Test as matching person, non-matching person, anonymous visitor, and campaign URL visitor.
9. Document fallback behavior.

### Playbook: Use adaptive messages for giving campaign variants

1. Create personalization segments for the major audiences.
2. Do not create a segment for the fallback audience; use the default/fallback message ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages)).
3. Create the adaptive message under `Admin Tools > Adaptive Message`.
4. Add adaptations and associate segments.
5. Configure saturation to prevent overexposure.
6. Add date windows if campaign timing matters.
7. Render the adaptive message through the appropriate block/Lava path.
8. Test overlap cases where one person matches multiple segments.
9. Test saturation by repeated views or inspect interaction/message history if available.
10. Monitor performance and user feedback.

### Playbook: Publish sermon media through content channel items

1. Configure media account/provider and folder.
2. Configure automatic content item creation if desired ([Intro to Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media)).
3. Ensure the content channel has an item attribute of type `Media Element` ([Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media)).
4. Use a Lava template that renders media via Rock’s media player shortcode or approved block.
5. Verify linked media elements in the item list if the deployed block supports that surface ([LinkedMediaElementBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/LinkedMediaElementBag.cs)).
6. Verify content item status/dates after media sync.
7. Verify media analytics and content interactions separately.

### Playbook: Configure RSS feed for a content channel

1. Enable RSS on the content channel.
2. Confirm public items have approved/published status and valid dates.
3. Test `https://yourserver/GetChannelFeed.ashx?ChannelId=X`.
4. If a custom feed format is needed, create a Lava template under `Admin Tools > General Settings > Defined Types > Lava Templates`.
5. Add `TemplateId=Y` to the feed query string ([Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds)).
6. Validate XML/feed output.
7. Confirm images/media URLs are absolute and publicly reachable.
8. Monitor caching.

## 18. Troubleshooting Decision Tree

### Content item is missing from a page

1. Is the block on the expected page and zone?
2. Is the block pointed at the expected channel?
3. Does the block filter by status, date, tags, campus, or attributes?
4. Does the item exist in the channel?
5. Is the item status included by the block?
6. Is the current date within the item start/expire window?
7. Does the current user have view access to the channel/item?
8. Does the Lava template iterate over `Items` and render the item?
9. Does the template require an attribute that is empty?
10. Is personalization enabled and filtering the item?
11. If collection-based, has `Index Content Collections` run?
12. Is block/page output cached?

### Personalized content is wrong

1. Is personalization enabled for the site?
2. Is visitor tracking enabled if browsing/anonymous behavior is required?
3. Is the person logged in or anonymous?
4. Does the known person actually satisfy segment criteria?
5. Is the segment active?
6. Has `Update Personalization Data` run since data changed?
7. Is the request filter active and keyed correctly?
8. Does the URL/IP/query string match the request filter?
9. Is channel-level personalization enabled?
10. Are the item’s segment/filter assignments correct?
11. Is Lava using the correct segment/filter key?
12. Are cache or saturation settings affecting output?

Official troubleshooting emphasizes checking the person, site personalization enablement, and active segments/filters ([Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization)).

### Content collection search is stale or empty

1. Is the collection configured with the expected channels/calendars?
2. Are the source items approved and in date?
3. Is the Content Collection View block pointed to the expected collection?
4. Has `Index Content Collections` run?
5. Did the job fail?
6. Are selected indexed attributes too large or misconfigured?
7. Is personalization enabled at site level if personalized collection results are expected?
8. Are attribute filters configured and not excluding everything?
9. Are interactions available if trending is expected?

Official troubleshooting specifically points to site personalization for personalized collection behavior and the index job for stale results ([Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections)).

### Asset image does not display

1. Is the field a file attribute, asset attribute, inline HTML asset, media element, or structured content image?
2. Does the referenced file exist?
3. Is the storage provider accessible from Rock?
4. Is the URL public or signed as expected?
5. Does file type security allow access?
6. Is the image being resized or transformed by a Lava filter/file endpoint?
7. Is the URL absolute where required, such as RSS/social sharing?
8. Is browser/CDN cache stale?
9. Was the file deleted or renamed in Asset Manager?
10. Is the content copied from a template that shares a binary file reference?

### Adaptive message does not behave

1. Does the adaptive message exist and is it active?
2. Is the render path using the correct key/id?
3. Do adaptations have segment assignments?
4. Does the viewer match the expected segment?
5. Is fallback configured?
6. Are date windows valid?
7. Has saturation been reached?
8. Has personalization data updated?
9. Are request filters active and matching?
10. Does the deployed version include the expected adaptive message fields/migrations?

## 19. Agent Task Recipes

### Recipe: Audit a content channel before editing

Collect:

- Channel name, ID/GUID, type, and purpose.
- Channel item count by status.
- Item attributes and required fields.
- Channel attributes.
- Personalization enabled state.
- RSS enabled state.
- Content Library enabled state.
- Security rules for view/edit/approve/delete/admin.
- Blocks/pages that render it.
- Collection memberships.
- Jobs/workflows that update it.
- Recent release caveats relevant to the deployed version.

Do not change anything until you know which pages and workflows depend on the channel.

### Recipe: Diagnose “editor cannot see channel in Tools > Content”

Check:

- Does the channel exist?
- Does the editor have View access to the channel?
- Is the channel hidden by any filter/toggle in `Tools > Content`?
- Is the editor expecting pending-only view?
- Does the editor need Edit or Approval rights for the action?
- Is there a security inheritance issue?
- Is the instance on a version affected by content channel block permission bugs?

The `Tools > Content` page lists channels the current user has View access to, according to official docs ([Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items)).

### Recipe: Diagnose “segment should include this person”

Check:

- Person record demographics and attributes.
- Group/registration/connection data used by the segment.
- Whether the segment is person-data based or browsing-history based.
- Visitor tracking if browsing history is involved.
- Segment active state.
- `Update Personalization Data` last run.
- Current membership list from the Personalization Segments page.
- `PersonAliasPersonalization` only if safe and appropriate to inspect.

### Recipe: Create safe Lava for channel display

Use a pattern like this conceptually, adapting to live merge fields:

```liquid
{% for item in Items %}
  <article>
    <h2>{{ item.Title }}</h2>
    {% if item.Summary != empty %}
      <p>{{ item.Summary }}</p>
    {% endif %}
  </article>
{% endfor %}
```

Before using item properties such as `PrimarySlug`, `ItemGlobalKey`, custom attributes, linked media elements, or linked pages, verify they exist in the target Rock version and block merge context. Use debug only in a non-public review context ([Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Recipe: Verify content interactions

Check:

- Is the item rendered by a block that logs views?
- Is a Lava command logging interactions manually?
- Does the command specify `contentchannelitemid`?
- Are operation and summary within documented limits?
- Is the current person/person alias resolved?
- Is the Rock version patched for content channel item entity type logging?
- Are interactions visible in `Tools > Interactions`?

Use the Lava command docs and release notes together ([Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Recipe: Public launch review for content personalization

Before launch:

- Disable any Lava debug output.
- Verify anonymous experience.
- Verify logged-in target experiences.
- Verify non-target experience.
- Verify fallback content.
- Verify assets load without authenticated sessions.
- Verify RSS/social metadata if used.
- Verify no private content appears in feed, page source, API output, or image URLs.
- Verify content item delete/edit permissions.
- Verify jobs have run.
- Verify release notes for known content/personalization bugs.
- Verify public repo/site hardening if publishing generated docs.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

Primary official documentation used:

- [Content Management](https://community.rockrms.com/documentation/digital-publishing/content-management): Top-level map for content channels, collections, dynamic content, components, library, media, social networks, asset manager, and directory/file structure.
- [Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels): Primary channel guide index.
- [Intro to Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels): Core type/channel/item model.
- [Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/channel-types): Channel type strategy.
- [Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels): Channel setup.
- [Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item): Item creation.
- [Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block): Listing/rendering block.
- [Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content): Content channel security.
- [Add Content Channel Child Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-content-channel-child-items): Parent/child relationships.
- [Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items): Job-driven item visibility updates.
- [Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds): RSS endpoint and Lava feed templates.
- [Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections), [Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view), [Trending Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/trending-content), [Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections): Collection aggregation, search, indexing, and trending.
- [Content Component](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component), [Intro to Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components), [Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates), [Add Content Component Item Attributes](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes), [Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components): Component templates, attributes, cache, and configuration.
- [Asset Manager System](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system), [Intro to The Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager), [View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager), [Add Content](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content): Asset storage and usage.
- [Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media), [Intro to Digital Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/intro-to-digital-media), [Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media), [Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items): Media publishing through content items.
- [Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization), [Intro to Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization), [Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments), [Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization), [Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors), [Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters), [Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items), [Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava), [Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job), [Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization): Personalization configuration and troubleshooting.
- [Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages), [Intro to Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages), [Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages): Adaptive message behavior and setup.

Training and community examples:

- [RockU Content Channel Types and Content Channels](https://community.rockrms.com/rocku/content-channels/content-channel-types-and-content-channels): Training index metadata for content channels, content components, asset manager, media, and content library.
- [Content Channels With Slugs](https://community.rockrms.com/recipes/128): Community recipe for slug-based listing/detail routing. Use carefully; it is not core-reviewed.
- [From Chaos to Clarity](https://www.triumph.tech/resources/structured-content-rock-upgrade): Vendor perspective on moving from HTML-heavy items to structured content.

Developer/source landmarks:

- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock): Source repository.
- [FileAssetManager.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/FileAssetManager.cs): Asset manager block landmark.
- [AdaptiveMessagesController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs): REST v2 adaptive messages route.
- [AdaptiveMessageService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/AdaptiveMessageService.CodeGenerated.cs): Adaptive message service.
- [AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessageAdaptationSegmentsController.CodeGenerated.cs): REST v2 adaptation segment route.
- [ContentChannelItemPersonalListLava.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs): Personal content item list block.
- [ImageRenderer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageRenderer.cs) and [ImageChangeHandler.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageChangeHandler.cs): Structured content image behavior.
- [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write): Lava interaction logging command.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): Version caveats, security fixes, and content/personalization behavior changes.

Dependency notes:

- Content channels depend on CMS pages/blocks and Lava for display.
- Content collection search depends on indexing.
- Trending depends on interactions and the collection trending window.
- Media publishing depends on media account/provider configuration and a `Media Element` item attribute.
- Personalization depends on site enablement, visitor tracking, active segments/request filters, and the update job.
- Anonymous personalization depends on visitor cookies and privacy/browser behavior.
- Adaptive messages depend on personalization conditions, fallback configuration, date windows, and saturation.
- Asset rendering depends on provider configuration, file type security, public URL behavior, and caching.
- API behavior depends on deployed Rock version, security configuration, and whether REST v1/v2 endpoints are enabled.
