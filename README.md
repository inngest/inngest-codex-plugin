<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="plugins/inngest/assets/inngest-wordmark-light.png">
    <img src="plugins/inngest/assets/inngest-wordmark.png" alt="Inngest" width="280">
  </picture>
</p>

# Inngest Plugin for Codex

The official Inngest plugin for Codex. One install, and Codex knows how
to build reliable durable functions, design event-driven workflows,
configure flow control, add middleware, and stream realtime updates with
[Inngest](https://www.inngest.com).

> **Beta:** v0.1.0 is the first Codex port of the Inngest Claude Code
> plugin. Feedback is welcome via GitHub issues, the
> [Inngest Discord](https://www.inngest.com/discord), or
> [@inngest](https://twitter.com/inngest).

## What's included

- **7 Codex skills** covering setup, events, durable functions, steps,
  flow control, middleware, and realtime.
- **Codex plugin manifest** at `plugins/inngest/.codex-plugin/plugin.json`.
- **Local marketplace entry** at `.agents/plugins/marketplace.json`.
- **MCP server config** for the local Inngest dev server at
  `http://127.0.0.1:8288/mcp`.
- **Eval harness** adapted from the Claude Code plugin repo.

## Repository layout

```text
.agents/plugins/marketplace.json    # Local Codex marketplace catalog
plugins/inngest/                    # Installable Codex plugin bundle
plugins/inngest/.codex-plugin/      # Codex plugin manifest
plugins/inngest/skills/             # Inngest Codex skills
plugins/inngest/assets/             # Plugin brand assets
plugins/inngest/.mcp.json           # Local dev-server MCP config
eval/                               # Prompt catalog and judge harness
scripts/sync-skills.sh              # Pull latest skills from inngest-skills
```

## Installation

### Local Codex marketplace

From this repository, install the plugin through the Codex local
marketplace entry in `.agents/plugins/marketplace.json`.

For development, you can also point Codex directly at the plugin bundle:

```bash
/plugin install /path/to/inngest-codex-plugin/plugins/inngest
```

## Quick start

1. Install the plugin.
2. Start the Inngest dev server in your project:

   ```bash
   npx inngest-cli@latest dev
   ```

3. Ask Codex for an Inngest-shaped change:

   ```text
   Add a durable function that sends a welcome email when a user signs up,
   retries on failure, and waits 24 hours before sending the second email.
   ```

Codex will load the relevant Inngest skill, write or update the function,
register it with your serve endpoint, and use the dev-server MCP endpoint
when available to inspect local runs and events.

## Skills

| Skill | What it covers |
|-------|----------------|
| [`inngest-setup`](./plugins/inngest/skills/inngest-setup/) | SDK install, client config, serve endpoints, connect-as-worker, dev server |
| [`inngest-durable-functions`](./plugins/inngest/skills/inngest-durable-functions/) | Function config, triggers, step execution, retries, cancellation, observability |
| [`inngest-steps`](./plugins/inngest/skills/inngest-steps/) | `step.run`, `step.sleep`, `step.waitForEvent`, `step.invoke`, `step.ai`, parallel work |
| [`inngest-events`](./plugins/inngest/skills/inngest-events/) | Event schemas, IDs for idempotency, fan-out patterns, system events |
| [`inngest-flow-control`](./plugins/inngest/skills/inngest-flow-control/) | Concurrency, throttling, rate limits, debounce, priority, singleton, batching |
| [`inngest-middleware`](./plugins/inngest/skills/inngest-middleware/) | Lifecycle hooks, dependency injection, Sentry, encryption, custom middleware |
| [`inngest-realtime`](./plugins/inngest/skills/inngest-realtime/) | v4 native realtime, channels, subscription tokens, React and SSE consumers |

## Dev server MCP

The plugin ships `plugins/inngest/.mcp.json`:

```json
{
  "mcpServers": {
    "inngest-dev": {
      "type": "http",
      "url": "http://127.0.0.1:8288/mcp"
    }
  }
}
```

If the Inngest dev server starts on a fallback port such as `8289`, update
that URL before using the MCP integration.

## Skills source of truth

The skills are mirrored from
[`inngest/inngest-skills`](https://github.com/inngest/inngest-skills).
Run `scripts/sync-skills.sh` whenever upstream skills change.

## License

Apache 2.0. See [LICENSE](./LICENSE).
