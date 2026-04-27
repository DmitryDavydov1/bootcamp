import { useEffect, useState } from "react";
import SortableShelf from "./SortableShelf";
import { saveCurrentTop } from "../api/client";

export default function Results({ data }) {
  const [carousel, setCarousel] = useState([]);
  const [top10, setTop10] = useState([]);
  const [hot, setHot] = useState([]);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!data) return;

    setCarousel(data.carousel || []);
    setTop10(data.top10 || []);
    setHot(data.hot || []);
  }, [data]);

  const handleSave = async () => {
    try {
      setIsSaving(true);

      await saveCurrentTop({
        carousel,
        top10,
        hot,
      });

      alert("Порядок сохранен");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <section className="results">
      <div className="section-header">
        <div>
          <p className="eyebrow">Generated report</p>
          <h3>Редактируемые подборки</h3>
        </div>

        <button
          className="primary-button"
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? "Сохраняем..." : "Сохранить порядок"}
        </button>
      </div>

      <div className="shelves-grid">
        <SortableShelf title="Carousel" items={carousel} setItems={setCarousel} />
        <SortableShelf title="Top 10" items={top10} setItems={setTop10} />
        <SortableShelf title="Hot" items={hot} setItems={setHot} />
      </div>
    </section>
  );
}