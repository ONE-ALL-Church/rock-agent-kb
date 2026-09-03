# Connection Request Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Engagement`
- Model title: `ConnectionRequest`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `36b0d0c7-8125-48fa-9da2-729aaa65f718`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 72 |
| Database-marked properties | 29 |
| Lava-marked properties | 55 |
| Lava-marked non-database properties | 26 |
| Related model links | 19 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssignedGroup |  | yes | yes |  |  | Gets or sets the assigned Group. |
| AssignedGroupId | yes | yes |  |  |  | Gets or sets the assigned Group identifier. |
| AssignedGroupMemberAttributeValues | yes | yes |  |  |  | Gets or sets the assigned group member attribute values. |
| AssignedGroupMemberRoleId | yes | yes |  |  |  | Gets or sets the assigned group member role identifier. |
| AssignedGroupMemberStatus | yes | yes |  |  |  | Gets or sets the assigned group member status. This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus. |
| CampusId | yes | yes |  |  |  | Gets or sets the Campus identifier. |
| Comments | yes | yes |  |  |  | Gets or sets the comments. |
| ConnectedDateTime | yes | yes |  |  |  | The date and time when this request was marked as connected. |
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the Connection Opportunity. |
| ConnectionOpportunityId | yes | yes |  | yes |  | Gets or sets the Connection Opportunity identifier. |
| ConnectionRequestActivities |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionRequestActivities who are associated with the ConnectionRequest. |
| ConnectionRequestAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionRequestStatusHistories |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionRequestStatusHistory records associated with the ConnectionRequest. |
| ConnectionRequestWorkflows |  |  | yes |  |  | Gets or sets a collection containing the ConnectionRequestWorkflows who are associated with the ConnectionRequest. |
| ConnectionState | yes | yes |  | yes |  | Gets or sets the state of the connection. This is a hard coded list of values defined in the code as an enumeration. |
| ConnectionStatus |  | yes | yes |  |  | Gets or sets the Connection Status. |
| ConnectionStatusHistoryNote |  |  | yes |  |  | Gets or sets a transient note used when recording a Connection Request Status History entry during a Connection Request status change. |
| ConnectionStatusId | yes | yes |  | yes |  | Gets or sets the Connection Status identifier. |
| ConnectionTypeId | yes | yes |  | yes |  | Gets or sets the Connection Type identifier. |
| ConnectionTypeSource |  | yes | yes |  |  | Gets or sets the Connection Type Source. |
| ConnectionTypeSourceId | yes | yes |  |  |  | The source ConnectionType identifier. |
| ConnectorPersonAlias |  | yes | yes |  |  | Gets or sets the connector Person Alias. |
| ConnectorPersonAliasId | yes | yes |  |  |  | Gets or sets the connector Person Alias identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateKey | yes | yes |  |  |  | Gets the created date key. |
| CreatedDateTime | yes | yes |  |  |  |  |
| CreatedSourceDate |  | yes | yes |  |  | Gets or sets the created source date. |
| CustomSortValue |  |  | yes |  |  |  |
| DueDate | yes | yes |  |  |  | The due date for this request. |
| DueInDays |  | yes | yes |  |  | Gets the count of days within which this request is due. |
| DueSoonDate | yes | yes |  |  |  | The date when this request becomes considered due soon. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FollowupDate | yes | yes |  |  |  | Gets or sets the followup date. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsDueSoon |  | yes | yes |  |  | Gets whether this request is considered due soon. |
| IsOverdue |  | yes | yes |  |  | Gets whether this request is overdue. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| OverdueDays |  | yes | yes |  |  | Gets the count of days by which this request is overdue. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Person Alias identifier. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WasCompletedOnTime | yes | yes |  |  |  | Indicates whether the request was completed within the expected timeframe. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AssignedGroup | Gets or sets the assigned Group. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus. |
| ConnectionOpportunity | Gets or sets the Connection Opportunity. |
| ConnectionRequestActivities | Gets or sets a collection containing the ConnectionRequestActivities who are associated with the ConnectionRequest. |
| ConnectionRequestStatusHistories | Gets or sets a collection containing the ConnectionRequestStatusHistory records associated with the ConnectionRequest. |
| ConnectionStatus | Gets or sets the Connection Status. |
| ConnectionTypeSource | Gets or sets the Connection Type Source. |
| ConnectorPersonAlias | Gets or sets the connector Person Alias. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| CreatedSourceDate | Gets or sets the created source date. |
| DueInDays | Gets the count of days within which this request is due. |
| EntityStringValue |  |
| IdKey |  |
| IsDueSoon | Gets whether this request is considered due soon. |
| IsOverdue | Gets whether this request is overdue. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OverdueDays | Gets the count of days by which this request is overdue. |
| PersonAlias | Gets or sets the Person Alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AssignedGroup | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| AssignedGroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| ConnectionOpportunity | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionOpportunityId | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionRequestActivities | ConnectionRequestActivities | 3248f40d-7661-42cc-ad9b-ef63322937b7 |
| ConnectionRequestStatusHistories | [ConnectionRequestStatusHistory](connection-request-status-history.md) | 9d73fa0e-5787-4357-bd7c-43ad1800dbb1 |
| ConnectionRequestWorkflows | ConnectionRequestWorkflows | c69d1c9f-5521-4c83-8fe9-5044ecc2ce65 |
| ConnectionStatus | [Connection Status](connection-status.md) | f3840c8b-63bf-4f98-ac4a-9336896e589b |
| ConnectionStatusHistoryNote | [Connection Request](connection-request.md) | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectionStatusHistoryNote | [Connection Request Status History](connection-request-status-history.md) | 9d73fa0e-5787-4357-bd7c-43ad1800dbb1 |
| ConnectionStatusId | [Connection Status](connection-status.md) | f3840c8b-63bf-4f98-ac4a-9336896e589b |
| ConnectionTypeId | [Connection Type](connection-type.md) | b1e52ead-65bd-4c4d-bccd-73368067621d |
| ConnectionTypeSource | [Connection Type Source](connection-type-source.md) | 06fd04c5-8a18-43d1-ae13-3611344fb40a |
| ConnectorPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ConnectorPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
