import { View, Text, FlatList } from "react-native";
import { useEffect, useState } from "react";
import { useAppState } from "../hooks/useAppState";
import { subscribeJobs } from "../hooks/usePusher";

export default function Jobs() {
  const { taskId } = useAppState();
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    if (!taskId) return;

    const disconnect = subscribeJobs(taskId, setJobs);
    return () => disconnect();
  }, [taskId]);

  return (
    <View>
      <Text>Jobs</Text>

      <FlatList
        data={jobs}
        keyExtractor={(item, i) => i.toString()}
        renderItem={({ item }) => (
          <View style={{ margin: 10 }}>
            <Text>{item.title}</Text>
            <Text>{item.company}</Text>
          </View>
        )}
      />
    </View>
  );
}
