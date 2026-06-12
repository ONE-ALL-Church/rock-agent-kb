# Connection Request Activity Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `ConnectionRequestActivity`
- EntityType GUID: `3248f40d-7661-42cc-ad9b-ef63322937b7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 14 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 16 |
| Related model links | 8 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionActivityType |  | yes | yes |  |  | Gets or sets the type of the connection activity. |
| ConnectionActivityTypeId | yes | yes |  | yes |  | Gets or sets the ConnectionActivityType identifier. |
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the ConnectionOpportunity. |
| ConnectionOpportunityId | yes | yes |  | yes |  | Gets or sets the ConnectionOpportunity identifier. |
| ConnectionRequest |  | yes | yes |  |  | Gets or sets the ConnectionRequest. |
| ConnectionRequestActivityAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionRequestId | yes | yes |  | yes |  | Gets or sets the ConnectionRequest identifier. |
| ConnectorPersonAlias |  | yes | yes |  |  | Gets or sets the connector PersonAlias. |
| ConnectorPersonAliasId | yes | yes |  |  |  | Gets or sets the connector PersonAlias identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
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
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
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
| ConnectionActivityType | Gets or sets the type of the connection activity. |
| ConnectionOpportunity | Gets or sets the ConnectionOpportunity. |
| ConnectionRequest | Gets or sets the ConnectionRequest. |
| ConnectorPersonAlias | Gets or sets the connector PersonAlias. |
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
| ConnectionActivityType | type |  |
| ConnectionActivityTypeId | [ConnectionActivityType](connection-activity-type.md) |  |
| ConnectionOpportunity | [ConnectionOpportunity](connection-opportunity.md) |  |
| ConnectionOpportunityId | [ConnectionOpportunity](connection-opportunity.md) |  |
| ConnectionRequest | [ConnectionRequest](connection-request.md) |  |
| ConnectionRequestId | [ConnectionRequest](connection-request.md) |  |
| ConnectorPersonAlias | [PersonAlias](person-alias.md) |  |
| ConnectorPersonAliasId | [PersonAlias](person-alias.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
