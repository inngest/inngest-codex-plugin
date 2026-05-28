# Next.js Durable Workflow Example

This example shows a minimal Next.js App Router integration where an HTTP route
creates a user, emits an event, and returns quickly. The Inngest function owns
the retryable side effects.

Use it for signup/onboarding, checkout follow-ups, report generation, file
pipelines, and other workflows that should survive deploys and request
timeouts.

## Files

- `src/inngest/client.ts`: shared Inngest client and typed event.
- `src/inngest/functions.ts`: durable workflow with one step per side effect.
- `src/app/api/inngest/route.ts`: serve endpoint.
- `src/app/api/signup/route.ts`: thin route that emits an event.
- `src/lib/services.ts`: placeholder domain services.

## Verification

After adapting:

```bash
INNGEST_DEV=1 npm run dev
npx inngest-cli@latest dev
```

Then exercise the route and confirm the function appears in the dev server.
