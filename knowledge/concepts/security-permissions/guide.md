---
id: authored-security-permissions
title: Security And Permissions
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "ced36397a2f4c709aa1fbdeccb5064bae106402b82e94779d502a6c645e45cd2"
---

# Security And Permissions

## 1. Executive Summary For Agents

Rock authorization is evaluated for a specific person, action, and secured item. Access may depend on role membership, explicit item rules, inherited rules, parent entities, page and block security, data-level security, and the authenticated identity behind an API or automation. Never infer authorization from a visible menu, reachable route, hidden control, opaque identifier, or successful administrator test.

Use this operating sequence:

1. Identify the exact person or integration identity.
2. Identify the secured entity and requested action.
3. Inspect direct and inherited permission rules in their evaluated order.
4. Inspect every surrounding boundary, such as the page, block, parent application, content entity, endpoint, workflow, or API controller.
5. Test with the intended identity, plus an unauthorized identity when exposure is possible.
6. Record what was verified separately from what is merely configured or inferred.

Rock's developer guidance treats authorization as an action evaluated against a component, while the source implementation exposes the action vocabulary used by those checks. Use the fuller inspection procedure later in this guide to evaluate ordered direct and inherited rules for the exact identity, object, and action. [Rock Security developer guidance](https://community.rockrms.com/developer/303---blast-off/rock-security), [Authorization source snapshot](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/Authorization.cs)

For APIs, Lava, Helix, workflows, reporting, and AI tools, authentication is only the beginning. The execution surface must authorize the requested operation, validate inputs, preserve business rules, and return only the data required for the task. Rock's authorization implementation defines the action vocabulary and evaluation surface used by these checks. [Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [Lava Commands](https://community.rockrms.com/lava/commands), [Authorization source snapshot](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/Authorization.cs)

## Scope And Boundaries

This guide covers:

- Security roles and item-level authorization.
- Allow/Deny ordering and inherited security.
- Login, user accounts, Account Protection Profiles, passwordless login, two-factor authentication, external providers, and login history.
- REST authentication, identity-bound links, IdKeys, Lava APIs, and Helix endpoints.
- Page, block, content-channel, personalization, Person Profile, note, communication, reporting, and background-check exposure.
- Operational controls for workflows, mobile check-in, Sign-Ups, AI agents, and other permission-sensitive features.
- Version-specific security behavior and release-note checks.

This guide does not define the underlying People, Groups, CMS, API, Workflow, Check-in, Communications, or Reporting features. It addresses their authorization and exposure boundaries. It also does not prove that a particular installation is secure. The supplied evidence includes bounded read-only verification of several structural surfaces, but no target installation was inspected while authoring this guide.

Authentication, authorization, personalization, obscurity, and abuse prevention are different controls:

- **Authentication** establishes an identity.
- **Authorization** determines what that identity may see or do.
- **Personalization** selects content for an audience; it is not a security boundary.
- **Opaque identifiers** make guessing harder; they do not authorize access.
- **CAPTCHA** mitigates automated abuse; it does not replace authentication, authorization, validation, or rate limiting.

These distinctions are supported across Rock’s [security documentation](https://community.rockrms.com/documentation/core-concepts/security), [Rock Security developer guidance](https://community.rockrms.com/developer/303---blast-off/rock-security), and [v19 CAPTCHA documentation](https://community.rockrms.com/documentation/core-concepts/security/captcha/intro-to-captcha).

## 3. Security And Permissions Mental Model

Evaluate access as a chain:

`identity → role membership → secured entity → requested action → ordered direct rules → inherited rules → surrounding boundaries → data returned or mutation performed`

### The Object Layer

The object layer identifies the specific securable item whose rules must be evaluated. Rock secures pages, blocks, workflows, entities, data views, financial accounts, and other concrete objects independently, so access to a containing page does not prove access to its block, workflow, entity, or returned data. For a diagnosis, resolve the exact object type and identifier, then inspect its own rules and the parent hierarchy from which it may inherit. Treat route visibility or a rendered control only as discovery evidence. Pages and blocks can impose separate checks, and workflows or entity records can add authorization boundaries after the page is already visible. [Intro to Security](https://community.rockrms.com/documentation/core-concepts/security/overview/intro-to-security), [Rock Security developer guidance](https://community.rockrms.com/developer/303---blast-off/rock-security)

### The Action Layer

The action layer identifies the operation being requested on that object. Common actions include View, Edit, and Administrate. An immutable public source snapshot also defines action names used in parts of Rock, including Delete, Approve, Interact, Refund, and ManageMembers; this is implementation evidence, not a promise that every entity exposes every action. Object authorization therefore answers which object is being secured, while action authorization answers what the current identity may do to it. [Intro to Security](https://community.rockrms.com/documentation/core-concepts/security/overview/intro-to-security), [Authorization source snapshot](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/Authorization.cs)

Most secured items inherit permissions from a parent unless direct rules are added. Direct rules are evaluated from top to bottom, and the first rule matching the current person determines the result. A broad Deny above a narrower Allow can therefore block the narrower role. The security editor identifies both item permissions and inherited permissions, including the parent supplying an inherited rule. [Handle Permissions](https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions)

A correct result at one layer does not prove the complete operation is authorized. For example:

- A visible page does not prove its block, content item, or endpoint is authorized.
- A hidden block does not prove its underlying endpoint is protected.
- A successful administrator test does not prove the intended role has access.
- A valid API credential does not prove the identity has permission for the controller or entity.
- An IdKey does not replace server-side entity authorization.
- A personalized content rule does not protect the underlying data.
- A tool exposed to an AI agent is not safe merely because Rock recognizes the current person.

## Authorization And Security Roles

Use security roles as the normal unit of access. Rock permits individual Allow and Deny rules, but its official guidance favors roles because person-specific rules are harder to maintain and more prone to inconsistency. Plan role scope and naming before adding roles, and review the roles shipped with Rock before creating a parallel structure. Rock documents prefixes such as `RSR`, `APP`, and `WEB`; other groups can also be marked as security roles. [Intro to Security Roles](https://community.rockrms.com/documentation/core-concepts/security/security-roles/intro-to-security-roles), [Administering Security Roles](https://community.rockrms.com/documentation/core-concepts/security/security-roles/administering-security-roles)

Security roles also have an Elevated Security Level that contributes to a person’s Account Protection Profile. The documented values are None, High, and Extreme. Current v19 guidance recommends Extreme for new roles that provide access inside Rock, while organizations should verify how the resulting protection profile affects login, token, merge, and passwordless behavior before rollout. [Administering Security Roles](https://community.rockrms.com/documentation/core-concepts/security/security-roles/administering-security-roles), [Configure Security Settings](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/configure-security-settings)

When copying an existing access pattern, Rock can clone a security-role group together with its security configuration, but group members are not copied. Rename the clone, review its description and settings, and explicitly assign members only after validating its inherited privileges. [Cloning Security Role Groups](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/cloning-security-role-groups)

### Permission evaluation

For each authorization question, capture:

- Person or integration identity.
- Entity type and entity ID or GUID.
- Requested action.
- Direct permission rules in order.
- Inherited rules and their source.
- Relevant role memberships.
- Additional parent or child entities that may impose a separate check.

Use `Admin Tools > Settings > Inspect Security` to evaluate a person against an entity type and entity ID or GUID. The result can identify the source of the effective permission, including an inherited parent. Rock also provides an administrative unlock operation for accidental self-lockout; treat that as a recovery control, not a substitute for understanding the rule chain. [Inspect Security](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/inspect-security), [Handle Permissions](https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions)

### Auditing changes

The Security Change Audit records changes to an item’s permission rules, including rules assigned directly to a person or to a role. It does not record adding or removing a person from a security role. When investigating a changed outcome, review both the item audit and the relevant role membership history or current membership through an appropriate separate process. [View the Security Change Audit](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/view-the-security-change-audit)

## Login, Accounts, And Protection Profiles

A Rock user account authenticates a person and connects that identity to the pages, tools, and information available to them. Authentication success does not itself grant authorization; effective access still depends on secured items and role membership. [Intro to User Accounts](https://community.rockrms.com/documentation/core-concepts/security/user-accounts/intro-to-user-accounts), [Intro to Login and Authentication](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/intro-to-login-and-authentication)

Account Protection Profiles influence safeguards for people whose access is more sensitive. Current documented settings include controls for duplicate checking, predictable file identifiers, protected-record merges, personal tokens, two-factor authentication, passwordless throttling and session duration, disabling passwordless sign-in for selected profiles, and rejecting older authentication cookies. Some security settings intentionally favor account protection over duplicate prevention. [Configure Security Settings](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/configure-security-settings)

If an impersonation token or similar sensitive credential may have been exposed, changing the cookie-rejection cutoff alone does not disable the token. Follow the current incident guidance, revoke the relevant capability, reject affected sessions where appropriate, and notify affected stakeholders according to organizational policy. [Configure Security Settings](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/configure-security-settings)

### Passwordless login and 2FA

Passwordless login in the documented Obsidian Login and Account Entry blocks uses email links or SMS codes. It depends on working communication configuration, block settings, selected templates, IP throttling, session duration, and Protection Profile restrictions. Shared family email addresses can also produce a person-selection step. [Use Passwordless Login](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/use-passwordless-login)

Rock’s documented 2FA flow uses email or SMS as an additional step and is enabled by Protection Profile. It requires the related communication configuration. People using passwordless login who are also subject to 2FA must establish a traditional username and password. Built-in external providers such as Google and Facebook do not satisfy Rock’s documented 2FA flow; enabling 2FA while the Login block hides database login and redirects directly to one external provider can lock users out. [Two-Factor Authentication](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/two-factor-authentication)

The Obsidian Login block can also send confirmation when a protected person uses an unrecognized browser. The feature is disabled until Account Protection Profiles are selected in the block settings, and its recognition cookie is documented as expiring after a year while being renewed on login. [Register on an Unrecognized Browser](https://community.rockrms.com/documentation/core-concepts/security/user-accounts/register-for-an-account-on-an-unrecognized-br)

### External authentication and OIDC

After a fresh installation, the Rock database provider is the active authentication provider. Additional providers must be configured and activated, then enabled on the relevant Login blocks. Provider configuration can include callback URLs, client identifiers, client secrets, requested scopes, and provider-side review. Protect those credentials and validate every configured login route rather than assuming activation affects all Login blocks. [External Authentication](https://community.rockrms.com/documentation/core-concepts/security/external-authentication-services/intro-to-external-authentication), [Google Authentication](https://community.rockrms.com/documentation/core-concepts/security/external-authentication-services/set-up-google-authentication), [Auth0 Authentication](https://community.rockrms.com/documentation/core-concepts/security/external-authentication-services/set-up-auth0-authentication)

Rock can also act as an OpenID Connect authorization server so an external client can rely on Rock-authenticated identity. Keep the server/client distinction explicit and verify client configuration, requested scopes, redirect behavior, and installed-version fixes. Rock v19.4 release notes include an OIDC authorization fix involving the `openid` scope and returned ID token. [Intro to OpenID Connect](https://community.rockrms.com/documentation/core-concepts/security/rock-authentication/intro-to-openid-connect), [Rock release notes](https://www.rockrms.com/releasenotes)

### Login investigation

Use `Admin Tools > Settings > Security > Login History` for successful and unsuccessful attempts. The Person Profile History tab provides a person-scoped view. Documented statuses include verification required, unconfirmed user, user not found, invalid credentials, password change required, locked out, and invalid OIDC client. Use the recorded failure reason before changing credentials, providers, or protection settings. [Use Login History](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/use-login-history)

## API Authentication And Identity-Bound Links

Rock REST requests require authorization. The approved official claim identifies two supported approaches: an HTTP cookie associated with an existing Rock user session or an `Authorization-Token` that accompanies subsequent API requests. The authenticated identity must still have permission for the requested API surface and data. [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) (approved claim `claim:2cb25390d2b5f4ffeb6f`)

Before diagnosing or changing an integration, identify:

- Exact controller and route.
- HTTP method and whether the operation reads or writes.
- Authenticated person, session, or REST key.
- Entity and action being authorized.
- Direct and inherited grants.
- Token storage, transmission, rotation, and revocation expectations.
- Installed Rock version and applicable release notes.
- Readback or rollback method for writes.

Do not broaden a role merely because a request returns `401`, `403`, or a permission message. First separate missing authentication from insufficient authorization, invalid route or method, version-specific defects, and entity-level restrictions.

Rock v17.5 fixed a REST issue where a model’s `DataView/{id}` endpoint checked permissions on the wrong entity, sometimes denying a person or API key that had explicit DataView permission. If this symptom appears on an older installation, compare the installed version with that fix before rewriting the permission model. [Rock release notes](https://www.rockrms.com/releasenotes)

For public-facing Obsidian blocks beginning with Rock v14, use IdKeys rather than exposing predictable numeric entity IDs in URLs. An IdKey only reduces exposure of sequential identifiers: the server must still validate the referenced entity and authorize the caller. [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security) (approved claim `claim:751d703f1c8d30a9db1e`)

A `PersonActionIdentifier` identifies a person for one bound action, such as an RSVP. It is not a general-purpose login credential or authorization token and must not be accepted for unrelated operations. [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security) (approved claim `claim:9734cd32fce9f8e7c221`)

A reviewed community pattern recommends PATCH rather than PUT when an API v2 integration owns only a subset of an entity, followed by non-production testing and field-scoped readback. This is a community implementation pattern that still requires validation against the installed API documentation, endpoint semantics, and Model Map; the pack does not establish it as universal endpoint behavior. [Community API v2 pattern](https://community.rockrms.com/api-docs)

## CMS, Content, Personalization, And Lava

### Pages and blocks

Adding a page or block changes both navigation and authorization. Before publishing, inspect the site, page hierarchy, route, block type, zone, direct security, and inherited security. When a page is missing or unexpectedly exposed, test the exact user context and compare parent-page, page, and block security instead of treating the route as the only boundary. [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) (approved claims `claim:39735f6a8684f32d8191` and `claim:09bc1e14a8ad2c40145e`)

Content Channel View pages are both presentation and data-exposure surfaces. Lists can reveal titles, dates, attributes, and detail links. Audit the channel, item, block, page, route, and Lava template together. Hiding an item in one rendering path does not prove it is unavailable through another configured view or detail route. [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view) (approved claims `claim:49453ea8932cdc4b0736` and `claim:d5d56ebc6176db44cbc`)

Personalization conditionally selects content based on an audience rule and person state. It is not authorization. Diagnose personalized output by checking the rule, person data used by the rule, fallback content, cache behavior, and exact authenticated or anonymous state; independently secure the page, block, and underlying entity. [Personalization](https://community.rockrms.com/rocku/cms/personalization) (approved claims `claim:64100db2b5d60396b9fd` and `claim:95e015e3407ed10e9e7c`)

### Advanced HTML and Lava commands

Advanced HTML blocks can combine markup, Lava, request or entity context, and enabled commands. Treat edit access as privileged. Review page and block authorization, every enabled Lava command, query-string and context inputs, sanitization, and whether rendered output exposes sensitive entity data. [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block) (approved claims `claim:4c6c24811261384a0eb4` and `claim:7e6e3979faad614f0b42`)

Lava Commands can bypass Rock’s normal security or business-logic paths. Enable only the commands needed on each execution surface. HTML blocks begin with no commands enabled unless configured, so a working command also indicates an explicit configuration decision that should be reviewed. [Lava Commands](https://community.rockrms.com/lava/commands) (approved claim `claim:7bca2f8db03f8f468586`)

Lava APIs can support custom channels such as Apple TV or Roku, but Lava webhooks do not include security by default. The supplied pack’s reviewed read-only conclusion also found no explicit permission check in the inspected webhook handler path. Inspect each configured URL, method, template, and enabled-command set, and add an intentional authentication and authorization boundary before operational use. [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api) (approved claim `claim:410bf6750e90b7193262`)

When Lava produces mobile XAML, use the documented filters that are supported locally in the shell and escape user-entered text, URLs, and strings containing characters such as `&` or `'`. Output escaping protects markup integrity but does not authorize the data being rendered. [Rock Mobile Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava) (approved claim `claim:3b4b8ec335aa0a17968c`)

## Helix Applications And Endpoint Security

Treat every Helix endpoint as callable independently of its front end. The browser interface cannot be the security boundary. Validate all query and body inputs, enforce the caller’s View or Edit rights, avoid GET for mutations, and sanitize values before any SQL use. Endpoint-backed applications require both security and data-integrity review because they can expose data or perform work beyond static rendering. [Helix Security](https://community.rockrms.com/developer/helix/overview/security) (approved claims `claim:72d56e7ee7ef0be4b92e` and `claim:da56681f6277c12df324`)

A complete endpoint review should cover:

- Application and endpoint authorization.
- Endpoint security mode.
- Page and content-block security.
- Enabled Lava commands.
- CSRF behavior for state-changing requests.
- Rate-limit configuration.
- Input allowlists, length bounds, and sanitization.
- Data returned for anonymous, intended-role, and administrator contexts.
- Correct HTTP method and idempotency expectations.
- Readback of mutations and failure behavior.

Reviewed community experience adds two useful hypotheses that require local verification:

- An endpoint using application-level security may fail for anonymous or non-admin users when the parent Lava Application lacks the intended authorization, even if the page and content block are visible. Inspect the endpoint security mode and parent application, then test with the intended role; administrator success is insufficient. [Helix endpoint guidance](https://community.rockrms.com/developer/helix/lava-applications/endpoints)
- Full-page iframe embedding can be affected by Content Security Policy and sandbox behavior. A page-hosted Lava Application block or purpose-built endpoint may provide a clearer integration boundary, but the correct choice depends on current headers, authentication, and application behavior. [Lava Application content blocks](https://community.rockrms.com/developer/helix/lava-applications/content-block)

Rock v19.5 release notes describe a fix for non-administrators being blocked from a Lava Application endpoint when the Lava Application Developer role was inactive, before normal permissions were evaluated. Check the installed version before compensating with broader access. [Rock release notes](https://www.rockrms.com/releasenotes)

## Sensitive People And Ministry Data

### Person Profile and notes

The Person Profile is a collection of tabs, blocks, badges, notes, attributes, and actions. Identify the exact surface before changing access. Permission to view the profile does not imply permission to edit every person-related record; review page, block, entity, action, and field-level exposure. [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile) (approved claims `claim:34144e7226c4a430a307` and `claim:5c53977793c7673b19e9`)

Person Notes are structured staff context, not one undifferentiated text field. Note type, target entity, visibility, sensitivity, author and date metadata, lifecycle, and downstream workflow or report consumers all matter. Use Note Types to govern categorization and which roles may create or view sensitive notes. [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1), [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types) (approved claims `claim:00300ae5ab574ad7c48b`, `claim:09c6a4834867ba6879d7`, and `claim:c161a6f06a707e04dbea`)

### Background checks

Background-check administrators can access detailed results and approve or deny requests at multiple points. Current documentation directs administrators to the dedicated Background Check Administration security role and describes sensitive profile fields including status, date, result, report document, and driver’s-license data. Keep that role limited to trusted personnel and separately review workflow, document, profile-field, and provider access. [Administer Background Checks](https://community.rockrms.com/documentation/core-concepts/security/background-checks/administer-background-checks)

Rock documents integrations with Checkr and Protect My Ministry. Provider configuration includes credentials or tokens and result webhooks; Protect My Ministry’s result webhook must use HTTPS, while Checkr requires its configured webhook to return results. Never place provider secrets in templates, logs, guide output, or client-visible code. [Configure Checkr](https://community.rockrms.com/documentation/core-concepts/security/background-checks/configure-checkr), [Configure Protect My Ministry](https://community.rockrms.com/documentation/core-concepts/security/background-checks/configure-protect-my-ministry)

Rock v17.8 corrected workflow-added document linkage so access is evaluated through Document Type security rather than falling back to File Type security. It also added a warning for publicly viewable Document Types. Review version applicability and both security surfaces when protected documents may have been uploaded through workflows. [Rock release notes](https://www.rockrms.com/releasenotes)

### Communications and reports

Communication safeguards span sender policy, access, templates, delivery configuration, and version behavior. Communication visibility is distinct from authorization to approve, cancel, edit, or send. Review the current block and entity permissions before enabling operational communication actions. [Rocking Security and Email Safeguards](https://shows.acast.com/rock-cast/episodes/episode-168-rocking-security-navigating-new-features-and-ema) (community-reviewed approved claim `claim:21e74a6bcebdab9c194a`)

Analytics-enabled or persisted data can reduce repeated reconstruction of operational metrics, but a snapshot is still a data-exposure surface. When an external BI report is embedded in Rock, honor the external platform’s licensing and secure the Rock page and block for the intended roles. The supplied verification did not evaluate any external license. [Community analytics example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz), [Embedded BI example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) (approved claims `claim:a5f0a54f29d226cec5fc` and `claim:ffba67d8847c47e68ea6`)

## Feature-Specific Authorization Workflows

### Sign-Ups and groups

Sign-Up authorization can come from Group Role permissions, project-level permissions, or Group Type security. Inspect all three sources when access is missing or unexpectedly broad. Creating a top-level Sign-Up group additionally requires Edit permission on both the Project Type group attribute and the Sign-Up Groups block. [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions) (approved claims `claim:fc1c8fb6ae5414717fe3` and `claim:32be14ce0431e82d2f1b`)

Rock v19.3 release notes state that the Sign-Up Finder was corrected to honor Group View security. A discrepancy on an earlier v19 build may be a version defect rather than a missing role grant. [Rock release notes](https://www.rockrms.com/releasenotes)

### Mobile check-in

Mobile check-in uses virtual kiosk device records, campus geofences, and a Mobile Check-in Launcher configured with the correct devices, check-in configuration, theme, and valid areas. Campuses needing distinct boundaries should use separate devices. These configuration relationships were structurally verified in the supplied evidence, but no specific launcher or geofence was certified. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) (approved claims `claim:0b6f8c45033ed0228a3b`, `claim:72dd1841cd10ed6d5a30`, and `claim:c78fd6f074218814ab14`)

Launcher text can be customized with Lava, but early screens may not have an identified person. Do not assume person context exists when rendering prompts or making authorization decisions. Location permission can also be absent, denied, limited to app use, or always allowed in the supplied implementation snapshot; test geofence behavior under the actual device permission state. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration), [location-permission implementation snapshot](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Mobile/LocationPermissionStatus.cs)

### CAPTCHA and exposed forms

Rock v19 documents self-hosted proof-of-work CAPTCHA with organization-wide Visible, Invisible, and Disabled modes plus block-level support. CAPTCHA is enabled by default on supported blocks but may be disabled in individual block settings. Support varies by block generation and Rock version, so confirm the actual block type and test every exposed form. [Configure CAPTCHA](https://community.rockrms.com/documentation/core-concepts/security/captcha/configure-captcha), [Use CAPTCHA](https://community.rockrms.com/documentation/core-concepts/security/captcha/use-captcha)

### Version-scoped operational controls

The following are approved v19 caveats, not universal behavior:

- Prevent Duplicate Registrants can stop a matched person from being registered twice, but its warning may disclose that someone is already registered to a person who knows matching identity details. Evaluate the event’s sensitivity before enabling it. [v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=357s)
- A person without merge permission can request notification after an authorized reviewer completes a merge, keeping request submission separate from merge authority. [v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=902s)
- Selected connection requests can support reassignment, status changes, completion, workflows, activities, SMS, and email, subject to permissions, templates, snippets, and phone eligibility. [v19 Connections overview](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=466s)
- Outreach Toolbox can contain contact-specific prayer, connection, touchpoint, and pulse information. Review block settings and who may see that contact data before ministry use. [Outreach Toolbox overview](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s)

## AI Agents, Tools, And Data Access

Rock’s presented agent model separates agents, skills, and tools, with configuration and security decisions at each layer. Chat versus MCP and Internal versus Public are separate choices. Expose only the tools appropriate to the current person and agent. Tool availability and Rock authorization must both permit an operation; organizations can, for example, make drafting available without exposing sending or destructive tools. These are approved pre-release or early-release design claims and must be checked against the installed version. [AI Summit](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s), [RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s)

The planned MCP flow uses OAuth so the external harness holds and renews access tokens rather than exposing a general Rock API key to the model. The pre-release design applies Rock permissions as the authenticated person. Administrators must still verify the released implementation, client authorization, scopes, revocation, and each tool’s actual permission behavior. [RockIQ Q&A on permissions](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s), [RockIQ Q&A on OAuth](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s)

Do not give an AI integration unrestricted database access or an arbitrary SQL-execution tool. Route operations through managed Rock code that enforces authorization and business rules. Reviewed static SQL inside a narrowly secured tool is distinct from allowing a model to generate and execute open-ended SQL. Before choosing SQL, consider cache objects or entity commands, return only necessary fields, and account for business logic and query cost. [AI Summit SQL warning](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s), [RockIQ production guidance](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=1490s)

Custom tool names and result shapes should be explicit and bounded. Lava tools should return structured `AgentToolResult` values, sanitize explicit parameters, use the dedicated filters for instructions, compact history, metadata, and Rock routes, and use built-in tool logs to inspect calls and results. Pass IdKeys rather than raw integer identifiers in prompt context, while retaining server-side authorization. [AI Summit tool design](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s), [AI Summit Lava tools](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s), [AI Summit prompt context](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s)

## Version And Authority Caveats

Most hydrated Rock documentation in this evidence pack was retrieved as current v19 documentation on September 3, 2026. The release-note snapshot also listed v20.0 as Alpha. Do not apply alpha or pre-release behavior to a production installation without confirming the installed build and released documentation. [Rock release notes](https://www.rockrms.com/releasenotes)

Several approved claims have an unprocessed version scope. Treat them as guidance to verify, not proof that every supported Rock version behaves identically.

High-impact version checks in the pack include:

- v17.5: corrected DataView REST permission evaluation.
- v17.8: corrected workflow-added Document linkage and Document Type security evaluation.
- v19.3: corrected Sign-Up Finder handling of Group View security.
- v19.4: corrected OIDC authorization behavior involving the `openid` scope.
- v19.5: corrected a Lava Application endpoint failure involving an inactive developer role.
- v19: introduced or documented the self-hosted proof-of-work CAPTCHA controls and the other version-scoped features described above.

Self-hosted operators own their patch cadence. Supported dot releases can contain security fixes, so patch releases should not be treated as optional without reviewing current supported branches, release notes, and local compatibility. Major-version validation and patch-version validation are separate activities. [Patch-cadence discussion](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s), [Rock release notes](https://www.rockrms.com/releasenotes)

Official documentation and approved official claims are the primary authority. RockU claims in this pack are operational training guidance with bounded structural verification. Community contributions are examples or troubleshooting hypotheses and require installation-specific validation. Public source excerpts at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` describe implementation at that snapshot, not a target installation’s configuration.

## Troubleshooting Decision Tree

### A person cannot access an item they should be able to use

1. Confirm the exact person, entity type, entity identifier, and requested action.
2. Use Inspect Security to locate the effective result and inherited source.
3. Read the direct and inherited Allow/Deny rules in order; the first matching rule wins.
4. Confirm current role membership separately because the Security Change Audit does not record role-membership changes.
5. Inspect adjacent secured entities, such as parent page, block, Group Type, project, application, or endpoint.
6. Retest as the person, not only as an administrator.
7. Check release notes before compensating for a known version defect. [Handle Permissions](https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions), [Security Change Audit](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/view-the-security-change-audit)

### A page or content item is missing or publicly exposed

1. Resolve the exact site and route.
2. Inspect the page hierarchy and inherited page security.
3. Inspect each block’s security, block type, zone, and configuration.
4. For content channels, inspect channel, item, list block, detail block, route, and Lava template.
5. Separate personalization rules from authorization.
6. Test anonymous, intended-role, and administrator sessions.
7. Inspect alternate routes, mobile surfaces, and direct endpoints before declaring the content closed or protected. [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy), [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view)

### Login fails after enabling 2FA or an external provider

1. Read the Login History status and detailed failure reason.
2. Confirm which Account Protection Profile applies.
3. Verify the email or SMS communication configuration required by 2FA.
4. Confirm the person has a usable Rock username and password when Rock 2FA requires it.
5. Inspect the Login block’s database-login and external-provider redirect settings.
6. Do not enable Rock 2FA for a flow that exposes only an incompatible built-in external provider.
7. For OIDC, verify client identity, scopes, redirect settings, and installed-version fixes. [Two-Factor Authentication](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/two-factor-authentication), [Use Login History](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/use-login-history)

### A REST request returns unauthorized or permission denied

1. Confirm that the session cookie or `Authorization-Token` is present and valid.
2. Identify the authenticated person or REST key rather than reasoning from the token string alone.
3. Confirm route, controller, method, entity, and intended action.
4. Inspect the identity’s direct and inherited grants.
5. Determine whether the failure is authentication, authorization, validation, routing, or a known version bug.
6. Check the v17.5 DataView fix if that endpoint family is involved.
7. Stop before broadening permissions unless the missing grant is demonstrated. [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api), [Rock release notes](https://www.rockrms.com/releasenotes)

### A Helix endpoint works for administrators but not the intended role

1. Confirm page and block access for the intended role.
2. Inspect the endpoint’s security mode.
3. Inspect direct endpoint authorization.
4. Where application-level security applies, inspect the parent Lava Application.
5. Inspect enabled commands, input validation, CSRF, and rate-limit settings.
6. Check whether the installed version predates the relevant v19.5 fix.
7. Retest as anonymous, intended role, and administrator; do not treat admin override as role proof. [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [Rock release notes](https://www.rockrms.com/releasenotes)

### A note is missing, visible to the wrong staff, or behaves unexpectedly downstream

1. Identify the exact Person Profile block or other entity surface.
2. Identify the Note Type and target entity.
3. Inspect note-type and surface permissions.
4. Review author and date metadata plus current lifecycle state.
5. Identify reports and workflows that consume that Note Type.
6. Test with the intended staff role and an unauthorized role.
7. Stop before reclassifying or moving notes if that would alter reporting or workflow meaning. [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1), [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types)

### A public form is receiving abuse or CAPTCHA is not appearing

1. Confirm the installed Rock version and exact block generation.
2. Verify the organization-wide CAPTCHA mode.
3. Inspect the block-level CAPTCHA setting.
4. Determine whether the configured mode is Visible, Invisible, or Disabled.
5. Test a real submission path; absence of a checkbox does not prove CAPTCHA is inactive.
6. Confirm the block is among the version’s supported CAPTCHA surfaces.
7. Continue to enforce authorization, validation, and rate limits where relevant. [Configure CAPTCHA](https://community.rockrms.com/documentation/core-concepts/security/captcha/configure-captcha), [Use CAPTCHA](https://community.rockrms.com/documentation/core-concepts/security/captcha/use-captcha)

### A top-level Sign-Up project cannot be created or is visible to the wrong people

1. Inspect Group Role, project-level, and Group Type authorization.
2. Confirm Edit permission on the Project Type group attribute.
3. Confirm Edit permission on the Sign-Up Groups block.
4. Inspect Group View security for finder visibility.
5. Compare the installed version with the v19.3 Sign-Up Finder fix.
6. Test creation, management, and public discovery as separate actions. [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions), [Rock release notes](https://www.rockrms.com/releasenotes)

## Agent Task Recipes

### Recipe: Explain an effective permission result

**Outcome:** A sourced explanation of why one person is allowed or denied one action.

1. Record the person, entity type, entity ID or GUID, and requested action.
2. Run the equivalent of an Inspect Security review.
3. Capture the matching direct or inherited rule and its position.
4. Identify the parent when the rule is inherited.
5. Check relevant role membership separately.
6. State the effective result, matching rule, inheritance source, and any unverified adjacent boundary. [Inspect Security](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/inspect-security)

**Do not assume:**

- A role name proves membership.
- A visible route proves block or entity access.
- An administrator result represents the user’s result.

**Stop when:**

- The exact entity or person cannot be identified.
- A write would be required to continue and no authorization to change security was given.

### Recipe: Publish a page or block with bounded access

**Outcome:** The intended audience can use the surface while unauthorized users cannot.

1. Identify the site, page hierarchy, route, zone, block type, and data source.
2. Inspect inherited page security before adding direct rules.
3. Add the minimum necessary direct rule only when inheritance does not express the requirement.
4. Inspect block security and any underlying entity or endpoint.
5. Review Lava commands, query/context inputs, personalization, and detail routes.
6. Test anonymously, as the intended role, and as an administrator.
7. Verify alternate and mobile routes before publishing. [Handle Permissions](https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions), [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)

**Inspect:**

- First-matching Allow/Deny order.
- Parent-page inheritance.
- Data exposed by list and detail views.
- Whether personalization is being mistaken for authorization.

### Recipe: Preflight a least-privilege REST integration

**Outcome:** A documented integration identity with only the access required for known routes and methods.

1. Inventory every route and HTTP method.
2. Classify each operation as read or write.
3. Identify the authenticated user session or REST key.
4. Map each operation to its entity and authorization action.
5. Grant only demonstrated permissions.
6. Store and transmit credentials outside templates, logs, and client-visible output.
7. Test against non-production or non-sensitive records where possible.
8. Read back intended writes and compare only integration-owned fields.
9. Document rotation, revocation, logging, and rollback. [The Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)

**Do not assume:**

- A successful call proves least privilege.
- An IdKey authorizes access.
- An API key should have administrator-equivalent rights.
- Community PATCH guidance applies identically to every API v2 endpoint.

### Recipe: Secure a Lava API or Helix endpoint

**Outcome:** A directly callable endpoint with explicit identity, authorization, validation, and bounded output.

1. Enumerate the endpoint URL, method, parent application, page, and block.
2. Define authenticated and anonymous behavior explicitly.
3. Enforce the caller’s required View or Edit permission.
4. Validate and sanitize every query and body value.
5. Use non-GET methods for mutations.
6. Enable only required Lava commands.
7. Review CSRF and rate-limit settings.
8. Return only approved fields.
9. Test direct calls without the front end.
10. Test unauthorized, intended-role, and administrator contexts.
11. Verify resulting data or mutations independently. [Helix Security](https://community.rockrms.com/developer/helix/overview/security), [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)

**Stop when:**

- Authorization depends only on hidden UI.
- Arbitrary SQL or unrestricted database access is required.
- Administrator success is the only available test evidence.

### Recipe: Audit Person Profile notes

**Outcome:** Sensitive notes are categorized, visible, and consumed only as intended.

1. Inventory the relevant Note Types and target entity contexts.
2. Map who may view, add, edit, or otherwise act on each type.
3. Inspect the Person Profile page and block surfaces.
4. Sample author, date, visibility, and lifecycle behavior without publishing private note text.
5. Identify workflows and reports that consume each type.
6. Test with authorized and unauthorized staff roles.
7. Record configuration gaps without moving or rewriting notes. [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types), [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1)

### Recipe: Validate an AI agent tool before production

**Outcome:** A bounded tool whose availability, authorization, input handling, and output have been demonstrated.

1. Identify agent, skill, tool, current-person context, and Chat or MCP exposure.
2. Confirm whether the feature is released in the installed Rock version.
3. Define explicit parameters and a bounded result shape.
4. Expose only the minimum operation; separate drafting from sending and omit destructive tools unless required.
5. Route data access through managed Rock code.
6. Enforce Rock permission checks for the authenticated person.
7. Sanitize inputs and avoid arbitrary model-generated SQL execution.
8. Test allowed and denied users.
9. Inspect built-in tool logs for calls, inputs, results, and failures.
10. Test OAuth scope and revocation for MCP clients.
11. Stop before production use if any permission behavior remains inferred. [AI Summit](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s), [RockIQ Q&A](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s)

### Recipe: Run a security-sensitive upgrade preflight

**Outcome:** A version-aware plan that distinguishes security fixes from feature changes.

1. Record the installed Rock version and hosting model.
2. Review current supported branches and release notes.
3. Identify security-relevant fixes between the installed and target versions.
4. Separate major-version validation from dot-release validation.
5. Inventory affected authentication, API, CMS, workflow, document, and Helix surfaces.
6. Rehearse the upgrade and rollback in the organization’s approved environment.
7. Retest unauthorized, intended-role, and administrator scenarios.
8. Verify protected documents, Sign-Up visibility, OIDC, APIs, and endpoint authorization where applicable.
9. Do not declare completion from package installation alone; verify rendered and callable behavior. [Rock release notes](https://www.rockrms.com/releasenotes), [Patch-cadence discussion](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s)

## Known Gaps And Live Verification

The guide cannot determine the following without a bounded review of the target installation:

- Installed Rock version, enabled plugins, block generations, or local customizations.
- Actual security-role membership and Elevated Security Levels.
- Direct and inherited rules on a particular page, block, group, Note Type, content item, workflow, application, endpoint, API controller, or report.
- Whether external authentication callback URLs, scopes, secrets, and provider-side approvals are current.
- Whether passwordless communications, SMS sender configuration, 2FA, browser checks, or cookie revocation behave correctly end to end.
- Whether a Lava webhook has an application-specific security layer.
- Whether a Helix endpoint’s security mode, parent application authorization, CSRF, rate limiting, and enabled commands are correctly configured.
- Whether CAPTCHA is active and effective on each exposed form.
- External BI licensing.
- Specific mobile check-in device, campus, geofence, area, theme, or location-permission behavior.
- AI/MCP availability and authorization behavior in the installed release.
- Current supported branches and security patches.

The evidence pack includes reviewed read-only conclusions from June 9, 2026 confirming that several relevant schema and authorization surfaces existed in one connected Rock instance. Those conclusions support the inspection workflows in this guide but do not prove any other installation’s configuration.

All reviewed community patterns remain examples requiring local verification. In particular:

- Do not adopt the community API v2 PATCH pattern without confirming endpoint semantics.
- Do not rely on parent Lava Application authorization behavior without testing the installed endpoint security mode.
- Do not treat full-page iframe limitations, seasonal-feature closeout steps, anonymous SMS verification, saved-account payment checks, or delayed-workflow revalidation as verified local behavior.
- Do not deploy the supplied communication-history, registration-dashboard, registration-transfer, or SMS-verification recipes without reviewing their permissions, data exposure, provider behavior, and end-to-end results.
- Do not retain plain verification codes or expose matched person identifiers based only on a community recipe; define retention and verification rules for the target installation.

The Group Security RockU record in the pack was approved only as a public-safe training distillation, and its hydrated page did not supply detailed instructional evidence. This guide therefore does not infer group-security mechanics beyond the approved Sign-Up and general authorization claims.

## Source Map

### Primary official security documentation

- [Security](https://community.rockrms.com/documentation/core-concepts/security)
- [Intro to Security](https://community.rockrms.com/documentation/core-concepts/security/overview/intro-to-security)
- [Intro to Security Roles](https://community.rockrms.com/documentation/core-concepts/security/security-roles/intro-to-security-roles)
- [Administering Security Roles](https://community.rockrms.com/documentation/core-concepts/security/security-roles/administering-security-roles)
- [Handle Permissions](https://community.rockrms.com/documentation/core-concepts/security/security-roles/handle-permissions)
- [Inspect Security](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/inspect-security)
- [Configure Security Settings](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/configure-security-settings)
- [Security Change Audit](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/view-the-security-change-audit)
- [Cloning Security Role Groups](https://community.rockrms.com/documentation/core-concepts/security/advanced-security/cloning-security-role-groups)

### Authentication and accounts

- [Intro to Login and Authentication](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/intro-to-login-and-authentication)
- [Passwordless Login](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/use-passwordless-login)
- [Two-Factor Authentication](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/two-factor-authentication)
- [Login History](https://community.rockrms.com/documentation/core-concepts/security/login-and-authentication/use-login-history)
- [Unrecognized Browser](https://community.rockrms.com/documentation/core-concepts/security/user-accounts/register-for-an-account-on-an-unrecognized-br)
- [External Authentication](https://community.rockrms.com/documentation/core-concepts/security/external-authentication-services/intro-to-external-authentication)
- [OpenID Connect](https://community.rockrms.com/documentation/core-concepts/security/rock-authentication/intro-to-openid-connect)
- [CAPTCHA](https://community.rockrms.com/documentation/core-concepts/security/captcha/intro-to-captcha)

### APIs, Lava, Helix, and source evidence

- [Rock REST API](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api)
- [Rock Security](https://community.rockrms.com/developer/303---blast-off/rock-security)
- [Lava Commands](https://community.rockrms.com/lava/commands)
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
- [Helix Security](https://community.rockrms.com/developer/helix/overview/security)
- [Authorization implementation snapshot](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Security/Authorization.cs)
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Operational RockU sources

- [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy)
- [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block)
- [Content Channel View](https://community.rockrms.com/rocku/content-channels/content-channel-view)
- [Personalization](https://community.rockrms.com/rocku/cms/personalization)
- [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile)
- [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1)
- [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types)
- [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

### Sensitive workflows and feature documentation

- [Administer Background Checks](https://community.rockrms.com/documentation/core-concepts/security/background-checks/administer-background-checks)
- [Configure Checkr](https://community.rockrms.com/documentation/core-concepts/security/background-checks/configure-checkr)
- [Configure Protect My Ministry](https://community.rockrms.com/documentation/core-concepts/security/background-checks/configure-protect-my-ministry)
- [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions)

### Reviewed community examples

- [Communication History Active Search](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/communication-history-active-search)
- [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)
- [Registration-to-Connection Request](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)
- [Workflow-Backed SMS Verification](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)

These community sources illustrate patterns only. Each is marked as requiring live verification before use.
