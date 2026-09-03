---
concept_id: hosting-infrastructure
task_id: recipe-select-a-hosting-model
title: Recipe: Select a hosting model
generated: true
---

# Recipe: Select a hosting model

A documented hosting choice with explicit ownership, workload, security, and verification conditions.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Restate the underlying organizational problem.
2. Produce distinct options that include at least SaaS hosting and self-managed hosting; include Azure only when it fits the requirements.
3. Inventory staff capacity, peak workload, public-site use, payment processing, integrations, plugins, customizations, availability goals, and budget constraints.
4. For each option, assign ownership for infrastructure, database, patches, certificates, domains, backups, monitoring, incidents, Rock configuration, users, and workflows.
5. Reject any single-server payment-processing topology.
6. Compare the options and record the unresolved live checks.
7. Stop when the selected model has a named owner for every operational responsibility.

## Do Not Assume

- Azure is required.
- SaaS transfers ownership of Rock configuration.
- A lower-cost provider supplies equivalent Rock expertise or service quality.
- A proposed platform is the only way to solve the underlying problem.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting
- https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server
- https://community.rockrms.com/rocku/workflows/text-to-workflow-performance
