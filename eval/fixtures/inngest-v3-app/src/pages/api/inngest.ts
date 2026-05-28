import { serve } from "inngest/next";
import { inngest } from "@/inngest/client";
import { functions } from "@/inngest/functions";

export default serve({
  client: inngest,
  functions,
  signingKey: process.env.INNGEST_SIGNING_KEY,
  baseUrl: process.env.INNGEST_BASE_URL,
  streaming: "force",
});
