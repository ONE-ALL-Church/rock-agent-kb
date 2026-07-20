---
id: answer:developer-resources:risks-caveats
concept_id: developer-resources
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Rock Developer Resources?

Helix applications require explicit security and data-integrity review because endpoint-backed application surfaces can expose data or perform work beyond static content rendering. Rock Mobile compatibility is two-dimensional: documentation uses `M` tags for minimum Mobile Shell versions and `C` tags for minimum Rock Core versions, and a feature may require both. Moving a Rock Mobile app from shell V5 or earlier to V6 or later changes the framework from Xamarin Forms to .NET MAUI; much XAML remains similar, but documented breaking layout behavior must be tested and adapted.

## Top Claims

- `claim:da56681f6277c12df324`
- `claim:896d78fdcfa734dde54e`
- `claim:dc73468ceef82ee62d45`

## Citations

- [Helix Security](https://community.rockrms.com/developer/helix/overview/security)
- [Core & Shell Dependencies](https://community.rockrms.com/developer/mobile-docs/developers/core-shell-dependencies)
- [Migrating to .NET MAUI (V6)](https://community.rockrms.com/developer/mobile-docs/essentials/tips-and-tricks/migrating-to-net-maui-v6)
