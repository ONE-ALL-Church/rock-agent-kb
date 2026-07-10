# Community Recipe Contract

A recipe is a reusable Rock implementation pattern with enough code, context,
security guidance, and validation detail for another organization to build its
own version. Recipes are community evidence, not official Rock documentation.

## Ownership Model

The code owner keeps substantial implementation files in a public repository
they control. The Rock KB stores a structured digest and an immutable commit
pin. This keeps attribution, issues, releases, and code maintenance with the
owner while making the reusable pattern discoverable to agents.

One public recipe repository per organization is usually sufficient. Use a
separate repository only when a project needs independent ownership, release,
or security boundaries.

Every recipe must declare:

- a public HTTPS GitHub repository and owner;
- an exact 40-character commit SHA, never only `main` or a mutable tag;
- a source directory, machine-readable manifest, license, and file hashes;
- concept routes, use cases, outcomes, prerequisites, and adaptation points;
- data access, authentication, authorization, CSRF, and sensitive-data notes;
- tested Rock versions, last verification date, limitations, validation, and
  rollback steps;
- a version matrix that distinguishes verified, expected, and unsupported Rock
  releases, plus a public feedback or issue URL when one exists;
- optional release history and consumer verification attestations recording the
  organization, Rock version, date, outcome, and verification scope;
- reusable learnings that explain why the implementation is structured this
  way, not only what files to copy.

Supported ingestion modes are:

- `link_only`: index metadata and links when the license does not permit more.
- `index_documentation`: index the owner-written description and file inventory
  while leaving code in the owner repository. This is the normal default.
- `snapshot_source`: copy source only when its license and maintainer policy
  explicitly permit a public snapshot.

## Agent Retrieval

Use exact retrieval when the recipe ID is known:

```bash
uvx rock-kb recipes list
uvx rock-kb recipes list --concept check-in
uvx rock-kb recipes search "registration attendance dashboard"
uvx rock-kb recipe oneall:check-in-status-dashboard
uvx rock-kb recipe oneall:registration-to-connection-request
uvx rock-kb recipe verify oneall:check-in-status-dashboard --rock-version 18
```

With MCP, use `kb_list_recipes`, `kb_get_recipe`, and `kb_verify_recipe`. A recipe result includes
the source pin, file inventory, adaptation points, security boundary,
compatibility, instructions, validation steps, limitations, and learnings.

Agents should use a recipe as a starting pattern, not deploy it blindly. Verify
the target Rock version and local configuration, preserve its security
boundary, and cite the community trust tier.

Recipe verification is deliberately read-only. It confirms the immutable
source hashes, declared target-version compatibility, and available verifier
files. It does not execute community code or modify a Rock instance.

## Contributing A Recipe

1. Sanitize and publish the implementation in a licensed public repository.
   Remove production IDs, routes, people, secrets, private paths, and private
   evidence.
2. Add a `recipe.json` manifest in the recipe directory. The external manifest
   may use `rock-kb-external-recipe-v1`; the KB submission carries the complete
   `rock-kb-recipe-v1` record.
3. Commit the files and calculate SHA-256 hashes for every indexed file.
4. Create a normal `rock-kb-org-contribution-v1` bundle row with
   `contribution_type: recipe`. Set `contribution_id` equal to `recipe_id` and
   include the complete record in the `recipe` field.
5. Validate and submit through GitHub or the hosted token flow. Do not edit
   `recipes/`, `agent/`, or `knowledge/recipes/` directly in a contributor PR.

After review, a maintainer promotes the nested recipe record and rebuilds:

```bash
uv run kb recipes promote community-contributions/<org-id>/bundle.jsonl <org-id>:<recipe-slug>
uv run kb recipes validate
uv run kb recipes build
uv run kb recipes check-upstream
uv run kb recipes verify <org-id>:<recipe-slug> --rock-version 18
uv run kb build --stage agent-pack
uv run kb publish export
uv run kb audit public-export
```

The generated public surfaces are `agent/recipes.jsonl` and
`knowledge/recipes/<org-id>/<recipe-slug>.md`.

## Staleness

Normal builds are deterministic and do not contact external repositories.
`uv run kb recipes check-upstream` compares each indexed file hash with that
path on the repository's default branch. This avoids false staleness when an
unrelated recipe changes in the same repository. `upstream_changed` means a
maintainer should inspect the new version, update compatibility and file hashes,
and repin intentionally. It does not automatically replace reviewed content.

Consumer attestations are evidence, not authority promotion. A passing
attestation says a named adaptation was tested on a declared Rock version and
scope; it does not make the recipe official or guarantee another instance's
configuration.
