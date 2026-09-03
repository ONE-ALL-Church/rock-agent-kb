---
concept_id: helix
task_id: recipe-build-a-validated-mutation-form
title: Recipe: Build a validated mutation form
generated: true
---

# Recipe: Build a validated mutation form

A non-GET endpoint that rejects unauthorized or invalid direct calls as well as invalid browser submissions.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Place the controls inside `<lava-form>`.
2. Prefer supplied Helix control shortcodes where they meet the requirement.
3. Add native validation rules and clear validation messages.
4. Use POST, PUT, or DELETE according to the operation.
5. Configure endpoint or application execution security.
6. Enable only the commands needed for the mutation.
7. Repeat every validation rule in the endpoint.
8. Resolve the target entity from validated input.
9. Verify the caller’s edit rights to that entity.
10. Parameterize or sanitize any SQL inputs.
11. If multiple writes must succeed together, assess the DB Transaction command.
12. Return an appropriate status or HTMX response instruction.
13. Test the endpoint directly with missing, malformed, unauthorized, and tampered input.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/helix/forms-controls/form-validation
- https://community.rockrms.com/lava/commands/db-transaction
- https://community.rockrms.com/lava/commands/http-response
- https://community.rockrms.com/developer/helix/overview/security
