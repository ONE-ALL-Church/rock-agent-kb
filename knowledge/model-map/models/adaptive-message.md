# Adaptive Message Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CMS`
- Model title: `AdaptiveMessage`
- EntityType GUID: `63d98f58-da81-46ae-ae0c-662a7bfaa7d0`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 15 |
| Lava-marked properties | 29 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdaptiveMessageAdaptations |  | yes | yes |  |  | Gets or sets the collection of AdaptiveMessageAdaptations. |
| AdaptiveMessageAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AdaptiveMessageCategories |  | yes | yes |  |  | Gets or sets the collection of Categories that this Adaptive Message is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
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
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EncryptedKey |  |  | yes |  |  |  |
| EndDate | yes | yes |  |  |  | Gets or sets the end date of the Adaptive Message. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  |  |  | Gets or sets the key. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StartDate | yes | yes |  |  |  | Gets or sets the optional start date of the Adaptive Message. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AdaptiveMessageAdaptations | Gets or sets the collection of AdaptiveMessageAdaptations. |
| AdaptiveMessageCategories | Gets or sets the collection of Categories that this Adaptive Message is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AdaptiveMessageCategories | [Adaptive Message](adaptive-message.md) | 63d98f58-da81-46ae-ae0c-662a7bfaa7d0 |
| AdaptiveMessageCategories | Categories | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| EndDate | [Adaptive Message](adaptive-message.md) | 63d98f58-da81-46ae-ae0c-662a7bfaa7d0 |
| StartDate | [Adaptive Message](adaptive-message.md) | 63d98f58-da81-46ae-ae0c-662a7bfaa7d0 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
