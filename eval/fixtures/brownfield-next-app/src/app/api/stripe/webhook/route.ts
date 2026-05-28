import Stripe from "stripe";
import { sendOrderEmail } from "@/lib/email";
import { upgradeAccount } from "@/lib/accounts";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "sk_test_missing");

export async function POST(request: Request) {
  const rawBody = await request.text();
  const signature = request.headers.get("stripe-signature");

  if (!signature) {
    return new Response("missing signature", { status: 400 });
  }

  const event = stripe.webhooks.constructEvent(
    rawBody,
    signature,
    process.env.STRIPE_WEBHOOK_SECRET ?? "whsec_missing"
  );

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;
    const userId = String(session.metadata?.userId);
    const email = String(session.customer_details?.email);

    await sendOrderEmail(email, session.id);
    await upgradeAccount(userId, "pro");
  }

  return Response.json({ received: true });
}
