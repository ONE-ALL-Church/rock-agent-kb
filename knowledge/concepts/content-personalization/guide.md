---
id: authored-content-personalization
title: Content And Personalization
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "1d9f3b587ae2c8d2ed56a01db8d0626cf74067bb28bf84d97a23c1661892a205"
---

# Content And Personalization

## Agent Summary

Rock’s content system separates structure, entries, presentation, assets, audience selection, and publishing:

- Content Channel Types define the fields and behavior available to channels and items.
- Content Channels apply a type to a publishing purpose.
- Content Channel Items hold individual entries.
- Content Components give editors structured controls while designers retain control of markup and Lava.
- Content Collections search across multiple channels and calendars.
- The Content Library exchanges selected content between Rock organizations.
- Asset Manager and File Manager address different file-management workflows.
- Personalization Segments, Request Filters, Adaptive Messages, and Lava select or prioritize content for a person or visit.
- Localization settings adjust distinct display and entry conventions; a display setting does not necessarily change processing behavior.

Begin any investigation by identifying the exact channel, page, block, site, content item, and Rock version. Then separate four questions:

1. Is the content structurally valid?
2. Is it approved, in date, and permitted?
3. Does the rendering block select and process it correctly?
4. Are personalization, caching, indexing, provider, or localization settings changing the outcome?

The current supplied documentation is primarily Rock 19.0 documentation. Version-scoped behavior is identified where the evidence explicitly limits it. ([Intro to Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels), [Intro to Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization))

## Scope And Boundaries

This guide covers structured website content, content channels and components, content collections, Content Library workflows, assets and files, media-linked content, social metadata, personalization, Adaptive Messages, and localization.

It does not replace the owning guides for:

- Page architecture and block placement: see the CMS concept.
- Lava syntax, security enablement, and execution behavior: see the Lava concept.
- Entity and page authorization design: see the Security concept.
- Communication delivery: see the Communications concept.
- Media provider administration and encoding: see the Media concept.
- Workflow design beyond media-watching requirements: see the Workflows concept.
- Person records, aliases, and data-view design: see the People concept.

Treat Content Library material as externally sourced content subject to its assigned license. Treat community recipes as unreviewed examples, not as official behavior. No live Rock instance was inspected for this guide. ([Set Up The Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library), [Intro to Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization))

## Mental Model

The core hierarchy is:

```text
Content Channel Type
└── Content Channel
    └── Content Channel Item
        ├── fields and item attributes
        ├── optional child items
        ├── dates, status, and permissions
        └── optional personalization assignments
```

A Content Channel Type defines the available channel attributes and item attributes. A Content Channel instantiates that structure for a particular publishing purpose, and Content Channel Items are the individual entries. Channel attributes hold shared channel-level information; item attributes hold values that vary by entry. ([Intro to Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels), [Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/channel-types))

Presentation is a separate layer. A Content Channel View or Content Channel Item View block selects content and renders it through Lava. Content Components similarly separate editor-supplied values from designer-controlled output. Collections add a search index across sources. Personalization adds matching inputs that a rendering surface may ignore, prioritize, filter, or boost. ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block), [Intro to Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components), [Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections))

Do not collapse visibility, personalization, and security into one concept:

- Dates and approval status control publication eligibility.
- Personalization controls relevance or conditional display.
- Security controls authorization.
- Collection indexing does not enforce each indexed item’s individual security.
- Output caching can bypass per-request personalization by serving previously rendered output.

## Content Channels

### Choose the structure

Use a reusable Content Channel Type when several channels need the same structure. The type can define channel attributes, item attributes, date behavior, and whether concepts such as priority, content, or approval status apply. Date behavior can be a single date, a date range, or no dates. ([Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/channel-types))

Universal Channel Types are attribute-free starting points for one-off channels. Each channel supplies its own required item attributes. The available universal types differ by their date fields, including an option with no dates. ([Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types))

A channel can use an HTML editor, code editor, or structured-content configuration as supplied by its setup. The Rock 19.0 documentation says that enabling structured content affects newly created items while existing HTML items remain HTML. Therefore, enabling the setting is not evidence that historical entries were converted. ([Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels))

### Configure publication behavior

A Content Channel can require approvals, enable personalization, permit manual ordering, define allowed child channels, enable RSS, and expose inherited or channel-specific item attributes. Personalization fields on items are available only when personalization is enabled on the channel. ([Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels))

A Content Channel Item is displayed no earlier than its Start date. An optional Expire date can remove it from display automatically. The available date controls come from the channel type. ([Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item), [Add Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items))

Where approvals are enabled, only a user with Approval permission can set the approval status. To authorize a role, grant `Approve` on the `Rock.Model.ContentChannelType` entity through Entity Administration. That permission is distinct from ordinary View or Edit access. ([Add Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items), [Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content))

### Manage editorial work

`Tools > Content` shows staff the channels for which they have View permission. It displays a pending-item count for each channel and can limit the channel list to channels with pending items. Inside a channel, items can be filtered by status, date range, or title. ([Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items))

Use the administrative channel screen to change channel structure or settings. Use `Tools > Content` for routine item entry, review, and approval. If an editor cannot see a channel, inspect View permission before diagnosing item filters.

Rock 19.3 fixed a Content Channel Item List issue in which add and delete controls required Edit access on the Content Channel Item entity instead of honoring Edit access on the channel. Include the installed patch version when investigating that historical symptom. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### Relate items

A channel item can use items from other channels as children. An editor can link an existing item or create a new one during the same workflow. A child can belong to multiple parents and may have children of its own. ([Add Content Channel Child Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-content-channel-child-items))

Treat these links as relationships, not ownership assumptions. Before changing or deleting a child, inspect every parent and downstream presentation that may reuse it.

### Render channels and items

The Content Channel View block selects a channel, status, format, filters, order, personalization behavior, and other presentation options. Its Lava template iterates through selected items. A Content Channel Item View block renders a single item and can be restricted to a channel. ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block))

If an item’s Content field contains Lava, the Content Channel Item View block must process it explicitly, for example with:

```liquid
{{ Item.Content | RunLava }}
```

Storing Lava in the item does not by itself prove that a block will execute it. ([Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item))

Do not enable output caching when channel output contains visitor-specific values. A cached response can expose one visitor’s personalized content to another. Also provide fallback behavior for contextual Lava used in RSS, because current-person and other page-request values may not be available in a feed-rendering context. ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block))

### Publish an RSS feed

`GetChannelFeed.ashx` publishes the channel identified by the required `ChannelId` query parameter when RSS is enabled for that channel. The feed uses the default RSS Lava template unless `TemplateId` selects another value from Lava Templates. `Count` defaults to 10 and limits the returned items; `EnableDebug` exposes the merge fields available to the template. ([Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds))

Validate the feed independently from the website page. A page may have current-person, route, or block context that the feed does not.

### Secure content

Content Channel Items support an Interact permission. This permits a design in which visitors can see that an item exists while only authorized people can access its complete content. The rendering implementation must honor that distinction. ([Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content))

Do not infer authorization from personalization. A segment match, request-filter match, or personalized ranking is not a security grant.

### Automate item attributes

The Content Channel Item Self Update job evaluates Lava stored in one item attribute and writes its result into another. The output must be valid for the target attribute’s field type. Configure a separate job for each channel, with Template Key pointing to the Lava attribute and Target Key pointing to the attribute to update. ([Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items))

A changed default value on the Lava attribute does not establish that existing items received the new Lava. Inspect the actual value on an affected item when results differ between old and new entries.

## Content Components

Content Components let a designer own markup and Lava while editors change structured values. This reduces the need for editors to modify fragile HTML. Rock implements each component with an associated content channel behind the editing experience. ([Intro to Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components))

A Content Component block can permit multiple items, select a component template, expose presentation settings, and filter displayed content by Content Channel Item fields or attributes. Item caching reduces repeated retrieval, while output caching stores rendered output. Avoid output caching for personalized content because the rendered response may contain values intended for another visitor. ([Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components))

In Rock 19.0, administrators can create templates under `Admin Tools > CMS Configuration > Content Component Templates`. Display Lava can access the component’s related content items and configuration settings. During controlled development, `{{ 'Lava' | Debug }}` in Display Lava exposes the available context; remove diagnostic output before publishing. ([Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates))

To scope a Content Component item attribute to particular templates, create Content Channel Item attribute categories whose names exactly match the target templates, then assign the attribute to those categories. Selecting multiple categories reuses one attribute across several templates. Leaving Categories empty exposes the attribute to all Content Component templates. ([Add Content Component Item Attributes](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes))

## Content Collections

A Content Collection can combine any number of content channels and calendars so their content is searchable together. A source can participate in more than one collection without changing the source’s existing structure. ([Intro to Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections), [Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections))

In Rock 19.0, Content Collections depend on Universal Search and require an active Universal Search index component. Collection and item changes are indexed automatically by the overnight `Index Content Collections` job; run the job or rebuild the index manually when same-day changes must appear sooner. ([Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections))

Collection configuration and the Content Collection View block are separate layers. Sources and indexed attributes belong to the collection. Visible search filters and presentation behavior also depend on block settings. A filter activated on the collection must also be active in the block before visitors can use it. ([Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections), [Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections))

Collections can evaluate segments, request filters, or both. The Content Collection View block can boost matching Content Channel Items by a configured amount rather than simply hiding nonmatches. ([Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections), [Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view))

Trending ranking uses interactions during the configured Trending Window divided by item age in days, with the age divisor capped at the window length. Trending Gravity changes how strongly the result favors newer items. The views needed for this feature depend on interaction logging by the item-viewing surface. ([Trending Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/trending-content), [Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections))

Critical security boundary: collections index, store, and display items without enforcing each indexed item’s individual security. Do not place restricted content in a visitor-facing collection unless the collection and presentation design prevent its exposure independently. ([Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view))

## Content Library

A church can selectively publish content to the Content Library, where it is stored in a Spark-hosted cloud environment and can be downloaded into another church’s Rock instance. ([Intro to the Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/intro-to-the-content-library))

Content Library functionality is enabled per Content Channel and applies to all items in that channel. Uploading a particular item requires both an Experience Level and a Topic. The channel’s configured license governs new uploads; changing that license does not alter the license already assigned to previously uploaded items. ([Set Up The Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library))

Open the Library Viewer from the destination channel’s **Download from Library** action so Rock knows which channel should receive the content. The first download creates a new item. Downloading the same library content again refreshes the existing item and overwrites local changes made after the prior download. ([Library Viewer](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/library-viewer))

Before refreshing downloaded content, identify local edits and confirm that overwriting them is intended. Treat the assigned license as part of the item’s operational state, not as decorative metadata.

## Digital Media In Content Operations

Each external media source requires a Media Account and its provider plugin. Rock’s built-in Local Media Account instead requires folders, media elements, and metadata to be maintained manually. ([Configure Media Accounts](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/configure-media-accounts))

Rock can create a Content Channel Item automatically when a media element is added to a synchronized Media Folder. The destination channel must have a Media Element item attribute in which Rock can store the association. Media can also be linked manually through the same attribute type. ([Configure Media Accounts](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/configure-media-accounts), [Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media))

To retain Rock Media watch interactions and analytics when rendering a Media Element stored on a Content Channel Item, read the attribute’s raw value and pass the resulting GUID to the Media Player shortcode’s `media` parameter. Passing a file URL through `src` embeds that file but is not the documented Media Element integration pattern for those interactions. ([Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items))

The Media Player shortcode can also embed YouTube or Rock Media file URLs through `src`. When a Media Element has HLS, HD, SD, or other generated files, copy the desired file URL from the element’s Media Files page. ([Media Player Lava Shortcode](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/media-player-lava-shortcode))

Rock Media can preserve playback progress between mobile and web. Shortcode settings determine whether viewing sessions are combined or reported separately. `autoresumeindays` and `combineplaystatisticsindays` default to seven days. If both are set to 14, a return after more than 14 days begins at the start and records a new Individual Play. ([Use Media Analytics](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-media-analytics), [Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items))

Media analytics include aggregate engagement, rewatches, play counts, cumulative viewing time, and daily plays. Individual records can report the viewer, viewing time, portions watched or repeated, device category, ISP, operating system, and browser. Interpret these only after confirming that the intended player integration and interaction logging were active. ([Use Media Analytics](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-media-analytics))

A required Media Watch workflow attribute can prevent form submission until the participant watches the configured percentage of its single assigned video. Progress counts unique watched seconds, so seeking forward does not meet the threshold. On an entry form, configure the attribute as both visible and editable. Auto-resume is disabled when its lookback period is blank or zero. ([Use Digital Media in Workflows](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-digital-media-in-workflows))

Rock’s basic podcast setup uses Podcast Series and Podcast Messages channels, which can be extended with attributes. Podcast series graphics use the Unsecured file type by default and therefore consume database storage; configure a file type backed by the filesystem or an external provider when that storage behavior is undesirable. ([Podcasts](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/podcasts))

## Asset Manager And File Operations

In Rock 19.0, Asset Manager is located under `Admin Tools > CMS Configuration` and manages files and folders in configured storage providers, including cloud storage and the Rock server. The Asset field type can be placed on entities such as content channels, people, and groups so editors can select files from an integrated remote provider such as Azure or Amazon S3. ([View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager), [Intro to the Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager))

Use an Asset attribute or the HTML editor’s asset picker when editors need explicit storage control or need to reuse a file already present in a configured provider. If a file was uploaded directly through the provider and does not appear in a Rock 19.0 Asset Manager folder, refresh the folder’s displayed file list. ([Add Content](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content), [View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager))

File Manager, also under CMS Configuration, supports uploads, deletion, and directory management. A separately placed File Manager block can be given a root folder and scoped permissions so a role manages only one portion of the file hierarchy without receiving FTP credentials. ([File Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/file-manager))

`GetImage.ashx` can resize an image identified by file GUID using width and height query parameters. Its `max`, `pad`, `stretch`, and `crop` options determine how the image fits the requested dimensions. If an external CDN or image service should perform the resizing, add `disableoptimizations=true` to avoid both systems resizing or optimizing the image. ([Understand File Types](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/understand-file-types))

## Social Metadata

Set a page description in Page Settings for pages likely to be shared. Without one, a social platform may derive its description from other page content. Network-specific metadata can be generated with Lava and inserted from an HTML block. ([Intro to Social Networks](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/intro-to-social-networks))

For Facebook, use Lava’s `AddMetaTagToHead` filter to add Open Graph title, description, and image metadata. After publishing, use Facebook’s Share Validator to preview the share and inspect its debugging information. ([Facebook](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/facebook))

For Twitter/X, use `AddMetaTagToHead` for `twitter:title`, `twitter:description`, and `twitter:image`; the image value must be the URL of an image uploaded to the website. Set `twitter:card` to `summary_large_image` for a large-image card or `summary` for a smaller image. ([Twitter/X](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/twitterx))

Public calendar-event templates can generate social metadata through Lava. Event attributes provide separately formatted images for Facebook and Twitter/X sharing. ([Calendar Events](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/calendar-events))

## Personalization And Segments

### Enable the site

Enable a site’s **Enable Personalization** setting under `Admin Tools > Websites` before expecting personalization on that site. Enable Visitor Tracking as well when personalization should use visitor activity. ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization))

Website personalization can combine:

- Personalization Segments for stored person data or browsing behavior.
- Request Filters for current request or session characteristics.
- Site settings that enable personalization and, when needed, visitor tracking.

Rock can personalize for visitors who are not logged in using available session and visitor signals. ([Intro to Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization))

### Build personalization segments

A person must satisfy every configured filter area in a segment. Within one area, its conditions may use Any or All logic. A Person Filter requires a persisted data view, so membership is not real-time and cannot include anonymous visitors. ([Intro to Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments))

The Update Personalization Data job reevaluates conditions and adds or removes people from the current membership list. Internally, segment membership is stored in `PersonAliasPersonalization`: `PersonAliasId` identifies the alias, `PersonalizationType` is `0` for a segment record, and `PersonalizationEntityId` identifies the segment. This implementation detail is useful for a separately authorized read-only diagnosis; it is not permission to modify the table. ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job))

After refreshing an underlying persisted data view, run Update Personalization Data before expecting the segment’s person list to reflect the change. Rock also stores matching segments in the `ROCK_SEGMENT_FILTERS` browser cookie, refreshed every five minutes by default. The Personalization Segment Cookie Affinity Duration system setting controls that interval. ([Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization))

### Personalize anonymous visits

Anonymous visitor personalization requires Enable Visitor Tracking on each applicable site. Rock uses a browser cookie to recognize returning visitors. The default persistence is 365 days and can be changed with Visitor Cookie Persistence Length in System Configuration. ([Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors))

Rock initially associates tracked anonymous page views with a Person Alias record. When the visitor later logs in, Rock links that alias to the identified Person so the earlier activity is attributed to that person. ([Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors))

Do not interpret recognition as authentication. An anonymous cookie may support continuity and audience matching, but it does not grant identity-based permissions.

### Use Request Filters

Request Filters can evaluate request context without identifying the visitor, including site, new-versus-returning status, device type, query parameters, cookies, browser version, IP range, IP-derived location, and visit day or time. ([Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters))

A Request Filter key should omit spaces and special characters because Lava references it by key. Leaving the Site setting blank allows the filter to apply across sites. Confirm whether global applicability is intended before leaving that field blank. ([Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters))

### Apply personalization

For a personalized Content Channel Item, matching any configured segment is sufficient within the segment group, and matching any configured Request Filter is sufficient within the filter group. If the item contains both groups, the visitor must match at least one segment and at least one Request Filter. ([Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items))

The Content Channel View block determines how those item assignments affect output:

- **Ignore** does not consider segments or filters.
- **Prioritize** places matching items before nonmatching items, with each group ordered by the configured item order.
- **Filter** shows matching items; items without any segment or filter assignments remain eligible because they have nothing to match.

These choices belong to the rendering block, not merely to the item or channel. ([Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items))

The Lava `Personalize` command conditionally renders content when the current person or request matches a supplied segment key or Request Filter key. It can be used in page content and communications. For explicit conditional handling, `PersonalizationItems` can determine whether the current context matches a specified segment or Request Filter. ([Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava))

## Adaptive Messages

Adaptive Messages centralize several message adaptations behind one `adaptivemessage` Lava command. Selection can consider personalization data, date windows, view counts, and optional saturation limits. ([Intro to Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages))

When a viewer qualifies for multiple adaptations, configured order determines which one is selected. Treat ordering as active business logic, not cosmetic organization. ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages))

When view tracking is enabled on the command, an adaptation stops displaying to a viewer after its configured saturation count is reached within the configured day range. Diagnose an apparently missing adaptation by checking qualification, date applicability, ordering, tracking, and saturation in that order. ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages))

## Localization

Rock configures localization independently for phone numbers, dates and times, currency symbols, addresses, and school grades. An organization can change only the areas it needs. A changed display setting does not necessarily alter processing behavior. ([Intro to Localization](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/intro-to-localization))

For additional phone countries, add entries under `Admin Tools > Settings > Defined Types > Phone Country Code`. Each entry needs the dialing code, a description, a regular expression matching entered numbers, and a formatting expression mapping captured groups to placeholders. When multiple entries exist, phone controls include a country selector and default to the first defined value; reorder the entries to change that default. ([Localize Phone Numbers](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-phone-numbers))

When a date or time unexpectedly uses a US format, first inspect the server culture in the System Information dialog available from the Admin Toolbar. ([Localize Dates & Times](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-dates-times))

The Organization Currency Code controls the symbol displayed with numeric amounts. It does not convert values or configure payment processing. Payment gateways must use the matching currency to avoid incorrect account crediting. In Lava, `FormatAsCurrency` applies the symbol associated with the configured Organization Currency Code. ([Localize Currency](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-currency))

To enable international address entry and display, set **Support International Addresses** to Yes under `Admin Tools > Settings > Global Attributes`. Configure each supported country’s abbreviation, localized City, State, and Postal Code labels, and display format. For commonly used countries, add Address States tied to the country, placing the abbreviation in Value and the full name in Description. ([Configure International Addresses](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/configure-international-addresses))

## Version And Authority Caveats

- The supplied official documentation was hydrated as Rock 19.0 documentation. Claims explicitly marked Rock 19.0—such as Asset Manager navigation, Content Collection Universal Search dependency, and Content Component template behavior—should not be projected backward without checking the installed version.
- Many approved claims were not assigned a narrower version scope. Treat them as documented behavior in the supplied documentation set, not as proof for every historical or future Rock release.
- Rock 17.5 fixed an interaction-classification issue affecting the Content Channel Item View block and `InteractionContentChannelItemWrite`. Older affected installations may record interactions under the wrong entity type. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- Rock 19.3 fixed Content Channel Item List add/delete controls for users with Edit access on the channel. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- Community recipes are neither reviewed nor endorsed by the Rock core team. The supplied slug recipe is a draft community example and is not used as the factual basis of this guide. ([Content Channels With Slugs](https://community.rockrms.com/recipes/128))
- The supplied GitHub excerpts are tied to immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. For example, the generated [`AdaptiveMessagesController`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/AdaptiveMessagesController.CodeGenerated.cs) shows authenticated REST endpoints and explicit read/write security actions. This implementation evidence does not establish any installation’s version, enabled API surface, permissions, or configuration, so verify those surfaces live before use.
- No contribution record, private draft conclusion, Model Map record, or reviewed live-instance conclusion was supplied.

## Troubleshooting Decision Tree

### A content item does not appear

1. Confirm that the expected page uses the intended Content Channel View or Content Channel Item View block and the intended channel.
2. Check the item’s approval status and whether the channel requires approval.
3. Check Start and Expire dates using the date model defined by the channel type.
4. Inspect block status filters, item filters, context filters, route parameters, and ordering.
5. If the item contains Lava, verify that the item-view block processes `Item.Content` with `RunLava`.
6. If personalization is enabled, inspect the channel setting, item assignments, and the block’s Ignore, Prioritize, or Filter choice.
7. Check View and Interact permissions separately.
8. If the content is being rendered through RSS, test without current-person or page-context assumptions. ([Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item), [Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block), [Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items))

### Staff cannot find or approve a channel item

1. Confirm that the user has View permission on the channel; that controls whether the channel appears under `Tools > Content`.
2. Clear or adjust the status, date-range, and title filters.
3. If the item is pending, use the pending-only channel toggle to locate the channel.
4. Confirm that approvals are enabled for the channel.
5. Confirm that the user’s role has `Approve` on `Rock.Model.ContentChannelType`.
6. For missing add/delete controls, record the installed version and determine whether the Rock 19.3 fix applies. ([Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items), [Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### Content Collection results are stale or empty

1. Confirm an active Universal Search index component.
2. Confirm the expected channel or calendar is a source in the collection.
3. Confirm the needed item attributes were selected for indexing.
4. Run `Index Content Collections` or use Rebuild Index after same-day changes.
5. Confirm filters are enabled both in the collection and in the Content Collection View block.
6. Recheck the block’s selected collection, search-on-load behavior, result count, and templates.
7. If personalization is involved, verify site personalization and the block’s boost configuration.
8. Stop before exposing the collection if it contains restricted items; individual item security is not enforced by the collection. ([Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections), [Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view))

### Personalized content is wrong or stale

1. Confirm **Enable Personalization** on the exact site.
2. If browsing activity is required, confirm Enable Visitor Tracking on that site.
3. Confirm the item’s channel has personalization enabled.
4. Evaluate every segment filter area and its internal Any or All logic.
5. Refresh the persisted data view when person data has changed.
6. Run Update Personalization Data.
7. Allow for or inspect the `ROCK_SEGMENT_FILTERS` cookie affinity interval.
8. Evaluate Request Filters against the current site, device, query, cookie, IP, location, day, and time.
9. Confirm the rendering block is not set to Ignore.
10. Disable output caching for personalized output and retest in isolated sessions. ([Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization), [Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization), [Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components))

### One visitor sees another visitor’s personalized values

1. Disable output caching on the affected Content Channel View or Content Component block.
2. Clear the relevant rendered-output cache.
3. Retest with separate browser sessions.
4. Inspect parent-page, CDN, or proxy caching if the symptom persists.
5. Stop publication until cross-visitor isolation is demonstrated. ([Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block), [Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components))

### An Adaptive Message adaptation does not display

1. Confirm the page or communication invokes the intended Adaptive Message.
2. Check the adaptation’s date window.
3. Check its segment and request-context qualification.
4. Check whether an earlier ordered adaptation also qualifies.
5. If view tracking is enabled, inspect whether the saturation count was reached within the configured day range.
6. Retest with an appropriate clean or known viewer context; do not assume an anonymous session shares an identified person’s history. ([Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages))

### An externally uploaded asset is missing

1. Confirm that the expected storage provider and folder are selected.
2. Refresh the Asset Manager folder.
3. Confirm the editor is using an Asset attribute or asset picker tied to that provider.
4. If the issue is a preview rather than existence, distinguish provider listing, Rock preview support, and public delivery.
5. Verify provider/plugin configuration in the installed instance before changing content references. ([View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager), [Add Content](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content))

### Media analytics or resume behavior is unexpected

1. Confirm the page passes a Media Element GUID to the shortcode’s `media` parameter when Media Element analytics are required.
2. If `src` is used, identify whether it points to the intended generated file variant.
3. Inspect `autoresumeindays` and `combineplaystatisticsindays`.
4. Confirm whether the return occurred inside or outside the configured window.
5. Record the Rock version; if interaction entity classification appears wrong, assess the Rock 17.5 fix.
6. Do not infer lack of engagement solely from analytics until player configuration and interaction logging are verified. ([Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### A required Media Watch form cannot be submitted

1. Confirm the Media Watch attribute is visible and editable on the workflow entry form.
2. Confirm it has one assigned video.
3. Check the required watch percentage.
4. Confirm the participant watched enough unique seconds; seeking forward does not count.
5. Inspect the lookback period. Blank or zero disables auto-resume.
6. Retest using the same participant context intended by the workflow. ([Use Digital Media in Workflows](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-digital-media-in-workflows))

### A social share preview is wrong

1. Confirm the page description in Page Settings.
2. Inspect the rendered Open Graph or Twitter/X metadata.
3. Confirm the image metadata contains a reachable website image URL.
4. Confirm `twitter:card` matches the desired card size.
5. For Facebook, run the Share Validator and review its preview and diagnostics.
6. For calendar events, confirm the template uses the intended network-specific event image attribute. ([Intro to Social Networks](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/intro-to-social-networks), [Facebook](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/facebook), [Twitter/X](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/twitterx))

### Dates, phone numbers, currency, or addresses appear incorrectly localized

1. Identify whether the problem concerns display, entry validation, or downstream processing.
2. For dates and times, inspect server culture in System Information.
3. For phones, inspect Phone Country Code ordering, regular expressions, and formatting expressions.
4. For currency display, inspect Organization Currency Code and Lava formatting.
5. Independently confirm payment-gateway currency; a symbol change does not reconfigure it.
6. For addresses, confirm Support International Addresses and the selected country’s labels, format, and states. ([Localize Dates & Times](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-dates-times), [Localize Phone Numbers](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-phone-numbers), [Localize Currency](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-currency), [Configure International Addresses](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/configure-international-addresses))

## Agent Task Recipes

### Recipe: Publish a governed Content Channel Item

**Outcome:** An item is structurally complete, correctly scheduled, reviewable, and eligible for display.

1. Identify the destination channel and inspect its channel type, item attributes, date mode, approval requirement, and personalization setting.
2. Enter the item through `Tools > Content` unless channel administration is required.
3. Populate the required fields and structured item attributes.
4. Set Start and optional Expire dates according to the channel type.
5. Add or create child items only after confirming the allowed child channels.
6. If the channel requires approval, leave or move the item into the appropriate review state and have a user with Approval permission complete approval.
7. Inspect the exact rendering block’s channel, status, filters, ordering, and template.
8. Verify the public result in both pre-start or expired and active conditions as applicable. ([Add Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items), [Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items))

**Inspect:**

- Channel type and channel-specific attributes
- Approval and permissions
- Start and Expire dates
- Rendering block configuration
- Cache and personalization behavior

**Do not assume:**

- Saving means approved.
- Approval means in date.
- In-date means permitted.
- A valid item means the page block selects it.

**Stop when:**

- The intended authorized audience sees the correct item.
- An unauthorized or ineligible context does not receive restricted content.

### Recipe: Add personalization to Content Channel Items

**Outcome:** Matching visitors receive the intended filtered or prioritized content without cross-visitor cache leakage.

1. Enable personalization on the exact site.
2. Enable Visitor Tracking if activity-based or anonymous continuity is required.
3. Create or validate the Personalization Segments and Request Filters.
4. For Person Filters, confirm the backing data views are persisted.
5. Enable personalization on the Content Channel.
6. Assign segments and/or Request Filters to each target item.
7. Remember that multiple segments are OR within their group, multiple Request Filters are OR within their group, and using both groups requires one match from each.
8. Configure the Content Channel View block as Ignore, Prioritize, or Filter.
9. Disable output caching.
10. Run Update Personalization Data when segment membership has changed.
11. Test a matching identified person, a nonmatching person, and an anonymous or request-filter context. ([Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items), [Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization))

**Do not assume:**

- Personalization grants permission.
- Segment membership updates in real time.
- A channel setting controls how the block applies matches.
- One browser session is enough to prove audience isolation.

### Recipe: Refresh personalization membership

**Outcome:** A persisted segment and its browser-facing membership state reflect current person data.

1. Identify the segment and each persisted data view used by its Person Filter.
2. Refresh the underlying persisted data view.
3. Run Update Personalization Data.
4. Inspect the segment’s current person list.
5. Account for the `ROCK_SEGMENT_FILTERS` cookie affinity duration.
6. Retest with the intended person and site.
7. If the result remains wrong, evaluate every filter area and its Any or All logic. ([Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job), [Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization))

**Stop when:**

- Server-side membership and visitor-facing behavior agree after the documented refresh boundaries.

### Recipe: Build and refresh a Content Collection

**Outcome:** Multiple channels or calendars are searchable together with deliberate filtering, ranking, and security boundaries.

1. Confirm an active Universal Search index component.
2. Create or select the collection under `Admin Tools > CMS Configuration > Content Collections`.
3. Add the required content channels and calendars.
4. Select the source attributes that should be indexed.
5. Enable and arrange the collection’s search filters.
6. Configure trending only if interaction logging exists on the item-viewing surfaces.
7. Configure segment and Request Filter evaluation if personalized ranking is required.
8. Rebuild the index.
9. Configure a Content Collection View block with the collection, result count, search behavior, filters, templates, sort orders, and personalization boost.
10. Verify that each visible filter is enabled in both the collection and block.
11. Audit every source for restricted content before public display. ([Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections), [Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view))

**Stop when:**

- Expected sources and indexed fields appear.
- Same-day changes appear after indexing.
- Restricted source items cannot be exposed through the chosen design.

### Recipe: Configure a Content Component template

**Outcome:** Editors can change structured content without editing presentation markup.

1. In Rock 19.0, open `Admin Tools > CMS Configuration > Content Component Templates`.
2. Copy a suitable existing template as a starting point when appropriate.
3. Build Display Lava using related content items and component settings.
4. Temporarily use `{{ 'Lava' | Debug }}` to inspect available context.
5. Remove debug output.
6. Create Content Channel Item attribute categories whose names exactly match each target template.
7. Add item attributes to the applicable categories; leave Categories blank only when the attribute should appear for every template.
8. Configure the block’s template, filters, item multiplicity, and presentation values.
9. Avoid output caching if any rendered value varies by visitor.
10. Test editing and rendering without requiring the editor to modify HTML. ([Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates), [Add Content Component Item Attributes](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes))

### Recipe: Automate a channel item attribute with Lava

**Outcome:** A scheduled job safely writes evaluated Lava output into a compatible target attribute.

1. Add a Lava-type item attribute to hold the expression.
2. Add the target item attribute with the required field type.
3. Populate and test the Lava on representative items.
4. Confirm its output is valid for the target field type.
5. Create a Content Channel Item Self Update job for the channel.
6. Set Template Key to the Lava attribute key.
7. Set Target Key to the target attribute key.
8. Run the job in a controlled test and inspect the affected item values.
9. Configure page Lava to use the target attribute.
10. Create a separate job for each additional channel. ([Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items))

**Do not assume:**

- A changed attribute default updates existing item values.
- Text that resembles a Boolean or date is valid for every target field type.

### Recipe: Publish a Media Element through a channel

**Outcome:** A media item appears through normal content tools with the intended player behavior and analytics.

1. Confirm the Media Account and provider plugin, or identify that the Local Media Account is being maintained manually.
2. Add a Media Element item attribute to the target Content Channel.
3. Either link the Media Element manually or enable channel synchronization on the Media Folder.
4. Confirm that a newly added element creates the expected item when synchronization is used.
5. In the display Lava, read the Media Element attribute’s raw value.
6. Pass the GUID to the Media Player shortcode’s `media` parameter.
7. Configure auto-resume and play-combination windows deliberately.
8. Play the media from the published page and inspect the resulting analytics.
9. If a direct variant is needed instead, select its URL from Media Files and use `src`, recognizing that this is a different integration pattern. ([Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media), [Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items))

### Recipe: Share or refresh Content Library material

**Outcome:** An item is uploaded or downloaded with its license and overwrite behavior understood.

1. Enable Content Library features on the source or destination channel as appropriate.
2. For upload, confirm the channel license and populate the item’s Experience Level and Topic.
3. Upload only the selected item.
4. For download, start from the destination channel’s **Download from Library** action.
5. Select and download the library item.
6. Before downloading it again, identify any local edits.
7. Refresh only when overwriting those local edits is acceptable.
8. Preserve the license and required attribution in downstream presentation. ([Set Up The Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library), [Library Viewer](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/library-viewer))

### Recipe: Configure localized currency display safely

**Outcome:** Numeric values display the intended currency symbol without implying conversion or silently changing gateway behavior.

1. Confirm the organization’s intended transaction currency.
2. Confirm every relevant payment gateway uses the matching currency.
3. Set Organization Currency Code for the intended display symbol.
4. Use `FormatAsCurrency` for numeric currency output in Lava.
5. Test display values and payment processing as separate checks.
6. Stop if gateway currency and organization currency do not agree. ([Localize Currency](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-currency))

## Known Gaps And Live Verification

No reviewed live-instance evidence was supplied. Before changing or certifying an installation, perform a separate bounded, read-only review of:

- Installed Rock version and patch level.
- Actual channel types, channel settings, item attributes, approval configuration, and security.
- Site-level personalization and visitor-tracking settings.
- Persisted data-view state, personalization job schedule, recent job results, and cookie-affinity configuration.
- Adaptive Message definitions, ordering, date windows, tracking, and saturation.
- Active Universal Search components and Content Collection indexing health.
- Collection sources containing restricted items.
- Installed media and storage-provider plugins.
- Asset provider credentials and connectivity without exposing secrets.
- Payment-gateway currency before any currency-display change.
- Server culture and configured localization records.
- Actual behavior across identified, anonymous, matching, nonmatching, and unauthorized sessions.

Evidence gaps in the supplied pack include:

- No approved claim defining the complete Asset Manager storage-provider setup workflow.
- No approved claim covering school-grade localization beyond its existence as an independent localization area.
- No reviewed live proof of a Content Library connection, provider installation, index state, scheduled-job execution, media analytics, or personalization behavior.
- No official answer-bearing claim promoting the draft community slug recipe into recommended core behavior.
- No evidence that an existing HTML channel’s historical items are automatically converted when structured content is enabled.
- No evidence that a display setting alone reconfigures a payment gateway, CDN, media provider, storage provider, or security boundary.

Mark these as verification work rather than filling them with inferred configuration.

## Source Map

### Content channels and structured content

- [Intro to Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/intro-to-content-channels)
- [Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/channel-types)
- [Use Content Channels](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels)
- [Add a Content Channel Item](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-a-content-channel-item)
- [Secure Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content)
- [Use Universal Channel Types](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-universal-channel-types)
- [Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)
- [Add Content Channel Child Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/add-content-channel-child-items)
- [Publish Content Through Feeds](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/publish-content-through-feeds)
- [Self Update Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/self-update-content-channel-items)
- [Manage Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items)
- [Add Content Items](https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/add-content-items)

### Content Components and collections

- [Intro to Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/intro-to-content-components)
- [Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components)
- [Create Content Component Templates](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/create-content-component-templates)
- [Add Content Component Item Attributes](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/add-content-component-item-attributes)
- [Intro to Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/intro-to-content-collections)
- [Set Up Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/set-up-content-collections)
- [Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view)
- [Trending Content](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/trending-content)
- [Troubleshoot Content Collections](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/troubleshoot-content-collections)

### Library, assets, media, and social metadata

- [Intro to the Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/intro-to-the-content-library)
- [Set Up The Content Library](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/set-up-the-content-library)
- [Library Viewer](https://community.rockrms.com/documentation/digital-publishing/content-management/content-library/library-viewer)
- [Intro to the Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/intro-to-the-asset-manager)
- [View Asset Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/view-asset-manager)
- [Add Content](https://community.rockrms.com/documentation/digital-publishing/content-management/asset-manager-system/add-content)
- [File Manager](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/file-manager)
- [Understand File Types](https://community.rockrms.com/documentation/digital-publishing/content-management/rock-directory-structure/understand-file-types)
- [Configure Media Accounts](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/configure-media-accounts)
- [Publishing Media](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/publishing-media)
- [Media Player Lava Shortcode](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/media-player-lava-shortcode)
- [Use With Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-with-content-channel-items)
- [Use Media Analytics](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-media-analytics)
- [Use Digital Media in Workflows](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/use-digital-media-in-workflows)
- [Podcasts](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/podcasts)
- [Intro to Social Networks](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/intro-to-social-networks)
- [Facebook](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/facebook)
- [Twitter/X](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/twitterx)
- [Calendar Events](https://community.rockrms.com/documentation/digital-publishing/content-management/social-networks/calendar-events)

### Personalization, Adaptive Messages, and localization

- [Intro to Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/overview/intro-to-personalization)
- [Intro to Personalization Segments](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/intro-to-personalization-segments)
- [Use Request Filters](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/use-request-filters)
- [Configure Site for Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization)
- [Personalize for Anonymous Visitors](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-for-anonymous-visitors)
- [Personalize Content Channel Items](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items)
- [Personalize Using Lava](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava)
- [Update Personalization Job](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/update-personalization-job)
- [Troubleshoot Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/troubleshoot-personalization)
- [Intro to Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/intro-to-adaptive-messages)
- [Set Up Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages/set-up-adaptive-messages)
- [Intro to Localization](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/intro-to-localization)
- [Localize Phone Numbers](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-phone-numbers)
- [Localize Dates & Times](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-dates-times)
- [Localize Currency](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/localize-currency)
- [Configure International Addresses](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/configure-international-addresses)

### Version and secondary evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- [Interaction Content Channel Item Write](https://community.rockrms.com/lava/commands/interaction-content-channel-item-write)
- [Content Channels With Slugs — draft community recipe](https://community.rockrms.com/recipes/128)
