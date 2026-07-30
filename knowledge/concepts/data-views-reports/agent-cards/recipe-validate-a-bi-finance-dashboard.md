---
concept_id: data-views-reports
task_id: recipe-validate-a-bi-finance-dashboard
title: Recipe: Validate A BI Finance Dashboard
generated: true
---

# Recipe: Validate A BI Finance Dashboard

Complete Validate A BI Finance Dashboard with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Campus`

## Entities And Tables

- `Group`
- `Campus`

## Steps

1. Identify dashboard filters.
2. Identify source model/table.
3. Check BI job last success.
4. Check Power BI dataset refresh.
5. Run Rock UI finance report for same dates/accounts.
6. Run direct read-only SQL if needed.
7. Compare totals.
8. Investigate differences by transaction type, account, campus, refunds, registration payments, and giving group.
9. Document reconciliation.
10. Get finance owner signoff.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.triumph.tech/resources/grouping-sets
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/GroupTypeDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/GroupMemberDataViewFilter.cs
- https://community.rockrms.com/recipes/264
- https://community.rockrms.com/recipes/397
