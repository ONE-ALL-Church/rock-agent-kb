---
concept_id: roku
generated: true
artifact_level: claim_graph
approved_claim_count: 6
---

# Roku Apps Approved Claims

This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.

| Claim ID | Authority | Type | Claim | Source |
| --- | --- | --- | --- | --- |
| `claim:563e520ec15928e19628` | official | behavior | Rock Roku pages display custom Lava-driven content as part of the application and render SceneGraph-oriented output rather than normal Rock CMS HTML. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/pages) |
| `claim:a43c6281e5328e7cac68` | official | configuration | A Rock Roku application includes configuration such as page-view tracking, page-view retention duration, and API key settings, so Roku troubleshooting should start with the application record before page Lava. | [source](https://community.rockrms.com/developer/roku-docs/getting-started/applications) |
| `claim:9398f3fb18e8a79c0e4d` | official | implementation_pattern | Roku commands are executed by setting a rockCommand and command-specific parameters on supported controls, and multiple commands can be chained by separating command names with commas. | [source](https://community.rockrms.com/developer/roku-docs/commands) |
| `claim:410bf6750e90b7193262` | official | risk | Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. | [source](https://community.rockrms.com/lava/lava-api) |
| `claim:669456b72f0978dc418a` | official | source_summary | Rock Roku documentation describes Roku support as a way to extend Rock-powered digital ministry to Roku TV through Rock-managed Roku integration. | [source](https://community.rockrms.com/developer/roku-docs) |
| `claim:52b50da71870c1d611da` | release-note-confirmed | release_caveat | Triumph's GitHub Spotlight for the v17.0.29 pre-alpha notes that the Roku TV app feature was added for Rock v16.7, making Roku coverage version-sensitive. | [source](https://www.triumph.tech/resources/github-spotlight-1042024) |
