---
concept_id: communications
task_id: recipe-diagnose-one-missing-recipient
title: Recipe: Diagnose one missing recipient
generated: true
---

# Recipe: Diagnose one missing recipient

A specific, evidence-backed reason the person was included, excluded or routed to a different medium.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`

## Entities And Tables

- `Person`
- `Group`

## Steps

1. Confirm the person belongs in the authoritative targeting result.
2. Confirm current membership in the communication-list group.
3. Inspect sync state and applicable segment filters.
4. Inspect the person’s email address, SMS number and channel-specific eligibility.
5. Inspect global email preference, list subscription and medium preference.
6. Confirm whether the communication was personal or bulk.
7. Confirm duplicate prevention did not consolidate a shared destination.
8. Inspect the stored recipient result for the communication.
9. Report the exact failing layer without changing consent or contact data.

## Do Not Assume

- Group membership equals email eligibility.
- A mobile number is SMS-eligible.
- Shared contact information should generate duplicate messages.

## Source Links

- https://community.rockrms.com/documentation/engagement/communications/communication-preferences/set-subscription-preferences
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationDetail/createPersonalTemplateRequestBag.d.ts
