---
id: authored-hosting-infrastructure
title: Hosting And Infrastructure
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Hosting And Infrastructure

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Hosting And Infrastructure index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock hosting is not one setting or one server choice. It is the operational boundary around the whole Rock instance: the web runtime, SQL database, file storage, mail transport, cache behavior, search indexing, background jobs, SSL, DNS, backups, patching, monitoring, recovery, and the staff practices that keep those pieces predictable.

For most agent tasks, start with four questions:

1. Where does Rock run?
2. Where does the database run?
3. Where do files and integrations depend on infrastructure outside Rock?
4. What proof exists that the system can be restored, scaled, patched, and monitored?

Rock’s official hosting documentation divides the subject into SaaS hosting, Azure hosting, internal hosting, and scaling guidance. The official Hosting index links those major areas from [Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting), with deeper paths for [Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting), [Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting), [SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting), and [Scale Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock).

The critical operational distinction is responsibility. In SaaS hosting, a provider handles most infrastructure, updates, monitoring, and backups while the church team operates Rock itself, as summarized in [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting). In self-hosted Azure or internal hosting, the church or its partner owns the server, database, network, certificate, file storage, SMTP, backup, and monitoring posture. In scaled hosting, the team also owns distributed runtime concerns such as load balancing, message bus behavior, node identity, leader election, and read-only database routing, all introduced in [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster), [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm), and [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context).

For agents doing real Rock work, hosting decisions should be treated as production-change decisions. Do not assume the public website, internal staff UI, check-in, jobs, integrations, and file storage all have the same risk profile. A small church using only basic staff workflows can run safely on a simpler architecture than a large church running Rock as its public CMS, giving platform, check-in engine, workflow automation hub, mobile backend, search surface, and integration broker. Rock’s Azure sizing guidance explicitly warns that attendance alone is only a starting point because a medium-sized church using many Rock features heavily may need more resources than a larger church using Rock lightly [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options).

The most useful hosting evidence for an agent is not a verbal statement like “we are on Azure.” It is an infrastructure map, current Azure or server inventory, connection string inventory, Rock version, job schedule, storage provider list, mail transport configuration, certificate status, backup restore proof, and current performance telemetry. Community and partner material reinforce this operational habit: infrastructure maps make troubleshooting faster and reduce reliance on memory [The Importance of Infrastructure Maps](https://www.triumph.tech/resources/the-importance-of-infrastructure-maps), while monitoring and alerting should track infrastructure health, backups, SSL, CPU, memory, and related signals [Introducing Imperator: Proactive Azure Monitoring and Alerting for Rock RMS](https://www.triumph.tech/resources/introducing-imperator-proactive-azure-monitoring-and-alerting-for-rock-rms).

When a fact cannot be proven from documentation or the source pack, inspect the live Rock instance rather than inventing behavior. In particular, verify current Rock version, installed plugins, storage providers, configured transports, job schedules, web farm status, connection strings, SQL tier, Azure service sizes, security rules, and backup policies in the actual environment.

## 2. Scope And Terminology

This guide covers Rock RMS hosting and infrastructure. It includes:

- SaaS hosting, Azure hosting, internal Windows/IIS hosting, and scaled web farm hosting.
- Application server, database server, load balancer, file storage, SMTP, DNS, SSL, caching, jobs, search, observability, and backup posture.
- Operational readiness for production, staging, development, and disaster recovery.
- Agent-oriented inspection tasks and troubleshooting branches.
- Version caveats from release notes where hosting-related behavior changed.

This guide does not replace vendor-specific Azure, Windows Server, SQL Server, network, or security documentation. It translates the Rock-specific hosting surface into operational decisions and inspection paths.

Key terms:

**Rock application server** means the Windows/IIS or platform runtime that serves Rock’s ASP.NET application. In internal hosting this is commonly an IIS server. In Azure this may be a Windows VM or, in community examples, an Azure App Service. In SaaS it is provider-managed.

**Rock database** means the SQL Server or Azure SQL Database holding Rock’s operational data. The official internal hosting guide distinguishes Azure SQL Database from SQL Server on Azure VMs because account creation and administration differ [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server).

**Internal hosting** means the church or partner manages Windows Server, IIS, SQL Server, firewall, certificates, backups, and updates. Rock’s internal hosting documentation starts from Windows Server because Rock was developed on Microsoft’s ASP.NET platform and requires a Windows Server environment in that official self-hosting path [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting).

**Azure hosting** means Rock runs on Azure-provisioned infrastructure. This may include Windows Server VMs, Azure SQL Database, Azure Storage, Application Gateway, and supporting Azure services. The official Azure guide emphasizes cost and quality, including Microsoft nonprofit credits where eligible [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting).

**SaaS hosting** means a provider installs, secures, updates, monitors, backs up, and hosts Rock while the church uses Rock. The provider owns much of the infrastructure burden, but the church still owns data governance, configuration decisions, user access, ministry process, and escalation paths [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting).

**Scaling up** means increasing capacity on existing resources, such as adding CPU, memory, storage, DTUs, vCores, or a larger App Service/VM tier. **Scaling out** means adding nodes, usually with load balancing and distributed-state coordination. Rock’s scaling guide uses these vertical and horizontal scaling concepts in [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster).

**Web farm** means multiple Rock web nodes operate together behind shared infrastructure. Rock’s web farm documentation requires prework such as a web farm license key and configured infrastructure before activating the feature [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm).

**Read-only context** means Rock can use a read-only database connection for eligible reads, reducing load on the primary database. Azure Business Critical or Premium SQL tiers may provide a read-only replica, but the actual connection strings and behavior must be verified in the instance [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context).

## 3. Hosting And Infrastructure Mental Model

Think of Rock infrastructure as five layers.

### Layer 1: Request Entry

This includes DNS, SSL/TLS, CDN or reverse proxy if used, web application firewall if used, load balancer or Azure Application Gateway if used, and the inbound firewall rules. In a single-server internal install, request entry may simply be DNS pointing to a public IP with IIS serving HTTP/HTTPS. In a cluster, the request entry layer is responsible for sending traffic to healthy web nodes and avoiding failed nodes, which is one of the central duties described for the application gateway in [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster).

Agent inspection should confirm:

- Public and internal hostnames.
- Certificate issuer, expiration, renewal method, and bound sites.
- Whether HTTP redirects to HTTPS and where that redirect is implemented.
- Whether the load balancer does health checks and what path it checks.
- Whether staff, public, API, webhook, mobile, and check-in traffic all share the same ingress path.
- Whether source IP restrictions exist for admin/RDP/SQL management.

### Layer 2: Web Runtime

This is where Rock code runs. In internal hosting, this is IIS on Windows Server. Rock’s IIS article includes application pool settings such as .NET Framework Version v4.0, Start Mode Always Running, Identity LocalSystem, Idle Time-out 0, and recycling changes in the official configuration path [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis). Agents should not blindly apply these settings to every environment, especially hosted or customized environments, but they are important landmarks for diagnosing cold starts, application pool behavior, and runtime instability.

Agent inspection should confirm:

- IIS site bindings.
- Application pool identity, idle timeout, start mode, and recycle schedule.
- Rock physical path and deployed code version.
- `web.ConnectionStrings.config` target database.
- Whether the app is preloaded or kept warm.
- Whether multiple sites or environments share one server or app pool.
- Whether logs and temp/cache directories are growing unexpectedly.

Community material on preloading Rock reinforces the operational issue: after restart, the first request can be slow if IIS has not started and initialized the Rock application; preload/always-running patterns reduce that first-hit delay [Preload Rock For a Faster Start](https://community.rockrms.com/recipes/176).

### Layer 3: Database And Persistence

Rock is database-centered. A slow or unavailable database can make the site appear down even if IIS is healthy. Official hosting documentation covers SQL Server installation, SQL user creation, Azure SQL differences, firewall access, and snapshot isolation during install [Install SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server), [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server), and [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock).

Agent inspection should confirm:

- Database platform: SQL Server on VM, Azure SQL Database, SQL Server local, or provider-managed.
- SQL tier, DTUs/vCores, storage size, max storage, backup retention, and geo-redundancy settings.
- Connection string timeout and encryption settings.
- SQL login used by Rock and whether least privilege is understood.
- Database maintenance job status.
- Index/statistics health and whether manual Azure SQL maintenance procedures are in use.
- Largest tables and growth trends.
- Blocking, deadlocks, query duration, CPU, IO, and worker saturation during known peaks.

Community Azure SQL maintenance guidance is useful but should be treated as community-contributed, not core-reviewed. It notes that Rock’s Database Maintenance job handles much of the regular need, while some environments may still need planned statistics/index maintenance and should avoid blindly accepting Azure advisor index suggestions because Rock manages its own expected indexes [How to Maintain your Azure SQL Database](https://community.rockrms.com/recipes/259).

### Layer 4: Shared Services

Rock depends on services that are not always obvious from the web server: file storage providers, SMTP transports, SMS providers, background checks, payment gateways, APIs, authentication providers, search indexers, cache, message bus, observability, and external integrations.

Agent inspection should confirm:

- File Types and storage providers.
- SMTP transport and verified outbound mail behavior.
- SMS transport and compliance posture.
- Payment gateway and webhook endpoints.
- Authentication services such as Active Directory or Entra-related patterns.
- Universal Search indexing status.
- Persisted DataViews and persisted datasets.
- Workflow volume and job queues.
- Message bus and real-time configuration if clustered.
- Observability provider and alerting paths.

Rock v19.1 added an automatic migration from a legacy Azure Blob Storage provider plugin to the core Azure Blob Storage provider because the legacy provider could no longer upload large files after library updates. That release note makes storage provider inventory especially important before and after v19 upgrades [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Layer 5: Operations And Governance

Operations are the human and automation routines that keep the environment useful: backup drills, certificate renewal, patch windows, change control, monitoring, incident response, access review, environment refresh, and documentation.

Agent inspection should confirm:

- Who can access Azure, Windows, SQL, DNS, registrar, SSL provider, SMTP, payment gateway, and Rock admin.
- Whether infrastructure maps exist and are current.
- Whether production, staging, development, and test are separated.
- Whether production data copied to development is scrubbed, reconfigured, or restricted.
- Whether backup restores have been tested.
- Whether update windows and rollback plans exist.
- Whether alert recipients are current.
- Whether public launch hardening has happened.

The official SaaS guide frames one side of this responsibility split: a hosted provider may own infrastructure care, but the church still owns its use of Rock and the decisions made inside it [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting). For self-hosted environments, those operational responsibilities stay with the church or partner.

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. Current official Rock documentation and release notes.
2. Rock source code, Model Map, and generated API/model artifacts.
3. RockU training where it explains operational concepts.
4. Trusted partner resources for applied operational patterns.
5. Community recipes and Q&A as examples, not as definitive guidance.

Official hosting documentation is the backbone for hosting types, installation, Azure provisioning, scaling, IIS, SQL Server, and web farm behavior [Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting). Release notes are authoritative for version caveats such as storage provider migrations, performance fixes, security hardening, and database index changes [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Source code is useful for locating implementation landmarks but should not be treated as a substitute for a tested live configuration; the public repository is available at [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock).

Community recipes are valuable because they show real operational workflows: refreshing a development environment, maintaining Azure SQL, configuring AWS SES, scaling Azure DTUs, and installing on AWS. However, Rock Community recipe pages include a disclaimer that recipes are community-contributed and not reviewed or endorsed by the core team, so agents should mark them as examples and verify against the current Rock version and environment before applying them [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355), [How to Maintain your Azure SQL Database](https://community.rockrms.com/recipes/259), [Automatically scale Azure DTUs on a schedule](https://community.rockrms.com/recipes/296).

When documentation conflicts with a live instance, the live instance wins for operational diagnosis, but the documentation remains the guide for intended behavior. For example, if documentation says a web farm uses message bus coordination, but a live instance has web farm enabled and message bus missing or unhealthy, the agent should report the mismatch and inspect the current web farm settings rather than assuming the cluster is safe.

## 5. Core Configuration And Data Model

Hosting configuration spans file-based settings, database records, service registrations, and cloud/server configuration. There is no single “Hosting” entity that fully describes the environment.

### File-Based Configuration

The most important file-based hosting configuration is the database connection string. Community and official installation flows refer to `web.ConnectionStrings.config` or connection string entry during install [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock), [Refreshing a Rock Development Environment from Production](https://community.rockrms.com/recipes/352). In self-hosted environments, this file determines which SQL database the Rock web application uses.

Agent checks:

- Confirm the file exists in the deployed Rock web root.
- Confirm `RockContext` points to the intended database and server.
- Confirm production and development connection strings are not swapped.
- Confirm a restored development copy does not still point to production.
- Confirm timeout values are intentional. A Q&A example discusses increasing `ConnectionTimeout` for SQL timeout cases, but this should be treated as a diagnostic or mitigation, not a root-cause fix [SQL Timeout](https://community.rockrms.com/ask/using/2832).

Do not expose full connection strings, usernames, passwords, or server names in public documentation.

### IIS And Windows Configuration

Official internal hosting instructions cover Windows roles/features, IIS setup, application pool settings, response compression, and disabling unnecessary Windows OS services [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features), [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis).

Key fields and settings to inspect:

- IIS site name and physical path.
- Bindings for hostnames and ports.
- SSL certificate binding.
- Application pool name.
- Application pool .NET version.
- Application pool start mode.
- Application pool idle timeout.
- Application pool identity.
- Recycling schedule.
- Preload behavior.
- Static and dynamic compression.
- Logs directory and retention.
- HTTP redirect rules.

The official IIS guidance says Rock’s Keep Alive process must be enabled when needed, but also notes it is not needed if the app pool idle timeout is set to 0, which is highly recommended in that guide [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis). In a live instance, inspect both the IIS app pool and any Rock keep-alive configuration before concluding which mechanism is active.

### SQL Configuration

Official SQL configuration differentiates Azure SQL Database from SQL Server on Azure VMs or local installs. Azure SQL Database account creation uses SQL commands in SSMS, while SQL Server on Azure VMs and local hosting can use SQL Server UI flows [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server).

Key fields and settings to inspect:

- SQL Server edition or Azure SQL tier.
- Database compatibility level.
- Snapshot isolation settings.
- Login/user used by Rock.
- Database role memberships.
- Firewall rules.
- Backup retention.
- Index and statistics maintenance.
- `tempdb` health for SQL Server VMs.
- Max degree of parallelism and cost threshold, if SQL Server VM/local.
- Azure SQL DTU/vCore utilization and wait stats.

Rock release notes show database performance is an active area of change. Rock v17.0 added and revised indexes across several high-impact tables, including financial transactions, person records, group hierarchies, and interactions [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Rock v17.2 changed index fill factor from 80% to 100% to reduce database footprint and improve maintenance task performance [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Agents should account for Rock version before recommending custom index changes.

### Rock Database Records That Affect Hosting

Common records to inspect in Rock:

- Service Jobs and job schedules.
- File Types and File Storage Providers.
- Communication Transports.
- SMS Transports.
- Site records and domains.
- Cache settings and global attributes.
- Security settings and authentication services.
- Universal Search settings.
- Persisted DataView and persisted dataset settings.
- Web farm configuration, if enabled.
- Observability settings.
- Lava endpoints and endpoint security, if used.
- API keys, REST keys, and external application registrations.

Do not assume exact table names from memory when doing live data work. Use Rock Model Map, EntityType records, or schema inspection in the live database. The source pack does not include a hosting-specific Model Map excerpt, so agents should verify entity names, table names, and columns in the target instance before writing operational SQL.

### Azure Resource Configuration

For Azure-hosted Rock, inspect:

- Resource group.
- App/runtime resource: VM, App Service, or other host.
- SQL database and server.
- Storage accounts and containers.
- Application Gateway or load balancer.
- Virtual network and subnets.
- Network security groups.
- Public IPs.
- DNS zones or external DNS.
- Key Vault if used.
- Backup vaults or database retention.
- Monitor alerts.
- Log Analytics or observability integrations.
- Managed identities and role assignments.

Rock’s Azure next steps begin by creating a resource group as the logical container for related Rock services [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting). Agents should use the resource group as the initial inventory boundary but still check for resources outside the group, especially DNS, Key Vault, storage, or third-party services.

## 6. Primary Entities And Relationships

Hosting work crosses Rock entities and external infrastructure. The most important relationships are operational rather than purely relational.

### Site, Domain, And Request Handling

A Rock Site represents a web surface, such as internal staff site, external public site, or specialized site. The infrastructure side must route hostnames to IIS/app services, and Rock must know how to resolve requests to the correct site. Inspect:

- Site list and configured domains.
- Page routes and site themes.
- Public vs internal site exposure.
- Login pages and authentication flows.
- API and webhook endpoints.
- Request filters if used.

The Rock source snippets include CMS request filter view models such as `EnvironmentRequestFilterBag`, which indicates request filters can include environment-style conditions such as days of week and times of day in the Obsidian block surface [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock). Verify exact fields in the live Rock version before relying on that implementation detail.

### File Type And Storage Provider

Binary files are stored through File Types and File Storage Providers. Operationally, this affects:

- Person photos.
- Content channel images.
- Documents.
- Communication attachments.
- Mobile assets.
- Public file URLs.
- Large file upload behavior.
- CDN/cache headers if configured.

Rock v19.1’s Azure Blob provider migration is a key caveat: legacy Azure Blob Storage provider settings can be moved to the core Azure Blob Storage provider, with related File Types updated, while the legacy provider remains active so existing files continue to work [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Before v19 upgrades, inventory every File Type and provider. After upgrade, verify uploads, downloads, public access, private file security, cache-control behavior, and large file upload paths.

Rock v17.5 fixed an error when editing Content Channel Types with Image, File, or Binary File attributes if storage used Azure Blob Storage, File System, or newly created FileType; the fix set default cache-control header settings for newly created Binary File Types and migrated missing values [Rock Core Release Notes](https://www.rockrms.com/releasenotes). If CMS file attributes fail, inspect File Type cache settings and version.

### Communication Transport And SMTP

Rock communications rely on transport configuration and network egress. A community recipe demonstrates configuring AWS SES as an SMTP transport, including outbound TCP 587 and mapping SES credentials into Rock’s SMTP transport fields [AWS SES Email SMTP Transport for RockRMS](https://community.rockrms.com/recipes/171). Treat the recipe as an example; in production, verify:

- Active email transport.
- SMTP host, port, TLS/SSL, username, and sender domain.
- DNS records: SPF, DKIM, DMARC, MX where relevant.
- Bounce handling.
- Rate limits.
- Outbound firewall allowance.
- Test send success.
- Whether development has mail disabled or redirected to a trap provider.

### Jobs And Background Processing

Service Jobs are part of hosting because they consume CPU, SQL, external APIs, and file storage. Rock jobs can also create the highest load during low-traffic hours. Community Azure DTU scaling guidance describes a scenario where DTUs hit 100% during large overnight jobs and during weekend check-in, motivating scheduled scaling [Automatically scale Azure DTUs on a schedule](https://community.rockrms.com/recipes/296).

Agent checks:

- Job Pulse health.
- Rock Cleanup status.
- Database Maintenance status.
- Process Workflows duration and backlog.
- Universal Search Re-Index frequency.
- Update Persisted DataViews duration.
- Calculate Metrics duration.
- Communication send jobs.
- Custom plugin jobs.
- Jobs disabled in development.
- Job overlap with backups, imports, or check-in.

RockU workflow training includes a Workflow Performance Tips item, and workflow-related training emphasizes that workflows can run request systems, data changes, background tables, and automation [Workflows](https://community.rockrms.com/rocku/workflows), [Workflow Performance Tips](https://community.rockrms.com/rocku/workflows/workflow-performance-tips). Use this as a reminder that workflow design can become infrastructure load.

### Web Farm Nodes And Message Bus

A Rock web farm introduces multi-node coordination. Official web farm configuration includes message bus setup, web farm activation, node restart, node startup/shutdown, leader responsibilities, leader election, node names, node metrics, and current limitations [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm).

Agent checks:

- Whether web farm is licensed and enabled.
- Message bus provider and connectivity.
- All nodes started after web farm activation.
- Node names and metrics.
- Which node is leader.
- Whether jobs run only where expected.
- Cache invalidation behavior across nodes.
- Real-time features and SignalR/Azure SignalR health.
- Deployment synchronization across nodes.

A partner GitHub spotlight notes a v18 issue that prevented Rock from starting in web farm environments using Azure SignalR, highlighting that clustered runtime and real-time services can be version-sensitive [GitHub Spotlight: 1/15/2026](https://www.triumph.tech/resources/github-spotlight-1152026). Verify exact release notes and installed version before diagnosing a SignalR/web farm startup issue.

### Authentication Services

Authentication crosses security and infrastructure. Community recipes describe using Azure AD Domain Services or Microsoft Entra-related infrastructure so Rock can authenticate against Active Directory-style services [Using Office 365 / Azure Active Directory (Microsoft Entra ID) Accounts for Rock Authentication](https://community.rockrms.com/recipes/92), [Syncing Local Active Directory with Azure AD (Microsoft Entra ID) for Rock Authentication](https://community.rockrms.com/recipes/91). Treat these as historical/community examples; verify current Rock authentication provider capabilities, Microsoft naming, network paths, LDAPS requirements, and firewall rules in the live instance.

Agent checks:

- Active authentication providers.
- Admin accounts with local fallback.
- External identity dependency during internet outage.
- MFA policy.
- Passwordless login behavior if enabled.
- Security role assignment.
- Elevated security processing jobs.

The source snippets include `ProcessElevatedSecurity` in Rock jobs and passwordless login view model/enum files in the Rock repository [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock). Use these as source-code landmarks, then verify actual block settings and jobs in the live version.

## 7. Common Hosting And Infrastructure Workflows

### New Hosting Selection

Start with responsibility and complexity.

Use SaaS when the organization needs Rock running quickly, has limited technical staff, prefers predictable cost, and wants a provider to manage installation, updates, backups, monitoring, and security care. The official SaaS intro frames SaaS as fully managed Rock where the team uses Rock and the provider manages infrastructure [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting).

Use Azure self-hosting when the organization has technical capacity or a partner, wants control over infrastructure, can manage Azure operations, and may benefit from nonprofit credits. The official Azure intro discusses Microsoft’s nonprofit Azure credit and warns that cost is not the only factor because hosting quality varies widely for Rock workloads [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting).

Use internal hosting when the organization requires on-premises control, has Windows/IIS/SQL competence, and can maintain server hardware/virtualization, backups, network security, certificates, and patching. The official internal guide provides server roles, IIS, SQL Server, and Rock install steps [Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting).

Use scaled/web farm hosting when a single web node is no longer enough or high availability is required. This adds cost and complexity. Rock’s scaling guide explains scale-up versus scale-out and introduces cluster components [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster).

### Provision Azure Hosting

A practical Azure workflow:

1. Confirm nonprofit credit eligibility and budget model if applicable. The official nonprofit credit article describes the credit as an annual Azure credit with a monthly spending pattern and prerequisites [Register for Credits as a Non-Profit](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit).
2. Create a resource group for Rock-related services [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting).
3. Decide runtime model: VM/IIS, App Service, or provider-managed architecture. Official docs focus on Azure services broadly; community material includes an Azure App Service walkthrough but it is a recipe and must be validated [Deploying Rock RMS as an Azure App Service](https://community.rockrms.com/recipes/202).
4. Provision SQL database or SQL Server VM.
5. Provision storage for backups and files if needed.
6. Configure network, firewall, and private/public endpoints.
7. Install Rock and connect it to the database.
8. Configure DNS and SSL.
9. Configure mail, SMS, payment gateway, and storage providers.
10. Configure jobs and maintenance windows.
11. Set monitoring and alerts.
12. Prove backup and restore.
13. Document the architecture.

### Install Internally

The official internal hosting flow is:

1. Confirm system requirements and installation prerequisites [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting).
2. Install Windows Server roles and IIS features [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features).
3. Configure IIS [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis).
4. Install SQL Server if hosting database locally or on a VM [Install SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server).
5. Configure SQL Server, users, and firewall [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server).
6. Install Rock by placing installer files in the web root and launching the install [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock).
7. For larger or more secure installs, split web and database onto two servers [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment).

The two-server recommendation is not only about capacity. The official article cites performance, security, and PCI-related reasons for separating database and web environment, including the possibility of placing a public web server in a DMZ [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment).

### Refresh Development From Production

A development refresh workflow must not simply copy production and walk away. Community recipes describe copying the production database, copying the web root/code, updating `web.ConnectionStrings.config`, running scripts or manual steps to make the copy safe for development, disabling or limiting jobs, changing visual cues, and redirecting email [Refreshing a Rock Development Environment from Production](https://community.rockrms.com/recipes/352), [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355).

Agent checklist:

- Confirm the refresh is authorized.
- Take production backup or snapshot according to policy.
- Copy database to development.
- Copy files/code if required.
- Update development connection string.
- Disable outbound email or point to a trap.
- Disable SMS and payment/webhook side effects.
- Disable production-only jobs.
- Change site domains and visual identifiers.
- Clear caches.
- Verify development cannot affect production.
- Document refresh date, source version, and post-refresh modifications.

A community Azure refresh recipe includes a list of jobs kept running in that environment, but job IDs and job sets are instance-specific [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355). Never assume another organization’s job IDs match the target instance.

## 8. Sizing And Service Options Deep Dive

Rock sizing should be workload-based, not attendance-only. Official Azure sizing guidance states that average attendance is a starting point but can be too simplistic because feature usage can make a medium-sized church heavier than a larger church using Rock lightly [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options).

### Workload Drivers

Assess these drivers:

- Public website hosted in Rock.
- Giving volume and payment processing.
- Check-in attendance and label printing.
- Mobile app traffic.
- API integrations.
- Workflow volume.
- Communication volume.
- Data imports and sync jobs.
- Content channel size.
- Interaction tracking volume.
- Universal Search indexing.
- Persisted DataViews and datasets.
- Reporting and analytics usage.
- Number of staff users and concurrent sessions.
- Plugin load.
- File volume and storage location.
- Weekend peak traffic.
- Event registration bursts.
- Nightly job window.

### Small Install Pattern

A small environment may use one server for web and database, but this is the least isolated pattern. Official internal hosting guidance includes small-install requirements in the internal hosting intro [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting). In practice, agents should treat single-server hosting as acceptable only when:

- The church has low traffic.
- Check-in and giving loads are modest.
- There is a clear backup plan.
- There is no public high-traffic CMS dependence.
- The team understands that web and database compete for resources.
- Monitoring confirms headroom.

### Medium Pattern

A medium environment should strongly consider separating web and database. The official two-server article recommends separate Rock database and web environment even for smaller installations because of performance, security, and compliance benefits [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment).

Typical medium concerns:

- Public website and internal admin traffic share runtime.
- Check-in peak can collide with background jobs.
- SQL maintenance window matters.
- File storage may need to move from local disk to blob/object storage.
- Development should not share production resources.
- Monitoring must be active, not occasional.

### Large Pattern

A large environment usually needs:

- Dedicated web server(s).
- Dedicated database service.
- Azure SQL tier or SQL VM sized for peak.
- Externalized file storage.
- Formal backup/restore testing.
- Separate development and staging.
- Observability and alerting.
- Performance review before major events.
- Review of check-in code length and performance constraints.
- Scheduled scaling or temporarily increased capacity for known peaks.

Community examples describe scheduled Azure SQL scaling for nightly jobs and Sunday check-in peaks [Automatically scale Azure DTUs on a schedule](https://community.rockrms.com/recipes/296). This pattern should be validated with current Azure capabilities, budget, and exact tier model.

### Extra-Large And Cluster Pattern

Use scale-out when:

- A single web node cannot handle traffic.
- High availability is required.
- Deployments need node rotation.
- Public web and staff/API workloads must remain available during failures.
- The team can manage message bus, node coordination, and load balancing.

Rock cluster architecture includes an application gateway/load balancing layer and multiple cluster components [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster). The web farm configuration requires Rock-specific activation and message bus setup, not just putting two IIS servers behind a load balancer [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm).

## 9. Azure Hosting Deep Dive

Azure is a strong Rock hosting option when the team can manage cloud operations or has a partner. The official Azure intro highlights Microsoft nonprofit credits but also emphasizes that cost is not the only factor; hosting quality matters for Rock [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting).

### Azure Resource Group

The resource group is the operational inventory boundary. The official Azure next steps begin with creating a resource group to hold Rock services [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting). Agents should inventory:

- Resource group name and region.
- All resources inside it.
- Any related resources outside it.
- Tags for environment, owner, cost center, and criticality.
- Access control assignments.
- Locks and delete protection.

### Azure Runtime Choices

Common choices:

- Windows Server VM with IIS.
- Azure App Service, as shown in a community recipe [Deploying Rock RMS as an Azure App Service](https://community.rockrms.com/recipes/202).
- Partner-managed SaaS or managed hosting.
- Multi-node web farm behind Application Gateway.

For VM-based hosting, official internal hosting guidance still applies: IIS, SQL Server if local/VM-based, firewall, app pool settings, and Rock install flow [Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting). For App Service, validate current Rock support expectations, file persistence, deployment workflow, application settings, connection strings, background behavior, and plugin compatibility in the live environment before assuming parity with IIS on a VM.

### Azure SQL Database

Azure SQL can reduce database administration burden but still requires capacity planning, backup policy review, maintenance awareness, and monitoring. Official SQL configuration notes Azure SQL Database has a different user creation path than SQL Server on Azure VMs or local servers [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server).

Agent checks:

- Service tier.
- DTU/vCore model.
- Max storage.
- Backup retention.
- Geo-redundancy.
- Firewall and private endpoint.
- Entra authentication if used.
- SQL login used by Rock.
- Elastic pool membership if any.
- Read-only replica availability.
- Query performance insight.
- Maintenance history.

If Azure advisor recommends indexes, do not apply blindly. Rock release notes show core-managed index changes, and community SQL maintenance guidance warns that Rock maintains expected indexes as needed [Rock Core Release Notes](https://www.rockrms.com/releasenotes), [How to Maintain your Azure SQL Database](https://community.rockrms.com/recipes/259). Escalate index changes through a Rock-aware DBA or partner.

### Azure Storage

Use Azure Storage for backups, blob file storage, deployment artifacts, logs, or static assets where appropriate. Rock v19.1’s Azure Blob Storage provider migration makes this area version-sensitive [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Agent checks:

- Storage account names and regions.
- Containers used by Rock.
- Public access policy.
- SAS tokens or connection strings.
- File Type mapping.
- Private endpoint/firewall rules.
- Lifecycle management.
- Backup/replication.
- Large upload behavior after v19.
- Cache-control headers after v17.5 and later.

### Azure Monitoring

Monitoring should include resource metrics, application errors, SSL status, backup health, and job health. A partner resource on proactive Azure monitoring describes tracking CPU, memory, backups, SSL status, and similar health signals, with alerts to responsible teams [Introducing Imperator: Proactive Azure Monitoring and Alerting for Rock RMS](https://www.triumph.tech/resources/introducing-imperator-proactive-azure-monitoring-and-alerting-for-rock-rms). The Azure Mobile App can provide quick health views and service alerts for Azure-hosted Rock, but it is a companion, not a full operational console [Azure Mobile App](https://www.triumph.tech/resources/azure-mobile-app).

Agent checks:

- Metric alerts for CPU, memory, disk, DTU/vCore, failed requests, response time, storage capacity.
- Availability tests.
- SSL expiration alerts.
- Backup failure alerts.
- Service Health alerts.
- App logs and exception logs.
- Notification recipients.
- On-call/escalation coverage.
- Alert noise and ignored alerts.

## 10. Operational Readiness Deep Dive

Operational readiness means the system can survive ordinary failure, maintenance, growth, and staff turnover.

### Backup Readiness

For Rock, backup readiness usually includes:

- Database backup.
- File system or blob storage backup.
- Rock web root/code backup.
- Plugin files.
- Theme files.
- `web.ConnectionStrings.config`.
- Encryption keys and secrets, stored securely.
- DNS and SSL recovery info.
- Payment/webhook configuration.
- Mail/SMS credentials.
- Infrastructure-as-code or screenshots/exported inventory if no IaC exists.

Community AWS hosting guidance emphasizes taking a clean database snapshot and backing up/zipping the `inetpub` folder after install because both are critical for restore/migration [Turn-key RockRMS Hosting with AWS](https://community.rockrms.com/recipes/190). That principle applies broadly: database-only backups are not enough if file storage, plugins, or web root changes are not recoverable.

### Restore Readiness

A backup is not proven until restored. Agents should ask:

- When was the last test restore?
- Where was it restored?
- How long did it take?
- Did files and database match?
- Did login work?
- Were integrations disabled during test?
- Was DNS cutover tested or simulated?
- Was the restore procedure documented?

For Azure SQL, point-in-time restore or copy may be available depending on tier and configuration. A community Azure development refresh recipe compares Azure SQL restore and copy approaches for development refreshes [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355). Treat the exact performance claims as environment-specific.

### SSL Readiness

Inspect:

- Certificate expiration.
- Auto-renew method.
- ACME client or managed certificate provider.
- IIS/App Service binding.
- Intermediate chain.
- Redirect behavior.
- External dependencies that need certificate renewal notifications.

A community recipe demonstrates notifying third parties when ACME SSL certificates renew, especially for services like background screening integrations that may need updated certificates [Get Notified of ACME SSL Certificate Renewal](https://community.rockrms.com/recipes/263). Verify whether current integrations actually require notification before implementing a similar workflow.

### SMTP Readiness

Inspect:

- Transport provider.
- Authentication method.
- Sender verification.
- SPF/DKIM/DMARC.
- Bounce handling.
- Rate limits.
- Test sending.
- Development environment protections.

Community SMTP guidance using AWS SES is an example of configuring outbound port 587 and using provider credentials in Rock’s SMTP transport [AWS SES Email SMTP Transport for RockRMS](https://community.rockrms.com/recipes/171). For Mailgun, SendGrid, Microsoft, or another provider, verify provider-specific fields and current Rock transport support.

### Security Readiness

Inspect:

- Windows updates.
- SQL patching.
- Public firewall exposure.
- RDP restrictions.
- SQL port exposure.
- Admin account inventory.
- Rock admin roles.
- API keys and REST keys.
- Authentication providers.
- SSL/TLS posture.
- File Type public security.
- Document Type security.
- Workflow Type security.

Rock v19.1 includes security-related release notes such as Workflow Type view permission hardening and Document Type view permission behavior [Rock Core Release Notes](https://www.rockrms.com/releasenotes). These affect operational review because file/document access may change after upgrade.

A partner article on PrintNightmare recommends disabling the Windows Print Spooler service on Rock Windows servers when not needed and notes standard Rock check-in server-based printing does not use the Windows print spooler [What To Do About the Microsoft Windows PrintNightmare Vulnerability](https://www.triumph.tech/resources/microsoft-windows-printnightmare-vulnerability). Treat this as vulnerability-specific guidance and verify current Microsoft recommendations before applying.

## 11. Related Rock Areas: Operations, Security, Jobs, Cache, Search, Cms, Api Integrations

### Operations

Hosting is part of operations because the health of Rock depends on routines: patching, monitoring, backups, capacity planning, job review, certificate renewal, release testing, and incident response. Infrastructure maps are especially valuable because they capture the last-known-good architecture and help external helpers understand the environment quickly [The Importance of Infrastructure Maps](https://www.triumph.tech/resources/the-importance-of-infrastructure-maps).

### Security

Security crosses Rock permissions, Windows/IIS, SQL, Azure, DNS, SSL, secrets, and third-party providers. Rock release notes show security posture changes across versions, including workflow type view restrictions and document security changes [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Agents should verify both configured Rock security and infrastructure access control.

### Jobs

Jobs affect performance and correctness. A failed cleanup job, stuck workflow job, or long-running persisted DataView job can degrade the instance. Community refresh recipes also show development environments often disable most jobs to avoid production-like side effects [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355). Always inspect actual job IDs and names in the target instance.

### Cache

Cache affects deployment, development refreshes, web farms, and perceived correctness. Community refresh guidance clears cache before copying files to reduce copied data [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355). In web farms, cache invalidation depends on proper cluster coordination and message bus health [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm).

### Search

Universal Search indexing and search-heavy pages can create both scheduled and interactive load. Rock release notes include performance fixes for person/history/search-related areas across versions, and source snippets show performance benchmark projects in the repository [Rock Core Release Notes](https://www.rockrms.com/releasenotes), [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock). In live work, inspect Universal Search jobs, index health, and custom search pages.

### CMS

If Rock hosts the public website, CMS traffic becomes infrastructure traffic. Content channel images, binary file storage, request filters, Lava endpoints, page routes, and public cache settings matter. Rock v17.5’s binary file type cache-control fix is especially relevant to CMS file attributes [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### API Integrations

APIs affect hosting because they create inbound web traffic, outbound dependencies, webhook retries, authentication risk, and background processing. Inspect REST keys, external app registrations, Lava endpoints, webhook endpoints, payment gateway callbacks, and integration jobs. The source snippets include a `LavaEndpointSecurityMode` enum with endpoint/application security modes in Rock source, but exact configuration must be verified in the live version [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock).

## 12. Administration And Operational Guardrails

### Public-Safe Documentation

Do not put secrets, private hostnames, SQL connection strings, raw logs, or security diagrams into public repositories. For public knowledge-base work, convert environment-specific evidence into generalized guidance and keep private operational evidence in private storage.

### Change Control

Before hosting changes:

- Record current state.
- Capture rollback path.
- Confirm maintenance window.
- Confirm affected ministry surfaces.
- Confirm backup freshness.
- Confirm monitoring during and after change.
- Confirm who can approve production impact.

Hosting changes include SQL tier changes, app pool changes, certificate changes, DNS changes, storage provider changes, job schedule changes, web farm activation, mail transport changes, and authentication provider changes.

### Production And Development Separation

Production and development should be separated by more than a URL. Partner guidance argues against placing development and production on the same VM because of shared resources and configuration complexity [Separating Development and Production](https://www.triumph.tech/resources/separating-development-and-production). Some community recipes describe shared-server patterns to save cost [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355), but agents should treat those as risk-accepted local choices, not best practice.

Minimum separation checks:

- Separate database.
- Separate connection string.
- Separate app pool.
- Separate hostnames.
- Separate mail/SMS/payment behavior.
- Separate storage containers where possible.
- Visual environment indicator.
- Disabled or redirected integrations.
- No production webhook target in development.
- No public indexing of development.

### Secrets And Credentials

Secrets include:

- SQL passwords.
- SMTP credentials.
- Storage keys.
- Payment gateway keys.
- SMS provider credentials.
- API keys.
- Azure service principal secrets.
- Certificate private keys.
- Machine keys if relevant.
- OAuth client secrets.

Agents should never paste secrets into public docs. In live review, identify where secrets are stored and whether rotation is possible, but redact values.

### Upgrade Guardrails

Before upgrading:

- Read release notes for current-to-target versions.
- Capture database and file backup.
- Inventory plugins.
- Inventory storage providers.
- Check web farm compatibility.
- Check file type security and document type behavior.
- Test in development using production-like data.
- Confirm rollback path.
- Monitor jobs and migrations after restart.

Hosting-related release caveats include v19.1 Azure Blob provider migration, v17.5 file type cache-control fix, v17.0 database index improvements, v17.2 fill factor change, and several performance fixes in check-in and attendance blocks [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

## 13. Developer, API, Lava, And Source-Code Landmarks

The Rock source repository is a key landmark for implementation details, but agents should use it carefully. The repository is available at [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock). Source-code snippets in the pack point to several relevant areas:

- `Rock/Jobs/ProcessElevatedSecurity.cs`: job implementation pattern for security-related background processing.
- `Rock.Enums/Cms/LavaEndpointSecurityMode.cs` and TypeScript equivalent: Lava endpoint security modes.
- `Rock.ViewModels/Blocks/Cms/RequestFilterDetail/EnvironmentRequestFilterBag.cs`: CMS request filter view model.
- `Rock.Tests.Performance` and `Rock.Tests.Integration.Performance`: performance benchmark infrastructure.
- Passwordless login view models and enums under security/login folders.

Use source code to answer “where is this implemented?” and “what version likely contains this surface?” Use live Rock configuration to answer “is this enabled here?” and “what will happen if we change it?”

### Lava Endpoints

Lava endpoints can become infrastructure surfaces because they expose routes, run Lava, depend on security mode, and may be used by external systems. Inspect:

- Endpoint routes.
- Security mode.
- Lava command availability.
- Caching.
- API consumers.
- Error handling.
- Rate and traffic volume.

The source snippet for `LavaEndpointSecurityMode` shows modes such as endpoint execute and application-level permissions in source-code metadata [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock). Verify exact UI labels and behavior in the live Rock version.

### API And REST Keys

API integrations should be reviewed as hosting dependencies:

- Which API keys exist?
- Which users own them?
- Which endpoints are called?
- Are calls internal, public, or partner-facing?
- Is traffic routed through the same load balancer?
- Are webhook retries creating traffic spikes?
- Are API users over-permissioned?

### Source-Code Version Caveat

The public repository develop branch may be ahead of the installed Rock version. Do not cite a develop-branch file as proof that a production instance has that behavior. Use it as a landmark, then verify against the installed version, release notes, and live files.

## 14. Reporting, Analytics, And Model Map

Hosting reports should answer capacity, health, and risk questions.

### Useful Operational Reports

Create or inspect reports for:

- Service Job last success, last duration, and failures.
- Exceptions by count and recency.
- Communication sends and failures.
- Workflow counts by status and age.
- Persisted DataView refresh duration.
- Universal Search index status.
- Attendance/check-in volume by peak hour.
- API request volume if logged.
- Interaction growth.
- Binary file growth.
- Database table growth.
- Storage provider usage.
- Login failures and authentication provider errors.

### Model Map Usage

Use the Model Map or live schema inspection for exact entity/table/field names. Hosting work often touches entities whose names vary by version or plugin. The source pack does not include a detailed hosting Model Map record, so avoid pretending exact schema certainty. For live work, inspect:

- EntityType records for target entity.
- Table columns through database metadata.
- Rock block/entity definitions in the installed version.
- Model Map pages if available for that version.
- Source code matching the installed tag, not only develop.

### Analytics And Digital Load

Website analytics and interaction tracking influence hosting because public traffic, mobile usage, and search-driven behavior can shift load patterns. Partner resources discuss changing website and mobile engagement patterns, which should prompt agents to validate actual traffic rather than sizing from old assumptions [The Digital Ministry Blind Spot That AI Just Exposed](https://www.triumph.tech/resources/digital-ministry-blind-spot).

## 15. Version And Release Caveats

### v19.1

Rock v19.1 includes an automatic migration from a legacy Azure Blob Storage provider plugin to the core Azure Blob Storage provider. This is required because the legacy provider cannot upload large files after library updates in v19. File Type associations are updated, settings are carried over, and the legacy provider remains active for existing files [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Operational action:

- Before upgrade, inventory File Storage Providers and File Types.
- After upgrade, test existing file reads and new large file uploads.
- Confirm public/private file access.
- Confirm storage provider settings.
- Confirm plugin cleanup plan with reviewer approval.

v19.1 also includes security hardening for workflow type view permissions and document type view permissions [Rock Core Release Notes](https://www.rockrms.com/releasenotes). After upgrade, inspect staff workflows, document access, and public file/document exposure.

### v18.3 And v19 Pre-Alpha Notes

Partner GitHub spotlight material notes v18.3 improvements such as improved performance of the Update Persisted Attribute Values job for certain field types and fixes for simultaneous connection requests causing performance issues/timeouts [GitHub Spotlight: 3/19/2026](https://www.triumph.tech/resources/github-spotlight-3192026). Treat spotlight posts as helpful summaries and confirm against official release notes and installed version.

### v18.1

Rock v18.1 added a separate global attribute for server-side Google API requests such as geocoding and routing, distinct from client-side JavaScript API calls [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Hosting implication: server-side outbound network, secret storage, and API quota are separate concerns from browser-side keys.

### v17.5

Rock v17.5 fixed a severe performance issue where the Obsidian Attendance History block could attempt to load all attendance records when person context was missing [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Hosting implication: page/block context bugs can become server incidents.

v17.5 also fixed file attribute editing issues involving Azure Blob Storage or File System-backed file types and added/migrated cache-control header settings [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### v17.2

Rock v17.2 changed database index fill factor from 80% to 100% to reduce table size and improve maintenance performance [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Hosting implication: review custom DBA maintenance assumptions after upgrade.

### v17.1

Rock v17.1 fixed Next-Gen Check-in Bluetooth printing performance related to label image data encoding [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Hosting implication: check-in performance can be affected by client and encoding behavior, not only server capacity.

### v17.0

Rock v17.0 added and revised indexes across several tables to improve query efficiency for transactions, person records, groups, and interactions [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Hosting implication: performance baselines may shift after upgrade, and custom indexes should be reviewed carefully.

### v16.3

Rock v16.3 fixed an issue where Communication Entry Wizard became unusable when SMS image attachments were auto-resized and uploaded to Azure Blob Storage [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Hosting implication: communication media storage can affect staff UI reliability.

## 16. Implementation Playbooks

### Playbook: Choose Hosting Model

1. List ministry-critical surfaces: staff, public web, giving, check-in, mobile, workflows, integrations.
2. Estimate workload: attendance, check-in volume, giving volume, public traffic, communication volume, workflows, jobs.
3. Determine team capacity: Azure/Windows/SQL skill, monitoring skill, backup skill, availability expectations.
4. Choose responsibility model:
   - SaaS for managed infrastructure.
   - Azure self-hosted for cloud control.
   - Internal hosting for local control.
   - Web farm for scale/high availability.
5. Price all components, not just compute.
6. Define backup and restore targets.
7. Define monitoring and escalation.
8. Document the architecture.

Cite official starting points: [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting), [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting), [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting).

### Playbook: Production Readiness Review

Inspect:

- Rock version and pending updates.
- Hosting model.
- Infrastructure map.
- DNS and SSL.
- Runtime health.
- SQL health.
- Backup policy and restore proof.
- File storage providers.
- SMTP/SMS/payment integrations.
- Jobs and schedules.
- Web farm/message bus if present.
- Observability and alerting.
- Admin access and secrets.
- Development separation.
- Release notes for target version.

Deliver:

- Risk list.
- Evidence list.
- Required fixes.
- Recommended fixes.
- Unknowns requiring live verification.

### Playbook: Azure Cost And Capacity Review

Inspect:

- Resource group inventory.
- VM/App Service sizes.
- Azure SQL tier and utilization.
- Storage capacity and transactions.
- Backup retention costs.
- Bandwidth.
- Monitoring/log retention.
- Idle dev/test resources.
- Scheduled scale patterns.
- Nonprofit credit status if applicable.

Use official sizing guidance as starting input and actual telemetry as the final decision basis [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options).

### Playbook: Web Farm Readiness

Before enabling:

- Confirm license key.
- Confirm load balancer/application gateway.
- Confirm shared database.
- Confirm shared file strategy.
- Confirm message bus.
- Confirm cache invalidation strategy.
- Confirm deployment sync.
- Confirm node names.
- Confirm health checks.
- Confirm jobs/leader responsibilities.
- Confirm all nodes restart cleanly.
- Confirm real-time/SignalR behavior.
- Confirm rollback to single-node.

Use [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm) as the primary Rock-specific reference.

### Playbook: Storage Provider Upgrade Review

Before upgrade to v19+:

- List File Storage Providers.
- Identify legacy Azure Blob provider use.
- List File Types using each provider.
- Test uploads in staging.
- Backup database and file storage.
- Read v19.1 release note.
- Upgrade staging first.
- Test existing file reads.
- Test new large uploads.
- Test Content Channel file/image attributes.
- Test private file security.

Cite [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

## 17. Troubleshooting Decision Tree

### Site Is Down

1. Confirm DNS resolves.
2. Confirm SSL certificate is valid.
3. Confirm load balancer/app gateway health.
4. Confirm IIS/App Service is running.
5. Confirm app pool is started.
6. Confirm database is reachable.
7. Confirm connection string points to expected database.
8. Confirm SQL login works.
9. Check Rock exception logs and Windows/app logs.
10. Check recent deployments, updates, certificate renewals, DNS changes, and SQL scaling.

If SQL timeout appears, do not stop at increasing connection timeout. A Q&A example mentions `ConnectionTimeout=360`, but root cause may be SQL unavailability, blocking, resource exhaustion, firewall, DNS, or connection string error [SQL Timeout](https://community.rockrms.com/ask/using/2832).

### Site Is Slow

1. Identify whether slowness is global or page-specific.
2. Check CPU, memory, disk, SQL DTU/vCore, and SQL waits.
3. Check current running jobs.
4. Check long-running SQL queries.
5. Check recent content/page/block changes.
6. Check cache clears or app restarts.
7. Check file storage latency.
8. Check external integrations.
9. Check check-in, giving, communication, or registration traffic peaks.
10. Compare with release notes for known performance fixes.

### Check-In Is Slow

1. Confirm whether issue is server, network, kiosk, printer, or database.
2. Check weekend peak SQL utilization.
3. Check attendance code volume and code length for very large ministries.
4. Check label printing path and printer type.
5. Check recent Rock version.
6. Check jobs running during check-in.
7. Check wireless/network health.
8. Check Next-Gen Check-in release caveats.

Partner guidance notes that very large ministries using 3-digit check-in security codes can approach a practical code-space limit in a day, causing performance issues near saturation [Heads Up: Check-in for Very Large Ministries](https://www.triumph.tech/resources/check-in-for-very-large-ministries). Verify the query and current Rock behavior before acting.

### File Uploads Fail

1. Identify File Type.
2. Identify File Storage Provider.
3. Test small and large upload.
4. Check storage account/container permissions.
5. Check v19.1 Azure Blob migration status.
6. Check cache-control fields if CMS file attributes are involved.
7. Check plugin provider status.
8. Check exceptions and browser/network errors.

Use v19.1 and v17.5 release notes as version landmarks [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Development Environment Sends Real Messages

1. Disable or redirect SMTP transport.
2. Disable SMS transport.
3. Disable communication jobs.
4. Confirm payment gateways are test/sandbox or disabled.
5. Confirm webhook URLs are development-only.
6. Confirm Rock Shop/plugin notifications are safe.
7. Confirm visual environment banner.
8. Review refresh script.

Community development refresh recipes explicitly include steps for limiting development behavior after copying production [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355), [Refreshing a Rock Development Environment from Production](https://community.rockrms.com/recipes/352).

### Web Farm Node Behaves Differently

1. Confirm same Rock code on every node.
2. Confirm same connection strings.
3. Confirm file storage consistency.
4. Confirm message bus connectivity.
5. Confirm node registered and metrics update.
6. Confirm leader election.
7. Confirm cache invalidation.
8. Confirm load balancer routing and health checks.
9. Confirm Azure SignalR/real-time compatibility if used.
10. Review web farm limitations.

Use [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm).

## 18. Agent Task Recipes

### Recipe: Inventory Hosting

Return:

- Hosting model.
- Rock version.
- Runtime host(s).
- Database host/service.
- File storage providers.
- SMTP/SMS/payment providers.
- DNS and SSL.
- Jobs health.
- Backup policy.
- Monitoring.
- Known risks.
- Unknowns requiring live verification.

### Recipe: Validate Azure Hosting

Return:

- Resource group and region.
- Compute resources.
- SQL tier and utilization.
- Storage resources.
- Network path.
- Public endpoints.
- Backups.
- Alerts.
- Cost drivers.
- Nonprofit credit status if relevant.
- Gaps against official Azure setup guidance [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting).

### Recipe: Review SQL Performance

Return:

- SQL platform and tier.
- Current utilization.
- Top waits or slow queries if available.
- Job overlap.
- Database Maintenance job status.
- Rock version index caveats.
- Any custom indexes.
- Azure advisor recommendations and whether ignored/applied.
- Next safe actions.

Cite release notes before recommending index changes [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Recipe: Review Backup And Restore

Return:

- Database backup method.
- File backup method.
- Web root/config backup method.
- Retention.
- Restore test date.
- Restore duration.
- Missing secrets or dependencies.
- Disaster recovery steps.
- Person/team responsible.

### Recipe: Review Web Farm

Return:

- Web farm enabled.
- License status.
- Nodes and names.
- Leader node.
- Message bus provider.
- Load balancer.
- Health checks.
- Shared storage.
- Job behavior.
- Cache behavior.
- Version caveats.

Use [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster) and [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm).

### Recipe: Public Launch Hosting Gate

Return pass/fail for:

- DNS.
- SSL.
- Redirects.
- Public site routes.
- Login and security.
- Giving/payment gateway.
- Email/SMS.
- File access.
- Backup/restore.
- Monitoring.
- Load test or peak readiness.
- Rollback plan.
- Admin access.
- Incident contacts.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

Primary official sources:

- [Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting): top-level official hosting index.
- [Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting): official Azure hosting section.
- [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting): Azure rationale, cost/quality framing, nonprofit credit pointer.
- [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options): official sizing and workload caution.
- [Register for Credits as a Non-Profit](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit): nonprofit credit workflow.
- [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting): Azure provisioning starting point.
- [Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting): official internal hosting section.
- [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting): system requirements and prerequisites.
- [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features): Windows role setup.
- [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis): IIS/app pool guidance.
- [Install SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server): SQL install path.
- [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server): SQL user/firewall/configuration guidance.
- [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock): Rock installer flow and database settings.
- [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment): separation of web and database.
- [SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting): official SaaS section.
- [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting): managed hosting responsibilities.
- [Scale Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock): official scaling section.
- [Intro to Scaling Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/intro-to-scaling-rock): scaling motivation.
- [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster): scale-up/scale-out and cluster components.
- [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm): Rock-specific web farm setup and behavior.
- [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context): read-only database context and connection strings.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): version caveats and upgrade impacts.

Source-code and implementation landmarks:

- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock): public Rock source repository. Use installed-version source or tagged release where possible, not only the develop branch.

Training and applied sources:

- [Workflows](https://community.rockrms.com/rocku/workflows) and [Workflow Performance Tips](https://community.rockrms.com/rocku/workflows/workflow-performance-tips): workflow load and performance awareness.
- [Introducing Imperator: Proactive Azure Monitoring and Alerting for Rock RMS](https://www.triumph.tech/resources/introducing-imperator-proactive-azure-monitoring-and-alerting-for-rock-rms): applied monitoring themes.
- [The Importance of Infrastructure Maps](https://www.triumph.tech/resources/the-importance-of-infrastructure-maps): documentation and incident-readiness theme.
- [Azure Mobile App](https://www.triumph.tech/resources/azure-mobile-app): Azure health companion concept.
- [Separating Development and Production](https://www.triumph.tech/resources/separating-development-and-production): development/production separation risk.
- [What To Do About the Microsoft Windows PrintNightmare Vulnerability](https://www.triumph.tech/resources/microsoft-windows-printnightmare-vulnerability): Windows service hardening example.
- [What is "MAXDOP"?](https://www.triumph.tech/resources/what-is-maxdop): SQL performance troubleshooting example.

Community examples to verify before applying:

- [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355).
- [Refreshing a Rock Development Environment from Production](https://community.rockrms.com/recipes/352).
- [How to Maintain your Azure SQL Database](https://community.rockrms.com/recipes/259).
- [Automatically scale Azure DTUs on a schedule](https://community.rockrms.com/recipes/296).
- [AWS SES Email SMTP Transport for RockRMS](https://community.rockrms.com/recipes/171).
- [Deploying Rock RMS as an Azure App Service](https://community.rockrms.com/recipes/202).
- [Turn-key RockRMS Hosting with AWS](https://community.rockrms.com/recipes/190).
- [Free Tier AWS Hosting for RockRMS](https://community.rockrms.com/recipes/96).
- [Get Notified of ACME SSL Certificate Renewal](https://community.rockrms.com/recipes/263).
- [Using Office 365 / Azure Active Directory (Microsoft Entra ID) Accounts for Rock Authentication](https://community.rockrms.com/recipes/92).
- [Syncing Local Active Directory with Azure AD (Microsoft Entra ID) for Rock Authentication](https://community.rockrms.com/recipes/91).

Dependency notes:

- Hosting depends on operations because monitoring, backup, restore, patching, and incident response are operational disciplines.
- Hosting depends on security because DNS, SSL, firewall, authentication, API access, file permissions, and secrets are infrastructure concerns.
- Hosting depends on jobs because jobs drive load and side effects.
- Hosting depends on cache because cache clearing, warmup, and web farm invalidation affect correctness and performance.
- Hosting depends on search because indexing and search-heavy pages can drive database and CPU load.
- Hosting depends on CMS because public website traffic, content files, request filters, and Lava endpoints can become production infrastructure surfaces.
- Hosting depends on API integrations because external systems create inbound/outbound traffic, authentication risk, and retry behavior.

When source material is thin or version-dependent, inspect the live Rock instance. The minimum live inspection set is Rock version, hosting model, connection strings, IIS/App Service settings, SQL tier and health, File Storage Providers, File Types, Communication Transports, Service Jobs, Web Farm settings, Observability settings, SSL/DNS, backup policy, and current alert recipients.
