---
concept_id: giving-finance
task_id: recipe-trace-a-public-gift-end-to-end
title: Recipe: Trace a public gift end to end
generated: true
---

# Recipe: Trace a public gift end to end

Account for a gift from donor action through its Rock records and reporting treatment.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Location`
- `Page`

## Entities And Tables

- `Person`
- `Location`
- `Page`

## Steps

1. Record the entry surface, date, intended person or business, amount, and intended account without collecting payment secrets.
2. Inspect the page’s gateway, transaction type, source, account, batch-prefix, and receipt settings.
3. Determine whether processing is immediate, future-dated, or recurring.
4. Confirm gateway outcome using a safe provider reference.
5. Locate the Rock transaction and inspect all transaction details.
6. Confirm the account on each detail and the sum of the allocations.
7. Locate the batch and compare status, totals, control values, account totals, and currency totals.
8. Check receipt configuration and evidence independently.
9. Reproduce any report or statement with its exact inclusion rules.
10. Record which links were observed and which remain unverified.

## Do Not Assume

- Gateway acceptance proves Rock synchronization.
- A transaction has only one account.
- A receipt was sent.
- A report uses transaction-date grain.

## Source Links

- https://community.rockrms.com/documentation/church-management/finance/advanced-finance/advanced-utility-payment-entry-block-settings
- https://community.rockrms.com/documentation/church-management/finance/online-giving/giving-pages
- https://community.rockrms.com/documentation/church-management/finance/track-giving/view-giving-on-person-profile
- https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway
- https://community.rockrms.com/rocku/finance/giving-journey-1
