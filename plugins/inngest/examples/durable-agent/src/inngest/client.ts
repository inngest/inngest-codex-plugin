import { Inngest, eventType } from "inngest";
import { z } from "zod";

export const supportAgentRequested = eventType("support/agent.requested", {
  schema: z.object({
    runId: z.string(),
    ticketId: z.string(),
    accountId: z.string(),
    question: z.string(),
  }),
});

export const supportReplyApproved = eventType("support/reply.approved", {
  schema: z.object({
    runId: z.string(),
    approvalId: z.string(),
  }),
});

export const inngest = new Inngest({
  id: "support-agent-app",
});
