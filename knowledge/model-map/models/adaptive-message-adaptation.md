# Adaptive Message Adaptation Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CMS`
- Model title: `AdaptiveMessageAdaptation`
- EntityType GUID: `39753cce-184a-4f14-ae80-08241de8fc2e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 18 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 14 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdaptiveMessage |  | yes | yes |  |  | Gets or sets the adaptive message. |
| AdaptiveMessageAdaptationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AdaptiveMessageAdaptationSegments |  | yes | yes |  |  | Gets or sets the collection of AdaptiveMessageAdaptationSegments. |
| AdaptiveMessageId | yes | yes |  | yes |  | Gets or sets the adaptive message identifier. |
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
| EndDate | yes | yes |  |  |  | Gets or sets the end date of the AdaptiveMessageAdaptation. |
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
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StartDate | yes | yes |  |  |  | Gets or sets the optional start date of the AdaptiveMessageAdaptation. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| ViewSaturationCount | yes | yes |  |  |  | Gets or sets the view saturation count. |
| ViewSaturationInDays | yes | yes |  |  |  | Gets or sets the view saturation in days. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AdaptiveMessage | Gets or sets the adaptive message. |
| AdaptiveMessageAdaptationSegments | Gets or sets the collection of AdaptiveMessageAdaptationSegments. |
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
| EndDate | [AdaptiveMessageAdaptation](adaptive-message-adaptation.md) |  |
| StartDate | [AdaptiveMessageAdaptation](adaptive-message-adaptation.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
