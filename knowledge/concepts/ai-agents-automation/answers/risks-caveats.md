---
id: answer:ai-agents-automation:risks-caveats
concept_id: ai-agents-automation
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for AI Agents And Automation?

The pre-release design applies Rock permission checks as the authenticated person using the agent, including MCP access, rather than granting an agent unrestricted administrative access. Verify the shipped version and each enabled tool's authorization behavior before production use. Connection-request AI summaries and insights require a configured prompt on the connection type and a configured AI provider. Their output should be treated as generated assistance, not authoritative person data. Agent capabilities are intended to be controlled at the individual tool level, allowing an organization to enable drafting while disabling sending, or to omit destructive tools such as delete operations. Tool availability and Rock permissions should both be treated as required controls. Rock's planned MCP flow uses OAuth so the external harness holds and renews the access token without exposing a general Rock API key to the language model. Administrators should still review client authorization, token scope and revocation behavior in the released implementation.

## Top Claims

- `claim:2a7ef23854b5dd315c7d`
- `claim:069aa7a39db4563841a2`
- `claim:903c8ff9b5d2590fd616`
- `claim:2a2a9fc94666d58b0e4f`
- `claim:538f1a4e0ad7c90f7c5a`

## Citations

- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s) (`01:53`)
- [Connections Helps Prevent Your People from Falling Through the Cracks](https://www.youtube.com/watch?v=7rxTGLLhlrU&t=583s) (`09:43`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s) (`06:25`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s) (`05:40`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=909s) (`15:09`)
