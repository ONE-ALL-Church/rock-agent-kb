---
concept_id: roku
task_id: recipe-configure-resumable-media-playback
title: Recipe: Configure Resumable Media Playback
generated: true
---

# Recipe: Configure Resumable Media Playback

A directly playable media resource starts correctly and uses the intended interaction history.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Reject YouTube as an input for the Rock Roku playback command.
2. Supply a direct MP4 or HLS URL for video, or MP3 for audio.
3. Add title, subtitle, artwork, and description when required.
4. Associate the Rock Media Element and related entity when applicable.
5. Decide whether resume should be enabled.
6. For resume-only behavior, supply the prior watch map.
7. To append progress to the prior interaction, supply both the watch map and interaction GUID.
8. Mark live video with the documented live-stream field when applicable.
9. Test playback, resume position, and resulting interaction behavior separately.

## Do Not Assume

- A browser-playable URL is reachable or playable on Roku.
- A watch map alone appends to the prior interaction.
- Resume enablement proves tracking.

## Source Links

- https://community.rockrms.com/developer/roku-docs/commands/media
