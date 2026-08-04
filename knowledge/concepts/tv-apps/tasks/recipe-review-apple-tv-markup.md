---
concept_id: tv-apps
task_id: recipe-review-apple-tv-markup
title: Recipe: Review Apple TV Markup
generated: true
---

# Recipe: Review Apple TV Markup

Sources: Apple TV Tips, Apple TV Templates.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Document root is valid TVML.
2. Template matches content type.
3. Dynamic text is escaped.
4. Images are supported formats, not SVG.
5. No WebView assumptions.
6. Theme styles are valid.
7. Text overflow is handled.
8. Large images are compressed/resized.
9. Commands are valid for the shell.
10. Media URLs are not YouTube links.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates
