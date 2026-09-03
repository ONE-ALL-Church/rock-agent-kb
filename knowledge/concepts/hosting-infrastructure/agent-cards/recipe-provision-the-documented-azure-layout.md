---
concept_id: hosting-infrastructure
task_id: recipe-provision-the-documented-azure-layout
title: Recipe: Provision the documented Azure layout
generated: true
---

# Recipe: Provision the documented Azure layout

A resource group containing the intended Rock web VM and Azure SQL resources.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Step`
- `Group`

## Entities And Tables

- `Step`
- `Group`

## Steps

1. Create or select the Rock production resource group.
2. Provision the Windows web VM in that group.
3. Configure IIS on the web VM.
4. Provision the Azure SQL server and database in the same resource group.
5. Create Rock’s Azure SQL login and `master` user.
6. Grant `dbmanager` and `loginmanager`.
7. Run the Rock installation so the application database is created.
8. Create the Rock user in the application database and add it to `db_owner`.
9. Test the restricted Rock login.
10. Verify the resulting resources and connections directly; do not rely on portal-screen similarity.

## Do Not Assume

- Verify the resulting resources and connections directly; do not rely on portal-screen similarity.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Blocks/Security/Login/PasswordlessLoginStep.cs
