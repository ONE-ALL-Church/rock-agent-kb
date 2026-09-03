---
concept_id: hosting-infrastructure
task_id: recipe-activate-a-rock-19-web-farm
title: Recipe: Activate a Rock 19 web farm
generated: true
---

# Recipe: Activate a Rock 19 web farm

All expected Rock nodes are visible and coordinated without duplicate job runners.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Page`

## Entities And Tables

- `Schedule`
- `Page`

## Steps

1. Obtain and record the Spark web-farm license.
2. Confirm that the gateway, database, web nodes, and Rock installations are running.
3. Configure session affinity at the gateway.
4. Move shared Rock File Types away from node-local storage or establish deliberate synchronization.
5. Configure one supported message-bus transport: Azure Service Bus or RabbitMQ.
6. Configure jobs to run on only one node.
7. Open `Admin Tools > System Settings > Web Farm`.
8. Activate the farm and enter the license.
9. Restart every web node.
10. Confirm every expected node appears on the Web Farm page.
11. Exercise cache-affecting changes, shared files, page routes, check-in sessions, and a scheduled job.
12. Stop when node membership, affinity, shared-file access, message-bus coordination, and single job execution are proven.
13. Confirm that the Spark web-farm license is active.
14. Confirm that exactly one supported message-bus transport is active.
15. Verify that the gateway, database, and expected web nodes are running.
16. Confirm that Rock is installed on each node.
17. Restart all nodes after web-farm activation or configuration changes.
18. Inspect the Web Farm page and web-farm log for startup, shutdown, status, or leadership events.
19. Confirm that every expected node appears.
20. Stop when node membership and message-bus communication are stable.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock
- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis
- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster
- https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s
