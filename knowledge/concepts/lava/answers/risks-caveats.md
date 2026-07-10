---
id: answer:lava:risks-caveats
concept_id: lava
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Lava?

Rock v19 adds a contains parameter to the Lava where filter for partial field matching rather than only equality comparisons. Confirm case, type and performance behavior with current Lava documentation before using it in broad queries. Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. Rock v19 materializes recurring iCal schedule occurrences into ScheduleDate rows so date-based SQL and Lava queries can avoid repeatedly expanding recurrence rules. Use the generated dates rather than inventing a separate recurrence expansion process. When reviewing an Advanced HTML block, inspect page/block security, enabled Lava commands, query-string or context inputs, and whether the output exposes sensitive entity data.

## Top Claims

- `claim:524be15ef7a48290a72a`
- `claim:410bf6750e90b7193262`
- `claim:4c4098a035a5ca256bfe`
- `claim:7e6e3979faad614f0b42`
- `claim:32f0173b23a7d2c356c0`

## Distilled Claims

- `distilled-claim:018890c9ff7df61a429b`

## Citations

- [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1080s) (`18:00`)
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
- [3 Underrated Features Churches Are Overlooking | Ep 217](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s) (`06:26`)
- [Advanced HTML Block](https://community.rockrms.com/rocku/cms/advanced-html-block) (`00:00`)
- [3 Underrated Features Churches Are Overlooking | Ep 217](https://shows.acast.com/rock-cast/episodes/3-underrated-features-ep-217) (`06:26`)
