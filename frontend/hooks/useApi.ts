import axios from "axios";

const BASE_URL = "http://YOUR_BACKEND_URL";

type UploadInitResponse = {
  upload_url: string;
  file_key: string;
};

type UploadFinishResponse = {
  status: string;
};

export const uploadInit = async (
  token: string,
  file: any
): Promise<UploadInitResponse> => {
  const res = await axios.post(
    `${BASE_URL}/upload`,
    {
      file_name: file.name,
      content_type: file.mimeType,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return res.data;
};

export const uploadFinish = async (
  token: string,
  file_key: string
): Promise<UploadFinishResponse> => {
  const res = await axios.post(
    `${BASE_URL}/upload-fin`,
    { file_key },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return res.data;
};
