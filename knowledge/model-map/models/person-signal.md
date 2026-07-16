# Person Signal Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `PersonSignal`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `0fff77a1-e92d-4a05-8b36-1d2b6d46660f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 14 |
| Lava-marked properties | 29 |
| Lava-marked non-database properties | 15 |
| Related model links | 4 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
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
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpirationDate | yes | yes |  |  |  | Gets or sets the date this signal expires. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note applied to this signal. |
| OwnerPersonAlias |  | yes | yes |  |  | Gets or sets the person alias of the individual that reported this signal. |
| OwnerPersonAliasId | yes | yes |  | yes |  | Gets or sets the person alias identifier of the individual that reported this signal. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority of this PersonSignal. Where security is inherited from. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Person |  | yes | yes |  |  | Gets or sets the Person representing the person who has the signal applied to them. |
| PersonId | yes | yes |  | yes |  | Gets or sets the Id of the Person that is represented by the PersonSignal. This property is required. |
| PersonSignalAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SignalType |  | yes | yes |  |  | Gets or sets the Signal Type representing the signal that has been applied. |
| SignalTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Signal Type that is represented by the PersonSignal. This property is required. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OwnerPersonAlias | Gets or sets the person alias of the individual that reported this signal. |
| Person | Gets or sets the Person representing the person who has the signal applied to them. |
| SignalType | Gets or sets the Signal Type representing the signal that has been applied. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Person | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PersonId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| SignalType | [Signal Type](signal-type.md) | 0ba03b9b-e974-4526-9b21-5037424b6d16 |
| SignalTypeId | [Signal Type](signal-type.md) | 0ba03b9b-e974-4526-9b21-5037424b6d16 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
