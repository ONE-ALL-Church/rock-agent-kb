---
id: answer:hosting-infrastructure:risks-caveats
concept_id: hosting-infrastructure
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Hosting And Infrastructure?

In a Rock web farm, files stored on a node's local file system are unavailable from other nodes unless the relevant directories are synchronized; Rock file types should therefore use cloud-backed or database-backed storage. In a self-hosted two-server Rock deployment, SQL Server should remain private and TCP 1433 should be limited to the Rock web server and any explicitly authorized development host. Rock v18 and later require SQL Server 2022 or newer according to the internal-hosting system requirements, including installations whose other sizing guidance still lists older SQL editions. In a Rock 19.0 web farm, scheduled jobs must be configured to run on only one node because the web-farm feature does not prevent multiple nodes from running them.

## Top Claims

- `claim:0ac39c6f9dbf72e1b72a`
- `claim:249814408c9c8842ef96`
- `claim:867da60eac2e0656c815`
- `claim:53bd55e60a2554640a1a`
- `claim:82f246088b04f492eae3`

## Distilled Claims

- `distilled-claim:4f8517744cd8958fbeb8`

## Citations

- [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)
- [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)
- [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)
- [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)
- [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server)
