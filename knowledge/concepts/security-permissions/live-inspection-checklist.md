---
id: live-checklist:security-permissions
concept_id: security-permissions
generated: true
artifact_level: live_checklist
---

# Security And Permissions Live Inspection Checklist

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
11. Inspect `Group, GroupType, Location, and Schedule records` in the live instance when the question touches this surface.
12. Inspect `Communication recipient, medium, and send history` in the live instance when the question touches this surface.
13. Inspect `Mobile shell version and mobile block settings` in the live instance when the question touches this surface.
14. Inspect `Registration instance and registrant records` in the live instance when the question touches this surface.
15. Inspect `Person, family, alias, and attribute records` in the live instance when the question touches this surface.

## Inspection Targets

- `Rock version`
- `Block settings`
- `Security roles and permissions`
- `WorkflowType and Workflow records`
- `DataView and report filters`
- `Group, GroupType, Location, and Schedule records`
- `Communication recipient, medium, and send history`
- `Mobile shell version and mobile block settings`
- `Registration instance and registrant records`
- `Person, family, alias, and attribute records`

## Read-Only Probes

- **Auth rows**

```sql
SELECT EntityTypeId, EntityId, Action, AllowOrDeny, SpecialRole, GroupId, PersonAliasId FROM Auth WHERE EntityId = <entity_id> ORDER BY [Order];
```
- **Page/block security**

```sql
SELECT Id, InternalName, PageId, BlockTypeId FROM Block WHERE PageId = <page_id>;
```
- **Group membership**

```sql
SELECT gm.PersonId, gm.GroupId, g.Name, gm.GroupRoleId FROM GroupMember gm JOIN [Group] g ON g.Id = gm.GroupId WHERE gm.PersonId = <person_id>;
```
- **PersonAlias effective context**
  - Verify the exact logged-in PersonAlias, route, page, block, entity, and action being tested.
