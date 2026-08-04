---
concept_id: connections
task_id: recipe-audit-one-connection-type
title: Recipe: Audit One Connection Type
generated: true
---

# Recipe: Audit One Connection Type

Complete Audit One Connection Type with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Campus`
- `Workflow`
- `Block`

## Entities And Tables

- `Group`
- `Campus`
- `Workflow`
- `Block`

## Steps

1. Type name/id/guid.
2. Active state.
3. Enabled views.
4. Statuses with order/default/active/auto behavior.
5. Opportunities with active state, order, campus, connector groups, default connector.
6. Open request counts by status/state.
7. Idle request count.
8. Future follow-up count.
9. Requests missing connector.
10. Workflows and automation summary.
11. Security concerns.
12. Version caveats.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/add-connection-request
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs
- https://community.rockrms.com/documentation/bookcontent/39
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionTypeFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionTypeDetail/connectionStatusAutomationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/ConnectionTypeDetail/ConnectionStatusAutomationBag.cs
- https://www.triumph.tech/resources/github-spotlight-422025
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-list
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-opportunity-list
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/ConnectionRequest/ConnectionOpportunityFilter.cs
