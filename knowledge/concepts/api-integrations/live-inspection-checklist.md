---
id: live-checklist:api-integrations
concept_id: api-integrations
generated: true
artifact_level: live_checklist
---

# API And Integrations Live Inspection Checklist

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
10. Inspect `DataView and report filters` in the live instance when the question touches this surface.
11. Inspect `Communication recipient, medium, and send history` in the live instance when the question touches this surface.
12. Inspect `Financial transaction and gateway settings` in the live instance when the question touches this surface.
13. Inspect `Mobile shell version and mobile block settings` in the live instance when the question touches this surface.
14. Inspect `Registration instance and registrant records` in the live instance when the question touches this surface.
15. Inspect `Person, family, alias, and attribute records` in the live instance when the question touches this surface.

## Inspection Targets

- `Rock version`
- `Block settings`
- `Security roles and permissions`
- `WorkflowType and Workflow records`
- `DataView and report filters`
- `Communication recipient, medium, and send history`
- `Financial transaction and gateway settings`
- `Mobile shell version and mobile block settings`
- `Registration instance and registrant records`
- `Person, family, alias, and attribute records`

## Read-Only Probes

- **Version and release context**
  - Confirm the installed Rock version in the Rock application/system information before applying release-note caveats; do not rely on a RockMigration table in SQL.
- **Database migration context**

```sql
SELECT TOP 1 MigrationId, ProductVersion FROM __MigrationHistory ORDER BY MigrationId DESC;
```
- **Page/block settings**

```sql
SELECT p.Id AS PageId, p.InternalName, pr.Route, b.Id AS BlockId, b.Name FROM Page p LEFT JOIN PageRoute pr ON pr.PageId = p.Id LEFT JOIN Block b ON b.PageId = p.Id WHERE p.InternalName LIKE '%<page name>%' OR pr.Route LIKE '%<route>%';
```
- **Security rows**

```sql
SELECT EntityTypeId, EntityId, Action, AllowOrDeny, SpecialRole, GroupId FROM Auth WHERE EntityId = <entity_id> ORDER BY [Order];
```
- **Named records**
  - Search the live Rock instance for the exact API And Integrations record, page, block, entity, or configured object named by the user.
