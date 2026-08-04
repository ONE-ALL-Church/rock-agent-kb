---
concept_id: giving-finance
task_id: recipe-giving-automation-review
title: Recipe: Giving Automation Review
generated: true
---

# Recipe: Giving Automation Review

The recurring-giving prompt recipe is a useful pattern but includes a clear warning about external recurring profiles not synced into Rock (Automate asking Regular Givers to Set up Recurring Giving).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Schedule`

## Entities And Tables

- `DataView`
- `Schedule`

## Steps

1. Data View criteria.
2. Transaction source and type filters.
3. Account filters.
4. Date logic.
5. Scheduled transaction visibility.
6. Gateway sync completeness.
7. Exclusions and opt-outs.
8. Communication approval.
9. Test recipient count.
10. Audience definition.
11. Known false positives/negatives.
12. Test SQL/Data View count.
13. Recommended dry run.
14. Communication review requirements.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentFrequencyConfiguration.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationOptions.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfiguration.cs
- https://community.rockrms.com/rocku/finance/scheduled-transactions
- https://community.rockrms.com/recipes/122
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/FinancialScheduledTransactionDetail/AccountFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/FinancialScheduledTransactionPaymentPlanPair.cs
