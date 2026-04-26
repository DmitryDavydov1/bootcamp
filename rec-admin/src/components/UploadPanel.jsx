import { useState } from "react";
import { uploadFile } from "../api/client";

export default function UploadPanel() {
  const [titles, setTitles] = useState(null);
  const [ctr, setCtr] = useState(null);

  const handleUpload = async () => {
    if (titles) await uploadFile(titles);
    if (ctr) await uploadFile(ctr);

    alert("Upload done");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Upload CSV</h2>

      <input type="file" onChange={(e) => setTitles(e.target.files[0])} />
      <input type="file" onChange={(e) => setCtr(e.target.files[0])} />

      <button onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
}