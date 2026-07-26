# Lava Context Directory

The Lava context directory answers a narrower question than the Model Map:
which root values are available in a specific Rock rendering surface?

Use exact grouped retrieval before generic search:

```bash
uvx rock-kb lava-context list --family check-in-label
uvx rock-kb lava-context get check-in-label-family-dynamic-text
uvx rock-kb lava-context get check-in-label-checkout-dynamic-text --root CheckoutDateTime
```

MCP clients use `kb_list_lava_contexts` and `kb_get_lava_context`. Generic
`kb_search` remains useful when the surface name or context ID is unknown.

## Reading A Result

- `roots` contains direct and explicitly inherited roots.
- `defined_in_context_id` identifies the context that declares each root.
- `inherited` distinguishes composed common fields from surface-specific fields.
- `coverage_status` states whether the source-backed extraction is complete for
  the pinned source snapshot, curated, partial, or dynamic.
- `availability_condition`, `required_setting`, `execution_phase`, and
  `may_be_null` describe when a root is available or populated.
- `model_map_links` points to model details only when the type relationship is
  clear.
- `source_commit`, `source_version`, and the pinned `source_url` make source
  changes and version drift reviewable.
- `needs_live_verification` marks configuration-dependent behavior.

`complete_for_source_snapshot` means all explicit roots recognized in that
source contract were captured. It does not mean every root has a non-null value
in every request. A missing root in a `partial_curated` or `dynamic` surface is
not proof that Rock can never provide it.

## Agent Workflow

1. Identify the exact rendering surface.
2. Get the grouped Lava context and inspect conditions and coverage.
3. Follow a linked Model Map slug to inspect object properties and relationships.
4. Use Lava capabilities for filters, commands, syntax, and security behavior.
5. Cite the pinned public source or official documentation in the final answer.
6. Check the target Rock version and live configuration when marked.

Do not infer roots from the Model Map alone. A model can exist without being
placed in a particular Lava context.

## Maintainer Workflow

Refresh and rebuild the public source-backed directory:

```bash
uv run kb lava contexts-refresh-source
uv run kb lava contexts-build --skip-fetch
uv run kb lava contexts-list
uv run kb lava contexts-get check-in-label-checkout-dynamic-text
```

The refresh resolves the configured upstream branch to one immutable commit,
records the observed Rock version, and downloads every tracked source file from
that commit. Generated row IDs exclude line numbers, so source movement does not
break exact IDs; old line-based IDs remain aliases.

To find possible omissions in a public Rock source checkout:

```bash
uv run kb lava contexts-discover /path/to/public/Rock/source
```

Discovery output is a private review queue, not publishable evidence. Every
candidate requires call-path, condition, type, and source review before adding a
tracked parser or curated context.

## Community Extensions

Organization-specific contexts must remain in a private overlay unless their
source is intentionally public, licensed, redacted, pinned to a commit, and
reviewed. Public extension manifests live under
`lava-contexts/extensions/<org-id>/` and validate with:

```bash
uv run kb lava contexts-validate-extension lava-contexts/extensions/<org-id>/<manifest>.json
```

Private overlays validate separately:

```bash
uv run kb lava contexts-validate-overlay /path/to/private-overlay.jsonl
```

Private overlays are never loaded into the public generator or public vector
index. Scanner output, instance identifiers, queries, logs, secrets, and local
paths are not public evidence.

## Verification

After changes:

```bash
pytest
python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit source-url-duplicates
uv run kb audit public-export
```
