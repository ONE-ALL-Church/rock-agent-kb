# Connection Status Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `ConnectionStatus`
- EntityType GUID: `f3840c8b-63bf-4f98-ac4a-9336896e589b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 22 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 14 |
| Related model links | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutoFutureFollowUpPauseInDays | yes | yes |  |  |  | When set, automatically moves the request to Future Follow-Up for the specified number of days. Leave blank to disable this behavior. |
| AutoInactivateState | yes | yes |  |  |  | Gets or sets a value indicating whether choosing this Status will set the Request's State to Inactive. |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionStatusAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionStatusAutomations |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionStatusAutomations who are associated with the Connection Status. |
| ConnectionType |  | yes | yes |  |  | Gets or sets the type of the connection. |
| ConnectionTypeId | yes | yes |  |  |  | Gets or sets the Connection Type identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HighlightColor | yes | yes |  |  |  | Gets or sets the color of the highlight. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsCritical | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is critical. |
| IsDefault | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is default. |
| IsNoteRequiredOnCompletion | yes | yes |  |  |  | Indicates whether completing a request requires entering a note. |
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
| RequestStatusDueDateOffsetInDays | yes | yes |  |  |  | Number of days added to the calculated due date for a request status. |
| RequestStatusDueSoonOffsetInDays | yes | yes |  |  |  | Number of days before the due date when a request status is considered "due soon." |
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
| ConnectionStatusAutomations | Gets or sets a collection containing the ConnectionStatusAutomations who are associated with the Connection Status. |
| ConnectionType | Gets or sets the type of the connection. |
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
| ConnectionStatusAutomations | ConnectionStatusAutomations | acf794c7-f12d-42df-85c5-089a28993ee6 |
| ConnectionType | type | b1e52ead-65bd-4c4d-bccd-73368067621d |
| ConnectionTypeId | [Connection Type](connection-type.md) | b1e52ead-65bd-4c4d-bccd-73368067621d |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
