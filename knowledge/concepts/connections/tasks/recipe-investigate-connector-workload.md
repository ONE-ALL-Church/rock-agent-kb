---
concept_id: connections
task_id: recipe-investigate-connector-workload
title: Recipe: Investigate Connector Workload
generated: true
---

# Recipe: Investigate Connector Workload

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`

## Entities And Tables

- `Group`

## Steps

1. Connector group membership by opportunity.
2. Open request count by connector.
3. Requests with no connector.
4. Idle requests by connector.
5. Future follow-up by connector.
6. Availability/leave process.
7. Suggested assignment correction.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs
- https://www.triumph.tech/resources/github-spotlight-422025
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusAutomationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups
- https://community.rockrms.com/recipes/446
