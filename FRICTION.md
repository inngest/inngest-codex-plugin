# CLI Friction Log: `inngest alpha api`

**Agent under test:** Codex (GPT-5, Codex desktop)
**Operator:** Sterling Chin
**CLI:** `npx inngest-cli@latest alpha api`
**Date started:** 2026-05-21
**Target:** Inngest Cloud Production, read-only checks only
**Schema version:** v1 (matches sibling log in `inngest-claude-code-plugin/FRICTION.md` for cross-agent diff)

---

## Method

Codex inspected the new CLI surface, added a first-pass `inngest-api` skill to
the Codex plugin, then ran read-only and negative-path commands to evaluate
whether a coding agent can discover, authenticate, target, and chain results
without human reshaping.

This run did not exercise mutating commands. Claude Code's sibling log did
exercise a throwaway env and should be treated as the stronger signal for
`create-env`, `create-webhook`, `patch-env`, `sync-app`, and
`invoke-function`.

**Dimensions (consistent across agents):**

| Code | Dimension | Asks |
|------|-----------|------|
| D | Discoverability | Did the agent know the command/flag/endpoint existed? |
| A | Affordance | Did the name/shape match the agent's intent? |
| C | Auth & context | Did the agent know which key / env / target to use? |
| E | Error legibility | When something failed, did the message tell the agent what to do next? |
| O | Output usability | Could the agent chain the output into the next step without human reshaping? |
| M | Mental model | Did the agent have to ask a human something the CLI/docs should have answered? |

**Severity:** `low` (cosmetic), `med` (slows the agent), `high` (blocks the
agent or causes wrong action). `critical` is used where the CLI blocks a core
agent workflow.

---

## Task Ladder

### Task 1: Sanity — top-level help
- **Goal:** Discover the API surface and understand target/auth flags.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api --prod --help
  ```
- **Outcome:** success.
- **Friction:**
  - [D] low — Positive note. Top-level help lists all available endpoints and
    inherited auth/target/output flags. This is enough for an agent to build a
    first command map.
  - [A] low — Endpoint grouping by generated command names is compact but not
    task-oriented. `sync-app`, `get-function-run`, and `invoke-function` are
    usable if the agent already understands the Inngest object model.
- **Recommendation:**
  1. Keep top-level help as the canonical command map.
  2. Add task-oriented summaries or examples for high-level workflows such as
     "debug a failed run", "register/sync an app", and "invoke a function".

### Task 2: Subcommand help
- **Goal:** Check whether an agent can learn command-specific flags from
  subcommand help.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api health --help
  npx inngest-cli@latest alpha api get-function-run --help
  npx inngest-cli@latest alpha api get-function-trace --help
  npx inngest-cli@latest alpha api invoke-function --help
  npx inngest-cli@latest alpha api sync-app --help
  npx inngest-cli@latest alpha api create-env --help
  npx inngest-cli@latest alpha api create-webhook --help
  ```
- **Outcome:** success, with recurring friction.
- **Friction:**
  - [D] med — Subcommand help uses `[target/auth flags]` in `USAGE` but does
    not show the inherited `--prod`, `--env`, `--api-key`, `--api-host`,
    `--raw`, or timeout/config flags. An agent reading only subcommand help
    can miss how to target Cloud or authenticate.
  - [D] med — Field descriptions are often single words copied from schema
    property names, such as `data`, `url`, `transform`, `response`, `id`, and
    `name`. This is especially costly for webhook transforms and function
    invocation payloads.
  - [A] low — Positive note. `Path`, `Query`, and `Body` sections are excellent
    for agent mental models and should be preserved.
- **Recommendation:**
  1. Echo inherited Target/Auth/Output flags in every subcommand's help, or add
     an explicit pointer that names the important inherited flags.
  2. Replace one-word field descriptions with semantic descriptions and examples
     where the value shape is non-obvious.

### Task 3: Local target failure
- **Goal:** See how the CLI behaves when the default local dev server is absent.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api health
  ```
- **Outcome:** success as a negative-path test.
- **Friction:**
  - [E] low — Positive note. The error says the local dev server is unavailable
    at `http://localhost:8288`, suggests `inngest dev`, and suggests `--prod`
    for Cloud. This is the best error style observed.
  - [M] low — Defaulting to local dev is fine for humans, but a cold agent with
    a Cloud API key may first hit a target that is not running.
- **Recommendation:**
  1. Use this error's `<problem>; <two remediations>` style across the CLI.
  2. Consider a notice or inference when `INNGEST_API_KEY` is present and the
     user omitted `--prod`.

### Task 4: Authentication smoke test
- **Goal:** Validate the provided API key with low-risk read-only calls.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api --prod get-account
  npx inngest-cli@latest alpha api --prod get-account-envs --limit 5
  ```
- **Outcome:** success. Account lookup worked; env listing returned
  `production` and `branch`.
- **Friction:**
  - [E] high — Missing auth and bad auth both surface as the same API-shaped
    `401 Unauthorized` with `access_denied` and no remediation. Agents need to
    distinguish "no key was sent" from "the key was rejected".
  - [O] low — Positive note. Successful responses use a predictable
    `{data, metadata}` envelope.
  - [M] med — The `branch` env appears as a normal peer of `production`.
    Without `kind` or `description`, an agent cannot tell whether this is a real
    target, a parent placeholder, or a convention.
- **Recommendation:**
  1. Add client-side no-auth preflight before making Cloud calls.
  2. Wrap API 401s with a remediation hint.
  3. Add `kind` or `description` to env list entries, especially branch parent
     rows.

### Task 5: Env-scoped reads
- **Goal:** Verify env targeting and error behavior for env-scoped endpoints.
- **Commands tried:**
  ```bash
  INNGEST_ENV=production npx inngest-cli@latest alpha api --prod get-webhooks --limit 5
  INNGEST_ENV=branch npx inngest-cli@latest alpha api --prod get-webhooks --limit 5
  INNGEST_ENV=does-not-exist npx inngest-cli@latest alpha api --prod get-webhooks --limit 1
  ```
- **Outcome:** success. Production and branch reads worked; bogus env returned
  a clear 404.
- **Friction:**
  - [C] high — Env-scoped commands silently default to production when `--env`
    / `INNGEST_ENV` is omitted. This is risky for write operations, especially
    when an agent forgets one flag.
  - [E] low — Positive note. Unknown env returns a specific `env_not_found`
    error.
  - [O] med — Empty list response for webhooks omitted `data` instead of
    returning `data: []`. Agents need consistent empty shapes.
- **Recommendation:**
  1. Require explicit `--env` for env-scoped write operations, or echo the
     resolved environment to stderr for every env-scoped call.
  2. Always return `data: []` for empty list endpoints.

### Task 6: Raw output and pagination
- **Goal:** Check whether output can be piped or parsed by agents.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api --prod get-account-envs --limit 1 --raw
  ```
- **Outcome:** success.
- **Friction:**
  - [O] low — Positive note. `--raw` returns compact parseable JSON, and list
    pagination includes `cursor`, `hasMore`, and `limit` when more results
    exist.
  - [O] low — Pagination fields may be absent when not needed on some
    endpoints. Agents prefer stable nullable fields over inference.
- **Recommendation:**
  1. Always include `page.hasMore` and `page.cursor`/`page.nextCursor`, even
     when false/null.
  2. Keep `--raw` as compact JSON, not logs or mixed output.

### Task 7: Run inspection
- **Goal:** Determine whether an agent can inspect a failed run.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api --prod get-function-run
  npx inngest-cli@latest alpha api --prod get-function-trace
  ```
- **Outcome:** blocked without a known run ID.
- **Friction:**
  - [E] low — Positive note. Missing `--run-id` fails locally with a concise
    `missing required --run-id` message.
  - [D] critical — There is no `list-runs`, `list-functions`, or `list-apps`
    endpoint. An agent cannot discover the run ID, function ID, or app ID needed
    for the operational commands. This blocks core debugging workflows unless a
    human already provides IDs.
  - [A] med — Positional run IDs are not accepted. Many agents will try
    `get-function-run <run-id>` before discovering the required flag form.
  - [O] med — `--include-output` defaults false, causing an extra round trip in
    debugging flows.
- **Recommendation:**
  1. Add `list-runs` with filters for app, function, status, time range, and
     event ID.
  2. Add `list-apps` and `list-functions`.
  3. Accept positional path params in addition to flags.
  4. Consider defaulting `--include-output` to true for CLI debugging commands.

### Task 8: Invoke/sync discovery
- **Goal:** Determine whether an agent can invoke or sync without pre-known IDs.
- **Commands tried:**
  ```bash
  npx inngest-cli@latest alpha api invoke-function --help
  npx inngest-cli@latest alpha api sync-app --help
  ```
- **Outcome:** structurally blocked without app/function discovery.
- **Friction:**
  - [D] critical — `invoke-function` requires `--app-id` and `--function-id`,
    but the CLI cannot enumerate either.
  - [M] high — `sync-app` requires `--app-id`, which appears to make first-time
    app registration impossible from only a URL. The canonical first sync
    workflow is "fetch this URL and discover/register the app"; current command
    shape only supports re-syncing known apps.
  - [D] med — `--data`, `--url`, and `--idempotency-key` have insufficient
    semantic help.
- **Recommendation:**
  1. Add a first-sync/register command that accepts only `--url`, or rename the
     current command to `resync-app`.
  2. Add app/function enumeration.
  3. Improve semantic help for invocation data and idempotency.

---

## Friction Summary

| Dim | High / Critical | Med | Low (incl. positives) | Headline |
|-----|-----------------|-----|------------------------|----------|
| D — Discoverability | 3 | 4 | 1 | No list apps/functions/runs; inherited flags hidden in subcommand help. |
| A — Affordance | 0 | 2 | 3 | REST sectioning is good, but positional IDs and field semantics need polish. |
| C — Auth & context | 1 | 0 | 0 | Silent production env default is a write footgun. |
| E — Error legibility | 1 | 0 | 4 | Local-dev and required-flag errors are good; auth needs remediation. |
| O — Output usability | 0 | 3 | 4 | Envelope is strong; empty lists and pagination should be stable. |
| M — Mental model | 1 | 1 | 1 | First-sync model and branch env semantics are unclear. |

### What the CLI does well

- Top-level help exposes the whole endpoint list.
- Responses generally use a consistent `{data, metadata}` envelope.
- `Path` / `Query` / `Body` help sections are agent-friendly.
- Required path flags fail before network requests.
- The local dev-server error gives concrete next actions.
- `--body`, `--body-file`, and field flags give agents multiple composition
  paths.

---

## Recommendations (ranked)

### P0 — Blocks great agent usage

1. Add `list-runs`, `list-functions`, and `list-apps`.
2. Require or loudly echo target env for env-scoped write operations.
3. Distinguish no-auth from bad-auth and add remediation hints.
4. Add first-time app sync/register from URL.
5. Fix validation/status-code issues from the Claude mutating run, especially
   `create-env` returning 500 for missing required fields.

### P1 — Makes agents confident

6. Echo inherited target/auth flags in every subcommand help.
7. Replace single-word field descriptions with semantic help.
8. Mark sensitive response fields, including webhook URLs and decrypted keys.
9. Aggregate validation errors instead of reporting one missing field per run.
10. Resolve env name vs env ID inconsistencies.

### P2 — Smooth chaining

11. Always return `data: []` for empty lists.
12. Always return stable pagination fields.
13. Accept positional path params in addition to `--run-id` style flags.
14. Include `updatedAt` on mutation responses.
15. Add env `kind` / `description` fields for branch placeholders.

---

## Upstream PRs

- [inngest/inngest#4245](https://github.com/inngest/inngest/pull/4245) —
  improves generated subcommand help with OpenAPI operation/field descriptions
  and inherited target/auth flag guidance.
- [inngest/inngest#4246](https://github.com/inngest/inngest/pull/4246) —
  accepts positional path params for generated endpoint commands, while keeping
  the explicit `--run-id`, `--app-id`, and similar flag forms.

---

## Comparison vs Claude Code run

**Both stumbled:** discovery endpoints, inherited help, auth remediation,
silent production env default, first-sync shape, semantic field descriptions.
These are CLI-side issues and should be fixed in the product surface.

**Claude uniquely exposed:** mutating endpoint behavior: `create-env` validation
500, webhook transform discoverability, sensitive webhook URL handling,
name-vs-id inconsistency in `patch-env`, empty PATCH no-op, and validation
ordering for bogus app/function IDs. Codex did not run mutating commands in this
session, so Claude's log is the source of truth for those.

**Codex plugin action taken:** added `inngest-api` skill and captured current
guardrails so future Codex agents start with read-only smoke tests, avoid
implicit production writes, and know when the CLI cannot discover required IDs.
