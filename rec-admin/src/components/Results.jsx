import { useEffect, useState } from "react";
import SortableShelf from "./SortableShelf";

import { saveCurrentTop } from "../api/client";

export default function Results({ data }) {
  const [carousel, setCarousel] = useState([]);
  const [top10, setTop10] = useState([]);
  const [hot, setHot] = useState([]);
  const [recommendedRatings, setRecommendedRatings] = useState([]);
  const [excludedTitles, setExcludedTitles] = useState([]);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!data) return;

    setCarousel(data.carousel || []);
    setTop10(data.top10 || []);
    setHot(data.hot || []);
    setRecommendedRatings(data.recommended_ratings || []);
    setExcludedTitles(data.excluded_titles || []);
  }, [data]);

  const handleSave = async () => {
    try {
      setIsSaving(true);

      await saveCurrentTop({
        carousel,
        top10,
        hot,
        recommended_ratings: recommendedRatings,
      });

      alert("Порядок сохранён");
    } catch (error) {
      console.error(error);
      alert("Ошибка при сохранении порядка");
    } finally {
      setIsSaving(false);
    }
  };

  const warnings = data?.meta?.warnings || [];

  return (
    <section className="results">
      <div className="section-header">
        <div>
          <p className="eyebrow">Generated report</p>

          <h3>Редактируемые подборки</h3>

          <p className="muted">
            Подборки можно вручную перетаскивать и сохранять.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? "Сохраняем..." : "Сохранить порядок"}
        </button>
      </div>

      {warnings.length > 0 && (
        <div className="report-card warning-card">
          <h4>Предупреждения</h4>

          <ul>
            {warnings.map((warning) => (
              <li key={warning}>{warning}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="shelves-grid">
        <SortableShelf
          title="Carousel"
          items={carousel}
          setItems={setCarousel}
        />

        <SortableShelf
          title="Top 10"
          items={top10}
          setItems={setTop10}
        />

        <SortableShelf
          title="Hot"
          items={hot}
          setItems={setHot}
        />

        <SortableShelf
          title="Рекомендуемые рейтинги"
          description="Лента + Карусель. Рейтинг можно вручную переставлять и сохранить."
          items={recommendedRatings}
          setItems={setRecommendedRatings}
        />
      </div>

      <div className="report-grid">
        <ReportTable
          title="Исключённые тайтлы"
          description="Тайтлы, которые алгоритм исключил из рекомендаций из-за аномального CTR Ленты."
          emptyText="Исключённых тайтлов нет"
          items={excludedTitles}
          columns={[
            { key: "title", label: "Тайтл" },
            { key: "ctr_feed", label: "CTR Ленты" },
            { key: "reason", label: "Причина" },
          ]}
        />

        <div className="report-card">
          <h4>New</h4>

          <p className="muted">
            Подборка New формируется редактором вручную по дате публикации.
            Алгоритм её не трогает. Тайтл из New может одновременно стоять
            в Карусели, Top 10 или Hot — редактор решает самостоятельно.
          </p>
        </div>
      </div>
    </section>
  );
}

function ReportTable({ title, description, items, columns, emptyText }) {
  return (
    <div className="report-card">
      <div className="report-card-header">
        <div>
          <h4>{title}</h4>

          {description && <p className="muted">{description}</p>}
        </div>

        <span>{items.length} items</span>
      </div>

      {items.length === 0 ? (
        <p className="empty-text">{emptyText}</p>
      ) : (
        <div className="table-scroll">
          <table className="report-table">
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column.key}>{column.label}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {items.map((item, index) => (
                <tr key={`${item.title}-${index}`}>
                  {columns.map((column) => (
                    <td key={column.key}>
                      {formatValue(item[column.key])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function formatValue(value) {
  if (value === undefined || value === null || value === "") {
    return "—";
  }

  if (typeof value === "number") {
    return Number.isInteger(value) ? value : value.toFixed(2);
  }

  return String(value);
}