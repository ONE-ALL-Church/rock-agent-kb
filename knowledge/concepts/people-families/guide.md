---
id: authored-people-families
title: People And Families
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# People And Families

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [People And Families index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

People and families are the operational center of Rock RMS. Most ministry, reporting, communication, check-in, contribution, workflow, and security work eventually resolves to one or more `Person` records, their family group membership, their aliases, their attributes, their known relationships, and the audit trail around how those records were created or changed.

For agent work, the most important rule is this: never treat the visible name on a profile as the complete identity model. A Rock person record has identity fields, contact fields, record status fields, connection status fields, family membership, one or more aliases, attributes, notes, photos, logins, communication preferences, group memberships, attendance, interactions, history, and relationship edges. The person profile is a useful surface, but the durable model lives across multiple entities and features.

The second important rule is that custom references to people should generally use `PersonAlias`, not a raw `Person.Id`. Rock's developer guidance says duplicate records happen over time and are later merged; aliases survive merges and point to the current surviving person record. Custom models that store a raw `Person.Id` can break after a merge, while `PersonAlias` references remain resolvable through `PersonAlias.PersonId` ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)). For agents diagnosing integrations, workflows, custom SQL, Lava, or plugin data, this is not a style preference. It is a data durability boundary.

The third important rule is that families in Rock are groups. A "family" is not just a denormalized field on `Person`; it is a family group with group members and roles. This means family work intersects directly with the Groups system: group type configuration, group member roles, group member status, inherited security, check-in behavior, attendance, group sync, and group requirements. Official group documentation describes Rock's group system as broad enough to represent families, security roles, check-in groups, serving teams, and general groups, with group type settings controlling behavior such as attendance, locations, schedules, requirements, check-in rules, security, and role permissions ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

The fourth important rule is that attributes are an extension mechanism, not a secondary notes field. Rock attributes can be attached to many entity types, including `Person`, `Group`, `GroupType`, workflow types, campuses, devices, and other models. Attribute definitions live separately from attribute values. The `Attribute` record defines field type, entity type, key, qualifiers, required behavior, categories, ordering, and display behavior. The `AttributeValue` record stores the value for a specific entity instance, including persisted typed columns such as numeric, date/time, boolean, and person-id representations where applicable ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)). Agents should inspect attribute definitions before interpreting an attribute value.

The fifth important rule is that many workflows use a person attribute field type, but the stored value may not be a direct person id. Rock's workflow Lava documentation notes that a workflow `Person` attribute's raw value returns a person alias GUID because that is how the person field type stores its value ([Workflows and Lava](https://community.rockrms.com/lava/workflows)). When debugging workflow forms, person entry, workflow-to-person reports, or custom Lava links, inspect the raw value and resolve it through `PersonAlias`.

The sixth important rule is that version matters. Recent Rock releases changed person/family behavior in places agents are likely to touch: record source support in person creation through Get Person From Fields, Add Family, and Check-in in v18.1; workflow Person Entry spouse fixes in v18.1; family registration giving behavior in v17.2; check-in known relationship removal in v17.5; attribute editor fixes in v18.2 and v19.1; registration eligibility rules in v19.1; and Giving History API behavior around family giving in v18.3 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Always verify the live Rock version before giving operational instructions that depend on these behaviors.

For real operational work, agents should follow this sequence:

1. Identify the record surface: person profile, family group, workflow, check-in registration, communication recipient, event registration, or custom page.
2. Resolve identity: `Person.Id`, `Person.Guid`, `PrimaryAliasId`, `PrimaryAlias.Guid`, family group id, and whether duplicate or merged aliases exist.
3. Determine family context: primary family group, group member role, household adults/children, family address, and any known relationships outside the family group.
4. Inspect attributes by definition, not just value: entity type, qualifier, key, field type, categories, security, default value, and actual `AttributeValue`.
5. Check related systems: group memberships, security roles, communication preferences, attendance/check-in history, notes, interactions, workflows, financial giving family settings, and event registrations.
6. Use live Rock inspection for ambiguous behavior: Rock instances differ by version, configuration, plugins, block settings, custom Lava, data automation jobs, and imported history.

This guide is written as an agent-first concept manual. It does not replace live inspection. It tells an agent what the model means, which source records support the claim, which surfaces to inspect, and what to verify before making changes.

## 2. Scope And Terminology

This guide covers the Rock RMS people and families model: individual person records, family groups, aliases, attributes, relationships, notes, profile surfaces, data hygiene, operational workflows, and developer-facing access patterns.

It includes:

- `Person` as the core individual CRM entity.
- `PersonAlias` as the durable reference layer for people.
- Family groups and family membership.
- Person, family, and workflow attributes.
- Known relationships and relationship-driven check-in behavior.
- Person profile surfaces, mobile profile blocks, search, and Lava access.
- Related group, security, communication, check-in, workflow, reporting, BI, and API concerns.
- Data hygiene workflows such as duplicate merge, accidental merge recovery, deactivation recovery, record source tracking, photos, and attribute cleanup.
- Release caveats from v16 through v19.1 where the provided source pack includes relevant records.

It does not attempt to define every column on every entity. The source pack includes model-map metadata for `Person Alias` but not a complete current Model Map export for every person-related entity. Where exact schema is required, inspect the live Model Map, the REST API metadata, a current Rock source checkout, or the live database schema before writing code or SQL.

Terminology used in this guide:

`Person` means the Rock entity representing an individual human profile. A person may be active, inactive, deceased, nameless, merged into another person, associated with one or more aliases, and connected to families, groups, notes, workflows, communication records, attendance, financial transactions, or security roles.

`PersonAlias` means a durable identity reference that points to a `Person`. A person can have multiple aliases. Rock developer guidance says custom models should reference `PersonAlias` rather than raw `Person.Id` because aliases survive duplicate merges ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

`PrimaryAlias` means the main alias Rock exposes for a person in many contexts. Agents should still inspect all aliases when diagnosing merge history, duplicate records, financial history, attendance, workflow links, or integration references.

`Family` means a Rock group of the family group type. Family membership is group membership. Family roles, member status, group location, group attributes, and group type behavior matter.

`PrimaryFamilyId` means the id of the person's primary family group. It is commonly used in Lava and SQL recipes for household-level views, event balances, family members, and profile customizations. Verify exact behavior and availability in the live version before building mission-critical logic.

`Known Relationship` means a relationship represented through Rock's known relationships group type and roles, not necessarily a family group membership. It is used for relational edges like who can check in a child, parent/child relationships outside a household, guardianship patterns, and other named relationships. Check-in source code and release notes show known relationships can directly affect check-in behavior ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

`Attribute` means a configurable field definition attached to an entity type, sometimes scoped by qualifier columns and values.

`AttributeValue` means the stored value for one entity instance and one attribute definition. The value is stored as text plus typed helper columns where applicable ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)).

`Defined Type` and `Defined Value` mean configurable controlled vocabularies used throughout Rock. Connection Status, Record Status, Record Type, Phone Type, and many custom classification lists are represented this way.

`Connection Status` means a defined value describing a person's ministry relationship or engagement stage. It is not the same as record status. Community examples use connection status as a temporary signal for how records were created, but that is a local pattern and must be verified before assuming it exists ([Track How Person Records are Created](https://community.rockrms.com/recipes/223)).

`Record Status` means whether a person record is active, inactive, or otherwise operationally available. Release notes include a CRM fix around family record status editing and deceased-person alerts, which confirms record status edits can be family-sensitive ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

`Record Source` means newer CRM metadata for where a person record was created. The provided release notes say v18.1 improved Person Record Source support in Get Person From Fields, the internal Add Family page, and default Check-in new-person creation ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Inspect the live instance for configured record source values before depending on them.

`Person Entry` means the workflow, block, or action pattern for collecting person data and creating or resolving person records. Workflow Person Entry appears in RockU training, and release notes identify recent Obsidian Workflow Entry person/spouse fixes ([Workflow Person Entry](https://community.rockrms.com/rocku/workflows/workflow-person-entry), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

`Data Integrity` means the operational discipline of finding, preventing, and correcting person/family data problems. RockU has multiple Individuals in Rock lessons around data integrity, data automation, merging duplicates, deleting people, attributes, known relationships, and profile management ([Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock)).

## 3. People And Families Mental Model

Think of Rock's people model as five overlapping layers.

The first layer is the individual identity record. This is the `Person` entity: name, nickname, gender, birthdate, marital information, anniversary date, photo id, record type, record status, connection status, giving settings, phone numbers, email, and related core identity fields. The person profile renders this layer to staff and allows many related surfaces to be reached from one place. RockU's Individuals in Rock curriculum treats searching, profile review, adding/editing individuals and families, notes, attributes, known relationships, merging duplicate records, deleting a person, impersonation, data integrity, and data automation as one coherent training track ([Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock)).

The second layer is the alias layer. A person can be addressed by `PersonAlias`, and aliases survive merge events. The Rock developer guide is explicit that duplicate person records are common and that custom code should avoid storing raw `Person.Id`; instead, store `PersonAlias.Id` so the reference remains valid after merge ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)). This layer is easy to miss because staff often talk about a "person id", while workflows and APIs may carry person alias GUIDs. Agents should always ask: "Is this value a person id, person guid, person alias id, or person alias guid?"

The third layer is the household layer. A family is a group. A person belongs to a family group as a group member with a role. Adult/child relationships inside a family are not just a display convention; they affect salutations, check-in, registration, household giving, and operational reporting. Family data can include addresses, family attributes, group locations, group member roles, group member status, and group-level security. The Groups manual explains that Rock uses group types to drive behavior such as attendance, check-in, locations, schedules, and role capabilities ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). The mobile Group Members block documentation says one common use case is displaying a person's family members by selecting the appropriate group type and providing person context ([Group Members](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)).

The fourth layer is the relational graph beyond the household. Known relationships can connect people who are not in the same family group. This matters in blended family scenarios, guardianship, check-in permissions, care relationships, emergency contacts, and operational access. RockU separates Blended Families, Family Attributes, and Known Relationships into distinct lessons in the Individuals in Rock path, which is a useful hint that these are related but different operational concepts ([Blended Families](https://community.rockrms.com/rocku/individuals-in-rock/blended-families), [Known Relationships](https://community.rockrms.com/rocku/individuals-in-rock/known-relationships)). Check-in source code specifically looks for known relationship roles with a `CanCheckin` attribute when finding related people who can be checked in with a family ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)).

The fifth layer is extension and behavior. Attributes, badges, notes, following, tags, workflows, communication subscriptions, assessments, background checks, security, person tokens, and mobile profile blocks all add behavior around the person. Attributes in particular are deeply embedded. Developer docs describe attributes as broadly attachable to entity types, with fields defining how values are edited and stored ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide), [Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)). Lava has dedicated person filters and attribute filters, and entity commands can query people with filters, sort, limits, and attribute prefetch behavior ([Person Filters](https://community.rockrms.com/lava/filters/person-filters), [Entity Commands](https://community.rockrms.com/lava/commands/entity-commands), [Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

An agent should treat a person/family question as a graph traversal, not as a profile lookup. For example:

- "Why does this child not appear in check-in?" may involve `Person.RecordStatus`, age/grade, family group membership, group member status, family search results, known relationship roles, group type check-in rules, group attributes, schedule availability, and check-in template settings.
- "Why did this communication go to the wrong person?" may involve duplicate aliases, family giving or registration behavior, communication preferences, `PrimaryAlias`, registrar person alias, family members, or a workflow person attribute that stored an alias GUID.
- "Why did this report miss people?" may involve connection status, record status, `PersonAlias` joins, family group type joins, attribute field types, attribute security, data view filters, and whether the report used `Person.Id` where it should have used alias history.
- "Can this profile be deleted?" may involve financial records, attendance, group membership, notes, workflows, logins, security roles, and merge history. RockU has a "How to Delete a Person" lesson, but agents should still inspect live dependencies before removal ([How to Delete a Person](https://community.rockrms.com/rocku/individuals-in-rock/how-to-delete-a-person)).

The practical mental model:

`Person` is the current profile.

`PersonAlias` is the durable pointer.

`Family` is a group.

`Known Relationship` is a relationship group edge.

`Attribute` is the configurable schema.

`AttributeValue` is the per-entity stored data.

`Workflow`, `Communication`, `Check-in`, `Finance`, `Security`, and `Reporting` are consumers of those identities.

## 4. Source Authority And How To Use This Guide

Source authority matters because Rock has official docs, developer docs, RockU training pages, release notes, model map metadata, source code, community recipes, and partner articles. They do not have equal authority.

Use this guide with the following evidence order:

1. Rock core source code and generated view models when behavior is implementation-specific.
2. Official Rock developer docs for API, Lava, attributes, block development, and person alias guidance.
3. Official Rock documentation books for admin concepts and operational configuration.
4. RockU training records for workflow and admin surface coverage.
5. Rock release notes for version caveats and confirmed behavior changes.
6. Model Map for entity presence and category confirmation.
7. Community recipes for patterns, examples, warnings, and practical ideas, but not as authoritative best practice.
8. Partner resources only as supporting operational suggestions.

Examples of higher-authority sources in this pack:

- `PersonAlias` guidance comes from official developer documentation ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).
- Attribute entity and value fields come from official developer documentation ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)).
- Attribute rendering and saving in custom blocks comes from official developer documentation ([Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)).
- Lava entity commands and person/attribute filters come from official Lava docs ([Entity Commands](https://community.rockrms.com/lava/commands/entity-commands), [Person Filters](https://community.rockrms.com/lava/filters/person-filters), [Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).
- Group-type behavior and check-in role behavior come from official documentation ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).
- Version changes come from release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Implementation details for check-in family search, known relationships, and registration bags come from source code snippets ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs), [FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs), [EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs)).

Community recipes are useful but should be treated carefully. Rock recipe pages themselves include a disclaimer that community-contributed recipes are not reviewed or endorsed by the Rock core team and may have performance or security implications. This matters especially for SQL, dynamic data pages, unmerge scripts, and security-sensitive person profile tabs ([Registration Fee Per Family](https://community.rockrms.com/recipes/476), [Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344), [Recovering a Merged Person](https://community.rockrms.com/recipes/184)).

How agents should use this guide:

- Use the conceptual sections to orient.
- Use entity and relationship sections to decide which tables, blocks, or services to inspect.
- Use workflow sections to identify operational paths.
- Use troubleshooting branches to narrow behavior.
- Use source links to validate a claim or find the original implementation.
- Use live inspection whenever this guide says "verify in live Rock".

Do not use this guide as a license to make blind production changes. Person and family data is high-impact. A bad merge, delete, deactivation, family move, relationship change, or attribute update can alter check-in permissions, giving visibility, security access, communication eligibility, and pastoral care workflows.

## 5. Core Configuration And Data Model

The core data model can be understood through a small number of entities and configuration surfaces.

### Person

`Person` is the central individual entity. The provided source pack does not include a full current `Person` model file, so exact properties must be verified in a live Rock instance or current source checkout before writing exhaustive schema documentation. The source pack does show repeated official and code-level references to common fields such as `Id`, `Guid`, `FullName`, `NickName`, `FirstName`, `LastName`, `Gender`, `BirthDate`, `AnniversaryDate`, `Email`, `PhotoId`, `RecordTypeValueId`, `RecordStatusValueId`, `ConnectionStatusValueId`, `CreatedByPersonAliasId`, and `PrimaryAlias` through Lava examples, SQL recipes, and source snippets ([Filters](https://community.rockrms.com/rocku/lava/filters), [Simple 'who created who' functionality](https://community.rockrms.com/recipes/271), [FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)).

Operationally important person configuration includes:

- Record Type: usually distinguishes person records from business or other record types. Check-in source code filters family search results to the person record type ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)).
- Record Status: active/inactive/deceased-style lifecycle state. Release notes include family-sensitive record status fixes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Connection Status: ministry relationship classification. Community patterns use transient connection statuses for record source tracking, but this is local and must be verified before reuse ([Track How Person Records are Created](https://community.rockrms.com/recipes/223)).
- Campus: may be directly stored or derived through family, address, attendance, interactions, or other local rules. Person filters include `Campus`, `NearestCampus`, geofencing group filters, and group filters, but exact local campus assignment logic must be verified ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)).
- Photo: `PhotoId` indicates profile photo binary file relationship. Release notes state v16.3 improved avatar handling when workflows update profile photos with different file types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Giving settings: family/individual giving behavior matters, and release notes include multiple family-giving fixes in v17.2 and v18.3 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Communication preferences: SMS and email behavior can be affected by registrations and communication settings. Release notes include a v18.2 fix preserving SMS preference when a registration template does not show SMS opt-in ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Live inspection for a `Person` should include:

- Person profile Bio or main detail block.
- History tab for created/modified fields and audit records.
- Extended attributes and category tabs.
- Family members and family group.
- Known relationships.
- Notes, tags, following, badges, and signals.
- Logins/security roles.
- Communication preferences and unsubscribes.
- Group membership, attendance, registrations, workflows, interactions, and financial surfaces.

### PersonAlias

`PersonAlias` is a CRM model in Model Map metadata ([Model Map](https://community.rockrms.com/ModelMap)). Its operational purpose is confirmed by developer documentation: it is the durable way to reference people across merges ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

When a duplicate is merged, aliases that pointed to the removed person can continue pointing to the surviving person. That means historic records linked through aliases remain resolvable. The source pack also includes the workflow Lava note that a workflow `Person` attribute raw value returns a person alias GUID ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).

Inspect these alias facts in live Rock:

- `Person.PrimaryAlias.Id`
- `Person.PrimaryAlias.Guid`
- all aliases where `PersonAlias.PersonId = Person.Id`
- references in foreign tables using `PersonAliasId`
- workflow attribute raw values storing alias GUIDs
- created/modified by person alias fields such as `CreatedByPersonAliasId`
- merge history and aliases reassigned during merge

### Family Group

A Rock family is a group of the family group type. The source pack confirms family handling through group-oriented docs and mobile blocks. The mobile Group Members block displays members in the same group type for a person context and identifies family members as its main use case ([Group Members](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)). The Groups manual explains group types, group roles, group security, group attendance, group locations, requirements, check-in rules, and group role permissions ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

Inspect these family facts:

- Family group id and group type.
- Group name and whether it is active/archived.
- Group members and group member roles.
- Group member status: active, inactive, pending, or local equivalents.
- Family address/group location.
- Campus associated with the family or members.
- Family attributes.
- Whether a person has multiple family memberships.
- `PrimaryFamilyId` where used by the live version and custom code.
- Related known relationships outside the family group.

### GroupMember And GroupTypeRole

Family membership is represented by group membership. Group types define roles, and roles can carry behavior. The Groups manual says group member roles can have capabilities such as Can View, Can Edit, Can Manage Members, and, as of Rock v16.7, Is Check-in Allowed for group type role check-in scenarios ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

For family work, agents must inspect not only who is in the group, but what role they have. Adults, children, guests, owners, and custom roles may appear differently in display, check-in, registration, and reports.

### Known Relationships

Known relationships are group-based relationship records. Check-in source code identifies the known relationships group type, owner role, and role attributes such as `CanCheckin` when finding related people ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)). Release notes include a v17.5 fix for removing an individual with a `Can Check-In` known relationship under certain configurations ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Known relationships should be inspected when:

- A child is eligible for check-in under an adult who is not in their family.
- A blended family configuration differs from family group membership.
- The kiosk shows or hides related people unexpectedly.
- A relationship was removed or cannot be removed.
- A family registration process asks for child relationship type.
- A check-in template configures relationship options for adding children.

### Attribute

`Attribute` defines custom data fields. Official developer docs describe these properties as central:

- `Name`: friendly administrative/display name.
- `Key`: programmatic key used by Lava and code.
- `EntityTypeId`: entity type the attribute applies to.
- `EntityTypeQualifierColumn`: optional scoping column.
- `EntityTypeQualifierValue`: optional scoping value.
- `FieldTypeId`: field type controlling edit/storage behavior.
- `IsMultiValue`: whether multiple values are allowed.
- `IsRequired`: whether editing requires a value.
- `IsGridColumn`: whether displayed in grids where supported.
- `Description`: administrative help text.
- `Order`: display ordering ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)).

Person attributes are attributes where the entity type is `Rock.Model.Person`. Family attributes are usually group attributes on the family group type or group entity, not person attributes. Check-in and registration configuration can use group type attributes scoped to check-in templates, as shown in source migrations that add check-in registration display attributes to group types by purpose value ([AddCheckinRegistrationChildrenDisplayAttributes.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202205061756248_AddCheckinRegistrationChildrenDisplayAttributes.cs)).

### AttributeValue

`AttributeValue` stores values for entity instances. Developer docs identify these properties:

- `AttributeId`
- `EntityId`
- `Value`
- `ValueAsNumeric`
- `ValueAsDateTime`
- `ValueAsBoolean`
- `ValueAsPersonId` when applicable to a person alias GUID ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)).

This means an attribute value is not self-describing. You must join to `Attribute`, `FieldType`, and `EntityType` to interpret it. The source pack includes a SQL helper that lists person attribute values by joining `AttributeValue`, `Attribute`, `EntityType`, `FieldType`, and `Person` where the entity type name is `Rock.Model.Person` ([View_PersonAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_PersonAttributeValues.sql)).

### Notes, Tags, Following, Badges, Assessments, Background Checks

RockU's Individuals in Rock track includes Person Note, Tags, Following, Person Attributes, Bookmarked Attributes, Custom Badges, Assessments, Background Checks, Data Integrity, Data Automation, and Tag Security as person-profile-adjacent features ([Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock)). The source pack does not provide deep implementation detail for all of these, so agents should use the training pages as coverage signals and inspect the live instance for the exact note types, tag security, badge components, assessment attributes, and background check provider configuration.

Background check fields also appear in source SQL helpers as well-known attributes for checked status, date, and result ([Populate_Person_Attribute_Values_With_RandomValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_Person_Attribute_Values_With_RandomValues.sql)). Do not assume those attributes have the same GUIDs in every custom workflow unless they are core well-known attributes in the target version; verify in live Rock.

## 6. Primary Entities And Relationships

The following relationship map is the practical core.

### Person To PersonAlias

A `Person` can have one or more aliases. `PersonAlias.PersonId` points to the current person. A merge can leave multiple aliases pointing to the surviving person. Custom references should store alias ids, not raw person ids ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

Operational checks:

- When a person-related record is missing, search by both `Person.Id` and aliases.
- When workflow attributes point to a person, check whether the stored value is a person alias GUID ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).
- When a record was created by someone, fields like `CreatedByPersonAliasId` may need alias resolution.
- When a duplicate merge occurred, inspect all aliases and affected tables before claiming data was lost.

### Person To Family Group

A person belongs to a family through group membership. The family group is a group of the family group type. A profile can display family members, but code and reports should inspect group membership. Mobile docs for Group Members confirm that a person context plus group type can be used to show family members ([Group Members](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)).

Operational checks:

- Is the person in a family group?
- Which group is primary?
- What role does the person hold?
- Is the group active?
- Is the group member active?
- Does the family group have a home location?
- Are all household members active, or are inactive people hidden by the consuming block?
- Does a report join on family group type, group member role, or `PrimaryFamilyId`?

### Family Group To GroupLocation And Location

Family address is commonly represented through group location. The source pack does not include a complete family address schema record, but group documentation covers group locations and the person Lava `Address` filter exposes address retrieval by address type for a person ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296), [Person Filters](https://community.rockrms.com/lava/filters/person-filters)). For exact address storage, inspect the live database and version-specific model map.

Operational checks:

- Family group locations by location type.
- Person address output through Lava filters.
- Address modified history if a custom page exposes it.
- Campus assignment based on address or geocoding.
- Whether address geocoding jobs or IP geocoding are enabled. RockU includes IP Address Geocoding in the Individuals track, but the source pack does not provide implementation details ([IP Address Geocoding](https://community.rockrms.com/rocku/individuals-in-rock/ip-address-geocoding)).

### Person To Known Relationships

Known relationships are modeled through known relationship groups and roles. Check-in source code fetches role ids from the known relationships group type and checks a `CanCheckin` role attribute before adding related people to check-in context ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)).

Operational checks:

- Which known relationship group belongs to the person?
- Which role is owner?
- Which related people are linked?
- Which roles have `CanCheckin` or local equivalents?
- Are inactive related people prevented by check-in configuration?
- Is the relationship available in the check-in UI or registration UI?

### Person To PhoneNumber And Email

Person search and communication workflows depend heavily on phone and email. Check-in family search code includes phone-number search behavior using numeric/reversed phone values, and mobile Smart Search supports person search by name, birthdate, email, and address ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs), [Smart Search](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search)).

Operational checks:

- Phone number type and SMS enabled flag.
- Email address and communication preference.
- Whether registration or workflow processes update SMS settings.
- Whether an imported or nameless record has enough contact information.
- Whether duplicate search uses phone suffix, full number, email, name, or birthdate.

### Person To Attributes

A person can have any number of person attributes. Person attribute values are stored in `AttributeValue` rows where `EntityId` is the person id and the attribute's entity type is `Rock.Model.Person`. Source SQL shows the basic join pattern ([View_PersonAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_PersonAttributeValues.sql)).

Operational checks:

- Attribute definition exists and has the expected key.
- Attribute category makes it visible where expected.
- Attribute security allows the current user or block to view/edit.
- Attribute field type stores the value as expected.
- Attribute value exists for the person.
- Attribute value has the expected raw value and formatted value.
- Attribute prefetch is enabled or disabled in Lava entity command context.

### Group Or Family To Attributes

A family attribute is usually a group attribute, not a person attribute. RockU has a Family Attributes lesson, and group docs explain group type extension through attributes ([Family Attributes](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes), [Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). Always inspect the attribute's `EntityTypeId` and qualifiers before deciding whether a "family attribute" is stored on the family group, the family group type, or each person.

### Person To Workflows

Workflows often store people in attributes. Workflow Lava documentation states that raw values for person attributes are person alias GUIDs ([Workflows and Lava](https://community.rockrms.com/lava/workflows)). The Workflow Person Entry training page is a coverage signal that person entry is a first-class workflow surface ([Workflow Person Entry](https://community.rockrms.com/rocku/workflows/workflow-person-entry)). Release notes include fixes for Obsidian Workflow Entry around person and spouse attributes and blank spouse creation ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Operational checks:

- Workflow attribute key and field type.
- Raw value vs formatted value.
- Whether value is person alias GUID, person id, or text.
- Whether the workflow launched from a person context.
- Whether person/spouse attributes are hidden or autofilled.
- Whether record source is set by Get Person From Fields in v18.1+.

### Person To Communications

Communications use person aliases and recipients. The source pack includes communication-related RockU coverage for nameless people and SMS pipeline, plus release notes around SMS opt-in preservation in registrations ([Nameless People](https://community.rockrms.com/rocku/communication/nameless-people), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)). The exact communication entity schema is outside this pack; inspect live communication records, `CommunicationRecipient`, unsubscribe records, and communication preferences before troubleshooting delivery.

### Person To Attendance And Check-In

Attendance has `PersonAliasId`, `StartDateTime`, `RSVP`, `DidAttend`, `ScheduleId`, `GroupId`, `SundayDate`, and other check-in fields per the Advanced Entity Guide ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)). Check-in family search and relationship logic are visible in source snippets ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs), [FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)). Group documentation describes check-in rules, group attendance requiring location or schedule, and group role check-in permissions ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

Operational checks:

- Does the person have an active alias?
- Is the person active?
- Is the family found by the configured search type?
- Is the person in a check-in group or eligible to be added?
- Does the group type allow check-in for the person's role?
- Do schedules, locations, capacity, age, grade, and gender restrictions match?
- Are known relationships allowed?
- Are labels configured with family security code settings?

### Person To Security

People can have logins and security roles. In Rock, security roles are groups. Person filters include `IsInSecurityRole`, which takes a group id and returns a boolean, logging an exception if the id is not a security role ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)). Developer block docs show checking authorization with `IsUserAuthorized( Authorization.EDIT )` and adding UI conditionally ([Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)).

Operational checks:

- Current person is authenticated.
- Current person has the expected security role membership.
- Block/page/entity security permits the action.
- Attribute-level security permits viewing or editing.
- Tag security or note security is separately configured.
- Impersonation or passwordless login behavior is restricted and audited.

## 7. Common People And Families Workflows

### Search For A Person

Person search can happen in staff UI, check-in, mobile app, Lava, SQL, and custom blocks.

RockU includes "Searching for a Person" in the Individuals in Rock track ([Searching for a Person](https://community.rockrms.com/rocku/individuals-in-rock/searching-for-a-person)). Mobile Smart Search supports multiple person search components: birthdate, name, email, and address, plus group name search. The Smart Search docs note that unsupported components result in an error display, and that the block has configuration for components, result size, keyboard focus, search history, birthdate/age display, and person detail page ([Smart Search](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search)).

Agent workflow:

1. Identify the search surface.
2. Identify search component: name, phone, email, birthdate, address, barcode, family, group, or custom entity search.
3. Check whether inactive people are included.
4. Check whether record type filters apply.
5. Check whether family search groups results by family.
6. Check whether search value normalization applies, especially phone numeric search.
7. If search fails in check-in, inspect the check-in configuration template and kiosk context.

Check-in family search source code shows phone search normalizes numeric phone values and can use reversed-number matching depending on phone search type. It also filters to family groups and person record type when resolving family ids ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)). This is implementation evidence, but exact current behavior should be verified against the target Rock version.

### Add Or Edit An Individual

RockU includes "Adding and Editing Individuals and Families" as a core person workflow ([Adding and Editing Individuals and Families](https://community.rockrms.com/rocku/individuals-in-rock/adding-and-editing-individuals-and-families)). Recent release notes add an important version caveat: v18.1 improved the Person Record Source feature by adding support for setting a Record Source within Get Person From Fields and the internal Add Family page, plus a default Record Source for new persons created during Check-in ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent workflow:

1. Determine whether the person is new, existing, duplicate, nameless, or a business/non-person record.
2. Search by name, email, phone, birthdate, family, and alternate ids before creating.
3. Confirm record type and connection status defaults for the creation surface.
4. On v18.1+, inspect Record Source configuration for the creation path.
5. Add contact fields, demographics, campus, family, and relevant attributes.
6. Verify alias creation and primary alias.
7. Verify family group membership and role.

### Add Or Edit A Family

Adding a family usually creates or edits a group and group members, not only persons. Family registration and check-in registration add more complexity.

Relevant sources:

- RockU has Adding and Editing Individuals and Families, Blended Families, Family Attributes, Known Relationships, and Extending the Add Family Block ([Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock)).
- Mobile/source view models expose family edit and save behavior for check-in registration, including family attributes, adult attributes, child attributes, relationships, address display requirement, birthdate/grade/gender/race fields, suffix display, SMS button behavior, and whether check-in after registration is allowed ([EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs), [SaveFamilyOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyOptionsBag.cs)).
- Family registration settings include address display and optional/required attributes for families ([checkInFamilyRegistrationSettingsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/checkInFamilyRegistrationSettingsBag.d.ts)).

Agent workflow:

1. Identify whether this is internal Add Family, public family pre-registration, check-in family edit, event registration family selection, or a custom workflow.
2. Inspect the family group and group type.
3. Inspect adult/child roles and active statuses.
4. Inspect family address and location type.
5. Inspect family-level attributes and person-level attributes separately.
6. Inspect known relationship settings if children are being added to another family or a blended family.
7. On v18.1+, inspect Record Source for new people created through Add Family or Check-in.
8. Verify giving settings for adults added to existing families. Release notes include a v17.2 fix around new adults added through Family Registration being set to combined giving rather than individual giving ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Merge Duplicate Records

Duplicate person records are expected over time. RockU includes Merging Duplicate Records in the Individuals track ([Merging Duplicate Records](https://community.rockrms.com/rocku/individuals-in-rock/merging-duplicate-records)). Developer guidance around `PersonAlias` exists because merges happen ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

Agent workflow before merge:

1. Confirm both profiles represent the same person.
2. Compare names, birthdate, email, phone, photo, family, address, campus, connection status, record status, notes, aliases, logins, attendance, giving, registrations, workflows, group memberships, and attributes.
3. Identify which record should survive.
4. Check sensitive records: financial giving, security roles, background checks, signed documents, and communication preferences.
5. Verify whether any custom external systems store raw `Person.Id`; those may not survive cleanly.
6. Prefer UI-supported merge over direct SQL.

Agent workflow after merge:

1. Verify the surviving `Person.Id`.
2. Verify aliases now point to the survivor.
3. Verify family membership and known relationships.
4. Verify logins/security roles.
5. Verify attendance, giving, communication history, notes, and workflows.
6. Check custom reports for stale raw person ids.

If a merge was wrong, do not improvise. Community recipes describe recovery and unmerge approaches involving database backups, alias detection, preview/rollback transactions, and validation, but they are community-contributed and not core-endorsed ([Recovering a Merged Person](https://community.rockrms.com/recipes/184), [Unmerge Accidentally Merged Person with Alias Detection](https://community.rockrms.com/recipes/474/unmerge-accidentally-merged-person-with-alias-detection), [Rock Unmerge Profiles Tool](https://community.rockrms.com/recipes/541)). Treat these as incident response references, not routine admin guidance.

### Delete Or Deactivate A Person

RockU includes "How to Delete a Person", but the source pack does not include the full procedural content ([How to Delete a Person](https://community.rockrms.com/rocku/individuals-in-rock/how-to-delete-a-person)). Agents must verify live dependencies before deletion.

Prefer deactivation over deletion when the person has history. Deactivation is reversible and preserves relational context. A community recipe for undoing accidental deactivation highlights that deactivation can affect group and security role memberships and can be tedious to reverse manually ([Undo Accidentally Deactivated People](https://community.rockrms.com/recipes/291)).

Before deletion or deactivation, inspect:

- Financial records and giving family settings.
- Attendance and check-in history.
- Group memberships and security roles.
- Workflows and person attributes.
- Communication history and subscriptions.
- Notes, tags, following, badges, and signals.
- Known relationships.
- Logins and impersonation tokens.
- Merge history and aliases.

Use deletion only when the live Rock UI allows it and organizational policy approves it. If deletion fails, inspect dependency warnings rather than bypassing them.

### Add Person Or Family Attributes

RockU includes Person Attributes, Bookmarked Attributes, Family Attributes, and Extending the Add Family Block ([Person Attributes](https://community.rockrms.com/rocku/individuals-in-rock/person-attributes), [Bookmarked Attributes](https://community.rockrms.com/rocku/individuals-in-rock/bookmarked-attributes), [Family Attributes](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes), [Extending the Add Family Block](https://community.rockrms.com/rocku/individuals-in-rock/extending-the-add-family-block)). Developer docs describe the underlying attribute model ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)).

Agent workflow:

1. Decide whether the data belongs on the person, family group, group member, known relationship, workflow, registration, campus, or another entity.
2. Create an attribute definition with a durable key.
3. Choose the correct field type.
4. Choose categories for display.
5. Set required and grid behavior carefully.
6. Set security if sensitive.
7. Add values through UI, workflow, import, Lava, API, or code.
8. Verify raw value and formatted display.
9. Verify behavior in profile, mobile, check-in, reports, and workflows.

Version caveat: v18.2 fixed Attribute Editor saving for attributes designed to store other attributes, and v19.1 fixed category dropdown behavior in multiple attribute editing blocks ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If attribute editor behavior looks wrong, check version and release notes.

### Track How A Person Record Was Created

Modern Rock has Record Source improvements in v18.1, but many older instances used local patterns. A community recipe describes using transient connection statuses and a "How Created" person attribute to preserve where a record originated before moving the person to a target connection status ([Track How Person Records are Created](https://community.rockrms.com/recipes/223)). That is a practical historical pattern, not a universal core feature.

Agent workflow:

1. Check Rock version.
2. Inspect Person Record Source settings if on v18.1+.
3. Inspect person created date, created by alias, history, connection status, and record source.
4. Inspect local attributes such as `HowCreated` only after verifying they exist.
5. Inspect workflows, event registration, giving, SMS pipeline, form builder, and check-in creation paths.
6. Avoid assuming connection status means creation source unless local documentation confirms it.

### Run Person-Based Automation

Common patterns use Data Views, Group Sync, and group member workflow triggers. Community recipes show workflows launched when someone enters a Data View and connection requests created for new people through a synced group ([Run Workflow When Someone Enters a Dataview](https://community.rockrms.com/recipes/113), [Auto Create Connection Requests for New People](https://community.rockrms.com/recipes/251)). These are powerful but require guardrails.

Agent workflow:

1. Define the source predicate as a Data View or SQL-backed report.
2. Test the predicate on a small sample.
3. Use a dedicated automation group if using group sync.
4. Set sync interval deliberately.
5. Add workflow person attribute with `Person` field type.
6. Remember workflow person raw values may be alias GUIDs ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).
7. Prevent reprocessing with statuses, attributes, history, or group membership.
8. Add monitoring and rollback procedures.

## 8. Person Model Deep Dive

### Identity Fields

The person model contains multiple identity-like fields. Agents must distinguish them.

`Person.Id` is the numeric primary key for the current person row. It is convenient in internal URLs and many queries, but it is not the best durable external reference after merge.

`Person.Guid` is a globally unique identifier for the person row. It can be useful for API and cross-system references, but the provided official guidance specifically recommends `PersonAlias` for custom models that reference people because merges alter which person row survives ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

`PersonAlias.Id` is the preferred numeric foreign key for many person-related references.

`PersonAlias.Guid` is commonly stored by workflow person field types and used by Lava raw values ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).

`PrimaryAliasId` or `PrimaryAlias.Guid` appears in Lava and recipes. For example, community recipes expose `Context.Person.PrimaryAlias.Id` and use `CurrentPerson.PrimaryAlias.Guid` in links, but always verify syntax and security before using recipe code in production ([Recovering a Merged Person](https://community.rockrms.com/recipes/184), [Outstanding Registration Payment Accessible to All Family Members](https://community.rockrms.com/recipes/488)).

`CreatedByPersonAliasId` appears in recipes for "who created who" functionality ([Simple 'who created who' functionality](https://community.rockrms.com/recipes/271)). This reinforces the pattern that audit ownership often points through person alias.

### Names

Rock commonly exposes `FirstName`, `NickName`, `MiddleName`, `LastName`, and `FullName`. Lava examples use `Person.NickName`, `Person.FullName`, and sorting by `LastName`/`NickName` ([Filters](https://community.rockrms.com/rocku/lava/filters), [Entity Commands](https://community.rockrms.com/lava/commands/entity-commands)). Family salutations can use informal or formal names, separators, and active/inactive behavior through the `FamilySalutation` person filter ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)).

Operational checks:

- Use nickname for informal ministry display where appropriate.
- Use legal/first name when legal or finance processes require it.
- For family reporting, do not assume all family members share a last name. A community attendance recipe exists specifically because family-grouped attendance is not the same as last-name sorting ([Sort Attendance By Family](https://community.rockrms.com/recipes/115)).
- For duplicate detection, compare email, phone, birthdate, family, address, photo, and aliases, not just name.

### Demographics

The source pack shows person fields such as gender, birthdate, anniversary date, age, grade, race, suffix, and marital status through Lava examples, mobile check-in registration bags, Smart Search, and release notes ([Filters](https://community.rockrms.com/rocku/lava/filters), [EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs), [Smart Search](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Important version caveat: a v18.3 pre-alpha spotlight record notes a fix where the Person Entry workflow action defaulted Marital Status to "Married" when no value was provided and Autofill Current Person was disabled ([GitHub Spotlight: 4/8/2026](https://www.triumph.tech/resources/github-spotlight-482026)). The official release note pack also includes workflow entry person/spouse fixes in v18.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Verify the target version before diagnosing unexpected spouse or marital-status values.

### Contact Fields

Contact fields include email and phone numbers. Phone numbers have types and SMS flags. Person search, SMS pipelines, communication preferences, registrations, and family registration may update or depend on these values. Release notes include an Event v18.2 fix preserving SMS opt-in when the registration template hides SMS opt-in ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Check-in family edit response bags expose SMS button visibility and default state ([EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs)).

Operational checks:

- Inspect phone number type.
- Inspect SMS enabled flag.
- Inspect communication preferences and unsubscribe records.
- Inspect whether a registration, workflow, or family edit path recently modified contact data.
- In public forms, verify duplicate matching rules before creating a new person from phone or email.

### Photo And Avatar

A `Person` can have a `PhotoId`. Release notes for v16.3 say Rock updated the Get Avatar handler so workflow-updated profile photos using different file types correctly set the person's photo ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). A partner article suggests monitoring what percentage of people have photos, but the source pack's hydrated excerpt is empty, so treat it only as a supporting operational idea ([Person Photos in Rock](https://www.triumph.tech/resources/person-photos-in-rock)).

Operational checks:

- Does the person have `PhotoId`?
- Is the binary file accessible?
- Is the avatar handler returning default or custom photo?
- Did a workflow update the photo?
- Does the file type behave correctly in the target version?

### Record Status, Connection Status, And Record Source

Record status controls lifecycle availability. Connection status controls relationship/engagement classification. Record source describes creation source in newer versions.

Do not conflate them.

Common diagnostics:

- If a person does not appear in a search, check record status and whether inactive records are included.
- If a person appears in ministry reports unexpectedly, check connection status and report filters.
- If a person was created by check-in or workflow, check record source in v18.1+ and local "How Created" patterns in older/custom instances.
- If a family-level record status edit behaves strangely, check version; v16.5 fixed a deceased-person alert issue when editing a family's record status ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Logins, Account Protection, Impersonation, And Passwordless Login

RockU includes Account Protection Profiles, Impersonation, and Passwordless Login in the Individuals track ([Account Protection Profiles](https://community.rockrms.com/rocku/individuals-in-rock/account-protection-profiles), [Imersonation](https://community.rockrms.com/rocku/individuals-in-rock/impersonation), [Passwordless Login](https://community.rockrms.com/rocku/individuals-in-rock/passwordless-login)). Mobile Login docs describe login, registration page settings, forgot password URL, and external authentication surfaces ([Login](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/login)).

Because the source pack does not include detailed account protection internals, agents should verify:

- User login records attached to the person.
- Authentication provider.
- Security role membership.
- Account protection profile settings.
- Person token settings and limits.
- Impersonation permissions and audit trails.
- Passwordless login global attributes and block settings.

Person filters include `PersonActionIdentifier`, `PersonByPersonActionIdentifier`, and token-related parameters such as expiration minutes and max usage in the excerpt, but exact usage should be verified against the live Lava docs and target version ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)).

## 9. Families Deep Dive

### Family As Group

A family is a Rock group. This has several consequences:

- Family membership is group membership.
- Family roles are group roles.
- Family address is generally a group location.
- Family attributes are group attributes or group-type-scoped attributes.
- Family security can interact with group security.
- Family search in check-in resolves group ids.
- Family-level reports often join `Group`, `GroupMember`, `GroupType`, and `Person`.

The official Groups manual is the grounding source for group behavior ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). It describes group types, roles, attendance, schedules, locations, requirements, security, group type inheritance, and check-in behavior. Agents should avoid making family-specific claims without verifying the underlying group type and role configuration.

### Family Membership Roles

Typical family roles include adult and child, but local Rock instances may customize roles or labels. Roles affect display and behavior. Check-in registration response bags include adult and child attributes separately, display settings for adults and children, and relationship choices for new children ([EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs)).

Operational checks:

- Which role does each family member have?
- Are adults marked active?
- Are children marked active?
- Are inactive people hidden by the current feature?
- Do role settings affect check-in?
- Are family members duplicated across multiple family groups?

### Head Of Household And Salutation

Person Lava filters include `HeadOfHousehold` and `FamilySalutation` ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)). The `FamilySalutation` excerpt indicates parameters for including inactive people, formal names, final separator, and separator. Exact parameters should be verified in the live Lava docs for the target version, but the principle is clear: salutation is generated behavior, not a static field to blindly reuse.

Operational checks:

- Which adults are active in the family?
- Does the filter include inactive people?
- Are nicknames or formal first names desired?
- Are children included in the selected salutation format?
- Does the organization have custom salutations or name rules?

### Blended Families

RockU has a Blended Families lesson and a Known Relationships lesson in the Individuals track ([Blended Families](https://community.rockrms.com/rocku/individuals-in-rock/blended-families), [Known Relationships](https://community.rockrms.com/rocku/individuals-in-rock/known-relationships)). The source snippets for check-in relationship settings show that child relationship settings can specify which known relationship types add the child to the parent's family and which create a new family with a relationship back to the parent's family ([CheckInChildRelationshipSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInChildRelationshipSettingsBag.cs)).

Operationally, blended families require agents to separate three questions:

1. Who is in the same family group?
2. Who has a known relationship edge?
3. Which features use family membership, known relationship, or both?

For check-in, known relationships with `CanCheckin` can bring related people into the family context ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)). For event registration, family member dropdowns depend on registration template settings and version-specific eligibility rules. For giving, family giving depends on giving group settings and release-specific API behavior. For communication, family membership does not automatically mean every person should receive every message.

### Family Address And Campus

The source pack gives indirect evidence for family address through person address filters, group locations, and registration settings. The Person `Address` filter retrieves a person address by address type and supports formatting behavior across versions ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)). Group docs cover group location concepts ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). Check-in family registration settings include display requirements for family address ([CheckInFamilyRegistrationSettingsBag](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/checkInFamilyRegistrationSettingsBag.d.ts)).

Live verification required:

- Which location type represents home address?
- Is the address stored on the family group, individual person, or both in local customizations?
- Does campus assignment derive from address geocoding, postal code, explicit person campus, group campus, attendance campus, or manual setting?
- Are there address standardization or geocoding jobs?
- Does mobile or check-in family edit require address?

### Family Giving

Family giving is a version-sensitive area. Release notes include:

- v17.2: fixed new adults added to an existing family through Family Registration being incorrectly set to Individual Giving instead of Combined Giving.
- v18.3: fixed Giving History API issues where blank "Combine Giving With" incorrectly returned family giving data and where excluding family giving missed contributions from the individual's other records ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Operational checks:

- Inspect each adult's giving setting.
- Inspect "Combine Giving With" or equivalent giving group configuration in the live version.
- Check whether API calls include family giving.
- Check whether statements are generated for single individual or family.
- Check v18.1 Statement Generator fix if a single individual statement was filtered by a previous Data View selection ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Family Event Registration

Event registration can be family-aware. A community recipe shows a per-family fee workaround using max registrants and discount codes, but it is a local pattern ([Registration Fee Per Family](https://community.rockrms.com/recipes/476)). A v19.1 release note is more authoritative: Rock added registrant eligibility rules to the Registration Template Detail Block and updated the Registration Entry Block to prevent incorrect family member registrations. Eligibility can limit registrants by age, grade, gender, and age classification, and the Family Member to Register dropdown defaults blank when family registrants are enabled to force intentional selection ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Operational checks:

- Registration template: registrants in same family setting.
- Eligibility rules: age, grade, gender, adult/child.
- Current person and family member list.
- Registrar person alias.
- Payment responsibility and outstanding balances.
- Security around person profile registration tabs.

A community recipe for outstanding registration payments accessible to all family members changes the registrar to the current person before redirecting to payment. That may solve a local barrier but changes communication ownership and must be reviewed for security and audit implications ([Outstanding Registration Payment Accessible to All Family Members](https://community.rockrms.com/recipes/488)).

## 10. Attributes Deep Dive

### Attribute Definition

An attribute definition is schema. The key is the most important stable identifier for Lava and code. The friendly name can change; the key should not be changed casually. The `EntityTypeId` and qualifiers define where the attribute applies. Field type defines edit UI and storage. Categories control where users see it. Security controls who can view/edit it.

Official docs describe attributes as broad and extensible. Nearly every entity type can have attributes, and Rock has UI for common entities plus an Attributes block that can manage attributes for many entity types ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)). Developer 303 shows how custom blocks can add an `AttributeValuesContainer` for editing and saving attributes ([Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)).

Agent checklist for an attribute definition:

- Entity Type: `Rock.Model.Person`, `Rock.Model.Group`, `Rock.Model.GroupType`, `Rock.Model.Workflow`, etc.
- Qualifier Column and Value: scoping to a workflow type, group type purpose, group type, defined type, or other subset.
- Key: exact programmatic key.
- Name and abbreviated name.
- Field Type and qualifiers.
- Category assignments.
- Required flag.
- Grid flag.
- Security.
- Default value.
- Is system flag.
- Modified date and migration ownership if source-controlled.

### Attribute Value

Attribute values are stored as strings, with typed helper fields. Official docs identify `Value`, `ValueAsNumeric`, `ValueAsDateTime`, `ValueAsBoolean`, and `ValueAsPersonId` ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)). Do not sort or compare values as strings if the attribute is logically numeric or date/time and the typed fields are available and maintained.

Agent checklist for an attribute value:

- Does an `AttributeValue` row exist?
- Is `EntityId` the expected person/group/workflow/etc. id?
- Does the field type store GUID, id, text, JSON, CSV, or another serialized format?
- Does formatted Lava display differ from raw value?
- Is the value cached?
- Does the entity need `LoadAttributes()` before code can read it?
- Are attribute values saved in the same transaction as entity changes?

### Person Attribute Field Type In Workflows

Workflow person attributes can be misunderstood. The workflow Lava docs state that `{{ Workflow | Attribute:'Person','RawValue' }}` returns a person alias GUID for a `Person` field type ([Workflows and Lava](https://community.rockrms.com/lava/workflows)). That means:

- Do not parse it as `Person.Id`.
- Resolve through alias when needed.
- Use `{{ Workflow | Attribute:'Person','FirstName' }}` only when the field type returns a full entity in the Lava context and the docs support it.
- If a workflow report searches workflow attribute values, compare against alias GUID or join through alias.

A community recipe for finding people from workflows builds a reporting page around workflow types and person attribute keys; use it as a pattern only after checking security and performance ([Finding People from Workflows](https://community.rockrms.com/recipes/437)).

### Attribute Lava Filters

Lava can read attributes through the `Attribute` filter. The attribute filter docs show:

- `{{ CurrentPerson | Attribute:'BaptismDate' }}` returns a string representation.
- A second parameter can request a property from an entity-like attribute value, such as a mentor last name.
- `Object` can return a full object for attribute inception patterns.
- `CurrentPerson.AttributeValues` can loop attributes but bypasses security checks, so it is useful for inspection but must be treated carefully.
- Rock v17.5+ adds a third parameter to control attribute-level security checks; passing `false` bypasses checks and should only be used in appropriate secure/internal contexts ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

Agent rule: when using Lava on person attributes in a public or semi-public block, default to respecting security. Only bypass attribute security for internal, reviewed use cases.

### Entity Commands And Attribute Prefetch

Lava entity commands can query people, groups, and other entities. The docs show parameters such as `where`, `id`, `ids`, `dataview`, `sort`, `limit`, `offset`, `securityenabled`, `lazyloadenabled`, `include`, `select`, `groupby`, `disableattributeprefetch`, and `prefetchattributes` ([Entity Commands](https://community.rockrms.com/lava/commands/entity-commands)). RockU examples query people by last name, attributes such as Position, id, ids, data view, gender, sort, offset, and limit ([Entity Commands RockU](https://community.rockrms.com/rocku/lava/entity-commands)).

Important nuance from the Lava docs: security is enabled by default for most entity commands, but person entity commands are different because person does not have user-specific security in the same way. Verify the exact behavior in the target version and context before exposing person data ([Entity Commands](https://community.rockrms.com/lava/commands/entity-commands)).

Attribute prefetching matters for performance. Starting in v15, Rock automatically prefetches attributes for returned entities in entity commands, and you can disable attribute prefetch if you do not need attributes ([Entity Commands](https://community.rockrms.com/lava/commands/entity-commands)). Agents should consider this when writing dashboards or repeated person loops.

### Attribute UI And Mobile Support

Mobile Attribute Values block displays and edits attribute values by category and entity type. The docs warn that it only edits field types supported in the mobile shell and that category/entity compatibility is the implementer's responsibility ([Attribute Values](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)).

Check-in family registration settings expose family, adult, and child attributes in edit family responses ([EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs)). Source snippets also show optional and required family attributes in check-in family registration settings ([checkInFamilyRegistrationSettingsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/checkInFamilyRegistrationSettingsBag.d.ts)).

Operational checks:

- Is the attribute category selected by the block?
- Is the entity type set correctly?
- Is the field type supported in mobile?
- Does the block use abbreviated names?
- Is attribute security respected?
- Are required attributes enforced?

### Attribute Migration And Source Control

The source pack includes SQL/codegen helpers for person attributes, such as generating `RockMigrationHelper.AddOrUpdatePersonAttributeByGuid` calls for recently modified person attributes and qualifiers ([CodeGen_AddUpdatePersonAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/CodeGen_AddUpdatePersonAttributes.sql)). It also includes developer docs for custom field types and field attributes ([Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further)).

Agent recommendation:

- For one-off operational attributes, UI creation may be enough.
- For plugin/core/shared attributes, use migrations with well-known GUIDs.
- Do not rely on attribute names alone in source-controlled code.
- Include qualifiers and categories in migration.
- Include rollback/delete behavior where appropriate.
- Test copying behavior and persisted value updates for custom field types.

## 11. Related Rock Areas: Groups, Security, Communications, Check In

### Groups

Groups are the structural backbone for families, security roles, check-in groups, serving teams, and general ministry groups. The Groups manual explicitly covers these categories and group type settings ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). People/family agents need enough group knowledge to diagnose:

- Family membership.
- Group member roles.
- Security role membership.
- Check-in group eligibility.
- Serving team scheduling preferences.
- Attendance.
- Group sync and automation.
- Group requirements.

RockU's Groups track includes group viewer, details, attendance, group types, inheritance, history, location, purposes, placements, requirements, security, extending groups, scheduling, RSVP, roster, communications, and group placement ([Groups](https://community.rockrms.com/rocku/groups)).

### Security

Person and family data is security-sensitive. Related security surfaces include:

- Page security.
- Block security.
- Entity security.
- Attribute security.
- Group security.
- Security role group membership.
- Tag security.
- Note security.
- Impersonation.
- Account protection.
- Passwordless login.
- Person tokens.

Developer docs show block authorization checks and page authorization patterns ([Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)). Attribute filter docs warn that attribute security can be bypassed with a third parameter in v17.5+, which should only be done deliberately ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)). Person filters include `IsInSecurityRole`, but it only applies to security groups and logs an exception for a non-security group id ([Person Filters](https://community.rockrms.com/lava/filters/person-filters)).

Operational rule: do not add person profile tabs, Dynamic Data blocks, or Lava snippets that expose registrations, giving, workflows, background checks, notes, or attributes without explicit security review. A community recipe for a registrations tab warns that the initial recipe does not account for registration template security ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)).

### Communications

Person records drive communication, but communication eligibility is not only "has an email". Agents should inspect:

- Email address.
- Phone number and SMS enabled.
- Communication preferences.
- Unsubscribe records.
- Communication lists and segments.
- Communication recipient history.
- Nameless people flows.
- SMS pipeline workflows.
- Family or registrar relationships for event registration.
- Notification messages for mobile.

RockU includes Nameless People in communication training ([Nameless People](https://community.rockrms.com/rocku/communication/nameless-people)). Mobile docs describe Notification Messages as persistent, actionable in-app inbox messages scoped to the currently logged-in person, expiring after 90 days and hidden for unauthenticated visitors ([Notification Messages](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/notification-messages)). The source pack does not provide full communication schema, so live inspection is required for delivery issues.

### Check-In

Check-in consumes people, families, known relationships, group membership, attributes, schedules, locations, security codes, labels, and device/kiosk configuration.

Official and source-backed points:

- RockU Check-In covers configuration, locations, schedules, types and groups, settings, devices, running check-in, attendance analytics, check-in manager, rapid attendance entry, person attributes in check-in manager, mobile check-in, self-entry, and celebrations ([Check-In](https://community.rockrms.com/rocku/check-in)).
- Attendance records include `PersonAliasId`, start date/time, RSVP, did attend, schedule id, group id, and Sunday date ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)).
- Check-in family search source resolves family groups and person record type ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)).
- Check-in relationships source uses known relationship roles with `CanCheckin` ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)).
- Check-in security codes settings define alpha-numeric, alpha, numeric lengths, random numeric behavior, and whether one code is reused across a family check-in ([CheckInSecurityCodesSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs)).
- Next-Gen Check-In default security was updated through a v16.7 migration assigning view permissions to administrators, staff, staff-like members, and denying all users by default on the site ([UpdateNextGenCheckInDefaultSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2016.0/Version%201.16.7/202411182318196_UpdateNextGenCheckInDefaultSecurity.cs)).

Version caveats:

- v17.1 fixed Next-Gen Check-In family sorting alphabetically like legacy check-in.
- v17.5 fixed removal of an individual with a `Can Check-In` known relationship under specific configuration.
- v18.1 added default Record Source for new person records created during Check-in.
- v19.1 release notes include multiple check-in and label improvements in the hydrated release excerpt ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 12. Administration And Operational Guardrails

### Person Data Is High Impact

Person/family changes can affect:

- Child safety and check-in authorization.
- Financial statements and family giving.
- Security role access.
- Ministry eligibility.
- Communication opt-ins and unsubscribes.
- Background checks.
- Event registrations and payments.
- Workflow assignments.
- Data views and automation.
- Reporting and analytics.

Agents should default to read-only diagnosis until the user explicitly asks for writes or the task clearly requires a controlled change. For writes, prefer Rock UI or supported APIs over direct SQL. Use direct SQL only when Rock's supported tools cannot perform the work, the query is reviewed, and there is a backup/rollback plan.

### Before Creating A Person

Checklist:

- Search by full name and nickname.
- Search by phone number.
- Search by email.
- Search by birthdate.
- Search by spouse/family.
- Search inactive records if appropriate.
- Search aliases if working at SQL/API level.
- Check nameless or partial records if the source is SMS, giving, or form entry.
- Confirm record type and connection status.
- Confirm record source settings if v18.1+.
- Confirm family placement.

### Before Editing A Family

Checklist:

- Confirm target family group.
- Confirm all members and roles.
- Confirm active/inactive status.
- Confirm address and campus.
- Confirm known relationships.
- Confirm giving settings for adults.
- Confirm check-in eligibility impact.
- Confirm event registration impact.
- Confirm communication impact.
- Confirm workflow automation triggers.

### Before Merging

Checklist:

- Confirm same person with multiple evidence points.
- Decide surviving record.
- Preserve the better photo/contact fields.
- Compare attributes and notes.
- Compare logins.
- Compare giving and statements.
- Compare group memberships and security roles.
- Compare known relationships.
- Compare attendance/check-in.
- Compare workflow attributes.
- Check custom systems that store raw person ids.
- After merge, verify aliases.

### Before Deactivating

Checklist:

- Confirm not needed for active check-in, serving, security, workflows, or communications.
- Understand whether deactivation removes or inactivates group memberships.
- Confirm logins/security roles.
- Confirm whether automation jobs react to record status.
- Confirm whether the person is in a family with active members.
- Add a note or history reason if organizational practice requires it.

### Before Deleting

Checklist:

- Confirm deletion is allowed by policy.
- Confirm no giving, attendance, registration, security, workflow, background check, or legal retention concerns.
- Use Rock UI dependency warnings.
- Do not bypass with direct SQL unless performing a reviewed, backed-up remediation.

### Before Exposing Person Data In Lava Or Dynamic Data

Checklist:

- Is this internal or external?
- Does the page require login?
- Does block security inherit safely?
- Are attributes sensitive?
- Is attribute security respected?
- Are entity command security settings safe?
- Does the query filter to the current person where needed?
- Does the output expose family members, registrations, giving, or minors?
- Does the Lava use person alias or person id correctly?
- Is the report performant?

### Data Integrity Monitoring

Useful recurring audits:

- Duplicate candidates by name/email/phone/birthdate.
- Inactive people with active logins.
- Active people with no family.
- Children with no adult in family.
- Adults with children in separate family and no known relationship.
- People with no primary alias.
- Person attributes missing required values.
- Person field type attributes storing invalid alias GUIDs.
- Family groups without active members.
- Families without home address.
- Active check-in children missing birthdate/grade where required.
- People with SMS enabled but no mobile phone.
- People with email communication enabled but no email.
- Recently created records by source.
- Recently modified sensitive attributes.
- Photos coverage if profile photos are operationally important.

## 13. Developer, API, Lava, And Source-Code Landmarks

### PersonAlias Service

The developer guide shows `PersonAliasService.GetByAliasId( int aliasId )` as the service pattern for resolving a known alias id to a person alias and current person ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)). Agents writing C# or reviewing plugins should look for:

- Raw `PersonId` foreign keys in custom models.
- `PersonAliasId` foreign keys in durable references.
- Alias GUIDs in workflow attributes.
- Merge safety in queries.

### Person Entity Lava Command

Lava can query people with the entity command:

- `where`
- `id`
- `ids`
- `dataview`
- `sort`
- `offset`
- `limit`
- `include`
- `select`
- `groupby`
- attribute prefetch controls

RockU and Lava docs both show person entity command examples ([Entity Commands RockU](https://community.rockrms.com/rocku/lava/entity-commands), [Entity Commands](https://community.rockrms.com/lava/commands/entity-commands)). Use entity commands cautiously in public contexts. Keep limits explicit when listing people.

### Person Lava Filters

Important filters from the source excerpt include:

- `Address`
- `Campus`
- `Children`
- `FamilySalutation`
- `Group`
- `Groups`
- `GroupsAttended`
- `HeadOfHousehold`
- `IsInSecurityRole`
- `LastAttendedGroupOfType`
- `NearestCampus`
- `Parents`
- `PersonByAliasGuid`
- `PersonByAliasId`
- `PersonByGuid`
- `PersonById`
- token/action identifier filters ([Person Filters](https://community.rockrms.com/lava/filters/person-filters))

Before using filters in production, inspect the live Lava docs for the target version because the pack lists many version additions across v1.0 through v18.0.

### Attribute Filters

Use `{{ Entity | Attribute:'Key' }}` for formatted values and optional qualifiers for entity properties or objects. Use `RawValue` for workflow attribute raw values where documented. Use the v17.5+ security bypass parameter only in reviewed internal contexts ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters), [Workflows and Lava](https://community.rockrms.com/lava/workflows)).

### AttributeValuesContainer

For C# blocks, Developer 303 shows:

- `LoadAttributes()`
- `AddDisplayControls( entity, Authorization.VIEW, CurrentPerson )`
- `AddEditControls( entity )` or security-aware overloads
- `GetEditValues( entity )`
- saving entity and attribute values inside a transaction ([Attributes](https://community.rockrms.com/developer/303---blast-off/attributes))

This is the preferred pattern for custom blocks that edit attributes.

### SetPersonAttribute Workflow Action

The source file `SetPersonAttribute.cs` describes a workflow action component named "Person Attribute Set" that updates a person attribute for a workflow-provided person. The snippet shows it accepts a workflow `Person` attribute, a target person attribute, and a value/text-or-attribute input; it resolves value merge fields or workflow attribute values, resolves the workflow person through a person alias GUID, loads person attributes, and updates the selected attribute ([SetPersonAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/SetPersonAttribute.cs)).

Agent use:

- Inspect workflow action settings.
- Confirm the Person workflow attribute uses Person field type.
- Confirm target person attribute GUID/key.
- Confirm value source and merge fields.
- Confirm whether the workflow person attribute contains the alias GUID expected.

### PersonAttributeForms Block

Source snippets show `PersonAttributeForms` has block settings for progress bar, save timing (`PAGE` or `END`), workflow launched on completion, done page, and forms configuration. The markup includes per-field settings such as person attribute, use current value, required in initial entry, pre-HTML, and post-HTML ([PersonAttributeForms.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Crm/PersonAttributeForms.ascx), [PersonAttributeForms.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Crm/PersonAttributeForms.ascx.cs)).

Agent use:

- Inspect block settings before assuming an attribute form writes immediately.
- Check whether save happens per page or at end.
- Check whether a workflow launches after completion.
- Check whether pre/post HTML includes Lava or UI behavior.
- Check required settings per field.

### Mobile Person Profile Block

Mobile Person Profile docs describe a block that displays and edits information about a person. It requires person context configured through page settings, including the Person Parameter Name of context parameters. Configuration includes phone types, header template, commands like `ShowEdit` subject to security authorization, custom actions template, badge bar template, demographics panel, contact information panel, reminder page, and styling ([Person Profile](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/person-profile)).

Agent use:

- Verify person context parameter.
- Verify security for editing.
- Verify configured phone types.
- Verify whether demographics/contact panels are shown.
- Verify templates for Lava and commands.

### Mobile Group Members Block

Mobile Group Members docs describe displaying other members of the same group type for a person context, commonly family members. Settings include members template, group type, auto-create group, group edit page, and styling ([Group Members](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)).

Agent use:

- Verify group type is Family.
- Verify person context.
- Verify whether auto-create group is enabled.
- Verify edit page link.
- Inspect template for security-sensitive output.

### Check-In Source Landmarks

Key files in the pack:

- `FindFamilies.cs`: check-in workflow action that finds families by search criteria and initializes check-in families ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)).
- `FindRelationships.cs`: check-in workflow action that finds people related to members of the selected family via known relationships and `CanCheckin` roles ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)).
- `SearchForFamiliesOptionsBag.cs` and `SearchForFamiliesResponseBag.cs`: REST view models for check-in family search options and results ([SearchForFamiliesOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Rest/CheckIn/SearchForFamiliesOptionsBag.cs), [SearchForFamiliesResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Rest/CheckIn/SearchForFamiliesResponseBag.cs)).
- `EditFamilyResponseBag.cs`, `SaveFamilyOptionsBag.cs`, and related TypeScript files: Next-Gen Check-In family edit/save view models ([EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs), [SaveFamilyOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyOptionsBag.cs)).
- `CheckInChildRelationshipSettingsBag.cs`: settings for known relationship types used when adding children ([CheckInChildRelationshipSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInChildRelationshipSettingsBag.cs)).
- `CheckInSecurityCodesSettingsBag.cs`: security code settings for labels ([CheckInSecurityCodesSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs)).
- `DateAttributeFieldDataSource.cs`: Next-Gen label data source reading date/date-time attributes from label data entities ([DateAttributeFieldDataSource.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/DateAttributeFieldDataSource.cs)).
- `SecurityCodeAndNameDataFormatter.cs`: formats label security code and nickname variants ([SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs)).

### Observe Lava Tag

For performance diagnostics in Lava, the `observe` tag wraps Lava in an observability activity and can tag the activity with feature metadata. The docs show use around a family/person list and note that `name` is required ([Observe](https://community.rockrms.com/lava/tags/observe)). Use this for expensive person/family templates in internal contexts where observability is configured.

## 14. Reporting, Analytics, And Model Map

### Person Reports

Person reports often fail because they join the wrong identity layer or ignore family/group membership. Agents should choose the join shape based on the question:

- Individual profile fields: `Person`.
- Durable historic references: `PersonAlias`.
- Family membership: `GroupMember` joined to family group type.
- Attributes: `AttributeValue` joined to `Attribute`, `FieldType`, and `EntityType`.
- Attendance: `Attendance.PersonAliasId`.
- Communication recipients: inspect current communication schema.
- Workflows: workflow attribute values, often storing alias GUIDs.
- Giving: financial tables and family giving settings.
- Security: group membership in security role groups.

The Model Map source confirms `Person Alias` is a CRM model, but the hydrated page excerpt is empty beyond metadata ([Model Map](https://community.rockrms.com/ModelMap)). Use the live Model Map for current entity details.

### Attribute Reporting

Attribute reporting requires correct field type interpretation. The Advanced Entity Guide says `AttributeValue.Value` is a string representation, with typed columns such as numeric, date/time, boolean, and person id ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)). Source helper SQL demonstrates the basic join for person attribute values ([View_PersonAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_PersonAttributeValues.sql)).

Agent pattern:

```sql
-- Conceptual shape only. Verify table names and field types in the live version.
AttributeValue
JOIN Attribute ON Attribute.Id = AttributeValue.AttributeId
JOIN EntityType ON EntityType.Id = Attribute.EntityTypeId
JOIN FieldType ON FieldType.Id = Attribute.FieldTypeId
JOIN Person ON Person.Id = AttributeValue.EntityId
WHERE EntityType.Name = 'Rock.Model.Person'
```

Do not run or ship SQL from this guide without adapting to the live schema, security model, and reporting tool.

### Family Reporting

Family reporting should begin with the family group type. Avoid grouping people by last name and calling that a family. The community attendance recipe highlights why last-name sorting is not family grouping: children may have different last names, and unrelated families may share a last name ([Sort Attendance By Family](https://community.rockrms.com/recipes/115)).

Family report checks:

- Group type is Family.
- Group members are active or intentionally include inactive.
- Roles distinguish adults and children.
- Family group is active.
- Family address exists.
- Known relationships are included only if the report explicitly needs them.
- Family giving and registration reports handle individual vs household behavior correctly.

### BI Family Report

RockU includes a BI Family Report lesson and links a Power BI template for Rock RMS v7 ([BI Family Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report)). Because the pack only includes training metadata and a template link, use it as a coverage signal rather than a current schema reference. For modern BI, inspect the live BI job, model definitions, persisted datasets, and current version docs.

### Data Views And Automation

Data Views are common predicates for person automation. Community examples use Data Views plus Group Sync plus workflow triggers for background check expiry, absentee follow-up, and new-person connection requests ([Run Workflow When Someone Enters a Dataview](https://community.rockrms.com/recipes/113), [Absentee Follow up Process using Connection Requests, Data Views and Jobs](https://community.rockrms.com/recipes/304), [Auto Create Connection Requests for New People](https://community.rockrms.com/recipes/251)). Use these patterns carefully:

- Confirm Data View scope.
- Add exclusion criteria.
- Test counts.
- Avoid sending automated communication without review.
- Prevent duplicate workflow launches.
- Log actions.
- Monitor job errors.

### Profile Custom Reports

Community recipes add profile tabs or panels for registrations, created/modified dates, staff directories, fundraising donors, bookmarked groups, and workflow people ([Show Created/Modified Dates on a Person Profile](https://community.rockrms.com/recipes/288), [Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344), [Internal Staff Directory](https://community.rockrms.com/recipes/341), [Add a Person Page tab to show a person's Fundraising Opportunity donors](https://community.rockrms.com/recipes/502), [Add a Bookmarked Groups Panel to the Person Profile](https://community.rockrms.com/recipes/282), [Finding People from Workflows](https://community.rockrms.com/recipes/437)).

These patterns are useful, but agents must review:

- Page security.
- Block security.
- SQL command permissions.
- Person context parameter.
- Whether the output includes minors, giving, registrations, workflows, or sensitive attributes.
- Whether recipes account for existing Rock security.

## 15. Version And Release Caveats

Version caveats from the source pack:

### v16.3

The Get Avatar handler was updated to correctly set a person's profile photo regardless of binary file type when updated by workflow. If profile photos updated by workflow still show default avatars, inspect version and file type handling ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v16.5

A CRM bug was fixed where editing a family's Record Status could show an incorrect deceased-person alert even when no deceased people were in the family ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v16.7

Group role check-in permission appears in group docs as "Is Check-in Allowed" for roles when the check-in rule is already enrolled in group ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). Source also includes a v16.7 migration for Next-Gen Check-In default security ([UpdateNextGenCheckInDefaultSecurity.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2016.0/Version%201.16.7/202411182318196_UpdateNextGenCheckInDefaultSecurity.cs)).

### v17.1

Next-Gen Check-In family search sorting was fixed so families sort alphabetically by name like legacy check-in. If a check-in kiosk on an older version presents confusing ordering, this may be relevant ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v17.2

New adults added to an existing family through Family Registration were fixed to use Combined Giving instead of Individual Giving. Inspect adult giving settings after family registration on older versions ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v17.5

Removing an individual with a `Can Check-In` known relationship had a fix for a specific configuration. If kiosk removal errors occur around known relationships, check version and relationship configuration ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Attribute filter security behavior changed in v17.5+ with a third optional parameter allowing bypass of attribute-level security checks. Use with caution ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### v18.1

CRM added or improved Person Record Source support in Get Person From Fields, internal Add Family, and default new-person creation during Check-in ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Finance fixed Statement Generator behavior for a single individual after a Data View had been used previously ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Workflow fixed Obsidian Workflow Entry behavior around Person and Spouse attributes when "Hide if Current Person Known" is enabled, and fixed blank spouse person record creation in some non-logged-in Person Entry scenarios ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v18.2

Core fixed Attribute Editor configuration changes for attributes designed to store other attributes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Event fixed registration behavior so hiding SMS opt-in no longer disables an individual's SMS setting ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Finance fixed Benevolence Request creation from a Person Profile so it automatically associates the current person ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### v18.3

Finance fixed Giving History API issues around family giving and giving across an individual's other records ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Triumph's v18.3 spotlight notes a Person Entry workflow action fix where Marital Status defaulted to "Married" when no value was provided and Autofill Current Person was disabled ([GitHub Spotlight: 4/8/2026](https://www.triumph.tech/resources/github-spotlight-482026)). Verify against official release notes and target build before relying on the partner summary.

### v19.1

Core fixed category dropdown behavior in multiple attribute editing blocks, where global attribute categories could appear instead of categories for the actual entity type ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Event added registrant eligibility rules to the Registration Template Detail Block and changed Registration Entry family member dropdown behavior to require intentional selection when family registrants are enabled. Eligibility can include age, grade, gender, and age classification ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Event fixed Event Occurrence Attribute validation in Event Item Detail ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 16. Implementation Playbooks

### Playbook: Build A Person Attribute

Use when a ministry needs a new field on person records.

1. Confirm the field belongs on the person, not the family, group member, workflow, campus, or known relationship.
2. Define the key in stable PascalCase or local convention.
3. Choose field type.
4. Add description and category.
5. Decide required status.
6. Decide whether it should appear in grids.
7. Set security if sensitive.
8. Test on a sample person.
9. Verify Lava access: `{{ Person | Attribute:'Key' }}`.
10. Verify report access by joining `AttributeValue` to `Attribute`.
11. If source-controlled, add migration with stable GUIDs.

Citations: attribute entity/value model ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)), C# attribute container ([Attributes](https://community.rockrms.com/developer/303---blast-off/attributes)), Lava attribute filter ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### Playbook: Build A Family Attribute

Use when a household-level field applies once per family.

1. Confirm "family" is a group.
2. Identify the family group type.
3. Add a group or group-type-scoped attribute, not a person attribute.
4. Choose field type and category.
5. Add it to the appropriate family edit/profile surface.
6. Test family edit and display.
7. Verify reports join to the group entity, not person.
8. Verify check-in or registration surfaces if the attribute appears there.

Citations: family attributes RockU ([Family Attributes](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes)), group model behavior ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

### Playbook: Build A New Person Entry Workflow

Use when a public or internal workflow collects person details.

1. Identify whether the workflow should find an existing person or create a new person.
2. Configure person attributes and spouse behavior carefully.
3. On v18.1+, configure Record Source if applicable.
4. Avoid blank spouse records by checking version and Person Entry settings.
5. Store person values using Person field type where appropriate.
6. Remember raw values may be person alias GUIDs.
7. Add validation for required fields.
8. Add duplicate review workflow if high risk.
9. Add data integrity notification.
10. Test unauthenticated, authenticated, current person known, and spouse blank scenarios.

Citations: workflow person entry training ([Workflow Person Entry](https://community.rockrms.com/rocku/workflows/workflow-person-entry)), workflow Lava person raw value ([Workflows and Lava](https://community.rockrms.com/lava/workflows)), release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Playbook: Add A Person Profile Panel

Use when a staff-facing person page needs a custom panel.

1. Identify the person context parameter.
2. Decide whether the data is safe to display.
3. Choose a supported block: HTML Content, Dynamic Data, custom block, Attribute Values, or mobile block.
4. Set page and block security.
5. If using Lava, enable only required commands.
6. If using SQL, sanitize page parameters and avoid public exposure.
7. Use `PersonAlias` where historic references matter.
8. Limit results and account for security.
9. Test as admin, staff, and unauthorized user.
10. Document the customization.

Citations: block security docs ([Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)), security warning example ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)), entity commands ([Entity Commands](https://community.rockrms.com/lava/commands/entity-commands)).

### Playbook: Diagnose Missing Check-In Family

Use when a family or person cannot be found at check-in.

1. Confirm search type and search value.
2. Search by another method: phone, name, barcode, birthdate, address.
3. Confirm person record type is Person.
4. Confirm person record status is active unless inactive people are allowed.
5. Confirm family group membership.
6. Confirm family group type.
7. Confirm group member status.
8. Confirm phone number normalization if phone search.
9. Confirm kiosk/configuration template.
10. Confirm whether family is associated with kiosk campus if campus prioritization or filtering is enabled.
11. Confirm known relationships if expecting non-family children/adults.
12. Check version for known check-in fixes.

Citations: Check-In RockU ([Check-In](https://community.rockrms.com/rocku/check-in)), family search source ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)), known relationship source ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)), release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Playbook: Safely Merge Duplicate People

Use when duplicate records need cleanup.

1. Collect both person ids, guids, and primary aliases.
2. Compare identity, family, contact, and history.
3. Compare financial and check-in surfaces.
4. Compare logins and security roles.
5. Compare attributes and notes.
6. Decide survivor.
7. Use Rock merge UI.
8. Verify all aliases point to survivor.
9. Verify dependent surfaces.
10. Add a note if required by local data policy.

Citations: merge training ([Merging Duplicate Records](https://community.rockrms.com/rocku/individuals-in-rock/merging-duplicate-records)), alias guidance ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

### Playbook: Recover From Wrong Merge

Use only for incident response.

1. Stop further edits to affected records if possible.
2. Identify merge time and actors.
3. Identify survivor and merged-away person.
4. Restore a point-in-time database copy for inspection, not overwrite.
5. Compare aliases and affected tables.
6. Prefer vendor/core-supported guidance if available.
7. If using community scripts/tools, run preview/rollback first.
8. Validate impacted tables before commit.
9. Verify profile, aliases, group memberships, giving, attendance, workflows, attributes, notes, and logins after recovery.
10. Document exactly what changed.

Citations: community recovery patterns ([Recovering a Merged Person](https://community.rockrms.com/recipes/184), [Unmerge Accidentally Merged Person with Alias Detection](https://community.rockrms.com/recipes/474/unmerge-accidentally-merged-person-with-alias-detection), [Rock Unmerge Profiles Tool](https://community.rockrms.com/recipes/541)).

### Playbook: Build A Family Registration Or Pre-Registration Flow

Use when collecting new household information.

1. Choose public family pre-registration, check-in registration, workflow, or custom form.
2. Define required family address fields.
3. Define adult and child required fields separately.
4. Define family attributes, adult attributes, and child attributes.
5. Define child relationship types.
6. Decide whether children are added to the parent's family or a new family with relationship.
7. Decide check-in after registration behavior.
8. Configure record source on v18.1+.
9. Configure SMS opt-in behavior and verify v18.2+ behavior if applicable.
10. Add data integrity review after submission.

Citations: Family Pre-Registration RockU ([Family Pre-Registration](https://community.rockrms.com/rocku/cms/family-pre-registration)), check-in family edit source ([EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs)), child relationship settings ([CheckInChildRelationshipSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInChildRelationshipSettingsBag.cs)), release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 17. Troubleshooting Decision Tree

### Person Does Not Appear In Search

1. Is the search surface staff UI, mobile Smart Search, check-in, Lava, or custom SQL?
2. Is the search type supported by that surface?
3. Is the person active?
4. Is the record type a person?
5. Does the search include inactive records?
6. Is the name stored in `NickName`, `FirstName`, or another field?
7. Is phone normalized correctly?
8. Is email on the correct person record?
9. Was the person merged into another record?
10. Does the search need aliases?
11. Does the block have correct security/context?

Sources: Smart Search ([Smart Search](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search)), check-in family search ([FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)), alias guidance ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

### Family Members Are Wrong

1. Is the displayed "family" actually a family group?
2. Is the person in more than one family group?
3. Which group is primary?
4. Are inactive members hidden?
5. Are group member roles correct?
6. Are known relationships being displayed as family members?
7. Did check-in registration add a child to a new family with relationship instead of the parent's family?
8. Was there a bad merge?
9. Did a family registration or edit flow recently run?

Sources: Group Members mobile docs ([Group Members](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)), child relationship settings ([CheckInChildRelationshipSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInChildRelationshipSettingsBag.cs)), known relationships ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)).

### Person Attribute Does Not Display

1. Does the attribute definition exist?
2. Is the entity type `Rock.Model.Person`?
3. Is the category displayed by the block?
4. Does the current user have view access?
5. Does an `AttributeValue` row exist for the person?
6. Is the field type supported by the display surface?
7. Is the value cached?
8. Is the Lava key correct?
9. Did v17.5+ attribute security affect the output?
10. Is the block's entity context actually the person?

Sources: Attribute model ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide)), Attribute filters ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)), mobile Attribute Values block ([Attribute Values](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)).

### Workflow Person Attribute Resolves Wrong Person

1. Inspect the workflow attribute field type.
2. Inspect raw value.
3. Is it a person alias GUID?
4. Resolve through `PersonAlias`, not `Person.Id`.
5. Was the person merged?
6. Does the workflow hide/autofill current person?
7. Is spouse blank behavior affected by v18.1 bug fixes?
8. Does the workflow action use a value from another attribute?

Sources: Workflows and Lava ([Workflows and Lava](https://community.rockrms.com/lava/workflows)), SetPersonAttribute source ([SetPersonAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/SetPersonAttribute.cs)), release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Child Cannot Check In With Adult

1. Are they in the same family group?
2. Is the child active?
3. Is the adult active?
4. Does the selected family include the child?
5. Is a known relationship needed?
6. Does the relationship role have `CanCheckin`?
7. Does check-in prevent inactive related people?
8. Does group type/role allow check-in?
9. Do age, grade, gender, schedule, location, and capacity match?
10. Is the Rock version affected by v17.5 relationship removal bug or other check-in fixes?

Sources: FindRelationships ([FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)), group docs ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)), release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Registration Shows Wrong Family Member

1. Check Registration Template settings for same-family registrants.
2. Check v19.1 registrant eligibility settings if available.
3. Check age, grade, gender, and age classification.
4. Check whether Family Member to Register defaults blank in target version.
5. Check family group membership and active status.
6. Check whether the current person is registrar or family member.
7. Check custom Lava or workflow that changes registrar.

Sources: v19.1 release note ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)), outstanding balance family workaround as a caution ([Outstanding Registration Payment Accessible to All Family Members](https://community.rockrms.com/recipes/488)).

### Giving History Looks Wrong

1. Is the request for individual or family giving?
2. Is "Combine Giving With" blank or configured?
3. Does the API include family giving?
4. Are there multiple aliases or merged records?
5. Is Rock v18.3+ with Giving History API fixes?
6. Are statement generator filters stale from a Data View in v18.1 or earlier?

Sources: release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Profile Custom Tab Exposes Too Much

1. Check page security.
2. Check block security.
3. Check SQL/Lava command permissions.
4. Check whether the query filters to context person.
5. Check whether records have their own security, such as registration templates.
6. Check whether attributes bypass security.
7. Test as non-admin.
8. Remove or restrict until reviewed.

Sources: block security ([Customizing and Securing Blocks](https://community.rockrms.com/developer/quickstart-tutorials/blocks/customizing-and-securing-blocks)), registration tab security warning ([Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344)), attribute security ([Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

## 18. Agent Task Recipes

### Recipe: Identify A Person Safely

Collect:

- `Person.Id`
- `Person.Guid`
- `PrimaryAlias.Id`
- `PrimaryAlias.Guid`
- all aliases
- full name and nickname
- birthdate
- email
- phone numbers
- record status
- connection status
- family group id
- family role

Then verify whether any referenced workflow, attendance, communication, registration, or financial record uses `PersonAliasId` or alias GUID.

### Recipe: Explain Why `PersonAlias` Matters

Use this concise explanation:

Rock people can be duplicated and later merged. After a merge, the losing `Person.Id` may no longer be the correct active record. `PersonAlias` records remain and point to the current surviving person, so custom models should reference `PersonAlias` instead of raw `Person.Id` ([Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person)).

### Recipe: Inspect A Person Attribute

Inspect:

- Attribute key.
- Entity type.
- Qualifier column/value.
- Field type.
- Categories.
- Security.
- Attribute value row.
- Raw value.
- Formatted value.
- Typed persisted columns.
- Lava output.

Use official attribute docs as the model reference ([Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide), [Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters)).

### Recipe: Determine If A Value Is Person Id Or Alias Guid

1. If it came from a workflow Person attribute `RawValue`, treat it as person alias GUID until proven otherwise ([Workflows and Lava](https://community.rockrms.com/lava/workflows)).
2. If it is an integer ending in `PersonAliasId`, resolve through `PersonAlias`.
3. If it is an integer named `PersonId`, verify whether it is a current person id.
4. If it is a GUID, compare to `Person.Guid` and `PersonAlias.Guid`.
5. If the record survived a merge, search aliases.

### Recipe: Audit A Family For Check-In

Inspect:

- Family group.
- Members and roles.
- Active statuses.
- Known relationships.
- `CanCheckin` role attributes.
- Check-in configuration template.
- Relationship settings.
- Security code settings.
- Family search type.
- Schedules and locations.
- Age/grade/gender restrictions.
- Group type check-in rule.

Source landmarks: Check-In RockU ([Check-In](https://community.rockrms.com/rocku/check-in)), `FindFamilies.cs` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs)), `FindRelationships.cs` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs)).

### Recipe: Review A Person Profile Customization

1. Identify page route and context person parameter.
2. List all blocks on the page.
3. Check inherited and explicit security.
4. Check Lava commands enabled.
5. Check SQL commands enabled.
6. Review query filters.
7. Review whether data is registration, giving, workflow, minors, background check, or attributes.
8. Test unauthorized access.
9. Document the customization.

### Recipe: Triage An Accidental Merge

1. Do not create more edits until evidence is collected.
2. Identify merge timestamp and survivor.
3. Collect aliases before and after merge.
4. Inspect history and affected person surfaces.
5. Restore backup to separate database if recovery is required.
6. Use preview/rollback transaction for any script-based recovery.
7. Validate group membership, giving, attendance, attributes, notes, workflows, logins, and aliases.
8. Prefer expert review.

Community recovery references exist, but they are not core-endorsed ([Recovering a Merged Person](https://community.rockrms.com/recipes/184), [Unmerge Accidentally Merged Person with Alias Detection](https://community.rockrms.com/recipes/474/unmerge-accidentally-merged-person-with-alias-detection)).

### Recipe: Track New Record Source

1. Check Rock version.
2. If v18.1+, inspect Person Record Source configuration for Add Family, Get Person From Fields, and Check-in new records ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
3. Inspect person created date and created by alias.
4. Inspect history.
5. Inspect local "How Created" attributes only if defined.
6. Inspect source workflows and registrations.

### Recipe: Build A Staff Directory From Person Attributes

1. Create person attributes for staff hire date and title if not already present.
2. Set security to HR/staff admins as appropriate.
3. Use a report or Dynamic Data page only in secure internal context.
4. Join person attribute values by attribute id/key.
5. Exclude former staff using a clear status or attribute, not a magic date if avoidable.
6. Review community examples critically ([Internal Staff Directory](https://community.rockrms.com/recipes/341)).

### Recipe: Add A Bookmarked Groups-Like Profile Panel

A community recipe demonstrates a staff-personalized panel showing groups the current staff user follows and whether the viewed person is in them ([Add a Bookmarked Groups Panel to the Person Profile](https://community.rockrms.com/recipes/282)). To implement safely:

1. Verify group following entity type ids in live Rock.
2. Respect group security.
3. Filter by current person.
4. Filter by context person.
5. Limit output.
6. Test as users with different group access.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `82`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | implementation_pattern | Agents should inspect connection types, opportunities, statuses, activities, workflows, and staff ownership together because a connection request is both a person record and a process state. | [source](https://community.rockrms.com/rocku/engagement/overview) |
| rocku-confirmed | implementation_pattern | When troubleshooting connections, identify whether the problem is person context, request status, opportunity configuration, staff assignment, or automation rather than treating it as one generic workflow issue. | [source](https://community.rockrms.com/rocku/engagement/connections-overview) |
| rocku-confirmed | operational_guidance | Person Notes should be handled as structured staff context on a person record; note type, visibility, sensitivity, and lifecycle matter as much as the note text itself. | [source](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1) |
| rocku-confirmed | operational_guidance | Use Note Types to govern where notes appear, how they are categorized, and which staff roles can create or view sensitive notes; do not treat all person notes as one undifferentiated field. | [source](https://community.rockrms.com/rocku/core-concepts/note-types) |
| rocku-confirmed | operational_guidance | The Person Profile is a dense operational surface; agents should identify which tab, block, badge, note, attribute, or action is involved before troubleshooting or changing access. | [source](https://community.rockrms.com/rocku/individuals-in-rock/person-profile) |
| rocku-confirmed | operational_guidance | When diagnosing personalization, inspect the audience rule, person data used by the rule, fallback content, cache behavior, and the exact logged-in or anonymous state being tested. | [source](https://community.rockrms.com/rocku/cms/personalization) |
| rocku-confirmed | operational_guidance | Data integrity work should start from the exact entity and field being corrected, then identify the owner, source of truth, duplicate risk, and reporting impact before changing records. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| rocku-confirmed | operational_guidance | People and reporting guides should distinguish cleanup, merge, verification, and governance tasks because each has different audit and permission requirements. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) |
| rocku-confirmed | operational_guidance | Personalization should be reviewed as conditional content delivery, not as a security substitute; hidden or targeted content still needs proper page, block, and entity authorization. | [source](https://community.rockrms.com/rocku/cms/personalization) |
| rocku-confirmed | operational_guidance | When troubleshooting notes, inspect the person profile surface, note type, permissions, author/date metadata, and any workflow or report that consumes note data. | [source](https://community.rockrms.com/rocku/individuals-in-rock/person-note-1) |
| rocku-confirmed | operational_guidance | Connections work should be modeled as a ministry follow-up process: define the person, opportunity, connector, status, and next action before automating or reporting on the flow. | [source](https://community.rockrms.com/rocku/engagement/overview) |
| rocku-confirmed | operational_guidance | For reporting agents, data integrity issues should be surfaced as source-data problems, not hidden by report logic that masks duplicates, missing values, or stale attributes. | [source](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) |
| More |  | 70 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `24`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [BI Family Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report) | approved_for_public_distillation | 3 | media-insight:26c55120b777db34 |
| [Connections Overview Transcript Insight](https://community.rockrms.com/rocku/engagement/overview) | approved_for_public_distillation | 2 | media-insight:ac3acf7f8ce265ff |
| [Connections Overview Transcript Insight](https://community.rockrms.com/rocku/engagement/connections-overview) | approved_for_public_distillation | 2 | media-insight:f689579d363f61a6 |
| [Data Integrity Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity) | approved_for_public_distillation | 2 | media-insight:71943d00f00d6d5c |
| [Data Integrity Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/data-integrity-1) | approved_for_public_distillation | 2 | media-insight:8a7a44d45ee79557 |
| [Episode 94: Special Edition with Jay Nestle Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-94-special-edition-with-jay-nestle) | approved_for_public_distillation | 2 | media-insight:b5920a1a51b4ec4f |
| [Extending the Add Family Block Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/extending-the-add-family-block) | approved_for_public_distillation | 1 | media-insight:d556845e27d9ad0c |
| [Family Attributes Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes) | approved_for_public_distillation | 2 | media-insight:0e1933333f48c31e |
| More |  | 16 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

### Primary Official Sources

- [Using PersonAlias vs Person](https://community.rockrms.com/developer/101---launchpad/using-personalias-vs-person): primary authority for alias-vs-person custom data model guidance.
- [Advanced Entity Guide](https://community.rockrms.com/developer/202---ignition/advanced-entity-guide): primary authority for `Attendance`, `Attribute`, `AttributeValue`, notes, workflows, and entity concepts included in the pack.
- [Attributes](https://community.rockrms.com/developer/303---blast-off/attributes): primary authority for C# attribute view/edit/save patterns.
- [Extending Rock Even Further](https://community.rockrms.com/developer/303---blast-off/extending-rock-even-further): source for field types and field attributes.
- [Workflows and Lava](https://community.rockrms.com/lava/workflows): primary authority for workflow attribute raw values and field type storage notes.
- [Entity Commands](https://community.rockrms.com/lava/commands/entity-commands): primary authority for Lava entity command parameters, security, attribute prefetch, and performance-related options.
- [Attribute Filters](https://community.rockrms.com/lava/filters/attribute-filters): primary authority for Lava attribute access and v17.5+ attribute security parameter.
- [Person Filters](https://community.rockrms.com/lava/filters/person-filters): primary authority for person-specific Lava filters.
- [Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296): primary authority for group type, group security, check-in roles, group locations, attendance, and family-as-group implications.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): primary authority for version caveats listed in this guide.

### RockU Training Coverage

- [Individuals In Rock](https://community.rockrms.com/rocku/individuals-in-rock): training map for person profile, search, editing, notes, attributes, family attributes, known relationships, merges, delete, impersonation, data integrity, data automation, tags, background checks, badges, assessments, account protection, passwordless login, peer networks.
- [Searching for a Person](https://community.rockrms.com/rocku/individuals-in-rock/searching-for-a-person): search workflow coverage.
- [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile): profile workflow coverage.
- [Adding and Editing Individuals and Families](https://community.rockrms.com/rocku/individuals-in-rock/adding-and-editing-individuals-and-families): add/edit coverage.
- [Person Attributes](https://community.rockrms.com/rocku/individuals-in-rock/person-attributes): person attribute coverage.
- [Family Attributes](https://community.rockrms.com/rocku/individuals-in-rock/family-attributes): family attribute coverage.
- [Known Relationships](https://community.rockrms.com/rocku/individuals-in-rock/known-relationships): relationship coverage.
- [Merging Duplicate Records](https://community.rockrms.com/rocku/individuals-in-rock/merging-duplicate-records): merge workflow coverage.
- [Check-In](https://community.rockrms.com/rocku/check-in): check-in configuration and operation coverage.
- [Groups](https://community.rockrms.com/rocku/groups): group configuration and relationship-management coverage.
- [Workflow Person Entry](https://community.rockrms.com/rocku/workflows/workflow-person-entry): workflow person entry coverage.
- [Family Pre-Registration](https://community.rockrms.com/rocku/cms/family-pre-registration): family pre-registration coverage.
- [BI Family Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-family-report): BI family reporting coverage signal.

### Source-Code Landmarks

- [SetPersonAttribute.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/SetPersonAttribute.cs): workflow action for setting a person attribute from a workflow person/value context.
- [PersonAttributeForms.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Crm/PersonAttributeForms.ascx) and [PersonAttributeForms.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Crm/PersonAttributeForms.ascx.cs): person attribute forms block configuration and field UI.
- [View_PersonAttributeValues.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_PersonAttributeValues.sql): SQL join pattern for person attribute values.
- [CodeGen_AddUpdatePersonAttributes.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/CodeGen_AddUpdatePersonAttributes.sql): migration helper generation pattern for person attributes.
- [PersonAttributeValueCsvMapper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Slingshot/CSVMapper/PersonAttributeValueCsvMapper.cs): Slingshot person attribute value import mapping by attribute keys.
- [FindFamilies.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindFamilies.cs): check-in family search workflow implementation.
- [FindRelationships.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FindRelationships.cs): check-in known relationships workflow implementation.
- [SearchForFamiliesOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Rest/CheckIn/SearchForFamiliesOptionsBag.cs) and [SearchForFamiliesResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Rest/CheckIn/SearchForFamiliesResponseBag.cs): check-in family search REST models.
- [EditFamilyResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/EditFamilyResponseBag.cs), [SaveFamilyOptionsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/SaveFamilyOptionsBag.cs), and [SaveFamilyResponseBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/saveFamilyResponseBag.d.ts): Next-Gen Check-In family edit/save models.
- [CheckInChildRelationshipSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInChildRelationshipSettingsBag.cs): check-in child relationship settings.
- [CheckInSecurityCodesSettingsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInConfigurationSettings/CheckInSecurityCodesSettingsBag.cs): check-in label security code settings.
- [DateAttributeFieldDataSource.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/DateAttributeFieldDataSource.cs): label attribute data source.
- [SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs): label formatter for security code and nickname.

### Community Recipes Used As Examples Only

- [Recovering a Merged Person](https://community.rockrms.com/recipes/184): accidental merge recovery pattern using backup comparison and rollback/commit workflow.
- [Unmerge Accidentally Merged Person with Alias Detection](https://community.rockrms.com/recipes/474/unmerge-accidentally-merged-person-with-alias-detection): alias-aware unmerge script pattern.
- [Rock Unmerge Profiles Tool](https://community.rockrms.com/recipes/541): community tool for merge recovery.
- [Track How Person Records are Created](https://community.rockrms.com/recipes/223): local pattern for record creation source tracking through transient connection statuses and a person attribute.
- [Run Workflow When Someone Enters a Dataview](https://community.rockrms.com/recipes/113): Data View plus Group Sync plus workflow trigger pattern.
- [Auto Create Connection Requests for New People](https://community.rockrms.com/recipes/251): new-person connection workflow pattern.
- [Registrations Tab on Person Profile](https://community.rockrms.com/recipes/344): profile tab customization with explicit security caution.
- [Sort Attendance By Family](https://community.rockrms.com/recipes/115): example showing family grouping is not last-name sorting.
- [Undo Accidentally Deactivated People](https://community.rockrms.com/recipes/291): deactivation recovery pattern.
- [Buttonizing Rock Person Attributes](https://community.rockrms.com/recipes/159): profile UI compaction pattern for attribute blocks.
- [Internal Staff Directory](https://community.rockrms.com/recipes/341): staff directory via person attributes.
- [Outstanding Registration Payment Accessible to All Family Members](https://community.rockrms.com/recipes/488): family payment workaround with registrar-change caveats.

### Records Requiring Live Verification

The source pack does not include full current schema for every person/family table, full implementation of every profile block, or full official documentation for every training topic. Verify in a live Rock instance before depending on:

- Exact `Person` model property list.
- Exact family group type id and role ids.
- Local family attribute storage.
- Local campus assignment logic.
- Local connection statuses and record source values.
- Local "How Created" attributes.
- Local note types, tag security, badges, signals, and assessment attributes.
- Background check provider configuration.
- Communication preference and unsubscribe schema.
- Custom dynamic data pages and Lava blocks.
- Plugin-provided workflow actions or SQL reports.
- Version-specific check-in and registration behavior.
