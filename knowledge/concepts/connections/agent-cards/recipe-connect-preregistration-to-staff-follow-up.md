---
concept_id: connections
task_id: recipe-connect-preregistration-to-staff-follow-up
title: Recipe: Connect preregistration to staff follow-up
generated: true
---

# Recipe: Connect preregistration to staff follow-up

A preregistered family reaches a verified staff-owned next step without avoidable duplicate records.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Step`
- `Campus`
- `Family`
- `Workflow`
- `Page`
- `Attribute`
- `Schedule`

## Entities And Tables

- `Person`
- `Step`
- `Campus`
- `Family`
- `Workflow`
- `Page`
- `Attribute`
- `Schedule`

## Steps

1. Explain the practical value of preregistration on the public page.
2. Collect only the information required for the arrival and follow-up process.
3. Test person and family matching with representative scenarios.
4. Verify check-in eligibility and campus handling.
5. Create the intended workflow or connection request using reviewed mappings.
6. Preserve only an appropriate source reference and approved attributes.
7. Verify the request's opportunity, status, campus, comments, and assignment.
8. Complete a staff follow-up test.
9. Inspect for duplicate or partial people and family records.
10. Repeat the full path before broad publication.
11. Confirm the request is in Future Follow-up state.
12. Inspect the stored follow-up date.
13. Confirm the date has passed in the installation's effective time context.
14. Inspect the Connection Request Workflow Triggers job's schedule and recent results.
15. Check whether another workflow or status rule changed the request after deferral.
16. Re-open the request without restrictive list filters.
17. Stop when the job, date, state, or filter condition explains the behavior.

## Do Not Assume

- That registration success proves person matching, check-in eligibility, or staff follow-up.
- That the presence of relevant Rock tables proves the flow is configured.

## Source Links

- https://community.rockrms.com/documentation/engagement/connections/connections-tools/connection-workflows
- https://community.rockrms.com/documentation/engagement/connections/connections-tools/bulk-update-connection-requests
- https://www.rockrms.com/releasenotes
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request
- https://community.rockrms.com/recipes/57
- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz
- https://community.rockrms.com/documentation/engagement/connections/overview/intro-to-connections
