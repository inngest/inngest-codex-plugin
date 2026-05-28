import { runSupportAgent } from "@/lib/support-agent";

export async function POST(request: Request) {
  const body = await request.json();
  const result = await runSupportAgent({
    ticketId: body.ticketId,
    accountId: body.accountId,
    question: body.question,
  });

  return Response.json(result);
}
