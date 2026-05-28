import { inngest } from "./client";
import { sendReply } from "@/lib/support";

export const sendSupportReply = inngest.createFunction(
  { id: "send-support-reply" },
  { event: "support/ticket.created" },
  async ({ event, step, publish }) => {
    await publish({
      channel: `ticket:${event.data.ticketId}`,
      topic: "status",
      data: { status: "drafting" },
    });

    const approval = await step.waitForEvent("wait-for-approval", {
      event: "support/reply.approved",
      timeout: "3d",
      match: "data.ticketId",
    });

    if (!approval) {
      return { status: "expired" };
    }

    await step.invoke("notify-account-owner", {
      function: "support-app-notify-account-owner",
      data: {
        accountId: event.data.accountId,
        ticketId: event.data.ticketId,
      },
    });

    await step.run("send-reply", () => sendReply(event.data.ticketId));
    return { status: "sent" };
  }
);

export const functions = [sendSupportReply];
