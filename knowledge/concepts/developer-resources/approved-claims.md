---
concept_id: developer-resources
generated: true
artifact_level: claim_graph
approved_claim_count: 13
---

# Rock Developer Resources Approved Claims

This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.

| Claim ID | Authority | Type | Claim | Source |
| --- | --- | --- | --- | --- |
| `claim:2a7f5e6781a2d2fa30a4` | official | behavior | Helix Lava Forms address the mismatch between independent HTML forms and ASP.NET WebForms' single-page form model, which matters when validating or troubleshooting nested form behavior. | [source](https://community.rockrms.com/developer/helix/forms-controls/understanding-forms) |
| `claim:d35ed98aadeaabd2cf1e` | official | configuration | Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. | [source](https://community.rockrms.com/developer/helix/lava-applications/endpoints) |
| `claim:29f4e0bbc81c08861367` | official | implementation_pattern | Rock Apple TV documentation groups JavaScript command behavior as a core part of building TV applications, so TV app guidance should treat commands as part of navigation, media, utility, and demo workflows. | [source](https://community.rockrms.com/developer/apple-tv-docs/javascript) |
| `claim:855f7a33bcc8bb936067` | official | implementation_pattern | An Obsidian block combines a C# block, a TypeScript component, and block actions, so developer guidance should connect server logic, client UI, and action endpoints instead of treating a block as one file. | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| `claim:9398f3fb18e8a79c0e4d` | official | implementation_pattern | Roku commands are executed by setting a rockCommand and command-specific parameters on supported controls, and multiple commands can be chained by separating command names with commas. | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| `claim:ee2f4e5a371c3b243567` | official | implementation_pattern | The Lava Application Content block automatically registers HTMX, and its templates can call an application endpoint with `^/application-slug/endpoint-slug` instead of hard-coding the full `/api/v2/lava-app/1/...` route. | [source](https://community.rockrms.com/developer/helix/lava-applications/content-block) |
| `claim:6ae226ddf1e1e1df52ed` | official | operational_guidance | Rock plugin and theme packaging guidance frames the Rock Shop as the distribution path for community extensions, so plugin work should include packaging, review, and uninstall behavior rather than only local code changes. | [source](https://community.rockrms.com/developer/packaging-plugins-themes) |
| `claim:da56681f6277c12df324` | official | risk | Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. | [source](https://community.rockrms.com/developer/helix/overview/security) |
| `claim:5416735ea289965714bf` | official | source_summary | Rock's Obsidian documentation is primarily written for the core developer team, but some sections such as Grids are published for broader public reading and require judgment when translating them to plugin development. | [source](https://community.rockrms.com/developer/obsidian) |
| `claim:940f299b268510da61d8` | official | source_summary | Helix is a Rock web-development surface that combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as an evolution of Lava-driven web development. | [source](https://community.rockrms.com/developer/helix/overview) |
| `claim:2cb25390d2b5f4ffeb6f` | official | configuration | Rock REST API requests require authorization; supported approaches include an HTTP cookie tied to an existing Rock user session or an `Authorization-Token`, which must accompany subsequent API requests. _(live verification recommended)_ | [source](https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api) |
| `claim:896d78fdcfa734dde54e` | official | release_caveat | Rock Mobile compatibility is two-dimensional: documentation uses `M` tags for minimum Mobile Shell versions and `C` tags for minimum Rock Core versions, and a feature may require both. _(live verification recommended)_ | [source](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies) |
| `claim:dc73468ceef82ee62d45` | official | release_caveat | Moving a Rock Mobile app from shell V5 or earlier to V6 or later changes the framework from Xamarin Forms to .NET MAUI; much XAML remains similar, but documented breaking layout behavior must be tested and adapted. _(live verification recommended)_ | [source](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6) |
