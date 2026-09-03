---
concept_id: hosting-infrastructure
task_id: recipe-offload-reports-and-analytics-to-a-read-only-database
title: Recipe: Offload reports and analytics to a read-only database
generated: true
---

# Recipe: Offload reports and analytics to a read-only database

Eligible Rock 19 reporting or analytics traffic uses the intended read-only target.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `DataView`
- `Block`

## Entities And Tables

- `Attendance`
- `DataView`
- `Block`

## Steps

1. Confirm the read-only database or replica exists.
2. Determine whether the target workload is Data Views and Reports or the three supported analytics blocks.
3. Add `RockContextReadOnly` for Data Views and Reports, or `RockContextAnalytics` for Giving, Attendance, and Pledge Analytics.
4. Preserve the primary `RockContext`.
5. Test connectivity without exposing connection-string secrets.
6. Exercise each target workload.
7. For a Data View that requires writes, enable **Disable Use Of Read Only Context** on that Data View.
8. Observe which database receives the test traffic.
9. Stop when routing and write behavior match the intended design.
10. Confirm that `RockContextReadOnly` is present and points to the intended database.
11. Test basic connectivity and data availability.
12. Identify whether the Data View contains a plugin or filter that performs writes.
13. If writes are required, enable **Disable Use Of Read Only Context** for that specific Data View.
14. Retest the operation against the primary context.
15. Stop when the operation succeeds and its context selection is documented.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginMfaBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginStartRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/RequestFilterDetail/environmentRequestFilterBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginVerifyResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/Login/passwordlessLoginVerifyResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginVerifyOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Blocks/Security/Login/PasswordlessLoginStep.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginAutoVerifyOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Cms/RequestFilterDetail/EnvironmentRequestFilterBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Security/Login/PasswordlessLoginVerifyRequestBag.cs
