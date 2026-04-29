import { Tabs } from "expo-router";

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: "Login" }} />
      <Tabs.Screen name="explore" options={{ title: "Upload" }} />
    </Tabs>
  );
}
