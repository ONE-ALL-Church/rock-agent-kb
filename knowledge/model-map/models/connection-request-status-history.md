# Connection Request Status History Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `ConnectionRequestStatusHistory`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `9d73fa0e-5787-4357-bd7c-43ad1800dbb1`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 48 |
| Database-marked properties | 17 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 16 |
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
| CompletedByPersonAlias |  | yes | yes |  |  | Gets or sets the type that the connection request status was completed by. |
| CompletedByPersonAliasId | yes | yes |  |  |  | The person alias who completed the request, if applicable. |
| ConnectionRequest |  | yes | yes |  |  | Gets or sets the type of the status history. |
| ConnectionRequestId | yes | yes |  |  |  | The identifier of the connection request. |
| ConnectionRequestStatusHistoryAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionStatus |  | yes | yes |  |  | Gets or sets the type of the connection. |
| ConnectionStatusId | yes | yes |  |  |  | The identifier of the connection type status. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EndDateTime | yes | yes |  |  |  | The end date time. |
| EntityStringValue |  | yes | yes |  |  |  |
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
| Note | yes | yes |  |  |  | Additional notes recorded when this status entry was created. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PreviousConnectionStatus |  | yes | yes |  |  | Gets or sets the previous Connection Status, if applicable. This represents the connection status prior to the current status of this history record. |
| PreviousConnectionStatusId | yes | yes |  |  |  | The identifier of the previous connection status, if applicable. This is used to determine the status prior to the ConnectionStatusId of this history record. |
| StartDateTime | yes | yes |  |  |  | The start date time. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WasCompletedOnTime | yes | yes |  |  |  | Indicates whether the request was completed on time while in this status. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CompletedByPersonAlias | Gets or sets the type that the connection request status was completed by. |
| ConnectionRequest | Gets or sets the type of the status history. |
| ConnectionStatus | Gets or sets the type of the connection. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PreviousConnectionStatus | Gets or sets the previous Connection Status, if applicable. This represents the connection status prior to the current status of this history record. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| CompletedByPersonAlias | type | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ConnectionRequest | type | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectionStatus | type | f3840c8b-63bf-4f98-ac4a-9336896e589b |
| PreviousConnectionStatus | [Connection Status](connection-status.md) | f3840c8b-63bf-4f98-ac4a-9336896e589b |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
