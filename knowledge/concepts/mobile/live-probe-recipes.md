---
concept_id: mobile
generated: true
artifact_level: live_probe_recipes
---

# Rock Mobile Live Probe Recipes

These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.

## Mobile page and blocks

- Recipe id: `live-probe-recipe:mobile:mobile-page-and-blocks`
- Target binding: Bind `<mobile page>`, `<mobile route>` from the exact live object named by the user before running this probe.
- Required parameters: `<mobile page>`, `<mobile route>`
- Expected tables: `Block`, `BlockType`, `Page`, `PageRoute`

```sql
SELECT p.Id, p.InternalName, pr.Route, b.Id AS BlockId, b.Name, bt.Name AS BlockType FROM Page p LEFT JOIN PageRoute pr ON pr.PageId = p.Id JOIN Block b ON b.PageId = p.Id JOIN BlockType bt ON bt.Id = b.BlockTypeId WHERE p.InternalName LIKE '%<mobile page>%' OR pr.Route LIKE '%<mobile route>%';
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Mobile page and blocks` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Block settings

- Recipe id: `live-probe-recipe:mobile:block-settings`
- Target binding: Bind `<block_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<block_id>`
- Expected tables: `Attribute`, `AttributeValue`

```sql
SELECT av.EntityId, a.[Key], av.Value FROM AttributeValue av JOIN Attribute a ON a.Id = av.AttributeId WHERE av.EntityId = <block_id>;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Block settings` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Selector x-ray

- Recipe id: `live-probe-recipe:mobile:selector-x-ray`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Open knowledge/concepts/mobile/resources and compare selectors, block page docs, theme variables, and dark-mode notes.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Selector x-ray` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Shell/platform

- Recipe id: `live-probe-recipe:mobile:shell-platform`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Confirm iOS/Android shell version and whether the issue occurs in light mode, dark mode, or both.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Shell/platform` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.
