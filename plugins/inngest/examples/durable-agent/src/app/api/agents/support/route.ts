import { inngest } from "@/inngest/client";

export async function POST(request: Request) {
  const body = await request.json();
  const runId = crypto.randomUUID();

  await inngest.send({
    id: `support-agent:${runId}`,
    name: "support/agent.requested",
    data: {
      runId,
      ticketId: body.ticketId,
      accountId: body.accountId,
      question: body.question,
    },
  });

  return Response.json({ runId }, { status: 202 });
}
