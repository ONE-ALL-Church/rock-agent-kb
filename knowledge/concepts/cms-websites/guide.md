---
id: authored-cms-websites
title: CMS And Websites
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# CMS And Websites

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [CMS And Websites index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock RMS can operate as a public website platform, internal portal platform, content management system, media publishing system, and relationship-aware personalization engine. Treat the CMS as a live application surface, not as a static page editor. A Rock page can expose blocks that read and mutate people, groups, workflows, registrations, content channels, media, interactions, and files. A website change can therefore become a security change, data change, workflow launch, reporting change, or performance change.

The core mental model is:

- A **Site** defines a website or application surface.
- A **Page** defines routeable structure, title, layout, security, display behavior, and parent-child navigation.
- A **Layout** and **Theme** define where zones exist and how those zones render.
- A **Block** is executable functionality placed into a page zone.
- **Block settings** control behavior for that page instance.
- **HTML / Advanced HTML / Lava-capable blocks** can render dynamic output and, if commands are enabled, execute privileged actions.
- **Content Channels** hold structured or unstructured content items such as articles, devotionals, sermon notes, media posts, announcements, and reusable content libraries.
- **Media** and **Interactions** connect content display to engagement, analytics, required watching, and personalization.
- **Security** is applied at multiple layers: site, page, block, content channel, content item, file/document type, data views, reports, and block-specific actions.

RockU’s CMS course positions Rock as an all-in-one relationship and content management system that can run an organization’s website, with training topics spanning pages, blocks, Page Builder, HTML blocks, Advanced HTML, cache tags, short links, asset management, persisted datasets, entity documents, Rock Media, personalization, interactive experiences, and icon systems ([RockU CMS](https://community.rockrms.com/rocku/cms)). Use that breadth as a warning: “CMS” in Rock is not only website editing. It crosses presentation, data, identity, security, content modeling, and operational analytics.

For agents doing real Rock work, the safest operating sequence is:

1. Identify the **site, page, route, block instance, and content object** involved.
2. Inspect **page security and block security** before assuming a rendering bug is only a content bug.
3. Inspect **block type and block settings** before editing HTML, Lava, or SQL.
4. Inspect **content channel type, channel, item status, start/expire dates, categories, and item attributes** before assuming a content item should appear.
5. Inspect **Lava commands enabled on the block** before modifying Lava.
6. Inspect **cache duration, cache tags, and interaction logging settings** before testing a change.
7. If media, files, or documents are involved, inspect **media element, binary file, file type, document type, and security inheritance**.
8. For production changes, make a reversible plan: export current Lava/settings, record page/block IDs, test as anonymous and authenticated users, and clear only the relevant cache.

This guide is draft-level synthesis. It cites the source pack, but every live implementation should be verified against the target Rock version, installed plugins, custom themes, configured jobs, and local security model.

## 2. Scope And Terminology

This guide covers Rock CMS and website operations: pages, blocks, themes, content channels, personalization, media, assets, entity documents, cache behavior, reporting, analytics, and developer landmarks. It also covers operational guardrails for agents diagnosing or changing those areas.

It does not replace the dedicated guides for Lava, security, media, content, or personalization. Those areas are dependency topics for this guide. When a task touches Lava commands, authorization, uploaded files, media analytics, or personalized content, use the dedicated topic as the deeper authority and use this guide as the CMS integration map.

Key terms:

**Site**
A Rock website or app surface. Sites commonly represent the internal Rock portal, external public website, microsites, mobile surfaces, and other routeable experiences. Site settings may control domains, themes, advanced behavior, and whether page views are logged. Community reporting examples specifically instruct admins to confirm “Log Page Views” under site advanced settings before building page-view reports ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)).

**Page**
A routeable CMS node. Pages sit in a hierarchy, can have layouts and display settings, can be secured, and can host blocks in layout zones. Page identity matters because many blocks receive page parameters, build links to detail pages, update the page title, or write interactions tied to a page.

**Page route**
The URL path or route that resolves to a page. Rock instances may support multiple routes per page depending on version and configuration. For live work, inspect the page route table or page detail UI instead of assuming a URL maps one-to-one to a single page.

**Layout**
A template supplied by a theme that defines zones such as Main, Sidebar, Feature, Header, or Footer. Blocks are placed into zones. If a block is configured correctly but invisible, verify that the selected layout exposes the zone where the block is placed.

**Theme**
A package of layouts, CSS, scripts, assets, and conventions used by a site or page. RockU includes theme-adjacent CMS topics such as Font Awesome legacy guidance and Tabler Icons, implying that icon and style systems are part of CMS implementation decisions ([Font Awesome 5 Legacy](https://community.rockrms.com/rocku/cms/font-awesome-5-1), [Tabler Icons](https://community.rockrms.com/rocku/cms/tabler-icons)).

**Block type**
The reusable functionality definition, such as HTML Content, Advanced HTML, Dynamic Data, Content Channel Item View, Content Channel Item List, Page Parameter Filter, Workflow Entry, Login, or a custom Obsidian block.

**Block instance**
A specific placement of a block type on a page. Instance settings, security, zone, order, cache behavior, and HTML content can differ across pages.

**HTML block / HTML Content block**
A block used to place authored HTML and often Lava into a page. Source material distinguishes HTML Block and Advanced HTML Block training ([HTML Block](https://community.rockrms.com/rocku/cms/html-block), [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)). In live Rock, inspect the exact block type and settings because naming and implementation vary by version.

**Advanced HTML block**
A more powerful authored-content block. Treat it as privileged. The source pack’s distilled insight says Advanced HTML guidance should include CMS security and Lava review: inspect enabled commands, context inputs, and page/block authorization ([Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)).

**Lava**
Rock’s templating language. Lava by itself can render dynamic output. Lava commands can enable database, entity, cache, web request, workflow, interaction, JavaScript, stylesheet, and other operations, but commands must be enabled where used and can bypass normal business logic if misused ([Lava Commands](https://community.rockrms.com/lava/commands)).

**Content Channel Type**
The schema-like category for channels. It can define item attributes, inherited behavior, and editing model.

**Content Channel**
A container for content items. Source-code view models show channel-level properties including content channel type, categories, child content channels, channel URL, icon CSS class, content control type, structured content flags, RSS enablement, personalization enablement, indexing, tagging, content library enablement, and image/summary/author attribute references ([ContentChannelBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)).

**Content Channel Item**
An individual article, media post, devotional, announcement, structured content entry, or other channel item. Items usually have status, dates, attributes, content, and security.

**Content Channel Item View block**
A display block that resolves and renders a single content item. Source-code settings include cache tags, content channel GUID, allowed item statuses, URL query parameter name, detail page, display-most-recent behavior, item merge field behavior, workflow launch rules, interaction logging, page-title update behavior, item cache duration, Lava template, and metadata attribute mappings ([ContentChannelItemView settings source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).

**Interaction**
A logged engagement record such as a page view or content item view. Content item view source snippets show a server-issued interaction token with an expiration and browser session de-duplication behavior for view logging ([ContentChannelItemView options source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts)).

**Personalization**
Rock’s ability to tailor content based on person, segment, content, or context. RockU treats personalization as part of CMS training ([Personalization](https://community.rockrms.com/rocku/cms/personalization)). Content channel source fields include `enablePersonalization`, so personalization can be channel-aware as well as block- or Lava-driven ([ContentChannelBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)).

**Asset Manager**
The CMS surface for managing website assets. RockU includes Asset Manager training under CMS ([Asset Manager](https://community.rockrms.com/rocku/cms/asset-manager)). In live work, inspect the file path, file type, storage provider, and security rather than assuming every asset is just a public static file.

**Entity Document**
A document attached to an entity, often backed by a binary file and document type. RockU includes Entity Documents in CMS training ([Entity Documents](https://community.rockrms.com/rocku/cms/entity-documents)). Release notes warn that document linkage affects security enforcement: files uploaded through an Entity Document Add workflow action must be linked to the parent Document so Document Type security can be checked ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

**Short Link**
A short URL managed in Rock. RockU includes Short Links in CMS training ([Short Links](https://community.rockrms.com/rocku/cms/short-links)). For live work, inspect the configured target, route conflicts, redirects, campaign tracking, and security implications.

## 3. CMS And Websites Mental Model

Rock CMS work is best understood as four layers running together.

The first layer is **routing and structure**. A browser request resolves to a site and page. The page selects a layout. The layout provides zones. Blocks in those zones execute. Navigation, breadcrumbs, page titles, and route parameters all depend on this layer. If a public URL gives the wrong content, start by proving the route-to-page mapping, then page hierarchy, then block placement.

The second layer is **execution**. Blocks are not passive widgets. A block can query data, render Lava, launch workflows, write interactions, accept form submissions, upload files, call APIs, or expose custom actions. Obsidian developer docs describe a modern block as a C# server-side block, a TypeScript client component, and block actions that let the client communicate with the server ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). Older Web Forms blocks follow a different implementation pattern, but the operational principle is the same: the block instance is executable software.

The third layer is **content modeling**. Content channels provide reusable content structures that can be listed, filtered, categorized, secured, indexed, personalized, rendered as RSS, and connected to media. Source-code view models show that channel configuration includes content channel type, child channels, item attributes, structured content, RSS, personalization, content library, indexing, tagging, root image directory, and settings ([ContentChannelBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)). A display issue may therefore be caused by channel schema, item status, dates, security, category filtering, Lava template logic, indexing, or cache.

The fourth layer is **identity-aware engagement**. Rock websites know about people, authentication, cookies, interactions, workflows, and segments. Content item view settings include interaction logging controls and logged-in-only options ([ContentChannelItemView settings source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)). RockU includes Rock Media analytics, required watching, and personalization in CMS training ([Rock Media Analytics](https://community.rockrms.com/rocku/cms/rock-media-analytics), [Rock Media Required Watching](https://community.rockrms.com/rocku/cms/rock-media-required-watching), [Personalization](https://community.rockrms.com/rocku/cms/personalization)). This makes CMS behavior dependent on the current person, whether the viewer is anonymous, whether interactions are logged, and whether personalization rules match.

Agents should avoid flat “page content” assumptions. Ask:

- Is this a page problem, block problem, template problem, content item problem, route problem, security problem, cache problem, or identity/context problem?
- Is the page being rendered through a Web Forms block, Obsidian block, mobile block, or custom plugin?
- Is the content embedded in block settings, stored as shared HTML content, stored in a content channel item, generated from Lava, fetched by SQL/entity command, or provided by a workflow?
- Is the viewer anonymous, authenticated, impersonated, or a staff user with edit controls?
- Is the observed output stale because of item cache duration, cache tags, page output cache, CDN/proxy cache, browser session de-duplication, or persisted datasets?

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. **Live Rock instance inspection** for the exact site, page, block, content channel, item, route, security rules, attributes, and version.
2. **Official Rock documentation, RockU, developer docs, release notes, and source code** for intended behavior and version changes.
3. **Model Map or database schema inspection** for entity relationships and column names.
4. **Community recipes and partner articles** for examples and patterns, not as final authority.
5. **Local custom code and theme files** for instance-specific behavior.

The source pack includes RockU CMS training pages with a broad curriculum but limited hydrated detail. Treat those as official coverage signals for what belongs in CMS: pages and blocks, Page Builder, HTML blocks, Advanced HTML, cache tags, short links, asset management, persisted datasets, entity documents, phone number lookup, Rock Media, personalization, interactive experiences, and icons ([RockU CMS](https://community.rockrms.com/rocku/cms)).

Developer docs are stronger for implementation landmarks. The Obsidian block guide identifies the parts of modern blocks: C# block, TypeScript component, and block actions ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). Mobile CMS block docs show that CMS concepts are reused in mobile surfaces, including a Lava Item List block with page size, detail page, list template, list data template, and merge fields for page and page size ([Lava Item List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/lava-item-list)).

Source-code snippets are strong evidence for field names and configuration surfaces but may represent the `develop` branch at retrieval time, not the target production version. Use them to know what to inspect, then verify in the running Rock instance. For example, `ContentChannelItemViewCustomSettingsBag` exposes settings for cache tags, allowed content item statuses, query parameter, detail page, display-most-recent, Lava template, interaction logging, page-title updates, workflow launch conditions, and item cache duration ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)). A production instance on an earlier version may expose a different set of block settings.

Release notes are mandatory when behavior changed. The pack includes CMS-related release notes such as:

- v19.1: deleting an HTML Content block could remove shared content for other linked blocks using the same Context Name; Rock changed behavior so shared content can be preserved when a block is deleted ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v18.2: a security issue affecting multiple Content Channel blocks allowed users with only View permissions to delete content items; delete is now limited to Edit access ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v17.1: Content Channel Item View breadcrumbs could fail when a page was accessed directly rather than through site navigation ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- v16.1: editing Dynamic Data block settings could update the page name of the internal page editor page ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Community recipes are useful but explicitly not endorsed by the Rock core team. The recipe pages include a disclaimer that contributed recipes may not follow best practices and could affect performance or security ([Search Rock Pages recipe](https://community.rockrms.com/recipes/432), [Easy Page Views Reporting recipe](https://community.rockrms.com/recipes/261)). Use them as examples only after reviewing SQL, Lava commands, security, and performance in the target instance.

## 5. Core Configuration And Data Model

### Sites

A Site is the top-level configuration for a web surface. Agents should inspect:

- Site name and purpose.
- Domains or hostnames.
- Default page and login-related pages.
- Theme and default layout behavior.
- Advanced settings such as whether page views are logged.
- Security for who can administer the site.
- Whether the site is internal, external, mobile, TV, or custom.
- Whether site-level settings are inherited by pages or blocks.

The page-view reporting recipe specifically depends on “Log Page Views” being enabled under Admin Tools > Sites > selected site > Advanced Settings ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)). If page analytics appear empty, verify this before writing SQL or blaming interactions.

### Pages

A Page is the navigable CMS node. Core things to inspect:

- `Id`, `Guid`, internal name, browser title/page title, route(s), parent page, and display order.
- Site and layout.
- Page icon, description, breadcrumbs, and navigation inclusion.
- Security rules, especially View/Edit/Administrate.
- Page parameters passed through query string or route.
- Blocks assigned to each zone.
- Whether page title can be overwritten by blocks such as Dynamic Data or Content Channel Item View.
- Whether the page is used as a detail page by another block.

Community recipes show agents how page identity is used operationally. The Search Rock Pages recipe uses Page Parameter Filter to produce a searchable page selector, with SQL returning `Page.Id` as value and `InternalName` as text ([Search Rock Pages](https://community.rockrms.com/recipes/432)). Do not copy that SQL blindly into production; use it as a reminder that page lookup tasks should use real page IDs and names instead of searching by visible URL alone.

### Blocks

A block instance joins a block type to a page zone. Inspect:

- Block instance ID and GUID.
- Block type name, category, path, and implementation technology.
- Zone and order.
- Instance name.
- Block settings.
- Block security.
- Whether the block uses shared content, context name, entity context, or page parameters.
- Whether the block is visible only in certain modes.
- Lava commands enabled.
- Cache duration and cache tags if applicable.
- Whether the block writes interactions, launches workflows, uploads files, mutates content, or calls external services.

The Web Forms `ContentChannelItemPersonalListLava` source shows a classic block with attributes such as Content Channel, Max Items, Detail Page, and Lava Template; it renders items for the current person using a Lava template and optionally links them to a detail page ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs)). That is a useful pattern: a block’s visible behavior is often almost entirely controlled by instance attributes.

### Layouts And Zones

Layouts determine where blocks can appear. If an agent is told “the block is on the page but not showing,” inspect:

- The page’s selected layout.
- Whether the layout file contains the zone used by the block.
- Whether the zone is hidden in the theme CSS.
- Whether the block is in a zone that only renders for certain page modes.
- Whether the theme has layout variants for internal, external, mobile, check-in, or modal contexts.

### Themes

Themes define presentation. Inspect:

- Site theme.
- Page-level theme override if present.
- Layout files.
- CSS/LESS/SCSS build process.
- JavaScript loaded globally.
- Asset directories.
- Icon library expectations.
- Bootstrap version or design system conventions.
- Whether the theme is customized from a stock Rock theme.

The source pack includes Apple TV theme docs, which are not the same as web CMS themes, but they show that Rock platform surfaces can have theme-specific behavior and page-level theme declarations in non-web contexts ([Apple TV Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes)). For web work, verify the actual Rock web theme files and version.

### Content Channel Types

Content Channel Types define reusable content schema. Inspect:

- Type name and item terminology.
- Inherited item attributes.
- Whether structured content is available.
- Whether content library behavior is enabled in this version.
- Whether channels of this type allow child channels.
- Security.

The `ContentChannelDetailOptionsBag` source shows that the detail UI may need available licenses, content channels, content channel types, content control types, inherited content library item attributes, current page URL, a disable-content-field flag, approver configuration, and index availability ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelDetailOptionsBag.d.ts)). Use this as an inspection checklist, not as a guarantee that every field exists in every production version.

### Content Channels

A Content Channel is the configured container. Inspect:

- Channel name and ID/GUID.
- Content Channel Type.
- Description.
- Channel URL.
- Categories.
- Child content channel rules.
- Whether child items are manually ordered.
- Content control type.
- Personalization enabled.
- RSS enabled.
- Icon CSS class.
- Image attribute GUID.
- Summary attribute GUID.
- Author attribute GUID.
- Root image directory.
- Settings.
- Content library enabled.
- Index enabled.
- Structured content enabled.
- Tagging enabled.
- Item attributes and attribute values.
- Security and approval rules.

Most of these fields appear in the source snippet for `ContentChannelBag` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)). In live work, confirm the exact UI labels and database fields.

### Content Channel Items

For each item, inspect:

- Channel.
- Title and slug/key if configured.
- Status, including whether status is approved/published/pending depending on version.
- Start and expiration dates.
- Priority and order.
- Categories and tags.
- Parent/child item relationships if used.
- Attribute values.
- Content field or structured content payload.
- Linked media elements.
- Security.
- Created/modified/audited values.
- Whether it is indexed.
- Whether it has interactions.

The Content Channel Item List options source indicates the list UI tracks content channel ID, item name, date type, include-time behavior, content library enablement, manual ordering, license GUID, and which columns to show such as priority, reorder, security, start date/time, and status ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/contentChannelItemListOptionsBag.d.ts)).

### Media And Linked Media Elements

Content items can be connected to media. The source pack includes request and response bags for retrieving linked media elements from the Content Channel Item List block. The request includes a content channel item identifier key; the response returns a list of linked media element bags ([request source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsRequestBag.cs), [response source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsResponseBag.cs)). The linked media element bag implements `ITranslateIdKey`, indicating ID-key translation is part of the API contract ([LinkedMediaElementBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/LinkedMediaElementBag.cs)).

When media does not show or analytics are wrong, inspect both the CMS item and the media record. RockU treats publishing, analytics, and required watching as CMS-adjacent workflows ([Publishing Rock Media](https://community.rockrms.com/rocku/cms/publishing-rock-media), [Rock Media Analytics](https://community.rockrms.com/rocku/cms/rock-media-analytics), [Rock Media Required Watching](https://community.rockrms.com/rocku/cms/rock-media-required-watching)).

## 6. Primary Entities And Relationships

The following relationship map is the practical minimum for CMS troubleshooting.

### Site To Page

A Site owns or scopes pages. A page generally belongs to a site or participates in a site’s route tree. A public URL must resolve through domain/site selection and page route/page ID resolution. When diagnosing a URL:

1. Determine the requested host.
2. Determine the matching Site.
3. Determine the route/page.
4. Determine whether the page is active and viewable.
5. Determine whether the user has View access.
6. Determine whether a redirect, short link, route table, or proxy is changing the request.

### Page To Layout To Zone To Block

A page selects a layout. The layout defines zones. Blocks sit in zones. A block can be correctly configured and still never render if the page layout does not render its zone. If a block appears to have vanished after a layout or theme change, inspect zone names and block assignments.

### Page To Block Settings

Block settings are instance-specific. Two blocks of the same type can behave differently on different pages. Many CMS bugs come from editing the wrong block instance or editing a shared content record that multiple instances use.

Release notes include a v19.1 fix for deleting an HTML Content block where shared content using the same Context Name could be removed for other linked blocks; the fix preserves shared content by allowing the source `HtmlContent` block ID to be null when a block is deleted ([Rock Release Notes](https://www.rockrms.com/releasenotes)). For agents, this means shared HTML content requires special caution. Before deleting or editing an HTML Content block, inspect whether other blocks share the same context name/content.

### Block To Lava Commands

HTML and Advanced HTML blocks often render Lava. Lava commands are not globally safe. The Lava commands documentation says commands must be enabled when needed and that commands can bypass built-in security and business logic ([Lava Commands](https://community.rockrms.com/lava/commands)). For every Lava-bearing block, inspect:

- Which commands are enabled on the block.
- Whether SQL, Entity, Modify Entity, Delete Entity, Web Request, Workflow Activate, Interaction Write, JavaScript, or Cache commands are enabled.
- Whether untrusted page parameters are used in Lava.
- Whether command output is HTML-encoded where needed.
- Whether the Lava author assumed staff-only access but the page is public.
- Whether the Lava queries data the viewer should not see.

### Content Channel Type To Channel To Item

Content Channel Type defines schema and behavior. Channel config selects type and channel-level options. Items hold content and values. Display blocks select channels and item statuses.

If an item does not show, inspect:

1. Is the block pointing at the expected channel GUID/ID?
2. Is the item in that channel?
3. Is the item status included in the block’s allowed statuses?
4. Is the current date within start/expire windows?
5. Does the item satisfy category/tag filters?
6. Does the viewer have item/channel/page/block access?
7. Is the block cache serving old output?
8. Is the list/detail query parameter matching the item identifier expected by the block?

The Content Channel Item View settings source explicitly includes content channel GUID, allowed item statuses, URL parameter name, display-most-recent setting, cache duration, and Lava template ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).

### Content Channel Item To Media

A content item can have linked media elements. When video/audio/media display is broken:

- Inspect the item’s linked media elements.
- Inspect the media element record and file/provider.
- Inspect media permissions.
- Inspect whether the display block fetches linked media by item ID key.
- Inspect whether the viewer is eligible for required watching or analytics.
- Inspect browser errors for player/provider failures.

The linked media source snippets provide the implementation landmark for Content Channel Item List linked media calls ([GetLinkedMediaElementsRequestBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsRequestBag.cs), [GetLinkedMediaElementsResponseBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsResponseBag.cs)).

### Page And Content To Interactions

Interactions can represent page views and content item views. A community recipe demonstrates page-view reporting by enabling Log Page Views and combining Page Parameter Filter with Dynamic Data ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)). Content Channel Item View has settings for logging interactions and whether interactions should be written only for logged-in individuals ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)). The options bag shows the client may receive an opaque interaction token with an expiration and sessionStorage de-duplication behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts)).

If counts are lower than expected, verify:

- Site page-view logging.
- Block interaction logging.
- Logged-in-only settings.
- Known crawler filtering.
- Token expiration.
- Browser session de-duplication.
- Whether navigation is full page load, AJAX, mobile, or embedded player.
- Whether analytics are delayed by jobs or aggregation.

### Files, Binary Files, Entity Documents, And Security

Entity documents cross CMS, files, and security. Release notes state that files uploaded by Entity Document Add workflow action must be linked to their parent Document so Document Type security applies; otherwise access may fall back to File Type security ([Rock Release Notes](https://www.rockrms.com/releasenotes)). When a CMS page links a document:

- Inspect the entity document record.
- Inspect the document type.
- Inspect the binary file and file type.
- Inspect security rules on document type and file type.
- Inspect whether the file URL bypasses the intended document access path.
- Test as anonymous, authenticated non-staff, and intended authorized users.

## 7. Common CMS And Websites Workflows

### Create A New Public Page

1. Identify the target Site and parent page.
2. Confirm URL route requirements.
3. Choose a layout that has the needed zones.
4. Create the page with a clear internal name and page title.
5. Set security explicitly. Public pages need View for All Users or the intended public role, but edit/administrate should remain limited.
6. Add blocks.
7. Configure block settings.
8. If using Lava, enable only required commands.
9. If using content channels, select channel and statuses intentionally.
10. Test anonymous and authenticated.
11. Test desktop and mobile.
12. Verify page title, meta description, open graph image, canonical behavior if configured, and breadcrumbs.
13. Verify interactions if analytics matter.
14. Clear relevant caches and retest.

RockU’s Adding Pages and Blocks and Page Builder lessons are the primary official training landmarks for this workflow ([Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy), [Page Builder](https://community.rockrms.com/rocku/cms/page-builder)).

### Add Or Edit An HTML Content Block

1. Locate the exact page and block instance.
2. Export or copy current block settings and content before editing.
3. Inspect whether content is shared by context name or another linking mechanism.
4. Inspect block security.
5. Inspect enabled Lava commands.
6. Make the smallest content change.
7. Avoid inline JavaScript unless there is a strong operational need.
8. Avoid SQL/Entity commands in public HTML blocks unless reviewed.
9. Test with edit controls hidden and as a public visitor.
10. Confirm no console errors.
11. Confirm no layout shifts or theme regressions.
12. If cached, clear the block/page cache or adjust cache tags.

HTML Block and Advanced HTML Block are separate RockU topics ([HTML Block](https://community.rockrms.com/rocku/cms/html-block), [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)). Treat Advanced HTML as higher risk because it is commonly where agents encounter richer Lava, scripts, and context-driven output.

### Build A Content Channel Listing And Detail Flow

A typical content flow has a list page and a detail page:

1. Define or identify Content Channel Type.
2. Configure Content Channel.
3. Add item attributes for image, summary, author, topic, media, call-to-action, or structured data.
4. Create items with status and dates.
5. Create a listing page.
6. Add Content Channel Item List, Content Channel Navigation, Dynamic Data, Lava list, or custom block.
7. Configure channel, status, category filters, date behavior, sort order, page size, and detail page.
8. Create a detail page.
9. Add Content Channel Item View.
10. Configure content channel, query parameter, statuses, item cache duration, Lava template, metadata attributes, page title update, and interaction logging.
11. Test direct detail URL and navigation from listing.
12. Test breadcrumbs. Note v17.1 fixed a direct-link breadcrumb issue in Content Channel Item View ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
13. Test expired, pending, future, and unauthorized items.
14. Test social preview metadata if configured.
15. Test cache invalidation after editing an item.

### Publish Media Through CMS

1. Identify whether media is managed as Rock Media, binary files, external provider embeds, or content item attributes.
2. Link media to the content item or page block.
3. Configure player/display block.
4. Confirm media file/provider access.
5. Confirm thumbnail/image attributes.
6. Enable interaction/media analytics if needed.
7. Configure required watching if this is training/compliance/discipleship content.
8. Test as anonymous and logged-in users.
9. Verify analytics after view events are processed.

RockU has separate CMS lessons for Publishing Rock Media, Rock Media Analytics, and Required Watching ([Publishing Rock Media](https://community.rockrms.com/rocku/cms/publishing-rock-media), [Rock Media Analytics](https://community.rockrms.com/rocku/cms/rock-media-analytics), [Rock Media Required Watching](https://community.rockrms.com/rocku/cms/rock-media-required-watching)).

### Add Personalization To A Page Or Channel

1. Define the audience rule or segment.
2. Determine whether personalization belongs in Lava, content channel configuration, a personalization block, or a content component.
3. Confirm the viewer context: anonymous, known person, logged-in person, family, campus, group, or segment.
4. Avoid hiding critical content behind personalization without a fallback.
5. Confirm caching does not serve one person’s personalized output to another person.
6. Test all expected audiences.
7. Inspect interactions or analytics after launch.

Content Channel configuration includes `enablePersonalization` in source snippets ([ContentChannelBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)). RockU includes personalization as a CMS topic ([Personalization](https://community.rockrms.com/rocku/cms/personalization)).

### Add A Search Or Filter Interface For Pages

A community recipe demonstrates adding a Page Parameter Filter to the Pages page to help search Rock pages ([Search Rock Pages](https://community.rockrms.com/recipes/432)). Use the recipe as a pattern, but harden it:

- Confirm the page is internal staff-only.
- Use parameterized or constrained filters where available.
- Avoid exposing internal page IDs publicly.
- Decide whether `InternalName`, `PageTitle`, route, or breadcrumb path is the best search label.
- Confirm the SQL performs acceptably.
- Confirm the result navigates to the intended page.
- Review security because page search can reveal page structure.

### Build Page View Reporting

The page-view reporting recipe shows a simple pattern: enable site page-view logging, create a reporting page, add Page Parameter Filter, add Dynamic Data, and filter by page/person/date range ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)). Before using this pattern:

- Confirm the site has Log Page Views enabled.
- Confirm interaction data exists for the target date range.
- Confirm Dynamic Data block permissions.
- Confirm report security because interaction data can expose browsing behavior.
- Confirm whether anonymous views, authenticated views, crawlers, and de-duplicated interactions are included.
- Avoid running broad unbounded interaction queries on large databases.

## 8. Pages And Blocks Deep Dive

### Page Identity

Agents should capture both human-readable and stable identifiers:

- Page ID.
- Page GUID.
- Internal name.
- Page title/browser title.
- Route/path.
- Parent page.
- Site.
- Layout.
- Security.

Use stable IDs in notes and reversible plans. Page names and routes can change; page IDs and GUIDs are safer for audit trails.

### Page Hierarchy And Navigation

Page hierarchy affects:

- Breadcrumbs.
- Navigation blocks.
- inherited assumptions about security.
- User mental model.
- Page Map and page picker behavior.
- Detail/list parent relationships.

The Search Rock Pages recipe exists because deeply nested pages can be hard to find through Page Map alone ([Search Rock Pages](https://community.rockrms.com/recipes/432)). For agents, that means page hierarchy should be inspected, not guessed from URL segments.

### Page Parameters

Page parameters are commonly used to pass:

- Content item ID/key.
- Category GUID.
- Group ID.
- Person alias ID.
- Workflow type ID.
- Registration instance ID.
- Campus.
- Date range.
- Search query.

The Content Channel Navigation source indicates a `CategoryGuid` page parameter can determine the initially selected category ([ContentChannelNavigationBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts)). The Content Channel Item View settings source includes a configurable URL parameter name used to determine which item to display ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).

When debugging page parameters:

1. Capture the full URL.
2. Identify route parameters and query parameters.
3. Inspect the block settings for expected parameter names.
4. Confirm parameter value type: integer ID, GUID, idKey, slug, category GUID, or custom key.
5. Check whether Lava reads the same parameter.
6. Confirm invalid parameters fail safely.

### Block Types And Implementation Generations

Rock has classic Web Forms blocks and modern Obsidian blocks. Some installations also have custom plugin blocks. The developer guide describes Obsidian blocks as a C# block, TypeScript component, and block actions ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). Web Forms blocks may use `.ascx` and `.ascx.cs`, as seen in `ContentChannelItemPersonalListLava.ascx` and its code-behind ([markup source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx), [code source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs)).

For an agent, this matters because:

- Obsidian blocks may have custom settings bags, action endpoints, encrypted tokens, and client-side state.
- Web Forms blocks may rely on UpdatePanels, server controls, view state, and block attributes.
- A source-code snippet from `develop` may describe a newer Obsidian block that does not exist in the production instance.
- A plugin may override or supplement stock CMS behavior.

### Block Settings

Always inspect block settings before editing content. Common CMS block settings include:

- Content Channel.
- Content Channel Item statuses.
- Query parameter name.
- Detail page.
- Lava template.
- Cache duration.
- Cache tags.
- Page size.
- Sort order.
- Show/hide columns.
- Enable item merge fields.
- Enable page title updates.
- Enable interaction logging.
- Workflow launch condition.
- Logged-in-only behavior.
- Meta description/image/title attribute mappings.
- Enabled Lava commands.

The `ContentChannelItemViewCustomSettingsBag` source is a useful checklist for detail display blocks: cache tags, channel GUID, statuses, query parameter, detail page, display-most-recent, item merge field, workflow launch only when logged in, log interactions, update page title, write interactions only when logged in, item cache duration, launch workflow condition, Lava template, and metadata fields ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).

### Block Security

A block can have its own security independent of page security. Inspect:

- View access.
- Edit access.
- Administrate access.
- Any custom actions or block-specific authorization.
- Whether edit controls appear only for authorized users.
- Whether AJAX/block actions enforce server-side authorization.

The v18.2 release note about Content Channel blocks allowing View-only users to delete content items is an important reminder: UI visibility and server-side permissions must both be correct ([Rock Release Notes](https://www.rockrms.com/releasenotes)). If the instance is before that fix, verify whether the affected blocks are exposed to users with only View rights.

### Dynamic Data Blocks

Dynamic Data can be powerful and risky. The release pack mentions a v16.1 bug where editing Dynamic Data block settings updated the internal page editor page name ([Rock Release Notes](https://www.rockrms.com/releasenotes)). The reporting recipe uses Dynamic Data for page-view reports ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)). Treat Dynamic Data as a privileged reporting surface:

- Confirm SQL scope and performance.
- Confirm parameters are constrained.
- Confirm output does not expose sensitive fields.
- Confirm the block is not publicly viewable unless the data is public.
- Confirm database functions and joins are compatible with the target Rock version.

### Page Builder

Page Builder is Rock’s editing experience for building pages and placing/configuring blocks. RockU includes Page Builder as a CMS topic ([Page Builder](https://community.rockrms.com/rocku/cms/page-builder)). Agents should distinguish:

- Page Builder UI changes.
- Page configuration changes.
- Block setting changes.
- Content changes inside a block.
- Theme/layout file changes.

When a user says “change this page,” determine which layer is actually required.

## 9. Themes Deep Dive

### What Themes Control

Themes control presentation but can also affect functionality. Inspect theme files for:

- Layout definitions and zone names.
- CSS variables, Bootstrap overrides, and utility classes.
- JavaScript loaded on every page.
- Icon fonts and SVG/icon libraries.
- Image and asset paths.
- Responsive behavior.
- Header/footer/nav implementations.
- Print styles.
- Dark/light mode assumptions if used.
- Custom Lava includes or reusable partials.

A CMS block can render correct markup and still look wrong because theme CSS changed. Conversely, a theme can hide or modify CMS block behavior by targeting generic selectors.

### Theme Selection

A site generally has a theme. Pages may have layout choices or overrides depending on version and configuration. To diagnose theme issues:

1. Identify the site theme.
2. Identify the page layout.
3. Inspect whether the block is in a zone exposed by that layout.
4. Inspect whether the theme has a compiled CSS pipeline.
5. Inspect whether custom CSS is stored in files, CMS blocks, or theme settings.
6. Inspect whether a CDN/browser cache is serving stale assets.

### Icon Systems

RockU includes Font Awesome 5 as a legacy topic and Tabler Icons as a newer CMS topic ([Font Awesome 5 Legacy](https://community.rockrms.com/rocku/cms/font-awesome-5-1), [Tabler Icons](https://community.rockrms.com/rocku/cms/tabler-icons)). Agents should verify the active icon system before changing icon classes. Do not assume a class like `fa fa-user`, `fas fa-user`, or `ti ti-user` works on every Rock version/theme.

For icon troubleshooting:

- Inspect rendered HTML class names.
- Inspect loaded CSS/font files.
- Inspect theme version.
- Inspect whether the icon library changed during an upgrade.
- Check browser console/network for missing font files.
- Replace icons using the site’s current standard.

### Asset Manager And Theme Assets

RockU includes Asset Manager in CMS training ([Asset Manager](https://community.rockrms.com/rocku/cms/asset-manager)). Asset questions require determining whether an image/script/file is:

- Stored under the web root/theme directory.
- Managed by Asset Manager.
- Stored as a BinaryFile.
- Served by `/GetImage.ashx`.
- Stored in an external media provider.
- Referenced from a content channel item attribute.
- Part of a plugin package.

When changing assets:

- Preserve the existing path if external pages reference it.
- Confirm dimensions and compression.
- Confirm alt text where rendered.
- Confirm cache busting.
- Confirm file type security.
- Confirm whether the asset is included in source control or only in database/file storage.

### JavaScript In CMS

Community recipes can include page-level scripts, including playful examples that add JavaScript through an HTML block ([Chip Cursor Pet recipe](https://community.rockrms.com/recipes/535)). Use those as evidence that Rock permits scripted CMS blocks, not as a recommendation. Page-level scripts can:

- Break other blocks.
- Leak data into the browser.
- Cause accessibility issues.
- Interfere with postbacks or Obsidian client behavior.
- Create mobile performance issues.
- Persist after the original campaign or event ends.

Require a security and maintainability review for scripts on public or high-traffic pages.

## 10. Content Channels Deep Dive

### When To Use Content Channels

Use content channels when content is structured, repeated, filtered, listed, dated, categorized, personalized, indexed, or reused. Examples include:

- Sermon series and messages.
- Blog posts or news articles.
- Events or announcements.
- Devotionals.
- Stories.
- Training modules.
- Media libraries.
- Homepage feature cards.
- Reusable call-to-action content.
- Mobile app content.
- Required watching content.

Use a simple HTML block when content is one-off, not reused, not filtered, not scheduled, and not security-sensitive.

### Content Channel Design

Design the channel before adding items:

1. Define the content item type in plain language.
2. Define required fields.
3. Define optional fields.
4. Decide if content is structured.
5. Decide if items need media.
6. Decide if items need categories, tags, parent-child relationships, or manual ordering.
7. Decide if items need approval.
8. Decide if items need start/expire dates.
9. Decide if items need RSS.
10. Decide if items need personalization.
11. Decide if items need search indexing.
12. Decide what pages list and display the content.
13. Decide who can author, approve, edit, and delete.

The source-code `ContentChannelBag` shows channel-level fields that align with these design questions: categories, child content channels, child manual ordering, content control type, personalization, RSS, icon, image attribute, indexing, structured content, tagging, root image directory, settings, and structured content tool value ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)).

### Content Channel Item Statuses

Display blocks may include only selected item statuses. The Content Channel Item View settings source includes `contentChannelItemStatuses`, described as statuses considered approved for display ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)). If an item exists but does not render, check status before changing templates.

### Dates And Ordering

The Content Channel Item List options source includes a date type and include-time behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/contentChannelItemListOptionsBag.d.ts)). Agents should inspect:

- Start date/time.
- Expire date/time.
- Date type used by the channel.
- Whether time is included.
- Manual ordering.
- Priority.
- Sort direction.
- Time zone assumptions.

For “missing” content, future start dates and expired items are common causes.

### Categories And Navigation

Content channels can have categories. Content Channel Navigation source snippets show category-driven initialization via page parameter and channel tiles with pending approval count for channels requiring approval ([ContentChannelNavigationBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts), [ContentChannelNavigationChannelBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationChannelBag.d.ts)). For navigation bugs:

- Inspect the category GUID parameter.
- Inspect channel-category relationships.
- Inspect whether the channel requires approval.
- Inspect user preferences if filters are saved server-side; the grid data request source notes filter values are read from person preferences on the server side ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationGetGridDataRequestBag.d.ts)).
- Inspect security for categories and items.

### Content Channel Item View

This block is central to content detail pages. Based on source settings, inspect:

- `cacheTags`.
- `contentChannelGuid`.
- `contentChannelItemStatuses`.
- `contentChannelQueryParameter`.
- `detailPage`.
- `isDisplayMostRecentEnabled`.
- `isItemMergeFieldEnabled`.
- `isLaunchWorkflowOnlyIfIndividualLoggedInEnabled`.
- `isLogInteractionsEnabled`.
- `isPageTitleUpdateEnabled`.
- `isWriteInteractionOnlyIfIndividualLoggedInEnabled`.
- `itemCacheDuration`.
- `launchWorkflowCondition`.
- `lavaTemplate`.
- `metaDescriptionAttributeValueKey`.
- Other metadata image/title fields available in the target UI.

These fields are from the source-code view model ([ContentChannelItemView settings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)). In production, verify exact labels and availability.

Operational cautions:

- If `isDisplayMostRecentEnabled` is on, a missing query parameter can still render content. This is useful for latest-message pages but dangerous if agents expect a 404-like blank state.
- If `isPageTitleUpdateEnabled` is on, content item title may replace page title.
- If item merge fields are enabled, Lava may process item content or attributes. Review for unsafe Lava and cache behavior.
- If interaction logging is enabled, test crawler exclusion and logged-in-only settings.
- If workflow launch is enabled, verify it does not trigger repeatedly on cached, refreshed, or bot requests.

### Content Channel Item List

The list block can expose operational columns such as status, security, reorder, priority, and dates. Source options include content channel ID, item name, date type, include time, content library enablement, manual ordering, license GUID, and show/hide flags for columns ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/contentChannelItemListOptionsBag.d.ts)).

RockU's Content Channel View lesson is useful training context for auditing channel item lists as both presentation and data exposure surfaces; inspect channel, item, block, page, route, and Lava template settings together ([Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view)).

If authors cannot manage content:

- Inspect block security.
- Inspect channel security.
- Inspect whether the user has Edit, not just View.
- Inspect version because v18.2 fixed a delete authorization issue in content channel blocks ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- Inspect whether filters are hiding items.
- Inspect whether items are in a different channel/type.

### Content Channel Detail

The detail/admin block uses option lists such as content channels, content channel types, content control types, available licenses, current page URL, and inherited content library item attributes ([ContentChannelDetailOptionsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelDetailOptionsBag.d.ts)). If the content channel edit screen behaves oddly:

- Confirm the target Rock version.
- Confirm content library feature availability.
- Confirm indexing is enabled if index fields are shown.
- Confirm an approver is configured if approval fields are present.
- Confirm inherited attributes from the type.
- Confirm categories are saved and modified timestamps update as expected; source comments note category changes may require setting modified date because changes are not tracked by ChangeTracker ([ContentChannelBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)).

## 11. Related Rock Areas: Lava, Security, Media, Content, Personalization

### Lava

Lava is the connective tissue of many CMS pages. Use it for rendering, conditional content, formatting, and controlled dynamic output. Treat Lava commands as privileged operations.

The Lava commands docs state that commands must be enabled for use and that commands can bypass built-in security and business logic ([Lava Commands](https://community.rockrms.com/lava/commands)). The command list in the source pack includes areas such as Cache, Entity, Delete Entity, Modify Entity, Interaction Write, JavaScript, Personalize, SQL, Stylesheet, Tag List, Web Request, Workflow Activate, and Render Lava Endpoint. For agents, that means a Lava-bearing CMS block can become a database writer, HTTP client, workflow launcher, or cache manipulator if commands are enabled.

Lava review checklist:

- Identify all Lava blocks on the page.
- Identify enabled commands per block.
- Search for page parameter usage.
- Search for SQL/entity/web request/workflow commands.
- Search for unencoded output.
- Search for person, group, financial, or children/youth data access.
- Confirm cache scope.
- Confirm anonymous behavior.
- Confirm failure behavior when merge fields are missing.

### Security

Security is layered. Do not stop at one layer.

Inspect:

- Site security.
- Page View/Edit/Administrate.
- Block View/Edit/Administrate.
- Content channel security.
- Content item security.
- Category security if relevant.
- File type and binary file security.
- Document type security.
- Data view/report security.
- Workflow type security.
- Custom block actions and API permissions.

The reporting documentation excerpt warns that report data can expose data beyond what a viewer might access elsewhere and places responsibility on report authors to secure report outputs ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6)). Apply that same principle to CMS pages that use Dynamic Data, Lava SQL, or Data Views.

### Media

Rock Media is treated as a CMS training area, including publishing, analytics, and required watching ([Publishing Rock Media](https://community.rockrms.com/rocku/cms/publishing-rock-media), [Rock Media Analytics](https://community.rockrms.com/rocku/cms/rock-media-analytics), [Rock Media Required Watching](https://community.rockrms.com/rocku/cms/rock-media-required-watching)). Media troubleshooting requires checking:

- Media element.
- Linked content item.
- Media file/provider.
- Thumbnail/image fields.
- Player block.
- Interaction/media analytics.
- Required watching rules.
- Person identity.
- Browser autoplay/device restrictions.
- CDN/provider errors.

### Content

Content is not always stored where the editor sees it. It may live in:

- HTML block content.
- Shared HTML content records.
- Content channel item fields.
- Content channel item attributes.
- Structured content payloads.
- Lava templates.
- Theme files.
- Asset Manager files.
- Binary files.
- Documents.
- External embeds.
- Plugin settings.

Before editing, determine the storage location and whether it is shared.

### Personalization

Personalization should be explicit and testable. RockU includes Personalization as CMS training ([Personalization](https://community.rockrms.com/rocku/cms/personalization)). Content channels can have personalization enabled in source configuration ([ContentChannelBag source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)). Lava commands include Personalize commands in the Lava command area ([Lava Commands](https://community.rockrms.com/lava/commands)).

Personalization guardrails:

- Provide a default fallback.
- Do not cache personalized output globally.
- Do not show sensitive segmentation labels to public users.
- Test every segment and anonymous state.
- Verify personalization rules against live data.
- Log decisions only if privacy policy allows it.
- Prefer server-side security for sensitive content, not merely personalized hiding.

## 12. Administration And Operational Guardrails

### Production Change Protocol

For production CMS changes:

1. Record the current page URL, page ID, block ID, block type, and content item ID.
2. Screenshot or export current settings when possible.
3. Identify shared content dependencies.
4. Identify all enabled Lava commands.
5. Identify cache settings.
6. Make the smallest reversible change.
7. Test as anonymous, authenticated normal user, and staff editor.
8. Test mobile and desktop.
9. Verify analytics/workflow side effects.
10. Clear only relevant caches.
11. Record what changed and how to roll back.

### Cache Guardrails

RockU includes Cache Tags as a CMS topic ([Cache Tags](https://community.rockrms.com/rocku/cms/cache-tags)). Source-code settings for Content Channel Item View include cache tags and item cache duration ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).

Cache checklist:

- Is the page output cached?
- Is the block output cached?
- Is the item view cached?
- Are cache tags configured?
- Is Lava using cache commands?
- Is a CDN or reverse proxy caching HTML/assets?
- Is the browser caching scripts/styles/images?
- Is the content item index stale?
- Is a persisted dataset stale?

When testing, avoid broad cache clears unless necessary. Prefer targeted cache tags, item cache invalidation, or page-specific refresh.

### Shared Content Guardrails

The v19.1 HTML Content deletion fix is a major operational warning: shared HTML content can be linked across blocks by context settings, and deletion behavior has had version-specific caveats ([Rock Release Notes](https://www.rockrms.com/releasenotes)). Before deleting HTML Content blocks:

- Check context name.
- Check whether other blocks use the same content.
- Check Rock version.
- Export content.
- Prefer unpublishing/hiding over deletion when uncertain.
- Test linked blocks afterward.

### Community Recipe Guardrails

Community recipes can be useful but are not core-reviewed. Recipe pages explicitly warn that recipes may affect performance or security ([Search Rock Pages](https://community.rockrms.com/recipes/432), [Easy Page Views Reporting](https://community.rockrms.com/recipes/261)). Before adapting a recipe:

- Remove unrelated code.
- Review SQL for performance and injection risk.
- Review Lava commands.
- Review page/block security.
- Test on a copy.
- Confirm version compatibility.
- Document local modifications.

### Reporting Guardrails

Dynamic Data and reports can expose sensitive data. Official reporting documentation says report authors are responsible for considering the security of the data they provide and notes that report data can bypass normal row-level security expectations for valid performance and operational reasons ([Taking Off With Reporting](https://community.rockrms.com/documentation/bookcontent/6)). For CMS reports:

- Put reports on internal pages.
- Restrict View and Edit.
- Avoid exposing person, giving, child, group, or browsing data publicly.
- Add date filters.
- Add row limits.
- Avoid unbounded interaction scans.
- Validate SQL against live schema.

### Upgrade Guardrails

Before and after Rock upgrades:

- Review CMS release notes for the current and target versions.
- Test public pages, content item details, content authoring, Dynamic Data, media playback, personalization, and page views.
- Test block security behavior.
- Test deletion/editing permissions for content channel blocks.
- Test breadcrumbs for direct content item links if near v17.1 behavior.
- Test HTML shared content deletion behavior if near v19.1 behavior.
- Test entity document access if using document upload workflows.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Rock Source Repository

Rock’s source repository is SparkDevNetwork/Rock, described as an open-source CMS, RMS, and ChMS ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). Use source-code records as landmarks for implementation, but verify branch and version.

### Obsidian Blocks

Modern Obsidian blocks are composed of:

- C# block for server-side logic and database access.
- TypeScript component for rendering and client interactions.
- Block actions as server-call endpoints from the TypeScript client.

This structure is documented in the Obsidian Creating Blocks developer guide ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)). For CMS agents, this means a setting shown in a TypeScript bag often maps to a C# block setting or action contract.

### Content Channel Source Landmarks

Useful source paths from the pack:

- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts` for channel fields ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)).
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelDetailOptionsBag.d.ts` for detail UI option lists ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelDetailOptionsBag.d.ts)).
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/contentChannelItemListOptionsBag.d.ts` for item list options ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/contentChannelItemListOptionsBag.d.ts)).
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts` for item view settings ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts` for interaction token behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts)).
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/*` for navigation and category selection ([navigation bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts), [channel bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationChannelBag.d.ts), [grid request bag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationGetGridDataRequestBag.d.ts)).

### Web Forms CMS Block Landmark

`ContentChannelItemPersonalListLava.ascx.cs` is a classic CMS block example. It defines block attributes for Content Channel, Max Items, Detail Page, and Lava Template and displays content items for the current person ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs)). Use this to remember that not all CMS blocks are Obsidian and that many legacy blocks are Lava-template driven.

### Mobile CMS Landmark

The Mobile Lava Item List block has configuration for Page Size, Detail Page, List Template, and List Data Template, with merge fields including page number and page size ([Lava Item List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/lava-item-list)). If a CMS concept appears in a mobile app, inspect mobile block configuration separately; web page settings do not automatically explain mobile behavior.

### Lava Command Landmark

The Lava commands documentation is the required safety reference for any CMS block using commands ([Lava Commands](https://community.rockrms.com/lava/commands)). In reviews, list the commands enabled and justify each one.

## 14. Reporting, Analytics, And Model Map

### Page View Analytics

Rock can log page views when enabled for a site. The community recipe for page-view reporting starts by enabling Log Page Views under the site’s advanced settings and then uses filters for page, person, and date range with Dynamic Data ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)).

Operational checks:

- Confirm site setting.
- Confirm interaction component/entity model in the target version.
- Confirm page IDs.
- Confirm person identifiers.
- Confirm date range and time zone.
- Confirm anonymous handling.
- Confirm crawler handling.
- Confirm row counts before rendering broad reports.

### Content Item Analytics

Content Channel Item View can log interactions depending on settings. Source-code options show a server-issued interaction token and sessionStorage de-duplication behavior ([ContentChannelItemView options source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts)). The settings source includes whether to log interactions and whether to write interactions only for logged-in users ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).

If analytics are missing:

- Confirm item view block settings.
- Confirm item resolved.
- Confirm viewer eligibility.
- Confirm token present.
- Confirm no crawler exclusion.
- Confirm browser storage/cookies.
- Confirm interaction write path.
- Confirm jobs or reports consuming interactions.

### Media Analytics

RockU includes Rock Media Analytics as a CMS topic ([Rock Media Analytics](https://community.rockrms.com/rocku/cms/rock-media-analytics)). When reporting on media:

- Distinguish page view, item view, media play, media progress, and required completion.
- Confirm person identity.
- Confirm media element linkage.
- Confirm player integration.
- Confirm analytics event ingestion.
- Confirm any aggregation jobs.

### Model Map Usage

When the source material is thin, use Model Map or live schema inspection. For CMS tasks, inspect entities and columns for:

- Site.
- Page.
- PageRoute.
- Block.
- BlockType.
- Attribute.
- AttributeValue.
- HtmlContent or equivalent content storage.
- ContentChannelType.
- ContentChannel.
- ContentChannelItem.
- Category.
- BinaryFile.
- FileType.
- Document.
- DocumentType.
- Interaction.
- InteractionComponent.
- InteractionChannel.
- MediaElement or related media tables.
- Personalization segment entities if used.

Do not invent column names. If writing SQL, verify schema in the target database first.

## 15. Version And Release Caveats

### v19.1 CMS Caveat: HTML Content Shared Deletion

Release notes state that deleting an HTML Content block could also remove shared content for other linked blocks using the same Context Name setting. The fix preserves shared content by allowing the source HtmlContent block ID to be null when a block is deleted ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Agent action: Before deleting HTML Content blocks, inspect shared context/content dependencies and Rock version.

### v18.2 CMS Caveat: Content Channel Delete Authorization

Release notes state that multiple blocks interacting with Content Channels had a security issue where individuals with only View permissions could delete content items; delete is now limited to Edit access ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Agent action: On versions before the fix, treat content channel management blocks as higher risk. Verify permissions and avoid exposing management blocks to broad audiences.

### v18.2 Entity Document Caveat

Release notes state that files uploaded through Entity Document Add workflow action were not properly linked to parent Document, causing access checks to fall back to File Type security instead of Document Type security. The fix links files correctly and copies security for default document types when no document type security exists ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Agent action: For CMS pages exposing documents, verify document linkage and security after upgrades or workflow uploads.

### v17.1 Content Channel Breadcrumb Caveat

Release notes state that Content Channel Item View breadcrumbs could fail when accessing a page directly by link rather than by navigating through the site; this produced a Page Not Found error when clicking a parent breadcrumb ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Agent action: If direct content links have breadcrumb problems, check Rock version and block configuration.

### v16.1 Dynamic Data Caveat

Release notes state that editing Dynamic Data block settings could update the page name of the internal page editor page ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

Agent action: If page names unexpectedly change around Dynamic Data configuration, check version and audit logs.

### Icon Version Caveats

RockU lists Font Awesome 5 as legacy and Tabler Icons as a CMS topic ([Font Awesome 5 Legacy](https://community.rockrms.com/rocku/cms/font-awesome-5-1), [Tabler Icons](https://community.rockrms.com/rocku/cms/tabler-icons)). Agent action: verify active icon library after upgrades.

### Source Branch Caveat

GitHub source snippets in the pack are from the `develop` branch at retrieval time. They may represent future or unreleased behavior relative to a production Rock instance. Use them as implementation landmarks and field-name hints, then verify in live Rock.

## 16. Implementation Playbooks

### Playbook: Diagnose A Missing Page

1. Confirm exact URL, host, and user state.
2. Resolve host to Site.
3. Resolve URL to Page or Short Link.
4. Confirm page exists and is active.
5. Confirm page route.
6. Confirm page security.
7. Confirm layout renders.
8. Confirm blocks exist in rendered zones.
9. Confirm no redirect loop or route conflict.
10. Test as anonymous and staff.
11. Inspect Rock exception logs and web server logs.

### Playbook: Diagnose A Block That Does Not Render

1. Capture page ID and block ID.
2. Confirm block zone exists in layout.
3. Confirm block View security.
4. Confirm block type exists and is not obsolete for the version.
5. Confirm block settings are valid.
6. Check required page parameters.
7. Check Lava errors.
8. Check enabled Lava commands.
9. Check cache.
10. Check browser console/network.
11. Check server exception logs.
12. Test with a minimal setting/template if safe.

### Playbook: Safely Modify Advanced HTML

1. Export current content and block settings.
2. Identify shared context.
3. Identify enabled commands.
4. Identify all page parameters used.
5. Identify all data access in Lava.
6. Remove unnecessary commands.
7. Make scoped change.
8. Test anonymous and authenticated.
9. Check console and server logs.
10. Clear targeted cache.
11. Record rollback content.

### Playbook: Build A Content Channel

1. Define content purpose and owners.
2. Create or select Content Channel Type.
3. Define attributes.
4. Create Content Channel.
5. Configure categories, RSS, personalization, indexing, content library, image/summary/author attributes as needed.
6. Set channel security.
7. Add authoring/list/admin page if needed.
8. Add listing page.
9. Add detail page.
10. Configure item view statuses, query parameter, cache, template, and interactions.
11. Add sample items in every status/date case.
12. Test public display.
13. Test authoring and approval.
14. Document IDs, pages, and rollback.

### Playbook: Audit A Public CMS Page For Security

1. List all blocks.
2. Identify block types.
3. Review View/Edit/Administrate for page and blocks.
4. Review all Lava commands.
5. Review SQL/entity/web request/workflow usage.
6. Review exposed data fields.
7. Review forms and upload controls.
8. Review content channel item security.
9. Review linked files/documents.
10. Review JavaScript for external calls or data leakage.
11. Test anonymous.
12. Test low-privilege authenticated.
13. Confirm no edit/delete actions are available.
14. Confirm server rejects unauthorized block actions.

### Playbook: Add Content Item Analytics

1. Confirm item view block.
2. Enable interaction logging if appropriate.
3. Decide whether anonymous views count.
4. Confirm token/options behavior in current version.
5. Confirm known crawlers are excluded if intended.
6. Confirm site interaction settings.
7. Test one authenticated view and one anonymous view.
8. Query/report interactions after expected processing.
9. Document metric definition.

### Playbook: Troubleshoot Media Required Watching

1. Confirm media element linked to content item.
2. Confirm player renders.
3. Confirm viewer identity.
4. Confirm required watching rule.
5. Confirm progress/completion events are written.
6. Confirm analytics processing.
7. Confirm browser/device supports playback tracking.
8. Confirm media duration and completion threshold.
9. Test with a fresh user.
10. Inspect exceptions and network calls.

## 17. Troubleshooting Decision Tree

### The Page Returns Not Found

- If the URL is a short link, inspect Short Links first ([Short Links](https://community.rockrms.com/rocku/cms/short-links)).
- If the host is wrong, inspect Site domains.
- If the route is wrong, inspect page routes.
- If the page exists but user lacks View, inspect page security.
- If only content item detail links fail, inspect Content Channel Item View query parameter and item status.
- If breadcrumbs cause Page Not Found on direct item links, check version around the v17.1 breadcrumb fix ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### The Page Loads But Content Is Missing

- Check block exists and is in a rendered zone.
- Check block View security.
- Check block settings.
- Check content channel/item status and dates.
- Check item security.
- Check category/page parameter filters.
- Check Lava errors.
- Check cache duration and cache tags.
- Check personalization conditions.
- Check anonymous versus authenticated context.

### The Wrong Content Shows

- Check route-to-page mapping.
- Check block query parameter name.
- Check `display most recent` behavior on content item view.
- Check listing/detail page configuration.
- Check cache.
- Check shared HTML context.
- Check personalization.
- Check whether content was edited in a different channel/item than the one displayed.

### Authors Cannot Edit Content

- Check page/block Edit security.
- Check Content Channel security.
- Check item security.
- Check whether management block is the correct version/type.
- Check approval configuration.
- Check browser console/server logs.
- If delete buttons behave unexpectedly, check the v18.2 Content Channel delete authorization fix ([Rock Release Notes](https://www.rockrms.com/releasenotes)).

### Lava Works For Staff But Not Public

- Check block View security.
- Check enabled commands.
- Check whether Lava depends on `CurrentPerson`.
- Check whether public user lacks entity access.
- Check whether a command is disabled in the public block instance.
- Check caching by person.
- Check null handling.

### Analytics Are Empty

- For page views, confirm site Log Page Views is enabled ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)).
- For content items, confirm item view interaction logging settings ([ContentChannelItemView settings source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts)).
- Confirm user identity rules.
- Confirm crawler exclusion.
- Confirm interaction token generation and de-duplication behavior ([ContentChannelItemView options source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts)).
- Confirm reporting query filters and date range.
- Confirm aggregation jobs if used.

### Files Or Documents Are Accessible To The Wrong Users

- Inspect File Type security.
- Inspect BinaryFile.
- Inspect Document and Document Type.
- Inspect entity document linkage.
- Check v18.2 document upload linkage fix if using Entity Document Add workflow action ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- Test direct file URLs and document URLs.
- Restrict public links until verified.

### Styling Or Icons Are Broken

- Confirm theme and layout.
- Confirm CSS/JS files load.
- Confirm icon library: Font Awesome legacy versus Tabler Icons ([Font Awesome 5 Legacy](https://community.rockrms.com/rocku/cms/font-awesome-5-1), [Tabler Icons](https://community.rockrms.com/rocku/cms/tabler-icons)).
- Confirm compiled theme assets are current.
- Confirm CDN/browser cache.
- Confirm no CMS block injected conflicting CSS/JS.

## 18. Agent Task Recipes

### Recipe: “Find The Block That Controls This Text”

1. Open the page as staff with block edit controls.
2. Identify visible block names and zones.
3. Search page blocks for HTML Content, Advanced HTML, Content Channel Item View, Dynamic Data, and custom Lava blocks.
4. If content is in a content channel, identify channel and item.
5. If content is in a shared HTML context, identify all linked blocks.
6. Export current content before editing.
7. Make a scoped change.
8. Test as public.

### Recipe: “Why Is This Content Item Not Public?”

Inspect:

- Content channel ID/GUID.
- Item status.
- Start and expire dates.
- Block allowed statuses.
- Item and channel security.
- Category filters.
- Query parameter.
- Cache.
- Personalization.
- Direct link behavior.
- Version caveats around Content Channel Item View.

### Recipe: “Can I Enable SQL In This HTML Block?”

Default answer: only after review.

Verify:

- Page is staff-only or data is public.
- SQL command is strictly necessary.
- Query is read-only.
- Query is bounded.
- Query does not expose sensitive data.
- Parameters are constrained.
- Output is encoded.
- Block security is locked down.
- A Dynamic Data/reporting page would not be safer.
- The enabled command list is minimal.

The Lava commands documentation explicitly warns that commands can bypass built-in security and business logic ([Lava Commands](https://community.rockrms.com/lava/commands)).

### Recipe: “Add A Detail Page For Channel Items”

1. Create detail page.
2. Add Content Channel Item View.
3. Configure content channel.
4. Configure query parameter.
5. Configure allowed statuses.
6. Configure Lava template.
7. Configure cache duration and tags.
8. Configure page title update.
9. Configure meta description/image fields if available.
10. Configure interaction logging if needed.
11. Link list page’s detail page setting to this page.
12. Test direct URL and list navigation.
13. Test invalid item ID/key.
14. Test future/pending/expired items.

### Recipe: “Review A Community Recipe Before Installing”

1. Read recipe disclaimer and treat it as unreviewed community code ([Search Rock Pages](https://community.rockrms.com/recipes/432)).
2. Identify every SQL query.
3. Identify every Lava command.
4. Identify every script/style injection.
5. Identify page/block security assumptions.
6. Identify version assumptions.
7. Test in non-production.
8. Replace broad permissions with least privilege.
9. Document local changes.

### Recipe: “Build A Page View Report”

1. Confirm site Log Page Views.
2. Create internal reporting page.
3. Restrict View to staff/reporting role.
4. Add filters for page, person, and date range.
5. Add Dynamic Data or report block.
6. Use schema-verified SQL.
7. Add date limits and defaults.
8. Validate against known test views.
9. Document whether anonymous, crawler, and duplicate views are included.

The community page-view recipe provides the basic pattern but should be hardened for security and performance ([Easy Page Views Reporting](https://community.rockrms.com/recipes/261)).

### Recipe: “Troubleshoot Required Watching”

1. Confirm media item plays.
2. Confirm required watching feature is configured.
3. Confirm current person is identified.
4. Confirm media analytics are recorded.
5. Confirm completion threshold.
6. Confirm viewer is in required audience.
7. Confirm no browser restrictions block events.
8. Confirm reports use correct media interaction data.
9. Test with a new user.

RockU identifies Required Watching as part of the CMS/media learning path ([Rock Media Required Watching](https://community.rockrms.com/rocku/cms/rock-media-required-watching)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `164`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms' single-page form model, which matters when validating or troubleshooting nested form behavior. | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| official | implementation_pattern | An Obsidian block combines a C# block, a TypeScript component, and block actions, so developer guidance should connect server logic, client UI, and action endpoints instead of treating a block as one file. | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| rocku-confirmed | operational_guidance | Adding pages and blocks changes both navigation and authorization; agents should inspect site, page hierarchy, route, block type, zone, and inherited security before publishing. | [source](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) |
| rocku-confirmed | operational_guidance | Content Channel View pages should be reviewed as both CMS presentation and data exposure surfaces because channel item lists can reveal titles, dates, attributes, or detail links. | [source](https://community.rockrms.com/rocku/content-channels/content-channel-view) |
| rocku-confirmed | operational_guidance | Advanced HTML blocks are powerful CMS surfaces because they can combine markup, Lava, context, and sometimes enabled commands; treat edit access as privileged. | [source](https://community.rockrms.com/rocku/cms/advanced-html-block) |
| rocku-confirmed | operational_guidance | When diagnosing personalization, inspect the audience rule, person data used by the rule, fallback content, cache behavior, and the exact logged-in or anonymous state being tested. | [source](https://community.rockrms.com/rocku/cms/personalization) |
| rocku-confirmed | operational_guidance | Content Components should be treated as reusable CMS building blocks; changes can affect every page or theme area where the component is used. | [source](https://community.rockrms.com/rocku/cms/content-component) |
| rocku-confirmed | operational_guidance | Personalization should be reviewed as conditional content delivery, not as a security substitute; hidden or targeted content still needs proper page, block, and entity authorization. | [source](https://community.rockrms.com/rocku/cms/personalization) |
| rocku-confirmed | operational_guidance | Before editing a content component, identify where it is rendered, what content it owns, and whether the component is part of a public, staff, or theme-managed surface. | [source](https://community.rockrms.com/rocku/cms/content-component) |
| rocku-confirmed | risk | When diagnosing a missing or exposed page, compare the page route, parent-page security, block security, and the specific user context instead of assuming the route alone controls access. | [source](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) |
| rocku-confirmed | risk | When reviewing an Advanced HTML block, inspect page/block security, enabled Lava commands, query-string or context inputs, and whether the output exposes sensitive entity data. | [source](https://community.rockrms.com/rocku/cms/advanced-html-block) |
| rocku-confirmed | risk | When troubleshooting content visibility, inspect channel, item, block, page, route, and Lava template settings instead of assuming the channel item itself is the only security boundary. | [source](https://community.rockrms.com/rocku/content-channels/content-channel-view) |
| More |  | 152 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `49`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Adding Content Transcript Insight](https://community.rockrms.com/rocku/content-channels/adding-content) | approved_for_public_distillation | 2 | media-insight:de94e4d41ee28a38 |
| [Adding Pages and Blocks Transcript Insight](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) | approved_for_public_distillation | 2 | media-insight:7848aa46e6ac3794 |
| [Advanced HTML Block Transcript Insight](https://community.rockrms.com/rocku/cms/advanced-html-block) | approved_for_public_distillation | 2 | media-insight:2cf056c2b84e6365 |
| [Asset Manager Transcript Insight](https://community.rockrms.com/rocku/cms/asset-manager) | approved_for_public_distillation | 1 | media-insight:313e84f7d769f286 |
| [CMS Components Transcript Insight](https://community.rockrms.com/rocku/cms/cms-components) | approved_for_public_distillation | 2 | media-insight:47ad3e0c6f28cb69 |
| [Cache Tags Transcript Insight](https://community.rockrms.com/rocku/cms/cache-tags) | approved_for_public_distillation | 1 | media-insight:5c0dae456ef72854 |
| [Content Channel Types and Content Channels Transcript Insight](https://community.rockrms.com/rocku/content-channels/content-channel-types-and-content-channels) | approved_for_public_distillation | 2 | media-insight:6d0e9b93da800c18 |
| [Content Channel View Transcript Insight](https://community.rockrms.com/rocku/content-channels/content-channel-view) | approved_for_public_distillation | 2 | media-insight:7b84e33ae0a6eee9 |
| More |  | 41 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

### Primary Official / Core Sources

- RockU CMS course: official training coverage for Rock as CMS, pages, blocks, Page Builder, HTML/Advanced HTML, cache tags, short links, family pre-registration, content component, asset manager, persisted datasets, entity documents, phone lookup, Rock Media, personalization, interactive experiences, and icons ([RockU CMS](https://community.rockrms.com/rocku/cms)).
- HTML Block and Advanced HTML Block training are the main official CMS-authoring landmarks ([HTML Block](https://community.rockrms.com/rocku/cms/html-block), [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)).
- Page Builder and Adding Pages and Blocks are the main page construction landmarks ([Page Builder](https://community.rockrms.com/rocku/cms/page-builder), [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy)).
- Lava Commands documentation is the main security reference for command-enabled CMS templates ([Lava Commands](https://community.rockrms.com/lava/commands)).
- Obsidian Creating Blocks is the main developer reference for modern block anatomy ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).
- Release notes are required for version-specific CMS behavior ([Rock Release Notes](https://www.rockrms.com/releasenotes)).
- SparkDevNetwork/Rock is the source repository landmark ([GitHub](https://github.com/SparkDevNetwork/Rock)).

### Source-Code Landmarks Used

- Content Channel Detail data model fields ([ContentChannelBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)).
- Content Channel Detail options ([ContentChannelDetailOptionsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelDetailOptionsBag.d.ts)).
- Content Channel Item List options ([ContentChannelItemListOptionsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/contentChannelItemListOptionsBag.d.ts)).
- Content Channel Item View settings and options ([settings](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts), [options](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewOptionsBag.d.ts)).
- Linked media request/response and linked media element model ([request](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsRequestBag.cs), [response](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsResponseBag.cs), [linked element](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/LinkedMediaElementBag.cs)).
- Content Channel Navigation category and grid request models ([navigation](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts), [channel](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationChannelBag.d.ts), [grid request](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationGetGridDataRequestBag.d.ts)).
- Classic Web Forms Lava content item list block ([ASCX](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx), [code-behind](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs)).

### Secondary And Community Sources

- Search Rock Pages recipe for Page Parameter Filter page-search pattern; use only after security/performance review ([recipe](https://community.rockrms.com/recipes/432)).
- Easy Page Views Reporting recipe for site page-view logging and Dynamic Data reporting pattern; use only after hardening ([recipe](https://community.rockrms.com/recipes/261)).
- Chip Cursor Pet recipe as evidence that HTML blocks can inject JavaScript; not a best-practice source for production scripting ([recipe](https://community.rockrms.com/recipes/535)).
- Triumph Tech GitHub Spotlight is secondary release commentary and should not override official release notes or source code ([GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-1242025)).

### Dependencies To Other Guides

Use the Lava guide when:

- A block uses Lava commands.
- A template reads page parameters.
- A template queries entities or SQL.
- A template writes interactions or launches workflows.
- A template uses personalization commands.

Use the Security guide when:

- A page or block is public.
- Content authoring is delegated.
- Reports or Dynamic Data expose records.
- Documents or files are linked.
- Content Channel management blocks are visible to non-admins.

Use the Media guide when:

- Content items link media elements.
- Analytics, required watching, or playback is involved.
- Files, providers, thumbnails, or media permissions are involved.

Use the Content guide when:

- Designing content channel types.
- Migrating content.
- Standardizing attributes.
- Building structured content.

Use the Personalization guide when:

- Content varies by person, segment, campus, group, or behavior.
- Caching might mix personalized output.
- Anonymous fallback content matters.
