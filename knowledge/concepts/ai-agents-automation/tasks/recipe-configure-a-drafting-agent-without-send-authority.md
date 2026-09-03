---
concept_id: ai-agents-automation
task_id: recipe-configure-a-drafting-agent-without-send-authority
title: Recipe: Configure a drafting agent without send authority
generated: true
---

# Recipe: Configure a drafting agent without send authority

Staff can research and compose a communication while sending remains a separate approved action.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`

## Entities And Tables

- `Group`

## Steps

1. Create or select an Internal agent for the intended staff group.
2. Attach only the read tools needed to resolve recipients and context.
3. Attach a compose or draft tool.
4. Omit send and delete tools from the agent.
5. If a separate send agent is required, restrict it to a smaller role and add an explicit confirmation prerequisite.
6. Test that drafting succeeds for an authorized user.
7. Test that direct and indirect requests to send are refused.
8. Review returned recipient data for least privilege.

## Do Not Assume

- An instruction saying “do not send” is equivalent to withholding the send tool.
- Draft creation proves delivery.
- Recipient identity may be inferred safely. Native Tools and

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools
- https://www.youtube.com/watch?v=dpYJiOAiJYM
