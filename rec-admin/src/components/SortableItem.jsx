import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

export default function SortableItem({ item }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({
    id: item.title,
  });

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
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
    >
      <strong>{item.title}</strong>

      <div style={{ fontSize: 12, color: "#666", marginTop: 6 }}>
        {item.views !== undefined && <div>Views: {item.views}</div>}
        {item.ctr_carousel !== undefined && <div>CTR Carousel: {item.ctr_carousel}%</div>}
        {item.ctr_feed !== undefined && <div>CTR Feed: {item.ctr_feed}%</div>}
        {item.depth !== undefined && <div>Depth: {item.depth}%</div>}
        {item.bwr !== undefined && <div>BWR: {item.bwr}</div>}

        {item.carousel_score !== undefined && (
          <div>Score: {item.carousel_score.toFixed(2)}</div>
        )}
        {item.top10_score !== undefined && (
          <div>Score: {item.top10_score.toFixed(2)}</div>
        )}
        {item.hot_score !== undefined && (
          <div>Score: {item.hot_score.toFixed(2)}</div>
        )}
      </div>
    </div>
  );
}