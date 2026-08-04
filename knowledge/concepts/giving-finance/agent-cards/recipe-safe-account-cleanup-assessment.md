---
concept_id: giving-finance
task_id: recipe-safe-account-cleanup-assessment
title: Recipe: Safe Account Cleanup Assessment
generated: true
---

# Recipe: Safe Account Cleanup Assessment

Complete Safe Account Cleanup Assessment with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Location`
- `Schedule`
- `Block`
- `Attribute`

## Entities And Tables

- `DataView`
- `Location`
- `Schedule`
- `Block`
- `Attribute`

## Steps

1. Historical transactions by account.
2. Scheduled transaction details.
3. Pledges.
4. Online giving block settings.
5. Statement saved settings.
6. Reports/Data Views.
7. External fund mappings.
8. Attributes/integrations.
9. Security.
10. Whether account can be deactivated.
11. What still references it.
12. Whether transactions should remain historical.
13. Migration plan if allocations must move.
14. Risks to statements and reporting.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentFrequencyConfiguration.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationOptions.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfiguration.cs
- https://community.rockrms.com/recipes/254
- https://community.rockrms.com/rocku/finance/scheduled-transactions
- https://community.rockrms.com/documentation/bookcontent/15
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/FinancialScheduledTransactionDetail/AccountFilter.cs
