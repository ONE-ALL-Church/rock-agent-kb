---
concept_id: event-registration
task_id: recipe-audit-payment-risk
title: Recipe: Audit Payment Risk
generated: true
---

# Recipe: Audit Payment Risk

Return a prioritized collection list.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. Registrations with balance due.
2. Confirmation emails present/missing.
3. Last reminder date.
4. Payment plans active.
5. Gateway schedule state.
6. Failed transactions.
7. Discounts applied after plan creation.
8. Event date proximity.
9. Staff owner.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
