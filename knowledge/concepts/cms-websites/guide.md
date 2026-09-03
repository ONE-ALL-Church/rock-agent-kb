---
id: authored-cms-websites
title: CMS And Websites
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "1f67abb67d8c73e24ead44780fa055f9b88dd0ca72678166f7d20bfca080fb56"
---

# CMS And Websites

## Agent Summary

Rock builds websites from a hierarchy of sites, themes, pages, layouts, zones, and blocks. A request is routed to a page, the page is assembled for the current visitor, and each block contributes content or behavior. This means a CMS change can affect navigation, authorization, presentation, data exposure, caching, and performance at the same time. [Rock website architecture](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/intro-to-websites-in-rock)

Use these operating rules:

- Treat a route as an address, not an authorization boundary. For missing or exposed content, inspect the site, page hierarchy, inherited page security, block security, context, and exact visitor state. [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy)
- Confirm block scope before changing it. A page block affects one page, a layout-scoped block affects every page using that layout, and a site-scoped block affects every page in the site. [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)
- Treat HTML and Lava authorship as privileged. Lava Commands can bypass built-in security or business logic, and HTML blocks begin with no commands enabled unless configured. [Lava Commands security](https://community.rockrms.com/lava/commands/getting-started)
- Treat personalization as conditional delivery, not security. Targeted content still requires page, block, and entity authorization. [Personalization](https://community.rockrms.com/rocku/cms/personalization)
- Review Content Channel View pages as both presentation and data-exposure surfaces. Lists can reveal titles, dates, attributes, and detail links even when the full item is elsewhere. [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view)
- Locate every render point before editing reusable content components, layout blocks, site blocks, or shared HTML content. [Content Component](https://community.rockrms.com/rocku/cms/content-component)
- Separate saved configuration from verified behavior. Test the anonymous visitor, intended authenticated role, and administrator independently.

## Scope And Boundaries

This guide covers website structure, site creation, routes, pages, layouts, blocks, HTML and Lava surfaces, themes, content channels, personalization, landing pages, SEO-related configuration, media presentation, parameter-driven pages, Helix and Obsidian CMS boundaries, website forms, mobile content boundaries, caching, and performance.

Detailed Lava syntax and entity-write behavior belong in the Lava concept. Security role design belongs in Security and Permissions. Media ingestion and analytics belong in Media. Content modeling belongs in Content. Audience construction belongs in Personalization. Mobile shell migration belongs in Mobile. This guide addresses those topics only where they change the behavior or review requirements of a CMS surface.

Communication composition and sender training remain in Communications even when templates contain Lava. Workflow design remains in Workflows except where a website must hand slow content processing to a background workflow.

No organization-specific configuration is asserted here. The evidence pack includes reviewed read-only validation that the relevant CMS, authorization, content-channel, and workflow surfaces existed in one connected installation; that validation did not prove that any particular site, route, block, audience, or item was configured correctly.

## Mental Model

A useful CMS model is:

1. **Site** selects a related collection of pages and its site-level configuration, including theme, domains, login page, encryption, personalization, tracking, indexing, and shared head content.
2. **Route** maps an address to a page. Routes are site-scoped, can contain parameters, and can coexist with the default `/page/{id}` address.
3. **Page** supplies hierarchy, properties, inherited authorization, layout selection, and page-level metadata.
4. **Theme** supplies styling resources and defines layouts.
5. **Layout** defines named zones in which blocks may be placed.
6. **Block** supplies content or application behavior and may be scoped to a page, layout, or site.
7. **Context and parameters** tell context-aware blocks which entity or filter state applies to the request.
8. **Content source** may be HTML content, a content channel, a content component, a Lava application, a media element, or another block-specific data source.
9. **Visitor state** includes route, query or virtual parameters, authentication, authorization, personalization data, context, cookies, and cache state.
10. **Rendered output** is the final public or staff-facing response. It must be reviewed separately from the saved configuration.

Rock dynamically assembles pages rather than treating each page as a server file. Page hierarchy supports navigation, while the visitor’s permissions and context can change what the same page renders. [Intro to Websites in Rock](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/intro-to-websites-in-rock)

## Sites, Routes, And Navigation

Create a distinct Rock site for a related collection of pages that shares configuration and visual treatment. Site creation begins under `Admin Tools > Websites`. The documented sequence recommends allowing Rock to create the root default page rather than creating that page prematurely, then configuring the site’s theme, domains, login and error pages, encryption, short-link eligibility, tracking, personalization, icon, shared header content, and indexing behavior as applicable. Marking a site inactive removes it from the normal site list but does not itself stop the site from functioning. [Create a Site](https://community.rockrms.com/documentation/digital-publishing/websites/sites/create-a-site)

Routes provide friendly addresses for dynamically assembled pages. A page can have multiple routes, and advanced routes can map path segments to parameters, such as an item identifier. Routes are scoped to a site, although global routes and fallback matching can affect resolution. The documented routing order begins with an explicit `/page/{id}`, then considers matching page routes and short links for the current site before older matches elsewhere and finally the 404 page. Multiple indexed routes for identical content can create duplicate-page SEO problems. [Routes](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/routes)

A route that resolves successfully does not prove that the visitor should see the page or every block on it. When auditing a route:

- Resolve the domain to the intended site.
- Identify the exact page and its parent hierarchy.
- Inspect page authorization, including inherited rights.
- Inspect block authorization and scope.
- Identify route and query parameters that establish context.
- Test as the actual visitor class, including anonymous users.
- Confirm redirects, short links, and alternate routes do not expose a different path to the same feature.

Domain login sharing can let authentication cookies apply across sites under a common domain, but cookie behavior should not be confused with authorization. Site-specific and shared cookies can coexist, which can also affect logout and reproduction steps. [Cookies](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/cookies)

## Pages, Layouts, Zones, And Blocks

Pages are arranged in a parent-child hierarchy and assigned a layout. The theme defines available layouts, and each layout defines the zones where blocks can live. Standardized layout names make it easier to change a site’s theme while retaining compatible page structure. Custom layouts can be created, but departing from the standard layout conventions can reduce theme portability. [Page Layouts](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts)

Adding or moving a block requires an explicit scope decision:

- **Page scope:** the block appears on the current page.
- **Layout scope:** the block appears on every page using that layout.
- **Site scope:** the block appears on every page in the site.

The block configuration interface separates content editing, block settings, block security, movement, and deletion. Block security controls viewing as well as editing or administration. Page security is hierarchical: when a page has no explicit rights, it inherits from its ancestors and ultimately the site. [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)

Copying a page also copies its blocks, child-page hierarchy, and child-page blocks. Rock rewires references among the copied pages and blocks, but the resulting settings still require review before publication. Inspect routes, linked detail pages, workflow types, content channels, parameter names, block scope, security, and any references that should continue pointing outside the copied hierarchy. [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)

## HTML Content, Scheduling, And Shared Components

The HTML Content block supports direct content editing and can use code or WYSIWYG editing modes. Content can have a display date range. The documented end date is exclusive: content configured through January 7 would use January 8 as its end date. [Intro to the HTML Content Block](https://community.rockrms.com/documentation/digital-publishing/websites/html-content-block/intro-to-the-html-content-block)

Its settings can also control document and image roots, user-specific folders, cache duration, context, approval, versioning, markup validation, and protected pre/post content. Important operational consequences include:

- Context-dependent content should not be served from a cache configuration that erases the needed variation.
- Reusing the same context name across HTML blocks shares their content, so one edit can affect multiple layouts or pages.
- Enabling approvals also enables versioning so previously approved content can remain visible while a revision awaits approval.
- With versioning and date ranges, Rock selects the most recently approved version applicable to the date range.
- Pre/post content can protect structural markup while allowing staff to edit the central content. [Configure Block Settings](https://community.rockrms.com/documentation/digital-publishing/websites/html-content-block/configure-block-settings)

Content Components are reusable CMS building blocks. Before editing one, identify every page or theme area where it renders, what content it owns, and whether its consumers are public, staff-only, or theme-managed. A change is not local merely because it was initiated from one visible page. [Content Component](https://community.rockrms.com/rocku/cms/content-component)

## Advanced HTML, Lava, And Context

Advanced HTML surfaces can combine markup, Lava, page parameters, entity context, and enabled commands. Treat edit access as privileged. A safe review covers:

- Page and block view, edit, and administrative authorization.
- Block scope and every render point.
- Enabled Lava Commands.
- Query-string, route, page-parameter, and context inputs.
- Whether output exposes person, group, financial, authentication, or other sensitive entity data.
- Cache behavior across users and contexts.
- Who can edit any stored value that is later processed as Lava.

Lava Commands can bypass Rock’s built-in security and business logic. Enable only the commands required by the specific execution surface; do not infer that a command is available because it worked in another block, communication, tester, or endpoint. HTML blocks have no commands enabled by default unless configured. [Lava Commands security](https://community.rockrms.com/lava/commands/getting-started)

Context lets the same page render for different entities. A page context can come from a query parameter or block code. For example, an HTML block configured for Group context can consume the page’s configured group parameter and access that group through `Context`. [Intro to Context](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/intro-to-context), [HTML Block Context](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/html-block-context)

A Campus Context Setter can change campus-specific content without navigating to a different page. Its settings can include a default campus, allowed campus types, and an option that updates the person’s family campus when the selection changes. Review that write-affecting option before treating the block as a display-only selector. [Campus Context Setter](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/campus-context-setter)

The Person Profile supplies Person context to compatible blocks, including HTML blocks placed on that page. That convenience increases the importance of inspecting output and block authorization before displaying person data. [Context on the Person Profile](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile)

A reviewed community pattern reports that stored Lava or shortcodes may appear as literal text unless intentionally passed through a Lava-processing step such as `RunLava`. If execution is intended, first validate edit ownership, enabled commands, authorization, and public exposure. This pattern requires local reproduction and should not be enabled merely to suppress visible shortcode syntax. [Other Lava filters](https://community.rockrms.com/lava/filters/other-filters)

## Personalization

Personalization conditionally selects content for an audience. It does not grant or deny access. Page, block, and underlying entity authorization remain the security boundaries. [Personalization](https://community.rockrms.com/rocku/cms/personalization)

When targeted content is wrong or inconsistent, inspect these separately:

1. Whether personalization is enabled for the site.
2. The audience rule.
3. The person or visitor data used by the rule.
4. Whether the visitor is anonymous or logged in.
5. Visitor-tracking prerequisites where the design depends on them.
6. The content selected for the audience.
7. Fallback content.
8. Page, block, and entity authorization.
9. Cache behavior.
10. The exact route and context used in the test.

An administrator’s result is not evidence for an anonymous visitor or ordinary member. Use representative actor states and retain fallback behavior for visitors who do not match an audience or lack the data required by a rule.

## Themes And Styling

Themes are assigned at site level and provide styling resources and layouts. Installed themes can be reviewed under `Admin Tools > CMS Configuration > Themes`. Depending on the theme, Rock can expose compilation, copying, deletion, and editable variables. System themes cannot be deleted, and a theme designer may disable compilation or provide no editable variables. [Themes](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/themes)

Saving in Theme Styler saves the selected changes and compiles Less into CSS. CSS Overrides are appended after compiled styles, allowing them to take precedence in normal CSS cascade conditions. This does not guarantee that every override wins; selector specificity and other CSS behavior still apply.

Do not customize upgrade-managed global styles or core themes in place. The official guidance says global styles, the Rock internal theme, the Stark theme, and the root global scripts area can be overwritten or otherwise conflict with updates. Copy a theme before customization and place custom CSS, Less, or scripts in an appropriate custom theme or plugin location. The shipped external site should be treated as a reference rather than the long-term public site because future Rock updates can add pages and blocks to it. [What Not to Do](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/what-not-to-do)

Before changing a theme, inventory:

- Sites using it.
- Layout names and page assignments.
- Layout- and site-scoped blocks.
- Theme variables and overrides.
- Custom scripts, fonts, images, and other assets.
- Pages using nonstandard zones.
- Internal, check-in, landing-page, and public consumers.
- Responsive and accessibility behavior after compilation.

## Content Channels And Media Presentation

Content channels separate managed content from the pages that display it. A Content Channel View or Item View block turns channel data into a CMS surface through block settings, filters, routes, detail-page links, and Lava templates.

Audit both sides:

- **Content side:** channel, item, dates, status, attributes, personalization, media links, and applicable authorization.
- **Presentation side:** page, route, block, template, context, detail link, and page/block authorization.

Do not assume the channel item is the only security boundary. A list can expose a title, date, attribute, summary, or detail URL even when the full item is protected. Conversely, a valid item may appear missing because the list block, page, route, template, or context excludes it. [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view)

Immutable source excerpts from commit `471fd303d111b2e46218228dbc1e93dba8856fa3` show current development-branch request and response models for retrieving media elements linked to content-channel items and CMS administration models containing channel, personalization, date, approval, slug, and attribute options. These are implementation observations, not proof that a particular installation exposes, enables, or configures every option. [Linked-media request model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/ContentChannelItemList/GetLinkedMediaElementsRequestBag.cs), [Content-channel model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts)

For video presentation, the Media Player Lava shortcode can render a supplied video URL, including an available HLS, HD, or SD file URL copied from a Rock Media Element. Select the source appropriate to the intended delivery path and test the rendered player rather than treating the presence of a URL as playback proof. [Media Player Lava Shortcode](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/media-player-lava-shortcode)

A reviewed community implementation pattern recommends moving slow video rendering or similar work into a Rock workflow with explicit states, retries, and completion checks. Do not link output into a public page or app until the workflow has confirmed completion and the output is readable. This is a community pattern, not a guarantee about a specific provider or renderer. [Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)

## Landing Pages And SEO

Rock’s documented landing-page pattern uses a Landing Page site and theme, with individual campaigns usually implemented as pages within that site. Layouts can supply headline, hero, content, secondary hero, and workflow zones. Hero images may be page attributes, while HTML, content-channel, and Workflow Entry blocks provide content and calls to action. [Sample Landing Pages](https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages), [Set Up Landing Pages](https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages)

A landing-page review should cover:

- Internal name, page title, browser title, and friendly route.
- Layout and expected zones.
- Header and secondary images.
- Page and block security.
- Form or workflow authorization and completion behavior.
- Mobile rendering.
- Indexing intent.
- Page description and head metadata.
- Expiration or retirement behavior after the campaign.

Rock’s website settings support site-level analytics configuration, page routes, page descriptions, and arbitrary page head content for additional metadata. [SEO](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo)

A reviewed community pattern for HTMX detail pages warns that metadata emitted only by a later swapped fragment may not appear in the initial response seen by crawlers. Put canonical URLs, titles, Open Graph data, JSON-LD, and other crawl-critical metadata on the initial server-rendered route, or provide a server-rendered detail route. This requires local verification of both the anonymous initial response and the enhanced browser state. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

## Page Parameters, Filters, And Short Links

The Page Parameter Filter publishes each selected value under its configured key. Redirects, listening Obsidian blocks, and Lava `PageParameter` lookups can consume the same filter state. [Page Parameter Filter Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/page-parameter-filter-block)

Its delivery mode matters:

- With legacy reload disabled, selections are sent as virtual parameters to listening Obsidian blocks.
- With legacy reload enabled, parameters are placed in the query string and the full page reloads for legacy consumers.

When a filter appears inert, verify the configured key, the consumer’s expected key, the consumer type, virtual-parameter listening, legacy reload mode, redirect behavior, first-load defaults, and whether Lava is reading the same parameter name.

A community recipe demonstrates adding a Page Parameter Filter to the Pages administration screen to locate deeply nested pages. Treat its SQL and block settings as an example rather than official behavior; evaluate performance and authorization before applying community recipe code. [Search Rock Pages recipe](https://community.rockrms.com/recipes/432)

The `CreateShortLink` Lava filter accepts optional settings in this order: token, site ID, overwrite, random length, category ID, and pinned flag. Invalid values may fall back to defaults. An empty URL, or the absence of a shortening-enabled site, returns an empty string. [Other Lava filters](https://community.rockrms.com/lava/filters/other-filters)

Because creating a short link persists operational state, verify argument positions, target site, generated row, and final URL before using links in public pages or bulk communications.

## Obsidian, Helix, HTMX, And Forms

An Obsidian block is not a single file. It combines server-side C#, a TypeScript component, and block actions. Diagnose server logic, client state, and action endpoints as one feature. [Creating Obsidian Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)

The Helix Lava Application Content block automatically registers HTMX. Within its templates, a caret-form route such as `^/application-slug/endpoint-slug` can address an application endpoint instead of hard-coding the full `/api/v2/lava-app/1/...` path. This behavior is documented for the version 2.0 application model in the supplied claim. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

Reviewed community patterns, each requiring local verification, recommend:

- Keep the host content block responsible for the shell, filters, loading state, and useful first render; return only inner rows or cards from an active-search endpoint.
- Keep filter, pagination, and sort state in the server contract. A results partial can emit hidden sort values that later filter and refresh requests include.
- Normalize GUID casing consistently. Delimit short numeric IDs rather than using substring matching that could confuse `5` with `15`.
- Reapply locally stored UI state after `htmx:afterSwap`, or encode that state in the URL so the server renders consistent classes and ARIA state.
- Load shared scripts and styles in the host shell when endpoint responses cannot reliably emit them.
- Where sanitization removes inline scripts, use declarative `hx-on:*` only for presentation behavior; keep authorization on the server.
- Test application-level authorization in addition to page, block, and endpoint settings. Administrator success does not prove intended-role access.
- Validate application configuration as JSON before changing endpoint code.
- Verify each endpoint’s enabled-command allow-list. Keep it narrow and apply CSRF protection to state-changing endpoints.
- After deploying Rock-managed block, endpoint, or server-file content, read back the saved content or hash and compare it with the intended artifact.

These patterns are operational examples rather than official guarantees. Their supporting surfaces are described in the [Helix Content Block documentation](https://community.rockrms.com/developer/helix/lava-applications/content-block), [Lava Commands documentation](https://community.rockrms.com/lava/commands), and related Helix documentation.

For forms, Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms’ single-page form model. Include that boundary when diagnosing nested-form validation or submission behavior. [Understanding Helix Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)

Rock v19 introduces built-in proof-of-work CAPTCHA with organization- and block-level controls. Confirm whether each exposed form uses visible, invisible, or disabled mode, then test the form rather than assuming the organization default reached every block. [Rock v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=155s)

## Mobile Content Boundary

In Rock Mobile’s Content block, Dynamic Content fetches fresh server content on each page initialization. Static content is bundled into the shell, requires a deployment to update, and processes Lava without `CurrentPerson` context. [Rock Mobile Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

Before relying on personalization, secure lookups, parameters, or authenticated context in mobile content, verify:

- Dynamic Content.
- Server-side Lava processing.
- Enabled Lava commands.
- Context entity.
- Shell version.
- Whether the content came from a fresh server request or a bundled deployment.

Community migration patterns also recommend placing shell-version gates inside the XAML fragment actually rendered, parsing the observed shell-version format, and treating .NET MAUI layout changes as separate visual migration tasks. Those patterns require testing in the real target shells and should not be inferred from web CMS behavior.

## Version And Authority Caveats

Most hydrated website documentation in this pack was retrieved as Rock v19 documentation. Confirm the installed Rock version and block generation before applying names, settings, or interface paths.

Specific version conditions include:

- Built-in proof-of-work CAPTCHA is a Rock v19 feature in the supplied evidence.
- The supplied `CreateShortLink` claim is scoped from Rock v8 onward, but current syntax should still be verified before persistent link creation.
- The supplied Lava Application Content block claim is scoped to the documented version 2.0 application model.
- Rock v17.1 fixed a Content Channel Item View breadcrumb issue that could produce a Page Not Found error when a detail page was opened directly.
- Rock v16.1 fixed a Dynamic Data block settings issue that could overwrite the internal page editor’s page name.
- The hydrated release notes describe v19.5 fixes involving page routes not taking effect until restart and duplicate content-channel attribute keys preventing an item list from loading.
- The hydrated release notes identify Rock v20.0 as alpha and describe CMS changes including content-channel item caching and an Obsidian Content Channel Item View block. Do not treat alpha behavior as stable production behavior. [Rock release notes](https://www.rockrms.com/releasenotes)

Authority distinctions:

- Official documentation and developer documentation describe supported behavior for their applicable versions.
- Approved RockU claims provide the guide’s operational security and review spine.
- Immutable GitHub excerpts describe implementation at one commit, not installed configuration.
- Community recipes and reviewed contributions are examples that require local validation.
- Read-only schema or surface validation proves inspectability, not correct configuration or successful visitor behavior.

## Troubleshooting Decision Tree

### A page is missing or visible to the wrong visitor

1. Confirm the requested domain maps to the intended site.
2. Resolve the actual page through the route, short link, redirect, or `/page/{id}`.
3. Inspect the page’s parent hierarchy and inherited authorization.
4. Inspect block view authorization and block scope.
5. Identify required route, query, virtual, and context parameters.
6. Test anonymously, as the intended role, and as an administrator.
7. Compare results without treating administrator override as proof.
8. If behavior differs after a recent route edit, check the installed version against route-related release fixes. [Routes](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/routes), [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy)

### A saved page, block, route, or style change does not appear

1. Verify the edit was made on the block, page, site, theme, or endpoint actually rendering the request.
2. Check page-, layout-, and site-scoped copies of similar blocks.
3. Check approval, versioning, display date range, and exclusive end-date behavior.
4. Check HTML, content-channel, application, and browser caching.
5. For themes, confirm the save compiled Less and inspect the generated CSS plus overrides.
6. For deployed file content, read back the saved artifact or hash.
7. Clear cache only after identifying which cache could retain the old value.
8. If a route edit is stale, compare the installation with the relevant route fix in release notes. [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)

### The wrong personalized or contextual content appears

1. Record the exact route, parameters, login state, person, campus, or group used in the test.
2. Confirm the site has the required personalization setting enabled.
3. Inspect the audience rule and source person data.
4. Inspect context entity type and the parameter or setter that establishes it.
5. Check fallback content.
6. Disable or vary caching in a controlled test.
7. Inspect page, block, and entity authorization separately.
8. Retest with representative actors. [Personalization](https://community.rockrms.com/rocku/cms/personalization), [HTML Block Context](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/html-block-context)

### A content-channel item is missing, duplicated, or exposed

1. Confirm the channel and item.
2. Check item status, dates, attributes, and personalization.
3. Inspect the list block’s channel, filters, Lava template, and detail-page settings.
4. Inspect the page, route, context parameters, and block security.
5. Review what the list exposes even when the detail view is restricted.
6. Check for duplicate attribute keys if the item list fails to load on an affected version.
7. If direct-link breadcrumbs fail on an older installation, compare against the v17.1 fix.
8. Test list and detail routes independently. [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view), [Rock release notes](https://www.rockrms.com/releasenotes)

### A Page Parameter Filter does not update its consumer

1. Compare the configured filter key with the consumer’s expected key.
2. Determine whether the consumer is an Obsidian listener, legacy block, redirect, or Lava lookup.
3. Inspect legacy reload mode.
4. For virtual parameters, verify the Obsidian block is listening.
5. For query-string consumers, verify the full reload and resulting URL.
6. Check defaults, pagination, sorting, and HTMX include behavior.
7. Test first load, change, refresh, and back navigation. [Page Parameter Filter Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/page-parameter-filter-block)

### A Helix endpoint works for an administrator but fails for the intended visitor

1. Confirm the page and Lava Application Content block render for the visitor.
2. Inspect endpoint security mode.
3. Inspect parent application authorization where applicable.
4. Inspect the endpoint’s enabled Lava Commands.
5. Verify request method and CSRF behavior for state-changing requests.
6. Test the endpoint as anonymous and as the intended role.
7. Compare the hosted caret-route request with direct endpoint execution.
8. Stop if success depends only on administrator override. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

### An HTMX result is correct but its controls, assets, or metadata are wrong

1. Inspect the anonymous initial response.
2. Inspect the swapped fragment separately.
3. Confirm the partial returns only the intended target content.
4. Verify scripts and styles are loaded by the host shell.
5. Reapply or server-render view, sort, expansion, and ARIA state after swaps.
6. Put crawl-critical metadata on the initial route.
7. Test refresh, back navigation, no-JavaScript behavior, and the intended actor states.
8. Verify security server-side regardless of visible controls.

### A page is slow

1. Reproduce the exact route and actor state.
2. Open Page Debug Timings from the page-load-time control.
3. Identify the largest request, block initialization, task trace, or query.
4. Compare cached and uncached behavior.
5. Isolate expensive blocks or customizations.
6. Retest after one bounded change rather than inferring the cause from total page time. [Page Load Time](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time)

### A web form fails validation, nests incorrectly, or receives bot submissions

1. Identify whether the surface uses WebForms, Helix Lava Forms, a workflow form, or another block.
2. For nested-form behavior, verify the Helix form boundary.
3. Confirm installed Rock version and CAPTCHA availability.
4. Inspect organization- and block-level CAPTCHA mode.
5. Test visible, invisible, or disabled behavior as configured.
6. Submit the exposed form anonymously and as the intended authenticated role.
7. Verify completion and error behavior without relying only on visual presence. [Understanding Helix Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)

### Mobile content is stale or lacks `CurrentPerson`

1. Determine whether the Content block is static or dynamic.
2. Confirm whether Lava is processed on the server.
3. Inspect enabled commands and context entity.
4. For static content, verify the latest shell deployment.
5. Do not expect `CurrentPerson` in bundled static processing.
6. Test the actual target shell and account state. [Rock Mobile Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

### A generated short link is blank or uses the wrong options

1. Confirm the input URL is nonempty.
2. Confirm at least one intended site has shortening enabled.
3. Verify optional arguments in the documented order.
4. Inspect fallback behavior for invalid values.
5. Generate one controlled link.
6. Read the stored link and open the final URL.
7. Stop before bulk use if the site, token, overwrite, category, length, or pinning value is unverified. [Other Lava filters](https://community.rockrms.com/lava/filters/other-filters)

### Background-generated media is linked before it is ready

1. Identify the workflow or provider job responsible for generation.
2. Record explicit queued, processing, retry, failed, and completed states.
3. Confirm retry limits and failure reporting.
4. Verify the output exists and is readable.
5. Test the public page or app that consumes it.
6. Publish the link only after completion and readback. [Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr)

## Agent Task Recipes

### Recipe: Publish a page and block safely

**Outcome:** A page resolves through the intended site and route and shows only the intended blocks to each visitor class.

1. Identify the site, parent page, intended route, layout, zone, and block type.
2. Determine page, layout, or site scope before adding the block.
3. Inspect inherited page authorization.
4. Configure block view, edit, and administrative authorization.
5. Configure required parameters, context, content, and caching.
6. Review alternate routes, redirects, short links, and navigation placement.
7. Test anonymously, as the intended authenticated role, and as an administrator.
8. Confirm the final route, visible output, hidden output, and navigation behavior. [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)

**Do not assume:**

- A friendly route grants access.
- A hidden navigation item secures a page.
- Page security automatically matches block security.
- Administrator success proves public behavior.

**Stop when:**

- The intended site or parent page is ambiguous.
- Required authorization ownership is unknown.
- A site- or layout-scoped change has unreviewed consumers.

### Recipe: Copy a page hierarchy without carrying stale configuration

**Outcome:** A copied hierarchy is structurally complete and its settings point to the intended new or shared resources.

1. Record the source page, descendants, blocks, routes, and external dependencies.
2. Copy the page with child pages only when the full hierarchy is intended.
3. Confirm Rock created the expected pages and blocks.
4. Review rewired references among the copies.
5. Review content channels, workflows, detail pages, parameters, routes, block scope, and security.
6. Remove or replace copied campaign content and dates.
7. Test every entry route and important child route.
8. Publish only after confirming no copied setting points to an unintended live resource. [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)

### Recipe: Audit an Advanced HTML or stored-Lava surface

**Outcome:** Executable CMS content has a known owner, minimum command set, and verified exposure boundary.

1. Locate the page, block, scope, and all shared render points.
2. Identify who can view, edit, and administer it.
3. Inventory markup, Lava, stored values, context inputs, and query parameters.
4. Inventory enabled Lava Commands.
5. Remove commands that are not required.
6. Review every entity field emitted by the template.
7. Test cache separation between actors and contexts.
8. Test anonymous and intended-role output.
9. If stored text is processed through Lava, verify its editors and execution context.
10. Stop publication if sensitive output or command authority cannot be bounded. [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block), [Lava Commands security](https://community.rockrms.com/lava/commands/getting-started)

### Recipe: Change a theme without surprising other sites or pages

**Outcome:** The intended site receives the new styling while layouts, zones, and shared blocks remain functional.

1. Identify every site using the theme.
2. Copy an upgrade-managed or shared theme before customization.
3. Inventory layout names, zones, layout blocks, site blocks, variables, overrides, and assets.
4. Make the smallest theme or override change.
5. Save and confirm Less compilation.
6. Test representative pages across each layout.
7. Test responsive sizes, interactive controls, accessibility, and staff editing.
8. Verify no unrelated site changed.
9. Retain a recoverable prior theme configuration. [Themes](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/themes)

### Recipe: Publish a content-channel list and detail experience

**Outcome:** Intended items appear with correct metadata and detail links without exposing restricted information.

1. Identify the channel, items, statuses, dates, attributes, media, and personalization settings.
2. Configure the list block’s channel, filters, Lava template, and detail page.
3. Configure the detail route and required item parameter.
4. Inspect page and block authorization on list and detail pages.
5. Review every field exposed in cards, lists, attributes, and links.
6. Test missing, expired, future, targeted, and unauthorized items.
7. Test direct detail links as well as navigation from the list.
8. Confirm anonymous, intended-role, and administrator behavior separately. [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view)

### Recipe: Build and verify personalized content

**Outcome:** Each target audience receives the intended content while authorization remains independently enforced.

1. Define the intended audience and fallback.
2. Identify the exact person or visitor data used by the rule.
3. Confirm site personalization and any required tracking settings.
4. Configure targeted and fallback content.
5. Inspect page, block, and entity authorization.
6. Configure caching so audience or context differences are preserved.
7. Test anonymous, matching, nonmatching, incomplete-data, and administrator cases.
8. Record the actor state and route used for each test.
9. Stop if targeting is the only thing preventing access to sensitive content. [Personalization](https://community.rockrms.com/rocku/cms/personalization)

### Recipe: Connect a Page Parameter Filter to a consumer

**Outcome:** One configured key controls the intended redirect, Lava lookup, or listening block consistently.

1. Choose a stable parameter key.
2. Configure the filter control and its value source.
3. Configure the consumer to use the exact same key.
4. Select virtual-parameter delivery for listening Obsidian blocks or legacy reload for query-string consumers.
5. Configure defaults, redirects, sort, and pagination state.
6. Test first load, filter change, reload, copied URL, and back navigation.
7. Test no-JavaScript behavior when the route requires a usable fallback.
8. Verify that untrusted parameter values cannot expose unauthorized data. [Page Parameter Filter Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/page-parameter-filter-block)

### Recipe: Build a bounded Helix active-search page

**Outcome:** The initial page is useful, HTMX updates only the result region, and authorization is verified for the intended actors.

1. Put the shell, form, loading indicator, target container, and first render in the Lava Application Content block.
2. Use the caret route for application endpoint calls.
3. Make the endpoint return only inner result markup.
4. Pass filters, pagination, sort, and direction through one server-side contract.
5. Keep the endpoint query bounded.
6. Validate application, page, block, and endpoint authorization.
7. Enable only required Lava Commands and apply CSRF protection to state changes.
8. Put scripts, shared styles, and crawl-critical metadata in the host response.
9. Test anonymous, intended-role, administrator, no-JavaScript, refresh, and back-button behavior.
10. Read back deployed content before declaring the change live. [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

### Recipe: Launch a landing page

**Outcome:** A campaign page has the intended route, content, call to action, metadata, and retirement plan.

1. Create or copy the page under the intended Landing Page site.
2. Set internal name, page title, browser title, layout, and images.
3. Add HTML, content-channel, workflow, or other blocks to the intended zones.
4. Configure page and block authorization.
5. Add one canonical friendly route and required metadata.
6. Confirm indexing intent.
7. Test the call to action through completion.
8. Test mobile and anonymous rendering.
9. Define the end date, redirect, archival behavior, or removal procedure before launch. [Set Up Landing Pages](https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages)

### Recipe: Retire a seasonal public feature

**Outcome:** Expired content can no longer be viewed or submitted through any supported route.

1. Inventory public routes, short links, redirects, blocks, alternate pages, mobile surfaces, and underlying filters.
2. Identify date flags, Lava conditions, workflow or registration state, and block authorization.
3. Disable or expire the owning feature using its supported configuration.
4. Verify page and block exposure independently.
5. Test direct URLs, old shared links, alternate routes, and mobile entry points.
6. Confirm submissions or actions are rejected as intended.
7. Verify replacement messaging or redirects.
8. Stop only after the public and authenticated paths are both retested.

### Recipe: Publish background-generated video

**Outcome:** A public page references a completed and readable media output.

1. Start the background work through the owning workflow or provider integration.
2. Record explicit state and retry behavior.
3. Wait for a completed state rather than blocking the visitor request.
4. Verify the generated output and intended HLS, HD, or SD source.
5. Configure the Media Player shortcode with the reviewed source URL.
6. Test playback on the target page and visitor state.
7. Publish the link only after completion and playback verification. [Media Player Lava Shortcode](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/media-player-lava-shortcode)

### Recipe: Configure mobile CMS content with the correct freshness and identity

**Outcome:** Mobile content updates on the intended schedule and uses only context available in its processing mode.

1. Decide whether content must be bundled or fetched on page initialization.
2. Enable Dynamic Content when fresh server content is required.
3. Confirm where Lava is processed.
4. Verify available person and context data.
5. Review enabled commands and secure lookups.
6. For static content, deploy a new shell artifact.
7. Test the exact target shell version and authenticated state.
8. Do not publish identity-dependent static Lava that assumes `CurrentPerson`. [Rock Mobile Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

## Known Gaps And Live Verification

The following cannot be established universally from this pack and require a bounded review of the target installation:

- Installed Rock version, patch level, block generation, plugins, and Helix availability.
- Actual sites, domains, themes, layout files, variables, compilation settings, and custom assets.
- Page hierarchy, routes, redirects, short links, navigation placement, and exclusive-route settings.
- Page, block, content-channel, item, application, endpoint, and entity authorization.
- Enabled Lava Commands on each block or endpoint.
- Stored Lava values, editor permissions, and actual exposed entity fields.
- Personalization audiences, person data quality, fallback content, visitor tracking, and cache variation.
- Content-channel configuration, duplicate attribute keys, list/detail templates, dates, approval state, and media links.
- HTML approval, versioning, context names, scheduled versions, folder roots, and cache duration.
- CAPTCHA organization defaults, block overrides, and form coverage.
- Mobile shell version, deployment freshness, Dynamic Content, and runtime context.
- Workflow/provider behavior for background media generation, retries, and completion.
- Whether HTMX endpoints emit scripts or styles, preserve UI state, expose metadata, or authorize anonymous requests as intended.
- Whether community-reported Lava change-tracking, `ModifyResult`, stored-Lava, endpoint, filtering, deployment, and migration patterns reproduce on the installed version.
- Performance bottlenecks on real routes and actor states.
- Accessibility, responsive behavior, browser compatibility, SEO crawl results, analytics collection, and media playback.

A live review should remain read-only until the intended change is approved. Record the exact site, page, route, block, version, actor state, and cache state. Do not treat schema presence as configuration proof, administrator access as visitor proof, a successful save as deployment proof, or an upload response as exact-content readback.

## Source Map

### Approved operational claim sources

- [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) — claims `claim:09bc1e14a8ad2c40145e`, `claim:39735f6a8684f32d8191`.
- [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block) — claims `claim:4c6c24811261384a0eb4`, `claim:7e6e3979faad614f0b42`.
- [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view) — claims `claim:49453ea8932cdc4b0736`, `claim:d5d56ebc6176db44cbc7`.
- [Personalization](https://community.rockrms.com/rocku/cms/personalization) — claims `claim:64100db2b5d60396b9fd`, `claim:95e015e3407ed10e9e7c`.
- [Content Component](https://community.rockrms.com/rocku/cms/content-component) — claims `claim:88f836ef3f599ca8bf84`, `claim:d20bc9c809f8b6dd7904`.

### Official website documentation

- [Websites](https://community.rockrms.com/documentation/digital-publishing/websites)
- [Intro to Websites in Rock](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/intro-to-websites-in-rock)
- [Create a Site](https://community.rockrms.com/documentation/digital-publishing/websites/sites/create-a-site)
- [Routes](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/routes)
- [Block Configuration](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration)
- [Page Layouts](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts)
- [Themes](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/themes)
- [What Not to Do](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/what-not-to-do)
- [Intro to the HTML Content Block](https://community.rockrms.com/documentation/digital-publishing/websites/html-content-block/intro-to-the-html-content-block)
- [Configure Block Settings](https://community.rockrms.com/documentation/digital-publishing/websites/html-content-block/configure-block-settings)
- [Intro to Context](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/intro-to-context)
- [HTML Block Context](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/html-block-context)
- [Campus Context Setter](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/campus-context-setter)
- [Context on the Person Profile](https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile)
- [Page Load Time](https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time)
- [Sample Landing Pages](https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages)
- [Set Up Landing Pages](https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages)
- [SEO](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo)
- [Cookies](https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/cookies)

### Official specialized documentation

- [Page Parameter Filter Block](https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/page-parameter-filter-block)
- [Lava Commands](https://community.rockrms.com/lava/commands/getting-started)
- [Other Lava filters](https://community.rockrms.com/lava/filters/other-filters)
- [Media Player Lava Shortcode](https://community.rockrms.com/documentation/digital-publishing/content-management/digital-media/media-player-lava-shortcode)
- [Creating Obsidian Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)
- [Lava Application Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)
- [Understanding Helix Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)
- [Rock Mobile Content block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)
- [Rock release notes](https://www.rockrms.com/releasenotes)

### Community examples and implementation observations

- [Search Rock Pages recipe](https://community.rockrms.com/recipes/432) — community recipe; evaluate security and performance locally.
- [Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr) — reviewed community background-processing pattern.
- [Rock source at immutable commit](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3) — implementation evidence only; not proof of installed configuration.
