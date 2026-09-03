---
concept_id: apple-tv
task_id: recipe-add-tracked-video-or-audio-playback
title: Recipe: Add tracked video or audio playback
generated: true
---

# Recipe: Add tracked video or audio playback

A supported media file plays with intentional resume and interaction behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Select `playVideo` for MP4 or HLS, or `playAudio` for MP3.
2. Supply the direct media URL.
3. Add title, subtitle, artwork, and description when required.
4. Associate the Rock Media Element and related entity when watch tracking requires them.
5. Decide the interaction outcome before adding resume parameters.
6. Add `rockWatchMap` when a prior resume position is required.
7. Add `rockInteractionGuid` only when progress must append to that existing interaction.
8. Test initial playback.
9. Stop partway through and retest resume.
10. Verify whether the expected interaction was appended or newly created.
11. Confirm the command is `playVideo` or `playAudio`.
12. Confirm video uses a direct MP4 or HLS source.
13. Confirm audio uses a direct MP3 source.
14. Reject YouTube as a supported source for these commands.
15. Inspect the exact media URL and metadata parameters.
16. If Rock watch tracking is expected, inspect the Media Element and related-entity parameters.
17. Test the same media without interaction parameters to separate playback failure from tracking failure.

## Do Not Assume

- YouTube is supported.
- A watch map alone appends to the old interaction.
- Successful playback proves tracking succeeded.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands
