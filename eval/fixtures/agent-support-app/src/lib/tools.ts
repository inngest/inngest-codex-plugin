export async function getTicket(ticketId: string) {
  return { id: ticketId, subject: "Refund request", status: "open" };
}

export async function getAccount(accountId: string) {
  return { id: accountId, plan: "enterprise", health: "at-risk" };
}

export async function searchKnowledgeBase(query: string) {
  return [{ id: "kb_1", title: "Refund policy", query }];
}

export async function sendDraftReply(ticketId: string, draft: string) {
  console.log("send draft", ticketId, draft);
}
