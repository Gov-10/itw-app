"use client";

import { signIn, signOut, useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import Pusher from "pusher-js";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL!

export default function Login() {
  const { data: session } = useSession();

  const [taskId, setTaskId] = useState<string | null>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [status, setStatus] = useState("Idle");

  const id_token = (session as any)?.id_token;
  useEffect(() => {
    if (!taskId) return;

    const pusher = new Pusher(process.env.NEXT_PUBLIC_PUSHER_ID!, {
      cluster: "ap2",
    });

    const channel = pusher.subscribe(`task_id-${taskId}`);

    channel.bind("jobs-ready", (data: any) => {
      console.log("Jobs received:", data);
      setJobs(data.ranked || []);
      setStatus(data.taskStatus || "Completed");
    });

    return () => {
      channel.unbind_all();
      pusher.unsubscribe(`task_id-${taskId}`);
      pusher.disconnect();
    };
  }, [taskId]);
  const handleUpload = async (file: File) => {
    if (!id_token) return;

    try {
      setStatus("Uploading...");
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

      const { upload_url, file_key } = await res1.json();
      await fetch(upload_url, {
        method: "PUT",
        body: file,
      });
      const res2 = await fetch(`${BASE_URL}/upload-fin`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${id_token}`,
        },
        body: JSON.stringify({ file_key }),
      });

      const data = await res2.json();
      const match = data.status.match(/[0-9a-f\-]+/);
      const tId = match?.[0];

      if (tId) {
        setTaskId(tId);
        setStatus("Processing...");
      }
    } catch (err) {
      console.error(err);
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
      {/* Existing UI */}
      <p>{session.user?.email}</p>
      <button onClick={() => signOut()}>Logout</button>

      <hr />


      <input
        type="file"
        onChange={(e) => {
          if (e.target.files?.[0]) {
            handleUpload(e.target.files[0]);
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
                <a href={job.apply_link} target="_blank">
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
