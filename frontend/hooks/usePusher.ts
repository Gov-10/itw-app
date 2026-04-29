import {
  Pusher,
  PusherEvent,
} from "@pusher/pusher-websocket-react-native";

type Job = {
  title: string;
  company?: string;
  apply_link?: string;
};

type Payload = {
  taskStatus: string;
  task_id: string;
  ranked: Job[];
  domain?: string;
  skills?: string[];
};

let isInitialized = false;

export const subscribeJobs = async (
  taskId: string,
  onData: (data: Payload) => void
) => {
  const pusher = Pusher.getInstance();
  if (!isInitialized) {
    await pusher.init({
      apiKey: "c9a222f907891fec23ee",
      cluster: "ap2",
    });
    await pusher.connect();
    isInitialized = true;
  }

  const channelName = `task_id-${taskId}`;

  await pusher.subscribe({
    channelName,
    onEvent: (event: PusherEvent) => {
      if (event.eventName === "jobs-ready") {
        try {
          const data: Payload = JSON.parse(event.data);
          console.log("📡 Received:", data);
          onData(data);
        } catch (err) {
          console.log("Parse error:", err);
        }
      }
    },
  });

  return async () => {
    await pusher.unsubscribe({ channelName });
  };
};
