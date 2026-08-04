---
concept_id: content-personalization
task_id: recipe-diagnose-editor-cannot-see-channel-in-tools-content
title: Recipe: Diagnose “editor cannot see channel in Tools > Content”
generated: true
---

# Recipe: Diagnose “editor cannot see channel in Tools > Content”

The `Tools > Content` page lists channels the current user has View access to, according to official docs (Manage Content Items).

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

1. Does the channel exist?
2. Does the editor have View access to the channel?
3. Is the channel hidden by any filter/toggle in `Tools > Content`?
4. Is the editor expecting pending-only view?
5. Does the editor need Edit or Approval rights for the action?
6. Is there a security inheritance issue?
7. Is the instance on a version affected by content channel block permission bugs?

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageRenderer.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageChangeHandler.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/FileAssetManager.cs
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/secure-content
- https://community.rockrms.com/documentation/digital-publishing/content-management/dynamic-content/manage-content-items
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-content-channel-items
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/use-content-channels
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/configure-site-for-personalization
- https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Cms/StructuredContent/BlockTypes/ImageDataFile.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemList/getLinkedMediaElementsResponseBag.d.ts
