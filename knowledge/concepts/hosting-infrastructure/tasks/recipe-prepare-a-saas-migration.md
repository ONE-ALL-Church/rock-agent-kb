---
concept_id: hosting-infrastructure
task_id: recipe-prepare-a-saas-migration
title: Recipe: Prepare a SaaS migration
generated: true
---

# Recipe: Prepare a SaaS migration

A provider-ready migration plan with a reserved test window and clear responsibility boundary.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. Choose the hosting partner and plan.
2. Inventory the current Rock version, database, files, domains, certificates, integrations, SMTP, plugins, custom code, jobs, and external dependencies.
3. Schedule the provider kickoff.
4. Define the migration sequence and rollback decision points.
5. Reserve a test period before public launch.
6. Confirm plan-specific responsibility for updates, backups, restores, certificates, domains, monitoring, incidents, and custom work.
7. Run representative administrative and public journeys in the migrated environment.
8. Stop before public launch if ownership, migration scope, or test results remain unresolved.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting
