---
concept_id: giving-finance
task_id: recipe-build-a-detail-preserving-finance-report
title: Recipe: Build a detail-preserving finance report
generated: true
---

# Recipe: Build a detail-preserving finance report

Show each account allocation with transaction-level context without accidental row collapse.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Location`
- `Family`
- `Page`

## Entities And Tables

- `Person`
- `Group`
- `Location`
- `Family`
- `Page`

## Steps

1. Define whether the output grain is transaction, transaction detail, giving unit, person, family, registration, registrant, or batch.
2. Begin with the entity that represents that grain.
3. For detail-level reporting, retain one row per financial transaction detail.
4. Use `OVER (PARTITION BY TransactionId)` when transaction totals or detail counts must appear beside each detail.
5. Add ranking functions only when the report requires sequence, rank, or buckets.
6. Test a transaction split across multiple accounts.
7. Compare the sum of detail rows with the expected transaction and batch totals.
8. Secure the report and every page or dashboard that exposes it.

## Do Not Assume

- `GROUP BY` and a window function preserve the same rows.
- One registration equals one registrant.
- One transaction equals one account allocation.
- A report creator’s permission protects report viewers.

## Source Links

- https://www.triumph.tech/resources/sql-window-functions
- https://community.rockrms.com/documentation/church-management/finance/fundraising-groups/fundraising-financial-transactions
- https://community.rockrms.com/documentation/church-management/finance/advanced-finance/advanced-utility-payment-entry-block-settings
- https://community.rockrms.com/documentation/church-management/finance/online-giving/giving-pages
- https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations
- https://community.rockrms.com/documentation/church-management/finance/fundraising-groups
- https://community.rockrms.com/documentation/church-management/finance/track-giving/view-giving-on-person-profile
- https://community.rockrms.com/documentation/church-management/finance/track-giving/family-giving
- https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql
