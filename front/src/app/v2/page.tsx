"use client";

import { signIn, signOut, useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import Pusher from "pusher-js";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL!;

export default function Login() {
  const { data: session } = useSession();

  const [taskId, setTaskId] = useState<string | null>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [status, setStatus] = useState("Idle");

  const id_token = (session as any)?.id_token;

  useEffect(() => {
    if (!taskId) return;

    console.log("Connecting to Pusher...");
    console.log("Task ID:", taskId);

    const pusher = new Pusher(process.env.NEXT_PUBLIC_PUSHER_ID!, {
      cluster: "ap2",
    });

    const channelName = `task_id-${taskId}`;

    const channel = pusher.subscribe(channelName);

    channel.bind("pusher:subscription_succeeded", () => {
      console.log("Subscribed successfully:", channelName);
    });

    channel.bind("jobs-ready", (data: any) => {
      console.log("Jobs received from Pusher:");
      console.log(data);

      setJobs(data.ranked || []);
      setStatus(data.taskStatus || "Completed");
    });

    channel.bind("pusher:error", (err: any) => {
      console.error("Pusher error:", err);
    });

    return () => {
      console.log("Cleaning up Pusher connection");

      channel.unbind_all();
      pusher.unsubscribe(channelName);
      pusher.disconnect();
    };
  }, [taskId]);

  const handleUpload = async (file: File) => {
    if (!id_token) {
      console.error("No ID token found");
      return;
    }

    try {
      console.log("================================");
      console.log("UPLOAD FLOW STARTED");
      console.log("================================");

      console.log("Selected file:");
      console.log({
        name: file.name,
        size: file.size,
        type: file.type,
      });

      setStatus("Uploading...");

      console.log("Requesting presigned URL...");

      const res1 = await fetch(`${BASE_URL}/upload`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${id_token}`,
        },
        body: JSON.stringify({
          file_name: file.name,
          content_type: file.type,
        }),
      });

      console.log("Upload endpoint response status:", res1.status);

      const uploadData = await res1.json();

      console.log("Upload endpoint response:");
      console.log(uploadData);

      const { upload_url, file_key } = uploadData;

      if (!upload_url) {
        throw new Error("No upload URL returned");
      }

      console.log("Presigned URL generated successfully");
      console.log("File key:", file_key);

      console.log("Starting S3 upload...");

      const uploadRes = await fetch(upload_url, {
        method: "PUT",
        body: file,
      });

      console.log("S3 upload completed");
      console.log("S3 response status:", uploadRes.status);
      console.log("S3 response ok:", uploadRes.ok);

      const uploadText = await uploadRes.text();

      console.log("S3 response body:");
      console.log(uploadText);

      if (!uploadRes.ok) {
        throw new Error(
          `S3 upload failed with status ${uploadRes.status}`
        );
      }

      console.log("S3 upload successful");

      console.log("Calling upload-fin endpoint...");

      const res2 = await fetch(`${BASE_URL}/upload-fin`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${id_token}`,
        },
        body: JSON.stringify({ file_key }),
      });

      console.log("upload-fin response status:", res2.status);

      const data = await res2.json();

      console.log("upload-fin response body:");
      console.log(data);

      const match = data.status?.match(/[0-9a-f\-]+/);

      console.log("Extracted task ID:", match?.[0]);

      const tId = match?.[0];

      if (tId) {
        setTaskId(tId);
        setStatus("Processing...");
      } else {
        console.error("Task ID extraction failed");
      }

      console.log("================================");
      console.log("UPLOAD FLOW FINISHED");
      console.log("================================");

    } catch (err) {
      console.error("================================");
      console.error("UPLOAD FLOW FAILED");
      console.error("================================");

      console.error(err);

      if (err instanceof Error) {
        console.error("Error message:", err.message);
        console.error("Error stack:", err.stack);
      }

      setStatus("Error occurred");
    }
  };

  if (!session) {
    return (
      <div style={{ padding: 20 }}>
        <button onClick={() => signIn("google")}>
          Sign in with Google
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <p>{session.user?.email}</p>

      <button onClick={() => signOut()}>
        Logout
      </button>

      <hr />

      <input
        type="file"
        onChange={(e) => {
          console.log("File input changed");

          if (e.target.files?.[0]) {
            console.log("File detected");

            handleUpload(e.target.files[0]);
          } else {
            console.log("No file selected");
          }
        }}
      />

      <p>Status: {status}</p>

      {jobs.length > 0 && (
        <div>
          <h3>Jobs</h3>

          {jobs.map((job, i) => (
            <div
              key={i}
              style={{
                border: "1px solid #ccc",
                padding: 12,
                marginTop: 10,
                borderRadius: 8,
              }}
            >
              <h4>{job.title}</h4>

              <p>{job.company}</p>

              {job.apply_link && (
                <a
                  href={job.apply_link}
                  target="_blank"
                  rel="noreferrer"
                >
                  Apply →
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
