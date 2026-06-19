---
concept_id: engagement-tracking
generated: true
artifact_level: live_probe_recipes
---

# Engagement Tracking Live Probe Recipes

These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.

## Version and release context

- Recipe id: `live-probe-recipe:engagement-tracking:version-and-release-context`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Confirm the installed Rock version in the Rock application/system information before applying release-note caveats; do not rely on a RockMigration table in SQL.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Version and release context` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Database migration context

- Recipe id: `live-probe-recipe:engagement-tracking:database-migration-context`
- Target binding: Run only after identifying the exact live object or schema surface being inspected.

```sql
SELECT TOP 1 MigrationId, ProductVersion FROM __MigrationHistory ORDER BY MigrationId DESC;
```

Evidence to record:
- Rock version or migration context used for the review.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Database migration context` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Page/block settings

- Recipe id: `live-probe-recipe:engagement-tracking:page-block-settings`
- Target binding: Bind `<page name>`, `<route>` from the exact live object named by the user before running this probe.
- Required parameters: `<page name>`, `<route>`
- Expected tables: `Block`, `Page`, `PageRoute`

```sql
SELECT p.Id AS PageId, p.InternalName, pr.Route, b.Id AS BlockId, b.Name FROM Page p LEFT JOIN PageRoute pr ON pr.PageId = p.Id LEFT JOIN Block b ON b.PageId = p.Id WHERE p.InternalName LIKE '%<page name>%' OR pr.Route LIKE '%<route>%';
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Page/block settings` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Security rows

- Recipe id: `live-probe-recipe:engagement-tracking:security-rows`
- Target binding: Bind `<entity_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<entity_id>`
- Expected tables: `Auth`

```sql
SELECT EntityTypeId, EntityId, Action, AllowOrDeny, SpecialRole, GroupId FROM Auth WHERE EntityId = <entity_id> ORDER BY [Order];
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Security rows` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Named records

- Recipe id: `live-probe-recipe:engagement-tracking:named-records`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Search the live Rock instance for the exact Engagement Tracking record, page, block, entity, or configured object named by the user.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Named records` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.
