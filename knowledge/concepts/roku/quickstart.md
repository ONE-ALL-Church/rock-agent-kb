---
concept_id: roku
title: Roku Apps Quickstart
generated: true
---

# Roku Apps Quickstart

Roku developer documentation for Rock-powered SceneGraph applications, pages, commands, controls, focus handling, media playback, layout nodes, resources, and operational guardrails.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Prepare A Roku Development Readiness Review](tasks/recipe-prepare-a-roku-development-readiness-review.md): A bounded determination of whether page development can begin.
- [Recipe: Author A Focusable Roku Page Skeleton](tasks/recipe-author-a-focusable-roku-page-skeleton.md): A SceneGraph page with a valid page root and deterministic initial focus.
- [Recipe: Build And Validate A Navigation Action](tasks/recipe-build-and-validate-a-navigation-action.md): A control that produces the intended navigation-stack behavior.
- [Recipe: Add Campus Or Other Application Context](tasks/recipe-add-campus-or-other-application-context.md): A selected value remains available to pages until the application closes or the context is cleared.
- [Recipe: Configure A Remote Login Journey](tasks/recipe-configure-a-remote-login-journey.md): A Roku login page displays a verification code and routes correctly on success or timeout.
- [Recipe: Configure Resumable Media Playback](tasks/recipe-configure-resumable-media-playback.md): A directly playable media resource starts correctly and uses the intended interaction history.
- [Recipe: Review A Roku-Related Lava Endpoint](tasks/recipe-review-a-roku-related-lava-endpoint.md): A public-safe inventory of the endpoint’s exposure, template, and enabled capabilities.

## High-Signal Sections

- `agent-summary` lines 18-33: Agent Summary (normal)
- `scope-and-boundaries` lines 34-60: Scope And Boundaries (normal)
- `mental-model` lines 61-75: Mental Model (normal)
- `getting-started-and-application-configuration` lines 76-98: Getting Started And Application Configuration (normal)
- `page-authoring-and-caching` lines 99-142: Page Authoring And Caching (normal)
- `scenegraph-controls-and-focus` lines 143-181: SceneGraph Controls And Focus (normal)

## Core Entities

- `Campus`: Rock concept/entity referenced by the roku guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the roku guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the roku guide.
- `Person`: Rock concept/entity referenced by the roku guide.

## Version Caveats


## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
