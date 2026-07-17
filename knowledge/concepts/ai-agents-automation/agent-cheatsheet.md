---
concept_id: ai-agents-automation
title: AI Agents And Automation Agent Cheatsheet
generated: true
---

# AI Agents And Automation Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: “Find The Right Person”](tasks/recipe-find-the-right-person.md) |  |  |
| [Recipe: “Summarize This Person”](tasks/recipe-summarize-this-person.md) |  |  |
| [Recipe: “Draft A Communication”](tasks/recipe-draft-a-communication.md) |  |  |
| [Recipe: “Create A Connection Request”](tasks/recipe-create-a-connection-request.md) |  |  |
| [Recipe: “Explain A Workflow Queue”](tasks/recipe-explain-a-workflow-queue.md) |  |  |
| [Recipe: “Audit Agent Security”](tasks/recipe-audit-agent-security.md) |  |  |
| [Recipe: “Build A Safe Public Agent”](tasks/recipe-build-a-safe-public-agent.md) |  |  |
| [Recipe: “Review An Agent Answer”](tasks/recipe-review-an-agent-answer.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added a new "Chat Message" Automation Trigger that can launch Automation Events when a Chat message is sent. Also added a "Send Fallback Chat Notification" Automation Event that alerts individuals via alternate methods (such as email or SMS |
| `17.5` | core | Fixed an issue where trying to access a model's ./DataView/{id} endpoint would check permissions on the wrong entity. This often resulted in a permission denied error even when the Person or API Key had been granted explicit permission to t |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-ai-agents-and-automation-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model` | normal | live verification |
| `6-primary-entities-and-relationships` | normal | live verification |
| `7-common-ai-agents-and-automation-workflows-event-registration-support` | normal | live verification |
| `7-common-ai-agents-and-automation-workflows-chat-message-automation` | normal | live verification |
| `7-common-ai-agents-and-automation-workflows-mobile-voice-agent` | normal | live verification |
| `8-agent-tools-and-lookup-surfaces-deep-dive-availableattributes-tools` | normal | live verification |
| `9-permissions-and-data-boundaries-deep-dive` | normal | live verification |
| `9-permissions-and-data-boundaries-deep-dive-generated-v2-endpoint-boundary` | normal | live verification |
| `10-automation-design-and-workflows-deep-dive-agent-as-reviewer-automation` | structural | live verification |
| `11-verification-and-review-gates-deep-dive-read-only-low-risk-gate` | structural | live verification |
| `11-verification-and-review-gates-deep-dive-sensitive-read-gate` | structural | live verification |
| `11-verification-and-review-gates-deep-dive-security-review-gate` | normal | live verification |
| `11-verification-and-review-gates-deep-dive-debugging-gate` | normal | live verification |
| `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-security` | normal | live verification |
| `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-api-integrations` | normal | live verification |
| `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-platform-configuration` | structural | live verification |
| `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-data-views` | normal | live verification |
| `12-related-rock-areas-security-api-integrations-workflows-platform-configuration-data-views-reports-operations-lava-operations` | normal | live verification |
| `13-administration-and-operational-guardrails` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-native-tool-development` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-tool-development` | normal | live verification |
| `15-reporting-analytics-and-model-map` | citation-only | live verification |
| `16-version-and-release-caveats` | high | live verification |
| `17-implementation-playbooks-playbook-build-a-read-only-staff-agent` | normal | live verification |
| `17-implementation-playbooks-playbook-build-a-custom-lookup-tool` | normal | live verification |
| `17-implementation-playbooks-playbook-build-a-lava-insight-tool` | normal | live verification |
| `17-implementation-playbooks-playbook-build-a-native-addorupdate-tool` | normal | live verification |
| `17-implementation-playbooks-playbook-add-a-skill-to-an-agent` | normal | live verification |
| `17-implementation-playbooks-playbook-configure-chat-message-automation` | structural | live verification |
| `18-troubleshooting-decision-tree-agent-does-not-call-the-expected-tool` | normal | live verification |
| `18-troubleshooting-decision-tree-tool-returns-no-records` | structural | live verification |
| `18-troubleshooting-decision-tree-permissions-look-wrong` | normal | live verification |
| `18-troubleshooting-decision-tree-lava-webrequest-or-external-call-behaves-unexpectedly` | community-supported | live verification |
| `19-agent-task-recipes-recipe-draft-a-communication` | structural | live verification |
| `19-agent-task-recipes-recipe-create-a-connection-request` | structural | live verification |
| `19-agent-task-recipes-recipe-audit-agent-security` | structural | live verification |
| `19-agent-task-recipes-recipe-build-a-safe-public-agent` | structural | live verification |
| `19-agent-task-recipes-recipe-review-an-agent-answer` | structural | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `20-source-map-and-dependency-notes` | high | live verification |
