---
concept_id: giving-finance
task_id: recipe-read-only-finance-record-inspection
title: Recipe: Read-Only Finance Record Inspection
generated: true
---

# Recipe: Read-Only Finance Record Inspection

Complete Read-Only Finance Record Inspection with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Location`
- `Block`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Location`
- `Block`

## Steps

1. Transaction header.
2. Transaction details.
3. Payment detail.
4. Batch.
5. Authorized person alias and person/business.
6. Account(s).
7. Gateway transaction code.
8. Receipt communication.
9. Statement eligibility.
10. Audit history.
11. Exceptions.
12. Transaction ID/GUID.
13. Donor identity.
14. Date/time.
15. Total amount and detail allocations.
16. Payment method.
17. Batch status.
18. Receipt status.
19. Statement eligibility and blockers.
20. Recommended next action.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contribution_UsingFrequency.sql
- https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes
