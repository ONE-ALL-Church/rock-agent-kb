# Financial Transaction Scanned Check Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Other`
- Model title: `FinancialTransactionScannedCheck`
- EntityType GUID: `0ad40889-547b-4966-b3e1-2f9b2829c09c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 3 |
| Database-marked properties | 3 |
| Lava-marked properties | 3 |
| Lava-marked non-database properties | 0 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| FinancialTransaction | yes | yes |  |  |  | Gets or sets the financial transaction. |
| ScannedCheckMicrData | yes | yes |  |  |  | Gets or sets the scanned check MICR (the raw track data) |
| ScannedCheckMicrParts | yes | yes |  |  |  | Gets or sets the scanned check parsed MICR in the format {routingnumber}_{accountnumber}_{checknumber} |

## Lava-Marked Non-Database Properties

No Lava-marked non-database properties were found in the scraped Model Map for this model.

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| model_removed |  |  |
