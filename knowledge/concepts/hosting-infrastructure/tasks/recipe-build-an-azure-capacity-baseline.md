---
concept_id: hosting-infrastructure
task_id: recipe-build-an-azure-capacity-baseline
title: Recipe: Build an Azure capacity baseline
generated: true
---

# Recipe: Build an Azure capacity baseline

A provisional Azure tier supported by workload evidence and marked for validation.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Schedule`

## Entities And Tables

- `Attendance`
- `Schedule`

## Steps

1. Record peak weekend attendance.
2. Select the corresponding starting tier from the current Rock Azure sizing table.
3. Move one tier larger if Rock hosts the public website.
4. Adjust for database size, feature intensity, analytics, reports, check-in, scheduled jobs, integrations, plugins, and growth.
5. Use the documented Windows VM plus Azure SQL pattern as the baseline.
6. Retrieve current Azure SKU availability and pricing before budgeting.
7. Define the telemetry and representative journeys that will validate the tier.
8. Stop when the baseline, assumptions, and post-provision validation plan are recorded.

## Do Not Assume

- Attendance predicts every workload.
- Prices or nonprofit credits in an older excerpt remain current.
- More memory alone resolves a CPU or database bottleneck.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options
