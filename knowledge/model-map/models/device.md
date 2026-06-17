# Device Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `Device`
- EntityType GUID: `c06ee1fe-af12-410a-a364-7a366cd72414`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 54 |
| Database-marked properties | 22 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 17 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CameraBarcodeConfigurationType | yes | yes |  |  |  | Gets or sets the camera barcode configuration. This is currently only used for reading barcodes on iPads. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a description of the device. |
| DeviceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| DeviceType |  | yes | yes |  |  | Gets or sets the Defined Value that represents the type of the device. |
| DeviceTypeValueId | yes | yes |  |  |  | Gets or sets the Id of the DeviceType Defined Value that identifies what type of device this is. These are found in the Device Type Defined Type. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HasCamera | yes | yes |  |  |  | Gets or sets a value indicating whether this instance has camera. Only applies when DeviceTypeValueId is Checkin-Kiosk. |
| IPAddress | yes | yes |  |  |  | Gets or sets the IP address of the device. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| KioskType | yes | yes |  |  |  | The type of checkin client this Check-in Kiosk could be using. Only applies when DeviceTypeValueId is Checkin-Kiosk. This is a hard coded list of values defined in the code as an enumeration. |
| Location |  | yes | yes |  |  | Gets or sets the physical location or geographic fence for the device. |
| LocationId | yes | yes |  |  |  | Gets or sets the Id of the Location where this device is located at. |
| Locations |  | yes | yes |  |  | Gets or sets a collection containing the Locations that use this device. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the device name. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PrintFrom | yes | yes |  |  |  | Gets or sets where print jobs for this device originates from. This is a hard coded list of values defined in the code as an enumeration. |
| PrintToOverride | yes | yes |  |  |  | Gets or sets a flag that overrides which printer the print job is set to. This is a hard coded list of values defined in the code as an enumeration. |
| PrinterDevice |  | yes | yes |  |  | Gets or sets the printer that is associated with this device. |
| PrinterDeviceId | yes | yes |  |  |  | Gets or sets the DeviceId of the printer that is associated with this device. This is mostly used if this device is a kiosk. |
| ProxyDevice |  | yes | yes |  |  | Gets or sets the proxy that is associated with this device. |
| ProxyDeviceId | yes | yes |  |  |  | Gets or sets the Id of the device that will handle proxying commands to this device. Currently this means a printer proxy. |
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
| DeviceType | Gets or sets the Defined Value that represents the type of the device. |
| EntityStringValue |  |
| IdKey |  |
| Location | Gets or sets the physical location or geographic fence for the device. |
| Locations | Gets or sets a collection containing the Locations that use this device. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PrinterDevice | Gets or sets the printer that is associated with this device. |
| ProxyDevice | Gets or sets the proxy that is associated with this device. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DeviceType | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| DeviceTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| LocationId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| Locations | Locations | 0d6410ad-c83c-47ac-af3d-616d09edf63b |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | DeviceTypeValueId | enum_values |
