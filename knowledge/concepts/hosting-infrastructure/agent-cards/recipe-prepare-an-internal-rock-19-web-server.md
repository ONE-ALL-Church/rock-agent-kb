---
concept_id: hosting-infrastructure
task_id: recipe-prepare-an-internal-rock-19-web-server
title: Recipe: Prepare an internal Rock 19 web server
generated: true
---

# Recipe: Prepare an internal Rock 19 web server

A Windows/IIS host ready for the documented Rock 19 installer.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Confirm the current Rock technical requirements and SQL Server requirement.
2. Install IIS, the applicable ASP.NET 4.x role service, WebSocket Protocol, Application Initialization, and .NET Framework 3.5 Features.
3. Configure the application pool for .NET Framework v4.0, automatic startup, `LocalSystem`, and zero idle timeout.
4. Configure a specific low-traffic recycling time.
5. Enable website preload.
6. Enable dynamic-content compression when the module is available.
7. Place only `Start.aspx` and `web.config` from the installer in the web root.
8. Open `/Start.aspx` locally.
9. Stop when the installer’s environmental checks pass.
10. Identify the database type: Azure SQL Database, SQL Server on an Azure VM, or local/self-hosted SQL Server.
11. Verify the server name, database name, Rock-specific login, and connection target without exposing the password.
12. For Azure SQL Database, verify the login and `master` user, the `dbmanager` and `loginmanager` roles, and the database user’s `db_owner` membership.
13. For a self-hosted two-server deployment, verify TCP 1433 is permitted from the Rock web server’s address.
14. Confirm that SQL Server is private rather than generally internet-exposed.
15. Test the Rock-specific SQL login independently.
16. Stop when the Rock web server can connect using the intended restricted identity and network path. Configure SQL Server

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment
