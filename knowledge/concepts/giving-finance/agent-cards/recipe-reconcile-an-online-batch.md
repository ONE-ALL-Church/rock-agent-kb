---
concept_id: giving-finance
task_id: recipe-reconcile-an-online-batch
title: Recipe: Reconcile an online batch
generated: true
---

# Recipe: Reconcile an online batch

Explain every batch total and variance at the correct grain.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Confirm batch status; wait for an automated pending batch to complete.
2. Record the transaction total, control amount, and amount variance.
3. Record transaction count, control count, and count variance.
4. Review transaction details for split-account gifts.
5. Compare account and currency totals.
6. Resolve unmatched imported items through the intended matching workflow.
7. Review the audit log for edits.
8. Compare the reconciled batch total with the external settlement or general-ledger handoff according to the organization’s documented process.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/church-management/finance/financial-components/batches
