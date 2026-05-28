import cron from "node-cron";
import { fetchHubSpotLeadsPage, upsertLead } from "@/lib/hubspot";

cron.schedule("0 2 * * *", async () => {
  let cursor: string | undefined;

  do {
    const page = await fetchHubSpotLeadsPage(cursor);
    for (const lead of page.leads) {
      await upsertLead(lead);
    }
    cursor = page.nextCursor;
  } while (cursor);
});
