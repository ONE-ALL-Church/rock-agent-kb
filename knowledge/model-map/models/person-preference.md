# Person Preference Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `PersonPreference`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `fdcf766c-f36b-403b-89f3-7030da65507e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 26 |
| Database-marked properties | 12 |
| Lava-marked properties | 18 |
| Lava-marked non-database properties | 7 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the Id of the IEntity that this preference is associated with. This is used to limit the preferences that are automatically loaded to only the ones related to the request. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the the EntityType that this preference is associated with. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the Id of the EntityType that this preference is associated with. This is used to limit the preferences that are automatically loaded to only the ones related to the request. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsEnduring | yes |  |  |  |  | Gets or sets a value indicating whether this preference is should have an extended life. Enduring preferences have a life of 18 months since last accessed. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  | yes |  | Gets or sets the unique key that identifies this preference. This is unique to each related PersonAliasId. The key should always follow the pattern of {entity-type-slug}-{entity-id}-{user-key}. For example, a block preference might look like block-283-show-inactive. In the case of a preference not attached to any entity it should follow the pattern of global-0-{user-key}. For example, a global person preference might look like global-0-default-grid-page-size. |
| LastAccessedDateTime | yes | yes |  |  |  | Gets or sets the date this preference was last accessed by the owner. This should only be updated once per day. |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias that owns this preference. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Id of the PersonAlias that owns this preference. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Value | yes | yes |  |  |  | Gets or sets the preference value. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| EntityType | Gets or sets the the EntityType that this preference is associated with. |
| IdKey |  |
| PersonAlias | Gets or sets the PersonAlias that owns this preference. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
