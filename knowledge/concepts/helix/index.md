---
id: concept-helix
title: Helix
generated: true
last_built: 2026-07-26T00:28:42+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - lava
  - api-integrations
  - security
  - cms
  - workflows
  - forms
  - htmx
  - observability
---

# Helix

Helix, HTMX, Lava Applications, Lava Endpoints, Lava Application Content blocks, forms and controls, endpoint security, observability, and production-readiness caveats.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Helix` spans lava, api-integrations, security, cms, workflows, forms. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_developer, rock_documentation, rock_recipes, rock_core_release_notes, rock_model_map, rock_lava_docs.
- Related tags found in source records: development, lava, cms, workflow, api, obsidian, security, sql.
- Source detail types include: developer_doc, documentation_article, recipe, rock_community_site, rock_lava_docs, triumph_resources.

## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms' single-page form model, which matters when validating or troubleshooting nested form behavior. | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| official | behavior | In Rock 19 and later, Helix Lava endpoints expose request content through Body and RawBody merge fields; Body converts JSON or XML into objects, RawBody preserves the original string, and neither field supplies a body for GET requests. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | behavior | Each Helix Lava Endpoint call creates an observability activity whose name identifies both the endpoint and its Lava Application; the root activity also records their names as attributes, while the HTTP method is available through an existing activity attribute. | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| official | configuration | In Rock 18 or later, Helix loading indicators can reference spinner assets under `/Assets/Images/Spinners/`; installations using the Helix plugin instead use `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/`. | [source](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | implementation_pattern | The Magnus plugin supports editing Lava Applications and their endpoints in Visual Studio Code, allowing linked front-end content blocks and back-end endpoints to be managed together during application development. | [source](https://community.rockrms.com/developer/helix/lava-applications/magnus) |
| official | implementation_pattern | A Helix form can display a form-level HTMX loading indicator by placing an element with the `htmx-indicator` class inside the form and setting the submitting control's `hx-indicator` attribute to target that form. | [source](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| official | implementation_pattern | The Lava Application Content block automatically registers HTMX, and its templates can call an application endpoint with `^/application-slug/endpoint-slug` instead of hard-coding the full `/api/v2/lava-app/1/...` route. | [source](https://community.rockrms.com/developer/helix/lava-applications/content-block) |
| official | implementation_pattern | A Helix Lava Application groups server-side endpoints that return HTML fragments, and each endpoint is addressed by a route composed from the application slug and endpoint slug; endpoints may share that route when they use different HTTP methods. | [source](https://community.rockrms.com/developer/helix/lava-applications) |
| official | operational_guidance | When developing Helix Lava Applications, monitor endpoint observability data to identify inefficient execution and excessive database calls. | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| official | operational_guidance | Consider replacing a Helix Lava Application with a purpose-built custom solution if it would require custom models, at least 50 endpoints, or has become difficult and fragile to develop. | [source](https://community.rockrms.com/developer/helix/overview/customizing-rock) |
| official | operational_guidance | For readable Helix HTMX markup, place each HTML attribute on its own line and list the CSS class attribute first. | [source](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides) |
| official | release_caveat | Lava javascript and stylesheet commands do not function in Helix endpoint templates because endpoint output is injected into the page by JavaScript, which prevents reliable detection of resources already present on the page. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| official | release_caveat | Helix does not support the Lava javascript and stylesheet commands because they depend on RockPage, which is unavailable when Helix dynamically replaces page regions. | [source](https://community.rockrms.com/developer/helix/strategies/limitations) |
| official | risk | Treat every Helix endpoint as directly callable outside its front end: validate all inputs, enforce the caller's view or edit rights, avoid GET for mutations, and sanitize query and body values before SQL use. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| official | risk | Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| official | source_summary | Helix is a Rock web-development surface that combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. | [source](https://community.rockrms.com/developer/helix/overview) |

## Source Coverage

- `public_rock_repos`: 1
- `rock_community_site`: 1
- `rock_core_release_notes`: 3
- `rock_developer`: 27
- `rock_documentation`: 4
- `rock_lava_docs`: 39
- `rock_model_map`: 12
- `rock_recipes`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Overview | rock_developer | Helix is the codename for an upcoming project that represents the next evolution of Lava for web development, integrating four distinct technologies. * [HTMX](/documentation/helix/overview#htmx) * [Lava Applications](/documentation/helix/overview#lava-applications) * [Lava Commands](/documentation/helix/overview#lava-commands) * [Control Shortcodes](/documentation/helix/overview#control-shortcodes) Important Before... | [source](https://community.rockrms.com/developer/helix/overview) |
| Observability | rock_developer | We expect our applications to be fast. Embracing the principle of "inspect what you expect," we've integrated observability into each Lava Endpoint call. Activities for each endpoint are named using the pattern: `LavaEndpoint: {LavaEndpoint.Name} \| {LavaEndpoint.LavaApplication.Name}`. Additionally, we add the following attributes to the root activity: * rock.lava\_endpoint: the name of the endpoint. *... | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| Magnus | rock_developer | Lava Applications and Magnus are a perfect match. You can easily edit your applications and endpoints right in VS Code. Since content blocks can link to an application, we can group front-end content blocks with back-end endpoints, simplifying application development. See the [Magnus homepage](https://www.triumph.tech/magnus) on the Triumph site for more information on installing and configuring this plugin. | [source](https://community.rockrms.com/developer/helix/lava-applications/magnus) |
| Learning More | rock_developer | Want to go deeper on HTMX? The [HTMX website](https://www.htmx.org/) provides a much deeper understanding of what's passible. There's also two ebooks you can check-out. ## Examples The best way to understand is to see it in action. Triumph has created a small gallery of simple examples for you to see the power and jumpstart you on your way to implementing HTMX yourself. If you know of any other HTMX galleries for... | [source](https://community.rockrms.com/developer/helix/htmx/learning-more) |
| Forms & Controls | rock_developer | [Understanding Forms](/documentation/helix/forms-controls/understanding-forms) [Using Form Controls](/documentation/helix/forms-controls/using-form-controls) [Creating New Controls](/documentation/helix/forms-controls/creating-new-controls) [Form Validation](/documentation/helix/forms-controls/form-validation) [Loading Indicator](/documentation/helix/forms-controls/loading-indicator) | [source](https://community.rockrms.com/developer/helix/forms-controls) |
| Lava Applications | rock_developer | HTMX empowers you to build responsive and dynamic applications by creating server-side endpoints that return HTML snippets. Managing multiple endpoints is common, even in basic applications. To simplify this, we introduced Lava Applications, which consist of two key components: the Application and its Endpoints. Below is a diagram of a very basic Lava Application: The example showcases an application with five... | [source](https://community.rockrms.com/developer/helix/lava-applications) |
| Content Block | rock_developer | With your application and endpoints ready you're pretty much set on the backend. While you can technically call the backend from any webpage by importing the HTMX library yourself, we highly recommend using the provided Lava Application Content block on the front-end. This block automatically registers HTMX for you and provides convenience features and styling. Below are the block settings for the Lava Application... | [source](https://community.rockrms.com/developer/helix/lava-applications/content-block) |
| HTMX | rock_developer | [Learning More](/documentation/helix/htmx/learning-more) [Syntax Style Guides](/documentation/helix/htmx/syntax-style-guides) | [source](https://community.rockrms.com/developer/helix/htmx) |
| 🧬 Helix | rock_developer | Redefine the boundaries of what you believed possible with Lava. ** Dynamic Content without the Need for JavaScript** Infuse your web pages with live content updates using Lava, bypassing the complexity of JavaScript. [HTMX](/documentation/helix/htmx) ** Elevate Lava Beyond Reading to Updating Data** Transform Lava into a powerful tool that not only reads but also updates data seamlessly within your applications.... | [source](https://community.rockrms.com/developer/helix) |
| Customizing Rock | rock_developer | There are several levels of customization available for your Rock instance, described below in basic categories. While it might seem desirable to aim for the highest level, it's often better to aim lower. Each new level, while offering more power and capabilities, also introduces greater complexity and increased support costs. We advise staying as low on the pyramid as possible. Lava Applications provide enhanced... | [source](https://community.rockrms.com/developer/helix/overview/customizing-rock) |
| Applications | rock_developer | Configuring a Lava Application is quite straightforward. Below is a screenshot of the editing panel. Below are the properties that are required: * **Name** - A friendly name for you to keep your applications organized. * **Description** - To serve as a place for some documentation about your application. * **Slug** - Helps to tell HTMX what application to use (in the example above the application slug is... | [source](https://community.rockrms.com/developer/helix/lava-applications/applications) |
| Loading Indicator | rock_developer | HTMX has a sophisticated and well considered loading indicator pattern. See their documentation for all of the details. Below are a couple of prebuilt patterns to help you get started. Note The image paths below are for when using Helix with Rock v18 or later. If you are using the plugin version of Helix, the paths will be `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/...` ## Adding Indicator To Buttons One great... | [source](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Lava Application](../../model-map/models/lava-application.md) | CMS | 19.2.0 | 44 | 16 | 29 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Lava Endpoint](../../model-map/models/lava-endpoint.md) | CMS | 19.2.0 | 52 | 23 | 36 | 13 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.2.0 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.2.0 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.2.0 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.2.0 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Association](../../model-map/models/content-channel-item-association.md) | CMS | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item Slug](../../model-map/models/content-channel-item-slug.md) | CMS | 19.2.0 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Type](../../model-map/models/content-channel-type.md) | CMS | 19.2.0 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

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
| 18.1 | CMS | Added Helix support for Lava Applications to core. This provides a great new way to build interactive pages in Rock powered by Lava for more advanced administrators. | [source](https://www.rockrms.com/releasenotes) |
| 19.1 | Lava | Added Body and RawBody merge fields to Lava Applications. | [source](https://www.rockrms.com/releasenotes) |
| 16.4 | Core | Updated the Save button in Obsidian Detail blocks to show a loading indicator while waiting for the data to be saved. Fixes: #5661 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| Triumph-Tech/magnus-vscode | TypeScript | github search: "Rock RMS" in:name,description,readme | [source](https://github.com/Triumph-Tech/magnus-vscode) |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Overview And Roadmap

Keywords: `helix, overview, roadmap, customizing rock, plugin installation, faq`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Overview | rock_developer | Helix is the codename for an upcoming project that represents the next evolution of Lava for web development, integrating four distinct technologies. * [HTMX](/documentation/helix/overview#htmx) * [Lava Applications](/documentation/helix/overview#lava-applications) * [Lava Commands](/documentation/helix/overview#lava-commands) * [Control Shortcodes](/documentation/helix/overview#control-shortcodes) Important Before... | [source](https://community.rockrms.com/developer/helix/overview) |
| Customizing Rock | rock_developer | There are several levels of customization available for your Rock instance, described below in basic categories. While it might seem desirable to aim for the highest level, it's often better to aim lower. Each new level, while offering more power and capabilities, also introduces greater complexity and increased support costs. We advise staying as low on the pyramid as possible. Lava Applications provide enhanced... | [source](https://community.rockrms.com/developer/helix/overview/customizing-rock) |
| FAQ | rock_developer | Here you'll find a comprehensive list of frequently asked questions about the Helix project, accompanied by detailed answers. **Why is Helix not a part of core?** ~~Helix is a R&D project by Triumph Tech. Only Spark Development Network can decide to put code into core.~~ It is now in core! **Is Helix available in Rock Mobile?** We like the way you think! Helix would be very powerful if it was a part of Rock Mobile.... | [source](https://community.rockrms.com/developer/helix/overview/faq) |
| Plugin Installation | rock_developer | **Helix Is Currently in Limited Beta** With great power comes a great amount of testing. Helix is currently being tested by a few select organizations. Keep checking back for the latest details. Helix operates seamlessly with the aid of two complimentary plugins, both freely available. Simply navigate to the Rock Shop to install the following: 1. Helix Plugin - This is the main plugin that contains all of the logic... | [source](https://community.rockrms.com/developer/helix/overview/plugin-installation) |
| Security | rock_developer | We can't stress enough the importance of considering security when using Helix tools. ## Points to Consider Here are some key points to keep in mind when building Helix applications. Warning Application security covers a wide range of topics. While it's impossible to document every safeguard, this list provides an overview of the major considerations you should keep in mind. 1. Remember that your endpoints might be... | [source](https://community.rockrms.com/developer/helix/overview/security) |
| Roadmap | rock_developer | We're just getting started with Helix. There a lot of plans and thoughts in the future. Below is just the beginning of what we're considering. Note These are just ideas. Some may not see the light of day. 1. More recipes and how-tos. 2. Additional form controls. 3. Simplify advanced concepts like annimation and drag-drop. 4. Provide a toast framework. 5. Potential use-cases for Rock's Real-time Engine. 6. Support... | [source](https://community.rockrms.com/developer/helix/overview/roadmap) |

### HTMX

Keywords: `htmx, syntax, style guide, hx-get, hx-post, hx-target`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Learning More | rock_developer | Want to go deeper on HTMX? The [HTMX website](https://www.htmx.org/) provides a much deeper understanding of what's passible. There's also two ebooks you can check-out. ## Examples The best way to understand is to see it in action. Triumph has created a small gallery of simple examples for you to see the power and jumpstart you on your way to implementing HTMX yourself. If you know of any other HTMX galleries for... | [source](https://community.rockrms.com/developer/helix/htmx/learning-more) |
| HTMX | rock_developer | [Learning More](/documentation/helix/htmx/learning-more) [Syntax Style Guides](/documentation/helix/htmx/syntax-style-guides) | [source](https://community.rockrms.com/developer/helix/htmx) |
| Syntax Style Guides | rock_developer | They say if you're going to do something, do it with style—and we believe that applies to coding as well. HTMX's strength lies in its preference for attributes over coding, though this can be a bit overwhelming at first. To enhance readability, we recommend adopting the following syntax style. ``` <a class="btn btn-primary btn-xs" hx-post="^/cato/link-client?ClientGuid={{ client.Guid }}&OrganizationGuid={{... | [source](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides) |

### Lava Applications

Keywords: `lava application, lava applications, application slug, configuration, lava application content block`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Observability | rock_developer | We expect our applications to be fast. Embracing the principle of "inspect what you expect," we've integrated observability into each Lava Endpoint call. Activities for each endpoint are named using the pattern: `LavaEndpoint: {LavaEndpoint.Name} \| {LavaEndpoint.LavaApplication.Name}`. Additionally, we add the following attributes to the root activity: * rock.lava\_endpoint: the name of the endpoint. *... | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| Magnus | rock_developer | Lava Applications and Magnus are a perfect match. You can easily edit your applications and endpoints right in VS Code. Since content blocks can link to an application, we can group front-end content blocks with back-end endpoints, simplifying application development. See the [Magnus homepage](https://www.triumph.tech/magnus) on the Triumph site for more information on installing and configuring this plugin. | [source](https://community.rockrms.com/developer/helix/lava-applications/magnus) |
| Lava Applications | rock_developer | HTMX empowers you to build responsive and dynamic applications by creating server-side endpoints that return HTML snippets. Managing multiple endpoints is common, even in basic applications. To simplify this, we introduced Lava Applications, which consist of two key components: the Application and its Endpoints. Below is a diagram of a very basic Lava Application: The example showcases an application with five... | [source](https://community.rockrms.com/developer/helix/lava-applications) |
| Content Block | rock_developer | With your application and endpoints ready you're pretty much set on the backend. While you can technically call the backend from any webpage by importing the HTMX library yourself, we highly recommend using the provided Lava Application Content block on the front-end. This block automatically registers HTMX for you and provides convenience features and styling. Below are the block settings for the Lava Application... | [source](https://community.rockrms.com/developer/helix/lava-applications/content-block) |
| Applications | rock_developer | Configuring a Lava Application is quite straightforward. Below is a screenshot of the editing panel. Below are the properties that are required: * **Name** - A friendly name for you to keep your applications organized. * **Description** - To serve as a place for some documentation about your application. * **Slug** - Helps to tell HTMX what application to use (in the example above the application slug is... | [source](https://community.rockrms.com/developer/helix/lava-applications/applications) |
| Endpoints | rock_developer | Endpoints are the fundamental units of work for your applications, encapsulating the logic called from the client. Below is the editing panel for an endpoint. Each of the properties of the endpoint are described in more detail below: * **Name** - A friendly name for you to keep your applications organized * **Description** - To serve as a place for some documentation about your application. * **Slug** - Helps to... | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |

### Lava Endpoints

Keywords: `lava endpoint, lava endpoints, endpoint slug, http method, security mode, rate limit, cache`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Endpoints | rock_developer | Endpoints are the fundamental units of work for your applications, encapsulating the logic called from the client. Below is the editing panel for an endpoint. Each of the properties of the endpoint are described in more detail below: * **Name** - A friendly name for you to keep your applications organized * **Description** - To serve as a place for some documentation about your application. * **Slug** - Helps to... | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |

### Forms And Controls

Keywords: `form, forms, control, controls, form validation, loading indicator, using form controls, creating new controls`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Forms & Controls | rock_developer | [Understanding Forms](/documentation/helix/forms-controls/understanding-forms) [Using Form Controls](/documentation/helix/forms-controls/using-form-controls) [Creating New Controls](/documentation/helix/forms-controls/creating-new-controls) [Form Validation](/documentation/helix/forms-controls/form-validation) [Loading Indicator](/documentation/helix/forms-controls/loading-indicator) | [source](https://community.rockrms.com/developer/helix/forms-controls) |
| Loading Indicator | rock_developer | HTMX has a sophisticated and well considered loading indicator pattern. See their documentation for all of the details. Below are a couple of prebuilt patterns to help you get started. Note The image paths below are for when using Helix with Rock v18 or later. If you are using the plugin version of Helix, the paths will be `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/...` ## Adding Indicator To Buttons One great... | [source](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| Form Validation | rock_developer | The form validation logic below only works for inputs that are placed within `<lava-form>` tags. Warning This page covers client-side validation, but it's critical to also validate input on the server side. This ensures security even if your endpoints are accessed directly. Note Form validation only applies to POST, PUT and DELETE calls. Validation is not processed on GET requests. ## Validation Convention... | [source](https://community.rockrms.com/developer/helix/forms-controls/form-validation) |
| Understanding Forms | rock_developer | HTMX, and HTML in general, assume that forms are independent units and that a page may contain multiple forms. However, ASP.Net, specifically WebForms, operates with a single form that encompasses the entire page. Understanding this distinction is crucial to avoid issues with nested forms. When working with forms for validation we've added the concept of a 'Lava Form'. These forms are independent and make up for the... | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| Creating New Controls | rock_developer | Lava shortcodes, acting as controls, streamline the process of rendering form elements, making them more efficient to use. Note When considering creating new controls, evaluate whether they're broadly applicable or specific to your project. If you believe a control could benefit the toolkit, let's collaborate. We can either integrate it directly or assist you in submitting a pull request. ## Patterns Most new... | [source](https://community.rockrms.com/developer/helix/forms-controls/creating-new-controls) |
| Using Form Controls | rock_developer | To simplify the process of designing forms we've created a set of Lava shortcodes for common types of form fields. To create a simple textbox in Rock you'd normally have to provide the following markup: ``` <div class="form-group rock-text-box required"> <label class="control-label" for="rc-ab5633b7-2a1f-41b6-b346-cb48679ae68d">Last Name</label> <div class="control-wrapper"> <input name="lastname" type="text"... | [source](https://community.rockrms.com/developer/helix/forms-controls/using-form-controls) |

### Security And Observability

Keywords: `security, endpoint security, validate input, idkey, guid, observability, traces, database calls`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Observability | rock_developer | We expect our applications to be fast. Embracing the principle of "inspect what you expect," we've integrated observability into each Lava Endpoint call. Activities for each endpoint are named using the pattern: `LavaEndpoint: {LavaEndpoint.Name} \| {LavaEndpoint.LavaApplication.Name}`. Additionally, we add the following attributes to the root activity: * rock.lava\_endpoint: the name of the endpoint. *... | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| Security | rock_developer | We can't stress enough the importance of considering security when using Helix tools. ## Points to Consider Here are some key points to keep in mind when building Helix applications. Warning Application security covers a wide range of topics. While it's impossible to document every safeguard, this list provides an overview of the major considerations you should keep in mind. 1. Remember that your endpoints might be... | [source](https://community.rockrms.com/developer/helix/overview/security) |

### Strategies And Limitations

Keywords: `strategy, strategies, tips, related entities, limitations, rockpage`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Strategies | rock_developer | [Tips](/documentation/helix/strategies/tips) [Related Entities](/documentation/helix/strategies/related-entities) [Limitations](/documentation/helix/strategies/limitations) | [source](https://community.rockrms.com/developer/helix/strategies) |
| Limitations | rock_developer | While we've worked to make Lava and Rock compatible with Helix, there are some limitations: 1. Lava Commands That Require RockPage - The `{% javascript %}` and `{% stylesheet %}` commands won’t work with Helix. These commands rely on RockPage to execute and render their markup. Since Helix dynamically updates portions of the page, RockPage isn’t available in those cases. | [source](https://community.rockrms.com/developer/helix/strategies/limitations) |
| Tips | rock_developer | Below are some tips we've gathered from our experience rolling out Helix in our work. 1. Browser Dev Tools - Something not working? Be sure to check the JavaScript console in your browser's Dev Tools. Often times you'll have the `hx-target` or some other configuration wrong and you'll find a helpful tip in the console. 2. Inheritance - Many attributes in HTMX can be inherited from parent elements, which is a... | [source](https://community.rockrms.com/developer/helix/strategies/tips) |
| Related Entities | rock_developer | Warning Writing in progress! We will talk about the power of this hidden gem. | [source](https://community.rockrms.com/developer/helix/strategies/related-entities) |


## Lava Capability References

This concept depends on the generated Lava capability layer. Agents should use the stable guidance first, then verify syntax and behavior against the official source and the live Rock instance.

- Reference index: [../lava/lava-reference-index.md](../lava/lava-reference-index.md)
- Safety matrix: [../lava/lava-safety-matrix.md](../lava/lava-safety-matrix.md)
- Agent usage examples: [../lava/lava-agent-usage-examples.md](../lava/lava-agent-usage-examples.md)
- Machine-readable rows: [agent/lava-capabilities.jsonl](../../../agent/lava-capabilities.jsonl)

## Rebuild Dependencies

- Source records: `104`
- Lava capability source records: `53`
- Approved claims: `17`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
