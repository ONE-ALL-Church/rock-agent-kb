---
concept_id: data-views-reports
task_id: recipe-diagnose-an-empty-bi-dashboard
title: Recipe: Diagnose an empty BI dashboard
generated: true
---

# Recipe: Diagnose an empty BI dashboard

Identify whether the failure is Rock population, job processing, external refresh, licensing, or authorization.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`
- `Schedule`

## Entities And Tables

- `Page`
- `Block`
- `Schedule`

## Steps

1. Record the expected domain and freshness.
2. Check whether Process BI Analytics has run successfully.
3. Confirm the domain process is enabled.
4. Identify any separate job instance responsible for that process.
5. Verify that the required `Analytics` views contain the expected bounded sample.
6. Check the external dataset or gateway refresh.
7. Verify external licensing and user entitlement.
8. Verify Rock page and block authorization.
9. Compare the dashboard timestamp with the Rock job completion time.
10. Report the failing layer without claiming the whole pipeline is verified.
11. Confirm that Process BI Analytics is scheduled.
12. Confirm that it has completed at least once.
13. Inspect whether the required domain process is enabled.
14. Check whether another BI job instance owns that process.
15. Verify the external dataset or gateway refresh after Rock’s job completes.
16. Confirm that the report uses published `Analytics` views rather than incomplete source tables. Use the BI Job,

## Do Not Assume

- a successful Rock job proves the cloud dataset refreshed;
- a visible embedded page proves the user is properly licensed;
- administrator access proves role access.

## Source Links

- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block
- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-data-block
- https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-bi-job
- https://community.rockrms.com/documentation/church-management/reporting/power-bi/use-the-on-premises-data-gateway
- https://community.rockrms.com/lava/commands/entity-commands
- https://www.youtube.com/watch?v=dpYJiOAiJYM&t=1490s
- https://community.rockrms.com/documentation/church-management/reporting/power-bi/intro-to-bi
