<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="plugins/inngest/assets/inngest-wordmark-light.png">
    <img src="plugins/inngest/assets/inngest-wordmark.png" alt="Inngest" width="280">
  </picture>
</p>

# Inngest Plugin for Codex

The official Inngest plugin for Codex. One install, and Codex knows how
to audit an existing codebase for durability gaps, build reliable durable
functions, design event-driven workflows, configure flow control, add
middleware, stream realtime updates, create durable agent workflows, and operate
[Inngest](https://www.inngest.com) through the alpha API CLI.

> **Beta:** v0.3.0 is the current Codex port of the Inngest Claude Code
> plugin. Feedback is welcome via GitHub issues, the
> [Inngest Discord](https://www.inngest.com/discord), or
> [@inngest](https://twitter.com/inngest).

## What's included

- **11 Codex skills** covering brownfield audits, setup, events, durable
  functions, steps, durable agents, flow control, middleware, realtime,
  v3-to-v4 migrations, and API CLI operations.
- **Codex plugin manifest** at `plugins/inngest/.codex-plugin/plugin.json`.
- **Local marketplace entry** at `.agents/plugins/marketplace.json`.
- **MCP server config** for the local Inngest dev server at
  `http://127.0.0.1:8288/mcp`.
- **Eval harness** adapted from the Claude Code plugin repo.
- **CLI friction log** at `FRICTION.md` for cross-agent AX testing.

## Repository layout

```text
.agents/plugins/marketplace.json    # Local Codex marketplace catalog
plugins/inngest/                    # Installable Codex plugin bundle
plugins/inngest/.codex-plugin/      # Codex plugin manifest
plugins/inngest/skills/             # Inngest Codex skills
plugins/inngest/assets/             # Plugin brand assets
plugins/inngest/examples/           # Copyable TypeScript integration patterns
plugins/inngest/.mcp.json           # Local dev-server MCP config
docs/                               # Website-ready documentation drafts
eval/                               # Prompt catalog and judge harness
scripts/sync-skills.sh              # Pull latest skills from inngest-skills
FRICTION.md                         # Codex-side CLI friction log
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
| [`inngest-brownfield-audit`](./plugins/inngest/skills/inngest-brownfield-audit/) | Analyze existing repos for durability gaps and plan incremental Inngest integrations |
| [`inngest-setup`](./plugins/inngest/skills/inngest-setup/) | SDK install, client config, serve endpoints, connect-as-worker, dev server |
| [`inngest-durable-functions`](./plugins/inngest/skills/inngest-durable-functions/) | Function config, triggers, step execution, retries, cancellation, observability |
| [`inngest-steps`](./plugins/inngest/skills/inngest-steps/) | `step.run`, `step.sleep`, `step.waitForEvent`, `step.invoke`, `step.ai`, parallel work |
| [`inngest-agents`](./plugins/inngest/skills/inngest-agents/) | Durable AI agents with AgentKit, `step.ai`, tools, approval waits, realtime progress, and flow control |
| [`inngest-events`](./plugins/inngest/skills/inngest-events/) | Event schemas, IDs for idempotency, fan-out patterns, system events |
| [`inngest-flow-control`](./plugins/inngest/skills/inngest-flow-control/) | Concurrency, throttling, rate limits, debounce, priority, singleton, batching |
| [`inngest-middleware`](./plugins/inngest/skills/inngest-middleware/) | Lifecycle hooks, dependency injection, Sentry, encryption, custom middleware |
| [`inngest-realtime`](./plugins/inngest/skills/inngest-realtime/) | v4 native realtime, channels, subscription tokens, React and SSE consumers |
| [`inngest-v3-v4-migration`](./plugins/inngest/skills/inngest-v3-v4-migration/) | Upgrade TypeScript SDK v3 projects to v4 and fix mixed v3/v4 API usage |
| [`inngest-api`](./plugins/inngest/skills/inngest-api/) | Alpha API CLI workflows for account/env operations, webhooks, app syncs, function invocation, runs, and traces |

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

## Examples

The plugin ships small, copyable examples under
[`plugins/inngest/examples`](./plugins/inngest/examples/). They are designed as
agent-facing patterns rather than complete apps:

- `nextjs-durable-workflow` shows a thin route emitting a typed event and a
  durable function handling side effects.
- `durable-agent` shows an AgentKit workflow with `step.ai`, durable tool
  boundaries, approval waits, and provider flow control.

## Website docs

The website-ready docs draft lives at
[`docs/ai-dev-tools/codex-plugin.mdx`](./docs/ai-dev-tools/codex-plugin.mdx).
It is written to fit beside the existing Inngest AI dev tools docs.

## Skills source of truth

Most skills are mirrored from
[`inngest/inngest-skills`](https://github.com/inngest/inngest-skills).
Run `scripts/sync-skills.sh` whenever upstream skills change. The
`inngest-api`, `inngest-brownfield-audit`, `inngest-agents`, and
`inngest-v3-v4-migration` skills are maintained in this repository while the
alpha CLI and Codex-specific agent workflow stabilize.

## License

Apache 2.0. See [LICENSE](./LICENSE).
