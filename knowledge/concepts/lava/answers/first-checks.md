---
id: answer:lava:first-checks
concept_id: lava
generated: true
artifact_level: answer
---

# What should I check first for Lava?

When using Lava to expose API-style endpoints, treat Lava webhooks as custom integration surfaces: verify security explicitly, especially for TV app or channel scenarios, before exposing data or commands. Rock v19 materializes recurring iCal schedule occurrences into ScheduleDate rows so date-based SQL and Lava queries can avoid repeatedly expanding recurrence rules. Use the generated dates rather than inventing a separate recurrence expansion process. Roku app pages should be reviewed as Lava-generated SceneGraph output, not normal CMS HTML, so agents should validate the TV application record, page Lava, and command behavior together. Advanced HTML Block adds public-safe guidance for CMS security and Lava review: block authorship is privileged, and agents should inspect enabled commands, context inputs, and page/block authorization.

## Top Claims

- `claim:524be15ef7a48290a72a`
- `claim:5d109547ddfc0fd7b9c2`
- `claim:4b7b8d0b0379ceb7587f`
- `claim:5d8bddb267bffde3cfe7`
- `claim:c3921cb1d8b61e06c713`
- `claim:4bf4025847cf0c78adf0`
- `claim:2d534c63c723204ad8c9`
- `claim:3b4b8ec335aa0a17968c`

## Distilled Claims

- `distilled-claim:018890c9ff7df61a429b`
- `distilled-claim:0fdef944e805ef0178c0`
- `distilled-claim:1b24fed3c10b3e77023a`
- `distilled-claim:76309df0960788340bf4`

## Citations

- [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1080s) (`18:00`)
- [Workflow Activate](https://community.rockrms.com/lava/commands/workflow-activate-commands)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s) (`87:48`)
- [Other](https://community.rockrms.com/lava/filters/other-filters)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s) (`71:20`)
- [Entity](https://community.rockrms.com/lava/commands/entity-commands)
- [Content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)
- [Lava](https://community.rockrms.com/developer/mobile-docs/essentials/lava)
