import * as Google from "expo-auth-session/providers/google";
import { useEffect, useState } from "react";
import * as WebBrowser from "expo-web-browser";

WebBrowser.maybeCompleteAuthSession();

export default function useAuth() {
  const [token, setToken] = useState<string | null>(null);

  const [request, response, promptAsync] = Google.useAuthRequest({
    clientId: "YOUR_GOOGLE_CLIENT_ID",
  });

  useEffect(() => {
    if (response?.type === "success") {
      const id_token = response.params.id_token;
      setToken(id_token);
    }
  }, [response]);

  return {
    token,
    promptAsync,
  };
}
