---
id: answer:lava:first-checks
concept_id: lava
generated: true
artifact_level: answer
---

# What should I check first for Lava?

When using Lava to expose API-style endpoints, treat Lava webhooks as custom integration surfaces: verify security explicitly, especially for TV app or channel scenarios, before exposing data or commands. Roku app pages should be reviewed as Lava-generated SceneGraph output, not normal CMS HTML, so agents should validate the TV application record, page Lava, and command behavior together. Advanced HTML Block adds public-safe guidance for CMS security and Lava review: block authorship is privileged, and agents should inspect enabled commands, context inputs, and page/block authorization.

## Top Claims

- `claim:410bf6750e90b7193262`
- `claim:563e520ec15928e19628`
- `claim:5bd2b6b4cac279be5e13`
- `claim:7e6e3979faad614f0b42`
- `claim:940f299b268510da61d8`
- `claim:4c6c24811261384a0eb4`
- `claim:f34b7d439fac6c9062f0`
- `claim:ffba67d8847c47e68ea6`

## Distilled Claims

- `distilled-claim:018890c9ff7df61a429b`
- `distilled-claim:1b24fed3c10b3e77023a`
- `distilled-claim:76309df0960788340bf4`

## Citations

- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
- [Roku Pages](https://community.rockrms.com/developer/roku-docs/getting-started/pages)
- [Apple TV Pages](https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages)
- [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block) (`00:00`)
- [Helix Overview](https://community.rockrms.com/developer/helix/overview)
- [Media Watch](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) (`07:12`)
