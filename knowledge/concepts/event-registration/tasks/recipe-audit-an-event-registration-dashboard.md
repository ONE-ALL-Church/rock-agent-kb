---
concept_id: event-registration
task_id: recipe-audit-an-event-registration-dashboard
title: Recipe: Audit an event-registration dashboard
generated: true
---

# Recipe: Audit an event-registration dashboard

Every published metric has an explicit grain, population, and reconciliation test.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Label`

## Entities And Tables

- `Person`
- `Label`

## Steps

1. Inventory all metrics and label their grain.
2. Define confirmed, wait-listed, canceled, and other local populations.
3. Trace a multi-person registration through registration-level and registrant-level metrics.
4. Trace a wait-listed person through every chart.
5. Reconcile fee, payment, discount, and balance metrics separately.
6. Document local sources and precedence for staff, serving, or department segments.
7. Mark overlapping dimensions as non-additive.
8. If comparing events, align them by the chosen lifecycle stage.
9. Restrict participant drilldowns to the intended staff audience.
10. Stop publication if a metric cannot be reconciled or its local truth source cannot be validated.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-wait-lists
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/commands/entity-commands
- https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard
- https://www.youtube.com/watch?v=c-wycR9HEuQ&t=445s
