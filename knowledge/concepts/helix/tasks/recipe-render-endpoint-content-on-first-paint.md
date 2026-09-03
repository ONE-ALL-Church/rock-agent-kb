---
concept_id: helix
task_id: recipe-render-endpoint-content-on-first-paint
title: Recipe: Render endpoint content on first paint
generated: true
---

# Recipe: Render endpoint content on first paint

Endpoint-generated content appears during the initial page render without a second request or avoidable layout shift.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Confirm the installed version supports `renderlavaendpoint`.
2. Select a read-safe endpoint for the initial render.
3. Invoke it with the caret route.
4. Specify the method when it is not GET.
5. Do not rely on the default GET method for any mutation.
6. Compare the initial output with the later HTMX-rendered fragment.
7. Confirm authorization behaves consistently in both contexts.
8. Measure whether the extra-request and layout-shift problem is resolved.

## Do Not Assume

- Do not rely on the default GET method for any mutation.

## Source Links

- https://community.rockrms.com/lava/commands/render-lava-endpoint
- https://community.rockrms.com/developer/helix/lava-applications/content-block
