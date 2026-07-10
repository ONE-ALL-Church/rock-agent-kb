---
concept_id: hosting-infrastructure
generated: true
artifact_level: claim_graph
approved_claim_count: 4
---

# Hosting And Infrastructure Approved Claims

This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.

| Claim ID | Authority | Type | Claim | Source |
| --- | --- | --- | --- | --- |
| `claim:bed80224adc3fdd6cdd5` | official | implementation_pattern | Rock's Azure hosting layout places the web virtual machine, Azure SQL server, and Azure SQL database in a shared resource group, with IIS running on the web VM. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting) |
| `claim:68698a0c2c178f98cb2f` | official | operational_guidance | Azure is a supported hosting path rather than a Rock requirement; organizations should choose among hosting options based on their scale, technical capacity, cost, and service quality needs. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) |
| `claim:867da60eac2e0656c815` | official | release_caveat | Rock v18 and later require SQL Server 2022 or newer according to the internal-hosting system requirements, including installations whose other sizing guidance still lists older SQL editions. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) |
| `claim:249814408c9c8842ef96` | official | risk | In a self-hosted two-server Rock deployment, SQL Server should remain private and TCP 1433 should be limited to the Rock web server and any explicitly authorized development host. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment) |
