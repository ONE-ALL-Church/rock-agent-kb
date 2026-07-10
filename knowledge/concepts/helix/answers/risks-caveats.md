---
id: answer:helix:risks-caveats
concept_id: helix
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Helix?

Lava javascript and stylesheet commands do not function in Helix endpoint templates because endpoint output is injected into the page by JavaScript, which prevents reliable detection of resources already present on the page. Helix does not support the Lava javascript and stylesheet commands because they depend on RockPage, which is unavailable when Helix dynamically replaces page regions. Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering.

## Top Claims

- `claim:b297afe1c2b0a341ed44`
- `claim:c707a9d9cd2878d9e056`
- `claim:da56681f6277c12df324`

## Citations

- [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)
- [Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)
- [Helix Security](https://community.rockrms.com/developer/helix/overview/security)
