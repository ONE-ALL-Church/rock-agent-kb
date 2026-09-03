---
concept_id: security-permissions
title: Security And Permissions Agent Cheatsheet
generated: true
---

# Security And Permissions Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Explain an effective permission result](tasks/recipe-explain-an-effective-permission-result.md) | `Person`, `Block` | `Person`, `Block` |
| [Recipe: Publish a page or block with bounded access](tasks/recipe-publish-a-page-or-block-with-bounded-access.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Preflight a least-privilege REST integration](tasks/recipe-preflight-a-least-privilege-rest-integration.md) |  |  |
| [Recipe: Secure a Lava API or Helix endpoint](tasks/recipe-secure-a-lava-api-or-helix-endpoint.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Audit Person Profile notes](tasks/recipe-audit-person-profile-notes.md) | `Person`, `Workflow`, `Page`, `Block` | `Person`, `Workflow`, `Page`, `Block` |
| [Recipe: Validate an AI agent tool before production](tasks/recipe-validate-an-ai-agent-tool-before-production.md) | `Person` | `Person` |
| [Recipe: Run a security-sensitive upgrade preflight](tasks/recipe-run-a-security-sensitive-upgrade-preflight.md) | `Workflow` | `Workflow` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.5` | core | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to t |
| `17.8` | core | Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules when someone tried to |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `1-executive-summary-for-agents` | normal | live verification |
| `scope-and-boundaries` | normal | live verification |
| `3-security-and-permissions-mental-model-the-object-layer` | normal | live verification |
| `3-security-and-permissions-mental-model-the-action-layer` | high | live verification |
| `authorization-and-security-roles` | normal | live verification |
| `authorization-and-security-roles-permission-evaluation` | normal | live verification |
| `login-accounts-and-protection-profiles-external-authentication-and-oidc` | high | live verification |
| `api-authentication-and-identity-bound-links` | normal | live verification |
| `cms-content-personalization-and-lava-pages-and-blocks` | citation-only | live verification |
| `cms-content-personalization-and-lava-advanced-html-and-lava-commands` | normal | live verification |
| `helix-applications-and-endpoint-security` | normal | live verification |
| `feature-specific-authorization-workflows-sign-ups-and-groups` | normal | live verification |
| `feature-specific-authorization-workflows-mobile-check-in` | normal | live verification |
| `feature-specific-authorization-workflows-captcha-and-exposed-forms` | normal | live verification |
| `ai-agents-tools-and-data-access` | citation-only | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-person-cannot-access-an-item-they-should-be-able-to-use` | normal | live verification |
| `troubleshooting-decision-tree-a-page-or-content-item-is-missing-or-publicly-exposed` | citation-only | live verification |
| `troubleshooting-decision-tree-login-fails-after-enabling-2fa-or-an-external-provider` | normal | live verification |
| `troubleshooting-decision-tree-a-rest-request-returns-unauthorized-or-permission-denied` | normal | live verification |
| `troubleshooting-decision-tree-a-helix-endpoint-works-for-administrators-but-not-the-intended-role` | normal | live verification |
| `troubleshooting-decision-tree-a-note-is-missing-visible-to-the-wrong-staff-or-behaves-unexpectedly-downstream` | citation-only | live verification |
| `troubleshooting-decision-tree-a-public-form-is-receiving-abuse-or-captcha-is-not-appearing` | normal | live verification |
| `troubleshooting-decision-tree-a-top-level-sign-up-project-cannot-be-created-or-is-visible-to-the-wrong-people` | normal | live verification |
| `agent-task-recipes-recipe-explain-an-effective-permission-result` | normal | live verification |
| `agent-task-recipes-recipe-publish-a-page-or-block-with-bounded-access` | normal | live verification |
| `agent-task-recipes-recipe-preflight-a-least-privilege-rest-integration` | community-supported | live verification |
| `agent-task-recipes-recipe-secure-a-lava-api-or-helix-endpoint` | community-supported | live verification |
| `agent-task-recipes-recipe-audit-person-profile-notes` | citation-only | live verification |
| `agent-task-recipes-recipe-validate-an-ai-agent-tool-before-production` | citation-only | live verification |
| `agent-task-recipes-recipe-run-a-security-sensitive-upgrade-preflight` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-primary-official-security-documentation` | normal | live verification |
| `source-map-reviewed-community-examples` | community-supported | community-supported |
