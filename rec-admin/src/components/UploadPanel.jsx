import { useState } from "react";
import { uploadFile } from "../api/client";

export default function UploadPanel() {
  const [titles, setTitles] = useState(null);
  const [ctr, setCtr] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    try {
      setIsUploading(true);

      if (titles) await uploadFile(titles);
      if (ctr) await uploadFile(ctr);

      alert("Файлы загружены");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <section className="panel upload-panel">
      <div>
        <p className="eyebrow">CSV upload</p>
        <h3>Загрузка данных</h3>
        <p className="muted">
          Добавь файлы с тайтлами и CTR-метриками.
        </p>
      </div>

      <div className="upload-grid">
        <label className="file-card">
          <span>Titles CSV</span>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setTitles(e.target.files[0])}
          />
          <strong>{titles ? titles.name : "Выбрать файл"}</strong>
        </label>

        <label className="file-card">
          <span>CTR CSV</span>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setCtr(e.target.files[0])}
          />
          <strong>{ctr ? ctr.name : "Выбрать файл"}</strong>
        </label>
      </div>

      <button
        className="secondary-button"
        onClick={handleUpload}
        disabled={isUploading || (!titles && !ctr)}
      >
        {isUploading ? "Загружаем..." : "Загрузить CSV"}
      </button>
    </section>
  );
}