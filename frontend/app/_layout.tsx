import { Stack } from "expo-router";
import { AppProvider } from "../hooks/useAppState";

export default function RootLayout() {
  return (
    <AppProvider>
      <Stack />
    </AppProvider>
  );
}
