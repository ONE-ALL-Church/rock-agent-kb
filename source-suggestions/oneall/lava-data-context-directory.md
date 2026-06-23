# Lava Data Context Directory Source Suggestion

## Source URLs

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelField.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/FieldSourceHelper.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs
- https://github.com/SparkDevNetwork/Rock/tree/develop/Rock/Blocks/Types/Mobile
- https://github.com/SparkDevNetwork/Rock/tree/develop/RockWeb/Blocks

## Why It Matters

Rock has many text/template fields that render Lava with a context-specific set of root objects. The current public knowledge surfaces explain Lava, models, commands, and specific features, but agents still need a directory that answers: "what objects are available in this particular UI field, system communication, workflow action, label, or block template?"

This should become a permanent KB fixture adjacent to the model map:

- The context directory answers which root objects exist in a surface.
- The model map answers which properties and relationships are available once a root object is known.
- Curated contracts should cover high-value contexts such as common merge fields, Check-In Label Designer Dynamic Text, communication recipients, workflow actions/forms, CMS/content channel templates, mobile block templates, group scheduling emails, finance receipts/statements, reporting blocks, and badges.

## Relevant Concept IDs

- `lava`
- `check-in`
- `workflows`
- `communications`
- `cms-websites`
- `mobile`
- `data-views-reports`
- `giving-finance`
- `groups`

## Source Type

Official source code, source-code-confirmed. The ONE&ALL repo has a generated scanner output that can be used as a local development aid, but the public KB should cite upstream Rock source files rather than local private evidence.

## Version Scope

Version-sensitive. The pattern is stable across Rock, but exact context roots and label data properties can change by Rock version. Generated rows should include source branch/tag or Rock version.

## Suggested KB Shape

- Create a concept guide named something like "Lava Data Contexts and Merge Field Roots."
- Add a generated artifact keyed by context family, source file, source scope, merge field key, and source line.
- Link each root object to Model Map digests when possible.
- Promote only reviewed high-value contracts into claims; keep raw inventory rows as source-backed lookup data.

## Reuse Caveats

Do not include private instance IDs, raw task evidence, internal URLs, SQL exports, screenshots, or organization-specific templates. Public contribution should be source-code based and should not quote large source blocks.
