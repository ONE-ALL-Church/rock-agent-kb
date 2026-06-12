# Rock Model Map

This generated resource is built from scraped generic Rock Model Map pages, not from a local SQL schema snapshot.

## How To Use This

- Use `stable-models.jsonl` for the preferred stable generic Rock model landmarks.
- Use `stable-properties.jsonl` for stable per-model property flags, descriptions, enum values, and related entity link text from the scraped Model Map.
- Use `models/*.md` for direct human-readable stable model detail pages.
- Use `version-diff.jsonl`, `latest-models.jsonl`, and `latest-properties.jsonl` only to call out pre-alpha/upcoming differences.
- For database columns in a specific Rock instance, verify against that instance's schema separately; this public layer intentionally avoids organization-specific SQL metadata.

## Tracks

| Track | Rock Version | Source | Models | Properties |
| --- | --- | --- | ---: | ---: |
| Stable | `18.2.4` | [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map) | 321 | 15895 |
| Pre-alpha / upcoming | `20.0.3` | [Model Map](https://rockrmslatest.com/admin/power-tools/model-map) | 325 | 16093 |

## Stable Coverage

- Models: 321
- Properties: 15895
- Database-marked properties: 6645
- Lava-marked properties: 11199
- Lava-marked non-database properties: 4622
- NotMapped properties: 9250

## Pre-Alpha Difference Callouts

- Total changes: 299
- Models added: 5
- Models removed: 1
- Properties added: 71
- Properties removed: 32
- Properties changed: 190

## Largest Stable Models

| Model | Category | Properties | DB | Lava | NotMapped | Obsolete |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Financial Transaction](models/financial-transaction.md) | Finance | 232 | 38 | 66 | 47 | 0 |
| [Financial Scheduled Transaction](models/financial-scheduled-transaction.md) | Finance | 223 | 32 | 53 | 39 | 0 |
| [Person](models/person.md) | CRM | 203 | 72 | 123 | 71 | 0 |
| [Financial Person Saved Account](models/financial-person-saved-account.md) | Finance | 188 | 22 | 38 | 31 | 0 |
| [Group Type](models/group-type.md) | Group | 155 | 88 | 116 | 50 | 0 |
| [Learning Class](models/learning-class.md) | LMS | 140 | 64 | 99 | 62 | 0 |
| [Analytics Dim Family Head Of Household](models/analytics-dim-family-head-of-household.md) | Reporting | 132 | 81 | 87 | 13 | 0 |
| [Analytics Dim Person Current](models/analytics-dim-person-current.md) | Reporting | 132 | 81 | 87 | 13 | 0 |
| [Analytics Dim Person Historical](models/analytics-dim-person-historical.md) | Reporting | 132 | 81 | 87 | 13 | 0 |
| [Group](models/group.md) | Group | 129 | 61 | 93 | 54 | 0 |
| [Registration Template](models/registration-template.md) | Event | 125 | 70 | 95 | 41 | 0 |
| [Workflow Action Form](models/workflow-action-form.md) | Workflow | 121 | 48 | 72 | 39 | 0 |
| [Site](models/site.md) | CMS | 108 | 54 | 88 | 53 | 0 |
| [Attendance](models/attendance.md) | Event | 96 | 39 | 65 | 43 | 0 |
| [Communication](models/communication.md) | Communication | 94 | 53 | 76 | 41 | 0 |
| [Analytics Source Person Historical](models/analytics-source-person-historical.md) | Reporting | 94 | 43 | 49 | 13 | 0 |
| [Analytics Fact Financial Transaction](models/analytics-fact-financial-transaction.md) | Reporting | 86 | 48 | 56 | 15 | 0 |
| [Registration Instance](models/registration-instance.md) | Event | 85 | 37 | 54 | 34 | 0 |
| [Page](models/page.md) | CMS | 84 | 45 | 66 | 38 | 0 |
| [Location](models/location.md) | Core | 84 | 39 | 66 | 42 | 0 |
| [Communication Template](models/communication-template.md) | Communication | 80 | 41 | 63 | 39 | 0 |
| [Interaction Channel](models/interaction-channel.md) | Core | 76 | 34 | 50 | 31 | 0 |
| [Benevolence Request](models/benevolence-request.md) | Finance | 76 | 28 | 50 | 40 | 0 |
| [Learning Participant](models/learning-participant.md) | LMS | 75 | 36 | 58 | 39 | 0 |
| [Analytics Source Financial Transaction](models/analytics-source-financial-transaction.md) | Reporting | 74 | 36 | 44 | 15 | 0 |

## Category Slices

- [AI](concept-slices/ai.md) - 8 models
- [CMS](concept-slices/cms.md) - 37 models
- [CRM](concept-slices/crm.md) - 15 models
- [Check -in](concept-slices/check-in.md) - 1 models
- [Communication](concept-slices/communication.md) - 23 models
- [Core](concept-slices/core.md) - 76 models
- [Engagement](concept-slices/engagement.md) - 27 models
- [Event](concept-slices/event.md) - 30 models
- [Finance](concept-slices/finance.md) - 21 models
- [Group](concept-slices/group.md) - 19 models
- [LMS](concept-slices/lms.md) - 14 models
- [Meta](concept-slices/meta.md) - 3 models
- [Prayer](concept-slices/prayer.md) - 1 models
- [Reporting](concept-slices/reporting.md) - 30 models
- [Security](concept-slices/security.md) - 1 models
- [Web Farm](concept-slices/web-farm.md) - 3 models
- [Workflow](concept-slices/workflow.md) - 12 models

## Regeneration

```bash
uv run kb modelmap build
uv run kb build --stage agent-pack
uv run kb publish export
```
