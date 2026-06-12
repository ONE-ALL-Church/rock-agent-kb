# Connection Status Automation Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `ConnectionStatusAutomation`
- EntityType GUID: `acf794c7-f12d-42df-85c5-089a28993ee6`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 15 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 15 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutomationName | yes | yes |  | yes |  | Gets or sets the automation name. |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionStatusAutomationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  | yes | yes |  |  | Gets or sets the DataView. |
| DataViewId | yes | yes |  |  |  | Gets or sets the DataView identifier. |
| DestinationStatus |  | yes | yes |  |  | Gets or sets the destination ConnectionStatus. |
| DestinationStatusId | yes | yes |  | yes |  | Gets or sets the destination ConnectionStatus identifier. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupRequirementsFilter | yes | yes |  |  |  | Gets or sets the Group Requirements filter. This is a hard coded list of values defined in the code as an enumeration. |
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
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SourceStatus |  | yes | yes |  |  | Gets or sets the ConnectionStatus. |
| SourceStatusId | yes | yes |  | yes |  | Gets or sets the source ConnectionStatus identifier. |
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
| DataView | Gets or sets the DataView. |
| DestinationStatus | Gets or sets the destination ConnectionStatus. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SourceStatus | Gets or sets the ConnectionStatus. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DataView | [DataView](data-view.md) |  |
| DataViewId | [DataView](data-view.md) |  |
| DestinationStatus | [ConnectionStatus](connection-status.md) |  |
| DestinationStatusId | [ConnectionStatus](connection-status.md) |  |
| SourceStatus | [ConnectionStatus](connection-status.md) |  |
| SourceStatusId | [ConnectionStatus](connection-status.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
