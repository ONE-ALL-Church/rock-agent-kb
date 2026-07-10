---
id: live-checklist:mobile
concept_id: mobile
generated: true
artifact_level: live_checklist
---

# Rock Mobile Live Inspection Checklist

## Steps

1. Confirm the Rock version and any relevant release-note caveats.
2. Open the exact page, block, workflow, group, data view, or mobile screen named by the user.
3. Inspect configured settings before inferring behavior from documentation.
4. Check security roles, inherited permissions, and feature flags where applicable.
5. Verify current data rows and recent history before changing production behavior or recommending writes.
6. Inspect `Rock version` in the live instance when the question touches this surface.
7. Inspect `Block settings` in the live instance when the question touches this surface.
8. Inspect `Security roles and permissions` in the live instance when the question touches this surface.
9. Inspect `WorkflowType and Workflow records` in the live instance when the question touches this surface.
10. Inspect `Group, GroupType, Location, and Schedule records` in the live instance when the question touches this surface.
11. Inspect `Financial transaction and gateway settings` in the live instance when the question touches this surface.
12. Inspect `Mobile shell version and mobile block settings` in the live instance when the question touches this surface.
13. Inspect `Person, family, alias, and attribute records` in the live instance when the question touches this surface.

## Inspection Targets

- `Rock version`
- `Block settings`
- `Security roles and permissions`
- `WorkflowType and Workflow records`
- `Group, GroupType, Location, and Schedule records`
- `Financial transaction and gateway settings`
- `Mobile shell version and mobile block settings`
- `Person, family, alias, and attribute records`

## Read-Only Probes

- **Mobile page and blocks**

```sql
SELECT p.Id, p.InternalName, pr.Route, b.Id AS BlockId, b.Name, bt.Name AS BlockType FROM Page p LEFT JOIN PageRoute pr ON pr.PageId = p.Id JOIN Block b ON b.PageId = p.Id JOIN BlockType bt ON bt.Id = b.BlockTypeId WHERE p.InternalName LIKE '%<mobile page>%' OR pr.Route LIKE '%<mobile route>%';
```
- **Block settings**

```sql
SELECT av.EntityId, a.[Key], av.Value FROM AttributeValue av JOIN Attribute a ON a.Id = av.AttributeId WHERE av.EntityId = <block_id>;
```
- **Selector x-ray**
  - Open knowledge/concepts/mobile/resources and compare selectors, block page docs, theme variables, and dark-mode notes.
- **Shell/platform**
  - Confirm iOS/Android shell version and whether the issue occurs in light mode, dark mode, or both.
