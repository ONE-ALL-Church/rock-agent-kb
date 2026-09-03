---
concept_id: tv-apps
task_id: recipe-add-tracked-media-playback-with-resume
title: Recipe: Add tracked media playback with resume
generated: true
---

# Recipe: Add tracked media playback with resume

A supported media resource plays and resumes according to an explicitly selected interaction strategy.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Choose a direct MP4 or HLS video URL, or a direct MP3 audio URL.
2. Prove playback with only the command and direct URL.
3. If the resource is a Rock Media Element, add its identifier.
4. Add title, subtitle, artwork, and description as needed.
5. Decide whether to resume from prior state or append to an existing interaction.
6. For resume-only, pass the prior watch map.
7. To append, pass both the prior interaction identifier and watch map.
8. Test first play, interrupted play, resumed play, and completion.
9. Confirm whether a new or existing interaction was expected.

## Do Not Assume

- A YouTube URL can be passed to the media command.
- A watch map alone appends to the original interaction.
- Playback success proves tracking success.

## Source Links

- https://community.rockrms.com/developer/roku-docs/commands/media
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands
