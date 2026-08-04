---
concept_id: giving-finance
task_id: recipe-pledge-progress-analysis
title: Recipe: Pledge Progress Analysis
generated: true
---

# Recipe: Pledge Progress Analysis

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`

## Entities And Tables

- `Person`
- `Page`

## Steps

1. Pledge account.
2. Pledge date range.
3. Gift date range.
4. Pledge amount.
5. Transaction details to the pledged account.
6. Giving unit/person basis.
7. Refund/correction handling.
8. Current date vs analysis date.
9. v19.1 Pledge Analytics filter naming if installed.
10. Pledged amount.
11. Given amount.
12. Percent fulfilled.
13. Expected percent by elapsed time.
14. Meets/behind/ahead status.
15. Date/account assumptions.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/recipes/90
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contribution_UsingFrequency.sql
