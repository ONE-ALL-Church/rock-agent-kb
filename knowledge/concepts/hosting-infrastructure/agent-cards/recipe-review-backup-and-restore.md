---
concept_id: hosting-infrastructure
task_id: recipe-review-backup-and-restore
title: Recipe: Review Backup And Restore
generated: true
---

# Recipe: Review Backup And Restore

Complete Review Backup And Restore with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Step`

## Entities And Tables

- `Person`
- `Step`

## Steps

1. Database backup method.
2. File backup method.
3. Web root/config backup method.
4. Retention.
5. Restore test date.
6. Restore duration.
7. Missing secrets or dependencies.
8. Disaster recovery steps.
9. Person/team responsible.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Security/AccountEntry/AccountEntryStep.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialPersonSavedAccountService/Options/FinancialPersonSavedAccountQueryOptions.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration.Performance/BenchmarkRunners/PersonSearchBenchmarks.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Security/Login/PasswordlessLoginStep.cs
