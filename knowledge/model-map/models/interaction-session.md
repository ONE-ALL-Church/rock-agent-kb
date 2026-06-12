# Interaction Session Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `InteractionSession`
- EntityType GUID: `338025de-c16f-47bb-ba31-6de0c59e59aa`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 19 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 15 |
| Related model links | 3 |
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
| DeviceType |  | yes | yes |  |  | Gets or sets the device type. |
| DeviceTypeId | yes | yes |  |  |  | Gets or sets the Id of the InteractionDeviceType device type that that is associated with this Session. |
| DurationLastCalculatedDateTime | yes |  |  |  |  | Gets or sets the last date and time when this was calculated. |
| DurationSeconds | yes | yes |  |  |  | Gets or set the duration in seconds. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractionChannel |  |  | yes |  |  | Gets or sets the interaction channel. |
| InteractionChannelId | yes | yes |  |  |  | Gets or sets the interaction channel identifier. |
| InteractionCount | yes | yes |  |  |  | Gets or sets the Interaction Count. |
| InteractionMode | yes | yes |  |  |  | Gets or sets the interaction mode. |
| InteractionSessionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractionSessionLocation |  | yes | yes |  |  | Gets or sets the interaction session location. |
| InteractionSessionLocationId | yes | yes |  |  |  | Gets or sets the Id of the InteractionSessionLocation Session Location that that is associated with this Interaction Session. |
| Interactions |  | yes | yes |  |  | Gets or sets the Interactions for this session. |
| IpAddress | yes | yes |  |  |  | Gets or sets the IP address of the request. |
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
| SessionData | yes | yes |  |  |  | Gets or sets the interaction session data. |
| SessionStartDateKey | yes | yes |  |  |  | Gets or sets the session start date key which is the form YYYYMMDD. |
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
| DeviceType | Gets or sets the device type. |
| EntityStringValue |  |
| IdKey |  |
| InteractionSessionLocation | Gets or sets the interaction session location. |
| Interactions | Gets or sets the Interactions for this session. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DeviceTypeId | [InteractionDeviceType](interaction-device-type.md) |  |
| InteractionSessionLocationId | [InteractionSessionLocation](interaction-session-location.md) |  |
| Interactions | Interactions |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
