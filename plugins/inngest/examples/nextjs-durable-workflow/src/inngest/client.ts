import { Inngest, eventType } from "inngest";
import { z } from "zod";

export const userCreated = eventType("user/created", {
  schema: z.object({
    userId: z.string(),
    email: z.string().email(),
    signupRequestId: z.string(),
  }),
});

export const inngest = new Inngest({
  id: "my-app",
  // For local development set INNGEST_DEV=1. In production set
  // INNGEST_SIGNING_KEY in the environment.
});
