import { createAgent, openai } from "@inngest/agent-kit";
import { inngest, supportAgentRequested, supportReplyApproved } from "./client";
import {
  getAccount,
  getTicket,
  saveDraftForApproval,
  searchKnowledgeBase,
  sendApprovedReply,
} from "@/lib/support-tools";

export const runSupportAgent = inngest.createFunction(
  {
    id: "run-support-agent",
    triggers: [supportAgentRequested],
    concurrency: [{ key: "event.data.accountId", limit: 2 }],
    throttle: {
      key: `"openai"`,
      limit: 120,
      period: "1m",
    },
  },
  async ({ event, step }) => {
    const [ticket, account, articles] = await Promise.all([
      step.run("load-ticket", () => getTicket(event.data.ticketId)),
      step.run("load-account", () => getAccount(event.data.accountId)),
      step.run("search-knowledge-base", () =>
        searchKnowledgeBase(event.data.question)
      ),
    ]);

    const agent = createAgent({
      name: "support-agent",
      system:
        "Draft a helpful support reply. Escalate if policy-sensitive actions are needed.",
      model: openai({ model: "gpt-4o-mini" }),
    });

    const { output } = await agent.run(
      JSON.stringify({
        ticket,
        account,
        articles,
        question: event.data.question,
      })
    );

    await step.run("save-draft-for-approval", () =>
      saveDraftForApproval({
        runId: event.data.runId,
        ticketId: event.data.ticketId,
        draft: output,
      })
    );

    const approval = await step.waitForEvent("wait-for-approval", {
      event: supportReplyApproved,
      timeout: "3d",
      match: "data.runId",
    });

    if (!approval) {
      return { status: "expired", runId: event.data.runId };
    }

    await step.run("send-approved-reply", () =>
      sendApprovedReply({
        runId: event.data.runId,
        ticketId: event.data.ticketId,
        approvalId: approval.data.approvalId,
      })
    );

    return { status: "sent", runId: event.data.runId };
  }
);

export const functions = [runSupportAgent];
