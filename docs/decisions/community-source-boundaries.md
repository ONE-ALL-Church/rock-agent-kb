# Community Source Boundaries

The `rock_community_site` source is a residual source, not a broad owner for every
page under `community.rockrms.com`.

Narrower source families own their own paths:

- `rock_documentation` owns `/documentation`.
- `rock_developer` owns general `/developer` docs except paths split into narrower sources.
- `rock_mobile_docs` owns `/developer/mobile-docs`.
- `rock_lava_docs` owns `/lava`.
- `rock_api_docs` owns `/api-docs`.
- `rock_recipes`, `rock_qa`, `rock_rocku`, and `rock_community_hubs` own their matching paths.

`rock_community_site` should only keep leftover public pages that are useful to
agents and not covered by a narrower source family, currently `/learn`,
`/podcast`, and `/styling`.

Do not add `/subscriptions` back to `rock_community_site`. Recent refresh testing
found many slow low-value subscription URLs, and they caused the residual site
refresh to stall. If subscription material becomes useful for Rock implementation
guidance, add a dedicated `rock_subscriptions` source with its own scope,
timeouts, tests, and source-quality review rather than hiding it inside the
residual site crawl.
