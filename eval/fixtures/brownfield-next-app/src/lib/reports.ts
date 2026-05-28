export async function generateReportPdf(input: {
  accountId: string;
  range: string;
}) {
  console.log("generate report", input);
  await new Promise((resolve) => setTimeout(resolve, 60_000));
  return { url: `https://example.com/reports/${input.accountId}.pdf` };
}
