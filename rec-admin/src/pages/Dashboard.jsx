import { useState } from "react";
import UploadPanel from "../components/UploadPanel";
import Results from "../components/Results";
import { generateReport } from "../api/client";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    try {
      setIsGenerating(true);
      const res = await generateReport();
      setData(res.data);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h2>Отчет по рекомендациям</h2>
          <p className="page-description">
            Загрузи CSV, сгенерируй подборки и отредактируй порядок тайлов.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={handleGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? "Генерируем..." : "Сгенерировать отчет"}
        </button>
      </header>

      <UploadPanel />

      {data ? (
        <Results data={data} />
      ) : (
        <div className="empty-state">
          <h3>Отчет пока не сгенерирован</h3>
          <p>Нажми «Сгенерировать отчет», чтобы увидеть подборки.</p>
        </div>
      )}
    </div>
  );
}