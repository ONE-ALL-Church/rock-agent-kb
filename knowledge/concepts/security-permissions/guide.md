---
id: authored-security-permissions
title: Security And Permissions
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Security And Permissions

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Security And Permissions index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock security is not a single setting. It is an authorization system layered across people, user accounts, security roles, groups, pages, blocks, entity records, entity types, API endpoints, Lava, workflows, files, documents, mobile shells, and integration keys. Agents working in Rock should treat every access question as an evidence problem: identify the authenticated actor, identify the secured thing, identify the action verb, identify whether an explicit allow or deny exists, then identify the parent or fallback authority Rock will use when no direct rule exists.

The core operational object behind most permission work is the `Auth` record. A community security inspector recipe correctly frames many audits as inspection of `Auth` rows for a selected role and entity, while warning that a flat list of rows does not by itself prove inherited effective access ([Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)). This is the central distinction agents must keep clear:

- **Configured security** is what has been explicitly stored on an entity, page, block, role, person, or type.
- **Effective security** is the result Rock returns after applying the actor, the requested action, direct rules, inherited rules, parent authority, role membership, person-specific rules, allow/deny ordering, default behavior, and version-specific code paths.

For most administrative tasks, the safest workflow is:

1. Confirm the actor: person, user login, API key user, public/anonymous context, or workflow/system context.
2. Confirm the secured object: page, block, group, report, data view, workflow type, document type, file type, REST endpoint, Lava endpoint, API tool, or model/entity record.
3. Confirm the action verb: common verbs include `View`, `Edit`, `Administrate`, `Approve`, `Delete`, `ViewAll`, `Interact`, `Refund`, and `ManageMembers`, as shown in the Rock source constants ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).
4. Inspect explicit security entries.
5. Inspect inherited/parent authority.
6. Test as the actual actor or with a reliable impersonation/test account.
7. Document the exact entity, action, role/person, and reason for the change.

Security roles in Rock are generally groups used for authorization. Do not assume that adding someone to a role only affects one screen. Role membership can affect pages, blocks, groups, reports, workflows, REST/API access, Lava-powered screens, and custom blocks. A community recipe about a non-finance admin role is useful because it highlights a common reality: administrators sometimes need broad administrative capability with targeted denies for sensitive domains, but this is not a complete containment strategy against a determined Rock administrator ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).

For developers, page and block visibility is partly handled by the framework, but action-level functionality inside a block must still be checked by code. Official developer guidance says blocks should use authorization checks before exposing or executing sensitive actions, and custom blocks can define additional verbs with security action metadata ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)).

For API work, agents must separate legacy REST access from newer v2 endpoint patterns. The REST API can use an authentication cookie or an authorization token/API key, while v17 introduced a v2 API pattern that is secure by default and requires explicit authorization when endpoints are secured ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns)). Never expose API keys or Lava execution endpoints in client-side JavaScript. The Lava remote endpoint documentation specifically warns that exposing the endpoint plus key allows arbitrary Lava to be sent under the linked key’s authority ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

For agents, the most important rule is: do not infer access from the UI alone. Inspect the live security record, inheritance path, role membership, and actual action being attempted.

## 2. Scope And Terminology

This guide covers Rock RMS security and permissions as they appear in core administration, custom development, API integrations, Lava, workflows, reporting, mobile apps, and agent tools. It is written for agents doing real work in a Rock instance: troubleshooting a “permission denied” error, designing a role, auditing who can see sensitive data, reviewing a custom Lava screen, hardening a workflow, or verifying an API key.

### In Scope

This guide includes:

- Authorization records and action verbs.
- Security roles and person-specific permissions.
- Page, block, entity, and entity type security.
- Parent authority and inherited permissions.
- API key and REST authorization patterns.
- v2 API endpoint authorization patterns.
- Lava command and remote Lava security.
- Workflow, document, file, report, group, and mobile security caveats.
- Developer checks using Rock authorization APIs.
- Operational guardrails and troubleshooting branches.
- Agent task recipes for investigation and implementation.

### Out Of Scope

This guide does not fully cover:

- General web application security theory.
- Network perimeter controls, WAF configuration, or server patching.
- Payment gateway security outside Rock permission implications.
- Full OAuth provider implementation details beyond Rock Mobile references.
- Exact database schema for every security-related entity where the source pack does not provide a model-map record.

Where a field, table, or behavior must be confirmed in the instance, this guide says what to inspect.

### Key Terms

**Actor**
The person or process attempting the action. In Rock this might be a logged-in person, anonymous visitor, API key user, staff user, security role member, workflow action, Lava-rendering context, or agent tool runner.

**Secured Object**
The item protected by authorization. Common examples are pages, blocks, groups, workflow types, data views, reports, document types, file types, content channel items, API endpoints, or custom tool definitions.

**Action Verb**
The named permission being requested. Rock source defines standard constants such as `View`, `ViewAll`, `Edit`, `Delete`, `Administrate`, `Approve`, `Interact`, `Refund`, and `ManageMembers` ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)). Some blocks or entities define custom verbs.

**Authorization Rule**
A configured allow or deny entry for a specific actor or role, action, and secured object.

**Security Role**
A group used as an authorization principal. Many out-of-box roles use names like `RSR - Staff Workers`, `RSR - Staff Like Workers`, and `RSR - Rock Administration`, as reflected in release-note security hardening for workflow types ([Release Notes](https://www.rockrms.com/releasenotes)).

**Effective Permission**
The final answer Rock returns after evaluating direct security, inherited security, actor identity, role membership, action verb, and fallback rules.

**Parent Authority**
The upstream secured object used when the current object has no direct security rule for the requested action. The developer security page identifies “Entity Parent Authority” as a core Rock security concept ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)).

**IdKey**
A shorter identifier designed to avoid exposing raw integer IDs in public-facing URLs and model-facing outputs. Rock developer guidance recommends IdKey for v14+ Obsidian public-facing blocks and agent tools ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).

**PersonActionIdentifier**
A token concept for identifying a person for a particular action rather than for general security. The developer security page uses RSVP as an example of an action-bound identifier ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)).

**Lava Commands**
Extra Lava capabilities that must be enabled in specific contexts and may bypass normal security or business logic if misused ([Lava Commands](https://community.rockrms.com/lava/commands)).

## 3. Security And Permissions Mental Model

Rock authorization is best understood as a layered decision engine. The question is never simply “does Bob have access?” The precise question is:

> For this authenticated or anonymous actor, on this secured object, for this action verb, after direct rules and inherited rules are evaluated, is the result allow or deny?

### The Actor Layer

Start with identity. A permission check depends on who Rock believes is acting.

For a web page, the actor is usually `CurrentPerson` derived from the authenticated session or anonymous context. For REST calls, the actor may be derived from a Rock authentication cookie or from an authorization token/API key ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)). For agent tools, the actor is the person who can run the tool, because Rock’s custom tool guidance says tool access inherits Rock security ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).

When troubleshooting, agents should inspect:

- Person record.
- User login record.
- Security role/group memberships.
- API key association and key purpose, if relevant.
- Elevated security level or impersonation-related settings, if relevant.
- Whether the context is truly logged in or anonymous.
- Whether the action is being executed by a workflow, scheduled job, Lava endpoint, or external integration.

The source pack does not include a complete model-map record for `UserLogin`, API key storage, or auth token tables. In a live instance, inspect the Security area, the person profile Security tab, API key configuration pages, and the Model Map or database schema for exact table/field names before writing automation.

### The Object Layer

The secured object must be identified precisely. A page and a block are not the same object. A file type and a document type are not the same object. A report page, report block, data view, and underlying entity rows are separate security surfaces.

A common operational failure is changing the page permission while the block, report, data view, or entity type still denies access. Another common failure is granting access to a list screen without granting the user access to the detail page, workflow type, or entity record the list opens.

This object-specific framing follows Rock's developer security model: secured entities can have their own authority, parent authority, and action checks, so agents must identify the exact securable object before changing rules ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)).

Agents should ask:

- Is the failing object a page, block, entity type, entity record, or API route?
- Is a block rendering data from a more sensitive object?
- Is the UI hiding a button, or is the server rejecting the action?
- Is the permission configured on the child object or inherited from a parent?
- Is the object a legacy WebForms block, Obsidian block, Lava app, Helix endpoint, or mobile block?

### The Action Layer

Authorization is action-specific. `View` does not imply `Edit`. `Edit` is often broader than the name suggests and may include adding or changing properties. `Administrate` controls configuration/security-level operations. Source constants and developer docs identify standard verbs including `View`, `Edit`, `Administrate`, and `Approve`; the source code adds others such as `ViewAll`, `Delete`, `Interact`, `Refund`, and `ManageMembers` ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).

Agents must verify the actual verb being checked. A user may be able to view a group but not manage members. A person may access a communication detail page but not approve or cancel the communication. The Obsidian communication permission view models expose action-specific booleans such as approve and cancel capability, which illustrates how modern blocks often send explicit permission flags to the client ([CommunicationDetailPermissionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationDetail/CommunicationDetailPermissionsBag.cs), [communicationEntryAuthorizationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryAuthorizationBag.d.ts)).

### The Direct Rule Layer

Direct rules are explicit allow/deny entries on the secured object for a person or role. A flat `Auth` row inspection can answer “what direct rules exist?” but not always “what does Rock effectively allow?” A role permissions inspector recipe explicitly warns that its list of `Auth` records does not account for inheritance ([Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)).

When auditing direct rules, inspect:

- Entity type.
- Entity ID or entity GUID.
- Action.
- Allow or deny.
- Person-specific principal.
- Group/security-role principal.
- Special all-users or anonymous/public principals, if present.
- Order/precedence fields where available.
- Whether the target entity still exists.

The source pack’s community dashboard recipe calls out practical data integrity problems: duplicate rules, orphaned rules pointing to deleted pages, user-specific vs role-based permissions, and rules for people who have left ([Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol)). Treat that as an audit pattern, not as official core behavior documentation.

### The Inheritance Layer

Inheritance is where many wrong conclusions happen. Page and block security may inherit from parent pages or block/page context. Entity security may inherit from parent authority. Group security may be affected by group type and hierarchy. Reporting and workflow security may involve both the container and the underlying entity.

A Page Security Visualizer recipe demonstrates the need to inspect a page/block tree and determine not only allow/deny but the ancestor from which the result came, while warning that complex security evaluation may have edge cases and that the recipe only covers common actions like `View`, `Edit`, and `Administrate` ([Page Security Visualizer](https://community.rockrms.com/recipes/441)).

For agents, inheritance troubleshooting should be explicit:

- If no direct rule exists, identify the parent authority.
- If a direct rule exists but the observed behavior differs, inspect higher-level deny rules and custom code checks.
- If a page is visible but a block is missing, inspect block security separately.
- If a block appears but an action button is missing, inspect action-specific authorization in block code or block settings.
- If a report shows too much data, inspect not only the page and block but also the data view, report, entity security, and Lava/SQL used by the block.

### The Code Layer

Rock’s framework handles some visibility checks, but developers must still secure internal actions. Official block guidance says the page framework can hide a block from users who cannot view it, but block code must check security before allowing other operations ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)). The quickstart shows the same pattern: check authorization before showing or wiring an Add action ([Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)).

The code layer includes:

- C# block authorization checks.
- Obsidian server-side permission bags.
- Custom action verbs.
- Lava filters such as `HasRightsTo`.
- API endpoint attributes.
- Workflow action code.
- Helix endpoint validation.
- Agent tool permission checks.

### The Cache Layer

Rock caches authorization information. The source pack includes `AuthorizationCacheConsumer`, which consumes authorization cache update messages and applies cache invalidation/update behavior ([AuthorizationCacheConsumer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs)). Agents should not overstate cache mechanics from a snippet, but operationally they should consider cache staleness when a permission change does not appear immediately.

Inspect or try:

- Whether the change was saved on the correct object.
- Whether the user’s role membership is current.
- Whether the user needs to log out/in.
- Whether Rock cache needs to be cleared through supported admin tools.
- Whether a multi-node environment is receiving cache update messages.
- Whether the failing request is served by a different node or stale browser session.

## 4. Source Authority And How To Use This Guide

Use this guide as a synthesis, not as a replacement for live verification. The source pack includes official/developer documentation, release notes, RockU training pages, GitHub source snippets, and community recipes. These sources have different authority levels.

### Highest Authority Sources

Use these first:

- **Rock source code snippets** for constants, available enums, cache classes, and view-model field names. Examples include `Authorization.cs`, `ApiKeyPurpose.cs`, and permission bag types ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs), [ApiKeyPurpose.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Security/ApiKeyPurpose.cs)).
- **Official developer docs** for supported patterns, especially block security, REST API auth, v2 API security, Lava command warnings, Helix security, and custom tool security ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns), [Lava Commands](https://community.rockrms.com/lava/commands), [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).
- **Release notes and tech bulletins** for version-specific security changes, especially v17.5, v17.8, v18.3, and v19.1 ([Release Notes](https://www.rockrms.com/releasenotes)).

### Medium Authority Sources

Use these as contextual evidence:

- **RockU training pages** for training topics and conceptual coverage. The source pack includes Group Security and Reporting Security pages, but only compact metadata was available ([Group Security](https://community.rockrms.com/rocku/groups/group-security), [Reporting Security](https://community.rockrms.com/rocku/reporting/reporting-security)).
- **Mobile docs** for mobile-specific auth patterns and block caveats, including Auth0, Entra, Rock logins, and group finder behavior ([Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins), [Using Auth0](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-auth0), [Using Entra](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-entra), [Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).
- **RockU training transcripts** for operational security review topics such as tag security. Treat these as training context: inspect tag type, tag configuration, visibility, and secured actions before assuming person-profile access controls all tag exposure ([Tag Security](https://community.rockrms.com/rocku/individuals-in-rock/tag-security)).
- **Rock Cast security discussions** for operational framing, not authoritative implementation guidance. Episode 125 can help frame role, permission, release-note, and audit questions, but exact behavior must still be verified against docs, source, and the live `Auth` model ([Episode 125: Security](https://shows.acast.com/rock-cast/episodes/episode-125-security)).

### Lower Authority But Useful Sources

Use community recipes and third-party resources as examples, audit ideas, or cautionary patterns. Community recipes are explicitly not reviewed or endorsed by the Rock core team. They can be operationally useful but should not be treated as core behavior unless verified in code or official docs.

Useful recipe-derived patterns include:

- Listing direct `Auth` records by role ([Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)).
- Visualizing effective page/block security with inheritance caveats ([Page Security Visualizer](https://community.rockrms.com/recipes/441)).
- Auditing duplicate/orphaned page and block rules ([Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol)).
- Designing deny-based non-finance admin roles with caution ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).
- Avoiding reports or custom tabs that ignore security ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)).

### How Agents Should Use This Guide

For implementation:

1. Use this guide to form the investigation path.
2. Verify the live Rock version.
3. Inspect the exact object and actor.
4. Prefer official UI, Model Map, source, or read-only SQL to confirm fields.
5. Make the smallest permission change that satisfies the task.
6. Test with the actual actor or a controlled test account.
7. Record the before/after security state.

Use official developer docs and source constants as the baseline, then use community visualizer/inspector recipes only as audit aids because direct rows and page trees can miss inherited or code-level checks ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs), [Page Security Visualizer](https://community.rockrms.com/recipes/441)).

For generated code or custom tools:

1. Use server-side permission checks.
2. Avoid raw integer IDs in public/model-facing outputs.
3. Treat Lava and SQL as privileged surfaces.
4. Do not expose API keys, Lava templates, or admin-only endpoints to clients.
5. Add migrations for default v2 API authorization when core functionality requires it.

## 5. Core Configuration And Data Model

Rock’s security model is implemented through configuration records, securable entities, security roles, login/authentication records, and code-level authorization checks. The source pack does not include a full Model Map export, so exact table/column names beyond source snippets and common entity names must be verified in a live instance before automation.

### Core Configuration Areas

Agents should expect to work in these areas:

- **Admin Tools > Security > Security Roles** for role/group management, as referenced by the non-finance admin recipe ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).
- **Security dialogs on pages, blocks, and list rows** for item-specific permissions.
- **Person Profile > Security** for user logins and account-related settings. Mobile app review docs reference creating credentials from the profile Security tab ([Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins)).
- **API key configuration** for integrations, TV apps, mobile apps, remote Lava, and REST/API access.
- **System Settings or Security Settings** for cookie/token behavior, account protection, and related global controls. A third-party release spotlight notes a v16.7 setting to reject security cookies older than a configured date; verify the exact setting name and availability in the live version ([GitHub Spotlight: 9/6/2024](https://www.triumph.tech/resources/github-spotlight-962024-2)).
- **CMS Configuration** for sites, pages, blocks, mobile/TV applications, and app API keys. Apple TV and Roku docs identify application settings such as API key, page view tracking, and authentication page, but the hydrated excerpt is thin; verify the exact fields in the live application detail page ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)).
- **Workflow Type, Document Type, File Type, Report, Data View, Group Type, and Group detail screens** for domain-specific security.

### `Auth` Records

Many Rock permissions are stored as authorization records. Community recipes around security inspection and dashboards focus on the `Auth` table/records as the operational source for explicit security entries ([Security Role Permissions Inspector](https://community.rockrms.com/recipes/243), [Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol)).

An `Auth` audit should verify:

- Secured entity type.
- Secured entity identifier.
- Action.
- Allow/deny value.
- Principal type: person-specific or group/security-role.
- Principal identifier.
- Order/precedence, if present.
- Whether the target entity still exists.
- Whether the rule is inherited or direct.
- Whether the current Rock version has known security migrations affecting the object.

Do not assume a direct `Auth` list gives effective access. It can miss parent authority, inherited rules, custom code checks, or action-specific logic.

### Authorization Constants

The source code is the best authority for standard action constants in the provided pack. `Authorization.cs` defines `VIEW`, `VIEW_ALL`, `EDIT`, `DELETE`, `ADMINISTRATE`, `APPROVE`, `INTERACT`, `REFUND`, and `MANAGE_MEMBERS` among other security constants ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).

Operational meaning:

- `View`: display/read the object or its public properties.
- `ViewAll`: broader viewing power that may override entity-specific restrictions in certain contexts; inspect code before relying on it.
- `Edit`: modify the object or related editable properties.
- `Delete`: separate delete control in places where delete is not simply edit.
- `Administrate`: manage settings, security, or child configuration.
- `Approve`: approve content, communications, prayer requests, ads, or similar approval workflows.
- `Interact`: interaction permission, used by some content-style entities.
- `Refund`: financial refund capability.
- `ManageMembers`: manage group membership.

If troubleshooting a custom block, inspect attributes such as `[SecurityAction(...)]` because custom verbs may exist ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)).

### Security Roles As Groups

Security roles are generally implemented through Rock group concepts. The source pack’s RockU Group Security page confirms security is a formal topic inside group training ([Group Security](https://community.rockrms.com/rocku/groups/group-security)). The non-finance admin recipe walks through creating a security role under Admin Tools > Security > Security Roles and adding a person to it ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).

When working with roles, verify:

- Whether the group is marked/used as a security role.
- Current active members.
- Whether membership is inherited through group type, parent group, or manual group membership.
- Whether inactive, archived, or former staff remain in roles.
- Whether person-specific rules exist that bypass the intended role model.
- Whether a deny role is used to restrict a subset of admins.

### Person, User Login, And Account Security

A person record is not the same as a user login. A person may have multiple logins, no login, mobile credentials, or app-review credentials. The mobile app review guidance says app stores require active demo credentials and that these do not need special permissions ([Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins)). That is a useful principle for all temporary/test accounts: use purpose-specific accounts with minimal access.

For live verification, inspect:

- Person profile Security tab.
- User login records.
- Login provider.
- Account protection profile.
- Elevated security level.
- Personal token settings.
- MFA/external auth settings, if installed/configured.
- Security role/group membership.

The check-in documentation notes that account protection profile can affect duplicate matching behavior in family pre-registration based on Security Settings ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). This is a reminder that security settings can affect CRM workflows outside obvious permission screens.

### API Keys And Purpose

The source pack includes `ApiKeyPurpose.cs` and its Obsidian TypeScript equivalent, which identify that Rock tracks an intended purpose for API keys ([ApiKeyPurpose.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Security/ApiKeyPurpose.cs), [apiKeyPurpose.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Security/apiKeyPurpose.ts)). The snippets do not include enum values, so verify values in source or the live UI before writing automation.

Operationally, agents should treat API keys as identity-bearing credentials:

- Every key should have an owner/use case.
- The linked actor should have only the permissions needed.
- Keys should not be embedded in public JavaScript.
- Keys should be rotated when exposed.
- Keys should be disabled or deleted when no longer used.
- App-specific keys should be scoped by use and reviewed separately from general REST integration keys.

### Document Type And File Type Security

Release notes identify a high-severity issue fixed in v17.8: files uploaded through the Entity Document Add workflow action were not properly linked to the parent document, causing Rock to evaluate file type security instead of document type security. The fix links files correctly so document type security applies; default document types may copy security from paired file types if no security already exists, and document type list screens can display public-viewable warnings ([Release Notes](https://www.rockrms.com/releasenotes)).

Agents auditing documents must inspect:

- Document Type security.
- File Type security.
- Binary file linkage to document.
- Workflow action used to create/upload the file.
- Rock version.
- Whether built-in document types have inherited/copied security.
- Whether any document type is publicly viewable.

This is a high-risk area because a file may appear protected by one layer while another layer controls access.

### Workflow Type Security

Release notes for newer versions identify workflow type view permission hardening: several core workflow types that previously lacked explicit View permissions were restricted to staff-oriented roles and Rock Administration ([Release Notes](https://www.rockrms.com/releasenotes)). The source pack also includes a hotfix/migration snippet named `HardenCoreWorkflowSecurity`, which restricts view on core workflow types and adds `SanitizeSql` to certain out-of-box workflow SQL Lava expressions ([291_HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs)).

Agents working with workflow security should inspect:

- Workflow Type View/Edit/Administrate permissions.
- Workflow Activity and Action permissions, if exposed.
- Workflow entry pages and blocks.
- Entity attached to workflows.
- Lava/SQL attributes in workflow action settings.
- Whether workflows are public-entry workflows, staff workflows, or system workflows.
- Version-specific hardening migrations.

### Reporting And Data View Security

RockU includes a Reporting Security training topic ([Reporting Security](https://community.rockrms.com/rocku/reporting/reporting-security)). The release notes also include an API bug fix in v17.5: a model’s `./DataView/{id}` endpoint checked permissions on the wrong entity, sometimes causing permission denied even when the person or API key had DataView permission ([Release Notes](https://www.rockrms.com/releasenotes)).

For agents, reporting security requires layered checks:

- Data View security.
- Report security.
- Dynamic Data block/page security.
- Underlying entity security.
- API endpoint security when reports are exposed through API.
- Lava/SQL used in dynamic blocks.
- Whether a custom report bypasses security by querying directly.
- Whether a recipe or custom page explicitly warns it ignores security, as the registrations tab recipe does ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)).

## 6. Primary Entities And Relationships

The source pack does not provide a full Model Map, so this section describes relationships at an operational level. Before writing SQL or migration code, verify exact entity names, table names, foreign keys, and property names in the live Model Map or source.

### Person, UserLogin, Group, And Security Role

A person is the human record. A user login is an authentication credential. A group can represent organizational membership, serving teams, families, small groups, or security roles. Security-role membership affects authorization.

Rock's security docs and group-security training support this separation between authenticated actor, role/group membership, and authorization rules; source constants then define the actions being checked ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Group Security](https://community.rockrms.com/rocku/groups/group-security), [Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).

Common relationship pattern:

- `Person` represents the individual.
- `UserLogin` authenticates the individual.
- `GroupMember` links the person to a group/security role.
- Security role groups are referenced by authorization records.
- A permission check evaluates the person and their relevant role memberships.

Operational checks:

- If a user cannot access something, confirm they have a login and are logged in as the expected person.
- If a person has multiple duplicate records, confirm which person owns the login.
- If a role assignment seems ineffective, confirm the group membership is active/current.
- If a former staff member retains access, inspect both security-role membership and user-specific auth entries.
- If an API key is used, identify the person or account behind the key, not only the key label.

### EntityType And Securable Entities

Rock uses entity metadata to secure many object types. The developer security page references entity type security and entity parent authority ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)). An authorization record usually needs to know what type of thing it secures.

Common secured entities include:

- Page.
- Block.
- Group.
- GroupType.
- Report.
- DataView.
- WorkflowType.
- DocumentType.
- BinaryFileType/FileType.
- ContentChannelItem.
- Communication.
- Financial objects.
- Custom plugin entities.
- API endpoints or endpoint-related objects in newer patterns.

Live verification:

- Inspect Entity Type for the secured object.
- Confirm whether the object implements a securable interface or parent authority.
- Confirm whether the UI security dialog is editing the object you think it is.
- For custom entities, inspect source code for authorization methods and parent authority.

### Page, Site, And Block

A site contains pages. Pages contain blocks. Page security controls whether the page can be visited. Block security controls whether the block renders or can be administered. Block code can further check action-specific authorization.

Developer docs state that a block does not need to hide itself for View access because the page framework handles that, but the block must check security for additional functionality ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)). The Page Security Visualizer recipe treats pages and blocks as a hierarchy and evaluates inherited effective permissions ([Page Security Visualizer](https://community.rockrms.com/recipes/441)).

Operational checks:

- If the page returns access denied, inspect page View.
- If the page loads but a section is missing, inspect block View.
- If the block loads but a button is absent, inspect block action authorization and code.
- If an admin cannot configure the block, inspect `Administrate`.
- If content appears to the wrong audience, inspect both page/block security and data source security.

### Group, GroupType, And Group Security

Group security can apply to group detail screens, group finder results, member management, attendance, scheduling, and serving eligibility. The RockU Group Security topic confirms this area has dedicated training ([Group Security](https://community.rockrms.com/rocku/groups/group-security)). `ManageMembers` appears in source as a standard authorization action ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).

A mobile Group Finder doc warns that returned groups matching filters do not account for user security and that the Lava template should use `HasRightsTo` as needed to check view permissions ([Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)). This is one of the clearest examples of why agents must not assume search results are security-filtered.

Operational checks:

- Group Type security.
- Individual Group security.
- Parent group inheritance.
- Group member role permissions.
- `View` for group visibility.
- `Edit` for group edits.
- `ManageMembers` for membership changes.
- Attendance/scheduling permissions where separate.
- Custom Lava templates that display groups.
- Mobile or public group finder security filters.

### Report, DataView, And Dynamic Data

Reports and data views are often secured separately from pages. A user may be able to see a report page but not the data view, or a custom SQL/Lava page may expose rows without respecting data view/report permissions.

Operational checks:

- Report View/Edit/Administrate.
- DataView View/Edit/Administrate.
- Page and block View.
- Dynamic Data block settings.
- SQL command security and Lava command settings.
- Entity permissions for underlying records.
- Version-specific API endpoint behavior for DataView routes, especially v17.5 fix ([Release Notes](https://www.rockrms.com/releasenotes)).

### WorkflowType, Workflow, Activity, And Action

Workflow Type security governs who can view, edit, administrate, or launch workflows depending on configuration. Workflow pages and blocks may add additional security. Workflows often run with system-like behavior and can execute SQL, Lava, communications, entity updates, and file operations, making them high-risk.

Operational checks:

- Workflow Type View/Edit/Administrate.
- Workflow entry block/page security.
- Workflow action settings.
- Lava/SQL commands in workflow actions.
- Entity context passed to workflow.
- Scheduled job that launches workflows.
- Release hardening affecting core workflow types ([Release Notes](https://www.rockrms.com/releasenotes), [291_HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs)).

### DocumentType, BinaryFileType, BinaryFile, And Document

Document/file security is layered and version-sensitive. The v17.8 release note explains that workflow-uploaded files previously could be checked against File Type security rather than Document Type security because of missing parent linkage; after the fix, Document Type security is intended to control access ([Release Notes](https://www.rockrms.com/releasenotes)).

Operational checks:

- Is the file a generic binary file or a document-linked file?
- What Document Type applies?
- What Binary File Type applies?
- Was it created by workflow action?
- Is the parent document linked?
- Is the document type public viewable?
- Did the instance run the v17.8+ migration/hotfix?

### API Endpoints, Auth Clients, Claims, And Scopes

The source pack shows Obsidian view-model files for auth claims, auth client list, and auth scope list, but not full docs on OpenID/OAuth configuration ([authClaimBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/AuthClaims/authClaimBag.d.ts), [authClientListOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/AuthClientList/authClientListOptionsBag.d.ts), [authScopeListOptionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/AuthScopeList/authScopeListOptionsBag.d.ts)). Agents should verify this area in the live UI and current docs before making changes.

For API access, distinguish:

- Legacy REST cookie/token auth.
- API keys for apps and integrations.
- v2 API endpoint security.
- Auth clients/scopes/claims, if using modern auth features.
- External identity providers like Auth0 or Entra for mobile login ([Using Auth0](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-auth0), [Using Entra](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-entra)).

## 7. Common Security And Permissions Workflows

### Grant A Staff User Access To A Page

1. Identify the person and login.
2. Identify the page by route, page title, or page ID.
3. Inspect page `View` security.
4. Inspect parent page security if no direct rule exists.
5. Inspect each block on the page for `View`.
6. Inspect action verbs needed inside the page, such as `Edit`, `Approve`, or `Administrate`.
7. Add the user to an existing role if the access matches a durable staff responsibility.
8. Avoid person-specific allows unless this is a temporary exception.
9. Test as the user or controlled test account.

This workflow follows Rock's page/block authorization model: page access, block visibility, and action-specific checks can be separate, and community visualizer patterns are useful for tracing inherited page/block rules ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Page Security Visualizer](https://community.rockrms.com/recipes/441)).

Do not grant `Administrate` just to make a page visible. `Administrate` can allow configuration and security changes.

### Explain Why A User Can See A Page

1. Confirm the user’s person record and role memberships.
2. Inspect direct page `Auth` entries.
3. Inspect inherited page rules up the page tree.
4. Inspect whether a role allow applies.
5. Inspect whether a person-specific allow applies.
6. Inspect whether the page or block has public/all-user access.
7. Inspect whether the user is in Rock Administration or another broad role.
8. If the page contains sensitive data, inspect the block and underlying data source too.

Community recipes focused on page/block security dashboards are useful audit ideas for this pattern, especially for duplicate/orphaned rules and role/user-specific rules ([Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol), [Page Security Visualizer](https://community.rockrms.com/recipes/441)).

### Create A New Security Role

Use a role when multiple people share an ongoing responsibility. Do not create roles for one-off exceptions unless the exception is operationally meaningful.

Implementation path:

1. Define the responsibility in plain language.
2. Define what the role should view, edit, administrate, approve, or manage.
3. Define what the role must not see.
4. Create the security role under the Security Roles area.
5. Add a description explaining the role’s purpose.
6. Add members.
7. Apply permissions to pages, blocks, entity types, reports, data views, workflows, groups, document types, or API endpoints as needed.
8. Test with a non-admin account.
9. Document the role.

For deny-based roles, be careful. The non-finance admin recipe demonstrates using a role to deny selected finance access while the person also has broad admin access, but it explicitly cautions that this is not a complete security boundary against a determined Rock admin ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).

### Remove Access For Departed Staff

1. Disable or remove the person’s user logins according to local policy.
2. Remove from staff/security role groups.
3. Search for person-specific `Auth` entries.
4. Search for API keys linked to the person or account.
5. Check workflow assignments, scheduled jobs, communication approvals, and integration ownership.
6. Check mobile/app credentials if relevant.
7. Confirm the person cannot log in.
8. Confirm role membership cleanup did not remove access needed by active staff.

A security dashboard recipe’s mention of rules tied to people who have left is a practical audit item ([Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol)).

### Secure A Custom Block

Official developer guidance supports this pattern:

1. Allow the framework to handle block `View` where appropriate.
2. Use server-side authorization checks for action buttons, save operations, deletes, approvals, exports, or custom actions.
3. Check both block-level permission and entity-level permission where the block acts on a specific entity.
4. Use standard action constants from `Rock.Security.Authorization`.
5. Define custom security verbs with `[SecurityAction(...)]` when the block has domain-specific actions.
6. Return permission flags to Obsidian clients from the server rather than deciding sensitive access purely in TypeScript.
7. Retest as a user with view-only access and as a user with edit/admin access.

Developer docs show checking block authorization before exposing Add behavior and also checking entity authorization for a specific group ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)).

### Secure A Custom Lava Page

1. Identify whether Lava commands are enabled.
2. Identify whether the Lava queries data through entity commands, SQL, workflows, or REST.
3. Check whether the page and block are secured.
4. Add explicit `HasRightsTo` checks where a collection is not security-filtered.
5. Avoid exposing raw IDs in URLs; prefer IdKeys or GUIDs for public routes.
6. Avoid rendering hidden sensitive data into the page.
7. Avoid client-side calls to remote Lava with exposed API keys.
8. Test anonymous and low-privilege users.

Lava command docs warn that commands can bypass built-in security and business logic and must be enabled intentionally per context ([Lava Commands](https://community.rockrms.com/lava/commands)). The mobile Group Finder doc warns its returned groups do not account for user security and advises checking rights in Lava as needed ([Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

### Secure A REST Integration

1. Identify the endpoint.
2. Identify auth method: cookie, authorization token/API key, or v2 API auth.
3. Identify the linked person/account for the key.
4. Grant the minimum role permissions to that account.
5. Avoid using an administrator account.
6. Avoid embedding keys in client-side code.
7. Use HTTPS.
8. Rotate keys after exposure or staff/vendor transition.
9. Test exact read/write operations.
10. Log or monitor integration use where possible.

The REST API docs describe cookie and authorization-token access ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)). Remote Lava docs warn strongly against exposing API keys with client-side Lava calls ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

## 8. Authorization Deep Dive

### Standard Actions

The developer docs and source code establish the standard vocabulary. Commonly encountered actions include:

| Action | Operational Use |
| --- | --- |
| `View` | See the page, block, entity, report, or object. |
| `ViewAll` | Broader view override used in some code paths; verify exact behavior in source for the entity. |
| `Edit` | Modify the object or create/update related content. |
| `Delete` | Delete where delete is secured separately. |
| `Administrate` | Change settings, security, or child configuration. |
| `Approve` | Approve content, communications, prayer, ads, or similar items. |
| `Interact` | Interact with certain content-style objects. |
| `Refund` | Refund a financial transaction. |
| `ManageMembers` | Manage group members. |

Sources: developer block security docs and Rock source constants ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).

### Custom Actions

Custom block functionality should not overload `Edit` when a narrower action is needed. Official developer docs say custom action names can be defined by decorating a block with a security action attribute ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)).

Use custom actions when:

- A user can view/edit general data but should not approve.
- A user can manage one operation but not another.
- A block has sensitive exports.
- A block performs external side effects.
- A block launches workflows or sends communications.
- A financial operation needs separate authorization.

Agent checklist for custom action review:

- Does the block define custom security actions?
- Are those actions documented for admins?
- Does server-side code enforce them?
- Does UI hide buttons based on the same checks?
- Is there a server-side guard even if a user posts directly?
- Are migrations or default permissions needed?

### Allow And Deny Strategy

Rock supports granular allow/deny configuration. Use allows to grant normal access by role. Use denies sparingly for exception boundaries, especially when broad admin roles are involved.

Deny-based design is appropriate when:

- A broad role must be blocked from a narrow sensitive area.
- A temporary or special exclusion is needed.
- A sensitive domain like finance needs explicit separation.

But denies can become difficult to reason about. Agents should document:

- Why the deny exists.
- Which broader allow it is counteracting.
- Who owns review.
- How to test it.
- Whether it should expire.

The non-finance admin recipe is a practical example of deny-based thinking with a strong caveat that broad administrators may still have ways to access data ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).

### Person-Specific Permissions

Person-specific rules can solve urgent cases but create long-term audit problems. Prefer role-based permissions unless the access is truly personal, temporary, or exception-based.

Use person-specific entries only when:

- The access is temporary and documented.
- The person’s responsibility is unique.
- There is no existing role and creating one would be misleading.
- You set a review date.

Audit person-specific entries regularly. Community dashboard examples call out user-specific vs role-based rules and rules for former staff as practical security health checks ([Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol)).

### Page And Block Security Order

The developer security page identifies “Block Security Order” as a core security topic ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)). The source pack does not include the detailed order algorithm. Agents should not invent it. In live work, verify by inspecting:

- Direct block rules.
- Direct page rules.
- Parent page rules.
- User-specific rules.
- Role-based rules.
- Any deny entries.
- The actual effective result through the UI or controlled test account.

If effective behavior differs from expected behavior, inspect the Rock source for the current version or use a known-good page security visualizer only as a diagnostic aid, not as final authority ([Page Security Visualizer](https://community.rockrms.com/recipes/441)).

### Entity Parent Authority

Entity parent authority controls where Rock looks when the entity itself does not carry direct security. The developer security page lists it as a security concept ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)). Because exact parent authority varies by entity, agents must inspect the entity’s code, Model Map, or live security dialog.

Examples of questions to ask:

- Does a block inherit from the page?
- Does a document file inherit from Document Type or File Type?
- Does a content item inherit from content channel?
- Does a group inherit from group type or parent group?
- Does a workflow inherit from workflow type?
- Does a report inherit from data view or page?
- Does a custom entity implement a parent authority method?

### Authorization Cache

Authorization changes may involve cache updates. The source pack includes a cache consumer for authorization update messages ([AuthorizationCacheConsumer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs)). Agents should include cache in troubleshooting when changes do not apply.

Operational branch:

- If the UI still denies immediately after a change, re-check the saved rule.
- If another user/session sees different behavior, check session/login state.
- If a multi-node environment behaves inconsistently, inspect cache/message-bus health.
- If a key/integration still has old access, rotate or disable the key and test a fresh request.
- If a browser still shows stale UI, force refresh and re-login.

Do not treat cache clearing as the first fix. It should follow evidence that the rule is correct and stale state is plausible.

## 9. API Auth Deep Dive

### Legacy REST API Authorization

Rock’s REST API supports external applications and internal components. Official REST docs say authorization can be based on an HTTP cookie or an authorization token ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)).

Cookie-based access generally means:

- Authenticate with valid Rock user credentials.
- Receive a Rock auth cookie.
- Send the cookie with subsequent requests.
- Authorization then acts as that user.

Authorization-token/API-key access generally means:

- Send the token/key in the required header.
- Rock maps that credential to an authorized context.
- Authorization depends on the permissions granted to the linked account/key context.

Agents should verify the exact header names, endpoint routes, and authentication behavior in the live version before automating. The provided REST doc excerpt mentions `Authorization-Token`; remote Lava examples also show that header ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

### v2 API Pattern

Rock v17 introduced a new v2 API pattern. The developer API patterns page says the v2 pattern is secure by default: secured endpoints do not allow execution until explicit authorization has been granted. If an out-of-box staff role needs a secured endpoint for Rock to function, the developer must add default permissions in a migration; if it is a third-party feature, leaving it denied by default may be correct ([API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns)).

Agent implications:

- Do not assume new v2 endpoints are public.
- If a new secured endpoint breaks staff functionality, check whether default auth migration exists.
- If a plugin adds endpoints, inspect endpoint security.
- If writing migration code, add only the required roles/actions.
- Test with a non-admin staff account, not only Rock Administration.

### API Keys

The source pack includes API key purpose enum files but not full UI documentation. Treat API key purpose as a classification aid, not as proof of effective scope unless source/live UI confirms behavior ([ApiKeyPurpose.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Security/ApiKeyPurpose.cs), [apiKeyPurpose.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Security/apiKeyPurpose.ts)).

Operational rules:

- Name keys by system and owner.
- Use one key per integration.
- Use low-privilege users/accounts.
- Do not reuse staff personal accounts for integrations.
- Do not expose keys in public JavaScript.
- Rotate on vendor/staff changes.
- Review keys during access audits.
- Test key access to exact endpoints.

### Remote Lava Endpoint

Remote Lava is high risk. The Lava remote endpoint renders submitted Lava under the authority of the linked key/user. The docs warn that exposing the endpoint and key in browser-visible JavaScript allows users to submit arbitrary Lava with that authority and recommend avoiding that pattern in favor of server-side calls ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

Hardening checklist:

- Use HTTPS only.
- Do not call from public client-side JavaScript.
- Use a narrowly permissioned key.
- Restrict Lava commands.
- Sanitize inputs.
- Avoid templates that accept raw entity IDs.
- Log usage.
- Disable if not needed.
- Rotate key if exposed.

### Mobile And TV App API Keys

Apple TV and Roku app docs reference application API key settings and related configuration such as page view tracking and authentication page ([Creating An App](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app), [Roku Applications](https://community.rockrms.com/developer/roku-docs/getting-started/applications)). Hydrated excerpts are thin for those pages, so agents should inspect the live application detail page before changing fields.

Questions to verify:

- Which key does the app use?
- What actor/permissions does that key have?
- Is the key used only by the intended app?
- Does the app expose authenticated content?
- Is page view tracking enabled?
- What authentication page is configured?
- Are old app keys still active?

### External Identity Providers: Auth0 And Entra

Mobile docs include Auth0 and Microsoft Entra as login provider patterns. Auth0 docs describe a cloud identity platform and Rock Mobile configuration; Entra docs describe app registration, permissions, optional claims, and Rock Mobile configuration ([Using Auth0](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-auth0), [Using Entra](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login/using-entra)).

Agents should separate authentication from authorization:

- Auth0/Entra proves identity or supplies claims.
- Rock still needs to map identity to a person/login.
- Rock permissions still decide what the person can do.
- Missing claims can break login/account matching.
- Overbroad external app permissions can expose identity data.
- Demo/app-review logins should not have special permissions ([Rock Logins](https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins)).

### API Auth Troubleshooting

If an API request returns permission denied:

1. Confirm the endpoint URL and version.
2. Confirm auth method: cookie, token, v2 auth, OAuth/client, or anonymous.
3. Confirm the request is HTTPS where required.
4. Confirm the header name and value.
5. Identify the linked person/account/key.
6. Confirm that actor can perform the same action in the UI.
7. Inspect endpoint security.
8. Inspect entity/model security.
9. Inspect DataView/Report security if the route uses reporting.
10. Check release caveats, especially v17.5 DataView route permission fix ([Release Notes](https://www.rockrms.com/releasenotes)).
11. Test with a deliberately low-privilege key and with an admin key to isolate authentication vs authorization vs endpoint behavior.

## 10. Related Rock Areas: People, Groups, Api, Cms, Workflows

### People

Person security touches logins, account protection, impersonation, personal tokens, signals, badges, documents, workflows, and profile tabs.

Person-profile customizations are especially risky because they often show consolidated data. A registrations tab recipe warns that its initial implementation does not account for registration template security, meaning restricted registrations could become visible through the custom tab ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)). Treat any custom person profile tab as a data-exposure risk until entity-level authorization is proven.

Person security work should inspect:

- Person profile page and block security.
- Security tab visibility.
- Signals block security.
- Documents tab and document type security.
- Badges and what data they reveal.
- Registration/event custom tabs.
- Workflows launched from the profile.
- Person-specific auth entries.
- User login status.
- Account protection settings.

A security signal notification recipe describes adjusting the Security tab and Signals block so staff could view signal notes and selected staff could add signals ([Notify Staff of New Security Signal](https://community.rockrms.com/recipes/494)). That is a useful pattern: separate view from add/edit and make the role boundary explicit.

### Groups

Group security affects ministries, serving teams, small groups, check-in groups, group scheduling, RSVP, attendance, and public group finders. The RockU Group Security topic confirms this area is a formal training area ([Group Security](https://community.rockrms.com/rocku/groups/group-security)).

Critical group checks:

- Group type security.
- Group detail security.
- Group member management.
- Group attendance access.
- Public group finder filtering.
- Mobile group finder templates.
- Whether returned group lists are security-filtered.
- Whether `ManageMembers` is required.

The mobile Group Finder doc is explicit that returned groups do not account for user security and recommends using `HasRightsTo` in Lava as needed ([Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)). Any public or mobile group finder should be reviewed for this.

### API

API security spans legacy REST, v2 endpoints, Lava render endpoints, app keys, TV/mobile apps, custom agent tools, and auth clients/scopes.

Key principles:

- Keys are credentials.
- Endpoint security is separate from entity security.
- v2 endpoints are secure by default when secured.
- Remote Lava is especially dangerous if exposed.
- API keys should be tied to low-privilege accounts.
- Never test only as Rock Administration.

Sources: REST API docs, v2 API patterns, remote Lava docs, and custom tool docs ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava), [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).

### CMS

CMS security includes sites, pages, blocks, content channels, content channel items, HTML blocks, Lava, shortcodes, and app shells.

CMS checks:

- Site/page hierarchy.
- Page security.
- Block security.
- Content channel/item security.
- HTML block Lava command settings.
- Shortcode security and command enablement.
- Public routes using raw IDs.
- Obsidian block use of IdKey.
- SecurityColumn availability in admin grids.

The Obsidian `SecurityColumn` documentation describes a grid column that opens the standard security editor modal for an item, with properties such as item title and disabled field ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)). For admin tools, using the standard security editor is preferable to custom ad hoc permission UIs.

### Workflows

Workflows can create, update, query, notify, upload, and automate. They can be launched by users, blocks, jobs, entity triggers, or data views. This makes workflow security a core operational concern.

Workflow checks:

- Who can view the workflow type?
- Who can launch it?
- Who can edit/administer it?
- What entity does it operate on?
- Does it run SQL or Lava?
- Does it upload documents/files?
- Does it send communications?
- Does it expose person data?
- Are out-of-box workflow hardening migrations applied?

Release notes and source snippets show workflow type view hardening and SQL/Lava sanitization work in newer versions ([Release Notes](https://www.rockrms.com/releasenotes), [291_HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs)).

## 11. Administration And Operational Guardrails

### Least Privilege

Grant the smallest durable role that allows the work. Avoid making staff Rock administrators because a page is missing. Avoid giving integration keys admin-level rights. Avoid person-specific allows when a role fits.

The non-finance admin recipe is a useful cautionary example: broad admin rights with targeted denies can help in a narrow scenario, but it is not a complete containment boundary for a determined administrator ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181)).

Least privilege checklist:

- Does the actor need view, edit, approve, administrate, or manage members?
- Can access be scoped to a page/block/entity rather than all admin tools?
- Can access be granted through an existing role?
- Is there a data domain boundary such as finance, safety, minors, counseling, or personnel?
- Is the permission temporary?
- Is there a review date?

### Separation Of Duties

Separate sensitive operations:

- Finance viewing vs finance editing/refunds.
- Communication drafting vs approval.
- Group viewing vs member management.
- Workflow launch vs workflow administration.
- Document upload vs document viewing.
- Security signal viewing vs signal creation.
- API integration read vs write.

Use custom action verbs where needed. Source constants include action-specific verbs like `Refund` and `ManageMembers`, and developer docs allow custom security actions ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs), [Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)).

### Sensitive Domain Guardrails

High-risk domains include:

- Giving/finance.
- Minors and check-in.
- Safety/security signals.
- Background checks and volunteer eligibility.
- Counseling/care notes.
- Documents and statements.
- Workflows with SQL/Lava.
- API keys and Lava endpoints.
- Person profile custom tabs.
- Public group finders.

Community recipes illustrate several of these risks: finance admin separation, security signal visibility, volunteer safety indicators, and custom person registration visibility ([Add a Non-Finance Admin Security Role](https://community.rockrms.com/recipes/181), [Notify Staff of New Security Signal](https://community.rockrms.com/recipes/494), [Volunteer Capacity Indicator](https://community.rockrms.com/recipes/452), [Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)).

### Temporary Access And Impersonation

Impersonation is useful for debugging but risky. A community recipe describes temporarily changing elevated security level to allow impersonation and then restoring it via workflow; treat this as an example requiring careful review, not official policy ([Just in Time Impersonation](https://community.rockrms.com/recipes/337)).

Temporary access guardrails:

- Prefer test accounts.
- Record who requested access and why.
- Avoid broad admin if view-only is sufficient.
- Set an expiration/review.
- Restore settings after testing.
- Do not use impersonation to bypass policy.
- Disable personal tokens where policy requires.
- Confirm elevated security level is restored.

### Public And Anonymous Access

Public access should be intentional. When a page, block, document type, group finder, Lava endpoint, or API route is public, agents must inspect what data can be reached by changing query strings, IDs, IdKeys, filters, and post bodies.

Public access checklist:

- Test anonymous.
- Test with manipulated route parameters.
- Use IdKeys/GUIDs instead of raw IDs where appropriate.
- Check server-side authorization, not just hidden UI.
- Inspect Lava templates for unguarded entity access.
- Inspect API endpoints with curl/Postman-style direct calls.
- Confirm no API key is visible in page source.
- Confirm file/document types are not public unless intended.

Helix docs warn that endpoints can be accessed outside the frontend and that users can modify parameters, so endpoints must be secured and inputs validated ([Helix Security](https://community.rockrms.com/developer/helix/overview/security)).

### Lava Command Governance

Lava command docs state commands can bypass built-in security and business logic and must be enabled where needed ([Lava Commands](https://community.rockrms.com/lava/commands)). This makes Lava command configuration a security boundary.

Governance:

- Maintain an inventory of blocks with enabled commands.
- Limit SQL/entity commands to trusted staff/admin pages.
- Do not enable commands broadly in Communication Entry unless required.
- Review shortcodes that execute privileged logic.
- Sanitize user-supplied values.
- Avoid raw SQL in public contexts.
- Use `HasRightsTo` where data is not security-filtered.
- Review workflow Lava/SQL attributes after upgrades.

### Security Audits

Recurring audit checklist:

- Security roles and members.
- Rock Administration members.
- Person-specific auth entries.
- Public/all-user page/block/document rules.
- Duplicate and orphaned auth records.
- Former staff access.
- API keys.
- Remote Lava usage.
- Workflow types with public view.
- Document types marked public.
- Data views/reports with sensitive data.
- Public/mobile group finders.
- Custom person tabs.
- Lava command-enabled blocks.
- Multi-node cache consistency, if applicable.

Community recipes provide dashboard and visualizer examples for these audits, but agents should validate any recipe logic before relying on it ([Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol), [Page Security Visualizer](https://community.rockrms.com/recipes/441), [Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)).

## 12. Developer, API, Lava, And Source-Code Landmarks

### `Rock.Security.Authorization`

Primary source-code landmark for standard action constants and authorization infrastructure. The snippet includes constants for common verbs and a cache key ([Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs)).

Use it to verify:

- Exact action names.
- Whether a verb exists in core.
- Whether a custom action name conflicts with core naming.
- SameSite cookie-related settings, if inspecting auth cookie behavior.

### `AuthorizationCacheConsumer`

Source landmark for cache update handling. The snippet shows a consumer applying authorization cache update messages ([AuthorizationCacheConsumer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs)).

Use it to understand:

- Authorization cache updates are message-driven.
- Stale permission behavior may involve cache/message-bus state.
- Multi-node environments may require cache propagation checks.

### Block Authorization APIs

Official docs show:

- `IsUserAuthorized(action)` for current block/user checks.
- Entity `IsAuthorized(action, person)` checks for secured model objects.
- Standard action names.
- `[SecurityAction(...)]` for custom action verbs ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)).

Pattern:

- UI visibility is not enough.
- Server-side event handlers must re-check authorization.
- Entity-specific operations need entity-specific checks.
- Page checks can be used when page-level permission is the intended authority.

### Obsidian Permission Bags

Modern blocks often pass authorization flags to clients. The source pack includes communication detail and entry permission/authorization bags showing action-specific booleans such as approve, cancel, and edit states ([CommunicationDetailPermissionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationDetail/CommunicationDetailPermissionsBag.cs), [communicationDetailPermissionsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/communicationDetailPermissionsBag.d.ts), [communicationEntryAuthorizationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryAuthorizationBag.d.ts)).

Review questions:

- Are permission flags computed server-side?
- Are dangerous actions checked again on submit?
- Does the client hide actions based on accurate flags?
- Are flags named clearly enough for maintenance?

### `SecurityColumn`

Obsidian grids can use a standard `SecurityColumn` to open the security editor modal for a row item ([SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn)). Use standard UI surfaces where possible, because custom permission editors are more likely to omit inheritance, disabled states, or entity titles.

### API Patterns

The v2 API pattern page is the key source for newer endpoint security. It says v2 endpoints are secure by default and need explicit authorization; core-required permissions should be added through migrations ([API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns)).

Review questions:

- Is the endpoint v1/legacy REST or v2?
- Is it decorated/secured?
- Are default auth rules created in a migration?
- Is the endpoint intended for third-party use?
- Does the endpoint validate both auth and input?

### Lava Commands

Lava commands are privileged. The docs warn that commands can bypass built-in security/business logic and must be explicitly enabled in contexts such as HTML blocks and Communication Entry ([Lava Commands](https://community.rockrms.com/lava/commands)).

Review questions:

- Which commands are enabled?
- Who can edit the block/template?
- Is the page public?
- Does the Lava use user-supplied parameters?
- Does it check rights before displaying records?
- Does it execute SQL or workflows?

### Remote Lava

Remote Lava renders submitted templates through an API endpoint and key. The docs warn against browser-visible JavaScript usage because endpoint/key exposure allows arbitrary Lava under that key’s authority ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

Review questions:

- Is the endpoint enabled?
- Is it restricted to HTTPS?
- Where is the key stored?
- Is any JavaScript exposing it?
- What permissions does the linked key/user have?
- Can it be replaced with server-side code?

### Helix Endpoints

Helix security docs warn that endpoints can be invoked externally and parameters can be modified; they recommend securing endpoints, validating inputs, and using IdKeys or GUIDs for query-string identifiers ([Helix Security](https://community.rockrms.com/developer/helix/overview/security)).

Review questions:

- Does the endpoint enforce server-side authorization?
- Does it validate every parameter?
- Does it use IdKey/GUID instead of raw ID?
- Does it assume the frontend is the only caller?
- Does it leak sensitive fields in responses?

### Agent Tools

Rock custom tool docs say every tool inherits Rock security and that public agents should only have tools safe for strangers. They also warn not to expose raw integer IDs to the model; use IdKey and convert internally ([Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools)).

Tool review checklist:

- Who can run the tool?
- What Rock permissions does it rely on?
- Does it expose raw IDs?
- Does it return sensitive data?
- Does it mutate data?
- Is it safe for a public agent?
- Are inputs validated?
- Are outputs minimized?

## 13. Reporting, Analytics, And Model Map

### Reporting Security

RockU includes Reporting Security as part of the reporting curriculum ([Reporting Security](https://community.rockrms.com/rocku/reporting/reporting-security)). The source pack excerpt does not include the full lesson, so agents should verify exact report/data view permission behavior in live Rock or official docs.

Operational model:

- A report can be secured.
- A data view can be secured.
- A page/block displaying the report can be secured.
- The underlying entity may have security.
- Custom SQL/Lava may bypass some of those layers unless explicitly coded.

### Dynamic Data And SQL Reports

Dynamic Data blocks can be powerful and dangerous. The registrations tab recipe explicitly warns that it does not account for registration template security and may show registrations even where templates are restricted ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)). This is the pattern to watch for whenever SQL/Lava joins bypass standard screens.

Audit questions:

- Does the SQL query enforce the same security as the standard UI?
- Does the block filter by current person only where intended?
- Does it expose hidden registrations, financial data, security notes, or documents?
- Can route parameters be changed to view another person’s data?
- Does the page use raw person IDs?
- Does the current user have rights to every row returned?

### DataView API Caveat

Release notes for v17.5 describe a bug where a model’s `./DataView/{id}` endpoint checked permissions on the wrong entity and could deny access even when the person or API key had explicit DataView permission ([Release Notes](https://www.rockrms.com/releasenotes)). If an API DataView route behaves unexpectedly, verify Rock version before redesigning permissions.

Troubleshooting branch:

- If v17.5 or later: inspect DataView security and actor permissions.
- If earlier than the fix: check whether the bug applies and whether an upgrade/hotfix is needed.
- If using an API key: confirm explicit DataView permission on the key’s actor.
- If a model endpoint is involved: inspect model/entity security too.

### Model Map Use

The prompt references Model Map, but the source pack does not include hydrated Model Map entries. For live work, use Model Map to confirm:

- Entity class.
- Table name.
- Primary key.
- Guid/IdKey availability.
- Security-related navigation properties.
- Parent authority behavior if documented.
- Foreign key relationship from `Auth` records to target entity.
- Whether the entity implements authorization.

Do not invent fields. If a playbook says “query `Auth`,” first verify table and column names in the live Rock version.

### Analytics For Security Health

Useful security analytics include:

- Count of public page/block rules.
- Count of public document types.
- Count of person-specific auth rules.
- Count of inactive/former staff in security roles.
- Count of API keys by purpose/owner.
- Count of auth records pointing to deleted entities.
- Duplicate direct rules for same entity/action/principal.
- Workflow types with no explicit View security.
- Data views/reports containing sensitive entity types.
- Lava command-enabled HTML blocks.
- Group finder pages that do not check rights.
- Check-in security code volume for very large ministries.

A Triumph resource warns that Rock will not allow a check-in security code to be reused within a day, and very large ministries using short codes can approach code-space limits, causing performance issues ([Heads Up: Check-in for Very Large Ministries](https://www.triumph.tech/resources/check-in-for-very-large-ministries)). This is a security-adjacent operational metric: code length and uniqueness policy affect both safety and performance.

## 14. Version And Release Caveats

### v14: IdKey In Public Obsidian Blocks

Developer security docs say that starting with Rock v14 Obsidian blocks, IdKey can/should be used instead of raw IDs, especially in public-facing blocks ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)). Agents reviewing public routes should flag raw integer IDs for replacement or mitigation.

### v14: Check-in Manager Delete Attendance Verb

The check-in documentation notes that Rock 14.0 added a security verb controlling who can delete attendance from the Check-in Manager Roster ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). If a staff user cannot delete attendance, inspect the specific check-in/attendance delete permission rather than broadly granting edit/admin.

### v15: Fluid Lava Requirement For Some Community Security Tools

The Page Security Visualizer recipe says it requires the Fluid Lava engine and will not work on DotLiquid ([Page Security Visualizer](https://community.rockrms.com/recipes/441)). If using community audit tooling, verify Lava engine/version first.

### v16.7: Security Cookie Rejection Setting

A Triumph release spotlight reports a v16.7 setting to reject security cookies older than a configured date, useful after login token misuse or sharing; users logged in before the date must re-login ([GitHub Spotlight: 9/6/2024](https://www.triumph.tech/resources/github-spotlight-962024-2)). Verify the exact setting name and current availability in the Rock instance before using it.

### v17: v2 API Secure By Default

The developer API patterns page says v17 introduced v2 API endpoints and that secured endpoints default to no access until explicitly authorized ([API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns)). Plugin and custom endpoint work must include security review and migrations where appropriate.

### v17.5: DataView Endpoint Permission Fix

Release notes describe a v17.5 fix for model `./DataView/{id}` endpoints checking permissions on the wrong entity ([Release Notes](https://www.rockrms.com/releasenotes)). If a DataView endpoint denies access unexpectedly, verify whether the instance is before or after this fix.

### v17.8: Document Upload Security Fix

Release notes describe a v17.8 fix for Entity Document Add workflow action uploads not linking files to parent documents, causing File Type security to be used instead of Document Type security. The fix also copies security to built-in document types if no security was configured and surfaces public-viewable warnings ([Release Notes](https://www.rockrms.com/releasenotes)). Document security audits must account for this version boundary.

### v18.3 And v19.1: Workflow Type View Hardening And Document Type Visibility

Release note excerpts for v18.3 and v19.1 mention workflow type view hardening and document type view permission changes/public labels ([Release Notes](https://www.rockrms.com/releasenotes)). If an upgrade changes workflow visibility or document warnings, inspect release notes and tech bulletins before reverting security.

### v18.3/v19.1/v20 Pre-Alpha Notes

A Triumph GitHub spotlight mentions v18.3 document security fixes, v19.1 highlights, and v20 pre-alpha context ([GitHub Spotlight: 5/21/2026](https://www.triumph.tech/resources/github-spotlight-5212026)). Treat third-party spotlights as helpful release awareness, then confirm against official release notes or source.

## 15. Implementation Playbooks

### Playbook: Audit Who Can Administrate A Page

1. Identify page route/title/ID.
2. Inspect direct page `Administrate` rules.
3. Inspect parent page inherited `Administrate`.
4. Inspect block-level `Administrate` for blocks on the page.
5. Resolve each role to active members.
6. Resolve person-specific entries.
7. Flag public/all-user admin rules immediately.
8. Flag former staff, inactive users, and broad admin roles.
9. Test with a non-admin account.
10. Document final effective access and source of inheritance.

Useful source patterns: page/block visualizer and security dashboard recipes ([Page Security Visualizer](https://community.rockrms.com/recipes/441), [Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol)).

### Playbook: Build A Staff-Only Report Page

1. Create or identify the Data View.
2. Secure the Data View to the staff role that should use it.
3. Create or identify the Report.
4. Secure the Report.
5. Create the page under the appropriate internal hierarchy.
6. Secure page `View` to the staff role.
7. Add the report/dynamic block.
8. Secure block `View` and `Administrate`.
9. Avoid SQL that bypasses entity security.
10. Test as authorized staff, unauthorized staff, and anonymous.
11. If exposed through API, test endpoint permissions.

Source caution: custom report tabs can expose data if they do not account for underlying security ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)).

### Playbook: Create A Public Group Finder Safely

1. Identify group types and groups eligible for public display.
2. Confirm which groups should be hidden.
3. Configure page/block public access only as needed.
4. Review block template.
5. Add `HasRightsTo` checks where the returned group collection is not security-filtered.
6. Avoid exposing private group attributes.
7. Use IdKeys/GUIDs for detail links where possible.
8. Test anonymous with changed filters and route parameters.
9. Test hidden/private group IDs/IdKeys.
10. Document public display rules.

Source caveat: mobile Group Finder results do not account for user security by default ([Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

### Playbook: Harden A Workflow Type

1. Identify workflow type and purpose.
2. Classify as public-entry, staff, admin, or system.
3. Inspect View/Edit/Administrate.
4. Restrict View if workflow data contains sensitive values.
5. Restrict Edit/Administrate to workflow admins.
6. Inspect actions using SQL, Lava, entity updates, documents, communications, or web requests.
7. Sanitize Lava-derived SQL values where applicable.
8. Inspect workflow entry pages/blocks.
9. Test launch and view behavior.
10. Review version hardening notes.

Sources: release notes and workflow hardening source snippet ([Release Notes](https://www.rockrms.com/releasenotes), [291_HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs)).

### Playbook: Review A Custom Lava/SQL Block

1. Identify page and block.
2. Inspect page/block security.
3. Inspect enabled Lava commands.
4. Identify all parameters: route, query string, form, person context.
5. Identify all entities queried.
6. Add or verify `HasRightsTo` checks.
7. Sanitize user input.
8. Avoid raw SQL in public contexts.
9. Avoid direct person ID route exposure.
10. Test unauthorized users and anonymous.
11. Review output for hidden sensitive fields.

Sources: Lava command warning and Rock architecture note that Lava authors may access data not available to the current person and must handle rights checks ([Lava Commands](https://community.rockrms.com/lava/commands), [Rock Architecture](https://community.rockrms.com/developer/developer-codex/coding-standards/rock-architecture)).

### Playbook: Add A v2 API Endpoint

1. Confirm endpoint belongs to the v2 API pattern.
2. Decide whether it should be secured.
3. Define the intended actor roles.
4. Add server-side authorization.
5. If core staff need it, add default permissions in a migration.
6. If third-party only, leave denied by default until configured.
7. Validate all input.
8. Use IdKeys/GUIDs instead of raw IDs where possible.
9. Test with no auth, low-privilege auth, intended auth, and admin.
10. Document required permissions.

Source: v2 API secure-by-default guidance ([API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns)).

### Playbook: Rotate An Exposed API Key

1. Identify where the key was exposed.
2. Identify linked actor and permissions.
3. Disable or revoke the old key.
4. Create a replacement key only if the integration is still needed.
5. Store key server-side.
6. Remove browser/client exposure.
7. Rotate credentials in dependent systems.
8. Review logs for suspicious use.
9. Reduce permissions if overbroad.
10. Document the incident and owner.

Source: REST/API key and remote Lava warnings ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

### Playbook: Review Document Security After Upgrade

1. Confirm Rock version.
2. Identify document types.
3. Identify paired file types.
4. Inspect View rules on built-in and custom document types.
5. Check for public-viewable labels/warnings.
6. Inspect workflow-created documents.
7. Verify binary files are linked to parent documents.
8. Test as unauthorized user.
9. Compare file URL access vs document UI access.
10. Update document type permissions before changing file type permissions if document type is intended authority.

Source: v17.8 document upload/document type security fix ([Release Notes](https://www.rockrms.com/releasenotes)).

## 16. Troubleshooting Decision Tree

### User Cannot See A Page

1. Is the user logged in as the expected person?
2. Does the person have an active login?
3. Is the page route correct?
4. Does the page have direct `View` security?
5. Does a parent page deny or allow?
6. Is the user in the allowed role?
7. Is there a deny rule for the user or role?
8. Does the page load but block is hidden?
9. Does the site require a different context?
10. Is authorization cache/session stale?

Check page and block authorization separately, then inspect inherited rules with a visualizer-style page tree if the direct rule does not explain the result ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Page Security Visualizer](https://community.rockrms.com/recipes/441), [AuthorizationCacheConsumer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs)).

If the page loads for admins only, do not immediately add the user to Rock Administration. Identify the missing `View` rule.

### User Can See Page But Not Button

1. Identify the button action.
2. Inspect block action security.
3. Inspect custom security verbs.
4. Inspect entity-specific permission for the row/object.
5. Inspect server-side permission bag if Obsidian.
6. Test direct submit/post if possible.
7. Confirm the block code checks `IsUserAuthorized` or entity `IsAuthorized`.

Source pattern: developers must check action-level permissions inside blocks ([Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks)).

### User Can See Too Much Data

1. Identify where data comes from.
2. Is it a standard block, SQL, Lava, report, or API?
3. Does the data source enforce security?
4. Does the custom template use `HasRightsTo`?
5. Are route/query parameters changeable?
6. Are raw IDs exposed?
7. Does the user have broad role access?
8. Is a person-specific allow present?
9. Is the data public because page/block is public?
10. Does a recipe/customization warn it ignores security?

Source caution: custom registration tab can expose restricted registrations if not security-aware ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)).

### API Key Gets Permission Denied

1. Confirm key is active.
2. Confirm correct header.
3. Confirm endpoint URL/version.
4. Identify linked actor.
5. Test actor’s UI permission.
6. Inspect endpoint security.
7. Inspect entity/data view/report security.
8. If v2 endpoint, confirm explicit authorization exists.
9. If DataView route, check v17.5 caveat.
10. If remote Lava, confirm HTTPS and command/security settings.

Sources: REST API, v2 API, and DataView endpoint fix ([The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns), [Release Notes](https://www.rockrms.com/releasenotes)).

### API Key Works But Should Not

1. Disable key if exposure is active.
2. Identify linked actor and roles.
3. Inspect endpoint security.
4. Inspect broad role permissions.
5. Inspect `ViewAll`, admin, or entity type security.
6. Inspect remote Lava or custom endpoint bypass.
7. Rotate key.
8. Recreate with least privilege.
9. Move key out of client-side code.
10. Review logs.

Source warning: remote Lava with exposed key allows arbitrary Lava under that key’s authority ([Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

### Workflow Visible To Wrong Users

1. Inspect Workflow Type View.
2. Inspect workflow list/detail page security.
3. Inspect block security.
4. Inspect role memberships.
5. Check upgrade version and hardening migrations.
6. Confirm no public/all-user rule.
7. Inspect workflow data sensitivity.
8. Restrict View to staff/admin roles as appropriate.

Source: workflow type view hardening release notes ([Release Notes](https://www.rockrms.com/releasenotes)).

### Document Or File Visible To Wrong Users

1. Identify file/document URL.
2. Determine whether it is linked to a Document.
3. Inspect Document Type security.
4. Inspect Binary File Type security.
5. Check whether workflow uploaded it.
6. Confirm Rock version relative to v17.8 fix.
7. Test as anonymous and low-privilege user.
8. Fix document type permissions if document type is intended authority.
9. Fix file type permissions if generic binary file exposure is involved.

Source: document workflow upload security fix ([Release Notes](https://www.rockrms.com/releasenotes)).

### Group Finder Shows Private Groups

1. Identify group finder block and platform.
2. Inspect group selection/filter settings.
3. Inspect group/group type security.
4. Inspect template.
5. Add `HasRightsTo` check if returned groups are not security-filtered.
6. Remove sensitive attributes from output.
7. Test anonymous and low-privilege users.
8. Test direct detail links.

Source: mobile Group Finder caveat ([Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

### Permission Change Did Not Apply

1. Confirm the rule was saved.
2. Confirm it was saved on the correct entity.
3. Confirm action verb.
4. Confirm role membership.
5. Confirm user logged out/in if membership/session is stale.
6. Check direct deny rules.
7. Check inheritance.
8. Check cache/message-bus state in multi-node environments.
9. Check custom code path.
10. Test with another controlled account.

Source: authorization cache consumer source snippet ([AuthorizationCacheConsumer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs)).

## 17. Agent Task Recipes

### Recipe: Answer “Who Has Access To This?”

Return:

- Secured object.
- Action verb.
- Direct allows.
- Direct denies.
- Inherited source.
- Effective roles.
- Effective people, if needed.
- Person-specific exceptions.
- Public/all-user access.
- Unknowns requiring live test.

Do not answer from direct `Auth` rows alone unless the question is explicitly “what rules are configured?” The role inspector recipe warns direct rows do not account for inheritance ([Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)).

### Recipe: Answer “Why Was I Denied?”

Return:

- Actor identified.
- Requested action.
- Object identified.
- Direct rule result.
- Inherited rule result.
- Role membership state.
- Version caveat checked.
- Next remediation.

Do not stop at direct `Auth` rows: Rock security includes inherited authority and code-level action checks, and the role inspector recipe explicitly warns that direct row listings do not account for inheritance ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)).

Example shape:

```markdown
The denial is for `Edit` on the Group Detail block, not for `View` on the page. The user can load the page through role `X`, but the block does not grant `Edit`, and the group entity also does not grant `Edit`/`ManageMembers`. Add the user to the group manager role or grant the role `ManageMembers` on the target group/group type, then retest as that user.
```

### Recipe: Review A Permission Change Request

Before making changes, classify:

- Is this access temporary or durable?
- Does an existing role match?
- Does the requested action require View, Edit, Administrate, Approve, Delete, Refund, or ManageMembers?
- Is the data sensitive?
- Is there a lower-scope object?
- Does this require workflow/report/API changes too?

Then implement the smallest change and test.

### Recipe: Review A Custom Agent Tool

Use Rock’s custom tool guidance:

- Confirm who can run the tool.
- Confirm tool security before attaching to an agent.
- For public agents, include only stranger-safe tools.
- Do not return raw integer IDs to the model; use IdKey and convert internally.
- Validate input.
- Avoid exposing sensitive fields.
- Re-check permissions server-side before mutation.

Source: [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools).

### Recipe: Review A Public Route

Inspect:

- Route parameters.
- Raw IDs vs IdKeys/GUIDs.
- Page View.
- Block View.
- Entity-specific authorization.
- Lava commands.
- API calls in browser.
- File/document links.
- Query string manipulation.
- Anonymous test.
- Low-privilege authenticated test.

Sources: IdKey guidance, Helix security, and remote Lava warnings ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava)).

### Recipe: Review A Security Role

Return:

- Role name.
- Purpose/description.
- Active members.
- Former/inactive members.
- Direct auth entries.
- Sensitive domains granted.
- Deny rules.
- Person-specific overlaps.
- API keys or workflows depending on the role.
- Recommended cleanup.

Use direct `Auth` listing as a starting point, not final effective access ([Security Role Permissions Inspector](https://community.rockrms.com/recipes/243)).

### Recipe: Review After Upgrade

Check:

- Release notes for the exact version.
- Workflow type view changes.
- Document type/file type changes.
- API endpoint behavior changes.
- Security cookie/token settings.
- New action verbs.
- Lava/shortcode deprecations.
- Public-viewable warnings.
- Custom recipes relying on old behavior.
- AI assistant boundaries. Triumph's AI ministry discussion is useful public training context: AI can assist ministry work, but data boundaries, staff review, and live-system verification govern what an agent should see or do ([AI in Digital Ministry](https://www.triumph.tech/resources/ai-in-digital-ministry)).

Sources: [Release Notes](https://www.rockrms.com/releasenotes), [GitHub Spotlight: 9/6/2024](https://www.triumph.tech/resources/github-spotlight-962024-2), [GitHub Spotlight: 5/21/2026](https://www.triumph.tech/resources/github-spotlight-5212026).



















<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `272`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| official | risk | Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| rocku-confirmed | configuration | The Mobile Check-in Launcher page should enable the virtual kiosk devices and list the check-in configuration and areas that are valid for the campuses served by that page. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| rocku-confirmed | operational_guidance | Person Notes should be handled as structured staff context on a person record; note type, visibility, sensitivity, and lifecycle matter as much as the note text itself. | [source](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1) |
| rocku-confirmed | operational_guidance | Use Note Types to govern where notes appear, how they are categorized, and which staff roles can create or view sensitive notes; do not treat all person notes as one undifferentiated field. | [source](https://community.rockrms.com/rocku/core-concepts/note-types) |
| rocku-confirmed | operational_guidance | The Person Profile is a dense operational surface; agents should identify which tab, block, badge, note, attribute, or action is involved before troubleshooting or changing access. | [source](https://community.rockrms.com/rocku/individuals-in-rock/person-profile) |
| rocku-confirmed | operational_guidance | Adding pages and blocks changes both navigation and authorization; agents should inspect site, page hierarchy, route, block type, zone, and inherited security before publishing. | [source](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) |
| rocku-confirmed | operational_guidance | Content Channel View pages should be reviewed as both CMS presentation and data exposure surfaces because channel item lists can reveal titles, dates, attributes, or detail links. | [source](https://community.rockrms.com/rocku/content-channels/content-channel-view) |
| rocku-confirmed | operational_guidance | Advanced HTML blocks are powerful CMS surfaces because they can combine markup, Lava, context, and sometimes enabled commands; treat edit access as privileged. | [source](https://community.rockrms.com/rocku/cms/advanced-html-block) |
| rocku-confirmed | operational_guidance | When diagnosing personalization, inspect the audience rule, person data used by the rule, fallback content, cache behavior, and the exact logged-in or anonymous state being tested. | [source](https://community.rockrms.com/rocku/cms/personalization) |
| rocku-confirmed | operational_guidance | Personalization should be reviewed as conditional content delivery, not as a security substitute; hidden or targeted content still needs proper page, block, and entity authorization. | [source](https://community.rockrms.com/rocku/cms/personalization) |
| rocku-confirmed | operational_guidance | Mobile check-in block text can be customized and Lava-enabled, but copy should account for where the visitor is in the flow because Rock may not know the person's identity on early screens. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| More |  | 260 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `73`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Account Protection Profiles Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/account-protection-profiles) | approved_for_public_distillation | 3 | media-insight:06f483c71c224790 |
| [Adding Pages and Blocks Transcript Insight](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) | approved_for_public_distillation | 2 | media-insight:7848aa46e6ac3794 |
| [Adding Steps Transcript Insight](https://community.rockrms.com/rocku/engagement/adding-steps) | approved_for_public_distillation | 2 | media-insight:3910dddf1fe8be0c |
| [Advanced HTML Block Transcript Insight](https://community.rockrms.com/rocku/cms/advanced-html-block) | approved_for_public_distillation | 2 | media-insight:2cf056c2b84e6365 |
| [Assessments - Emotional Intelligence (EQ) Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/assessments-emotional-intelligence) | approved_for_public_distillation | 2 | media-insight:2d198493692adb6c |
| [Attendance Self-Entry Transcript Insight](https://community.rockrms.com/rocku/check-in/attendance-self-entry) | approved_for_public_distillation | 3 | media-insight:1fb05cc8930bc9e2 |
| [BI Embed Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report) | approved_for_public_distillation | 3 | media-insight:5fc8b3a315612c59 |
| [Background Checks Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/background-checks) | approved_for_public_distillation | 3 | media-insight:c2c19665d7147da4 |
| More |  | 65 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->



















## 18. Source Map And Dependency Notes

### Primary Source Map

| Topic | Best Source(s) |
| --- | --- |
| Standard action constants | [Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs) |
| Authorization cache | [AuthorizationCacheConsumer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/AuthorizationCacheConsumer.cs) |
| Block security checks | [Securing Access to Your Blocks](https://community.rockrms.com/developer/101---launchpad/securing-access-to-your-blocks), [Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks) |
| Rock security concepts | [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Rock Security Video](https://community.rockrms.com/developer/videos/70) |
| v2 API security | [API Patterns](https://community.rockrms.com/developer/developer-codex/coding-standards/api-patterns) |
| REST API auth | [The Rock Rest API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) |
| API key purpose | [ApiKeyPurpose.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Security/ApiKeyPurpose.cs), [apiKeyPurpose.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Security/apiKeyPurpose.ts) |
| Lava command risk | [Lava Commands](https://community.rockrms.com/lava/commands) |
| Remote Lava risk | [Using Lava Remotely](https://community.rockrms.com/lava/remote-lava) |
| Helix endpoint security | [Helix Security](https://community.rockrms.com/developer/helix/overview/security) |
| Agent tool security | [Writing Custom Tools](https://community.rockrms.com/developer/ai-agents/writing-custom-tools) |
| Obsidian security UI | [SecurityColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/securitycolumn) |
| Obsidian permission bags | [CommunicationDetailPermissionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationDetail/CommunicationDetailPermissionsBag.cs), [communicationEntryAuthorizationBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryAuthorizationBag.d.ts) |
| Group security | [Group Security](https://community.rockrms.com/rocku/groups/group-security), [Group Finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder) |
| Tag security | [Tag Security](https://community.rockrms.com/rocku/individuals-in-rock/tag-security) |
| Reporting security | [Reporting Security](https://community.rockrms.com/rocku/reporting/reporting-security), [Release Notes](https://www.rockrms.com/releasenotes) |
| Security operations context | [Episode 125: Security](https://shows.acast.com/rock-cast/episodes/episode-125-security), [AI in Digital Ministry](https://www.triumph.tech/resources/ai-in-digital-ministry) |
| Workflow/document release caveats | [Release Notes](https://www.rockrms.com/releasenotes), [291_HardenCoreWorkflowSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs) |
| Security dashboards/audit examples | [Security Management - Data Integrity and QoL](https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol), [Page Security Visualizer](https://community.rockrms.com/recipes/441), [Security Role Permissions Inspector](https://community.rockrms.com/recipes/243) |

### Dependency Notes: People

Security depends on the People domain because authorization almost always resolves to a person and their relationships:

- Person record.
- User login.
- Security role memberships.
- Account protection profile.
- Signals, badges, documents, and profile tabs.
- External identity mapping for mobile login.

Verify live person/login mapping before making access changes.

### Dependency Notes: Groups

Security depends on Groups because roles are group-like and many protected ministry objects are groups:

- Security roles.
- Group membership.
- Group type inheritance.
- Group finder visibility.
- `ManageMembers`.
- Attendance and scheduling actions.

For group visibility, always inspect both group security and template filtering.

### Dependency Notes: API

Security depends on API because integrations and modern blocks can bypass normal UI paths:

- REST cookie/token auth.
- API keys.
- v2 endpoint security.
- Remote Lava.
- Auth clients/scopes/claims.
- Mobile/TV app keys.
- Agent tools.

API security must be tested with direct requests, not only UI behavior.

### Dependency Notes: CMS

Security depends on CMS because pages and blocks are the front door to much of Rock:

- Site/page hierarchy.
- Block security.
- HTML/Lava blocks.
- Content channels.
- Obsidian security editor.
- Public routes.
- Mobile shells.

If a page is public, every block and data source on it must be reviewed.

### Dependency Notes: Workflows

Security depends on Workflows because workflows can automate privileged operations:

- Workflow Type permissions.
- Workflow entry blocks.
- SQL/Lava action attributes.
- Entity updates.
- Document uploads.
- Communications.
- Scheduled jobs.

Release notes show Rock continues to harden workflow security, so always check version caveats before assuming current behavior.

### Live Verification Requirements

Before finalizing production changes, inspect these in the actual Rock instance:

- Current Rock version and applied hotfixes.
- Exact `Auth` record schema and target entity IDs.
- Entity parent authority for the specific object.
- Current role membership.
- User login mapping.
- API key owner/purpose/linked actor.
- Page and block security dialogs.
- DataView, Report, Workflow Type, Document Type, and File Type security.
- Lava command settings.
- Whether custom blocks define custom action verbs.
- Whether a page/block/template uses raw IDs.
- Whether release notes apply to the installed version.

These checks are required because security behavior is version- and instance-specific; official docs, source constants, release notes, and live `Auth`/page/block state must agree before changing production access ([Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security), [Authorization.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs), [Release Notes](https://www.rockrms.com/releasenotes)).

This guide is a draft authority synthesis. Treat it as the operating manual for investigation and implementation, then anchor every production change in live Rock evidence.
