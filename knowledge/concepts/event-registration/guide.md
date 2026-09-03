---
id: authored-event-registration
title: Event Registration
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "3c44b5acb7f2cad5c3d70b2f389e70b46eef26a88a66c8b265462e3f99657b70"
---

# Event Registration

## Agent Summary

Rock Event Registration coordinates reusable registration configuration, event-specific registration instances, registrars and registrants, forms, costs, payments, communications, capacity, wait lists, groups, calendar occurrences, and follow-up processes.

Use this operating model:

1. Start with the registration template. It holds most reusable settings, including fields, costs or cost behavior, fees, payment options, eligibility, communications, workflows, signatures, and group-related configuration.
2. Create a registration instance for the specific offering. The instance supplies event-specific details such as dates, contact information, capacity, and—when configured at the instance level—cost and finance settings.
3. Link the instance to the correct event occurrence, calendar, campus, and group when those relationships are required.
4. Test the public journey with representative people before publishing it.
5. During operations, keep registrations, registrants, payments, fees, discounts, wait-list status, and group placement distinct.
6. Require live verification for installed configuration, provider behavior, custom integrations, reports, and version-dependent features.

Rock explicitly distinguishes a registration record from the people registered through it: one registration can contain multiple registrants. Account, fee, and payment information is managed separately, so reports and automations must state their intended grain. [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

## Scope And Boundaries

This guide covers:

- Registration templates and instances
- Public and staff-entered registrations
- Forms, identity matching, eligibility, workflows, and communications
- Costs, fees, discounts, partial payments, payment plans, payment matching, and refunds
- Capacity and wait lists
- Calendars, event items, occurrences, linkages, campuses, groups, and promotion
- Group placement and check-in handoff
- Operational reporting and reconciliation
- Family preregistration as a reviewed community pattern

This guide does not replace the owning concepts for finance, groups, check-in, workflows, communications, people and families, or general calendar administration. For example, it explains when a registration payment or group linkage matters but does not define an organization’s accounting controls, check-in configuration, identity policy, or workflow security model.

Do not treat the existence of a registration, group, workflow, or payment record as proof that the complete ministry process works. The approved preregistration evidence confirms that these surfaces can be traced together, but it does not prove that a particular implementation is correctly configured. [Community-reviewed preregistration guidance at 02:10](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

## Mental Model

Rock’s documented v19 structure can be read as several related layers:

- **Template:** Reusable configuration shared by registration instances.
- **Instance:** One specific registration offering created from a template.
- **Registration:** The transaction-like container created by a registrar; it can include multiple registrants.
- **Registrant:** One person being registered.
- **Finance:** Cost, fees, discounts, payments, balance, account, gateway, and any payment plan.
- **Calendar:** The calendar contains event items; event occurrences supply the scheduled, campus, contact, and location context.
- **Linkage:** Connects an occurrence to a registration instance and optionally a group, campus context, public name, and URL slug.
- **Group placement:** Moves registered people into operational groups used for rosters, activities, teams, or check-in.
- **Workflow and communications:** Turn captured registration data into confirmation, reminders, payment follow-up, or ministry action.

Templates carry most shared configuration, while instances supply the details that differ between offerings. A recurring class can therefore reuse one template across multiple dated instances, while a substantially different annual event may use a dedicated template and instance. [Official v19 documentation: Intro to Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations)

The registrar and registrant are not necessarily the same person. A parent, household member, or other registrar may submit one registration containing several registrants. An agent must therefore avoid using “registration,” “registrar,” “registrant,” and “person” interchangeably. [Official v19 documentation: Intro to Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations)

## Registration Instances

### Build reusable behavior in the template

Most registration configuration belongs in the template. The supplied v19 documentation supports template settings for activation and categorization, person and group behavior, custom forms, conditional fields, registration attributes, eligibility, confirmation and reminder communications, costs, gateways, partial payments, payment plans, workflows, electronic signatures, and customized terms. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

Deactivating an obsolete template is materially different from deleting it. The documentation warns that deleting a template also deletes the registrations that use it. Treat deletion as a destructive operation requiring a confirmed retention decision; deactivation is the bounded choice when the goal is simply to prevent future use. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

A template category can help organize and secure templates. Template creation and template administration are also permission-sensitive; access to an instance does not imply permission to create or administer its template. [Official v19 documentation: Secure Events and Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/advanced-events/secure-events-and-calendars)

### Put occurrence-specific settings on the instance

Create an instance for a particular offering and confirm its event-specific values. The Event Wizard documentation identifies fields such as registration start and end dates, contact, maximum attendees, payment deadline, account, and—when the template does not own them—cost, minimum initial payment, and default payment amount. [Official v19 documentation: Event Wizard](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/event-wizard)

The Event Wizard is optional. It provides a constrained staff-facing process that can use allowed templates and optionally create or select a group, event item, occurrence, campus, schedule, and finance settings. Its block configuration controls which templates are available, whether a group is required, whether the created instance starts active, whether calendar events are enabled, and whether staff can create a new calendar event. [Official v19 documentation: Event Wizard](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/event-wizard)

Use the wizard when its configured choices match the operating model. Do not assume that completing the wizard proves that the resulting group, calendar linkage, public route, payment gateway, or communications have been tested.

### Manage at the correct grain

The instance detail surface separates operational concerns into registrations, registrants, payments, fees, discounts, linkages, and wait-list views. The Registrations tab shows registration containers, which may each contain multiple people; the Registrants tab lists individual registrants. [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

A registration can be moved only to another instance using the same template, because different templates can have incompatible fields, costs, fees, and discounts. Staff can also manually add a registration or add another registrant to an existing registration from the documented management surface. [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

## Forms, Identity, Eligibility, And Communications

### Design the form around the record being updated

Rock supports custom entry forms, person and registration fields, registration attributes, conditional fields, confirmation and reminder emails, workflows, and electronic signatures through template configuration. Decide whether each value belongs to the person, registration, registrant, group member, or another related entity before building the form. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

Requiring login can reduce the chance of creating a duplicate registrar record, but it adds the cost of requiring the guest to authenticate or create a login. This is not the same control as preventing a matched person from being registered twice for one instance. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

When conditional or custom update logic is added outside the standard registration flow, treat identity resolution and preservation of omitted values as local implementation concerns. A reviewed community pattern recommends resolving the intended person on the server, reading back saved values, and preserving existing attribute values when a conditional path omits them. This is not universal core behavior and requires live verification against the endpoint, workflow, and installed schema. [Reviewed community pattern: person resolution and conditional attribute preservation](https://community.rockrms.com/lava/commands/entity-commands)

### Test combined eligibility

For v19 registrant eligibility, the approved official claim states that a registrant must satisfy every enabled criterion. Test combined age, gender, grade, and Data View rules using representative people before opening registration; testing each criterion independently is not enough. [Official v19 feature guidance at 07:25](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=445s)

Do not infer that a person is eligible from one visible field. Grade, age, gender, Data View membership, stored person data, effective dates, and the exact enabled criteria all need inspection when a representative person is rejected.

### Evaluate duplicate-prevention disclosure

The v19-era Prevent Duplicate Registrants capability blocks a matched person from being registered twice for the same instance. The supplied v19.1 release record says validation occurs during the registrant step and again before submission, including every person in a multi-registrant entry. The v19 template documentation further notes that matching is based on Person ID and does not detect or merge separate duplicate person records. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates) [Official release notes](https://www.rockrms.com/releasenotes)

The approved release caveat identifies a privacy tradeoff: someone who knows enough matching identity information may learn from the warning that the person is already registered. Evaluate that disclosure before enabling the setting for sensitive events. [Official feature guidance at 05:57](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=357s)

### Verify communications as part of the lifecycle

Template configuration can include confirmation, event reminder, and payment reminder emails. The supplied documentation notes that event reminders include people on the wait list and can depend on the instance’s additional reminder details for event timing. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

Do not stop at confirming that a communication template is selected. Test its audience, merge fields, links, event details, payment state, wait-list wording, and delivery behavior using non-sensitive test records.

## Payments

### Configure the finance path deliberately

Rock documents free and paid registrations, partial payments, additional fees, percentage or fixed discounts, payment plans, and payment reminders. The template can select the financial gateway and determine whether costs are shared by all instances or set on each instance. A financial account is required when the Event Wizard creates a paid instance. [Official v19 documentation: Intro to Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations) [Official v19 documentation: Event Wizard](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/event-wizard)

Staff can manually enter a payment from the registration’s details and Payments area. At the instance level, the Payments tab lists payments and links to the corresponding financial transaction; the documented transaction detail path is where a refund can be processed by an authorized user. [Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances) [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

Permissions differ: the supplied v19 security documentation says staff and staff-like roles can add registration payments, while the default refund path requires Finance Administration. Verify local block and entity security because an installation can be more restrictive. [Official v19 documentation: Secure Events and Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/advanced-events/secure-events-and-calendars)

### Partial payments and payment plans are different

A positive minimum initial payment enables partial-payment behavior, and a default payment amount can prefill the amount due today when the minimum is greater than zero. The registrar may lower the prefilled amount to the configured minimum. [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

Payment plans require template enablement and a compatible payment gateway. The documented payment schedule is controlled by the external gateway rather than Rock. Later changes to the registration balance—for example, applying a discount—do not automatically update the gateway-controlled payment plan. Administrators must reconcile the remaining registration balance with the external schedule; deleting a plan cancels its remaining payments, and continuing afterward requires a new plan. [Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)

The supplied v20 release snapshot, labeled alpha, adds a template setting requiring either payment in full or a payment plan covering the remaining balance before registration can complete. Do not describe that as established v19 behavior or enable it without confirming the installed release. [Official release notes](https://www.rockrms.com/releasenotes)

### Apply discounts with balance consequences in mind

The documented finance surface supports discount codes, quantity discounts, early-bird and automatic discounts, limits on usage, and discount reporting. The Discounts tab reports which discounts were used, by whom, usage counts, and total discount cost. [Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances) [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

A person with an unpaid balance can apply a post-registration discount through the documented registration block. The supplied v19 documentation says this is unavailable after the registration is paid in full or after another discount code has already been used. A discount larger than the remaining amount can produce a negative registration balance, which requires a manual refund to return the balance to zero. [Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)

### Match externally entered transactions

Event Registration Matching operates on one registration instance at a time and matches transactions from a selected open batch to registrations. The batch must be Open, not Pending. The tool is located under `Finance > Event Registration Matching` in the supplied v19 documentation. [Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)

Do not treat the presence of a transaction in a batch as proof that it is attached to the intended registration. Verify the batch state, template, instance, registration, amount, and post-match balance.

## Wait Lists And Capacity

Wait lists are enabled on the template, while maximum registrant capacity is configured on the instance. When capacity is exhausted, the public flow can offer a wait-list position. If one place remains in a multi-person entry, Rock can fully register one person and place the next person on the wait list. [Official v19 documentation: Manage Wait Lists](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists)

Wait-listed people are not charged during their initial wait-list entry. They are not added to the linked group at that point, so Rock cannot store Group Member Attributes for them. Those fields are hidden during initial wait-list entry, while first and last name must be shown to avoid anonymous records. [Official v19 documentation: Manage Wait Lists](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists)

Moving someone from the wait list makes the person a full registrant and adds them to configured groups. The documented administration flow can send an email asking the person to finish registration. That completion step matters because it collects any payment due and fields skipped during wait-list entry, including applicable Group Member Attributes. Without completion, the registration can remain operationally incomplete. [Official v19 documentation: Manage Wait Lists](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists)

Keep confirmed and wait-listed populations explicit in exports, dashboards, rosters, communications, and check-in tools. The supplied implementation excerpt for the registration list models wait-list status per registrant, reinforcing that status belongs at the person-within-registration grain. [Core source at immutable commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs)

## Event Calendar

### Separate calendars, event items, and occurrences

Rock’s documented calendar model has three components: calendars, event items, and event occurrences. The event item represents the reusable event concept, while an occurrence carries the scheduled manifestation. This supports one event type with multiple upcoming occurrences. An event can appear on more than one calendar. [Official v19 documentation: Intro to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/intro-to-calendars)

An occurrence can supply campus, contact information, location description, schedule, occurrence notes, attributes, and linkages. A single occurrence may use a one-time or recurring schedule. [Official v19 documentation: Add Event Occurrences](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/add-event-occurrences)

The supplied pre-alpha core source models an occurrence with its event item, next start time, campus, contact, location, schedule description, and registration/group linkages. Treat this as implementation evidence for the upcoming agent surface, not proof that an installed Rock instance exposes or authorizes the same tool. [Core source at immutable commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Classes/Skills/EventCalendarSkill/EventItemOccurrenceResult.cs)

### Link the occurrence, registration, and group

The documented sequence is to create the event group, create the calendar event and occurrence, and then add a linkage. The linkage can create a new registration instance from an existing template, connect an existing instance, or create a public slug without requiring registration. Afterward, the occurrence can optionally be connected to content channel items for promotion. [Official v19 documentation: Link Events to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars)

When a calendar occurrence is linked to a registration, the public event detail can display a Register button. A registration may also be promoted using its direct registration URL. For edits, a registration URL can include `StartAtBeginning=true` when the person should review every step instead of opening at the summary. [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

The v19 documentation states that the URL slug is required for registrants to be placed automatically into the correct linked group. Include the slug in launch testing rather than assuming that an instance-to-group relationship alone proves placement. [Official v19 documentation: Link Events to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars)

A linkage can also establish campus association. If no campus linkage exists, the registration flow can use a `CampusId` URL parameter; if a campus linkage does exist, the linkage campus takes precedence over the URL parameter. [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

Content channel items are attached to the occurrence. The content channels available for that operation are configured at the calendar level. An administrator can create a new content item or link an existing one. [Official v19 documentation: Link Content Channel Items](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-content-channel-items)

## Groups, Placement, And Check-In Handoff

A registration can place registrants into a linked group, although group placement is not required for every registration. Groups are commonly the handoff surface for rosters and check-in. Multiple registrations can feed one group when that matches the event design. [Official v19 documentation: Intro to Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations)

Post-registration placement is configured on the template. Each placement specifies a destination Group Type and can allow either one or multiple group assignments per registrant. Shared destination groups can be available across instances using the template, while instance-specific groups can be added during operations. [Official v19 documentation: Group Placement](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/group-placement)

The immutable core excerpts show that the current registrant-list implementation represents each template placement with its identifier, name, icon, and multiple-placement setting, and reports each registrant’s placement group count and names. This confirms implementation structure, not the placement configuration of any installation. [Placement configuration source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementConfigBag.cs) [Registrant placement source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementBag.cs)

A reviewed community pattern for check-in dashboards recommends combining the registration roster with allowed manually placed group members and deriving check-in state from relevant attendance records. It also recommends treating “registered but not placed,” “group-only,” and “checked in” as separate states. This is a custom read-only reporting pattern, not core registration behavior, and it requires live validation of group roles, attendance scope, permissions, and event-specific fields. [Reviewed community source context](https://community.rockrms.com/developer/helix/lava-applications/content-block)

## Family Preregistration And Follow-Up

Family preregistration is valuable when it reduces first-visit friction and improves the quality of person, family, and child information before check-in. The public page should explain that value and should be designed to avoid duplicate or partial records that staff must clean manually. These are community-reviewed operating patterns, not a universal configuration supplied by Rock. [Community-reviewed guidance at 01:16](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) [Community-reviewed guidance at 03:50](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

Connect new-family preregistration to a clear workflow or connection process so captured information produces an assigned ministry action. A public form that creates records but does not trigger an owned follow-up process is incomplete from an operational perspective. [Community-reviewed guidance at 00:37](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

Before broad launch, test the complete path from the public form through family record creation, check-in eligibility, and staff follow-up. The supplied read-only review verified that the relevant registration, form-field, person, group, workflow, connection, and check-in surfaces existed in one reviewed environment; it did not certify any particular preregistration configuration. [Community-reviewed guidance at 02:10](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

A reviewed community recipe demonstrates transferring registrant context into a native Connection Request while preserving the source registration reference and copying only reviewed attributes. Treat that as a custom implementation option requiring local workflow, connection type, campus, attribute, permission, and end-to-end verification. [Reviewed community recipe at immutable commit](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)

## Reporting And Reconciliation

Name both the grain and population of every metric:

- Count registrant records when the metric means people registered.
- Count distinct registration records when the metric means registrations or registrar submissions.
- Keep confirmed and wait-listed people separate.
- Do not assume payment rows, fee selections, discounts, and registration balances share the same grain.
- Reconcile any custom segment to the population it claims to partition.

The registration-versus-registrant distinction is official documented behavior. More detailed reconciliation rules below are reviewed community reporting patterns that need validation against the installed data model and custom definitions. [Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

A reviewed community dashboard pattern recommends testing at least a multi-person registration, a wait-listed person, and a recent registrant; defining population predicates once; and checking that mutually exclusive segments sum to the confirmed population. For historical pace, it aligns events by days remaining until registration close rather than calendar date. [Reviewed community dashboard at immutable commit](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

Staff, serving, and department segments are not universal Rock meanings. A reviewed community pattern recommends documenting the local source groups, using active non-archived memberships, declaring precedence for mutually exclusive segments, and disclosing when one person can count in multiple departments. Disable such a module if the organization cannot define and validate its truth sources. [Reviewed community dashboard at immutable commit](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

The community Registration Instance Totals Report is an example rather than official behavior. Its own page warns that community recipes are not reviewed or endorsed by the core team. Audit its Lava, permissions, data grain, performance, and arithmetic before adoption. [Community recipe: Registration Instance Totals Report](https://community.rockrms.com/recipes/348)

## Permissions And Operational Control

In the documented default roles:

- Staff Workers and Staff Like Workers can create registration instances.
- Event Registration Administration can create registration templates.
- A person can edit a specific template through Administrate permission on that template.
- Edit permission on the template-management block can allow editing any template exposed through that block.
- Staff and staff-like roles can add payments.
- Finance Administration is required by default to process refunds.

These are documented defaults, not proof of local authorization. Inspect the installed role memberships, template security, block security, page security, account access, and financial permissions before allowing an action. [Official v19 documentation: Secure Events and Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/advanced-events/secure-events-and-calendars)

For custom public forms or endpoints, do not trust browser-only identity or verification state. A reviewed community SMS-verification pattern recommends exact server-side matching, a persisted expiring challenge with bounded attempts, withholding the matched person alias from the browser, and server-side consumption immediately before the intended action. This is a security-sensitive custom pattern and requires local threat modeling and live verification. [Reviewed community recipe at immutable commit](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)

## Version And Authority Caveats

Most official documentation supplied for this guide is scoped to Rock v19.0. Confirm the installed Rock version and the version selector on the documentation before applying exact settings or navigation.

Specific supplied release evidence includes:

- The duplicate-registrant capability is described in the approved v19 guidance, while the supplied release record identifies its addition in v19.1. Confirm the exact installed minor release.
- Rock v18.3 fixed internal registration blocks that could show a signature document by matching on the person instead of the registrant relationship, and included a migration for qualifying missing relationships.
- Rock v19.3 fixed several registration issues, including payment completion after moving someone off a wait list or exceeding capacity, staff linkage editing, and saved-account display for certain anonymous registrars.
- The supplied release snapshot labels v20.0 as alpha. Its new payment-completion requirement and event-linkage changes are upcoming behavior, not a safe assumption for v19 installations.

[Official release notes](https://www.rockrms.com/releasenotes)

The supplied RockU pages provide approved training context, but several hydrated pages returned navigation rather than substantive lesson content. Their titles must not be promoted into unsupported instructions. The legacy group-placement training is explicitly labeled legacy; use the current v19 Group Placement documentation for operational steps. [Official v19 documentation: Group Placement](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/group-placement)

Community contributions and recipes in this guide are examples. Each requires live verification before implementation. Core source excerpts are tied to immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` and describe implementation at that commit, not an organization’s installed configuration.

## Troubleshooting Decision Tree

### The public event has no Register button

1. Confirm that the intended calendar event occurrence exists and is the occurrence being displayed.
2. Inspect its linkage and verify that it points to the intended registration instance.
3. Confirm that the registration instance is active and within its intended public registration window.
4. Verify the page route or direct registration URL being used.
5. If group placement depends on the linkage, confirm that the URL slug is present.
6. If the problem began after an upgrade, compare the installed release with the supplied v19.3 linkage-editing fix and v20 pre-alpha friendly-route fix.
7. Stop when the public event detail opens the intended registration and a representative test can reach the correct entry form.

[Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations) [Official v19 documentation: Link Events to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars)

### A representative person is unexpectedly ineligible

1. Record the exact instance, template, person, and rejection point.
2. Inspect every enabled eligibility criterion: age, gender, grade, and Data View.
3. Verify the person values used by those criteria.
4. Evaluate the criteria together; v19 requires the person to satisfy all enabled criteria.
5. Retest with one person expected to pass and one expected to fail each combined rule.
6. Stop when the observed results match a written eligibility matrix.

[Official v19 feature guidance at 07:25](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=445s)

### A duplicate-registration warning exposes sensitive participation

1. Confirm that Prevent Duplicate Registrants is enabled on the template.
2. Confirm the installed minor version and actual warning behavior.
3. Identify what identity information an unauthenticated or unrelated person must know to trigger the match.
4. Classify whether merely revealing prior registration is sensitive for this event.
5. If the disclosure is unacceptable, pause launch and choose a reviewed identity or staff-mediated process.
6. Do not assume the setting resolves duplicate person records; it follows matched Person IDs.

[Official feature guidance at 05:57](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=357s) [Official v19 documentation: Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)

### A person moved from the wait list is missing payment or form data

1. Confirm the registrant is now marked as a full registrant.
2. Confirm that configured group placement occurred.
3. Verify whether the move email was sent.
4. Open its completion link as a test recipient and confirm it requests payment and fields omitted during wait-list entry.
5. Check whether the person completed that follow-up flow.
6. If payment completion fails, compare the installed version with the supplied v19.3 fix.
7. Stop when status, required data, payment, and group placement all reconcile.

[Official v19 documentation: Manage Wait Lists](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists) [Official release notes](https://www.rockrms.com/releasenotes)

### A registration balance no longer matches its payment plan

1. Inspect registration cost, fees, discounts, payments, and current balance.
2. Identify any change made after the plan started.
3. Inspect the schedule at the external gateway.
4. Do not assume Rock changed that gateway schedule when the balance changed.
5. Decide whether the gateway schedule must be adjusted or the plan canceled and recreated.
6. Verify the resulting registration balance and future gateway payments independently.
7. Stop when both systems agree with the approved collection plan.

[Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)

### A batch transaction is not attached to the registration

1. Confirm that the batch is Open rather than Pending.
2. Confirm the intended registration template and instance.
3. Open Event Registration Matching and select that single instance.
4. Find the intended registration at registration grain, not merely a registrant with a matching name.
5. Match the transaction and verify the resulting payment and balance from the registration details.
6. Stop when the financial transaction and registration both show the intended relationship.

[Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)

### Registrants are not entering the expected group

1. Confirm that the registration instance is linked to the intended group.
2. Confirm that the registration is being entered through the intended event linkage and URL slug.
3. Separate full registrants from wait-listed people; initial wait-list entries are not added to the group.
4. Inspect the registrant’s group membership and, if used, placement state.
5. For post-registration placement, confirm the template placement, Group Type, destination group, and single-versus-multiple placement rule.
6. If a custom REST loader created the membership, read the created member back and verify the registrant points to the intended active member. This last step is a reviewed community integration pattern requiring local API verification.
7. Stop when every expected full registrant has the intended active membership and wait-list exceptions are documented.

[Official v19 documentation: Link Events to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars) [Official v19 documentation: Group Placement](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/group-placement) [Community integration source context](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs)

### Dashboard totals disagree

1. Label each metric as registration, registrant, payment, fee, discount, group membership, or another explicit grain.
2. Define confirmed and wait-list predicates once.
3. Test one multi-person registration, one wait-list registrant, and one recent registrant.
4. Reconcile mutually exclusive segments to confirmed registrants.
5. Do not require overlapping department categories to total unique people.
6. Compare historical pace at the same days-remaining stage if events have different calendars.
7. Stop when every discrepancy is explained by grain, population, overlap, timing, or a verified defect.

[Official v19 documentation: Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations) [Reviewed community dashboard at immutable commit](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

### A signature document is missing or belongs to the wrong registration

1. Confirm that the template requires a signature document.
2. Inspect the affected registrant rather than matching only by person.
3. Confirm the installed Rock version.
4. If the installation predates or recently crossed v18.3, review the supplied signature-document fix and migration applicability.
5. Retest the internal registration list, registration details, and registrant details surfaces.
6. Stop when the displayed document follows the intended registrant relationship.

[Official release notes](https://www.rockrms.com/releasenotes)

## Agent Task Recipes

### Recipe: Create a reusable registration and one event instance

**Outcome:** A configured but not yet broadly launched instance with explicit ownership of shared and event-specific settings.

1. Define the registrant population, registrar model, required fields, cost model, capacity, group destination, communications, and follow-up owner.
2. Reuse an appropriate template or create one with authorized template administration.
3. Put reusable form, eligibility, finance, communication, workflow, signature, and placement settings on the template.
4. Create the instance and set its registration dates, contact, capacity, payment deadline, and any instance-owned finance settings.
5. Create or select the operational group if the event requires a roster or check-in.
6. Create or select the event item and occurrence.
7. Add the registration, group, campus, public name, and URL slug linkage as required.
8. Leave the instance inactive when the workflow requires review before publication.
9. Test representative free or paid, single- or multi-person, eligible and ineligible paths.
10. Activate only after public routing, communications, payments, placement, and permissions pass.

**Inspect:**

- Installed Rock version
- Template and block security
- Registration window and capacity
- Financial account and gateway
- Event occurrence and linkage
- Group and role
- Confirmation and reminder content

**Do not assume:**

- Wizard completion equals launch readiness
- A calendar event automatically has a registration
- An instance automatically places people into a group
- A selected gateway supports payment plans

[Official v19 documentation: Event Wizard](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/event-wizard) [Official v19 documentation: Link Events to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars)

### Recipe: Validate a paid registration before launch

**Outcome:** Evidence that representative costs and payment paths produce the intended registration and financial state.

1. Confirm whether cost is owned by the template or instance.
2. Verify the financial account and gateway.
3. Test base cost, every required or optional fee used by the event, and representative discounts.
4. If partial payments are enabled, test the minimum initial payment and default amount.
5. If payment plans are enabled, verify provider compatibility and inspect the plan at the gateway.
6. Confirm payment, total cost, balance, fees, and discounts on the registration.
7. Test confirmation and payment-reminder communications.
8. Test an authorized manual payment and refund in a safe environment or approved reversible scenario.
9. Document how post-registration balance changes will be reconciled with gateway schedules.
10. Stop before launch if Rock and the gateway disagree.

[Official v19 documentation: Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)

### Recipe: Promote a wait-listed person to full registration

**Outcome:** The person becomes a complete, paid-as-required registrant with the intended group membership.

1. Confirm available capacity and identify the exact wait-listed registrant.
2. Move that registrant from the Wait List tab.
3. Send the completion email unless a reviewed alternative follow-up is in place.
4. Confirm the person opens the correct registration.
5. Collect any payment and questions omitted during wait-list entry.
6. Verify the full-registration status.
7. Verify configured group membership and any required Group Member Attributes.
8. Reconcile capacity and the remaining wait-list order.
9. Stop when the registrant is complete across status, data, finance, and group placement.

[Official v19 documentation: Manage Wait Lists](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists)

### Recipe: Audit an event-registration dashboard

**Outcome:** Every published metric has an explicit grain, population, and reconciliation test.

1. Inventory all metrics and label their grain.
2. Define confirmed, wait-listed, canceled, and other local populations.
3. Trace a multi-person registration through registration-level and registrant-level metrics.
4. Trace a wait-listed person through every chart.
5. Reconcile fee, payment, discount, and balance metrics separately.
6. Document local sources and precedence for staff, serving, or department segments.
7. Mark overlapping dimensions as non-additive.
8. If comparing events, align them by the chosen lifecycle stage.
9. Restrict participant drilldowns to the intended staff audience.
10. Stop publication if a metric cannot be reconciled or its local truth source cannot be validated.

[Reviewed community dashboard at immutable commit](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)

### Recipe: Launch family preregistration with follow-up

**Outcome:** A family can preregister without unnecessary friction, records are usable at check-in, and staff receive an owned follow-up action.

1. State the benefit to the family on the public page.
2. Define how adults, children, families, aliases, and existing records will be resolved.
3. Minimize duplicate and partial record creation.
4. Define the workflow or connection process that receives the submission.
5. Assign an owner and expected follow-up state.
6. Test a new family, an existing family, a partial submission, and likely duplicate inputs.
7. Confirm family records and child data are usable by the intended check-in configuration.
8. Confirm the workflow or connection request appears with the intended person, campus, and reviewed attributes.
9. Confirm staff can complete the follow-up without relying on private troubleshooting data.
10. Stop broad launch if record quality, check-in eligibility, or follow-up ownership is unresolved.

[Community-reviewed preregistration guidance](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

## Known Gaps And Live Verification

The evidence pack does not establish the following for any target installation:

- Installed Rock version, applied migrations, or applicability of v18.3, v19.1, v19.3, or v20 changes
- Which registration blocks are Obsidian, legacy, customized, or replaced
- Actual template, instance, page, block, account, calendar, group, workflow, or refund permissions
- Active gateways and their support for saved accounts, redirects, ACH, cards, partial payments, or payment plans
- Exact form fields, conditional logic, attributes, signatures, and identity-matching behavior
- Whether public routes, URL slugs, campus precedence, and Register buttons work end to end
- Whether registration groups are configured for check-in
- Whether reminders, confirmations, wait-list promotions, or payment emails are delivered
- Whether a preregistration workflow creates correct family records and owned follow-up actions
- Whether custom dashboards, REST loaders, Helix endpoints, SMS verification, or Connection Request workflows are installed or safe
- Whether custom reporting predicates match local confirmed, wait-list, staff, serving, campus, source, and department definitions

A bounded live review should use read-only inspection first. It should identify the version and relevant configuration, reproduce the issue with approved test records, and return only a public-safe conclusion. Do not publish raw person data, financial details, organization-specific identifiers, secrets, or SQL output.

The supplied live-verified preregistration claims confirm only that relevant feature surfaces existed in one reviewed environment. They do not certify a target installation or make that organization’s configuration universal.

## Source Map

### Approved official claims

- [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations): registration versus registrant grain
- [New Features & Enhancements Coming to v19 at 07:25](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=445s): combined eligibility criteria
- [New Features & Enhancements Coming to v19 at 05:57](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=357s): duplicate-prevention disclosure caveat

### Official documentation

- [Intro to Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/intro-to-event-registrations)
- [Registration Templates](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-templates)
- [Event Wizard](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/event-wizard)
- [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)
- [Registration Finances](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances)
- [Manage Wait Lists](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists)
- [Group Placement](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/group-placement)
- [Intro to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/intro-to-calendars)
- [Add Event Occurrences](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/add-event-occurrences)
- [Link Events to Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-events-to-calendars)
- [Link Content Channel Items](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/link-content-channel-items)
- [Secure Events and Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/advanced-events/secure-events-and-calendars)
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Approved community guidance and examples

- [Family preregistration community guidance](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)
- [Registration-to-Connection Request recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)
- [Event Registration Analytics Dashboard](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)
- [Workflow-Backed SMS Verification](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)
- [Registration Instance Totals Report](https://community.rockrms.com/recipes/348)

### Immutable implementation evidence

- [Occurrence result model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Classes/Skills/EventCalendarSkill/EventItemOccurrenceResult.cs)
- [Registrant-list block](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Event/RegistrationInstanceRegistrantList.cs)
- [Placement configuration model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementConfigBag.cs)
- [Registrant placement model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrantList/RegistrantPlacementBag.cs)
- [Wait-list display model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs)