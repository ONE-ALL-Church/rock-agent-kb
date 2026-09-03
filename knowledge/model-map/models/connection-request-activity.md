# Connection Request Activity Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Engagement`
- Model title: `ConnectionRequestActivity`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
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
| ConnectionActivityType |  | yes | yes |  |  | Gets or sets the type of the connection activity. |
| ConnectionActivityTypeId | yes | yes |  | yes |  | Gets or sets the Connection Activity Type identifier. |
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the Connection Opportunity. |
| ConnectionOpportunityId | yes | yes |  | yes |  | Gets or sets the Connection Opportunity identifier. |
| ConnectionRequest |  | yes | yes |  |  | Gets or sets the Connection Request. |
| ConnectionRequestActivityAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionRequestId | yes | yes |  | yes |  | Gets or sets the Connection Request identifier. |
| ConnectorPersonAlias |  | yes | yes |  |  | Gets or sets the connector Person Alias. |
| ConnectorPersonAliasId | yes | yes |  |  |  | Gets or sets the connector Person Alias identifier. |
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
| ConnectionOpportunity | Gets or sets the Connection Opportunity. |
| ConnectionRequest | Gets or sets the Connection Request. |
| ConnectorPersonAlias | Gets or sets the connector Person Alias. |
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
| ConnectionActivityType | type | 97b143f0-cb9d-4652-8ff1-ff2fa1ea4945 |
| ConnectionActivityTypeId | [Connection Activity Type](connection-activity-type.md) | 97b143f0-cb9d-4652-8ff1-ff2fa1ea4945 |
| ConnectionOpportunity | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionOpportunityId | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionRequest | [Connection Request](connection-request.md) | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectionRequestId | [Connection Request](connection-request.md) | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectorPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ConnectorPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
