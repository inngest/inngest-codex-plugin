# Inngest Codex Plugin Roadmap

This repo is the Codex port of the Inngest Claude Code plugin. It keeps
the same Inngest skill inventory while replacing Claude-specific
marketplace metadata with Codex plugin and marketplace metadata.

## Today (v0.3.3)

The current release covers the core TypeScript surface for durable systems
with Inngest, CLI/dev-server workflows, API CLI operations, REST API v2
fallback, durable agent patterns, and an agent-first brownfield audit workflow
for existing repositories:

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
| `inngest-cli` | General CLI and dev server workflows: install/run `inngest dev`, local testing, Docker, MCP setup, deployment checks, and self-hosted `inngest start` |
| `inngest-api-cli` | Prescriptive terminal workflows for `inngest api`, Cloud debugging, run traces, event runs, app syncs, invocation, webhooks, envs, keys, and Insights |
| `inngest-api` | REST API v2 and OpenAPI fallback when raw HTTP is needed or the CLI does not expose an endpoint |

The plugin also ships local Inngest dev-server MCP configuration so Codex
can inspect runs, events, and function state during local development.

## Next

- Add marketplace screenshots once the Codex plugin UI screenshot convention is
  stable.
- Track the beta API CLI as endpoint coverage grows and update `inngest-api-cli`
  guardrails when commands stabilize.
- Deepen durable AI agent examples with UI traces.
- Replace eval context-mode with true non-interactive Codex plugin install when
  the CLI exposes a stable session interface.
- Add automated judge-model execution on top of the current blind judge packets.

## Versioning

Releases are tagged from this repository.

- **v0.1.0** - first Codex port with seven Inngest TypeScript skills,
  Codex plugin manifest, local marketplace metadata, dev-server MCP
  config, and eval harness scaffolding.
- **v0.2.0** - adds `inngest-api` for API CLI operations across accounts,
  environments, webhooks, app syncs, function invocation, runs, and traces.
- **v0.3.0** - adds `inngest-brownfield-audit` for agent-first repository
  analysis and incremental integration planning, plus `inngest-agents` for
  AgentKit, `step.ai`, tool calls, human review, realtime progress, and flow
  control, and `inngest-v3-v4-migration` for TypeScript SDK v3 to v4 upgrades.
- **v0.3.1** - updates `inngest-api` for the `inngest api` beta entrypoint,
  REST API v2 docs lookup, event-run inspection, Insights commands, and
  agent-first debugging guardrails.
- **v0.3.2** - adds `inngest-cli` as the general CLI/dev-server skill and
  narrows `inngest-api` to REST API v2/OpenAPI fallback.
- **v0.3.3** - adds `inngest-api-cli` as the prescriptive `inngest api`
  operations skill, keeping `inngest-cli` focused on dev server and general CLI
  workflows.
