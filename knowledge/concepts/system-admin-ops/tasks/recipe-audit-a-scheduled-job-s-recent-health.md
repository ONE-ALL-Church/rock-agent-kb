---
concept_id: system-admin-ops
task_id: recipe-audit-a-scheduled-job-s-recent-health
title: Recipe: Audit a scheduled job’s recent health
generated: true
---

# Recipe: Audit a scheduled job’s recent health

Determine whether recorded executions match the expected schedule and whether the downstream result is current.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Label`

## Entities And Tables

- `Schedule`
- `Label`

## Steps

1. Identify the exact scheduled job.
2. Inspect several consecutive history records.
3. Compare expected schedule with start and stop timestamps.
4. Review status, status message, and duration.
5. Check whether the installed version is affected by the v19.5 job-history defects.
6. Inspect the job’s downstream artifact, such as index freshness, automated record changes, or persisted data.
7. Report history status and downstream verification separately.
8. Inspect the job’s expected schedule and its most recent consecutive history rows.
9. Compare start time, stop time, status, status message, and duration rather than relying on the last status label alone.
10. Check whether the installed version predates the v19.5 fix for jobs silently stopping after errors while recording status, writing history, or sending notifications.
11. If rows are duplicated, falsely `Incomplete`, or show implausible durations for extremely fast work, check applicability of the separate v19.5 sub-second-history fix.
12. Verify the downstream result independently; history recording and business work are related but not identical outcomes.
13. Stop when version applicability or the installed job configuration cannot be established without live review. Rock release notes

## Do Not Assume

- A false `Incomplete` row on an affected version proves the job failed.
- A successful history row proves the intended business records changed.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/specs/completed/core/260731-servicejobhistory-sub-second-orphaned-incomplete-rows.md
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/ScheduledJobHistoryList/scheduledJobHistoryListOptionsBag.d.ts
