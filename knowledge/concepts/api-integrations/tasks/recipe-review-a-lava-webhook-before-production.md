---
concept_id: api-integrations
task_id: recipe-review-a-lava-webhook-before-production
title: Recipe: Review A Lava Webhook Before Production
generated: true
---

# Recipe: Review A Lava Webhook Before Production

A bounded webhook with an explicit security and input contract.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Locate the active webhook configuration.
2. Record its route, method, purpose, and expected callers.
3. Inspect the complete Lava template.
4. List every enabled Lava command and remove any not required.
5. Enumerate every input and define validation for its type, size, and allowed values.
6. Determine whether the webhook returns data, activates a workflow, or mutates entities.
7. Define and test caller authentication or request verification.
8. Confirm the response content type and remove unnecessary fields.
9. Exercise valid, missing, malformed, unauthorized, and replayed requests in a safe environment.
10. Inspect logs without retaining secrets or unnecessary raw payloads.
11. Stop if protection relies only on an obscure URL.
12. Assume no default Lava-webhook security.
13. Inspect the active route, method, template, and enabled Lava commands.
14. Identify every accepted query, form, header, cookie, and body value.
15. Determine whether the webhook exposes data or performs mutations.
16. Verify the explicit caller-authentication or signature-validation mechanism.
17. Remove unneeded commands and returned fields.
18. Stop production use if authentication, input validation, or caller authorization cannot be demonstrated. (Creating APIs Using Lava; approved claim `claim:410bf6750e90b7193262`)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/lava/remote-lava
- https://community.rockrms.com/lava/lava-api
