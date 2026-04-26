import { useState } from "react";
import UploadPanel from "../components/UploadPanel";
import Results from "../components/Results";
import { generateReport } from "../api/client";

export default function Dashboard() {
  const [data, setData] = useState(null);

  const handleGenerate = async () => {
    const res = await generateReport();
    setData(res.data);
  };

  return (
    <div>
      <UploadPanel />

      <button onClick={handleGenerate}>
        Generate report
      </button>

      {data && <Results data={data} />}
    </div>
  );
}



