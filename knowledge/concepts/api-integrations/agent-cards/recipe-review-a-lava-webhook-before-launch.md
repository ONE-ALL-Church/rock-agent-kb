---
concept_id: api-integrations
task_id: recipe-review-a-lava-webhook-before-launch
title: Recipe: Review A Lava Webhook Before Launch
generated: true
---

# Recipe: Review A Lava Webhook Before Launch

Complete Review A Lava Webhook Before Launch with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Confirm purpose and owner.
2. Confirm route and method.
3. Verify no sensitive data is exposed publicly.
4. Review enabled Lava commands.
5. Review input validation.
6. Review output content type.
7. Review caching.
8. Test malformed, missing, unauthorized, and valid requests.
9. Add monitoring/logging.
10. Document rollback/disable path.
11. Defined Type is `Lava Webhook`.
12. Defined Value value matches path after `/Webhooks/Lava.ashx/`.
13. Method/verb matches.
14. Regex/path variables are correct.
15. The site route/casing/rewrite is not altering path.
16. Template compiles.
17. Required Lava commands are enabled.
18. Errors are not swallowed by production error settings.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
- https://community.rockrms.com/ask/developing/2842
