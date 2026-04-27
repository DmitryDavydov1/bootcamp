import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

export default function SortableItem({ id, item }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const score =
    item.carousel_score ??
    item.top10_score ??
    item.hot_score ??
    item.rating_score;

  return (
    <article
      ref={setNodeRef}
      style={style}
      className={isDragging ? "tile dragging" : "tile"}
      {...attributes}
      {...listeners}
    >
      <div className="tile-top">
        <h4>{item.title}</h4>
        {score !== undefined && (
          <span className="score">{Number(score).toFixed(2)}</span>
        )}
      </div>

      <div className="metrics">
        <Metric label="Views" value={item.views} />
        <Metric label="CTR carousel" value={item.ctr_carousel} suffix="%" />
        <Metric label="CTR feed" value={item.ctr_feed} suffix="%" />
        <Metric label="Depth" value={item.depth} suffix="%" />
        <Metric label="BWR" value={item.bwr} />
        <Metric label="Time" value={item.total_time} />
      </div>
    </article>
  );
}

function Metric({ label, value, suffix = "" }) {
  if (value === undefined || value === null) return null;

  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}{suffix}</strong>
    </div>
  );
}