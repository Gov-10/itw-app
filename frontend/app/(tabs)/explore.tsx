import { View, Button } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import { useAppState } from "../../hooks/useAppState";
import { uploadInit, uploadFinish } from "../../hooks/useApi";
import { useRouter } from "expo-router";

export default function Upload() {
  const { token, setTaskId } = useAppState();
  const router = useRouter();

  const handleUpload = async () => {
    const res = await DocumentPicker.getDocumentAsync({});
    const file = res.assets[0];

    const { upload_url, file_key } = await uploadInit(token, file);

    await fetch(upload_url, {
      method: "PUT",
      body: await fetch(file.uri).then((r) => r.blob()),
      headers: {
        "Content-Type": file.mimeType,
      },
    });

    const fin = await uploadFinish(token, file_key);

    const taskId = fin.status.match(/[0-9a-f\-]+/)[0];

    setTaskId(taskId);

    router.push("/modal"); // go to jobs screen
  };

  return (
    <View>
      <Button title="Upload Resume" onPress={handleUpload} />
    </View>
  );
}
