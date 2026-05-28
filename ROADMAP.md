# Inngest Codex Plugin Roadmap

This repo is the Codex port of the Inngest Claude Code plugin. It keeps
the same Inngest skill inventory while replacing Claude-specific
marketplace metadata with Codex plugin and marketplace metadata.

## Today (v0.3.0)

The current release covers the core TypeScript surface for durable systems
with Inngest, the alpha API CLI for operational workflows, durable agent
patterns, and an agent-first brownfield audit workflow for existing
repositories:

| Skill | What it covers |
|---|---|
| `inngest-brownfield-audit` | Repository analysis, durability-gap discovery, incremental integration planning, durable agent patterns |
| `inngest-setup` | SDK installation, client config, serve endpoints, dev server |
| `inngest-events` | Event schema, idempotency, fan-out patterns |
| `inngest-durable-functions` | Triggers, memoization, retries, error handling |
| `inngest-steps` | `step.run`, `step.sleep`, `step.waitForEvent`, `step.invoke`, `step.ai` |
| `inngest-agents` | AgentKit, `step.ai`, tool calls, human review, realtime progress, provider flow control |
| `inngest-flow-control` | Concurrency, throttling, rate limits, debounce, batching |
| `inngest-middleware` | Cross-cutting concerns, dependency injection |
| `inngest-realtime` | v4 native realtime, channels, subscription tokens, UI consumers |
| `inngest-v3-v4-migration` | TypeScript SDK v3 to v4 migration, mixed API cleanup, realtime migration |
| `inngest-api` | Alpha API CLI for account/env operations, webhooks, app syncs, function invocation, runs, and traces |

The plugin also ships local Inngest dev-server MCP configuration so Codex
can inspect runs, events, and function state during local development.
`FRICTION.md` tracks the Codex-side CLI agent-experience findings so they can
be compared with the Claude Code plugin's sibling log.

## Next

- Revisit `inngest-api` as the alpha CLI stabilizes and promote any durable
  production workflows into deeper examples.
- Add marketplace screenshots once the Codex plugin UI screenshot convention is
  stable.
- Deepen durable AI agent examples with UI traces.
- Replace eval context-mode with true non-interactive Codex plugin install when
  the CLI exposes a stable session interface.
- Add automated judge-model execution on top of the current blind judge packets.

## Versioning

Releases are tagged from this repository.

- **v0.1.0** - first Codex port with seven Inngest TypeScript skills,
  Codex plugin manifest, local marketplace metadata, dev-server MCP
  config, and eval harness scaffolding.
- **v0.2.0** - adds `inngest-api` for alpha API CLI operations across
  accounts, environments, webhooks, app syncs, function invocation, runs,
  and traces.
- **v0.3.0** - adds `inngest-brownfield-audit` for agent-first repository
  analysis and incremental integration planning, plus `inngest-agents` for
  AgentKit, `step.ai`, tool calls, human review, realtime progress, and flow
  control, and `inngest-v3-v4-migration` for TypeScript SDK v3 to v4 upgrades.
