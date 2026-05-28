import OpenAI from "openai";
import {
  getAccount,
  getTicket,
  searchKnowledgeBase,
  sendDraftReply,
} from "./tools";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const pendingApprovals = new Map<string, { approved: boolean }>();

export async function runSupportAgent(input: {
  ticketId: string;
  accountId: string;
  question: string;
}) {
  const ticket = await getTicket(input.ticketId);
  const account = await getAccount(input.accountId);
  const articles = await searchKnowledgeBase(input.question);

  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "Draft a support response. Ask for manager approval for refunds.",
      },
      {
        role: "user",
        content: JSON.stringify({ ticket, account, articles }),
      },
    ],
  });

  const draft = completion.choices[0]?.message.content ?? "";

  if (draft.toLowerCase().includes("refund")) {
    pendingApprovals.set(input.ticketId, { approved: false });
    await waitForApproval(input.ticketId);
  }

  await sendDraftReply(input.ticketId, draft);
  return { ticketId: input.ticketId, draft };
}

async function waitForApproval(ticketId: string) {
  while (!pendingApprovals.get(ticketId)?.approved) {
    await new Promise((resolve) => setTimeout(resolve, 30_000));
  }
}
