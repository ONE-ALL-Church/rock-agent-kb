---
id: authored-hosting-infrastructure
title: Hosting And Infrastructure
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "477d65eedb87b5d8f440c40328163d0d9eaf6d7d2065852d2a3791d3155b7d7c"
---

# Hosting And Infrastructure

## Agent Summary

Treat hosting as an operating model, not merely a server-selection exercise. An agent should determine:

1. Who owns infrastructure, database, patching, certificates, backups, monitoring, and incident response.
2. Whether the topology satisfies the organization’s security, payment-processing, availability, and performance requirements.
3. Whether the selected capacity reflects actual Rock workloads rather than attendance alone.
4. Whether Rock-specific requirements—such as shared file storage, session affinity, message-bus communication, and a single job-running node in a Rock 19.0 web farm—are satisfied.
5. Which claims are documented behavior and which settings still require inspection in the target environment.

Azure is a supported path, not a Rock requirement. Select among SaaS hosting, internally managed infrastructure, Azure, or another capable provider according to scale, staff expertise, cost, service quality, and desired ownership boundaries. For Azure, Rock’s documented pattern is a Windows virtual machine for the web/application server and Azure SQL as the managed database service. [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)

For a self-hosted deployment that processes credit cards, do not place Rock’s web server and database on the same server. The official internal-hosting guidance identifies that topology as noncompliant with PCI requirements. In a two-server deployment, keep SQL Server private and restrict TCP 1433 to the Rock web server and any explicitly authorized development host. [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server) [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)

Do not claim an environment is operationally ready from documentation or configuration intent alone. The installed Rock version, technical requirements, topology, certificates, storage providers, backups, SMTP transport, scheduled-job placement, and recovery behavior must be inspected or tested in the target environment.

## Scope And Boundaries

This guide covers:

- Hosting-model selection and responsibility boundaries.
- Initial capacity planning.
- Rock’s documented Azure architecture.
- Internally hosted Windows, IIS, and SQL Server preparation.
- Two-server security and PCI constraints.
- Rock web-farm architecture and configuration.
- Shared storage and session-affinity requirements.
- Rock 19.0 read-only and analytics database contexts.
- SSL, patching, backup ownership, and performance posture.
- Infrastructure-oriented troubleshooting and verification recipes.

Related topics remain in their owning concepts:

- Detailed job design and scheduling belong under **Jobs**.
- Cache behavior beyond web-farm coordination belongs under **Cache**.
- Search indexing and search performance belong under **Search**.
- Page, site, and content administration belong under **CMS**.
- Authentication, authorization, secret handling, and broader hardening belong under **Security**.
- Email deliverability and communication-provider configuration belong under **API And Integrations** or the applicable communications concept.
- General application operations and incident management belong under **Operations**.

The source pack contains no reviewed live-instance conclusion. Therefore, this guide describes documented behavior and bounded inspection procedures; it does not certify any installation’s current configuration, security, performance, backups, or readiness.

## Mental Model

Model a Rock environment as five connected decisions.

### 1. Workload

Attendance or database record count can provide an initial sizing category, but neither represents the complete workload. Public-site traffic, check-in peaks, analytics, reports, workflows, APIs, scheduled jobs, plugins, and feature adoption can materially change resource needs. Rock’s Azure guidance explicitly treats attendance tiers as starting points and recommends moving to the next larger tier when the public website also runs in Rock. [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)

### 2. Service ownership

A SaaS provider can operate the cloud environment and database and manage infrastructure concerns such as monitoring, maintenance, backups, certificates, domains, and incidents according to the selected plan. The organization still owns its data and content and remains responsible for Rock configuration, pages, blocks, security, users, workflows, and routine administration. [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)

With internal hosting, those infrastructure duties remain with the organization or its contracted operator. That includes maintaining the supported platform, applying relevant patches, protecting credentials, managing certificates, and proving that backup and recovery arrangements work.

### 3. Topology

A basic environment has a web/application tier and a database tier. A scaled-out environment can add an application gateway, multiple Rock web nodes, and a message bus. A separate read-only database may absorb supported reporting or analytics traffic. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster) [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

### 4. Rock-specific invariants

Generic infrastructure health does not prove that Rock is configured correctly. Important Rock-specific conditions include:

- Payment-processing deployments require separation between the web and database servers.
- A web-farm gateway needs session affinity because check-in relies on session state.
- Files needed by every node must use shared, cloud-backed, database-backed, or deliberately synchronized storage.
- Rock 19.0 web farms require a Spark license and one active supported message-bus transport.
- Rock 19.0 scheduled jobs must run on only one farm node.
- Read-only database contexts can only serve operations that do not need to write.

These conditions are documented in the internal-hosting and scaling guides. [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server) [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster) [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm) [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

### 5. Operational proof

Provisioning and configuration are inputs, not proof of readiness. Readiness requires environment-specific evidence: observed version, current settings, valid certificates, controlled network exposure, known backup ownership, successful restore testing, healthy jobs, reachable dependencies, and workload behavior under representative conditions.

When a stakeholder requests a particular server, screen, workflow, or automation, first restate the underlying problem and generate genuinely distinct approaches. The proposed implementation is valuable requirements evidence, but it may not be the best solution. [Rock Cast, 12:27](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=747s)

## Sizing And Service Options

### Choose the ownership model first

Use the responsibility boundary to narrow the hosting choices:

- **SaaS hosting:** Appropriate when the organization wants a provider to operate and monitor the infrastructure and database. Confirm exactly which updates, backups, certificates, domains, incidents, exceptions, and custom work are included in the selected plan. [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)
- **Internal or self-managed hosting:** Appropriate only when the organization or its operator can maintain Windows, IIS, SQL Server, networking, certificates, patches, backups, monitoring, and incident response. Rock’s internal-hosting guide describes the required Windows Server foundation and directs administrators to the current technical-requirements page before provisioning. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)
- **Azure:** A supported self-managed or partner-managed option, not a requirement. Rock recommends a Windows VM for the web/application tier and Azure SQL for the managed database tier. [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)
- **Other infrastructure providers:** The evidence pack does not establish an official universal architecture for every provider. Community AWS and Azure App Service recipes are examples, not Rock core requirements or endorsements.

Before accepting a hosting proposal, identify the desired outcome: lower operational burden, greater control, PCI-compatible separation, higher availability, better peak performance, geographic placement, predictable cost, or some combination. Do not treat “move to Azure,” “add another server,” or “use App Service” as the problem statement.

### Use sizing tables as baselines

The Rock 19.0 Azure guide supplies attendance-based starting tiers that pair a Windows web VM with an Azure SQL tier. It warns that attendance alone is too simplistic for every environment and that listed prices are estimates subject to change. It also recommends selecting the next larger tier when Rock hosts the public website. [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)

For an assessment, collect at least:

- Peak weekend attendance and peak concurrent use.
- Whether Rock serves the public website.
- Check-in concurrency and event peaks.
- Database size and growth.
- Analytics and reporting intensity.
- Scheduled-job load.
- API and integration traffic.
- Plugin and custom-code usage.
- Availability and recovery expectations.
- Current CPU, memory, database, storage, and response-time evidence.

The internal-hosting guide also provides record-count-based small, medium, and large examples. Treat those as sizing guidance, not the current platform compatibility matrix. The same guide directs administrators to Rock’s technical-requirements page for current server, database, browser, and mobile minimums. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)

For Rock v18 and later, the supplied approved claim states that the internal-hosting requirements call for SQL Server 2022 or newer, even where older sizing material may still name earlier SQL editions. Confirm the current supported requirements before purchasing or provisioning.

### Decide between scaling up and scaling out

Scaling up adds resources such as CPU and memory to an existing server. Scaling out adds servers. Rock’s cluster guidance notes that CPU is often the limiting resource in a Rock environment and warns that clustering adds infrastructure and operational complexity. A poorly designed or poorly operated cluster can reduce uptime rather than improve it. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

Do not recommend a web farm solely because an environment is slow. First determine whether the constraint is:

- Insufficient compute capacity.
- Database contention.
- A slow page component.
- A report or analytics workload.
- A scheduled job.
- A plugin or customization.
- Local-file access across nodes.
- Session routing.
- A broader infrastructure or network issue.

## SaaS Hosting

In the documented SaaS model, the provider runs and monitors the cloud environment and database and manages infrastructure functions according to the selected plan. The organization uses and configures Rock and retains responsibility for its data, content, users, security, pages, blocks, workflows, and day-to-day administration. [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)

Before a public SaaS launch:

1. Select the hosting partner and plan.
2. Inventory the current system, including data, files, domains, integrations, plugins, customizations, and communication dependencies.
3. Arrange a kickoff with the provider.
4. Prepare the migration plan.
5. Reserve a test period before public launch.
6. Confirm the responsibility boundary for updates, backups, certificates, domains, monitoring, incidents, and custom work.
7. Verify the migrated environment through representative administrative and public journeys.

The first five steps are part of Rock’s documented SaaS getting-started sequence. [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)

Do not infer that “fully managed” transfers ownership of Rock configuration or organizational security to the provider. Do not infer a recovery objective, backup-retention period, restore-testing practice, update cadence, or incident-response commitment unless the selected plan states it.

## Azure Hosting

### Recommended service pattern

Rock’s documented Azure recommendation combines:

- A Windows virtual machine using infrastructure as a service for the Rock web/application server.
- IIS running on that VM.
- Azure SQL using platform as a service for the database.
- A shared Azure resource group containing the web VM, Azure SQL server, and Azure SQL database. [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options) [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting)

Rock recommends Azure SQL over running SQL Server in another VM in this pattern. The documentation intentionally avoids fixed portal walkthroughs because Azure screens and steps change frequently. An agent should therefore verify the resulting resource relationships and settings instead of relying on matching screenshots. [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting)

A community draft describes deploying Rock to Azure App Service, but it is explicitly unpublished community material. It does not override the official Windows VM plus Azure SQL recommendation. [Community draft: Deploying Rock RMS as an Azure App Service](https://community.rockrms.com/recipes/202)

### Azure SQL identity setup

Azure SQL Database and SQL Server hosted on a VM use different administration paths. For Azure SQL Database, the approved setup sequence is:

1. Create Rock’s SQL-authenticated login.
2. Create the corresponding user in the `master` database.
3. Add that user to the `dbmanager` and `loginmanager` roles.
4. Allow Rock’s installer to create the application database.
5. Create the corresponding user inside the new Rock database.
6. Add that database user to `db_owner`.
7. Test the Rock-specific login before proceeding.

The official guide provides the applicable SQL and distinguishes Azure SQL Database from SQL Server running locally or on an Azure VM. [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server)

Do not copy example passwords or connection strings from documentation. Use environment-specific credentials, protect them, and avoid exposing them in logs or public artifacts.

### Azure nonprofit credits

The supplied v19.0 documentation describes an Azure nonprofit-credit program and eligibility and registration steps. Program eligibility, amounts, covered products, renewal behavior, and pricing can change independently of Rock. Treat the documentation as a route to the program, then confirm the current Microsoft terms before using the credit in a budget or architecture decision. [Register for Credits as a Non-Profit](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit)

## Internal Hosting

### Platform requirements

Rock’s internal-hosting guide requires a Windows Server environment and directs administrators to the current Rock Technical Requirements before purchasing or provisioning. The supplied approved claim further scopes Rock v18 and v19 to SQL Server 2022 or newer. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)

For a Rock 19.0 SQL Server installation:

- Use Mixed Mode authentication.
- Retain the SQL Server password securely because it is needed during Rock database setup.
- Prefer the default SQL Server instance unless the administrator is experienced with named instances. The default instance simplifies later Rock configuration. [Install SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server)

These are installation-specific instructions, not permission to expose administrative credentials or use the server-wide administrator account as Rock’s routine application identity.

### Windows roles and features

For an internally hosted Rock web server, install:

- The IIS Web Server role.
- The ASP.NET 4.x role service appropriate to the Windows Server version.
- WebSocket Protocol.
- Application Initialization.
- .NET Framework 3.5 Features. [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features)

If Windows reports that feature sources are unavailable, mount installation media matching the Windows Server version and specify its `sources\sxs` directory as the alternate source path. [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features)

### IIS configuration

For Rock 19.0, the supplied official configuration specifies:

- .NET Framework v4.0 for the application pool.
- Automatic application-pool startup.
- `LocalSystem` as the application-pool identity.
- An idle timeout of zero.
- Website preloading enabled.
- Recycling at a specific low-traffic time rather than at regular intervals. [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis)

Enable IIS dynamic-content compression when the setting is available. If it is disabled because the required compression module is absent, the official guide permits skipping that step. [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis)

These settings are version-scoped guidance. Inspect the actual application pool and site before concluding they are present.

### Initial Rock installation

For the documented Rock 19.0 installation path:

1. Place only `Start.aspx` and `web.config` from the installer package in the IIS web root.
2. Open `/Start.aspx` locally.
3. Supply the Rock database server, database name, and Rock-specific SQL credentials.
4. Complete the installer’s environmental checks.
5. Create the initial Rock administrator account.
6. Enter the intended internal and public URLs and organizational information.
7. Allow the installer to download the application and configure the database.
8. After installation, inspect the Administrator Checklist and the resulting site routing. [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock)

Rock recommends enabling snapshot isolation so database writes do not block reads. The setting may already be enabled depending on SQL Server edition and version, so inspect rather than assume. [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock)

### Two-server deployments

Separating the web and database tiers avoids resource competition, enables a stronger network boundary, and is required by the supplied Rock guidance when the installation processes credit cards. [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)

For a self-hosted two-server environment:

- Do not publish the SQL Server through a public IP or general internet-facing NAT rule.
- Restrict TCP 1433 to the Rock web server and any explicitly authorized development host.
- Install and configure SQL Server on the database server.
- Install the required roles and configure IIS on the web server.
- Point Rock’s installer at the private database endpoint. [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)

## Web Farms And Server Clusters

### Architecture

Rock’s documented cluster model includes:

1. An application gateway.
2. Multiple Rock web application nodes.
3. A database.
4. A message bus used by the nodes to coordinate. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

A database cluster is optional from Rock’s perspective; database clustering is provider-specific and transparent to Rock when exposed through the expected database connection. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

### Licensing and message bus

A Rock web farm requires:

- A Spark web-farm license.
- The gateway, database, and web nodes already provisioned.
- Rock installed and running on each web node.
- An active supported message-bus transport.
- Web-farm activation under `Admin Tools > System Settings > Web Farm`.
- A restart of all web nodes after activation.
- Confirmation that every expected node appears on the Web Farm page. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

For Rock 19.0, the supported transports in the approved claim are Azure Service Bus and RabbitMQ, with only one transport active. Earlier Redis-based clustering is deprecated in the documented cluster guidance. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

### Session affinity

Enable session affinity at the gateway so a client continues to reach the same node. This is especially important because Rock check-in relies on session state. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

A healthy-node count does not prove affinity. Verify that the gateway’s routing behavior preserves the client session during an actual check-in journey.

### Shared files

A node’s local file system is not automatically visible from another node. Consequently:

- Rock File Types used across the farm should use cloud-backed or database-backed storage.
- Directories that accept local uploads must be synchronized if their files must be served by every node.
- Content uploaded to a node-local directory can appear as a broken link when a later request reaches a different node. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

The cluster guidance specifically identifies the HTML editor’s local content directory as an example of a path that may need synchronization. Synchronization introduces another service to operate, so shared storage should be considered during architecture rather than after broken links appear. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

Rock 19.1 release notes also describe an automatic migration from a legacy Azure Blob Storage provider to the core provider because the legacy provider could no longer upload large files after v19 library updates. Existing files continue to work while File Types are updated. This is version-specific upgrade behavior, not proof that any installation completed the migration successfully. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Scheduled jobs

In Rock 19.0, configure scheduled jobs to run on only one web-farm node. The web-farm feature does not prevent multiple nodes from running them. The controlling placement is configured in the server’s web configuration. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

Rock v20.0 alpha release notes describe a shared locking system intended to prevent a single job from executing concurrently across node instances. Because that behavior is alpha and later than the approved v19.0 claim, it must not be used to relax the single-job-node requirement for a v19 environment. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Routes and node coordination

The Rock 19.0 web-farm documentation states that page-route changes are not immediately communicated to other nodes. They are refreshed with application-pool restart behavior; if the route must be available sooner, restart each node. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

The message bus supports node coordination such as cache invalidation and node-status communication. Inspect the Web Farm page and logs when nodes appear inactive, cache behavior diverges, or leadership changes unexpectedly. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

## Read-Only And Analytics Database Contexts

Rock 19.0 supports separate connection strings for selected read workloads.

### `RockContextReadOnly`

Adding `RockContextReadOnly` to `web.ConnectionStrings.config` allows Data Views and Reports to use a read-only database. If an individual Data View contains filters or plugins that write to the database, an administrator can enable **Disable Use Of Read Only Context** for that Data View. [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

Do not assume that every report-like operation is read-only. A plugin filter can perform writes even when the surrounding task appears analytical.

### `RockContextAnalytics`

In Rock 19.0, these blocks use `RockContextAnalytics`:

- Giving Analytics.
- Attendance Analytics.
- Pledge Analytics.

The connection can be added to `web.ConnectionStrings.config` and directed to a separate read-only database. [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

Before enabling either context, verify:

- The replica or secondary database exists.
- Its data freshness is acceptable for the workload.
- Rock’s credentials can connect with the intended access.
- The connection-string name is exact.
- The target operation does not require writes.
- Failure behavior is understood before production use.

The evidence establishes the Rock configuration mechanism, not the replication technology or the target environment’s consistency and failover behavior.

## Operational Readiness

### SSL and public exposure

Before publishing an internally hosted Rock site, configure a valid SSL certificate. The v19.0 internal-hosting guide recommends requiring encryption at the Rock Site level for both the internal Rock site and the external site, causing HTTP requests to be redirected to HTTPS. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)

For a clustered environment, Rock recommends a provisioned wildcard certificate instead of an ACME certificate because cluster-wide certificate handling adds complexity. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

The internal-hosting documentation references a community ACME plugin as a simpler option for some non-clustered installations. Plugin installation, compatibility, renewal, IIS binding, and visible HTTPS behavior must be verified in the actual environment. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)

### Backups and recovery

The SaaS documentation describes daily backups as a benefit and assigns backup management to the provider according to the selected plan. Confirm the plan’s actual retention and recovery terms rather than inferring them from the general description. [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)

For internal hosting, the sizing examples explicitly exclude local backup storage. The evidence pack does not provide an approved self-hosted backup architecture, retention policy, recovery objective, or restore procedure. Those are live operational gaps that must be resolved before launch. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting)

Community recipes discuss database snapshots, web-root backups, and development refreshes, but those examples are not core-reviewed standards and may contain organization-specific assumptions. [Community recipe: Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355) [Community recipe: Refreshing a Rock Development Environment from Production](https://community.rockrms.com/recipes/352)

### SMTP

The evidence pack contains no approved official SMTP configuration for this concept. A community recipe demonstrates one historical AWS SES pattern, including provider credentials, an SMTP endpoint, and a test message, but the recipe is not endorsed by the Rock core team and its pricing, ports, provider behavior, and tracking limitations may have changed. [Community recipe: AWS SES Email SMTP Transport for RockRMS](https://community.rockrms.com/recipes/171)

Treat SMTP as an integration that requires separate verification of:

- The active Rock transport.
- Provider account and sending-domain state.
- Credential storage.
- Network egress.
- Sender authorization.
- Test delivery.
- Bounce, complaint, and tracking behavior.
- The distinction between infrastructure health and email deliverability.

### Patching

Self-hosted operators own their patch cadence. Supported Rock dot releases can contain security fixes and should not automatically be treated as optional. Confirm the currently supported branches and read the release notes before an upgrade. [Rock Cast, 06:36](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s) [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

Do not infer that a newer major version is production-ready from its presence in release notes. The supplied release page labels v20.0 as alpha, while the installation and configuration evidence in this guide is primarily scoped to v19.0.

### Performance posture

For a slow page in Rock v19, the Page Load Time diagnostic can expose page-debug timing traces without a separate observability platform. Use it to identify slow page components, then correlate the result with broader telemetry when the problem is intermittent or appears infrastructure-wide. [New Features & Enhancements Coming to v19, 16:43](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s)

Other evidence-supported performance controls include:

- Correct IIS application-pool startup, timeout, preload, recycling, and compression settings. [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis)
- Snapshot isolation to reduce read/write blocking. [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock)
- Read-only contexts for supported reporting and analytics traffic. [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)
- Capacity decisions that account for public-site and feature workload rather than attendance alone. [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)

A single diagnostic does not prove the absence of database, network, storage, provider, or cross-node problems.

## Version And Authority Caveats

- Most installation, IIS, web-farm, and database-context evidence in this guide is from Rock v19.0 documentation.
- The SQL Server 2022-or-newer requirement is explicitly scoped to Rock v18 and later in the supplied approved claim. Confirm the current technical-requirements page before provisioning.
- Rock v20.0 behavior mentioned here is alpha release-note information. It is upcoming behavior, not a substitute for v19.0 operating rules.
- The Azure sizing chart and pricing are planning baselines. Azure SKUs, pricing, credits, and portal workflows can change independently of Rock documentation.
- The Rock 19.1 Azure Blob Storage migration is release-specific. Confirm installed version, migration completion, provider state, and File Type assignments in the target installation.
- Official documentation and approved claims establish product guidance; they do not prove an installation’s configuration.
- Rock release notes establish that a fix or migration was released for a version; they do not prove that the target environment installed it successfully.
- Community recipes are examples. They are explicitly not reviewed or endorsed by the Rock core team and may be old, provider-specific, insecure for another topology, or dependent on unstated configuration.
- The supplied GitHub source matches were not used as factual authority because they did not directly support this concept’s hosting behavior. For example, [`FinancialPersonSavedAccountQueryOptions.cs`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Finance/FinancialPersonSavedAccountService/Options/FinancialPersonSavedAccountQueryOptions.cs) describes finance query options, not hosting topology. A repository path or matching property name is not enough to establish an operational requirement.
- No live database, server, Azure subscription, provider portal, DNS zone, certificate, gateway, Rock configuration, or recovery test was inspected for this guide.

## Troubleshooting Decision Tree

### A Rock page is slow

1. Confirm the Rock version. In v19, capture the Page Load Time diagnostic trace for the affected page. [New Features & Enhancements Coming to v19, 16:43](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s)
2. Identify whether one block or component dominates the trace.
3. Reproduce at a known time and record whether the issue is constant, intermittent, or load-dependent.
4. Inspect IIS application-pool startup, idle timeout, preload, recycling, and dynamic-compression settings. [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis)
5. Determine whether the page invokes Data Views, Reports, analytics, plugins, APIs, or long-running database operations.
6. Inspect whether snapshot isolation is enabled and whether supported read workloads are eligible for `RockContextReadOnly` or `RockContextAnalytics`. [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock) [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)
7. Compare the symptom with CPU, database, network, and provider telemetry.
8. Stop when the slow component or infrastructure constraint is identified with repeatable evidence; do not prescribe a web farm solely from the symptom.

### Files or images work intermittently in a web farm

1. Confirm that requests are reaching more than one web node.
2. Identify the Rock File Type or upload path used by the missing asset.
3. If the File Type uses node-local File System storage, move the design toward cloud-backed or database-backed storage.
4. If the file was uploaded directly to a node-local content directory, verify whether that directory is synchronized across nodes.
5. Request the same asset through each node or controlled gateway routing.
6. Stop when every node can serve the same asset and the storage or synchronization owner is documented. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

### Check-in loses state or behaves differently between requests

1. Confirm that the environment uses multiple web nodes.
2. Inspect the gateway’s session-affinity configuration.
3. Trace a representative check-in client across consecutive requests.
4. Confirm that the client remains on the same node for the session.
5. Stop when the session remains stable through an end-to-end check-in journey. [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

### A scheduled job runs more than once in a web farm

1. Confirm the exact Rock version.
2. For Rock 19.0, inspect every node’s web configuration and identify which node is allowed to run jobs.
3. Ensure only one node is configured as the job runner.
4. Review job history and downstream effects for duplicate execution.
5. Do not use v20.0 alpha shared-locking release notes as evidence that a v19 farm is safe.
6. Stop when a single v19 job-running node is proven and a subsequent scheduled execution produces only the expected run. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm) [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### A web-farm node is missing or appears unresponsive

1. Confirm that the Spark web-farm license is active.
2. Confirm that exactly one supported message-bus transport is active.
3. Verify that the gateway, database, and expected web nodes are running.
4. Confirm that Rock is installed on each node.
5. Restart all nodes after web-farm activation or configuration changes.
6. Inspect the Web Farm page and web-farm log for startup, shutdown, status, or leadership events.
7. Confirm that every expected node appears.
8. Stop when node membership and message-bus communication are stable. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

### A new page route works on only some nodes

1. Confirm that the environment is a Rock 19.0 web farm.
2. Verify that the route itself was saved correctly.
3. Restart each node so the route table is refreshed before the normal application-pool cycle.
4. Test the route against every node or through repeated controlled gateway requests.
5. Stop when all nodes resolve the route consistently. [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

### Rock cannot connect to SQL Server

1. Identify the database type: Azure SQL Database, SQL Server on an Azure VM, or local/self-hosted SQL Server.
2. Verify the server name, database name, Rock-specific login, and connection target without exposing the password.
3. For Azure SQL Database, verify the login and `master` user, the `dbmanager` and `loginmanager` roles, and the database user’s `db_owner` membership.
4. For a self-hosted two-server deployment, verify TCP 1433 is permitted from the Rock web server’s address.
5. Confirm that SQL Server is private rather than generally internet-exposed.
6. Test the Rock-specific SQL login independently.
7. Stop when the Rock web server can connect using the intended restricted identity and network path. [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server) [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment)

### Windows cannot install a required server feature

1. Confirm that the requested feature is part of the documented Rock web-server prerequisites.
2. Obtain installation media matching the Windows Server version.
3. Mount the media.
4. Set the alternate feature source to its `sources\sxs` directory.
5. Retry installation.
6. Stop when IIS, the applicable ASP.NET 4.x role service, WebSocket Protocol, Application Initialization, and .NET Framework 3.5 Features are present. [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features)

### A Data View or report fails against the read-only database

1. Confirm that `RockContextReadOnly` is present and points to the intended database.
2. Test basic connectivity and data availability.
3. Identify whether the Data View contains a plugin or filter that performs writes.
4. If writes are required, enable **Disable Use Of Read Only Context** for that specific Data View.
5. Retest the operation against the primary context.
6. Stop when the operation succeeds and its context selection is documented. [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

### Analytics still load the primary database

1. Confirm the installation is Rock 19.0 or another version documented to support the setting.
2. Verify that the connection-string name is exactly `RockContextAnalytics`.
3. Confirm that it points to the intended read-only target.
4. Test Giving Analytics, Attendance Analytics, and Pledge Analytics separately.
5. Observe the target database or connection telemetry during the test.
6. Stop when the intended analytics traffic is observed on the target context. [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

### HTTP does not redirect to HTTPS

1. Confirm a valid certificate is installed and bound to the intended IIS site.
2. Inspect the Rock Site record for **Require Encryption**.
3. Enable the setting for the internal and external Rock sites where applicable.
4. Test direct HTTP and HTTPS requests from outside the server.
5. In a farm, confirm certificate coverage and binding behavior across the gateway and nodes.
6. Stop when HTTP consistently reaches the intended HTTPS endpoint and the presented certificate is valid. [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster)

## Agent Task Recipes

### Recipe: Select a hosting model

**Outcome:** A documented hosting choice with explicit ownership, workload, security, and verification conditions.

1. Restate the underlying organizational problem.
2. Produce distinct options that include at least SaaS hosting and self-managed hosting; include Azure only when it fits the requirements.
3. Inventory staff capacity, peak workload, public-site use, payment processing, integrations, plugins, customizations, availability goals, and budget constraints.
4. For each option, assign ownership for infrastructure, database, patches, certificates, domains, backups, monitoring, incidents, Rock configuration, users, and workflows.
5. Reject any single-server payment-processing topology.
6. Compare the options and record the unresolved live checks.
7. Stop when the selected model has a named owner for every operational responsibility.

**Do not assume:**

- Azure is required.
- SaaS transfers ownership of Rock configuration.
- A lower-cost provider supplies equivalent Rock expertise or service quality.
- A proposed platform is the only way to solve the underlying problem.

Sources: [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting), [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting), [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server)

### Recipe: Build an Azure capacity baseline

**Outcome:** A provisional Azure tier supported by workload evidence and marked for validation.

1. Record peak weekend attendance.
2. Select the corresponding starting tier from the current Rock Azure sizing table.
3. Move one tier larger if Rock hosts the public website.
4. Adjust for database size, feature intensity, analytics, reports, check-in, scheduled jobs, integrations, plugins, and growth.
5. Use the documented Windows VM plus Azure SQL pattern as the baseline.
6. Retrieve current Azure SKU availability and pricing before budgeting.
7. Define the telemetry and representative journeys that will validate the tier.
8. Stop when the baseline, assumptions, and post-provision validation plan are recorded.

**Do not assume:**

- Attendance predicts every workload.
- Prices or nonprofit credits in an older excerpt remain current.
- More memory alone resolves a CPU or database bottleneck.

Source: [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options)

### Recipe: Prepare a SaaS migration

**Outcome:** A provider-ready migration plan with a reserved test window and clear responsibility boundary.

1. Choose the hosting partner and plan.
2. Inventory the current Rock version, database, files, domains, certificates, integrations, SMTP, plugins, custom code, jobs, and external dependencies.
3. Schedule the provider kickoff.
4. Define the migration sequence and rollback decision points.
5. Reserve a test period before public launch.
6. Confirm plan-specific responsibility for updates, backups, restores, certificates, domains, monitoring, incidents, and custom work.
7. Run representative administrative and public journeys in the migrated environment.
8. Stop before public launch if ownership, migration scope, or test results remain unresolved.

Source: [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting)

### Recipe: Provision the documented Azure layout

**Outcome:** A resource group containing the intended Rock web VM and Azure SQL resources.

1. Create or select the Rock production resource group.
2. Provision the Windows web VM in that group.
3. Configure IIS on the web VM.
4. Provision the Azure SQL server and database in the same resource group.
5. Create Rock’s Azure SQL login and `master` user.
6. Grant `dbmanager` and `loginmanager`.
7. Run the Rock installation so the application database is created.
8. Create the Rock user in the application database and add it to `db_owner`.
9. Test the restricted Rock login.
10. Verify the resulting resources and connections directly; do not rely on portal-screen similarity.

**Inspect:**

- Subscription and environment.
- Resource-group membership.
- Network access.
- Database identity and roles.
- Connection target.
- Installed Rock version.

Sources: [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting), [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server)

### Recipe: Prepare an internal Rock 19 web server

**Outcome:** A Windows/IIS host ready for the documented Rock 19 installer.

1. Confirm the current Rock technical requirements and SQL Server requirement.
2. Install IIS, the applicable ASP.NET 4.x role service, WebSocket Protocol, Application Initialization, and .NET Framework 3.5 Features.
3. Configure the application pool for .NET Framework v4.0, automatic startup, `LocalSystem`, and zero idle timeout.
4. Configure a specific low-traffic recycling time.
5. Enable website preload.
6. Enable dynamic-content compression when the module is available.
7. Place only `Start.aspx` and `web.config` from the installer in the web root.
8. Open `/Start.aspx` locally.
9. Stop when the installer’s environmental checks pass.

Sources: [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features), [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis), [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock)

### Recipe: Activate a Rock 19 web farm

**Outcome:** All expected Rock nodes are visible and coordinated without duplicate job runners.

1. Obtain and record the Spark web-farm license.
2. Confirm that the gateway, database, web nodes, and Rock installations are running.
3. Configure session affinity at the gateway.
4. Move shared Rock File Types away from node-local storage or establish deliberate synchronization.
5. Configure one supported message-bus transport: Azure Service Bus or RabbitMQ.
6. Configure jobs to run on only one node.
7. Open `Admin Tools > System Settings > Web Farm`.
8. Activate the farm and enter the license.
9. Restart every web node.
10. Confirm every expected node appears on the Web Farm page.
11. Exercise cache-affecting changes, shared files, page routes, check-in sessions, and a scheduled job.
12. Stop when node membership, affinity, shared-file access, message-bus coordination, and single job execution are proven.

Sources: [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster), [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm)

### Recipe: Offload reports and analytics to a read-only database

**Outcome:** Eligible Rock 19 reporting or analytics traffic uses the intended read-only target.

1. Confirm the read-only database or replica exists.
2. Determine whether the target workload is Data Views and Reports or the three supported analytics blocks.
3. Add `RockContextReadOnly` for Data Views and Reports, or `RockContextAnalytics` for Giving, Attendance, and Pledge Analytics.
4. Preserve the primary `RockContext`.
5. Test connectivity without exposing connection-string secrets.
6. Exercise each target workload.
7. For a Data View that requires writes, enable **Disable Use Of Read Only Context** on that Data View.
8. Observe which database receives the test traffic.
9. Stop when routing and write behavior match the intended design.

Source: [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

### Recipe: Diagnose a slow Rock 19 page

**Outcome:** A repeatable diagnosis identifies either a page component or a broader infrastructure constraint.

1. Capture the affected URL, user context, time, and expected behavior.
2. Run the v19 Page Load Time diagnostic.
3. Identify the slowest page components.
4. Repeat the test to determine whether the result is stable.
5. Correlate it with IIS, CPU, database, storage, network, and provider telemetry.
6. Inspect snapshot isolation and supported read-only-context opportunities.
7. Record whether the cause is component-specific, database-related, capacity-related, intermittent, or unresolved.
8. Stop when the evidence supports a bounded next action.

**Do not assume:**

- A slow page proves the server is undersized.
- A clean trace rules out intermittent infrastructure issues.
- Adding web nodes fixes database or custom-code constraints.

Sources: [New Features & Enhancements Coming to v19, 16:43](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s), [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock), [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context)

### Recipe: Perform a pre-launch infrastructure review

**Outcome:** A go/no-go record separates verified readiness from unresolved conditions.

1. Confirm the exact Rock, Windows, IIS, and SQL versions against current requirements.
2. Confirm topology and PCI-required web/database separation.
3. Inspect SQL network exposure and allowed TCP 1433 sources.
4. Validate HTTPS for internal and external Rock sites.
5. Confirm backup ownership, retention, and a tested restore path.
6. Confirm patch ownership and supported Rock branch.
7. Verify SMTP through a controlled delivery test.
8. Confirm file-storage behavior, especially across multiple nodes.
9. Confirm the single job-running node for Rock 19 farms.
10. Exercise representative public, administrative, check-in, reporting, and integration journeys.
11. Record unresolved gaps and assign owners.
12. Stop before launch if a security, payment-processing, recovery, certificate, or critical-path dependency remains unverified.

## Known Gaps And Live Verification

No reviewed live-instance evidence was supplied. Before applying this guide to an installation, verify:

- Exact installed Rock version and supported branch.
- Current Rock Technical Requirements.
- Windows Server, IIS, .NET, and SQL Server versions.
- SaaS plan terms and provider responsibility boundaries.
- Azure subscription, region, resource group, VM, database, SKU, cost, credit, and network configuration.
- SQL authentication, database roles, firewall scopes, and public exposure.
- PCI applicability and actual web/database separation.
- IIS application-pool settings, preload, recycling, and compression.
- Snapshot-isolation state.
- SSL certificate coverage, expiration, renewal, gateway termination, IIS bindings, and Rock Site encryption settings.
- Backup scope, retention, encryption, recovery objectives, off-system storage, and successful restore testing.
- Active SMTP transport, provider status, egress, sender authorization, delivery, bounce, complaint, and tracking behavior.
- Active Rock File Types and storage providers.
- Node-local upload paths and synchronization.
- Spark web-farm license.
- Active message-bus transport and connectivity.
- Gateway health and session affinity.
- Expected web-farm node membership.
- The one node permitted to run scheduled jobs in Rock 19.
- `RockContextReadOnly` and `RockContextAnalytics` targets, credentials, freshness, and workload compatibility.
- Plugin and custom-code behavior against read-only contexts.
- Completion of the Rock 19.1 Azure Blob Storage migration when applicable.
- Representative performance under public-site, check-in, reporting, job, and integration load.

The evidence pack does not provide an approved universal design for:

- Self-hosted backup and disaster recovery.
- SMTP provider selection or configuration.
- Monitoring and alert thresholds.
- CDN architecture.
- DNS failover.
- Storage synchronization tooling.
- Database high availability.
- Azure region selection.
- App Service hosting.
- AWS hosting.
- Development-environment refreshes.
- Production database-maintenance scripts.

Community recipes exist for several of these tasks, but they remain examples requiring separate review, current-provider validation, security assessment, and testing.

## Source Map

### Official hosting documentation

- [Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting) — Documentation branch index; routing only.
- [Intro to SaaS Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting) — SaaS responsibility boundary and migration preparation. Supports approved claims `claim:3800f13989d805462464` and `claim:8c1831684d187b61b4b3`.
- [Intro to Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) — Azure as an optional hosting path and service-quality consideration. Supports `claim:68698a0c2c178f98cb2f`.
- [Compare Sizing and Service Options](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options) — Attendance-based starting tiers, public-site sizing adjustment, and Windows VM plus Azure SQL recommendation. Supports `claim:b6d0c03e3e8239dd60fa` and `claim:dba9f8a7413cfd92b396`.
- [Register for Credits as a Non-Profit](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit) — Versioned program-registration material; current external terms require confirmation.
- [Next Steps for Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting) — Resource-group, Windows VM, IIS, Azure SQL server, and database pattern. Supports `claim:bed80224adc3fdd6cdd5`.
- [Intro to Internal Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) — Technical-requirement routing, sizing examples, PCI warning, SSL, and backup-storage caveat. Supports `claim:867da60eac2e0656c815`.
- [Install Server Roles and Features](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features) — IIS and Windows prerequisites and alternate-source recovery. Supports `claim:9b9df369582719c96c6f` and `claim:c73905a84136ab13b3ee`.
- [Configure Internet Information Services (IIS)](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis) — Rock 19 IIS application-pool, recycling, preload, and compression settings. Supports `claim:cdd73efcdcd014bed67e` and `claim:febe1cab499e9e195f40`.
- [Install SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server) — Rock 19 default-instance and Mixed Mode guidance. Supports `claim:3f74a64709044adaf969` and `claim:76b31296b6897d4734e3`.
- [Configure SQL Server](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server) — Azure SQL roles, SQL networking, and PCI topology. Supports `claim:6655fc3d1ab7b3e572b8` and `claim:82f246088b04f492eae3`.
- [Install Rock](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock) — Rock 19 installer entrypoint and snapshot-isolation guidance. Supports `claim:c8c3b5fee19159470362` and `claim:f62f45338771fcbbac1a`.
- [Configure a Two-Server Environment](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment) — Server separation and restricted SQL access. Supports `claim:249814408c9c8842ef96`.
- [Architect a Server Cluster](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster) — Scaling model, cluster components, session affinity, shared storage, and cluster complexity. Supports `claim:0ac39c6f9dbf72e1b72a` and `claim:9c187d24db6cdacee04d`.
- [Configure a Rock Web Farm](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm) — Licensing, message bus, activation, node restart, job-runner limitation, routes, and node coordination. Supports `claim:53bd55e60a255464` and `claim:89bb09e36da247e182b1`.
- [Configure Your Rock Context](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context) — Rock 19 read-only and analytics database contexts. Supports `claim:3ed81d9b24e959e50b55` and `claim:b9c67d8e492d7f718308`.

### Official release and operational evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — Version-specific fixes and migrations, including the Rock 19.1 Azure Blob Storage migration and v20.0 alpha job-locking behavior.
- [New Features & Enhancements Coming to v19, 16:43](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s) — Page Load Time diagnostic. Supports `claim:091606bd3b8b0472392a`.
- [Rock Cast, 06:36](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s) — Patch-cadence guidance. Supports `claim:e78d41d7fefc84b6e9e7`.
- [Rock Cast, 12:27](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=747s) — Problem-first solution design. Supports `claim:9f3fc654783d47c63bb4`.

### Community examples not promoted to official behavior

- [Refresh a Development Server in Azure](https://community.rockrms.com/recipes/355) — Provider- and organization-specific development-refresh example.
- [Refreshing a Rock Development Environment from Production](https://community.rockrms.com/recipes/352) — Community overview of database, preparation-script, and web-root refresh stages.
- [How to get a Free SSL Certificate on your Windows Server](https://community.rockrms.com/recipes/66) — Historical Windows/IIS ACME example.
- [AWS SES Email SMTP Transport for RockRMS](https://community.rockrms.com/recipes/171) — Historical provider-specific SMTP example.
- [Turn-key RockRMS Hosting with AWS](https://community.rockrms.com/recipes/190) — Community AWS architecture example; not an official universal topology.
- [How to Maintain your Azure SQL Database](https://community.rockrms.com/recipes/259) — Community database-maintenance example requiring independent review.
- [Deploying Rock RMS as an Azure App Service](https://community.rockrms.com/recipes/202) — Unpublished draft community recipe; does not override the official Azure VM plus Azure SQL recommendation.
