---
id: answer:hosting-infrastructure:first-checks
concept_id: hosting-infrastructure
generated: true
artifact_level: answer
---

# What should I check first for Hosting And Infrastructure?

In a self-hosted two-server Rock deployment, SQL Server should remain private and TCP 1433 should be limited to the Rock web server and any explicitly authorized development host. Rock v18 and later require SQL Server 2022 or newer according to the internal-hosting system requirements, including installations whose other sizing guidance still lists older SQL editions. Rock's Azure hosting layout places the web virtual machine, Azure SQL server, and Azure SQL database in a shared resource group, with IIS running on the web VM. Azure is a supported hosting path rather than a Rock requirement; organizations should choose among hosting options based on their scale, technical capacity, cost, and service quality needs.

## Top Claims

- `claim:249814408c9c8842ef96`
- `claim:867da60eac2e0656c815`
- `claim:bed80224adc3fdd6cdd5`
- `claim:68698a0c2c178f98cb2f`

## Citations

- [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)
- [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)
- [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting)
- [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting)
