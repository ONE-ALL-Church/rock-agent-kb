---
concept_id: connections
task_id: recipe-transfer-and-complete-a-request-safely
title: Recipe: Transfer and complete a request safely
generated: true
---

# Recipe: Transfer and complete a request safely

The request reaches the correct destination with ownership and placement preserved.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Campus`
- `Attribute`

## Entities And Tables

- `Group`
- `Campus`
- `Attribute`

## Steps

1. Review current comments, attributes, activities, campus, connector, and due date.
2. Confirm transfer is preferable to completing or inactivating the request.
3. Search for the best destination opportunity.
4. Choose the destination campus and status when those controls are enabled.
5. Select the destination's default connector, current connector, another eligible connector, or no connector deliberately.
6. Set the destination due date and add a transfer note.
7. Verify the destination request details and activity history.
8. When ready for completion, verify final status, placement group, role, member status, requirements, and required completion note.
9. Complete the request.
10. Verify the resulting placement and inactive/completed state.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/documentation/engagement/connections/connection-requests/connections-views
- https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-requests
- https://community.rockrms.com/documentation/engagement/connections/configure-connections/configure-connection-opportunities
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/CodeGenerated/ConnectionOpportunityConnectorGroupsController.CodeGenerated.cs
- https://www.youtube.com/watch?v=7rxTGLLhlrU
