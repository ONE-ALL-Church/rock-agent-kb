---
concept_id: roku
generated: true
artifact_level: claim_graph
approved_claim_count: 16
---

# Roku Apps Approved Claims

This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.

| Claim ID | Authority | Type | Claim | Source |
| --- | --- | --- | --- | --- |
| `claim:563e520ec15928e19628` | official | behavior | Rock Roku pages display custom Lava-driven content as part of the application and render SceneGraph-oriented output rather than normal Rock CMS HTML. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| `claim:84305ad4d42aafc22e6d` | official | behavior | In Rock Roku layouts, a FocusGroup arranges its child views horizontally or vertically and automatically moves focus left/right for horizontal groups or up/down for vertical groups. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group) |
| `claim:c1b03d50f87ed2b41b40` | official | behavior | For Roku media playback, supplying a prior watch map sets the resume position; including its interaction GUID also appends progress to that interaction, while omitting the GUID creates a new interaction with a new watch map beginning from the resumed position. | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| `claim:a43c6281e5328e7cac68` | official | configuration | A Rock Roku application includes configuration such as page-view tracking, page-view retention duration, and API key settings, so Roku troubleshooting should start with the application record before page Lava. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| `claim:d67d29d2e4b62513a89b` | official | configuration | A Rock Roku application can reference a website authentication page that supports remote authentication within the TV application. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| `claim:f1a329c4eb4099f7fa88` | official | configuration | Roku page caching can be configured as public, application-private, revalidated on every load, or disabled; separate maximum-age settings control application and shared-cache retention. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| `claim:49c04d8f25f6c5546bb4` | official | implementation_pattern | When selecting SceneGraph layout elements for a Rock Roku application, account for the fact that most Roku layouts lack default item templates and prefer built-in elements where possible to avoid custom BrightScript components. | [source](https://community.rockrms.com/developer/roku-docs/resources/layout-nodes) |
| `claim:6ff04ce9f309e8163832` | official | implementation_pattern | A Rock Roku page's SceneGraph content should use `Rock:Page` as its outermost component so the page can define which content receives initial focus. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| `claim:9398f3fb18e8a79c0e4d` | official | implementation_pattern | Roku commands are executed by setting a rockCommand and command-specific parameters on supported controls, and multiple commands can be chained by separating command names with commas. | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| `claim:b850114f9e68b1d54b0c` | official | implementation_pattern | Rock Roku applications use Roku's SceneGraph XML language and are composed primarily from built-in SceneGraph components, supplemented by Rock-provided custom components. | [source](https://community.rockrms.com/developer/roku-docs/resources/controls) |
| `claim:003a9c4612c20c61b9f4` | official | operational_guidance | Beginning Roku development with Rock requires contacting the Rock Core team to obtain a development application setup. | [source](https://community.rockrms.com/developer/roku-docs) |
| `claim:ac1a7656566fe397bb04` | official | recipe | Starting Roku development with Rock requires requesting a development application from the Rock Core team through the designated request form; the team then provides setup instructions. | [source](https://community.rockrms.com/developer/roku-docs/getting-started) |
| `claim:410bf6750e90b7193262` | official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| `claim:48551097f44d6d7860ae` | official | risk | Rock's Roku TV application cannot play YouTube content; its video command expects a directly playable MP4 or HLS resource instead. | [source](https://community.rockrms.com/developer/roku-docs/commands/media) |
| `claim:669456b72f0978dc418a` | official | source_summary | Rock Roku documentation describes Roku support as a way to extend Rock-powered digital ministry to Roku TV through Rock-managed Roku integration. | [source](https://community.rockrms.com/developer/roku-docs) |
| `claim:52b50da71870c1d611da` | release-note-confirmed | release_caveat | Triumph's GitHub Spotlight for the v17.0.29 pre-alpha notes that the Roku TV app feature was added for Rock v16.7, making Roku coverage version-sensitive. | [source](https://www.triumph.tech/resources/github-spotlight-1042024) |
