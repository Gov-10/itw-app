import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
} from "react-native";
import { useEffect, useState } from "react";
import { useAppState } from "../hooks/useAppState";
import { subscribeJobs } from "../hooks/usePusher";

export default function Jobs() {
  const { taskId } = useAppState();

  const [jobs, setJobs] = useState<any[]>([]);
  const [status, setStatus] = useState("Waiting...");
  const [domain, setDomain] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) return;

    let cleanup: (() => Promise<void>) | null = null;

    (async () => {
      cleanup = await subscribeJobs(taskId, (data) => {
        console.log("📦 Payload:", data);

        setJobs(data.ranked || []);
        setStatus(data.taskStatus || "Completed");
        setDomain(data.domain || null);
      });
    })();

    return () => {
      if (cleanup) {
        cleanup(); // unsubscribe
      }
    };
  }, [taskId]);

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 18, fontWeight: "bold" }}>
        Job Results
      </Text>

      <Text>Status: {status}</Text>
      {domain && <Text>Domain: {domain}</Text>}

      {jobs.length === 0 ? (
        <ActivityIndicator size="large" style={{ marginTop: 20 }} />
      ) : (
        <FlatList
          data={jobs}
          keyExtractor={(item, i) => i.toString()}
          renderItem={({ item }) => (
            <View
              style={{
                marginVertical: 8,
                padding: 12,
                borderWidth: 1,
                borderRadius: 8,
              }}
            >
              <Text style={{ fontWeight: "bold" }}>
                {item.title}
              </Text>
              <Text>{item.company}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
}
