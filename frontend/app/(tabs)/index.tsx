import { View, Button } from "react-native";
import useAuth from "../../hooks/useAuth";
import { useAppState } from "../../hooks/useAppState";

export default function Index() {
  const { token, promptAsync } = useAuth();
  const { setToken } = useAppState();

  if (token) {
    setToken(token);
  }

  return (
    <View style={{ marginTop: 100 }}>
      <Button
        title="Login with Google"
        onPress={() => promptAsync()}
      />
    </View>
  );
}
