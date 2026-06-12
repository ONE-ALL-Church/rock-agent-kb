# Connection Request Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `ConnectionRequest`
- EntityType GUID: `36b0d0c7-8125-48fa-9da2-729aaa65f718`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 60 |
| Database-marked properties | 24 |
| Lava-marked properties | 44 |
| Lava-marked non-database properties | 20 |
| Related model links | 15 |
| Pre-alpha changes touching this model | 12 |

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
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the ConnectionOpportunity. |
| ConnectionOpportunityId | yes | yes |  | yes |  | Gets or sets the ConnectionOpportunity identifier. |
| ConnectionRequestActivities |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionRequestActivities who are associated with the ConnectionRequest. |
| ConnectionRequestAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionRequestWorkflows |  |  | yes |  |  | Gets or sets a collection containing the ConnectionRequestWorkflows who are associated with the ConnectionRequest. |
| ConnectionState | yes | yes |  | yes |  | Gets or sets the state of the connection. This is a hard coded list of values defined in the code as an enumeration. |
| ConnectionStatus |  | yes | yes |  |  | Gets or sets the ConnectionStatus. |
| ConnectionStatusId | yes | yes |  | yes |  | Gets or sets the ConnectionStatus identifier. |
| ConnectionTypeId | yes | yes |  | yes |  | Gets or sets the ConnectionType identifier. |
| ConnectorPersonAlias |  | yes | yes |  |  | Gets or sets the connector PersonAlias. |
| ConnectorPersonAliasId | yes | yes |  |  |  | Gets or sets the connector PersonAlias identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateKey | yes | yes |  |  |  | Gets the created date key. |
| CreatedDateTime | yes | yes |  |  |  |  |
| CreatedSourceDate |  | yes | yes |  |  | Gets or sets the created source date. |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FollowupDate | yes | yes |  |  |  | Gets or sets the followup date. |
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
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the PersonAlias identifier. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AssignedGroup | Gets or sets the assigned Group. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus. |
| ConnectionOpportunity | Gets or sets the ConnectionOpportunity. |
| ConnectionRequestActivities | Gets or sets a collection containing the ConnectionRequestActivities who are associated with the ConnectionRequest. |
| ConnectionStatus | Gets or sets the ConnectionStatus. |
| ConnectorPersonAlias | Gets or sets the connector PersonAlias. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| CreatedSourceDate | Gets or sets the created source date. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the PersonAlias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AssignedGroup | [Group](group.md) |  |
| AssignedGroupId | [Group](group.md) |  |
| Campus | [Campus](campus.md) |  |
| CampusId | [Campus](campus.md) |  |
| ConnectionOpportunity | [ConnectionOpportunity](connection-opportunity.md) |  |
| ConnectionOpportunityId | [ConnectionOpportunity](connection-opportunity.md) |  |
| ConnectionRequestActivities | ConnectionRequestActivities |  |
| ConnectionRequestWorkflows | ConnectionRequestWorkflows |  |
| ConnectionStatus | [ConnectionStatus](connection-status.md) |  |
| ConnectionStatusId | [ConnectionStatus](connection-status.md) |  |
| ConnectionTypeId | [ConnectionType](connection-type.md) |  |
| ConnectorPersonAlias | [PersonAlias](person-alias.md) |  |
| ConnectorPersonAliasId | [PersonAlias](person-alias.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PersonAliasId | [PersonAlias](person-alias.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | ConnectedDateTime |  |
| property_added | ConnectionRequestStatusHistories |  |
| property_added | ConnectionStatusHistoryNote |  |
| property_added | ConnectionTypeSource |  |
| property_added | ConnectionTypeSourceId |  |
| property_added | DueDate |  |
| property_added | DueInDays |  |
| property_added | DueSoonDate |  |
| property_added | IsDueSoon |  |
| property_added | IsOverdue |  |
| property_added | OverdueDays |  |
| property_added | WasCompletedOnTime |  |
