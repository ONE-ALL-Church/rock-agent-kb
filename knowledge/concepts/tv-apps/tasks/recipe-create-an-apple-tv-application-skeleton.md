---
concept_id: tv-apps
task_id: recipe-create-an-apple-tv-application-skeleton
title: Recipe: Create an Apple TV application skeleton
generated: true
---

# Recipe: Create an Apple TV application skeleton

A Rock-managed Apple TV application with a valid Start Screen and explicitly reviewed application settings.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Confirm Rock 14 or later.
2. Open `Admin Tools > CMS Configuration > Apple TV Apps`.
3. Create the application with an internal name and optional description.
4. Review global styles, page-view tracking, retention, API key, and Authentication Page.
5. Save and open the generated Start Screen.
6. Add the smallest valid TVML document that the target shell can render.
7. Test the Start Screen in the target Apple TV client.
8. Identify the target platform.
9. Confirm the installed Rock version: Apple TV requires Rock 14 or later; Roku requires Rock 16.7 or later.
10. Confirm that the expected TV application administration blocks and site types exist in the installed package.
11. Confirm the operator has permission to view and administer the relevant CMS configuration pages.
12. For Roku development, verify whether the current Core-team development-application process is required and has been completed.
13. Stop page-level debugging until the application record can be opened. Apple TV Docs Roku Docs

## Do Not Assume

- The Rock-side name becomes the App Store name.
- Saving the Rock record packages or publishes an App Store application.
- Browser-valid markup is valid TVML.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app
- https://community.rockrms.com/developer/apple-tv-docs/styling/themes
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://community.rockrms.com/developer/apple-tv-docs
- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/roku-docs/getting-started
