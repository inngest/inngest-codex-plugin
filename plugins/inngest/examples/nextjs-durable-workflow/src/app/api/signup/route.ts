import { inngest } from "@/inngest/client";
import { createUser } from "@/lib/services";

export async function POST(request: Request) {
  const body = await request.json();
  const signupRequestId = crypto.randomUUID();

  const user = await createUser({
    email: body.email,
    signupRequestId,
  });

  await inngest.send({
    id: `signup:${signupRequestId}`,
    name: "user/created",
    data: {
      userId: user.id,
      email: user.email,
      signupRequestId,
    },
  });

  return Response.json({ userId: user.id }, { status: 201 });
}
