---
concept_id: cms-websites
task_id: recipe-publish-background-generated-video
title: Recipe: Publish background-generated video
generated: true
---

# Recipe: Publish background-generated video

A public page references a completed and readable media output.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Workflow`
- `Page`
- `Block`

## Steps

1. Start the background work through the owning workflow or provider integration.
2. Record explicit state and retry behavior.
3. Wait for a completed state rather than blocking the visitor request.
4. Verify the generated output and intended HLS, HD, or SD source.
5. Configure the Media Player shortcode with the reviewed source URL.
6. Test playback on the target page and visitor state.
7. Publish the link only after completion and playback verification.
8. Identify the workflow or provider job responsible for generation.
9. Record explicit queued, processing, retry, failed, and completed states.
10. Confirm retry limits and failure reporting.
11. Verify the output exists and is readable.
12. Test the public page or app that consumes it.
13. Publish the link only after completion and readback.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages
- https://community.rockrms.com/documentation
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/intro-to-pages
- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr
