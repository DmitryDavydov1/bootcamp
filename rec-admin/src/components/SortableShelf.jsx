import { DndContext, closestCenter } from "@dnd-kit/core";

import {
  SortableContext,
  verticalListSortingStrategy,
  arrayMove,
} from "@dnd-kit/sortable";

import SortableItem from "./SortableItem";

export default function SortableShelf({ title, description, items, setItems }) {
  const getItemId = (item, index) => {
    return item.id || `${title}-${item.title}-${index}`;
  };

  const itemIds = items.map((item, index) => getItemId(item, index));

  const handleDragEnd = (event) => {
    const { active, over } = event;

    if (!over || active.id === over.id) return;

    const oldIndex = itemIds.findIndex((id) => id === active.id);
    const newIndex = itemIds.findIndex((id) => id === over.id);

    if (oldIndex === -1 || newIndex === -1) return;

    setItems(arrayMove(items, oldIndex, newIndex));
  };

  return (
    <div className="shelf-card">
      <div className="shelf-header">
        <div>
          <h4>{title}</h4>

          {description && <p className="muted">{description}</p>}
        </div>

        <span>{items.length} items</span>
      </div>

      <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={itemIds} strategy={verticalListSortingStrategy}>
          {items.map((item, index) => (
            <SortableItem
              key={getItemId(item, index)}
              id={getItemId(item, index)}
              item={item}
            />
          ))}
        </SortableContext>
      </DndContext>
    </div>
  );
}