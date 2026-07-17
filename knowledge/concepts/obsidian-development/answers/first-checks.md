---
id: answer:obsidian-development:first-checks
concept_id: obsidian-development
generated: true
artifact_level: answer
---

# What should I check first for Obsidian Development?

The Obsidian developer documentation is a work in progress, so described behavior may change or may not yet be implemented as documented. An Obsidian field configuration change handled entirely in the client should emit an updated model value, while a change that requires refreshed server-derived options should additionally request a configuration update. Obsidian block actions are stateless server calls, so every action must revalidate client data and recheck authorization rather than relying on TypeScript visibility or a previous C# instance. Set an Obsidian Grid's key field to the data property that uniquely identifies each row when using advanced grid features that depend on row identity.

## Top Claims

- `claim:200236163eb04b5ba086`
- `claim:2435a526d1ed1eaebbe7`
- `claim:2502ae4f58523612e4a1`
- `claim:c129f3cd12206e1e425b`
- `claim:0968c36e7240abc05a8f`
- `claim:78428dfda89499f150b2`
- `claim:92fc3e39e7763d1e2bc1`
- `claim:a42b7d81a72eccfcfccf`

## Distilled Claims

- `distilled-claim:3afcc918fe79e80c4b4a`
- `distilled-claim:44f4aa9e42ec03ed8e97`
- `distilled-claim:6e4324da54be4f35da7c`
- `distilled-claim:9a5e26521cb4b7e66eec`

## Citations

- [Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)
- [Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)
- [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)
- [Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types)
- [CopyColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/copycolumn)
- [Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)
- [Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined)
- [App Laws](https://community.rockrms.com/developer/obsidian/app-laws)
