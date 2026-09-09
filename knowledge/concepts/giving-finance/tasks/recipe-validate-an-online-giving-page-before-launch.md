---
concept_id: giving-finance
task_id: recipe-validate-an-online-giving-page-before-launch
title: Recipe: Validate an online giving page before launch
generated: true
---

# Recipe: Validate an online giving page before launch

Establish that the page’s configuration expresses the intended finance path.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Campus`
- `Page`
- `Block`

## Entities And Tables

- `Schedule`
- `Campus`
- `Page`
- `Block`

## Steps

1. Identify the installed Rock version and exact Utility Payment Entry or legacy block.
2. Verify the gateway and whether its mode represents test/live or hosted/unhosted.
3. Confirm enabled payment methods.
4. Confirm transaction type, source, accounts, campus mapping, and scheduled-giving option.
5. Confirm batch prefix and gateway batch timing.
6. Confirm business, anonymous, CAPTCHA, confirmation-page, and receipt settings as applicable.
7. Execute an authorized non-production test.
8. Verify the gateway result, Rock transaction, details, account, batch, receipt behavior, and visible giving history.

## Do Not Assume

- A gateway named “Test” is harmless if it has been reconfigured.
- An active gateway is selected by the page.
- A successful confirmation page proves downstream records.

## Source Links

- https://community.rockrms.com/documentation/church-management/finance
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/FinancialScheduledTransactionDetail/AccountFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentFrequencyConfiguration.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationOptions.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/FinancialScheduledTransactionPaymentPlanPair.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfiguration.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs
- https://community.rockrms.com/rocku/finance/scheduled-transactions
- https://community.rockrms.com/recipes/90
