# Organization Registry

This folder is the planned public registry for organizations that contribute Rock KB bundles.

Milestone 0.5 does not auto-trust any organization. Until the registry validator and server-side GitHub rulesets are active, all contribution PRs need maintainer review even when they touch only `community-contributions/<org-id>/` or `source-suggestions/<org-id>/`.

Future registration files should use:

```text
orgs/<org-id>.yaml
```

Use a stable lowercase `org-id` with letters, numbers, dashes, or underscores. The same id should be used for:

```text
community-contributions/<org-id>/bundle.jsonl
source-suggestions/<org-id>/
```

Do not include private database details, instance URLs, staff contact details, access tokens, internal repo links, or confidential operational context in registry files. Public contact and GitHub organization/team handles are acceptable when the contributor wants them public.
