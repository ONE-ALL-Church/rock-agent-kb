---
id: answer:hosting-infrastructure:first-checks
concept_id: hosting-infrastructure
generated: true
artifact_level: answer
---

# What should I check first for Hosting And Infrastructure?

With SaaS-hosted Rock, the hosting provider operates and monitors the cloud environment and database and manages infrastructure concerns such as maintenance, backups, certificates, domains, and incidents according to the selected plan; the organization remains responsible for its data, content, Rock configuration, users, security, workflows, and routine administration. Azure is a supported hosting path rather than a Rock requirement; organizations should choose among hosting options based on their scale, technical capacity, cost, and service quality needs. Rock v18 and later require SQL Server 2022 or newer according to the internal-hosting system requirements, including installations whose other sizing guidance still lists older SQL editions. A Rock web farm requires a Spark web-farm license and an active message-bus transport; Rock 19.0 supports Azure Service Bus or RabbitMQ, with only one transport active.

## Top Claims

- `claim:8c1831684d187b61b4b3`
- `claim:68698a0c2c178f98cb2f`
- `claim:867da60eac2e0656c815`
- `claim:89bb09e36da247e182b1`
- `claim:3800f13989d805462464`
- `claim:dba9f8a7413cfd92b396`
- `claim:b6d0c03e3e8239dd60fa`
- `claim:0ac39c6f9dbf72e1b72a`

## Citations

- [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)
- [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting)
- [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)
- [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)
- [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)
- [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)
