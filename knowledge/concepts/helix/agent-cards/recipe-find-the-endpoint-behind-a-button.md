---
concept_id: helix
task_id: recipe-find-the-endpoint-behind-a-button
title: Recipe: Find The Endpoint Behind A Button
generated: true
---

# Recipe: Find The Endpoint Behind A Button

Complete Find The Endpoint Behind A Button with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Inspect the rendered element.
2. Read `hx-get`, `hx-post`, `hx-put`, or `hx-delete`.
3. Note the application slug and endpoint slug.
4. Note the HTTP method.
5. Find the Lava Application by slug.
6. Find the Lava Endpoint by slug and method.
7. Check active state, security mode, enabled commands, and code template.
8. Test the request in browser dev tools.
9. Review observability using endpoint/application names.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications/observability
