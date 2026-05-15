# Inngest Codex Plugin Roadmap

This repo is the Codex port of the Inngest Claude Code plugin. It keeps
the same Inngest skill inventory while replacing Claude-specific
marketplace metadata with Codex plugin and marketplace metadata.

## Today (v0.1.0)

The first release covers the core TypeScript surface for durable systems
with Inngest:

| Skill | What it covers |
|---|---|
| `inngest-setup` | SDK installation, client config, serve endpoints, dev server |
| `inngest-events` | Event schema, idempotency, fan-out patterns |
| `inngest-durable-functions` | Triggers, memoization, retries, error handling |
| `inngest-steps` | `step.run`, `step.sleep`, `step.waitForEvent`, `step.invoke`, `step.ai` |
| `inngest-flow-control` | Concurrency, throttling, rate limits, debounce, batching |
| `inngest-middleware` | Cross-cutting concerns, dependency injection |
| `inngest-realtime` | v4 native realtime, channels, subscription tokens, UI consumers |

The plugin also ships local Inngest dev-server MCP configuration so Codex
can inspect runs, events, and function state during local development.

## Next

- Add Codex-specific examples and screenshots to the plugin manifest.
- Add a v3 to v4 migration skill for existing Inngest projects.
- Add a brownfield audit skill for finding durability gaps in existing
  repositories.
- Adapt the eval harness so it can run against Codex sessions directly.

## Versioning

Releases are tagged from this repository.

- **v0.1.0** - first Codex port with seven Inngest TypeScript skills,
  Codex plugin manifest, local marketplace metadata, dev-server MCP
  config, and eval harness scaffolding.
