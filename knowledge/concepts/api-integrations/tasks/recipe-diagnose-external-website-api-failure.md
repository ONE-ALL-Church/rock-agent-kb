---
concept_id: api-integrations
task_id: recipe-diagnose-external-website-api-failure
title: Recipe: Diagnose External Website API Failure
generated: true
---

# Recipe: Diagnose External Website API Failure

Complete Diagnose External Website API Failure with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Determine browser vs server caller.
2. If browser, inspect CORS and token exposure.
3. If server, inspect auth header/token.
4. Test route with same method and headers.
5. Verify REST action security.
6. Verify entity security.
7. Check API docs and ExceptionLog.
8. Prefer public feed or server proxy if sensitive token would otherwise be exposed.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
