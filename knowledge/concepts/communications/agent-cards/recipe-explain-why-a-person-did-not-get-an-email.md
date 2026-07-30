---
concept_id: communications
task_id: recipe-explain-why-a-person-did-not-get-an-email
title: Recipe: Explain why a person did not get an email
generated: true
---

# Recipe: Explain why a person did not get an email

Answer in evidence form: "Person was in audience but excluded by preference", "Person was not in audience", "Person had pending recipient row but transport failed", or "Rock sent successfully; provider logs must be checked."

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Person email
2. email active
3. email preference
4. deceased status
5. list membership
6. subscription state
7. recipient row
8. medium entity type
9. status/status note
10. unsubscribe fields
11. transport/provider logs
12. bounce/suppression state

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationEntry/communicationEntryRecipientBag.d.ts
