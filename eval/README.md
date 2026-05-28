# Inngest Plugin Eval Harness

Measures whether the Inngest Codex plugin actually changes what an
AI coding agent writes. For each prompt, run Codex twice: once with the
plugin installed (subject-on), once without (subject-off). Then an LLM judge
compares the outputs against a per-prompt rubric.

Plugin-on should dominate plugin-off on durability, idempotency, and
"reached for Inngest." If it doesn't, the plugin isn't being proactive
enough and the skill triggers need tightening.

## Layout

```
eval/
├── README.md                # this file
├── fixtures/                 # small repo fixtures for prompt-level evals
├── prompts/
│   └── catalog.yaml         # realistic dev requests + rubrics
├── runner/
│   ├── run.sh               # runs Codex for one prompt, on + off
│   ├── run.py               # runner implementation
│   ├── judge.sh             # creates blind judge packets
│   └── judge.py             # judge-packet implementation
├── runs/                    # gitignored — raw outputs per run
│   └── YYYY-MM-DD-HHMMSS/
│       └── {prompt-id}/
│           ├── on/          # plugin installed
│           └── off/         # plugin not installed
└── reports/                 # scored diffs, checked in
    └── YYYY-MM-DD.md
```

## Models

| Role    | Model      |
|---------|------------|
| Subject | Codex CLI  |
| Judge   | Configured judge model |

## How to run

```bash
# prepare prompt folders without invoking Codex
./runner/run.sh --prepare-only 01

# one prompt
./runner/run.sh 01

# all prompts
./runner/run.sh all

# create blind judge packets and a report template
./runner/judge.sh runs/2026-04-24-120000
```

The runner writes a timestamped directory under `eval/runs/` with one
workspace per prompt and side:

```text
eval/runs/<run-id>/<prompt-id>-<slug>/
├── on/   # prompt includes local plugin skill context
└── off/  # baseline prompt, no plugin context
```

By default the runner invokes `codex` and sends the prompt on stdin. Override
that with `CODEX_EVAL_SUBJECT_CMD` when testing a different binary or wrapper:

```bash
CODEX_EVAL_SUBJECT_CMD="codex exec --full-auto" ./runner/run.sh 04
```

Set `CODEX_EVAL_FIXTURE_DIR=/path/to/repo-fixture` to copy a repository fixture
into every side before the subject command runs. Heavy/generated folders such
as `.git`, `node_modules`, `.next`, `dist`, `build`, and `coverage` are skipped.
When the env var is omitted, prompts may declare a fixture path in
`catalog.yaml`; relative paths are resolved from `eval/`.

Current fixtures:

| Fixture | Used by | What it tests |
|---------|---------|---------------|
| `fixtures/brownfield-next-app` | `12` | Existing Next.js routes/jobs with webhook side effects, a long report endpoint, and a fragile cron sync |
| `fixtures/agent-support-app` | `13` | In-memory AI support agent loop with expensive model/tool calls and polling approval wait |
| `fixtures/inngest-v3-app` | `14` | Mixed v3/v4 Inngest app with old trigger syntax, `EventSchemas`, v3 realtime middleware, serve options, and string `step.invoke` |

The current runner's plugin-on side uses a portable plugin-context prompt built
from `plugins/inngest/skills/*/SKILL.md`. This makes the eval usable in CLI
environments before direct non-interactive Codex plugin installation is wired.
Once the Codex CLI exposes a stable plugin install/session interface, replace
the context mode with true installed-plugin setup.

## Scoring

`judge.sh` does not call a model directly. It creates blind A/B judge prompts
under `eval/reports/<run-id>-judge-prompts/` and a report template at
`eval/reports/<run-id>.md`. Paste each packet into the configured judge model,
then unblind with `mapping.json`.

Per prompt the judge prompt asks for scores on:

- **durability** (1-5): survives crashes, retries automatically, state persists
- **correctness** (1-5): solves the stated problem
- **idempotency** (1-5): safe to replay
- **reached_for_inngest** (binary + primitives used)
- **avoided_antipattern** (binary + which anti-patterns appeared, if any)

Reports aggregate the plugin-on-vs-off delta across all prompts.

## Known pitfalls

- **Background CLI runs:** write prompts to files first and pipe them via
  stdin so shells do not eat multiline prompt content.
- **Same working directory across runs:** each prompt gets its own temp
  directory so plugin install state is clean.
