---
concept_id: data-views-reports
task_id: recipe-build-people-who-attended-x-but-not-y
title: Recipe: Build "People Who Attended X But Not Y"
generated: true
---

# Recipe: Build "People Who Attended X But Not Y"

Complete Build "People Who Attended X But Not Y" with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `PersonAlias`
- `DataView`

## Entities And Tables

- `Attendance`
- `Person`
- `PersonAlias`
- `DataView`

## Steps

1. Create child Attendance Data View for X.
2. Create child Attendance Data View for Y.
3. Create Person Data View using related Attendance Data View filter for X.
4. Add exclusion for people related to Y if supported.
5. Verify alias behavior.
6. Test known people.
7. If Data View cannot express exclusion cleanly, use SQL with `PersonAlias`.
8. Validate against attendance UI.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://community.rockrms.com/lava/commands/sql-commands
- https://community.rockrms.com/documentation/bookcontent/6/331
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs
- https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report
- https://www.triumph.tech/resources/grouping-sets
- https://www.triumph.tech/resources/sql-window-functions
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://community.rockrms.com/rocku/lava/sql-command
- https://community.rockrms.com/recipes/526/sql-model-map-qol-reference
- https://community.rockrms.com/recipes/349
