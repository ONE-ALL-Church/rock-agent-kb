---
concept_id: security-permissions
task_id: recipe-run-a-security-sensitive-upgrade-preflight
title: Recipe: Run a security-sensitive upgrade preflight
generated: true
---

# Recipe: Run a security-sensitive upgrade preflight

A version-aware plan that distinguishes security fixes from feature changes.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Record the installed Rock version and hosting model.
2. Review current supported branches and release notes.
3. Identify security-relevant fixes between the installed and target versions.
4. Separate major-version validation from dot-release validation.
5. Inventory affected authentication, API, CMS, workflow, document, and Helix surfaces.
6. Rehearse the upgrade and rollback in the organization’s approved environment.
7. Retest unauthorized, intended-role, and administrator scenarios.
8. Verify protected documents, Sign-Up visibility, OIDC, APIs, and endpoint authorization where applicable.
9. Do not declare completion from package installation alone; verify rendered and callable behavior. Rock release notes,

## Do Not Assume

- Do not declare completion from package installation alone; verify rendered and callable behavior.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration
- https://community.rockrms.com/documentation/core-concepts/security/captcha/use-captcha
- https://community.rockrms.com/documentation/core-concepts/security/captcha/configure-captcha
- https://community.rockrms.com/documentation
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Mobile/LocationPermissionStatus.cs
- https://community.rockrms.com/documentation/core-concepts/security/background-checks/administer-background-checks
- https://community.rockrms.com/documentation/core-concepts/security/background-checks/configure-checkr
- https://community.rockrms.com/documentation/core-concepts/security/background-checks/configure-protect-my-ministry
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Plugin/HotFixes/291_HardenCoreWorkflowSecurity.cs
- https://community.rockrms.com/rocku/workflows
