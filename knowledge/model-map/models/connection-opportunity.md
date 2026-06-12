# Connection Opportunity Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `ConnectionOpportunity`
- EntityType GUID: `79f64363-bc90-4109-9d31-a5eeb397cb2f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 58 |
| Database-marked properties | 22 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 16 |
| Related model links | 9 |
| Pre-alpha changes touching this model | 3 |

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
| ConnectionTypeId | yes | yes |  | yes |  | Gets or sets the ConnectionType identifier. |
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
| Photo |  | yes | yes |  |  | Gets or sets the BinaryFile that contains the Opportunity's photo. |
| PhotoId | yes | yes |  |  |  | Gets or sets the photo identifier. |
| PhotoUrl |  | yes | yes |  |  | Gets the URL of the Opportunity's photo. |
| PublicName | yes | yes |  | yes |  | Gets or sets the name of the public. |
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
| Photo | Gets or sets the BinaryFile that contains the Opportunity's photo. |
| PhotoUrl | Gets the URL of the Opportunity's photo. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ConnectionOpportunityCampuses | ConnectionOpportunityCampuses |  |
| ConnectionOpportunityConnectorGroups | [ConnectionOpportunityConnectorGroup](connection-opportunity-connector-group.md) |  |
| ConnectionOpportunityGroupConfigs | connection opportunity group configs |  |
| ConnectionOpportunityGroups | ConnectionOpportunityGroups |  |
| ConnectionRequests | ConnectionRequests |  |
| ConnectionType | type |  |
| ConnectionTypeId | [ConnectionType](connection-type.md) |  |
| ConnectionWorkflows | ConnectionWorkflows |  |
| Photo | [BinaryFile](binary-file.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | RequestDueDateOffsetInDays |  |
| property_added | RequestDueSoonOffsetInDays |  |
| property_changed | ConnectionOpportunityGroupConfigs | related_entity_links |
