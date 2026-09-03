---
concept_id: apple-tv
task_id: recipe-implement-remote-sign-in
title: Recipe: Implement remote sign-in
generated: true
---

# Recipe: Implement remote sign-in

A viewer can authenticate from a phone or computer by scanning a QR code or entering a short code.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Device`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Device`
- `Page`
- `Block`

## Steps

1. Create an external Rock web page.
2. Add the Remote Authentication block.
3. Associate the block with the intended TV application site.
4. Establish the external URL or route.
5. Set that page as the application’s Authentication Page.
6. Create the TV login page.
7. Display `{ authQrCodeUrl }`, `{ authCode }`, and the external page URL.
8. Create a timeout page with a clear route home.
9. Select a success page.
10. Add the `login` command with the login, timeout, and success page GUIDs.
11. Retain navigation-stack clearing unless the tested journey requires otherwise.
12. Test QR, manual-code, timeout, failure, success, and Back-button paths.

## Do Not Assume

- Lava double braces work for the auth fields.
- A visible QR image proves authentication completion.
- A code remains valid beyond the configured lifetime.
- Source behavior from `develop` matches the installed release.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Security/Login/externalAuthenticationButtonBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/RemoteAuthentication/remoteAuthenticationAuthenticateResultBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/RemoteAuthentication/remoteAuthenticationOptionsBag.d.ts
