type Lead = {
  id: string;
  email: string;
};

export async function fetchHubSpotLeadsPage(cursor?: string): Promise<{
  leads: Lead[];
  nextCursor?: string;
}> {
  console.log("fetch hubspot page", cursor);
  return { leads: [] };
}

export async function upsertLead(lead: Lead) {
  console.log("upsert lead", lead.id);
}
