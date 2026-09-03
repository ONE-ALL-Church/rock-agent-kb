---
concept_id: data-views-reports
task_id: recipe-validate-a-registration-analytics-dashboard
title: Recipe: Validate a registration analytics dashboard
generated: true
---

# Recipe: Validate a registration analytics dashboard

Every displayed total has an explicit grain and reconciled population.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Campus`
- `Label`
- `Page`
- `Attribute`

## Entities And Tables

- `Person`
- `Group`
- `Campus`
- `Label`
- `Page`
- `Attribute`

## Steps

1. Label measures as registrations, registrants, or distinct people.
2. Define confirmed and wait-list predicates once.
3. Apply those predicates consistently to every component.
4. Test a multi-person registration.
5. Test a wait-list registrant.
6. Test a recent registrant near the reporting boundary.
7. Reconcile mutually exclusive segments to the confirmed population.
8. Identify many-to-many categories and label them non-additive.
9. Align historical pace comparisons by the same event stage when using that community pattern.
10. Test permissions, empty states, Lava errors, browser errors, filters, and responsive layout in the rendered page.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.triumph.tech/resources/grouping-sets
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/ConnectionRequest/GroupMemberDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/ConnectionRequest/PersonDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Group/GroupTypeDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs
- https://community.rockrms.com/rocku/groups/group-scheduling-analytics
