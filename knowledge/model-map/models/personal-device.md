# Personal Device Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CRM`
- Model title: `PersonalDevice`
- EntityType GUID: `e9cd3369-e087-4809-9952-f2dcd6b8816b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 58 |
| Database-marked properties | 28 |
| Lava-marked properties | 41 |
| Lava-marked non-database properties | 15 |
| Related model links | 1 |
| Pre-alpha changes touching this model | 2 |

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
| DeviceRegistrationId | yes | yes |  |  |  | Gets or sets the registration id of the device. |
| DeviceUniqueIdentifier | yes | yes |  |  |  | Gets or sets the device unique identifier (MEID/IMEI) |
| DeviceVersion | yes | yes |  |  |  | Gets or sets the device version. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a flag indicating if this is an active personal device. This value is required. |
| IsBeaconMonitoringEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this device is enabled for beacon monitoring. |
| IsPreciseLocationEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether precise location is enabled. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastSeenDateTime | yes |  |  |  |  | Gets or sets the date and time this device was last seen initiating contact to the Rock server. |
| LastVerifiedDateTime | yes |  |  |  |  | Gets or sets the date and time this device was last verified as active and available for contact. |
| LocationPermissionDisabledDateTime | yes | yes |  |  |  | Gets or sets a value of when the location permission was last disabled. |
| LocationPermissionStatus | yes | yes |  |  |  | Gets or sets the location permission status. This is a hard coded list of values defined in the code as an enumeration. |
| MACAddress | yes | yes |  |  |  | Gets or sets the MAC address. |
| Manufacturer | yes | yes |  |  |  | Gets or sets the manufacturer. |
| Model | yes | yes |  |  |  | Gets or sets the model. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name. |
| NotificationsEnabled | yes | yes |  |  |  | Gets or sets whether or not notifications are enabled for this device. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| PersonalDeviceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| PersonalDeviceType |  | yes | yes |  |  | Gets or sets the personal device type. |
| PersonalDeviceTypeValueId | yes | yes |  |  |  | Gets or sets the Id of the Device Type DefinedValue representing what type of device this is. These are found in the "Personal Device Type" Defined Type. |
| PlatformValueId | yes | yes |  |  |  | Gets or sets the platform value identifier (i.e. iOS, Android, etc) These are found in the "Mobile Device Platform" Defined Type. |
| Site |  | yes | yes |  |  | Gets or sets the site. |
| SiteId | yes | yes |  |  |  | Gets or sets the site identifier. |
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
| PersonAlias | Gets or sets the person alias. |
| PersonalDeviceType | Gets or sets the personal device type. |
| Site | Gets or sets the site. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| PersonalDeviceTypeValueId | [DefinedValue](defined-value.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | Platform |  |
| property_changed | PersonalDeviceTypeValueId | enum_values |
