# Entity Set Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `EntitySet`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `50e3f9c8-4010-41af-8f61-08308dc44640`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 17 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 17 |
| Related model links | 2 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChildEntitySets |  | yes | yes |  |  | Gets or sets the child entity sets. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntitySetAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EntitySetPurposeValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the EntitySet's purpose |
| EntitySetPurposeValueId | yes | yes |  |  |  | Gets or sets Id of the EntitySet purpose Defined Value representing the EntitySet's purpose. These are found in the Entity Set Purpose Defined Type. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the type of the entity. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the entity type identifier. |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the expire date time. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Items |  | yes | yes |  |  | Gets or sets the items. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name. |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentEntitySet |  | yes | yes |  |  | Gets or sets the parent entity set. |
| ParentEntitySetId | yes | yes |  |  |  | Gets or sets the parent entity set identifier. |
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
| ChildEntitySets | Gets or sets the child entity sets. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntitySetPurposeValue | Gets or sets the Defined Value representing the EntitySet's purpose |
| EntityStringValue |  |
| EntityType | Gets or sets the type of the entity. |
| IdKey |  |
| Items | Gets or sets the items. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentEntitySet | Gets or sets the parent entity set. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntitySetPurposeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| EntitySetPurposeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
