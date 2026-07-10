---
concept_id: obsidian-development
generated: true
artifact_level: claim_graph
approved_claim_count: 4
---

# Obsidian Development Approved Claims

This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.

| Claim ID | Authority | Type | Claim | Source |
| --- | --- | --- | --- | --- |
| `claim:200236163eb04b5ba086` | official | behavior | The Obsidian Browser Bus is a page-local publish-subscribe mechanism backed by DOM events; its messages do not cross browser tabs or reach another user's browser. | [source](https://community.rockrms.com/developer/obsidian/browser-bus) |
| `claim:2502ae4f58523612e4a1` | official | implementation_pattern | Obsidian block actions are stateless server calls, so every action must revalidate client data and recheck authorization rather than relying on TypeScript visibility or a previous C# instance. | [source](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks) |
| `claim:fea01b9e6403198166d2` | official | implementation_pattern | An Obsidian field configuration change handled entirely in the client should emit an updated model value, while a change that requires refreshed server-derived options should additionally request a configuration update. | [source](https://community.rockrms.com/developer/obsidian/creating-field-types/core-field-type-patterns) |
| `claim:e92f0b8e130c396de463` | official | operational_guidance | Core `.obs` development is supported in Visual Studio Code rather than the Visual Studio editor, and the repository workspace supplies the expected settings and watch tasks for Obsidian controls and blocks. | [source](https://community.rockrms.com/developer/obsidian/core-development-environment) |
