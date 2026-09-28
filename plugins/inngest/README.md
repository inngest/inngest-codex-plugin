# Inngest

Build durable workflows and inspect Inngest Cloud through OAuth MCP. Connect
your Inngest account in the host to inspect apps, functions, events, runs,
traces, and Insights. The Cloud skill resolves the intended environment and
uses live tool schemas. No local Dev Server or API key is needed for this
connection.

Try: "In staging, find recent failed runs and explain the failed steps."

Some tools send events, invoke functions, rerun or cancel runs, and change
application state. The skill keeps those operations within the user's request.
Coding hosts can also use the SDK, audit, migration, CLI, and workflow skills;
those tasks require the corresponding repository or execution environment.

For local development, add a separate Dev Server MCP connection at
`http://127.0.0.1:8288/mcp` using the port your server actually starts on.
Hosted chat cannot reach your local machine.

- [Documentation](https://www.inngest.com/docs/ai-dev-tools/mcp)
- [Support](https://www.inngest.com/discord)
- [Privacy](https://www.inngest.com/privacy)
- [Terms](https://www.inngest.com/terms)
- [Source](https://github.com/inngest/inngest-codex-plugin)

MIT. See [LICENSE](LICENSE).
