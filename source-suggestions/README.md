# Source Suggestions

Use this folder for lightweight source-discovery notes when a full contribution bundle is not ready.

Source suggestions submitted by GitHub PR do not need a Rock KB submit token. The contributor only needs GitHub access to open a PR.

Preferred path:

```text
source-suggestions/<org-id>/<short-topic>.md
```

The fastest start is to copy the template:

```bash
mkdir -p source-suggestions/<org-id>
cp source-suggestions/SUGGESTION_TEMPLATE.md source-suggestions/<org-id>/<short-topic>.md
```

Each suggestion should include:

- Source URL.
- Why it matters to Rock RMS knowledge work.
- Relevant concept IDs if known.
- Rock version or plugin scope if version-specific.
- Whether the source is official, RockU, release notes, source code, community pattern, vendor/partner material, or org-local evidence.
- Any license or reuse caveats.

Do not include raw private docs, copied proprietary text, transcripts, SQL exports, screenshots with private data, internal URLs, secrets, or live Rock IDs.

Maintainers convert accepted source suggestions into source registry updates, approved claims, or reviewed contribution rows before they affect public guides.
