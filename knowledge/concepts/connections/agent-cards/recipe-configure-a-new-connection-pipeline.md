---
concept_id: connections
task_id: recipe-configure-a-new-connection-pipeline
title: Recipe: Configure a new connection pipeline
generated: true
---

# Recipe: Configure a new connection pipeline

A bounded connection type and opportunity are ready for controlled staff testing.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Campus`
- `Workflow`

## Entities And Tables

- `Group`
- `Campus`
- `Workflow`

## Steps

1. Define the real lifecycle, responsible team, completion condition, and escalation path.
2. Create or select the connection type.
3. Configure only the statuses that represent genuine lifecycle stages.
4. Choose whether sequential status mode matches the process.
5. Configure states, activities, sources, due-date rules, enabled views, and request security.
6. Create the opportunity with public summary and details.
7. Configure campus scope, connector groups, default connectors, placement groups, roles, member statuses, transfer controls, and workflows.
8. Create test requests through each intended intake path.
9. Exercise assignment, status movement, activity logging, future follow-up, transfer, placement, and completion.
10. Train connectors on the enabled v19 views before broad rollout.

## Do Not Assume

- That a default connector exists for every campus.
- That a public opportunity is discoverable.
- That completion creates the intended membership without verification.

## Source Links

- https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows
- https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests
- https://www.rockrms.com/releasenotes
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views
- https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-types
- https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs
- https://www.youtube.com/watch?v=7rxTGLLhlrU
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request
- https://community.rockrms.com/recipes/57
