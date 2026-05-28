export async function getTicket(ticketId: string) {
  return {
    id: ticketId,
    subject: "Billing question",
    body: "Can you help me understand this invoice?",
  };
}

export async function getAccount(accountId: string) {
  return {
    id: accountId,
    plan: "enterprise",
    health: "healthy",
  };
}

export async function searchKnowledgeBase(question: string) {
  return [{ id: "kb_1", title: "Billing FAQ", question }];
}

export async function saveDraftForApproval(input: {
  runId: string;
  ticketId: string;
  draft: unknown;
}) {
  return input;
}

export async function sendApprovedReply(input: {
  runId: string;
  ticketId: string;
  approvalId: string;
}) {
  return input;
}
