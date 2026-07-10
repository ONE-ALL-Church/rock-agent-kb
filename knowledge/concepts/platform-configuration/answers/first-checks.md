---
id: answer:platform-configuration:first-checks
concept_id: platform-configuration
generated: true
artifact_level: answer
---

# What should I check first for Platform Configuration?

Rock's agent model separates agents, skills and tools, with configuration and security boundaries at each layer. Chat versus MCP and Internal versus Public are separate design choices, and only authorized tools should be exposed to the model for the current person and agent. Lava tools should return structured AgentToolResult values and use the dedicated filters for instructions, compact history content, metadata and Rock reference routes. Parameters should be explicit and sanitized, and the built-in tool logs should be used to inspect calls, inputs and results during debugging. Prompt context is layered across Rock's core prompt, organization prompt, agent instructions, skill instructions and current-person context. The practical guidance is to keep each layer concise, add instructions only when testing shows they are needed and pass IdKeys rather than raw integer identifiers. Custom tools should use clear verb-and-entity names and intentionally shaped result types such as Lookup, List, Get, Summary, Insights, AvailableAttributes and AddOrUpdate. Tool names, parameters and bounded result shapes help the model choose correctly and avoid filling its context window with unnecessary data.

## Top Claims

- `claim:b4fb38224ff8452078f3`
- `claim:4b7b8d0b0379ceb7587f`
- `claim:57e32b4d554a759231a1`
- `claim:60c2bcd25e1cce4efef4`
- `claim:6ae226ddf1e1e1df52ed`
- `claim:c3921cb1d8b61e06c713`
- `claim:60d40983fd53c0173dd9`
- `claim:ffba67d8847c47e68ea6`

## Citations

- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s) (`24:01`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s) (`87:48`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s) (`76:13`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s) (`67:34`)
- [Packaging Plugins and Themes](https://community.rockrms.com/developer/packaging-plugins-themes)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s) (`71:20`)
- [Media Watch](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) (`49:32`)
- [Media Watch](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/D9PDOXelqz) (`07:12`)
