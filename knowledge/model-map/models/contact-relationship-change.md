# Contact Relationship Change Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `ContactRelationshipChange`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `0397d69f-1e9e-4202-bcb8-9deedaa554c9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 25 |
| Database-marked properties | 12 |
| Lava-marked properties | 18 |
| Lava-marked non-database properties | 6 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Contact |  | yes | yes |  |  | Gets or sets the contact. |
| ContactId | yes | yes |  |  |  | Gets or sets the contact identifier. |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HasAcceptedJesus | yes | yes |  |  |  | Gets or sets a value indicating whether the change was app influenced growth. |
| HasBeenBaptized | yes | yes |  |  |  | Gets or sets a value indicating whether the contact has been baptized. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| NewRelationshipStrength | yes | yes |  |  |  | Gets or sets the new relationship strength. This is a hard coded list of values defined in the code as an enumeration. |
| PreviousRelationshipStrength | yes | yes |  |  |  | Gets or sets the previous relationship strength. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WasAcceptanceInfluencedByApp | yes | yes |  |  |  | Gets or sets a value indicating whether acceptance was influenced by the app. |
| WasBaptismInfluencedByApp | yes | yes |  |  |  | Gets or sets a value indicating whether the baptism was influenced by the app. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Contact | Gets or sets the contact. |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
