---
concept_id: connections
task_id: recipe-validate-status-automation
title: Recipe: Validate status automation
generated: true
---

# Recipe: Validate status automation

A status rule moves only currently eligible requests and can be retried safely.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`

## Entities And Tables

- `DataView`

## Steps

1. Record the source status, destination status, Data View, job, and intended business rule.
2. Review the Data View with a bounded sample.
3. Confirm every returned request is still in the source status.
4. Remove unintended fixed cutoff dates or stale criteria.
5. If age in status matters, validate the available status-history evidence rather than assuming `ModifiedDateTime` represents the transition.
6. Run the automation through its configured job in a controlled scope.
7. Compare source and destination counts.
8. Verify request state consistency and review job history.
9. Re-evaluate the Data View to confirm moved requests no longer qualify.
10. Stop if history semantics or installed automation behavior cannot be verified.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/ModelMap
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request
- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz
