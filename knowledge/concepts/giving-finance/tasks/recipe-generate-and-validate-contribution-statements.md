---
concept_id: giving-finance
task_id: recipe-generate-and-validate-contribution-statements
title: Recipe: Generate and validate contribution statements
generated: true
---

# Recipe: Generate and validate contribution statements

Produce a reviewable statement set whose population and finance rules are explicit.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Family`

## Entities And Tables

- `Person`
- `Family`

## Steps

1. Verify Statement Generator compatibility, user role, and Rock version.
2. Select the population and decide how inactive people and businesses are handled.
3. Review family and individual giving-unit settings for exceptions.
4. Copy or select a contribution template.
5. Verify accounts, currency types, transaction types, refund rules, same-day corrections, and pledge settings.
6. Set period, minimum contribution, suppression behavior, sort, split, and output settings.
7. Generate single-person samples representing family, individual, business, refund, non-cash, and pledge scenarios that actually apply.
8. Compare each sample with underlying transaction details.
9. Run the full generation.
10. Preserve and review the generated summary separately from printing or delivery.

## Do Not Assume

- Generated means delivered.
- Family membership alone determines the giving unit.
- Pledges appear by default.
- Web and PDF output are visually identical.

## Source Links

- https://community.rockrms.com/documentation/church-management/finance/contribution-statements/use-contribution-statement-templates
- https://community.rockrms.com/documentation/church-management/finance/track-giving/view-giving-on-person-profile
- https://community.rockrms.com/documentation/church-management/finance/track-giving/family-giving
- https://community.rockrms.com/documentation/church-management/finance/contribution-statements/set-up-the-statement-generator-software
