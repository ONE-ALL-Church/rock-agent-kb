---
concept_id: developer-resources
task_id: recipe-prepare-a-plugin-or-theme-package
title: Recipe: Prepare a plugin or theme package
generated: true
---

# Recipe: Prepare a plugin or theme package

Produce a reviewable extension package with understood install and uninstall behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Identify supported Rock versions.
2. Verify that the selected plugin tooling supports those versions.
3. Inventory binaries, Obsidian assets, server files, migrations, and configuration.
4. Build the extension from a clean environment.
5. Generate the package using the current documented packaging workflow.
6. Install it into a disposable supported Rock environment.
7. Test first install and upgrade from the prior supported package.
8. Test uninstall behavior and identify intentionally retained data.
9. Review the package for secrets, environment-specific paths, and organization-specific configuration.
10. Prepare it for the current Rock Shop review process.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer
