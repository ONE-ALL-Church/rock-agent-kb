---
concept_id: workflows
generated: true
artifact_level: live_probe_recipes
---

# Workflows Live Probe Recipes

These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.

## Workflow type

- Recipe id: `live-probe-recipe:workflows:workflow-type`
- Target binding: Bind `<workflow name>` from the exact live object named by the user before running this probe.
- Required parameters: `<workflow name>`
- Expected tables: `WorkflowType`

```sql
SELECT Id, Name, IsActive, CategoryId FROM WorkflowType WHERE Name LIKE '%<workflow name>%';
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Workflow type` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Workflow actions

- Recipe id: `live-probe-recipe:workflows:workflow-actions`
- Target binding: Bind `<workflow_type_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<workflow_type_id>`
- Expected tables: `EntityType`, `WorkflowActionType`, `WorkflowActivityType`

```sql
SELECT wat.Id, wat.Name, wat.[Order], wat.EntityTypeId, et.Name AS ActionEntityTypeName FROM WorkflowActionType wat LEFT JOIN EntityType et ON et.Id = wat.EntityTypeId WHERE wat.ActivityTypeId IN (SELECT Id FROM WorkflowActivityType WHERE WorkflowTypeId = <workflow_type_id>) ORDER BY wat.[Order], wat.Id;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Workflow actions` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Recent workflow runs

- Recipe id: `live-probe-recipe:workflows:recent-workflow-runs`
- Target binding: Bind `<workflow_type_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<workflow_type_id>`
- Expected tables: `Workflow`

```sql
SELECT TOP 25 Id, Status, CreatedDateTime, CompletedDateTime FROM Workflow WHERE WorkflowTypeId = <workflow_type_id> ORDER BY CreatedDateTime DESC;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Recent workflow runs` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Launch surfaces

- Recipe id: `live-probe-recipe:workflows:launch-surfaces`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Search pages, blocks, Lava endpoints, REST routes, jobs, and connection/check-in actions that reference the WorkflowType GUID or Id; this schema does not expose a dedicated Webhook table.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Launch surfaces` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.
