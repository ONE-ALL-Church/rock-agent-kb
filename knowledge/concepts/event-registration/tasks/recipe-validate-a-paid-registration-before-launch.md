---
concept_id: event-registration
task_id: recipe-validate-a-paid-registration-before-launch
title: Recipe: Validate a paid registration before launch
generated: true
---

# Recipe: Validate a paid registration before launch

Evidence that representative costs and payment paths produce the intended registration and financial state.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. Confirm whether cost is owned by the template or instance.
2. Verify the financial account and gateway.
3. Test base cost, every required or optional fee used by the event, and representative discounts.
4. If partial payments are enabled, test the minimum initial payment and default amount.
5. If payment plans are enabled, verify provider compatibility and inspect the plan at the gateway.
6. Confirm payment, total cost, balance, fees, and discounts on the registration.
7. Test confirmation and payment-reminder communications.
8. Test an authorized manual payment and refund in a safe environment or approved reversible scenario.
9. Document how post-registration balance changes will be reconciled with gateway schedules.
10. Stop before launch if Rock and the gateway disagree.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/registration-finances
