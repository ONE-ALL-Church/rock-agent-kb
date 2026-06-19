# Rock Model Map

This generated resource is built from authenticated Obsidian block-action responses from generic Rock Model Map pages, not from a local SQL schema snapshot.

## How To Use This

- Use `stable-models.jsonl` for the preferred stable generic Rock model landmarks.
- Use `stable-properties.jsonl` for stable per-model property flags, descriptions, enum values, and related entity link text from the scraped Model Map.
- Use `stable-methods.jsonl` for stable method signatures, inheritance, and obsolete-method callouts from the model detail payload.
- Use `models/*.md` for direct human-readable stable model detail pages.
- Use `version-diff.jsonl`, `latest-models.jsonl`, and `latest-properties.jsonl` only to call out pre-alpha/upcoming differences.
- For database columns in a specific Rock instance, verify against that instance's schema separately; this public layer intentionally avoids organization-specific SQL metadata.

## Tracks

| Track | Rock Version | Source | Models | Properties |
| --- | --- | --- | ---: | ---: |
| Stable | `19.1.8` | [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map) | 326 | 16111 |
| Pre-alpha / upcoming | `20.0.4` | [Model Map](https://rockrmslatest.com/admin/power-tools/model-map) | 325 | 16100 |

## Stable Coverage

- Models: 326
- Properties: 16111
- Database-marked properties: 6754
- Lava-marked properties: 11358
- Lava-marked non-database properties: 4677
- NotMapped properties: 9357
- Enum properties: 208
- DefinedValue properties: 106
- Method signatures: 10665
- Models with API table name: 1
- Models missing API table name: 325
- Obsolete models: 1

## Pre-Alpha Difference Callouts

- Total changes: 84
- Models added: 0
- Models removed: 1
- Properties added: 9
- Properties removed: 17
- Properties changed: 57

## Largest Stable Models

| Model | Category | Properties | DB | Lava | NotMapped | Obsolete |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Person](models/person.md) | CRM | 148 | 77 | 125 | 71 | 2 |
| [Group Type](models/group-type.md) | Group | 135 | 86 | 113 | 49 | 0 |
| [Learning Class](models/learning-class.md) | LMS | 126 | 64 | 99 | 62 | 3 |
| [Group](models/group.md) | Group | 115 | 61 | 93 | 54 | 3 |
| [Registration Template](models/registration-template.md) | Event | 113 | 72 | 97 | 41 | 1 |
| [Site](models/site.md) | CMS | 107 | 54 | 88 | 53 | 1 |
| [Communication](models/communication.md) | Communication | 94 | 53 | 76 | 41 | 2 |
| [Analytics Dim Family Head Of Household](models/analytics-dim-family-head-of-household.md) | Reporting | 94 | 81 | 87 | 13 | 0 |
| [Analytics Dim Person Current](models/analytics-dim-person-current.md) | Reporting | 94 | 81 | 87 | 13 | 0 |
| [Analytics Dim Person Historical](models/analytics-dim-person-historical.md) | Reporting | 94 | 81 | 87 | 13 | 0 |
| [Financial Transaction](models/financial-transaction.md) | Finance | 85 | 38 | 66 | 47 | 2 |
| [Workflow Action Form](models/workflow-action-form.md) | Workflow | 85 | 47 | 70 | 38 | 0 |
| [Page](models/page.md) | CMS | 83 | 45 | 66 | 38 | 3 |
| [Attendance](models/attendance.md) | Event | 82 | 39 | 65 | 43 | 0 |
| [Location](models/location.md) | Core | 81 | 39 | 66 | 42 | 0 |
| [Communication Template](models/communication-template.md) | Communication | 80 | 41 | 63 | 39 | 2 |
| [Learning Participant](models/learning-participant.md) | LMS | 75 | 36 | 58 | 39 | 0 |
| [Attribute](models/attribute.md) | Core | 73 | 43 | 59 | 30 | 0 |
| [Interactive Experience](models/interactive-experience.md) | Event | 73 | 39 | 58 | 34 | 0 |
| [Achievement Type](models/achievement-type.md) | Engagement | 72 | 33 | 56 | 39 | 0 |
| [Connection Request](models/connection-request.md) | Engagement | 72 | 29 | 55 | 43 | 0 |
| [Metric YTD Data](models/metric-ytd-data.md) | Reporting | 72 | 36 | 57 | 36 | 0 |
| [Content Channel Item](models/content-channel-item.md) | CMS | 71 | 31 | 52 | 40 | 0 |
| [Registration Instance](models/registration-instance.md) | Event | 71 | 37 | 54 | 34 | 0 |
| [Financial Scheduled Transaction](models/financial-scheduled-transaction.md) | Finance | 71 | 32 | 53 | 39 | 1 |

## Category Slices

- [AI](concept-slices/ai.md) - 8 models
- [CMS](concept-slices/cms.md) - 37 models
- [CRM](concept-slices/crm.md) - 15 models
- [Check-in](concept-slices/check-in.md) - 1 models
- [Communication](concept-slices/communication.md) - 22 models
- [Core](concept-slices/core.md) - 76 models
- [Engagement](concept-slices/engagement.md) - 32 models
- [Event](concept-slices/event.md) - 30 models
- [Finance](concept-slices/finance.md) - 21 models
- [Group](concept-slices/group.md) - 19 models
- [LMS](concept-slices/lms.md) - 14 models
- [Meta](concept-slices/meta.md) - 3 models
- [Other](concept-slices/other.md) - 1 models
- [Prayer](concept-slices/prayer.md) - 1 models
- [Reporting](concept-slices/reporting.md) - 30 models
- [Security](concept-slices/security.md) - 1 models
- [WebFarm](concept-slices/webfarm.md) - 3 models
- [Workflow](concept-slices/workflow.md) - 12 models

## Regeneration

```bash
uv run kb modelmap build
uv run kb build --stage agent-pack
uv run kb publish export
```
