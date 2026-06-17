---
id: authored-event-registration
title: Event Registration
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Event Registration

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Event Registration index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Event Registration in Rock RMS is the system area that turns an event invitation into a structured operational workflow: a person or family opens a registration link, selects registrants, answers form questions, chooses options and fees, optionally signs documents, pays or commits to pay, receives communications, and becomes visible to staff for follow-up, reporting, placement, finance reconciliation, and event execution.

For agents, the most important mental model is this:

- A **Registration Template** defines the reusable form, rules, cost model, payment behavior, confirmation/reminder communication, eligibility, signature requirements, fields, fees, discounts, and placement structure.
- A **Registration Instance** is the concrete registration configured for a specific offering, trip, class, camp, event date, or ministry use case.
- A **Registration** is one submitted transaction or submission, usually tied to the person who submitted it.
- A **Registrant** is the actual person being registered. One registration can contain multiple registrants.
- An **Event Item Occurrence linkage** connects calendar/event display to a registration instance and public-facing registration path.
- Finance records, payment plans, batches, gateway activity, workflows, groups, communications, and attributes may all participate depending on configuration.

The official [Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29) is the primary documentation authority for event registration configuration and operations. [RockU Event Registration](https://community.rockrms.com/rocku/event-registration) is useful for training sequence and topic coverage. Release notes are authoritative for version-specific behavior, especially current changes in v18.3 and v19.1 affecting signature documents, eligibility rules, duplicate prevention, wait list fields, and discount-code display behavior in event registration blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

When working in a live Rock instance, do not infer registration state from a public page alone. Inspect the registration template, registration instance, event item occurrence linkage, registration entry block settings, payment gateway settings, registrants, payments, discounts, attributes, workflow hooks, and related groups. Registration bugs often come from the boundary between these objects rather than from the form itself.

## 2. Scope And Terminology

This guide covers Rock RMS Event Registration as a concept and operating surface: templates, instances, forms, registrants, payments, fees, discounts, wait lists, group placement, event/calendar linkages, communications, workflows, reporting, and developer landmarks.

It depends on five adjacent Rock areas:

- **Events**: Event Items, Event Item Occurrences, calendars, public event display, iCalendar feeds, and linkages.
- **Finance**: payment gateways, financial transactions, batches, registration matching, refunds, discounts, partial payments, and payment plans.
- **Workflows**: automated follow-up, custom approval/change flows, reminders, ministry notifications, and exception handling.
- **Communications**: confirmation emails, payment reminders, staff alerts, registrant updates, merge fields, and delivery health.
- **Groups**: placement groups, group member creation, team/cabin/room assignment, event teams, and capacity management.

Terminology to normalize before troubleshooting:

**Registrar**
The person submitting the registration. In many cases this is a parent, spouse, staff user, ministry leader, or attendee. The registrar may or may not be one of the registrants. The [Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29) explicitly distinguishes registrar and registrant as a foundational concept.

**Registrant**
The person being registered. A children’s camp registration may have a parent as registrar and a child as registrant. A staff-entered registration may have an admin user as registrar and a participant as registrant.

**Registration Template**
The reusable definition for the registration experience. It controls the shape of the form, cost rules, fields, communications, payment/reminder behavior, wait list settings, and, in newer versions, eligibility and duplicate-prevention behavior.

**Registration Instance**
The concrete registration built from a template. Instances carry operational dates, active status, capacity, public names/linkages, accounting configuration, payment settings, and event-specific context. The documentation identifies instance settings such as **Registration Instance Name**, **Active**, **Registration Starts**, and **Registration Ends** ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)).

**Registration**
A submitted registration record. It groups one or more registrants under one submission and usually stores registrar/contact, confirmation email, payment totals, balances, and links to financial activity.

**Registration Form**
The step or group of fields shown to collect answers. Template form fields can become registrant fields, registration-level fields, or wait-list-visible fields depending on configuration and Rock version.

**Fee**
An optional or required cost component beyond the base per-registrant cost. Fees can represent shirts, lodging, ticket levels, add-ons, quantity-based items, or selectable options. RockU separates registration fees, additional fees, discounts, partial payments, and payment plans as distinct training topics ([Registration Fees](https://community.rockrms.com/rocku/event-registration/registration-fees), [Additional Registration Fees](https://community.rockrms.com/rocku/event-registration/additional-registration-fees), [Registration Discounts](https://community.rockrms.com/rocku/event-registration/registration-discounts), [Partial Payments](https://community.rockrms.com/rocku/event-registration/partial-payments), [Payment Plans](https://community.rockrms.com/rocku/event-registration/payment-plans)).

**Discount Code**
A configured code that reduces registration cost or fees. Discount visibility and reporting have version caveats. In v19.1, Rock fixed a Registration Instance Registration List issue where the Discount Code column could be hidden when the template had no per-registrant cost even though a discount applied to fees ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

**Wait List**
A registrant state used when capacity is full or the template/instance permits waiting-list capture. The Obsidian/WebForms list surfaces wait-list state; source snippets show `IsOnWaitList` driving the “WL” warning label in registration grids ([RegistrantInfoBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs), [registrantInfoBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/registrantInfoBag.d.ts)).

**Linkage**
The relationship between an event occurrence and a registration instance, commonly involving a URL slug and public display configuration. RockU includes Linkages as a dedicated event registration training topic ([Linkages](https://community.rockrms.com/rocku/event-registration/linkages)). A community Q&A example shows that API consumers may find `RegistrationInstanceId` through `EventItemOccurrences?$expand=Linkages` but still need to verify where the public URL is resolved in their Rock version and page setup ([API Q&A](https://community.rockrms.com/ask/developing/2547)).

## 3. Event Registration Mental Model

A Rock event registration is not just a form. It is a chain of objects and decisions.

The typical chain is:

1. A calendar or event item occurrence describes the event.
2. A registration template defines the registration rules.
3. A registration instance uses that template for a specific event offering.
4. A linkage connects the occurrence, public display, slug, and registration instance.
5. A public page with a Registration Entry block renders the form.
6. The registrar selects registrants, answers fields, chooses fees, and submits payment or unpaid balance.
7. Rock creates Registration and RegistrationRegistrant records.
8. Rock creates or associates financial records when money is collected.
9. Rock sends configured communications.
10. Staff manage registrants, balances, discounts, placement, notes, exports, and follow-up from internal event registration pages.

The failure points follow the same chain. If the event page says registration is closed, check the instance dates and active flag. If the page has no button, check the linkage and registration URL. If the form opens but a person cannot be selected, inspect family-member rules, registrant eligibility, duplicate prevention, and same-family settings. If payment fails, inspect gateway configuration, allowed payment methods, saved account options, and finance exceptions. If reports are wrong, confirm whether the report is using registrations, registrants, fees, financial transactions, or gateway payment-plan state.

For agents, the safe operating posture is:

- Treat **template settings** as the source of form/rule behavior.
- Treat **instance settings** as the source of event-specific open/closed, capacity, accounting, and operational state.
- Treat **linkages and block attributes** as the source of public URL behavior.
- Treat **registrant rows** as the source of participant state.
- Treat **financial transactions and gateway records** as the source of money movement.
- Treat **payment plans** as partly external to Rock because the documentation states payment schedules are controlled by the external payment gateway, and balance changes in Rock do not automatically synchronize an existing payment plan ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)).

## 4. Source Authority And How To Use This Guide

Use sources in this order when resolving a real issue:

1. **Live Rock instance evidence**
   Inspect the exact template, instance, occurrence, linkage, block, registration, registrant, payment, workflow, group, or communication. Live state wins over general documentation.

2. **Official Rock documentation**
   The [Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29) is the highest-authority narrative source in this pack. It includes registration concepts, instance settings, payment plans, matching, group placement, SSL, URL slug requirements, and event/calendar context.

3. **Release notes**
   The [Rock Core Release Notes](https://www.rockrms.com/releasenotes) are authoritative for version-specific features and fixes. In this source pack, the most important recent changes are v18.3 signature document handling and v19.1 eligibility, duplicate-prevention, discount-code display, empty-form exception logging, and wait-list field behavior.

4. **RockU training**
   [RockU Event Registration](https://community.rockrms.com/rocku/event-registration) is strong for topic coverage and mental sequencing. Its module list is useful because it separates templates, instances, attributes, fees, discounts, partial payments, wait lists, calendar linkages, iCalendar, electronic signatures, payment plans, and group placement.

5. **Developer docs and source-code landmarks**
   Developer docs identify block inputs, page parameters, merge fields, and mobile behavior. For example, the mobile Calendar Event Item Occurrence View block takes an `EventOccurrenceGuid` page parameter and exposes merge fields including `RegistrationUrl`, `EventItemOccurrence`, `Event`, `RegistrationStatusLabel`, and `RegistrationStatusLabels` ([Calendar Event Item Occurrence View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view)).

6. **Community recipes and Q&A**
   Recipes can be operationally useful but must be treated as contributed patterns, not official behavior. The recipe pages themselves include a disclaimer that community recipes are not reviewed or endorsed by the Rock core team and should be evaluated for performance and security ([Registration Instance Totals Report](https://community.rockrms.com/recipes/348), [Registration Instance Fees Report](https://community.rockrms.com/recipes/400), [Show Active Registration Discount Codes](https://community.rockrms.com/recipes/472), [Registration Notes](https://community.rockrms.com/recipes/245)).

Do not copy recipe SQL or Lava directly into production. Use recipes to learn what data relationships people commonly need, then rebuild using parameterized, permission-scoped, version-appropriate implementation.

## 5. Core Configuration And Data Model

### Configuration Surfaces

A complete event registration configuration usually spans these surfaces:

**Registration Template**
Controls reusable rules and form behavior. Inspect it first when behavior applies across many registrations or when the same problem occurs on every instance using the template.

Template-level areas commonly include:

- Name and administrative description.
- Forms and fields.
- Per-registrant cost behavior.
- Additional fees and fee options.
- Discount codes.
- Payment and partial-payment behavior.
- Payment reminder email configuration.
- Confirmation email configuration.
- Wait list behavior.
- Signature document requirement.
- Group placement settings.
- Registrants-in-same-family behavior.
- Eligibility rules in v19.1 and later.
- Prevent Duplicate Registrants in v19.1 and later.
- Placement settings if using registration placement.
- Security and staff access.

When exact fields differ by version or customization, inspect the live Registration Template Detail block rather than relying on a static checklist.

**Registration Instance**
Controls the concrete registration offering. Official documentation explicitly identifies instance settings such as Registration Instance Name, Active, Registration Starts, and Registration Ends ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)). Other common instance-level concerns include capacity, contact, accounting, public display, linkage, event occurrence, campus, group placement, and fee availability.

When diagnosing public access, inspect at minimum:

- Is the instance active?
- Has registration started?
- Has registration ended?
- Is the URL slug present where required?
- Is the instance linked to the intended Event Item Occurrence?
- Is capacity full?
- Is wait list enabled?
- Is the template active/valid?
- Does the public page’s Registration Entry block route to this instance?
- Are permissions blocking the public user?

**Event Item And Event Item Occurrence**
These belong to the Events/calendar side. They provide public event context, event date/time, calendar visibility, and occurrence-specific linkage. RockU includes calendar overview, calendars/events, linkages, event attributes, and iCalendar feed as part of the event registration training sequence ([Calendar Overview](https://community.rockrms.com/rocku/event-registration/calendar-overview), [Calendars and Events](https://community.rockrms.com/rocku/event-registration/calendars-and-events), [Linkages](https://community.rockrms.com/rocku/event-registration/linkages), [Event Attributes](https://community.rockrms.com/rocku/event-registration/event-attributes), [iCalendar Feed](https://community.rockrms.com/rocku/event-registration/icalendar-feed)).

**Registration Entry Block**
This is the public-facing form renderer. Troubleshooting needs the page, route, block attributes, page parameters, and URL slug behavior. If an issue appears only on one website/page, inspect the block instance and page route before changing a template.

**Internal Registration Blocks**
Internal tools include registration instance lists, registration details, registrant lists, fee lists, payment lists, payment reminders, group placement, and registrant detail pages. Source snippets show block-specific view models for registration instance registration lists, registrant lists, fee lists, payment lists, and payment reminders in both WebForms and Obsidian surfaces ([RegistrationInstanceRegistrantList.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx.cs), [RegistrationInstancePaymentListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstancePaymentList/RegistrationInstancePaymentListOptionsBag.cs), [RegistrationInstanceFeeListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceFeeList/RegistrationInstanceFeeListOptionsBag.cs)).

### Data Model Orientation

The core relationship chain is:

`RegistrationTemplate -> RegistrationInstance -> Registration -> RegistrationRegistrant`

Then additional relationships attach:

- `RegistrationRegistrant -> PersonAlias -> Person`
- `RegistrationInstance -> EventItemOccurrence linkage`
- `Registration/Registrant -> AttributeValues`
- `Registration -> FinancialTransaction(s)` or transaction details, depending on payment path
- `Registration -> PaymentPlan` or gateway-managed recurring/payment-plan arrangement where enabled
- `RegistrationRegistrant -> SignatureDocument` when signatures are required and completed
- `RegistrationRegistrant -> GroupMember` or placement group membership where group placement is used
- `Registration -> Communication` or communication recipient history where emails are sent
- `Registration/Registrant -> Workflow` when custom automations are triggered

Because Rock installations can have plugins, migrations, Obsidian/WebForms differences, and custom pages, agents should verify the actual table and property names in the live model map or schema before writing SQL. Community examples commonly join `RegistrationRegistrant`, `Registration`, `PersonAlias`, and `Person` to produce registrant reports, but those examples are not a substitute for live schema validation ([Single Page Registrant Info recipe](https://community.rockrms.com/recipes/313)).

## 6. Primary Entities And Relationships

### Registration Template

The template is the reusable design. It should be treated like code: changes can affect every current and future instance using it.

Operational questions to ask:

- Is this template shared across many ministries?
- Are current active registrations using it?
- Would a form change alter already submitted registrations or exports?
- Are payment reminders, discounts, fees, or signature documents configured here?
- Does the template use new v19.1 eligibility or duplicate prevention features?
- Is wait-list field visibility configured correctly?
- Are staff allowed to edit only instances, or can they edit templates?

A common permission pattern is that ministry staff can manage instances but not templates. The [Show Active Registration Discount Codes](https://community.rockrms.com/recipes/472) recipe exists because some staff could edit instances but could not see template-level discount details. In a governed Rock environment, that is not a bug by itself; it is a permission design decision. If staff need discount visibility, prefer a read-only, reviewed reporting surface over broad template edit rights.

### Registration Instance

The instance is the operating record for a specific registration. The [Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29) describes instance settings and emphasizes the displayed importance of the Registration Instance Name during the registration process.

Agents should collect these values for any incident:

- Instance Id and Guid.
- Template Id and name.
- Instance name and public name if linkages provide one.
- Active flag.
- Registration start and end date/time.
- Capacity or spots available settings.
- Wait list setting.
- Cost basis.
- Payment gateway.
- Financial account/batch naming behavior.
- Confirmation email and contact email.
- Linked event item occurrence.
- URL slug.
- Campus or audience scope.
- Group placement configuration.
- Current counts: registrations, registrants, wait-listed registrants, canceled/dropped records if retained, paid, due, discounts, refunds.

### Registration

A registration is the submitted container. It answers “what submission happened?” It may include one or more registrants. It commonly carries the confirmation email used for payment reminders. Source-code snippets for the payment reminder block state that reminder email addresses are pulled from the registration’s confirmation email and that selected registrations are identified by registration IdKeys ([RegistrationBalanceBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationBalanceBag.cs), [sendPaymentRemindersRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersRequestBag.d.ts)).

Inspect registration-level data when:

- The registrar says they registered multiple people but only one appears.
- Payment was made once for several registrants.
- Confirmation email went to the wrong person.
- Balance due looks incorrect.
- A payment reminder did or did not send.
- A discount code was applied to a submission.
- A workflow refers to the registration rather than an individual registrant.

### RegistrationRegistrant

A registrant is the person being registered. It is the operational row for attendance, roster, wait list, signature, placement, and person-specific form answers.

Source snippets show that registrant list grids include a registrant display name and wait-list indicator ([RegistrantInfoBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs)). The legacy WebForms registrant list block includes filters for registration date range, first name, last name, in-group state, signed document state, and dynamic registrant form field filters ([RegistrationInstanceRegistrantList.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx)).

Inspect registrant-level data when:

- A person appears on a roster but the registration payment is under someone else.
- A wait-list label appears or does not appear.
- A signed document is missing or wrong.
- A group placement is missing.
- A child/adult eligibility rule blocked selection.
- A duplicate-prevention setting blocked submission.
- A registrant field answer is missing from an export.
- A family-member selection produced the wrong person.

### Event Item Occurrence And Linkage

An event occurrence describes the event’s scheduled occurrence. A linkage connects it to registration. Developer docs for the mobile Calendar Event Item Occurrence View block show that the page parameter is `EventOccurrenceGuid`, and the template has merge fields including `RegistrationUrl`, `EventItemOccurrence`, `Event`, and registration status labels ([Calendar Event Item Occurrence View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view)).

The important operational detail is that there may be more than one path to the same registration:

- Direct registration instance page parameter.
- Slug-based public URL.
- Event occurrence page with registration URL merge field.
- Mobile event occurrence block.
- Calendar item card.
- Email link.
- Custom Lava link.
- QR code or external landing page.

When URLs differ, inspect the linkage, public page route, Registration Entry block, slug, and any custom Lava that rewrites the title or link.

### Attributes And Form Fields

Event registration uses attributes in several places:

- Event attributes.
- Registration instance attributes.
- Registration-level form fields.
- Registrant-level form fields.
- Wait-list-visible fields.
- Attribute filters in internal grids.

RockU separates Event Registration Attributes and Event Attributes as distinct training topics ([Event Registration Attributes](https://community.rockrms.com/rocku/event-registration/event-registration-attributes), [Event Attributes](https://community.rockrms.com/rocku/event-registration/event-attributes)). In practice, agents must identify which entity owns the attribute before querying or editing.

If a field is missing from a grid or export:

1. Identify whether it is a registration field, registrant field, event field, occurrence field, or instance attribute.
2. Inspect whether the field is set to show on grid/export.
3. In v19.1 and later, inspect wait-list field visibility because Rock updated handling of “Show On Wait List” for registrant fields and requires First Name and Last Name to remain visible on wait lists ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
4. Confirm the block’s dynamic filters or export behavior include that attribute.
5. Verify the value exists on the expected entity.

## 7. Common Event Registration Workflows

### Basic Public Registration

The common public flow is:

1. Person opens an event detail page, calendar page, mobile event occurrence, or direct registration URL.
2. Rock resolves the registration instance by page parameter or slug.
3. Registration Entry checks whether registration is active, open by date, not full, and eligible for registration or wait list.
4. Registrar enters contact information.
5. Registrar selects one or more registrants.
6. Registrar answers form fields.
7. Registrar selects fee options.
8. Rock calculates cost, discounts, minimum due, balance, and payment choices.
9. Registrar pays, partially pays, or submits without payment depending on configuration.
10. Rock creates registration and registrant records.
11. Rock sends confirmation communication.
12. Staff see the registration in internal tools.

Troubleshooting branch: if the public form does not open, check instance active flag, start/end dates, slug/linkage, public page block configuration, authentication requirements, capacity/wait-list behavior, and template validity.

### Family And Guest Registration

Family registration creates frequent mistakes because the registrar and registrant differ. In v19.1, Rock added registrant eligibility rules and updated the Registration Entry block so that when “Registrants In Same Family” is “Yes” or “Ask”, the Family Member to Register dropdown defaults blank when the registrant page first loads, reducing accidental self-registration ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

For agents, this means modern troubleshooting should include:

- What Rock version is running?
- Is `Registrants In Same Family` set to Yes, No, or Ask?
- Are family members filtered by eligibility?
- Was the first family member auto-selected in this version, or must the user choose intentionally?
- Did the user register themselves when they meant to register a child?
- Does the registrant row’s PersonAlias point to the expected person?

### Paid Registration

Paid registration adds finance dependencies:

- Payment gateway configuration.
- Accepted payment methods.
- Saved account payment options.
- Gateway-specific ACH/card rules.
- Cost and fee calculation.
- Discounts.
- Partial payments.
- Payment plans.
- Financial account routing.
- Batches.
- Transaction matching.

RockU treats registration fees, additional fees, discounts, partial payments, and payment plans as separate topics, which is the right diagnostic shape ([Registration Fees](https://community.rockrms.com/rocku/event-registration/registration-fees), [Additional Registration Fees](https://community.rockrms.com/rocku/event-registration/additional-registration-fees), [Registration Discounts](https://community.rockrms.com/rocku/event-registration/registration-discounts), [Partial Payments](https://community.rockrms.com/rocku/event-registration/partial-payments), [Payment Plans](https://community.rockrms.com/rocku/event-registration/payment-plans)).

Do not treat “paid” as a single flag. Inspect total cost, paid amount, balance due, discount amount, transaction status, gateway status, refund status, and payment plan state.

### Wait List Registration

Wait-list behavior depends on capacity and template settings. The source-code view models identify wait-list state as a registrant-level display property in internal grids ([RegistrantInfoBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs)). The mobile event occurrence developer doc notes that registration status labels can return “Full” when spots available is less than one unless wait-list behavior changes the status label; verify exact wording in the live block/version ([Calendar Event Item Occurrence View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view)).

For wait-list issues, inspect:

- Instance capacity and remaining spots.
- Whether wait list is enabled.
- Whether the registrant is on wait list or fully registered.
- Whether required wait-list fields are configured.
- In v19.1, whether First Name and Last Name are always shown on wait list, and whether new fields default to Show On Wait List ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Whether payment is required for wait-list entries.
- Whether staff moved someone off the wait list manually.
- Whether group placement excludes wait-listed registrants.

### Group Placement

Group placement is used for teams, cabins, rooms, tracks, serving groups, classroom rosters, and other post-registration assignment flows. RockU includes both legacy group placement and revamped group placement training topics ([Group Placements [Legacy]](https://community.rockrms.com/rocku/event-registration/group-placement-in-event-registration), [Group Placement](https://community.rockrms.com/rocku/event-registration/group-placement)). The [Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29) says Rock 18.1 documentation was updated for revamped Registration Group Placement and includes placement rule/default details.

The documentation excerpt identifies parameters and placement concepts such as:

- `DestinationGroupType`
- `DestinationGroup`
- `RegistrationInstanceId`
- `RegistrationTemplateId`
- `RegistrationTemplatePlacementId`
- Registration Mode
- Group Mode
- Entity Set Mode
- Allowing a person to be placed in more than one group

Before changing placement behavior, inspect the live template placement configuration and identify which placement mode is being used.

### Payment Reminder Workflow

Payment reminders are internal tools for registrations with outstanding balances. Source-code snippets show the Obsidian payment reminder block has initialization state for outstanding balance rows, default From Name, From Email, Subject, message body, preview HTML, instructions, preselected registration keys, and selected registration IdKeys ([RegistrationInstanceSendPaymentReminderInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationInstanceSendPaymentReminderInitializationBox.cs), [sendPaymentRemindersRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersRequestBag.d.ts)).

Key operational details from the source snippets:

- Balance rows include cost, paid, balance due, email, registration date, and last reminder date.
- The email is pulled from registration confirmation email.
- Reminder body is Lava and is resolved per registration at send time.
- Preview rendering resolves Lava against a sample registration.
- Recently reminded rows may be visually inactive based on the template’s payment reminder time span, but that state is display guidance rather than necessarily a hard send prohibition.
- Registrations without confirmation email are skipped and not counted as sent ([sendPaymentRemindersResponseBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersResponseBag.d.ts)).

## 8. Registration Instances Deep Dive

### Instance Identity

The instance name matters. The documentation notes the Registration Instance Name is shown during registration and used in confirmation-style wording ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)). Do not use purely internal naming conventions if the instance name surfaces publicly in your version/page setup. If a church needs different public and internal naming, use supported public-name/linkage features where available and verify the page output.

A community recipe attempted to control public titles with slug and public name, but that recipe is unpublished because of SQL injection risk ([Control the Title on The Event Registration Page](https://community.rockrms.com/recipes/361)). Treat it as a cautionary example: solve public-title needs with supported configuration or carefully reviewed, parameterized code, not raw page-parameter SQL.

### Active And Date Windows

The minimum open/closed decision is:

- Instance active?
- Current date/time greater than or equal to Registration Starts?
- Current date/time before or equal to Registration Ends?
- Capacity available, or wait list allowed?
- Public URL valid?
- Required payment/signature/settings valid?

When a user says “registration is closed but it should be open,” inspect instance values first. Do not begin with CSS, browser cache, or workflow unless the database state is correct.

### Capacity And Spots

Capacity may be represented at the instance level, fee-option level, group/placement level, or a combination depending on setup. The community [Registration Change Tool](https://community.rockrms.com/recipes/518/registration-change-tool) illustrates a real operational edge case: staff may need to add someone when a registration instance or a fee option is full. It recommends a custom tool and workflow, but because it is a recipe with plugin dependency, use it as a pattern rather than authority.

Operationally, full-capacity changes require care:

- Increasing instance spots can expose public capacity to anyone with the URL.
- Obscure slugs are not true security.
- Adding someone to a full fee option can violate capacity assumptions.
- Manual inserts can bypass business logic.
- Payment, wait list, and placement state must remain consistent.
- Auditable staff notes are valuable.

Preferred playbook: temporarily close public registration, make an admin-controlled change through supported UI or reviewed workflow, document the reason, validate counts, then reopen if needed.

### URL Slug And Public Linkage

The official guide includes a “URL Slug Required” section in its event registration content map ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)). The exact behavior can vary by route and block setup, so inspect:

- Event Item Occurrence linkage.
- Registration Instance linkage fields.
- URL slug.
- Public name.
- Registration Entry page route.
- Page parameters used by the route.
- Any event calendar/detail block registration URL setting.
- Mobile block registration URL setting.

A developer Q&A shows that querying EventItemOccurrences with expanded Linkages may reveal `RegistrationInstanceID` while not directly yielding the desired public URL in `UrlSlug` ([API Q&A](https://community.rockrms.com/ask/developing/2547)). For integrations, build URLs from the same route and linkage logic the site uses, and verify against live rendered links.

### Attributes

Registration instance attributes are useful for operational metadata: campus-specific labels, ministry owner, event season, external IDs, rooming deadlines, export flags, custom reporting tags, or integration state. They are not the same as registrant form answers.

When an agent needs an attribute:

- Identify entity type.
- Confirm attribute key, field type, and qualifier values.
- Confirm whether the value is stored on the instance, registration, registrant, event item, event occurrence, group, or person.
- Confirm whether it is included in grids, exports, APIs, or Lava merge fields.
- Avoid assuming attribute keys are short or stable. A Triumph Tech release spotlight mentions a fix for Registration Instance List filtering when an attribute key exceeded 250 characters ([GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-182025)); verify current version behavior before building reports around unusual keys.

## 9. Payments Deep Dive

### Cost Model

Event registration money can come from multiple layers:

- Base per-registrant cost.
- Additional fees.
- Quantity-based fees.
- Optional selections.
- Discounts.
- Minimum due or deposit.
- Partial payments.
- Payment plan schedules.
- Manual payments.
- Refunds or adjustments.

Do not diagnose payment issues from only the visible balance. Recalculate from source records:

1. Registrants included.
2. Base cost per registrant.
3. Fee selections per registrant or registration.
4. Quantity selections.
5. Discount code and discount rules.
6. Payments received.
7. Refunds or failed payments.
8. Payment plan state.
9. Manual adjustments.
10. Gateway transaction status.

RockU’s separate modules for fees, additional fees, discounts, partial payments, and payment plans are useful because each layer can be configured or fail independently ([Event Registration](https://community.rockrms.com/rocku/event-registration)).

### Discounts

Discount codes are typically template-level configuration. If staff can manage instances but not templates, they may not see discount rules. The [Show Active Registration Discount Codes](https://community.rockrms.com/recipes/472) recipe describes adding a read-only panel to expose active or scheduled discount codes to staff with limited rights. Use this as an operational pattern, not as official implementation guidance.

Troubleshoot discounts by checking:

- Code spelling and case behavior in the live UI.
- Active/scheduled date window.
- Usage limits.
- Whether the discount applies to base cost, fees, or both.
- Whether the template has per-registrant cost.
- Whether the Registration List block version correctly displays the Discount Code column for fee-only discounts. v19.1 fixed a bug in this area ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Whether a payment plan was created before discount changes. Payment plans may not auto-sync with balance changes ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)).

### Partial Payments

Partial payments allow a registration to be submitted with a balance due. This is operationally useful for camps, retreats, mission trips, and high-cost events. It also creates collection risk.

Before enabling partial payments:

- Confirm the minimum amount due.
- Configure reminder communication.
- Decide who monitors balances.
- Decide whether registrants with balances can attend.
- Decide when to cancel unpaid registrations.
- Confirm whether payment plans are allowed or separate.
- Test confirmation email wording.
- Test staff views for balance due.

Payment reminder block source shows balance rows include total cost, paid amount, balance due, registered date, last reminder date, and email ([RegistrationBalanceBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationBalanceBag.cs)). That is the right minimum data set for operational collection.

### Payment Plans

Payment plans require extra caution. The official guide says payment plan management happens in the same screens used for event registrations and that a calendar icon appears next to Balance Due when a payment plan is in place. It also states payment plan changes do not automatically synchronize when a registration balance changes, because schedules are controlled by an external payment gateway such as My Well ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)).

Agent rules for payment plans:

- Never assume changing a Rock registration balance updates the gateway schedule.
- Inspect both Rock and gateway state.
- If a discount, refund, fee change, registrant removal, or manual adjustment happened after plan creation, verify gateway schedule separately.
- Confirm whether a payment plan is active, completed, canceled, or failed.
- Confirm whether the balance due display has been adjusted for active payment plan state.
- Communicate to finance staff when Rock and gateway state diverge.

### Payment Gateways And Saved Accounts

Gateway configuration affects available payment options. A Triumph Tech spotlight notes a v16.10 issue where the Obsidian Event Registration block could still show an individual’s saved ACH option even when ACH was disabled in Financial Gateway settings ([GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-182025)). Treat gateway/payment-option behavior as version-sensitive.

When payment methods look wrong:

- Inspect the Financial Gateway settings.
- Inspect whether ACH/card is enabled.
- Inspect saved account behavior.
- Check whether the block is WebForms or Obsidian.
- Check Rock version and release notes.
- Test with a user who has saved accounts and a user who does not.
- Verify the gateway transaction logs.

### Batches And Matching

The official guide describes Event Registration Matching with open batches, registration template, and registration instance; it notes that the batch must be open and not pending ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)). This is finance-side reconciliation, not public registration configuration.

When reconciling:

- Select the correct open batch.
- Select the correct template.
- Select the correct instance.
- Match one registration instance at a time unless the live tool explicitly supports otherwise.
- Confirm transaction dates and amounts.
- Watch for partial payments and payment plans.
- Confirm refunds and failed gateway transactions.
- Keep finance permissions tight.

## 10. Related Rock Areas: Events, Finance, Workflows, Communications, Groups

### Events And Calendars

Event registration often begins with Event Item and Event Item Occurrence configuration. RockU includes calendar overview, calendars/events, linkages, event attributes, and iCalendar feed in the same Event Registration training section ([RockU Event Registration](https://community.rockrms.com/rocku/event-registration)).

Use the Events side to answer:

- Where should this event appear?
- Which calendar owns it?
- Which occurrence is linked to registration?
- Does the public event detail page show the right registration status?
- Does the mobile app show the same registration link/status?
- Are event attributes driving visibility, filtering, or layout?
- Does the iCalendar feed need the event but not the registration?

### Finance

Finance owns real money. Event registration owns the registration workflow. The boundary matters.

Finance checks:

- Payment gateway.
- Financial account.
- Batch naming.
- Transaction detail mapping.
- Discounts.
- Refunds.
- Payment plans.
- Failed transactions.
- Reconciliation.
- Permissions for staff who can adjust costs.

Community reporting recipes for totals and fees show common operational needs: organizers want quick views of paid, due, discounted, and fee-option totals ([Registration Instance Totals Report](https://community.rockrms.com/recipes/348), [Registration Instance Fees Report](https://community.rockrms.com/recipes/400)). Build production reporting with reviewed SQL/Lava or native reporting tools, not unreviewed copy-paste.

### Workflows

Workflows are common around event registration:

- Approval required before registration is final.
- Staff notification on submission.
- Scholarship review.
- Cancellation request.
- Change request.
- Wait-list promotion.
- Roommate/team preference processing.
- Payment reminder escalation.
- Required document chase.
- Background check or leader approval.
- External system sync.

The [Registration Change Tool](https://community.rockrms.com/recipes/518/registration-change-tool) recipe demonstrates a custom page plus workflow pattern for controlled registration edits. If implementing similar behavior, prefer safe entity services, workflow actions, and permission checks over raw SQL inserts.

### Communications

Communications include:

- Confirmation email.
- Payment reminders.
- Staff notifications.
- Wait-list messages.
- Signature reminders.
- Cancellation notices.
- Event updates.
- Merge templates.
- Communication history.

Source snippets for payment reminders show message bodies are Lava, default sender/subject/body can come from the registration template, and previews resolve against sample registration data ([RegistrationInstanceSendPaymentReminderInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationInstanceSendPaymentReminderInitializationBox.cs), [ResolvePreviewRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/ResolvePreviewRequestBag.cs)).

For communication issues:

- Confirm the template has the expected sender, subject, and body.
- Confirm merge fields render for a sample registration.
- Confirm confirmation email exists on the registration.
- Check communication queue/history.
- Check email delivery provider logs.
- Check suppressions/bounces.
- Confirm reminders skip registrations without confirmation email, per source-code response behavior ([sendPaymentRemindersResponseBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersResponseBag.d.ts)).

### Groups

Groups are used for event rosters, placement, teams, cabins, classes, serving assignments, and post-registration follow-up. The official guide’s group placement update and RockU group placement modules make clear that group placement is a first-class event registration concern ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29), [Group Placement](https://community.rockrms.com/rocku/event-registration/group-placement)).

When groups are involved:

- Identify the source registration instance/template.
- Identify destination group type.
- Identify destination groups.
- Confirm group capacity if relevant.
- Confirm whether a person can be placed in more than one group.
- Confirm whether placement is manual or automatic.
- Confirm wait-listed registrants should be included or excluded.
- Confirm whether group membership drives check-in, communication, or attendance.

## 11. Administration And Operational Guardrails

### Permissions

Event registration touches public forms, personal data, payment data, group placement, and communications. Permission design should separate:

- Template administrators.
- Instance managers.
- Finance users.
- Ministry viewers.
- Group placement users.
- Communication senders.
- Developers/integration users.
- Public/anonymous users.

Do not grant template edit rights merely because staff need discount visibility or registrant totals. Build read-only reporting surfaces where appropriate.

### Naming

Use names that support both internal operations and public clarity. If public name differs from internal naming, use supported public-name/linkage behavior and verify output. Avoid hacks that depend on raw slug SQL. The unpublished SQL-injection-risk recipe for title control is a useful warning ([Control the Title on The Event Registration Page](https://community.rockrms.com/recipes/361)).

### Change Management

For active registrations, changes are risky. Before changing a template or instance:

- Count active registrations and registrants.
- Export or snapshot key values.
- Identify whether changes affect future submissions only or existing records.
- Confirm finance impact.
- Confirm payment plan impact.
- Test public form.
- Test confirmation email.
- Notify ministry owner.
- Document the change.

High-risk changes include:

- Fees.
- Discounts.
- Payment gateway.
- Partial payment minimum.
- Required fields.
- Signature documents.
- Eligibility rules.
- Duplicate prevention.
- Capacity.
- Wait list behavior.
- Group placement rules.
- URL slug.

### Notes And Auditability

Community practice includes adding Notes blocks to registration detail pages to preserve context around drops, changes, and exceptions ([Registration Notes](https://community.rockrms.com/recipes/245)). If your instance needs this, configure a proper Note Type and secure it. Notes are especially useful when staff remove or alter registrants and later need to know why.

### Security

Event registration customizations often expose SQL/Lava risk because page parameters, registration IDs, slugs, and person IDs are tempting shortcuts.

Guardrails:

- Do not put raw page parameters into SQL.
- Prefer entity commands, Lava filters, or server-side code with authorization checks.
- If SQL is necessary, parameterize and restrict.
- Do not expose internal IDs in public links unless Rock’s route requires them and permissions are appropriate.
- Do not trust obscure slugs as access control.
- Do not expose discount code lists publicly.
- Do not include sensitive medical or child data in broad exports.
- Review community recipes before use.

### Operational Health Checks

For each active registration, agents should be able to report:

- Public URL works.
- Registration status label is accurate.
- Instance is active and date window is correct.
- Capacity and wait list behavior are intentional.
- Test registration can be submitted in staging or approved test mode.
- Payment gateway works with intended methods.
- Confirmation email renders.
- Staff can view registrants.
- Required reports exist.
- Finance reconciliation path is known.
- Group placement path is known.
- Payment reminders are configured if balances can remain.
- Version-specific caveats have been checked.

## 12. Developer, API, Lava, And Source-Code Landmarks

### Public/Mobile Event Occurrence Rendering

The mobile Calendar Event Item Occurrence View block is a useful developer landmark. It uses `EventOccurrenceGuid` as a page parameter and has a configurable Registration URL plus a rendering template. Its merge fields include `RegistrationUrl`, `EventItemOccurrence`, `Event`, `RegistrationStatusLabel`, and `RegistrationStatusLabels` ([Calendar Event Item Occurrence View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view)).

Use this when building or debugging mobile/event-detail surfaces:

- Confirm the occurrence Guid.
- Confirm the block’s Registration URL setting.
- Inspect merge-field output.
- Compare first-instance status label vs all status labels.
- Test full/wait-list edge cases.
- Confirm mobile and web use the same registration target when intended.

### API Linkage Caveat

A community Q&A shows a developer querying `EventItemOccurrences` filtered by Event Item Id and expanding `Linkages`, receiving a valid `RegistrationInstanceID` but not the expected public URL slug ([API Q&A](https://community.rockrms.com/ask/developing/2547)). Because the Q&A has no authoritative answer in the source pack, agents should not invent a universal API path.

Instead, inspect live:

- `EventItemOccurrence` linkage records.
- Registration instance route/slug fields.
- Public page route.
- Registration Entry block page parameters.
- Lava used by event cards.
- Mobile block Registration URL setting.
- API shape in the running Rock version.

### Internal Registrant List

The legacy WebForms `RegistrationInstanceRegistrantList` block displays registrants related to a Registration Instance and has linked pages for registration details and group placement. Source snippets show filters for registration date range, first name, last name, in-group state, signed document state, and registrant form field filters ([RegistrationInstanceRegistrantList.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx.cs), [RegistrationInstanceRegistrantList.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx)).

Use this landmark to troubleshoot:

- Why a registrant is not visible.
- Whether a signed document filter is excluding records.
- Whether a group placement link is configured.
- Whether dynamic form field filters exist.
- Whether export columns include expected fields.

### Registration List Wait-List Indicator

Obsidian view models include registrant display name and `IsOnWaitList`, which drives a wait-list warning label in grids ([RegistrantInfoBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs), [registrantInfoBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/registrantInfoBag.d.ts)). Use this to distinguish display issues from data issues: if the database says a registrant is wait-listed but the grid does not show it, check block version and model binding.

### Fee And Payment List Blocks

The Obsidian fee and payment list option bags identify export configuration and currency information surfaces ([RegistrationInstanceFeeListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceFeeList/RegistrationInstanceFeeListOptionsBag.cs), [RegistrationInstancePaymentListOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstancePaymentList/RegistrationInstancePaymentListOptionsBag.cs)). These are developer landmarks for customizing or debugging internal list exports.

### Payment Reminder Block

The payment reminder source snippets are unusually operationally rich. They identify:

- Outstanding balance grid initialization.
- Empty-state behavior.
- Default From Name, From Email, Subject, and Body from template values.
- Lava message preview against a sample registration.
- Preselected registrations based on reminder timing.
- Selected registration keys sent to the server.
- Skipping registrations without confirmation email.
- Success message with sent count.

Use these source files when payment reminder behavior is disputed:

- [RegistrationBalanceBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationBalanceBag.cs)
- [RegistrationInstanceSendPaymentReminderInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationInstanceSendPaymentReminderInitializationBox.cs)
- [ResolvePreviewRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/ResolvePreviewRequestBag.cs)
- [ResolvePreviewResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/ResolvePreviewResponseBag.cs)
- [sendPaymentRemindersRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersRequestBag.d.ts)
- [sendPaymentRemindersResponseBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersResponseBag.d.ts)

### Agent Skills

Rock developer docs describe Skills as a way to group related tools and shared context for agents, using Event Registration as an example of a skill that explains how templates, instances, registrations, and registrants relate ([Skills](https://community.rockrms.com/developer/ai-agents/skills)). For a Rock agent environment, Event Registration is a strong candidate for a dedicated skill because it has repeatable object navigation, permissions, live-state checks, and cross-domain dependencies.

## 13. Reporting, Analytics, And Model Map

### Core Metrics

For a registration instance, agents should be able to compute:

- Total registrations.
- Total registrants.
- Wait-listed registrants.
- Canceled/dropped registrants if retained.
- Total capacity.
- Remaining capacity.
- Total cost.
- Total paid.
- Balance due.
- Total discounts.
- Fee totals by fee option.
- Registrants by campus, grade, age, gender, group, or attribute.
- Missing signatures.
- Missing required form answers.
- Outstanding payment reminders.
- Registrants not placed in groups.
- Registrants without valid confirmation email.

### Reporting Entity Choice

Choose the reporting root carefully:

- Use **RegistrationInstance** for instance-level dashboards.
- Use **Registration** for payment/balance/contact submission reporting.
- Use **RegistrationRegistrant** for roster, person, wait-list, signature, and placement reporting.
- Use **FinancialTransaction** or related finance tables for actual money movement.
- Use **AttributeValue** only after confirming entity type and attribute id/key.
- Use **GroupMember** for placement outcomes.
- Use **Communication** records for send/delivery history.

Community recipes illustrate the demand for instance totals, fee totals, registrant packets, discount visibility, and notes ([Registration Instance Totals Report](https://community.rockrms.com/recipes/348), [Registration Instance Fees Report](https://community.rockrms.com/recipes/400), [Single Page Registrant Info](https://community.rockrms.com/recipes/313), [Show Active Registration Discount Codes](https://community.rockrms.com/recipes/472), [Registration Notes](https://community.rockrms.com/recipes/245)). Use them to identify user needs, then implement reports in a secured, reviewed way.

### Model Map Verification

When the source material is thin or version-sensitive, inspect the live model map or schema. Verify:

- Table names.
- Property names.
- Navigation properties.
- Obsidian vs WebForms block availability.
- Attribute entity type ids.
- Enum values.
- Financial transaction relationships.
- Signature document relationship.
- Payment plan tables/foreign keys.
- Group placement tables.
- Linkage table and slug fields.

Do not assume a community SQL snippet is correct for the current Rock version. The source pack includes examples that join `RegistrationRegistrant`, `Registration`, `PersonAlias`, and `Person` for roster output ([Single Page Registrant Info](https://community.rockrms.com/recipes/313)), but agents should validate schema before adapting.

### Analytics Checks

For leadership or ministry dashboards, include definitions:

- **Registered**: registrants not on wait list and not canceled/dropped, if cancellation is tracked.
- **Wait-listed**: registrants with wait-list flag.
- **Paid in full**: registration balance due equals zero and payments are settled.
- **Outstanding**: balance due greater than zero after discounts, refunds, and active payment plan adjustments.
- **Placed**: registrant has expected group membership or placement record.
- **Ready for event**: registered, paid or approved, required forms complete, signature complete, placement complete.

Each definition must be adapted to the organization’s Rock version and operational policy.

## 14. Version And Release Caveats

### Rock 18.1

The official Event & Calendar Guide notes updates for Rock 18.1, including revamped Registration Group Placement for sorting registrants into groups such as sports teams and camps ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)). If a site has recently upgraded around v18, compare old legacy group placement patterns to the revamped workflow.

### Rock 18.3

Release notes for v18.3 include a bug fix for internal Event Registration blocks: Registration Instance - Registration List, Registration Details, and Registrant Details could show an incorrect Signature Document for a registrant without a valid `SignatureDocumentId` because documents were matched by person instead of the registrant record. The fix updated blocks to use the registrant’s SignatureDocument relationship and included a data migration to backfill missing values when a matching valid document exists, excluding legacy templates ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Operational implication: if a signature document looks wrong, verify Rock version and inspect the registrant’s actual signature document relationship, not just person-level documents.

### Rock 19.1

The v19.1 Event release notes in this pack include several important changes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)):

- **Registrant eligibility rules** were added to Registration Template Detail and enforced in Registration Entry. Rules can limit registrants by age, grade, gender, and age classification. When multiple rules are enabled, registrants must meet all selected criteria.
- **Family member dropdown behavior** changed so that when Registrants In Same Family is Yes or Ask, the dropdown defaults blank on initial load, requiring intentional selection.
- **Prevent Duplicate Registrants** was added to Registration Template to prevent the same person record from registering for the same Registration Instance more than once. Validation occurs during registrant selection and before submission, including multi-registrant entries.
- **Discount Code column display** was fixed for registrations where no per-registrant cost exists but a discount applies to fees.
- **Empty registration template form exception logging** was corrected so empty form-field configurations do not create false-positive exceptions during submission.
- **Show On Wait List handling** changed so First Name and Last Name are always shown on wait list and new fields default to Show On Wait List.

Operational implication: a v19.1 registration may block people who could register in earlier versions because eligibility or duplicate-prevention settings are now active. Conversely, some old accidental family-member registration behavior should be reduced.

### v16.10 / v17.0 Spotlight

A Triumph Tech GitHub spotlight reports v16.10 highlights including an optional `SignatureDetails` merge field for electronic signature templates and an Obsidian Event Registration ACH saved-payment-option fix when ACH is disabled in the gateway ([GitHub Spotlight](https://www.triumph.tech/resources/github-spotlight-182025)). Treat this as secondary release commentary; verify against official release notes and live version before relying on it.

## 15. Implementation Playbooks

### Playbook A: Create A Standard Paid Event Registration

1. Define the event goal, audience, date, capacity, and owner.
2. Decide whether the registration is individual, family, guest, or multi-registrant.
3. Choose or create a Registration Template.
4. Configure forms and required fields.
5. Configure base cost and additional fees.
6. Configure discounts if needed.
7. Configure partial payments or require full payment.
8. Configure payment gateway and financial account.
9. Configure confirmation email.
10. Configure payment reminders if balances can remain.
11. Configure wait list if capacity may fill.
12. Configure signature documents if required.
13. Create the Registration Instance.
14. Set Active, Registration Starts, and Registration Ends.
15. Configure capacity/spots.
16. Link the instance to the Event Item Occurrence.
17. Configure URL slug/public name.
18. Test public registration as anonymous and logged-in users.
19. Test payment in approved test mode or staging.
20. Verify internal registration, registrant, payment, and fee lists.
21. Verify confirmation email.
22. Document owner, support path, and finance reconciliation path.

### Playbook B: Add Eligibility Rules In v19.1+

1. Confirm Rock version supports registrant eligibility rules.
2. Open the Registration Template Detail.
3. Locate Registrant Eligibility settings.
4. Decide age minimum/maximum, grade minimum/maximum, gender, and age classification.
5. Confirm rules should combine with AND behavior, because release notes state registrants must meet all selected criteria ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
6. Test with eligible and ineligible family members.
7. Confirm the Family Member to Register dropdown filters correctly.
8. Attempt final submission with an ineligible selected registrant if possible in staging to confirm server-side validation.
9. Update staff instructions.

### Playbook C: Prevent Duplicate Registrants In v19.1+

1. Confirm the event should prevent duplicate person records in the same instance.
2. Enable Prevent Duplicate Registrants on the Registration Template.
3. Test a single registrant already registered.
4. Test a multi-registrant submission where one person is already registered.
5. Confirm the user-facing message is clear.
6. Define staff override procedure for legitimate exceptions.
7. Document whether duplicate prevention applies only to the same person record, not duplicate names or unresolved guests.

### Playbook D: Configure Payment Reminders

1. Confirm partial payments or outstanding balances are allowed.
2. Configure template payment reminder sender, subject, body, and time span.
3. Use Lava carefully; preview against a sample registration.
4. Open the payment reminder block for the instance.
5. Confirm outstanding balances exist.
6. Confirm confirmation emails exist.
7. Review preselected rows and recently reminded rows.
8. Send to a small test set if possible.
9. Verify communication history and sent count.
10. Follow up on skipped registrations without confirmation email.

### Playbook E: Diagnose A Missing Public Registration Button

1. Open the event page and capture the exact URL.
2. Identify the Event Item Occurrence.
3. Inspect linkage to Registration Instance.
4. Confirm Registration URL/block settings.
5. Confirm instance is Active.
6. Confirm Registration Starts/Ends window.
7. Confirm capacity and wait list.
8. Confirm public page route and page parameters.
9. Confirm the public user has view access.
10. Confirm no custom Lava hides the button.
11. Compare web and mobile status labels if applicable.

### Playbook F: Build A Read-Only Registration Dashboard

1. Define audience: ministry, finance, executive, check-in, camp admin.
2. Define metrics and entity roots.
3. Prefer native reporting or reviewed SQL.
4. Include registrations, registrants, wait list, paid, due, discounts, fee totals, missing signatures, and placement status.
5. Secure by event owner or staff role.
6. Avoid exposing sensitive child/medical fields by default.
7. Validate totals against internal Registration Instance pages.
8. Document definitions.

## 16. Troubleshooting Decision Tree

### Public page says registration is closed

Check:

- Instance Active.
- Registration Starts.
- Registration Ends.
- Current server time/time zone.
- Capacity/spots.
- Wait list enabled.
- Linkage points to correct instance.
- Public page block resolves correct instance.
- Template is valid.
- Version-specific status label behavior.

If all database settings look open, inspect block configuration and custom Lava.

### User cannot select the intended family member

Check:

- Rock version.
- Registrants In Same Family setting.
- v19.1 eligibility rules.
- Age, grade, gender, and age classification data on the person.
- Whether the person is in the same family.
- Duplicate-prevention setting.
- Existing registrant records for the same instance.
- Person merge/duplicate records.

### Duplicate registration is blocked

Check:

- Whether v19.1 Prevent Duplicate Registrants is enabled.
- Existing RegistrationRegistrant rows for the same person record and instance.
- Whether wait-listed registrants count for the duplicate check in the live version.
- Whether a staff override path exists.
- Whether the person has duplicate Person records.

### Discount code does not work

Check:

- Template discount configuration.
- Code spelling.
- Active/scheduled dates.
- Usage limits.
- Applies-to scope.
- Fee-only vs base-cost discount.
- Registration date/time.
- Already-applied codes.
- v19.1 display fix if the issue is only grid visibility.

### Balance due is wrong

Check:

- Base cost.
- Fee selections.
- Quantity fees.
- Discounts.
- Payments.
- Failed payments.
- Refunds.
- Manual adjustments.
- Payment plan state.
- Gateway state.
- Whether a post-payment discount or fee change failed to sync to payment plan.

### Payment plan amount is wrong

Check:

- Rock balance.
- Gateway schedule.
- Date payment plan was created.
- Discounts or fees changed after plan creation.
- Gateway cancellation/update history.
- Finance notes.
- The official warning that payment plan changes do not auto-sync from balance changes ([Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29)).

### Signature document shown for wrong registrant

Check:

- Rock version.
- v18.3 signature document fix/migration.
- Registrant `SignatureDocumentId`.
- Person-level signature documents.
- Required template.
- Legacy template exclusion.
- Internal block version.

### Registrant missing from group placement

Check:

- Is registrant wait-listed?
- Is registrant fully registered?
- Placement mode.
- Destination group type/group.
- Template placement id.
- Group capacity.
- Allow multiple placements.
- Existing group member record.
- Placement block/page configuration.

### Payment reminder did not send

Check:

- Outstanding balance.
- Confirmation email.
- Selected row.
- Recently reminded visual state.
- Template reminder time span.
- Sender/from email.
- Communication queue/history.
- Email provider delivery.
- Source-code behavior that skips registrations without confirmation email ([sendPaymentRemindersResponseBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersResponseBag.d.ts)).

## 17. Agent Task Recipes

### Recipe: Summarize A Registration Instance

Collect and return:

- Instance name, Id, Guid.
- Template name and Id.
- Active/start/end state.
- Public URL and linkage.
- Capacity, registered count, wait-list count.
- Total registrations and registrants.
- Total paid, due, discounts.
- Fee totals.
- Missing signatures.
- Unplaced registrants.
- Payment plans.
- Recent errors or exceptions.
- Version caveats.

### Recipe: Verify A Public Registration URL

Inspect:

- URL route and parameters.
- Event occurrence linkage.
- Registration Instance Id.
- Slug/public name.
- Registration Entry block settings.
- Instance active/date/capacity.
- Rendered status label.
- Mobile equivalent if applicable.
- Anonymous access.

Return whether the URL targets the intended registration and why it is open, closed, full, wait-listing, or broken.

### Recipe: Audit Payment Risk

Inspect:

- Registrations with balance due.
- Confirmation emails present/missing.
- Last reminder date.
- Payment plans active.
- Gateway schedule state.
- Failed transactions.
- Discounts applied after plan creation.
- Event date proximity.
- Staff owner.

Return a prioritized collection list.

### Recipe: Audit Discount Codes

Inspect:

- Template discount configuration.
- Active and scheduled codes.
- Usage counts.
- Applies-to scope.
- Current instances using the template.
- Staff visibility requirements.
- v19.1 discount column behavior.

Return codes only to authorized staff.

### Recipe: Audit Wait List

Inspect:

- Capacity.
- Wait-list enabled setting.
- Wait-listed registrants.
- Required wait-list fields.
- First/Last name visibility in v19.1.
- Payment requirements.
- Promotion process.
- Communication sent to wait-listed people.

Return who is waiting, what data is missing, and what staff action is needed.

### Recipe: Build A Registrant Packet Export

Use the [Single Page Registrant Info](https://community.rockrms.com/recipes/313) recipe only as a concept reference. Build a reviewed report that:

- Filters by RegistrationInstanceId.
- Excludes wait-listed registrants unless requested.
- Joins registrant to person through PersonAlias.
- Pulls only needed attributes.
- Avoids exposing sensitive data broadly.
- Sorts predictably.
- Supports printing/page breaks if needed.
- Uses safe parameter handling.

### Recipe: Add Staff Notes To Registration Detail

Use the [Registration Notes](https://community.rockrms.com/recipes/245) recipe as a pattern:

- Create a Note Type.
- Add a Notes block to the appropriate internal registration detail page.
- Scope note permissions.
- Decide whether notes attach to registration, registrant, or another entity.
- Test retention when registrants are removed or changed.
- Train staff on note standards.

### Recipe: Investigate API Registration URL Issues

Do not assume expanded Linkages contain a complete public URL. Inspect:

- EventItemOccurrence.
- Linkage record.
- RegistrationInstanceId.
- Slug/public name fields.
- Page route.
- Registration Entry block.
- Mobile Registration URL setting.
- Custom Lava.
- Current API response shape.

Use the [API Q&A](https://community.rockrms.com/ask/developing/2547) as evidence that this is a known integration question, not as an answered recipe.
























<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `64`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | operational_guidance | The Wait Lists RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/wait-lists) |
| rocku-confirmed | operational_guidance | The Calendars and Events RockU lesson provides training context for source context; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/calendars-and-events) |
| rocku-confirmed | operational_guidance | The Additional Registration Fees RockU lesson provides training context for source context; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/additional-registration-fees) |
| rocku-confirmed | operational_guidance | The Group Placements [Legacy] RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/group-placement-in-event-registration) |
| rocku-confirmed | operational_guidance | For Rock operations and administration, Registration Discounts should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/registration-discounts) |
| rocku-confirmed | operational_guidance | For reporting, analytics, and measurement, Registration Instances should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/registration-instances) |
| rocku-confirmed | operational_guidance | For ministry process design, Family Pre-Registration should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/cms/family-pre-registration) |
| rocku-confirmed | operational_guidance | For staff training and operational readiness, iCalendar Feed should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/icalendar-feed) |
| rocku-confirmed | operational_guidance | For ministry process design, Registration Structure should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/registration-structure) |
| rocku-confirmed | operational_guidance | The Registration Structure RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/registration-structure) |
| rocku-confirmed | operational_guidance | The Registration Walk-through RockU lesson provides training context for ministry process design; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/registration-walk-through) |
| rocku-confirmed | operational_guidance | The Registration Fees RockU lesson provides training context for source context; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/registration-fees) |
| More |  | 52 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->











































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `23`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Additional Registration Fees Transcript Insight](https://community.rockrms.com/rocku/event-registration/additional-registration-fees) | approved_for_public_distillation | 1 | media-insight:6600e5869dac2651 |
| [Calendar Overview Transcript Insight](https://community.rockrms.com/rocku/event-registration/calendar-overview) | approved_for_public_distillation | 1 | media-insight:b7cb6e0f0354451c |
| [Calendars and Events Transcript Insight](https://community.rockrms.com/rocku/event-registration/calendars-and-events) | approved_for_public_distillation | 1 | media-insight:45d14ff6240ffaca |
| [Electronic Signatures Transcript Insight](https://community.rockrms.com/rocku/event-registration/electronic-signatures) | approved_for_public_distillation | 2 | media-insight:7ededa8a19f050ad |
| [Episode 111: Special Edition with Tim Dear Transcript Insight](https://shows.acast.com/rock-cast/episodes/podcast-episode-111-special-edition-with-tim-dear) | approved_for_public_distillation | 3 | media-insight:05f4fce834300a65 |
| [Episode 37: Special Edition Garrett Johnson Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-37-special-edition-garrett-johnson) | approved_for_public_distillation | 3 | media-insight:97a12ee26ba9575f |
| [Event Attributes Transcript Insight](https://community.rockrms.com/rocku/event-registration/event-attributes) | approved_for_public_distillation | 1 | media-insight:9799f4791807924b |
| [Event Registration Attributes Transcript Insight](https://community.rockrms.com/rocku/event-registration/event-registration-attributes) | approved_for_public_distillation | 1 | media-insight:0936a5104d35e615 |
| More |  | 15 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->
























## 18. Source Map And Dependency Notes

Primary authority:

- [Event & Calendar Guide](https://community.rockrms.com/documentation/bookcontent/29): official guide for event registration concepts, instance settings, payment plans, matching, group placement, SSL, URL slugs, events, and calendars.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): authoritative source for v18.3 and v19.1 event registration behavior changes and fixes.
- [RockU Event Registration](https://community.rockrms.com/rocku/event-registration): training map for registration walk-through, structure, templates, instances, attributes, fees, discounts, partial payments, wait lists, calendar linkages, electronic signatures, payment plans, and group placement.

Training topic citations:

- [Registration Walk-through](https://community.rockrms.com/rocku/event-registration/registration-walk-through)
- [Registration Structure](https://community.rockrms.com/rocku/event-registration/registration-structure)
- [Registration Templates](https://community.rockrms.com/rocku/event-registration/registration-templates)
- [Registration Instances](https://community.rockrms.com/rocku/event-registration/registration-instances)
- [Event Registration Attributes](https://community.rockrms.com/rocku/event-registration/event-registration-attributes)
- [Registration Fees](https://community.rockrms.com/rocku/event-registration/registration-fees)
- [Additional Registration Fees](https://community.rockrms.com/rocku/event-registration/additional-registration-fees)
- [Registration Discounts](https://community.rockrms.com/rocku/event-registration/registration-discounts)
- [Partial Payments](https://community.rockrms.com/rocku/event-registration/partial-payments)
- [Wait Lists](https://community.rockrms.com/rocku/event-registration/wait-lists)
- [Electronic Signatures](https://community.rockrms.com/rocku/event-registration/electronic-signatures)
- [Payment Plans](https://community.rockrms.com/rocku/event-registration/payment-plans)
- [Group Placement](https://community.rockrms.com/rocku/event-registration/group-placement)

Developer/source landmarks:

- [Calendar Event Item Occurrence View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-item-occurrence-view): mobile block page parameter, registration URL setting, merge fields, and registration status labels.
- [AI Agents Skills](https://community.rockrms.com/developer/ai-agents/skills): agent skill concept using Event Registration as an example domain.
- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock): source repository.
- [RegistrationInstanceRegistrantList.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx.cs): internal registrant list block attributes and page links.
- [RegistrationInstanceRegistrantList.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/RegistrationInstanceRegistrantList.ascx): internal registrant list filters and grid shape.
- [RegistrantInfoBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceRegistrationList/RegistrantInfoBag.cs): registrant grid display name and wait-list indicator.
- [RegistrationBalanceBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationBalanceBag.cs): outstanding balance row fields.
- [RegistrationInstanceSendPaymentReminderInitializationBox.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/RegistrationInstanceSendPaymentReminderInitializationBox.cs): payment reminder initialization data.
- [sendPaymentRemindersRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersRequestBag.d.ts): payment reminder send request shape.
- [sendPaymentRemindersResponseBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationInstanceSendPaymentReminder/sendPaymentRemindersResponseBag.d.ts): payment reminder send response and skipped-email behavior.

Community examples, use with review:

- [Registration Instance Totals Report](https://community.rockrms.com/recipes/348): organizer totals for paid, due, and discounted amounts.
- [Registration Instance Fees Report](https://community.rockrms.com/recipes/400): fee totals by option/quantity.
- [Single Page Registrant Info](https://community.rockrms.com/recipes/313): registrant packet/reporting pattern.
- [Show Active Registration Discount Codes](https://community.rockrms.com/recipes/472): read-only discount visibility pattern for limited staff permissions.
- [Registration Notes](https://community.rockrms.com/recipes/245): notes block pattern for registration detail pages.
- [Registration Change Tool](https://community.rockrms.com/recipes/518/registration-change-tool): custom workflow/page pattern for controlled registration changes.
- [Control the Title on The Event Registration Page](https://community.rockrms.com/recipes/361): cautionary unpublished recipe with SQL injection risk.
- [API registration URL Q&A](https://community.rockrms.com/ask/developing/2547): unresolved example of API consumers needing to trace event occurrence linkage to public registration URL.

Dependency notes:

- Event Registration depends on Events for public discovery and occurrence linkage.
- It depends on Finance for payment, discounts, batches, matching, gateways, refunds, and payment plans.
- It depends on Communications for confirmations and reminders.
- It depends on Groups for placement and rosters.
- It depends on Workflows for custom review, change, scholarship, notification, and exception processes.
- It depends on live Rock version because recent releases materially changed eligibility, duplicate prevention, wait-list field handling, signature document display, and discount-code grid behavior.
