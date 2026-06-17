# Location Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `Location`
- EntityType GUID: `0d6410ad-c83c-47ac-af3d-616d09edf63b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 81 |
| Database-marked properties | 39 |
| Lava-marked properties | 66 |
| Lava-marked non-database properties | 27 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssessorParcelId | yes | yes |  |  |  | Gets or sets the Local Assessor's parcel identification value that is linked to the location. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Barcode | yes | yes |  |  |  | Gets or sets the barcode. |
| BeaconId | yes | yes |  |  |  | The identifier of the beacon that is associated with this location. This is typically used with Bluetooth proximity beacons and allows the Location to be determined from a beacon. |
| CampusId |  | yes | yes |  |  | Gets the campus that is at this location, or one of this location's parent location |
| ChildLocations |  | yes | yes |  |  | Gets or sets a collection of child Locations associated that inherit for this location. This property will only return the immediate descendants of this locations. |
| City | yes | yes |  |  |  | Gets or sets the city component of the Location's Street/Mailing Address. |
| ContextKey |  |  | yes |  |  |  |
| Country | yes | yes |  |  |  | Gets or sets the country component of the Location's Street/Mailing Address. |
| County | yes | yes |  |  |  | Gets or sets the county. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description of the location. For locations without a name, this value contains the computed name generated from the location’s address. |
| Distance |  | yes | yes |  |  | Gets the distance (in miles). Note, this just stores whatever value was passed into SetDistance Some of the REST APIs, such as Groups/ByLocation, will set this for you |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FirmRoomThreshold | yes | yes |  |  |  | Gets or sets threshold that will prevent checkin (no option to override) |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FormattedAddress |  | yes | yes |  |  | Gets the formatted address. |
| FormattedHtmlAddress |  | yes | yes |  |  | Gets the formatted HTML address. |
| GeoFence | yes | yes |  |  |  | Gets or sets the geographic parameter around the a Location's GeoPoint. This can also be used to define a large area like a neighborhood. |
| GeoFenceCoordinates |  | yes | yes |  |  | Gets the GeoFence coordinates. |
| GeoPoint | yes | yes |  |  |  | Gets or sets the GeoPoint (GeoLocation) for the location |
| GeocodeAttemptedDateTime | yes | yes |  |  |  | Gets and sets the date and time that an attempt was made to geocode the Location's address. |
| GeocodeAttemptedResult | yes | yes |  |  |  | Gets or sets the result code returned by geocoding service during the last geocode attempt. |
| GeocodeAttemptedServiceType | yes | yes |  |  |  | Gets or sets the component name of the Geocoding service that attempted the most recent address Geocode attempt. |
| GeocodedDateTime | yes | yes |  |  |  | Gets or sets date and time that this Location's address has been successfully geocoded. |
| GooglePolygon |  | yes | yes |  |  | Gets the polygon for Google maps. |
| GroupLocations |  | yes | yes |  |  | Gets or sets a collection containing the GroupLocations that reference this Location. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| Image |  | yes | yes |  |  | Gets or sets the image. |
| ImageId | yes | yes |  |  |  | Gets or sets the image identifier. |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsGeoPointLocked | yes | yes |  |  |  | Gets or sets flag indicating if GeoPoint is locked (shouldn't be geocoded again) |
| IsNamedLocation |  | yes | yes |  |  | Gets or sets a value indicating whether this instance is a named location. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| Latitude |  | yes | yes |  |  | Gets the latitude ( use GeoPoint to set a latitude/longitude values ). |
| LocationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LocationTypeValue |  | yes | yes |  |  | Gets or sets the location type value. |
| LocationTypeValueId | yes | yes |  |  |  | Gets or sets the Id of the LocationType Defined Value that is used to identify the type of Location that this is. Examples: Campus, Building, Room, etc These are found in the Location Type Defined Type. |
| Longitude |  | yes | yes |  |  | Gets the longitude ( use GeoPoint to set a latitude/longitude values ). |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the Location's Name. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority for the location. Location security is automatically inherited from the parent location, unless explicitly overridden. If there is no parent location, it is inherited from the EntityType |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentLocation |  | yes | yes |  |  | Gets or set this Location's parent Location. |
| ParentLocationId | yes | yes |  |  |  | Gets or sets the if the location's parent Location. |
| PostalCode | yes | yes |  |  |  | Gets or sets the Zip/Postal Code component of the Location's Street/Mailing Address. |
| PrinterDevice |  | yes | yes |  |  | Gets or sets the Attendance Printer Device that is used at this Location. |
| PrinterDeviceId | yes | yes |  |  |  | Gets or sets the Device Id of the printer (if any) associated with the location. |
| SoftRoomThreshold | yes | yes |  |  |  | Gets or sets a threshold that will prevent checkin unless a manager overrides |
| StandardizeAttemptedDateTime | yes | yes |  |  |  | Gets or sets the date and time of the last address standardization attempt. |
| StandardizeAttemptedResult | yes | yes |  |  |  | Gets or sets the result code returned from the address standardization service. |
| StandardizeAttemptedServiceType | yes | yes |  |  |  | Gets or set the component name of the service that attempted the most recent address standardization attempt. |
| StandardizedDateTime | yes | yes |  |  |  | Gets or sets the date and time that the Location's address was successfully standardized. |
| State | yes | yes |  |  |  | Gets or sets the State component of the Location's Street/Mailing Address. |
| Street1 | yes | yes |  |  |  | Gets or sets the first line of the Location's Street/Mailing Address. |
| Street2 | yes | yes |  |  |  | Gets or sets the second line of the Location's Street/Mailing Address. |
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
| CampusId | Gets the campus that is at this location, or one of this location's parent location |
| ChildLocations | Gets or sets a collection of child Locations associated that inherit for this location. This property will only return the immediate descendants of this locations. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| Distance | Gets the distance (in miles). Note, this just stores whatever value was passed into SetDistance Some of the REST APIs, such as Groups/ByLocation, will set this for you |
| EntityStringValue |  |
| FormattedAddress | Gets the formatted address. |
| FormattedHtmlAddress | Gets the formatted HTML address. |
| GeoFenceCoordinates | Gets the GeoFence coordinates. |
| GooglePolygon | Gets the polygon for Google maps. |
| GroupLocations | Gets or sets a collection containing the GroupLocations that reference this Location. |
| IdKey |  |
| Image | Gets or sets the image. |
| IsNamedLocation | Gets or sets a value indicating whether this instance is a named location. |
| Latitude | Gets the latitude ( use GeoPoint to set a latitude/longitude values ). |
| LocationTypeValue | Gets or sets the location type value. |
| Longitude | Gets the longitude ( use GeoPoint to set a latitude/longitude values ). |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentLocation | Gets or set this Location's parent Location. |
| PrinterDevice | Gets or sets the Attendance Printer Device that is used at this Location. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BeaconId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| GroupLocations | GroupLocations | 26248ee7-09f3-4578-a1d6-47e01d91d6ef |
| LocationTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| LocationTypeValueId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| PrinterDevice | [Device](device.md) | c06ee1fe-af12-410a-a364-7a366cd72414 |
| PrinterDeviceId | [Device](device.md) | c06ee1fe-af12-410a-a364-7a366cd72414 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
