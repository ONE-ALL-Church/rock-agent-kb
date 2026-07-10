---
id: answer:ai-agents-automation:first-checks
concept_id: ai-agents-automation
generated: true
artifact_level: answer
---

# What should I check first for AI Agents And Automation?

Prompt context is layered across Rock's core prompt, organization prompt, agent instructions, skill instructions and current-person context. The practical guidance is to keep each layer concise, add instructions only when testing shows they are needed and pass IdKeys rather than raw integer identifiers. Custom tools should use clear verb-and-entity names and intentionally shaped result types such as Lookup, List, Get, Summary, Insights, AvailableAttributes and AddOrUpdate. Tool names, parameters and bounded result shapes help the model choose correctly and avoid filling its context window with unnecessary data. Rock's agent model separates agents, skills and tools, with configuration and security boundaries at each layer. Chat versus MCP and Internal versus Public are separate design choices, and only authorized tools should be exposed to the model for the current person and agent. The summit strongly warns against allowing an agent to generate and execute arbitrary SQL at runtime because that bypasses Rock security and business logic. Reviewed static SQL inside a narrowly secured Lava tool is distinguished from giving the model an open-ended SQL execution capability.

## Top Claims

- `claim:57e32b4d554a759231a1`
- `claim:60c2bcd25e1cce4efef4`
- `claim:b4fb38224ff8452078f3`
- `claim:c3921cb1d8b61e06c713`
- `claim:2a7ef23854b5dd315c7d`
- `claim:4b7b8d0b0379ceb7587f`
- `claim:903c8ff9b5d2590fd616`
- `claim:2a2a9fc94666d58b0e4f`

## Citations

- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s) (`76:13`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s) (`67:34`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s) (`24:01`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s) (`71:20`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=113s) (`01:53`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s) (`87:48`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=385s) (`06:25`)
- [RockIQ Rapid Fire Q&A from the AI Summit | Ep 218](https://www.youtube.com/watch?v=dpYJiOAiJYM&t=340s) (`05:40`)
