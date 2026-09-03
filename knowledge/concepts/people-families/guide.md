---
id: authored-people-families
title: People And Families
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "adf640f08dc72002045c683af1ed25a9d5a025ede13f916619d85274cf751938"
---

# People And Families

## Agent Summary

Treat a people-record task as a data-model, security, and downstream-process task—not merely an edit to a screen.

1. Resolve the exact person before creating or changing anything. Search for existing records and possible duplicates first.
2. Identify the owning entity and field: person, family, family membership, known relationship, note, attribute, connection request, or another related record.
3. Identify the exact Person Profile tab, block, badge, note type, attribute, or action involved. Seeing the profile does not imply permission to edit every surface.
4. Establish the source of truth, record owner, duplicate risk, and reporting impact before correcting data.
5. Keep cleanup, merge, verification, and governance distinct because their permissions and audit requirements differ.
6. Verify the installed Rock version, local block configuration, security, workflows, and downstream reports before relying on version-specific or organization-specific behavior.

Rock v19 documentation establishes that every person belongs to at least one Family group and may belong to more than one. Adding a person therefore begins by creating or selecting a family. [Intro to People](https://community.rockrms.com/documentation/church-management/people/overview/intro-to-people?Version=v19.0)

## Scope And Boundaries

This guide owns:

- Person records and their profile surfaces.
- Families, family membership, primary-family context, addresses, and blended-family patterns.
- Known relationships as they affect person and family modeling.
- Person and family attributes.
- Person notes and note-type governance.
- Duplicate prevention, merge preparation, inactivation, and data-integrity workflows.
- People-facing portions of preregistration, connections, personalization, and family analytics.

Related concepts retain ownership of their deeper configuration:

- **Groups:** group types, group membership, scheduling, and attendance.
- **Security:** page, block, entity, action, field, role, and account-protection authorization.
- **Communications:** consent, delivery, templates, and provider behavior.
- **Check-in:** eligibility, schedules, locations, labels, and check-in security.
- **Workflows and Connections:** workflow design and connection-process automation.
- **Reporting:** Data View and report design.

The Person Profile exposes information from many of these domains, but it is not a single security or data boundary. Agents should first name the exact tab, block, action, and record type involved. [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile)

## Mental Model

Use this model when decomposing a request:

- **Person:** the individual’s core record, bio, contact information, statuses, and person-scoped attributes.
- **Family:** a Family group containing people in roles such as Adult or Child. A person always belongs to at least one family and may belong to several.
- **Family membership:** the link between a person and a family, including the person’s role in that family.
- **Primary family:** one family is primary behind the scenes; on the Person Profile, the family at the top of the list is treated as primary.
- **Address:** family-scoped rather than person-scoped in the documented v19 model.
- **Known relationship:** a relationship between people stored through the Known Relationship group type. It is separate from family membership.
- **Attribute:** extensible data attached to the correct entity—often a person, family, or group member.
- **Note:** structured context governed by a Note Type, entity context, visibility, sensitivity, and lifecycle.
- **Connection request:** both person context and ministry-process state.
- **Person Alias:** the supplied Model Map evidence identifies Person Alias as a CRM model, but the pack does not establish enough alias lifecycle semantics for prescriptive merge or repair instructions. [Person Alias Model Map](https://community.rockrms.com/ModelMap)

The core modeling rule is to modify the narrowest correct entity. Do not store family-wide information on one adult merely because that person is convenient, and do not use an attribute when a family membership, known relationship, group membership, note, or process record owns the meaning more accurately. [Manage Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes?Version=v19.0) [Configure Family Attributes](https://community.rockrms.com/documentation/church-management/people/families/configure-family-attributes?Version=v19.0)

## Person Model And Record Lifecycle

### Creating and locating people

Rock v19 does not present person creation as an isolated “Add Person” operation. Because people are family members, staff begin at `People > New Family`, creating a family or adding the person to the appropriate existing family. Before adding a family, the official guidance says to search the database even when the person appears to be new. Existing people should be attached after the new family is saved rather than recreated through the new-person fields. [Add a Person](https://community.rockrms.com/documentation/church-management/people/people-basics/add-a-person?Version=v19.0) [Add a Family](https://community.rockrms.com/documentation/church-management/people/families/add-a-family?Version=v19.0)

The Family Entry block can present possible duplicate records. That warning may be absent when no duplicate is detected or when an existing record’s Account Protection Profile causes duplicate checking to be skipped under the applicable security settings. A missing warning is therefore not proof that no matching person exists. [Add a Family](https://community.rockrms.com/documentation/church-management/people/families/add-a-family?Version=v19.0)

### Editing, inactivating, and preserving history

Core bio and contact fields are edited from the Person Profile. When a person is marked inactive, Rock asks for an inactive reason and note so later reviewers can understand the change. A protected profile can also display a caution based on the person’s Account Protection Profile; visibility of that warning is controlled through block security. [Edit a Person](https://community.rockrms.com/documentation/church-management/people/people-basics/edit-a-person?Version=v19.0)

The v19 documentation says people are not deleted because their historical giving and attendance records must remain accurate. Common alternatives are:

- Inactivate a person who is no longer participating.
- Merge a duplicate into the surviving record.
- Keep test data out of production; if it already exists, inactivate or merge it according to local policy.

Custom reports must deliberately handle inactive records rather than assuming Rock will exclude them from every query. [Delete a Person](https://community.rockrms.com/documentation/church-management/people/people-basics/delete-a-person?Version=v19.0)

### Derived person data

In v19 documentation, Rock calculates age from birthdate and derives age classification when a person is saved and when the Rock Cleanup job runs. Grade is calculated from graduation year and the configured Grade Transition Date. Because these values are derived, troubleshoot their inputs and the responsible job or global configuration before overwriting symptoms elsewhere. [Intro to People](https://community.rockrms.com/documentation/church-management/people/overview/intro-to-people?Version=v19.0)

Search Keys can hold alternate or outdated email addresses used when Rock searches for matching people, but the documentation states those alternate addresses are not used for communications. Alternate identifiers are person-level values that can support check-in lookup; the supplied v19 excerpt also says a nightly process assigns an alternate identifier to people who lack one. Treat communication addresses, search keys, and alternate identifiers as different surfaces. [Edit a Person](https://community.rockrms.com/documentation/church-management/people/people-basics/edit-a-person?Version=v19.0)

## Person Profile And Access Boundaries

The Person Profile is a dense operational surface. Its documented areas include the Person Bio, Badge Bar, Family section, and a tab bar whose visible tabs depend on security. Those tabs can expose notes, attributes, groups, documents, financial information, security information, history, and other domain records. [Intro to the Person Profile](https://community.rockrms.com/documentation/church-management/people/person-profile-page/intro-to-the-person-profile?Version=v19.0)

For every profile issue, identify:

- The person and expected actor.
- The exact page and tab.
- The block and action: view, add, edit, delete, download, launch, or export.
- The underlying entity or field.
- Whether the display is a summary, badge, label, attribute, note, or source record.
- The actor’s page, block, entity, action, and field-level authorization.

Profile visibility does not imply edit permission. For example, the Contributions tab can show giving information while creating or editing giving still requires Edit access to the relevant giving blocks. Badges can also appear without lighting correctly if a custom role lacks access to the badges REST controller or to the data used by the badge. [Contributions Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/contributions-tab?Version=v19.0) [Use Badges](https://community.rockrms.com/documentation/church-management/people/person-profile-page/use-badges?Version=v19.0)

The History tab can show communication, attendance, person-change, assessment, and login history. Person History includes changes such as Connection Request and Step updates and can help identify what changed and who changed it. It is supporting evidence, not automatic proof that the current value is correct. [History Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/history-tab?Version=v19.0)

### Tags, signals, and badges

Use these profile indicators according to their documented purposes:

- **Tags** categorize people or other entities. Personal tags are normally visible only to their creator and administrators; organizational tags are broadly shared but can be secured.
- **Signals** are action-oriented flags with a type, owner, expiration date, and note. Their type security and Security-tab access both matter.
- **Badges and labels** summarize underlying data. They do not replace inspection of the underlying record.

Signal names should avoid unnecessarily labeling people, and signal security is essential because the underlying information may be sensitive. [Use Tags](https://community.rockrms.com/documentation/church-management/people/person-profile-page/use-tags?Version=v19.0) [Use Person Signal Types](https://community.rockrms.com/documentation/church-management/people/person-profile-page/use-person-signal-types?Version=v19.0) [Use Badges](https://community.rockrms.com/documentation/church-management/people/person-profile-page/use-badges?Version=v19.0)

## Families, Membership, And Relationships

### Family structure

A Family is a group containing people in family roles. The family holds shared data such as address and campus, while family membership connects each person to the household. A person may belong to multiple families but remains one person record. [Intro to Families](https://community.rockrms.com/documentation/church-management/people/families/intro-to-families?Version=v19.0)

The Family Edit surface supports:

- Family-level name, campus, and record status.
- Adding an existing or new person.
- Changing Adult or Child roles.
- Moving a person to a new family.
- Removing one of a person’s multiple family memberships.
- Maintaining current and prior addresses.

Inactivating a family also inactivates its members and their memberships in other groups according to the supplied v19 documentation, so this is a broad operation that requires impact review. Changes on the Family Edit screen, including staged member moves, are not saved until the page’s Save action completes. [Edit a Family](https://community.rockrms.com/documentation/church-management/people/families/edit-a-family?Version=v19.0)

### Addresses and moves

Addresses are attached to families. When a household moves, the documented workflow is to use the Family Moved action so the former home address becomes a previous address and a new home address is created. Simply overwriting the old address removes useful transition context and can make later submissions appear to reverse the correction. [Edit a Family](https://community.rockrms.com/documentation/church-management/people/families/edit-a-family?Version=v19.0)

A family can have several address types, but one address is marked as the map location. That flag identifies the address selected for mapping; it does not guarantee successful geocoding. [Edit a Family](https://community.rockrms.com/documentation/church-management/people/families/edit-a-family?Version=v19.0)

### Blended families and multiple-family membership

The v19 documentation presents two patterns rather than one universal blended-family structure:

- **Dual-family approach:** one child record belongs to multiple families. Family-based reports may return both families, mail may go to both home addresses, and either family’s contact information may be usable for check-in.
- **Single-family plus relationships:** the child belongs to one family while known relationships connect other adults. This may fit sole-custody or non-participating-household situations, and a relationship such as Can Check-in can support check-in access.

Choose the structure from the real household, custody, communication, reporting, and check-in requirements. Do not duplicate the child to make both households visible. [Blended Families](https://community.rockrms.com/documentation/church-management/people/families/blended-families?Version=v19.0)

### Known relationships

Known relationships model links such as parent, child, grandparent, or invited-by separately from family membership. Rock stores them through the Known Relationship group type. Relationship roles can have inverse roles, and a configured inverse can be created automatically when the relationship is added. A relationship type can also be configured to allow one person to check in another. [Use Known Relationships](https://community.rockrms.com/documentation/church-management/people/person-profile-page/use-known-relationships?Version=v19.0)

Do not assume that family membership, a known relationship, and check-in authorization are interchangeable. Inspect the specific family membership and relationship configuration used by the affected check-in path.

## Person And Family Attributes

### Choosing the correct entity

Use a person attribute for a characteristic of an individual. Before creating one, determine:

1. Whether a standard person field or existing attribute already represents the information.
2. Whether the value actually belongs to a group membership.
3. Whether collecting it serves a defined operational purpose.
4. Whether an owner can keep it accurate.

The official documentation warns that inaccurate attribute data may be worse than not collecting it. [Manage Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes?Version=v19.0)

Use a family attribute when the value describes the household rather than one adult. In v19, family attributes are configured as Group Attributes on the Family group type and displayed through the Family Members block. Attributes marked Show in Grid are always displayed there; other configured family attributes can be opened from the family bar. The supplied v19 documentation says attribute categories are not supported for family attributes. [Configure Family Attributes](https://community.rockrms.com/documentation/church-management/people/families/configure-family-attributes?Version=v19.0)

### Configuration and security

Person attributes include a name, categories, stable key, required setting, field type, and field-type-specific settings. One attribute may belong to multiple categories while retaining one value. Person attributes can be secured separately for viewing and editing; the supplied v19 documentation states that the default is All Users for viewing and Administrators for editing, which should be reviewed before sensitive data is introduced. [Manage Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes?Version=v19.0)

An Attribute Values block can display a selected category of person attributes on any Person Profile tab. Therefore, an attribute that appears missing may be absent from the block’s selected category, hidden by security, or placed on another tab rather than lacking a stored value. [Display Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes?Version=v19.0)

### Public self-service attributes

The documented Person Attribute Forms block lets a logged-in person update selected person attributes on an external site. Its configuration can include multiple forms, progress display, per-page or final saving, current-value display, field requiredness, a completion workflow, and a done page. If Use Current Value is disabled and the person submits no replacement, the documented behavior warns that the existing value can be replaced with a blank. [Person Public Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/person-public-attributes?Version=v19.0)

Immutable source at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` independently shows configuration fields for save timing, workflow, done page, selected person attribute, current-value display, and requiredness. This is implementation evidence from that commit, not proof that a given installation uses that block or configuration. [PersonAttributeForms source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Crm/PersonAttributeForms.ascx.cs)

A workflow action at the same immutable commit can update a selected person attribute for a person supplied through a workflow attribute. Before using such automation, verify the target person, attribute key, field type, value format, workflow authorization, and local version. [SetPersonAttribute source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Workflow/Action/People/SetPersonAttribute.cs)

## Person Notes And Note-Type Governance

Person Notes are structured staff context, not one undifferentiated memo field. The approved claims require agents to consider the note’s type, entity context, visibility, sensitivity, author/date metadata, lifecycle, and downstream workflow or report consumers. [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1)

Use Note Types to govern categorization, where notes appear, and which staff roles can create or view sensitive notes. Auditing only the text can miss the controlling configuration or the fact that two similarly named notes target different entities. [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types)

A note investigation should distinguish:

- The profile page and block where the note is expected.
- The Note Type.
- The note’s target entity.
- View and edit authorization.
- Author and date metadata.
- Sensitivity and intended retention or lifecycle.
- Reports or workflows that consume the note.

The evidence pack includes reviewed public-safe conclusions from a prior bounded read-only probe confirming that Note, NoteType, Auth, Workflow, and Report surfaces existed in the reviewed instance. That verification supports the inspection model but does not establish another installation’s note types, permissions, or retention policy.

## Data Integrity, Duplicates, And Merge Preparation

Data-integrity work should begin with the exact entity and field being corrected. Then identify the owner, authoritative source, duplicate risk, correction rule, known examples, and downstream reporting impact. Cleanup, merge, verification, and governance should remain distinct tasks because each has different permissions and audit consequences. [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity)

A repeatable cleanup workflow is:

1. Define the affected population without changing it.
2. State the correction rule in testable terms.
3. Identify the owner and source of truth.
4. Test known positive and negative examples.
5. Inspect aliases, attributes, family memberships, reports, Data Views, workflows, and communications that may be affected.
6. Obtain the authorization required for the specific correction or merge.
7. Change a bounded set.
8. Re-run the same verification and compare results.

The approved repeatability claim still requires live verification before bulk changes. Do not turn it into permission to update records.

Reporting logic should expose source-data defects such as duplicates, missing values, or stale attributes rather than silently masking them. A cleaner report result does not prove the source record is correct. [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1)

### Rock v19 merge evidence

Official v19 feature evidence in the pack adds these scoped behaviors:

- The merge interface can show last-modified time and actor information. Recency is a comparison signal, not proof that the newer record is correct.
- A requester without merge permission can ask for notification after an authorized reviewer completes the merge, separating submission from authorization.
- If the surviving last name changes, Rock can add the former value to Previous Last Names. Verify that field’s local visibility and data-handling policy.
- External person-entry blocks can assign record sources, and duplicate detail can show that source to help trace repeated-record origins.

These statements are scoped to Rock v19 evidence and require local applicability checks. [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=790s)

## Family Preregistration And Follow-Up

The documented Family Pre-Registration page lets visitors create person and family records before arrival. Its block settings control adult and child questions, requiredness, attribute categories, SMS opt-in presentation, campus, planned visit date, and optional workflows. The submitted address is applied to the entered household as a Home address. [Pre-Register a Family](https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family?Version=v19.0)

The block can launch:

- Workflows associated with the primary family group.
- A parent workflow once for each parent, with that Person as the entity.
- A child workflow once for each child, with that Person as the entity.

For the family-level workflow, documented workflow attributes with keys `ParentIds`, `ChildIds`, or `PlannedVisitDate` can be populated automatically when configured. Verify these keys, entity types, and local workflow definitions before relying on them. [Pre-Register a Family](https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family?Version=v19.0)

Reviewed community evidence recommends validating the complete path from public form through family creation, check-in eligibility, and staff follow-up. It also recommends explaining the value to families and avoiding duplicate or partial records that staff must later repair. These are community-reviewed operational patterns, not universal proof that a local preregistration path is configured correctly. [Community preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

Two additional community patterns are relevant but require local review:

- A registrant workflow can resolve the person and campus, create a native Connection Request, preserve a source registration identifier, and copy reviewed attributes. [Registration-to-Connection Request recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)
- An anonymous form can use a bounded workflow-backed SMS challenge after one exact person match, without exposing the matched alias to the browser. [Workflow-Backed SMS Verification recipe](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification)

Neither recipe is official Rock behavior, and both need security, configuration, and end-to-end verification before use.

## Connections As Person-Centered Process State

A connection request should be inspected as both person context and ministry-process state. Define the person, connection type, opportunity, connector or staff owner, status, activities, next action, and related automation before changing or reporting on the flow. [Connections Overview](https://community.rockrms.com/rocku/engagement/overview)

When a connection appears wrong or stuck, separate these causes:

- The request points to the wrong or duplicate person.
- The request has the wrong status.
- The opportunity or connection type is misconfigured.
- The connector or staff assignment is absent or incorrect.
- An activity or next action was not completed.
- A workflow or other automation did not run as intended.

Do not collapse all of these into a generic “workflow issue.” [Connections Overview](https://community.rockrms.com/rocku/engagement/connections-overview)

## Personalization And Person Data

Personalization is conditional content delivery, not authorization. A targeted or hidden content variant still needs appropriate page, block, and entity security. [Personalization](https://community.rockrms.com/rocku/cms/personalization)

When person-based personalization behaves unexpectedly, inspect:

1. The audience rule.
2. The exact person data used by that rule.
3. The expected fallback content.
4. Cache behavior.
5. Whether the test is anonymous or authenticated.
6. The exact authenticated person being tested.
7. Page, block, and entity authorization independently of audience matching.

A successful audience match does not prove access is safe, and a security denial does not prove the audience rule failed.

## Person And Family Analytics

Rock’s person and family analytics summarize engagement data and can produce predictive indicators. The official documentation explicitly warns that these tools require careful, ethical use because the conclusions can feel invasive or be misused. [Intro to Person & Family Analytics](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/intro-to-person-family-analytics?Version=v19.0)

In documented v19 behavior, eRA—Estimated Regular Attender—uses giving and attendance criteria. The status is estimated rather than definitive, and workflows or communications responding to it should avoid claiming certainty about a person’s attendance or disengagement. [Use eRA](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/use-era?Version=v19.0)

The Family Analytics job:

- Is available out of the box but is not enabled automatically.
- Must be scheduled to run regularly for the related measures.
- Can launch workflows when a family enters or exits eRA.
- Can calculate visit-date attributes under documented constraints involving record creation time and check-in data.

Its results therefore depend on job enablement, schedule, source attendance and giving data, family structure, and the Group Types whose attendance is configured as Weekend Service. [Calculate Analytics](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/calculate-analytics?Version=v19.0)

## Version And Authority Caveats

- Most official documentation excerpts in this pack are scoped to Rock v19.0. Confirm the installed version and block generation before applying navigation or behavior literally.
- The v19 merge enhancements are based on official feature evidence but still require local field visibility, authorization, and configuration review. [v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=790s)
- Rock v19.5 release notes report a fix for a Family Analytics boundary-Sunday calculation issue affecting eRA and related first/last gift, first/last check-in, and count attributes. If those values appear wrong on an earlier v19 patch, verify exact version and reproduction before changing source data. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Rock v19.4 release notes report a fix for indexed Person Attribute Values missing from Universal Search after a bulk re-index. Search absence on an affected patch may therefore differ from a missing stored value. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Rock v18.2 release notes report an Attribute Editor issue involving attributes whose field type stores other attributes. Treat this as a version-specific editor defect, not a general person-attribute rule. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Rock v18.3 release notes report Giving History API corrections involving individual versus family giving and contributions associated with a person’s other records. Verify version and API parameters before treating a giving discrepancy as bad person data. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- RockU-approved operational claims in this pack have unprocessed version scope. Use them as bounded guidance, then verify version-sensitive details locally.
- Community contributions are examples. They are neither core-product guarantees nor proof of installation.
- Supplied source-code excerpts are tied to immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They show implementation at that commit, not current configuration.
- Prior read-only instance probes in the evidence pack verified that relevant tables and authorization surfaces existed in one reviewed installation. They did not verify this guide’s reader’s installation.

## Troubleshooting Decision Tree

### A person cannot be found, or a new record may be a duplicate

1. Search using current identity information.
2. Check relevant alternate or former email Search Keys, remembering that they are matching aids rather than communication destinations.
3. Inspect possible duplicate results and any record-source information available in the installed version.
4. Confirm whether Account Protection Profile behavior affected duplicate checking.
5. Inspect inactive or pending records before creating a new person.
6. If multiple records exist, stop creation and begin a merge review; do not delete one record. [Add a Family](https://community.rockrms.com/documentation/church-management/people/families/add-a-family?Version=v19.0) [Delete a Person](https://community.rockrms.com/documentation/church-management/people/people-basics/delete-a-person?Version=v19.0)

### A person is in the wrong family, campus, or household report

1. Confirm that the correct person record is open.
2. List every family membership and the role in each.
3. Identify which family is primary.
4. Compare the documented household situation with the dual-family and single-family-plus-relationship patterns.
5. Inspect each family’s campus and address.
6. Evaluate reporting, mailing, and check-in consequences before moving or removing membership.
7. Save and then verify the final family list and primary-family ordering. [Edit a Family](https://community.rockrms.com/documentation/church-management/people/families/edit-a-family?Version=v19.0) [Blended Families](https://community.rockrms.com/documentation/church-management/people/families/blended-families?Version=v19.0)

### A user can see a profile but cannot view or edit one part of it

1. Name the page, tab, block, entity, field, and requested action.
2. Confirm the exact signed-in user and security roles.
3. Test page and tab visibility.
4. Test block authorization.
5. Test entity, attribute, note-type, signal-type, document-type, or other record authorization.
6. Test action-specific authorization such as edit, download, launch, or delete.
7. Inspect account-protection behavior if a protected person is involved.
8. Stop when the missing permission is identified; do not broaden unrelated access. [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile) [Security Tab](https://community.rockrms.com/documentation/church-management/people/person-profile-page/security-tab?Version=v19.0)

### A note is missing, appears in the wrong place, or is visible too broadly

1. Confirm the target person and profile block.
2. Identify the Note Type.
3. Confirm the note’s target entity.
4. Inspect Note Type visibility and create/edit permissions.
5. Review author and date metadata.
6. Inspect workflows and reports that consume the note.
7. Compare the result using the exact affected staff role.
8. Escalate sensitive exposure according to local policy rather than copying the note into diagnostics. [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types) [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1)

### An attribute is absent, blank, stale, or unexpectedly overwritten

1. Confirm whether the value belongs to the person, family, or group membership.
2. Identify the attribute by stable key as well as display name.
3. Check categories and the Attribute Values block’s selected category.
4. Check view and edit security.
5. Check field type and field-specific settings.
6. For public forms, inspect Use Current Value, requiredness, and save timing.
7. Inspect workflows or imports that write the attribute.
8. Verify version-specific indexing or editor defects before changing data.
9. Test a known example and one unaffected record. [Manage Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes?Version=v19.0) [Person Public Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/person-public-attributes?Version=v19.0)

### Family preregistration creates partial or duplicate records

1. Test with a controlled new-family case and a controlled existing-person case.
2. Record which adult, child, address, contact, and attribute fields are required.
3. Verify the duplicate-matching result before saving.
4. Confirm the family and person records created.
5. Confirm family roles, address, campus, and check-in eligibility.
6. Confirm the expected family, parent, and child workflows and their entity types.
7. Confirm staff follow-up or connection creation.
8. Stop broad launch if any path creates ambiguous, duplicate, or incomplete records. [Pre-Register a Family](https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family?Version=v19.0) [Community preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

### A connection request is missing or stuck

1. Resolve the person and check for duplicates.
2. Confirm the Connection Type and Opportunity.
3. Confirm current request status.
4. Inspect assigned connector or staff owner.
5. Review activities and the next expected action.
6. Inspect related workflow state and automation.
7. Confirm whether a registration-to-connection transfer was expected.
8. Report the fault in the correct category rather than as a generic workflow failure. [Connections Overview](https://community.rockrms.com/rocku/engagement/connections-overview)

### Personalized content appears for the wrong person or not at all

1. Identify the expected audience rule.
2. Inspect the exact person data referenced by the rule.
3. Confirm the test person and authenticated or anonymous state.
4. Check fallback content.
5. Test cache behavior.
6. Test page, block, and entity authorization independently.
7. Stop if targeting is being used to conceal content that lacks proper authorization. [Personalization](https://community.rockrms.com/rocku/cms/personalization)

### Family analytics or eRA values appear stale or wrong

1. Confirm the exact Rock version and relevant release fixes.
2. Confirm the Family Analytics job is enabled.
3. Review its schedule and latest execution status.
4. Inspect the person’s family structure and active status.
5. Inspect source giving and attendance data.
6. Confirm which Group Types count as Weekend Service.
7. Check calculation-window boundary cases.
8. Re-run only through the authorized job workflow and verify resulting values and history.
9. Treat eRA as an estimate even after calculation succeeds. [Calculate Analytics](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/calculate-analytics?Version=v19.0) [Use eRA](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/use-era?Version=v19.0)

## Agent Task Recipes

### Recipe: Add a person or family without creating a duplicate

**Outcome:** The correct person records are attached to the correct family with no avoidable duplicate.

1. Search for every adult and child using available current and alternate identity information.
2. Separate people already in Rock from genuinely new people.
3. Create the family through `People > New Family`.
4. Enter only people who are not already present.
5. Review possible duplicate warnings.
6. Save the family.
7. Edit the saved family to attach existing people.
8. Verify roles, campus, address, marital-status handling, and final family membership.

**Inspect:**

- Pending and inactive people.
- Search Keys and possible duplicates.
- Account Protection Profile behavior.
- Existing family memberships.

**Do not assume:**

- A missing duplicate warning proves uniqueness.
- Two households require two person records.
- Similar names alone prove a match.

**Stop when:**

- Identity remains ambiguous.
- A protected record requires an authorized reviewer.
- Family structure cannot be established safely.

Source: [Add a Family](https://community.rockrms.com/documentation/church-management/people/families/add-a-family?Version=v19.0)

### Recipe: Correct a family structure or household move

**Outcome:** Family membership, primary-family context, address history, and downstream behavior reflect the reviewed household reality.

1. Document the current memberships, roles, primary family, campuses, and addresses.
2. Confirm the intended household structure with the responsible data owner.
3. Choose dual-family membership or family-plus-known-relationship based on custody, participation, reporting, mailing, and check-in needs.
4. Move, add, or remove membership only after reviewing downstream effects.
5. Use Family Moved for an address transition.
6. Save the Family Edit page.
7. Reopen the profile and verify every affected family.
8. Test relevant reporting, mailing, and check-in behavior.

**Do not assume:**

- The first visible family is the only family.
- A known relationship replaces family membership.
- An address overwrite preserves move history.
- An unsaved member move has taken effect.

Source: [Edit a Family](https://community.rockrms.com/documentation/church-management/people/families/edit-a-family?Version=v19.0) [Blended Families](https://community.rockrms.com/documentation/church-management/people/families/blended-families?Version=v19.0)

### Recipe: Design or review a person or family attribute

**Outcome:** The attribute has a clear owner, correct entity, maintainable value, appropriate display, and bounded security.

1. Define the operational question the value must answer.
2. Search for a standard field or existing attribute.
3. Select the correct entity: person, family, or group membership.
4. Define the owner and update lifecycle.
5. Choose the field type and allowed values.
6. Choose a stable key and appropriate categories.
7. Configure requiredness only where every relevant editing path can supply the value.
8. Configure view and edit security.
9. Place the attribute in the required internal or external block.
10. Test creation, display, editing, blank submission, workflow updates, reporting, and search behavior.

**Inspect:**

- Current-value behavior on public forms.
- Category and block configuration.
- Version-specific editor or indexing issues.
- Sensitive-data exposure.

**Stop when:**

- No owner can maintain the value.
- The value belongs to another entity.
- Requiredness would block a valid family-member path.

Source: [Manage Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes?Version=v19.0) [Configure Family Attributes](https://community.rockrms.com/documentation/church-management/people/families/configure-family-attributes?Version=v19.0)

### Recipe: Audit Person Note governance

**Outcome:** Notes are categorized, visible, and consumed according to documented staff purpose and authorization.

1. Inventory the relevant Note Types without exporting note bodies.
2. Identify each Note Type’s target entity and profile location.
3. Review who can view, create, edit, and administer the type.
4. Identify sensitive categories and their intended lifecycle.
5. Review author/date metadata expectations.
6. Identify reports and workflows that consume the notes.
7. Test representative authorized and unauthorized roles.
8. Record configuration findings without reproducing sensitive content.

**Stop when:**

- A note is exposed beyond its intended audience.
- The Note Type’s owner or retention policy is unknown.
- Remediation requires broader security changes than authorized.

Source: [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types)

### Recipe: Prepare a duplicate-person merge for authorized review

**Outcome:** A reviewer receives a bounded comparison and can merge without relying on recency alone.

1. Confirm that the records represent the same person.
2. Compare core identity, contact information, statuses, family memberships, attributes, notes, accounts, and history.
3. Inspect aliases and record-source information where available.
4. Compare last-modified time and actor data in supported v19 interfaces.
5. Identify the intended surviving values field by field.
6. Document downstream reporting and process impact.
7. Route the request to an authorized merger.
8. If supported, request completion notification.
9. After the merge, verify the surviving profile, family links, Previous Last Names behavior, and downstream reports.

**Do not assume:**

- The newest record is correct.
- The most complete record should survive unchanged.
- Merge permission follows from permission to submit a request.
- Former-name visibility matches local policy.

Source: [v19 merge feature evidence](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=845s)

### Recipe: Validate family preregistration end to end

**Outcome:** A visitor can preregister without producing preventable duplicates, and the resulting people data leads to check-in and staff action.

1. Review the public explanation and requested fields.
2. Review adult and child requiredness separately.
3. Review SMS opt-in, attributes, campus, visit date, and address handling.
4. Test one new family.
5. Test one existing-person match.
6. Verify people, family memberships, roles, address, and campus.
7. Verify check-in eligibility through the intended path.
8. Verify family, parent, and child workflows with the expected entities.
9. Verify staff follow-up or connection creation.
10. Review resulting duplicates, partial records, and failed workflow cases before launch.

**Stop when:**

- Existing people are recreated.
- Children or adults cannot complete a valid path because unrelated contact fields are required.
- Workflow entity or attribute assumptions are unverified.
- Follow-up has no owner.

Source: [Pre-Register a Family](https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family?Version=v19.0)

### Recipe: Diagnose a connection request from the person record

**Outcome:** The failure is classified as person context, request state, opportunity configuration, assignment, activity, or automation.

1. Open the exact person and check for duplicates.
2. Locate the exact Connection Request.
3. Record its type, opportunity, status, connector, activities, and next action.
4. Compare those values with the intended ministry process.
5. Inspect linked workflow or registration automation.
6. Identify the first state that differs from expectation.
7. Route remediation to the owner of that state.
8. Recheck the person profile and connection detail after correction.

**Do not assume:**

- A visible person record proves the request exists.
- A request-status issue is a workflow-engine failure.
- A created request has an assigned follow-up owner.

Source: [Connections Overview](https://community.rockrms.com/rocku/engagement/overview)

### Recipe: Run a bounded people-data cleanup

**Outcome:** A defined population is corrected by a testable rule with before-and-after evidence.

1. Identify the exact entity and field.
2. Define the affected population.
3. Name the data owner and source of truth.
4. Define positive, negative, and edge-case examples.
5. Measure duplicate and reporting impact.
6. Separate verification, correction, merge, and governance work.
7. Obtain action-specific authorization.
8. Correct a small bounded sample.
9. Re-run the original population and downstream reports.
10. Expand only after the sample passes.

**Stop when:**

- The source of truth is disputed.
- The rule cannot distinguish valid exceptions.
- The required permission or audit trail is missing.
- A report-only workaround would conceal bad source data.

Source: [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1)

## Known Gaps And Live Verification

The following require a current, bounded review of the target installation:

- Installed Rock version, patch level, and whether classic or next-generation blocks are in use.
- Exact Person Alias creation, retention, and merge semantics beyond the model’s documented existence.
- Local duplicate-matching rules, Account Protection Profile behavior, and record-source configuration.
- Current page, block, entity, action, attribute, Note Type, signal, tag, document, and REST-controller authorization.
- Local family roles, relationship types, inverse relationships, and check-in permissions.
- Whether family-attribute category support differs from the supplied v19 documentation.
- Person Attribute Forms configuration, save timing, workflow, requiredness, and blank-value behavior.
- Note retention, sensitivity classification, and downstream consumers.
- The correctness of any particular preregistration, registration-to-connection, or SMS-verification implementation.
- Whether the Family Analytics job is enabled, scheduled, healthy, and running on data unaffected by version-specific defects.
- Whether personalization rules and caches produce the expected result for real authenticated and anonymous actors.
- The actual population and correction rule for any proposed bulk cleanup.

No live review of the reader’s installation occurred for this guide. The pack’s prior read-only verification established only that relevant operational surfaces existed in one connected instance; it did not prove local configuration, record correctness, workflow success, or universal behavior.

## Source Map

| Area | Authority and approved claim spine | Primary sources |
|---|---|---|
| Person Profile and access | RockU-confirmed operational and risk claims `claim:34144e7226c4a430a307`, `claim:5c53977793c7673b19e9` | [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile), [official v19 profile documentation](https://community.rockrms.com/documentation/church-management/people/person-profile-page/intro-to-the-person-profile?Version=v19.0) |
| Notes and Note Types | RockU-confirmed claims `claim:00300ae5ab574ad7c48b`, `claim:09c6a4834867ba6879d7`, `claim:c161a6f06a707e04dbea`, `claim:ced0968707b2a7a9d6a1` | [Person Note](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1), [Note Types](https://community.rockrms.com/rocku/core-concepts/note-types) |
| Data integrity | RockU-confirmed claims `claim:7e9a4bdea4ebdb5d77a4`, `claim:8ffba8d5adf492765f21`, `claim:d40bfdc2c3879d0290a3`; live-check-required claim `claim:4ccbececc1c30ce62894` | [Data Integrity](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity), [Data Integrity continuation](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| Connections | RockU-confirmed claims `claim:90c918310ef30a92a729`, `claim:970086a35aa016eccb8d`, `claim:d270bb647c2f125dcbdd`, `claim:ffa69d01f0fb1999048c` | [Connections Overview](https://community.rockrms.com/rocku/engagement/overview), [Connections Overview alternate route](https://community.rockrms.com/rocku/engagement/connections-overview) |
| Personalization | RockU-confirmed claims `claim:64100db2b5d60396b9fd`, `claim:95e015e3407ed10e9e7c` | [Personalization](https://community.rockrms.com/rocku/cms/personalization) |
| Family preregistration | Community-reviewed claims `claim:57b56ebf5bb293682e3d`, `claim:90fecb6ea51cf994ff92`, `claim:b6025804c011523e291d`, `claim:bd2faf9d63fc7ecc41c1` | [Official v19 preregistration documentation](https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family?Version=v19.0), [community example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) |
| Rock v19 merge behavior | Official approved claims `claim:23c173130e89f0eba735`, `claim:5d80cd1847429a0181d0`, `claim:b81391274ac89ca6c69f`, `claim:f39e0cab003d876835c1` | [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=790s) |
| Person and family fundamentals | Official v19 documentation | [People](https://community.rockrms.com/documentation/church-management/people?Version=v19.0), [Families](https://community.rockrms.com/documentation/church-management/people/families?Version=v19.0) |
| Attributes | Official v19 documentation and immutable implementation evidence | [Manage Person Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes?Version=v19.0), [Person Public Attributes](https://community.rockrms.com/documentation/church-management/people/person-attributes/person-public-attributes?Version=v19.0), [immutable source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Crm/PersonAttributeForms.ascx.cs) |
| Analytics | Official v19 documentation and version-scoped release notes | [Use eRA](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/use-era?Version=v19.0), [Calculate Analytics](https://community.rockrms.com/documentation/church-management/people/person-family-analytics/calculate-analytics?Version=v19.0), [release notes](https://www.rockrms.com/releasenotes) |
| Community workflow patterns | Reviewed examples requiring live verification | [Registration-to-Connection Request](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request), [Workflow-Backed SMS Verification](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/workflow-backed-sms-verification) |

Source-summary claims were used only to locate their underlying answer-bearing material and were not independently promoted into factual guidance.