---
id: answer:hosting-infrastructure:risks-caveats
concept_id: hosting-infrastructure
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Hosting And Infrastructure?

In a self-hosted two-server Rock deployment, SQL Server should remain private and TCP 1433 should be limited to the Rock web server and any explicitly authorized development host. Rock v18 and later require SQL Server 2022 or newer according to the internal-hosting system requirements, including installations whose other sizing guidance still lists older SQL editions.

## Top Claims

- `claim:249814408c9c8842ef96`
- `claim:867da60eac2e0656c815`

## Citations

- [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)
- [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)
