---
concept_id: ai-agents-automation
title: AI Agents And Automation Open Questions
generated: true
---

# AI Agents And Automation Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `8-agent-tools-and-lookup-surfaces-deep-dive-list-tools`: List Tools (85 words)
- `8-agent-tools-and-lookup-surfaces-deep-dive-availableattributes-tools`: AvailableAttributes Tools (84 words)
- `8-agent-tools-and-lookup-surfaces-deep-dive-addorupdate-tools`: AddOrUpdate Tools (90 words)
- `9-permissions-and-data-boundaries-deep-dive-sensitive-data-classes`: Sensitive Data Classes (98 words)
- `10-automation-design-and-workflows-deep-dive-trigger-design`: Trigger Design (109 words)
- `13-administration-and-operational-guardrails`: 13. Administration And Operational Guardrails (233 words)
- `17-implementation-playbooks-playbook-build-a-read-only-staff-agent`: Playbook: Build A Read-Only Staff Agent (90 words)

## Community-Supported Only

- `18-troubleshooting-decision-tree-lava-webrequest-or-external-call-behaves-unexpectedly`: Lava WebRequest Or External Call Behaves Unexpectedly

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-ai-agents-and-automation-mental-model`: 3. AI Agents And Automation Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model`: 5. Core Configuration And Data Model
- `6-primary-entities-and-relationships`: 6. Primary Entities And Relationships
- `7-common-ai-agents-and-automation-workflows-event-registration-support`: Event Registration Support
- `7-common-ai-agents-and-automation-workflows-chat-message-automation`: Chat Message Automation
- `7-common-ai-agents-and-automation-workflows-mobile-voice-agent`: Mobile Voice Agent
- `8-agent-tools-and-lookup-surfaces-deep-dive-availableattributes-tools`: AvailableAttributes Tools
- `9-permissions-and-data-boundaries-deep-dive`: 9. Permissions And Data Boundaries Deep Dive
- `9-permissions-and-data-boundaries-deep-dive-generated-v2-endpoint-boundary`: Generated v2 Endpoint Boundary
- `10-automation-design-and-workflows-deep-dive-agent-as-reviewer-automation`: Agent-As-Reviewer Automation
- `11-verification-and-review-gates-deep-dive-read-only-low-risk-gate`: Read-Only Low-Risk Gate
- `11-verification-and-review-gates-deep-dive-sensitive-read-gate`: Sensitive Read Gate
- `11-verification-and-review-gates-deep-dive-security-review-gate`: Security Review Gate
- `11-verification-and-review-gates-deep-dive-debugging-gate`: Debugging Gate
- `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-security`: Security
- `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-api-integrations`: API Integrations
- `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-platform-configuration`: Platform Configuration
- `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-data-views`: Data Views
- `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-operations`: Operations
- `13-administration-and-operational-guardrails`: 13. Administration And Operational Guardrails
- `14-developer-api-lava-and-source-code-landmarks-native-tool-development`: Native Tool Development
- `14-developer-api-lava-and-source-code-landmarks-lava-tool-development`: Lava Tool Development
- `15-reporting-analytics-and-model-map`: 15. Reporting, Analytics, And Model Map
- `16-version-and-release-caveats`: 16. Version And Release Caveats
- `17-implementation-playbooks-playbook-build-a-read-only-staff-agent`: Playbook: Build A Read-Only Staff Agent
- `17-implementation-playbooks-playbook-build-a-custom-lookup-tool`: Playbook: Build A Custom Lookup Tool
- `17-implementation-playbooks-playbook-build-a-lava-insight-tool`: Playbook: Build A Lava Insight Tool
- `17-implementation-playbooks-playbook-build-a-native-addorupdate-tool`: Playbook: Build A Native AddOrUpdate Tool
- `17-implementation-playbooks-playbook-add-a-skill-to-an-agent`: Playbook: Add A Skill To An Agent
- `17-implementation-playbooks-playbook-configure-chat-message-automation`: Playbook: Configure Chat Message Automation
- `18-troubleshooting-decision-tree-agent-does-not-call-the-expected-tool`: Agent Does Not Call The Expected Tool
- `18-troubleshooting-decision-tree-tool-returns-no-records`: Tool Returns No Records
- `18-troubleshooting-decision-tree-permissions-look-wrong`: Permissions Look Wrong
- `18-troubleshooting-decision-tree-lava-webrequest-or-external-call-behaves-unexpectedly`: Lava WebRequest Or External Call Behaves Unexpectedly
- `19-agent-task-recipes-recipe-draft-a-communication`: Recipe: “Draft A Communication”
- `19-agent-task-recipes-recipe-create-a-connection-request`: Recipe: “Create A Connection Request”

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
