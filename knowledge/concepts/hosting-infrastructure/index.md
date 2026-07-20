---
id: concept-hosting-infrastructure
title: Hosting And Infrastructure
generated: true
last_built: 2026-07-20T05:21:53+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 60
depends_on_topics:
  - operations
  - security
  - jobs
  - cache
  - search
  - cms
  - api-integrations
---

# Hosting And Infrastructure

Rock hosting, sizing, Azure and infrastructure guidance, web farms, backups, SSL, SMTP, storage, performance posture, and operational readiness.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Hosting And Infrastructure` spans operations, security, jobs, cache, search, cms. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_youtube, rock_podcast_rss, rock_recipes, triumph_resources, rock_core_release_notes.
- Related tags found in source records: operations, sql, usage, workflow, admin, lava, releases, integrations.
- Source detail types include: documentation_article, question, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| The Vatican on AI and Grandmasters on Ministry \| Ep 215 Transcript Insight | Rock security patch cadence | 06:36 | Self-hosted Rock operators own their patch cadence, and supported dot releases can carry security fixes that should not be treated as optional. Confirm currently supported branches and review current release notes before upgrading. | [source](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s) |
| The Vatican on AI and Grandmasters on Ministry \| Ep 215 Transcript Insight | solution-option discipline | 12:27 | Before implementing a requested screen, workflow or automation, restate the underlying problem and generate several genuinely distinct approaches. A stakeholder's proposed solution may be valuable requirements evidence without being the best implementation. | [source](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=747s) |
| The Vatican on AI and Grandmasters on Ministry \| Ep 215 Transcript Insight | Rock security patch cadence | 06:36 | Self-hosted Rock operators own their patch cadence, and supported dot releases can carry security fixes that should not be treated as optional. Confirm currently supported branches and review current release notes before upgrading. | [source](https://shows.acast.com/rock-cast/episodes/the-vatican-on-ai-and-grandmasters-on-ministry-ep-215) |
| The Vatican on AI and Grandmasters on Ministry \| Ep 215 Transcript Insight | solution-option discipline | 12:18 | Before implementing a requested screen, workflow or automation, restate the underlying problem and generate several genuinely distinct approaches. A stakeholder's proposed solution may be valuable requirements evidence without being the best implementation. | [source](https://shows.acast.com/rock-cast/episodes/the-vatican-on-ai-and-grandmasters-on-ministry-ep-215) |
| Workflow Performance Tips Transcript Insight | Rock operations | 00:00 | The Workflow Performance Tips RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/workflows/workflow-performance-tips) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | configuration | In Rock 19.0, Giving Analytics, Attendance Analytics, and Pledge Analytics use the RockContextAnalytics connection, which can be configured in web.ConnectionStrings.config to target a separate read-only database. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context) |
| official | configuration | For a Rock 19.0 internal-hosting installation, configure SQL Server with Mixed Mode authentication and retain the SQL Server password securely because it is required when setting up the Rock database. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server) |
| official | configuration | A Rock web farm requires a Spark web-farm license and an active message-bus transport; Rock 19.0 supports Azure Service Bus or RabbitMQ, with only one transport active. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm) |
| official | configuration | With SaaS-hosted Rock, the hosting provider operates and monitors the cloud environment and database and manages infrastructure concerns such as maintenance, backups, certificates, domains, and incidents according to the selected plan; the organization remains responsible for its data, content, Rock configuration, users, security, workflows, and routine administration. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting) |
| official | configuration | For an internally hosted Rock web server, install the IIS Web Server role with the Windows ASP.NET 4.x role service appropriate to the server OS, WebSocket Protocol, Application Initialization, and .NET Framework 3.5 Features. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features) |
| official | configuration | A Rock web-farm gateway should enable session affinity so each client continues reaching the same web node, because check-in relies on session state. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/architect-a-server-cluster) |
| official | configuration | In Rock 19.0, adding a RockContextReadOnly connection string to web.ConnectionStrings.config allows Data Views and Reports to use a read-only database; an administrator can disable that context for an individual Data View when its filters or plugins need to write to the database. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context) |
| official | configuration | For Rock 19.0 on IIS, configure the application pool to use .NET Framework v4.0, start automatically, run as LocalSystem, disable idle timeout, and preload the website; schedule recycling for a specific low-traffic time instead of using regular recycling intervals. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis) |
| official | configuration | For Azure hosting, Rock recommends running the web and application server on a Windows virtual machine using IaaS and using Azure SQL as a managed PaaS database. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options) |
| official | configuration | Rock recommends enabling snapshot isolation on its SQL Server database so that database writes do not block reads; the setting may already be enabled depending on the SQL Server edition and version. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock) |
| official | configuration | Enable IIS dynamic-content compression when the option is available; if it is disabled because the required compression module is not installed, the step may be skipped. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis) |
| official | implementation_pattern | Rock's Azure hosting layout places the web virtual machine, Azure SQL server, and Azure SQL database in a shared resource group, with IIS running on the web VM. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting) |
| official | operational_guidance | Azure is a supported hosting path rather than a Rock requirement; organizations should choose among hosting options based on their scale, technical capacity, cost, and service quality needs. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) |
| official | operational_guidance | For a Rock 19.0 internal-hosting installation, use SQL Server's default instance unless the administrator is experienced with named instances, because the default instance simplifies subsequent Rock configuration. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server) |
| official | operational_guidance | Before implementing a requested screen, workflow or automation, restate the underlying problem and generate several genuinely distinct approaches. A stakeholder's proposed solution may be valuable requirements evidence without being the best implementation. | [source](https://www.youtube.com/watch?v=pvgZLvcfmFQ) |
| official | operational_guidance | Azure capacity planning should treat attendance-based tiers as starting points; organizations that also host their public website in Rock should select the next larger tier, while accounting for feature usage and workload intensity. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options) |
| official | operational_guidance | An organization that already has an Azure account should ask Microsoft Support to merge it with the nonprofit account so the nonprofit credit can be applied to the existing Azure setup. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit) |
| official | recipe | Before launching a SaaS-hosted Rock instance publicly, an organization should select a hosting partner, inventory its current system, arrange a kickoff, prepare a migration plan, and reserve a test period. | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting) |
| More |  | 14 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_core_release_notes`: 8
- `rock_documentation`: 21
- `rock_model_map`: 12
- `rock_podcast_rss`: 1
- `rock_qa`: 2
- `rock_recipes`: 12
- `rock_rocku`: 3
- `rock_youtube`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 11

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Azure Hosting | rock_documentation | [Intro to Azure Hosting](/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting?Version=v19.0) [Compare Sizing and Service Options](/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options?Version=v19.0) [Register for Credits as a Non-Profit](/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit?Version=v19.0) [Next Steps for... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting) |
| Internal Hosting | rock_documentation | [Intro to Internal Hosting](/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting?Version=v19.0) [Install Server Roles and Features](/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features?Version=v19.0) [Configure Internet Information Services... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting) |
| Intro to Azure Hosting | rock_documentation | The big factors in deciding where to host are cost and quality. Microsoft brings the best of both worlds to non-profits by offering a generous $2,000 annual Azure hosting credit. That's right, you can get premium hosting services with an industry-leading cloud provider at a significantly reduced rate. Depending on your organization's size and needs, your hosting costs might even be completely covered by the credit.... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) |
| Next Steps for Azure Hosting | rock_documentation | Whether or not you qualify for Microsoft's non-profit credit, your next steps will be about the same. Azure hosting includes Windows Server and Azure SQL Server, so you don’t need to worry about obtaining separate licenses. Once your account is set up with Azure, you're ready to start provisioning. # Provision Your Services First, create the *resource group* that you'll use to group all of your Rock services. A... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting) |
| Configure a Two-Server Environment | rock_documentation | If you were looking at the [system requirements](/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) in this guide's introduction, you might have noticed that there is a two-server configuration for larger installations. Even for smaller installations, we recommend two servers for the following reasons: * **Performance:** Having your Rock Database and Web Environment on separate... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment) |
| Configure SQL Server | rock_documentation | In this article, we'll start by setting up a user account for Rock to use to access the SQL Server. But before you begin creating users, it's important to understand the type of SQL Server environment you're working with: * **Azure SQL Database**: A fully managed database service where you interact with the database directly. To create users in Azure SQL Database, you'll need to use actual SQL commands in SSMS. We... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server) |
| Install SQL Server | rock_documentation | In this article, we will be installing SQL Server onto our Rock server. Let's begin.Start the SQL Server installer and on the first screen click on `New SQL Server stand-alone installation or add features to an existing installation`. On the next screen, agree to the license agreement and then click `Next`. Keep the *Include SQL Server Product Updates* checkbox checked and click `Next`. Next, the SQL installer will... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server) |
| Install Server Roles and Features | rock_documentation | In this section, we'll install the required server roles and features needed for Rock. Let’s open up `Start > Server Manager`. Once opened, the first thing we need to do is to install the Web Server role. That can be done by clicking on `Manage`and then `Add Roles and Features`. Click `Next`. On the next screen, select `Role-based or feature-based installation`. Choose `Select a server from the server pool` and then... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features) |
| Register for Credits as a Non-Profit | rock_documentation | So you've heard about Microsoft Azure's $2,000 annual hosting credit for non-profits, and you'd like to give it a try? Good news; those who have gone before you have marked the path to success. First, though, let's go over a few things we need to know up front. Note **How Do I Receive My Credit?**The $2,000 credit allows you to "spend" up to $167 per month with approved Azure products, and you'll be able to track... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit) |
| Intro to Internal Hosting | rock_documentation | Looking for information on how to host Rock internally? Well look no further. In this step-by-step guide we'll walk through the process of getting Rock up and running. Before we jump in, let's cover a few things to make sure we get started off on the right foot. In this section we will cover what you need for Rock to perform at its best. # System Requirements Rock was developed on Microsoft's ASP.Net platform so it... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) |
| Compare Sizing and Service Options | rock_documentation | How much power and space will you need for your Rock instance? It’s difficult to predict the perfect configuration. Fortunately, we have some suggestions based on our experience and the experiences shared with us by the Rock community. We've provided recommendations based on average attendance. It's important to note that while average attendance is a good starting point, it's often too simplistic of a measure to be... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options) |
| Intro to SaaS Hosting | rock_documentation | One of Rock’s core values is accessibility. From the beginning we’ve aimed to make Rock’s powerful technology available to every church regardless of size or technical resources. Rock hosting delivers on that vision by removing barriers that often prevent adoption and by making setup simple. With just a few clicks your church can be live and ready to use. ## What SaaS hosting is A fully managed cloud version of... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/saas-hosting/intro-to-saas-hosting) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Asset Storage Provider](../../model-map/models/asset-storage-provider.md) | Core | 19.2.0 | 42 | 14 | 27 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Web Farm Node](../../model-map/models/web-farm-node.md) | WebFarm | 19.2.0 | 50 | 20 | 35 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Web Farm Node Log](../../model-map/models/web-farm-node-log.md) | WebFarm | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Web Farm Node Metric](../../model-map/models/web-farm-node-metric.md) | WebFarm | 19.2.0 | 43 | 15 | 28 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.2.0 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.2.0 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.2.0 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.2.0 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 19.1 | Core | Added an automatic data migration that moves File Storage Provider settings from any existing legacy Azure Blob Storage provider plugin (Pillars) to the core Azure Blob Storage provider. This is required because the legacy provider can no longer upload large files due to library updates in v19. All settings are carried over, related File Types are updated,... | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | CMS | Fixed an error that occurred when editing a Content Channel Type with Attributes of type Image, File, or Binary File. The issue happened if the storage location was set to Azure Blob Storage or File System (or newly created FileType). This was resolved by setting a default CacheControlHeaderSettings value when new Binary File Types are created using the... | [source](https://www.rockrms.com/releasenotes) |
| 17.0 | Core | Improved database performance with new and revised indexes across multiple tables. These changes improve query efficiency for transactions, person records, group hierarchies, and interactions, based on SQL Server recommendations and other analysis. Key updates include new indexes on FinancialTransaction, enhanced indexing on Person and Group, and a... | [source](https://www.rockrms.com/releasenotes) |
| 18.1 | Core | Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #6524 | [source](https://www.rockrms.com/releasenotes) |
| 17.5 | Check-in | Fixed an issue where loading the Obsidian Attendance History block without person context could cause severe performance issues and possible server crashes by attempting to load all attendance records. The block now prevents loading attendance data when context is missing. Fixes: #6409 | [source](https://www.rockrms.com/releasenotes) |
| 17.1 | Check-in | Fixed a performance issue in Next-Gen Check-in that caused delays when printing to Bluetooth printers. The slowdown was due to how label image data was encoded, which has now been optimized. Printing performance should now be smooth and immediate. Fixes: #6260 | [source](https://www.rockrms.com/releasenotes) |
| 16.3 | Communication | Fixed issue where Communication Entry Wizard block becomes unusable when an SMS image attachment is auto-resized and uploaded to Azure Blob Storage. Fixes: #5719 | [source](https://www.rockrms.com/releasenotes) |
| 17.2 | Core | Improved the database index fill factor from 80% to 100% to reduce table size and improve maintenance performance. In the past, this was changed due to a common practice of reserving space to reduce page splits in the tables but, upon further research, it is an industry recommendation to fill the pages to 100% to reduce database footprint and improve... | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Sizing And Service Options

Keywords: `sizing, service options, compare sizing, hosting plan`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Azure Hosting | rock_documentation | [Intro to Azure Hosting](/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting?Version=v19.0) [Compare Sizing and Service Options](/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options?Version=v19.0) [Register for Credits as a Non-Profit](/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit?Version=v19.0) [Next Steps for... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting) |
| Internal Hosting | rock_documentation | [Intro to Internal Hosting](/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting?Version=v19.0) [Install Server Roles and Features](/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features?Version=v19.0) [Configure Internet Information Services... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting) |
| Intro to Azure Hosting | rock_documentation | The big factors in deciding where to host are cost and quality. Microsoft brings the best of both worlds to non-profits by offering a generous $2,000 annual Azure hosting credit. That's right, you can get premium hosting services with an industry-leading cloud provider at a significantly reduced rate. Depending on your organization's size and needs, your hosting costs might even be completely covered by the credit.... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) |
| Next Steps for Azure Hosting | rock_documentation | Whether or not you qualify for Microsoft's non-profit credit, your next steps will be about the same. Azure hosting includes Windows Server and Azure SQL Server, so you don’t need to worry about obtaining separate licenses. Once your account is set up with Azure, you're ready to start provisioning. # Provision Your Services First, create the *resource group* that you'll use to group all of your Rock services. A... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting) |
| Configure a Two-Server Environment | rock_documentation | If you were looking at the [system requirements](/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) in this guide's introduction, you might have noticed that there is a two-server configuration for larger installations. Even for smaller installations, we recommend two servers for the following reasons: * **Performance:** Having your Rock Database and Web Environment on separate... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment) |
| Configure SQL Server | rock_documentation | In this article, we'll start by setting up a user account for Rock to use to access the SQL Server. But before you begin creating users, it's important to understand the type of SQL Server environment you're working with: * **Azure SQL Database**: A fully managed database service where you interact with the database directly. To create users in Azure SQL Database, you'll need to use actual SQL commands in SSMS. We... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-sql-server) |
| Install SQL Server | rock_documentation | In this article, we will be installing SQL Server onto our Rock server. Let's begin.Start the SQL Server installer and on the first screen click on `New SQL Server stand-alone installation or add features to an existing installation`. On the next screen, agree to the license agreement and then click `Next`. Keep the *Include SQL Server Product Updates* checkbox checked and click `Next`. Next, the SQL installer will... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-sql-server) |
| Install Server Roles and Features | rock_documentation | In this section, we'll install the required server roles and features needed for Rock. Let’s open up `Start > Server Manager`. Once opened, the first thing we need to do is to install the Web Server role. That can be done by clicking on `Manage`and then `Add Roles and Features`. Click `Next`. On the next screen, select `Role-based or feature-based installation`. Choose `Select a server from the server pool` and then... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-server-roles-and-features) |
| Register for Credits as a Non-Profit | rock_documentation | So you've heard about Microsoft Azure's $2,000 annual hosting credit for non-profits, and you'd like to give it a try? Good news; those who have gone before you have marked the path to success. First, though, let's go over a few things we need to know up front. Note **How Do I Receive My Credit?**The $2,000 credit allows you to "spend" up to $167 per month with approved Azure products, and you'll be able to track... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit) |
| Intro to Internal Hosting | rock_documentation | Looking for information on how to host Rock internally? Well look no further. In this step-by-step guide we'll walk through the process of getting Rock up and running. Before we jump in, let's cover a few things to make sure we get started off on the right foot. In this section we will cover what you need for Rock to perform at its best. # System Requirements Rock was developed on Microsoft's ASP.Net platform so it... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) |

### Azure Hosting

Keywords: `azure, app service, sql database, storage account`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Azure Hosting | rock_documentation | [Intro to Azure Hosting](/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting?Version=v19.0) [Compare Sizing and Service Options](/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options?Version=v19.0) [Register for Credits as a Non-Profit](/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit?Version=v19.0) [Next Steps for... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting) |
| Intro to Azure Hosting | rock_documentation | The big factors in deciding where to host are cost and quality. Microsoft brings the best of both worlds to non-profits by offering a generous $2,000 annual Azure hosting credit. That's right, you can get premium hosting services with an industry-leading cloud provider at a significantly reduced rate. Depending on your organization's size and needs, your hosting costs might even be completely covered by the credit.... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/intro-to-azure-hosting) |
| Next Steps for Azure Hosting | rock_documentation | Whether or not you qualify for Microsoft's non-profit credit, your next steps will be about the same. Azure hosting includes Windows Server and Azure SQL Server, so you don’t need to worry about obtaining separate licenses. Once your account is set up with Azure, you're ready to start provisioning. # Provision Your Services First, create the *resource group* that you'll use to group all of your Rock services. A... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/next-steps-for-azure-hosting) |
| Register for Credits as a Non-Profit | rock_documentation | So you've heard about Microsoft Azure's $2,000 annual hosting credit for non-profits, and you'd like to give it a try? Good news; those who have gone before you have marked the path to success. First, though, let's go over a few things we need to know up front. Note **How Do I Receive My Credit?**The $2,000 credit allows you to "spend" up to $167 per month with approved Azure products, and you'll be able to track... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/register-for-credits-as-a-non-profit) |
| Compare Sizing and Service Options | rock_documentation | How much power and space will you need for your Rock instance? It’s difficult to predict the perfect configuration. Fortunately, we have some suggestions based on our experience and the experiences shared with us by the Rock community. We've provided recommendations based on average attendance. It's important to note that while average attendance is a good starting point, it's often too simplistic of a measure to be... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting/compare-sizing-and-service-options) |

### Operational Readiness

Keywords: `backup, ssl, smtp, storage, performance, readiness`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Workflow Performance Tips Transcript Insight | Rock operations | 00:00 | The Workflow Performance Tips RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/workflows/workflow-performance-tips) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Configure a Two-Server Environment | rock_documentation | If you were looking at the [system requirements](/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) in this guide's introduction, you might have noticed that there is a two-server configuration for larger installations. Even for smaller installations, we recommend two servers for the following reasons: * **Performance:** Having your Rock Database and Web Environment on separate... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-a-two-server-environment) |
| Intro to Internal Hosting | rock_documentation | Looking for information on how to host Rock internally? Well look no further. In this step-by-step guide we'll walk through the process of getting Rock up and running. Before we jump in, let's cover a few things to make sure we get started off on the right foot. In this section we will cover what you need for Rock to perform at its best. # System Requirements Rock was developed on Microsoft's ASP.Net platform so it... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/intro-to-internal-hosting) |
| Configure Your Rock Context | rock_documentation | Some organizations may find that it's worthwhile to maintain a separate database for Rock that's only used for reading (and not writing) data. A read-only database gives people a place to go besides your primary database, helping to lighten the load on that database. You may already have a database for this purpose. Any Azure customer using a Business Critical or Premium SQL tier is automatically provided with a... | [source](https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context) |
| How to get a Free SSL Certificate on your Windows Server | rock_recipes | 0 How to get a Free SSL Certificate on your Windows Server Shared by Nathan Parikh , Hallmark Church 6 years ago 7.0 General, Web Advanced SSL certificates are a necessity, and if you take a few minutes you can have one for free thanks to LetsEncrypt and CertifyTheWeb . Note: We use an Azure VM for our Rock server, and Cloudflare for our DNS, but these steps should still apply to most setups where you have an admin... | [source](https://community.rockrms.com/recipes/66) |
| Skills Rubric | triumph_resources | Level 1: Foundational Awareness Basic understanding and vocabulary; competently follows guidance of experienced team members. Understands the core components of Azure (VMs, SQL, Resource Groups, Networking). Can follow step-by-step documentation to create or configure basic Azure resources (e.g., create VM, attach disk). Follows all Triumph’s Azure naming conventions and resource group structure. Can navigate the... | [source](https://www.triumph.tech/resources/skills-rubric) |
| AWS SES Email SMTP Transport for RockRMS | rock_recipes | 1 AWS SES Email SMTP Transport for RockRMS Shared by Ben Murphy , Harvest Bible Chapel Pittsburgh North 6 years ago Communications, General Intermediate Setting up Customer Engagement: Amazon Simple Email Service (SES) with the RockRMS SMTP Transport Amazon Simple Email Service (SES) is a free SMTP mail delivery service that also falls into the free tier if you are hosting your RockRMS environment on Amazon's AWS... | [source](https://community.rockrms.com/recipes/171) |
| Rock Core Release Notes | rock_core_release_notes | Added an automatic data migration that moves File Storage Provider settings from any existing legacy Azure Blob Storage provider plugin (Pillars) to the core Azure Blob Storage provider. This is required because the legacy provider can no longer upload large files due to library updates in v19. All settings are carried over, related File Types are updated,... | [source](https://www.rockrms.com/releasenotes) |
| How to Maintain your Azure SQL Database | rock_recipes | 5 How to Maintain your Azure SQL Database Shared by Brent Pirolli , CedarCreek Church 4 years ago Administration / Finance, General Intermediate How to Maintain your Azure SQL Database Maintaining your SQL database can be crucial to the performance of your Rock install. Rock's "Database Maintenance" job runs nightly and is set to cover most of what you need. But, there are further times you can and should take... | [source](https://community.rockrms.com/recipes/259) |
| Get Notified of ACME SSL Certificate Renewal | rock_recipes | 4 Get Notified of ACME SSL Certificate Renewal Shared by Victor Garcia , Pillars 4 years ago 11.0 Operations Beginner If you are using Protect My Ministry or Active Screening, this will be a helpful tool in automatically notifying them when your SSL certificate gets renewed! Get set up to receive a notification whenever an SSL certificate is automatically renewed with these few steps: 1. First, run the following SQL... | [source](https://community.rockrms.com/recipes/263) |


## Rebuild Dependencies

- Source records: `72`
- Approved claims: `32`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
