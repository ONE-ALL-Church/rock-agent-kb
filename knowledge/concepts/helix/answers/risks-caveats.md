---
id: answer:helix:risks-caveats
concept_id: helix
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Helix?

Treat every Helix endpoint as directly callable outside its front end: validate all inputs, enforce the caller's view or edit rights, avoid GET for mutations, and sanitize query and body values before SQL use. Lava javascript and stylesheet commands do not function in Helix endpoint templates because endpoint output is injected into the page by JavaScript, which prevents reliable detection of resources already present on the page. Helix does not support the Lava javascript and stylesheet commands because they depend on RockPage, which is unavailable when Helix dynamically replaces page regions. Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering.

## Top Claims

- `claim:72d56e7ee7ef0be4b92e`
- `claim:b297afe1c2b0a341ed44`
- `claim:c707a9d9cd2878d9e056`
- `claim:da56681f6277c12df324`

## Distilled Claims

- `distilled-claim:dc59b27ab0c0ccfc17c5`

## Citations

- [Security](https://community.rockrms.com/developer/helix/overview/security)
- [Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)
- [Limitations](https://community.rockrms.com/developer/helix/strategies/limitations)
