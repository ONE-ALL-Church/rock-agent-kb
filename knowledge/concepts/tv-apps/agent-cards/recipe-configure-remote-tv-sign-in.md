---
concept_id: tv-apps
task_id: recipe-configure-remote-tv-sign-in
title: Recipe: Configure remote TV sign-in
generated: true
---

# Recipe: Configure remote TV sign-in

A person can authenticate on a website and the TV client transitions to the configured success page.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Device`
- `Page`
- `Block`
- `Label`

## Entities And Tables

- `Person`
- `Device`
- `Page`
- `Block`
- `Label`

## Steps

1. Create an external website page containing the Remote Authentication block.
2. Associate the block with the intended TV application site.
3. Give the page a reachable route.
4. Select that website page as the application’s Authentication Page.
5. Create distinct TV pages for login display, timeout, and success.
6. Add the platform-specific QR-code and code placeholders or recognized Roku control IDs.
7. Add a `login` command with the three TV-page destinations.
8. Test QR navigation, manual-code entry, timeout, success, and Back behavior.
9. Test while signed out of the website and while already signed in.
10. Confirm the application record points to the intended external website Authentication Page.
11. Confirm that page contains the Remote Authentication block.
12. Confirm the block is associated with the correct TV application site.
13. Confirm the person can reach the website route.
14. For Apple TV, verify the login page contains the single-brace `{ authQrCodeUrl }` and `{ authCode }` placeholders.
15. For Roku, verify the page contains controls with IDs `lgnQrPoster` and `lgnCodeLabel`.
16. Confirm the login command targets the correct login, timeout, and success TV pages. Creating an Apple TV Sign-in Page

## Do Not Assume

- The application API key secures the website Remote Authentication page.
- The website Authentication Page and TV login-display page are the same page.
- A code from one device session can authenticate another.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/roku-docs/commands/personal
- https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries
- https://community.rockrms.com/developer/apple-tv-docs/styling/themes
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style
- https://community.rockrms.com/developer/roku-docs/commands/navigation
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Mobile/Cms/LavaApplicationContent.cs
