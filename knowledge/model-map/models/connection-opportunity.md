# Connection Opportunity Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Engagement`
- Model title: `ConnectionOpportunity`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `79f64363-bc90-4109-9d31-a5eeb397cb2f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 60 |
| Database-marked properties | 24 |
| Lava-marked properties | 40 |
| Lava-marked non-database properties | 16 |
| Related model links | 8 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  | Gets or sets the additional settings as a JSON document. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionOpportunityAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionOpportunityCampuses |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionOpportunityCampuses who are associated with the ConnectionOpportunity. |
| ConnectionOpportunityConnectorGroups |  |  | yes |  |  | Gets or sets a collection containing the ConnectionOpportunityConnectorGroup who are associated with the ConnectionOpportunity. |
| ConnectionOpportunityGroupConfigs |  |  | yes |  |  | Gets or sets the connection opportunity group configs. |
| ConnectionOpportunityGroups |  |  | yes |  |  | Gets or sets a collection containing the ConnectionOpportunityGroups who are associated with the ConnectionOpportunity. |
| ConnectionRequests |  |  | yes |  |  | Gets or sets a collection containing the ConnectionRequests who are associated with the ConnectionOpportunity. |
| ConnectionType |  | yes | yes |  |  | Gets or sets the type of the connection. |
| ConnectionTypeId | yes | yes |  | yes |  | Gets or sets the Connection Type identifier. |
| ConnectionWorkflows |  |  | yes |  |  | Gets or sets a collection containing the ConnectionWorkflows who are associated with the ConnectionOpportunity. |
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
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is active. |
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
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Photo |  | yes | yes |  |  | Gets or sets the Binary File that contains the Opportunity's photo. |
| PhotoId | yes | yes |  |  |  | Gets or sets the photo identifier. |
| PhotoUrl |  | yes | yes |  |  | Gets the URL of the Opportunity's photo. |
| PublicName | yes | yes |  | yes |  | Gets or sets the name of the public. |
| RequestDueDateOffsetInDays | yes | yes |  |  |  | Number of days added to the calculated due date for a request. |
| RequestDueSoonOffsetInDays | yes | yes |  |  |  | Number of days before the due date when a request is considered "due soon." |
| ShowCampusOnTransfer | yes | yes |  |  |  | Gets or sets a value indicating whether [show campus on transfer]. |
| ShowConnectButton | yes | yes |  |  |  | Gets or sets a value indicating whether [show connect button]. |
| ShowStatusOnTransfer | yes | yes |  |  |  | Gets or sets a value indicating whether [show status on transfer]. |
| Summary | yes | yes |  |  |  | Gets or sets the summary. |
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
| ConnectionOpportunityCampuses | Gets or sets a collection containing the ConnectionOpportunityCampuses who are associated with the ConnectionOpportunity. |
| ConnectionType | Gets or sets the type of the connection. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Photo | Gets or sets the Binary File that contains the Opportunity's photo. |
| PhotoUrl | Gets the URL of the Opportunity's photo. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ConnectionOpportunityCampuses | ConnectionOpportunityCampuses | e656e8b3-12ab-476e-aa63-5f9b76f64a08 |
| ConnectionOpportunityConnectorGroups | [ConnectionOpportunityConnectorGroup](connection-opportunity-connector-group.md) | 2adbe499-c9ec-479b-b33b-6e92bde09fd1 |
| ConnectionOpportunityGroups | ConnectionOpportunityGroups | cd3f425c-9b36-4433-9c38-d58de42c9f65 |
| ConnectionRequests | ConnectionRequests | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectionType | type | b1e52ead-65bd-4c4d-bccd-73368067621d |
| ConnectionTypeId | [Connection Type](connection-type.md) | b1e52ead-65bd-4c4d-bccd-73368067621d |
| ConnectionWorkflows | ConnectionWorkflows | 4eb8711f-7301-4699-a223-0505a7ceb20a |
| Photo | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
