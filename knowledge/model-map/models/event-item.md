# Event Item Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `EventItem`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `42`
- Obsolete methods: `4`
- EntityType GUID: `6a58ad11-3491-84ae-4896-8f39906ea65e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 19 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 17 |
| Related model links | 7 |
| Method signatures | 42 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowsInteractiveBulkIndexing | yes |  |  |  |  | Gets a value indicating whether [allows interactive bulk indexing]. |
| ApprovedByPersonAlias |  | yes | yes |  |  | Gets or sets the approved by Person Alias. |
| ApprovedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonId of the Person who approved this event. |
| ApprovedOnDateTime | yes | yes |  |  |  | Gets or sets the date this event was approved. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the Description of the EventItem. |
| DetailsUrl | yes | yes |  |  |  | Gets or sets the URL for an external event. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EventCalendarItems |  | yes | yes |  |  | Gets or sets a collection of the EventCalendarItems that belong to this EventItem. |
| EventItemAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EventItemAudiences |  | yes | yes |  |  | Gets or sets a collection of the EventItemAudiences that belong to this EventItem. |
| EventItemOccurrences |  | yes | yes |  |  | Gets or sets a collection of the EventItemOccurrence that belong to this EventItem. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets the is active. |
| IsApproved | yes | yes |  |  |  | Gets or sets a flag indicating if the event has been approved. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the EventItem. This property is required. |
| NextStartDateTime |  |  | yes |  |  | Gets the next start date time. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Photo |  | yes | yes |  |  | Gets or sets the Binary File that contains the EventItem's photo. |
| PhotoId | yes | yes |  |  |  | Gets or sets the Id of the Binary File that contains the photo of the EventItem. |
| Summary | yes | yes |  |  |  | Gets or sets the Summary of the EventItem. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ApprovedByPersonAlias | Gets or sets the approved by Person Alias. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EventCalendarItems | Gets or sets a collection of the EventCalendarItems that belong to this EventItem. |
| EventItemAudiences | Gets or sets a collection of the EventItemAudiences that belong to this EventItem. |
| EventItemOccurrences | Gets or sets a collection of the EventItemOccurrence that belong to this EventItem. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Photo | Gets or sets the Binary File that contains the EventItem's photo. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ApprovedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ApprovedByPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| EventCalendarItems | EventCalendarItems | e37fb26f-03f6-48da-8e96-f412616f5ee4 |
| EventItemAudiences | EventItemAudiences | 22394315-e21b-40af-afda-75d9f5dad721 |
| EventItemOccurrences | [EventItemOccurrence](event-item-occurrence.md) | 71632e1a-1e7f-42b9-a630-ec99f375303a |
| Photo | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |
| PhotoId | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
