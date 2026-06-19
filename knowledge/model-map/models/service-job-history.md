# Service Job History Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `ServiceJobHistory`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `d6a7c6e0-004f-4f38-9dca-16e645f5edf4`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 15 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 15 |
| Related model links | 1 |
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
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DurationSeconds |  | yes | yes |  |  | Gets the job duration in seconds. |
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
| ServiceJob |  | yes | yes |  |  | Gets or sets the ServiceJob Service Job that this ServiceJobHistory provides a History value for. |
| ServiceJobHistoryAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ServiceJobId | yes | yes |  |  |  | The Id of the ServiceJob |
| ServiceWorker | yes | yes |  |  |  | Gets or sets the name of the service worker. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the date and time that the Job started. |
| Status | yes | yes |  |  |  | Gets or sets the completion status that was returned by the Job. |
| StatusMessage | yes | yes |  |  |  | Gets or sets the status message that was returned by the job. In most cases this will be used in the event of an exception to return the exception message. |
| StatusMessageAsHtml |  | yes | yes |  |  | Gets the status message as HTML. |
| StopDateTime | yes | yes |  |  |  | Gets or sets the date and time that the job finished. |
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
| DurationSeconds | Gets the job duration in seconds. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ServiceJob | Gets or sets the ServiceJob Service Job that this ServiceJobHistory provides a History value for. |
| StatusMessageAsHtml | Gets the status message as HTML. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ServiceJob | [Service Job](service-job.md) | 52766196-a72f-4f60-997a-78e19508843d |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
