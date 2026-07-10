---
id: answer:obsidian-development:risks-caveats
concept_id: obsidian-development
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Obsidian Development?

When an Obsidian field type uses different public display and edit representations, its client-side value-formatting methods must accept either representation because an unsaved edit component value can be supplied where the display representation is normally expected. Public field-type configuration keys and their meanings form a compatibility contract with remote consumers such as Rock Mobile, so changing them can break existing clients. Generated detail-block save handlers initially treat every selected property as writable, so properties included only to control the UI, such as IsSystem, must be removed from the saveable-property list to prevent unintended database updates. PersonColumn can link a displayed person to the person detail page, but it does not verify that the viewer is authorized to access that page; the documented showAsLink behavior is scoped to Rock 17.

## Top Claims

- `claim:20744671aaaa67e12057`
- `claim:018d0b4c3314bed2719c`
- `claim:25c0ae257b7f419ae7bd`
- `claim:485b886cc73703d3f339`
- `claim:93e0a70a12a20cd668de`

## Citations

- [Converting Core Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types)
- [Creating Field Types](https://community.rockrms.com/developer/obsidian/creating-field-types)
- [Creating Detail Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks)
- [PersonColumn](https://community.rockrms.com/developer/obsidian/grid-reference/columns/personcolumn)
- [Obsidian](https://community.rockrms.com/developer/obsidian)
