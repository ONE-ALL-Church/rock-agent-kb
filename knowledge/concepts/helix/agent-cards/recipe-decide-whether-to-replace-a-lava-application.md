---
concept_id: helix
task_id: recipe-decide-whether-to-replace-a-lava-application
title: Recipe: Decide whether to replace a Lava Application
generated: true
---

# Recipe: Decide whether to replace a Lava Application

A documented decision to retain Helix or move to a purpose-built solution.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Count the application’s endpoints.
2. Identify whether the requested design requires custom models.
3. Assess whether ordinary changes are becoming complex or fragile.
4. Review security, deployment, testing, and maintenance costs.
5. If custom models, approximately 50 or more endpoints, or persistent fragility are present, compare a purpose-built implementation.
6. Keep the application in Helix only when its operational boundaries remain understandable and supportable.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/helix/overview/customizing-rock
