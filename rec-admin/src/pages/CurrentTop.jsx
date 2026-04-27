import { useEffect, useState } from "react";
import SortableShelf from "../components/SortableShelf";
import { getCurrentTop, saveCurrentTop } from "../api/client";

export default function CurrentTop() {
  const [carousel, setCarousel] = useState([]);
  const [top10, setTop10] = useState([]);
  const [hot, setHot] = useState([]);
  const [savedAt, setSavedAt] = useState(null);

  useEffect(() => {
    loadCurrentTop();
  }, []);

  const loadCurrentTop = async () => {
    const res = await getCurrentTop();

    setCarousel(res.data.carousel || []);
    setTop10(res.data.top10 || []);
    setHot(res.data.hot || []);
    setSavedAt(res.data.saved_at || null);
  };

  const handleSave = async () => {
    const res = await saveCurrentTop({
      carousel,
      top10,
      hot,
    });

    setCarousel(res.data.carousel || []);
    setTop10(res.data.top10 || []);
    setHot(res.data.hot || []);
    setSavedAt(res.data.saved_at || null);

    alert("Текущий топ сохранен");
  };

  const hasCurrentTop =
    carousel.length > 0 || top10.length > 0 || hot.length > 0;

  if (!hasCurrentTop) {
    return (
      <div>
        <h1>Текущий топ</h1>
        <p>Пока сохраненного топа нет</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Текущий топ</h1>

      {savedAt && (
        <p>Последнее сохранение: {new Date(savedAt).toLocaleString()}</p>
      )}

      <button onClick={handleSave}>
        Сохранить изменения
      </button>

      <SortableShelf title="Carousel" items={carousel} setItems={setCarousel} />
      <SortableShelf title="Top 10" items={top10} setItems={setTop10} />
      <SortableShelf title="Hot" items={hot} setItems={setHot} />
    </div>
  );
}