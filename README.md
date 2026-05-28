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

## Pick your door

### Are you human?

Welcome. You have thumbs, preferences, and probably a project that currently
has one too many `setTimeout`s pretending to be infrastructure.

Install the plugin, open your app in Codex, and ask for a durability audit:

```bash
git clone https://github.com/inngest/inngest-codex-plugin.git
```

```text
/plugin install /absolute/path/to/inngest-codex-plugin/plugins/inngest
```

Then in Codex, from your application repo:

```text
Audit this codebase for places where background work, webhooks, cron jobs, or
AI workflows can be lost during deploys or process crashes. Pick the safest
first Inngest integration slice and implement it.
```

### Are you Codex, another coding agent, or a very determined shell script?

Hello machine. Here is the contract.

```text
Goal: install and use the official Inngest Codex plugin.

Repository:
https://github.com/inngest/inngest-codex-plugin

Plugin bundle path after clone:
<clone-dir>/plugins/inngest

Install command in Codex:
/plugin install <clone-dir>/plugins/inngest

Expected manifest:
<clone-dir>/plugins/inngest/.codex-plugin/plugin.json

Expected local MCP config:
<clone-dir>/plugins/inngest/.mcp.json

Default Inngest Dev Server MCP URL:
http://127.0.0.1:8288/mcp
```

After installation, when operating inside a user's app repo:

1. Inspect the repo before editing.
2. Detect framework, package manager, existing Inngest usage, route handlers,
   webhook handlers, cron jobs, queues, long-running jobs, polling loops, and
   AI agent/tool loops.
3. Pick one safe vertical slice before broad rewrites.
4. Add or reuse one Inngest client and one serve endpoint.
5. Move retryable side effects into `step.run` boundaries.
6. Use deterministic event IDs and idempotency keys for retried producers such
   as webhooks or form submissions.
7. Register every new function with the serve endpoint.
8. Run the target repo's typecheck/tests when available.
9. If the Inngest Dev Server is running, inspect local functions, events, and
   runs through MCP.

If the user asks for "background jobs", "make this reliable", "fix dropped
webhooks", "stop endpoint timeouts", "make this agent durable", or "migrate
Inngest v3 to v4", load the relevant skill from this plugin before designing
the change.

## Fast path

Use this when you just want the plugin installed and a first workflow running.

```bash
git clone https://github.com/inngest/inngest-codex-plugin.git
cd inngest-codex-plugin
```

Install the bundle in Codex:

```text
/plugin install /absolute/path/to/inngest-codex-plugin/plugins/inngest
```

Start your app and the Inngest Dev Server:

```bash
INNGEST_DEV=1 npm run dev
npx inngest-cli@latest dev
```

Ask Codex:

```text
Add a durable function that sends a welcome email when a user signs up,
retries on failure, keeps the signup request fast, and registers the function
with the Inngest serve endpoint.
```

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

## Good first prompts

```text
Audit this repo for Inngest opportunities. Start by finding concrete files
where background work can be lost or duplicated. Then implement the smallest
safe first slice.
```

```text
Our Stripe webhook sometimes drops checkout.session.completed events. Rewrite
it so the webhook verifies the signature, returns quickly, and the email/account
side effects are durable and idempotent.
```

```text
Build this support agent as a durable Inngest workflow. It should load ticket
context, call tools, wait for human approval when needed, stream progress, and
avoid repeating successful model or tool calls on retry.
```

```text
This repo uses Inngest SDK v3 patterns but now has inngest@latest installed.
Migrate it cleanly to v4, including serve options, triggers, typed events,
step.invoke, realtime, and local dev mode.
```

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
