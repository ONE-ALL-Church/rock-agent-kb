---
id: answer:security-permissions:risks-caveats
concept_id: security-permissions
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Security And Permissions?

Person Profile security should be reviewed at the page, block, entity, action, and data-field level because profile visibility does not imply permission to edit every person-related record. The pre-release design applies Rock permission checks as the authenticated person using the agent, including MCP access, rather than granting an agent unrestricted administrative access. Verify the shipped version and each enabled tool's authorization behavior before production use. Agent capabilities are intended to be controlled at the individual tool level, allowing an organization to enable drafting while disabling sending, or to omit destructive tools such as delete operations. Tool availability and Rock permissions should both be treated as required controls. Rock's planned MCP flow uses OAuth so the external harness holds and renews the access token without exposing a general Rock API key to the language model. Administrators should still review client authorization, token scope and revocation behavior in the released implementation.

## Top Claims

- `claim:5c53977793c7673b19e9`
- `claim:2a7ef23854b5dd315c7d`
- `claim:903c8ff9b5d2590fd616`
- `claim:2a2a9fc94666d58b0e4f`
- `claim:09bc1e14a8ad2c40145e`

## Distilled Claims

- `distilled-claim:1444283a684196cee6b2`

## Citations

- [Person Profile](https://community.rockrms.com/rocku/individuals-in-rock/person-profile) (`00:00`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s) (`01:53`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s) (`06:25`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s) (`05:40`)
- [Adding Pages and Blocks](https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy) (`00:00`)
