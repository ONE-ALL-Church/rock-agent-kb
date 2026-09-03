---
concept_id: apple-tv
task_id: recipe-prepare-the-application-image-package
title: Recipe: Prepare the application image package
generated: true
---

# Recipe: Prepare the application image package

A delivery set contains the documented icon, launch, Top Shelf, and optional parallax assets.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Create three-layer app icons.
2. Export PNG foreground layers and a JPG background layer.
3. Export icon sets at 400 × 240, 800 × 480, and 1280 × 768.
4. Export static launch images at 1920 × 1080 and 3840 × 2160.
5. If Top Shelf assets are required, export the documented standard or wide PNG sizes.
6. If content parallax is required, produce an LCR file.
7. Host the LCR at a direct URL.
8. Verify that no LSR file was substituted.
9. Test focus, parallax, and launch appearance in the target shell.
10. Reconfirm current Apple packaging requirements before final submission.

## Do Not Assume

- Flattened icons retain parallax.
- LSR works in place of LCR.
- Historical Top Shelf dimensions are current App Store requirements.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/top-shelf-image
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/launch-image
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/parallax-images
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/application-images/app-icons
