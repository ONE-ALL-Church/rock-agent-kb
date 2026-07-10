---
id: answer:ai-agents-automation:first-checks
concept_id: ai-agents-automation
generated: true
artifact_level: answer
---

# What should I check first for AI Agents And Automation?

Prompt context is layered across Rock's core prompt, organization prompt, agent instructions, skill instructions and current-person context. The practical guidance is to keep each layer concise, add instructions only when testing shows they are needed and pass IdKeys rather than raw integer identifiers. Custom tools should use clear verb-and-entity names and intentionally shaped result types such as Lookup, List, Get, Summary, Insights, AvailableAttributes and AddOrUpdate. Tool names, parameters and bounded result shapes help the model choose correctly and avoid filling its context window with unnecessary data. When work must survive a conversation, prefer an agent workflow that creates a durable file or handoff artifact instead of leaving the result only inside a transient chat thread. Rock's agent model separates agents, skills and tools, with configuration and security boundaries at each layer. Chat versus MCP and Internal versus Public are separate design choices, and only authorized tools should be exposed to the model for the current person and agent.

## Top Claims

- `claim:57e32b4d554a759231a1`
- `claim:60c2bcd25e1cce4efef4`
- `claim:679a38216f2b07097624`
- `claim:b4fb38224ff8452078f3`
- `claim:c3921cb1d8b61e06c713`
- `claim:4b083dda9f0d9ccc4aff`
- `claim:c8c3a60f71790dd3616d`
- `claim:c9c1fa08cb0434d501e6`

## Citations

- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s) (`76:13`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s) (`67:34`)
- [AI Voice Models & the Hidden Costs of Untrained Staff | Ep 214](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=713s) (`11:53`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s) (`24:01`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s) (`71:20`)
- [AI Voice Models & the Hidden Costs of Untrained Staff | Ep 214](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2042s) (`34:02`)
- [AI Voice Models & the Hidden Costs of Untrained Staff | Ep 214](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s) (`40:09`)
- [AI Voice Models & the Hidden Costs of Untrained Staff | Ep 214](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1714s) (`28:34`)
