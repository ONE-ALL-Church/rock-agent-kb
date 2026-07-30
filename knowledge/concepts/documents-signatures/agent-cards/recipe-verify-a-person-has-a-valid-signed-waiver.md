---
concept_id: documents-signatures
task_id: recipe-verify-a-person-has-a-valid-signed-waiver
title: Recipe: Verify A Person Has A Valid Signed Waiver
generated: true
---

# Recipe: Verify A Person Has A Valid Signed Waiver

Complete Verify A Person Has A Valid Signed Waiver with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`

## Entities And Tables

- `Person`
- `PersonAlias`

## Steps

1. The person and aliases.
2. Signature template ID.
3. `SignatureDocument` records for applies-to person alias.
4. Status `Signed`.
5. Signed date/time.
6. Template validity settings.
7. Validity duration.
8. Binary file presence.
9. Whether document is legacy.
10. Found or not found.
11. Signed date.
12. Expiration date if duration applies.
13. Signed by person.
14. PDF present or missing.
15. Any ambiguity due to duplicates or multiple aliases.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents
- https://community.rockrms.com/rocku/workflows/workflow-person-entry
