<script setup lang="ts" generic="T">
import { extractClosestEdge } from '@atlaskit/pragmatic-drag-and-drop-hitbox/closest-edge'
import { getReorderDestinationIndex } from '@atlaskit/pragmatic-drag-and-drop-hitbox/util/get-reorder-destination-index'
import { announce } from '@atlaskit/pragmatic-drag-and-drop-live-region'
import { monitorForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter'
import { reorder } from '@atlaskit/pragmatic-drag-and-drop/reorder'
import { onMounted, useId } from 'vue'
import { SORTABLE_ITEM_TYPE } from '@/composables/dnd/useDraggableElement'
import CspSortableListItem from './CspSortableListItem.vue'

interface Props {
  items: T[]
  getItemKey: (item: T) => string
  getItemLabel?: (item: T) => string
  isItemDraggable?: (item: T, index: number) => boolean
  getItemVariant?: (item: T, index: number) => 'default' | 'alt'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
})

const emit = defineEmits<{
  reorder: [items: T[]]
}>()

const listId = useId()

function isDraggable(item: T, index: number) {
  if (props.disabled)
    return false
  return props.isItemDraggable?.(item, index) ?? true
}

function getVariant(item: T, index: number): 'default' | 'alt' {
  return props.getItemVariant?.(item, index) ?? 'default'
}

function getLabel(item: T): string {
  return props.getItemLabel?.(item) ?? props.getItemKey(item)
}

function moveItem(fromIndex: number, toIndex: number) {
  if (props.disabled)
    return
  if (toIndex < 0 || toIndex >= props.items.length)
    return
  if (!isDraggable(props.items[fromIndex], fromIndex))
    return

  const newItems = reorder({ list: props.items, startIndex: fromIndex, finishIndex: toIndex })
  emit('reorder', newItems)

  const item = props.items[fromIndex]
  announce(`${getLabel(item)} déplacé`)
}

function createMoveUp(index: number) {
  return () => moveItem(index, index - 1)
}

function createMoveDown(index: number) {
  return () => moveItem(index, index + 1)
}

onMounted(() => {
  return monitorForElements({
    canMonitor: ({ source }) => source.data.type === SORTABLE_ITEM_TYPE && source.data.listId === listId,
    onDrop: ({ source, location }) => {
      if (props.disabled)
        return

      const destination = location.current.dropTargets[0]
      if (!destination)
        return

      const startIndex = source.data.index
      const indexOfTarget = destination.data.index

      if (typeof startIndex !== 'number' || typeof indexOfTarget !== 'number')
        return

      const finishIndex = getReorderDestinationIndex({
        startIndex,
        indexOfTarget,
        closestEdgeOfTarget: extractClosestEdge(destination.data),
        axis: 'vertical',
      })

      if (finishIndex === startIndex)
        return

      const newItems = reorder({ list: props.items, startIndex, finishIndex })
      emit('reorder', newItems)

      const item = props.items[startIndex]
      announce(`${getLabel(item)} déplacé`)
    },
  })
})
</script>

<template>
  <ul class="csp-sortable-list">
    <CspSortableListItem
      v-for="(item, index) in items"
      :key="getItemKey(item)"
      :item="item"
      :item-id="getItemKey(item)"
      :index="index"
      :list-id="listId"
      :draggable="isDraggable(item, index)"
      :variant="getVariant(item, index)"
      :disabled="disabled"
    >
      <template #default="slotProps">
        <slot
          name="item"
          v-bind="slotProps"
          :can-move-up="isDraggable(item, index) && index > 0"
          :can-move-down="isDraggable(item, index) && index < items.length - 1"
          :move-up="createMoveUp(index)"
          :move-down="createMoveDown(index)"
        />
      </template>
    </CspSortableListItem>
  </ul>
</template>

<style scoped lang="scss">
.csp-sortable-list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
}
</style>
