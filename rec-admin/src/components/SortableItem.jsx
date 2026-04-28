import {useSortable} from "@dnd-kit/sortable";
import {CSS} from "@dnd-kit/utilities";

const HIDDEN_FIELDS = ["sortableId"];

export default function SortableItem({id, item}) {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({id});

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    };

    const score =
        item.carousel_score ??
        item.top10_score ??
        item.hot_score ??
        item.rating_score;

    const fields = Object.entries(item).filter(
        ([key, value]) =>
            !HIDDEN_FIELDS.includes(key) &&
            key !== "title" &&
            value !== undefined &&
            value !== null
    );

    return (
        <article
            ref={setNodeRef}
            style={style}
            className={isDragging ? "tile dragging" : "tile"}
            {...attributes}
            {...listeners}
        >
            <div className="tile-top">
                <h4>{item.title || "Без названия"}</h4>

                {score !== undefined && (
                    <span className="score">{Number(score).toFixed(2)}</span>
                )}
            </div>

            <div className="metrics">
                {fields.map(([key, value]) => (
                    <Metric key={key} label={formatLabel(key)} value={value}/>
                ))}
            </div>
        </article>
    );
}

function Metric({label, value}) {
    return (
        <div className="metric">
            <span>{label}</span>
            <strong>{formatValue(value)}</strong>
        </div>
    );
}

function formatLabel(key) {
    return key
        .replaceAll("_", " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatValue(value) {
    if (typeof value === "number") {
        return Number.isInteger(value) ? value : value.toFixed(2);
    }

    if (typeof value === "boolean") {
        return value ? "Да" : "Нет";
    }

    if (Array.isArray(value)) {
        return value.join(", ");
    }

    if (typeof value === "object") {
        return JSON.stringify(value);
    }

    return String(value);
}