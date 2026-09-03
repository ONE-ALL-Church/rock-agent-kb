---
concept_id: security-permissions
title: Security And Permissions Open Questions
generated: true
---

# Security And Permissions Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `agent-task-recipes-recipe-preflight-a-least-privilege-rest-integration`: Recipe: Preflight a least-privilege REST integration
- `agent-task-recipes-recipe-secure-a-lava-api-or-helix-endpoint`: Recipe: Secure a Lava API or Helix endpoint
- `source-map-reviewed-community-examples`: Reviewed community examples

## Needs Live Verification

- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `scope-and-boundaries`: Scope And Boundaries
- `3-security-and-permissions-mental-model-the-object-layer`: The Object Layer
- `3-security-and-permissions-mental-model-the-action-layer`: The Action Layer
- `authorization-and-security-roles`: Authorization And Security Roles
- `authorization-and-security-roles-permission-evaluation`: Permission evaluation
- `login-accounts-and-protection-profiles-external-authentication-and-oidc`: External authentication and OIDC
- `api-authentication-and-identity-bound-links`: API Authentication And Identity-Bound Links
- `cms-content-personalization-and-lava-pages-and-blocks`: Pages and blocks
- `cms-content-personalization-and-lava-advanced-html-and-lava-commands`: Advanced HTML and Lava commands
- `helix-applications-and-endpoint-security`: Helix Applications And Endpoint Security
- `feature-specific-authorization-workflows-sign-ups-and-groups`: Sign-Ups and groups
- `feature-specific-authorization-workflows-mobile-check-in`: Mobile check-in
- `feature-specific-authorization-workflows-captcha-and-exposed-forms`: CAPTCHA and exposed forms
- `ai-agents-tools-and-data-access`: AI Agents, Tools, And Data Access
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-person-cannot-access-an-item-they-should-be-able-to-use`: A person cannot access an item they should be able to use
- `troubleshooting-decision-tree-a-page-or-content-item-is-missing-or-publicly-exposed`: A page or content item is missing or publicly exposed
- `troubleshooting-decision-tree-login-fails-after-enabling-2fa-or-an-external-provider`: Login fails after enabling 2FA or an external provider
- `troubleshooting-decision-tree-a-rest-request-returns-unauthorized-or-permission-denied`: A REST request returns unauthorized or permission denied
- `troubleshooting-decision-tree-a-helix-endpoint-works-for-administrators-but-not-the-intended-role`: A Helix endpoint works for administrators but not the intended role
- `troubleshooting-decision-tree-a-note-is-missing-visible-to-the-wrong-staff-or-behaves-unexpectedly-downstream`: A note is missing, visible to the wrong staff, or behaves unexpectedly downstream
- `troubleshooting-decision-tree-a-public-form-is-receiving-abuse-or-captcha-is-not-appearing`: A public form is receiving abuse or CAPTCHA is not appearing
- `troubleshooting-decision-tree-a-top-level-sign-up-project-cannot-be-created-or-is-visible-to-the-wrong-people`: A top-level Sign-Up project cannot be created or is visible to the wrong people
- `agent-task-recipes-recipe-explain-an-effective-permission-result`: Recipe: Explain an effective permission result
- `agent-task-recipes-recipe-publish-a-page-or-block-with-bounded-access`: Recipe: Publish a page or block with bounded access
- `agent-task-recipes-recipe-preflight-a-least-privilege-rest-integration`: Recipe: Preflight a least-privilege REST integration
- `agent-task-recipes-recipe-secure-a-lava-api-or-helix-endpoint`: Recipe: Secure a Lava API or Helix endpoint
- `agent-task-recipes-recipe-audit-person-profile-notes`: Recipe: Audit Person Profile notes
- `agent-task-recipes-recipe-validate-an-ai-agent-tool-before-production`: Recipe: Validate an AI agent tool before production
- `agent-task-recipes-recipe-run-a-security-sensitive-upgrade-preflight`: Recipe: Run a security-sensitive upgrade preflight
- `known-gaps-and-live-verification`: Known Gaps And Live Verification
- `source-map-primary-official-security-documentation`: Primary official security documentation

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
