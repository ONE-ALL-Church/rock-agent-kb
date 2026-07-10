---
id: answer:api-integrations:risks-caveats
concept_id: api-integrations
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for API And Integrations?

Rock's planned MCP flow uses OAuth so the external harness holds and renews the access token without exposing a general Rock API key to the language model. Administrators should still review client authorization, token scope and revocation behavior in the released implementation. The pre-release design applies Rock permission checks as the authenticated person using the agent, including MCP access, rather than granting an agent unrestricted administrative access. Verify the shipped version and each enabled tool's authorization behavior before production use. Rock skills and tools provide Rock-side capabilities, while skills in an external harness can hold organization-specific business rules that guide how those capabilities are used. Churches should govern and version both layers instead of assuming the MCP tools alone contain local process policy. Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default.

## Top Claims

- `claim:2a2a9fc94666d58b0e4f`
- `claim:2a7ef23854b5dd315c7d`
- `claim:538f1a4e0ad7c90f7c5a`
- `claim:410bf6750e90b7193262`

## Citations

- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s) (`05:40`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s) (`01:53`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=909s) (`15:09`)
- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
