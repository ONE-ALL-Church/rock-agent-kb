# Sms Action Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Communication`
- Model title: `SmsAction`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `1f5e26be-0ed4-4250-8ffc-1ded5e9eacf0`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 17 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
| Method signatures | 36 |
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
| ContextKey |  |  | yes |  |  |  |
| ContinueAfterProcessing | yes | yes |  |  |  | Gets or sets a value indicating whether further actions should be processed. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDate | yes | yes |  |  |  | Gets or sets when to expire the Sms Action |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsInteractionLoggedAfterProcessing | yes | yes |  |  |  | Gets or sets a value indicating whether an interaction should be recorded after this action is processed. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name of the action. |
| Order | yes | yes |  |  |  | Gets or sets the order of this action in the system. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SmsActionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SmsActionComponentEntityTypeId | yes | yes |  |  |  | Gets or sets the identifier for the entity type that handles this action's logic. |
| SmsPipeline |  | yes | yes |  |  | Gets or sets the Sms Pipeline representing the SmsPipeline. |
| SmsPipelineId | yes | yes |  | yes |  | Gets or sets the SMS pipeline identifier. |
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
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SmsPipeline | Gets or sets the Sms Pipeline representing the SmsPipeline. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ExpireDate | [Sms Action](sms-action.md) | 1f5e26be-0ed4-4250-8ffc-1ded5e9eacf0 |
| SmsPipeline | [Sms Pipeline](sms-pipeline.md) | 64da3a06-fd39-4e5b-8126-38404fb0092a |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
