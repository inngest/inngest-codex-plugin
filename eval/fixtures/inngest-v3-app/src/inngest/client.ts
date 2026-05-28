import { EventSchemas, Inngest } from "inngest";
import { realtimeMiddleware } from "@inngest/realtime";

type Events = {
  "support/ticket.created": {
    data: {
      ticketId: string;
      accountId: string;
    };
  };
  "support/reply.approved": {
    data: {
      ticketId: string;
      approvalId: string;
    };
  };
};

export const inngest = new Inngest({
  id: "support-app",
  logLevel: "debug",
  middleware: [realtimeMiddleware()],
  schemas: new EventSchemas().fromRecord<Events>(),
});
