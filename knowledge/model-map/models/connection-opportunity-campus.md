# Connection Opportunity Campus Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `ConnectionOpportunityCampus`
- EntityType GUID: `e656e8b3-12ab-476e-aa63-5f9b76f64a08`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 42 |
| Database-marked properties | 12 |
| Lava-marked properties | 27 |
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
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus. |
| CampusId | yes | yes |  | yes |  | Gets or sets the Campus identifier. |
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the Connection Opportunity. |
| ConnectionOpportunityCampusAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionOpportunityId | yes | yes |  | yes |  | Gets or sets the Connection Opportunity identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultConnectorPersonAlias |  | yes | yes |  |  | Gets or sets the default connector Person Alias. |
| DefaultConnectorPersonAliasId | yes | yes |  |  |  | Gets or sets the default connector Person Alias identifier. |
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
| Campus | Gets or sets the Campus. |
| ConnectionOpportunity | Gets or sets the Connection Opportunity. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefaultConnectorPersonAlias | Gets or sets the default connector Person Alias. |
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
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| ConnectionOpportunity | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionOpportunityId | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| DefaultConnectorPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| DefaultConnectorPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
