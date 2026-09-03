---
id: authored-developer-resources
title: Rock Developer Resources
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "fbccc8d629850d0c99dbf58e6940f2f3492bd909d90dfb4f636a48fc2e1eb6d5"
---

# Rock Developer Resources

## Agent Summary

Rock’s developer resources are a collection of learning paths and platform-specific references, not a single development manual. Start with the smallest surface that owns the requested behavior:

- Use Quickstart, 101, 202, and 303 as the general progression from blocks and configuration through entities, migrations, APIs, jobs, filters, and workflows.
- Use the Developer Codex for core coding standards, architecture, migrations, code generation, compatibility, testing, and contribution practices.
- Use Obsidian guidance for blocks that combine C# server logic, a TypeScript UI, and block actions.
- Use Helix for HTMX-driven Lava applications, endpoint work units, Lava commands, and control shortcodes.
- Use the Mobile, Apple TV, or Roku documentation when the behavior runs in one of those shells.
- Treat packaging, migration, release notes, and reference utilities as separate operational concerns rather than implementation afterthoughts.

This routing reflects the official [Developer Resources index](https://community.rockrms.com/developer). The index describes 202 Ignition as draft, and several supplied sources contain beta, upcoming, pre-release, or core-team-specific material. Verify the applicable Rock version, shell version, installed components, and documentation status before applying a pattern.

## Scope And Boundaries

This guide helps an agent select, inspect, implement, and verify work across Rock’s documented developer surfaces. It covers the evidence supplied for:

- The general Quickstart, 101, 202, and 303 learning path.
- Developer Codex standards and core-development workflows.
- Obsidian block and plugin development.
- Helix applications, endpoints, forms, and security.
- AI-agent developer resources and selected implementation observations.
- Rock Mobile compatibility.
- Apple TV and Roku application development.
- Plugin and theme packaging.
- Slingshot migration.
- Developer utility and release-reference pages.

Detailed API design, Lava syntax, Helix internals, security administration, plugin architecture, themes, migration planning, and individual platform shells remain owned by their corresponding concepts. This aggregate guide routes to those topics and records cross-surface operational checks without reproducing every specialist guide.

Do not infer installed configuration from public documentation or source code. The supplied GitHub excerpts are tied to immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` and show implementation at that revision; they do not prove what any Rock installation currently runs.

## Mental Model

Treat Rock development as five connected decisions:

1. **Choose the runtime surface.** Determine whether the behavior belongs to a legacy or Obsidian block, a Helix endpoint, REST API, workflow action, job, mobile shell, TV shell, plugin, theme, or migration.
2. **Resolve the governing version.** Core Rock, Mobile Shell, TV shell, plugin, and documentation versions can move independently.
3. **Inspect the contract.** Identify inputs, attributes, permissions, security mode, command allowances, routes, entity relationships, caching, and persistence behavior before changing code or configuration.
4. **Use the owning mutation path.** A reviewed community pattern recommends using the normal API for stable entity/controller updates, Lava commands for appropriate Lava-driven operations, Obsidian block actions when they are the actual UI save path, and file-content deployment for Rock-managed files. This is community operational guidance, not an official universal rule, and it requires instance-specific verification.
5. **Verify the result independently.** A successful request, save response, package import, or file upload proves only that the operation was accepted. Read back the saved state and test the actual runtime surface.

The first three decisions are grounded in the official [Developer Resources index](https://community.rockrms.com/developer), [Obsidian block model](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks), [Helix overview](https://community.rockrms.com/developer/helix/overview), and platform documentation. The last two include reviewed community operational patterns and should not be presented as documented Rock guarantees.

## Learning Path: Quickstart, 101, 202, And 303

The official developer index presents a progression:

1. **Quickstart Tutorials** introduce creating, configuring, and connecting blocks.
2. **101 Launchpad** covers where blocks live, how they work, and how to secure and store data.
3. **202 Ignition** moves into entities, data models, and migrations. The index labels this material as draft.
4. **303 Blast Off** advances into automation such as custom jobs, data filters, and workflows.

These are route descriptions, not evidence for the detailed behavior of every topic named. Use them to select a learning stage, then require a directly supporting article before asserting a specific implementation rule. [Developer Resources](https://community.rockrms.com/developer)

The supplied Quickstart environment appendix describes a Windows-oriented development setup involving SQL Server, Visual Studio, relevant web and Node.js workloads, the Rock solution, and local connection-string configuration. Because toolchains and prerequisites drift, treat that appendix as a starting point and verify it against the target branch and current setup instructions. [New Developer Environment Setup](https://community.rockrms.com/developer/quickstart-tutorials/appendix/appendix---new-developer-environment-setup)

### REST authorization in 303

Rock REST API requests require authorization. The approved claim identifies two documented approaches: an HTTP cookie associated with an existing Rock user session or an `Authorization-Token` sent with subsequent requests. Possessing a route does not establish permission to call it, and successful authentication does not establish authorization for the requested entity or operation. [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)

The broader API resource page distinguishes API v1, described there as legacy, from API v2 and also routes developers to the full API reference, API concepts, and Lava-based API creation. Do not transfer an API v1 assumption to API v2 without direct documentation for the target endpoint. [API Documentation](https://community.rockrms.com/api-docs)

## Developer Codex

The Developer Codex is the standards and practices collection for Rock development. Its supplied index covers coding rules, naming, architecture, security, migrations, code generation, testing, peer review, compatibility, API patterns, performance, logging, SQL formatting, UI standards, and other core-development concerns. The evidence pack supplies detailed support for only a subset of those areas. [Developer Codex](https://community.rockrms.com/developer/developer-codex) and [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards)

### Naming and compatibility

The database naming guidance says fields ending in `Id` should be integers; a non-integer identifier should use another suffix such as `Key`. It also recommends fully qualifying relationship properties, such as naming a relationship for both the owning and referenced concepts rather than using an ambiguous short name. [Database Naming Conventions](https://community.rockrms.com/developer/developer-codex/coding-standards/naming-conventions/database-naming-conventions)

Compatibility guidance recommends limiting `public` and `protected` exposure when `internal` or `private` is sufficient, because exposed members can become compatibility obligations. The documented core test assemblies can access internal members through `InternalsVisibleToAttribute`, so testability alone does not require making an API public. [Tips for Maintaining Compatibility](https://community.rockrms.com/developer/developer-codex/coding-standards/maintaining-compatibility/tips-for-maintaining-compatibility)

### Model changes and generated artifacts

When an existing model changes or a model is added, the Codex directs core developers to run the code generator. The documented sequence is:

1. Build Rock.
2. Run model generation and confirm the generator is using the expected DLL.
3. Add newly generated C# files to the appropriate projects.
4. Build Rock and the view-model project.
5. Run Obsidian view-model generation.
6. Preview the proposed writes and investigate unexpected files before saving.

If a property is being removed and stale generated code prevents the initial build, the documentation notes that corresponding generated classes may first require manual adjustment. [Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)

### Core migration coordination

The supplied Codex material says standard Entity Framework migrations are ordered and coordinated among core developers through a migration token. The documented token duration is 40 minutes. This is a core-team coordination workflow and may change; it is not evidence that community plugin developers should use the same process. [Standard EF Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/standard-ef-migrations)

For a core hotfix branch, the documentation describes plugin hotfix migrations under `Rock.Plugin.HotFixes` and requires a corresponding Entity Framework migration in `Rock.Migrations`. It also explains that hotfix migration execution must be disabled after merger into the development branch so the ordered EF migration owns the change there. These instructions are specific to Rock’s core release workflow. [Plugin Hotfix Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/plugin-hotfix-migrations)

### Community contributions

The supplied core contribution guidance says community developers should submit pull requests rather than directly commit unapproved changes, even if repository permissions happen to permit a commit. [Community Member Commits](https://community.rockrms.com/developer/developer-codex/coding-standards/committing-code/community-member-commits)

## Obsidian Development

An Obsidian block is a multi-part feature: a C# block supplies server behavior, a TypeScript component supplies the client UI, and block actions connect client requests to server operations. Inspect all three before concluding where a defect or change belongs. [Creating Obsidian Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)

The Obsidian book is primarily aimed at Rock’s core development team. Some material, including grid references, is publicly useful, but agents must decide whether a core-only convention transfers safely to a plugin. The grid reference supplied in the pack confirms a broad family of column components, but it does not supply their individual contracts. [Obsidian](https://community.rockrms.com/developer/obsidian) and [Grid Columns](https://community.rockrms.com/developer/obsidian/grid-reference/columns)

### Plugin development

The supplied plugin-development article uses `rock-dev-tool` to create environments and plugins, generate view models and standard blocks, build Obsidian assets, and assist with packaging. It states that plugin development can be done manually, but the tool reduces setup work. Not every Rock version is necessarily published for use by the tool, so verify that the intended version exists before creating an environment. [Obsidian Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)

The article distinguishes entity security from CMS security in generated block choices. Entity-security-aware blocks should honor per-entity access where the model provides it; CMS security relies on the block’s access instead. The correct choice depends on the entity and use case and must not be guessed from a generated default. [Obsidian Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)

### Lava behavior inside Obsidian

Some Lava operations that modify the full HTTP response—such as redirects or adding metadata—may not work from an Obsidian block action. Obsidian actions do not reload the entire page, and the original response may already have been sent when the action runs. Move such behavior to a supported client navigation or full-response surface rather than assuming legacy Lava response behavior will carry over. [Lava With Obsidian](https://community.rockrms.com/lava/obsidian)

### Debugging

The supplied core-environment guide documents separate VS Code configurations for the Obsidian framework and block projects, with variants that open a new browser or attach to an existing Chrome process. Attaching requires Chrome to have remote debugging enabled. These instructions describe that documented environment and should be adapted cautiously for other operating systems or plugin toolchains. [Debugging Obsidian in VS Code](https://community.rockrms.com/developer/obsidian/core-development-environment/debugging-obsidian-in-vs-code)

### Replacing WebForms blocks

The Codex uses three terms for core WebForms-to-Obsidian transitions:

- **Chop:** replace old block instances and permanently remove the old block type.
- **Swap:** replace instances but retain the old block type temporarily.
- **Sneak:** make the Obsidian block available to selected organizations for testing before later replacement.

A replacement is considered complex when block-type attribute keys and values do not match exactly or when a chop follows an earlier swap or sneak. The documented complex process uses a post-update migration job and requires local database backup, execution testing, confirmation that instances and settings were transferred, and—when chopping—confirmation that the old block type was removed. [Obsidian Chop, Swap, Sneak](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak) and [Process to Chop or Swap](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak/process-to-chop-or-swap)

At immutable Rock commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, the corresponding job accepts old-to-new block-type GUID mappings, supports swap and chop strategies, and replaces instances across sites, pages, and layouts. That is implementation evidence for the cited revision, not proof that every installed Rock version behaves identically. [Post-update replacement job](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs)

## Helix Development

Helix combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. HTMX enables partial-page requests; Lava Applications organize endpoint-backed behavior; Lava Commands can perform supported server work; and Control Shortcodes help generate Rock-styled form controls. [Helix Overview](https://community.rockrms.com/developer/helix/overview)

### Applications and endpoints

A Lava Application has identifying and configuration information such as a name, description, slug, active state, attributes, and configuration rigging. The supplied immutable source view model at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` confirms those fields in that implementation revision. [Lava application view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts)

Endpoints are the application work units called by the client. Before changing a flow, inspect the endpoint’s application, name, description, slug, HTTP method, active state, behavior, and security. The approved claim’s bounded read-only verification confirmed that live Rock endpoint records can also carry enabled Lava commands, caching, rate limits, security mode, and related settings, but it did not certify any particular endpoint configuration. [Helix Lava Application Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)

At the supplied immutable commit, the endpoint view model exposes a code template, HTTP method, security mode, CSRF protection, enabled Lava commands, caching, rate-limit settings, slug, and active state. The associated security enum includes endpoint execute and application view, edit, and administrate modes. These are source-code observations for that commit. [Endpoint view model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointDetail/lavaEndpointBag.d.ts) and [endpoint security modes](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/Enums/Cms/lavaEndpointSecurityMode.ts)

### Content blocks and routing

The approved content-block claim states that a Lava Application Content block automatically registers HTMX. Within its templates, an application endpoint can be addressed with the relative form `^/application-slug/endpoint-slug` instead of hard-coding the full `/api/v2/lava-app/1/...` route. The supplied claim is version-scoped to `2.0`; verify what that version denotes and whether it matches the installed Helix/Rock surface before relying on it. [Helix Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

### Security and data integrity

Helix endpoints can expose data or perform work beyond static rendering, so application development requires explicit security and data-integrity review. The approved claim’s bounded verification confirmed that Lava applications and endpoints are securable entity types and that endpoint surfaces include settings related to security mode, commands, CSRF, and rate limiting. It did not prove that any particular application is safe. [Helix Security](https://community.rockrms.com/developer/helix/overview/security)

For each endpoint:

- Confirm the HTTP method matches the operation.
- Inspect the effective endpoint or application security mode.
- Permit only the Lava commands required by the template.
- Review CSRF behavior for state-changing browser requests.
- Review rate limits, caching, and response behavior.
- Validate inputs and confirm the operation cannot cross the intended data boundary.
- Test as the actual authorized role and, where safe, confirm an unauthorized role is denied.

### Forms and controls

Helix forms address a structural mismatch: ordinary HTML expects independent forms, while ASP.NET WebForms uses a single page-level form. Keep this distinction in mind when investigating nested forms, browser submission behavior, and validation. The supplied forms index also routes to using controls, creating controls, validation, and loading indicators, but it does not provide enough detail here to restate their individual contracts. [Understanding Helix Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) and [Forms & Controls](https://community.rockrms.com/developer/helix/forms-controls)

### Packaging-status conflict

The supplied plugin-installation page calls Helix a limited beta and says the Helix and Magnus plugins are required, while the supplied FAQ says Helix is now in core. These statements appear to represent different stages or an incompletely updated documentation set. Do not resolve the conflict by assumption. Inspect the target Rock version, installed packages, available block types, and current official release guidance. [Plugin Installation](https://community.rockrms.com/developer/helix/overview/plugin-installation) and [Helix FAQ](https://community.rockrms.com/developer/helix/overview/faq)

A community case study demonstrates a Helix-powered group finder with partial-page filtering, but it is an example of one implementation rather than proof of standard Rock behavior. [Guided Group Finder case study](https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix)

## AI Agents

The official Developer Resources index provides an AI Agents book for creating agents and equipping them with tools. The supplied pack does not contain the detailed book articles for agent instructions, context anchors, native tools, custom tools, or Lava tools, so their contracts cannot be synthesized here. [Developer Resources](https://community.rockrms.com/developer)

Rock v20.0 release notes, marked alpha in the supplied snapshot, describe expanded agent capabilities including richer entity identifiers in tool results, a Core Administration skill, a Workflow Builder skill, and a Community Knowledge Base skill. These are upcoming or alpha-era release observations, not evidence that they are available on an earlier or production installation. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

At immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, the CMS agent implementation includes a block-listing tool that requires at least one page, layout, or site filter and instructs agents to inspect all three scopes when determining what renders on a page. The same revision includes tools for resolving block attributes from an existing block or a block type, and page attributes from an existing page or proposed placement context. These observations can guide source review, but installed availability and authorization still require live verification. [ListBlocks implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.ListBlocks.cs), [block attribute inspection](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetBlockAvailableAttributes.cs), and [page attribute inspection](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetPageAvailableAttributes.cs)

## Rock Mobile Development

Rock Mobile compatibility has two dimensions:

- `M` tags specify the minimum Mobile Shell version.
- `C` tags specify the minimum Rock Core version.

A feature may require both minimums. Checking only the server’s Rock version or only the installed app shell can therefore produce a false compatibility conclusion. [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)

Moving from Mobile Shell V5 or earlier to V6 or later changes the underlying framework from Xamarin Forms to .NET MAUI. Much XAML remains similar, but documented breaking layout behavior must be tested and adapted rather than assumed compatible. [Migrating to .NET MAUI V6](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

The supplied developer-controls index lists controls for command execution, validation, field layout, scanning, media, parameters, zones, and related tasks. It confirms that these reference pages exist but does not provide their individual behavior. Open the specific control article before generating markup or asserting shell support. [Mobile Developer Controls](https://community.rockrms.com/developer/mobile-docs/essentials/controls/developer-controls)

## Apple TV And Roku Development

Apple TV and Roku are distinct client platforms. Do not translate TVML, JavaScript, SceneGraph XML, BrightScript, focus behavior, styling, or shell commands directly between them.

### Apple TV

The approved Apple TV claim identifies JavaScript commands as a core part of Rock TV application development, including navigation, media, utility, and demonstration workflows. A reviewed bounded source-template inspection confirmed `rockCommand` usage for navigation, authentication, and playback in local implementation examples, but an agent must still inspect the exact application and page template being changed. [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript)

Apple TV documentation describes light and dark themes, user-selected theme response, theme-aware media queries, and an optional page-level theme. Verify appearance in both modes rather than assuming one style works universally. [Apple TV Themes](https://community.rockrms.com/developer/apple-tv-docs/styling/themes)

### Roku

Rock’s Roku support was introduced in Rock v16.7 according to the supplied documentation. Roku applications use SceneGraph XML, with most UI built from standard SceneGraph components and additional Rock controls layered on top. [Roku Docs](https://community.rockrms.com/developer/roku-docs) and [Roku Controls](https://community.rockrms.com/developer/roku-docs/resources/controls)

Roku commands are assigned through `rockCommand` and command-specific parameters on supported controls. Multiple command names may be chained with commas. Reviewed source-template inspection confirmed command-specific parameters in implementation examples, but comma chaining was supported by documentation rather than independently exercised in a running Roku client. [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands)

Rock’s extended Roku Button and Content Node controls expose `rockCommand` and command parameter fields. A page’s outer component should be `Rock:Page`, which also supplies initial-focus behavior. [Roku Button](https://community.rockrms.com/developer/roku-docs/resources/controls/button), [Content Node](https://community.rockrms.com/developer/roku-docs/resources/controls/content-node), and [Page control](https://community.rockrms.com/developer/roku-docs/resources/controls/page)

Roku pages contain Lava-driven SceneGraph content. The supplied page documentation identifies merge fields including the current person, context, campuses, current page, page permissions, page parameters, and TV shell version. It also documents public, private, no-cache, and no-store cacheability choices plus cache-age settings. Select caching according to the data sensitivity and expected freshness of the actual page. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)

The Rock `FocusGroup` control provides horizontal or vertical layout and directional focus management. Use explicit IDs and initial focus, then test navigation with a real remote or equivalent client input. [Roku Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)

## Packaging Plugins And Themes

Official packaging guidance treats the Rock Shop as the community distribution path for extensions. Packaging work must therefore include the deliverable, review readiness, installation behavior, migrations, and uninstall behavior—not only code that works in a local checkout. [Packaging Plugins and Themes](https://community.rockrms.com/developer/packaging-plugins-themes)

The supplied Obsidian plugin-development article says `rock-dev-tool` can assist with packaging and package import. Because the pack does not include the detailed packaging contract, do not invent manifest fields, migration semantics, Rock Shop submission rules, or uninstall guarantees. Inspect the current packaging documentation and test the produced package against the supported Rock versions. [Obsidian Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)

The Model Map record supplied for `Theme` confirms that Theme is a CMS model. It does not establish a theme’s packaging structure, installed values, or runtime selection. [Rock Model Map](https://community.rockrms.com/ModelMap)

## Slingshot Migration

Slingshot uses a two-step process: extract data from a prior system into a `.slingshot` file, then import that file into Rock. The documentation says an import can be scoped by record type and time frame and uses a Foreign System Key to distinguish files containing the same source data. [About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)

An import is not the same as a completed migration. The supplied documentation explicitly warns that imported data may require cleanup and configuration afterward; its example notes that attendance can be present without yet appearing correctly in analytics. Validate both record presence and the downstream Rock behavior that depends on those records. [About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)

The pack does not provide source-system mappings, supported entity matrices, duplicate-handling rules, rollback behavior, or detailed cleanup scripts. Those remain migration-specific gaps.

## Utility, Design, Query, Branch, And Release References

The official Developer Resources index links to the Design System, Dynamic LINQ Syntax, Pulled Pre-Alpha material, RealTime Visualizer, Rock Branches, SQL Style Guide, technical changelog, API documentation, workflow-action documentation, and Slingshot documentation. The evidence pack confirms these routes but does not supply enough article content to restate their operational rules. [Developer Resources](https://community.rockrms.com/developer)

Use release notes to determine when a feature or fix was introduced, then verify the installed version and reproduction. For example, the supplied records identify an Obsidian Communication Template Detail block in v17.1 and a cloned-theme display fix in v18.2. These release notes do not prove that a site has upgraded, that a fix was backported, or that the reported symptom has the same cause. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

## Version And Authority Caveats

- **Approved claims are the factual spine.** Source excerpts add only directly supported detail.
- **202 Ignition is marked draft** on the supplied Developer Resources page.
- **Helix documentation is internally inconsistent about lifecycle and packaging.** One supplied page says limited beta with Helix and Magnus plugins; another says Helix is now in core.
- **Rock v20.0 is identified as alpha** in the supplied release-note snapshot. Treat its AI-agent features as alpha-era behavior until the target installation and release status are verified.
- **Mobile requires both Core and Shell checks.** `C` and `M` requirements are independent.
- **Roku begins at v16.7** according to the supplied Roku overview.
- **Core Codex workflows are not automatically plugin workflows.** Migration tokens, hotfix rollups, chop/swap processes, and core repository practices may not apply to third-party extensions.
- **Source observations are commit-bound.** All source-code statements in this guide refer only to commit `471fd303d111b2e46218228dbc1e93dba8856fa3`.
- **Community patterns are examples.** The update-surface, independent-save-readback, and exact-file-readback practices are reviewed community contributions that still require target-instance verification.
- **Live verification is bounded.** Approved claims include reviewed public-safe conclusions from read-only checks, but no specific endpoint, application, mobile app, TV app, plugin, package, or migration was certified by this guide.

## Troubleshooting Decision Tree

### A REST request returns an authorization error

1. Confirm whether the request is targeting API v1 or API v2.
2. Confirm that the request carries either the documented session cookie or an `Authorization-Token`.
3. Confirm that the credential remains present on subsequent requests.
4. Separate authentication failure from authorization failure: verify the Rock person and security roles represented by the credential.
5. Inspect the target controller or endpoint permissions.
6. Stop if testing would require obtaining, exposing, or broadening credentials. [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)

### An Obsidian action works but redirect or metadata Lava does nothing

1. Determine whether the Lava operation tries to alter the full HTTP response.
2. Confirm whether it runs during initial page rendering or after an Obsidian block action.
3. If the original response has already been sent, do not expect legacy response mutation to work.
4. Move navigation to an appropriate client action or move response-header behavior to a full-response surface.
5. Retest the actual browser flow. [Lava With Obsidian](https://community.rockrms.com/lava/obsidian)

### An Obsidian block shows stale or mismatched generated types

1. Confirm the model change is present.
2. Build Rock and inspect the DLL selected by the code generator.
3. Run model generation.
4. Add any new C# files to the projects.
5. Build Rock and the view-model project.
6. Preview Obsidian view-model generation.
7. Investigate unexpected files before saving.
8. Rebuild and retest the block. [Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)

### A WebForms-to-Obsidian replacement loses settings

1. Compare old and new block-type attribute keys and their value expectations.
2. Determine whether this is a first-time chop or swap, or follows a prior swap or sneak.
3. Treat mismatched keys or a later conversion as a complex case.
4. Test the migration against a backed-up local database.
5. Verify instances on sites, pages, and layouts.
6. Compare transferred block settings.
7. For a chop, confirm both files and the old block-type record are removed.
8. Stop before production if the transfer cannot be reproduced safely. [Process to Chop or Swap](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak/process-to-chop-or-swap)

### A Helix request does not update the target content

1. Confirm that the page uses a Lava Application Content block and that HTMX is registered.
2. Verify the application and endpoint slugs.
3. Verify the relative `^/application-slug/endpoint-slug` route or the intentionally selected full route.
4. Confirm that the request method matches the endpoint’s configured HTTP method.
5. Inspect active state, security mode, CSRF behavior, and enabled Lava commands.
6. Check the target selector and returned fragment.
7. Review caching and rate-limit settings.
8. Test with the intended user role. [Helix Overview](https://community.rockrms.com/developer/helix/overview) and [Helix Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block)

### A Helix form submits or validates unpredictably

1. Identify the page-level WebForms form.
2. Look for nested or independently authored HTML forms.
3. Confirm that Helix form controls are being used according to the documented form model.
4. Inspect which control supplies validation and which request submits the values.
5. Test initial render, invalid submission, valid submission, and repeated submission separately.
6. Stop if the exact control contract is not present in the available evidence; open its specific documentation. [Understanding Helix Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms)

### A mobile feature works on one device but not another

1. Record the Rock Core version.
2. Record the Mobile Shell version on each device.
3. Check both the feature’s `C` and `M` minimums.
4. If crossing from Shell V5 or earlier to V6 or later, review .NET MAUI migration caveats.
5. Compare affected XAML layout behavior.
6. Test on each supported shell and device class. [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies) and [Migrating to .NET MAUI V6](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)

### Roku navigation or focus is broken

1. Confirm that the page has an outer `Rock:Page`.
2. Confirm that `initialFocus` names an existing focusable control.
3. Inspect the control’s `rockCommand` and every required command parameter.
4. If commands are chained, verify their comma-separated order.
5. Use a `FocusGroup` where directional focus needs explicit management.
6. Check whether stale personalized or shared cache content is being rendered.
7. Test with the actual Roku client and remote-navigation flow. [Roku Page](https://community.rockrms.com/developer/roku-docs/resources/controls/page), [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands), and [Focus Group](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group)

### Slingshot imported records but downstream reporting is wrong

1. Confirm the expected record types and time range were included.
2. Confirm the intended `.slingshot` file and Foreign System Key.
3. Verify representative imported records.
4. Inspect the Rock configuration required by the downstream feature.
5. Validate the downstream behavior, such as analytics, rather than stopping at row presence.
6. Document cleanup separately from extraction and import.
7. Stop before applying cleanup scripts that have not been reviewed for the target data. [About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)

## Agent Task Recipes

### Recipe: Select the correct developer resource

**Outcome:** Route a request to the narrowest applicable Rock development surface.

1. Describe the user-visible behavior and where it runs.
2. Identify whether the owner is a block, endpoint, API, workflow, job, mobile shell, TV shell, plugin, theme, or migration.
3. Record the Rock version and any shell or plugin version.
4. Select the corresponding specialist documentation.
5. Require a direct source before asserting implementation details.
6. Record unresolved version or installation dependencies as gaps.

**Do not assume:**

- A feature title proves its behavior.
- A core-development workflow applies to plugins.
- Similar concepts behave the same in web, Mobile, Apple TV, and Roku.

**Stop when:**

- The owning surface cannot be identified without inspecting live configuration.
- Proceeding would require a production write or credential not authorized by the task. [Developer Resources](https://community.rockrms.com/developer)

### Recipe: Review an Obsidian block change

**Outcome:** Identify and validate all layers affected by an Obsidian block change.

1. Inspect the C# block and its permissions and server logic.
2. Inspect the TypeScript component and UI state.
3. Identify the relevant block actions and their request/response contracts.
4. Inspect block settings and decide whether entity or CMS security owns access.
5. Check for Lava behavior that depends on a full-page response.
6. Rebuild the server and client projects.
7. Test initial load, each changed action, validation, authorization, and persisted readback.

**Inspect:**

- Block type and block instance.
- Attribute keys and current values.
- Action names and payloads.
- Generated view models.
- Client errors and server exceptions.

**Do not assume:**

- A successful action response proves persistence.
- A legacy Lava redirect will work after an asynchronous block action. [Creating Obsidian Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) and [Lava With Obsidian](https://community.rockrms.com/lava/obsidian)

### Recipe: Regenerate artifacts after a model change

**Outcome:** Produce synchronized C# and Obsidian view models.

1. Make the bounded model change.
2. Build Rock.
3. Confirm which DLL the generator will use and that it is current.
4. Run model generation.
5. Add new generated C# files to their projects.
6. Build Rock and the view-model project.
7. Run Obsidian view-model generation in preview mode.
8. Review every proposed change.
9. Save only the expected files.
10. Rebuild and run relevant tests.

**Stop when:**

- The generator reports an unexpected assembly.
- Preview includes unrelated model changes.
- Removed properties prevent a safe build and the required generated-file adjustment is unclear. [Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes)

### Recipe: Review a Helix endpoint before changing it

**Outcome:** Establish the endpoint’s current contract, security boundary, and runtime dependencies.

1. Identify the Lava Application and application slug.
2. Identify the endpoint, endpoint slug, and HTTP method.
3. Read the endpoint template.
4. Inspect active state, security mode, enabled Lava commands, CSRF setting, rate limits, and caching.
5. Find all client templates that call the endpoint.
6. Determine the expected input, returned fragment, and target element.
7. Identify all data reads and writes.
8. Test with the intended authorized role.
9. Where safe, confirm an unauthorized role is rejected.
10. After any authorized change, perform an independent content and behavior readback.

**Do not assume:**

- Application visibility grants endpoint execution.
- A GET-like UI interaction is read-only.
- A saved endpoint is the endpoint called by the page.
- Public source defaults match the installed configuration. [Helix Lava Application Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) and [Helix Security](https://community.rockrms.com/developer/helix/overview/security)

### Recipe: Validate Rock Mobile compatibility

**Outcome:** Determine whether a feature is supported by the exact Core/Shell pair.

1. Record the target feature.
2. Read its minimum `C` requirement.
3. Read its minimum `M` requirement.
4. Record the installed Rock Core version.
5. Record the actual Mobile Shell version on the test device.
6. Compare both dimensions.
7. If upgrading from V5 or earlier to V6 or later, identify XAML affected by the Xamarin Forms to .NET MAUI transition.
8. Test the affected layouts and controls on the supported devices.

**Stop when:**

- Either installed version is unknown.
- Testing has occurred only in a preview that does not use the deployed shell. [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)

### Recipe: Build or repair a Roku page

**Outcome:** Produce a navigable, correctly cached Lava-driven SceneGraph page.

1. Confirm the Rock version supports Roku.
2. Inspect the target Roku application and page.
3. Place page content beneath an outer `Rock:Page`.
4. Give focusable controls stable IDs.
5. Set a valid initial focus.
6. Add `rockCommand` and only the parameters required by that command.
7. Use a `FocusGroup` for explicit horizontal or vertical focus handling where needed.
8. Choose cacheability based on data sensitivity and freshness.
9. Render with representative merge-field states.
10. Test navigation, login state, playback where applicable, back behavior, and focus on a Roku client.

**Do not assume:**

- “Show in Menu” automatically creates Roku shell navigation.
- Apple TV focus or command behavior transfers to Roku.
- Documentation-backed command chaining has been verified in the target shell. [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages) and [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands)

### Recipe: Prepare a plugin or theme package

**Outcome:** Produce a reviewable extension package with understood install and uninstall behavior.

1. Identify supported Rock versions.
2. Verify that the selected plugin tooling supports those versions.
3. Inventory binaries, Obsidian assets, server files, migrations, and configuration.
4. Build the extension from a clean environment.
5. Generate the package using the current documented packaging workflow.
6. Install it into a disposable supported Rock environment.
7. Test first install and upgrade from the prior supported package.
8. Test uninstall behavior and identify intentionally retained data.
9. Review the package for secrets, environment-specific paths, and organization-specific configuration.
10. Prepare it for the current Rock Shop review process.

**Stop when:**

- Current packaging or uninstall requirements are unavailable.
- The package only works because of untracked local files.
- Migration behavior has not been tested. [Packaging Plugins and Themes](https://community.rockrms.com/developer/packaging-plugins-themes)

### Recipe: Validate a Slingshot migration

**Outcome:** Demonstrate that imported data supports the intended Rock workflows.

1. Define the source system, record types, and time range.
2. Produce the `.slingshot` file.
3. Record its Foreign System Key and migration scope.
4. Import into a non-production validation environment.
5. Monitor the import and capture errors without exposing private records.
6. Validate representative entities and relationships.
7. Configure downstream Rock features that do not become operational from import alone.
8. Test the actual workflows and reports.
9. Record cleanup needs and obtain review for any scripts.
10. Repeat the migration from a known starting state before scheduling production work.

**Do not assume:**

- Imported rows are correctly configured.
- Attendance presence means analytics is ready.
- Cleanup SQL is portable across installations. [About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot)

### Recipe: Inspect page content with a Rock AI agent

**Outcome:** Determine what blocks and settings contribute to a page, when the installed agent tools support it.

1. Verify that the applicable AI-agent feature and CMS skill are installed and authorized.
2. Resolve the page identifier.
3. List blocks at page, layout, and site scope.
4. Resolve the block type for each relevant block.
5. Inspect available and current block attributes.
6. Separate inherited layout/site behavior from page-local behavior.
7. Report identifiers without exposing secrets or private content.
8. Treat the result as an inspection, not authorization to modify the page.

**Do not assume:**

- Alpha release-note features exist in the target instance.
- Page-level blocks are the only blocks rendered.
- A tool’s presence grants access to every entity. [ListBlocks implementation](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.ListBlocks.cs)

### Recipe: Verify a save or Rock-managed file deployment

**Outcome:** Confirm that the intended state persisted at the exact target.

This recipe is a reviewed community pattern and requires instance-specific verification.

1. Identify the actual owning save or file-content surface.
2. Read the current object, file, or content hash.
3. Record the exact target and expected change.
4. Perform the authorized save through that owning surface.
5. Read the value back independently through Edit, Preview, refreshed initialization, a normal API read, exact file readback, or bounded read-only verification.
6. Compare normalized saved state or content hash with the intended artifact.
7. Test the live route that consumes the state.
8. If they differ, investigate normalization, defaults, ignored fields, caching, routing, or a wrong target.

**Do not assume:**

- A success response proves every submitted field persisted.
- A successful upload proves the live route reads that file.
- Read-only SQL is the correct mutation path.

**Stop when:**

- The target cannot be distinguished from similarly named blocks, endpoints, or files.
- Independent readback is unavailable.
- The operation requires production authorization that has not been granted.

## Known Gaps And Live Verification

The following questions cannot be answered from this evidence pack alone:

- The detailed contracts for most 101, 202, and 303 lessons.
- Whether 202 Ignition has progressed beyond draft status.
- Current prerequisites for the Quickstart development environment.
- The meaning and present applicability of the Helix content-block claim’s `2.0` version scope.
- Whether Helix is plugin-delivered, core-delivered, or mixed for a particular Rock version.
- The current contracts for Helix form controls, loading indicators, Magnus, and observability.
- Detailed AI-agent instructions, context anchors, skill contracts, custom-tool contracts, native-tool behavior, and Lava-tool behavior.
- Whether v20 AI-agent functionality is installed or production-ready.
- Individual Mobile developer-control syntax and version requirements.
- Complete Apple TV and Roku command catalogs.
- Current Rock Shop package manifests, review rules, upgrade behavior, and uninstall requirements.
- Slingshot entity coverage, source-system mappings, duplicate handling, rollback, and cleanup procedures.
- The substantive contents of the Design System, Dynamic LINQ Syntax, Pulled Pre-Alpha, RealTime Visualizer, Rock Branches, SQL Style Guide, and technical changelog pages.
- The target installation’s schema, security assignments, block settings, endpoint configuration, plugin inventory, shell versions, and reproduced behavior.

When one of these affects an answer, perform a separate bounded, read-only review of the target version or installation. Report only a reviewed public-safe conclusion. Do not expose raw instance data, credentials, organization-specific identifiers, or SQL output, and do not treat one installation as universal Rock behavior.

## Source Map

| Area | Authority and source |
|---|---|
| Developer learning routes | Official [Developer Resources](https://community.rockrms.com/developer) |
| REST authorization | Approved claim `claim:2cb25390d2b5f4ffeb6f`; official [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) |
| Developer Codex | Official [Developer Codex](https://community.rockrms.com/developer/developer-codex) and [Coding Standards](https://community.rockrms.com/developer/developer-codex/coding-standards) |
| Model generation | Official [Model Changes](https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes) |
| Core migrations | Official [Standard EF Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/standard-ef-migrations) and [Plugin Hotfix Migrations](https://community.rockrms.com/developer/developer-codex/coding-standards/writing-migrations/plugin-hotfix-migrations) |
| Obsidian block architecture | Approved claim `claim:855f7a33bcc8bb936067`; official [Creating Obsidian Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| Obsidian audience | Approved claim `claim:5416735ea289965714bf`; official [Obsidian](https://community.rockrms.com/developer/obsidian) |
| Obsidian and Lava | Official [Lava With Obsidian](https://community.rockrms.com/lava/obsidian) |
| WebForms replacement | Official [Obsidian Chop, Swap, Sneak](https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak) plus immutable source-code excerpts |
| Helix architecture | Approved claim `claim:940f299b268510da61d8`; official [Helix Overview](https://community.rockrms.com/developer/helix/overview) |
| Helix endpoints | Approved claim `claim:d35ed98aadeaabd2cf1e`; official [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints) plus immutable source-code excerpts |
| Helix security | Approved claim `claim:da56681f6277c12df324`; official [Helix Security](https://community.rockrms.com/developer/helix/overview/security) |
| Helix forms | Approved claim `claim:2a7f5e6781a2d2fa30a4`; official [Understanding Forms](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| Helix content routing | Approved claim `claim:ee2f4e5a371c3b243567`; official [Content Block](https://community.rockrms.com/developer/helix/lava-applications/content-block) |
| Mobile compatibility | Approved claims `claim:896d78fdcfa734dde54e` and `claim:dc73468ceef82ee62d45`; official Mobile documentation |
| Apple TV commands | Approved claim `claim:29f4e0bbc81c08861367`; official [Apple TV JavaScript Commands](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| Roku commands | Approved claim `claim:9398f3fb18e8a79c0e4d`; official [Roku Commands](https://community.rockrms.com/developer/roku-docs/commands) |
| Plugin and theme packaging | Approved claim `claim:6ae226ddf1e1e1df52ed`; official [Packaging Plugins and Themes](https://community.rockrms.com/developer/packaging-plugins-themes) |
| Slingshot | Official [About Slingshot](https://community.rockrms.com/developer/slingshot/about-slingshot) |
| Releases | Official [Rock Core Release Notes](https://www.rockrms.com/releasenotes) |
| Update-surface and readback recipes | Reviewed community contributions; examples requiring live verification, not official Rock guarantees |
| GitHub implementation evidence | `SparkDevNetwork/Rock` at immutable commit [`471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3) |