---
concept_id: tv-apps
task_id: recipe-make-an-apple-tv-page-theme-aware
title: Recipe: Make an Apple TV page theme-aware
generated: true
---

# Recipe: Make an Apple TV page theme-aware

One TVML page remains legible in both Light and Dark themes.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Apply global application styles through the documented site-style mechanism.
2. Add Light and Dark `tv-template` media-query rules for colors that need to change.
3. Use documented TVML text styles before introducing custom font choices.
4. Test the page in both user-selected themes.
5. If declaring a page-specific theme, retest all text, imagery, badges, and focus states.
6. Validate shadows and overlays for clipping.

## Do Not Assume

- HTML/CSS behavior transfers directly to TVML.
- A page-specific theme fixes hard-coded colors.
- Simulator appearance proves the final television presentation.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries
- https://community.rockrms.com/developer/apple-tv-docs/styling/themes
- https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/roku-docs/commands/navigation
