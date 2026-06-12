---
concept_id: security-permissions
generated: true
artifact_level: live_probe_recipes
---

# Security And Permissions Live Probe Recipes

These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.

## Auth rows

- Recipe id: `live-probe-recipe:security-permissions:auth-rows`
- Target binding: Bind `<entity_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<entity_id>`
- Expected tables: `Auth`

```sql
SELECT EntityTypeId, EntityId, Action, AllowOrDeny, SpecialRole, GroupId, PersonAliasId FROM Auth WHERE EntityId = <entity_id> ORDER BY [Order];
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Auth rows` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Page/block security

- Recipe id: `live-probe-recipe:security-permissions:page-block-security`
- Target binding: Bind `<page_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<page_id>`
- Expected tables: `Block`

```sql
SELECT Id, InternalName, PageId, BlockTypeId FROM Block WHERE PageId = <page_id>;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Page/block security` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Group membership

- Recipe id: `live-probe-recipe:security-permissions:group-membership`
- Target binding: Bind `<person_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<person_id>`
- Expected tables: `Group`, `GroupMember`

```sql
SELECT gm.PersonId, gm.GroupId, g.Name, gm.GroupRoleId FROM GroupMember gm JOIN [Group] g ON g.Id = gm.GroupId WHERE gm.PersonId = <person_id>;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Group membership` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## PersonAlias effective context

- Recipe id: `live-probe-recipe:security-permissions:personalias-effective-context`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Verify the exact logged-in PersonAlias, route, page, block, entity, and action being tested.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `PersonAlias effective context` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.
