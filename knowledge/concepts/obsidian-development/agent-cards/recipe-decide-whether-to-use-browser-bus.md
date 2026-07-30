---
concept_id: obsidian-development
task_id: recipe-decide-whether-to-use-browser-bus
title: Recipe: Decide Whether To Use Browser Bus
generated: true
---

# Recipe: Decide Whether To Use Browser Bus

The browser bus is page-local only (Browser Bus).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Two independent components on the same page must communicate.
2. Parent/child props are not a natural fit.
3. The message is page-local.
4. The interaction is not security enforcement.
5. A server action should own the state.
6. Components have a clear parent/child relationship.
7. The message must cross browser tabs.
8. The message must persist.
9. The message controls authorization.

## Do Not Assume

- Do not use browser bus when:

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/obsidian/browser-bus
