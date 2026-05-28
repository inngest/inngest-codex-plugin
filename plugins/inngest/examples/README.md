# Inngest Plugin Examples

These examples are small, copyable TypeScript patterns for Codex and other
coding agents. They are not full applications; they show the file boundaries
and durable execution shapes that agents should adapt to a target repository.

## Examples

| Example | Use when | Key files |
|---|---|---|
| `nextjs-durable-workflow` | Starting a Next.js app from scratch or moving signup side effects out of a request handler | `src/inngest/client.ts`, `src/inngest/functions.ts`, `src/app/api/inngest/route.ts`, `src/app/api/signup/route.ts` |
| `durable-agent` | Building an AI support/research agent that survives deploys and human approval waits | `src/inngest/client.ts`, `src/inngest/functions.ts`, `src/app/api/agents/support/route.ts` |

## Agent Rules

- Treat examples as patterns, not code to paste blindly.
- Preserve the target repo's framework, imports, test style, and domain service
  boundaries.
- Keep side effects inside `step.run` or AgentKit/`step.ai` boundaries.
- Use deterministic event IDs when the source request or webhook may retry.
- Register every new function with the repo's serve endpoint.
- Run the target repo's typecheck/tests after adapting an example.
