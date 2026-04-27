import { DndContext, closestCenter } from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
  arrayMove,
} from "@dnd-kit/sortable";

import SortableItem from "./SortableItem";

export default function SortableShelf({ title, items = [], setItems }) {
  const itemsWithIds = items.map((item, index) => ({
    ...item,
    sortableId: `${title}-${index}-${item.title}`,
  }));

  const handleDragEnd = (event) => {
    const { active, over } = event;

    if (!over || active.id === over.id) return;

    const oldIndex = itemsWithIds.findIndex(
      (item) => item.sortableId === active.id
    );

    const newIndex = itemsWithIds.findIndex(
      (item) => item.sortableId === over.id
    );

    setItems(arrayMove(items, oldIndex, newIndex));
  };

  return (
    <section className="shelf">
      <div className="shelf-header">
        <h3>{title}</h3>
        <span>{items.length} items</span>
      </div>

      <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext
          items={itemsWithIds.map((item) => item.sortableId)}
          strategy={verticalListSortingStrategy}
        >
          <div className="tile-list">
            {itemsWithIds.map((item) => (
              <SortableItem
                key={item.sortableId}
                id={item.sortableId}
                item={item}
              />
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </section>
  );
}