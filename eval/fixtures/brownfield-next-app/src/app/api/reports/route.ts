import { generateReportPdf } from "@/lib/reports";

export async function POST(request: Request) {
  const body = await request.json();
  const pdf = await generateReportPdf({
    accountId: body.accountId,
    range: body.range,
  });

  return Response.json({ url: pdf.url });
}
