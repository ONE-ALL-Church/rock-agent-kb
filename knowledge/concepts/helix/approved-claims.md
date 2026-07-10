---
concept_id: helix
generated: true
artifact_level: claim_graph
approved_claim_count: 15
---

# Helix Approved Claims

This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.

| Claim ID | Authority | Type | Claim | Source |
| --- | --- | --- | --- | --- |
| `claim:2a7f5e6781a2d2fa30a4` | official | behavior | Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms' single-page form model, which matters when validating or troubleshooting nested form behavior. | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| `claim:399553446fce014cb4bf` | official | behavior | In Rock 19 and later, Helix Lava endpoints expose request content through Body and RawBody merge fields; Body converts JSON or XML into objects, RawBody preserves the original string, and neither field supplies a body for GET requests. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| `claim:9b7c0c788640e9ade1e9` | official | behavior | Each Helix Lava Endpoint call creates an observability activity whose name identifies both the endpoint and its Lava Application; the root activity also records their names as attributes, while the HTTP method is available through an existing activity attribute. | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| `claim:1ab863013d2610a31c7d` | official | configuration | In Rock 18 or later, Helix loading indicators can reference spinner assets under `/Assets/Images/Spinners/`; installations using the Helix plugin instead use `/Plugins/tech_triumph/LavaHelix/Assets/Spinners/`. | [source](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| `claim:d35ed98aadeaabd2cf1e` | official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| `claim:7714f93d21d6594b978d` | official | implementation_pattern | The Magnus plugin supports editing Lava Applications and their endpoints in Visual Studio Code, allowing linked front-end content blocks and back-end endpoints to be managed together during application development. | [source](https://community.rockrms.com/developer/helix/lava-applications/magnus) |
| `claim:c5503c9cb23c6cca98d4` | official | implementation_pattern | A Helix form can display a form-level HTMX loading indicator by placing an element with the `htmx-indicator` class inside the form and setting the submitting control's `hx-indicator` attribute to target that form. | [source](https://community.rockrms.com/developer/helix/forms-controls/loading-indicator) |
| `claim:fa508a4851ef572dee65` | official | implementation_pattern | A Helix Lava Application groups server-side endpoints that return HTML fragments, and each endpoint is addressed by a route composed from the application slug and endpoint slug; endpoints may share that route when they use different HTTP methods. | [source](https://community.rockrms.com/developer/helix/lava-applications) |
| `claim:3f3dca6b455e9c9ed915` | official | operational_guidance | When developing Helix Lava Applications, monitor endpoint observability data to identify inefficient execution and excessive database calls. | [source](https://community.rockrms.com/developer/helix/lava-applications/observability) |
| `claim:6cccc1a4cde68921fa28` | official | operational_guidance | Consider replacing a Helix Lava Application with a purpose-built custom solution if it would require custom models, at least 50 endpoints, or has become difficult and fragile to develop. | [source](https://community.rockrms.com/developer/helix/overview/customizing-rock) |
| `claim:ecb2447933839fcdfb1b` | official | operational_guidance | For readable Helix HTMX markup, place each HTML attribute on its own line and list the CSS class attribute first. | [source](https://community.rockrms.com/developer/helix/htmx/syntax-style-guides) |
| `claim:b297afe1c2b0a341ed44` | official | release_caveat | Lava javascript and stylesheet commands do not function in Helix endpoint templates because endpoint output is injected into the page by JavaScript, which prevents reliable detection of resources already present on the page. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| `claim:c707a9d9cd2878d9e056` | official | release_caveat | Helix does not support the Lava javascript and stylesheet commands because they depend on RockPage, which is unavailable when Helix dynamically replaces page regions. | [source](https://community.rockrms.com/developer/helix/strategies/limitations) |
| `claim:da56681f6277c12df324` | official | risk | Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| `claim:940f299b268510da61d8` | official | source_summary | Helix is a Rock web-development surface that combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. | [source](https://community.rockrms.com/developer/helix/overview) |
