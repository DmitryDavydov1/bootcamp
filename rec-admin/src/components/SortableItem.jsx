import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

export default function SortableItem({ id, item }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    padding: "12px",
    marginBottom: "8px",
    background: "#fff",
    border: "1px solid #ddd",
    borderRadius: "8px",
    cursor: "grab",
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <strong>{item.title}</strong>

      <div className="item-meta">
        {item.rating !== undefined && (
          <span>Rating: {item.rating}</span>
        )}

        {item.views !== undefined && (
          <span>Views: {item.views}</span>
        )}

        {item.ctr_carousel !== undefined && (
          <span>CTR Carousel: {formatNumber(item.ctr_carousel)}%</span>
        )}

        {item.ctr_feed !== undefined && (
          <span>CTR Feed: {formatNumber(item.ctr_feed)}%</span>
        )}

        {item.depth !== undefined && (
          <span>Depth: {formatNumber(item.depth)}%</span>
        )}

        {item.bwr !== undefined && (
          <span>BWR: {formatNumber(item.bwr)}</span>
        )}

        {item.base_score !== undefined && (
          <span>Base: {formatNumber(item.base_score)}</span>
        )}

        {item.rating_score !== undefined && (
          <span>Rating Score: {formatNumber(item.rating_score)}</span>
        )}

        {item.carousel_score !== undefined && (
          <span>Score: {formatNumber(item.carousel_score)}</span>
        )}

        {item.top10_score !== undefined && (
          <span>Score: {formatNumber(item.top10_score)}</span>
        )}

        {item.hot_score !== undefined && (
          <span>Score: {formatNumber(item.hot_score)}</span>
        )}
      </div>

      {item.note && (
        <p className="item-note">{item.note}</p>
      )}
    </div>
  );
}

function formatNumber(value) {
  if (typeof value !== "number") {
    return value;
  }

  return Number.isInteger(value) ? value : value.toFixed(2);
}