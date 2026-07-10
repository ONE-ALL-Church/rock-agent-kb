---
id: answer:api-integrations:first-checks
concept_id: api-integrations
generated: true
artifact_level: answer
---

# What should I check first for API And Integrations?

Rock's Lava API guidance identifies Apple TV and Roku channels as examples of custom APIs that can be built with Lava, but warns that Lava webhooks do not include security by default. Helix Lava Endpoints are the application work units called from the client, so agents should inspect endpoint name, description, slug, behavior, and security before changing an application flow. Lava tools should return structured AgentToolResult values and use the dedicated filters for instructions, compact history content, metadata and Rock reference routes. Parameters should be explicit and sanitized, and the built-in tool logs should be used to inspect calls, inputs and results during debugging. Prompt context is layered across Rock's core prompt, organization prompt, agent instructions, skill instructions and current-person context. The practical guidance is to keep each layer concise, add instructions only when testing shows they are needed and pass IdKeys rather than raw integer identifiers.

## Top Claims

- `claim:410bf6750e90b7193262`
- `claim:d35ed98aadeaabd2cf1e`
- `claim:4b7b8d0b0379ceb7587f`
- `claim:57e32b4d554a759231a1`
- `claim:60c2bcd25e1cce4efef4`
- `claim:b4fb38224ff8452078f3`
- `claim:c3921cb1d8b61e06c713`
- `claim:cd52138ec6ca3848cae9`

## Citations

- [Creating APIs Using Lava](https://community.rockrms.com/lava/lava-api)
- [Helix Lava Application Endpoints](https://community.rockrms.com/developer/helix/lava-applications/endpoints)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=5268s) (`87:48`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4573s) (`76:13`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4054s) (`67:34`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=1441s) (`24:01`)
- [AI Summit: The Community's First Look at Rock's AI Agents](https://www.youtube.com/watch?v=UvW68dZBcJ8&t=4280s) (`71:20`)
- [Media Watch](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/YAP2VexPe5) (`01:43`)
