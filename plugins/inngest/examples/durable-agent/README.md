# Durable Agent Example

This example shows a minimal durable support agent. A route starts the agent by
sending an event and returns a run handle. The Inngest function loads context,
generates a draft through AgentKit, waits for approval, and persists/sends the
reply with step boundaries around side effects.

Use it for support agents, research agents, review workflows, and other AI
flows that need to survive deploys, retries, and human delays.

## Files

- `src/inngest/client.ts`: shared client and event types.
- `src/inngest/functions.ts`: durable agent workflow.
- `src/app/api/agents/support/route.ts`: starts the run.
- `src/app/api/inngest/route.ts`: serve endpoint.
- `src/lib/support-tools.ts`: placeholder tools and domain side effects.

## Notes

- AgentKit model calls use `step.ai` under the hood when the model is created
  with the current `step`.
- Tool writes should use deterministic IDs or run inside explicit `step.run`
  boundaries.
- Use `inngest-realtime` patterns if the UI needs live progress.
