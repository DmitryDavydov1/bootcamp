import {
  DndContext,
  closestCenter,
} from "@dnd-kit/core";

import {
  SortableContext,
  verticalListSortingStrategy,
  arrayMove,
} from "@dnd-kit/sortable";

import SortableItem from "./SortableItem";

export default function SortableShelf({
  title,
  items,
  setItems,
}) {
  const handleDragEnd = (event) => {
    const { active, over } = event;

    if (!over || active.id === over.id) return;

    const oldIndex = items.findIndex(
      (item) => item.title === active.id
    );

    const newIndex = items.findIndex(
      (item) => item.title === over.id
    );

    setItems(arrayMove(items, oldIndex, newIndex));
  };

  return (
    <div style={{ marginBottom: 40 }}>
      <h2>{title}</h2>

      <DndContext
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={items.map((i) => i.title)}
          strategy={verticalListSortingStrategy}
        >
          {items.map((item) => (
            <SortableItem
              key={item.title}
              item={item}
            />
          ))}
        </SortableContext>
      </DndContext>
    </div>
  );
}