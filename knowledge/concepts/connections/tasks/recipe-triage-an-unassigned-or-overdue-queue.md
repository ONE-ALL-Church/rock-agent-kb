---
concept_id: connections
task_id: recipe-triage-an-unassigned-or-overdue-queue
title: Recipe: Triage an unassigned or overdue queue
generated: true
---

# Recipe: Triage an unassigned or overdue queue

Every selected request has a verified owner or an explicit disposition.

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

1. Open the intended connection type and campus.
2. Filter to Active and Unassigned or Overdue requests.
3. Confirm due-date rules before prioritizing by lateness.
4. Group or sort by opportunity, campus, due date, or status.
5. Review connector capacity and eligibility.
6. Assign bounded batches to appropriate connectors.
7. Use Future Follow-up only when a real future date is known.
8. Transfer poor-fit requests instead of leaving them stalled.
9. Read bulk-action result counts and inspect exceptions.
10. Reopen the filtered queue and verify the remaining population.
11. Confirm the metric's campus, type, and opportunity scope.
12. Inspect the connection type's due-date calculation mode.
13. Check opportunity- and status-level due-date or due-soon offsets.
14. Confirm whether the request has a calculated due date.
15. Separate active requests from Future Follow-up, inactive, and completed requests.
16. Open a small sample of underlying requests and reproduce the expected calculation.
17. Stop when the discrepancy is explained or a version-specific defect is reproducible.

## Do Not Assume

- That every red metric represents the same urgency.
- That assignment means contact occurred.
- That an empty visible list means the scoped queue is empty.

## Source Links

- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views
- https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests
- https://community.rockrms.com/documentation/engagement/connections/connection-requests/operational-snapshot
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs
- https://www.youtube.com/watch?v=7rxTGLLhlrU
