---
concept_id: apple-tv
task_id: recipe-review-a-lava-api-before-connecting-it-to-apple-tv
title: Recipe: Review a Lava API before connecting it to Apple TV
generated: true
---

# Recipe: Review a Lava API before connecting it to Apple TV

The agent can state what a Lava webhook exposes and whether its protection has been verified.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Resolve the exact request URL and HTTP verb.
2. Identify the matching Lava Webhook Defined Value.
3. Read the complete Lava template.
4. Inventory its request inputs and output fields.
5. Inventory every enabled Lava command.
6. Identify any person or sensitive data that can be returned.
7. Verify the actual security layer outside the webhook.
8. Test unauthorized behavior with a bounded, read-only request.
9. Record only a public-safe conclusion.
10. Stop before launch if the endpoint relies on default webhook security.

## Do Not Assume

- Lava webhooks are secured by default.
- An application API key automatically protects the webhook.
- One installation’s handler behavior proves another installation’s state.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/lava/lava-api
