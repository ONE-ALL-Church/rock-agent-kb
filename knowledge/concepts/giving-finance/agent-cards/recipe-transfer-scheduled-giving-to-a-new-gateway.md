---
concept_id: giving-finance
task_id: recipe-transfer-scheduled-giving-to-a-new-gateway
title: Recipe: Transfer scheduled giving to a new gateway
generated: true
---

# Recipe: Transfer scheduled giving to a new gateway

Route new gifts to the new provider while giving existing scheduled donors a controlled transfer path.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Block`

## Entities And Tables

- `Schedule`
- `Block`

## Steps

1. Verify the installed block generation and gateway-provider support.
2. Configure and test the new gateway without modifying the Test Gateway into a live gateway.
3. Change the Give Now surface so new profiles use the new gateway.
4. Configure the Manage Giving Profiles surface to identify old-gateway profiles and offer transfer.
5. Test the transfer with an authorized non-production profile.
6. Verify creation of the replacement profile and deletion of the old profile only after completion.
7. Track remaining old-gateway profiles without exposing payment data.
8. Keep the old gateway available only as required by the migration and provider plan.

## Do Not Assume

- Changing Give Now migrates existing schedules.
- Making the old gateway inactive stops every assigned charge.
- Gateway-held payment credentials can be exported.

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
