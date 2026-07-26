# Reviewed Lava Context Extensions

This directory accepts reviewed public manifests for Lava contexts implemented
outside Rock core.

A public extension must:

- cite intentionally public source code in an HTTPS repository;
- pin a 40-character commit SHA and source line range;
- declare a compatible public license and license URL;
- attest that the source and metadata contain no private Rock data;
- use organization-namespaced context IDs such as `example-org:custom-label`;
- describe availability conditions, nullability, settings, execution phase, and
  coverage conservatively;
- link a Model Map slug only when the root type is clear; and
- complete maintainer review before entering this directory.

Validate a manifest with:

```bash
uv run kb lava contexts-validate-extension lava-contexts/extensions/<org-id>/<manifest>.json
```

Unreviewed suggestions belong under `source-suggestions/<org-id>/` or
`community-contributions/<org-id>/`. Private instance contexts belong in a
permission-scoped private overlay and are never copied into this directory.
