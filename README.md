<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="plugins/inngest/assets/inngest-wordmark-light.png">
    <img src="plugins/inngest/assets/inngest-wordmark.png" alt="Inngest" width="280">
  </picture>
</p>

# Inngest Plugin for Codex and ChatGPT

Connect your Inngest account through OAuth to inspect Cloud apps, functions,
events, runs, traces, and Insights. The same package includes coding skills for
durable workflows and agents, Agent Evals, codebase audits, flow control,
realtime, CLI operations, and SDK migrations. Cloud operations work in chat;
repository edits and local commands require a coding host.

> **Development:** v0.4.0 adds Cloud OAuth MCP to the existing coding plugin.
> Public directory submission is pending. Feedback is welcome via GitHub issues, the
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
codex plugin marketplace add /absolute/path/to/inngest-codex-plugin
```

In the Codex app, choose the Inngest marketplace in the Plugins directory,
install Inngest, and complete OAuth sign-in. Then, from your application repo:

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

Register the local marketplace from a terminal:
codex plugin marketplace add <clone-dir>

Expected manifest:
<clone-dir>/plugins/inngest/.codex-plugin/plugin.json

Expected Cloud MCP config:
<clone-dir>/plugins/inngest/.mcp.json

Bundled Inngest Cloud MCP URL:
https://api.inngest.com/mcp
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
10. For Cloud operations, use `inngest-cloud` and the OAuth MCP connection.
    For explicit terminal tasks, use `inngest-cli` or `inngest-api-cli`.
11. Keep credentials in the host OAuth flow for MCP. Never paste or
    write API keys, event keys, signing keys, webhook URLs, or decrypted secrets.

If the user asks for "background jobs", "make this reliable", "fix dropped
webhooks", "stop endpoint timeouts", "make this agent durable", or "migrate
Inngest v3 to v4", load the relevant skill from this plugin before designing
the change. If they ask to score agents, compare prompts or models, add
production evals, or connect user outcomes to runs, load `inngest-agent-evals`.

## Fast path

Use this when you just want the plugin installed and a first workflow running.

```bash
git clone https://github.com/inngest/inngest-codex-plugin.git
cd inngest-codex-plugin
```

Register the local marketplace, then install Inngest from it in the Codex app:

```text
codex plugin marketplace add /absolute/path/to/inngest-codex-plugin
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

- **15 skills** covering brownfield audits, setup, events, durable
  functions, steps, durable agents, Agent Evals, flow control, middleware,
  realtime, v3-to-v4 migrations, CLI/dev-server workflows, API CLI operations,
  and REST API v2 fallback.
- **Codex plugin manifest** at `plugins/inngest/.codex-plugin/plugin.json`.
- **Local marketplace entry** at `.agents/plugins/marketplace.json`.
- **Cloud MCP connection** at `https://api.inngest.com/mcp` with OAuth sign-in.
- **Shared Cloud operations skill** for runs, traces, events, and Insights.
- **Eval harness** adapted from the Claude Code plugin repo.

## Repository layout

```text
.agents/plugins/marketplace.json    # Local Codex marketplace catalog
plugins/inngest/                    # Installable Codex plugin bundle
plugins/inngest/.codex-plugin/      # Codex plugin manifest
plugins/inngest/skills/             # Inngest Codex skills
plugins/inngest/assets/             # Plugin brand assets
plugins/inngest/examples/           # Copyable TypeScript integration patterns
plugins/inngest/.mcp.json           # Cloud OAuth MCP config
docs/                               # Website-ready documentation drafts
eval/                               # Prompt catalog and judge harness
scripts/sync-skills.sh              # Pull latest skills from inngest-skills
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
Add Agent Evals to this support agent. Group runs by ticket, score guardrail
checks during the run, defer user-feedback scoring, and compare two answer
styles with a step experiment.
```

```text
This repo uses Inngest SDK v3 patterns but now has inngest@latest installed.
Migrate it cleanly to v4, including serve options, triggers, typed events,
step.invoke, realtime, and local dev mode.
```

## Skills

| Skill | What it covers |
|-------|----------------|
| [`inngest-cloud`](./plugins/inngest/skills/inngest-cloud/) | Cloud OAuth MCP: environments, apps, runs, traces, events, and Insights |
| [`inngest-brownfield-audit`](./plugins/inngest/skills/inngest-brownfield-audit/) | Analyze existing repos for durability gaps and plan incremental Inngest integrations |
| [`inngest-setup`](./plugins/inngest/skills/inngest-setup/) | SDK install, client config, serve endpoints, connect-as-worker, dev server |
| [`inngest-durable-functions`](./plugins/inngest/skills/inngest-durable-functions/) | Function config, triggers, step execution, retries, cancellation, observability |
| [`inngest-steps`](./plugins/inngest/skills/inngest-steps/) | `step.run`, `step.sleep`, `step.waitForEvent`, `step.invoke`, `step.ai`, parallel work |
| [`inngest-agents`](./plugins/inngest/skills/inngest-agents/) | Durable AI agents with AgentKit, `step.ai`, tools, approval waits, realtime progress, and flow control |
| [`inngest-agent-evals`](./plugins/inngest/skills/inngest-agent-evals/) | Agent Evals with scoring, deferred scorers, sessions, traces, step experiments, Insights, and outcome-based evaluation |
| [`inngest-events`](./plugins/inngest/skills/inngest-events/) | Event schemas, IDs for idempotency, fan-out patterns, system events |
| [`inngest-flow-control`](./plugins/inngest/skills/inngest-flow-control/) | Concurrency, throttling, rate limits, debounce, priority, singleton, batching |
| [`inngest-middleware`](./plugins/inngest/skills/inngest-middleware/) | Lifecycle hooks, dependency injection, Sentry, encryption, custom middleware |
| [`inngest-realtime`](./plugins/inngest/skills/inngest-realtime/) | v4 native realtime, channels, subscription tokens, React and SSE consumers |
| [`inngest-v3-v4-migration`](./plugins/inngest/skills/inngest-v3-v4-migration/) | Upgrade TypeScript SDK v3 projects to v4 and fix mixed v3/v4 API usage |
| [`inngest-cli`](./plugins/inngest/skills/inngest-cli/) | General CLI and Dev Server workflows: `inngest dev`, local testing, Docker, MCP setup, deployment checks, and self-hosted `inngest start` |
| [`inngest-api-cli`](./plugins/inngest/skills/inngest-api-cli/) | Prescriptive terminal workflows for `inngest api`, Cloud debugging, run traces, event runs, app syncs, invocation, webhooks, envs, keys, and Insights |
| [`inngest-api`](./plugins/inngest/skills/inngest-api/) | REST API v2 and OpenAPI fallback when raw HTTP is needed or the CLI does not expose an endpoint |

## Cloud MCP and OAuth

The plugin bundles `https://api.inngest.com/mcp` using Streamable HTTP. Connect
through your host's OAuth sign-in flow, choose the Inngest account and access,
and return to the conversation. No API key or client secret belongs in the
plugin configuration. The connection uses OAuth discovery and CIMD.

Try: "In staging, find recent failed runs and explain the failed steps."
The `inngest-cloud` skill resolves the environment and uses live tools and
schemas. Cloud reads work in chat; editing a repository and running local
commands require a coding host. Writes such as sending events, invoking
functions, rerunning, cancelling, and syncing apps can affect your application.

If a call needs authentication, reconnect in the host. If it is denied, check
the selected account, environment, and grants. An access error does not mean
that a run or function is missing.

### Optional local Dev Server

Ask: "Set up local Inngest Dev Server MCP for this project alongside Cloud."
The `inngest-cli` skill checks the running port, reuses an existing connection,
and verifies the local apps. See [local setup and removal](plugins/inngest/skills/inngest-cli/references/local-mcp.md).

Cloud and local can stay connected together. Requests for local apps use
`inngest-dev`; requests for deployed apps use `inngest-cloud`. A local
connection failure never redirects the operation to Cloud.

Local MCP is no longer installed automatically. Keep it as a separate
connection when developing on your machine. Prefer the project-only setup
linked above. For a user-level connection across projects, start `inngest dev`
and run:

```bash
codex mcp add inngest-dev --url http://127.0.0.1:8288/mcp
```

Use the actual port from the Dev Server's startup output if it differs from
8288. The Cloud connection remains separate. Hosted chat cannot reach localhost.

See [submission materials](docs/submission.md) for directory packaging, listing
copy, reviewer tests, and the remaining release gates. This repository can be
installed for development before a directory listing is approved.

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

Most skills, including `inngest-cli`, `inngest-api-cli`, and `inngest-api`,
are mirrored from
[`inngest/inngest-skills`](https://github.com/inngest/inngest-skills).
Merge [the Cloud skills update](https://github.com/inngest/inngest-skills/pull/15)
before syncing from `main`. Older upstream revisions lack the Cloud skill and
local MCP guidance and would remove them.
Run `scripts/sync-skills.sh` whenever upstream skills change. The
`inngest-brownfield-audit`, `inngest-agents`, and `inngest-v3-v4-migration`
skills are maintained in this repository while the Codex-specific agent
workflow stabilizes.

## License

MIT. See [LICENSE](./LICENSE).
