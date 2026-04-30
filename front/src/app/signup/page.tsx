"use client";
import { signIn, signOut, useSession } from "next-auth/react";
export default function Login() {
  const { data: session } = useSession();
  console.log((session as any)?.id_token);
  if (session) {
    return (
      <>
        <p>{session.user?.email}</p>
        <button onClick={() => signOut()}>Logout</button>
      </>
    );
  }

  return (
    <button onClick={() => signIn("google")}>
      Sign in with Google
    </button>
  );
}
