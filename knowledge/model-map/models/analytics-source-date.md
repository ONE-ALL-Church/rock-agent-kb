# Analytics Source Date Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Reporting`
- Model title: `AnalyticsSourceDate`
- EntityType GUID: `abe6dc7a-42af-479e-81d3-7bafcc416a9d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 49 |
| Lava-marked properties | 47 |
| Lava-marked non-database properties | 0 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Age | yes | yes |  |  |  | Gets or sets the age. |
| AgeBracket | yes | yes |  |  |  | Gets or sets the age bracket. This is a hard coded list of values defined in the code as an enumeration. |
| CalendarMonth | yes | yes |  |  |  | Gets or sets the calendar month number. Numeric Month (Jan = 1) |
| CalendarMonthName | yes | yes |  |  |  | Gets or sets the name of the calendar in month. Format: "MMMM" |
| CalendarMonthNameAbbrevated | yes |  |  |  |  | [Obsoleted in v13] Use CalendarMonthNameAbbreviated instead Gets or sets the calendar in month name abbreviated. Format: "MMM" |
| CalendarMonthNameAbbreviated | yes | yes |  |  |  | Gets or sets the calendar in month name abbreviated. Format: "MMM" |
| CalendarQuarter | yes | yes |  |  |  | Gets or sets the calendar quarter. Format: "Q{#}", for example "Q2" |
| CalendarWeek | yes | yes |  |  |  | Gets or sets the calendar week number. |
| CalendarYear | yes | yes |  |  |  | Gets or sets the calendar year. Format: "yyyy" |
| CalendarYearMonth | yes | yes |  |  |  | Gets or sets the calendar year month. Format: "yyyyMM" |
| CalendarYearMonthName | yes | yes |  |  |  | Gets or sets the name of the calendar year month. Format: "yyyy MMM", for example "2017 Mar" |
| CalendarYearQuarter | yes | yes |  |  |  | Gets or sets the calendar year quarter. Format: "yyyy Q{#}", for example "2017 Q2" |
| ChristmasIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [christmas indicator]. |
| ChristmasWeekIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [christmas week indicator]. |
| Count | yes | yes |  |  |  | Gets or sets the count. NOTE: This always has a (hard-coded) value of 1. It is stored in the table to assist with analytics calculations. |
| Date | yes | yes |  |  |  | Gets or sets the date. |
| DateKey | yes | yes |  |  |  | Gets or sets the date key in YYYYMMDD format |
| DayNumberInCalendarMonth | yes | yes |  |  |  | Gets or sets the day number in calendar month. |
| DayNumberInCalendarYear | yes | yes |  |  |  | Gets or sets the day number in calendar year. |
| DayNumberInFiscalMonth | yes | yes |  |  |  | Gets or sets the day number in fiscal month. |
| DayNumberInFiscalYear | yes | yes |  |  |  | Gets or sets the day number in fiscal year. |
| DayOfWeek | yes | yes |  |  |  | Gets or sets the day of week (Sunday=0) |
| DayOfWeekAbbreviated | yes | yes |  |  |  | Gets or sets the day of week abbreviated. |
| DayOfWeekName | yes | yes |  |  |  | Gets or sets the day of week. |
| EasterIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [easter indicator]. |
| EasterWeekIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [easter week indicator]. |
| FiscalHalfYear | yes | yes |  |  |  | Gets or sets the fiscal half year. |
| FiscalMonth | yes | yes |  |  |  | Gets or sets the fiscal month. |
| FiscalMonthAbbrevated | yes |  |  |  |  | [Obsoleted in v13] Use FiscalMonthAbbreviated instead Gets or sets the fiscal month abbreviated. |
| FiscalMonthAbbreviated | yes | yes |  |  |  | Gets or sets the fiscal month abbreviated. |
| FiscalMonthNumberInYear | yes | yes |  |  |  | Gets or sets the fiscal month number in year. |
| FiscalMonthYear | yes | yes |  |  |  | Gets or sets the name of the fiscal month year |
| FiscalQuarter | yes | yes |  |  |  | Gets or sets the fiscal quarter. |
| FiscalWeek | yes | yes |  |  |  | Gets or sets the fiscal week. |
| FiscalWeekNumberInYear | yes | yes |  |  |  | Gets or sets the fiscal week number in year. |
| FiscalYear | yes | yes |  |  |  | Gets or sets the fiscal year. |
| FiscalYearQuarter | yes | yes |  |  |  | Gets or sets the fiscal year quarter. |
| FullDateDescription | yes | yes |  |  |  | Gets or sets the full date description. |
| GivingMonth | yes | yes |  |  |  | Gets or sets the giving month. This is based on two options that they choose in the Date Generator UI 1) Fiscal Month and 2) Giving Month: Use Sunday Date If they choose the "Use Sunday Date" option, it will use whatever the SundayDate of Date is, but not if it crosses the Fiscal Year For example, if their Fiscal year starts on April 1st, it won't use the SundayDate for any of the last days of March if it ends up being in April |
| GivingMonthName | yes | yes |  |  |  | Gets or sets the giving month name. |
| HolidayIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [holiday indicator]. |
| LastDayInMonthIndictor | yes | yes |  |  |  | Gets or sets a value indicating whether [last day in month indictor]. |
| LeapYearIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether the containing year is a leap year. |
| SundayDate | yes | yes |  |  |  | Gets or sets the sunday date. |
| SundayDateYear | yes | yes |  |  |  | Gets or sets the sunday date year. |
| WeekCounter | yes | yes |  |  |  | Gets or sets the week counter. |
| WeekHolidayIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [week holiday indicator]. |
| WeekNumberInMonth | yes | yes |  |  |  | Gets or sets the week number in month. |
| WeekOfYear | yes | yes |  |  |  | Gets or sets the week of year. |

## Lava-Marked Non-Database Properties

No Lava-marked non-database properties were found in the scraped Model Map for this model.

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | CalendarMonthNameAbbrevated |  |
| property_removed | FiscalMonthAbbrevated |  |
