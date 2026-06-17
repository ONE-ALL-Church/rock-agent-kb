# Analytics Dim Campus Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `AnalyticsDimCampus`
- EntityType GUID: `dceb0575-1351-4cff-ba4f-410ba2d638cb`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 31 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 5 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AddressCity | yes | yes |  |  |  | Gets or sets the city component of the Location's Street/Mailing Address. |
| AddressCountry | yes | yes |  |  |  | Gets or sets the country component of the Location's Street/Mailing Address. |
| AddressCounty | yes | yes |  |  |  | Gets or sets the county. |
| AddressFull | yes | yes |  |  |  | Gets or sets the full address. |
| AddressGeoFence | yes | yes |  |  |  | Gets or sets the geographic parameter around the a Location's Geopoint. This can also be used to define a large area like a neighborhood. |
| AddressGeoPoint | yes | yes |  |  |  | Gets or sets the GeoPoint (geolocation) for the location |
| AddressLatitude | yes | yes |  |  |  | Gets or sets the latitude. (From AddressGeoPoint) |
| AddressLongitude | yes | yes |  |  |  | Gets or sets the longitude. (From AddressGeoPoint) |
| AddressPostalCode | yes | yes |  |  |  | Gets or sets the Zip/Postal Code component of the Location's Street/Mailing Address. |
| AddressState | yes | yes |  |  |  | Gets or sets the State component of the Location's Street/Mailing Address. |
| AddressStreet1 | yes | yes |  |  |  | Gets or sets the first line of the Location's Street/Mailing Address. |
| AddressStreet2 | yes | yes |  |  |  | Gets or sets the second line of the Location's Street/Mailing Address. |
| AvailableKeys |  |  | yes |  |  |  |
| CampusId | yes | yes |  |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  |  |
| Description | yes | yes |  |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LeaderFullName | yes | yes |  |  |  | Gets or sets the full name of the leader (from LeaderAliasPerson.Person.FullName) |
| LeaderPersonAliasId | yes | yes |  |  |  |  |
| LeaderPersonId | yes | yes |  |  |  | Gets or sets the leader person identifier (from LeaderAliasPerson.PersonId) |
| LocationId | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  |  |
| Order | yes | yes |  |  |  |  |
| PhoneNumber | yes | yes |  |  |  |  |
| ServiceTimes | yes | yes |  |  |  |  |
| ShortCode | yes | yes |  |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| Url | yes | yes |  |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
