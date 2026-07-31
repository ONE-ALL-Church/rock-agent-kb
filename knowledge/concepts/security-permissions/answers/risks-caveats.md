---
id: answer:security-permissions:risks-caveats
concept_id: security-permissions
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Security And Permissions?

Person Profile security should be reviewed at the page, block, entity, action, and data-field level because profile visibility does not imply permission to edit every person-related record. A v19 person-merge requester who lacks merge permission can ask to be notified when the reviewed merge completes, keeping request submission separate from merge authorization. The pre-release design applies Rock permission checks as the authenticated person using the agent, including MCP access, rather than granting an agent unrestricted administrative access. Verify the shipped version and each enabled tool's authorization behavior before production use. Agent capabilities are intended to be controlled at the individual tool level, allowing an organization to enable drafting while disabling sending, or to omit destructive tools such as delete operations. Tool availability and Rock permissions should both be treated as required controls.

## Top Claims

- `claim:5c53977793c7673b19e9`
- `claim:b81391274ac89ca6c69f`
- `claim:2a7ef23854b5dd315c7d`
- `claim:903c8ff9b5d2590fd616`
- `claim:e78d41d7fefc84b6e9e7`

## Distilled Claims

- `distilled-claim:52ca0e7e0ed800155e98`
- `distilled-claim:58912b597da2f790981d`
- `distilled-claim:ba482103593b2169755a`

## Citations

- [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile) (`00:00`)
- [New Features & Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=902s) (`15:02`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s) (`01:53`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s) (`06:25`)
- [The Vatican on AI and Grandmasters on Ministry | Ep 215](https://www.youtube.com/watch?v=pvgZLvcfmFQ&t=396s) (`06:36`)
