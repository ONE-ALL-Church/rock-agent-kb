---
concept_id: event-registration
task_id: recipe-audit-discount-codes
title: Recipe: Audit Discount Codes
generated: true
---

# Recipe: Audit Discount Codes

Return codes only to authorized staff.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. Template discount configuration.
2. Active and scheduled codes.
3. Usage counts.
4. Applies-to scope.
5. Current instances using the template.
6. Staff visibility requirements.
7. v19.1 discount column behavior.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
