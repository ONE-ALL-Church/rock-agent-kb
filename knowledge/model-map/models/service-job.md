# Service Job Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `ServiceJob`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `52766196-a72f-4f60-997a-78e19508843d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 56 |
| Database-marked properties | 26 |
| Lava-marked properties | 41 |
| Lava-marked non-database properties | 15 |
| Related model links | 0 |
| Method signatures | 35 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Assembly | yes | yes |  |  |  | Gets or sets the Assembly name of the .dll file that contains the job class. Set this to null to have Rock figure out the Assembly automatically. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Class | yes | yes |  | yes |  | Gets or sets the fully qualified class name with Namespace of the Job class. This property is required. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CronDescription |  | yes | yes |  | yes | Gets the cron description. |
| CronExpression | yes | yes |  | yes |  | Gets or sets the Cron Expression that is used to schedule the Job. This property is required. |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the Job. |
| EnableHistory | yes | yes |  |  |  | Gets or sets a value indicating whether jobs should be logged in ServiceJobHistory |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HistoryCount | yes | yes |  |  |  | Gets or sets the history count per job. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if the Job is active. |
| IsSystem | yes | yes |  |  |  | Gets or sets a flag indicating if this Job is part of the Rock core system/framework |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRunDateTime | yes | yes |  |  |  | Gets or sets the date and time that the job last ran. |
| LastRunDurationSeconds | yes | yes |  |  |  | Gets or set the amount of time, in seconds, that it took the job to run the last time that it ran. |
| LastRunSchedulerName | yes | yes |  |  |  | Gets or sets the name of the scheduler that the job ran under the last time that it ran. In most cases this is used to determine if the was run by the IIS or Windows service. |
| LastStatus | yes | yes |  |  |  | Gets or sets the completion status that was returned by the Job the last time that it ran. |
| LastStatusMessage | yes | yes |  |  |  | Gets or sets the status message that was returned the last time that the job was run. In most cases this will be used in the event of an exception to return the exception message. |
| LastStatusMessageAsHtml |  | yes | yes |  |  | Gets the last status message as HTML. |
| LastSuccessfulRunDateTime | yes | yes |  |  |  | Gets or sets the date and time that the Job last completed successfully. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the friendly Name of the Job. This property is required. |
| NotificationEmails | yes | yes |  |  |  | Gets or sets a comma delimited list of email address that should receive notification emails for this job. Notification emails are sent to these email addresses based on the completion status of the Job and the NotificationStatus property of this job. |
| NotificationStatus | yes | yes |  | yes |  | Gets or sets the NotificationStatus for this job, this property determines when notification emails should be sent to the NotificationEmails that are associated with this Job This is a hard coded list of values defined in the code as an enumeration. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ServiceJobAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ServiceJobHistory |  | yes | yes |  |  | Gets or sets the a list of previous values that this attribute value had (If ServiceJob.EnableHistory is enabled) |
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
| CronDescription | Gets the cron description. |
| EntityStringValue |  |
| IdKey |  |
| LastStatusMessageAsHtml | Gets the last status message as HTML. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ServiceJobHistory | Gets or sets the a list of previous values that this attribute value had (If ServiceJob.EnableHistory is enabled) |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
