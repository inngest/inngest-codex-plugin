import { inngest, userCreated } from "./client";
import {
  addUserToCrm,
  createStripeCustomer,
  sendWelcomeEmail,
} from "@/lib/services";

export const onboardUser = inngest.createFunction(
  {
    id: "onboard-user",
    triggers: [userCreated],
    retries: 4,
  },
  async ({ event, step }) => {
    const stripeCustomer = await step.run("create-stripe-customer", () => {
      return createStripeCustomer({
        userId: event.data.userId,
        email: event.data.email,
        idempotencyKey: event.data.signupRequestId,
      });
    });

    await step.run("add-user-to-crm", () => {
      return addUserToCrm({
        userId: event.data.userId,
        email: event.data.email,
        stripeCustomerId: stripeCustomer.id,
      });
    });

    await step.run("send-welcome-email", () => {
      return sendWelcomeEmail({
        userId: event.data.userId,
        email: event.data.email,
      });
    });

    return { userId: event.data.userId };
  }
);

export const functions = [onboardUser];
