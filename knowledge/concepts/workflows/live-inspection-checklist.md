---
id: live-checklist:workflows
concept_id: workflows
generated: true
artifact_level: live_checklist
---

# Workflows Live Inspection Checklist

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
14. Inspect `Person, family, alias, and attribute records` in the live instance when the question touches this surface.

## Inspection Targets

- `Rock version`
- `Block settings`
- `Security roles and permissions`
- `WorkflowType and Workflow records`
- `DataView and report filters`
- `Group, GroupType, Location, and Schedule records`
- `Communication recipient, medium, and send history`
- `Mobile shell version and mobile block settings`
- `Person, family, alias, and attribute records`

## Read-Only Probes

- **Workflow type**

```sql
SELECT Id, Name, IsActive, CategoryId FROM WorkflowType WHERE Name LIKE '%<workflow name>%';
```
- **Workflow actions**

```sql
SELECT wat.Id, wat.Name, wat.[Order], wat.EntityTypeId, et.Name AS ActionEntityTypeName FROM WorkflowActionType wat LEFT JOIN EntityType et ON et.Id = wat.EntityTypeId WHERE wat.ActivityTypeId IN (SELECT Id FROM WorkflowActivityType WHERE WorkflowTypeId = <workflow_type_id>) ORDER BY wat.[Order], wat.Id;
```
- **Recent workflow runs**

```sql
SELECT TOP 25 Id, Status, CreatedDateTime, CompletedDateTime FROM Workflow WHERE WorkflowTypeId = <workflow_type_id> ORDER BY CreatedDateTime DESC;
```
- **Launch surfaces**
  - Search pages, blocks, Lava endpoints, REST routes, jobs, and connection/check-in actions that reference the WorkflowType GUID or Id; this schema does not expose a dedicated Webhook table.
