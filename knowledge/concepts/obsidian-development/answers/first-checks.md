---
id: answer:obsidian-development:first-checks
concept_id: obsidian-development
generated: true
artifact_level: answer
---

# What should I check first for Obsidian Development?

The Obsidian Browser Bus is a page-local publish-subscribe mechanism backed by DOM events; its messages do not cross browser tabs or reach another user's browser. For an Obsidian plugin, `npm run build` performs TypeScript type checking before compiling and copying assets to RockWeb, whereas `npm run watch` continuously recompiles changed files without type checking. Obsidian block actions are stateless server calls, so every action must revalidate client data and recheck authorization rather than relying on TypeScript visibility or a previous C# instance. To make a core field type available in Obsidian, declare Obsidian platform support on its C# field type, expose its GUID through the generated field-type system GUIDs, and import and register its TypeScript implementation in the Obsidian field-type index.

## Top Claims

- `claim:200236163eb04b5ba086`
- `claim:2435a526d1ed1eaebbe7`
- `claim:2502ae4f58523612e4a1`
- `claim:c129f3cd12206e1e425b`
- `claim:0968c36e7240abc05a8f`
- `claim:78428dfda89499f150b2`
- `claim:92fc3e39e7763d1e2bc1`
- `claim:a42b7d81a72eccfcfccf`

## Citations

- [Browser Bus](https://community.rockrms.com/developer/obsidian/browser-bus)
- [Plugin Development](https://community.rockrms.com/developer/obsidian/plugin-development)
- [Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)
- [Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types)
- [CopyColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/copycolumn)
- [Creating UI Controls](https://community.rockrms.com/developer/obsidian/creating-ui-controls)
- [Null vs Undefined](https://community.rockrms.com/developer/obsidian/null-vs-undefined)
- [App Laws](https://community.rockrms.com/developer/obsidian/app-laws)
