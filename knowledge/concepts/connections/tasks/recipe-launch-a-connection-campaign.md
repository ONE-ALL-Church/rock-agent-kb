---
concept_id: connections
task_id: recipe-launch-a-connection-campaign
title: Recipe: Launch a connection campaign
generated: true
---

# Recipe: Launch a connection campaign

An eligible audience enters a controlled, assignable follow-up queue.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Group`
- `Campus`
- `Family`

## Entities And Tables

- `DataView`
- `Group`
- `Campus`
- `Family`

## Steps

1. Create or select the destination connection type and opportunity.
2. Configure the connector group and campus rules.
3. Build and validate the audience Data View.
4. Configure family limits and an opt-out group.
5. Choose All at Once or As Needed based on workload and request-age semantics.
6. Configure daily assignment limits, recurrence, and previous-connector preference where appropriate.
7. Confirm connector membership and any per-connector overrides.
8. Run a small controlled campaign cycle.
9. Compare eligible people, campaign-list entries, created requests, assignments, and exclusions.
10. Verify connector visibility and completion handling before increasing scale.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views
- https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/set-up-connection-campaigns
- https://community.rockrms.com/documentation/engagement/connections/connection-campaigns/intro-to-campaign-connectors
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs
- https://www.youtube.com/watch?v=7rxTGLLhlrU
- https://community.rockrms.com/ModelMap
