export async function createUser(input: {
  email: string;
  signupRequestId: string;
}) {
  return {
    id: `user_${input.signupRequestId}`,
    email: input.email,
  };
}

export async function createStripeCustomer(input: {
  userId: string;
  email: string;
  idempotencyKey: string;
}) {
  return {
    id: `cus_${input.userId}`,
  };
}

export async function addUserToCrm(input: {
  userId: string;
  email: string;
  stripeCustomerId: string;
}) {
  return input;
}

export async function sendWelcomeEmail(input: {
  userId: string;
  email: string;
}) {
  return input;
}
